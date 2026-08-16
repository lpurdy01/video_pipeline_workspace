# LLM Systematic Overcorrection in Requirement Conformance Judgement (arXiv:2603.00539)

## Provenance

raw_file: refrence_literature/raw/extracted_markdown/llm_overcorrection_2603.txt
raw_url: https://arxiv.org/abs/2603.00539
summary_method: llm-from-url
summary_verified: true

## Source

arXiv:2603.00539 — "Are LLMs Reliable Code Reviewers? Systematic Overcorrection in Requirement Conformance Judgement"
Authors: Haolin Jin, Huaming Chen
Year: 2026 (cs.SE)

## Why It Matters

Primary empirical foundation for the PPV/NPV asymmetry in the VRM formula. Establishes with measured false rejection rates that LLMs over-flag correct, requirement-conformant code as failing — at rates far higher than they miss genuinely non-compliant code.

**Critical finding for the Verification Compiler design**: elaborate prompting (requesting explanations and proposed corrections) dramatically INCREASES false rejection rates. GPT-4o false rejections: 35.9% → 87.9% with full explanation-requesting prompts. This means asking LLMs to "explain their reasoning" in code review does not improve accuracy — it worsens it.

The implication: LLM verdicts must be weighted by empirically measured PPV and NPV for the specific (model, prompt version, task type) combination, not trusted at face value or improved simply by asking for more reasoning.

## Key Ideas

- **False rejection rates (correct code flagged as non-compliant)**:
  - GPT-4o on MBPP: 35.9% (direct prompt) → 87.9% (full prompt with explanation)
  - Llama-3.1-8B on MBPP: 74.7% → 91.9%
  - Claude-4.5: substantial but more moderate increases

- **Top false rejection categories**: Logic Error claims (48.2%), Hallucinated requirements (14.1%), Boundary errors (13.2%), Specification misreadings (11.7%) — models invent plausible-sounding failure scenarios

- **Explanation vs. accuracy**: Adding explanation requirements reduces false acceptances but more than doubles false rejections. For GPT-4o on MBPP: false acceptances 3.70% → 0.20%, false rejections 184 → 451 cases

- **Diagnosis weakness**: Models are good at noticing symptoms (94-100%) but weak at root cause (44-75%). They can be "right for wrong reasons."

- **Proposed mitigation (not used in VC)**: Fix-guided Verification Filter — treat model's proposed fix as a testable hypothesis, execute it. Reduces false negatives from 54.8% to 16.3% on HumanEval.

## Implications for VRM Formula

This paper directly motivates the separate PPV/NPV design:
- FPR >> FNR in LLM code review (asymmetric error modes)
- A model with high FPR has low PPV → each PASS is less trustworthy
- A model with high FNR has low NPV → each FAIL is over-flagging
- A single accuracy number conflates these two opposite failure modes
- Per-(Model_ID, Prompt_Version, Task_Type) calibration is necessary, not optional
