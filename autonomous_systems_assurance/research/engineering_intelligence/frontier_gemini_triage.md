# Focused Gemini challenge: capacity frontiers and mathematical limits

Run: 2026-09-28, project-approved Gemini 3.8 Flash, high thinking, Google Search grounding. Prompt and full response are retained only under ignored `out/frontier_*_20260928T070420Z.*`. Gemini's output is a source scout, not evidence. This triage used the original Yarotsky, Safran–Shamir and Raz PDFs and publisher/arXiv records; it does not reproduce the proofs.

## Accepted directions with exact scope

- [Yarotsky, *Error bounds for approximations with deep ReLU networks*](https://arxiv.org/abs/1610.01145), §4.1 Theorem 3, states a lower bound `W >= c ε^(-d/n)` for uniform approximation of the Sobolev function class `F_d,n` **when weight selection depends continuously on the target function**. It is a function-class and selection-assumption result, not a lower bound for one driving policy. Gemini incorrectly gave `ε^(-d/(2n))` for that theorem.
- [Safran and Shamir, *Depth-Width Tradeoffs*](https://proceedings.mlr.press/v70/safran17a.html), Theorems 1–2, show a unit-ball indicator that needs exponential width at depth 2 for a specified continuous distribution and error regime, while a depth-3 network can approximate it efficiently. This is a real depth/architecture counterexample to a scalar P-only law. It does not imply every latency limit forces exponential model size.
- [Raz, *Fast Learning Requires Good Memory*](https://arxiv.org/abs/1602.05161), abstract and §1, proves an `n²/25`-bit memory versus exponential-samples tradeoff for learning random parity from a stream. It concerns **training memory and samples**, not deployed inference parameter count.
- [Merrill, Sabharwal and Smith, *Saturated Transformers are Constant-Depth Threshold Circuits*](https://arxiv.org/abs/2106.16213), abstract, gives a TC⁰ upper-bound result for a formal saturated-attention transformer model with floating-point values. Its details and any specific formal-language separations remain a lead for fuller inspection. It is not a statement about all transformers or vision-control systems.
- Econometric [frontier estimation](https://arxiv.org/abs/1011.5722) may be useful for an empirical *search-process* distribution if budgets, recipes and sampling mechanisms are controlled. No such control exists in the current mixed TorchVision atlas.

## Rejected or corrected Gemini claims

1. The proposed `P × b >= rate-distortion R(D)` is not a general neural parameter lower bound. Rate-distortion applies to an information channel or code under its own source/distortion assumptions; shared trained weights and per-instance observations cannot be substituted into it without a formal reduction.
2. Gemini's arbitrary-`L²` three-way orthogonal decomposition omitted a cross term between an approximation optimizer and an arbitrary trained network. An exact **telescoping risk ledger** works for any loss by defining nested infima; this is used in the method page.
3. `max(F/Ceff, Q/Beff) <= deadline` is only a necessary lower-bound screen. It does not establish that a pipeline is schedulable, so it cannot be the exact admissibility definition by itself.
4. A free-disposal hull or maximum of observed model scores is an **attained lower bound** on an allowed achievable frontier, despite being an “upper envelope” of the observed dots. Bootstrapping observed recipes does not upper-bound the supremum over unsearched models. Extreme-value intervals require distributional and search assumptions absent here.
5. The displayed Yarotsky/manifold/compute equation was assembled by Gemini from separate ideas and is not a theorem in the cited paper. The suggested `d*` substitution and `C/depth_min` term were rejected.
6. Hoffmann et al.'s compute-optimal scaling result is an empirical model-family study, not a proof of a universal parameter/token rule. “Increasing P guarantees a superior model exists” was corrected to “the best possible score cannot decrease under an at-most-P budget”; it may stay flat.
7. Replacing evaluation labels with independent random noise changes the Bayes/observation floor; no model can generalize above chance on that task. For a clean capacity-descriptor test, use alternative **deterministic** task rules over the same inputs and hold the Bayes floor comparable. Random labels remain a useful memorization control, not a size-frontier calibration target.

## Net change to the research hypothesis

The strongest new formulation is an exact separation of `Rraw`, `Rrepr`, `Rbudget`, and `Rrelease`. The unknown model/compute gap is the limit question. Assembly-like task grammar may predict its location across task families, but it must beat task-aware MDL and pilot-only fits on held-out sizes. Genuine lower bounds require explicit function classes or computational restrictions, and their constants/scope must be checked before any engineering use.
