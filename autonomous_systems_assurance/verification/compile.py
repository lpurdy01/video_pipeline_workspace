#!/usr/bin/env python3
"""Deterministic research graph, review queue and conservative change impact."""
from __future__ import annotations

import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import re
import sys

TASKS = ("source_support", "challenge", "cross_artifact", "human_disposition")
CONTRACT = "assurance-review-v1"
CLAIM_TAG = re.compile(r"\[(C-[A-Z0-9]+(?:-[A-Z0-9]+)*)\]")
MAX_PACKAGE_BYTES = 120_000
CASE_FILENAME = "assurance/assurance_case.json"
CROSSWALK_FILENAME = "assurance/method_crosswalk.json"


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":")).encode()).hexdigest()


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def local_path(root, name):
    path = (root / name).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f"Path escapes project: {name}")
    return path


def read_json(path, tracked=None):
    raw = path.read_bytes()
    if tracked is not None:
        tracked[str(path)] = hashlib.sha256(raw).hexdigest()
    return json.loads(raw)


def indexed(rows, label):
    result = {}
    for row in rows:
        key = row.get("id")
        if not isinstance(key, str) or not key:
            raise ValueError(f"Missing ID in {label}")
        if key in result:
            raise ValueError(f"Duplicate ID {key} in {label}")
        result[key] = row
    return result


def load_records(root, seed, filename, key, tracked):
    paths = [root / seed, *sorted((root / "research/contributions").glob(f"*/{filename}"))]
    rows = []
    for path in paths:
        data = read_json(path, tracked)
        if data.get("schema_version") != 1 or not isinstance(data.get(key), list):
            raise ValueError(f"Invalid schema in {path}")
        rows.extend(data[key])
    return indexed(rows, key), paths


def ids(value, label):
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise ValueError(f"{label} must be a nonempty-ID list")
    return value


def load_assurance_case(root, tracked):
    """Load the optional worked-case graph without making examples safety evidence."""
    path = root / CASE_FILENAME
    if not path.exists():
        return None
    case = read_json(path, tracked)
    if case.get("schema_version") != 1:
        raise ValueError("Unsupported assurance-case schema")
    required = ("system_releases", "assumptions", "hazards", "evidence_artifacts", "obligations")
    if any(not isinstance(case.get(key), list) for key in required):
        raise ValueError("Assurance case missing a node collection")
    if "risk_contexts" in case and not isinstance(case["risk_contexts"], list):
        raise ValueError("Assurance case risk_contexts must be a list")
    return case


def load_method_crosswalk(root, tracked):
    path = root / CROSSWALK_FILENAME
    if not path.exists():
        return None
    crosswalk = read_json(path, tracked)
    if crosswalk.get("schema_version") != 1 or not isinstance(crosswalk.get("methods"), list):
        raise ValueError("Unsupported method-crosswalk schema")
    return crosswalk


def check_review(record):
    required = ("id", "package_id", "input_digest", "task", "reviewer_id",
                "reviewer_kind", "verdict", "created_at", "rationale",
                "evidence_locators", "limitations", "resolves")
    for field in required:
        if field not in record:
            raise ValueError(f"Review missing {field}")
    if not re.fullmatch(r"R-[A-Za-z0-9_-]+", record["id"]):
        raise ValueError("Review ID must begin R- and contain only letters/numbers/_/-")
    if record["task"] not in TASKS or record["verdict"] not in ("pass", "fail", "uncertain"):
        raise ValueError(f"Invalid task/verdict in {record['id']}")
    if record["reviewer_kind"] not in ("model", "human"):
        raise ValueError("Unknown reviewer kind")
    if record["task"] == "human_disposition" and record["reviewer_kind"] != "human":
        raise ValueError("Human disposition requires a human reviewer")
    for key in ("reviewer_id", "rationale", "package_id", "input_digest"):
        if not isinstance(record[key], str) or not record[key].strip():
            raise ValueError(f"Review requires nonempty {key}")
    if not re.fullmatch(r"[a-f0-9]{64}", record["input_digest"]):
        raise ValueError("Invalid review digest")
    date.fromisoformat(record["created_at"][:10])
    for key in ("evidence_locators", "limitations", "resolves"):
        if not isinstance(record[key], list):
            raise ValueError(f"Review {key} must be a list")
    if not record["evidence_locators"]:
        raise ValueError("Review needs evidence locators")
    if record["reviewer_kind"] == "model":
        if not record.get("model_id") or not record.get("prompt_version"):
            raise ValueError("Model review requires model_id and prompt_version")


def impact(current, previous):
    old = previous.get("nodes", {})
    changed = sorted(k for k in set(current) | set(old)
                     if current.get(k, {}).get("hash") != old.get(k, {}).get("hash"))
    reverse = {}
    for graph in (old, current):
        for key, node in graph.items():
            for dependency in node["dependencies"]:
                reverse.setdefault(dependency, set()).add(key)
    affected = set(changed)
    queue = list(changed)
    while queue:
        for key in reverse.get(queue.pop(), ()):
            if key not in affected:
                affected.add(key)
                queue.append(key)
    return {"changed": changed, "affected": sorted(affected)}


def validate_reviews(reviews):
    for record in reviews.values():
        check_review(record)
        if record["resolves"] and record["task"] != "human_disposition":
            raise ValueError("Only human disposition may resolve prior objections")
        for rid in record["resolves"]:
            other = reviews.get(rid)
            if not other or other["verdict"] == "pass" or other["id"] == record["id"]:
                raise ValueError(f"Invalid resolution reference {rid}")
            claim_prefix = record["package_id"].removesuffix("-human_disposition")
            if other["package_id"] not in {f"{claim_prefix}-{task}" for task in TASKS}:
                raise ValueError(f"Resolution references another claim: {rid}")
            if other["created_at"] > record["created_at"]:
                raise ValueError(f"Resolution predates objection: {rid}")


def compile_project(root, today=None, baseline=None):
    root = root.resolve()
    today = today or date.today()
    initial_hashes = {}
    sources, source_paths = load_records(root, "research/sources.json", "sources.json", "sources", initial_hashes)
    claims, claim_paths = load_records(root, "verification/claims.json", "claims.json", "claims", initial_hashes)
    assurance_case = load_assurance_case(root, initial_hashes)
    method_crosswalk = load_method_crosswalk(root, initial_hashes)
    manifest_path = root / "verification/artifacts.json"
    manifest = read_json(manifest_path, initial_hashes)
    if manifest.get("schema_version") != 1:
        raise ValueError("Unsupported artifact schema")
    artifacts = indexed(manifest["artifacts"], "artifacts")
    if not sources or not claims or not artifacts:
        raise ValueError("Sources, claims and manifested artifacts must all be nonempty")
    nodes, regions, source_blockers = {}, {}, {}

    def add(key, kind, payload, dependencies=()):
        if key in nodes:
            raise ValueError(f"Duplicate graph ID: {key}")
        nodes[key] = {"kind": kind, "hash": digest(payload), "dependencies": sorted(set(dependencies))}

    for sid, source in sorted(sources.items()):
        for field in ("title", "url", "source_type", "jurisdiction", "accessed_at",
                      "inspection_scope", "limitations", "independence_group", "refresh_days", "regions"):
            if field not in source:
                raise ValueError(f"{sid} missing {field}")
        accessed = date.fromisoformat(source["accessed_at"])
        if accessed > today:
            raise ValueError(f"Future access date on {sid}")
        if not isinstance(source["refresh_days"], int) or source["refresh_days"] <= 0:
            raise ValueError(f"Invalid refresh interval on {sid}")
        blockers = []
        if (today - accessed).days > source["refresh_days"]:
            blockers.append(f"{sid}: source needs freshness review")
        add(sid, "source", source)
        for region in source["regions"]:
            rid = region["id"]
            if rid in regions:
                raise ValueError(f"Duplicate region ID {rid}")
            if not region.get("locator") or not region.get("excerpt"):
                raise ValueError(f"Missing locator/excerpt for {rid}")
            context = None
            snapshot = region.get("snapshot_path")
            context_path = region.get("context_path")
            if snapshot:
                path = local_path(root, snapshot)
                actual = file_hash(path)
                initial_hashes[str(path)] = actual
                if actual != region.get("snapshot_sha256"):
                    raise ValueError(f"Source snapshot hash mismatch: {rid}")
            if context_path:
                path = local_path(root, context_path)
                raw = path.read_bytes()
                context = raw.decode("utf-8")
                initial_hashes[str(path)] = hashlib.sha256(raw).hexdigest()
            if not (snapshot and context and region.get("context_status") == "full_context"):
                blockers.append(f"{rid}: original snapshot/full source context missing")
            regions[rid] = {"source_id": sid, "source": source,
                            "region": region, "context": context}
            add(rid, "source_region", regions[rid], [sid])
        source_blockers[sid] = blockers

    for cid, claim in sorted(claims.items()):
        if not re.fullmatch(r"C-[A-Z0-9]+(?:-[A-Z0-9]+)*", cid):
            raise ValueError(f"Invalid claim ID {cid}")
        for field in ("text", "kind", "status", "scope", "evidence", "challenge"):
            if field not in claim:
                raise ValueError(f"{cid} missing {field}")
        if claim["kind"] not in ("fact", "inference", "proposal"):
            raise ValueError(f"Invalid claim kind {cid}")
        for field in ("text", "scope", "challenge"):
            if not isinstance(claim[field], str) or not claim[field].strip():
                raise ValueError(f"Empty {field} on {cid}")
        deps = []
        for edge in claim["evidence"]:
            if edge["region_id"] not in regions:
                raise ValueError(f"Unknown region {edge['region_id']} in {cid}")
            if edge["relation"] not in ("supports", "contradicts", "background", "reasoning_basis"):
                raise ValueError(f"Unknown evidence relation on {cid}")
            deps.append(edge["region_id"])
        add(cid, "claim", claim, deps)

    case_links = {cid: [] for cid in claims}
    method_links = {cid: [] for cid in claims}
    worked_claim_ids = set()
    case_counts = {"system_releases": 0, "assumptions": 0, "hazards": 0,
                   "evidence_artifacts": 0, "risk_contexts": 0, "obligations": 0,
                   "external_methods": 0}
    case_blockers = []
    if assurance_case is not None:
        releases = indexed(assurance_case["system_releases"], "system_releases")
        assumptions = indexed(assurance_case["assumptions"], "assumptions")
        hazards = indexed(assurance_case["hazards"], "hazards")
        evidence_artifacts = indexed(assurance_case["evidence_artifacts"], "evidence_artifacts")
        risk_contexts = indexed(assurance_case.get("risk_contexts", []), "risk_contexts")
        obligations = indexed(assurance_case["obligations"], "obligations")
        case_counts = {"system_releases": len(releases), "assumptions": len(assumptions),
                       "hazards": len(hazards), "evidence_artifacts": len(evidence_artifacts),
                       "risk_contexts": len(risk_contexts), "obligations": len(obligations),
                       "external_methods": 0}

        for rid, release in sorted(releases.items()):
            for field in ("label", "release_version", "learning_mode", "release_status"):
                if not isinstance(release.get(field), str) or not release[field].strip():
                    raise ValueError(f"{rid} missing {field}")
            if not re.fullmatch(r"REL-[A-Z0-9]+(?:-[A-Z0-9]+)*", rid):
                raise ValueError(f"Invalid system release ID {rid}")
            if release["learning_mode"] != "frozen_trained":
                case_blockers.append(f"{rid}: worked case is limited to frozen_trained releases")
            if release["release_status"] not in ("defined", "released", "retired"):
                raise ValueError(f"Invalid release status on {rid}")
            if release["release_status"] != "released":
                case_blockers.append(f"{rid}: system release is not an evidence-backed released configuration")
            add(rid, "system_release", release)

        for aid, assumption in sorted(assumptions.items()):
            for field in ("text", "status", "release_ids"):
                if field not in assumption:
                    raise ValueError(f"{aid} missing {field}")
            if not re.fullmatch(r"AS-[A-Z0-9]+(?:-[A-Z0-9]+)*", aid):
                raise ValueError(f"Invalid assumption ID {aid}")
            release_ids = ids(assumption["release_ids"], f"{aid}.release_ids")
            if set(release_ids) - releases.keys():
                raise ValueError(f"Unknown release on {aid}")
            if assumption["status"] not in ("open", "supported", "invalidated"):
                raise ValueError(f"Invalid assumption status on {aid}")
            if assumption["status"] != "supported":
                case_blockers.append(f"{aid}: assumption is {assumption['status']}")
            add(aid, "assumption", assumption, release_ids)

        for hid, hazard in sorted(hazards.items()):
            for field in ("title", "release_id", "assumption_ids", "obligation_ids"):
                if field not in hazard:
                    raise ValueError(f"{hid} missing {field}")
            if not re.fullmatch(r"H-[A-Z0-9]+(?:-[A-Z0-9]+)*", hid):
                raise ValueError(f"Invalid hazard ID {hid}")
            if hazard["release_id"] not in releases:
                raise ValueError(f"Unknown release on {hid}")
            assumption_ids = ids(hazard["assumption_ids"], f"{hid}.assumption_ids")
            obligation_ids = ids(hazard["obligation_ids"], f"{hid}.obligation_ids")
            if set(assumption_ids) - assumptions.keys():
                raise ValueError(f"Unknown assumption on {hid}")
            if set(obligation_ids) - obligations.keys():
                raise ValueError(f"Unknown obligation on {hid}")
            add(hid, "hazard", hazard, [hazard["release_id"], *assumption_ids])

        for eid, evidence_artifact in sorted(evidence_artifacts.items()):
            for field in ("title", "kind", "status", "release_id", "claim_ids"):
                if field not in evidence_artifact:
                    raise ValueError(f"{eid} missing {field}")
            if not re.fullmatch(r"EA-[A-Z0-9]+(?:-[A-Z0-9]+)*", eid):
                raise ValueError(f"Invalid evidence artifact ID {eid}")
            if evidence_artifact["release_id"] not in releases:
                raise ValueError(f"Unknown release on {eid}")
            claim_ids = ids(evidence_artifact["claim_ids"], f"{eid}.claim_ids")
            if set(claim_ids) - claims.keys():
                raise ValueError(f"Unknown claim on {eid}")
            if evidence_artifact["status"] not in ("missing", "planned", "available", "verified"):
                raise ValueError(f"Invalid evidence-artifact status on {eid}")
            if evidence_artifact["status"] != "verified":
                case_blockers.append(f"{eid}: evidence artifact is {evidence_artifact['status']}")
            add(eid, "evidence_artifact", evidence_artifact, [evidence_artifact["release_id"]])
            for cid in claim_ids:
                case_links[cid].append({"node_id": eid, "role": "evidence_artifact"})
                worked_claim_ids.add(cid)

        for rcid, risk_context in sorted(risk_contexts.items()):
            for field in ("title", "release_id", "hazard_id", "status", "assumption_ids",
                          "evidence_artifact_ids", "claim_ids", "risk_statement", "metric_limit"):
                if field not in risk_context:
                    raise ValueError(f"{rcid} missing {field}")
            if not re.fullmatch(r"RC-[A-Z0-9]+(?:-[A-Z0-9]+)*", rcid):
                raise ValueError(f"Invalid risk-context ID {rcid}")
            if risk_context["release_id"] not in releases or risk_context["hazard_id"] not in hazards:
                raise ValueError(f"Unknown release/hazard on {rcid}")
            if hazards[risk_context["hazard_id"]]["release_id"] != risk_context["release_id"]:
                raise ValueError(f"Risk context release/hazard mismatch on {rcid}")
            assumption_ids = ids(risk_context["assumption_ids"], f"{rcid}.assumption_ids")
            artifact_ids = ids(risk_context["evidence_artifact_ids"], f"{rcid}.evidence_artifact_ids")
            claim_ids = ids(risk_context["claim_ids"], f"{rcid}.claim_ids")
            if set(assumption_ids) - assumptions.keys() or set(artifact_ids) - evidence_artifacts.keys():
                raise ValueError(f"Unknown assumption/evidence artifact on {rcid}")
            if set(claim_ids) - claims.keys():
                raise ValueError(f"Unknown claim on {rcid}")
            if risk_context["status"] not in ("open", "scoped", "supported"):
                raise ValueError(f"Invalid risk-context status on {rcid}")
            if risk_context["status"] != "supported":
                case_blockers.append(f"{rcid}: risk context is {risk_context['status']}")
            add(rcid, "risk_context", risk_context,
                [risk_context["release_id"], risk_context["hazard_id"], *assumption_ids, *artifact_ids, *claim_ids])
            for cid in claim_ids:
                case_links[cid].append({"node_id": rcid, "role": "risk_context"})
                worked_claim_ids.add(cid)

        for oid, obligation in sorted(obligations.items()):
            for field in ("title", "description", "status", "hazard_ids", "assumption_ids",
                          "evidence_artifact_ids", "claim_ids"):
                if field not in obligation:
                    raise ValueError(f"{oid} missing {field}")
            if not re.fullmatch(r"O-[A-Z0-9]+(?:-[A-Z0-9]+)*", oid):
                raise ValueError(f"Invalid obligation ID {oid}")
            hazard_ids = ids(obligation["hazard_ids"], f"{oid}.hazard_ids")
            assumption_ids = ids(obligation["assumption_ids"], f"{oid}.assumption_ids")
            artifact_ids = ids(obligation["evidence_artifact_ids"], f"{oid}.evidence_artifact_ids")
            claim_ids = ids(obligation["claim_ids"], f"{oid}.claim_ids")
            if set(hazard_ids) - hazards.keys() or set(assumption_ids) - assumptions.keys():
                raise ValueError(f"Unknown hazard/assumption on {oid}")
            if set(artifact_ids) - evidence_artifacts.keys() or set(claim_ids) - claims.keys():
                raise ValueError(f"Unknown evidence artifact/claim on {oid}")
            if obligation["status"] not in ("open", "in_progress", "closed"):
                raise ValueError(f"Invalid obligation status on {oid}")
            if obligation["status"] != "closed":
                case_blockers.append(f"{oid}: obligation remains {obligation['status']}")
            add(oid, "obligation", obligation, [*hazard_ids, *assumption_ids, *artifact_ids, *claim_ids])
            for cid in claim_ids:
                case_links[cid].append({"node_id": oid, "role": "obligation"})
                worked_claim_ids.add(cid)

        if method_crosswalk is not None:
            methods = indexed(method_crosswalk["methods"], "external_methods")
            case_counts["external_methods"] = len(methods)
            for mid, method in sorted(methods.items()):
                for field in ("title", "status", "scope", "claim_ids", "mappings"):
                    if field not in method:
                        raise ValueError(f"{mid} missing {field}")
                if not re.fullmatch(r"M-[A-Z0-9]+(?:-[A-Z0-9]+)*", mid):
                    raise ValueError(f"Invalid external method ID {mid}")
                if method["status"] not in ("guidance", "current_authority_guidance", "proposed_guidance",
                                            "consensus_standard", "research_method"):
                    raise ValueError(f"Invalid external-method status on {mid}")
                method_claims = ids(method["claim_ids"], f"{mid}.claim_ids")
                if set(method_claims) - claims.keys():
                    raise ValueError(f"Unknown claim on {mid}")
                if not isinstance(method["mappings"], list) or not method["mappings"]:
                    raise ValueError(f"{mid}.mappings must be a nonempty list")
                add(mid, "external_method", method, method_claims)
                for cid in method_claims:
                    method_links[cid].append({"node_id": mid, "role": "external_method"})
                for mapping in method["mappings"]:
                    for field in ("obligation_id", "coverage", "note", "claim_ids"):
                        if field not in mapping:
                            raise ValueError(f"{mid} mapping missing {field}")
                    if mapping["obligation_id"] not in obligations:
                        raise ValueError(f"Unknown obligation on {mid} mapping")
                    if mapping["coverage"] not in ("direct", "partial", "outside_scope", "proposed"):
                        raise ValueError(f"Invalid mapping coverage on {mid}")
                    mapping_claims = ids(mapping["claim_ids"], f"{mid}.mapping.claim_ids")
                    if set(mapping_claims) - claims.keys():
                        raise ValueError(f"Unknown claim on {mid} mapping")
                    mapping_id = f"MAP-{mid.removeprefix('M-')}-{mapping['obligation_id'].removeprefix('O-')}"
                    add(mapping_id, "method_obligation_mapping", mapping,
                        [mid, mapping["obligation_id"], *mapping_claims])
                    for cid in mapping_claims:
                        method_links[cid].append({"node_id": mapping_id, "role": "method_mapping"})
    elif method_crosswalk is not None:
        raise ValueError("Method crosswalk requires an assurance case")

    uses = {cid: [] for cid in claims}
    for aid, artifact in sorted(artifacts.items()):
        path = local_path(root, artifact["path"])
        raw = path.read_bytes()
        content = raw.decode("utf-8")
        initial_hashes[str(path)] = hashlib.sha256(raw).hexdigest()
        declared = artifact.get("claim_ids", [])
        if not isinstance(declared, list) or not all(isinstance(cid, str) for cid in declared):
            raise ValueError(f"Invalid explicit claim IDs in {artifact['path']}")
        tags = sorted(set(CLAIM_TAG.findall(content)) | set(declared))
        unknown = set(tags) - claims.keys()
        if unknown:
            raise ValueError(f"Unknown claim tags in {artifact['path']}: {sorted(unknown)}")
        dependencies = artifact.get("depends_on", [])
        if set(dependencies) - artifacts.keys():
            raise ValueError(f"Unknown artifact dependencies for {aid}")
        add(aid, artifact["kind"], {"manifest": artifact, "content": content}, tags + dependencies)
        for cid in tags:
            uses[cid].append({"artifact_id": aid, "path": artifact["path"], "text": content})

    visiting, visited = set(), set()

    def visit(key):
        if key in visiting:
            raise ValueError(f"Dependency cycle at {key}")
        if key in visited:
            return
        visiting.add(key)
        for dep in nodes[key]["dependencies"]:
            if dep not in nodes:
                raise ValueError(f"Dangling dependency {dep}")
            visit(dep)
        visiting.remove(key)
        visited.add(key)

    for key in list(nodes):
        visit(key)

    review_paths = sorted((root / "verification/reviews").glob("*.json"))
    reviews = indexed([read_json(p, initial_hashes) for p in review_paths], "reviews")
    validate_reviews(reviews)
    packages, queue, blockers = [], [], []
    for aid, artifact in artifacts.items():
        if not any(u["artifact_id"] == aid for claim_uses in uses.values() for u in claim_uses):
            blockers.append(f"{aid}: artifact has no explicit claim tags; coverage cannot be assumed")
    compiler_hash = file_hash(Path(__file__))
    for cid, claim in sorted(claims.items()):
        claim_blockers = []
        evidence = [dict(regions[e["region_id"]], relation=e["relation"]) for e in claim["evidence"]]
        if not evidence:
            claim_blockers.append(f"{cid}: no evidence or background linked")
        if claim["kind"] == "fact" and not any(e["relation"] == "supports" for e in claim["evidence"]):
            claim_blockers.append(f"{cid}: factual claim has no support edge")
        for item in evidence:
            claim_blockers.extend(source_blockers[item["source_id"]])
        if not uses[cid]:
            claim_blockers.append(f"{cid}: no manifested artifact use; integrate or retire explicitly")
        if claim["status"] in ("retired", "rejected"):
            claim_blockers.append(f"{cid}: retired/rejected claim remains in active registry")
        dependencies = set()

        def collect(key):
            if key in dependencies:
                return
            dependencies.add(key)
            for dep in nodes[key]["dependencies"]:
                collect(dep)

        for use in uses[cid]:
            collect(use["artifact_id"])
        claim_case_links = sorted(case_links[cid], key=lambda link: (link["node_id"], link["role"]))
        claim_method_links = sorted(method_links[cid], key=lambda link: (link["node_id"], link["role"]))
        base = {"contract": CONTRACT, "compiler_sha256": compiler_hash,
                "claim": claim, "evidence": evidence, "artifact_uses": uses[cid],
                "assurance_case_links": claim_case_links,
                "method_crosswalk_links": claim_method_links,
                "dependency_hashes": {key: nodes[key]["hash"] for key in sorted(dependencies)},
                "assurance_case_hashes": {link["node_id"]: nodes[link["node_id"]]["hash"]
                                          for link in claim_case_links},
                "method_crosswalk_hashes": {link["node_id"]: nodes[link["node_id"]]["hash"]
                                             for link in claim_method_links}}
        claim_pids = {f"P-{cid}-{task}" for task in TASKS}
        historical_issues = sorted([r for r in reviews.values()
                                   if r["package_id"] in claim_pids and r["verdict"] != "pass"],
                                  key=lambda r: r["id"])
        current_reviews = []
        claim_packages = []
        for task in TASKS:
            payload = dict(base, task=task)
            if task == "human_disposition":
                payload["review_results"] = sorted(current_reviews, key=lambda r: r["id"])
                payload["historical_issues"] = historical_issues
            pid = f"P-{cid}-{task}"
            packet = {"id": pid, "input_digest": digest(payload), **payload}
            if len(json.dumps(packet).encode()) > MAX_PACKAGE_BYTES:
                claim_blockers.append(f"{pid}: package exceeds {MAX_PACKAGE_BYTES} bytes; split explicit source regions/artifacts")
            matches = [r for r in reviews.values() if r["package_id"] == pid
                       and r["input_digest"] == packet["input_digest"] and r["task"] == task]
            current_reviews.extend(matches)
            passed = any(r["verdict"] == "pass" for r in matches)
            if not passed:
                claim_blockers.append(f"{pid}: missing current passing {task} review")
            queue.append({"package_id": pid, "claim_id": cid, "task": task,
                          "input_digest": packet["input_digest"],
                          "status": "review_recorded" if passed else "needs_review",
                          "review_ids": [r["id"] for r in matches]})
            claim_packages.append(packet)
        dispositions = [r for r in current_reviews if r["task"] == "human_disposition" and r["verdict"] == "pass"]
        resolved = {rid for r in dispositions for rid in r["resolves"]}
        for review in historical_issues:
            if review["verdict"] != "pass" and review["id"] not in resolved:
                claim_blockers.append(f"{cid}: unresolved {review['verdict']} review {review['id']}")
        blockers.extend(claim_blockers)
        for packet in claim_packages:
            packet["blockers"] = sorted(set(claim_blockers))
            packages.append(packet)
            # Review-package graph edges include every actual input, not just the claim.
            add(packet["id"], "review_package", {"input_digest": packet["input_digest"]},
                [cid] + [u["artifact_id"] for u in uses[cid]] + [link["node_id"] for link in claim_case_links]
                + [link["node_id"] for link in claim_method_links])

    active_digests = {(p["id"], p["input_digest"]) for p in packages}
    stale = sorted(r["id"] for r in reviews.values()
                   if (r["package_id"], r["input_digest"]) not in active_digests)
    for filename, original in (("sources.json", source_paths[1:]), ("claims.json", claim_paths[1:])):
        if sorted((root / "research/contributions").glob(f"*/{filename}")) != original:
            raise ValueError("Contribution inventory changed during compilation; freeze inputs and retry")
    if sorted((root / "verification/reviews").glob("*.json")) != review_paths:
        raise ValueError("Review inventory changed during compilation; retry")
    for path, before in initial_hashes.items():
        if file_hash(Path(path)) != before:
            raise ValueError(f"Input changed during compilation: {path}; freeze integration inputs and retry")
    snapshot = {"schema_version": 1, "as_of": today.isoformat(), "nodes": nodes}
    changes = impact(nodes, baseline) if baseline is not None else None
    worked_queue = [item for item in queue if item["claim_id"] in worked_claim_ids]
    automated_queue = [item for item in worked_queue if item["task"] != "human_disposition"]
    human_queue = [item for item in worked_queue if item["task"] == "human_disposition"]

    def percent(passed, total):
        return round(100 * passed / total, 1) if total else None

    verification_scores = {
        "label": "verification gate-completion coverage; not a safety probability or safety score",
        "worked_case_claims": len(worked_claim_ids),
        "worked_case_packages": len(worked_queue),
        "worked_case_passing_packages": sum(item["status"] == "review_recorded" for item in worked_queue),
        "worked_case_verification_coverage_percent": percent(
            sum(item["status"] == "review_recorded" for item in worked_queue), len(worked_queue)),
        "automated_review_coverage_percent": percent(
            sum(item["status"] == "review_recorded" for item in automated_queue), len(automated_queue)),
        "human_disposition_coverage_percent": percent(
            sum(item["status"] == "review_recorded" for item in human_queue), len(human_queue)),
    }
    return {"snapshot": snapshot, "packages": packages, "queue": queue,
            "blockers": sorted(set(blockers)), "stale_review_ids": stale,
            "changes": changes, "counts": {"sources": len(sources), "claims": len(claims),
            "artifacts": len(artifacts), "planned_reviews": len(packages),
            "current_passing_packages": sum(q["status"] == "review_recorded" for q in queue),
            "review_records": len(reviews), **case_counts}, "assurance_case_blockers": sorted(set(case_blockers)),
            "verification_scores": verification_scores}


def write_outputs(root, result):
    out = root / "verification/out"
    out.mkdir(parents=True, exist_ok=True)
    for name, value in (("snapshot.json", result["snapshot"]), ("graph.json", result["snapshot"]),
                        ("review_packages.json", result["packages"]), ("review_queue.json", result["queue"])):
        (out / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")
    case_blocked = bool(result["assurance_case_blockers"])
    lines = ["# Research composition verification", "", f"As of {result['snapshot']['as_of']}", "",
             "Structural compilation: PASS. This does not establish factual correctness.",
             "Composition release: " + ("BLOCKED" if result["blockers"] or case_blocked else "REVIEW GATES SATISFIED"), "",
             "This is not the final media/publication gate.", "", "## Counts", ""]
    lines.extend(f"- {k}: {v}" for k, v in result["counts"].items())
    lines += ["", "## Verification coverage", "", result["verification_scores"]["label"]]
    lines.extend(f"- {k}: {v}" for k, v in result["verification_scores"].items() if k != "label")
    lines += ["", "## Assurance-case blockers", ""] + [f"- {b}" for b in result["assurance_case_blockers"]]
    lines += ["", "## Blockers", ""] + [f"- {b}" for b in result["blockers"]]
    lines += ["", "## Stale review records", "", ", ".join(result["stale_review_ids"]) or "None."]
    lines += ["", "## Change impact", ""]
    lines.append(json.dumps(result["changes"], indent=2) if result["changes"] is not None else "No baseline supplied.")
    (out / "report.md").write_text("\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--release", action="store_true")
    parser.add_argument("--import-review", type=Path)
    args = parser.parse_args()
    try:
        if args.import_review:
            record = read_json(args.import_review)
            check_review(record)
            current = compile_project(args.root)
            if not any(p["id"] == record["package_id"] and p["input_digest"] == record["input_digest"]
                       and p["task"] == record["task"] for p in current["packages"]):
                raise ValueError("Review does not match a current package")
            existing = [read_json(p) for p in sorted((args.root / "verification/reviews").glob("*.json"))]
            validate_reviews(indexed(existing + [record], "reviews"))
            destination = args.root / "verification/reviews" / (record["id"] + ".json")
            destination.parent.mkdir(parents=True, exist_ok=True)
            with destination.open("x", encoding="utf-8") as handle:
                handle.write(json.dumps(record, indent=2) + "\n")
        result = compile_project(args.root, baseline=read_json(args.baseline) if args.baseline else None)
        write_outputs(args.root, result)
        all_blockers = result["blockers"] + result["assurance_case_blockers"]
        print(json.dumps({"structural_compile": "pass", "composition_release_ready": not all_blockers,
                          "blockers": len(all_blockers), **result["counts"],
                          "verification_scores": result["verification_scores"]}, indent=2))
        return 2 if args.release and all_blockers else 0
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(f"Compilation failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
