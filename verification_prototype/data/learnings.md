# Learnings from Running the Verification Compiler on the Whitepaper

Generated: 2026-05-19
Prototype run: 21 citation VQPs + 20 coverage VQPs + 1 orphan check
Verification agent: Gemini 2.5 Pro
VRM: 0.581

---

## 1. Whitepaper Content Gaps (Genuine Findings)

These are requirements that are defined in `verification_compiler_requirements.md` but are
not adequately described in the whitepaper. These should be added or expanded.

### Missing (no coverage in whitepaper):

**REQ-3-4: Conflict Resolution**
The whitepaper does not describe what happens when a human reviewer and LLM disagree on a query.
The requirement specifies: human result takes precedence; LLM result retained as "discrepant" with
explicit flag; disagreement rate feeds the model's accuracy profile recalibration.
→ Add a paragraph in the Verification Compiler concept section on conflict resolution workflow.

**REQ-3-5: Prompt Configuration Control**
The whitepaper does not mention that prompts are versioned artifacts. The requirements doc
has a detailed rationale (prompts are tool configuration analogous to DO-330 TOR scope).
→ Add one paragraph: "Prompts as versioned configuration — every prompt used in query assembly
has a unique version identifier recorded alongside model version in every result."

**REQ-4-1, REQ-4-2, REQ-4-3: Per-Query Confidence + VRM Formula + Model Accuracy Profiles**
The VRM is named and motivated in the whitepaper ("how ready is this codebase to be
verified?") but its composition is never explained. A reader cannot understand what VRM = 0.9
means without knowing:
  - Each query produces a confidence value from the model's task-specific accuracy profile
  - Queries are weighted by that profile (not a naive mean)
  - The VRM combines coverage fraction and mean weighted confidence
  - Task-specific accuracy profiles are maintained separately per task type (not global)

This is the most significant gap: the core output artifact (VRM) is not defined in terms
of its inputs. → Expand "Verification Readiness Metric" subsection with the formula and its
components.

**REQ-5-1: Immutable Evidence Records**
The whitepaper does not state that once a review result is written to the evidence graph,
it cannot be modified in place. This is important for certification auditability.
→ Add one sentence in the Artifact Graph section: updates create new versioned nodes, not
in-place modifications.

**REQ-6-1: Automation Bias Mitigation (partially missing from traversal)**
The whitepaper DOES discuss evidence-first presentation and canary queries (in the Regulatory
Pathway / Automation Bias section). However, the traversal prototype missed this because:
(a) the section text was truncated at 4000 chars and the content appears later in the section,
(b) the candidate section mapping didn't link REQ-6-1 to the correct H3 subsection.
→ This is primarily a prototype limitation, not a whitepaper gap. But the whitepaper could
make the connection to REQ-6-1 more explicit.

### Partially covered (needs more detail):

**REQ-1-3: DAG Structure Invariant** — paper mentions DAG concept but not why it's required
(bounded traversal, termination proof) nor that cycles are rejected at construction time.

**REQ-2-1: Context-Window Bounded Queries** — the crucial sentence about query sizing is
INCOMPLETE in the whitepaper: "a self-contained bundle sized to fit within a model's context
window" — the second half of the sentence appears to have been cut. Fix this.

**REQ-3-2: Structured Result Format** — whitepaper mentions "structured result" concept but
never lists the fields. A reader has no idea what "structured" means in practice (verdict,
confidence, rationale, evidence citations, reviewer ID, timestamp, code version).

---

## 2. Citation Source Mapping Issues (Builder-Level Findings)

Three of the five citation "fails" are builder artifacts — the source resolution logic
incorrectly mapped claims to wrong source nodes:

**Finding A**: Claims attributed to "Rierson" in the source_to_claim_matrix were sometimes
resolved to the NASA Jacklin source node because the resolver matched on "NASA" keywords.
- Affected: DO-178C verbatim quote claim, human reviewer qualification claim
- Fix: add a priority rule that "Rierson" keyword maps explicitly to SRC-rierson-do178c

**Finding B**: The LLM overcorrection claim (arXiv:2603.00539) was resolved to the
requirements-engineering-nl-ambiguity source because the resolver matched on "requirements".
- Fix: arXiv IDs in the source field should be matched directly as SRC slugs

**Finding C**: The assume-guarantee reasoning claim (Cobleigh et al.) was resolved to
NASA Jacklin because of "NASA NTRS" appearing in the evidence string.
- Fix: The Cobleigh source needs its own SRC-cobleigh-assume-guarantee node

**Structural lesson for the real VC**: Source resolution is non-trivial. When source identifiers
are natural-language labels (not stable IDs), ambiguous matching produces incorrect edges.
The real VC should use stable, machine-readable source IDs (e.g., DOI or arXiv ID as primary
key), not resolved from free-text labels.

**One genuine citation issue**: The "Certification standards define evidence objectives"
claim is mapped to AS9100 as supporting source. The AS9100 source note itself says AS9100 is
"an organizational-quality analogue, not a software verification standard." Gemini correctly
flagged that AS9100 doesn't support the specific claim about evidence objectives vs. reviewer
identity. The correct sources for this claim are Rierson (DO-178C independence definition)
and ISO 26262 / IEC 62443 (ASIL/SL levels define rigor, not reviewer method).

---

## 3. Structural Observations — Running VC on Prose vs. Code

### Observation 1: Prose claims are harder to scope than code units
In the real VC, each "code unit" is a function with clear boundaries. In prose, a "claim"
is a sentence or paragraph that bleeds across sections. The graph builder had to introduce
the CLAIM_SECTION_HINTS dict to manually map claims to sections — exactly the kind of
manual work that Stage 2 would automate for code via AST parsing.

### Observation 2: The "appears-in" edge is the hardest to build automatically
Citation markers in text provide a heuristic, but it's brittle. For code, this is equivalent
to identifying which function a requirement maps to — which AST parsers handle reliably.
For prose, there's no AST. The Gemini review team correctly identified this as the critical
risk, and it proved true: manual hints were needed for 60%+ of claims.

### Observation 3: Node text truncation hides content
Capping section text at 4000 chars caused Gemini to miss content present in longer sections.
This is the "context window as design primitive" problem in miniature: if you give the agent
too little context, it misses things; if too much, reasoning quality degrades.
→ For long sections, the traverser should split at H3 boundaries and emit separate VQPs
per sub-section, not one VQP with truncated H2 content.

### Observation 4: Two kinds of "missing" requirements
Type B results showed two distinct failure modes:
(a) **Genuinely missing** — the whitepaper doesn't describe this concept at all (REQ-4-1, 4-2, 4-3)
(b) **Hidden by traversal scope** — the content exists in the whitepaper but in a sub-section
    that wasn't mapped to the requirement (REQ-6-1 automation bias)
This distinction matters for the real VC: (a) is a traceability failure; (b) is a coverage
analysis failure that the graph invariant check should catch.

### Observation 5: The VRM formula for prose is different from code
For code verification, VRM weights:
  - coverage fraction (all code units processed)
  - per-query confidence (task-specific model accuracy)
  - evidence staleness (how old are test results)

For whitepaper verification, the prototype used:
  - citation_score (0.76) × 0.5
  - coverage_score (0.35) × 0.5

The resulting VRM = 0.581 reflects that citations are mostly good but 7/20 requirements are
missing from the whitepaper entirely. That's an informative signal. However, the 50/50
weighting is arbitrary — in a real deployment, weights would be calibrated to the specific
verification objectives (e.g., citation accuracy might matter more for a certification submission).

### Observation 6: Requirements document ≠ whitepaper sections (not 1:1)
The requirements doc has 20 sub-requirements across 6 sections. The whitepaper has 12 H2
sections and ~20 H3 subsections. The mapping between them is many-to-many and non-obvious.
For the real VC, this is the "requirement to code unit" traceability problem. The solution
there (explicit traceability links in a requirements database) is cleaner than keyword matching.
→ For Stage 2, the whitepaper should have explicit requirement tags (like `[REQ-3-5]` anchors)
that enable exact traceability. Or the requirements document should explicitly reference
which whitepaper section addresses each requirement.

---

## 4. Concepts to Feed Back into the Whitepaper

### Add to "Verification Readiness Metric" subsection:
Expand to include:
1. The VRM formula: `VRM = Σ(result_i × confidence_i × coverage_i) / total_scope`
   or equivalently broken down into component scores
2. Per-query confidence values derived from task-specific model accuracy profiles
3. Coverage fraction as a distinct component
4. Breakdown by component required (not just a single number)
5. Staleness factor for evidence tied to older code versions

### Add to "Concept: Verification Compiler" section:
1. One paragraph on prompt versioning as part of configuration control
2. One paragraph on conflict resolution (human overrides LLM; discrepant results retained)
3. One sentence on immutable evidence records (updates create new nodes, not in-place edits)

### Add to "Artifact Graph" subsection:
1. Explicitly state the graph is a DAG and why (bounded traversal, termination)
2. State that cycles are detected and rejected at construction time

### Fix incomplete sentence:
In "Graph Traversal as Decomposition":
> "a self-contained bundle sized to fit within a model's context window"
The text appears to be missing the rest of this sentence. Complete it.

---

## 5. New Concepts Discovered by Running the Prototype

**Claim-to-section traceability is a first-class problem**: In the VC concept, the DAG links
requirements to code units explicitly. The prototype revealed that for prose, this link is
just as important and just as hard. The whitepaper should acknowledge that for the VC concept
to work on documents (not just code), a similar explicit tracing would be needed.

**Source resolution needs stable IDs**: The prototype used natural-language source names and
keyword matching. This produced 3/5 citation failures that are actually builder errors.
The whitepaper's source_to_claim_matrix should use stable machine-readable IDs (DOI, arXiv ID)
as primary keys, not prose labels. This is analogous to using file paths + line numbers for
code units rather than function name strings.

**Sub-section granularity matters more than section-level coverage**: The H2-level section
mapping was too coarse. Requirements that ARE covered in H3 subsections were missed because
the H2 traversal didn't reach the right sub-section. The real VC should build the graph at
function granularity, not file granularity — this prototype confirms why.
