# Verification Compiler Prototype — Implementation Plan

## What This Is

A self-referential proof-of-concept: we apply the Verification Compiler concept (as described in
the whitepaper) to verify the whitepaper itself. The whitepaper is the artifact under verification.
The project_wiki is the source of requirements and citations. Gemini is the verification agent.

This is a practice run. Learnings will feed back into the whitepaper concept.

---

## The Analogy

| Real VC (for C code) | This Prototype (for the whitepaper) |
|---|---|
| Source code units | Whitepaper sections (by H2/H3 heading) |
| Requirements | System requirements from verification_compiler_requirements.md |
| Test artifacts | Claim–source pairs from source_to_claim_matrix.md |
| Static analysis | Claim files in project_wiki/claims/*.md |
| Evidence package | Source notes in project_wiki/sources/*.md |
| VRM | Coverage fraction × mean citation accuracy |

---

## Node Types

| ID Prefix | Type | Source |
|---|---|---|
| `SEC-` | WhitepaperSection | Parsed from Introductory_composition.md by H2 heading |
| `REQ-` | Requirement | Parsed from verification_compiler_requirements.md |
| `CLAIM-` | Claim | Parsed from project_wiki/claims/*.md + source_to_claim_matrix rows |
| `SRC-` | Source | Parsed from project_wiki/sources/*.md |

## Edge Types

| Type | From → To | Meaning |
|---|---|---|
| `supported-by` | CLAIM → SRC | Source cited in support of this claim |
| `appears-in` | CLAIM → SEC | Claim text appears in this whitepaper section |
| `covers` | SEC → REQ | This section addresses this requirement |
| `cited-by` | SRC → CLAIM | Source is cited by this claim |

---

## Verification Query Packages (VQPs)

Three types of bounded queries, each designed to fit in one Gemini call:

### Type A — Citation Verification
**Question**: Does this source actually support this claim as stated in the whitepaper?

Input:
- `claim_text`: the claim as stated in the source_to_claim_matrix
- `source_content`: key content from the source note (project_wiki/sources/*.md)
- `support_type`: from the matrix (direct, analogy, empirical, etc.)
- `whitepaper_excerpt`: the paragraph in the whitepaper where this claim appears

Output schema:
```json
{
  "verdict": "pass|fail|uncertain",
  "confidence": 0.0-1.0,
  "rationale": "...",
  "what_source_actually_says": "...",
  "misrepresentation_found": true|false,
  "misrepresentation_detail": "..."
}
```

### Type B — Requirement Coverage
**Question**: Does the whitepaper adequately describe this requirement?

Input:
- `requirement_id`: e.g., "1.1 Node Types"
- `requirement_text`: full requirement + rationale
- `candidate_sections`: text of whitepaper sections that might address it

Output schema:
```json
{
  "verdict": "covered|partial|missing",
  "confidence": 0.0-1.0,
  "rationale": "...",
  "coverage_gaps": ["..."],
  "best_matching_section": "..."
}
```

### Type C — Orphan Detection
Derived mechanically (no Gemini call needed):
- Requirements with zero covering sections → FLAG
- Claims with no supporting source → FLAG
- Sources cited in whitepaper but not in source_to_claim_matrix → FLAG

---

## VRM Formula (Prototype)

```
citation_score = pass_citations / total_citations
coverage_score = covered_requirements / total_requirements
VRM = 0.5 × citation_score + 0.5 × coverage_score
```

Range 0.0–1.0. Breakdown by component is reported separately.

---

## File Layout

```
verification_prototype/
  PLAN.md                       # this file
  run.py                        # main orchestrator
  graph/
    schema.py                   # Node, Edge, Graph dataclasses
    builder.py                  # parse wiki + whitepaper → graph.json
    traverser.py                # graph → list of VQPs
  agents/
    gemini.py                   # submit VQPs to Gemini, parse structured JSON
  evidence/
    collector.py                # write results to data/results/
    reporter.py                 # VRM + markdown report
  prompts/
    citation_verification.txt   # Type A prompt template
    requirement_coverage.txt    # Type B prompt template
  data/
    graph.json                  # built artifact graph (output of builder)
    results/                    # one JSON per VQP result
```

---

## Implementation Phases

### Phase 1 — Schema (graph/schema.py)
- Node dataclasses: WhitepaperSection, Requirement, Claim, Source
- Edge dataclass: Edge(from_id, to_id, type)
- Graph: nodes dict + edges list, serialize to/from JSON

### Phase 2 — Builder (graph/builder.py)
1. Parse `Introductory_composition.md` by H2 headings → SEC nodes
2. Parse `verification_compiler_requirements.md` by subsections → REQ nodes
3. Parse `project_wiki/claims/*.md` → CLAIM nodes
4. Parse `project_wiki/sources/*.md` → SRC nodes (key_content = "Key Ideas" section)
5. Parse `source_to_claim_matrix.md` → CLAIM nodes + `supported-by` edges
6. Text search: find which SEC contains each CLAIM's key phrase → `appears-in` edges
7. Emit `graph.json`

### Phase 3 — Traverser (graph/traverser.py)
1. For each `supported-by` edge: emit Type A VQP
2. For each REQ node: collect candidate SEC nodes (text match), emit Type B VQP
3. Orphan detection (no Gemini needed): emit Type C findings

### Phase 4 — Gemini Agent (agents/gemini.py)
- Reuse `whitepaper/gemini_tools/gemini_client.py` pattern
- For each VQP: format prompt, call Gemini, parse JSON from response
- Save raw response + parsed result to `data/results/{vqp_id}.json`
- Handle API errors gracefully: mark as `uncertain` with error note

### Phase 5 — Report (evidence/reporter.py)
- Load all results from `data/results/`
- Compute VRM and component scores
- Generate `data/verification_report.md`:
  - Per-citation results table
  - Per-requirement coverage table
  - Orphan findings
  - Issues requiring whitepaper update
  - VRM score with breakdown
  - Learnings for whitepaper feedback

---

## Learnings Capture

During and after the run, note:
- Which claims have no source or weak source
- Which requirements are not described in the whitepaper at all
- Which citations are misrepresented (source says something different)
- Structural observations about running a verification compiler on prose vs. code
- Data structure concepts that should be added to the whitepaper

---

## Known Constraints

- Source notes in project_wiki/sources/*.md are summaries, not full texts. Gemini cannot access
  the original papers. Citation verification is therefore checking "does the summary accurately
  characterize the source?" not "does the primary text say this?"
- Requirements coverage is assessed by Gemini reading both the requirement and the whitepaper
  section text — no formal proof, just structured AI review.
- This is a prototype: DAG is hand-built from wiki data, not auto-extracted from a codebase.
  That's fine — Stage 2 automates graph construction.
