# Episode 1 — How Do You Certify Code Nobody Wrote?

**Status:** recording-feedback draft, 25 September 2026. Part 1 of 3; stands alone. Target about 10–11 minutes including visual holds (about 1,140 spoken words at 130 wpm). Bracketed directions are not spoken. Every factual line carries its claim tag. The road scene is hypothetical; the Tempe section reports NTSB findings only.

---

## Cold open — 0:00–1:13

[Visual: top-down intersection. A delivery van is parked at the edge; our car approaches. Split screen: left world, the lane beside the van is empty; right world, a cyclist is about to ride out from behind it. Both halves feed the same green "LANE CLEAR" card into two boxes: PLANNER and SAFETY MONITOR.]

Two worlds. In the left one, the lane beside this van is empty. In the right one, a cyclist is about to ride out from behind it.

The car's world model is identical in both. The planner gets "lane clear." So does the safety monitor that's supposed to catch its mistakes. [C-016]

Every line of code can be correct. Every test can pass. And in one of these worlds, the car still does the wrong thing.

This isn't only a thought experiment. In 2018 a real automated test vehicle detected a pedestrian 5.6 seconds before impact, and the crash still happened, through a chain that ran from its perception software all the way to the human who was supposed to be watching. [C-CASE-001] [C-CASE-004] We'll come back to how.

Aviation has spent decades learning how to trust software. [C-STAT-006] This video is about why that playbook cracks when part of the system is learned instead of written, and what engineers can do about it.

[Title card: *How Do You Certify Code Nobody Wrote?*]

## 1. The playbook — 1:13–3:25

[Visual: an aircraft function splits into system, item and software boxes; each box receives a letter.]

Start with aviation, because it runs the strictest version of the playbook.

First, rate each function by what happens if it fails. The system safety assessment assigns a development assurance level, a DAL. The worse the consequence, the more rigor. [C-RISK-002] [C-RISK-001]

Then the software. The FAA recognizes a standard called DO-178C as an acceptable way to show airborne software is fit for certification, together with a companion document for qualifying tools. [C-BASE-001]

NASA's public explanation of DO-178C lays out what that means in practice. Five software levels, A through E, with A the most critical. Requirements that trace down to the code and back up again. Tests that show every requirement was met, and, at the top levels, structural coverage showing the tests actually exercised the code. And the tools that generate or check software have to be qualified too. [C-STAT-007] [C-BASE-002]

[Visual: a coverage bar fills line by line across source code; one untested branch lights up red.]

Why so much process? NASA's paper puts it plainly: testing can never prove the absence of errors. So the approach is to demonstrate the quality of the process that produced the code. [C-STAT-007]

Cars have their own version. ISO 26262 runs a functional-safety lifecycle from concept through hardware and software, with automotive safety integrity levels, ASILs, setting the rigor. [C-BASE-004]

[Visual: a timeline. December 1992: DO-178B. December 2011: DO-178C. 2019: a joint committee on AI in aviation forms. A dotted "draft" marker sits on 2026.]

This playbook took a long time to build. DO-178B came out in December 1992. Its successor, DO-178C, arrived in December 2011, after seven years of committee work. [C-STAT-006]

The first comparable standard for machine learning in aircraft? That committee started in 2019. As of this recording, its first edition is still a draft. [C-STAT-001] [C-CHAL-005]

**FEEDBACK PAUSE 1:** Is the playbook concrete enough for someone who has never worked under DO-178C or ISO 26262?

## 2. What a learned component breaks — 3:25–5:33

[Visual: the traceability chain from part 1. The bottom box dissolves into a grid of weights; the arrow from requirement to weights snaps.]

Here's the problem. In a trained neural network, the implementation is millions of learned weights. Engineers choose the task, the data and the training process, but nobody writes a requirement for each weight.

The FAA's AI roadmap names this directly: for learned AI, the designer can't derive lower-level requirements that describe the learned algorithm, or show that they cover the requirements above them. [C-AUTH-010] The same roadmap says existing software and complex-hardware guidance isn't adequate for learned implementations. [C-RISK-002]

Now walk down the playbook.

Traceability to code? The behavior came from data, so there is no line of code that says "this is a cyclist."

Structural coverage? You can count how many neurons your tests activated. One study of a self-driving network found only a small association between that and steering errors, and no evidence it was a reliable measure of test adequacy. [C-EVID-007] Covering the network doesn't tell you which real situations your data never contained.

Process quality? Still necessary. But the behavior now depends on what's in the data, not just how carefully people wrote code.

Configuration control? The "build" now includes the dataset, the labels, the training run, and the exported model on the target computer. Change any of them and you have a different function. [C-AUTH-002]

[Visual: six pillars labelled with the playbook items. Four develop hairline cracks; two new supports appear, labelled "data evidence" and "encounter evidence."]

So the playbook doesn't disappear. The sensors, interfaces, planner and control code around the model still need all of it. But the part that decides "is there a cyclist?" needs a different kind of evidence.

**FEEDBACK PAUSE 2:** Does the pillar-by-pillar walk land without slowing down?

## 3. The information problem — 5:33–6:58

[Visual: back to the two worlds. Zoom into the camera frame: the van's outline is identical pixel for pixel in both worlds until a wheel appears.]

And here's the part better training can't fix.

If the camera can't see the cyclist until after the last moment the car could stop, a bigger dataset can't add pixels that were never captured. And a monitor that only reads the same perception output shares the same blind spot. [C-016]

Runtime safety monitors are real, useful engineering. But the formal results behind them are conditional: the monitor has to observe the problem, detect it in time, switch fast enough, and hand control to something that can still reach a safe state. [C-EVID-005]

[Visual: four levers rise around the car, one at a time.]

So when the information isn't there, the design has four levers.

Change the observation path: a sensor or mounting that can see around the van.

Change the operating envelope: slow down near parked vans.

Change the authority: don't let this cue alone decide the lane is clear.

Change the recovery: make sure a safe action still exists when the cue arrives late.

A better accuracy number isn't on that list.

**FEEDBACK PAUSE 3:** Are the four levers memorable enough to carry the rest of the series?

## 4. What Tempe shows — 6:58–9:09

[Visual: a neutral rendered timeline, no crash imagery. A time-to-impact axis runs from minus six seconds to zero.]

This isn't only hypothetical. In 2018, in Tempe, Arizona, an Uber developmental automated vehicle struck and killed a pedestrian who was walking a bicycle across the road. The National Transportation Safety Board's report is an unusually detailed public trace of a perception-to-control chain failing. [C-CASE-001]

The system detected her 5.6 seconds before impact. But it never classified her as a pedestrian. At different moments it called her a vehicle, an unknown object, and a bicycle. [C-CASE-001]

[Visual: the object's label flickers: VEHICLE, OTHER, BICYCLE. Each flicker wipes the trail of past positions behind it.]

Every time the label changed, the system dropped her tracking history, so its prediction of where she was going started over. Objects labelled "other" weren't given a predicted goal at all. [C-CASE-002]

When it finally determined a collision was imminent, the design held off braking for one second, without alerting the safety operator, because of concerns about false alarms. And it wasn't allowed to brake just to reduce the impact. It relied on the human. [C-CASE-003]

The human was looking down at her phone. NTSB found the probable cause was the operator's failure to monitor the road; contributing factors included Uber's inadequate safety risk assessment and its safety culture. [C-CASE-004]

[Visual: the four levers from section 3 reappear beside the timeline.]

Now look at where the failure lived. A detection existed, 5.6 seconds out. It was lost between classification, tracking, prediction, and who had authority to act.

And the fixes NTSB describes afterwards were system-level: keep the car's own emergency braking active as an independent path, remove the braking delay, and keep an object's history even when its label changes. [C-CASE-005] None of them was "train a better classifier."

**FEEDBACK PAUSE 4:** Is the tone right for a fatal crash: precise, not sensational, probable cause stated clearly?

## Close — 9:09–10:05

[Visual: back to the van and the hidden cyclist. The question fades in.]

So the real question isn't "how accurate is the model?" It's this: in this situation, with these sensors, at this speed, does the right information arrive early enough, and survive all the way to an action?

The frameworks meant to answer that for aircraft and cars are being written right now. Some are still drafts, and some deliberately stop short of the most critical jobs. [C-STAT-002] [C-CHAL-004]

That's the next video: who's writing the rules, and what they've left open. Including why a US regulator says it doesn't pre-approve self-driving technology at all, while a single aircraft sensor needs separate approvals just to be built and installed. [C-STD-004] [C-INTAKE-003]

[End screen: Episode 2 — *Who Decides When AI Is Safe Enough?* · earlier channel video *The Software AI Isn't Allowed To Write* (confirm fit) · paper link in the description.]
