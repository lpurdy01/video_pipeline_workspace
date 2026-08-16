"""
Build the artifact graph from project_wiki and Introductory_composition.md.

Parse order:
  1. Whitepaper H2 sections → SEC nodes
  2. Requirements subsections → REQ nodes
  3. Claims/*.md + matrix rows → CLAIM nodes
  4. Sources/*.md → SRC nodes
  5. source_to_claim_matrix.md → supported-by edges
  6. Citation-marker heuristic → appears-in edges (CLAIM → SEC)
  7. Keyword overlap → candidate covers edges (SEC → REQ), confirmed in traverser
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "whitepaper" / "gemini_tools"))

from schema import Edge, Graph, Node  # noqa: E402


# ── Helpers ───────────────────────────────────────────────────────────────────

def _slug(text: str) -> str:
    """Make a stable ASCII slug from arbitrary text."""
    s = text.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")[:60]


def _h2_sections(md: str) -> list[tuple[str, str]]:
    """Split markdown by H2 headings. Returns [(heading, body), ...]."""
    parts = re.split(r"^## (.+)$", md, flags=re.MULTILINE)
    sections = []
    for i in range(1, len(parts), 2):
        heading = parts[i].strip()
        body = parts[i + 1].strip() if i + 1 < len(parts) else ""
        sections.append((heading, body))
    return sections


def _h3_sections(body: str, parent_heading: str) -> list[tuple[str, str]]:
    """Split an H2 body by H3 headings."""
    parts = re.split(r"^### (.+)$", body, flags=re.MULTILINE)
    sections = []
    for i in range(1, len(parts), 2):
        heading = parts[i].strip()
        sub_body = parts[i + 1].strip() if i + 1 < len(parts) else ""
        sections.append((f"{parent_heading} / {heading}", sub_body))
    return sections


def _extract_key_section(md: str, heading: str) -> str:
    """Extract text under a given markdown heading (## or ###) from md."""
    # Use {{2,3}} not {{{2,3}}} — the latter produces literal '{(2, 3)}' in f-strings
    pattern = rf"^#{{2,3}} {re.escape(heading)}\s*\n(.*?)(?=^#{{2,3}} |\Z)"
    m = re.search(pattern, md, flags=re.MULTILINE | re.DOTALL)
    return m.group(1).strip() if m else ""


def _extract_markdown_section(md: str, section_title: str) -> str:
    """Extract text between ## section_title and the next ## heading."""
    pattern = rf"^## {re.escape(section_title)}\s*\n(.*?)(?=^## |\Z)"
    m = re.search(pattern, md, flags=re.MULTILINE | re.DOTALL)
    return m.group(1).strip() if m else ""


# ── Parsers ───────────────────────────────────────────────────────────────────

def _parse_whitepaper_sections(wp_path: Path, graph: Graph) -> None:
    """Add SEC nodes for each H2 section; sub-section-of edges for H3s."""
    text = wp_path.read_text(encoding="utf-8")
    # Remove H1 title
    text = re.sub(r"^# .+\n", "", text, count=1)

    h2s = _h2_sections(text)
    for heading, body in h2s:
        sec_id = f"SEC-{_slug(heading)}"
        graph.add_node(Node(
            id=sec_id,
            type="section",
            title=heading,
            text=body[:6000],  # cap per node
            metadata={"source": wp_path.name, "level": 2},
        ))
        # H3 sub-sections
        for sub_heading, sub_body in _h3_sections(body, heading):
            short = sub_heading.split(" / ", 1)[1]
            sub_id = f"SEC-{_slug(sub_heading)}"
            if sub_id not in graph.nodes:
                graph.add_node(Node(
                    id=sub_id,
                    type="section",
                    title=sub_heading,
                    text=sub_body[:4000],
                    metadata={"source": wp_path.name, "level": 3, "parent_heading": heading, "short": short},
                ))
            graph.edges.append(Edge(
                from_id=sub_id,
                to_id=sec_id,
                type="sub-section-of",
            ))


def _parse_requirements(req_path: Path, graph: Graph) -> None:
    """Add REQ nodes from the requirements file, by numbered subsection."""
    text = req_path.read_text(encoding="utf-8")
    # Match patterns like "### 1.1 Node Types" or "### 2.1 Context-Window..."
    pattern = r"^### (\d+\.\d+\w*) (.+?)\n(.*?)(?=^### |\Z)"
    matches = re.finditer(pattern, text, flags=re.MULTILINE | re.DOTALL)

    parent_map: dict[str, str] = {}  # section_num → parent REQ id

    # Also parse top-level ## sections for parent grouping
    top_pattern = r"^## (\d+)\. (.+?)\n"
    for m in re.finditer(top_pattern, text, flags=re.MULTILINE):
        sec_num = m.group(1)
        sec_title = m.group(2).strip()
        parent_id = f"REQ-{sec_num}"
        if parent_id not in graph.nodes:
            graph.add_node(Node(
                id=parent_id,
                type="requirement",
                title=sec_title,
                text=f"Section {sec_num}: {sec_title}",
                metadata={"section": sec_num, "level": "top"},
            ))
        parent_map[sec_num] = parent_id

    for m in matches:
        req_num = m.group(1)
        req_title = m.group(2).strip()
        req_body = m.group(3).strip()
        req_id = f"REQ-{req_num.replace('.', '-')}"
        graph.add_node(Node(
            id=req_id,
            type="requirement",
            title=req_title,
            text=req_body[:3000],
            metadata={"req_num": req_num, "level": "sub"},
        ))
        # Link to parent section
        parent_num = req_num.split(".")[0]
        if parent_num in parent_map:
            graph.edges.append(Edge(
                from_id=req_id,
                to_id=parent_map[parent_num],
                type="sub-req-of",
            ))


def _parse_sources(sources_dir: Path, graph: Graph) -> None:
    """Add SRC nodes from project_wiki/sources/*.md."""
    for src_file in sorted(sources_dir.glob("*.md")):
        text = src_file.read_text(encoding="utf-8")
        # Title from first H1
        title_m = re.search(r"^# (.+)$", text, flags=re.MULTILINE)
        title = title_m.group(1).strip() if title_m else src_file.stem

        # Concatenate all substantive sections for VQP assembly.
        # "Useful Claims" is highest priority — it holds verbatim quotes and
        # paraphraseable assertions that citation VQPs need to verify.
        parts = []
        for section in ("Useful Claims", "Key Ideas", "Why It Matters"):
            s = _extract_key_section(text, section)
            if s:
                parts.append(f"## {section}\n{s}")
        key_content = "\n\n".join(parts) if parts else text[:2000]

        src_id = f"SRC-{_slug(src_file.stem)}"
        graph.add_node(Node(
            id=src_id,
            type="source",
            title=title,
            text=key_content[:4000],
            metadata={"file": src_file.name},
        ))


def _parse_claims_and_matrix(
    claims_dir: Path,
    matrix_path: Path,
    graph: Graph,
) -> None:
    """
    Add CLAIM nodes from:
      - project_wiki/claims/*.md (rich metadata)
      - source_to_claim_matrix.md rows (for claims not in claims/*.md)

    Add supported-by edges from the matrix.
    """

    # ── 1. Claims from *.md files ─────────────────────────────────────────
    rich_claims: dict[str, str] = {}  # slug → claim_id (for dedup with matrix)
    for cf in sorted(claims_dir.glob("*.md")):
        text = cf.read_text(encoding="utf-8")
        title_m = re.search(r"^# (.+)$", text, flags=re.MULTILINE)
        title = title_m.group(1).strip() if title_m else cf.stem

        claim_body = _extract_key_section(text, "Claim")
        if not claim_body:
            # fallback: first non-heading paragraph
            claim_body = re.sub(r"^#+.+\n", "", text).strip()[:500]

        status_section = _extract_key_section(text, "Status")
        challenges = _extract_key_section(text, "Challenges or Uncertainty")

        claim_id = f"CLAIM-{_slug(cf.stem)}"
        rich_claims[_slug(title)] = claim_id
        graph.add_node(Node(
            id=claim_id,
            type="claim",
            title=title,
            text=claim_body,
            metadata={
                "status": status_section[:200],
                "challenges": challenges[:400],
                "source_file": cf.name,
            },
        ))

    # ── 2. Matrix rows → more claims + supported-by edges ────────────────
    matrix_text = matrix_path.read_text(encoding="utf-8")

    # Parse table rows: | Source | source_key | Claim | Support Type | Status | Evidence |
    # Also handles old 5-column format (no source_key column) for backwards compat.
    row_pat_6 = re.compile(
        r"^\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|",
        re.MULTILINE,
    )
    row_pat_5 = re.compile(
        r"^\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|",
        re.MULTILINE,
    )

    # Detect format by checking header row
    is_6col = "source_key" in matrix_text.split("\n")[0:5][0] if matrix_text else False
    for line in matrix_text.splitlines()[:5]:
        if "source_key" in line.lower():
            is_6col = True
            break

    row_pat = row_pat_6 if is_6col else row_pat_5

    for m in row_pat.finditer(matrix_text):
        groups = [g.strip() for g in m.groups()]
        if is_6col:
            src_raw, source_key, claim_raw, support_type, status, evidence = groups
        else:
            src_raw, claim_raw, support_type, status, evidence = groups
            source_key = ""

        # Skip header/separator rows
        if src_raw.lower() in ("source", "---", ":---"):
            continue

        # Skip retired rows — don't create claims or edges for retired citations
        status_clean = re.sub(r"\*\*", "", status).strip().lower()
        if "retired" in status_clean:
            continue

        claim_text = re.sub(r"\*\*.*?\*\*:?\s*", "", claim_raw)  # strip bold markers
        claim_text = re.sub(r"\[verify URL\]", "", claim_text).strip()
        if not claim_text or len(claim_text) < 5:
            continue

        claim_id = rich_claims.get(_slug(claim_text), f"CLAIM-{_slug(claim_text[:50])}")
        if claim_id not in graph.nodes:
            graph.add_node(Node(
                id=claim_id,
                type="claim",
                title=claim_text[:80],
                text=claim_text,
                metadata={
                    "support_type": support_type[:100],
                    "status": status[:100],
                    "evidence": evidence[:200],
                },
            ))

        # Resolve source to SRC node
        src_id = _resolve_source(src_raw, source_key, graph)
        if src_id and src_id in graph.nodes:
            # Avoid duplicate edges
            existing = [
                e for e in graph.edges
                if e.from_id == claim_id and e.to_id == src_id and e.type == "supported-by"
            ]
            if not existing:
                graph.edges.append(Edge(
                    from_id=claim_id,
                    to_id=src_id,
                    type="supported-by",
                    metadata={
                        "support_type": support_type[:100],
                        "evidence": evidence[:200],
                    },
                ))


def _resolve_source(src_raw: str, source_key: str, graph: Graph) -> str | None:
    """Map a matrix source row to a SRC node id.

    Resolution order:
      1. Exact source_key lookup: SRC-<source_key> (preferred — deterministic)
      2. Exact slug of src_raw (legacy fallback)
      3. Fuzzy keyword match (last resort — warns in caller if used)
    """
    # 1. Exact source_key lookup (slug-normalized — underscores → hyphens to match node IDs)
    if source_key and source_key not in ("", "-", "source_key"):
        exact_id = f"SRC-{_slug(source_key)}"
        if exact_id in graph.nodes:
            return exact_id
        # source_key specified but no matching node — don't fall through to fuzzy
        return None

    # 2. Exact slug of src_raw (5-column compat)
    candidate_id = f"SRC-{_slug(src_raw[:50])}"
    if candidate_id in graph.nodes:
        return candidate_id

    # 3. Fuzzy keyword match
    src_raw_lower = src_raw.lower()
    keywords = [w for w in src_raw_lower.split() if len(w) > 3]
    for node in graph.nodes_of_type("source"):
        node_lower = node.title.lower() + " " + node.metadata.get("file", "").lower()
        if any(kw in node_lower for kw in keywords):
            return node.id
    return None


# ── appears-in edges via citation marker heuristic ────────────────────────────

# Map claim titles / key phrases to citation markers that appear in the whitepaper
CITATION_MARKERS = [
    "[Zave & Jackson",
    "[FAA AC 20-115D",
    "[NASA Jacklin",
    "[NASA-STD-8739.8B",
    "[Rierson",
    "arXiv:2406.01574",
    "arXiv:2201.11903",
    "arXiv:2510.05156",
    "arXiv:2603.00539",
    "Cobleigh",
    "Mosier",
    "Skitka",
    "[EASA AI Roadmap",
    "[FAA AI Safety",
]

# Map source slugs to citation markers
SOURCE_TO_MARKERS: dict[str, list[str]] = {
    "rierson-do178c": ["[Rierson", "Rierson (Section", "DO-178C independence"],
    "faa-ac-20-115d": ["[FAA AC 20-115D", "FAA AC 20-115D"],
    "nasa-jacklin-do178c-do278a": ["[NASA Jacklin", "NASA Jacklin"],
    "nasa-std-8739-8b": ["[NASA-STD-8739.8B", "NASA-STD-8739.8B"],
    "llm-task-specific-accuracy": ["arXiv:2406.01574", "MMLU-Pro", "TIGER-AI-Lab", "HumanEval"],
    "agent-decomposition-literature": ["arXiv:2201.11903", "Chain-of-Thought", "Wei et al"],
    "llm-veriguard": ["arXiv:2510.05156", "VeriGuard"],
    "requirements-engineering-nl-ambiguity": ["[Zave & Jackson", "Zave & Jackson", "[Davis", "Davis, 1993"],
    "regulatory-ai-aviation-automotive": ["EASA AI Roadmap", "FAA AI Safety", "ISO/PAS 8800"],
    "mintzberg-org-structure": ["Mintzberg"],
    "amodei-adaptability": ["Amodei", "cross-session"],
    "beningo-embedded-moats": ["Beningo"],
    "as9100-public-references": ["AS9100", "IAQG", "SAE AS9100"],
    "iso-26262-public-references": ["ISO 26262", "ASIL", "NHTSA"],
    "iec-62443-public-references": ["IEC 62443", "CISA", "SL-1", "SL 1-4"],
    "npr-7150-2d": ["NPR 7150", "NASA NPR"],
    "llm-context-window-limits": ["arXiv:2307.03172", "Lost in the Middle", "arXiv:2510.05381"],
    "mosier-automation-bias-nasa": ["Mosier", "Skitka", "automation bias", "canary quer", "evidence-first"],
    "llm-overcorrection": ["arXiv:2603.00539", "overcorrection", "false rejection", "false positive"],
    "cobleigh-assume-guarantee": ["Cobleigh", "assume-guarantee", "compositional verification"],
}

# Additional: map individual matrix claim slugs to specific whitepaper section hints
CLAIM_SECTION_HINTS: dict[str, list[str]] = {
    "natural-language-specifications-are-ambiguous": [
        "SEC-english-as-a-specification-medium"
    ],
    "safety-critical-verification-depends-on-traceability": [
        "SEC-safety-critical-verification-as-a-coordination-system",
        "SEC-concept-verification-compiler",
    ],
    "model-units-need-task-specific-qualification": [
        "SEC-core-concept-units-of-intelligence",
        "SEC-concept-verification-compiler",
    ],
    "verification-requires-review-analysis-and-test": [
        "SEC-safety-critical-verification-as-a-coordination-system",
    ],
    "context-window-bounded-queries": [
        "SEC-concept-verification-compiler",
    ],
    "agent-decomposition-improves-reliability-over-single-agent-approaches": [
        "SEC-concept-verification-compiler",
    ],
    "llm-based-verification-achieves-meaningful-accuracy-on-bounded-safety-tasks": [
        "SEC-concept-verification-compiler",
    ],
    "llms-systematically-flag-correct-code-as-non-compliant": [
        "SEC-concept-verification-compiler",
    ],
    "verification-of-large-systems-decomposes-into-bounded-sub": [
        "SEC-concept-verification-compiler",
    ],
    "model-adaptability-is-strong-within-context-but-do": [
        "SEC-core-concept-units-of-intelligence",
    ],
    "regulatory-bodies-actively-engaging-with-ai-in-saf": [
        "SEC-concept-verification-compiler",
    ],
    "regulatory-bodies-are-actively-engaging-with-ai-in": [
        "SEC-concept-verification-compiler",
    ],
    "known-negative-test-injection-canary-queries-and": [
        "SEC-concept-verification-compiler",
    ],
    "automation-bias-in-time-critical-decision-support": [
        "SEC-concept-verification-compiler",
    ],
    "do-178c-independence-a-tool-s-may-be-used-to-ac": [
        "SEC-concept-verification-compiler",
    ],
    "human-reviewer-qualification-in-do-178c-is-informa": [
        "SEC-concept-verification-compiler",
    ],
    "certification-standards-define-evidence-objectives": [
        "SEC-safety-critical-verification-as-a-coordination-system",
        "SEC-concept-verification-compiler",
    ],
    "model-accuracy-is-task-specific-not-global": [
        "SEC-concept-verification-compiler",
        "SEC-core-concept-units-of-intelligence",
    ],
    "wider-management-spans-in-innovation-oriented-orgs": [
        "SEC-motivation",
    ],
    "nvidia-operates-with-60-direct-reports-to-ceo-de": [
        "SEC-motivation",
    ],
    "traceability-link-requirements": [
        "SEC-safety-critical-verification-as-a-coordination-system",
    ],
    "evidence-and-auditability-requirements": [
        "SEC-concept-verification-compiler",
    ],
    "aerospace-quality-management-standardizes-coordina": [
        "SEC-safety-critical-verification-as-a-coordination-system",
    ],
    "aerospace-quality-management-standardizes-coordination": [
        "SEC-safety-critical-verification-as-a-coordination-system",
    ],
}


def _add_appears_in_edges(graph: Graph) -> None:
    """
    Create appears-in edges from CLAIM nodes to SEC nodes.

    Strategy:
      1. For each CLAIM, check its supported-by sources.
      2. For each source, look up citation markers associated with that source.
      3. Scan each SEC node's text for those markers.
      4. If found, add an appears-in edge.
    Also apply manual CLAIM_SECTION_HINTS overrides.
    """
    # Build a lookup: source_slug → [marker strings]
    for claim in graph.nodes_of_type("claim"):
        matched_sections: set[str] = set()

        # Manual hints first (sec IDs are now full node IDs)
        claim_slug = claim.id.replace("CLAIM-", "")
        for hint_prefix, sec_ids in CLAIM_SECTION_HINTS.items():
            if claim_slug.startswith(hint_prefix[:40]):
                for sec_id in sec_ids:
                    if sec_id in graph.nodes:
                        matched_sections.add(sec_id)

        # Citation-marker heuristic
        for edge in graph.edges_from(claim.id, "supported-by"):
            src = graph.nodes.get(edge.to_id)
            if not src:
                continue
            src_slug = src.id.replace("SRC-", "")
            markers = SOURCE_TO_MARKERS.get(src_slug, [])

            for sec in graph.nodes_of_type("section"):
                if sec.metadata.get("level") != 2:
                    continue  # only top-level sections for appears-in
                for marker in markers:
                    if marker.lower() in sec.text.lower():
                        matched_sections.add(sec.id)
                        break

        for sec_id in sorted(matched_sections):  # sorted → deterministic edge insertion order
            existing = [
                e for e in graph.edges
                if e.from_id == claim.id and e.to_id == sec_id and e.type == "appears-in"
            ]
            if not existing:
                graph.edges.append(Edge(
                    from_id=claim.id,
                    to_id=sec_id,
                    type="appears-in",
                ))


# ── Main build function ───────────────────────────────────────────────────────

def build(repo: Path | None = None) -> Graph:
    if repo is None:
        repo = REPO

    wp = repo / "Introductory_composition.md"
    req = repo / "project_wiki" / "requirements" / "verification_compiler_requirements.md"
    claims_dir = repo / "project_wiki" / "claims"
    sources_dir = repo / "project_wiki" / "sources"
    matrix = repo / "project_wiki" / "traceability" / "source_to_claim_matrix.md"

    graph = Graph()

    print("Parsing whitepaper sections…")
    _parse_whitepaper_sections(wp, graph)

    print("Parsing requirements…")
    _parse_requirements(req, graph)

    print("Parsing sources…")
    _parse_sources(sources_dir, graph)

    print("Parsing claims and matrix…")
    _parse_claims_and_matrix(claims_dir, matrix, graph)

    print("Adding appears-in edges…")
    _add_appears_in_edges(graph)

    print(graph.summary())
    return graph


if __name__ == "__main__":
    out = REPO / "verification_prototype" / "data" / "graph.json"
    g = build()
    g.save(out)
    print(f"Saved → {out}")
