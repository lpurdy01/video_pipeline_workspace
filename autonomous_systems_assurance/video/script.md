# Can We Build a Safety Case for a Machine That Learned?

**Status:** recording-feedback draft, 25 September 2026.  This is a narrated research proposal, not an assessment of a real vehicle, aircraft, product, operator, or model.

**Target:** about 31–33 minutes with visual holds at roughly 125–135 spoken words per minute.  Bracketed directions are not spoken. Every factual narration line carries a source claim tag. Lines marked **Project proposal** are the authors' proposed architecture and must not be read as authority guidance.

**How to review with a voice recording:** read a section naturally, including its transitions, then stop at its `FEEDBACK PAUSE`. Notes on pace, unclear terms, claims that need a source card, and visual ideas can be attached to the timecode or section title. Human audio remains local; this draft can change without changing the source record.

---

## 1. The missing object — 00:00–02:00

[Visual: a road scene becomes a simplified vector world model. A delivery van hides a cyclist. The planner, the monitor, and the display all receive the same green “clear lane” state. Freeze before the title.]

Imagine a car approaching a van at the edge of an intersection. It has cameras, radar, and software that turns sensor readings into a model of the world. It sees lanes, parked vehicles, moving traffic, and a clear path forward.

But there are two possible worlds in this image. In one, the near lane really is clear. In the other, a cyclist is hidden behind the van and will enter the lane. The planner receives the same world model in both cases. So does the safety monitor.

In this illustrative shared-input case, a monitor that relies only on the same failed perception output can share the failure it is supposed to catch. A deterministic planner may execute its logic exactly as designed, yet have no information that tells it to choose differently. [C-016] [C-METHOD2-019]

That is the point of this film. The question is not whether a neural network is magic, or whether ordinary engineering has stopped working. The question is: **what evidence would let this exact trained system take this exact action in this stated environment?**

[Title card: *Can We Build a Safety Case for a Machine That Learned?*]

We will start on the road because the picture is familiar. Then we will let the same visual task take off: find an unexpected object near the planned route and give navigation a timed, uncertain cue. The road model and the air model would need separate training and evidence. The physical details change. The assurance question does not disappear.

**FEEDBACK PAUSE 1:** Does the opening make the information problem clear before it introduces standards or certification?

## 2. Why learned implementation changes the assurance task — 02:00–04:45

[Visual: three columns labelled Designed implementation, Learned implementation, Evidence bridge.]

Conventional safety engineering has a familiar downward path. A vehicle or aircraft need becomes a system requirement. The system requirement becomes an item requirement. Engineers design software and hardware that implement those lower-level requirements. They can explain why the implementation satisfies the requirement above it.

A trained model changes one important part of that story. Engineers still choose its job. They still design the sensors, the compute platform, the interfaces, the surrounding control software, and the operating limits. But they do not write a requirement for each learned weight in a neural network.

The FAA's AI safety-assurance roadmap identifies this as the distinctive problem. For learned implementation, the designer cannot derive lower-level requirements that directly describe the learned algorithm, or validate those requirements by showing their usual coverage of the requirement above them. [C-AUTH-010]

That does not mean requirements disappear. It does not mean a trained model is beyond all analysis. And it does not mean conventional software and hardware assurance no longer matter. It means that a requirement-to-code explanation is incomplete for the behavior encoded by learned weights. [C-AUTH-010]

[Visual: the direct requirement-to-weight arrow breaks; a green bridge appears from hazard, domain, data, release, evaluation, monitor, recovery, and change control.]

The constructive response in this project is not to pretend that every weight needs a requirement. It is to build an evidence bridge around the hazardous decision. What is the operating domain? What can the sensors distinguish? Which exact trained release is running? Which dangerous cases were evaluated? What happens after a late or wrong answer? Who or what can intervene? And what changes reopen the argument?

This first proposal is deliberately limited to a frozen, versioned trained release: identified weights, preprocessing, sensors, decision logic, and operating assumptions. The FAA distinguishes that from a system that continues learning in operation, and says an updated learned version needs safety-assurance treatment. [C-AUTH-002]

Training may have been stochastic. That does not mean a frozen deployed release executes randomly. It does mean that the release needs a different kind of behavioral evidence than a line-by-line implementation story.

**FEEDBACK PAUSE 2:** Are “trained release,” “weight,” and “evidence bridge” understandable here without a longer definition?

## 3. Train one vision cue, then try to break it — 04:45–09:00

[Visual: a cyclist appears from behind a van. The image dissolves into a distant aircraft against terrain. A single green interface card stays on screen: “candidate location or bearing + time + uncertainty/unknown.” Separate road and air dataset cards remain distinct.]

Let's make the learned job simple. Give a camera model a short run of frames. Ask it to flag a possible object or unusual region near the route, say where it appears in the image, attach a time, and say when it is unsure. On the road that might be a cyclist partly visible behind a van. In the air it might be another aircraft, tiny against the sky or terrain.

The model is not being asked to steer the car or turn the aircraft. It supplies a **navigation cue**. Other parts of the system still have to estimate motion and clearance, decide what action is permitted, and show that there is time to act. A single picture does not establish range or collision course. And one road-trained model does not simply become an airworthy aircraft detector by changing the label on its output.

[Visual: the common cue flows into two different tracking and action paths. Then the image peels back to reveal training data, labels, model choices and tests.]

How do we create even that small cue responsibly? This is where AMLAS gets interesting. Its ML component process asks for data requirements tied to the real operating domain. Are images taken from the camera angle that will actually be installed? Do they cover the lighting and backgrounds we expect? Are partly hidden objects labeled consistently? Is a supposedly balanced dataset still missing the rare conditions that matter? [C-TRAIN-001]

The trained model has its own engineering traps. Too simple, and it may fail on both familiar and unseen images: underfitting. Too tuned to the development images, and it may look excellent there while failing on a new road, a new sky, or a different camera: overfitting. AMLAS even gives a case where a model can latch onto an artifact of simulated hazardous images instead of the hazard itself. The standard textbook sketch of model capacity shows the underfit and overfit patterns; neither diagnosis can be made from one accuracy number. [C-TRAIN-002] [C-TRAIN-004]

[Visual: two curves. One is high error on both train and held-out scenes; the other is low train error and high held-out error. A third card says “good score, wrong cue?” and shows the model looking at a simulator watermark instead of the object.]

Then there is leakage. If near-identical frames from the same encounter land in both training and verification, a held-out score can flatter the model. If engineers keep tuning after seeing the final challenge cases, they may learn those examples rather than the wider failure class. AMLAS calls for separate development and verification data and for sufficiently independent verification activity. It asks the verification side to look for realistic ways the model may fail. [C-TRAIN-002] [C-TRAIN-003]

For our example, we would group frames by encounter or capture campaign, write a policy for ambiguous labels, log model and threshold choices, and keep an independent challenge set. We would examine misses, false alarms and **delay** for partial occlusion, small targets, glare, blur, changing backgrounds and unfamiliar objects. Those are proposed tests for this case, not a list that AMLAS certifies as sufficient.

One boundary matters most: if the object cannot be distinguished in the available image before the last safe action, no larger training set can add the missing pixels. The case must change the sensor path, speed, operational domain or authority. A good detector score cannot erase that physical limit.

[Visual: the training pipeline stops at a red “no distinguishing signal” gate; the green action envelope shrinks instead of pretending the model will guess correctly.]

**FEEDBACK PAUSE 3:** Does this training sequence make the learned-component engineering challenges concrete without suggesting that a held-out score proves safety?

## 4. Permission is not proof — 09:00–11:30

[Visual: five separate cards: road authorization, deployment permit, passenger service, federal vehicle compliance, learned-system evidence. None nests inside another.]

When people see an autonomous vehicle operating on a public road, it is natural to ask: if it is allowed to operate, has it been proven safe? The practical answer is that “allowed” covers several different questions.

In Texas, qualifying commercial automated vehicles require an active authorization under the current program. California distinguishes testing with a driver, driverless testing, and deployment permits. California passenger service adds another layer through the Public Utilities Commission. [C-ROAD2-001] [C-ROAD2-006] [C-ROAD2-008]

Federal vehicle compliance is another layer. In the United States, a manufacturer or distributor certifies that a vehicle or item of equipment complies with applicable Federal Motor Vehicle Safety Standards, subject to a reasonable-care constraint. [C-STD-003] NHTSA also says in a nonbinding interpretation that it does not pre-approve new vehicles, equipment, or automated-driving-system technologies; manufacturer certification, applicable standards, and defect authority are different parts of the oversight arrangement. [C-STD-004]

This is not a blanket declaration that a learned perception model is safe in every scene. It is also not evidence that road deployment has no obligations. It tells us to keep product compliance, operational permission, and technical evidence for a particular learned-component claim as separate objects.

[Visual: a dated news-style card for an inquiry, then a large “not a safety finding” label.]

A current inquiry can illustrate the distinction without becoming this project's subject. NHTSA opened an audit query into process and technical data behind Tesla Cybercab self-certification. The inquiry is not a finding that the product is unsafe or noncompliant. [C-ROAD2-004] [C-ROAD2-005]

The same separation matters more visibly in aviation. A Technical Standard Order is distinct from installation approval and operation. A vendor product page, a scoped operating permission, or an article authorization cannot disclose the evidence for a particular learned model. [C-INTAKE-003] [C-INTAKE-001]

The lesson is simple: visible permission is not a substitute for a readable safety argument. It may be part of the context. It is not the whole technical case.

**FEEDBACK PAUSE 4:** Does this section keep the road example useful without making the video about Tesla?

## 5. Existing methods: structure, not a finished answer — 11:30–16:30

[Visual: a map rather than a ranking. Every card shows its status: public method, UK military guidance, proposed civil material, public standard scope, voluntary guidance.]

It would be wrong to say that no work exists. There is serious work on assurance for learned components. The harder question is what each document actually covers.

AMLAS is a public method for assuring a machine-learning component. It organizes work into six stages: safety-assurance scoping, requirements, data management, model learning, model verification, and deployment. AMLAS also says it is about the ML component, that it needs complementary system and domain assurance, and that its main focus is offline supervised learning. [C-CHAL-006]

That makes AMLAS a useful baseline for the data, labels, training decisions and independent tests we just saw. It does not, on its own, establish a car's braking margin, an aircraft's maneuver authority, the operational rules, or an authority decision for a specific release.

The UK Military Aviation Authority has a current, applicant-specific path for certified military air systems. Its notice recommends fixed supervised models in a defined operating domain for early safety-related applications and calls for architectural mitigation when no prescriptive solution is available. It is military guidance, not a civil approval route. [C-CHAL-001] [C-CHAL-002]

EASA's NPA 2025-07(B) is detailed proposed material. It addresses operational domain, risk assessment, development assurance, learning assurance, lifecycle data, and in-service monitoring. But it is proposed, not final. Its stated high-consequence scope boundary is also important: applying that boundary to a real function would require an aircraft-level failure-condition allocation. [C-CHAL-003] [C-CHAL-004]

Road material supplies other pieces. ISO/PAS 8800's public scope includes trained AI models and safety-assurance claims. UL 4600 describes a goal-based safety case for autonomous products. NHTSA's public automated-driving-system material is voluntary guidance, not federal approval. [C-AUTH-006] [C-AUTH-007] [C-AUTH-008]

[Visual: a status ladder, from statute and authority guidance to standard/method to product safety case. Arrows say “does not substitute for.”]

So the public landscape is not empty. It is unfinished and fragmented for the difficult case we are studying. A method can be for a component rather than a system. A document can be proposed rather than final. A military path can be informative without being transferable to civil approval. A standard can give a shared vocabulary without revealing a product's evidence.

This project therefore makes a modest claim: the inspected public material gives us useful structures, but it does not let us skip the case-specific evidence for a hazardous trained decision.

[Visual: the public-assurance coverage map. Do not animate it as a race toward a green “certified” zone. Reveal each source's boundary in turn.]

There is a more precise way to see this. Put the documents on a map with two axes: how much decision authority is delegated to the system, and which hazard/risk region the document actually addresses.

EASA's proposed aviation taxonomy gives Levels 1A through 3A named roles. They range from information and decision support, through directed and supervised action, to safeguarded action with limited authority upon alerting. Level 3B is not a defined no-human category. It is marked reserved, with no authority or responsibility assigned. [C-RISK-006]

The proposal also includes a scenario-based risk table. It measures likelihood per operational hour, from frequent through extremely improbable. For the H1 category, potential fatalities, every likelihood cell is unacceptable in that proposal. Some lower-severity and lower-likelihood cells are marked acceptable or moderate, and those categories feed a proposed assurance-level allocation. [C-RISK-007]

That is a meaningful boundary. It is not a statement that every organization refuses all AI risk. It is not an adopted approval of every green cell. It is one proposed aviation framework saying exactly where its current limits sit.

AMLAS occupies another region: a component lifecycle. The UK MAA material is an applicant-specific military route. The FAA roadmap explains the learned-implementation problem and research direction. NHTSA incident reporting provides oversight data, not a technical acceptance envelope. The blank spaces between them are the reason this project proposes an evidence graph rather than claiming there is one finished checklist. [C-CHAL-001] [C-CHAL-006] [C-AUTH-010] [C-DIR-003]

**FEEDBACK PAUSE 5:** Does the status language feel clear enough to skim and hear once?

## 6. What probability can and cannot say — 16:30–21:00

[Visual: a risk ledger. Inputs include encounter distribution, simulator, hazard definition, sensor configuration, release, and recovery. Removing an input turns the result into a question mark.]

At this point, the conversation often turns into a demand for one number. How accurate is the model? How many miles did it drive? What is the probability of failure?

Those can be useful questions. But they stop meaning the same thing when their assumptions are removed.

Conventional system-safety practice relates more severe outcomes to lower acceptable likelihoods. That is useful context. It does not turn a held-out detection result into a learned component's failure rate. The harm depends on the encounter distribution, sensing configuration, threshold, delay, downstream decision, and recovery path. [C-RISK-001]

Scenario coverage can show which selected combinations of conditions were exercised. It can reveal gaps in a test plan. But it cannot prove that the analyst selected every factor that matters, or that coverage alone establishes performance. [C-EVID-002]

Rare-event simulation can estimate a selected risk under a stated traffic distribution, simulator, and hazard threshold. That is valuable when direct testing would be impractical. Its result does not automatically transfer to a changed sensor, different weather model, or a dangerous tail of the distribution that the generator did not represent. [C-EVID-003]

Calibration asks whether a model's stated confidence matched observed frequency on an evaluation distribution. It can support a policy such as slow down, seek another observation, or limit authority when confidence is poor. But calibration on one evaluated distribution does not establish hazard awareness after an unfamiliar shift. [C-EVID-004]

[Visual: ROC curve and confusion matrix as an illustrative evidence type, not a safety score; two thresholds show different miss/false-alarm tradeoffs.]

An average can be misleading too. The UK CAA's DAA material warns that an average risk ratio can conceal a deficient encounter class. AMLAS's threshold and confusion-matrix example likewise shows why false alarms and misses have different costs. An operating point is a contextual choice, not a universal model-safety number. [C-RISK-004] [C-RISK-005]

Looking inside a model is not an escape hatch. Saliency images can look persuasive without faithfully explaining the behavior that matters. Neuron coverage may be a diagnostic worth investigating, but the inspected evidence does not make it a causal safety measure. [C-EVID-006] [C-EVID-007]

The useful replacement for a single number is a disciplined question: what does this measurement tell us about this hazard, in this scenario, for this release—and what else must be true before the system may take this action?

[Visual: an incident counter flips into a denominator ledger: vehicle population, operating domain, miles or hours, event definition, reporting access, duplicate reports, and data quality.]

Road data teaches the same lesson. NHTSA's Standing General Order collects incident reports for automated driving systems and Level 2 assistance. The data dictionary warns that access to crash data can affect reporting, reports may be incomplete or unverified, multiple reports can describe the same crash, and the published summary data are not normalized. [C-DIR-003]

So an incident count is a prompt to investigate, not a rate and not a safety conclusion. The denominator matters.

The same is true when people compare electric and combustion vehicles. In a 2016 hybrid and electric quiet-car rulemaking, NHTSA said it did not have the powertrain-specific vehicle-miles-traveled data needed to directly measure the pedestrian and pedalcyclist rate per mile against conventional vehicles. It used a proxy and case-control analysis with stated limits. [C-DIR-002]

For this film, electric-vehicle accident comparisons are context for measurement discipline, not a target for autonomy. Powertrain, automation, vehicle design, driver population, operating domain, and reporting are different variables. A useful risk number names every one it depends on.

**FEEDBACK PAUSE 6:** Is the probability section specific enough without becoming a statistics lecture?

## 7. The proposed safety layers — 21:00–27:00

[Visual: the learned component at the center of nested shells. Each shell is an evidence obligation. The green action envelope shrinks as uncertainty or recovery margin worsens.]

Here is the constructive part. **Project proposal:** a learned component should not sit alone in a binary trusted-or-untrusted box. It should be surrounded by separate, inspectable evidence obligations.

First, define the operating domain, hazardous decision, and delegated authority. Second, establish what sensing and preprocessing can distinguish, including their limits and timing. Third, identify the exact frozen release: data, labels, training configuration, weights, transforms, sensors, and interfaces.

Then ask how errors, uncertainty, and delay behave in the encounter classes that matter. Follow them through planning, actuation, and dynamics. Ask what the monitor can independently observe, when it can intervene, and whether a recovery controller can still reach a safe state. Finally, treat every material change as a reason to reopen affected evidence.

This proposal matches the project's eight evidence contracts: scope and authority, observability, lineage, hazard-relevant performance, closed-loop behavior, intervention and recovery, composition, and change control. It is a project architecture, not an adopted certification checklist. [C-015] [C-METHOD2-018]

Let's walk the cyclist case all the way through. Our first statement is not “the model detects cyclists.” It is narrower: in a named speed range, road layout and sensor configuration, this exact release may provide a candidate cue soon enough for a stated maneuver policy. The words **soon enough** force a timing budget. The words **exact release** force a record of the frames used for development, the label rules for partial visibility, the chosen weights, the camera calibration, and the threshold that turns a score into a cue. This is an example of what a claim would have to contain, not evidence that our hypothetical release has met it.

[Visual: a blank evidence card fills in from left to right. Camera mount and route geometry appear first; data and weight version appear next; the maneuver deadline stays red.]

Now split the test results by the encounters that can hurt us. Does the cue arrive when a cyclist is only briefly visible at the edge of a van? Does glare change the answer? Does a lower mounted camera change it? How often is the cue absent, and how much time is left when it finally appears? We would report misses and false alarms with the same scene definitions and tested population. We would also look at unfamiliar objects, because a model trained on a fixed list of classes should not confidently announce an empty route just because the hazard does not match one of its labels. [C-TRAIN-001] [C-TRAIN-003]

A test with no cyclist and no alarm is useful. It is not the same test as a cyclist hidden until the last safe braking point. Those scenes can produce almost the same camera image for part of the approach. That is why we need to know when information becomes available, not merely whether the final frame was classified correctly. A perfect answer after the deadline is a failure for the hazardous decision.

The next layer takes the cue through tracking and the planner. A bounding box is not a safe path. The tracker needs enough motion information to estimate whether the cyclist is entering the lane. The planner needs a feasible response within vehicle dynamics. The monitor needs a signal that can reveal a bad perception state without simply reading the same incorrect “clear lane” output. And the recovery controller needs enough braking or steering margin at the moment authority changes. [C-EVID-005]

[Visual: the cue reaches a planner, but the remaining distance bar runs out before braking finishes. The detector card remains green while the maneuver card turns red.]

Finally, change something ordinary: a camera lens, mounting angle, preprocessing step, label policy, training batch, threshold or route boundary. Which evidence still applies? The graph should point to the tests and argument sections that need to run again. If the new camera changes what can be seen around the van, an old held-out score on the previous camera cannot be pasted into the new release. This is the practical purpose of change control for a frozen trained model.

There are established ideas that inform this structure. A Simplex-style runtime-assurance pattern allows an advanced controller to act while a monitor can transfer authority to a trusted controller. But the safety implication is conditional. The monitor must observe the relevant condition, detect it in time, switch within a bound, rely on suitable dynamics, and hand over to a controller that can reach a safe state. [C-METHOD2-001] [C-METHOD2-003] [C-EVID-005]

[Visual: the monitor shell fractures because it receives the same incomplete world model as the planner. A second scenario shows an independent-enough sensor path, but marks its latency and common-cause assumptions as open.]

The nested shells are not a magic wrapper. A deterministic safety controller cannot create an unseen pedestrian, obstacle, or aircraft. If the relevant difference cannot be observed early enough, the honest response is to reduce authority, restrict the domain, improve the observation path, or block the release. [C-016] [C-METHOD2-019]

That is why the graph matters. A source, an assumption, a model release, an evaluation result, monitor premise, recovery premise, and authority boundary are distinct nodes. Changing the sensor, the weights, the operating domain, or the recovery argument should show which claims, diagrams, and tests need fresh review.

**FEEDBACK PAUSE 7:** Does the safety-layer proposal feel constructive rather than like another list of requirements?

## 8. Let the car take off — 27:00–31:15

[Visual: the road layout tilts up into an airspace view. The same evidence nodes remain pinned to the vehicle; labels change from stopping distance to closing rate and separation margin.]

Now let the vehicle take off. Keep the cue format from our vision example: candidate image region or bearing, time and uncertainty. Change the camera, the training set, the labels, the target sizes, the backgrounds, the tracker, and the release identity. A single road validation result cannot travel into airspace. [C-TRAIN-001] [C-TRAIN-003]

The problem did not simply become harder. Its assumptions changed. Instead of stopping distance, we have closing rate and separation margin. Instead of one road geometry, we have airspace, cooperative and noncooperative traffic, range, background clutter, weather, track latency, and maneuver limits. A camera cue alone does not establish range or range rate; the safety case must show how tracking or another sensor supplies them in time. A landing may be a later contingency; it is not an immediate answer to a collision encounter. [C-015]

The questions remain. What can the sensors see? When does a track become usable? What action authority is justified? What can the monitor independently observe? And if it orders an active escape, how does that recovery path independently show enough traffic and terrain clearance to avoid creating the next collision?

Imagine a camera that flags a dark pixel cluster as possible traffic. That might be a useful first cue, but the aircraft cannot turn on a pixel cluster alone. Is it an aircraft, a bird, a cloud edge, or a sensor artifact? If it is an aircraft, is it closing, and is there still maneuver time? The system may need consecutive frames, calibrated geometry, radar, cooperative surveillance, or a combination. Every added source can improve observability and create a new failure mode, delay or disagreement to test. We would evaluate the frozen air release on those combinations, including small targets against terrain and the times when a track is lost. [C-TRAIN-003]

[Visual: a bearing-only cue branches into “track not established” and “track plus range/rate support.” Only the latter reaches an avoidance proposal, and that proposal still passes through clearance and authority gates.]

The training plan also changes. Road scenes do not cover aircraft size, background, closing geometry or right-of-way constraints. We would define air-specific labels and group verification encounters so adjacent frames of one flight do not masquerade as independent evidence. We would challenge the air model with withheld collection conditions, then carry misses and delays into a separation-margin analysis. The result might still be a restriction: no learned cue authority in a particular background, weather or traffic mix. That is an engineering outcome, not a failure to produce a headline accuracy number. [C-TRAIN-001] [C-TRAIN-003]

GA-ASI publicly describes a detect-and-avoid architecture that combines cooperative surveillance sources with air-to-air radar for noncooperative traffic. The inspected material describes a sensor-fusion architecture; it does not establish a trained neural-network component. It tells us something about the vendor-described architecture, not that a particular configuration, installation, aircraft, operation, or learned component has closed every assurance question. [C-AIR2-001]

The inspected public material did not establish issuance of a GA-ASI DAA or ATAR Technical Standard Order authorization. And even a TSO would not itself establish installation or operational approval. [C-AIR2-003] [C-INTAKE-003]

A scoped BVLOS authorization can show that a particular operation was permitted. It does not disclose an unrestricted learned-perception assurance case or an equipment authorization. [C-AIR2-012] [C-INTAKE-001]

The road-to-air comparison is therefore not “cars are allowed but aircraft are not.” It is a test of whether the argument keeps its boundaries when the sensing, time, recovery, and approval layers change.

**FEEDBACK PAUSE 8:** Does this transition make flight feel like a deeper test of the same argument?

## 9. The evidence graph and the question to keep — 31:15–32:30

[Visual: eight evidence contracts become a live graph. A changed model hash and sensor configuration turn connected evidence amber. No percentage or composite score appears.]

A trained autonomous system does not become safe because we attach a permit, a standard, a monitor, a thousand test miles, or an interpretability picture. Each may contribute evidence. None substitutes for the others.

**Project proposal:** start with a hazardous decision. Bind it to an operating domain, sensing limits, an exact release, scenario evidence, closed-loop margin, a monitor premise, recovery behavior, and change history. If a link is missing, reduce authority, restrict the domain, or block the release. [C-015] [C-METHOD2-018]

That proposal does not certify a car or an aircraft. It gives engineers, reviewers, and authorities a more useful question to challenge: **what exactly lets this machine take this action, here, now—and what evidence would prove us wrong?**

The whitepaper, source library, and verification dashboard make the current argument inspectable. They distinguish source support, adversarial challenge, cross-artifact consistency, and human disposition. A green review mark is not a safety result. It only says a particular review task passed for a particular frozen input.

The open edges are part of the result. They tell us where the next experiment, source, design change, or authority conversation has to begin.

[End screen: “Read the paper / inspect the evidence graph / challenge an open edge.” Keep the graph in motion; do not introduce a verbal sign-off before the cards appear.]

**FEEDBACK PAUSE 9:** Which question or visual should be the final image the viewer remembers?
