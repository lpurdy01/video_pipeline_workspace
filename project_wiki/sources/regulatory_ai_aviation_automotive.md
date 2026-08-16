# Regulatory AI Sources — Aviation and Automotive

## Provenance

raw_file: null
raw_url: https://www.easa.europa.eu/en/document-library/general-publications/easa-artificial-intelligence-roadmap-20
summary_method: llm-from-url
summary_verified: true

## Source

1. EASA AI Roadmap 2.0 (May 2023): https://www.easa.europa.eu/en/document-library/general-publications/easa-artificial-intelligence-roadmap-20
2. EASA AI Concept Paper Issue 2 — Guidance for Level 1 & 2 ML Applications (March 2024): https://www.easa.europa.eu/en/document-library/general-publications/easa-artificial-intelligence-concept-paper-issue-2 PDF: https://www.easa.europa.eu/en/downloads/139504/en
3. FAA Roadmap for Artificial Intelligence Safety Assurance, Version I (July 2024): https://www.faa.gov/aircraft/air_cert/step/roadmap_for_AI_safety_assurance PDF: https://www.faa.gov/media/82891
4. ISO/PAS 8800:2024 — Road Vehicles: Safety and Artificial Intelligence (December 2024): https://www.iso.org/standard/83303.html

## Why It Matters

**Relevance is limited and carefully scoped.** These sources address a different problem than the Verification Compiler: they are primarily about certifying *AI/ML systems themselves* — how do you prove that a neural network deployed in an aircraft or vehicle is safe? The "learning assurance" framework in the EASA Concept Paper is about verifying trained model weights, not about using LLMs as verification tools for conventional software.

The Verification Compiler is in a different category: it uses LLMs as reviewers of deterministic C code verification evidence. The applicable regulatory framework for the Verification Compiler is **DO-330 tool qualification** (governing software tools used in development/verification processes), not AI safety assurance frameworks for AI-based aircraft systems.

These sources may still be worth a brief mention in the whitepaper to show that regulators are actively engaging with AI in aviation — but they should not be cited as supporting the "reviewer identity" argument directly, as they do not address that question.

## Key Ideas

**EASA AI Concept Paper Issue 2 (2024):** Introduces "learning assurance" as an alternative evidence framework to development assurance (DO-178C) for AI/ML systems deployed in aircraft. Explicitly acknowledges that DO-178C cannot address AI/ML learning-based components. The Level 1/2 distinction governs AI systems that enhance or replace human decision-making in flight. *This is about certifying AI avionics, not about using AI as a verification tool.*

**FAA AI Safety Assurance Roadmap (2024):** First formal FAA position on AI safety assurance. States that "the aviation industry currently lacks a method for the safety assurance of AI." Addresses AI as a component of airborne systems. Mentions AI may be used in "artifact generation processes" but this is in the context of AI-generated software, not LLM-reviewed human-written software. *Note: AC 20-178 does not exist as a published document — do not cite it.*

**ISO/PAS 8800:2024:** Automotive standard for AI safety in road vehicles. Extends ISO 26262 tool confidence clauses to AI development tools. Governs AI as a vehicle component, not as a verification tool.

**EASA AI Roadmap 2.0 (2023):** Strategic plan for integrating AI into aviation certification via Rulemaking Task RMT.0742. Shows that AI is being treated as a subject of ongoing regulation, not yet resolved.

## Useful Claims

These sources support only a narrow, carefully scoped claim: "Aviation and automotive regulatory bodies are actively engaging with AI as a subject of safety standards, indicating that the question of AI participation in safety-critical processes is an open regulatory question rather than a settled prohibition." This is background context, not direct evidence.

Do NOT use these to argue that AI-generated verification evidence currently satisfies DO-178C, ISO 26262, or IEC 62443 objectives — these documents do not say that.

## Requirements Impact

None directly. The Verification Compiler's regulatory pathway runs through DO-330 tool qualification (TQL-5), which governs development tools. That pathway does not depend on these AI safety assurance standards.

## Follow-Up Questions

- Should these sources be removed from the whitepaper entirely, or kept as a brief "the regulatory environment is evolving" footnote?
- Is there any FAA or EASA guidance that specifically addresses AI/ML tools used *to assist* the DO-178C verification process (rather than AI/ML as the certified system)? That would be directly relevant.
- DO-330 is the right framework — has FAA published any guidance specific to AI-assisted tool qualification?
