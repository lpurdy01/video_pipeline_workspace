"""
Structural validator — pre-flight check before running the verification compiler.

Verifies that all documents can be parsed into an addressable AST, every matrix
source row resolves unambiguously to a source node, and assembled VQP payloads
would fit a context window.

Checks (in order):
  1. Document AST — heading slugs, uniqueness, empty bodies, content hashes
  2. Source resolution — every matrix row resolves to exactly one SRC node
  3. VQP assemblability — estimated payload sizes within configured limit
  4. Orphan detection — claims without sources, requirements without sections

Exit code: 0 = all checks pass, 1 = errors present
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

REPO = Path(__file__).resolve().parents[1]
GRAPH_DIR = REPO / "verification_prototype" / "graph"
if str(GRAPH_DIR) not in sys.path:
    sys.path.insert(0, str(GRAPH_DIR))

from builder import build  # noqa: E402
from traverser import traverse  # noqa: E402

# ── Config ────────────────────────────────────────────────────────────────────

VQP_CHAR_WARN = 12_000   # ~3K tokens — warn if assembled VQP exceeds this
VQP_CHAR_ERROR = 40_000  # ~10K tokens — error; definitely won't fit most windows

DOCS_TO_VALIDATE = [
    REPO / "Introductory_composition.md",
    REPO / "project_wiki" / "requirements" / "verification_compiler_requirements.md",
]
SOURCES_DIR = REPO / "project_wiki" / "sources"
MATRIX_PATH = REPO / "project_wiki" / "traceability" / "source_to_claim_matrix.md"


# ── Issue dataclass ───────────────────────────────────────────────────────────

Severity = Literal["ERROR", "WARN", "INFO"]


@dataclass
class Issue:
    severity: Severity
    check: str
    detail: str
    location: str = ""

    def __str__(self) -> str:
        loc = f" [{self.location}]" if self.location else ""
        return f"  {self.severity:5s} {self.check}: {self.detail}{loc}"


@dataclass
class ValidationResult:
    issues: list[Issue] = field(default_factory=list)

    def add(self, severity: Severity, check: str, detail: str, location: str = "") -> None:
        self.issues.append(Issue(severity, check, detail, location))

    @property
    def errors(self) -> list[Issue]:
        return [i for i in self.issues if i.severity == "ERROR"]

    @property
    def warnings(self) -> list[Issue]:
        return [i for i in self.issues if i.severity == "WARN"]

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0


# ── Helpers ───────────────────────────────────────────────────────────────────

def _slug(text: str) -> str:
    s = text.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")[:60]


def _content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def _parse_headings(md: str, path: Path) -> list[tuple[int, str, str]]:
    """Return [(level, heading_text, body_text), ...] for every H2 and H3."""
    results = []
    pattern = re.compile(r"^(#{2,3}) (.+)$", re.MULTILINE)
    matches = list(pattern.finditer(md))
    for i, m in enumerate(matches):
        level = len(m.group(1))
        heading = m.group(2).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(md)
        body = md[start:end].strip()
        results.append((level, heading, body))
    return results


def _parse_matrix_rows(matrix_text: str) -> list[dict]:
    """
    Parse matrix rows. Supports both 5-column and 6-column formats:
      5-col: | Source | Claim | Support Type | Status | Evidence |
      6-col: | Source | source_key | Claim | Support Type | Status | Evidence |
    """
    rows = []
    for line in matrix_text.splitlines():
        if not line.startswith("|"):
            continue
        cols = [c.strip() for c in line.strip("|").split("|")]
        if len(cols) < 5:
            continue
        # Detect header/separator rows
        if cols[0].lower() in ("source", "---", ":---") or cols[0].startswith("---"):
            continue
        if len(cols) >= 6 and cols[1].lower() not in ("---", ":---", "source_key", "source key"):
            # 6-column format with source_key
            src_raw, source_key, claim_raw, support_type, status, evidence = cols[0], cols[1], cols[2], cols[3], cols[4], cols[5]
        else:
            src_raw, claim_raw, support_type, status, evidence = cols[0], cols[1], cols[2], cols[3], cols[4]
            source_key = ""
        rows.append({
            "source": src_raw,
            "source_key": source_key,
            "claim": claim_raw,
            "support_type": support_type,
            "status": status,
            "evidence": evidence,
        })
    return rows


def _src_node_title(src_file: Path) -> str:
    text = src_file.read_text(encoding="utf-8")
    m = re.search(r"^# (.+)$", text, flags=re.MULTILINE)
    return m.group(1).strip() if m else src_file.stem


def _src_key_content(src_file: Path) -> str:
    text = src_file.read_text(encoding="utf-8")
    for heading in ("Key Ideas", "Why It Matters"):
        pattern = rf"^#{{{2,3}}} {re.escape(heading)}\s*\n(.*?)(?=^#{{{2,3}}} |\Z)"
        m = re.search(pattern, text, flags=re.MULTILINE | re.DOTALL)
        if m:
            return m.group(1).strip()
    return text[:2000]


VALID_SUMMARY_METHODS = {
    "llm-extract-from-raw",   # LLM read the actual raw file — verifiable against raw_file
    "llm-from-url",           # LLM read a URL — re-verifiable; URL may change over time
    "human-written",          # Human wrote the summary from reading the source — most trusted
    "llm-stub-unverified",    # Created from memory/context without reading actual source — ERROR
}


# ── Check 0: Source Provenance ────────────────────────────────────────────────

def check_source_provenance(result: ValidationResult) -> None:
    """
    Every source .md must declare a ## Provenance section with structured fields.
    Checks:
    - Missing Provenance section → ERROR
    - llm-stub-unverified → ERROR (LLM hallucination risk)
    - raw_file declared but path doesn't exist → ERROR
    - no raw_file and no raw_url → ERROR (no backing at all)
    - llm-from-url with summary_verified: false → WARN (should re-read to confirm)
    - llm-extract-from-raw with summary_verified: false → WARN (can check against raw)
    """
    if not SOURCES_DIR.exists():
        result.add("ERROR", "provenance", "Sources directory not found", str(SOURCES_DIR))
        return

    n_ok = 0
    n_stubs = 0

    for src_file in sorted(SOURCES_DIR.glob("*.md")):
        text = src_file.read_text(encoding="utf-8")

        # Find ## Provenance section
        prov_match = re.search(
            r"^## Provenance\s*\n(.*?)(?=^## |\Z)",
            text, flags=re.MULTILINE | re.DOTALL,
        )
        if not prov_match:
            result.add("ERROR", "provenance",
                f"No ## Provenance section — summary has no declared backing source",
                src_file.name)
            continue

        prov_text = prov_match.group(1)

        def _field(name: str) -> str:
            m = re.search(rf"^{name}:\s*(.+)$", prov_text, flags=re.MULTILINE)
            return m.group(1).strip() if m else ""

        raw_file = _field("raw_file")
        raw_url = _field("raw_url")
        summary_method = _field("summary_method")
        summary_verified = _field("summary_verified").lower()

        # No backing at all
        if (not raw_file or raw_file == "null") and (not raw_url or raw_url == "null"):
            result.add("ERROR", "provenance",
                f"No raw_file or raw_url — source summary has no recoverable backing",
                src_file.name)
            continue

        # stub-unverified: LLM hallucination risk — hard error
        if summary_method == "llm-stub-unverified":
            n_stubs += 1
            result.add("ERROR", "provenance",
                f"summary_method is llm-stub-unverified — content not derived from reading actual source. "
                f"Obtain raw file from: {raw_url or raw_file}",
                src_file.name)
            continue

        # Unknown method
        if summary_method not in VALID_SUMMARY_METHODS:
            result.add("ERROR", "provenance",
                f"Unknown summary_method '{summary_method}'", src_file.name)
            continue

        # raw_file declared — check it exists
        if raw_file and raw_file != "null":
            raw_path = REPO / raw_file
            if not raw_path.exists():
                result.add("ERROR", "provenance",
                    f"raw_file declared but not found: {raw_file}", src_file.name)
                continue

        # Unverified warnings
        if summary_verified != "true":
            if summary_method == "llm-extract-from-raw":
                result.add("WARN", "provenance",
                    f"Summary not yet verified against raw file — run content spot-check",
                    src_file.name)
            elif summary_method == "llm-from-url":
                result.add("WARN", "provenance",
                    f"Summary not yet verified against URL — URL content may have changed",
                    src_file.name)

        n_ok += 1

    total = len(list(SOURCES_DIR.glob("*.md")))
    result.add("INFO", "provenance",
        f"{n_ok}/{total} sources have valid provenance ({n_stubs} stubs flagged)")


# ── Check 1: Document AST ─────────────────────────────────────────────────────

def check_document_ast(result: ValidationResult) -> dict[Path, list[tuple[str, str, str]]]:
    """
    Parse every document into (slug, heading, body) tuples.
    Check: no empty bodies, no slug collisions within a document.
    Returns the parsed nodes for use in downstream checks.
    """
    all_doc_nodes: dict[Path, list[tuple[str, str, str]]] = {}

    for doc_path in DOCS_TO_VALIDATE:
        if not doc_path.exists():
            result.add("ERROR", "doc-ast", f"Document not found", str(doc_path))
            continue

        md = doc_path.read_text(encoding="utf-8")
        headings = _parse_headings(md, doc_path)
        if not headings:
            result.add("WARN", "doc-ast", "No H2/H3 headings found — document not addressable", doc_path.name)
            continue

        slug_seen: dict[str, str] = {}
        nodes: list[tuple[str, str, str]] = []
        empty_bodies = 0

        for level, heading, body in headings:
            prefix = "H2" if level == 2 else "H3"
            slug = f"{prefix}-{_slug(heading)}"
            uri = f"doc:{doc_path.name}#{slug}"

            # Collision check
            if slug in slug_seen:
                result.add("ERROR", "doc-ast",
                    f"Slug collision: '{slug}' produced by both '{slug_seen[slug]}' and '{heading}'",
                    doc_path.name)
            else:
                slug_seen[slug] = heading

            # Empty body
            if not body:
                empty_bodies += 1
                result.add("WARN", "doc-ast",
                    f"Empty body for section '{heading}' — no content to inject into VQP",
                    doc_path.name)

            # Content hash (verifies it's computable)
            chash = _content_hash(body)
            nodes.append((uri, heading, body))

        all_doc_nodes[doc_path] = nodes
        n_sections = len(nodes)
        n_collisions = n_sections - len(slug_seen)
        result.add("INFO", "doc-ast",
            f"{n_sections} sections parsed, {empty_bodies} empty, {-n_collisions if n_collisions < 0 else n_collisions} collisions",
            doc_path.name)

    return all_doc_nodes


# ── Check 2: Source Resolution ────────────────────────────────────────────────

def check_source_resolution(result: ValidationResult) -> dict[str, str | None]:
    """
    For every matrix row, attempt to resolve the source label to a source file.
    Returns {source_label: resolved_file_stem | None}.
    """
    if not MATRIX_PATH.exists():
        result.add("ERROR", "src-resolve", "Matrix file not found", str(MATRIX_PATH))
        return {}
    if not SOURCES_DIR.exists():
        result.add("ERROR", "src-resolve", "Sources directory not found", str(SOURCES_DIR))
        return {}

    # Build index of available source nodes
    src_index: dict[str, tuple[Path, str]] = {}  # stem → (path, title)
    for src_file in sorted(SOURCES_DIR.glob("*.md")):
        title = _src_node_title(src_file)
        src_index[src_file.stem] = (src_file, title)

    matrix_text = MATRIX_PATH.read_text(encoding="utf-8")
    rows = _parse_matrix_rows(matrix_text)

    resolutions: dict[str, str | None] = {}
    unresolved: list[str] = []
    fuzzy_only: list[str] = []
    multi_match: list[str] = []
    retired: list[str] = []

    for row in rows:
        src_raw = row["source"]
        source_key = row.get("source_key", "").strip()
        status = row["status"].lower()

        # Mark retired sources — expected to not fully resolve
        if "retired" in row["evidence"].lower() or "retired" in status:
            retired.append(src_raw)
            resolutions[src_raw] = None
            continue

        # 1. Exact source_key match (preferred — stable machine-readable ID)
        if source_key and source_key in src_index:
            resolutions[src_raw] = source_key
            continue
        elif source_key and source_key not in src_index:
            # source_key specified but file doesn't exist — hard error
            resolutions[src_raw] = None
            unresolved.append(f"{src_raw} (source_key='{source_key}' — file not found)")
            continue

        # 2. Fallback: exact slug match against file stems
        src_slug = _slug(src_raw[:50])
        exact_matches = [stem for stem in src_index if stem == src_slug]

        # 3. Fallback: fuzzy keyword match
        src_keywords = [w for w in src_raw.lower().split() if len(w) > 3]
        fuzzy_matches = []
        for stem, (path, title) in src_index.items():
            combined = (stem + " " + title).lower()
            if any(kw in combined for kw in src_keywords):
                fuzzy_matches.append(stem)

        # Resolve
        if exact_matches:
            resolutions[src_raw] = exact_matches[0]
        elif len(fuzzy_matches) == 1:
            resolutions[src_raw] = fuzzy_matches[0]
            fuzzy_only.append(src_raw)
        elif len(fuzzy_matches) > 1:
            resolutions[src_raw] = fuzzy_matches[0]
            multi_match.append(f"'{src_raw}' → {fuzzy_matches[:4]}")
        else:
            resolutions[src_raw] = None
            unresolved.append(src_raw)

    # Report
    if unresolved:
        for u in unresolved:
            result.add("ERROR", "src-resolve",
                f"No source node found for: '{u}'", MATRIX_PATH.name)
    if multi_match:
        for m in multi_match:
            result.add("ERROR", "src-resolve",
                f"Ambiguous resolution (multiple fuzzy matches): {m} — wrong mapping likely",
                MATRIX_PATH.name)
    if fuzzy_only:
        for f in fuzzy_only:
            result.add("WARN", "src-resolve",
                f"Fuzzy-only resolution (no exact slug match): '{f}' — verify mapping is correct",
                MATRIX_PATH.name)
    if retired:
        result.add("INFO", "src-resolve",
            f"{len(retired)} source(s) marked retired (expected — tracked decisions)",
            MATRIX_PATH.name)

    n_ok = sum(1 for v in resolutions.values() if v is not None)
    result.add("INFO", "src-resolve",
        f"{n_ok}/{len(rows)} rows resolved ({len(unresolved)} errors, {len(multi_match)} ambiguous, {len(fuzzy_only)} fuzzy-only, {len(retired)} retired)",
        MATRIX_PATH.name)

    return resolutions


# ── Check 3: VQP Assemblability ───────────────────────────────────────────────

def check_vqp_size(result: ValidationResult, resolutions: dict[str, str | None]) -> None:
    """
    For each resolvable claim-source pair, estimate the assembled VQP payload size.
    Flag payloads that would exceed VQP_CHAR_WARN or VQP_CHAR_ERROR.
    """
    if not MATRIX_PATH.exists():
        return

    matrix_text = MATRIX_PATH.read_text(encoding="utf-8")
    rows = _parse_matrix_rows(matrix_text)
    wp_text = (REPO / "Introductory_composition.md").read_text(encoding="utf-8") if (
        REPO / "Introductory_composition.md").exists() else ""

    oversized_warn = 0
    oversized_error = 0

    for row in rows:
        src_raw = row["source"]
        resolved_stem = resolutions.get(src_raw)
        if not resolved_stem:
            continue

        src_file = SOURCES_DIR / f"{resolved_stem}.md"
        if not src_file.exists():
            continue

        claim_text = row["claim"]
        src_content = _src_key_content(src_file)

        # Find claim in whitepaper (heuristic: search for first ~40 chars of claim)
        search_str = claim_text[:40].lower()
        section_excerpt = ""
        if wp_text:
            idx = wp_text.lower().find(search_str)
            if idx != -1:
                # Take surrounding 2000 chars as section context
                start = max(0, idx - 500)
                end = min(len(wp_text), idx + 1500)
                section_excerpt = wp_text[start:end]

        payload_size = len(claim_text) + len(src_content) + len(section_excerpt)
        vqp_id = f"A-{_slug(claim_text[:30])}-{resolved_stem}"[:60]

        if payload_size > VQP_CHAR_ERROR:
            oversized_error += 1
            result.add("ERROR", "vqp-size",
                f"VQP '{vqp_id}' estimated at {payload_size:,} chars — exceeds hard limit ({VQP_CHAR_ERROR:,})",
                src_raw[:60])
        elif payload_size > VQP_CHAR_WARN:
            oversized_warn += 1
            result.add("WARN", "vqp-size",
                f"VQP '{vqp_id}' estimated at {payload_size:,} chars — exceeds warning threshold ({VQP_CHAR_WARN:,})",
                src_raw[:60])

    n_resolvable = sum(1 for v in resolutions.values() if v is not None)
    result.add("INFO", "vqp-size",
        f"{n_resolvable} VQPs estimated, {oversized_warn} oversized (warn), {oversized_error} oversized (error)")


def _fill_template(template: str, **kwargs: str) -> str:
    """Replace simple prompt placeholders without interpreting JSON braces."""
    result = template
    for key, value in kwargs.items():
        result = result.replace("{" + key + "}", value)
    return result


def _executable_prompt_size(vqp: dict) -> int:
    """Estimate the actual Gemini prompt size produced by agents/gemini.py."""
    prompts_dir = REPO / "verification_prototype" / "prompts"
    payload = vqp["payload"]

    if vqp["vqp_type"] == "citation_verification":
        template = (prompts_dir / "citation_verification.txt").read_text(encoding="utf-8")
        section_parts = [
            f"--- Section: {sec['section_title']} ---\n{sec['text'][:1500]}"
            for sec in payload.get("whitepaper_sections", [])
        ]
        wp_context = "\n\n".join(section_parts) if section_parts else "(no section context available)"
        return len(_fill_template(
            template,
            claim_title=payload["claim_title"],
            claim_text=payload["claim_text"],
            support_type=payload["support_type"],
            evidence_note=payload["evidence_note"],
            source_title=payload["source_title"],
            source_key_content=payload["source_key_content"][:2000],
            whitepaper_context=wp_context[:3000],
        ))

    if vqp["vqp_type"] == "requirement_coverage":
        template = (prompts_dir / "requirement_coverage.txt").read_text(encoding="utf-8")
        section_parts = [
            f"--- Section: {sec['section_title']} ---\n{sec['text']}"
            for sec in payload.get("candidate_sections", [])
        ]
        section_texts = "\n\n".join(section_parts) if section_parts else "(no candidate sections found)"
        return len(_fill_template(
            template,
            requirement_id=payload["requirement_id"],
            requirement_title=payload["requirement_title"],
            req_num=payload["req_num"],
            requirement_text=payload["requirement_text"][:2000],
            section_texts=section_texts,
        ))

    return len(json.dumps(vqp, ensure_ascii=False))


def check_graph_construction_and_actual_vqps(result: ValidationResult) -> None:
    """Build the real graph/VQPs and check DAG integrity plus full VQP sizes."""
    graph = build()

    dangling = [
        edge for edge in graph.edges
        if edge.from_id not in graph.nodes or edge.to_id not in graph.nodes
    ]
    for edge in dangling:
        result.add("ERROR", "dag",
            f"Dangling edge {edge.type}: {edge.from_id} -> {edge.to_id}")

    # Kahn topological traversal over all directed graph edges.
    adjacency: dict[str, list[str]] = {node_id: [] for node_id in graph.nodes}
    indegree: dict[str, int] = {node_id: 0 for node_id in graph.nodes}
    for edge in graph.edges:
        if edge.from_id in graph.nodes and edge.to_id in graph.nodes:
            adjacency[edge.from_id].append(edge.to_id)
            indegree[edge.to_id] += 1

    queue = [node_id for node_id, degree in indegree.items() if degree == 0]
    visited = 0
    while queue:
        node_id = queue.pop()
        visited += 1
        for target_id in adjacency[node_id]:
            indegree[target_id] -= 1
            if indegree[target_id] == 0:
                queue.append(target_id)

    if visited != len(graph.nodes):
        cycle_nodes = [node_id for node_id, degree in indegree.items() if degree > 0]
        result.add("ERROR", "dag",
            f"Cycle detected; topological traversal visited {visited}/{len(graph.nodes)} nodes",
            ", ".join(cycle_nodes[:8]))
    else:
        result.add("INFO", "dag",
            f"Acyclic graph confirmed ({len(graph.nodes)} nodes, {len(graph.edges)} edges)")

    vqps = [vqp.to_dict() for vqp in traverse(graph)]
    counts: dict[str, int] = {}
    for vqp in vqps:
        counts[vqp["vqp_type"]] = counts.get(vqp["vqp_type"], 0) + 1

    warn_count = 0
    error_count = 0
    largest: list[tuple[int, str]] = []
    for vqp in vqps:
        if vqp["vqp_type"] == "orphan_detection":
            findings = vqp["payload"].get("findings", [])
            if findings:
                result.add("WARN", "orphan",
                    f"Constructed orphan-detection VQP contains {len(findings)} finding(s)",
                    vqp["id"])
            continue

        prompt_size = _executable_prompt_size(vqp)
        largest.append((prompt_size, vqp["id"]))
        if prompt_size > VQP_CHAR_ERROR:
            error_count += 1
            result.add("ERROR", "vqp-size",
                f"Executable prompt '{vqp['id']}' estimated at {prompt_size:,} chars — exceeds hard limit ({VQP_CHAR_ERROR:,})")
        elif prompt_size > VQP_CHAR_WARN:
            warn_count += 1

    largest.sort(reverse=True)
    if largest:
        top_size, top_id = largest[0]
        result.add("INFO", "vqp-size",
            f"Actual executable VQPs: {counts}; largest {top_id} is {top_size:,} chars; "
            f"{warn_count} over warning threshold, {error_count} over hard limit")


# ── Check 4: Orphan Detection ─────────────────────────────────────────────────

def check_orphans(result: ValidationResult, resolutions: dict[str, str | None]) -> None:
    """
    Structural gap checks:
    - Claims with no resolved source (will produce unsupported VQP)
    - Source files in wiki/sources/ never referenced in the matrix (unused)
    - Requirements sections that parser won't find (no ### N.N pattern)
    """
    if not MATRIX_PATH.exists():
        return

    matrix_text = MATRIX_PATH.read_text(encoding="utf-8")
    rows = _parse_matrix_rows(matrix_text)

    # Claims with no source
    unsupported = [(r["claim"][:60], r["source"][:40]) for r in rows
                   if resolutions.get(r["source"]) is None
                   and "retired" not in r["evidence"].lower()]
    for claim, src in unsupported:
        result.add("WARN", "orphan",
            f"Claim will have no supporting source node: '{claim}'",
            f"source: '{src}'")

    # Source files not referenced in the matrix at all
    referenced_stems = {resolutions[r["source"]] for r in rows if resolutions.get(r["source"])}
    for src_file in sorted(SOURCES_DIR.glob("*.md")):
        if src_file.stem not in referenced_stems:
            result.add("INFO", "orphan",
                f"Source file not referenced in matrix (unused): {src_file.name}")

    # Requirements file — check that the ### N.N pattern fires
    req_path = REPO / "project_wiki" / "requirements" / "verification_compiler_requirements.md"
    if req_path.exists():
        req_text = req_path.read_text(encoding="utf-8")
        req_matches = re.findall(r"^### (\d+\.\d+\w*) (.+?)$", req_text, flags=re.MULTILINE)
        if not req_matches:
            result.add("ERROR", "orphan",
                "Requirements file has no parseable ### N.N sections — REQ nodes won't be built",
                req_path.name)
        else:
            result.add("INFO", "orphan",
                f"{len(req_matches)} requirement subsections parseable from requirements file",
                req_path.name)


# ── Runner ────────────────────────────────────────────────────────────────────

def run_validation() -> ValidationResult:
    result = ValidationResult()

    print("=" * 64)
    print("Verification Compiler — Structural Validator")
    print("=" * 64)

    print("\n[1/4] Source provenance")
    check_source_provenance(result)

    print("\n[2/4] Document AST parseability")
    doc_nodes = check_document_ast(result)

    print("\n[3/4] Source resolution")
    resolutions = check_source_resolution(result)

    print("\n[4/4] VQP size + orphan detection")
    check_vqp_size(result, resolutions)
    check_orphans(result, resolutions)
    check_graph_construction_and_actual_vqps(result)

    # ── Summary ───────────────────────────────────────────────────────────────
    print("\n" + "=" * 64)
    print("Results")
    print("=" * 64)

    for issue in result.issues:
        print(issue)

    print()
    n_err = len(result.errors)
    n_warn = len(result.warnings)
    n_info = len(result.issues) - n_err - n_warn
    status = "PASS" if result.ok else "FAIL"
    print(f"Status: {status}  |  {n_err} errors  {n_warn} warnings  {n_info} info")
    if result.ok:
        print("All structural checks passed — safe to proceed with verification run.")
    else:
        print("Fix errors above before running the verification compiler.")

    return result


if __name__ == "__main__":
    result = run_validation()
    sys.exit(0 if result.ok else 1)
