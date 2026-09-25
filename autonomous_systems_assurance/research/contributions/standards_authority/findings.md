# Standards and authority status — research handoff

**Lane:** standards_authority  
**As of:** 2026-09-22  
**Question tested:** Do aerospace and highway regulators have a finished, public method for showing that a frozen trained ML component in a safety-critical autonomous system is safe, and what exactly does road-vehicle manufacturer self-certification mean?

## Finding

The evidence supports a narrower, more useful opening than “there are no methods.”

There are real methods, standards and authority pathways:

- AMLAS is a public six-stage assurance methodology for an **ML component**, primarily offline supervised learning, and explicitly says it needs complementary system/domain assurance. [C-CHAL-006]
- The FAA’s 2024 roadmap calls the industry-method problem open, proposes incremental experience and consensus-standard development, and identifies research and project-specific paths. [C-AUTH-001] [C-AUTH-003]
- EASA has issued detailed candidate AI objectives, but its DS.AI material remains proposed. The captured EASA rulemaking-status page still labels RMT.0742 / NPA 2025-07(B) “awaiting responses to comments.” [C-AUTH-005] [C-STD-002]
- Road-vehicle work includes ISO/PAS 8800 and a new SAE AI/ML V&V information report; public scope alone does not make either a federal approval or an inspected vehicle assurance case. [C-AUTH-006] [C-STD-005]

What the public record inspected here does **not** demonstrate is a single, final, publicly inspectable civil lifecycle accepted for the hardest case: a high-criticality, trained component with broad perception/planning authority, a bounded operational domain, quantified residual risk, change control, and a public approval decision. That is a finding about the inspected public record, not proof that no applicant has a confidential method or that no authority can approve a particular project.

## Audit of the proposed video deductions

| Proposed deduction | What the sources support | What to avoid saying |
|---|---|---|
| “Aerospace does not yet have a formal certified process for trained ML components.” | FAA Version I says the industry lacks a method for AI safety assurance and lays out a method-development roadmap. EASA's detailed DS.AI is proposed rather than a final AMC/GM. [C-AUTH-001] [C-STD-002] | “No formal process exists anywhere.” AMLAS, EASA's candidate framework, FAA project-specific work and nonpublic applicant material are counterexamples to that blanket language. |
| “Automotive has a lower barrier because manufacturers self-certify.” | U.S. manufacturers certify compliance with **applicable FMVSS**; NHTSA says it does not pre-approve new vehicles or ADS technology. [C-STD-003] [C-STD-004] | “Manufacturers self-certify that the AI is safe” or “self-certification means no safety obligation.” The statutory obligation is FMVSS compliance; defect authority and other obligations still matter. |
| “The lack of clear guidance is glaring.” | NHTSA's ADS guidance is voluntary and its self-assessments are not federal approvals. SAE J3321's public scope calls it non-mandatory. These support a story of a fragmented, evolving guidance landscape. [C-AUTH-008] [C-STD-005] | “There are no standards.” ISO/PAS 8800, UL 4600, SAE J3321, and other documents exist with different legal status and scope. |
| “AMLAS was an attempt.” | AMLAS is a developed public research methodology, not merely a discarded attempt. Its defined limitation is that it addresses the ML component and should not be used alone. [C-CHAL-006] | “AMLAS failed” or “AMLAS is certification guidance.” The project should use it as a component-lifecycle baseline. |
| “FAA is starting committees.” | FAA says it is collaborating with standards-development organizations and the roadmap commits it to participate in consensus-standard development. [C-STD-001] [C-AUTH-001] | A claim that a named committee has failed, lacks members, or has reached no consensus unless a current committee record substantiates it. |
| “The field lacks mathematical rigor and experienced people.” | This lane found no authority source supporting either causal claim. FAA distinguishes theoretical ML research from aviation safety-assurance work, but does not diagnose a shortage of qualified people. [C-STD-001] | Claiming the reason standards are unfinished is a talent shortage, or that trained inference is inherently random. Formal/numerical methods and bounded verification are active topics, with limits that need their own evidence. |

## Authority status in plain language

### U.S. civil aviation: FAA

The FAA's current AI/ML discipline page says its aviation work is about measuring AI functionality and performance within the certification framework. It says FAA leadership collaborates with industry, government, standards-development organizations and academia. That demonstrates active coordination; it does not demonstrate that a final high-criticality learned-component method exists. [C-STD-001]

The FAA roadmap is the stronger historical statement of the gap. It calls the roadmap a living document, proposes scaling assurance to risk and developing consensus standards, and describes project-specific issue papers. Its three-to-five-year “might be possible” timing language is a 2024 forecast, not a current deadline or evidence of failure. [C-AUTH-001] [C-AUTH-003]

**Video use:** Say: “The FAA itself called the method unfinished, then set out a path: start where the risk is lower, build evidence, and turn repeated lessons into standards.” Do not say the FAA has no process at all.

### EASA: detailed proposal, still a proposal

EASA Issue 02 and Proposed Issue 03 already give the project valuable lifecycle material, including learning assurance and configuration/life-cycle data. They also explicitly disclaim being a complete, binding set of means of compliance. [C-AUTH-004] [C-AUTH-005]

The current CRT capture gives the project a status check: RMT.0742's NPA 2025-07(B), “DS.AI,” is shown as a proposed detailed-specification/AMC/GM package that is awaiting responses to comments. That makes it inaccurate to present DS.AI as final published AMC/GM today. [C-STD-002]

**Video use:** Show DS.AI as the closest public blueprint for civil aviation AI assurance, with a “proposed / still in rulemaking” status label. The paper should retain the captured date beside the label.

### U.S. road vehicles: self-certification is narrower than it sounds

The legal requirement is concrete: at delivery, the manufacturer or distributor must certify that the vehicle/equipment complies with **applicable** federal motor-vehicle safety standards. The issuer may not certify if it has reason to know, while exercising reasonable care, that the certificate is materially false or misleading. [C-STD-003]

NHTSA's 2025 interpretation explains the architecture in agency terms: NHTSA does not pre-approve a new vehicle, equipment item or ADS technology; ADS are not prohibited if applicable FMVSS are met and there is no safety defect; manufacturers self-certify. The letter itself is nonbinding and answers a particular lighting/ADAS question. [C-STD-004]

This does not convert a vehicle launch, state operating authorization, voluntary safety self-assessment, or investigation outcome into a conclusion about how a trained perception model was validated. The video should draw a clean three-way distinction:

1. **Product compliance:** the manufacturer’s FMVSS certification and NHTSA oversight.
2. **Operating permission:** state testing/deployment or passenger-service authority.
3. **Assurance evidence:** the scenario, sensor, model-release, monitor and recovery evidence needed to support a specific safety claim.

### Standards are emerging, with different roles

SAE’s new J3321_202603 demonstrates that the road-vehicle community has a current AI/ML V&V document. Its public page also says it is an information report with no mandatory requirements and general methods. This is useful counterevidence against a “nothing exists” hook, while leaving open the question of a rigorous, accepted high-criticality method. [C-STD-005]

The project should make a visual **status ladder**, not a winner-take-all table:

| Layer | Examples | What it can contribute | What it cannot prove by itself |
|---|---|---|---|
| Law and regulation | 49 U.S.C. § 30115; applicable FMVSS; aviation airworthiness rules | Who must comply, and which legal obligations apply | That a trained model handles every scene safely |
| Authority guidance / rulemaking | FAA roadmap; EASA DS.AI | Candidate evidence objectives and a path toward harmonization | A final product approval when guidance is proposed/nonbinding |
| Consensus / research methods | AMLAS; ISO/PAS 8800; UL 4600; SAE J3321 | Lifecycle vocabulary, evidence patterns and review questions | Regulatory acceptance or a product-specific evidence case |
| Product assurance case | A vehicle/aircraft applicant's controlled evidence | The claimed ODD, hazards, performance limits, monitors and releases | General safety outside the declared claim |

## Implications for the whitepaper and video structure

The broad scope requested by the user now has a defensible first three sections:

1. **The traceability break.** Conventional systems can explain lower-level design decisions; learned weights do not map cleanly back to requirements. Start with the FAA’s framing and immediately show the evidence bridge. [C-AUTH-010]
2. **The standards map.** Explain the four layers above, then position AMLAS as a component method, EASA DS.AI as a detailed proposal, FAA as an incremental roadmap, and road standards as complementary, differently binding artifacts.
3. **Why “approval” is not one thing.** Animate the separate product-compliance, operational-permission and assurance-evidence tracks for the same driverless car. This prevents the Tesla hook from carrying more technical meaning than it has.

Only after that setup should the video turn to probability, DAL/risk allocation, perception error tradeoffs and the proposed deterministic safety shell around learned capability. Those sections require their own source record; neither self-certification nor an AMLAS diagram determines an acceptable false-negative rate.

## Retrieval and source-quality record

| Source | Native snapshot | Status | Publication use |
|---|---:|---|---|
| FAA AI/ML technical-discipline page | Yes | Full page and text context retained | Eligible for source-support review |
| EASA CRT RMT.0742 status page | Yes | Full page and text context retained | Eligible for source-support review; refresh before publication |
| 49 U.S.C. § 30115 | Yes | Full current preliminary U.S. Code page and text context retained | Eligible for source-support review |
| NHTSA 2025 interpretation | No | Browser inspection completed; direct snapshot retrieval returned HTTP 403 | Context/retrieval blocker; recapture before release |
| SAE J3321 product page | No | Browser inspection completed; direct snapshot retrieval timed out | Context/retrieval blocker; recapture or obtain authorized copy before release |

## Direct primary links

- [FAA AI/ML technical discipline](https://www.faa.gov/aircraft/air_cert/step/disciplines/artificial_intelligence)
- [FAA AI Safety Assurance Roadmap](https://www.faa.gov/aircraft/air_cert/step/roadmap_for_AI_safety_assurance)
- [EASA CRT: RMT.0742 / NPA 2025-07](https://hub.easa.europa.eu/crt/docs/by_npa_ref/dir_1/dpp_50)
- [49 U.S.C. § 30115](https://uscode.house.gov/view.xhtml?edition=prelim&num=0&req=granuleid%3AUSC-prelim-title49-section30115)
- [NHTSA 2025 interpretation](https://www.nhtsa.gov/interpretations/ncc-230607-001-571108-automatic-activation-hazard-warning-signal-nonresponsive)
- [SAE J3321_202603 public scope](https://saemobilus.sae.org/standards/j3321_202603-verification-validation-ai-ml-based-systems-ground-vehicles)

