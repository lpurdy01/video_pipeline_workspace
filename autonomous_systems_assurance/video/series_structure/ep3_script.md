# Episode 3 — Building an AI Vision System to a Safety Standard, Then Letting It Fly

**Status:** recording-feedback draft, 25 September 2026. Part 3 of 3; stands alone. Target about 9–10 minutes including visual holds (about 1,089 spoken words at 130 wpm). Bracketed directions are not spoken. Every factual line carries its claim tag. The vision system is hypothetical: nothing here describes a real product.

---

## Cold open — 0:00–0:36

[Visual: a detector's score card glows green with a high score. Cut to the road: the cyclist emerges from behind the van; the detection box appears, correctly, just after a red line marked "last safe braking point."]

This detector is right. It spots the cyclist. It just spots her after the last moment the car could have stopped.

For a hazardous decision, a perfect answer after the deadline is a failure. So how would you build a vision system whose evidence is about deadlines and decisions, not just accuracy?

Let's build one, on paper, the way today's frameworks point. Then let's make it fly.

[Title card: *Building an AI Vision System to a Safety Standard — Then Letting It Fly*]

## 1. Decide what the model is allowed to do — 0:36–1:34

[Visual: the green cue card: "candidate location · time · uncertainty / unknown." A steering-wheel icon is crossed out.]

Start before the model. Our learned component gets a short run of camera frames and returns one thing: a cue. Where something might be, when, and how sure it is, including "I don't know." It doesn't steer. It doesn't declare the lane clear. Tracking, planning, a monitor and a recovery policy turn that cue into action.

Next, write down which decision the cue can influence, where it operates, and how much authority it gets, and find out how critical the function will be rated. In aviation that rating even decides whether the first machine-learning process standard, as drafted, applies at all: its first issue stops at a rating called DAL C. [C-STAT-002]

## 2. Data and labels — 1:34–2:57

[Visual: a frame with a half-hidden cyclist. Three labellers draw three different boxes; a fourth tag reads "unknown / occluded."]

The University of York's AMLAS method, a public guide to assuring machine-learning components, says data requirements have to be tied to the operating domain: relevant, complete, accurate and balanced. Its own examples include the installed camera viewpoint, lighting, and how to label partly hidden pedestrians. [C-TRAIN-001]

So write the label policy first. What do you call a cyclist who's a fifth visible? What about a frame where she's completely hidden? Label that frame "clear," and you've taught the model something false. The honest label is "unknown."

[Visual: frames from one drive fan out; some land in the training pile, some in the test pile; a warning flag appears.]

Then split the data by encounter, not by frame. If neighbouring frames from the same drive land in both training and test, the test score flatters you. And if you keep tuning after looking at the final test set, you're quietly training on it. AMLAS warns about exactly that leakage, calls for a log of every model choice, and treats the verification set as an independent challenge aimed at realistic failures. [C-TRAIN-002] [C-TRAIN-003]

**FEEDBACK PAUSE 1:** Is the data section concrete enough for someone who has never trained a model?

## 3. Learning, and its traps — 2:57–3:38

[Visual: two learning curves. One sits high for both training and test error; the other shows low training error and a widening gap.]

Two classic traps. Too little capacity, and the model misses things in training and testing alike: underfitting. Too tuned to the development data, and it shines there but fails on a new road, a new sky or a new camera: overfitting. [C-TRAIN-004]

[Visual: a heat map lands on a simulator watermark in the corner instead of on the cyclist.]

There's a nastier version: the shortcut. AMLAS gives the example of a model picking up artifacts of simulated images as a cue for the class it's supposed to detect. [C-TRAIN-002] A good score, for the wrong reason.

## 4. Test the thing that actually runs — 3:38–4:35

[Visual: the trained model passes through EXPORT, COMPILE, QUANTIZE; a fingerprint beside it changes at each step.]

Before it ships, the model is exported, compiled, and often quantized to run on the vehicle's computer. Each step can change its outputs. So evaluate the deployed artifact, not the version on the training server. The draft aviation ML standard, as presented in 2025, treats a deployed model as software: either correct and qualified, or not. [C-STAT-003]

Then evaluate the way the hazard cares: by type of encounter, counting misses, false alarms, and the one people forget, delay. [C-TRAIN-003] How much time is left when the cue arrives?

And don't trust one number. The UK Civil Aviation Authority notes that averaging detect-and-avoid risk metrics can hide weaknesses in particular encounters. [C-RISK-004]

**FEEDBACK PAUSE 2:** Does "test the thing that actually runs" come across as practical advice?

## 5. Close the loop — 4:35–6:30

[Visual: the cue flows into TRACKER, then PLANNER, then VEHICLE DYNAMICS; a remaining-distance bar drains toward zero.]

Now run the cue through tracking, planning and vehicle dynamics. A correct detection that arrives too late is still a failure.

[Visual: a timing bar along the road: 6.7 m of latency, then 15 m of braking, ending at the conflict point. A cyclist icon pops out from behind the van only 10 m ahead, inside the bar. The speed dial drops from 30 to 15 mph and the bar shrinks until the cyclist sits outside it. Caption: "illustrative assumptions".]

Put numbers on "too late." At 30 miles an hour, with half a second from camera frame to brake command and firm braking, the car needs the cue about 22 meters before the conflict. If the cyclist can first appear 10 meters out from behind a van, no detector can meet that deadline. Slow to 15 near parked vans, and it fits. Those are illustrative assumptions, but it's the arithmetic a real program has to write down, and it turns the envelope lever into a rule.

And the monitor needs a way to notice a bad perception state that doesn't just read the same "lane clear" output. Aviation even has an active standard practice for this kind of runtime-assurance architecture, ASTM F3269. [C-PRAC-001] But formal runtime-assurance results only hold when the monitor can observe the problem and act in time. [C-EVID-005] [C-016]

[Visual: a camera icon rotates a few degrees; three test results turn amber.]

Finally, change something ordinary: a lens, a mounting angle, a labelling rule. Which evidence still holds? Treat the change as a new release until the affected tests are rerun. [C-AUTH-002]

That's a program a team can actually run: eight phases, each with an artifact and a gate. The full table is in the paper linked below.

## 6. Let it take off — 6:30–7:30

[Visual: the road tilts up into airspace. The green cue card stays pinned on screen.]

Now keep the cue, and change the world.

[Visual: a small dark cluster against broken terrain; a detection box with a question mark.]

A glider with no transponder, against broken terrain. The camera can flag a bearing, but an aircraft can't turn on a pixel cluster. It needs a track, range and closing rate, traffic context, and room to maneuver without creating the next conflict. The air model needs its own data, its own labels and its own frozen release. The road model doesn't come along.

[Visual: the road's stopping-distance bar morphs into a separation timeline: DETECT, TRACK, DECIDE, MANEUVER, LAST RECOVERABLE SEPARATION.]

The approvals change too. Aviation approves equipment and installation separately, [C-INTAKE-003] and sets rigor by development assurance level from the safety assessment. [C-RISK-002] If a detect-and-avoid function lands above DAL C, the first edition of the aviation ML standard, as drafted, won't cover it. [C-STAT-002]

**FEEDBACK PAUSE 3:** Does the take-off feel like the payoff of the series?

## 7. Verified, and still unsafe — 7:30–8:44

[Visual: an enormous decision table shrinks into a small neural network.]

Aviation already has a cautionary example. ACAS Xu is a collision-avoidance system for unmanned aircraft. Its designers built an enormous decision table, and researchers compressed it about a thousand times into a set of neural networks. [C-CASE-007]

Formal-verification researchers then proved properties of those prototype networks, at a scale an order of magnitude beyond earlier tools. [C-CASE-006]

[Visual: two aircraft converge. The network outputs "turn"; the geometry evolves; the network is asked again; the tracks still meet.]

But those were open-loop properties: what the network says for a given input. Collision avoidance is a closed-loop property: what happens after the aircraft follows the advice, the geometry changes, and the network is asked again. When Stanley Bak and Hoang-Dung Tran analysed the closed loop, even assuming perfect sensors, instant response, ideal maneuvers and an intruder flying straight, they found cases where the early prototype still collided. [C-CASE-007]

Proving something about the component is valuable. It isn't the same as showing the system keeps aircraft apart.

## Close — 8:44–9:38

[Visual: the four levers rise around the aircraft: OBSERVATION, ENVELOPE, AUTHORITY, RECOVERY.]

Road or air, the conclusion is the same. When the evidence isn't there, you have four levers: improve what the system can observe, narrow where and how fast it operates, reduce the authority you give the learned part, or make sure a recovery still works in time.

And one question to keep: what exactly lets this machine take this action, here, now, and what evidence would prove us wrong?

The full eight-phase lifecycle, the open-items list and every source are in the paper linked below. And if you want the software-safety playbook all of this builds on, start with episode one.

[End screen: Episode 1 — *How Do You Certify Code Nobody Wrote?* · Episode 2 — *Who Decides When AI Is Safe Enough?* · paper link in the description.]
