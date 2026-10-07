# Toward an engineering of intelligence: a research draft

**Status:** exploratory research, 27 September 2026. This is a proposed measurement program, not a discovered universal law, a model-size calculator, or an assurance conclusion. The literature leads and their inspection limits are in [source_leads.md](source_leads.md). The Gemini pass and rejected suggestions are recorded in [gemini_triage.md](gemini_triage.md). A follow-on [assembly and scaling hypothesis](assembly_hypothesis.md), its [Gemini challenge triage](assembly_gemini_triage.md), [cross-domain frontier findings](cross_domain_findings.md), its [focused Gemini limit challenge](frontier_gemini_triage.md), and a standalone [Astro explorer](interactive/README.md) develop the reusable-skill idea without changing this draft’s assurance boundary. The condensed, bits-based synthesis is in [intelligence_budget.md](intelligence_budget.md), with its [Gemini triage](budget_gemini_triage.md). No claim here has been added to the project's verified claim register or to the whitepaper.

## The proposition

The useful question is: **For a specified task, observation path, operating distribution, architecture family, training recipe, and error target, how do data, model capacity, training compute, and inference latency trade off?** A second question asks how much evidence a performance claim needs. These are related, but one curve cannot answer both.

We can draft an *engineering of intelligence* as a set of conditional relationships:

1. **An observation ceiling:** missing task information cannot be recovered by enlarging a model.
2. **A resource frontier:** within a fixed task and model family, error may be forecast from pilot runs at different scales.
3. **A dynamics limit:** in a feedback task, observation timing and prediction horizon matter alongside prediction accuracy.
4. **An evidence limit:** rare failure rates require many relevant independent observations or additional justified structure to bound.

The order matters. A 2-dimensional control output can be hard to infer from video; output dimension does not measure the complexity of the map from observations to action. Likewise, millions of image pixels do not automatically require millions of independent learned concepts. Structure, sensor ambiguity, target loss, and the desired operating range decide what must be learned. The Tesla talk in the attached prior session is a concrete motivation: many visually distinct driving scenes share a routine action, so aggregate action accuracy can reward an uninformative shortcut. Its vendor statements are context, not a parameter-sizing law.

No-free-lunch results reinforce the need to state a task distribution and inductive bias: an algorithm cannot be ranked as best over every possible target relation without assumptions. That mathematical statement does **not** mean useful, model-relative engineering rules are impossible. [EI-19]

## Refinement: capacity ceiling versus attained performance

The limit question asks for the **best achievable** task fitness among allowed models using at most P parameters and a specified compute budget, with task, sensing, operating distribution and data allowance fixed. This frontier is nondecreasing in P by construction because a larger budget still permits a smaller model. A particular trained model may fall below it. Its lower-tail performance across important slices is another quantity again. Better training and implementation can raise attainment without changing the budget; more parameters can raise the achievable ceiling but do not ensure that a release uses it.

For a declared loss, define `Rraw` as minimum risk using raw observations, `Rrepr` as minimum risk after the sensor/token representation, `Rbudget` as minimum risk among models within the P/compute budget, and `Rrelease` as the actual frozen release risk. Nested model sets give an exact ledger: `Rrelease = Rraw + (Rrepr-Rraw) + (Rbudget-Rrepr) + (Rrelease-Rbudget)`. These are respectively irreducible uncertainty, representation loss, budget limitation, and attainment gap. Hardware deadlines restrict the admissible model set rather than adding a separate accuracy term. The middle infima are generally unknown and require bounded experiments or special-case theorems; see the [focused challenge triage](frontier_gemini_triage.md).

The observed best-of-budget curve in the [benchmark atlas](interactive/README.md) is a **lower bound** on this unknown ceiling. To claim a model size could *not* solve the task requires an upper bound on all allowed models under stated assumptions, not merely failed or absent examples. The resource curves below should be interpreted as conditional estimates of an attainable frontier from controlled sweeps, with uncertainty, rather than as a law fitted across unrelated benchmarks.

## 1. Define the task before counting parameters

Let the task contract be

\[
\mathcal T=(\mathcal O,\mathcal A,\mathcal D,\ell,H,\mathcal S,\tau),
\]

where observations \(\mathcal O\) specify sensors and history, actions \(\mathcal A\) specify authority, \(\mathcal D\) is the *stated* operating distribution, \(\ell\) is the consequence-sensitive loss, \(H\) is the decision horizon, \(\mathcal S\) is a set of important encounter slices, and \(\tau\) is the latency deadline. Record changes in illumination, weather, traffic, geography, sensor condition, and hazard prevalence as separate slices rather than one vague “complexity” number.

The first mathematical test is the best decision possible from the specified observations:

\[
R^*(\mathcal O)=\mathbb E_{o}\left[\min_a\mathbb E[\ell(a,Y)\mid O=o]\right]. \tag{1}
\]

Every policy using only \(O\), regardless of model size, has risk at least \(R^*(\mathcal O)\). For ordinary classification with zero-one loss this is \(\mathbb E_o[1-\max_y P(Y=y\mid O=o)]\); for log loss it is conditional entropy \(H(Y\mid O)\). **Conditional entropy is not itself the zero-one error rate.** Equation (1) is a decision-theory lower bound under an assumed joint distribution, not a practical recipe for measuring the unknown true distribution. A hidden aircraft behind an occluder can make two states need different actions despite identical camera histories. More weights cannot disambiguate those histories; an additional sensor, an active observation, a safer fallback, or a narrower operating domain might. The information-bottleneck work formalizes task-relevant compression, but supplies no direct conversion from retained information to neural parameter count. [EI-01] [EI-02]

This already gives a useful answer to “could this model possibly solve it?”: if a defensible observation or actuation lower bound exceeds the target, the *specified system* cannot meet it. If that lower bound is unknown, a negative conclusion from parameter count alone is not justified.

## 2. Representational structure changes the resource need

For known linear dynamics, \(x_{t+1}=Ax_t+Bu_t+w_t\) and \(y_t=Cx_t+v_t\), the engineer can test observability and controllability, estimate a compact state, and use established control synthesis under explicit assumptions. The state dimension and matrix operations give a tractable engineering description; Laplace or state-space methods help because the dynamical structure is supplied. If \(A\) and \(B\) must be learned, finite-sample control results still depend on excitation, noise, uncertainty and closed-loop sensitivity. They do not say that every four-state problem requires a four-unit network. [EI-03]

Vision-to-control and language require discovering much of the useful representation. Three existing ideas are promising **descriptors**, not universal sizing formulas:

| Descriptor | What it can reveal | Boundary |
|---|---|---|
| Task-relevant compression or rate-distortion | Information about an observation that must be retained for the stated decision/loss | Does not determine architecture, trainability, or parameter count [EI-02]. |
| Intrinsic objective dimension | Small random training subspaces can sometimes reach a target score in a larger network | Depends on the task, model, optimization setup, and target score; it is not an intrinsic dimension of all intelligence [EI-04]. |
| Compositional or repeated structure | Local reusable subfunctions can make some high-dimensional functions much cheaper to represent | Approximation results assume a specified function class; they do not prove that training discovers the structure [EI-05]. |

**Proposed complexity description:** for a given task, measure (a) ambiguity left by sensors, (b) reusable/compositional structure, (c) diversity and dependence of useful examples, (d) horizon and feedback sensitivity, and (e) loss concentration in rare slices. These are different axes. A nominally huge but repetitive corpus can contain fewer new constraints than a smaller, carefully varied one. In language-model experiments, modest reuse of data can help under a fixed budget, while further repetition eventually adds diminishing value. In image-classification experiments, selecting informative examples changed the observed data-scaling relation. Neither result transfers unchanged to a driving fleet. [EI-06] [EI-07]

## 3. Fit a local resource frontier

The clearest precedent is empirical neural scaling. For a *fixed* task, evaluation set, model family, data pipeline and training recipe, a candidate fit is

\[
\widehat L(N,D)=E+A N^{-\alpha}+B D^{-\beta}, \tag{2}
\]

where \(N\) is parameter count and \(D\) is **useful distinct training exposure** in a declared unit. The fitted \(E\) is an asymptote in that model of the data; it must not be called a measured Bayes-risk or safety floor. Training compute \(C\), optimizer settings and training duration must also be recorded, and a fitted \(L(N,D,C)\) can be used where the design varies them separately. Hoffmann et al. used a form like (2) for a family of autoregressive language models and showed that a 70B-parameter model trained on more tokens outperformed a 280B-parameter model at similar training compute. Their result shows that attained performance depends on training allocation as well as parameter budget; it does not negate a nondecreasing best-achievable frontier defined with an at-most-P budget. [EI-08]

For learned control, replace one global \(L\) with a **vector** of results: \(L_s(N,D,C)\) for each encounter slice \(s\), plus action latency, calibration, and closed-loop outcomes. The prospective tool should fit a curve only after small pilot runs span both model size and independent data diversity, with multiple seeds. It should reserve the largest pilot scale and shifted scenes as extrapolation tests. If a single power law misses them, allow a break or report “no stable forecast”; research already documents changes of scaling regime. [EI-09]

Resource sizing can then be posed as a conditional optimization:

\[
\min_{N,D,C,\,\text{architecture}}\ \text{development or deployment cost}
\quad\text{subject to}\quad
U_s(N,D,C)\le r_s\ \forall s,\quad
t_{\rm infer}\le\tau . \tag{3}
\]

Here \(U_s\) is a validated **upper uncertainty bound** for the *specified metric and slice*, and \(r_s\) is its target. This is a proposed decision rule, not an established law. If rare-slice samples are too few to estimate \(U_s\), the tool must say “insufficient evidence.” A best observed model size is an engineering forecast **within the tested family**, never a proof that a different architecture, feature set, data policy, or algorithm could not do better. The random-label memorization experiment and underspecification results show why nominal parameter count or ordinary validation loss alone cannot explain generalization. [EI-10] [EI-11]

## 4. Time and feedback introduce different limits

For a chaotic physical process with locally positive Lyapunov exponent \(\lambda\), nearby states can initially separate approximately as \(\delta(t)\approx\delta_0 e^{\lambda t}\). A rough open-loop point-forecast horizon is therefore \(T\approx\log(\delta_{\rm tol}/\delta_0)/\lambda\). This describes sensitivity to state-estimation error **in that dynamical regime**. It is not a formula for neural model size, and regular new observations can change the useful control horizon. Lorenz's original example supplies the physical motivation. [EI-12]

In imitation learning, the policy changes the states it next encounters. Ross et al. show why sequential decisions violate the ordinary independent-sample premise and analyze how errors can compound under particular assumptions. Their bounds are not a prediction that every behavioral-cloning policy will fail quadratically at every horizon. A vision-control estimator must therefore report both open-loop prediction and closed-loop behavior under declared scenario distributions. [EI-13]

## 5. ROC is part of the answer, not the answer

A hazard detector has a threshold curve between true-positive and false-positive rates. Those rates alone do not show how many alerts are real. At hazard prevalence \(\pi\), the positive predictive value is

\[
\mathrm{PPV}=\frac{\mathrm{TPR}\,\pi}
{\mathrm{TPR}\,\pi+\mathrm{FPR}(1-\pi)}. \tag{4}
\]

As an **illustrative calculation**, if \(\pi=0.001\), TPR is 0.99, and FPR is 0.01, then only about 9% of alerts represent the hazard. Whether an alert is harmful depends on the action it triggers. Plot ROC **and** precision-recall at a declared prevalence, calibration, detection delay, and outcome by encounter. The NIST instrument-performance note treats detection and false-alarm rates with confidence bounds; the project must still connect them to the whole system's hazards and recovery. [EI-14]

Suppose a frozen system has zero misses in \(n\) independent, representative **hazard-positive encounters**. A one-sided \(1-\alpha\) binomial upper bound for the conditional miss probability is

\[
p_{\rm miss,upper}=1-\alpha^{1/n}. \tag{5}
\]

At 95% confidence, zero misses in roughly 30,000 relevant encounters are needed before this bound falls below \(10^{-4}\); roughly 3 million are needed for \(10^{-6}\). These are mathematical illustrations under the stated sampling model. Replayed correlated frames do not count as independent encounters, a changed operational domain can invalidate the inference, and even a valid bound on the detector's miss rate is not a bound on collision probability. RAND's driving-exposure analysis shows why rare-event testing by accumulated miles alone becomes expensive. [EI-14] [EI-15]

## A first tool worth building

**Name:** task resource and evidence explorer (working title). Its first version should be a planning instrument, not a safety score.

**Inputs:** task/ODD, sensor and action definitions, loss and hazard slices, horizon, model family, architecture/training recipe, pilot runs by \((N,D,C)\), examples that are genuinely distinct, held-out and shifted evaluations, hardware/latency measurements, and the confidence assumptions for each statistical bound.

**Outputs:** (1) fitted performance curves and holdout error; (2) a range of model/data/compute combinations predicted to meet *specific* ordinary-performance targets within measured scales; (3) per-slice ROC/precision-recall, calibrated error and closed-loop outcome; (4) exact trial counts and confidence bounds for rare-event metrics; (5) explicit “observation-limited,” “compute/latency-limited,” “data-limited,” “model-limited within this family,” or “not enough evidence” findings, each linked to the test that supports it. No aggregate certainty or model-safety score.

**Could a given size have solved it?** Return three separate answers: (i) an actual lower bound if observations or actuation rule it out; (ii) the best measured or forecast performance **within a named family and range**, with uncertainty; and (iii) open alternatives. The second answer is not an impossibility theorem.

**Pilot comparison, before any whitepaper claim:**

1. Known linear system: compare a supplied state-space/LQR baseline with learned policies; vary data and model size while holding the same control objective. This checks whether supplied structure saves resources.
2. Partially observed chaotic forecasting/control example: vary observation history and refresh rate separately from model size; measure open-loop horizon and closed-loop task loss. Avoid treating one fitted Lyapunov exponent as a model-size bound.
3. Small, synthetic visual avoidance task: vary hazard prevalence, scene diversity, and architecture; compare aggregate error with hazard-slice detection and closed-loop violations. Label all toy data and assumptions. A later decision can determine whether a simulator adds value to this assurance project; D-026 currently rules out a runnable toy simulation for the whitepaper.

Pre-register which metric and held-out scale would count as a useful forecast. The hypothesis fails if the fitted frontier misses its held-out scales or scenario shifts by more than its declared interval, or if a structure-aware baseline beats the claimed parameter minimum. If the hazard slice cannot be populated and tested independently, report that the rare-event target is untested.

## Chaos and assembly theory: where each belongs

Chaos is relevant when a task involves sensitive physical dynamics and long open-loop prediction. The useful quantities are state uncertainty, observation cadence, feedback, and consequence of forecast divergence. It does not justify describing language generation as chaotic merely because outputs vary with prompts. [EI-12]

Assembly theory studies the construction and abundance of physical objects. Its relation to algorithmic compression is actively disputed by its authors and critics; neither side supplies an inspected, validated map from assembly index to neural parameters, training examples, or compute for this task. We should retain the broad intuition that reusable substructures can reduce description cost, but use information theory, minimum description length, and compositional approximation as the first mathematical tools. Treat “assembly index predicts model size” as an **unverified research hypothesis** requiring its own experiment, not as a law. A newer string result links a specific assembly index to smallest grammars, and skill-frequency and manifold theories supply closer scaling precedents; see [the follow-on note](assembly_hypothesis.md). [EI-16] [EI-17] [EI-18] [EI-20] [EI-28] [EI-29]

## What would count as a real contribution?

A valuable result would be a calibrated, falsifiable **task-specific resource frontier** that predicts unseen pilot scales and tells engineers when it cannot predict. A stronger result would link a measurable task descriptor (for example, controlled compositional structure or sensor ambiguity) to changes in that frontier across tasks, while preserving the rare-event evidence boundary. A universal parameter count for “solving” arbitrary problems is neither supported by the inspected work nor necessary to make a practical engineering tool.

Before publication, retrieve full text for the lead sources, record source regions and snapshot hashes, challenge the proposed equations against counterexamples, assign formal project source/claim IDs, and decide whether this inquiry belongs in the whitepaper's argument or in a separate follow-on essay. This draft makes no change to the current paper or its review baseline.
