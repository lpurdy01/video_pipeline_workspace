# Narration evidence and research-gap map

All cited claims below are currently **provisional**. “Supported use” means the proposed line stays inside the claim’s existing scope; it does not state that the claim has passed publication review. Project proposals must remain identified as proposals. This map is intentionally restrictive.

## Section-by-section factual narration map

| Video section | Supported narration proposition | Exact claim IDs | Required spoken/visual qualifier |
|---|---|---|---|
| Hook | A monitor that relies only on the same failed perception output may share the failure it is intended to catch. | [C-016], [C-METHOD2-019] | “In this illustrative shared-input case.” |
| Learned implementation | FAA describes learned implementation as breaking direct lower-level requirement traceability to the learned algorithm. | [C-AUTH-010] | “The FAA’s 2024 roadmap describes…”; never “all traceability is gone.” |
| Frozen release | FAA distinguishes static/frozen learned AI from systems that learn during operation; updated learned versions require assurance treatment. | [C-AUTH-002], [C-AIR2-007] | “Roadmap framing, not a complete means of compliance.” |
| Road operating layers | Texas authorization, California permit categories, California passenger-service conditions, federal inquiry, and learned evidence are different obligations. | [C-ROAD2-001], [C-ROAD2-006], [C-ROAD2-008], [C-ROAD2-014] | State/date/jurisdiction visible; no safety equivalence. |
| Cybercab inquiry | NHTSA opened AQ26002 into process/technical data behind self-certification; it is not a safety finding. | [C-ROAD2-004], [C-ROAD2-005] | Dated “September 2026 inquiry”; “not a finding.” |
| AMLAS | AMLAS is a six-stage public ML-component method; not sufficient alone; primary emphasis is offline supervised learning. | [C-CHAL-006] | “Component lifecycle baseline, not vehicle/aircraft approval.” |
| MAA | UK MAA path is applicant-specific military guidance; fixed supervised models/defined ODD are early recommendations; mitigation remains important. | [C-CHAL-001], [C-CHAL-002] | “UK military, current guidance; not civil approval.” |
| EASA | NPA 2025-07(B) is detailed proposed material; a high-consequence scope boundary needs function allocation to apply. | [C-CHAL-003], [C-CHAL-004] | “Proposed, not final”; no generic “EASA permits/prohibits AI.” |
| Road methods | ISO/PAS 8800 scope includes trained AI models; UL 4600 describes a safety case; NHTSA ADS is voluntary. | [C-AUTH-006], [C-AUTH-007], [C-AUTH-008] | Published/voluntary distinction stays on screen. |
| Scenario coverage | Selected combinatorial coverage exposes selected gaps but does not establish performance/safety probability. | [C-EVID-002] | State selection/taxonomy limitation. |
| Rare event | Simulation estimates selected risk conditional on distribution, simulator and threshold. | [C-EVID-003] | “Conditional estimate,” never “proves probability of safety.” |
| Calibration | Calibration can improve confidence alignment on evaluated settings, not establish system safety after shift. | [C-EVID-004] | State evaluation-distribution limit. |
| Interpretability | Saliency/feature visuals can be unfaithful; neural coverage lacks established causal adequacy meaning in the inspected study. | [C-EVID-006], [C-EVID-007], [C-METHOD2-016], [C-METHOD2-017] | “One research-method limitation”; do not reject all inspection. |
| Formal methods/reduction | Formal NN verification and sparse identification have assumptions and bounded applicability. | [C-METHOD2-013], [C-METHOD2-015] | Name assumptions; do not promise a general certification route. |
| Safety wrapper | Runtime assurance is conditional on observation, timing, recovery state and reversionary controller premises. | [C-EVID-005], [C-METHOD2-001], [C-METHOD2-003] | “Can establish a safety implication under stated premises.” |
| Project architecture | Evidence chain links ODD, sensors, learned behavior, authority, monitor, fallback and change control. | [C-015], [C-METHOD2-018], [C-METHOD2-019] | “This project proposes…” |
| DAA architecture | GA-ASI publicly describes cooperative surveillance plus air-to-air radar for noncooperative traffic. | [C-AIR2-001] | “Vendor-described architecture.” |
| DAA scope | Inspected public material did not establish GA-ASI DAA/ATAR TSO issuance; a TSO is separate from installation/use. | [C-AIR2-003], [C-INTAKE-003], [C-AIR2-004] | “The public sources inspected for this project…” |
| BVLOS scope | Zipline authorization/exemption is scoped operation-specific relief, distinct from DAA-system authorization. | [C-AIR2-012], [C-INTAKE-001], [C-INTAKE-002] | Date/location/scope card. |

## Claims rejected from the planned narration until research completes

| Desired claim | Why it is not currently narratable | Safe replacement line |
|---|---|---|
| “There is no formal method for certifying ML in aerospace or road autonomy.” | Contradicted by the existence of AMLAS, MAA guidance, EASA proposals, and road standards; global negative cannot be proven by the present search. | “The FAA’s 2024 roadmap identified a missing industry method, while existing methods and candidate paths cover different parts of the problem.” [C-AUTH-001] [C-CHAL-006] |
| “Automotive has a lower safety/certification bar than aviation.” | The project has separate-process facts, not a reviewed cross-jurisdiction comparison with a defined “bar.” | “Road and aviation systems use different authorization, compliance, equipment, installation, and operation layers.” [C-ROAD2-014] [C-INTAKE-003] |
| “Manufacturers are allowed to self-certify learned autonomy as safe.” | The project has a dated FMVSS self-certification inquiry, not a generalized learned-model assurance rule. | “NHTSA’s dated inquiry examines a manufacturer self-certification basis; it does not disclose the learned-model evidence.” [C-ROAD2-004] |
| “Standards boards lack experienced people or consensus.” | No source supports the causal sociological claim. | “The current materials show proposed, case-specific, and component-limited approaches; the reason for their maturity level remains an open research question.” |
| “FAA currently permits AI only up to X DAL / forbids Y.” | No authoritative current DAL-to-ML mapping or permission matrix is in the claim set. | “The project needs a function-level safety allocation before relating a hypothetical AI function to a particular authority boundary.” [C-CHAL-004] |
| “Electric vehicles are safer/less safe because of their accident rate.” | No compatible primary numerator/denominator/ODD data in project records; EV and ADS are conflated by the statement. | Omit pending research. |
| “Tesla’s vectors show how it proved safety.” | Public architecture description does not reveal private safety case or Cybercab-specific evidence. | “Tesla publicly describes camera-derived world representations and planning; this project does not infer its assurance evidence.” [C-ROAD2-010] |
| “GA-ASI is the only certified DAA system.” | No exhaustive comparison or precise certification proof supports it. | “The inspected GA-ASI page describes a DAA architecture; product-specific approval scope requires primary records.” [C-AIR2-001] [C-AIR2-003] |

## Candidate research requests triggered by this outline

These are not claims and must be assigned to independent research lanes before use.

1. **Risk/DAL lane:** primary FAA/EASA/RTCA safety-assessment material that can carefully explain failure-condition severity, development assurance allocation, and whether any public trained-model mapping exists. Preserve jurisdiction, status and exact scope.
2. **Road-versus-air authority lane:** a legally careful comparison of US road manufacturer self-certification and aviation approval layers, defining what “barrier” means before comparing them.
3. **Standards maturity lane:** current primary standards-body/authority evidence on AI/ML committees, published versus draft documents, and consensus process. Avoid unverified claims about expertise shortages.
4. **Exposure/risk-statistics lane:** primary crash, exposure and ODD data appropriate to a narrowly defined comparison. Separate EVs, conventional vehicles, ADS modes and human driving; define exposure denominator.
5. **DAA approval lane:** current primary FAA/equipment/installation/aircraft/operation records for any public DAA example. Do not infer an authorization from vendor material or operational press releases.

## Promotion checklist

Before a line becomes production narration:

- its claim ID resolves in the frozen compiler baseline;
- its source status/modifier appears in voice or visual form;
- its picture does not assert more than its wording;
- its exact script line and visual description are added to the artifact manifest;
- fresh `source_support`, `challenge`, and `cross_artifact` review packages are completed for the frozen digest; and
- a human disposition is completed only when the user chooses to begin that stage.
