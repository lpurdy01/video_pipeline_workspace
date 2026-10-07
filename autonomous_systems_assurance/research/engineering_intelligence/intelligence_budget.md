# The intelligence budget: one currency, one task curve, five numbers

**Status:** hypothesis synthesis, 28 September 2026. This builds on the [research draft](draft.md), the [assembly hypothesis](assembly_hypothesis.md) and the [cross-domain findings](cross_domain_findings.md). It does not replace their boundaries. Every statement below is labelled as one of:
- **[T] theorem:** true under the stated assumptions.
- **[E] empirical:** a measured or fitted result from a cited study.
- **[H] our hypothesis:** an extrapolation to be tested.

It changes nothing in the whitepaper or the project's claim register. The Gemini runs and corrections are in [budget_gemini_triage.md](budget_gemini_triage.md). The ladder data are in `interactive/src/data/budget_ladder.json`, each row with a verification status.

## 1. The lateral move

The earlier explorer used about fifteen inputs:
- pixels, frames, patch size, context and task factors;
- composition depth, motif reuse, novelty, novel and tail examples;
- model size, precision, memory, compute, bandwidth and deadline.

They look like different kinds of thing. **They are all supplies of, or demands for, information.** Measure each in bits and the problem becomes a budget, like an RF link budget:

| Ledger | Supplies or demands | Unit |
|---|---|---|
| Observation | Task-relevant information the sensor and tokenizer preserve | bits about the correct action |
| Description | Information needed to specify a policy good enough for error ε in the operating domain | bits of task description, `K(ε)` |
| Storage | Information a model can hold | `κ` bits/parameter × `P` parameters |
| Teaching | Task information the training data delivers | supervision bits per example × useful examples |
| Time | Parameters the hardware can exercise before the deadline | `P_max(hardware, deadline, tokens)` |
| Evidence | Information needed to show a rare-failure target was met | `log(1/a)` nats against the failure hypothesis |

An RF engineer asks whether transmit power, antenna gain and path loss leave enough margin over the signal-to-noise ratio a code needs. We ask whether sensing, model storage, hardware time and training data leave enough margin over the bits the task needs. Everything multiplies, so a **margin in decibels** is natural, and relative vendor figures plug in directly. For example, "AI5 has 10× AI4 compute" is simply +10 dB on the compute line, even with no absolute baseline.

## 2. The task is one curve: `K(ε)`

**Definition [H].** For an architecture family `A` and an operating-domain distribution, `K_A(ε)` is the minimum number of bits needed to specify a member of `A` that reaches error `ε`. It is the task's rate–distortion curve, written in the family's own "language".

**Theorem anchor [T].** For function classes, this idea is already a theorem. Elbrächter, Perekrestenko, Grohs and Bölcskei define:
- the **minimax code length** `L(ε, C)`: the fewest bits any encoder–decoder needs to reach uniform error ε over a class `C`;
- its **optimal exponent** `γ*(C)`.

Their **Theorem VI.4** proves that deep networks with polylogarithmic depth and polynomially bounded weights cannot approximate the class faster, in number of weights, than that exponent allows. *No network beats the class's description length* ([arXiv:1901.02220](https://arxiv.org/abs/1901.02220), Def. IV.1, Thm VI.4). Classical metric entropy gives `L(ε) ~ ε^(−d/s)` for smooth classes. That is the same form as [Yarotsky's](https://arxiv.org/abs/1610.01145) weight lower bound and [Sharma–Kaplan's](https://arxiv.org/abs/2004.10802) manifold exponent.

**Our step [H].** Replace a worst-case function class by the average case over a task distribution, and treat the result as a property of the task that can be measured.

**Empirical proxies [E].** Li et al. count how many random-subspace degrees of freedom reach 90% of full performance ([arXiv:1804.08838](https://arxiv.org/abs/1804.08838), Table 1). Multiplied by bits per degree of freedom, these give an upper estimate of `K_A`:

| Task | Architecture | `d_int90` |
|---|---|---:|
| Inverted pendulum | FC | **4** (same count as the gain vector of a 4-state LQR controller) |
| MNIST | LeNet / FC | 290 / 750 |
| Humanoid locomotion | FC | 700 |
| CIFAR-10 (>50% accuracy) | ResNet / LeNet / FC | ≈1k / 2.9k / 9k |
| Atari Pong | ConvNet | 6,000 |
| ImageNet | SqueezeNet | >500,000 |
| MNIST with **shuffled labels** (training fit) | FC | **190,000** |

That last row is the empirical form of the counterexample the assembly note posed. The images are identical and the label rule is random, and the description need grows about 250×. Raw-pixel complexity is not the task's complexity; `K` is.

**Architecture enters as a mismatch factor [H, with E support].** Write `K_A(ε) ≈ ρ_A · K*(ε)`, with `ρ_A ≥ 1`.
- On CIFAR-10, `ρ_FC/ρ_ResNet ≈ 9`.
- On MNIST with shuffled pixel positions, the CNN's `d_int90` rises from 290 to 1,400, while the permutation-blind FC network stays at 750.

A mismatched prior costs bits, and a matched prior saves them. This is where inductive bias, and the choice of tokenizer, enters.

**Where assembly theory belongs [H].** An additive sum of skills overcounts. Once skill A exists, skill B may cost only `c_B|A ≪ c_B`. So `K` should be the **assembled** size of the skill set with reuse, `K(S) ≤ Σ c_k`. That is exactly assembly theory's shortest construction with reuse. The ratio `Σ c_k / K(S)` is the task's reuse factor.

**Condensed parameterization [H].** Four task numbers replace about eight earlier ones:
- `ε_obs`, the observation floor;
- `K₀`, the bits needed at a reference error `ε₀`;
- `α`, the tail exponent, where `K(ε) ≈ K₀ (ε/ε₀)^(−1/α)`;
- `K_ODD`, the cap at which the operating-domain spectrum is exhausted.

## 3. A model stores about 1–4 bits per parameter

This is the most important new grounding, because it turns "bits the task needs" into "parameters required".

| Result | Value | Status |
|---|---|---|
| Allen-Zhu & Li, knowledge capacity ([arXiv:2404.05405](https://arxiv.org/abs/2404.05405), §1, Results 1, 4 and 8) | **2 bits/param** after ~1,000 exposures per fact; 1 bit/param at 100 exposures; int8 keeps 2; int4 falls to 0.7 | [E] |
| Morris et al., memorization capacity ([arXiv:2505.24832](https://arxiv.org/abs/2505.24832)) | **3.5–3.6 bits/param** in bf16; fp32 raises it only to 3.83 | [E] |
| Classical perceptron capacity (Cover 1965; Gardner 1988; as cited by Morris et al.) | 2 patterns per weight | [T] |
| BitNet b1.58 ([arXiv:2402.17764](https://arxiv.org/abs/2402.17764), p. 3) | Ternary weights (≤1.58 bits each) match FP16 LLaMA perplexity from 3B parameters | [E] |
| Deep Compression ([arXiv:1510.00149](https://arxiv.org/abs/1510.00149)) | AlexNet 240 → 6.9 MB with no accuracy loss, about 0.9 stored bits/param | [E] |

**Reading [H].** The counting ceiling is `κ ≤ b_eff`, where `b_eff` is the lowest precision at which the model still works: about 1.6–4 bits today. The measured storage rate is about 1–3.6 bits per parameter. **Trained networks already store close to the counting limit per parameter.**

The large inefficiencies are not in bits per weight. They are in:
- how many bits the chosen architecture needs for the task (`ρ_A`);
- how rarely the tail is seen, since rare knowledge is stored at about half the rate.

Gemini's challenge was right that `κ = 32` or `κ = 16` is not a meaningful ceiling. Precision above the working knee is not used. Its further claim, that generalizing programs escape the bound, confuses *output* bits with *description* bits. `K` counts the description of the generator, and the counting bound applies to it.

So, to first order:

```
P_min(ε) ≈ ρ_A · K*(ε) / κ,     κ ≈ 2 bits/param (1 for rarely seen knowledge)
```

## 4. Hardware sets `P_max` for a deadline

For a dense transformer at batch size 1 [T, as arithmetic for the stated workload model]:

| Resource | Constraint |
|---|---|
| Memory | `P·b/8 + M_KV + M_act ≤ M` |
| Compute | `2·P·T ≤ C_eff·L`, where `T` is tokens processed per decision |
| Bandwidth | `(1+Z)·P·b/8 ≤ B_eff·L`: weights are re-read for each of `Z` decode steps |
| Serial depth | `(1+Z)·n_layers·τ_layer ≤ L` |

The roofline estimate is optimistic when compute and memory transfer overlap perfectly (`max(compute time, memory time)`) and pessimistic when they don't overlap at all (`compute time + memory time`). Show both.

**Tokenization is the exchange rate [H].** For a camera, `T = streams × frames × (W/u)(H/u)`, where `u` is the patch size.
- In the compute-bound regime, `P_max ∝ u²`: coarser patches free parameters.
- But pixels on a distant target fall as `1/u`, which raises the observation floor.

So there is an optimal `u*`, and the explorer shows it. Real CNN and pyramid backbones do not obey `2·P·T` exactly, but the direction of the trade holds.

**Serial depth is a separate resource [E].** Merrill & Sabharwal show that transformers answering immediately cannot solve some simple sequential problems, such as graph connectivity. A linear number of chain-of-thought steps adds real power ([arXiv:2310.07923](https://arxiv.org/abs/2310.07923)). Snell et al. find that, FLOPs-matched, test-time compute can outperform a 14× larger model on problems the base model partly solves ([arXiv:2408.03314](https://arxiv.org/abs/2408.03314)).

`Z` output steps buy logical depth, and the deadline caps `Z`. This is the precise sense in which a 36 Hz control loop needs "fast path" skills, as in the Tesla talks' fast and reflective modes.

## 5. Data delivers bits; supervision bandwidth decides how fast

**Teaching condition [H].** Two conditions must both hold:

```
η · s_eff · D ≥ ρ_A K(ε)        and        D · p_k* ≥ τ   (for the rarest needed skill k*)
```

- `s_eff` is the task-relevant supervision bits per example.
- `η` is the learning efficiency.
- `τ` is roughly 100–1,000 exposures per item [E: Allen-Zhu & Li].

A derived illustration [H]: Chinchilla's roughly 20 training tokens per parameter, at κ ≈ 2, implies about 0.1 bit retained per training token.

**Where the teaching bits come from [H, caveat].** Labels are not the only source. Weights also absorb structure of the inputs, from augmentation, the architecture prior and self-supervised targets. The label channel alone is bounded: the information weights carry about the training labels given the inputs is at most `H(Y|X)` summed over the examples. So `s_eff` must count every task-relevant training signal, and `η` absorbs the rest.

A rough consistency check: ImageNet-1k's 1.28M labels carry at most ≈ 1.28M × log₂1000 ≈ 12.8 Mbit. At κ ≈ 2, that is the capacity of a roughly 6M-parameter model, close to where the best-listed TorchVision models reach about 80%. The highest-accuracy entries use extra pretraining data (SWAG). This is suggestive, not a test.

**Data required, as a planning output [H].** Inverting the teaching condition gives the quantity a program must collect:

```
D_required(ε) ≈ max{ ρ_A·K(ε) / (η·s_eff) ,  τ / p_rarest }        collection time ≈ D_required / (useful independent examples per hour)
```

- The first term is **bits-limited**: enough task information must arrive.
- The second is **tail-limited**: the rarest needed skill must be seen about τ times.

Dense supervision shrinks the first term by orders of magnitude but cannot shrink the second. Only curation and oversampling of rare encounters can, which is what Duan's "disagreement mining" does. The calculator reports both terms, which one binds, and the collection time. The reference-function experiment in `experiments/` supplies measured examples-per-parameter ratios for small known functions.

**Supervision bandwidth explains the Tesla degeneracy [H, grounded by E].**
- LeCun's "cake" slide: reinforcement learning gives "a few bits for some samples"; supervised learning gives 10–10,000 bits per sample; self-supervised learning gives "millions of bits per sample".
- Tesla's Duan, CVPR 2026: output is "mostly 2 degrees of freedom", and 90% of randomly sampled fleet data is straight highway driving. See `research/contributions/e2e_industry/findings.md`.

Action-only supervision is close to the reinforcement-learning end: the action entropy per frame is a fraction of a bit. Dense proxy tasks raise `s_eff` by orders of magnitude.

**Correction from the challenge [H].** Only *task-relevant* bits count. Reconstructing asphalt texture spends capacity. So auxiliary supervision has an optimum:
- it lowers the data requirement through `s_eff`;
- it raises the capacity requirement through the auxiliary mapping's own `K`.

This matches Duan's advice that proxy tasks need only be "healthy enough".

**Exponent consequence [T under assumptions; E mixed].** Michaud et al. derive `β = α/(1+α)` for Zipf-distributed skills of equal cost ([arXiv:2303.13506](https://arxiv.org/abs/2303.13506), §2). We checked a generalization in which skill cost grows with rarity, `c_k ∝ k^γ`:
- **If data needed per skill is proportional to its bits** (information-limited learning), `β = α/(1+α)` still holds. *The relation is invariant to γ.*
- **If a fixed exposure threshold applies** (threshold-limited learning), `β = g/(1+g)` with `α = g/(1+γ)`, and `β > α` whenever `γ > α/(1−α)`.

The evidence is mixed:
- Hoffmann et al.'s published fit (α = 0.339, β = 0.285) is near the first regime's prediction of 0.254.
- Epoch's replication refit (α = 0.348, β = 0.366; [arXiv:2404.10102](https://arxiv.org/abs/2404.10102), Table 1) contradicts it. It fits the second regime with γ ≈ 0.66.

Measuring γ independently decides between them. **This is an open question, not a confirmed prediction.**

**A third candidate [E, language only].** Three MIT papers derive a size exponent of 1/3 from representation geometry and a data exponent of 1/3 from softmax training dynamics. On that account the two are not linked through the skill spectrum at all. See [scaling_mechanisms_findings.md](scaling_mechanisms_findings.md).

## 6. Observation sets a floor that no budget buys

- **Bayes floor [T].** Under log loss the floor is `H(Y|R(O))`. Fano's inequality bounds classification error from mutual information (continuous control needs a distortion–rate form instead).
- **Johnson criteria [E, 1958].** The imaging engineer's version. For 50% probability, the target's critical dimension needs about 1.0 cycle (2 pixels) to detect, 1.4 to orient, 4 to recognize and 6.4 to identify.

**NASA flight test, our arithmetic [H on E data].**
- Setup: 4K camera, 41° field of view, about 0.186 mrad per pixel ([NTRS 20205011011](https://ntrs.nasa.gov/citations/20205011011), Table 1: Tempest 3.2 × 1 × 0.3 m; SR22 11.68 × 7.92 × 2.72 m).
- Geometric limit: at 2 pixels across the characteristic dimension √(w·h), detection is possible at about 15 km for the SR22 and 2.6 km for the Tempest.
- Measured first detection: 2.2–3.2 km and about 0.9 km, when the targets spanned about 11 and 6 pixels.
- So the fielded system sat **3–5.5× in range inside the geometric limit**, needing about 3–5.5 Johnson cycles rather than 1.

That gap is where contrast, atmosphere, clutter and detector design live. It is the observation analogue of a code's gap to the Shannon limit.

**Throughput is not description [E + H].** Zheng & Meister estimate human behavioural throughput at about 10 bits/s against sensory intake of about 10⁹ bits/s ([arXiv:2408.10234](https://arxiv.org/abs/2408.10234)). Driving's per-decision information is tiny (the degeneracy), while the size of the mapping, `K`, is huge. Confusing the two is why "2 floats out" felt paradoxical.

## 7. Evidence is bits too, and shares the tail with learning

- **Evidence [T].** Zero failures in `n` independent trials bounds `p < ln(1/a)/n`. Each trial supplies about `p_target·log₂e` bits against the hypothesis that the target was missed.
- **Learning [E + H].** A skill of frequency `p_k` needs about `τ/p_k` examples.

**Shared tail [H].** Both teaching and proving scale as `1/frequency` of the rare encounter. The same fleet exposure feeds both, but the evidence must stay independent of training. *You cannot prove what you could not have taught, and the data that teaches cannot also prove.*

## 8. The condensed law

```
ε*  ≈  ε_obs(sensor, u)  +  ε_K( min{ κ · P_max(hardware, L, T, Z) ,  η · s_eff · D } / ρ_A )     [H]
```

`ε_K(bits)` is the task's reducible error when given that many bits of description. It is decreasing, so the smaller of the storage and teaching budgets binds. For a Zipf spectrum truncated by the operating domain, `ε_K(b) = ε₀[(b/K₀)^(−α) − (K_ODD/K₀)^(−α)]₊`.

**Achievable error is the observation floor plus the reducible error left by the smaller of two bit budgets on one task curve.** Those two budgets are:
- what the hardware can hold and run in time;
- what the data can teach.

Whether the result can be *shown* is a separate budget.

**Five dimensionless numbers [H].** Each is a ratio of supply to demand, like a Reynolds or Mach number. Feasible only if all are ≥ 1 with margin.

| Number | Definition | Replaces earlier inputs |
|---|---|---|
| **Π_obs** observation | pixels on target at required range ÷ pixels the detector needs (Johnson `2N₅₀` as ideal; about 6–11 as measured by NASA). Formally `H(Y|R(O))` versus target. | width, height, patch, feature span, frames |
| **Π_cap** capacity | `κ·P / (ρ_A·K*(ε))` | factors, depth, reuse, novelty, anchors, model size |
| **Π_data** teaching | `min(η·s_eff·D / (ρ_A K(ε)),  D·p_k*/τ)` | novel examples, tail examples, output supervision |
| **Π_rt** real time | `L / t_inference` (roofline plus serial depth) | compute, bandwidth, memory, bits, context, Z, deadline |
| **Π_ev** evidence | `n·p_target / ln(1/a)` | independent trials, target, confidence |

**Intelligence margin [H]:**

```
margin_dB = 10 log κ + 10 log P_max − 10 log ρ_A − 10 log K*(ε)
```

In the capacity-limited regime, each extra 10 dB of hardware lowers error by `10α` dB. With α ≈ 0.3, a 10× hardware jump halves capacity-limited error, and a 10× error reduction needs about 10^(1/α) ≈ 2,000×.

## 9. Floor, ceiling and progress over time

- **Ceiling:** `K_A⁻¹(κ·P)` for the best architecture known.
- **Release:** sits below the ceiling (the attainment gap).
- **Edge-case floor:** the tail skills where `Π_data < 1`.

Progress lowers `ρ_A` (better priors and tokenizers) and pushes `κ` toward its counting limit:
- [E] Vision compute requirements halve about every 9 months (95% CI 4–25; [Erdil & Besiroglu](https://arxiv.org/abs/2212.05153)).
- [E] Language models halve about every 8 months (95% CI about 5–14; [Ho et al.](https://arxiv.org/abs/2403.05812)).
- [E] LLM "capacity density" doubles about every 3 months ([Xiao et al.](https://arxiv.org/abs/2412.04315)).

Same-task description series show descriptions shrinking toward an unknown `K*`:

| Series | Progression |
|---|---|
| ACAS Xu horizontal logic ([Julian et al.](https://arxiv.org/abs/1810.04240)) | Dynamic-programming table of "hundreds of gigabytes" → downsampled table of 600M floats (>2 GB) → networks totalling 2.4 MB, about 1,000× smaller. Decision trees of up to 100 MB still exceeded 6% policy error. |
| AlexNet-level ImageNet | 240 MB (2012) → 6.9 MB (Deep Compression, 2015) → <0.5 MB (SqueezeNet with compression, 2016, [arXiv:1602.07360](https://arxiv.org/abs/1602.07360)) |

These curves are the video's "approach to the Shannon limit" story: channel codes closed most of their gap to capacity over decades, and learned descriptions are doing the same.

**ODD as spectrum truncation [H].** Declaring an operating domain truncates the skill spectrum at `K_ODD`, so `K(ε)` becomes finite as ε approaches the floor. The task becomes completable. Real domains are not hard cut-offs, as the challenge noted. Out-of-domain encounters become an **exit-detection** requirement: a separate and usually cheaper skill, which is the paper's "unknown/ODD exit" contract. This is our proposed reason why bounded operating domains make assurance tractable, and why an unbounded one never finishes.

## 10. Worked illustrations

These are our arithmetic, not claims about any product.

1. **Cart-pole.** `d_int90 = 4`: bits ≈ 4 × 32 = 128. Any processor meets it. This is the regime where Laplace and state-space methods suffice.
2. **ACAS Xu.** The networks hold about 0.5M parameters (≈19 Mbit in fp32). At κ ≈ 2 that is at most about 1 Mbit of task information: an upper bound on `K` at this fidelity, about 10⁴× below the downsampled table's ≈19 Gbit (600M 32-bit floats). The table was large; the task was not. Latency is trivial. The assurance problem moved from storage to closed-loop verification, as the paper's ACAS Xu section shows.
3. **Face verification.** Gong, Boddeti and Jain estimate a *representation* capacity: FaceNet separates about 2.2×10³ identities at FAR 0.1% and 16 at 0.001% ([arXiv:1709.10433](https://arxiv.org/abs/1709.10433)). A strict false-accept target is an observation and representation limit (Π_obs), not a parameter limit. MobileFaceNet's 0.99M parameters reach 92.59% TAR at FAR 10⁻⁶ on MegaFace.
4. **Vision-to-control at 36 Hz.**
   - Setup: L ≈ 27.8 ms, int8, one decode step. The explorer computes `P_max` for several published edge platforms.
   - Tokens: eight 1280×960 streams at 16-pixel patches give `T ≈ 38,400`.
   - Result: at 100 effective TOPS, the compute line allows only about 36M dense-transformer parameters, while the bandwidth line allows billions.
   - Consequences: tokenization, temporal caching and sparse or hierarchical backbones decide feasibility. The gain from Tesla's AI5 over AI4 enters as +10 dB compute and +9.5 dB memory capacity on whichever line binds. Tesla's cited update gives no absolute AI4 figure.

## 11. Decisive experiments (what would falsify this)

1. **Collapse test.** Across architectures, iso-accuracy description size (`d_int90` × bits, or compressed size at the quantization knee) should collapse onto one `K*(ε)`. The per-family `ρ_A` should be stable across ε. Falsified if `ρ_A` swings by orders of magnitude with ε.
2. **κ universality.** Morris-style capacity measurement on CNN, ViT and control policies. The prediction is 1–4 bits/param. Falsified if vision or control models store ≫4 or ≪1 at capacity.
3. **Exponent regime.** Synthesize Zipf skills with controlled cost growth γ; measure α and β. Information-limited learning keeps `β = α/(1+α)`; threshold-limited learning gives `β = g/(1+g)`. This decides between Hoffmann's fit and Epoch's refit.
4. **Supervision optimum.** At fixed P near `Π_cap ≈ 1`, compare three conditions:
   - action-only;
   - action plus clean task-relevant auxiliary targets;
   - action plus nuisance-heavy video prediction.

   The prediction is that the clean condition is best and the nuisance-heavy one hurts tail skills. Falsified if performance rises monotonically with supervision bits.
5. **ODD saturation.** A bounded synthetic domain should saturate at `P ≈ K_ODD/κ`. Exit detection should cost much less than covering the tail.
6. **Tokenizer optimum.** Predict `u*` from Johnson geometry plus capacity scaling, then measure it on a small-target detection task.
7. **Depth on smooth dynamics.** Fixed-width residual networks, depth sweep, on the flow maps. The MIT toy result predicts loss ∝ `ℓ^(−3)` for a smooth dynamical target against `ℓ^(−1)` for language-like targets. Falsified if the flow maps also show `ℓ^(−1)`.

## 12. First measurements: the reference-function ladder

See [reference_ladder_findings.md](reference_ladder_findings.md) and the `/ladder` page. This was a laptop-scale run: 630 trainings, 49 minutes. MLPs were fitted to known functions: PID, clipped PID, pendulum, cart-pole, double pendulum, flow maps up to 800 ms, and the pendulum seen only through camera frames.

- **The ladder [E, this experiment].** Bits the network needed for 1%: ≈136 (PID, close to its formula) → ≈1.4k (pendulum) → ≈75k (cart-pole) → more than 149k for just 3% (double pendulum).
- **Mismatch is measurable [E].** A clip costs about 900× in parameters, sin/cos inputs save about 2–4×, and camera input costs about 58× in parameters and at least 5× in examples.
- **Chaos [E + H].** Required size grows about 18× from 50 to 400 ms, near the `d·λ ≈ 7/s` a Lipschitz argument predicts. At fixed size, error grows at roughly the Lyapunov rate.
- **Data calibration [E + H].** On well-matched, noise-free tasks, the labels needed carry about as many bits as the network needed. So retention `η` ≈ 0.3–1.4 when `s_eff = outputs × log₂(1/ε)`. Weights exceed labels by 10–40× exactly where the architecture fits badly, which gives a direct way to estimate ρ_A.

## 12a. The law read backwards: size for a tolerance

See [scaling_mechanisms_findings.md](scaling_mechanisms_findings.md).

- **Language transformers [E; our inversion H].** Liu, Gore and co-authors find excess loss ≈ `c_m/m + c_ℓ/ℓ + c_D/D^0.30`. Inverted, `N_req = (27/4)·k·c_m²·c_ℓ/ε³`: halving the excess loss costs 8× the parameters and 64× the training compute. That is `K(ε)` with α = 1/3.
- **The exponent is a task property [E, this experiment].** Refitting the ladder as `MSE ∝ P^(−a)` gives `a` ≈ 1.5 (pendulum), 1.1 (cart-pole), 0.9 falling to 0.55 with horizon (double pendulum) and 0.25 (clipped PID). Complexity moves both `K₀` and `α`.
- **Softmax outputs add a training term [E, language and MNIST].** Loss falls as `τ^(−1/3)` whatever the data carries, so `D_req` needs a third term for tokenized outputs, and η is not constant there.
- **Depth is the latency line [H].** Under `1/ℓ`, a deadline sets a depth-limited floor `c_ℓ/ℓ_max`.

## 13. Status summary

| Element | Status |
|---|---|
| Minimax code length bounds network approximation rate (function classes) | [T] Elbrächter et al. Thm VI.4 |
| Bayes floor, Fano, zero-failure bound, roofline arithmetic | [T] |
| κ ≈ 1–3.6 bits/param; ternary models match FP16 | [E] |
| `d_int90` ladder, random-label 250× | [E] |
| β = α/(1+α) under Zipf and equal cost | [T under assumptions] Michaud et al.; empirical support mixed |
| Loss ∝ 1/width, 1/depth, time^(−1/3) in language models | [E] Liu, Gore et al. (three papers); toy-model mechanisms; untested on vision or control |
| Inverted requirement `N_req ∝ ε^(−3)`; task-dependent exponent on the ladder | [H] our arithmetic; [E] our refit, few points per task |
| Invariance of that relation to power-law cost growth (information-limited) | [T under our stated model] our derivation, unreviewed |
| Average-case `K(ε)` as a measurable task property; the ε* max law; the five Π numbers; dB margin; ODD truncation; supervision optimum; tokenizer optimum | [H] ours |
| Prior art | Jeon & Van Roy derive information-theoretic scaling laws for a two-layer teacher, with data ∝ model size up to logs ([arXiv:2407.01456](https://arxiv.org/abs/2407.01456)). Hutter derives power-law learning curves from Zipf features ([arXiv:2102.04074](https://arxiv.org/abs/2102.04074)). A grounded search found no prior statement of model size as task rate–distortion divided by bits per parameter. That is not proof none exists. |
