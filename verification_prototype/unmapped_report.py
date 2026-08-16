"""
Generate a reverse-coverage report for the whitepaper verification prototype.

This is a deterministic pre-verification aid. It answers the opposite question
from Type B VQPs:

    Type B: Does the document cover each requirement?
    This:   Which document sections are not mapped to any requirement?

The report is intentionally advisory. Whitepapers need narrative scaffolding,
examples, related work, and conclusions that may not belong under a system
requirement.
"""
from __future__ import annotations

import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(HERE / "graph"))

from builder import build  # noqa: E402
from traverser import _sections_for_req  # noqa: E402

OUT_PATH = HERE / "data" / "unmapped_report.md"

SCAFFOLD_KEYWORDS = (
    "working title",
    "introduction",
    "terminology note",
    "motivation",
    "worked example",
    "deployment contexts",
    "limitations",
    "open questions",
    "related work",
    "conclusion",
    "stage 2 direction",
    "list of acronyms",
)


def _is_scaffold(title: str) -> bool:
    title_l = title.lower()
    return any(keyword in title_l for keyword in SCAFFOLD_KEYWORDS)


def _parent_sections(graph) -> dict[str, str]:
    parents = {}
    for edge in graph.edges:
        if edge.type == "sub-section-of":
            parents[edge.from_id] = edge.to_id
    return parents


def _section_requirement_map(graph) -> dict[str, set[str]]:
    section_to_reqs: dict[str, set[str]] = defaultdict(set)
    for req in graph.nodes_of_type("requirement"):
        if req.metadata.get("level") != "sub":
            continue
        for section in _sections_for_req(req, graph):
            section_to_reqs[section["section_title"]].add(req.id)

    title_to_id = {node.title: node.id for node in graph.nodes_of_type("section")}
    return {
        title_to_id[title]: reqs
        for title, reqs in section_to_reqs.items()
        if title in title_to_id
    }


def generate_report() -> str:
    graph = build()
    parents = _parent_sections(graph)
    direct_reqs = _section_requirement_map(graph)

    inherited_reqs: dict[str, set[str]] = {}
    for section_id, parent_id in parents.items():
        if section_id not in direct_reqs and parent_id in direct_reqs:
            inherited_reqs[section_id] = direct_reqs[parent_id]

    sections = graph.nodes_of_type("section")
    strict_unmapped = [
        section for section in sections
        if section.id not in direct_reqs and section.id not in inherited_reqs
    ]
    advisory_unmapped = [section for section in strict_unmapped if not _is_scaffold(section.title)]
    scaffold_unmapped = [section for section in strict_unmapped if _is_scaffold(section.title)]

    section_claims: dict[str, list[str]] = defaultdict(list)
    claim_to_sources: dict[str, list[str]] = defaultdict(list)
    for edge in graph.edges:
        if edge.type == "appears-in":
            section_claims[edge.to_id].append(edge.from_id)
        elif edge.type == "supported-by":
            claim_to_sources[edge.from_id].append(edge.to_id)

    claims_without_document_location = [
        claim for claim in graph.nodes_of_type("claim")
        if claim.id not in section_claims.values()
    ]
    # section_claims is keyed by section; build the direct claim set explicitly.
    located_claim_ids = {
        claim_id
        for claim_ids in section_claims.values()
        for claim_id in claim_ids
    }
    claims_without_document_location = [
        claim for claim in graph.nodes_of_type("claim")
        if claim.id not in located_claim_ids
    ]
    claims_without_sources = [
        claim for claim in graph.nodes_of_type("claim")
        if not claim_to_sources.get(claim.id)
    ]

    unused_sources = []
    used_source_ids = {source_id for source_ids in claim_to_sources.values() for source_id in source_ids}
    for source in graph.nodes_of_type("source"):
        if source.id not in used_source_ids:
            unused_sources.append(source)

    lines = [
        "# Whitepaper Unmapped Section Report",
        f"Generated: {date.today().isoformat()}",
        "",
        "This deterministic report checks reverse coverage before a verification run.",
        "It is advisory: a whitepaper can legitimately contain narrative, examples, and related work that are not system requirements.",
        "",
        "## Summary",
        "",
        f"- Sections parsed: {len(sections)}",
        f"- Sections directly mapped to requirements: {len(direct_reqs)}",
        f"- Subsections inheriting parent requirement context: {len(inherited_reqs)}",
        f"- Strictly unmapped sections: {len(strict_unmapped)}",
        f"- Advisory unmapped substantive sections: {len(advisory_unmapped)}",
        f"- Unmapped scaffold/front-back/example sections: {len(scaffold_unmapped)}",
        f"- Claims with source support but no located whitepaper section: {len(claims_without_document_location)}",
        f"- Claims without source support: {len(claims_without_sources)}",
        f"- Source notes not used by any current claim edge: {len(unused_sources)}",
        "",
        "## Advisory Unmapped Sections",
        "",
    ]

    if advisory_unmapped:
        for section in advisory_unmapped:
            claim_count = len(section_claims.get(section.id, []))
            lines.append(
                f"- `{section.id}` ({section.metadata.get('level')}) {section.title} "
                f"- located claims: {claim_count}"
            )
    else:
        lines.append("No advisory unmapped substantive sections.")

    lines += [
        "",
        "## Unmapped Scaffold / Narrative Sections",
        "",
    ]
    if scaffold_unmapped:
        for section in scaffold_unmapped:
            claim_count = len(section_claims.get(section.id, []))
            lines.append(
                f"- `{section.id}` ({section.metadata.get('level')}) {section.title} "
                f"- located claims: {claim_count}"
            )
    else:
        lines.append("No unmapped scaffold sections.")

    lines += [
        "",
        "## Requirement-Mapped Sections",
        "",
    ]
    for section_id in sorted(direct_reqs):
        section = graph.nodes[section_id]
        req_list = ", ".join(sorted(direct_reqs[section_id]))
        lines.append(f"- `{section_id}` {section.title} -> {req_list}")

    if inherited_reqs:
        lines += [
            "",
            "## Subsections Covered By Parent Context",
            "",
        ]
        for section_id in sorted(inherited_reqs):
            section = graph.nodes[section_id]
            parent = graph.nodes[parents[section_id]]
            req_list = ", ".join(sorted(inherited_reqs[section_id]))
            lines.append(
                f"- `{section_id}` {section.title} -> parent `{parent.id}` ({req_list})"
            )

    lines += [
        "",
        "## Claim / Citation Location Checks",
        "",
    ]
    if claims_without_document_location:
        lines.append("Claims with source support but no located whitepaper section:")
        for claim in claims_without_document_location:
            sources = ", ".join(claim_to_sources.get(claim.id, [])) or "none"
            lines.append(f"- `{claim.id}` {claim.title} -> {sources}")
    else:
        lines.append("All claim nodes are located in at least one whitepaper section.")

    if claims_without_sources:
        lines += [
            "",
            "Claims without source support:",
        ]
        for claim in claims_without_sources:
            lines.append(f"- `{claim.id}` {claim.title}")

    if unused_sources:
        lines += [
            "",
            "Source notes not used by current claim edges:",
        ]
        for source in unused_sources:
            lines.append(f"- `{source.id}` {source.title}")

    lines += [
        "",
        "## Interpretation",
        "",
        "Use this report to decide whether an unmapped section should become a requirement,",
        "be linked to an existing requirement, or remain intentional narrative material.",
    ]

    return "\n".join(lines) + "\n"


def main() -> None:
    report = generate_report()
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(report, encoding="utf-8")
    print(f"Report written -> {OUT_PATH}")


if __name__ == "__main__":
    main()
