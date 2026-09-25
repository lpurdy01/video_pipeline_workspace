# Risk, criticality, and evaluation evidence

**Lane:** `risk_evidence`  
**As of:** 2026-09-22  
**Question:** What can conventional aviation risk practice, current FAA/EASA AI material, DAA metrics, and learned-model evaluation plots actually establish?

## The usable distinction

A safety argument starts by asking what could go wrong, how severe the outcome would be, and how the system prevents or limits it. A performance report starts by asking how often a model gets labels or detections right on a chosen test set. They connect, but they are not the same thing.

FAA's conventional airplane system-safety guidance expresses a familiar relationship: as the consequence of a failure rises, its allowable likelihood falls. It combines failure analysis, engineering judgment, test evidence, and sometimes numerical probability analysis. The document also warns that failure-rate data are imprecise and that a single failure normally cannot simply be called extremely improbable. [C-RISK-001]

That framework is useful as a **shape of the question**, not a ready-made calculation for a trained perception model. A camera miss is conditional on scene geometry, glare, weather, sensor condition, preprocessing, model version, human/monitor behavior, and the following control action. A model's held-out accuracy is not a component failure rate.

## What current aviation AI material actually says

The FAA roadmap offers a constructive bridge, rather than a blanket prohibition. It describes DALs as a way to scale scrutiny from the system-safety assessment, encourages an incremental safety continuum, and says existing software and complex-hardware guidance is inadequate for learned AI implementations. [C-RISK-002] The roadmap is not itself an approval basis or a table authorizing particular learned flight functions.

EASA's proposed DS.AI is a more detailed candidate structure. It uses operational scenarios, severity and likelihood categories, documented operating domain, and defined allocations of authority. Its limits matter: the proposal excludes AI whose risk directly contributes to fatalities or multiple life-threatening injuries, excludes specified higher-contribution online-learning cases, and calls H1 fatality potential unacceptable at this time. [C-RISK-003] This is a scope statement for a proposal, not evidence that all higher-criticality aviation AI is categorically prohibited.

Together, these records support a careful video/paper message: **the public methods are becoming more concrete, but their authority and criticality boundaries are still explicit, scoped and evolving.** They do not support “there is no method” or “AI is already certified to fly an aircraft by itself.”

## Risk numbers need an argument around them

The UK CAA's DAA consultation response makes the limitation concrete. It describes NMAC and DAA-well-clear metrics, risk ratios and encounter sets, then acknowledges that risk ratios are averaging functions that can hide particular bad encounters. It says that losses of well-clear or NMAC events in the mitigated encounter should be investigated. [C-RISK-004]

For the paper's assurance graph, retain these separately:

1. **Severity:** What happens if the model misses, falsely detects, delays, or misclassifies?
2. **Exposure and scenario distribution:** Which encounters, weather, geometry, traffic behavior and sensor states are represented—and which are not?
3. **Observed model performance:** Confusion matrices, detection latency, calibration and error slices by operating-domain partition.
4. **System response:** The authority granted to the model, monitor coverage, takeover/recovery timing and safe-state assumptions.
5. **Residual risk judgment:** A bounded conclusion tied to the evidence above, rather than a single model-confidence or test-mile number.

The CAA evidence is especially helpful for a visual “graph of trade-offs.” Do not draw reliability, certainty and safety as axes that collapse to one score. Draw them as distinct evidence branches that meet at a hazard/operational claim. A high hit rate can coexist with unacceptable false alarms; a low average risk ratio can conceal a rare bad encounter; a calibrated score can be wrong when the operating distribution changes.

## How to use the supplied medical-evaluation figure

The supplied image is AMLAS Figure 11. AMLAS uses it to explain ROC curves, a threshold-dependent hit-rate/false-alarm trade-off, and confusion matrices that reveal *which* classes are confused. It explicitly notes that misclassification costs differ and that the right choice is a contextual judgment using multiple criteria. [C-RISK-005]

It is a good **teaching pattern** for the video:

- An ROC curve says what happens as a threshold moves; it does not select the threshold.
- A confusion matrix shows the error types hidden by an aggregate score.
- A safety argument must connect each consequential error type to a hazard, time margin, fallback and operating-domain assumption.

It is not evidence about cars, aviation, detect-and-avoid performance, or any individual company's system. Do not show the clinicians as a benchmark for autonomous systems without retaining the original AMLAS credit and making this limitation explicit.

## Electric-car accident-rate check

This lane did **not** find a current official, exposure-normalized electric-vehicle versus internal-combustion-vehicle accident-rate source suitable for a broad safety comparison. NHTSA's 2016 quiet-car final-rule material is a narrowly scoped pedestrian/pedalcyclist rulemaking and stated that it could not directly measure per-mile rates for hybrids and EVs because it did not have the needed vehicle-miles-traveled data. The direct NHTSA PDF returned HTTP 403 to this lane's retrieval attempt on 2026-09-22; it is therefore not a compiler source record and must not be cited in the paper yet.

That finding is not evidence that no usable modern dataset exists. It is a stop sign for an easy but weak narration line such as “electric cars have a lower/higher accident rate.” Any future comparison needs, at minimum, defined vehicle populations, exposure denominator, model years, geography, road mix, driver population, crash severity, automation state, confidence interval and a disclosed treatment of reporting differences. An electric powertrain is also not a proxy for a learned driving system.

## Proposed paper/video use

1. Start the risk section with a hazard, not a number: *“If the perception system is wrong here, what is the vehicle still allowed to do?”*
2. Show the conventional severity–likelihood curve as historical context, labeled as a system-safety framework rather than an ML score. [C-RISK-001]
3. Show FAA's incremental/DAL starting point next to EASA's proposed authority/scope boundary. [C-RISK-002] [C-RISK-003]
4. Use a ROC/confusion-matrix mini-example to make threshold choice intuitive, then show why the assurance graph retains encounter and recovery evidence. [C-RISK-005] [C-RISK-004]
5. Keep any road-fatality or EV comparison in a separately sourced context box until a valid exposure-normalized primary dataset is acquired.

## Open retrieval and research tasks

- Acquire a current, citable NHTSA/DOE source with a defensible exposure denominator before including any electric-versus-conventional crash-rate comparison.
- Retrieve and inspect the current FAA certification-basis guidance for the actual target aircraft class; AC 25.1309-1A is historical context, not a substitute.
- Refresh EASA NPA status and inspect the eventual decision/final DS.AI material before any publication assertion.
- Retrieve CAP3015 version 2 and the accepted means of compliance/guidance material before describing UK DAA requirements as final.
- Map the project’s road and airborne encounters to concrete severity, scenario, authority, monitor and recovery nodes. A numerical threshold belongs only after those objects and assumptions are fixed.
