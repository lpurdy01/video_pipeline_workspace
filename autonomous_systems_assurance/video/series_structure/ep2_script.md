# Episode 2 — Who Decides When AI Is Safe Enough to Drive — or Fly?

**Status:** recording-feedback draft, 25 September 2026. Part 2 of 3; stands alone. Target about 8–9 minutes including visual holds (about 940 spoken words at 130 wpm). Bracketed directions are not spoken. Every factual line carries its claim tag. Status statements are dated 25 September 2026 and must be rechecked before recording.

---

## Cold open — 0:00–0:52

[Visual: two cards slide in. Left: a car with the label "US: no federal pre-approval." Right: one small detect-and-avoid box collecting separate stamps: MANUFACTURE, INSTALLATION.]

In the United States, a carmaker certifies for itself that its vehicle meets federal safety standards. The national regulator says it doesn't pre-approve new vehicles or automated-driving technology. [C-STD-003] [C-STD-004]

In aviation, even a detect-and-avoid box gets one approval to be manufactured to a performance standard, and a separate approval to be installed. [C-INTAKE-003] [C-AIR2-004]

And the first standard for machine learning in aircraft, from a committee formed in 2019, is, as drafted, limited to functions no more critical than a rating called DAL C. [C-STAT-001] [C-STAT-002]

So who actually decides when a learned system is safe enough, and what haven't they decided yet?

[Title card: *Who Decides When AI Is Safe Enough to Drive — or Fly?*]

## 1. Permission is not proof — 0:52–2:52

[Visual: a stack of separate cards for one robotaxi: federal compliance, state permit, passenger service, learned-model evidence. None nests inside another.]

When you see a driverless car on a public road, it's natural to assume someone proved it safe. What actually exists is a stack of different permissions.

US federal law requires the manufacturer to certify compliance with the applicable Federal Motor Vehicle Safety Standards, and not to issue a certificate it knows, with reasonable care, is materially false. [C-STD-003] NHTSA's automated-driving guidance is voluntary; companies' safety self-assessments aren't federal approvals. [C-AUTH-008]

States add operating layers. Texas requires authorization for commercial automated-vehicle operation. California separates testing, driverless testing and deployment permits. [C-ROAD2-001] [C-ROAD2-006] And in July 2026, NHTSA said it had started developing performance standards for automated vehicles. [C-AUTH-009]

[Visual: a second card for a different road regime: "UN R157 — type approval."]

Other road regulators work differently. UN Regulation 157 sets type-approval rules for automated lane-keeping systems: a pre-market approval for one bounded automated function. The UK is building it into its vehicle approval scheme, and notes that as a contracting party it has to accept R157 approvals. [C-STAT-008]

Some companies publish their own process. Waymo describes a deployment-readiness process built on acceptance criteria and safety-case evidence, and announced a third-party audit of it, though the auditor's findings weren't part of the announcement. [C-ROAD2-012] [C-ROAD2-013]

Aviation splits permission by object. A Technical Standard Order authorization approves manufacturing an article to a minimum performance standard. Installing it on an aircraft needs a separate approval. [C-AIR2-004] [C-INTAKE-003]

None of these permissions shows you the evidence behind a trained model. They answer different questions.

**FEEDBACK PAUSE 1:** Does the permission stack stay clear without turning into a legal lecture?

## 2. What exists for machine learning — 2:52–4:33

[Visual: the coverage map builds row by row.]

So what exists specifically for machine learning?

The University of York's AMLAS method walks through assuring an ML component: from safety requirements to data, learning, verification and deployment. It says plainly that it covers the component, not the whole system, and mostly offline supervised learning. [C-CHAL-006]

The UK's military aviation authority has a live path. An applicant agrees a certification review item with the regulator, and early safety-related uses should be fixed, supervised models in a defined operating domain. [C-CHAL-001]

In Europe, EASA published a detailed proposal for AI in aviation in November 2025, responding to the EU's AI Act. Comments closed in March 2026, and in September the proposal was still awaiting responses. [C-STAT-005] [C-STD-002]

[Visual: EASA's authority scale from 1A to 3B; 3B glows "RESERVED." Then the risk matrix; the H1 row turns red cell by cell.]

Look at where EASA drew its own lines. Its scale of AI authority runs from information support up to safeguarded action. The top level, 3B, is simply reserved. [C-RISK-006] And in its proposed risk matrix, any scenario with potential fatalities is unacceptable, at every likelihood, even "extremely improbable." [C-RISK-007]

In the US, the FAA's 2024 roadmap said the aviation industry lacked a method for AI safety assurance, and pointed to project-specific issue papers as a way forward in the meantime. [C-AUTH-001] [C-AUTH-003]

**FEEDBACK PAUSE 2:** Is the coverage map readable on a phone at this pace?

## 3. The standard that's coming — 4:33–6:00

[Visual: a timeline. 2019: committee forms. 2021: statement of concerns. 2024: taxonomy. August 2025: open consultation. Target June 2026, which then slides to 31 December 2026.]

The piece aviation is waiting for is ED-324, known at SAE as ARP6983: a joint process standard for machine learning in aircraft systems.

The joint committee formed in 2019. It published a statement of concerns in 2021 and a taxonomy in 2024. [C-STAT-001] The draft went to public consultation in August 2025, [C-STAT-004] after an earlier ballot drew about 1,800 comments. [C-STAT-003] That August, the target was June 2026. When EUROCAE's page was captured in September 2026, it listed the draft with a target of 31 December 2026. [C-STAT-001] [C-CHAL-005]

[Visual: a ladder of levels A to E. A and B sit behind a line labelled "issue 1 stops here."]

Here's the key line in its scope, as presented to the FAA: issue 1 covers non-adaptive, supervised machine learning, up to DAL C. If the safety assessment puts a function above that, the draft standard can't be used. [C-STAT-002]

In aviation's software scheme, level A is the most critical. [C-STAT-007] So the first edition of the first aviation ML standard deliberately leaves the most critical jobs for later. A second issue is planned to add other techniques, like reinforcement learning. [C-STAT-003]

**FEEDBACK PAUSE 3:** Does "stops at DAL C" land as the headline without overclaiming what the final text will say?

## 4. What's still missing — 6:00–7:03

[Visual: a board titled "Not done yet — as of September 2026." Items tick on one at a time.]

Put it all on one board. Some items we've already met: the aviation standard is a draft, it stops at DAL C, and the EU rule is still a proposal. [C-CHAL-005] [C-STAT-002] [C-STD-002]

[Visual: the DAL ladder returns; the locked A and B rungs now carry tags: "potential fatalities," "top authority level," "learns after deployment."]

Three more sit behind that same barrier. AI that directly contributes to potential fatalities, and the top authority level: excluded or reserved in EASA's proposal. [C-CHAL-004] [C-RISK-006] Systems that keep learning after they're deployed: outside these first frameworks. [C-CHAL-006] [C-STAT-002] [C-AIR2-007] And on the road, US performance standards for automated driving: development only just started. [C-AUTH-009]

One more item we looked for and didn't find in the public material: a published method for turning a perception system's error rates into the likelihood numbers these risk frameworks use. [C-RISK-007] Every program has to build that bridge itself.

## 5. The architecture tension — 7:03–7:59

[Visual: a modular pipeline, camera to cue to tracker to planner to monitor, collapses into one large block labelled "one network."]

There's a harder problem underneath. The frameworks we just walked through are built around modular, frozen, supervised components. [C-CHAL-001] [C-CHAL-006] [C-STAT-002]

Some developers are going the other way. Wayve describes replacing the modular sense-plan-act architecture with a single neural network that turns raw sensor inputs into driving outputs. [C-CASE-008]

Assurance evidence attaches at interfaces: the cue, the track, the plan, the monitor. An end-to-end design removes most of them. That doesn't make it unassurable, but it has to supply that evidence some other way, for example through an independent observation path whose assumptions can be checked on their own. [C-METHOD2-019] [C-EVID-005]

For engineers and managers, that's the takeaway: architecture choice determines assurability.

## Close — 7:59–8:19

[Visual: the open-items board dims; one line stays lit: "What would a team actually build?"]

So if the rules aren't finished, what does a team actually build? What artifacts, what tests, what gates, for a real vision-to-control system?

That's the next video. And at the end, we'll let the car take off.

[End screen: Episode 3 — *Build It, Then Let It Fly* · Episode 1 — *How Do You Certify Code Nobody Wrote?* · paper link in the description.]
