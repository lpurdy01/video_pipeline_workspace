# LLM Task-Specific Accuracy Source Note

## Provenance

raw_file: null
raw_url: https://arxiv.org/abs/2406.01574
summary_method: llm-from-url
summary_verified: false

## Why It Matters

The verification compiler assigns confidence weights based on a model's accuracy profile for each task type — not a single global accuracy score. These sources establish that task-specific accuracy is empirically real and significant: the same model can differ by 35–50 percentage points across task categories. This makes per-task accuracy profiles a system requirement, not an optional refinement.

## Primary Sources

### MMLU-Pro: Multi-Task Language Understanding Benchmark
- **Authors:** TIGER-AI-Lab
- **Year:** 2024
- **Venue:** arXiv:2406.01574, NeurIPS 2024
- **URL:** https://arxiv.org/abs/2406.01574
- **Status:** High confidence — peer-reviewed, NeurIPS
- **Key finding:** Across 14 domains (Mathematics, Physics, Chemistry, Law, Engineering, Psychology, Health, Business, Computer Science, Economics, History, Philosophy, Biology, Other), models show 16–33% lower accuracy on MMLU-Pro vs. original MMLU depending on subject. Chain-of-thought prompting improves performance on MMLU-Pro but not on MMLU — the technique's effectiveness is itself task-specific. Direct evidence that a model cannot be assigned a single accuracy score: it must be characterized per task domain.

### SWE-bench vs. HumanEval Gap
- **Context:** Widely cited benchmark comparison data
- **Reference URLs:**
  - https://www.lxt.ai/blog/llm-benchmarks/
  - https://www.evidentlyai.com/llm-guide/llm-benchmarks
- **Status:** Secondary — blog synthesis of primary benchmark data; cite original benchmark papers if possible
- **Key finding:** The same model class achieves 90%+ on HumanEval (function completion from docstrings) but 40–55% on SWE-bench (real-world GitHub issue resolution) — a 35–50 percentage point gap between two "code tasks." This demonstrates that "good at code" is not a meaningful accuracy description; the task must be specified.

### GSM8K and Meta-Reasoning Collapse
- **Reference URL:** https://llm-stats.com/benchmarks/gsm8k
- **Status:** Secondary — use to support primary benchmark papers
- **Key finding:** Models achieving 97%+ on grade-school math word problems (GSM8K) score near 0 on meta-reasoning variants of the same problems and below 2% on error-localization tasks, even when the surface-level math is identical. "Good at math" does not generalize even within mathematics.

### LLM Bug Detection: Task-Specific Accuracy in Code Analysis
- **Title:** Can LLMs Find Bugs in Code? An Evaluation from Beginner Errors to Security Vulnerabilities in Python and C++
- **Year:** 2025
- **Venue:** arXiv:2508.16419
- **URL:** https://arxiv.org/html/2508.16419v2
- **Status:** Needs URL verification before final citation
- **Key finding:** GPT-3 achieves 87.3% on pedagogical/beginner errors but accuracy varies substantially by error type. Precision rates for specific structured bug-finding tasks differ by 13+ percentage points across error categories on the same model. Directly relevant to the verification compiler: bug detection accuracy for requirements consistency violations may differ significantly from accuracy for memory-safety checks or test coverage completeness.

## Useful Claims

- A model's accuracy on one task type does not predict its accuracy on another task type, even within the same domain (e.g., code analysis tasks can differ by 35–50 percentage points).
- Assigning a global accuracy score to a model and using it as a uniform confidence weight across all verification query types would systematically misrepresent the confidence in the results.
- Per-task accuracy profiles are therefore a system requirement for the verification compiler's confidence score, not an optional feature.

## Requirements Impact

- The model accuracy profile (see [Verification Compiler Requirements](../requirements/verification_compiler_requirements.md) Section 4.3) must be established separately for each task type the model is used for: requirements consistency checking, test coverage analysis, datasheet constraint verification, memory-safety pattern detection, etc.
- Benchmark results from general benchmarks (MMLU, HumanEval) are not acceptable as accuracy proxies for task-specific verification work. Task-specific evaluation on representative examples is required.
- The confidence score formula must weight each query by the accuracy profile for the specific task type of that query, not by a global model accuracy estimate.

## Follow-Up Questions

- What is the right benchmark suite for establishing accuracy profiles for requirements consistency verification tasks? (No standard benchmark exists for this — likely requires construction of a domain-specific eval set.)
- Should accuracy profiles be established on publicly available datasets or on held-out examples from the specific codebase being evaluated?
- How should the system handle task types for which no accuracy profile has yet been established?
