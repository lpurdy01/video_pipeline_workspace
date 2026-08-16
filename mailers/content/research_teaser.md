# Bounded LLM Review for Continuous Verification

**A Graph-Decomposition Architecture for Safety-Critical Software**
*Levi Purdy — Student, University of Wisconsin-Madison — lpurdy01@gmail.com*

---

## The Problem

Safety-critical software development requires continuous traceability between requirements,
implementation, test coverage, and review records. Current practice accumulates this evidence
manually through periodic audits — expensive, error-prone, and disconnected from daily CI
workflows.

Natural-language specifications drift from implementations. Evidence for one requirement
is scattered across multiple tools and documents. When a certifier asks "show me that
requirement 4.2.1 is covered," the answer requires assembling artifacts from a half-dozen
sources and hoping the chain is unbroken.

---

## The Architecture: A Verification Compiler

The Verification Compiler (VC) treats these artifacts as a **directed acyclic graph** (DAG).
Requirements decompose into testable sub-requirements. Source code units trace to requirements.
Test cases trace to code units. Static analysis, coverage data, and physical test records
attach as evidence nodes. The graph structure enforces what the standard requires: traceability
must form an acyclic chain from requirement through implementation to evidence.

A deterministic compiler pass traverses this DAG and produces **Verification Query Packages**
(VQPs) — bounded, self-contained evidence bundles. Each VQP contains exactly the artifacts
needed to evaluate one requirement against its implementation: the requirement text, relevant
code, applicable tests, analysis outputs, and prior review history. VQP size is bounded by
architecture, not by LLM context limits.

---

## The Reviewer Endpoint

VQPs are submitted to a **replaceable reviewer endpoint**. During development, an LLM
returns structured JSON verdicts (pass / fail / uncertain + citations). For formal
certification, the same evidence package goes to a qualified human reviewer.

The LLM is explicitly a *developmental pre-screen only*. Its results are labeled as
non-certifying. The certification endpoint is always human.

This separation is the core architectural claim: the deterministic evidence compiler is
qualifiable under DO-330 (TQL-5); the reviewer endpoint is swappable without changing the
graph or the evidence format.

---

## Continuous Verification Signal: VRM

**VRM = &Sigma; C_v(i) / N** — the fraction of requirements with a complete evidence
chain in the current build. A VRM of 1.000 means every requirement is covered. VRM below
1.0 identifies exactly which requirements are missing coverage and why, surfaced in CI
before anyone opens a review document.

**Stage 1 prototype result: VRM = 1.000 on 31 architectural requirements.**

---

## Why This Is Defensible in Safety-Critical Contexts

The architecture does not ask regulators to trust an LLM. It asks them to evaluate a
deterministic graph traversal and evidence packaging layer — something that can be
reviewed, tested, and qualified using existing DO-330 tool qualification procedures.
The LLM reviewer slot is no different in principle from a human reviewer slot: it receives
a structured evidence package and returns a structured verdict.

This maps onto the DO-178C tool equivalence pathway (Section 9.3): a tool may achieve
equivalence to a human verification activity when it can be shown to produce equivalent
evidence. The VC is designed so that equivalence — or its absence — is auditable.

---

## Current Status

**Stage 1:** Architecture specification complete. 31 sub-requirements defined, 27+ citations
verified. Prototype evaluator operational (Python). Full whitepaper available.

**Stage 2 (planned):** Runtime prototype integrating with real DO-178C project artifacts.
Formal accuracy evaluation of LLM reviewer (PPV/NPV) against human baseline. IDE plugin
for human reviewer interface.
