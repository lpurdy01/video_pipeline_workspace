# Assembly, task structure, and a candidate engineering law

**Status:** research hypothesis, 27 September 2026. This note separates inspected research from our extrapolation. It is not a publication claim, an assurance finding, or a validated model-sizing method. See [source leads](source_leads.md) for original sources and inspection scope; see the [interactive prototype](interactive/README.md) for an executable visualization of the proposed relationships.

## Best current guess

For a *specified distribution, loss, architecture family, training recipe, and observation path*, the resources required to reach a target error are governed less by raw sensor size than by the shortest **task-relevant reusable construction** that the learner can discover, the rate at which training exposes its reusable parts and exceptions, and the information the observation/tokenization path preserves. Time and memory then constrain which resource choices can be deployed. This is a hypothesis to test, not a known law.

The distinctive claim worth pursuing is **multiscale task assembly**: estimate reusable structure across a family of primitive units (pixel patches, object tracks, state variables, words, subwords), but score that structure by its ability to predict the *target relation*, not merely to reproduce the observations. This could become a predictor of where empirical scaling curves bend and which tokenization choices are efficient. It must be combined with the geometry of the task distribution and the difficulty of learning the construction with a given optimizer. We have no evidence yet that it predicts a parameter count better than existing task-aware compression or pilot scaling fits.

## What assembly theory gives us

Sharma et al. define an object's assembly index as the minimum number of recursive joining steps from chosen elementary blocks, with constructed subobjects available for reuse. Their ensemble measure also uses copy number: a complex object that recurs is different from a one-off complex object. The choice of primitives and permitted joins is part of the measurement. Their demonstrated application is physical assembly and selection, especially molecules; applying it to perception-action tasks is our extrapolation. [EI-16]

For **strings**, a July 2026 preprint summarizes an exact equivalence between assembly index and the rule count of a smallest straight-line grammar under binary concatenation. That makes a grammar-based estimator a plausible computational proxy in this restricted domain. The result says nothing directly about how many neural weights are needed, nor does a grammar of a video stream describe the correct steering action. The same paper says its string result does not model geometric or thermodynamic construction. [EI-20] Its cited complexity proof needs separate inspection before publication. [EI-21]

The value of assembly theory here is therefore a *design pattern for measurements*: record primitive scale, permitted composition operation, shortest reusable pathways, motif copy counts, and novel residuals. It is not a new universal information lower bound. Critics argue that assembly index overlaps substantially with established compression; the original authors dispute formal equivalence. A further 2026 critique claims the separation from dictionary compression has not been shown. That dispute makes ordinary grammar/MDL/compression baselines mandatory. [EI-17] [EI-18] [EI-22]

| Measured object | What the number can support | What it cannot support alone |
|---|---|---|
| Raw observation assembly | Repeated visual/textual motifs at a declared primitive scale | A bound on policy difficulty or required parameters |
| Paired observation/action assembly | Repetition of labeled examples and transitions | Generalization to unseen combinations or causality |
| Task-conditional grammar plus residual | A candidate description of reusable decision structure and exceptions at a target loss | Proof that a network can learn it efficiently or that its weights are minimal |
| Copy/novelty spectrum by scenario slice | A hypothesis about learning opportunity and evidence gaps | A safety rate or independent encounter count |

The key counterexample is easy: two datasets can have identical sensor sequences and hence identical raw assembly indices, while one task labels each sequence by a simple threshold and another uses an arbitrary random label table. Required learning behavior differs sharply. Any proposed metric that gives these tasks the same complexity has failed the first test. Another counterexample changes patch size and grammar alphabet without changing the physical task; a valid estimator must account for the information lost and the changed representation cost.

## Nearby theories that sharpen the guess

The closest inspected precedent is Michaud et al.'s **quantization model of neural scaling**. It treats performance as the accumulation of learned skills (“quanta”). In its simplified derivation, if skill-use frequencies follow a Zipf law and skills are learned in frequency order with equal capacity cost, the *remaining average loss* follows a power law; extra assumptions map learned skill count to model parameters and useful examples. Their toy experiments and tentative language-model skill-frequency analysis support investigating this mechanism, but the assumptions are not a proven law for visual control. This is a stronger starting point for our copy-number idea: a motif's *task-relevant encounter frequency* may influence whether it is learned. [EI-28]

A second precedent explains some scaling exponents through intrinsic dimension of a smooth data manifold. Sharma and Kaplan derive an approximate exponent relation under a regression-on-manifold model and test it in teacher/student, image and language settings; Bahri et al. distinguish scaling regimes that may have different causes. Those results caution us that **geometric resolution and spectrum** can matter even when grammar length and copy count are fixed. [EI-29] [EI-30]

Thus the proposed descriptor should be a **profile**, not only an MDL number: task-conditional construction cost, skill/motif use frequency, interaction depth, input-manifold geometry or spectrum, observed optimization difficulty, and per-slice loss contribution. Assembly-inspired copy counts may supply one part of that profile. Even a short parity or algorithmic rule can be difficult to learn with a particular architecture and optimizer; shortcut features can make a network learn a different, easier rule than the intended one. “Easy to describe” and “easy to train” are distinct hypotheses to measure. [EI-10] [EI-11]

## A measurable proposal

Let \(u\) define a primitive/tokenization rule, \(q\) an operating-scenario slice, \(D\) the observed training corpus, \(f\) a candidate task model, and \(\ell\) a specified loss. Define a **task description profile** rather than one scalar:

\[
\mathcal K_{u,q}(\epsilon)=\inf_{g}\bigl\{\operatorname{bits}(g)+\operatorname{bits}(r_{D,q}\mid g) : \widehat R_q(g)\le\epsilon\bigr\}. \tag{H1}
\]

Here \(g\) is a compositional grammar or executable model of the observation-history to action/outcome relation; \(r\) codes its exceptions. The coding language, training/evaluation split, and loss constraint must be published. **H1 is our proposed operational proxy** and depends on the chosen code. It is not Kolmogorov complexity, not assembly index itself, and not an architecture-independent lower bound on weights. Repeated motifs, their copy counts, and held-out recombinations should be reported alongside \(\mathcal K\), because a short grammar inferred from one occurrence has poor learning support.

For image patches of side \(u\), a simple input-length estimate is

\[
T_u\approx F\lceil W/u\rceil\lceil H/u\rceil+T_{\rm other}. \tag{H2}
\]

This counts patches, not information. Patch size can shorten sequences while removing small hazards; a larger token may carry more bits and have a harder embedding map. Vision Transformers establish the patch representation; tokenization experiments in language show that minimizing token count by itself need not improve downstream performance. [EI-23] [EI-24]

The **hypothesized** relation to the empirical frontier is deliberately weak:

\[
R_{q,u}(P,D,C)=R^*_{q,u}+\Phi_{q,u}(P,D,C;\mathcal K_{u,q},\text{copies},\text{novelty},\text{architecture}), \tag{H3}
\]

where \(P\) is trainable parameter count, \(D\) distinguishes useful novel exposure from repeats, and \(C\) is training compute. \(\Phi\) must be fitted from pilot runs; neither its exponents nor \(R^*\) can be read directly from assembly index.

A sharper **candidate mechanism** generalizes the skill-frequency idea. For skill or reusable subtask \(k\), let \(p_{k,q}\) be its encounter frequency in slice \(q\), \(D_q\) the independent training encounters in that slice, \(\Delta_{k,q}\) the loss reduction if learned, \(c_k(u)\) a construction/representation cost proxy, and \(\tau_k\) an empirical learning-exposure threshold. Then test whether a fitted learnable set \(S(P,D,C,u)\) obeys a relation of the form

\[
R_{q,u}\approx R^*_{q,u}+\sum_{k\notin S(P,D,C,u)}p_{k,q}\Delta_{k,q}+I_{q,u},
\qquad D_qp_{k,q}\gtrsim\tau_k\text{ for learned }k. \tag{H4}
\]

The interaction term \(I\) acknowledges that tasks can require several skills together and losses need not add. The relation between \(\sum_{k\in S}c_k\) and network parameter count is an unknown **architecture/optimization efficiency** to estimate, not a universal constant. For hazard slices, \(\Delta\) must reflect the specified consequence-sensitive loss and the slice results must remain separate from average risk. This is our extrapolation from the quantization model and assembly intuition, not a result asserted by those authors. [EI-28]

The proposed discovery would be that a task-conditional assembly profile improves *out-of-task prediction* of fitted frontier parameters beyond simpler compression, skill-frequency, manifold-dimension, pilot-only, data-diversity, and sensor-information baselines. A null result would still be useful: assembly may describe reusable history without improving engineering estimates.

## Bounds, forecasts, and limits

The relevant ceilings and floors have different status:

1. **Decision-information floor:** the best policy using observations \(O_u\) has \(R\ge E_o[\min_a E(\ell(a,Y)\mid O_u=o)]\). This is a theorem for the assumed joint distribution. It is normally unknown in a real deployment and changes with tokenization and sensor access. [EI-01]
2. **Finite-family counting floor:** if a task is uniformly selected from \(M\) distinguishable target mappings and *all task-specific information* resides in \(b\)-bit weights, at least \(\log_2 M\) bits, or \(P\ge\log_2 M/b\), are necessary to encode the selection exactly. External memory, prompts, training-set lookup, priors, continuous precision, allowed error, and nonuniform task probabilities change this statement. It is a deliberately weak teaching bound for a synthetic class, not a floor for driving or language.
3. **Empirical model forecast:** fit loss/coverage against \(P,D,C\) within a named family and held-out scenarios, with intervals and tests for scaling breaks. This is the only credible route to a numerical deployment model-size estimate today. [EI-08] [EI-09]
4. **Weight-storage floor:** storing \(P\) weights at \(b\) bits needs \(Pb/8\) bytes before scales, embeddings, runtime state, and caching. A chosen architecture and memory-traffic model can be passed through a roofline estimate \(t\gtrsim\max(F/\text{effective FLOP/s},B/\text{effective byte/s})\); this is an estimate for those assumptions, not a universal latency bound. [EI-25] [EI-26]
5. **Evidence bound:** a performance curve is distinct from evidence that rare hazards have been covered. Scenario-specific tests and confidence bounds remain separate even if a model fits in memory and meets a latency target. [EI-14] [EI-15]

These should be plotted as different layers with different labels. A single “percent of the problem understood” would conceal the assumed distribution and loss. The interactive therefore uses *ordinary and tail-slice coverage under its stated synthetic curve*, plus resource curves. It displays a nominal parameter range only after an anchor performance has been supplied or explicitly accepted as illustrative.

## Worked direction: visual avoidance

Let a camera deliver \(W\times H\) pixels per frame, \(F\) frames per decision, patch side \(u\), a total context budget \(X\), \(Y\) hypothesized task factors, \(Z\) output steps, and deadline \(L\). Add the missing variables: smallest hazard feature that must survive tokenization, scenario distribution and prevalence, independently varied training encounters, motif reuse, target loss per slice, model family, weight precision, effective compute rate, memory capacity, and memory bandwidth.

The processed sequence length \(T_{\rm eff}=\min(T_u,X)\) and an assumed dense-transformer matrix-work estimate \(F_{\rm work}\approx2P(T_{\rm eff}+Z)\) give one compute curve; this omits attention-specific work and model-family variation. Weight storage gives a hard capacity floor for that representation. A declared traffic assumption gives a roofline time estimate. **None of these equations says which action is correct.** Observation ambiguity and task-conditional structure determine the plausible coverage frontier, which must be anchored by experiments. A smaller patch may improve access to tiny hazards while exploding token count and deadline pressure; a larger patch may fit the hardware while imposing an observation ceiling. The feasible region is the intersection of *specific* performance, memory, and timing constraints, with uncertainty shown rather than hidden.

For a known low-dimensional linear system, \(Y\) could be an engineered state, and supplied dynamics replace much representation learning; the model-size curve may collapse relative to the vision case. For language, the primitive and target relation differ entirely, so a numeric curve calibrated on driving should not be transferred. Chaos enters only when physical state uncertainty grows over a prediction horizon; it contributes an observation/feedback constraint, not a parameter-size formula. [EI-03] [EI-12]

## Falsifiable research program

1. **Predefine tasks and primitives.** Use a known linear state-space control task, a compositional symbolic task, and a synthetic visual-avoidance task with controllable rare features. Specify loss, scenario slices and held-out combinations. The synthetic tasks are research probes, not assurance demonstrations.
2. **Measure structure blind to held-out outcomes.** Compute raw grammar/assembly proxies, copy distributions, task-conditional grammar length, residual exception cost, skill-use frequencies, geometric/spectral descriptors, and ordinary compressors at several primitive scales. Report approximation error where exact assembly index is intractable.
3. **Fit and predict.** Train several model sizes, datasets and seeds per architecture, reserve entire scales and composition patterns, fit per-slice curves, and ask whether adding assembly features improves predictive interval coverage and ranking of feasible tokenizers over MDL/compression and pilot-only baselines.
4. **Challenge with matched counterexamples.** Hold raw image sequences fixed while changing the label rule; change motif copy number while holding unique motif set fixed; permute labels; vary patch size across the minimum hazard feature; hide state from the camera while retaining it in the simulator. The proposed predictor should notice target-rule changes and observation loss.
5. **Reject overreach.** If one task-conditional assembly estimate does not predict held-out scale, if a simpler compressor performs as well, or if the inferred minimum is beaten by a structure-aware algorithm, narrow or abandon the claim. Keep a separate record of rare-event evidence and closed-loop failures.

**Best guess today:** assembly theory is most promising as a way to ask *which reusable parts recur at which scale*, especially in paired observation/action histories. The quantifiable bridge to model size is likely an empirically calibrated profile of task-conditional construction, skill frequency, geometric dimension and optimization response, not the original assembly index alone. The immediate product should be an honest explorer of these hypotheses and a protocol for calibrating them, followed by controlled experiments. No current source establishes a universal equation from pixels, assembly index, or parameter count to generalization certainty.
