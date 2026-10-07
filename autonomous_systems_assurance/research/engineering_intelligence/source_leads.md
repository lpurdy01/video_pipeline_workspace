# Engineering-of-intelligence source leads

**Search/inspection date:** 27 September 2026. These `EI-*` labels are local reading-list locators, **not** registered `S-*` evidence IDs or `C-*` publication claims. Original sources are linked separately from the synthesis in [draft.md](draft.md). Inspection scope varies by row: many leads were read only at the landing page or abstract, while selected original HTML articles and Hoffmann et al.'s Tables 1 and 6, §§3 and D.2 were inspected more closely. Full-text retrieval, local snapshots and region hashes remain publication work.

| Lead | Original source and inspected locator | Bounded use and inspection limit |
|---|---|---|
| EI-01 | [CMU 10-601, Bayes optimal classifier lecture](https://www.cs.cmu.edu/~mgormley/courses/10601-s24/slides/lecture10-reg-ink.pdf), 2024, search excerpt; [Hoffmann et al. §D.2](https://arxiv.org/html/2203.15556v1), 2022, inspected HTML | Basic Bayes decision risk and log-loss decomposition. The general cost-sensitive form in the draft is derived from conditional minimization; the lecture PDF was not fully inspected. |
| EI-02 | [Tishby, Pereira and Bialek, *The Information Bottleneck Method*](https://arxiv.org/abs/physics/0004057), 1999/2000, abstract | Task-relevant compression. No model-size conversion is asserted. |
| EI-03 | [Dean et al., *On the Sample Complexity of the Linear Quadratic Regulator*](https://arxiv.org/abs/1710.01688), 2017/2018, abstract | Finite-sample identification and robust control for unknown linear dynamics under the paper's assumptions; no formula generalized to vision. |
| EI-04 | [Li et al., *Measuring the Intrinsic Dimension of Objective Landscapes*](https://arxiv.org/abs/1804.08838), 2018, abstract | Random subspace experiment; the operational definition is specific to its task, target and training setup. |
| EI-05 | [Poggio et al., *Why and When Can Deep—but Not Shallow—Networks Avoid the Curse of Dimensionality?*](https://arxiv.org/abs/1611.00740), 2017, abstract | Function classes with compositional structure can favor deep representation. Exact approximation rates need full-text verification before publication. |
| EI-06 | [Muennighoff et al., *Scaling Data-Constrained Language Models*](https://arxiv.org/abs/2305.16264), 2023, revised 2025, abstract | Repeated tokens have a diminishing marginal value in the tested language-model regime; not a universal “four epochs” rule. |
| EI-07 | [Sorscher et al., *Beyond Neural Scaling Laws: Beating Power Law Scaling via Data Pruning*](https://arxiv.org/abs/2206.14486), 2022, abstract | Data selection changes observed image-classification scaling under the reported benchmarks; its ideal exponential possibility is theoretical/conditional, not a measured universal law. |
| EI-08 | [Hoffmann et al., *Training Compute-Optimal Large Language Models*](https://arxiv.org/html/2203.15556v1), 2022, §§3.3, D.2 and abstract inspected | Fitted \(E+A/N^\alpha+B/D^\beta\), efficient frontier and 70B versus 280B comparison for its language-model setting. Fitted \(E\) is not directly measured true Bayes risk. |
| EI-09 | [Caballero et al., *Broken Neural Scaling Laws*](https://arxiv.org/abs/2210.14891), 2023, abstract | Empirical scaling can have breaks and nonmonotonic regions; no guaranteed extrapolation to a new safety metric. |
| EI-10 | [Zhang et al., *Understanding Deep Learning Requires Rethinking Generalization*](https://arxiv.org/abs/1611.03530), 2017, abstract | Networks can fit random labels; parameter count alone does not explain ordinary generalization. |
| EI-11 | [D'Amour et al., *Underspecification Presents Challenges for Credibility in Modern Machine Learning*](https://arxiv.org/abs/2011.03395), 2020/2022, abstract | Similar held-out performance can coexist with different deployment behavior. |
| EI-12 | [Lorenz, *Deterministic Nonperiodic Flow*](https://journals.ametsoc.org/doi/abs/10.1175/1520-0469%281963%29020%3C0130%3Adnf%3E2.0.CO%3B2), 1963, publisher abstract | Sensitivity of certain deterministic flows to initial conditions. The exponential horizon expression in the draft is a local approximation, not a result about all controllers. |
| EI-13 | [Ross, Gordon and Bagnell, *A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning*](https://proceedings.mlr.press/v15/ross11a.html), 2011, PMLR abstract | Sequential policies change future observations; their bounds depend on reduction assumptions. No universal quadratic failure prediction. |
| EI-14 | [NIST Technical Note 2119, *Estimating Instrument Performance: with Confidence Intervals and Confidence Bounds*](https://www.nist.gov/publications/estimating-instrument-performance-confidence-intervals-and-confidence-bounds), 2020, publisher description; [NIST exact binomial guidance](https://www.itl.nist.gov/div898/software/dataplot/refman1/auxillar/propconf.htm), public documentation | Detection and false-alarm confidence intervals. Equation (5) is directly derived from the binomial zero-event probability, under independent representative trials. |
| EI-15 | [Kalra and Paddock, RAND, *Driving to Safety*](https://www.rand.org/pubs/research_reports/RR1478.html), 2016, publisher summary | Very large exposure needed for rare-event comparative driving claims; exact mile counts depend on the chosen claim and assumptions. |
| EI-16 | [Sharma et al., *Assembly Theory Explains and Quantifies Selection and Evolution*](https://www.nature.com/articles/s41586-023-06600-9), 2023, visible full article, especially “Assembly index and copy number” | Original assembly-index and copy-number proposal concerns constructed physical objects and selection; its primitive units are measurement-defined. No neural sizing result identified. |
| EI-17 | [Zenil et al., *On the Salient Limitations of the Methods of Assembly Theory*](https://pmc.ncbi.nlm.nih.gov/articles/PMC11306634/), 2024, accessible article abstract/search excerpt | Critique argues assembly-index calculations resemble existing compression measures. Its equivalence argument is contested; the draft does not adopt it as settled. |
| EI-18 | [Sharma et al., *Assembly Theory and Its Relationship with Computational Complexity*](https://www.nature.com/articles/s44260-025-00049-9), 2025, visible article introduction and comparison | Authors argue formal differences from LZW and other measures. This confirms the comparison is disputed; it does not establish a bridge to model sizing. |
| EI-19 | [Sterkenburg and Grünwald, *The No-Free-Lunch Theorems of Supervised Learning*](https://arxiv.org/abs/2202.04513), 2022, abstract | Explains the assumptions behind no-free-lunch results and why model-dependent inductive bias allows useful conditional claims; no numeric sizing law. |


| EI-20 | [Bieniawski, *Assembly Theory and the Smallest Grammar Problem*](https://arxiv.org/html/2608.19228v1), July 2026 preprint, inspected abstract and §§2.1–2.4 | Reports equality of string assembly index and smallest straight-line grammar rule count under binary concatenation; evaluates compressor approximations on 408 strings. Scope is strings; the paper states it does not model geometric/thermodynamic assembly. Peer review and cited proof not independently checked. |
| EI-21 | [Masierak, *Computational Complexity of Determining the Assembly Index*](https://arxiv.org/html/2604.16302v1), January 2026 journal article, inspected HTML §§1–3 definitions and proof setup | Establishes string-based ASI/SLP correspondence and NP-completeness with free terminal symbols, binary concatenation and unlimited intermediate reuse; not a statement about molecule graphs or neural networks. |
| EI-22 | [Ozelim et al., *Assembly Theory Collapses to Dictionary Compression and Is Rendered Redundant by Common Statistical Algorithms*](https://www.nature.com/articles/s44260-026-00088-w), accepted early article July 2026, publisher search rendering/abstract inspected; direct article fetch redirected | Authors argue assembly index adds no distinct information beyond compression. This is a contested critique, not an adjudicated result; compare with EI-18. |
| EI-23 | [Dosovitskiy et al., *An Image is Worth 16×16 Words*](https://arxiv.org/abs/2010.11929), 2020/2021, abstract | Original Vision Transformer divides images into patch sequences. Patch count is a representation/workload descriptor, not an information-retention or model-size law. |
| EI-24 | [Schmidt et al., *Tokenization Is More Than Compression*](https://arxiv.org/abs/2402.18376), 2024, abstract | In 64 tested language models, minimum token count did not yield better downstream performance by itself. Language result warns against a universal “fewer tokens is better” inference. |
| EI-25 | [Williams, Waterman and Patterson, *Roofline: An Insightful Visual Performance Model for Multicore Architectures*](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2008/EECS-2008-134.pdf), 2008, original technical-report PDF opened; equations and figures require closer local inspection | Hardware performance depends on arithmetic intensity, compute peak and memory bandwidth. A roofline estimate needs an explicitly assumed traffic/work model and effective hardware rates. |
| EI-26 | [Dao et al., *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*](https://arxiv.org/abs/2205.14135), 2022, abstract | Attention algorithms can change memory traffic materially; naive FLOP or parameter counts alone do not determine latency. |
| EI-27 | [Grünwald and Roos, *Minimum Description Length Revisited*](https://arxiv.org/abs/1908.08484), 2019, abstract | MDL is a mature family of task/model selection ideas for compact explanation. A chosen description language and residual coding scheme still do not provide a universal parameter conversion. |


| EI-28 | [Michaud et al., *The Quantization Model of Neural Scaling*](https://arxiv.org/html/2303.13506v3), NeurIPS 2023, revised 2024, inspected abstract and §2 | Under explicit equal-capacity, frequency-order and Zipf assumptions, derives a power-law remaining loss from learned skill “quanta”; toy validation and tentative language-model skill-frequency analysis. Does not prove those assumptions for control or derive an assembly-to-parameter conversion. |
| EI-29 | [Sharma and Kaplan, *A Neural Scaling Law from the Dimension of the Data Manifold*](https://arxiv.org/abs/2004.10802), 2020, abstract inspected | Regression-on-manifold theory predicts α≈4/d for the specified losses and assumptions, tested in teacher/student, image and language experiments. Not a universal task dimension or an observed law for visual control. |
| EI-30 | [Bahri et al., *Explaining Neural Scaling Laws*](https://arxiv.org/abs/2102.06701), 2021, abstract inspected | Proposes variance- and resolution-limited regimes with distinct causes of scaling and tests on controlled models and standard datasets. Its taxonomy cautions against one saturation curve across tasks. |

**Retrieval scope:** English-language web search, publisher pages, arXiv abstracts and selected accessible HTML as noted. This is a targeted discovery pass, not an exhaustive literature review. No paywalled standard text or private model architecture was inspected. No source was promoted into the project's `sources.json`/`claims.json` registers. Newer 2026 assembly publications may change on peer review or after early-access editing.

## Cross-domain primary-source additions (2026-09-27)

These leads support the separate [cross-domain findings](cross_domain_findings.md) and the site's source-linked observations. They are not yet formal publication claim records.

| ID | Original source and inspection scope | Useful limit question |
|---|---|---|
| EI-31 | [TorchVision 0.17 model tables](https://docs.pytorch.org/vision/0.17/models.html), official pinned documentation; all float-weight summary rows inspected and extracted, 139 scored configurations, per-weight row locators and links | Attained score against parameters and work on four separate benchmark tasks; no universal ceiling. |
| EI-32 | [Smyers et al., AVOIDDS](https://arxiv.org/pdf/2306.11203), author preprint v2, §§3–4 and Appendix C Tables 4–5 inspected | Same 11.2M-parameter YOLOv8s architecture, different training coverage and slice outcomes; synthetic domain. |
| EI-33 | [Gandhi et al., AirTrack](https://arxiv.org/pdf/2209.12849), author preprint, Figs. 1–2 and 5, §V inspected | High-resolution small-target pipeline, track probability by range and Xavier latency/optimization contrast; author standard interpretation only. |
| EI-34 | [Dolph et al., NASA monocular ranging](https://ntrs.nasa.gov/citations/20205011011), NASA-hosted conference paper, Table 3 and §VI inspected | Sensor/target geometry limit: first detection range for small UAS versus SR22 under one 4K optical setup. |
| EI-35 | [Chen et al., MobileFaceNets](https://arxiv.org/pdf/1804.07573), original paper, abstract and Tables 3–4 inspected | Sub-1M-parameter face model and thresholded MegaFace TAR at FAR 10^-6; task-specific narrow success. |
| EI-36 | [Tesla Q4 2025 update](https://ir.tesla.com/_flysystem/s3/sec/000162828026003837/tsla-20260128-gen.pdf), first-party investor update, p. 10 inspected | AI5 relative targets, 2027 production plan at the time; AI4 absolute throughput absent. |
| EI-37 | [Tesla Autonomy Day 2019](https://www.youtube.com/watch?v=Ucp0TTmvqOE), first-party video, auto-captions inspected at 01:18:38, 01:22:49 and 01:32:58; [Tesla event notice](https://ir.tesla.com/press-release/tesla-host-autonomy-investor-day) confirms event and presenter | HW3 vendor architecture/throughput claim; dual independent chips cannot be treated as one model's resources. |
| EI-38 | [NVIDIA Jetson AGX Orin technical brief v1.2](https://www.nvidia.com/content/dam/en-zz/Solutions/gtcf21/jetson-orin/nvidia-jetson-agx-orin-technical-brief.pdf) and [DRIVE AGX specifications](https://developer.nvidia.com/drive/agx), first-party specs | Peak INT8/sparse INT8 and bandwidth anchors, requiring precision/workload normalization before fitting. |
| EI-39 | Original CVPR papers: [DeepFace 2014](https://openaccess.thecvf.com/content_cvpr_2014/html/Taigman_DeepFace_Closing_the_2014_CVPR_paper.html), [FaceNet 2015](https://www.cv-foundation.org/openaccess/content_cvpr_2015/papers/Schroff_FaceNet_A_Unified_2015_CVPR_paper.pdf), [ArcFace 2019](https://openaccess.thecvf.com/content_CVPR_2019/papers/Deng_ArcFace_Additive_Angular_Margin_Loss_for_Deep_Face_Recognition_CVPR_2019_paper.pdf); abstracts/results inspected | Recognizable LFW cases, but changed training/protocols and near-saturated benchmark limit any cross-paper parameter frontier. |

No licensed ASTM text was inspected. Source status and bounds are recorded in `interactive/src/data/cross_domain.json`; raw downloaded copies are ignored under `out/sources/`.
| EI-40 | [Tesla Q1 2026 update](https://ir.tesla.com/_flysystem/s3/sec/000162828026026551/tsla-20260422-gen.pdf), p. 8; [Tesla Q2 2026 update](https://ir.tesla.com/_flysystem/s3/sec/000162828026049213/tsla-20260722-gen.pdf), p. 8; first-party PDFs inspected | AI5 final chip design, vendor up-to-20% software inference-latency claim, and qualitative AI4-to-AI3 FSD distillation. None supplies an AI4 absolute throughput or AI5 measured capacity. |
| EI-41 | [Karampinis et al., vision-only UAV collision avoidance](https://arxiv.org/pdf/2405.06749), 2024 author preprint; abstract, §III and experimental setup inspected | Detector + tracking + depth-estimator pipeline, useful architectural contrast; no matched whole-pipeline parameter and target-device throughput datum admitted to atlas. |

## Mathematical-limit leads from the focused Gemini challenge (2026-09-28)

| ID | Original source and inspection scope | Boundary |
|---|---|---|
| EI-42 | [Yarotsky, *Error bounds for approximations with deep ReLU networks*](https://arxiv.org/abs/1610.01145), 2017 original PDF, §4.1 Theorem 3 and surrounding assumptions inspected | `W >= c ε^(-d/n)` for uniform Sobolev-class approximation with continuous weight selection; not a particular autonomous task's P minimum. |
| EI-43 | [Safran and Shamir, *Depth-Width Tradeoffs in Approximating Natural Functions*](https://proceedings.mlr.press/v70/safran17a.html), ICML 2017 original PDF, Theorems 1–2 inspected | Exponential depth-2 width requirement for a ball indicator under specified distribution/error; efficient depth-3 counterpart. |
| EI-44 | [Raz, *Fast Learning Requires Good Memory*](https://arxiv.org/abs/1602.05161), original PDF, abstract and §1 inspected | Streaming parity learning needs quadratic training memory or exponential samples; not inference model-parameter bound. |
| EI-45 | [Merrill, Sabharwal and Smith, *Saturated Transformers are Constant-Depth Threshold Circuits*](https://arxiv.org/abs/2106.16213), original abstract inspected | Formal saturated-transformer TC⁰ upper bound; details and task separations need full-text audit before publication. |
| EI-46 | [Daouia, Florens and Simar, *Frontier Estimation and Extreme Values Theory*](https://arxiv.org/abs/1011.5722), original abstract/publisher record inspected | Potential statistical frontier method only if model-search sampling assumptions can be specified; current atlas cannot justify a true-capacity upper confidence bound. |

## Intelligence-budget sources (2026-09-28)

These support [intelligence_budget.md](intelligence_budget.md) and the `/budget` page. Unless noted, the locators below were checked in the original PDF, abstract or captions. Snapshots are in ignored `out/sources/`, with SHA-256 values below.

| ID | Source | Checked locator and use |
|---|---|---|
| EI-47 | [Elbrächter, Perekrestenko, Grohs & Bölcskei, *Deep Neural Network Approximation Theory*](https://arxiv.org/abs/1901.02220) | Def. IV.1 minimax code length and optimal exponent; Thm VI.4, network approximation rate ≤ γ*(C). Function classes, worst case. |
| EI-48 | [Allen-Zhu & Li, *Physics of Language Models 3.3*](https://arxiv.org/abs/2404.05405) | Abstract and §1 Results 1, 4, 8: 2 bits/param at 1,000 exposures, 1 at 100, int8 keeps 2, int4 0.7. Synthetic knowledge. |
| EI-49 | [Morris et al., *How much do language models memorize?*](https://arxiv.org/abs/2505.24832) | Abstract and precision section: 3.5–3.6 bits/param in bf16, 3.83 in fp32. Related work cites perceptron capacity of 2 bits/weight. |
| EI-50 | [Ma et al., *The Era of 1-bit LLMs*](https://arxiv.org/abs/2402.17764) | p. 3: ternary weights match LLaMA "at 3B model size". |
| EI-51 | [Li et al., intrinsic dimension](https://arxiv.org/abs/1804.08838) | Table 1 and §3 (see EI-04): pendulum 4 … ImageNet >500k; shuffled labels 190,000. |
| EI-52 | [Julian, Kochenderfer & Owen, ACAS Xu compression](https://arxiv.org/abs/1810.04240) | §II "hundreds of gigabytes", "600 million floating point numbers… over 2GB", decision trees, "2.4 MB"; §IV 45 × about 11,000 parameters. |
| EI-53 | [Han et al., Deep Compression](https://arxiv.org/abs/1510.00149); [Iandola et al., SqueezeNet](https://arxiv.org/abs/1602.07360) | Abstracts: AlexNet 240 → 6.9 MB; VGG-16 552 → 11.3 MB; SqueezeNet <0.5 MB at AlexNet level. |
| EI-54 | [Besiroglu et al., Chinchilla replication](https://arxiv.org/abs/2404.10102) | Table 1: refit α 0.3478, β 0.3658 vs published 0.3392, 0.2849. |
| EI-55 | [Zheng & Meister, *The Unbearable Slowness of Being*](https://arxiv.org/abs/2408.10234) | Abstract: about 10 bits/s behaviour vs about 10⁹ bits/s sensory. |
| EI-56 | [Gong, Boddeti & Jain, *On the Capacity of Face Representation*](https://arxiv.org/abs/1709.10433) | Abstract (arXiv version): FaceNet 2.2×10³ identities at FAR 0.1%, 16 at 0.001%. Journal version not compared. |
| EI-57 | [Erdil & Besiroglu](https://arxiv.org/abs/2212.05153); [Ho et al.](https://arxiv.org/abs/2403.05812); [Xiao et al., Densing law](https://arxiv.org/abs/2412.04315) | Vision compute halving about 9 months (CI 4–25); LM about 8 months (CI 5–14); capacity density doubling about 3 months. |
| EI-58 | [Merrill & Sabharwal, CoT expressivity](https://arxiv.org/abs/2310.07923); [Snell et al., test-time compute](https://arxiv.org/abs/2408.03314) | Abstracts: immediate-answer transformers fail simple sequential problems, while linear CoT adds power; test-time compute beats a 14× larger model FLOPs-matched on some problems. |
| EI-59 | [Jeon & Van Roy](https://arxiv.org/abs/2407.01456); [Hutter, *Learning Curve Theory*](https://arxiv.org/abs/2102.04074) | Prior art: information-theoretic scaling for a two-layer teacher (data ∝ model size up to logs); power-law learning curves from a Zipf toy model. |
| EI-60 | [Pomerleau, ALVINN](https://proceedings.neurips.cc/paper/1988/hash/812b4ba287f5ee0bc9d43bbf5bbe87fb-Abstract.html); [Bojarski et al., PilotNet](https://arxiv.org/abs/1604.07316); [Radford et al., Whisper](https://arxiv.org/abs/2212.04356) | ALVINN 1,217 → 29 → 46 units; PilotNet about 250k parameters (Fig. 4); Whisper 39M–1,550M (Table 1). |
| EI-61 | Tesla Autonomy Day 2019 captions (EI-37 snapshot) | 01:21:40: LPDDR4-4266, 68 GB/s peak; 32 MB SRAM per accelerator. Vendor statement. |

## Scaling-mechanism sources (2026-10-01)

These support [scaling_mechanisms_findings.md](scaling_mechanisms_findings.md). Full PDFs were read; snapshots are in ignored `out/sources/`.

| ID | Source | Checked locator and use |
|---|---|---|
| EI-62 | [Liu, Liu & Gore, *Superposition Yields Robust Neural Scaling*](https://arxiv.org/abs/2505.10465), NeurIPS 2025, arXiv v4 | Results 1–3; Eq. 5 (overlap bound); Fig. 6b exponent 0.91 ± 0.04; §3.3 `N ∝ m^2.52`; App. A.1 exponent `2(α−1)`; Fig. 16 about `m²/2` strongly represented features. Toy autoencoder plus four open model families. |
| EI-63 | [Liu, Kangaslahti, Liu & Gore, *Inverse Depth Scaling From Most Layers Being Similar*](https://arxiv.org/abs/2602.05970), ICML 2026, arXiv v2 | Eq. 3 decomposition; §2 fit `α_m` 0.98 ± 0.08, `α_ℓ` 1.2 ± 0.3, `α_D` 0.30 ± 0.01 on about 200 Chinchilla points; §4 exponent 3 for smooth targets when converged, 1 for non-smooth; §6 optimum `m ∝ ℓ`, `N^(−1/3)`; App. B `N ≈ 12m²ℓ`. Fitted constants are not printed. |
| EI-64 | [Liu, Liu, Pehlevan & Gore, *Universal One-third Time Scaling in Learning Peaked Distributions*](https://arxiv.org/abs/2602.03685), ICML 2026, arXiv v3 | Eqs. 17–19 derivation under the aligned-student ansatz; Results 1–4; Fig. 6 Pythia; App. D.8 MNIST exponent 0.35; D.9 OLMo. Intermediate regime only; gradient flow. |
| EI-65 | [Ng Chong, *Why AI Scaling Hits a Wall*](https://c3.unu.edu/blog/why-ai-scaling-hits-a-wall), UNU Campus Computing Centre blog, 20 Sep 2026 | Pointer only. Overstates the papers; its cost figures are not in EI-62; its references 8 and 9 could not be found elsewhere. |

**Not inspected, cited only as framing:** Johnson 1958 criteria (classical values 1.0 / 1.4 / 4.0 / 6.4 cycles); LeCun's "cake" slide.

```
79ca39183920efc169e297da18d157400a508d83bdc9c52ff6a47ec059d69c14  1901.02220.pdf
82dc2ad3c5fa6cf79240326ad5303d0cf1b4d3c6ca595d058f51cf04907aa2f8  2404.05405.pdf
ce0148ea694019714c4c3d5d8bb3a09b2f1e7c402f377f9db50cae705e32b123  2505.24832.pdf
b9157d12d63c14176b91a67945c58d34b90d8314a8a921f70d5e20e9f6c8ab07  2303.13506.pdf
4536c546d45f7f2f46f32d4abd120ce061fb1ad8c7164be996e3cf9d964e5500  1804.08838.pdf
c6e9d1f7793ad186a0bbd5deb1e3baf4a56816955ecd6c4fa6c0d3809f137680  1810.04240.pdf
bcd625e89f95c39dc9143af4174978fcf2467eb9659d86f8da448d7d9366c332  2402.17764.pdf
740f66a4055f9297d7725cfaa271a1307aa45dd522fd5cb681a9e566ba6b8342  2404.10102.pdf
d593ad9da8500a3f54f7ae803509126a15a71bdee5059b7303876ef0fea0f304  2408.10234.pdf
4017f54b9b7357d6da491e2edd5c315b75b1d0659c4844e5c06e1ab22a2be20c  2310.07923.pdf
ded7b20b51493258c5ce2a1a024cd33dd752de1fa3373d1207620da4cfe24545  2408.03314.pdf
548cbf81918d9d3a18b0aa57c8a507e8f425bc8338cd4f94da8a63f951ed0654  2403.05812.pdf
fe36c65932b6e7ca78319c95d626d21a1a7836616e5fb1743cc6bac54170483e  alvinn.pdf
c02b15a05434388b443b8f9a89ac37821eec91b9cd305c2c63ffa51fa2fdb123  pilotnet.pdf
6337bde031b2f237547a977b022f831169a7e05b4d9047f29501166d83594566  whisper.pdf
05f39985e65480e89071ef3410ea62de5dfd7538b54ebab8ac70df3bd0fc8204  2211.13609.pdf
716228de2455c069ca121e46d051f80d9ff94bada3b3152b10dcc497c746c5ce  2102.04074.pdf
1704b93d00cde26c1294e1115ad0eddfbdcd90d0640673b3d3612d4ad814b528  nasa_monocular_ranging.pdf
162bf1c6bc1454ee58d81f93a96f9aa507a71cad5f2bbe08d883d02c15f7e772  2505.10465.pdf
c4f46ad5a7736ade4027e0c8508de5908bba5867026e6245690290af86d7d4b8  2602.05970.pdf
f2addbf97db8a75178a1f35657850c0557523694b4453306995bf604344b3dcc  2602.03685.pdf
8192448b946a777061bda9f357958ff36cc09715de4c7075f5537ecdd17380c6  unu_c3_ai_scaling_wall_20260920.html
```
