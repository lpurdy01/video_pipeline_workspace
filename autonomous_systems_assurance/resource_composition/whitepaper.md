# What Would It Take to Trust a Trained Autonomous System?

## A practical assurance architecture, from road perception to airborne detect-and-avoid

**Status:** reader-review draft, 25 September 2026. This paper develops a proposed assurance case for a hypothetical, frozen trained component. It does not assess, certify, authorize, or describe the evidence of a real vehicle, aircraft, model, or company.

## The question

A car approaches a van at the edge of an intersection. The system’s world model says the near lane is clear.

There are two possible worlds. In one, the lane is clear. In the other, a cyclist is hidden behind the van and will enter the lane. If the planner and its safety monitor receive the same “clear lane” state in both worlds, they have no information that lets them choose differently. The planner can execute perfectly and still be wrong about the world.

That is the core problem in this paper. It comes before neural-network accuracy, formal verification, or certification vocabulary: **what lets this machine distinguish the dangerous world early enough to take a safe action?**

A trained model is useful here as a narrow component. It receives a calibrated sequence of camera frames and returns a navigation-relevant cue: candidate image location or bearing, time, and uncertainty or “unknown.” It does not steer the vehicle, establish range from one image, or declare the path clear. Tracking, geometry, planning, a monitor, and a recovery policy turn that cue into an action.

The same cue shape can be used in a road example and an airborne detect-and-avoid example. The releases, data, sensors, target sizes, geometry, and approvals remain separate. Sharing an interface is a teaching device, not a claim that a road model becomes an aircraft model.

![Designed traceability, learned implementation, and the proposed evidence bridge.](figures/learned_traceability_gap.svg)

*Figure 1. Conventional assurance still applies to the surrounding software and hardware. The gap is the direct explanation of learned behavior from lower-level requirements. The green bridge is this project’s proposal.* [C-AUTH-010]

> **About the standards cited.** Several standards named in this paper are copyrighted and were not available to this project in full text. The paper characterizes them only through public regulator, government, standards-body, or open-method material. Claim tags lead to the source record and its access limit.

## 1. The assurance playbook engineers already know

Conventional safety assurance is not a single test. It is a chain of work: identify a hazardous function, allocate it to a system and implementation, define requirements, verify the implementation and its integration, control changes and tools, and give independent reviewers something concrete to inspect.

Public FAA, NASA, and ISO material shows the same engineering grammar in different jurisdictions: validate requirements, verify implementation and integration, control configuration and tools, and preserve a review trail. The named aviation and road standards sit behind those public descriptions; their licensed clause text is outside this project’s access boundary. [C-BASE-001] [C-BASE-002] [C-BASE-003] [C-BASE-004]

The point is not that aviation and road programs use identical documents. It is that engineers already recognize the logic: a program should be able to show what it built, why it built it, how it tested it, what changed, and who challenged the result.

A learned component keeps most of that logic. The surrounding sensors, interfaces, planner, control code, build pipeline, and operating rules still need ordinary engineering. What changes is the link between intended behavior and the learned implementation. The team selects the task, training data, learning process, and frozen release; it does not derive a requirement for each learned weight. FAA’s AI roadmap identifies that break in the usual lower-level requirements explanation. [C-AUTH-010]

The right response is neither “requirements no longer matter” nor “a model score proves the requirement.” It is to add evidence where the direct implementation explanation is weak.

| Familiar assurance question | What changes for learned perception | What the program needs instead |
|---|---|---|
| What hazardous function is allocated? | A cue can influence a maneuver without being the maneuver itself. | An operating domain, hazard, delegated authority, and action limit. |
| What implements the requirement? | Behavior is learned from data and training choices. | Data/task requirements, a release manifest, preprocessing and interface trace. |
| What did testing cover? | A coverage number cannot show which real encounters the data omitted. | Encounter-grouped, shifted-condition, latency and unknown-cue evidence. |
| Does integration preserve safety? | A correct cue can arrive too late for a useful action. | Closed-loop tracker, planner, dynamics, monitor and recovery traces. |
| What changed? | Data, weights, sensor mounting, export or quantization can alter behavior. | Exact release identity, change impact, and repeated affected evidence. |
| Can we trust the tools and review? | Training, labeling, simulation and deployment tools shape the evaluated function. | A tool-influence argument and independent review of the deployed artifact. |

This table is the paper’s central proposal. It is not a substitute standard. It gives a manager and an engineer a way to ask what must exist before a trained cue may influence a hazardous action.

## 2. Start with the information problem

The cyclist case makes the distinction concrete. Suppose the camera cannot distinguish an empty lane from a cyclist hidden behind a van before the last recoverable moment. A larger training set cannot add pixels that were never observed. A deterministic monitor that sees only the same failed perception state adds no new information.

The design must change one of four things: the observation path, the speed or operating envelope, the authority delegated to the cue, or the recovery plan. This is why a safety monitor is not a decorative box. Runtime-assurance results depend on what the monitor observes, when it detects a problem, how quickly control changes, the vehicle dynamics, and whether a recovery state remains reachable. [C-EVID-005]

![A shared vision cue with separate road and airborne releases and evidence.](figures/vision_training_contract.svg)

*Figure 2. Road and air share a small cue interface, not a model, dataset, or approval. The red boundary is physical: an unobservable object cannot be recovered by stronger training alone.* [C-TRAIN-001] [C-TRAIN-003]

The completed Tempe investigation provides a useful warning against a component-only story. NTSB reports that the developmental automated driving system detected the pedestrian 5.6 seconds before impact and identifies inadequate safety-risk assessment procedures among the contributing factors. The teaching point is bounded: detection, system response, authority allocation, and safety management belong in one trace. This paper does not infer unreported details about that system’s classifier, tracker, or braking logic. [C-BASE-005]

For the hypothetical road release, the useful question is therefore not “what is the detector’s accuracy?” It is: **in this kind of encounter, with this sensing configuration and speed, does a cue arrive early enough for the complete system to make a safe response?**

That question also explains why an occluded cyclist is a SOTIF-relevant example. ISO’s public description of ISO 21448 frames SOTIF around unreasonable risk from functional insufficiencies in safety-relevant situational awareness from complex sensors and processing algorithms. A fault-oriented functional-safety lifecycle, AI-element safety work, and a goal-based autonomy safety case each cover different parts of the road stack. None supplies the missing evidence for this particular perception release. [C-METHOD2-011] [C-BASE-004] [C-AUTH-006] [C-AUTH-007]

## 3. Build a program someone can run

The assurance case becomes useful when it produces recognizable artifacts and review gates. The following lifecycle is a project proposal. AMLAS is the learned-component lifecycle reference; the familiar plan, requirement, verification, configuration, and tool analogues come from the public conventional baseline. [C-CHAL-006] [C-BASE-001] [C-BASE-002] [C-BASE-003]

| Phase | Artifact the team produces | Gate question |
|---|---|---|
| 1. Safety assessment and allocation | Hazard, ODD, authority statement, recovery margin | What decision may the cue influence, and where? |
| 2. ML requirements and ODD | Cue definition, “unknown” policy, data requirements | What has to be visible early enough? |
| 3. Data management | Data manifest, label policy, encounter-grouped splits | Does the evidence represent the claimed encounter classes? |
| 4. Model learning | Candidate log, frozen weights, training configuration | What exactly is the release candidate? |
| 5. Deployment transform | Export, compiler, quantization and installed-artifact manifest | Did we test the same function that will run? |
| 6. Independent evaluation | Partitioned misses, false alarms, delay and uncertainty results | Does performance support the stated authority limit? |
| 7. Closed-loop integration | Tracker/planner/dynamics/monitor and recovery traces | After an error, is a safe state still reachable? |
| 8. Operation and change | Change-impact record and release decision | Which evidence must be repeated after a change? |

This lifecycle gives the project’s eight evidence obligations one canonical home: scope and authority; observability; lineage; hazard-relevant performance; closed-loop behavior; intervention and recovery; composition; and change control. The paper stays with the plain-language gate questions; the assurance graph carries the IDs.

Two details matter especially to software teams. First, verification sets must be independent in the ways that matter: adjacent frames from the same encounter should not make a test set look broader than it is. Second, the evaluated network and the deployed network must be the same released function. Export, compilation, quantization, sensor preprocessing, and configuration are part of the identity of the case.

AMLAS gives useful component-level discipline for data requirements, model learning, independent verification, and deployment. It explicitly limits itself to the ML component and focuses primarily on offline supervised learning. The hypothetical case deliberately starts with a frozen versioned release; an update creates a new assurance problem rather than inheriting the old result. [C-CHAL-006] [C-AUTH-002] [C-TRAIN-001] [C-TRAIN-003]

## 4. Where the standards landscape helps—and stops

There is no assurance vacuum. There is also no single public document that closes the complete road-to-air case.

AMLAS supplies a public learned-component lifecycle. The UK Military Aviation Authority supplies an applicant-specific military path that uses a **Military Certification Review Item (MCRI)** and recommends fixed supervised models in a defined operating domain for early safety-related applications. EASA material offers detailed candidate objectives, but the relevant civil material is proposed rather than a final approval path. These are useful inputs to a program; they are different kinds of input. [C-CHAL-001] [C-CHAL-003] [C-CHAL-004] [C-CHAL-006]

The dated status matters. EUROCAE’s WG-114 page, captured 16 September 2026, lists ED-324 as a draft with a target publication date of 31 December 2026. Its public page does not establish technical contents, publication, FAA recognition, or use on a specific program. EASA’s NPA 2025-07 was the first planned step of RMT.0742, and EASA said a second NPA was planned to apply the framework to aviation-domain rules; the captured rulemaking status still labels DS.AI proposed and awaiting comment responses. [C-CHAL-005] [C-STD-002]

For an engineer, the practical reading is simple:

- Use a published method to structure work, while keeping its scope visible.
- Bring a regulator or authority into the loop for the actual certification basis and allocated function.
- Do not call a draft, a proposal, an operating permission, or an equipment authorization a complete learned-model safety case.
- Keep online learning out of the first argument unless the program can make a new assurance case for how it changes.

The public gaps are therefore program questions, not excuses to wait: how is perception performance connected to the hazard? what tools influence the installed function? what can the monitor see independently? how is change controlled? These questions are active precisely because a project cannot answer them with a document title alone. [C-STD-001] [C-AUTH-003] [C-EVID-005]

## 5. What each method can contribute

Methods are valuable when they answer a particular question in the lifecycle.

| Method | Good use | Boundary |
|---|---|---|
| Scenario taxonomy and combinatorial coverage | Shows which selected encounter factors were exercised. | It cannot reveal a causal factor the taxonomy omitted. [C-EVID-002] |
| Rare-event simulation | Estimates a stated event under a stated generator, simulator and threshold. | It does not automatically transfer to a changed sensor or tail distribution. [C-EVID-003] |
| Calibration | Connects uncertainty to an authority restriction on an evaluated partition. | It does not establish calibration after shift. [C-EVID-004] |
| Runtime monitoring | Supports a conditional switch to recovery. | It cannot rescue an unobservable or too-late failure. [C-EVID-005] |
| Interpretability and neuron coverage | Challenge a story and suggest new tests. | Neither is a causal proof of safe behavior. [C-EVID-006] [C-EVID-007] |

The pattern is consistent: a method can strengthen one edge of an argument. It should not be promoted into the whole argument.

![Questions that turn a broad trust claim into a reviewable release decision.](figures/evidence_bridge_ladder.svg)

*Figure 3. The evidence bridge is a project proposal. It groups the lifecycle questions above; it is not an authority checklist or a safety score.*

## 6. Let the vehicle take off

Now keep the cue shape and change the world. A non-cooperative glider appears as a small dark cluster against broken terrain. The camera can flag a possible bearing, but the aircraft cannot safely turn on that pixel cluster alone: it still needs a usable track, range/range rate, traffic context, maneuver clearance, and enough separation margin to act. The airborne release has separate training data, sensor configuration, and frozen identity.

The surface analogy is useful because it exposes what must change. A road case asks about occlusion, braking, steering and the safe stopping envelope. An air case asks about target size, closing rate, background clutter, cooperative and noncooperative traffic, tracking, airspace, and maneuver/separation margin. A landing or diversion can be a later contingency; it is not an immediate collision-avoidance response.

| Same assurance question | Road | Air |
|---|---|---|
| What must become observable? | A road actor and its likely conflict with the route. | An aircraft, usable track, and enough information for separation. |
| What is the last useful action? | Braking, steering, or a controlled minimum-risk response. | Alerting or maneuvering while preserving traffic and terrain clearance. |
| What is a dangerous shortcut? | Treating late detection as a safe detection. | Treating bearing-only cue or later landing as an escape path. |
| What must be separately argued? | Vehicle compliance, operation, and learned-component evidence. | Equipment, installation, aircraft, operation, and learned-component evidence. |

The road result cannot authorize flight. The value of the comparison is harsher and more useful: it forces every assumption that road intuition hides into view. The air case has its own data, frozen release, tracking, action authority, and evidence. MAA and EASA material can help describe the landscape, but neither closes this hypothetical high-consequence case. [C-CHAL-001] [C-CHAL-003] [C-CHAL-004]

## 7. What a team should do next

A team does not need to wait for a perfect standard before doing disciplined work. It can begin with a bounded function and make the argument inspectable.

1. Pick one hazardous decision and write the authority limit before selecting a model.
2. State which world difference must be observed, by which path, before the last recoverable action.
3. Freeze the release identity: data, labels, training choices, weights, preprocessing, deployment transform, sensors, and downstream interfaces.
4. Evaluate encounter groups, error delay, uncertainty, and closed-loop recovery—not just an aggregate score.
5. Give an independent reviewer permission to challenge the sensor path, the data split, the simulator, the monitor premise, and the change record.
6. Treat a material change as a new release until the affected evidence is repeated.

The four levers are the real conclusion: improve the observation path; narrow the speed and operating envelope; reduce delegated authority; or provide a recovery action that remains useful in time. A release earns more authority only when evidence supports those levers together.

The compiler is a supporting notebook for that work. It can show which sources, assumptions, and tests changed; it cannot create the missing observation, data, test, or recovery evidence.

The question to keep is the opening one: **what exactly lets this machine take this action, here, now—and what evidence would prove us wrong?**

## Continue in the technical reference

The main paper is deliberately optimized for the first read. [The technical reference](technical_reference.md) preserves the detailed methods, the full eight-contract case, risk and probability discussion, source-status distinctions, compiler/review model, source cards, and review agenda. It is the place to inspect the complete argument or use it as a project resource; it is not a discarded appendix.

## Appendix A. What this draft does and does not claim

This is a proposed architecture for a frozen trained component. It does not determine whether any named vehicle, aircraft, DAA product, or model meets a regulatory standard. It does not infer proprietary evidence from deployment and does not provide legal or certification advice. Online learning, a final ED-324 publication status, EU/UNECE road-regime scope, a runnable toy simulation, and the final video format remain separate decisions or research work.

## Appendix B. Primary reading links

- [FAA roadmap for AI safety assurance](https://www.faa.gov/aircraft/air_cert/step/roadmap_for_AI_safety_assurance) — learned-implementation framing and frozen-versus-updated release distinction. `[C-AUTH-002] [C-AUTH-010]`
- [AMLAS v1.1, University of York](https://www.york.ac.uk/media/assuring-autonomy/documents/AMLASv1.1.pdf) — learned-component lifecycle. `[C-CHAL-006]`
- [EASA NPA 2025-07(B)](https://www.easa.europa.eu/en/downloads/142701/en) — proposed DS.AI material and scope. `[C-CHAL-003] [C-CHAL-004]`
- [NTSB Tempe investigation](https://www-s.ntsb.gov/investigations/Pages/HWY18MH010.aspx) — completed investigation used for the bounded system-trace teaching point. `[C-BASE-005]`
- [FAA AC 20-115D](https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-115D.pdf) and [AC 20-174](https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-174.pdf) — public conventional assurance framing. `[C-BASE-001] [C-BASE-003]`
