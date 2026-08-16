# Whitepaper Diagrams

Diagrams created in Excalidraw. Restore any diagram by using the checkpoint ID with the Excalidraw MCP tool (`restoreCheckpoint`).

---

## Diagram 1: The Artifact Graph

**Checkpoint:** `24df162c861a4a948d`

**Caption:** The verification compiler links a C codebase to every verification artifact through a hierarchical graph. Requirements trace downward to code units; code units link outward to tests, static analysis, and referenced specifications; tests produce results. Graph structure proves coverage: orphan code (no requirement link) and orphan requirements (no code link) surface as anomalies.

**Whitepaper section:** Section 6 — Verification Compiler Concept

**Key visual elements:**
- Three zones: Requirements (blue), Code Units (purple), Verification Evidence (green)
- Requirement hierarchy: System → HL → LL → Code Unit (solid arrows, traced-to)
- Code unit links: to tests and static analysis (solid), to datasheets (dashed, references)
- Results tied to code version (note at bottom of physical test result)
- Node colors: blue = requirements, purple = code, orange = tests, yellow = analysis, teal = specs, green = results

---

## Diagram 2: Verification Query Assembly

**Checkpoint:** `c48b56825f8e4537a2`

**Caption:** Graph traversal visits one code unit (`read_sensor()`) and collects all linked artifacts — the full requirement chain (SR-1 → HL → LL), tests, physical test evidence, and referenced specs. These are assembled into a single bounded verification query sized to fit within a model's context window. The query is submitted to a reviewer (LLM or human) and returns a structured result.

**Whitepaper section:** Section 6 — Verification Compiler Concept (traversal mechanism)

**Key visual elements:**
- Left: artifact graph excerpt with `read_sensor()` highlighted as the evaluated node
- Center: "traversal collects" arrow showing the collection mechanism
- Right: assembled Verification Query packet with labeled sections (Requirements / Code / Tests / Specs / Evaluation)
- Bottom: query submitted to "LLM or Human Reviewer" → "pass / fail / uncertain + confidence"
- Context window note: "~6-8K tokens"

---

## Diagram 3: Dual-Mode Operation

**Checkpoint:** `7abcccf0c8aa4ec9bc`

**Caption:** The same graph decomposition feeds two execution modes. In LLM mode (automated, CI/CD), queries are submitted to a model whose results are confidence-weighted by task-specific accuracy profiles. In human mode (final certification), identical queries are reviewed by human engineers using the same evidence schema. The two modes are interchangeable per node — any node reviewed by an LLM can be re-reviewed by a human, and vice versa. Both modes produce the same Structured Result format, which feeds the Evidence Graph and yields a composite Confidence Score.

**Whitepaper section:** Section 6 — Verification Compiler Concept (dual-mode) and Section 3 — Counterargument response

**Key visual elements:**
- Top: "Verification Queries (from graph traversal)" as source
- Two branches: LLM Mode (purple) and Human Mode (blue)
- Double-headed dashed arrow: "interchangeable per node"
- Both produce "Structured Result" boxes with identical schema (dashed center box)
- Converge to "Evidence Graph" (green)
- Output: "Confidence Score = results × accuracy × coverage × staleness"
- Right side: "graph structure independently proves scope completeness"

---

## Diagram 4: Cross-Standard Evidence Structure

**Checkpoint:** `b02a1cdf1520465682`

**Caption:** DO-178C (aerospace), ISO 26262 (automotive), and IEC 62443 (industrial/OT) all share the same structural pattern: tiered severity/security levels, defined verification objectives per level, and required evidence artifact types. None of the three standards specifies reviewer identity — only that evidence meets the objective. A verification compiler producing conformant evidence satisfies the standard's requirements by design.

**Whitepaper section:** Section 4 — Safety-Critical Engineering as Coordination Pattern, and counterargument response to Beningo moat 2 (certification)

**Key visual elements:**
- Three columns: DO-178C (blue), ISO 26262 (green), IEC 62443 (orange)
- Rows: standard name/domain, safety levels (DAL / ASIL / SL), evidence artifact types
- "Reviewer: NOT SPECIFIED" row in red for all three standards
- Green footer box: "Common Pattern — evidence objectives are defined, reviewer identity is not → verification compiler satisfies the standard by design"

---

## Diagrams To Add

- **Units of Intelligence comparison** — capacity/accuracy/adaptability table comparing human engineers, LLM agents, and specialized tools
- **Confidence Score decomposition** — visual formula showing how per-query results × accuracy profiles × coverage × staleness produce the composite score
- **Pipeline overview** — end-to-end flow from specification intake through graph construction, traversal, query evaluation, and evidence packaging
- **Natural language specification problem** — showing ambiguity and drift between English requirement, implementation, and verification evidence
