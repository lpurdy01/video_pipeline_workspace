# Verification Compiler Requirements

## Purpose

This page defines the system requirements for the verification compiler as understood at the end of Stage 1 research. These requirements are the primary output of Stage 1 and the input to Stage 2 prototype work.

Requirements are organized by subsystem. Each requirement has a rationale and a source reference where one exists.

---

## 1. Artifact Graph Requirements

### 1.1 Node Types

The system shall support the following node types in the artifact graph:

- **Source code unit**: a function, module, or subsystem of a C codebase, identified by file path, function name, and version hash
- **Requirement**: a natural-language requirement at any level (high-level, low-level, derived), with a stable identifier
- **Interface specification / datasheet**: an external document describing the behavior of hardware or software interfaces
- **Static analysis result**: output from a tool (memory safety, timing, coverage), linked to a specific code version and tool configuration
- **Test artifact**: a test specification, test procedure, or test case
- **Test result**: a recorded pass/fail outcome linked to a test artifact and a specific code version
- **Physical test result**: a test result generated from hardware-in-the-loop or physical system testing, with version and conditions documented
- **Review record**: a structured output from a model or human reviewer, attached to a verification query
- **Certification evidence package**: a collected set of records structured for certification body review
- **SourceRegionNode**: a machine-addressable pointer to a specific region within a reference document (standard, datasheet, ICD, whitepaper). Primary key: `URI_Locator` — a stable, hierarchically-scoped identifier (e.g., `do:DO-178C-2011#6.3.b`, `arxiv:2603.00539#sec:3`, `git-blob:<hash>:<path>#L10-L45`). Contains `Content_Hash` (SHA-256 of region text — changes when text changes) and `Text_Payload` (the actual text injected into VQPs at assembly time). A content hash change invalidates all `supports-claim` edges from that region.
- **ModelAccuracyProfile**: a per-`(Model_ID, Prompt_Version, Task_Type)` calibration record storing empirical accuracy statistics: `TP, FP, TN, FN`. Initialized with a pessimistic 50/50 Beta prior and updated by human override events and canary query results. Computes `PPV = TP/(TP+FP)` (Bayesian-smoothed) and `NPV = TN/(TN+FN)`, used for Model Suitability threshold checks (REQ-4-3) and per-result confidence annotation.

**Rationale**: The artifact types listed mirror the life-cycle data categories described in DO-178C (via NASA Jacklin and FAA AC 20-115D) and the evidence artifact categories implied by ISO 26262 NHTSA assessments. Coverage across all node types is necessary for the traversal to produce complete verification queries. SourceRegionNode and ModelAccuracyProfile were identified as necessary additions in the Stage 1 practice prototype (2026-05-19): source resolution failures due to natural-language labels and calibration gaps in VRM weighting revealed that stable region IDs and empirical accuracy profiles are structural requirements, not implementation details.

### 1.2 Edge Types

The system shall support the following typed edge relationships:

- **traces-to**: requirement → child requirement, requirement → code unit
- **verified-by**: code unit → test artifact, requirement → test artifact
- **has-result**: test artifact → test result
- **analyzed-by**: code unit → static analysis result
- **references**: code unit → interface specification or datasheet
- **reviewed-by**: any node → review record
- **version-tied**: test result or physical test result → specific code version artifact
- **supports-claim**: CLAIM → SourceRegionNode. Contains `Selector_Logic` (how to extract text from the region node for VQP assembly). Both `Source_Version_Hash` and `Target_Version_Hash` are recorded on this edge; a mismatch between stored hash and current SourceRegionNode content_hash marks the edge as stale and triggers human re-confirmation before the VQP can be assembled.
- **traces-to / verified-by**: shall also carry `Source_Version_Hash` and `Target_Version_Hash` to support staleness discount calculation in the VRM (REQ-4-2).

**Rationale**: Typed edges allow the traversal to construct meaningful verification queries and to detect orphan nodes (code with no requirement link, requirements with no code link). Version hashes on evidence edges enable the VRM staleness discount — evidence tied to a different code version than the current artifact is discounted, not simply excluded. This preserves audit history while correctly weighting evidence recency.

### 1.3 DAG Structure Invariant

The artifact graph shall be a **Directed Acyclic Graph (DAG)**. Cycles in the graph are forbidden and shall be detected and rejected at construction time.

**Rationale**: The graph traversal algorithm assumes a DAG structure to produce bounded, terminating verification queries. A cycle would cause the traversal to loop indefinitely and produce unbounded query packages. The DAG invariant is also what makes graph traversal deterministic — the same traversal always visits nodes in the same topological order, which is required for the deterministic query assembly claim.

### 1.4 Completeness Invariants

The system shall enforce the following graph invariants and surface violations as anomalies:

- Every source code unit that is in scope shall be reachable from at least one requirement via traces-to edges
- Every requirement shall be linked to at least one code unit or child requirement
- Every test result shall be tied to a specific code version hash

**Rationale**: Orphan code (no requirement link) and orphan requirements (no code link) are equivalent to DO-178C traceability failures and indicate verification scope gaps.

---

## 2. Decomposition and Query Requirements

### 2.1 Context-Window Bounded Queries

The system shall decompose verification work into queries such that each query fits within the configured context window of the assigned model unit.

Each query shall include:
- The source code unit(s) under evaluation
- All requirements reachable from the code unit via parent traces-to edges
- All test artifacts and results linked to the code unit
- Any interface specifications or datasheets linked to the code unit
- Physical test evidence linked to the same code version, if present

**Rationale**: The context window is the design primitive — each query must be self-contained and bounded so that a model can reason over it reliably without truncation. This parallels how human reviewers receive bounded review packages.

### 2.2 Traversal Completeness

The system shall guarantee that every in-scope source code unit is included in at least one verification query.

The traversal algorithm and its coverage shall be inspectable independently of model results — a reviewer shall be able to confirm that the full scope was evaluated from the graph structure alone.

**Rationale**: Provable decomposition is a core property. The graph structure is the proof that no code was omitted. This is analogous to requirements traceability analyses under DO-178C.

### 2.3 Version Consistency

The system shall reject physical test evidence that is not tied to the same code version as the source code unit under evaluation.

**Rationale**: Physical test results derived from a different code version do not constitute evidence for the current version's behavior.

---

## 3. Reviewer Interface Requirements

### 3.1 Structured Query Format

Each verification query shall be rendered in a structured format that is compatible with both LLM and human review. The format shall include clearly delimited sections for: code, requirements, tests, results, and evaluation instructions.

### 3.2 Structured Result Format

Each review result shall be a structured record containing:
- Node identifier(s) evaluated
- Reviewer type (model or human) and reviewer identifier (model version + configuration, or person)
- Result: pass / fail / uncertain
- Confidence value (0–1 for model results; high/medium/low for human results)
- Rationale: a written explanation of the result
- Evidence citations: specific lines, sections, or artifacts that support the result
- Review timestamp and code version at time of review

**Rationale**: Structured results are auditable. They can be challenged, re-reviewed, or aggregated into a confidence score. Unstructured outputs (chat-style answers) are not admissible as verification evidence.

### 3.3 Dual-Mode Interoperability

The system shall support both LLM review mode and human review mode using the same query format and result schema.

A human reviewer shall be able to complete any query that was previously completed by a model, using the same input, and the result shall enter the evidence graph in the same structure.

**Rationale**: Dual-mode interoperability is what makes the system useful for both continuous integration (LLM mode) and final certification (human mode). The decomposition does not change — only the reviewer identity changes.

### 3.3b LLM Result Status and Determinism

LLM verification results shall be classified as **developmental results**, not certification evidence, unless explicitly promoted by a human reviewer.

- The graph decomposition and query assembly are deterministic: the same artifact graph state always produces the same set of queries with the same content.
- LLM review mode is intended for development-cycle passes (e.g., nightly CI), providing continuous feedback to developers without requiring human review on every iteration.
- For final certification, human reviewers evaluate the same deterministically-generated queries using the same evidence packages. Human results are the certification evidence; LLM results during development are feedback that may inform but do not substitute for that final pass.
- All LLM results shall be logged with model identifier, prompt version, and output. These logs are retained as developmental history but are not part of the certification evidence package unless a human reviewer explicitly confirms and promotes the result.

**Rationale**: The non-determinism concern raised by DO-330 does not apply to the certification evidence because certification evidence is always produced by human reviewers on the same deterministic query set. The LLM's role in the certification pathway is to reduce the cost and cycle time of development-phase verification — giving developers immediate, structured feedback on every commit — while ensuring the final certification pass is fully human. This is the correct architectural response to DO-330 scrutiny: not claiming the LLM is deterministic, but ensuring that the deterministic elements (graph structure, query assembly) and the human-reviewed final pass are what constitute the certification artifact.

### 3.5 Prompt Configuration Control

The system shall treat prompt configurations as versioned configuration data, subject to the same configuration management as source code.

Specifically:
- Every prompt used to generate a verification query submission shall have a unique version identifier (e.g., a hash or semantic version)
- The prompt version shall be recorded in every review result alongside the model identifier
- Changes to prompt text shall require a new prompt version — in-place editing of active prompts is not permitted
- The system shall be able to reproduce any historical verification query submission exactly, given the artifact graph state, code version, and prompt version at the time of submission

**Rationale**: Under DO-330 Tool Qualification, the Tool Operational Requirements (TOR) must specify the tool's operating conditions, including its configuration. Prompts are a form of tool configuration: they determine what the model is instructed to do, what output format is required, and how uncertainty is expressed. A result produced with one prompt version is not comparable to a result produced with a different prompt version for the same query. Versioned prompts are the minimum necessary for evidence records to be reproducible and auditable.

### 3.4 Conflict Resolution

When a query has been evaluated by both a model unit and a human reviewer and the results disagree:

- The human result shall take precedence in all confidence calculations and evidence packages.
- The model result shall be retained in the evidence record as a discrepant result, with the disagreement flagged explicitly.
- The disagreement shall be recorded as an input to the model's task-specific accuracy profile, triggering a recalibration event if the disagreement rate for that task type exceeds a configured threshold.

**Rationale**: Conflicts between LLM and human review are expected during early deployment. They are valuable signal for model qualification, not errors to be suppressed. Retaining both results preserves auditability; giving precedence to the human result ensures safety-conservative behavior.

---

## 4. Confidence Score Requirements

### 4.1 Per-Query Confidence

The system shall record a confidence value for each review result. For model results, this value shall be derived from the model's task-specific accuracy profile for the relevant task type.

### 4.2 Verification Readiness Metric (VRM) Formula

The system shall compute the VRM as follows:

```
C_v(i) = Σ_k w_k × I_k × S_k                   (vertical evidence completeness for requirement i)

VRM = Σ_i C_v(i) / N_total                      (sum over all requirements in scope; unevaluated requirements contribute 0)
```

Where:
- `w_k` = weight for evidence type k (requirement link, test artifact, test result, static analysis). Weights are configurable per deployment.
- `I_k` = binary existence indicator for evidence type k at requirement i
- `S_k` = staleness discount ∈ [0.0, 1.0]. S_k = 1.0 if evidence is tied to current code version; S_k = 0.0 if AST/content has changed since evidence was created.
- `N_total` = total requirements in scope. Requirements that have not yet been evaluated contribute C_v(i) = 0, so the formula naturally penalizes unevaluated scope.

The horizontal coverage fraction `C_h = N_eval / N_total` is surfaced separately on the dashboard as the completeness indicator — it shows what fraction of scope has been touched independently of evidence quality. The score shall be presented with a breakdown by component — aggregate VRM, C_h, and per-requirement C_v(i) values — so human reviewers and certification bodies can inspect coverage and completeness independently.

**Model Suitability (separate from VRM)**: Model accuracy is tracked as a separate indicator, not as a VRM multiplier. A model's task-specific PPV and NPV are compared against a project-configured minimum suitability threshold. A model falling below the threshold for a task type is ineligible for LLM review mode for that type until recalibrated. VRM describes *what has been reviewed and how completely*; Model Suitability describes *whether the reviewer is reliable enough to use*. These are distinct questions and must not be conflated in a single composite.

### 4.3 Model Accuracy Profile and Model Suitability Threshold

The system shall maintain a ModelAccuracyProfile node for each unique `(Model_ID, Prompt_Version, Task_Type)` triple. The profile shall record:
- `Model_ID`: the specific model version identifier (e.g., `gemini-3.1-pro-preview`, `claude-sonnet-4-6`)
- `Prompt_Version`: the versioned prompt configuration (see REQ-3.5) used when the results were produced
- `Task_Type`: fine-grained task label (e.g., `citation_verification`, `requirement_coverage`, `interface_constraint_check`)
- `TP, FP, TN, FN`: empirical confusion matrix values
- `Prior_Alpha, Prior_Beta`: Beta distribution prior (default: 1.0/1.0 — uniform; pessimistic deployments may use 1.0/10.0)
- Derived: `PPV = TP/(TP+FP)`, `NPV = TN/(TN+FN)` (Bayesian-smoothed)
- `Sample_Size`: number of queries contributing to the current empirical estimates
- `Profile_Version` and `Last_Updated` timestamp

Profiles shall be updated by two mechanisms:
1. **Human override**: when a human reviewer disagrees with a model result on a completed VQP, the disagreement is recorded against the profile for that `(Model_ID, Prompt_Version, Task_Type)` combination
2. **Canary queries**: queries with known ground-truth answers inserted into the evaluation stream to continuously probe model accuracy without requiring full human review of every query

The derived PPV and NPV are used in two ways: (a) as inputs to the **Model Suitability threshold check** — a model falling below the project-configured minimum PPV for a task type is ineligible to operate in LLM review mode for that type until recalibrated; (b) as per-result annotations surfaced alongside model results to inform human review prioritization. The asymmetric overcorrection pattern [arXiv:2603.00539, 2026] — models over-flag correct code more than they miss bad code — is captured by reporting separate PPV and NPV rather than a single accuracy number.

**Rationale**: Model accuracy is task-specific, not global. A model may have high PPV on citation verification but low PPV on interface constraint checking. Model Suitability is the gate that protects VRM signal quality — a model below threshold for a task type should not be generating results that enter the VRM numerator for that task type, as they degrade rather than improve the pre-screen signal.

---

## 5. Auditability and Evidence Requirements

### 5.1 Immutable Evidence Records

Once a review result is written to the evidence graph, it shall not be modified in place. Updates shall create new versioned records.

**Rationale**: Immutability is required for certification auditability. Modifying historical records would undermine the evidentiary chain.

### 5.2 Full Provenance

Every node in the evidence graph shall have recorded provenance: who or what created it, when, with what inputs, and against which code version.

### 5.3 Exportable Evidence Package

The system shall be able to export a structured evidence package for a specified scope (e.g., a requirement subtree or a code module), containing: all verification queries, results, confidence values, rationales, and graph coverage proof for that scope.

**Rationale**: Certification bodies and human reviewers need a structured, navigable evidence set. The evidence package is the primary artifact the system produces for external use.

---

## 6. Process Assurance Requirements

### 6.1 Automation Bias Mitigation

The system shall support process-level measures to mitigate automation bias — the risk that human reviewers become less rigorous when reviewing code that an LLM has already returned a "pass" verdict on.

The system shall provide:
- For each human-reviewed query, the full evidence package (code, requirements chain, test results, static analysis) shall be presented to the reviewer before any LLM verdict is revealed, if a prior LLM result exists for that query.
- Aggregated disagreement rates between LLM verdicts and human verdicts shall be reportable by reviewer, by task type, and by time period, so that systematic patterns can be detected.
- The confidence score breakdown shall always show the component inputs (coverage, accuracy profiles, staleness) independently, not only the aggregate — preventing the aggregate from being treated as a certification proxy.

**Rationale**: DO-330 TQL-5 qualification and the associated process assurance argument require that human review remains effective. A tool whose LLM outputs consistently prime human reviewers toward acceptance, regardless of accuracy, would undermine the independence and effectiveness of human review. This is the strongest regulatory concern about the architecture and must be addressed at the process level.

---

## 7. Source Region Addressing Requirements

### 7.1 Stable Region Identifiers

Every reference document used as evidence shall have its cited regions identified by a stable, machine-readable `URI_Locator`. The identifier shall encode the document identity, edition, and the precise region within it.

Three tiers of addressing are recognized, in order of stability:

**Tier 1 — Heading-slug IDs** (controlled documents, e.g., this whitepaper):
- Format: `doc:<doc-id>#H<level>:<heading-slug>`
- Example: `doc:whitepaper-v0.2#H2:concept-verification-compiler/H3:graph-traversal`
- Generated from: Markdown heading hierarchy. GitHub auto-generates these anchors.
- Stability: fragile if heading text changes. Acceptable for internally-controlled documents where changes are tracked.

**Tier 2 — Section-number IDs** (engineering standards, ICDs, datasheets):
- Format: `doc:<doc-id>#<section-number>`
- Example: `doc:DO-178C-2011#6.3.b` or `doc:ICD-001-rev-C#3.2.1.4`
- Stability: section numbers rarely change across minor document revisions. Content hash detects text changes within a stable section number. Engineers already cite this way — adoption cost is zero.
- This is the correct tier for real VC deployments against engineering standards.

**Tier 3 — Formal standard citation format** (legal/regulatory documents):
- Format: `std:<standard-id>:<part>:<section>:<para>:<subpara>`
- Example: `std:14-CFR:25.1309:b:1:ii` or `std:ISO-26262:2018:part-6:8.4.3`
- Stability: formally stable; can be resolved against official text databases.

### 7.2 SourceRegionNode Schema

Each SourceRegionNode shall contain:
```
id:           URI_Locator (primary key — unique, stable, hierarchically scoped)
doc_id:       parent document identifier
section_path: e.g., "6.3.b" or "H2:concept-vc/H3:traversal"
title:        human-readable section title
body:         actual text of the region (injected into VQPs at assembly time)
content_hash: SHA-256 of body (changes when text changes, even if section_path is stable)
parent_id:    URI_Locator of parent region (for hierarchy navigation)
doc_version:  document edition string
```

### 7.3 VQP Assembly from SourceRegionNodes

At VQP assembly time, the resolver shall fetch the `body` of each referenced SourceRegionNode and inject it directly into the VQP prompt — not just a citation label. The VQP must contain the actual text being evaluated, not a reference to it.

If a SourceRegionNode's `content_hash` has changed since a `supports-claim` edge was created, the edge shall be marked stale and the VQP shall not be assembled until a human confirms the citation still holds for the updated text.

### 7.4 Document Addressability Requirements

For a document to be VC-addressable, it shall have:
1. **Atomic, named units**: each verifiable claim shall reside in exactly one addressable region
2. **Stable IDs**: the region's identifier shall not change unless content is intentionally revised
3. **Content hash**: to detect silent text changes within a stable ID
4. **Hierarchy**: parent-child relationships enabling the traversal to navigate document structure

Technical engineering standards (DO-178C, ISO 26262, ICDs) satisfy (1), (2), and (4) natively. The VC adds (3). For the whitepaper and other informal documents, explicit section anchors shall be added (e.g., `## Section Title {#sec:unique-id}` in Pandoc Markdown, or AsciiDoc `[[anchor]]`).

---

## 8. Known Architectural Challenges (Deferred)

The following architectural problems are recognized as necessary for a production VC but are out of scope for the current Stage 2 practice implementation. They are documented here as constraints on future design.

### 8.1 Graph Invalidation Cascade

When a source code unit changes, which VQPs must be re-evaluated? A naive implementation re-runs all VQPs on every commit (wasteful but correct). A production implementation requires node-level version hashes and invalidation propagation rules up and down the DAG — so that only queries whose inputs changed are re-submitted.

**Current scope**: re-run all VQPs on every evaluation pass. Smart invalidation is a future feature.

**Future design constraint**: invalidation rules must be conservative — when in doubt, invalidate. A stale result that is not re-evaluated is worse than an unnecessary re-evaluation.

### 8.2 Multi-Unit and Emergent Requirements

Some requirements span many code units and cannot be assigned to a single VQP — timing budgets, memory limits, scheduling deadlines, system-level safety properties. These requirements emerge from the behavior of the whole, not any one function.

**Current scope**: note as architecture challenge. Multi-unit requirements are not required for the Stage 2 C-code prototype.

**Likely solution path**: System-Level VQPs that consume static analysis tool summary outputs (timing analyzer results, memory profiler summaries) rather than raw multi-function source code. The static analysis tool does the cross-unit reasoning; the VQP verifies that the tool's output satisfies the requirement.

### 8.3 Conflict Resolution Economics (Retroactive VRM Updates)

When a human reviewer overrides an LLM result, should the VRM score retroactively update for all past evaluations of the same query? This requires:
- Version tracking on all VRM computations
- Propagation of profile changes to historical VRM values
- A decision about how long a human override stands before requiring re-evaluation

**Current scope**: out of scope. VRM is computed fresh from current results.

**Future design constraint**: the clean solution requires the graph invalidation infrastructure from 8.1. A human override should stand as long as nothing relevant to that VQP has changed. When any input to the VQP changes (code, requirements, prompt version, model version), the override is invalidated and re-evaluation is required.

### 8.4 VQP Size Limits and Evidence Decomposition

When a code unit implements many requirements or references voluminous specifications, the assembled VQP may exceed the context window of the assigned reviewer. Evidence truncation to meet size limits is **explicitly forbidden** — a requirement evaluated against incomplete evidence is unverified and cannot enter the certification evidence record.

Three strategies address oversized VQPs, in order of architectural soundness:

1. **Hierarchical VQP splitting**: a parent VQP is split into child VQPs each covering a subset of requirements; child results are composed into a parent verdict via a declared aggregation rule. Soundness requires that child VQPs be logically independent — if sub-requirements interact, split evaluation may miss integration-level failures.
2. **Tool-summary nodes**: large deterministic evidence sets are processed by a qualified deterministic tool emitting a structured summary (e.g., a test runner emitting pass/fail counts). The summary node carries a content hash linking it to the raw artifacts. LLM-generated summaries are explicitly excluded — LLM summarization introduces hallucination risk into the evidence base.
3. **Proof composition (assume-guarantee)**: engineers define explicit interface contracts at component boundaries; each component is verified against its local contract, and a parent VQP verifies that composed contracts satisfy the parent requirement.

Emergent system properties (end-to-end timing, memory partitioning safety, freedom from priority inversion) cannot be verified by leaf-node examination regardless of VQP size. These require Whole-Program Analysis (WPA) tools; the VC consumes WPA tool outputs as first-class DAG evidence nodes, and the corresponding VQP verifies that the WPA output satisfies the requirement's stated bound.

**Current scope**: VQP size is bounded by graph construction discipline. Hierarchical splitting and tool-summary nodes are the near-term implementation paths. Proof composition and WPA integration are Stage 2 targets.

### 8.5 DAG Cycle Detection and Requirements Refactoring

Requirements with mutual dependencies create cycles in the traceability graph. The VC hard-rejects all cycles at graph construction time — cyclic traceability is circular reasoning and causes traversal to fail to terminate.

Three refactoring patterns resolve the common categories:
1. **Elevation**: move the shared constraint to a new parent requirement; both dependent requirements trace to it as children and are verified independently.
2. **Interface contract nodes**: introduce an explicit contract node specifying the boundary obligation; each module's requirement assumes the contract and guarantees its output (analogous to assume-guarantee decomposition).
3. **State separation**: split temporally coupled requirements by time step, since state T_n informing state T_{n+1} flows in one direction only.

A cycle that cannot be resolved by these patterns signals a software architecture that is not decomposable for independent verification. The VC surfaces it but cannot resolve it.

**Current scope**: Cycles are detected and rejected at graph build time. Refactoring guidance is a tool feature for future implementation.

### 8.6 Data and Control Coupling Coverage (DCCC)

DO-178C Section 6.4.4 requires confirmation that requirements-based testing has exercised the data and control coupling between code components — inter-module dependencies where one component reads data set by another, or where one component influences another's execution path. DCCC is an integration-level objective required for DAL A–C; it can only be observed on integrated code and explicitly focuses on interactions across module boundaries.

The Verification Compiler's Stage 1 per-leaf-node VQP structure is, by construction, blind to cross-module coupling paths. DCCC does not invalidate the VC architecture but identifies a complementary verification activity outside Stage 1 scope. Specialized DCCC tools (VectorCAST/Coupling, LDRA, Rapita RapiCoupling) generate structured coupling analysis reports; these enter the VC artifact graph as integration-level `analyzed-by` evidence nodes. An integration-level VQP then verifies that the report confirms all required coupling paths are covered.

**Current scope**: DCCC is an identified gap in Stage 1. Integration-level VQPs consuming DCCC tool reports are a Stage 2 target.

### 8.7 Object Code Verification

DO-178C Section 6.4.4.e requires verification that the compiled binary faithfully represents the source code. This is a separate objective from source-level verification. Where a qualified compiler is not used, OCV requires reviewing object code against source to confirm no spurious code was introduced and no required behavior was eliminated by compiler optimization.

This objective is out of the Verification Compiler's scope. Qualified compiler pathways (DO-178C Section 12.2) and dedicated OCV tools address this obligation. The VC architecture accepts OCV tool outputs as first-class evidence nodes using the same `analyzed-by` edge pattern as DCCC and static analysis; the relevant VQP verifies that the OCV result confirms no deviation between source and object code for the unit under review.

**Current scope**: OCV is out of Stage 1 scope. The architecture is designed to receive OCV evidence as graph nodes in Stage 2 certification-tier integration.

---

## 9. Non-Goals and Boundaries (Stage 2 Prototype)

The Stage 2 prototype is not required to:

- Achieve regulatory certification under DO-178C, ISO 26262, or IEC 62443
- Handle languages other than C
- Automate the construction of the artifact graph (manual linking is acceptable in Stage 2)
- Replace human review for any final certification decision
- Handle formal verification or proof generation (static analysis tools handle this; the compiler consumes their results)

The prototype shall demonstrate the core loop: ingest a small linked C codebase, traverse the graph, generate structured verification queries, submit to a model, collect structured results, compute a confidence score, and export an evidence package.

---

## Open Questions

- What is the minimum viable graph schema for the Stage 2 prototype? (Likely: source code unit + requirement + test result + SourceRegionNode for requirements citations)
- What static analysis tools should be integrated first? (Memory safety via valgrind/AddressSanitizer, coverage via gcov, or something else?)
- How should staleness weights `w_k` be calibrated for the Stage 2 deployment context? (Uniform weights are a reasonable starting point; empirical calibration comes later.)
- How should the Stage 2 prototype bootstrap ModelAccuracyProfile? (Canary queries with known ground-truth answers on the target codebase, or cross-validation on a labeled subset?)
- What model(s) should be used for the prototype evaluation? (gemini-3.1-pro-preview with HIGH thinking established as default for review; needs benchmarking for task-specific accuracy profiles)

*Resolved from Stage 1 practice run:*
- ~~What is the right confidence score formula?~~ → VRM formula now specified in REQ-4.2
- ~~How should the system handle emergent multi-unit requirements?~~ → Deferred to REQ-8.2; static analysis tool output is the likely solution path
- ~~Should graph invalidation be incremental?~~ → Deferred to REQ-8.1; wasteful full re-run acceptable for Stage 2
