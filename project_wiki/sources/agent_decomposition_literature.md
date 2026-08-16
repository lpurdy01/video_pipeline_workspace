# Task Decomposition Literature — Bounded Query Decomposition Improves LLM Reliability

## Provenance

raw_file: null
raw_url: https://arxiv.org/abs/2210.02406
summary_method: llm-from-url
summary_verified: false

Note: Previous version of this file led with Wei et al. (2022) Chain-of-Thought (arXiv:2201.11903).
That paper shows reasoning decomposition *within* one LLM call — a different mechanism from the VC's
bounded-query decomposition across separate calls. The VC architecture is better supported by the
papers below. Wei et al. is retained as a note but is no longer the primary citation.

## Primary Sources

### Decomposed Prompting: A Modular Approach for Solving Complex Tasks
- **Authors:** Tushar Khot, Harsh Trivedi, Matthew Finlayson, Yao Fu, Kyle Richardson, Peter Clark, Ashish Sabharwal
- **Year:** 2022 (published ICLR 2023)
- **Venue:** arXiv:2210.02406
- **URL:** https://arxiv.org/abs/2210.02406
- **Status:** Confirmed publicly accessible on arXiv
- **Key finding:** Decomposes complex tasks into sub-tasks handled by **separate, independently-called** LLM prompts (not a chain within one call). Each sub-task gets its own prompt; outputs feed into subsequent prompts. Outperforms few-shot and chain-of-thought baselines on GPT-3 across symbolic reasoning, multi-hop QA, and open-domain QA. The modular structure allows each prompt to be independently optimized and replaced — directly analogous to the VQP design where each query is independently evaluable.
- **Distinction from Wei et al.:** Khot uses separate model calls per sub-task; Wei et al. uses one call with intermediate reasoning steps. The VC's VQPs are separate calls — Khot is the correct theoretical backing.

### Exploring LLMs for Verifying Technical System Specifications Against Requirements
- **Authors:** Lasse M. Reinpold, Marvin Schieseck, Lukas P. Wagner, Felix Gehlhoff, Alexander Fay
- **Year:** 2024
- **Venue:** arXiv:2411.11582
- **URL:** https://arxiv.org/abs/2411.11582
- **Status:** Confirmed publicly accessible on arXiv
- **Key finding:** Tests LLMs (GPT-4o, Claude 3.5 Sonnet) verifying technical system specifications against requirements, varying the number of requirements per prompt. F1 score: 0.92 at 5 req/prompt → 0.83 at 10 → 0.81 at 20. Explicitly recommends: "the number of requirements to be evaluated in a single prompt should be kept low. Instead, several prompts can be used in parallel." This is the most directly analogous empirical precedent to the VQP design — see also `reinpold_requirements_verification.md`.

### Note on Wei et al. (Chain-of-Thought, 2022)
- **Venue:** arXiv:2201.11903 / NeurIPS 2022
- Chain-of-thought decomposition within a single LLM call improves reasoning accuracy.
- **Relevance to VC:** LLMs may internally use chain-of-thought when processing a VQP, improving per-VQP accuracy. This is an internal behavior of the model, not the VC architecture itself. The VC's decomposition happens at the query level (separate VQPs), not within a single inference call.
- **Not cited as primary support** for the VC architecture's decomposition claim — use Khot and Reinpold for that.

## Useful Claims

- "Decomposing complex verification tasks into bounded, separately-called queries improves LLM accuracy compared to monolithic single-prompt review" — supported by Khot (general task decomposition) and Reinpold (requirements verification specifically)
- The accuracy degradation from task overloading is empirically measurable and consistent across models — Reinpold shows this directly in a requirements-verification context
- Modular, independently-callable sub-task prompts are individually optimizable and replaceable — supports the VC's VQP design where query format is versioned and prompts are configuration-controlled

## Requirements Impact

Supports REQ-2-1 (Context-Window Bounded Queries) and the VQP architectural choice. Each VQP should address one code unit against its relevant requirements — not an entire codebase in one prompt. The Reinpold F1 degradation curve gives empirical support for the bounded-query design principle.

## Follow-Up Questions

- The Reinpold paper is in MBSE/smart grid domain, not safety-critical software. A paper showing the same degradation for DO-178C-class requirements verification would be stronger.
- Gemelli et al. (2024, arXiv:2512.22306) shows F1 drops 40% on vulnerability detection as bugs per file increases — may be worth adding as a second empirical data point.
