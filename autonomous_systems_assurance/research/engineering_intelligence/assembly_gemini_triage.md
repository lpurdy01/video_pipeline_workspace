# Gemini assembly challenge: human-source triage

**Run:** 27 September 2026, one approved Google-search-grounded `gemini-3.8-flash` request with high thinking. Prompt and unedited API response are ignored under `out/assembly_*_20260927T211219Z.*`. The model's answer is a research scout, not evidence or an independent review disposition. See [source leads](source_leads.md) for the original sources inspected after the call.

## Retained and independently checked

- The string assembly-index/straight-line-program correspondence is a useful restricted result. The [Masierak paper](https://arxiv.org/html/2604.16302v1) explicitly specifies free alphabet terminals, binary concatenation and unlimited reuse. The [Bieniawski preprint](https://arxiv.org/html/2608.19228v1) summarizes the equivalence and warns that string grammars do not model physical geometry or thermodynamics. Neither supplies a neural model-size conversion.
- The [quantization model of neural scaling](https://arxiv.org/html/2303.13506v3) is unusually close to our idea: skill-use frequency and learning order can generate power-law loss in its simplified model. Its assumptions and tentative empirical language analysis are explicit. It makes the assembly “copy number” intuition more testable, but also provides a strong baseline against which assembly features must add predictive value.
- The [manifold-dimension scaling theory](https://arxiv.org/abs/2004.10802) and [multiple-scaling-regime theory](https://arxiv.org/abs/2102.06701) are relevant alternatives. Grammar alone may omit geometric or spectral resolution limits.
- The challenge correctly emphasized matched inputs with different label rules, shortcut shifts, compositional extrapolation, optimization barriers, and rare-slice scarcity as falsifiers.

## Rejected or narrowed

- **“No primary research exists” connecting task complexity to scaling:** too broad for a targeted search, and the quantization/manifold papers are already candidate connections. Our narrower finding is that we have **not found a validated direct map from assembly index or task-conditional grammar length to deployment model size** in the inspected sources.
- **“The prototype excludes KV traffic”:** false. Its explicit traffic scenario includes a user-entered KV state and one full KV read per generated output step. That remains crude and excludes some activations, attention work, cache layout, batching and hardware overhead.
- **“Roofline assumes 100% device efficiency”:** not if the user enters measured *effective* compute and bandwidth, as the UI asks. The max-of-compute-and-bandwidth form still assumes an optimistic scheduling/overlap scenario and omits other latency.
- **“SQ lower bounds prove gradient descent needs \(d^{\Omega(k)}\) samples for sparse parity”:** the model promoted a more specific gradient-descent conclusion than we verified from the named original source. Sparse parity is retained as an experimental optimization challenge, without that quantitative claim.
- **“Canonical assembly is mathematically equivalent to Shannon entropy rate”:** this is the 2026 critics' contested position, not an adjudicated fact; the original authors dispute the comparison. Report both sides and test ordinary compression as a baseline.
- **“A short grammar makes the learned model small”:** description length does not establish learnability by an architecture or optimizer. The research note now includes optimization response as a separate axis.

The model also supplied an incorrect implication that its listed source locators were inspected by *this* project. Only the regions documented in [source_leads.md](source_leads.md) were independently inspected. Its raw response is not copied into publication inputs.
