"""
Generate the verification report and compute VRM from result files.
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path


def load_results(results_dir: Path) -> list[dict]:
    results = []
    for f in sorted(results_dir.glob("*.json")):
        results.append(json.loads(f.read_text(encoding="utf-8")))
    return results


def compute_vrm(results: list[dict]) -> dict:
    """Compute VRM and component scores from all results."""

    # Citation score (Type A)
    citations = [r for r in results if r["vqp_type"] == "citation_verification"]
    if citations:
        citation_pass = sum(
            r.get("confidence", 0.5) for r in citations if r.get("verdict") == "pass"
        )
        citation_fail_uncertain = sum(
            (1 - r.get("confidence", 0.5))
            for r in citations
            if r.get("verdict") in ("fail", "uncertain")
        )
        total_citation_weight = sum(r.get("confidence", 0.5) for r in citations)
        raw_pass_count = sum(1 for r in citations if r.get("verdict") == "pass")
        citation_score = raw_pass_count / len(citations) if citations else 0.0
        citation_conf_score = (
            sum(r.get("confidence", 0.5) for r in citations if r.get("verdict") == "pass")
            / len(citations)
            if citations else 0.0
        )
    else:
        citation_score = 0.0
        citation_conf_score = 0.0
        raw_pass_count = 0

    # Coverage score (Type B)
    coverage = [r for r in results if r["vqp_type"] == "requirement_coverage"]
    if coverage:
        covered = [r for r in coverage if r.get("verdict") == "covered"]
        partial = [r for r in coverage if r.get("verdict") == "partial"]
        missing = [r for r in coverage if r.get("verdict") == "missing"]
        uncertain_cov = [
            r for r in coverage if r.get("verdict") not in ("covered", "partial", "missing")
        ]
        # Partial counts as 0.5
        weighted_covered = len(covered) + 0.5 * len(partial)
        coverage_score = weighted_covered / len(coverage) if coverage else 0.0
        coverage_conf_score = (
            sum(r.get("confidence", 0.5) for r in coverage) / len(coverage)
            if coverage else 0.0
        )
    else:
        coverage_score = 0.0
        coverage_conf_score = 0.0
        covered = partial = missing = uncertain_cov = []

    # Orphan penalty
    orphan_results = [r for r in results if r["vqp_type"] == "orphan_detection"]
    orphan_count = sum(len(r.get("findings", [])) for r in orphan_results)

    # VRM = 0.5 × citation_score + 0.5 × coverage_score
    vrm = 0.5 * citation_score + 0.5 * coverage_score

    return {
        "vrm": round(vrm, 3),
        "citation_score": round(citation_score, 3),
        "citation_confidence": round(citation_conf_score, 3),
        "citation_pass": raw_pass_count,
        "citation_total": len(citations),
        "coverage_score": round(coverage_score, 3),
        "coverage_confidence": round(coverage_conf_score, 3),
        "covered": len(covered),
        "partial": len(partial),
        "missing": len(missing),
        "uncertain_coverage": len(uncertain_cov),
        "coverage_total": len(coverage),
        "orphan_findings": orphan_count,
    }


def generate_report(results: list[dict], out_path: Path) -> str:
    scores = compute_vrm(results)

    lines = [
        "# Whitepaper Verification Report",
        f"Generated: {date.today().isoformat()}",
        f"Verification agent: Gemini 3.1 Pro Preview (thinking mode)",
        "",
        "---",
        "",
        "## Verification Readiness Metric (VRM)",
        "",
        f"**VRM = {scores['vrm']:.3f}** (0.0–1.0)",
        "",
        "| Component | Score | Detail |",
        "|---|---|---|",
        f"| Citation accuracy | {scores['citation_score']:.2f} | "
        f"{scores['citation_pass']}/{scores['citation_total']} citations pass |",
        f"| Requirement coverage | {scores['coverage_score']:.2f} | "
        f"{scores['covered']} covered, {scores['partial']} partial, "
        f"{scores['missing']} missing / {scores['coverage_total']} total |",
        f"| Orphan findings | — | {scores['orphan_findings']} structural anomalies |",
        "",
        "---",
        "",
    ]

    # ── Citation results ─────────────────────────────────────────────────────
    citations = [r for r in results if r["vqp_type"] == "citation_verification"]
    lines += [
        "## Type A — Citation Verification Results",
        "",
        f"Total citations evaluated: {len(citations)}",
        "",
        "| VQP ID (short) | Claim | Source | Verdict | Conf | Misrep? |",
        "|---|---|---|---|---|---|",
    ]
    for r in sorted(citations, key=lambda x: x.get("verdict", ""), reverse=True):
        vqp_short = r["vqp_id"].replace("A-CLAIM-", "").replace("SRC-", "")[:50]
        claim_id = r.get("claim_id", "?")
        src_id = r.get("source_id", "?")
        verdict = r.get("verdict", "?")
        conf = r.get("confidence", 0)
        misrep = "YES" if r.get("misrepresentation_found") else "no"
        lines.append(
            f"| {vqp_short} | {claim_id[:30]} | {src_id[:20]} | **{verdict}** | {conf:.2f} | {misrep} |"
        )

    lines += ["", "### Citation Details (issues only)", ""]
    for r in citations:
        if r.get("verdict") in ("fail", "uncertain") or r.get("misrepresentation_found"):
            lines += [
                f"#### {r.get('claim_id', r['vqp_id'])[:70]}",
                f"- **Verdict**: {r.get('verdict')} (confidence {r.get('confidence', 0):.2f})",
                f"- **Source**: {r.get('source_id', '?')}",
                f"- **What source says**: {r.get('what_source_actually_says', '?')}",
                f"- **Rationale**: {r.get('rationale', '?')}",
            ]
            if r.get("misrepresentation_detail"):
                lines.append(f"- **Misrepresentation**: {r['misrepresentation_detail']}")
            if r.get("scope_caveat"):
                lines.append(f"- **Scope caveat**: {r['scope_caveat']}")
            lines.append("")

    # ── Coverage results ─────────────────────────────────────────────────────
    coverage = [r for r in results if r["vqp_type"] == "requirement_coverage"]
    lines += [
        "---",
        "",
        "## Type B — Requirement Coverage Results",
        "",
        f"Total requirements evaluated: {len(coverage)}",
        "",
        "| Requirement | Verdict | Conf | Best Section |",
        "|---|---|---|---|",
    ]
    for r in sorted(coverage, key=lambda x: ("covered", "partial", "missing", "uncertain").index(
        x.get("verdict", "uncertain") if x.get("verdict") in ("covered", "partial", "missing") else "uncertain"
    )):
        req_id = r.get("requirement_id", "?")
        req_title = r.get("requirement_title", "?")[:40]
        verdict = r.get("verdict", "?")
        conf = r.get("confidence", 0)
        best_sec = r.get("best_matching_section", "")[:40]
        lines.append(f"| {req_id} {req_title} | **{verdict}** | {conf:.2f} | {best_sec} |")

    lines += ["", "### Coverage Gaps and Improvement Suggestions", ""]
    for r in coverage:
        gaps = r.get("coverage_gaps", [])
        suggestion = r.get("whitepaper_improvement_suggestion", "")
        if r.get("verdict") in ("partial", "missing") or gaps:
            lines += [
                f"#### {r.get('requirement_id')} — {r.get('requirement_title', '')[:60]}",
                f"- **Verdict**: {r.get('verdict')} (confidence {r.get('confidence', 0):.2f})",
            ]
            if gaps:
                lines.append("- **Gaps**:")
                for g in gaps:
                    lines.append(f"  - {g}")
            if suggestion:
                lines.append(f"- **Suggestion**: {suggestion}")
            lines.append("")

    # ── Orphan detection ─────────────────────────────────────────────────────
    orphan_results = [r for r in results if r["vqp_type"] == "orphan_detection"]
    lines += [
        "---",
        "",
        "## Type C — Orphan Detection",
        "",
    ]
    for r in orphan_results:
        for f in r.get("findings", []):
            lines += [
                f"- **[{f['anomaly']}]** {f['node_title'][:70]}",
                f"  {f['detail']}",
                "",
            ]
    if not any(r.get("findings") for r in orphan_results):
        lines.append("No orphan findings.")

    # ── Learnings ────────────────────────────────────────────────────────────
    lines += [
        "---",
        "",
        "## Learnings for Whitepaper Feedback",
        "",
        "These observations came from running the verification prototype on the whitepaper itself.",
        "Each learning is a candidate addition or clarification to the whitepaper content.",
        "",
    ]

    # Collect all improvement suggestions
    suggestions = []
    for r in coverage:
        s = r.get("whitepaper_improvement_suggestion", "")
        if s and r.get("verdict") in ("partial", "missing"):
            suggestions.append(f"**{r.get('requirement_id')}**: {s}")
    if suggestions:
        lines.append("### Whitepaper content gaps (from coverage analysis):")
        for s in suggestions:
            lines.append(f"- {s}")
        lines.append("")

    # Misrepresentations
    misreps = [
        r for r in citations
        if r.get("misrepresentation_found") or r.get("verdict") == "fail"
    ]
    if misreps:
        lines.append("### Citation issues requiring whitepaper correction:")
        for r in misreps:
            lines.append(
                f"- **{r.get('claim_id', r['vqp_id'])[:60]}** "
                f"({r.get('source_id', '?')}): {r.get('rationale', '')[:120]}"
            )
        lines.append("")

    # Structural observations
    lines += [
        "### Structural observations from running VC on prose:",
        "",
        "*(To be filled in after reviewing results)*",
        "",
    ]

    report = "\n".join(lines)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report, encoding="utf-8")
    return report
