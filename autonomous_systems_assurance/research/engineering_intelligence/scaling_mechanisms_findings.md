# MIT scaling-mechanism papers: the diminishing-returns law, flipped

**Status:** source review and our own arithmetic, 1 October 2026. It bears on the [intelligence-budget hypothesis](intelligence_budget.md). It is not a claim register entry or a whitepaper change. Labels follow that note: [T] theorem, [E] empirical, [H] our hypothesis.

**Trigger:** a UN University blog post, [*Why AI Scaling Hits a Wall*](https://c3.unu.edu/blog/why-ai-scaling-hits-a-wall) (Ng Chong, 20 September 2026), which cites "foundational theoretical work from MIT".

## What the "MIT paper" is

It is three papers from Jeff Gore's group (first author Yizhou Liu). All three were read in the original PDF; snapshots and hashes are in [source_leads.md](source_leads.md) (EI-62 to EI-65).

| Axis | Paper | Result | Mechanism |
|---|---|---|---|
| Width `m` | Liu, Liu & Gore, *Superposition Yields Robust Neural Scaling*, NeurIPS 2025 ([arXiv:2505.10465](https://arxiv.org/abs/2505.10465)) | Loss ∝ `1/m`. Measured on four open model families: exponent 0.91 ± 0.04 (Fig. 6b). | Models hold more features than dimensions. Overlap between feature vectors is unavoidable and its square scales as `1/m`. |
| Depth `ℓ` | Liu, Kangaslahti, Liu & Gore, *Inverse Depth Scaling From Most Layers Being Similar*, ICML 2026 ([arXiv:2602.05970](https://arxiv.org/abs/2602.05970)) | Loss ∝ `1/ℓ`. Fitted on about 200 Chinchilla points: 1.2 ± 0.3 (§2). | Most layers make small, mutually uncorrelated updates. They average out error like repeated noisy measurements, instead of composing. |
| Training time `τ` | Liu, Liu, Pehlevan & Gore, *Universal One-third Time Scaling in Learning Peaked Distributions*, ICML 2026 ([arXiv:2602.03685](https://arxiv.org/abs/2602.03685)) | Loss ∝ `τ^(−1/3)`. Seen in Pythia and OLMo checkpoints, and in an MNIST classifier (0.35). | Softmax with cross-entropy has vanishing gradients when the target distribution is sharply peaked. The exponent does not depend on data structure. |

The depth paper combines them (its Eq. 3), with `L₀` the irreducible entropy of the data:

```
L − L₀  ≈  c_m / m  +  c_ℓ / ℓ  +  c_D / D^0.30
```

With parameter count `N ∝ m²ℓ`, the best split has `m ∝ ℓ`, and both size terms fall as `N^(−1/3)`. That is the paper's explanation of the Chinchilla size exponent of 0.34 (§6).

## Where the blog overstates

- **"Wall" and "proves".** The papers describe power laws that decay towards a floor, argued from toy models and fits. Their own words are "may", "likely" and "not derived from first principles" (depth paper §6). Each paper ends with ways to improve the exponent or the constant.
- **"Anchored to Zipf's law".** The width paper says the opposite for large language models: under strong superposition the `1/m` law comes from geometry and holds "across a broad class of frequency distributions". Strongly skewed frequencies would make the decay *faster*, exponent `2(α−1)` (Result 2, §5 box).
- **Cost figures.** "Doubling width inflates training cost four to six times", the dollar amounts and "cubic memory-bandwidth effects" do not appear in the width paper. What it reports is `N ∝ m^2.52` for the Chinchilla models (§3.3).
- **References.** We found no trace of references 8 (Thrun, *AI Magazine* 2024) and 9 (LeCun & Bastien, *Trends in Cognitive Sciences* 2024) outside the blog itself. The Hoffmann arXiv number is wrong (it is 2203.15556).

Treat the blog as a pointer, not a source.

## The flip: size needed for a tolerance

A scaling law `ε(N)` and a requirement law `N(ε)` are the same curve read on the other axis, so the inversion is legitimate. Write `ε = L − L₀` for the excess loss allowed, and split it across the terms. [H: our arithmetic on their Eq. 3, with exponents rounded to 1, 1 and 1/3.]

- **Width:** `m ≥ c_m / ε_m`.
- **Depth:** `ℓ ≥ c_ℓ / ε_ℓ`.
- **Training:** `τ ≥ (c_τ / ε_τ)³`.
- **Smallest model** with `N = k·m²ℓ`: give two-thirds of the size budget to width and one-third to depth. Then

```
N_req  =  (27/4) · k · c_m² · c_ℓ / ε³
```

- **Training compute** ∝ `N·τ` ∝ `ε^(−6)`.

So for language transformers, halving the excess loss costs 8× the parameters, 8× the training, and 64× the training compute. A tenfold cut costs 1,000× the parameters.

This is the form our note already uses: `K(ε) ≈ K₀ (ε/ε₀)^(−1/α)`. The MIT papers supply a mechanistic value, `α = 1/3`, for one family. Our note assumed α ≈ 0.3 from the Chinchilla fit.

## What it does not give: size for a *complexity*

The flipped law is size against tolerance, for one task. The task's complexity sits in the constants `c_m`, `c_ℓ`, `c_τ` and in which regime applies, and the papers do not say how the constants move with the task. They do identify three task properties that change the exponent. That is the useful part for us.

| Task property | Effect on the requirement | Source |
|---|---|---|
| **How many features, and how skewed** | With no superposition, width must equal the feature count `F`: `m = F`. With strong superposition, about `m²/2` features are held cleanly, so `m ≈ √(2F)`, and the remaining error is crosstalk ∝ `1/m`. The law ends when `m` reaches the true feature count. | Width paper, Results 1–2, App. A.1, Fig. 16 [E, toy model] |
| **Whether the target is a smooth dynamical system** | Smooth target, fully trained: loss ∝ `ℓ^(−3)`, so `ℓ_req ∝ ε^(−1/3)`. Non-smooth target: loss ∝ `ℓ^(−1)`. | Depth paper §4, Figs. 3–4 [E, toy model] |
| **How peaked the output distribution is** | Peaked targets under softmax: `τ^(−1/3)`. Flat targets converge roughly exponentially. | Time paper §3, Fig. 1 [E + T under its ansatz] |

**A consistency worth noting [H].** A layer of width `m` has about `m²` weights and holds about `m²/2` features cleanly. Capacity therefore tracks parameter count, not width, which is what a constant bits-per-parameter κ assumes.

## Check against our ladder

We refitted the existing ladder runs as `MSE ∝ P^(−a)` on the at-most-P frontier (`experiments/analyze_ladder.py`; no new training). [E, this experiment; 3–7 frontier points per task, one recipe.]

| Function | Size exponent `a` | Parameters × per halving of loss |
|---|---:|---:|
| Pendulum, 50 ms | 1.54 ± 0.21 | 1.6× |
| Pendulum, sin/cos inputs | 1.33 ± 0.18 | 1.7× |
| Cart-pole | 1.06 ± 0.13 | 1.9× |
| Double pendulum, 50 ms | 0.88 ± 0.05 | 2.2× |
| Double pendulum, 400 ms | 0.55 ± 0.01 (3 points) | 3.5× |
| Clipped PID | 0.25 ± 0.07 | 16× |
| *Language transformers (MIT)* | *0.33* | *8×* |

Not comparable, so left out: the plain PID (the smallest network already passes, so the fit is on the training floor) and the camera pendulum (2.42 ± 0.44, dominated by the fixed pixel-input layer).

Reading:
- **The exponent is a task property.** It falls as the function gets rougher or more chaotic, and it falls with prediction horizon. The cube law is one row of a table, not a constant of nature.
- **Smooth low-dimensional physics is cheap.** Each halving of loss costs under 2× the parameters for the pendulum and cart-pole, against 8× for language.
- **A kink is worse than language.** The clip sits at 16× per halving for this smooth-activation network.

So the answer to "size needed for a given complexity" has two numbers per task and architecture: a scale `K₀` and an exponent `α`. Complexity moves both.

## What changes in our hypothesis

1. **The mechanism in §2 is not the one MIT finds for language models.** Our truncated-Zipf curve assumes skills are either stored or missing (the paper's "weak superposition"). Under the paper's mapping of tokens to features, Zipf frequencies (α = 1) give that picture an exponent of zero. The MIT account is that every feature is stored and the error is crosstalk. The functional form survives; the story behind it differs by regime.
2. **The open exponent test in §5 has a third candidate.** Given a size exponent of 1/3, Michaud's relation predicts a data exponent of 0.25. The MIT account predicts 1/3 for both, for unrelated reasons (geometry for size, softmax dynamics for time). Published fits are 0.285 (Hoffmann), 0.366 (Epoch refit) and 0.30 ± 0.01 (MIT refit). The two exponents may simply not be linked through the skill spectrum.
3. **Retention η is not a constant for softmax systems.** Our data-required output is an information bound. The time paper says a softmax classifier needs 8× the training per halving regardless of how much information the data carries. A third term belongs in `D_req`: `(c_τ/ε)³` for outputs trained with softmax and cross-entropy on peaked targets. Our ladder tasks are regression with squared error, so the measured η ≈ 0.3–1.4 does not transfer to tokenized outputs.
4. **Hardware lines buy different loss terms.** Width costs memory and bandwidth (∝ `m²`). Depth costs latency, since layers run in series. Under `1/ℓ` scaling, a fixed deadline sets a depth-limited floor `c_ℓ / ℓ_max`, and halving the deadline doubles it. Our min-of-budgets law is the max-term approximation of their additive law; with three terms, the two agree within a factor of 3.
5. **Assurance reading [H].** In the toy model, a width shortfall leaves frequent features well separated and squeezes rare ones together, where they overlap each other. If that carries over, a too-narrow model fails by confusing rare cases with one another, not only by missing them. The width paper also notes that superposition makes interpretation harder (§5).

## Limits

- All three results are for language-model pre-training loss, supported by toy models. None has been tested on vision or control.
- The fitted constants `c_m`, `c_ℓ`, `c_D` are not printed in the papers, so the flipped law gives ratios, not absolute sizes.
- The depth fit rests on about 200 points reconstructed from one model family.
- Our exponent refit uses few points per task and one training recipe.

## Proposed experiment

**Depth sweep on the flow maps.** Fit residual networks of fixed width and varying depth to the pendulum and double-pendulum flow maps. Physical flow maps are smooth dynamical systems, so the depth paper's toy result predicts loss ∝ `ℓ^(−3)` once trained, against `ℓ^(−1)` for a non-smooth target. If it holds, depth should absorb the prediction horizon roughly linearly, where our shallow networks needed about 18× the parameters from 50 to 400 ms. That would also test the claim that a physics-like task can use depth far more efficiently than language does. Same laptop budget as the ladder.
