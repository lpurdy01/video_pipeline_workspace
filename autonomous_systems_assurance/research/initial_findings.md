# Initial findings — 2026-09-08

This is a sourced research seed, not a completed literature review or certification opinion. The [register](sources.json) records exactly what was inspected. All associated claims remain provisional pending contextual and independent review.

## A car that takes off

The useful comparison is the chain of perception, prediction, planning and action, followed by the assumptions that make the chain acceptable. The proposed visual transformation should preserve the architecture while exposing changes in geometry, maneuver options, encounter dynamics, sensing and authorization. Which differences dominate remains a research question. [C-015]

## What the GA-ASI page actually establishes

GA-ASI describes radar, cooperative surveillance and collision-avoidance elements. The inspected page still forecasts TSO-C211/C212 authorization in 2025. It does not establish that authorization was issued, that this was the only certified system, or that a neural camera model was certified. Obtain authorization numbers, holder, model and scope before making those statements. [C-001] [GA-ASI product page](https://www.ga-asi.com/detect-and-avoid-system)

FAA distinguishes TSO article authorization from installation/use approval. Separately, the UK MOD's June 2025 publication reports Protector's Military Type Certificate. These are different approval objects and jurisdictions. [C-002] [C-003] [FAA explanation](https://www.faa.gov/aircraft/air_cert/design_approvals/tso) · [MOD publication, printed p. 8](https://assets.publishing.service.gov.uk/media/685bf0de0433072fce0e1001/desider_-_issue_199__June_2025.pdf)

**Open:** inspect actual GA-ASI equipment records and other DAA providers. Failure to find a certificate in this pass is not proof none exists.

## A useful acoustic-perception research branch

FAA's September 2023 announcement authorizes Zipline delivery operations without visual observers around Salt Lake City. Zipline's November account describes flights using onboard perception. This is a concrete operational counterexample to investigate, not evidence of unrestricted DAA equipment certification. Acoustic/ML implementation details and approval conditions still require primary technical material and the underlying letters. [C-004] [FAA announcement](https://www.faa.gov/newsroom/faa-authorizes-zipline-deliver-commercial-packages-beyond-line-sight) · [Zipline account](https://www.zipline.com/newsroom/zipline-achieves-first-u-s-bvlos-flight)

## Cybercab: deployment and self-certification

NHTSA's September 4, 2026 announcement establishes an Audit Query into Tesla's Cybercab FMVSS self-certification after Austin deployment. Its stated focus includes how requirements apply to a vehicle without traditional human controls. This is not a final noncompliance finding. [C-005] [NHTSA](https://www.nhtsa.gov/press-releases/investigation-tesla-cybercab-self-certification)

California separately distinguishes testing with a driver, driverless testing and deployment permits. Do not use those rules to explain Texas operations. ISO/PAS 8800 also supplies a published automotive AI safety scope; operational permissions and engineering standards answer different questions. [C-006] [C-013] [California DMV](https://www.dmv.ca.gov/portal/vehicle-industry-services/autonomous-vehicles/) · [ISO scope](https://www.iso.org/standard/83303.html?browse=tc)

**Open:** primary Texas rules and Tesla authorization, current Waymo permits/ODDs, CPUC passenger-service permissions, and comparable safety-outcome data with exposure denominators.

## Aviation is working on assurance for learning

FAA's 2024 roadmap distinguishes models learned before deployment from systems that learn during operation, and discusses assurance of updated versions. This supports investigating a lifecycle and configuration-control problem rather than presuming a blanket AI ban. [C-007] [FAA roadmap](https://www.faa.gov/aircraft/air_cert/step/roadmap_for_AI_safety_assurance)

EASA's site now lists Proposed Issue 3, dated June 3, 2026. The landing page was inspected; the PDF retrieval failed. EUROCAE's inspected WG-114 page lists an ED-324 draft. Final standard publication/recognition status remains open; target dates are not proof of publication. [C-008] [C-014] [EASA](https://www.easa.europa.eu/en/document-library/general-publications/easa-artificial-intelligence-concept-paper-proposed-issue-3) · [EUROCAE](https://www.eurocae.net/working-group/wg-114-sg-1/)

## A monitor needs evidence too

NASA's runtime-assurance paper studies a monitor transferring authority to a trusted fallback, with recovery and timing conditions. It explicitly does not solve every industrial deployment difficulty. [C-009] [NASA paper](https://shemesh.larc.nasa.gov/fm/papers/DASC2024-SWDMC-draft.pdf)

Our key challenge is observability: if both the learned planner and its monitor receive the same missed-object representation, adding a monitor box may leave the hazard untouched. This is project reasoning to test, not a finding of that paper about a particular product. [C-016]

## Interpreting or simplifying a model

Tesla publicly describes camera-derived world representations and trajectory planning. This is a plausible lead for the video Levi remembers, but we have not identified the exact clip or verified a deployed model version. [C-010] [Tesla technical overview](https://www.tesla.com/AI)

Separate four ideas: visualizing predictions, testing causal mechanisms, compressing/distilling a model, and identifying governing equations. SINDy demonstrates the last under structural and data assumptions; it does not establish that arbitrary perception models reduce to physics. [C-011] [Original research](https://arxiv.org/abs/1509.03580)

A May 2026 landing-model preprint provides a timely interpretability case study. Its abstract proposes representation-based assurance and monitoring. Methods, coverage, failure cases and external validation need review before relying on its stronger assertions. [C-012] [Preprint](https://arxiv.org/abs/2605.20607)
