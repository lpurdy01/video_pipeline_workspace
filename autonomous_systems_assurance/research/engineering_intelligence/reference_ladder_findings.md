# Reference-function ladder: first measurements

**Status:** a small reproducible experiment, 28 September 2026. It tests pieces of the [intelligence-budget hypothesis](intelligence_budget.md) on functions whose true form we know. It is not a scaling law for vehicles, a claim register entry, or a whitepaper change.

**Reproduce:** `out/venv/bin/python experiments/reference_ladder.py`. It uses CPU-only PyTorch 2.14 in the ignored venv. The run took 630 training runs, 519 CPU-minutes and 49 minutes wall time on the 16-core laptop.
- Summary: `experiments/reference_ladder_results.json` (SHA-256 prefix `61a7ebb659a7`).
- Raw runs: ignored `out/ladder_runs/runs.json`.
- Charts: `/ladder` on the explorer.

## Question

Every task is a function. Known functions range from a PID law (three constants) through single-body and multi-body mechanics to the same mechanics seen only through a camera. How large a network, and how many examples, does each need to reach a stated fit? And do the answers behave as the bits framing predicts?

## Design

**Functions.** Each is sampled uniformly on a box of inputs, noise-free:

| Task | Function | Inputs → outputs |
|---|---|---|
| PID | `u = 2e + 0.5∫e + 0.1ė` | 3 → 1 |
| Saturated PID | the same law, clipped to ±1 | 3 → 1 |
| Pendulum | 50 ms state change, g/l = 9.81, damping 0.1, over θ ∈ [−π, π], ω ∈ [−6, 6] | 2 → 2 |
| Pendulum with physics prior | the same function with sin θ and cos θ as inputs | 3 → 2 |
| Cart-pole | 20 ms step (Barto parameters, force as input) | 5 → 4 |
| Double pendulum | 50 ms step, unit masses and lengths, ω ∈ [−3, 3] | 4 → 4 |
| Camera pendulum | the pendulum step, observed only as two rendered 24×24 frames 50 ms apart | 1,152 → 2 |
| Flow maps | pendulum and double pendulum over 50, 100, 200, 400 and 800 ms | as above |

**Model family.** Two-hidden-layer SiLU MLP, Adam at 3e-3 with cosine decay, 4,000 steps, batch 512. Early stopping uses an independent 2,048-sample validation set; testing uses a fixed 4,096-sample set.

**Fit metric.** Test NRMSE: RMS error ÷ target standard deviation, averaged over outputs. Thresholds are 10%, 3%, 1% and 0.3%.

**Capacity sweep.** Widths 2–256 (17 to about 70k parameters; up to 296k for the camera task), 32,768 training examples, 3 seeds. The minimum size is the smallest size at which the best seed at or below it passes, log-interpolated between widths. This is the at-most-P frontier from [the cross-domain note](cross_domain_findings.md).

**Data sweep.** Width 128, 128 to 32,768 training examples, 2 seeds.

**Bits.** The best network at the smallest width reaching 1% is quantized uniformly, per tensor, to 16…2 bits. We keep the fewest bits that still hold `max(1%, 1.25 × float error)`.

**Chaos.** Finite-time Lyapunov exponents over 0.8 s from 256 random states in each box: pendulum median 0.88/s, 90th percentile 2.4/s; double pendulum median 1.75/s, 90th percentile 3.7/s. The pendulum's positive value is shear near the separatrix, not chaos.

## Results

| Function | Constants in the law | Params for 10% / 3% / 1% / 0.3% | Bits kept per weight | Bits for 1% (P × bits) | Examples for 1% |
|---|---:|---|---:|---:|---:|
| PID | 3 | ≤17 / ≤17 / ≤17 / 77 | 8 | ≈136 | ≤128 |
| Saturated PID | 4 | ≤17 / 1.8k / 15.2k / — | 8 | ≈122k | 457 |
| Pendulum | 3 | 23 / 60 / 140 / 1.0k | 10 | ≈1.4k | ≤128 |
| Pendulum, sin/cos inputs | 3 | 20 / 34 / 81 / 276 | 8 | ≈650 | ≤128 |
| Cart-pole | 4 | 78 / 369 / 7.5k / — | 10 | ≈75k | 950 |
| Double pendulum | 3 | 752 / 14.9k / — / — | 10 | — (3%: ≈149k) | — |
| Camera pendulum | 3 | 2.8k / 4.1k / 8.1k / 35.7k | 10 | ≈81k | 637 |

"—" means not reached within about 70k parameters (296k for the camera). "≤" means passed at the smallest size tried.

**Chaos horizon.** Parameters needed for 10% error:

| Horizon | 50 ms | 100 ms | 200 ms | 400 ms | 800 ms |
|---|---:|---:|---:|---:|---:|
| Pendulum | 23 | 24 | 24 | 33 | 83 |
| Double pendulum | 752 | 883 | 1.4k | 13.5k | >70k |

At a fixed 70k parameters, the double pendulum's best error went 1.8% → 2.3% → 3.3% → 7.1% → 19.8% over those horizons. The pendulum's went 0.10% → 0.56%.

## Findings

Each finding is labelled as the hypothesis note does.

1. **The ladder exists and is steep [E, this experiment].** The bits the network needed for 1% run from ≈136 (PID, near the formula's 96 bits of constants) through ≈1.4k (pendulum) and ≈75k (cart-pole) to more than 149k for 3% on the double pendulum. From the formula to learned multibody dynamics is two to three orders of magnitude.
2. **Regularity is as important as complexity [E; interpreted as ρ_A, H].** Adding a clip to the PID law adds one constant but multiplies the parameters needed for 1% by about 900×: a smooth-activation network struggles to draw a kink. A ReLU network, whose prior matches piecewise-linear functions, would likely need little. That is a concrete, measured architecture mismatch.
3. **A physics prior pays [E].** sin/cos inputs cut the parameters needed about 1.7× at 1% and about 3.8× at 0.3%.
4. **Observing through a camera costs [E].** The same function needed about 58× the parameters at 1% and at least 5× the examples. For an MLP, most of the parameter cost is the pixel input layer. A convolutional network would share weights and pay less, but it would still have to learn to decode the image.
5. **Chaos multiplies model size with horizon [E + H].** From 50 to 400 ms the double pendulum's requirement grows about 18×, about e^(8.2 t). The argument predicts growth near `d·λ ≈ 4 × 1.75 ≈ 7/s`: the flow map's Lipschitz constant grows like e^(λt), and network size for Lipschitz functions scales as (L/ε)^(d/s) with s = 1. At fixed size, error grows at about e^(3.2 t), inside the measured Lyapunov range. The regular pendulum stays under 100 parameters at 10%.
   - Two horizon intervals are a demonstration, not a fitted exponent.
   - The argument is a standard approximation-theory step suggested by the Gemini scout. It is not a result claimed by the forecasting papers it pointed to: [Pathak et al. 2018](https://link.aps.org/accepted/10.1103/PhysRevLett.120.024102) and [Gilpin 2021](https://arxiv.org/abs/2110.05266); Gilpin correlates forecast performance with degree of chaos across 131 systems.
   - Engineering reading: feedback control needs only the short-horizon map, which is why a controller can stay small when a forecaster cannot.
6. **Data tracks the task; parameters track the task × mismatch [E + H].** Where the architecture fits (smooth state inputs, and not floored at 128 examples), the labels needed carry `examples × outputs × log₂(1/ε)` bits. That comes to 0.3–1.4× the bits the network needed; equivalently, the network's bits ÷ label bits = 0.7–3.6 (one outlier: 20, pendulum at 400 ms and 0.3%). Where it fits badly, weights need far more bits than labels: about 10–16× for the camera and 19–40× for the clipped PID. Two consequences:
   - The ratio is a way to *measure* ρ_A.
   - It is the first calibration of the calculator's data line: with `s_eff = outputs × log₂(1/ε)`, retention `η` ≈ 0.3–1.4 for well-matched, noise-free tasks.
7. **More data cannot buy what the model cannot hold [E].** In the data sweep, curves flatten where width 128 becomes the limit (cart-pole ≈0.8%, double pendulum ≈2.7%). This is the `min{storage, teaching}` structure of the condensed law, seen directly.

## Limits

- One architecture and one recipe; 4,000 steps; best of three seeds. Each minimum is attained, not proven.
- Uniform noise-free boxes. Real sensors add noise and an observation floor that these tasks do not have.
- The smallest data set tried (128) floors the easy tasks.
- The quantizer is crude uniform per-tensor. Per-channel or learned quantization would lower bits per weight; the absolute bit counts are upper estimates.
- "Not reached" is not "impossible".
- The camera renderer is idealized: a Gaussian bob with no background, lighting change or occlusion.

## Next experiments (same budget scale)

1. **ReLU and convolutional variants** of the saturated-PID and camera tasks, to measure how much of ρ_A an architecture change removes.
2. **Noise and occlusion** in the camera renderer, to show an observation floor (Π_obs) appear.
3. **Finer horizon steps** (25 ms) and a third system (Lorenz), to fit the growth rate against the Lyapunov exponent rather than read it from two intervals.
4. **Smaller data sizes (16–128)** to unfloor the easy tasks, and a noisy-label variant, to test retention η under noise.
5. **Morris-style capacity measurement** on the same MLPs with random targets, to measure κ for these networks directly. This is the "next step" from the previous round.

## Video demonstration idea

**"Every task is a function."** A single animated sweep:
- a network slider grows while a fitted surface converges on the PID plane;
- then the pendulum's curved map;
- then the double pendulum, which never quite settles;
- then the same pendulum rebuilt from camera frames.

Beside it, a bits counter shows how many bits the network needed; a second counter shows how many examples.

Then the chaos beat: stretch the horizon on the double pendulum and watch the needed network grow by 18× in a third of a second, while the ordinary pendulum barely moves. Close on the engineering point: a controller that looks again every 50 ms only has to learn the short map.

All values come from this reproducible run, so the scene can be regenerated deterministically for Manim.
