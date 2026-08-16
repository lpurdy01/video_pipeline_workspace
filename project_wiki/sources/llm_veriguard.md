# VeriGuard — Formal Safety for LLM Agent Code Generation (arXiv:2510.05156)

## Provenance

raw_file: refrence_literature/raw/extracted_markdown/llm_veriguard_2510.txt
raw_url: https://arxiv.org/abs/2510.05156
summary_method: llm-from-url
summary_verified: true

## Source

arXiv:2510.05156 — "VeriGuard: Enhancing LLM Agent Safety via Verified Code Generation"
Authors: Lesly Miculicich, Mihir Parmar, Hamid Palangi, Krishnamurthy Dj Dvijotham, Mirko Montanari, Tomas Pfister, Long T. Le
Year: 2025 (October)
Venue: arXiv cs.SE, cs.AI, cs.CR

## Why It Matters

The previous matrix claim ("LLM-based verification achieves meaningful accuracy on bounded safety tasks") was a mismatch — that has been corrected. The corrected claim this source now supports:

> **"Formal verification can be applied as a post-processing layer on LLM-generated code outputs, enabling their use in safety-critical contexts."**

VeriGuard demonstrates exactly this: LLM code generation output is of sufficient quality to be fed into formal verifiers, compilers, and static analyzers, even though LLMs do not produce perfect code. The formal verification layer provides the safety guarantee, not the LLM alone.

This is directly relevant to the VC's architecture: the VC does not claim LLMs produce correct verification verdicts alone. It claims that structured, bounded LLM evaluation combined with human oversight and evidence tracking can contribute to a defensible verification process — the same division of responsibilities VeriGuard uses in code generation.

## Key Ideas

- **Dual-stage architecture**: offline stage synthesizes safety policies and formally verifies them; online stage monitors each LLM action against pre-verified policies before execution
- LLM code generation output is of sufficient structural quality to be parsed by formal verification tooling — LLMs are useful inputs to verification pipelines even when not perfectly correct
- Demonstrates that formal verification + LLM generation is a viable combination for safety-critical applications
