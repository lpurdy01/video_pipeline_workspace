# Next steps: assurance for frozen learned systems

Status: active project direction, 2026-09-15. This is a research and architecture plan, not a proposed certification standard.

## The project claim to investigate

The project should ask: **what evidence contracts could support a bounded claim that a frozen, trained perception or decision component may participate in a safety-critical autonomous system?**

This is narrower and more useful than asking whether “AI is safe.” A trained model has a versioned training corpus, pipeline, weights, hardware/software configuration and release boundary. It may still fail because the world, sensors, surrounding actors and system integration differ from its evidence. A system that learns after release creates additional change-control and operational-validation obligations; retain it as a contrast case rather than smuggling it into the first worked example.

The likely paper conclusion is not that conventional assurance has been replaced, nor that there is no work in this area. AMLAS already provides a public six-stage learned-component methodology; the UK MAA provides current case-specific military guidance; and EASA has proposed a detailed civil AI-trustworthiness lifecycle. The research must compare their status, scope and evidence boundaries with road standards, runtime assurance and the worked system case. [C-CHAL-001] [C-CHAL-003] [C-CHAL-006]

If the final audit finds no public end-to-end method that meets the project criteria, the allowed wording is: **“we found no publicly inspectable end-to-end method meeting these stated criteria, as of the recorded search date.”** It is not “no method exists.”

## Design decision: evidence contracts, not a safety score

A fleet-mile count, a benchmark score, a neural-network explanation, or a calibration metric can all be useful evidence. None is a universal probability of safety. Each hides assumptions about scenario frequency, data representativeness, independence, distribution shift, vehicle dynamics and the meaning of a harmful outcome.

The working architecture therefore needs the following contracts for each material hazard and operating-domain claim:

| Contract | Question it must answer | Example failure it must expose |
|---|---|---|
| Operating scope and authority | What may the trained component decide, in which ODD, with what time and maneuver margin? | The model is given authority in a scene outside its defined conditions. |
| Data, training and release lineage | Which version of data, labels, split policy, training process, weights and deployment transformation produced this release? | An unrecorded relabeling or export change invalidates the result. |
| Scenario and statistical evidence | Which hazard-relevant scenarios were covered, how were they sampled, and what does the evidence bound under stated assumptions? | Many routine miles conceal a rare, decisive false negative. |
| Perception uncertainty and ODD exit | How are detection limits, uncertainty, disagreement, latency and out-of-distribution conditions represented and acted upon? | A confident miss is indistinguishable from an empty scene. |
| Closed-loop composition | Given imperfect world state, what can planner, controller and vehicle dynamics safely do before the last recoverable state? | A correct detection arrives too late for the available maneuver. |
| Independent intervention and recovery | What does a monitor observe, which failures are shared, and when can it actually recover or restrict operation? | A monitor receives the same missing-object output as the learned planner. |
| Change and operational control | What changes trigger renewed evidence, and what field observations can reveal violated assumptions? | A retrained model or changed camera is treated as a no-impact update. |
| Claim-specific analysis | Where can formal analysis, interpretability, minimization or system identification add discriminating evidence? | An explanation looks plausible but does not predict behavior under intervention. |

The last contract is deliberately conditional. Interpretability may help diagnose or challenge a learned component, and formal analysis may prove stated properties over stated models and input sets. Neither becomes an assurance substitute until its causal relation to the safety claim is demonstrated.

## State-of-art position after research wave one

The current source inventory rejects both “conventional process only” and “no process at all.” It now includes an inspectable ML-component lifecycle (AMLAS), a current case-specific military path, proposed EASA material, road-vehicle safety specifications and safety cases, runtime-assurance research, and actual aviation/road authorization records. Their status and scope differ. [C-CHAL-001] [C-CHAL-003] [C-CHAL-006] [C-AUTH-006] [C-AUTH-007]

The first research pass must classify each source as one of: binding requirement, accepted means of compliance, proposed guidance, voluntary consensus standard, research result, vendor assertion, or authorization for a specified operation. It must also state whether it covers a trained component, the whole vehicle/system, a particular operational domain, or merely a process concept. A road operating authorization and an aviation equipment authorization must never be represented as proof of the safety of an unrestricted learned model.

The comparison baseline is [AMLAS](https://www.york.ac.uk/media/assuring-autonomy/documents/AMLASv1.1.pdf), the [FAA AI safety-assurance roadmap](https://www.faa.gov/aircraft/air_cert/step/roadmap_for_AI_safety_assurance), [ISO/PAS 8800:2024](https://www.iso.org/standard/83303.html), [UL 4600](https://www.ul.com/news/ul-4600-edition-3-updates-incorporate-autonomous-trucking), the [UK MAA AI notice](https://assets.publishing.service.gov.uk/media/68f0b97c1c9076042263ef2a/MAA_RN_2025_04.pdf), and EASA's [NPA 2025-07(B)](https://www.easa.europa.eu/en/downloads/142701/en). Full standard text and clause-level mappings require lawful access and must remain separate from public redistribution.

## Immediate research wave — completed

The authority/standards, evidence-method and adversarial-challenge jobs have completed. Their contributions remain provisional and must receive source-support, challenge, cross-artifact and human-disposition reviews before publication. The adversarial result changed the thesis: the project will compare and operationalise existing methods instead of portraying its evidence contracts as the first lifecycle.

1. **Authority and standards map.** Inspect FAA, EASA, road-vehicle and selected UK authority material. For every candidate, record publisher, edition/date, jurisdiction, document status, subject, trained-versus-in-service learning scope, and exact safety claim supported. Obtain clause text where access permits; otherwise record the access boundary.
2. **Evidence-method map.** Inspect primary research and authoritative guidance on data provenance, scenario coverage, statistical claims, uncertainty/calibration, robustness, formal verification, runtime assurance, interpretability and model simplification. Translate each method into one of the contracts above, its assumptions and a counterexample.
3. **Independent gap challenge.** Search specifically for public, end-to-end assurance cases or accepted certification means for high-criticality frozen learned components. Challenge the planned thesis with commercial systems, aviation approvals, standards that combine the full lifecycle, and evidence that mileage or a metric can validly close a stated hazard. Record failed searches as failed searches, not absence proof.

The next completion condition is an artefact-level crosswalk from AMLAS, MAA and EASA material to the eight evidence contracts, with a status label and adverse-review note for every consequential conclusion. It must make unmatched external objectives and unmatched project obligations explicit. Only then may the paper state the scoped result: mature methods exist, while the searched public material has not closed the hardest high-criticality civil case.

## Worked-case and compiler milestones

After the research wave, instantiate one car encounter: a partially occluded conflict in which a trained perception model either detects late, misses, or reports uncertainty. Carry the same abstraction into an aircraft encounter. For each case, add explicit nodes for the hazard, ODD assumptions, learned-model release, evidence contracts, tests/analyses, monitor observations, recovery limits and claim uses.

The compiler now loads versioned `hazard`, `assumption`, `obligation`, `evidence_artifact`, and `system_release` nodes from the hypothetical road case. Links answer which hazard a claim addresses, which assumption limits its validity, which release it concerns, and which downstream artifact must be reviewed if a node changes. It reports defined releases, open assumptions, planned evidence and open obligations as separate blockers; it does not calculate a composite safety score. The next extension is to ingest an inspected external method's named artifacts/objectives into this graph rather than maintaining that crosswalk only in prose.

Once that graph works for the single road-to-air case, the composition and video lanes can proceed in parallel: the paper explains the contracts and their limits; the video reveals the architecture in the first 20 seconds, follows the car encounter, then asks what changes when it takes off. Tesla may illustrate public uncertainty about operating evidence, but does not supply the architecture or evidence claims.

## Decision gates

| Gate | Required evidence | Resulting action |
|---|---|---|
| Public-process finding | Audited authority/standards matrix and challenge search | State the bounded state-of-art finding; do not claim universal absence. |
| Worked-case adequacy | Every material hazard has linked assumptions, evidence contracts and an open/closed disposition | Draft the assurance case and its defeating traces. |
| Compiler adequacy | New node types, change impact and blockers demonstrated on the worked case | Pin a review baseline for paper and video authors. |
| Publication adequacy | Primary-source review, independent challenge, human dispositions and cross-artifact review | Release the whitepaper/video/resource package only with remaining gaps visible. |
