#!/usr/bin/env python3
"""Write a concise first-pass verification report and human-review queue."""
from __future__ import annotations

import importlib.util
from collections import Counter
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
OUT = PROJECT / "verification/out"

SPEC = importlib.util.spec_from_file_location("assurance_compiler", PROJECT / "verification/compile.py")
compiler = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(compiler)


def main() -> None:
    result = compiler.compile_project(PROJECT)
    scores = result["verification_scores"]
    worked_ids = {packet["claim"]["id"] for packet in result["packages"] if packet["assurance_case_links"]}
    reviews = {}
    for path in sorted((PROJECT / "verification/reviews").glob("*.json")):
        record = compiler.read_json(path)
        reviews.setdefault(record["package_id"], []).append(record)

    human = [packet for packet in result["packages"]
             if packet["claim"]["id"] in worked_ids and packet["task"] == "human_disposition"]
    source_uncertain = []
    current_nonpasses = []
    for packet in result["packages"]:
        if packet["claim"]["id"] not in worked_ids or packet["task"] != "source_support":
            continue
        for record in reviews.get(packet["id"], []):
            if record["input_digest"] == packet["input_digest"] and record["verdict"] != "pass":
                source_uncertain.append((packet["claim"]["id"], record))

    current_model_records = [
        record for packet in result["packages"] if packet["task"] != "human_disposition"
        for record in reviews.get(packet["id"], [])
        if record["input_digest"] == packet["input_digest"] and record["reviewer_kind"] == "model"
    ]
    verdicts = Counter(record["verdict"] for record in current_model_records)
    for packet in result["packages"]:
        if packet["task"] == "human_disposition":
            continue
        for record in reviews.get(packet["id"], []):
            if (record["input_digest"] == packet["input_digest"]
                    and record["reviewer_kind"] == "model" and record["verdict"] != "pass"):
                current_nonpasses.append((packet["claim"]["id"], packet["task"], record))
    active_pairs = {(packet["id"], packet["input_digest"]) for packet in result["packages"]}
    historical_nonpasses = [record for records in reviews.values() for record in records
                            if record["verdict"] != "pass"
                            and (record["package_id"], record["input_digest"]) not in active_pairs]
    lines = [
        "# First-pass worked-case verification report", "",
        f"As of {result['snapshot']['as_of']}. This is a verification-gate report for a hypothetical worked case, not a safety assessment or authorization.",
        "", "## Coverage score", "",
        f"- Worked-case verification coverage: **{scores['worked_case_verification_coverage_percent']}%** ({scores['worked_case_passing_packages']} passing gates of {scores['worked_case_packages']}).",
        f"- Automated-review coverage: **{scores['automated_review_coverage_percent']}%**.",
        f"- Human-disposition coverage: **{scores['human_disposition_coverage_percent']}%**.",
        "- The pre-human automated-review target is met only when source support, challenge and cross-artifact packages all have a current model pass. It does not resolve any recorded model objection.",
        "- The score measures current review-gate completion only. It is not a probability of safety, a model-confidence score, or certification evidence.",
        "", "## First-pass result", "",
        f"- Current model review records: {sum(verdicts.values())} ({verdicts['pass']} pass, {verdicts['uncertain']} uncertain, {verdicts['fail']} fail).",
        f"- Historical review records retained but stale after a manifest change: {len(result.get('stale_review_ids', []))}. They are evidence of prior review activity, not current passing gates.",
        f"- Historical non-pass records still preserved for later human disposition: {len(historical_nonpasses)}. A later model pass cannot erase an earlier objection.",
        f"- All {len(worked_ids)} worked-case claims have source-support, challenge and cross-artifact review packages through the compiler import path.",
        f"- {len(human)} human-disposition packages remain. They require a real human reviewer and have not been simulated.",
        "", "## Uncertain source-support reviews", "",
    ]
    for claim_id, record in source_uncertain:
        lines.extend([f"### {claim_id}", "", record["rationale"], "",
                      "Limitations: " + "; ".join(record["limitations"]), ""])
    lines += ["## Current model objections or uncertainty", ""]
    if not current_nonpasses:
        lines.append("None.")
    for claim_id, task, record in current_nonpasses:
        lines.extend([f"### {claim_id} — {task} ({record['verdict']})", "", record["rationale"], "",
                      "Limitations: " + "; ".join(record["limitations"]), ""])
    lines += ["## Assurance-case blockers", ""]
    lines.extend(f"- {item}" for item in result["assurance_case_blockers"])
    lines += ["", "## Next disposition", "",
              "1. Refresh source-support, challenge, cross-artifact and model-synthesis reviews against the current package digests before relying on historical verdicts.",
              "2. Capture or recheck full original context for any source-support package that remains uncertain in that refresh.",
              "3. Keep model-review findings distinct from a later human disposition; a human may import only a current `human_disposition` record when the project is ready for that stage.",
              "4. Do not close the hypothetical case until its release, assumptions, evidence artifacts and obligations have evidence-backed dispositions."]
    (OUT / "first_pass_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    queue_lines = ["# Human-disposition queue: first worked-case pass", "",
                   "These are current compiler packages. A human reviewer must inspect the cited source context and prior review records before issuing a disposition. A disposition cannot be produced by a model.", ""]
    for packet in human:
        claim = packet["claim"]
        queue_lines += [f"## {packet['id']}", "", f"- Claim: `{claim['id']}` — {claim['text']}",
                        f"- Scope: {claim['scope']}", f"- Current input digest: `{packet['input_digest']}`",
                        "- Preceding reviews:"]
        for prior in packet.get("review_results", []):
            queue_lines.append(f"  - {prior['task']}: {prior['verdict']} ({prior['id']})")
        queue_lines += ["- Human decision: pending", ""]
    (OUT / "first_pass_human_queue.md").write_text("\n".join(queue_lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT / 'first_pass_report.md'} and {OUT / 'first_pass_human_queue.md'}")


if __name__ == "__main__":
    main()
