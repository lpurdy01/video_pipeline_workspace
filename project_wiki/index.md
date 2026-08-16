# Project Wiki Index

## Schema

- [PROJECT_WIKI_SCHEMA.md](PROJECT_WIKI_SCHEMA.md): rules for maintaining this project wiki.

## Source Notes

- [LLM Wiki Pattern](sources/llm_wiki_pattern.md): Karpathy-inspired pattern for maintaining a persistent LLM-written knowledge base instead of repeatedly querying raw sources.
- [Rierson DO-178C](sources/rierson_do178c.md): selective notes from Rierson on verification, traceability, review, and tool qualification.
- [FAA AC 20-115D](sources/faa_ac_20_115d.md): public FAA guidance recognizing DO-178C, DO-330, and related supplements.
- [NASA Jacklin DO-178C and DO-278A](sources/nasa_jacklin_do178c_do278a.md): NASA public overview of DO-178C/DO-278A and companion documents.
- [NASA-STD-8739.8B](sources/nasa_std_8739_8b.md): NASA software assurance and software safety requirements.
- [NPR 7150.2D](sources/npr_7150_2d.md): NASA software engineering requirements.
- [AS9100 Public References](sources/as9100_public_references.md): public IAQG, SAE, and NASA references for AS9100/9100 without licensed text.
- [Beningo: Embedded Moats](sources/beningo_embedded_moats.md): practitioner counterargument — 3 structural moats (physics, certification, domain expertise) that AI won't dissolve; project response included.
- [LLM Context Window Limits](sources/llm_context_window_limits.md): empirical sources for context-length degradation — "Lost in the Middle" (Liu et al. 2023) and "Context Length Alone Hurts" (Amazon 2025); justifies bounded query design.
- [LLM Task-Specific Accuracy](sources/llm_task_specific_accuracy.md): MMLU-Pro, SWE-bench/HumanEval gap, bug detection benchmarks; justifies per-task accuracy profiles in the confidence score.
- [Agent Decomposition Literature](sources/agent_decomposition_literature.md): Chain-of-Thought (Wei et al. 2022), multi-agent frameworks, VeriGuard and formal verification papers; justifies hierarchical decomposition as reliability improvement.
- [Amodei: Model Adaptability](sources/amodei_adaptability.md): Dwarkesh Patel interview (2025) — pre-training as evolution framing, in-context adaptability, cited citation target from human-written notes.
- [ISO 26262 Public References](sources/iso_26262_public_references.md): NHTSA/Volpe government assessments as public proxy for the licensed automotive functional safety standard; ASIL levels, evidence structure, DO-178C comparison.
- [IEC 62443 Public References](sources/iec_62443_public_references.md): CISA and NIST public documents as proxy for the licensed ICS cybersecurity standard series; FR1–FR7, security levels SL1–SL4, verification evidence types.
- [Requirements Engineering — NL Ambiguity](sources/requirements_engineering_nl_ambiguity.md): Zave & Jackson (1997) TOSEM and Davis (1993) — canonical sources for NL spec ambiguity, implicit assumptions, and implementation drift; supports "English as Specification Medium" section.
- [Mintzberg Org Structure](sources/mintzberg_org_structure.md): Mintzberg (1979) *The Structuring of Organizations* — span of control and organizational configuration types; Machine Bureaucracy (narrow span, verification-heavy) vs. Adhocracy (wide span, innovative); supports "Agentic Structuring Hypothesis" section.
- [Nvidia Management Structure](sources/nvidia_management_structure.md): Fortune (Nov 2024) — Jensen Huang's ~60 direct reports, deliberately flat org; case study for wide-span innovation-oriented organization; supports Nvidia analogy in whitepaper.
- [Regulatory AI — Aviation and Automotive](sources/regulatory_ai_aviation_automotive.md): EASA AI Roadmap 2.0 (2023), EASA AI Concept Paper Issue 2 (2024), FAA AI Safety Assurance Roadmap v1 (2024), ISO/PAS 8800:2024 — all show regulators actively constructing (not foreclosing) AI participation in certification; EASA Concept Paper is strongest: introduces "learning assurance" as parallel to DO-178C verification assurance.

## Concepts

- [Safety-Critical Traceability](concepts/safety_critical_traceability.md): traceability as maintained, reviewable relationships among requirements, implementation, verification, and evidence.
- [Verification as Evidence Production](concepts/verification_as_evidence_production.md): verification as review, analysis, and test activities that produce auditable evidence.
- [Model or Tool Qualification](concepts/model_or_tool_qualification.md): qualification-inspired framing for model/tool units used in verification workflows.
- [Quality Management as Coordination Pattern](concepts/quality_management_as_coordination_pattern.md): AS9100-style quality management as an organizational coordination analogue.

- [Units of Intelligence](concepts/units_of_intelligence.md): capacity, accuracy, adaptability, specialization, reviewability, and qualification as properties of humans and model agents; how the verification compiler is designed around these properties.
- [Verification Compiler](concepts/verification_compiler.md): hierarchical artifact graph, graph traversal as decomposition, context window as design primitive, dual-mode LLM/human operation, confidence score, and provable decomposition.
- [Agentic Structuring](concepts/agentic_structuring.md): organizing units of intelligence into hierarchies and review loops; organization shape as a design variable; relationship to the verification compiler.

Pending pages:

- natural-language specifications

## Claims

- [Safety-Critical Verification Depends on Traceability](claims/safety_critical_verification_depends_on_traceability.md): claim page with Rierson evidence for traceability as an assurance requirement.
- [Verification Requires Review, Analysis, and Test](claims/verification_requires_review_analysis_and_test.md): claim page with Rierson evidence for verification as broader than test execution.
- [Model Units Need Task-Specific Qualification](claims/model_units_need_task_specific_qualification.md): speculative project claim using DO-330 as analogy support.
- [Aerospace Quality Management Standardizes Coordination](claims/aerospace_quality_management_standardizes_coordination.md): claim page using public AS9100/9100 references for quality-management coordination.

Pending pages:

- agent decomposition improves bounded work
- persistent source synthesis is better than repeated raw retrieval for this project

## Requirements

- [Traceability Link Requirements](requirements/traceability_link_requirements.md): requirement for stable, reviewable link records beyond Graphify's candidate edges.
- [Evidence and Auditability Requirements](requirements/evidence_and_auditability_requirements.md): requirement for verification outputs to become auditable evidence records.

- [Verification Compiler Requirements](requirements/verification_compiler_requirements.md): full Stage 1 system requirements — artifact graph schema, decomposition, reviewer interface, confidence score, auditability, and Stage 2 non-goals.

Pending pages:

- source ingest requirements

## Traceability

- [Link Registry](traceability/link_registry.md): promoted candidate links with stable IDs, status, evidence, and rationale.
- [Source to Claim Matrix](traceability/source_to_claim_matrix.md): compact matrix mapping sources to claims and evidence locations.

## Workflows

- [Graphify Workflow](graphify_workflow.md): process for using Graphify as a candidate relationship engine while maintaining verified links in the project wiki.
- [Verification Compiler Video Production Plan](video_production_plan.md): staged plan for adapting the representation-transform Manim video workflow to a second video about the verification compiler.
- [Verification Compiler Video Outline - First Pass](video_outline_first_pass.md): creative 10-minute outline, hook menu, visual motifs, and short-form concepts for the Verification Compiler video.
- [Verification Compiler Video Workspace](../verification_compiler_video/README.md): script, storyboard, manifest, narration-review workflow, and Manim prototypes for the short Verification Compiler explainer.
