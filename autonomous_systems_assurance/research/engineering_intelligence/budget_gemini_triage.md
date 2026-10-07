# Gemini triage: intelligence-budget scouts, 2026-09-28

**Runs.** Four grounded `gemini-3.8-flash` calls (thinking high, temperature 0.1, one worker, pauses between calls) from [run_budget_scouts.py](run_budget_scouts.py). Prompts and raw responses are in ignored `out/budget_*`. Gemini output is lead material, not evidence. Every number used in [intelligence_budget.md](intelligence_budget.md) or the site was checked against the original PDF, abstract or captions, or else carries a `documented`/`secondary` status in the ladder data.

| Run | Result |
|---|---|
| `sources` | **Empty response**: about 8k thinking tokens, no text. Replaced by direct retrieval and by `sources2`. |
| `ladder` | 51 candidate rows plus 10 hardware anchors. Used as a lead list only. |
| `challenge` | Adversarial check of hypotheses H0–H7. The most useful run. |
| `sources2` | Prior art and remaining anchors. |

## Accepted after checking the original

- **Kolmogorov–Donoho bound.** Elbrächter, Perekrestenko, Grohs & Bölcskei, [arXiv:1901.02220](https://arxiv.org/abs/1901.02220): minimax code length (Def. IV.1) and Theorem VI.4. Read in the PDF.
- **Bits per parameter.**
  - Allen-Zhu & Li: 2 bits/param after about 1,000 exposures; 1 bit at 100 exposures; int8 keeps 2, int4 falls to 0.7. Checked in PDF §1.
  - Morris et al.: 3.5–3.6 bits/param in bf16, 3.83 in fp32. The paper also cites perceptron capacity of 2 bits/weight (Cover 1965). Checked in PDF.
- **Ternary weights.** BitNet b1.58 matches LLaMA "at 3B model size" (PDF p. 3).
- **Skill-quanta relation.** Michaud et al. derive `α_D = α_N/(α_N+1)` (§2). Their Appendix F calls the empirical data "too messy to definitively support or contradict" it.
- **Chinchilla replication.** Besiroglu et al. refit α = 0.3478, β = 0.3658, against Hoffmann's α = 0.3392, β = 0.2849 (PDF Table 1).
- **Supporting sources checked in the original:**
  - Li et al. intrinsic-dimension Table 1;
  - ACAS Xu storage figures (Julian et al. PDF);
  - Deep Compression and SqueezeNet abstracts;
  - Zheng & Meister abstract;
  - Gong, Boddeti & Jain capacity abstract;
  - Erdil & Besiroglu (9 months, 95% CI 4–25);
  - Ho et al. (about 8 months, CI 5–14);
  - Densing law (about 3 months);
  - Merrill & Sabharwal and Snell et al. abstracts;
  - Jeon & Van Roy abstract;
  - Hutter 2021 abstract.
- **Hardware.** Tesla HW3 memory: LPDDR4-4266, 68 GB/s peak per chip, and 32 MB SRAM per accelerator (Autonomy Day 2019 captions, 01:21:40). NASA target dimensions (Table 1).
- **Challenge corrections adopted:**
  - `κ = b` is not a meaningful ceiling above the working-precision knee (Morris et al.'s fp32 result).
  - The bandwidth line needs the decode-step factor `(1+Z)`.
  - A serial-depth floor is required.
  - Memory must reserve activations and KV cache (the calculator reserves 30%, an assumption).
  - Roofline is shown as both optimistic `max` and pessimistic `sum`.
  - Auxiliary supervision counts only task-relevant bits, and nuisance targets spend capacity. This turns "more supervision is better" into a predicted optimum.
  - Skills are not additive: `K(S) ≤ Σ c_k`. We recast this as the place assembly theory contributes: shortest construction with reuse.
  - Operating-domain truncation is a reweighting plus an exit-detection requirement, not a hard cut-off.

## Rejected or corrected

1. **The challenge's claim that `β = α/(1+α+γ)` when skill cost grows as `k^γ`.** This is wrong because it held α fixed. With `α = g/(1+γ)` and data needed per skill proportional to its bits, `β = g/(1+g+γ) = α/(1+α)`: the relation is invariant. It fails only under a fixed exposure threshold. Our derivation is recorded in the note, unreviewed.
2. **The challenge's claim that generalizing "programs" escape `κ ≤ b`.** This confuses output bits with description bits. The counting bound applies to description.
3. **Ladder errors.**
   - ALVINN given as 4,073 weights with 4 hidden units. The 1989 paper has 1,217 → 29 → 46 units, about 36.6k weights.
   - ACAS Xu "10,755 weights, 5 × 50 ReLUs". We use Julian et al.'s own numbers: 45 networks of about 11,000 parameters, 2.4 MB in total.
   - ACAS Xu table "120M states, 2.1 GB, 16-bit". We use the paper's own "600 million floating point numbers… over 2GB".
4. **Ladder rows not found or not used.**
   - "Rozon et al., J. Aerosp. Inf. Syst., YOLOv5s DAA": not verified, not used.
   - openpilot `supercombo` 25.7M parameters and 51.5 MB: not verified, not used.
   - Space Shuttle PASS word count: not verified, not used.
   - Stockfish NNUE and AlphaGo Zero parameter counts: not verified, not used.
5. **Tesla AI4.** Teardown bandwidth and TOPS (384 or 224 GB/s, 300–500 TOPS) and the "3–5×" and "8× bandwidth" executive remarks are not used. AI4 remains the 0 dB reference, and AI5 enters only as Tesla's own relative targets.
6. **Hutter 2021's exponent formula** as stated by Gemini (`β = α − 1`) was not checked; only the paper's abstract-level claim is cited.
7. **LeCun "cake" numbers.** Widely reproduced slide wording; the primary slide deck was not retrieved. They are used only as framing, and the page labels its supervision bars "illustrative".
8. **Landauer comparison.** The 10⁸–10⁹ gap from Gemini's arXiv:2503.09844 citation was not checked and is not used.

## Open items before any publication use

- Retrieve the Johnson 1958 DTIC record and a primary LeCun slide deck.
- Capture PDF snapshots and hashes for all [E] rows.
- Have a human re-derive the γ-invariance result.
- Measure `κ` on a vision or control model (experiment 2 in the note) before transferring language-model κ to driving.
