"""
DAG traverser — converts the artifact graph into Verification Query Packages (VQPs).

Three VQP types:
  A  CitationVerification   — does source S actually support claim C?
  B  RequirementCoverage    — does the whitepaper adequately describe requirement R?
  C  OrphanDetection        — structural anomalies (no Gemini needed)
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from schema import Graph, Node


VQPType = Literal["citation_verification", "requirement_coverage", "orphan_detection"]


@dataclass
class VQP:
    id: str
    vqp_type: VQPType
    payload: dict  # all context needed for the verification query
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "vqp_type": self.vqp_type,
            "payload": self.payload,
            "metadata": self.metadata,
        }


def traverse(graph: Graph) -> list[VQP]:
    """Traverse the graph and emit all VQPs."""
    vqps: list[VQP] = []
    vqps.extend(_type_a_citation_vqps(graph))
    vqps.extend(_type_b_coverage_vqps(graph))
    vqps.extend(_type_c_orphan_vqps(graph))
    return vqps


# ── Type A: Citation Verification ────────────────────────────────────────────

def _type_a_citation_vqps(graph: Graph) -> list[VQP]:
    """One VQP per supported-by edge: does source actually support the claim?"""
    vqps = []
    for edge in graph.edges:
        if edge.type != "supported-by":
            continue

        claim = graph.nodes.get(edge.from_id)
        src = graph.nodes.get(edge.to_id)
        if not claim or not src:
            continue

        # Find whitepaper sections where this claim appears
        section_excerpts = []
        for ap_edge in graph.edges_from(claim.id, "appears-in"):
            sec = graph.nodes.get(ap_edge.to_id)
            if sec:
                # Truncate each section to keep query bounded
                section_excerpts.append({
                    "section_title": sec.title,
                    "text": sec.text[:2000],
                })

        vqp_id = f"A-{claim.id}-{src.id}"[:80]
        vqps.append(VQP(
            id=vqp_id,
            vqp_type="citation_verification",
            payload={
                "claim_id": claim.id,
                "claim_title": claim.title,
                "claim_text": claim.text,
                "support_type": edge.metadata.get("support_type", "unspecified"),
                "evidence_note": edge.metadata.get("evidence", ""),
                "source_id": src.id,
                "source_title": src.title,
                "source_key_content": src.text,
                "whitepaper_sections": section_excerpts,
            },
            metadata={
                "claim_status": claim.metadata.get("status", ""),
                "challenges": claim.metadata.get("challenges", ""),
            },
        ))
    return vqps


# ── Type B: Requirement Coverage ─────────────────────────────────────────────

# Keyword map: requirement ID prefix → section IDs likely to cover it
REQ_SECTION_MAP: dict[str, list[str]] = {
    "REQ-1": [  # Artifact Graph
        "SEC-concept-verification-compiler-the-artifact-graph",
        "SEC-concept-verification-compiler",
    ],
    "REQ-1-1": [  # Node Types — schema section first so evaluator sees SourceRegionNode immediately
        "SEC-source-region-addressing-sourceregionnode-schema",
        "SEC-concept-verification-compiler-the-artifact-graph",
        "SEC-concept-verification-compiler-verification-readiness-metric",
    ],
    "REQ-2": [  # Decomposition and Query
        "SEC-concept-verification-compiler-graph-traversal-as-decompositi",
        "SEC-concept-verification-compiler",
    ],
    "REQ-3": [  # Reviewer Interface
        "SEC-concept-verification-compiler-verification-query-and-result-",
        "SEC-concept-verification-compiler-dual-mode-operation",
        "SEC-concept-verification-compiler-llm-reliability-and-the-mitiga",
        "SEC-concept-verification-compiler",
        "SEC-core-concept-units-of-intelligence",
    ],
    "REQ-3-3b": [  # LLM Result Status
        "SEC-concept-verification-compiler-dual-mode-operation",
        "SEC-concept-verification-compiler-verification-query-and-result-",
        "SEC-concept-verification-compiler-llm-reliability-and-the-mitiga",
        "SEC-concept-verification-compiler",
        "SEC-deployment-contexts",
    ],
    "REQ-3-4": [  # Conflict Resolution — human precedence, discrepant result retention
        "SEC-concept-verification-compiler-dual-mode-operation",
        "SEC-concept-verification-compiler-verification-query-and-result-",
    ],
    "REQ-3-5": [  # Prompt Config Control — focused on dedicated section
        "SEC-concept-verification-compiler-prompt-configuration-control",
        "SEC-concept-verification-compiler-verification-query-and-result-",
    ],
    "REQ-4": [  # Confidence Score
        "SEC-concept-verification-compiler-verification-readiness-metric",
        "SEC-concept-verification-compiler",
    ],
    "REQ-5": [  # Auditability
        "SEC-concept-verification-compiler-evidence-auditability-and-conf",
        "SEC-concept-verification-compiler-provable-decomposition",
        "SEC-concept-verification-compiler",
        "SEC-deployment-contexts",
    ],
    "REQ-6": [  # Process Assurance
        "SEC-concept-verification-compiler-reviewer-qualification-and-ind",
        "SEC-concept-verification-compiler-automation-bias-mitigation-and",
        "SEC-concept-verification-compiler-regulatory-pathway",
        "SEC-concept-verification-compiler-llm-reliability-and-the-mitiga",
        "SEC-concept-verification-compiler",
        "SEC-deployment-contexts",
    ],
    "REQ-7": [  # Source Region Addressing
        "SEC-source-region-addressing",
        "SEC-source-region-addressing-stable-region-identifiers",
        "SEC-source-region-addressing-sourceregionnode-schema",
        "SEC-source-region-addressing-vqp-assembly-from-sourceregionnodes",
        "SEC-source-region-addressing-document-addressability-requirement",
    ],
    "REQ-8": [  # Known Architectural Challenges (all sub-requirements share parent)
        "SEC-known-architectural-challenges",
    ],
    "REQ-8-1": [  # Graph Invalidation Cascade
        "SEC-known-architectural-challenges-graph-invalidation-cascade",
        "SEC-known-architectural-challenges",
    ],
    "REQ-8-2": [  # Multi-Unit and Emergent Requirements
        "SEC-known-architectural-challenges-multi-unit-and-emergent-requi",
        "SEC-known-architectural-challenges",
    ],
    "REQ-8-3": [  # Conflict Resolution Economics
        "SEC-known-architectural-challenges-conflict-resolution-economics",
        "SEC-known-architectural-challenges",
    ],
    "REQ-8-4": [  # VQP Size Limits and Evidence Decomposition
        "SEC-known-architectural-challenges-vqp-size-limits-and-evidence-",
        "SEC-known-architectural-challenges",
    ],
    "REQ-8-5": [  # DAG Cycle Detection and Requirements Refactoring
        "SEC-known-architectural-challenges-dag-cycle-detection-and-requi",
        "SEC-concept-verification-compiler-the-artifact-graph",
        "SEC-known-architectural-challenges",
    ],
    "REQ-8-6": [  # Data and Control Coupling Coverage (DCCC)
        "SEC-known-architectural-challenges-data-and-control-coupling-cov",
        "SEC-known-architectural-challenges",
    ],
    "REQ-8-7": [  # Object Code Verification
        "SEC-known-architectural-challenges-object-code-verification",
        "SEC-known-architectural-challenges",
    ],
}


def _sections_for_req(req: Node, graph: Graph) -> list[dict]:
    """Find whitepaper sections relevant to a requirement.

    Section order follows the REQ_SECTION_MAP list order (most important first),
    so the evaluator encounters critical sections early in the combined VQP text.
    """
    # Match by req ID prefix — use longest matching prefix to avoid inheriting
    # all parent sections when a specific sub-requirement entry exists.
    matching_prefixes = [p for p in REQ_SECTION_MAP if req.id.startswith(p)]
    # Use an ordered dict to deduplicate while preserving insertion order.
    matched_ids: dict[str, None] = {}
    if matching_prefixes:
        longest = max(matching_prefixes, key=len)
        for sec_id in REQ_SECTION_MAP[longest]:
            matched_ids[sec_id] = None
        parent_prefixes = [p for p in matching_prefixes if p != longest and len(p) < len(longest)]
        if not parent_prefixes:
            # No more specific match — merge all matching prefix lists in order.
            for prefix in matching_prefixes:
                for sec_id in REQ_SECTION_MAP[prefix]:
                    matched_ids[sec_id] = None

    # Fallback: keyword overlap between req title and section title
    if not matched_ids:
        req_words = set(req.title.lower().split())
        for sec in graph.nodes_of_type("section"):
            sec_words = set(sec.title.lower().split())
            if len(req_words & sec_words) >= 2:
                matched_ids[sec.id] = None

    excerpts = []
    for sec_id in matched_ids:  # order from REQ_SECTION_MAP (most relevant first)
        sec = graph.nodes.get(sec_id)
        if sec:
            excerpts.append({
                "section_title": sec.title,
                "text": sec.text,  # builder already caps H3 at 4000, H2 at 6000
            })
    return excerpts


def _type_b_coverage_vqps(graph: Graph) -> list[VQP]:
    """One VQP per sub-requirement: is it adequately described in the whitepaper?"""
    vqps = []
    for req in graph.nodes_of_type("requirement"):
        if req.metadata.get("level") != "sub":
            continue  # skip parent grouping nodes

        sections = _sections_for_req(req, graph)
        vqps.append(VQP(
            id=f"B-{req.id}",
            vqp_type="requirement_coverage",
            payload={
                "requirement_id": req.id,
                "requirement_title": req.title,
                "requirement_text": req.text,
                "req_num": req.metadata.get("req_num", ""),
                "candidate_sections": sections,
            },
        ))
    return vqps


# ── Type C: Orphan Detection ──────────────────────────────────────────────────

def _type_c_orphan_vqps(graph: Graph) -> list[VQP]:
    """Structural anomalies — no Gemini needed, just graph inspection."""
    findings = []

    # Claims with no supported-by source
    for claim in graph.nodes_of_type("claim"):
        if not graph.edges_from(claim.id, "supported-by"):
            findings.append({
                "anomaly": "unsupported_claim",
                "node_id": claim.id,
                "node_title": claim.title,
                "detail": "Claim has no supporting source in the matrix.",
            })

    # Requirements with no candidate sections
    for req in graph.nodes_of_type("requirement"):
        if req.metadata.get("level") != "sub":
            continue
        sections = _sections_for_req(req, graph)
        if not sections:
            findings.append({
                "anomaly": "uncovered_requirement",
                "node_id": req.id,
                "node_title": req.title,
                "detail": "No whitepaper section mapped to this requirement.",
            })

    # Sources cited in matrix but no SRC node (would be a parsing failure)
    claimed_src_ids = set(
        e.to_id for e in graph.edges if e.type == "supported-by"
    )
    for src_id in claimed_src_ids:
        if src_id not in graph.nodes:
            findings.append({
                "anomaly": "missing_source_node",
                "node_id": src_id,
                "node_title": src_id,
                "detail": "Source referenced in matrix but no SRC node found in graph.",
            })

    return [
        VQP(
            id="C-orphan-detection",
            vqp_type="orphan_detection",
            payload={"findings": findings},
        )
    ]


# ── Save / load ───────────────────────────────────────────────────────────────

def save_vqps(vqps: list[VQP], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps([v.to_dict() for v in vqps], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from schema import Graph

    graph_path = Path(__file__).parents[1] / "data" / "graph.json"
    out_path = Path(__file__).parents[1] / "data" / "vqps.json"

    g = Graph.load(graph_path)
    vqps = traverse(g)

    counts: dict[str, int] = {}
    for v in vqps:
        counts[v.vqp_type] = counts.get(v.vqp_type, 0) + 1
    print("VQP counts:", counts)
    print(f"Total: {len(vqps)}")

    save_vqps(vqps, out_path)
    print(f"Saved → {out_path}")
