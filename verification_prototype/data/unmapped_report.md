# Whitepaper Unmapped Section Report
Generated: 2026-05-30

This deterministic report checks reverse coverage before a verification run.
It is advisory: a whitepaper can legitimately contain narrative, examples, and related work that are not system requirements.

## Summary

- Sections parsed: 52
- Sections directly mapped to requirements: 27
- Subsections inheriting parent requirement context: 10
- Strictly unmapped sections: 15
- Advisory unmapped substantive sections: 2
- Unmapped scaffold/front-back/example sections: 13
- Claims with source support but no located whitepaper section: 2
- Claims without source support: 0
- Source notes not used by any current claim edge: 4

## Advisory Unmapped Sections

- `SEC-english-as-a-specification-medium` (2) English as a Specification Medium - located claims: 5
- `SEC-safety-critical-verification-as-a-coordination-system` (2) Safety-Critical Verification as a Coordination System - located claims: 7

## Unmapped Scaffold / Narrative Sections

- `SEC-working-title` (2) Working Title - located claims: 0
- `SEC-introduction` (2) Introduction - located claims: 1
- `SEC-introduction-terminology-note` (3) Introduction / Terminology Note - located claims: 0
- `SEC-motivation` (2) Motivation - located claims: 0
- `SEC-worked-example-one-function-through-the-compiler` (2) Worked Example: One Function Through the Compiler - located claims: 0
- `SEC-worked-example-one-function-through-the-compiler-the-code-un` (3) Worked Example: One Function Through the Compiler / The Code Unit - located claims: 0
- `SEC-worked-example-one-function-through-the-compiler-the-artifac` (3) Worked Example: One Function Through the Compiler / The Artifact Graph Fragment - located claims: 0
- `SEC-worked-example-one-function-through-the-compiler-the-verific` (3) Worked Example: One Function Through the Compiler / The Verification Query (submitted to model or human reviewer) - located claims: 0
- `SEC-worked-example-one-function-through-the-compiler-the-structu` (3) Worked Example: One Function Through the Compiler / The Structured Result - located claims: 0
- `SEC-limitations-and-open-questions` (2) Limitations and Open Questions - located claims: 2
- `SEC-related-work` (2) Related Work - located claims: 3
- `SEC-conclusion-and-stage-2-direction` (2) Conclusion and Stage 2 Direction - located claims: 1
- `SEC-list-of-acronyms` (2) List of Acronyms - located claims: 1

## Requirement-Mapped Sections

- `SEC-concept-verification-compiler` Concept: Verification Compiler -> REQ-1-2, REQ-1-3, REQ-1-4, REQ-2-1, REQ-2-2, REQ-2-3, REQ-3-1, REQ-3-2, REQ-3-3, REQ-3-3b, REQ-4-1, REQ-4-2, REQ-4-3, REQ-5-1, REQ-5-2, REQ-5-3, REQ-6-1
- `SEC-concept-verification-compiler-automation-bias-mitigation-and` Concept: Verification Compiler / Automation Bias Mitigation and Reviewer Independence -> REQ-6-1
- `SEC-concept-verification-compiler-dual-mode-operation` Concept: Verification Compiler / Dual-Mode Operation -> REQ-3-1, REQ-3-2, REQ-3-3, REQ-3-3b, REQ-3-4
- `SEC-concept-verification-compiler-evidence-auditability-and-conf` Concept: Verification Compiler / Evidence, Auditability, and Configuration Management -> REQ-5-1, REQ-5-2, REQ-5-3
- `SEC-concept-verification-compiler-graph-traversal-as-decompositi` Concept: Verification Compiler / Graph Traversal as Decomposition -> REQ-2-1, REQ-2-2, REQ-2-3
- `SEC-concept-verification-compiler-llm-reliability-and-the-mitiga` Concept: Verification Compiler / LLM Reliability and the Mitigation Architecture -> REQ-3-1, REQ-3-2, REQ-3-3, REQ-3-3b, REQ-6-1
- `SEC-concept-verification-compiler-provable-decomposition` Concept: Verification Compiler / Provable Decomposition -> REQ-5-1, REQ-5-2, REQ-5-3
- `SEC-concept-verification-compiler-regulatory-pathway` Concept: Verification Compiler / Regulatory Pathway -> REQ-6-1
- `SEC-concept-verification-compiler-reviewer-qualification-and-ind` Concept: Verification Compiler / Reviewer Qualification and Independence -> REQ-6-1
- `SEC-concept-verification-compiler-the-artifact-graph` Concept: Verification Compiler / The Artifact Graph -> REQ-1-1, REQ-1-2, REQ-1-3, REQ-1-4, REQ-8-5
- `SEC-concept-verification-compiler-verification-query-and-result-` Concept: Verification Compiler / Verification Query and Result Schema -> REQ-3-1, REQ-3-2, REQ-3-3, REQ-3-3b, REQ-3-4, REQ-3-5
- `SEC-concept-verification-compiler-verification-readiness-metric` Concept: Verification Compiler / Verification Readiness Metric -> REQ-1-1, REQ-4-1, REQ-4-2, REQ-4-3
- `SEC-core-concept-units-of-intelligence` Core Concept: Units of Intelligence -> REQ-3-1, REQ-3-2, REQ-3-3
- `SEC-deployment-contexts` Deployment Contexts -> REQ-3-3b, REQ-5-1, REQ-5-2, REQ-5-3, REQ-6-1
- `SEC-known-architectural-challenges` Known Architectural Challenges -> REQ-8-1, REQ-8-2, REQ-8-3, REQ-8-4, REQ-8-5, REQ-8-6, REQ-8-7
- `SEC-known-architectural-challenges-conflict-resolution-economics` Known Architectural Challenges / Conflict Resolution Economics and Retroactive VRM Updates -> REQ-8-3
- `SEC-known-architectural-challenges-dag-cycle-detection-and-requi` Known Architectural Challenges / DAG Cycle Detection and Requirements Refactoring -> REQ-8-5
- `SEC-known-architectural-challenges-data-and-control-coupling-cov` Known Architectural Challenges / Data and Control Coupling Coverage (DCCC) -> REQ-8-6
- `SEC-known-architectural-challenges-graph-invalidation-cascade` Known Architectural Challenges / Graph Invalidation Cascade -> REQ-8-1
- `SEC-known-architectural-challenges-multi-unit-and-emergent-requi` Known Architectural Challenges / Multi-Unit and Emergent Requirements -> REQ-8-2
- `SEC-known-architectural-challenges-object-code-verification` Known Architectural Challenges / Object Code Verification -> REQ-8-7
- `SEC-known-architectural-challenges-vqp-size-limits-and-evidence-` Known Architectural Challenges / VQP Size Limits and Evidence Decomposition -> REQ-8-4
- `SEC-source-region-addressing` Source Region Addressing -> REQ-7-1, REQ-7-2, REQ-7-3, REQ-7-4
- `SEC-source-region-addressing-document-addressability-requirement` Source Region Addressing / Document Addressability Requirements -> REQ-7-1, REQ-7-2, REQ-7-3, REQ-7-4
- `SEC-source-region-addressing-sourceregionnode-schema` Source Region Addressing / SourceRegionNode Schema -> REQ-1-1, REQ-7-1, REQ-7-2, REQ-7-3, REQ-7-4
- `SEC-source-region-addressing-stable-region-identifiers` Source Region Addressing / Stable Region Identifiers -> REQ-7-1, REQ-7-2, REQ-7-3, REQ-7-4
- `SEC-source-region-addressing-vqp-assembly-from-sourceregionnodes` Source Region Addressing / VQP Assembly from SourceRegionNodes -> REQ-7-1, REQ-7-2, REQ-7-3, REQ-7-4

## Subsections Covered By Parent Context

- `SEC-concept-verification-compiler-artifact-graph-lifecycle` Concept: Verification Compiler / Artifact Graph Lifecycle -> parent `SEC-concept-verification-compiler` (REQ-1-2, REQ-1-3, REQ-1-4, REQ-2-1, REQ-2-2, REQ-2-3, REQ-3-1, REQ-3-2, REQ-3-3, REQ-3-3b, REQ-4-1, REQ-4-2, REQ-4-3, REQ-5-1, REQ-5-2, REQ-5-3, REQ-6-1)
- `SEC-concept-verification-compiler-physical-test-evidence` Concept: Verification Compiler / Physical Test Evidence -> parent `SEC-concept-verification-compiler` (REQ-1-2, REQ-1-3, REQ-1-4, REQ-2-1, REQ-2-2, REQ-2-3, REQ-3-1, REQ-3-2, REQ-3-3, REQ-3-3b, REQ-4-1, REQ-4-2, REQ-4-3, REQ-5-1, REQ-5-2, REQ-5-3, REQ-6-1)
- `SEC-concept-verification-compiler-scope-stage-1-trace-boundaries` Concept: Verification Compiler / Scope: Stage 1 Trace Boundaries -> parent `SEC-concept-verification-compiler` (REQ-1-2, REQ-1-3, REQ-1-4, REQ-2-1, REQ-2-2, REQ-2-3, REQ-3-1, REQ-3-2, REQ-3-3, REQ-3-3b, REQ-4-1, REQ-4-2, REQ-4-3, REQ-5-1, REQ-5-2, REQ-5-3, REQ-6-1)
- `SEC-core-concept-units-of-intelligence-llms-as-a-new-category-no` Core Concept: Units of Intelligence / LLMs as a New Category — Not DO-330 Tools -> parent `SEC-core-concept-units-of-intelligence` (REQ-3-1, REQ-3-2, REQ-3-3)
- `SEC-core-concept-units-of-intelligence-the-compound-architecture` Core Concept: Units of Intelligence / The Compound Architecture and Endpoint Replaceability -> parent `SEC-core-concept-units-of-intelligence` (REQ-3-1, REQ-3-2, REQ-3-3)
- `SEC-deployment-contexts-tier-1-development-teams-continuous-veri` Deployment Contexts / Tier 1: Development Teams — Continuous Verification Readiness -> parent `SEC-deployment-contexts` (REQ-3-3b, REQ-5-1, REQ-5-2, REQ-5-3, REQ-6-1)
- `SEC-deployment-contexts-tier-2-safety-focused-teams-structured-h` Deployment Contexts / Tier 2: Safety-Focused Teams — Structured Human Oversight -> parent `SEC-deployment-contexts` (REQ-3-3b, REQ-5-1, REQ-5-2, REQ-5-3, REQ-6-1)
- `SEC-deployment-contexts-tier-3-formal-certification-programs` Deployment Contexts / Tier 3: Formal Certification Programs -> parent `SEC-deployment-contexts` (REQ-3-3b, REQ-5-1, REQ-5-2, REQ-5-3, REQ-6-1)
- `SEC-deployment-contexts-what-changes-across-tiers` Deployment Contexts / What Changes Across Tiers -> parent `SEC-deployment-contexts` (REQ-3-3b, REQ-5-1, REQ-5-2, REQ-5-3, REQ-6-1)
- `SEC-known-architectural-challenges-human-in-the-loop-economics-a` Known Architectural Challenges / Human-in-the-Loop Economics and Scalability -> parent `SEC-known-architectural-challenges` (REQ-8-1, REQ-8-2, REQ-8-3, REQ-8-4, REQ-8-5, REQ-8-6, REQ-8-7)

## Claim / Citation Location Checks

Claims with source support but no located whitepaper section:
- `CLAIM-certification-standards-require-demonstrable-evide` Certification standards require demonstrable evidence of verification — the skep -> SRC-beningo-embedded-moats
- `CLAIM-formal-verification-can-be-applied-as-a-post-proce` Formal verification can be applied as a post-processing layer on LLM-generated c -> SRC-llm-veriguard

Source notes not used by current claim edges:
- `SRC-llm-context-window-limits` LLM Context Window Limits Source Note
- `SRC-llm-wiki-pattern` LLM Wiki Pattern
- `SRC-mintzberg-org-structure` Mintzberg — Organizational Structure and Span of Control
- `SRC-nvidia-management-structure` Nvidia Management Structure — Jensen Huang Span of Control

## Interpretation

Use this report to decide whether an unmapped section should become a requirement,
be linked to an existing requirement, or remain intentional narrative material.
