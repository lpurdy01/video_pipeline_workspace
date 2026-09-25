# Initial detailed script outline — 34-minute evidence-first video

**Status:** first long-form outline. Narration is not locked. Claim tags are mandatory for factual lines and point to provisional project claims. Bracketed production notes are project proposals, not statements about a real system.

## 0. Cold open — 00:00–01:10

**Picture:** A clean street grid. A car sees lanes, static objects, and predicted paths as translucent vector layers. An occluded cyclist exists behind a delivery van, absent from the system’s world model. The system selects “continue.” A monitor receives the same world model and displays “clear.” Freeze.

**Narration draft:**

> This car has a trained model of the world. It sees lanes, cars, motion, and a clear path ahead. But there are two possible worlds in this frame. In one, the lane really is clear. In the other, a cyclist is hidden behind that van.  
>  
> If the planner and its safety monitor receive the same incomplete picture, they can make the same decision in both worlds. The code can be perfectly deterministic. It still cannot react to information that never arrived. [C-016]  
>  
> That is the safety problem we need to solve before this car ever takes off.

**Source/status card:** “Illustrative shared-input failure case — project reasoning, not a reconstruction of a real vehicle.” [C-016]

**Beat purpose:** Show mechanism before title. Do not say that all learned systems have this failure.

## 1. Title and question — 01:10–02:30

**Picture:** The street grid resolves into an evidence graph. Labels appear: *What can it see? What may it decide? What catches failure? What changes when the model changes?*

**Narration draft:**

> The question is not whether a neural network is mysterious in principle. The question is much more practical: what evidence would let this exact trained system take this exact action in a stated environment?  
>  
> Cars are already being operated through a patchwork of road rules, permits, manufacturer compliance obligations, and service requirements. Aircraft have their own layers: equipment, installation, aircraft, and operating approval. Those layers matter. But none of them, by themselves, tells us what a trained perception model will do in every dangerous corner of the world. [C-ROAD2-014] [C-INTAKE-003]

**Transition:** Zoom from “clear path” label down to a line of model weights, then up to a conventional requirement diagram.

## 2. Designed versus learned implementation — 02:30–06:30

**Picture:** Split-screen diagram, used slowly:

- left: aircraft/vehicle need → system requirement → item requirement → designed code/hardware;
- center: requirement → training objective/data/process → learned weights, with the missing direct requirement-to-weight arrows visibly cut;
- right: proposed evidence bridge joins hazard, domain, sensors, release, scenario, monitor, recovery, and change.

**Narration draft:**

> In conventional engineering, teams build downward. A vehicle need becomes a system requirement. A system requirement becomes an item requirement. The implementation can be explained against those requirements.  
>  
> A trained model changes one part of that story. Engineers still choose its job. They still design the sensors, interfaces, compute platform, conventional software, and operating limits. But they do not write a requirement for each learned weight. The FAA describes that as a break in the direct lower-level traceability used to explain a designed implementation. [C-AUTH-010]  
>  
> This does not make ordinary engineering disappear. It means that a requirement-to-code story is incomplete for behavior that was learned from data. The model can be frozen and exactly versioned, but still encounter an occlusion, sensor fault, or condition the development evidence did not cover.  
>  
> Our first case is deliberately narrower than a system that learns on the road or in the air. It is a frozen trained release: fixed weights, preprocessing, sensors, decision logic, and operating assumptions. The FAA distinguishes that from a system that continues learning in operation, and says an updated learned version needs its own safety-assurance treatment. [C-AUTH-002]

**On-screen distinction:**

| Not the claim | The actual claim |
|---|---|
| “AI cannot be traced.” | Direct requirement-to-weight explanation is incomplete for learned implementation. [C-AUTH-010] |
| “Training makes deployed execution random.” | Frozen trained releases are distinguished from online learning. [C-AUTH-002] |
| “Conventional assurance no longer matters.” | Conventional system/software/hardware assurance remains part of the surrounding system. [C-AUTH-010] |

**Review concern:** The third line is a bounded paraphrase of FAA framing. Retain a source card and do not overextend it into a general regulation claim.

## 3. What does “allowed to operate” mean? — 06:30–10:30

**Picture:** Four nested but non-substitutable cards for a hypothetical road vehicle:

1. state commercial-operation authorization;
2. testing/deployment permission;
3. passenger-service permission;
4. federal vehicle-compliance oversight;

Fifth card floats beside them: **learned-system evidence**. It cannot be replaced by any other card.

**Narration draft:**

> It is tempting to treat “allowed on the road” as the answer to a safety question. It is not one answer. It is several different questions.  
>  
> In Texas, qualifying commercial automated vehicles require an active authorization under the current program. California separates testing with a driver, driverless testing, and deployment permits. California passenger service adds another layer through the CPUC. [C-ROAD2-001] [C-ROAD2-006] [C-ROAD2-008]  
>  
> Federal vehicle compliance is another layer. In September 2026, NHTSA opened an audit query into the process and technical data behind Tesla Cybercab’s self-certification. That is an inquiry, not a finding that the product is unsafe or noncompliant. [C-ROAD2-004] [C-ROAD2-005]  
>  
> The useful lesson is not about one company. An authorization, a permit, a passenger-service program, a compliance inquiry, and evidence for learned behavior must remain separate objects. Otherwise a visible permission label gets mistaken for proof that every perception, planning, and update question has been answered. [C-ROAD2-014]

**Hard stop card:** “Do not infer proprietary model evidence from permits, deployments, or an inquiry.”

## 4. Existing methods: real structure, different boundaries — 10:30–16:00

**Picture:** A landscape table transitions from six AMLAS lifecycle steps to the project’s eight evidence contracts. MAA and EASA overlay only the areas they address; grey regions label *outside scope*, *case-specific*, or *proposed*.

**Narration draft:**

> The absence of one final answer does not mean there is no structure. There is a serious body of work. But it does not all answer the same question.  
>  
> AMLAS is a public six-stage method for assurance of machine-learning components: scope the safety problem, state requirements, manage data, learn the model, verify it, and deploy it. It is valuable precisely because it does not pretend to close the entire vehicle or aircraft safety case by itself. AMLAS says it is for the ML component, should not be used alone, and focuses mainly on offline supervised learning. [C-CHAL-006]  
>  
> The UK Military Aviation Authority has a current, applicant-specific path. For early safety-related ML applications, it recommends fixed supervised models in a defined operating domain and calls for architectural mitigation when a prescriptive solution is not available. That is military guidance, not a civil approval path. [C-CHAL-001] [C-CHAL-002]  
>  
> EASA’s NPA 2025-07(B) goes further in detail: operational domain, risk assessment, development assurance, learning assurance, lifecycle data, and in-service monitoring. But it is proposed material, not final guidance. It also has a high-consequence scope boundary that a real aircraft function would need a system-level failure-condition allocation to interpret. [C-CHAL-003] [C-CHAL-004]  
>  
> On the road side, ISO/PAS 8800’s public scope includes trained AI models and safety-assurance claims. UL 4600 describes a goal-based safety case for autonomous products. NHTSA’s public ADS material is voluntary guidance, not federal approval. [C-AUTH-006] [C-AUTH-007] [C-AUTH-008]  
>  
> The important disagreement is often not a fight over whether safety matters. It is scope. Is the method about the learned component, the whole system, an applicant-specific military case, a proposed civil framework, a voluntary automotive argument, or a real approval? The answer changes what evidence remains open.

**On-screen source-strip format:** Every document card permanently shows one of: **published method**, **current military guidance**, **proposed civil material**, **public standard scope**, **voluntary guidance**.

**Do not narrate:** “there are no standards,” “EASA allows/disallows AI generally,” “AMLAS certifies systems,” or “an MAA path applies to FAA certification.”

## 5. What probability can and cannot say — 16:00–21:30

**Picture:** A risk ledger replaces a score dial. Inputs are pinned beside the calculated output: scenario distribution, simulator, hazard definition, sensor model, release, ODD. Pull one pin and the confidence band becomes a question mark.

**Narration draft:**

> This is where the conversation often collapses into one demand: how many miles, how much accuracy, what probability of failure? Those are useful questions. But they do not stay meaningful after their assumptions are removed.  
>  
> A scenario-coverage method can show which selected combinations of conditions were exercised. It cannot prove that the analyst chose every factor that matters, or that coverage alone establishes performance. [C-EVID-002]  
>  
> Rare-event simulation can estimate a selected risk under a stated traffic distribution, simulator, and hazard threshold. That is powerful. It is not an unconditional property of the model that transfers automatically to a changed sensor, weather model, or tail distribution. [C-EVID-003]  
>  
> Calibration asks whether a model’s stated confidence matched observed frequency on an evaluation distribution. It can support a rule such as slow down, seek another observation, or limit authority when confidence is poor. But calibrated confidence is not the same as hazard awareness after an unfamiliar shift. [C-EVID-004]  
>  
> And looking inside the model is not a shortcut. Saliency images can look persuasive without faithfully explaining the behavior that matters. Neuron coverage can be a diagnostic, but the evidence here does not establish it as a causal safety measure. [C-EVID-006] [C-EVID-007]  
>  
> Formal verification and model reduction are also valuable, but only when their plant, abstraction, data, and model assumptions match the claim we need to make. [C-METHOD2-013] [C-METHOD2-015]

**Visual micro-demo:** Show the supplied medical-model evaluation figure only as a **general visual grammar reference**, never as evidence for autonomous driving or aviation. The actual video should recreate a generic model-versus-expert comparison with invented labels, or license/use a relevant source figure after rights and source review. Do not use the image as an autonomous-system result.

**Research card, no narration assertion:** “DAL mapping, acceptance thresholds, and road/EV accident-rate comparisons require new authoritative sources and a defined denominator.”

## 6. The safety shells — 21:30–27:30

**Picture:** The car stack appears as nested shells. The learned component is in the center. Each shell grows in only after the viewer hears what it must establish. At 24:30, an occluded-actor trace enters through the sensor shell and tests whether the monitor shell has an independent-enough observation path.

**Narration draft:**

> Here is the constructive design move. Do not ask a trained component to carry the entire safety claim alone. Give it a bounded job, then make each surrounding layer earn its place.  
>  
> First: a declared operating domain and a hazard definition. Second: evidence about what the sensing system can and cannot observe. Third: an exact model release, including data, training, preprocessing, weights, interfaces, and sensor configuration.  
>  
> Then come authority limits. A learned perception output may influence a decision, but the planner and conventional controller can be constrained by speed, geometry, time, and vehicle dynamics. A monitor may intervene. A recovery controller may take over. Every model or sensor update reopens the affected evidence. [C-015] [C-METHOD2-018]  
>  
> This is related to a Simplex runtime-assurance pattern: an advanced component operates while a monitor can transfer control to a trusted controller. But the proof is conditional. The monitor must observe the relevant condition soon enough. The switch must finish within a bound. The recovery controller must still have a reachable safe state. [C-METHOD2-001] [C-METHOD2-003] [C-EVID-005]  
>  
> Now bring back the hidden cyclist. If the learned perception, planner, and monitor all inherit the same missed observation, the outer boxes may be deterministic and still be blind. A safety wrapper cannot manufacture the missing fact. The architecture needs another adequate observation path, a restriction that preserves recovery margin, or less authority for the learned component. [C-016] [C-METHOD2-019]

**Mini-sequence:** A “reliability / certainty / safety” triangle appears, then is rejected as a score. It transforms into three linked questions:

- **Reliability:** how often, in which scenario partition, did this component behave as specified?
- **Uncertainty:** what does the system know about the limits of this observation right now?
- **Safety:** given the hazard, time and control margin, is the allowed action acceptable under the declared assumptions?

These are presentation definitions for the project, not regulatory definitions or interchangeable metrics. No composite triangle score is shown.

## 7. The car takes off — 27:30–32:00

**Picture:** The nested-shell diagram stays fixed while the road surface falls away. Each shell receives a flight-specific label. The road vehicle becomes a small aircraft meeting a noncooperative intruder. A five-stage time bar animates: detection/track → alert/decision → authority switch → maneuver → remaining separation.

**Narration draft:**

> Now keep the architecture, and change the world. The vehicle needs to detect another aircraft early enough to alert, maneuver, or otherwise preserve separation.  
>  
> The road problem did not simply become “harder.” Its assumptions changed. Instead of stopping distance, we have closing rate and separation margin. Instead of one road geometry, we have airspace, traffic cooperation, range, background clutter, weather, and maneuver limits. A landing may be a contingency later; it is not an immediate answer to a collision encounter. [C-015]  
>  
> The same questions remain: what can the sensors see, when does a track become usable, what action authority is justified, what can the monitor independently observe, and when is recovery still possible?  
>  
> Publicly, GA-ASI describes a DAA architecture that combines cooperative surveillance sources with an air-to-air radar for noncooperative traffic. That tells us something about a described architecture, not that a particular configuration, installation, aircraft, operation, or learned component has closed every assurance question. [C-AIR2-001]  
>  
> The inspected public pages did not establish issuance of a GA-ASI DAA/ATAR TSO authorization. And even an FAA TSO is not installation or operational approval. [C-AIR2-003] [C-INTAKE-003]  
>  
> The same scope discipline applies to BVLOS permissions. A scoped authorization can show that a particular operation was permitted. It does not disclose an unrestricted learned-perception assurance case or an equipment authorization. [C-AIR2-012] [C-INTAKE-001]

**Review concern:** Avoid calling any DAA system “the only certified system.” Existing project claims do not establish that comparison.

## 8. Final proposal and call to inspect — 32:00–34:00

**Picture:** The eight contracts appear as a live graph. A sensor change turns affected edge(s) amber; a new model hash creates a new release node; the monitor premise becomes an open question. No percentage displays.

**Narration draft:**

> A trained autonomous system does not become safe because we attach a permit, a standard, a monitor, a thousand test miles, or an interpretability picture. Each may contribute evidence. None is a substitute for the others.  
>  
> The practical proposal is an evidence graph. Start with a hazardous decision. Bind it to the operating domain, sensing limits, exact release, scenario evidence, control margin, monitor premise, recovery behavior, and change history. If a link is missing, reduce authority, restrict the domain, or block the release. [C-015] [C-METHOD2-018]  
>  
> That does not certify a car or an aircraft. It gives engineers, reviewers, and authorities a better question to challenge: what exactly lets this machine take this action, here, now—and what evidence would prove us wrong?  
>  
> The whitepaper and source library make the current argument inspectable. The open edges are part of the result.

**End-screen restraint:** Keep the graph moving while the paper/resource link appears. Do not use a verbal “wrapping up” cue before the final question.

## Approximate runtime and drafting budget

| Section | Time | Intended spoken words at 135 wpm | Script state |
|---|---:|---:|---|
| Cold open + question | 2:30 | 338 | Drafted beats |
| Learned implementation | 4:00 | 540 | Drafted beats |
| Permission stack | 4:00 | 540 | Drafted beats |
| Standards landscape | 5:30 | 743 | Drafted beats |
| Risk evidence | 5:30 | 743 | Drafted beats |
| Safety shells | 6:00 | 810 | Drafted beats |
| Road-to-air transfer | 4:30 | 608 | Drafted beats |
| Ending | 2:00 | 270 | Drafted beats |
| **Total** | **34:00** | **4,590** | Full prose script still required |

The current draft excerpts are intentionally shorter than the final word budget. The unfilled time belongs to visual pauses, plain-language examples, source-status cards, and later scripted transitions—not unsupported detail.
