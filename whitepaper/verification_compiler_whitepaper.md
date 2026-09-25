# Bounded LLM Review for Continuous Verification

Subtitle: A Graph-Decomposition Architecture for Safety-Critical Software

Version: 1.0 public release, August 2026

## Introduction

Software teams have continuous integration for builds and tests. Nobody has continuous integration for verification — the question of whether a codebase satisfies its requirements is answered once, at the end, expensively. The **Verification Compiler** addresses this gap: a hierarchical artifact graph that decomposes verification obligations into bounded, independently-auditable queries, each producing a structured result that feeds a **Verification Readiness Metric (VRM)** on every commit. The VRM answers, continuously: *how ready is this codebase to be verified against its requirements?*

The system is designed so that the same architecture serving development-cycle feedback also has a clear path to formal certification. The same DAG structure, the same query packages, and the same evidence schema that drive nightly CI pre-screening can be reviewed by qualified human engineers for a DO-178C, ISO 26262, or IEC 62443 certification pass. This is not a coincidence of design — it is the point. Teams that do not need formal certification get tractable, continuous verification readiness feedback. Teams that do need it have an architecture that does not require a redesign.

This paper argues that the structural principles which make human verification rigorous — hierarchical traceability, bounded reviewable tasks, interchangeable reviewers, and evidence-based confidence — can be used to organize model units into a verification workflow that is neither a black box nor a replacement for human judgment. Models are not asked to certify software; they are asked to evaluate bounded, well-specified questions with all relevant evidence in scope. Structured outputs, task-specific accuracy profiles, dual-mode human/LLM interchangeability, and graph-provable completeness are each a direct response to a specific LLM failure mode.

The argument proceeds as follows. Section 1 motivates the problem: why verification is expensive and where the cost comes from. Section 2 frames units of intelligence — humans, models, tools — as comparable entities with different capacity, accuracy, and qualification properties. Section 3 shows that safety-critical engineering standards are themselves coordination patterns for limited human intelligence, and that all three major standards define evidence objectives without specifying reviewer identity. Section 4 introduces the Verification Compiler concept and its architectural responses to LLM reliability concerns. Section 5 addresses the model qualification problem. Section 6 describes the regulatory pathway. Section 7 describes deployment contexts across the spectrum from development teams to formal certification programs.

Throughout this paper, *Stage 1* refers to the current phase of this research: architectural definition, requirements specification, and the practice prototype that validated the core structural properties. *Stage 2* refers to implementation on a representative embedded C codebase and empirical measurement of model accuracy profiles on real verification tasks — the work needed to validate the system's development-cycle value before any certification program engagement.

<p data-fig="7"></p>

The resulting maturity path is intentionally staged. This paper records the architecture and likely failure modes; it is not a deployment claim. The next step is a practice deployment on a representative codebase where edge cases, graph-construction failures, VQP sizing limits, model error patterns, and human-review ergonomics can be discovered cheaply. Only after that should the deterministic implementation be hardened, analyzed by the same verification infrastructure it defines, and prepared for tool qualification. Actual project deployment is the final step, not the current one.

### Terminology Note

This paper uses *unit of intelligence* as an umbrella term for any entity that can perform a cognitive task — human engineers, language model instances, and specialized tools. A *model unit* is specifically a language model instance deployed to perform a defined verification sub-task, configured with a prompt, context, and toolchain. *Agent* is used in the broad sense of an autonomous or semi-autonomous process; *model unit* is preferred when referring to a specific AI component in the verification pipeline.

## Motivation

Software verification is expensive for a reason that persists across all rigor levels: it requires someone — human or tool — to systematically check that every code unit satisfies its requirements, that every requirement is covered by tests, and that the evidence chain is complete and consistent. In safety-critical settings (avionics, automotive, medical devices), this work must be done by qualified, independent human reviewers who examine each code unit against its full requirement chain, test coverage, and analysis evidence. The work is meticulous rather than creatively difficult: assembling artifacts, checking traceability, confirming coverage, and packaging evidence for audit. A senior engineer capable of complex architectural judgment spends significant time on tasks that are essentially structured consistency checking.

The problem is not limited to certified systems. Any team building software with meaningful correctness requirements — embedded firmware, industrial control systems, infrastructure software, high-reliability APIs — faces the same underlying issue: verification is a snapshot, not a signal. It happens at release, not continuously. By the time it reveals a traceability gap or an unsatisfied requirement, the fix is expensive.

This project investigates whether language models, structured by the same decomposition principles that make human verification rigorous, can bring continuous verification into the development cycle — reducing cost and accelerating feedback — while keeping qualified human engineers in the certification role where their judgment is genuinely required, for teams that need it.

## English as a Specification Medium

English is an imprecise medium for specifying software interactions. It is interesting that safety-critical engineering often depends on the concept of an English-language specification at all.

Natural-language specifications can be useful because they are accessible to humans, certifiers, customers, and engineering teams. However, they also create well-documented problems in requirements engineering [Zave & Jackson, 1997; Davis, 1993]:

- specifications may be ambiguous — the same sentence admits multiple valid implementations
- important assumptions may remain implicit — engineers share background knowledge that is never written down
- implementation may drift from intent — code evolves faster than requirements documents
- verification evidence may be incomplete — tests cover what engineers thought of, not what the specification implies
- reviewers may interpret requirements differently — independent review often surfaces divergent readings
- compliance artifacts may become disconnected from engineering work — traceability degrades as the project progresses

These problems compound in safety-critical contexts where the cost of a missed requirement is not a bug report but a safety incident. DO-178C and its equivalents respond by requiring bidirectional traceability between requirements and artifacts at each level, ensuring that every requirement is tested and every test is justified by a requirement [FAA AC 20-115D; NASA Jacklin DO-178C overview].

An important research question is whether model units can help maintain these traceability relationships and catch divergence between specification, implementation, and evidence — not as a replacement for human judgment, but as a systematic consistency check.

## Core Concept: Units of Intelligence

The initial idea for this project comes from thinking about agents, humans, and teams as units of intelligence — a shared vocabulary for comparing entities that receive information, apply reasoning, and produce outputs.

A unit of intelligence has several relevant properties:

- **Capacity:** roughly analogous to short-term memory, context window size, and the amount of information that can be considered at once.
- **Accuracy:** the degree to which the unit produces correct judgments or outputs. Accuracy may have several forms and may be a function of the available context window, task type, prompting, review structure, and feedback.
- **Adaptability:** the ability to adjust behavior in response to new information, examples, corrections, and environmental constraints.
- **Specialization:** the degree to which the unit is optimized for a particular class of tasks.
- **Reviewability:** the degree to which the unit's work can be inspected, challenged, reproduced, or validated by another unit.
- **Qualification:** the degree to which the unit has been validated as capable of performing a delegated task.

Adaptability has an important asymmetry: a model unit's adaptability within a session (in-context learning) is strong, but it does not accumulate experience across sessions. The artifact graph compensates for this — it is the persistent memory structure that a stateless model unit lacks. Each session begins from the same graph state; the model's lack of persistence is a design constraint that the graph structure resolves.

<p data-fig="1"></p>

### LLMs as a New Category — Not DO-330 Tools

A critical framing point: language models are not software tools in the sense that DO-330 governs. DO-330 tool qualification applies to software whose outputs directly become part of the certification evidence for a DO-178C project — compilers, static analysis tools, test frameworks. These tools were designed with deterministic behavior, fixed functional specifications, traceable design decisions, and testable qualification criteria built in from the ground up.

Language models were not designed to meet these constraints, and treating them as if they were creates a false regulatory framing. An LLM does not have a specification — it has a capability profile, probabilistic accuracy characteristics, and task-specific performance. Attempting to qualify an LLM under DO-330 as if it were a deterministic software tool would immediately run into the absence of a Tool Operational Requirements document, the absence of a fixed algorithm, and the non-determinism of outputs.

The correct framing is that language models are a new category of unit of intelligence — with measurable capability profiles, bounded task accuracy, and in-context adaptability — but not as a replacement for human intelligence and not as a DO-330-qualified tool. They are something between a human engineer and a specialized software tool, with distinct strengths (scale, consistency, breadth, rapid iteration) and distinct limitations (no persistence, non-deterministic, accuracy varies by task, cannot self-certify).

### The Compound Architecture and Endpoint Replaceability

This framing leads directly to the compound architecture. Rather than attempting to stretch the LLM into a role it was not designed for, the Verification Compiler treats each reviewer position in the artifact graph as an *endpoint* — a slot that can be filled by a human engineer, an LLM, or another review tool, depending on the workflow context:

```
DAG Node  (code unit + requirement chain + tool evidence)
       │
       └─► Verification Query Package  (deterministic assembly)
                      │
                      ├─► Human engineer
                      │   certification pass; qualified, independent reviewer
                      └─► LLM model
                          nightly CI; development feedback only

Specialized tool outputs enter as DAG evidence nodes:
static analysis, coverage, timing, and related tool reports.
They are not reviewer endpoints — see Figure 4.
```

The graph decomposition and query assembly are the same regardless of which reviewer endpoint is used. This has two practical consequences:

1. **Development cycle**: LLMs process queries nightly, providing continuous structured feedback without human bottleneck. Multiple vendors can be rotated so different training sets must concur before human time is spent.
2. **Certification pass**: Qualified, independent human engineers review the same deterministically-generated query packages. Their verdicts are the certification evidence. LLM verdicts from the development cycle are discarded for certification purposes.

The compound architecture is what allows the system to use LLMs at their actual capability level — rapid, broad, useful but fallible — without pretending they satisfy constraints they were not designed to satisfy. The human endpoint is not a fallback; it is the design. LLMs are a development-cycle optimization within an architecture where human review is structurally required.

## Safety-Critical Verification as a Coordination System

<p data-fig="2"></p>

Safety-critical software development standards — DO-178C, ISO 26262, IEC 62443 — share a common evidence structure: tiered rigor levels (DAL A–E, ASIL A–D, SL 1–4), specific artifact types required at each level, and bidirectional traceability between requirements, code, tests, and results [FAA AC 20-115D; NASA Jacklin DO-178C overview; NASA-STD-8739.8B]. What they do not prescribe is a particular tool or method for producing that evidence — they specify what the evidence must demonstrate, not how it is assembled. This is what creates space for the Verification Compiler: a tool that assembles the same evidence package a human reviewer would need, but does so systematically from a structured artifact graph.

Human engineers working in these frameworks must be qualified for their roles. Models and tools used in analogous roles require analogous qualification processes — not the same processes, but processes that establish measurable confidence that the delegated task is within their capability. This is the function of task-specific accuracy profiles and the TQL-5 tool qualification pathway described in the Regulatory Pathway section.

## Concept: Verification Compiler

The verification compiler is a hierarchical requirements and verification results tracking infrastructure that links a codebase to every artifact needed to prove software correctness — datasheets, interface specifications, static analysis results, tests, physical test results, memory tool outputs, and certification evidence — and then traverses that graph to decompose verification into units a model can evaluate.

The system is primarily designed for C codebases, where requirements-to-implementation traceability is most critical and where the safety-critical embedded software ecosystem the architecture targets is concentrated. The structural approach is language-agnostic and applies wherever requirements, code, and verification artifacts can be linked in a graph — C++, Ada, Rust, and higher-level languages with formal or semi-formal specifications are all viable targets, with C as the primary design context.

It is called a compiler by analogy: just as a software compiler transforms source code through a defined, mechanical process into a verified artifact, the verification compiler transforms a linked artifact graph through a defined traversal process into structured verification evidence.

### LLM Reliability and the Mitigation Architecture

The core objection to using language models in safety-critical verification is well-founded: models produce plausible-sounding but incorrect outputs, their reasoning is opaque, their accuracy varies dramatically by task type, and they degrade on long contexts. The Verification Compiler's architecture is a direct response to each of these failure modes. Before describing the artifact graph and traversal in detail, it is important to see that the architecture is not an LLM wrapper — it is a structure designed from first principles to contain and mitigate these specific failure modes.

**Hallucination and false confidence.** Models can state incorrect conclusions with apparent certainty. Mitigation: every query is structured — the model returns a pass/fail/uncertain verdict with a mandatory rationale field, and uncertain is a valid and useful result. Uncertain results require human escalation rather than propagating false confidence. The structured result format prevents the model from producing narrative summaries that obscure a lack of evidence.

**Irrelevant context pollution.** When a model is given an entire codebase or a loosely scoped document set, requirements, tests, and datasheets for unrelated code units dilute the signal for the unit under review. This is not primarily a token-count problem — modern frontier models handle large contexts — but a reasoning-focus problem: the model's attention is split across artifacts that are not logically related to the query. Mitigation: the graph traversal bounds each query by construction. The query contains exactly the code unit under review, its full parent requirement chain, linked tests and results, and referenced datasheets — nothing from other code units. This focus is the architectural mechanism for reliable reasoning, not a workaround for a context-window limitation.

**Task-specific accuracy variance.** Benchmarks show 16–33% performance variance across domains on MMLU-Pro (TIGER-AI-Lab, 2024), and 35–50 percentage-point gaps between ostensibly similar "code tasks" (SWE-bench vs. HumanEval). A single global accuracy rating is meaningless. Mitigation: model accuracy profiles are per task-type, not global. Model suitability is checked separately from the Verification Readiness Metric: the VRM measures evidence completeness and staleness, while the model accuracy profile determines whether a model is suitable for a given review task and how much human escalation is required.

**Opacity and non-reviewability.** A model's internal reasoning cannot be directly inspected. Mitigation: all query inputs, model outputs, model version, prompt configuration, and result are logged as immutable evidence records. A human reviewer can inspect any node's full evidence package — inputs, rationale, and verdict — and re-evaluate it. The structured result is the reviewable artifact, not the model's internal state.

**No cross-session memory.** Models do not retain state between evaluations. Mitigation: the artifact graph is the persistent memory. The graph records every relationship, every result, and every version tie. The model unit is stateless; the graph is not.

**Output non-determinism.** LLM results for identical inputs may vary across invocations. Mitigation: the graph decomposition and query assembly are deterministic — the same artifact graph state always produces the same query set with the same content. LLM review mode is classified as *developmental*, not certification evidence: it provides fast, structured feedback on every development iteration (e.g., nightly CI). The final certification pass uses human reviewers on the same deterministically-generated queries. The non-determinism of individual LLM calls is irrelevant to the certification evidence because that evidence comes from the human-reviewed final pass, not from LLM intermediate results. The two-mode architecture resolves the DO-330 concern without requiring the LLM to be deterministic.

**Open capability question.** The accuracy of current LLMs on bounded requirements-vs-code verification tasks specifically — as opposed to general code completion or bug detection — is beginning to be characterized. A direct-relevance finding: recent work on LLM requirement conformance checking finds that models systematically overcorrect, flagging correct code as non-compliant at higher rates than flagging genuinely incorrect code [arXiv:2603.00539, 2026]. This asymmetric error mode — false negatives are missed, false positives create reviewer fatigue — is a concrete reason to treat LLM verdicts as pre-screen signals requiring human confirmation rather than as authoritative findings. Establishing task-specific accuracy profiles, including direction and magnitude of systematic errors, for the verification query types used by the Verification Compiler is the primary empirical goal of Stage 2.

### The Artifact Graph

At minimum, the artifact graph supports these verification-relevant node types and attributes: **Source code unit** (`file_path`, `function_name`, `version_hash`), **Requirement** (`stable_id`, requirement level), **Interface specification / datasheet** (`document_id`, referenced region), **Static analysis result** (`tool_id`, `tool_version`, `tool_configuration`, code version), **Test artifact** (test specification, procedure, or case), **Test result** (pass/fail outcome tied to a test artifact and code version), **Physical test result** (hardware/physical test result with code version and documented test conditions), **Review record** (model or human verdict, rationale, reviewer identity, prompt/model version when applicable), **Certification evidence package** (export node linking the review records, VQPs, requirements, source code units, tests, analysis results, and graph coverage proof for a selected scope), **SourceRegionNode** (`URI_Locator`, `Content_Hash`, `Text_Payload`), and **ModelAccuracyProfile** (`Model_ID`, `Prompt_Version`, `Task_Type`, empirical `TP`, `FP`, `TN`, `FN`, `PPV`, and `NPV`).

The supported typed edge relationships are: **traces-to** (requirement to child requirement or code unit), **verified-by** (code unit or requirement to test artifact), **has-result** (test artifact to test result), **analyzed-by** (code unit to static analysis result), **references** (code unit to interface specification or datasheet), **reviewed-by** (any node to a review record), **version-tied** (test or physical result to a specific code version), and **supports-claim** (claim to SourceRegionNode with selector logic and content hash). The `traces-to`, `verified-by`, and `supports-claim` edges record both `Source_Version_Hash` and `Target_Version_Hash`; `supports-claim` also records `Content_Hash` and `Selector_Logic`. A hash mismatch marks the edge stale. Stale `traces-to` and `verified-by` edges apply a VRM staleness discount; a stale `supports-claim` edge halts VQP assembly until a human reviewer re-confirms the citation against the updated source region.

**DAG structure invariant.** The artifact graph is a Directed Acyclic Graph (DAG). Cycles are forbidden and detected at graph construction time. This invariant guarantees that traversal terminates with bounded query packages — a cycle would cause traversal to loop indefinitely — and makes traversal deterministic: the same graph state always processes nodes in the same topological order, which is required for reproducible query assembly.

Apparent requirement cycles arise in practice from genuine functional relationships — bidirectional interface contracts, shared resource constraints, closed-loop control relationships — but cyclic *traceability* is circular reasoning and is architecturally unsound regardless of how real the underlying coupling is. When graph construction detects a cycle, three refactoring patterns resolve the common cases: (1) **Elevation** — move the shared constraint to a parent requirement node that both dependent requirements trace to as children, verifying against it independently; (2) **Interface contract nodes** — introduce an explicit contract node specifying the boundary obligation; each module's requirement assumes the contract and guarantees its own output, with the contract sitting above both in the DAG (analogous to assume-guarantee decomposition); (3) **State separation** — split temporally coupled requirements by time step, since state $T_n$ informing state $T_{n+1}$ flows in one direction only. A cycle that cannot be resolved by these patterns signals a software architecture that is not decomposable for independent verification — a structural problem the VC surfaces but cannot resolve on its own. Detailed treatment of DAG cycles is in the Known Architectural Challenges section.

**Completeness invariants.** The system enforces the following structural invariants and surfaces violations as graph anomalies:

- Every in-scope source code unit shall be reachable from at least one requirement via `traces-to` edges
- Every requirement shall be linked to at least one code unit or child requirement
- Every test result shall be tied to a specific code version hash

Orphan code (no requirement link) and orphan requirements (no code link) are equivalent to DO-178C traceability failures. A certification body can inspect the graph structure and confirm evaluation completeness — before a single LLM call is made — by verifying no orphan nodes exist.

Edges carry typed relationships and version hashes. Edges connecting versioned artifacts carry `Source_Version_Hash` and `Target_Version_Hash`; the `supports-claim` edge additionally carries `Content_Hash` and `Selector_Logic`. A hash mismatch marks an edge stale — stale `traces-to` and `verified-by` edges apply a staleness discount in the VRM; a stale `supports-claim` edge halts VQP assembly until a human reviewer re-confirms the citation against the updated text. The complete edge type set:

- **traces-to**: requirement → child requirement, requirement → code unit; carries `Source_Version_Hash` and `Target_Version_Hash` for staleness calculation
- **verified-by**: code unit → test artifact, requirement → test artifact; carries `Source_Version_Hash` and `Target_Version_Hash`
- **has-result**: test artifact → test result
- **analyzed-by**: code unit → static analysis result
- **references**: code unit → interface specification or datasheet
- **reviewed-by**: any node → review record
- **version-tied**: test result or physical test result → specific code version
- **supports-claim**: CLAIM → SourceRegionNode; carries `Selector_Logic` specifying how to extract text from the node for VQP assembly, plus `Source_Version_Hash`, `Target_Version_Hash`, and `Content_Hash` (SHA-256 of the referenced document region); a hash mismatch marks the edge stale and triggers human re-confirmation before VQP assembly

`Source_Version_Hash` and `Target_Version_Hash` on `traces-to`, `verified-by`, and `supports-claim` edges enable staleness detection — a hash mismatch marks an edge stale and applies a staleness discount in the VRM, preserving audit history while correctly weighting evidence recency.

Every node in the graph is a verification-relevant artifact. The system supports the following node types:

- **Certification evidence package**: a collected set of records structured for certification body review
- **Test artifact**: test specification, procedure, or case
- **Test result**: a recorded pass/fail outcome linked to a test artifact and a specific code version
- **Source code unit**: a function, module, or subsystem identified by file path, function name, and version hash
- **Requirement**: any level of natural-language requirement (system, high-level, low-level, derived), with a stable identifier
- **Physical test result**: a test result from hardware-in-the-loop or physical testing, with version and conditions documented
- **Review record**: a structured output from a model or human reviewer, attached to a verification query
- **Interface specification / datasheet**: an external document describing hardware or software interface behavior
- **Static analysis result**: output from a tool (memory safety, timing, coverage) linked to a specific code version and tool configuration
- **SourceRegionNode**: a machine-addressable pointer to a specific region within a reference document (standard, datasheet, ICD, whitepaper). Primary key: `URI_Locator` — a stable, hierarchically-scoped identifier (e.g., `doc:DO-178C-2011#6.3.b`, `arxiv:2603.00539#sec:3`). Contains a `Content_Hash` (SHA-256 of the region text) and `Text_Payload` (the actual text injected into verification queries at assembly time). A content hash change invalidates all `supports-claim` edges from that region and triggers human review before the query can be assembled.
- **ModelAccuracyProfile**: a per-`(Model_ID, Prompt_Version, Task_Type)` calibration record storing empirical accuracy statistics (`TP, FP, TN, FN`). Initialized with a pessimistic Beta prior and updated by human override events and canary query results. Computes Bayesian-smoothed `PPV = TP/(TP+FP)` and `NPV = TN/(TN+FN)` used in Model Suitability threshold checks and surfaced alongside individual review results.

The **Certification evidence package** node is the export boundary for formal review: it links to the relevant review records, VQPs, requirements, source code units, test artifacts, test results, static-analysis results, and graph coverage proof for a selected scope. In development deployments this package may be an internal audit bundle; in certification deployments it is the structured record presented to qualified human reviewers or certification bodies.

<p data-fig="3"></p>

### Graph Traversal as Decomposition

Verification proceeds by graph traversal. For each leaf code unit, the traversal collects: the code itself, all requirements linked to it from ancestor levels, all test artifacts and results linked to the code unit, any interface specifications or datasheets referenced by the unit, and any physical test evidence tied to the same code version. This collection defines a **Verification Query Package (VQP)** — a self-contained evidence bundle.

**Context-window bounded queries.** Each VQP must fit within the configured context window of the assigned model unit. The context window is not a limitation to work around — it is the design primitive. Queries are constructed to be bounded by the graph traversal so that a model can reason without truncation. Physical test evidence from a code version different from the source unit under evaluation is actively rejected at VQP assembly time — such evidence does not prove the current version's behavior and must not enter the evidence record.

**Traversal completeness.** The system guarantees that every in-scope source code unit is included in at least one VQP. The traversal algorithm and its coverage are independently inspectable — a reviewer can confirm from the graph structure alone that the full scope was evaluated, without examining any model result. This property is analogous to DO-178C traceability analysis: the graph structure is the proof that no code was omitted. Empirical work in LLM-based requirements verification confirms that F1 score degrades from 0.92 to 0.81 as requirements per query grows from 5 to 20 [Reinpold et al., 2024] — bounded decomposition is both architecturally correct and empirically necessary.

This decomposition approach has a lineage in formal verification: assume-guarantee reasoning (Cobleigh, Giannakopoulou & Pasăreanu, 2003) decomposes verification of large systems into component-level sub-problems where each component is verified against assumptions about its environment. The Verification Compiler applies an analogous principle to requirements-to-code traceability checking: each leaf-node VQP is self-contained with its full requirement chain as the assumption context, and verified independently. The graph structure ensures that local verdicts compose into a global coverage proof.

Recent work on LLM-assisted requirements engineering addresses the complementary problem of *traceability link generation* — identifying which artifacts should be connected. TraceLLM [Alturayeif et al., arXiv:2602.01253, 2026] applies prompt engineering and demonstration selection to generate and complete traceability links across requirements, design elements, test cases, and regulations, achieving state-of-the-art F2 scores across aerospace and healthcare domains. Graph-RAG [Masoudifard et al., arXiv:2412.08593, 2024] combines graph-structured retrieval with chain-of-thought prompting to verify SRS compliance against higher-level requirements. The Verification Compiler operates *downstream* of traceability link generation: it assumes the artifact graph is already populated with correct links and focuses on verifying that linked artifacts satisfy their obligations — a distinct problem with different decomposition and evidence requirements. The two problem spaces are complementary and could be composed: a TraceLLM-style system populates the graph; the Verification Compiler then traverses and evaluates it.

<p data-fig="4"></p>

### Dual-Mode Operation

The same graph decomposition supports two execution modes. In **LLM review mode**, each VQP is submitted to a qualified model, which returns a structured result: pass, fail, or uncertain, with a confidence value and rationale weighted by the model's accuracy profile for that task type. In **human review mode**, each VQP is presented to a human reviewer in the same structured package — identical format, identical evidence bundle. The decomposition does not change; only the reviewer changes. A human reviewer can complete any VQP that was previously completed by a model, using the same input, and the result enters the evidence graph in the same schema. This direct interchangeability is what allows LLM review to pre-screen during development and human review to replace it for final certification, using the same graph structure as proof of complete scope.

Human-facing deployments require a presentation layer — an IDE plugin, web dashboard, or review tool — that renders the VQP's structured evidence bundle into a cognitively navigable format: section headings, inline code display, collapsible requirement chains, and one-click verdict submission. The VQP data payload is identical for both reviewer types; the rendering is a UI concern separate from the Verification Compiler's specification. Specifying and validating this human-facing presentation layer, including its automation bias controls, is a Stage 2 deliverable.

LLM results are classified as **developmental results** — not certification evidence — unless explicitly promoted by a human reviewer. All LLM results are logged with model identifier and prompt version as developmental history, separate from the certification evidence package. When a VQP has been evaluated by both a model and a human reviewer and the results disagree, the **human result takes precedence** in all confidence calculations and evidence packages; the model result is retained in the evidence record as a discrepant result, explicitly flagged, and recorded against the model's `(Model_ID, Prompt_Version, Task_Type)` accuracy profile.

<p data-fig="5"></p>

### Verification Query and Result Schema

**Query format.** Each VQP is rendered in a structured format with clearly delimited sections: code, requirements, tests, results, referenced specifications, and evaluation instructions. The format is identical for LLM and human review — including evaluation instructions ensures both reviewer types apply a consistent methodology. The worked example below illustrates a complete query.

**Result format.** Each review result is a structured record containing:

- **Node identifier(s)**: the code unit(s) evaluated and their version hash
- **Reviewer identity**: type (model or human), plus model version and prompt version, or person identifier
- **Verdict**: `pass`, `fail`, or `uncertain`
- **Confidence**: 0–1 for model results (derived from the ModelAccuracyProfile for that task type); `high/medium/low` for human results
- **Rationale**: a written explanation of the verdict citing specific evidence
- **Evidence citations**: specific lines, sections, or artifacts supporting the verdict
- **Review timestamp** and code version at time of review

Structured results are auditable — they can be challenged, re-reviewed, and aggregated into the VRM. Unstructured chat-style outputs are not admissible as verification evidence.

**Conflict resolution.** When a VQP has been evaluated by both a model and a human reviewer and the results disagree, the human result takes precedence in all confidence calculations and evidence packages. The model result is retained in the evidence record as a discrepant result, explicitly flagged. Each disagreement is recorded against the model's `(Model_ID, Prompt_Version, Task_Type)` accuracy profile and triggers a recalibration event if the disagreement rate for that task type exceeds a configured threshold. Conflicts are signal for model qualification, not errors to be suppressed — retaining both results preserves auditability while giving safety-conservative precedence to the human verdict.

**Prompt configuration control.** Prompt configurations are treated as versioned data, subject to the same configuration management as source code. Every prompt has a unique version identifier. The prompt version is recorded in every review result alongside the model identifier. In-place editing of active prompts is not permitted — changes require a new prompt version. The system can reproduce any historical VQP exactly from the artifact graph state, code version, and prompt version at time of submission. This is the minimum necessary for evidence records to be reproducible and auditable under DO-330 Tool Operational Requirements.

**LLM result status and determinism.** LLM verification results are classified as **developmental results**, not certification evidence, unless explicitly promoted by a human reviewer. LLM review mode is for development-cycle passes (nightly CI), providing continuous structured feedback without requiring human review on every iteration. All LLM results are logged with model identifier, prompt version, and full output. These logs are retained as developmental history but do not enter the certification evidence package unless a human reviewer confirms and promotes a result.

The graph decomposition and VQP assembly are deterministic: the same artifact graph state always produces the same VQPs with the same content. Determinism applies to the compilation process, not to individual LLM responses — but because each human reviewer receives the identical VQP the LLM received, meaningful comparison is preserved.

### Verification Readiness Metric

During LLM review mode, the compiler produces a **Verification Readiness Metric (VRM)** — a score reflecting evidence completeness across the entire requirement scope. The formula:

```
C_v(i) = Σ_k  w_k × I_k × S_k
         vertical evidence completeness for requirement i

VRM    = Σ_i  C_v(i) / N_total
         sum over all requirements in scope;
         unevaluated requirements contribute 0
```

Where: `w_k` = configurable weight for evidence type k (requirement link, test artifact, test result, static analysis); `I_k` = binary existence indicator for evidence type k at requirement i; `S_k` = staleness discount ∈ [0.0, 1.0] (1.0 = evidence tied to current code version, 0.0 = AST or content has changed); `N_total` = total requirements in scope. Requirements that have not yet been evaluated contribute C_v(i) = 0, so the formula naturally penalizes unevaluated scope without a separate coverage term. The horizontal coverage fraction `C_h = N_eval / N_total` is surfaced separately on the dashboard as the completeness indicator — it shows what fraction of scope has been touched at all, independently of how complete the evidence is for evaluated requirements.

Model accuracy is tracked separately as a **Model Suitability** indicator — not as a component of VRM. A model's task-specific `PPV = TP/(TP+FP)` and `NPV = TN/(TN+FN)` are computed from the `ModelAccuracyProfile` and compared against a project-configured minimum suitability threshold. A model that falls below the threshold for a task type is not eligible for LLM review mode for that type and is flagged for recalibration or replacement before the next evaluation pass. Keeping VRM as a pure coverage-and-completeness signal is a deliberate design choice: VRM describes *what has been reviewed and how completely*, independently of *how reliable a given reviewer is*. These are distinct questions that should not be conflated in a single composite — multiplying coverage by a probabilistic accuracy estimate produces a number that is metrologically uninterpretable as either a coverage measure or a reliability measure.

**Model Accuracy Profile.** The system maintains a `ModelAccuracyProfile` node for each unique `(Model_ID, Prompt_Version, Task_Type)` triple. The profile stores empirical confusion matrix values (`TP, FP, TN, FN`), a `Sample_Size` count of labeled evaluations, a `Profile_Version` identifier, a `Last_Updated` timestamp, a Bayesian Beta prior (default: uniform 1.0/1.0; pessimistic deployments may use 1.0/10.0), and derived `PPV` and `NPV` values. Profiles are updated by two mechanisms: (1) **human overrides** — when a human reviewer disagrees with a model result, the disagreement is recorded against the profile for that tuple; (2) **canary queries** — queries with known ground-truth answers inserted into the evaluation stream. The derived PPV and NPV serve two purposes: inputs to the Model Suitability threshold check (gate for which models may operate in LLM review mode for a given task type), and asymmetric error characterization that is always surfaced alongside model results to inform human review prioritization. Model accuracy is task-specific: a model with high PPV on citation verification may have low PPV on interface constraint checking. A global accuracy estimate conflates these.

**Per-query confidence.** The system records a confidence value for each review result. For model results, confidence is derived from the task-specific ModelAccuracyProfile. This value is attached to the review result record and surfaced in the evidence package for human reviewer interpretation — it is not aggregated into the VRM. The asymmetric overcorrection pattern identified in LLM requirement conformance checking [arXiv:2603.00539, 2026] — models over-flag correct code more than they miss bad code — is captured by reporting separate PPV and NPV alongside model results rather than a single accuracy number, enabling human reviewers to calibrate their attention to false-positive-heavy results from models with known overcorrection bias.

The VRM is a development management tool — it tells engineers how much of the codebase has been pre-screened and how reliable the pre-screen is likely to be. It is explicitly not a certification claim. A codebase at VRM = 0.91 is not certified; it is screened. Human verdicts produce the certification evidence record; LLM verdicts produce the developmental pre-screen. These are structurally separate outputs of the same system.

**Reporting format.** The VRM is most informative when reported alongside the horizontal coverage fraction — *(VRM = 0.91, C_h = 0.78)* — rather than as a single number. The VRM already penalizes unevaluated requirements (their C_v(i) = 0 pulls the numerator down), but surfacing C_h separately makes explicit *what fraction of scope has been touched at all*, independently of evidence quality. A project dashboard shall always show both values. The VRM is a development signal; C_h is the completeness claim. The component breakdown — per-requirement C_v(i) values and staleness flags — shall also be exportable for requirements-level inspection by human reviewers and certification bodies.

**Evidence weight configuration.** The `w_k` weights in the vertical completeness term `C_v(i)` are configurable per project and per evidence type. They are not architectural constants — they are a critical, qualified configuration parameter. A project that overweights easily-provided evidence artifacts (e.g., requirement links) relative to hard-to-produce evidence (e.g., test results with passing status) could inflate the VRM without improving actual verification completeness. The `w_k` values shall be documented in the Tool Operational Requirements, reviewed by the project's quality assurance function, and version-controlled as part of the VC configuration. Changes require re-evaluation of all VQPs affected by the reweighting.

**Cold-start and bootstrapping.** A new project or new task type begins with no empirical data for the `ModelAccuracyProfile`. The Model Suitability threshold cannot be meaningfully applied until sufficient data accumulates — the default behavior is to treat all models as provisionally suitable, with the sample count surfaced alongside every result to signal the absence of empirical calibration. Canary queries are the fastest path to bootstrap an accuracy profile: injecting known-correct and known-flawed VQPs into the evaluation stream produces labeled data before the system is deployed on production queries. Until a minimum empirical sample is available (e.g., 20+ canary results per task type), suitability assessments should be flagged as unvalidated and human review escalation thresholds set conservatively.

### Provable Decomposition

The graph structure is itself the proof that the decomposition is complete. Orphan code units (no requirement link) and orphan requirements (no code link) surface as graph anomalies, analogous to DO-178C traceability failures. A certification body can inspect the graph structure and confirm evaluation scope independently of any model result — before a single LLM call is made.

### Evidence, Auditability, and Configuration Management

**Immutable evidence records.** Once a review result is written to the evidence graph, it is not modified in place. Updates create new versioned records. Immutability is required for certification auditability — modifying historical records would undermine the evidentiary chain. Any human or regulatory reviewer can reconstruct the complete evidence history from the immutable record set.

**Full provenance.** Every node in the evidence graph carries provenance metadata: who or what created it, when, with what inputs, and against which code version. Provenance is not optional — without it, a result cannot be attributed, challenged, or placed in a certification evidence package. Node provenance is recorded at creation time and is part of the immutable record.

**Exportable evidence package.** The system exports structured evidence packages scoped to a specified requirement subtree or code module. Each package contains all verification queries, results, confidence values, rationales, and graph coverage proof for that scope. The evidence package is the primary artifact the system produces for external use — certification bodies and human reviewers receive a navigable, structured evidence set rather than raw query logs. Scoped export enables partial certification submissions: a team can certify a completed subsystem before the full codebase is ready.

### Artifact Graph Lifecycle

The Verification Compiler consumes an artifact graph — it does not create one. Building and maintaining the requirement-to-code traceability links that the graph represents is significant engineering work, and it is a prerequisite to using the compiler rather than a consequence of it.

This is not a new problem. Industrial requirements management tools — IBM Engineering Requirements DOORS, Jama Connect, Reqtify, Siemens Polarion ALM — are designed to create and maintain traceability links across a product lifecycle. Model-Based Systems Engineering (MBSE) environments such as Cameo Systems Modeler manage artifact relationships as a byproduct of model-driven design. The Verification Compiler maintains its own artifact graph, distinct from these project lifecycle databases. Existing ALM tools track project state and compliance workflows; the VC graph enforces strict DAG invariants and encodes all traceability as typed, version-hashed nodes and edges for query assembly — a different structural contract. Analysis tools — static analyzers, runtime coverage tools, memory analysis frameworks, DCCC coverage tools — produce output that enters the VC graph directly as `analyzed-by` evidence nodes, alongside human-authored traceability links.

The implication for teams adopting the Verification Compiler is that it provides the greatest return where disciplined requirements management already exists, and that adopting it creates incentive to maintain that discipline — every broken traceability link surfaces as a graph anomaly that stops a query from being assembled, immediately rather than at audit time. The compiler makes the cost of traceability debt visible on every commit.

**Graph lifecycle workflow.** At a high level, the graph lifecycle has three phases:

*Creation.* A requirements analyst creates requirement nodes for each HLR and LLR in scope. Developers create `traces-to` edges from each LLR to the implementing source code unit. Test engineers create `verified-by` edges from code units to test artifacts, and `has-result` edges from test artifacts to test results. Static analysis tool outputs are entered as `analyzed-by` edges. `SourceRegionNode` entries are created for every reference document cited in requirements or claims, with stable `URI_Locator` identifiers per the Source Region Addressing requirements.

*Review.* The graph structure is reviewed before any VQP is assembled. Graph review checks: (a) no orphan nodes; (b) all in-scope code units reachable from at least one requirement; (c) all requirements linked to at least one code unit or child requirement; (d) all test results version-tied to the current code baseline. For certification programs, this review is a qualified, documented activity — analogous to the traceability analysis required by DO-178C before verification begins — with defined roles and completion criteria.

*Update.* When code changes, affected `traces-to`, `verified-by`, and `version-tied` edges are marked stale by the version hash mechanism, triggering re-evaluation of dependent VQPs. When requirements change, downstream edges are re-evaluated. When source documents change (standard revised, datasheet updated), the `content_hash` on the affected `SourceRegionNode` changes, marking all `supports-claim` edges stale and requiring human re-confirmation before the VQP can be assembled. The compiler surfaces all staleness immediately on the next evaluation pass.

The cost structure of this update cycle is important: graph re-traversal and VQP assembly are computationally cheap — data structure operations that complete in seconds on any CI runner. The expensive operation is LLM evaluation of stale VQPs, which runs only on the affected subset. A single-function change marks only the VQPs containing that function stale; the LLM is called only for those. Full re-evaluation is reserved for requirement-scope changes — which is also when full re-evaluation is appropriate. This incremental cost model makes CI integration tractable: developers update graph edges in the same commit that changes code, and the nightly CI run re-evaluates only what changed.

### Physical Test Evidence

Physical test results from human functional testing can enter the graph as first-class nodes as long as they are tied to a specific code version, structured in a format parseable by the LLM, and linked to the requirements they exercise.

### Reviewer Qualification and Independence

DO-178C defines independence precisely. Rierson (Section 9.3, p. 188) quotes the standard directly:

> "independence is achieved when the verification activity is performed by a **person(s)** other than the developer of the item being verified, and **a tool(s) may be used to achieve equivalence to the human verification activity.**"

Two pathways exist: a qualified person, or a qualified tool achieving equivalence to human verification. Tool equivalence requires DO-330 qualification. This is the formal basis for the Verification Compiler's regulatory pathway — not a claim that standards are silent on reviewer identity, but a recognition that the standard explicitly provides a tool-based independence pathway when the tool is properly qualified.

**Independence requirements by DAL.** For DAL A software, 25 verification objectives require independence; for DAL B, 13; for DAL C and D, none. The number of objectives requiring a qualified person or tool scales with criticality [Rierson, Section 9.3, p. 188–189].

**Human reviewer qualification.** DO-178C "assumes the use of qualified and well-trained people; however, it is difficult to measure the adequacy of people. Some authorities examine résumés and training history to ensure that qualified and properly trained personnel are used" [Rierson, Section 3.3.3]. Human reviewer qualification is informally assessed — no formal certification process is specified. By contrast, DO-330 tool qualification is a rigorous formal process.

**Stage 1 architecture uses the person-based pathway.** Qualified, independent human engineers perform all certification review. The Verification Compiler provides those engineers with pre-assembled, bounded evidence packages; they do not need to locate and assemble artifacts manually. Their verdict is human-conducted and human-signed. The tool makes that review more thorough and auditable — the structure does not change the fact that a qualified person is reviewing and signing off.

The human reviewer has no foreknowledge of any LLM pre-screen result when reviewing a query package. Their verdict is formed independently from the evidence alone (Requirement 6.1).

**Longer-term tool-equivalence pathway.** The compound architecture's endpoint replaceability is specifically designed to support a future DO-330-qualified tool pathway for independence. At DAL C/D (no independence requirement), LLMs can operate freely as development tools. At DAL A/B, a DO-330-qualified version of the compiler could satisfy the tool-equivalence clause for applicable objectives. Stage 1 does not pursue this pathway — human final pass is the current design — but the architecture does not foreclose it.

**Model diversity for development quality.** During nightly CI, rotating LLM vendors introduces different training-induced blind spots. Findings that multiple families independently flag are more likely genuine. This allocates human review attention more efficiently. It is a development-quality benefit, not an independence mechanism.

### Scope: Stage 1 Trace Boundaries

Stage 1 is explicitly scoped to two trace types: **LLR-to-Code** (low-level requirement to source code unit) and **Code-to-Test** (source code unit to test case and test result). These two trace types cover the core verification loop for a leaf-node C function: does the code satisfy the requirement that generated it, and do the tests confirm that behavior?

This scope is deliberately narrow. DO-178C distinguishes High-Level Requirements (HLRs) from Low-Level Requirements (LLRs) — HLRs describe system behavior, LLRs describe software design decisions precise enough to be directly implemented and tested. Stage 1 begins at the LLR boundary because LLRs are already precise enough for bounded query evaluation. HLR-to-LLR consistency (checking that LLRs correctly decompose an HLR) and system-level traces (HLR-to-system behavior) are Stage 2 targets, as they require reasoning over multiple linked nodes rather than a single leaf-node query.

**Non-functional requirements (NFRs)** — timing constraints, worst-case execution time (WCET), stack depth, memory partitioning, and race conditions — cannot be evaluated by examining a single leaf-node query. These require system-level analysis tools: timing analyzers (e.g., AbsInt aiT), stack analyzers, and schedulability analysis. The Verification Compiler's artifact graph is designed to *consume* the outputs of these tools as evidence nodes (static analysis result nodes with `analyzed-by` edges), allowing their results to enter the traceability record and appear in relevant verification queries. The compiler does not replace those tools; it organizes and links their outputs. Full NFR coverage is a Stage 2 target.

### Automation Bias Mitigation and Reviewer Independence

The strongest regulatory challenge to this architecture is not LLM non-determinism — that is handled by the two-mode architecture. The concern is **automation bias**: a human reviewer who has seen hundreds of LLM "pass" verdicts may review less rigorously than one working without the tool. DO-330 TQL-5 qualification and the associated process assurance argument require that human review remain effective. A tool whose LLM outputs consistently prime reviewers toward acceptance, regardless of accuracy, would undermine the independence and effectiveness of human review — the core regulatory concern.

The architecture addresses this with three mechanisms:

**Disagreement rate reporting.** Aggregated disagreement rates between LLM verdicts and human verdicts are reportable by reviewer, by task type, and by time period, enabling systematic patterns in automation bias or model miscalibration to be detected. The VRM dashboard always surfaces horizontal coverage fraction and vertical completeness components independently — preventing the aggregate VRM from being treated as a certification proxy — and the Model Suitability status for each active model is reported alongside.

**Evidence-first presentation.** The human reviewer's interface presents the full evidence package — code, requirement chain, test results, analysis results — before any LLM pre-screen result is revealed. The reviewer must submit their independent verdict before seeing what the LLM concluded. This is a process assurance requirement (REQ-6.1) that the tool must enforce mechanically, not a UI convention: the verdict field must be locked once submitted, and the LLM result must not be accessible until after the reviewer submits. A reviewer who can click through to the LLM answer before completing their own assessment defeats the mechanism entirely. This implements the display prompt countermeasure documented in aviation supervisory control research [Mosier & Skitka, 1996–1997].

**Canary queries.** The system periodically injects known-flawed verification query packages — queries with deliberate evidence gaps, requirement mismatches, or incorrect test results — alongside real queries. The human reviewer does not know which queries are canaries. Failure to flag a canary is recorded in the reviewer's accuracy profile and triggers a review process calibration event. This implements the accountability effect countermeasure: when reviewers know their vigilance is being evaluated, automation-related errors decrease significantly [Mosier & Skitka, 1996–1997]. Canary queries provide continuous empirical validation that human review is functioning as intended and not degrading into rubber-stamping.

### Regulatory Pathway

The Verification Compiler is not, in Stage 1, a DO-178C-certified tool. The deterministic components of the system — graph traversal, query assembly, invariant enforcement, and structured result logging — are architecturally qualifiable under **DO-330 Tool Qualification Level 5 (TQL-5)**. This is a design property, not a near-term product claim: the system is built so that a TQL-5 qualification package is achievable for the deterministic components when a project requires it.

#### What Qualifies and What Does Not

The critical framing point is: **the thing being qualified is the deterministic query generator and evidence packager, not the LLM**. The TQL-5 submission covers the system that traverses the artifact graph, assembles complete verification query packages, enforces graph invariants, and produces structured result records. This system is fully deterministic — the same artifact graph state always produces the same query set — and its behavior can be specified in a Tool Operational Requirements (TOR) document and validated against a set of functional test cases.

The LLM integration is explicitly a non-qualified feature. It provides developmental feedback during the development cycle and is outside the certification workflow. The Verification Compiler's Requirement 3.3b makes this separation explicit: LLM results are classified as developmental, human results are certification evidence, and the two are structurally separate outputs. The LLM's non-determinism is irrelevant to the certification evidence because that evidence comes from the human-reviewed final pass on the same deterministic query packages.

#### What TQL-5 Actually Requires

TQL-5 is the lowest qualification level but is not trivial. A TQL-5 qualification package requires:

- **Tool Qualification Plan (TQP):** Documents the scope, the tool, and the plan for producing qualification evidence.
- **Tool Operational Requirements (TOR):** Specifies the tool's inputs, outputs, operational environment, and configuration requirements (including prompt version control per Requirement 3.5).
- **Validation evidence:** Functional test cases demonstrating that the deterministic components meet the TOR — graph traversal coverage, query assembly completeness, invariant enforcement, version consistency rejection.
- **Configuration management records:** Tool source code, qualification data, and all changes under version control.
- **Tool Accomplishment Summary (TAS):** Declares the tool qualified for its intended use.

#### Regulatory Environment

The broader regulatory environment is moving in this direction. The joint SAE G-34/EUROCAE WG-114 working group's ED-324/ARP6983 standard — *Process Standard for Development and Certification Approval of Aeronautical Products Implementing AI* — establishes process requirements for AI/ML components in certified avionics systems [EUROCAE WG-114, 2025; EASA AI Roadmap 2.0, May 2023]. An important distinction applies: ED-324/ARP6983 targets ML models *embedded in* operational certified systems — the ML component is itself part of the certified product, subject to rigorous design assurance at up to DAL C. The Verification Compiler's LLMs occupy a different role: they are developmental aids *external* to the certified system, used to pre-screen verification evidence during development. Applying ED-324/ARP6983's ML-in-product framework to an LLM-as-verification-tool deployment would be a category error — the correct existing framework is DO-330 qualification of the deterministic components, not ML design assurance of the LLM. No regulatory body has yet issued specific guidance on DO-330 qualification of LLM-assisted verification tools; this architecture is ahead of the published guidance. The DO-330 TQL-5 pathway is the correct existing framework; the architecture's design choices map directly onto its requirements.

## Worked Example: One Function Through the Compiler

To make the concept concrete, consider a minimal C sensor driver. The following shows how a single function moves through the Verification Compiler end-to-end.

### The Code Unit

```c
/* src/sensor.c — git commit a1b2c3 */
uint16_t read_sensor(adc_handle_t *adc) {
    return adc_read_raw(adc) & 0x0FFF;  /* 12-bit mask per ADC datasheet */
}
```

### The Artifact Graph Fragment

```
SR-1: "The system shall read sensor data without corruption"
  └─traces-to─► HL-1: "Sensor driver shall return a valid 12-bit ADC value"
                  └─traces-to─► LL-1: "read_sensor() shall mask the raw ADC
                                        output to 12 bits before returning"
                                  └─traces-to─► read_sensor() [src/sensor.c]
                                                  ├─verified-by─► TC-001
                                                  ├─analyzed-by─► SA-001
                                                  └─refs─► ADC_Datasheet
TC-001 ──has-result──► TR-001 [version-tied: git:a1b2c3]
```

### The Verification Query (submitted to model or human reviewer)

```
VERIFICATION QUERY — Node: read_sensor() @ git:a1b2c3
────────────────────────────────────────────────────
REQUIREMENTS
  SR-1: The system shall read sensor data without corruption.
  HL-1: Sensor driver shall return a valid 12-bit ADC value.
  LL-1: read_sensor() shall mask raw ADC output to 12 bits before returning.

CODE
  uint16_t read_sensor(adc_handle_t *adc) {
      return adc_read_raw(adc) & 0x0FFF;
  }

REFERENCED SPECIFICATION
  ADC_Datasheet_RevB, §3.2: "Output register is 16-bit; valid data occupies
  bits [11:0]; bits [15:12] are undefined and must be masked by software."

TESTS & RESULTS
  TC-001: Call read_sensor() with injected raw values 0x1FFF, 0xFFFF, 0x0000,
          0x0800. Assert return value equals input & 0x0FFF.
  TR-001: PASS — all four assertions passed @ git:a1b2c3.

STATIC ANALYSIS
  SA-001: No integer overflow or uninitialized reads detected.

EVALUATION INSTRUCTIONS
  Does read_sensor() satisfy LL-1? Consider: (1) whether the mask is correct
  per the datasheet, (2) whether TC-001 provides adequate coverage of LL-1,
  and (3) whether any requirement in the chain is unsatisfied by the evidence.
────────────────────────────────────────────────────
Context: ~1.2K tokens
```

### The Structured Result

```json
{
  "node": "read_sensor @ src/sensor.c",
  "code_version": "git:a1b2c3",
  "reviewer": { "type": "model", "id": "gemini-2.5-pro", "temperature": 0 },
  "result": "pass",
  "confidence": 0.94,
  "rationale": "The mask 0x0FFF correctly isolates bits [11:0] as specified in
                ADC_Datasheet_RevB §3.2. TC-001 covers boundary values and
                confirms the mask behavior at runtime. SA-001 confirms no
                overflow. LL-1 is fully satisfied; HL-1 and SR-1 are satisfied
                by transitivity through the requirement chain.",
  "evidence_citations": [
    "ADC_Datasheet_RevB §3.2",
    "TC-001",
    "TR-001",
    "SA-001"
  ],
  "flags": []
}
```

## Deployment Contexts

The Verification Compiler is not solely a certification tool. Its core capability — continuous, structured, evidence-backed verification readiness feedback — is useful across a spectrum of rigor levels. The architecture scales down to development teams that have no certification obligation, and scales up to full DO-178C certification programs. The VRM threshold, the CI gate policy, and the CD strategy are project-specific parameters, not architectural constants.

### Tier 1: Development Teams — Continuous Verification Readiness

A team building high-reliability software (infrastructure services, embedded firmware, industrial controls) without a formal certification obligation can deploy the Verification Compiler as a CI component. On every commit, the system:

- traverses the artifact graph to identify stale requirement-to-code links and uncovered requirements
- submits changed nodes to LLM review
- updates the Verification Readiness Metric
- fails the CI build if VRM drops below a project-configured threshold or if orphan nodes are introduced

The VRM operates as a living signal: engineers see not just "tests pass" but "what fraction of requirements are currently pre-screened and how confident is the pre-screen." Requirement drift, untested behavior, and broken traceability surface continuously rather than at release.

CD policy at this tier is project-defined — a team might deploy when VRM ≥ 0.85 with no high-severity open findings, or require a human review of flagged nodes before merging to a release branch. The compiler does not impose a policy; it provides the signal to enforce one.

### Tier 2: Safety-Focused Teams — Structured Human Oversight

Teams building safety-relevant systems that do not pursue formal certification (medical devices below certain classes, industrial automation, ADAS features below ASIL thresholds) gain two capabilities beyond Tier 1:

- **Structured human escalation**: nodes flagged by LLM review, or nodes where VRM falls below a threshold, are routed to a human reviewer queue with a pre-assembled evidence package — the same package the LLM used. Human time is spent where the pre-screen is uncertain, not uniformly across the codebase.
- **Audit trail**: the graph structure and all structured results form an auditable evidence record even without a formal certification submission. If an incident occurs, the team can demonstrate systematic, traceable verification activity.

The human review at this tier does not need to satisfy DO-178C independence requirements — it is engineering due diligence, not certification evidence. The compiler still provides the evidence package and enforces traceability discipline.

### Tier 3: Formal Certification Programs

For teams targeting DO-178C, ISO 26262, or IEC 62443 certification, the Verification Compiler's architecture is designed to support the full certification workflow:

- **Human final pass**: qualified, independent human engineers review the same deterministically-generated query packages that the LLM pre-screened during development. Their verdicts constitute the certification evidence record. LLM verdicts are discarded for certification purposes.
- **DO-330 TQL-5 pathway**: the deterministic query generator and evidence packager can be qualified under DO-330 TQL-5, establishing the tool as part of the formal certification evidence package. This qualification applies only to the deterministic components — graph traversal, query assembly, invariant enforcement — not to the LLM integration.
- **DAL-scaled independence**: the compiler's dual-mode architecture directly supports the DO-178C independence requirements that scale by Design Assurance Level. At DAL C/D (no independence requirement), LLM review can operate freely. At DAL A/B, the human final pass satisfies the independence requirement for applicable objectives.

The CD gate at this tier is a human decision: the certification pass either succeeds or it does not. VRM is a development management signal, not a certification gate — the binary is the human sign-off.

### What Changes Across Tiers

The underlying system is identical across all three tiers. What changes:

| | Tier 1 (Dev Teams) | Tier 2 (Safety-Focused) | Tier 3 (Certification) |
|---|---|---|---|
| Reviewer | LLM only | LLM + human escalation | LLM + human final pass |
| VRM threshold | Project-configured CI gate | Project-configured + human queue trigger | Development signal only |
| Human review standard | None required | Engineering due diligence | DO-178C independence |
| Tool qualification | Not required | Not required | TQL-5 available |
| Evidence artifact | CI output | Internal audit trail | Formal certification record |
| CD gate | VRM threshold | VRM + human queue cleared | Human certification sign-off |

<p data-fig="6"></p>

## Source Region Addressing

The Verification Compiler requires that every claim's supporting evidence be machine-addressable — not just cited as a document title, but as a specific, stable, content-hashable region within a document. This requirement was identified during Stage 1 prototype work as a structural necessity: natural-language source labels produced silent resolution failures at scale, preventing the graph from assembling correct VQPs.

### Stable Region Identifiers

Every reference document used as evidence shall have its cited regions identified by a stable, machine-readable `URI_Locator`. The identifier encodes document identity, edition, and the precise region within it. Three tiers of addressing are recognized, in order of stability:

**Tier 1 — Heading-slug IDs** (controlled documents, e.g., this whitepaper):
Format `doc:<doc-id>#H<level>:<heading-slug>` — for example, `doc:whitepaper-v0.2#H2:concept-verification-compiler/H3:graph-traversal`. Generated from the Markdown heading hierarchy. Fragile if heading text changes; acceptable for internally-controlled documents where changes are tracked and re-addressed.

**Tier 2 — Section-number IDs** (engineering standards, ICDs, datasheets):
Format `doc:<doc-id>#<section-number>` — for example, `doc:DO-178C-2011#6.3.b`. Section numbers rarely change across minor revisions; content hash detects text changes within a stable section number. This is the correct tier for VC deployments against engineering standards — engineers already cite this way, so adoption cost is zero.

**Tier 3 — Formal standard citation format** (legal/regulatory documents):
Format `std:<standard-id>:<part>:<section>:<para>:<subpara>` — for example, `std:14-CFR:25.1309:b:1:ii`. Formally stable; resolvable against official text databases.

### SourceRegionNode Schema

Each SourceRegionNode contains:

```
id:           URI_Locator
              primary key; unique, stable, hierarchically scoped
doc_id:       parent document identifier
section_path: e.g., "6.3.b" or "H2:concept-vc/H3:traversal"
title:        human-readable section title
body:         actual text of the region (injected into VQPs at assembly time)
content_hash: SHA-256 of body
              changes when text changes, even if section_path is stable
parent_id:    URI_Locator of parent region (for hierarchy navigation)
doc_version:  document edition string
```

### VQP Assembly from SourceRegionNodes

At VQP assembly time, the resolver fetches the `body` of each referenced SourceRegionNode and injects it directly into the VQP prompt — not a citation label, but the actual text being evaluated. The VQP must contain the source text itself. If a SourceRegionNode's `content_hash` has changed since a `supports-claim` edge was created, the edge is marked stale and the VQP is not assembled until a human confirms the citation still holds for the updated text.

### Document Addressability Requirements

For a document to be VC-addressable, it requires: (1) **atomic, named units** — each verifiable claim resides in exactly one addressable region; (2) **stable IDs** — the region's identifier does not change unless content is intentionally revised; (3) **content hash** — to detect silent text changes within a stable ID; (4) **hierarchy** — parent-child relationships enabling the traversal to navigate document structure. Technical engineering standards (DO-178C, ISO 26262, ICDs) satisfy (1), (2), and (4) natively; the VC adds (3). For informal documents such as this whitepaper, explicit section anchors shall be added (e.g., `## Section Title {#sec:unique-id}` in Pandoc Markdown or `[[anchor]]` in AsciiDoc).

## Known Architectural Challenges

The following architectural problems are recognized as necessary for a production Verification Compiler but are deferred from the current Stage 1 scope. They are documented here as constraints on future design — their existence is a scoping decision, not a conceptual gap.

### Graph Invalidation Cascade

When a source code unit changes, which VQPs must be re-evaluated? A naive implementation re-runs all VQPs on every commit — wasteful but correct. A production implementation requires node-level version hashes and invalidation propagation rules through the DAG so that only queries whose inputs changed are re-submitted.

**Current scope**: re-run all VQPs on every evaluation pass. Smart invalidation is a future feature.

**Future design constraint**: invalidation rules must be conservative — when in doubt, invalidate. A stale result that is not re-evaluated is worse than an unnecessary re-evaluation.

### Multi-Unit and Emergent Requirements

Some requirements span many code units and cannot be assigned to a single VQP — timing budgets, memory limits, scheduling deadlines, system-level safety properties. These requirements emerge from the behavior of the whole, not from any one function.

**Current scope**: noted as architecture challenge. Multi-unit requirements are not required for the Stage 1 C-code prototype.

**Likely solution path**: System-Level VQPs that consume static analysis tool summary outputs (timing analyzer results, memory profiler summaries) rather than raw multi-function source code. The static analysis tool performs the cross-unit reasoning; the VQP verifies that the tool's output satisfies the requirement.

### Conflict Resolution Economics and Retroactive VRM Updates

When a human reviewer overrides an LLM result, should the VRM score retroactively update for all past evaluations of the same query? This requires version tracking on all VRM computations, propagation of profile changes to historical VRM values, and a policy for how long a human override stands before requiring re-evaluation.

**Current scope**: out of scope. VRM is computed fresh from current results.

**Future design constraint**: the clean solution requires the graph invalidation infrastructure above. A human override should stand as long as nothing relevant to that VQP has changed. When any input to the VQP changes — code, requirements, prompt version, model version — the override is invalidated and re-evaluation is required.

### Human-in-the-Loop Economics and Scalability

The system's accuracy calibration loop depends on human overrides: when a human reviewer disagrees with an LLM result, the disagreement updates the `(Model_ID, Prompt_Version, Task_Type)` `ModelAccuracyProfile`. This dependency creates an economics problem: if a particular combination has a high false-positive rate (the model flags many VQPs as failing that human reviewers approve), it will flood the human review queue. The economic and speed advantages of the system erode precisely when the model performs poorly — the case where human review is most needed.

**Current scope**: not addressed in Stage 1. Manual monitoring of disagreement rates is expected.

**Future design constraint**: the architecture needs a monitoring mechanism that tracks the human override rate per `(Model_ID, Prompt_Version, Task_Type)` and automatically flags poorly-performing combinations. When the override rate for a combination exceeds a configured threshold (e.g., 30% of LLM-fail verdicts reversed by human reviewers), the system should alert the engineering team and queue the combination for re-qualification or replacement. This closes the loop between the accuracy profile and the model assignment policy: combinations with poor task-specific performance should be rotated out of that task type before they degrade the system's economic viability. The disagreement rate reporting mechanism (see Automation Bias Mitigation) provides the necessary data; the scheduling and alerting logic is the missing piece.

### VQP Size Limits and Evidence Decomposition

A VQP must fit within the context window of the assigned reviewer. For complex leaf nodes — functions implementing many requirements, units referencing voluminous specifications, modules with large test suites — the assembled VQP may exceed this bound. Evidence truncation to meet size limits is explicitly forbidden: a requirement evaluated against incomplete evidence is not verified and cannot enter the certification evidence record.

Three strategies address oversized VQPs, in order of architectural soundness:

**Hierarchical VQP splitting.** A parent VQP is split into child VQPs each covering a subset of requirements. Child results are composed into a parent verdict via a declared aggregation rule. Soundness requires that child VQPs be logically independent — if sub-requirements interact, split evaluation may miss integration-level failures. The composition relationship and aggregation rule must be recorded in the graph.

**Tool-summary nodes.** Large deterministic evidence sets (50 test results, a 300-page datasheet) are processed by a qualified deterministic tool — a test runner emitting a structured pass/fail count with coverage metrics, or a parser extracting the relevant datasheet section. The summary node carries a content hash linking it cryptographically to the raw artifacts. LLM-generated summaries are explicitly excluded from this pattern: LLM summarization introduces hallucination risk directly into the evidence base.

**Proof composition (assume-guarantee).** Engineers define explicit interface contracts at component boundaries. Each component is verified against its local contract independently; a parent VQP verifies that the composed contracts satisfy the parent requirement. This is the architecturally sound pattern for large-scale decomposition, analogous to assume-guarantee reasoning in formal verification, and improves the audit trail by making component boundaries explicit.

**Emergent properties.** Some system-level properties — end-to-end timing constraints, memory partitioning safety properties, freedom from priority inversion — cannot be verified by examining individual leaf nodes regardless of VQP size. They arise from the interactions of the whole, not from any single function. These require Whole-Program Analysis (WPA) tools: timing analyzers, stack analyzers, abstract interpretation engines. The VC architecture treats these tool outputs as first-class DAG evidence nodes — the LLM's role in the corresponding VQP is not to infer the property from code, but to verify that the WPA tool's output satisfies the requirement's stated bound. Stage 1 does not claim coverage of emergent properties.

**Current scope**: VQP size is bounded by graph construction discipline. Hierarchical splitting and tool-summary nodes are the near-term implementation paths. Proof composition and WPA integration are Stage 2 targets. A formal VQP budget specification (maximum tokens per VQP per task type) is a planned Stage 2 artifact.

### DAG Cycle Detection and Requirements Refactoring

Requirement relationships that are mutually dependent — Module A's behavior depends on Module B, and Module B's behavior depends on Module A — create cycles in the traceability graph. The VC detects and hard-rejects all cycles at graph construction time. Cyclic traceability is circular reasoning: a cycle implies that verification of node A depends on verification of node B, which depends on A, producing infinite regress with no sound termination.

In practice, apparent requirement cycles arise from genuine functional coupling — bidirectional interface contracts, shared resource constraints, closed-loop control — but the functional relationship and the traceability relationship are distinct. Every category of genuine functional cycle has a sound DAG representation through one of three refactoring patterns described in the Artifact Graph section: elevation of shared constraints to a parent requirement, interface contract nodes using assume-guarantee decomposition, or temporal state separation. These patterns resolve the common cases without loss of semantic content.

When graph construction detects a cycle, it surfaces the affected nodes and the edge that would close the cycle. If the cycle cannot be resolved by refactoring, it signals a software architecture that is not decomposable for independent verification — an architectural coupling problem that the VC surfaces but cannot resolve on its own. In safety-critical engineering, an un-decomposable cycle is an architectural deficiency, not a tooling limitation.

**Open question**: the VC's cycle detection is currently binary — a graph either builds successfully or fails. A more nuanced handling would classify detected cycles by category, suggest the applicable refactoring pattern, and allow partial graph builds that evaluate the acyclic subgraph while surfacing the cyclic nodes as unresolved anomalies. This is a planned Stage 2 feature.

### Data and Control Coupling Coverage (DCCC)

DO-178C Section 6.4.4 requires confirmation that requirements-based testing has exercised the data coupling and control coupling between code components — inter-module dependencies where one component reads data set by another, or where one component influences another's execution path. DCCC is an integration-level objective: it can only be observed on integrated code and explicitly focuses on interactions across module boundaries. It is required for DAL A–C projects with independence at DAL A and B.

The Verification Compiler's Stage 1 per-leaf-node VQP structure is, by construction, blind to cross-module coupling paths. A VQP evaluates a leaf code unit against its local requirement chain; it does not observe how that unit's outputs are consumed by other units or how calling patterns propagate across integration boundaries.

DCCC does not invalidate the VC architecture, but it identifies a complementary verification activity outside Stage 1 scope. Specialized DCCC tools — VectorCAST/Coupling, LDRA, Rapita RapiCoupling — perform dynamic instrumentation to identify and verify all data and control coupling paths across a component boundary. These tools generate structured coupling analysis reports. The VC artifact graph is designed to consume such reports as integration-level evidence nodes: a DCCC analysis result enters as an `analyzed-by` edge from a subsystem node (not a leaf node), and an integration-level VQP verifies that the report confirms all required coupling paths are covered. This pattern generalizes: the VC does not perform DCCC analysis internally; it consumes and verifies DCCC reports as structured evidence.

**Current scope**: DCCC is an identified gap in Stage 1's leaf-node scope. Integration-level VQPs consuming DCCC tool reports are a Stage 2 target, aligned with expanding scope to integration-level and HLR-to-LLR traces.

### Object Code Verification

The Verification Compiler operates at source code level. Verifying that a compiled binary faithfully represents the source code — Object Code Verification (OCV) as defined in DO-178C Section 6.4.4.e — is a separate objective. Where a qualified compiler is not used, OCV requires review of object code against source to confirm no spurious code was introduced and no required behavior was eliminated by compiler optimization.

This objective is not within the Verification Compiler's scope, nor does it need to be. Qualified compiler pathways (DO-178C Section 12.2) and dedicated OCV tools (e.g., Polyspace, CompCert for specific targets) address this obligation through their own defined processes. The VC architecture accepts OCV tool outputs as first-class evidence nodes using the same pattern as DCCC and static analysis: an OCV result enters the graph as an `analyzed-by` edge, and the relevant VQP verifies that the result confirms no deviation between source and object code for the code unit under review. The VC's role is to verify that the evidence requirement is satisfied — not to re-implement the analysis.

**Current scope**: OCV is out of Stage 1 scope. The architecture is designed to receive OCV evidence as graph nodes in Stage 2 certification-tier integration.

## Limitations and Open Questions

The Verification Compiler is presented here as an architectural proposal and a research direction. Several critical empirical questions remain open, and intellectual honesty requires stating them before the Conclusion.

**The LLM efficacy question is unresolved.** The entire system's development-cycle value depends on the hypothesis that current language models can provide a useful pre-screen signal when given bounded LLR-to-Code and Code-to-Test queries. This is not yet established for the specific query types and codebase characteristics the compiler targets. The overcorrection finding [arXiv:2603.00539] suggests the error pattern may be asymmetric and task-dependent. Stage 2 exists to test this hypothesis empirically — the Verification Compiler's architecture is the prerequisite structure for running that test safely.

**The VRM needs empirical calibration.** The Verification Readiness Metric formula is defined but not yet operationalized at scale. The evidence-type weights `w_k` in the vertical completeness term require empirical validation: what relative weighting of requirement links, test artifacts, test results, and static analysis outputs correctly reflects pre-screen confidence? This is a research question, not a design decision that can be made in advance. Additionally, the Model Suitability threshold — the minimum task-specific PPV required before a model may operate in LLM review mode — requires calibration from Stage 2 empirical data. The threshold directly determines how much human review time is protected from unreliable pre-screen signals.

**Automation bias mitigations are not yet empirically validated for this context.** Evidence-first presentation and canary queries are architecturally sound responses to automation bias, and both draw on established human factors principles — display prompt countermeasures and accountability effect interventions have been empirically demonstrated to reduce automation-related errors in aviation supervisory control tasks [Mosier & Skitka, 1996–1997]. However, their effectiveness in the specific context of verification query review has not been demonstrated. Stage 2 will include a human factors protocol to measure reviewer response rates on canary queries over time.

**Graph construction and maintenance cost.** The tool provides maximum value to teams with existing disciplined requirements management. Teams building the graph from scratch face a real initial investment in encoding traceability links; this cost is not eliminated, but it is reframed. Because graph recomposition is computationally cheap (no LLM calls, no network round-trips), developers can update graph edges as part of the normal PR workflow, in the same commit that changes code. The CI run then re-evaluates only the stale VQPs — shifting the pattern from expensive periodic manual reviews to lightweight continuous graph maintenance with selective LLM re-evaluation. The compiler makes the cost of skipping updates immediately visible: a broken link stops the affected VQP from assembling on the next run, creating a tight feedback loop rather than an end-of-cycle surprise.

**Scope is narrower than full verification.** Stage 1 covers LLR-to-Code and Code-to-Test traces for leaf-node C functions. It does not yet cover HLR-to-LLR consistency, system-level interactions, non-functional requirements (timing, memory, scheduling), or derived requirements. These are known gaps with planned Stage 2 coverage, not oversights.

## Related Work

**Requirements traceability and link generation.** TraceLLM [Alturayeif et al., arXiv:2602.01253, 2026] applies prompt engineering and demonstration selection to generate and complete requirements traceability links across requirements, design elements, test cases, and regulations, achieving state-of-the-art F2 scores across aerospace and healthcare domains. Graph-RAG [Masoudifard et al., arXiv:2412.08593, 2024] combines graph-structured retrieval with chain-of-thought prompting to verify SRS compliance against higher-level organizational requirements. Both address the problem of *traceability link generation* — identifying which artifacts should be connected. The Verification Compiler operates downstream: it assumes a populated artifact graph and focuses on *verification assessment* — whether linked artifacts satisfy their obligations. These two problem spaces are complementary. Empirical results in both traditions confirm the importance of bounded queries: F1 score degrades from 0.92 to 0.81 as requirements per query grows from 5 to 20 [Reinpold et al., 2024], directly supporting the VQP decomposition design.

**LLM accuracy on verification tasks.** Recent work on LLM requirement conformance checking finds that models systematically overcorrect, flagging correct code as non-compliant at higher rates than flagging genuinely incorrect code [arXiv:2603.00539, 2026]. This asymmetric error pattern — false positives dominate over false negatives — is a specific, actionable finding: the Verification Compiler's ModelAccuracyProfile maintains separate PPV and NPV rather than a single accuracy number, and surfaces both to human reviewers to enable calibrated response to pre-screen signals.

**Formal methods precedent.** Assume-guarantee reasoning [Cobleigh, Giannakopoulou & Pasăreanu, 2003] decomposes verification of large systems into component-level sub-problems where each component is verified against assumptions about its environment. The Verification Compiler applies an analogous principle: each leaf-node VQP is self-contained with its full requirement chain as the assumption context. The DAG structure ensures local verdicts compose into a global coverage proof. This precedent also informs the VQP decomposition strategy for large-scale systems (see Known Architectural Challenges).

**Industrial requirements management.** IBM Engineering Requirements DOORS, Jama Connect, Siemens Polarion ALM, and similar ALM platforms address requirements traceability maintenance at the project lifecycle level. Polarion has added LLM-assisted features for requirements quality checking and test case generation, targeting authoring productivity rather than verification assessment. The Verification Compiler maintains its own artifact graph, distinct from these project lifecycle databases; the two systems address different structural problems. The gap ALM tools do not address — automated, bounded, evidence-backed assessment of whether linked artifacts satisfy their obligations — is the Verification Compiler's contribution.

**Regulatory context.** The joint SAE G-34/EUROCAE WG-114 ED-324/ARP6983 standard [EUROCAE WG-114, 2025] establishes process requirements for ML components *embedded in* operational certified avionics systems. This is architecturally distinct from the Verification Compiler's LLM use: the VC's LLMs are developmental aids external to the certified system, not components within it. The applicable regulatory framework for the VC's deterministic components is DO-330 tool qualification, not ED-324 ML design assurance.

## Conclusion and Stage 2 Direction

Software teams have continuous integration for builds and tests. The Verification Compiler brings continuous integration to verification: a tractable, continuously-updated signal for how ready a codebase is to be verified against its requirements. This is its core value. The formal certification pathway is what the architecture is designed to grow into — not the only reason to use it.

The architecture's key resolution is structural equivalence: the same DAG, the same query packages, the same evidence schema serve both the LLM-driven development cycle and the human-conducted certification pass. LLMs provide rapid, broad pre-screening without displacing qualified human review. Human review, when it occurs, works from a pre-assembled evidence package rather than a manual artifact-gathering exercise. The system scales from a development-team CI component to a DO-178C certification tool by adjusting reviewer, VRM threshold, and CD policy — not by changing the underlying architecture.

The core properties of the Stage 1 design are:

- **Deterministic decomposition**: the artifact graph is a DAG; traversal is deterministic; query assembly is reproducible from graph state and prompt version alone.
- **Reviewer replaceability**: any query package can be processed by an LLM or by a human reviewer using the same interface; the two are structurally interchangeable, though only human verdicts constitute certification evidence in formal programs.
- **Provable scope**: the graph structure itself proves evaluation completeness; orphan nodes surface as anomalies before any review begins.
- **VRM as development signal**: the Verification Readiness Metric tracks pre-screen progress without making a safety claim; it tells engineering teams when the codebase is ready for the next review gate — human pass, release, or certification — at whatever rigor level the project requires.
- **Automation bias controls**: evidence is presented to human reviewers before any LLM pre-screen result is revealed; canary queries validate that human review remains attentive.
- **TQL-5 qualifiable deterministic core**: the graph traversal, query assembly, and invariant enforcement components are architecturally qualifiable under DO-330 TQL-5 for teams that need it.

Stage 2 priorities: implement the prototype on a representative embedded C codebase; establish empirical task-specific accuracy profiles for LLM review on LLR-to-Code and Code-to-Test trace evaluation; validate the VRM signal against human reviewer agreement rates; validate the canary query mechanism; and extend scope to HLR-to-LLR consistency traces.

## References

1. N. Alturayeif, H. Lutfi, and M. Ahmed, "TraceLLM: Harnessing Large Language Models for Traceability Link Generation in Safety-Critical Systems," *arXiv*:2602.01253, 2026. https://arxiv.org/abs/2602.01253

2. D. Amodei, interview with D. Patel, *Dwarkesh Podcast*, 2025. https://www.dwarkesh.com/p/dario-amodei-2

3. J. M. Cobleigh, D. Giannakopoulou, and C. S. Pasăreanu, "Learning Assumptions for Compositional Verification," in *Proc. Tools and Algorithms for the Construction and Analysis of Systems (TACAS 2003)*, Lecture Notes in Computer Science, vol. 2619, Springer, pp. 331–346, 2003. NASA NTRS 20030017771. https://ntrs.nasa.gov/citations/20030017771

4. European Union Aviation Safety Agency (EASA), *Artificial Intelligence Roadmap 2.0: A Human-Centric Approach to AI in Aviation*, May 2023. https://www.easa.europa.eu/en/document-library/general-publications/easa-artificial-intelligence-roadmap-20

5. EUROCAE WG-114 / SAE G-34, *ED-324/ARP6983: Process Standard for Development and Certification Approval of Aeronautical Products Implementing AI*, EUROCAE/SAE International, 2025. https://eurocae.net/news/posts/2023/november/eurocae-and-sae-release-a-new-standard-on-artificial-intelligence/

6. U.S. Federal Aviation Administration (FAA), *Advisory Circular 20-115D: Airborne Software Development Assurance Using EUROCAE ED-12( ) and RTCA DO-178( )*, Jul. 21, 2017. https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-115D.pdf

7. U.S. Federal Aviation Administration (FAA), *Roadmap for Artificial Intelligence Safety Assurance, Version I*, Jul. 2024. https://www.faa.gov/media/82891

8. H. Jin and H. Chen, "Are LLMs Reliable Code Reviewers? Systematic Overcorrection in Requirement Conformance Judgement," *arXiv*:2603.00539, 2026. https://arxiv.org/abs/2603.00539

9. S. A. Jacklin, "Certification of Safety-Critical Software Under DO-178C and DO-278A," NASA Ames Research Center, NASA NTRS 20120016835, 2012. https://ntrs.nasa.gov/citations/20120016835

10. T. Khot, H. Trivedi, M. Finlayson, Y. Fu, K. Richardson, P. Clark, and A. Sabharwal, "Decomposed Prompting: A Modular Approach for Solving Complex Tasks," in *Proc. ICLR 2023*, arXiv:2210.02406, 2022. https://arxiv.org/abs/2210.02406

11. M. Masoudifard et al., "Graph-RAG for Software Requirements Compliance Verification," *arXiv*:2412.08593, 2024. https://arxiv.org/abs/2412.08593

12. L. Miculicich, M. Parmar, H. Palangi, K. D. Dvijotham, M. Montanari, T. Pfister, and L. T. Le, "VeriGuard: Enhancing LLM Agent Safety via Verified Code Generation," *arXiv*:2510.05156, Oct. 2025. https://arxiv.org/abs/2510.05156

13. K. L. Mosier, L. J. Skitka, M. R. Burdick, S. T. Heers, and M. R. Rosekind, "Decision Making in a High-Tech World: Automation Bias and Countermeasures," *Proc. Society for Judgment and Decision Making*, 1996. NASA NTRS 20020041010. https://ntrs.nasa.gov/citations/20020041010

14. K. L. Mosier, L. J. Skitka, M. Dunbar, L. McDonnell, and M. Rosekind, "Automation Bias and Countermeasures in Flight Crews," 1997. NASA NTRS 20020043049. https://ntrs.nasa.gov/citations/20020043049

15. NASA, *NASA Procedural Requirements NPR 7150.2D: NASA Software Engineering Requirements*, Office of the Chief Engineer, effective Mar. 8, 2022. https://nodis3.gsfc.nasa.gov/displayDir.cfm?t=NPR&c=7150&s=2D

16. NASA, *NASA-STD-8739.8B: Software Assurance and Software Safety Standard*, approved Sep. 8, 2022. https://standards.nasa.gov/standard/nasa/nasa-std-87398b

17. L. M. Reinpold, M. Schieseck, L. P. Wagner, F. Gehlhoff, and A. Fay, "Exploring LLMs for Verifying Technical System Specifications Against Requirements," *arXiv*:2411.11582, Nov. 2024. https://arxiv.org/abs/2411.11582

18. L. Rierson, *Developing Safety-Critical Software: A Practical Guide for Aviation Software and DO-178C Compliance*, CRC Press, 2013. ISBN 978-1-4398-5253-4.

19. TIGER-AI-Lab, "MMLU-Pro: A More Robust and Challenging Multi-Task Language Understanding Benchmark," *arXiv*:2406.01574, *Proc. NeurIPS 2024 (Spotlight)*, 2024. https://arxiv.org/abs/2406.01574

20. P. Zave and M. Jackson, "Four Dark Corners of Requirements Engineering," *ACM Trans. Softw. Eng. Methodol.*, vol. 6, no. 1, pp. 1–30, Jan. 1997. https://doi.org/10.1145/237432.237434

### Standards

21. IAQG, *AS9100D: Quality Management Systems — Requirements for Aviation, Space, and Defense Organizations*, SAE International, rev. D, 2016. https://www.sae.org/standards/content/as9100d/

22. IEC, *IEC 62443: Security for Industrial Automation and Control Systems* (series), International Electrotechnical Commission, 2018–2022. https://www.iec.ch/iec62443

23. ISO, *ISO 26262: Road Vehicles — Functional Safety*, 2nd ed., International Organization for Standardization, 2018. https://www.iso.org/standard/68383.html

## List of Acronyms

| Acronym | Expansion |
|---|---|
| ADAS | Advanced Driver Assistance Systems |
| ASIL | Automotive Safety Integrity Level |
| CI | Continuous Integration |
| CD | Continuous Delivery / Continuous Deployment |
| DAG | Directed Acyclic Graph |
| DAL | Design Assurance Level |
| DO-178C | RTCA Document for Avionics Software (Software Considerations in Airborne Systems and Equipment Certification) |
| DO-330 | RTCA Software Tool Qualification Considerations |
| EASA | European Union Aviation Safety Agency |
| FAA | Federal Aviation Administration |
| HCI | Human-Computer Interaction |
| HLR | High-Level Requirement |
| IEC | International Electrotechnical Commission |
| ISO | International Organization for Standardization |
| LLM | Large Language Model |
| LLR | Low-Level Requirement |
| MBSE | Model-Based Systems Engineering |
| MCDC | Modified Condition/Decision Coverage |
| NFR | Non-Functional Requirement |
| RTCA | formerly Radio Technical Commission for Aeronautics |
| SL | Security Level (IEC 62443) |
| TAS | Tool Accomplishment Summary |
| TOR | Tool Operational Requirements |
| TQL | Tool Qualification Level |
| TQP | Tool Qualification Plan |
| UoI | Unit of Intelligence |
| VRM | Verification Readiness Metric |
| WCET | Worst-Case Execution Time |
