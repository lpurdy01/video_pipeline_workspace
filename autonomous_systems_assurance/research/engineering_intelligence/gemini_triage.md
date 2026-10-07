# Gemini research-scout triage

Run on **27 September 2026** with the project-approved Gemini API (`gemini-3.8-flash`, high thinking, Google Search grounding). One request; raw prompt, model response and grounding metadata are retained under ignored `out/`. The response reported 53 grounding chunks. SHA-256: prompt `ef0a71440fed545b57b460305765a6278a69fb19261653d46da0d1788ee88aa1`; Markdown response `1295e0483f21ae0b92dc8161e9662e63501c66fd025d2bca6da67374d4ca1299`. Its suggestions are leads, not evidence. Primary-source checks are recorded in [source_leads.md](source_leads.md).

| Gemini suggestion | Disposition |
|---|---|
| Chinchilla-style joint data/model fit, objective intrinsic dimension, compositional approximation, data repetition, and rare-event binomial bounds | Retained as bounded leads after checking original author or publisher pages. The draft does not transfer fitted constants between tasks. |
| “Conditional entropy defines the irreducible Bayes error” | Corrected: conditional entropy is optimal **log loss**; for zero-one classification, the Bayes error is \(\mathbb E[1-\max_y P(Y=y\mid X)]\). |
| A universal parameter lower bound obtained by substituting feature-covariance effective rank into a compositional approximation exponent | Rejected: the quantities come from different assumptions; no inspected source justifies that substitution. |
| Chinchilla's \(6ND\) training-FLOP estimate and equal data/parameter scaling as a general rule for control, vision or all tasks | Rejected outside its model/training setting. Useful only as a within-family language-model example. |
| Takens embedding dimension used as a hard neural context-length minimum; Lyapunov horizon said to improve as \(\log N\) with model parameters | Rejected. The former is a theorem with genericity and observation assumptions, not a blanket network limit; the latter has no established parameter-to-estimation-error relation in the cited source. |
| DAgger's error upper bound converted into a claim that every behavioral-cloning policy must diverge quadratically | Rejected. A bound under assumptions is not a universal observed rate or lower bound. |
| Assembly theory “proved equivalent” to LZ/Shannon entropy, with zero possible relevance | Corrected: an original critique and a later author response dispute equivalence. No inspected result maps assembly index to neural model resources. |
| A fabricated numeric claim that softmax abstention misses at least 30% of rare hazards; broad claim that safety standards mandate particular deterministic overrides | Rejected; not established by the cited papers or the project's public-source standard boundary. |
| One number for “certified” catastrophic risk from independent trials | Corrected: equation (5) applies only to a defined event rate under an independent, representative sampling model; hazard occurrence, detector misses, and system harm remain distinct. |

The new draft is separate from `resource_composition/whitepaper.md` and the verification compiler. Before any factual paragraph is used for publication, retrieve full source contexts, create stable `S-*` and `C-*` records with regions and hashes, and run the project's challenge/review workflow.
