# Reinpold et al. — LLM Verification of Technical System Specifications Against Requirements (2024)

## Provenance

raw_file: null
raw_url: https://arxiv.org/abs/2411.11582
summary_method: llm-from-url
summary_verified: false

## Source

Reinpold, L. M., Schieseck, M., Wagner, L. P., Gehlhoff, F., & Fay, A. (2024).
"Exploring LLMs for Verifying Technical System Specifications Against Requirements."
arXiv:2411.11582. Submitted November 2024.
Authors affiliated with: Helmut Schmidt University Hamburg (automation technology).
Code available: github.com/lreinpold/ONCON24_Requirements_Verification_by_LLM

## Why It Matters

The most directly empirical precedent for the Verification Compiler's per-unit, per-requirement VQP design. This paper tests exactly what the VC proposes: using LLMs (GPT-4o, Claude 3.5 Sonnet) to verify technical specifications against requirements, with varying numbers of requirements packed into a single prompt.

Key finding supporting the VQP bounded-query design: F1 score degrades as requirements per prompt increases — from approximately 0.92 at 5 requirements per prompt, to 0.83 at 10, and 0.81 at 20. The paper explicitly recommends: "the number of requirements to be evaluated in a single prompt should be kept low. Instead, several prompts can be used in parallel to evaluate the same set of requirements, to boost the LLMs' performance."

This is an independent empirical confirmation of the VQP design principle: one bounded query per unit/requirement pair, not bulk review.

## Key Ideas

- LLMs can verify technical system specifications (automation/smart grid domain) against requirements at useful accuracy levels
- Accuracy degrades measurably as task complexity (requirements per prompt) increases
- The degradation is consistent across GPT-4o and Claude 3.5 Sonnet — model-agnostic finding
- Explicit recommendation to decompose into parallel bounded prompts rather than a single large context
- Context: MBSE (Model-Based Systems Engineering) and smart grid configuration — not safety-critical software, but the requirements-verification structure is the same

## Useful Claims

- "Decomposing verification into bounded, task-specific queries improves LLM accuracy compared to monolithic review" — directly supported: F1 0.92 → 0.81 degradation as requirements per prompt grows from 5 to 20
- Supports the VQP design rationale: each VQP should address one code unit against its relevant requirements, not an entire codebase in one prompt
- Does NOT cover: safety standard compliance (DO-178C, ISO 26262), DAG dependency structure, continuous integration integration — those are the VC's novel contributions

## Requirements Impact

Direct empirical support for REQ-2-1 (Context-Window Bounded Queries) and the VQP architectural choice. Cite alongside Cobleigh (assume-guarantee reasoning as formal methods lineage) to establish both the theoretical and empirical basis for query decomposition.

## Follow-Up Questions

- The domain is MBSE/smart grid — a safety-critical software domain paper would be stronger. This is the best available empirical support without one.
- Verify paper is publicly accessible at arxiv.org/abs/2411.11582 before citing in final version.
