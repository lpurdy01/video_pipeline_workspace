# Evidence methods for a frozen trained component

Research date: 2026-09-16. This lane examined methods that could support a **bounded assurance case** for a released, versioned learned component. It did not search for, or find, an end-to-end certification decision for a particular model.

## What the evidence methods can establish

| Evidence contract | Selected source and method | What it can support | Assumptions and a defeating counterexample |
|---|---|---|---|
| Operational scope and change control | [C-EVID-001] NIST AI RMF lifecycle documentation | An inspectable record of intended use, knowledge limits, TEVV inputs, recovery and change processes | The RMF is voluntary and supplies no transport-specific acceptance threshold. A well-documented release can still fail in an unrepresented fog, glare or sensor-fault case. |
| Data/training lineage and scenario coverage | [C-EVID-002] combinatorial coverage | Measured coverage of selected factor combinations and a way to expose coverage gaps | Factors, bins and interaction strength are analyst choices. A causal factor omitted from the scenario model can defeat an apparently high coverage result. |
| Scenario/statistical evidence | [C-EVID-003] rare-event importance sampling | A conditional risk estimate for the selected simulator, base distribution and hazard threshold | It depends on simulator fidelity, distribution tails and the threshold. A shifted environment distribution or perception-rendering defect makes the result inapplicable. |
| Uncertainty / ODD exit | [C-EVID-004] confidence calibration | Calibration can be measured and improved on a stated evaluation distribution | Calibration can fail under shift. A camera classifier with well-calibrated clear-day validation confidence can be confidently wrong in glare. |
| Intervention and recovery | [C-EVID-005] Simplex-style formal runtime assurance | A formal safety implication for a black-box advanced component when monitor, timing, dynamics and fallback premises hold | A miss that no independent monitor observes in time prevents the system from reaching the formal recovery condition. |
| Explainability / inspection | [C-EVID-006] saliency randomization checks | A method-specific challenge for whether an explanation depends on model/data structure | An attractive heat map that survives neither model nor label randomization is unsuitable as evidence that the system used the claimed feature. |
| Test-adequacy metrics | [C-EVID-007] neuron-coverage study | A limited empirical association that motivates further testing | The study does not establish causal or consistent relation to hazardous behavior. A high activation/coverage score can coexist with a missed hazard. |

## Recommended minimum evidence for the road encounter

The project should require these linked artifacts for each material hazard before the worked case can call an obligation closed:

1. A frozen model, preprocessing, sensor configuration, training-data lineage and release hash.
2. An ODD and hazard statement that names occlusion, lighting/weather, range/range rate, other-agent behavior, latency and sensor degradation assumptions.
3. A scenario taxonomy with the chosen factors, combinations covered, omitted regions and reason for the selected test distribution.
4. Held-out and shifted-condition results with confusion/error costs tied to the hazard, calibration checks by ODD partition, and a documented response when uncertainty exceeds authority limits.
5. Closed-loop test and simulation evidence that traces a perception error through planning, actuation and outcome; any statistical estimate must preserve the generator, simulator and distribution assumptions.
6. A monitor and recovery argument with observable signals, maximum detection/switching delays, dynamics bounds and a demonstrated safe envelope. If independent observability is absent, that is an open blocker rather than a reason to assume recovery.
7. A release/change protocol: retraining, data, model, sensor, ODD or monitor changes trigger declared re-evaluation, evidence impact analysis and a new release identity.
8. Any interpretability, representation or coverage metric must be attached to a specific safety question and challenged by intervention or predictive-value testing. It cannot serve as a universal safety score.

This is a proposed project acceptance model, synthesized from the cited sources. It is not a standard and does not establish that these artifacts are sufficient for a civil road or aviation approval.

## Contrary evidence and limitations

- More test miles, more examples, neuron coverage, confidence calibration and a visually persuasive explanation all measure something useful under stated conditions. None establishes probability of safe operation on its own.
- Runtime assurance does not dissolve the perception problem: its formal result begins only after assumptions about what the monitor can detect, how fast it reacts and whether recovery remains possible are met.
- The methods evidence is mainly research and voluntary guidance. It should be used to define evidence obligations, not described as a published certification means of compliance.
- `S-EVID-005` has the same title and overlapping NASA authors/topic as canonical `S-010` and contribution `S-METHOD2-003`. The integrator must compare the two NTRS versions and retain one source identity or record an explicit source/region mapping. They are not independent evidence.
