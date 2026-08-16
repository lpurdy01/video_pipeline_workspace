# Verification Compiler

## Definition

The verification compiler is a hierarchical requirements and verification results tracking infrastructure that links a C codebase to every artifact needed to prove software safety — datasheets, interface specifications, static analysis results, tests, physical test results, memory tool outputs, and certification evidence — and then traverses that graph to decompose verification into units a model can evaluate.

It is called a compiler by analogy: just as a software compiler transforms source code through a defined, mechanical process into a verified artifact, the verification compiler transforms a linked artifact graph through a defined traversal process into structured verification evidence.

## Core Architecture

### The Artifact Graph

Every node in the graph is a verification-relevant artifact:

- Source code units (functions, modules, subsystems)
- Requirements (high-level, low-level, derived)
- Interface specifications and datasheets
- Static analysis results (memory safety, timing, coverage)
- Unit tests and integration tests
- Physical test results (tied to a specific code version and artifact hash)
- Review records and model outputs
- Certification evidence packages

Edges are typed hierarchical links: a requirement traces to child requirements, child requirements trace to code, code traces to tests, tests trace to results, results trace to physical evidence. The linking structure is the formal representation of coverage.

### Graph Traversal as Decomposition

Verification proceeds by graph traversal. Starting from a top-level requirement node, the traversal walks the graph and collects, for each leaf code unit:

- The code unit itself
- All requirements linked to it (from all ancestor levels)
- All tests and analysis results linked to it
- Any physical test evidence linked to the same version

This collection defines a **verification query**: a self-contained bundle of code, context, and evidence sized to fit within a model's context window. The traversal guarantees completeness — every code unit reachable from a requirement is eventually queried.

### Context Window as Design Primitive

The context window is not merely a limitation to work around. It is the unit of work the system is designed around.

Each verification query is sized and bounded so that a model can reason over it reliably: code chunk + linked requirements + linked tests + linked evidence, assembled into a structured prompt. The hierarchical decomposition is what makes this possible — large requirements trees are recursively broken into subtrees whose corresponding code and evidence fit within a single query.

This is structurally analogous to how DO-178C decomposes verification: requirements are reviewed atomically with traceability links ensuring that the full scope is covered. The verification compiler mechanizes that decomposition.

### Dual-Mode Operation

The same graph decomposition supports two execution modes:

**LLM review mode:** each verification query is submitted to a qualified model. The model returns a structured result: pass, fail, uncertain, with a confidence value and a rationale. The confidence value is weighted by the model's accuracy profile for that task type.

**Human review mode:** each verification query is presented to a human reviewer in a structured review package. The human returns a pass/fail judgment with notes. The decomposition is identical — only the reviewer changes. This makes the two modes directly comparable and interchangeable.

For final release, human review mode can replace LLM review mode on any subset of the graph. For continuous integration or pre-review screening, LLM review mode produces a confidence-scored snapshot of the verification state.

### Confidence Score (Verification Readiness Metric)

The verification compiler outputs a **Verification Readiness Metric (VRM)** for the evaluated scope:

```
C_h = N_eval / N_total                        (horizontal coverage)
C_v(i) = Σ_k w_k × I_k × S_k                (vertical evidence completeness for query i)
V(i) = PPV    if reviewer says PASS           (from ModelAccuracyProfile)
V(i) = 1-NPV  if reviewer says FAIL

VRM = C_h × (1/N_eval) × Σ_i C_v(i) × V(i)
```

Where `S_k ∈ [0,1]` is a staleness discount — evidence tied to a different code version than the current artifact is discounted toward zero. `PPV` and `NPV` come from the **ModelAccuracyProfile** for the `(Model_ID, Prompt_Version, Task_Type)` combination used for that query. A model with high false-positive rate (flags correct code as non-compliant) produces a low PPV, making each PASS worth less in the VRM — the asymmetry identified in LLM compliance evaluation research is directly captured.

The VRM is not a binary certified/not-certified result. It is a calibrated estimate of verification readiness given the evidence assembled. Human reviewers can inspect the component breakdown — C_h, each C_v(i), each V(i) — drill into failing or uncertain nodes, and make certification decisions with quantified confidence rather than opaque totals.

### Physical Test Evidence

Physical test results from human functional testing can be included in the graph as long as:

1. The test was run against a specific, identified version of the code (hash or revision tied to a specific artifact node)
2. The test artifacts (inputs, outputs, procedures, pass/fail records) are structured in a format the LLM can parse
3. The test is linked to the requirements it exercises

When these conditions hold, physical test evidence enters the graph as a first-class node and is included in the relevant verification queries.

## Provable Decomposition

The graph structure itself is the proof that the decomposition is complete. If all code units are reachable from requirements through typed links, and all requirements are linked to code, then the traversal covers the full scope of the specification. Orphan code units (code with no requirement link) and orphan requirements (requirements with no code link) are surfaced as graph anomalies, analogous to DO-178C traceability failures.

This makes the decomposition auditable independently of the model results: a certification body or human reviewer can inspect the graph structure and confirm that the scope of evaluation is correct before inspecting any individual query result.

## Relationship to DO-178C Verification Objectives

The verification compiler is not a DO-178C tool in the regulatory sense. It is a pattern inspired by DO-178C's requirement that verification produce auditable life-cycle evidence through review, analysis, and test. The compiler produces:

- Structured evidence records for each verification query
- Traceability from evidence to source requirements
- Coverage metrics showing what has and has not been evaluated
- A provable decomposition showing how the whole was broken into parts

These outputs are intended to support, not replace, human certification judgment. The compiler's role is to make the evidence surface area smaller and more navigable for human reviewers and certification bodies.

## Source Region Addressing: Documents as ASTs

The VC's deterministic decomposition depends on stable, machine-readable pointers to evidence. For code, this is straightforward — a function has a file path, name, and content hash. For reference documents (standards, datasheets, ICDs), it requires treating the document's hierarchical structure the same way a compiler treats an AST.

Technical engineering documents are already AST-structured — they just encode structure in typography and numbering rather than syntax:

| Document type | Example reference | Structure |
|---|---|---|
| DO-178C | "Section 6.3.b, Table A-1" | Chapter > Section > Subsection > Table > Row |
| ICD | "Interface 3.2.1, Signal VOLTAGE_IN" | ICD > Interface > Signal parameter |
| 14 CFR | "14 CFR § 25.1309(b)(1)(ii)" | Title > Part > Section > Para > Sub-para |
| ISO 26262 | "ISO 26262:2018 Part 6 § 8.4.3" | Standard > Part > Section > Subsection |

Engineers already cite by section number universally. The VC formalizes these into **`URI_Locator`** primary keys on **SourceRegionNodes**, with a `Content_Hash` that detects text changes even when the section number is stable. A hash change invalidates all `supports-claim` edges from that region, requiring human re-confirmation before VQPs can be assembled.

At VQP assembly time, the resolver fetches the actual text of the cited region and injects it directly into the prompt — not just a citation label. The VQP must contain the text being evaluated, making it self-contained and independently auditable.

## Open Architecture Questions

- What is the minimum evidence package for a node result to be accepted into the graph?
- How does the system handle requirements that span multiple code units (cross-cutting concerns)? (See deferred challenge REQ-8.2 — static analysis tool outputs as a likely path)
- What tool integrations are needed first: static analysis, memory tooling, test harnesses?
- How should graph invalidation work when source regions change? (See deferred challenge REQ-8.1)
