# End-to-end driving with proxy tasks: Tesla's 2026 talks and what they mean for this project

**Date:** 2026-09-27. **Status:** lead record and relevance assessment. No `sources.json` or `claims.json` yet: nothing here is a registered claim, and this file is not in `verification/artifacts.json`. The integrator decides what to promote. Proposed IDs use the unused `S-E2E-` / `C-E2E-` prefix.

**Trigger:** Levi remembered a Tesla talk about moving FSD to one network from video to controls. His recollection covered a "drive straight" degeneracy problem, and old perception tasks that now make the model "show its work." Question: does this alter or invalidate the project's direction?

**Raw material** is under ignored `research/gemini_independent_20260916/out/tesla_e2e_2026-09-27/`:
- Gemini transcripts of both talks;
- a Gemini grounded-search pass;
- local faster-whisper transcripts of the two key passages of the Duan talk;
- YouTube auto-captions of the Elluswamy WDFM-EAI talk;
- PDFs of the academic and Mobileye sources.

SHA-256 values are listed at the end.

## 1. The talk

The best match is **Phil Duan (Director of Engineering, Tesla AI), "Solving Self-Driving at Scale with Foundation Models," CVPR 2026 DriveX workshop, keynote 7**, Denver, 3 June 2026. It was uploaded by Mobility UCLA on 27 June 2026: <https://www.youtube.com/watch?v=cjzFjeSmh8M>. The title slide reads "CVPR 2024", a template slip.

The companion talk is **Ashok Elluswamy (VP AI, Tesla), "Building Foundational Models for Robotics at Tesla," CVPR 2026 Workshop on Autonomous Driving (WAD)**, the same day. It was uploaded 3 Sept 2026: <https://www.youtube.com/watch?v=2V0ddkF1Svo>. He gave the same talk at WDFM-EAI (<https://www.youtube.com/watch?v=i2hB_8BeueM>) and at ICCV 2025 WDFM-AD.

**How each passage was verified:**
- **Duan talk, passages quoted below:** local faster-whisper (small) on 14:00–19:30 and 25:30–29:10. It agrees with the Gemini transcript except where noted.
- **Duan talk, slide text:** Gemini only. Spot-check the video before publication.
- **Elluswamy talk:** the Gemini transcript of the WAD talk is corroborated by independent YouTube ASR of the WDFM-EAI version. Examples are the "2 billion tokens to 2 tokens" mapping, the "tree branches shaking" causal example, "reasoning traces", and the world simulator trained on the same dataset.

## 2. Recollection versus source

**1. FSD moved from parallel tasks to one network from vision to action.**
- **Verdict:** Supported.
- **Evidence:** Duan [07:26, Gemini transcript only]: "our entire approach before V12 was just wrong… a very modular approach like the rest of the industry." Duan [14:22]: "the most natural API for this is just video input and action as output. And everything else we predict are essentially just proxy tasks."
- **Nuance:** Tesla's 2021 HydraNet was already one backbone with many heads. The change was adding the action as a learned output and dropping the hand-written planner.

**2. The best control came from giving the model all the authority.**
- **Verdict:** Supported, as Tesla's performance claim.
- **Evidence:** the slide "The case for end-to-end driving" lists: codifying human values is hard; perception, prediction and planning interfaces are "ill-defined"; long-tail scaling; deterministic latency; "the bitter lesson". Duan [09:51, Gemini transcript only]: "better perception model does not necessarily mean a better final outcome."
- **Scope:** this is a claim about driving quality and scaling. It is not evidence of safety or assurance.

**3. Degeneracy: huge input, two floats out, "99% drive straight".**
- **Verdict:** Supported in substance. The number is off.
- **Evidence:** Duan's slide calls the problem "Massively underconstrained. … Output space: mostly 2 degrees of freedom, steering angle and acceleration." It shows four very different scenes, all labelled `<drive straight>`. Duan [16:53]: "the model just say, okay if I just drive straight, I'll get an answer right for most of the cases."
- **The number:** Duan gives **90%**, not 99%, and in a different context, data curation [26:46]: "If I randomly sample the data back, 90% of data will be driving straight on highway. So they're not useful at all." Tesla calls this "curse of dimensionality" and "underconstrained", not "degeneracy".

**4. Side tasks make the model "show its work", and this solved the degeneracy.**
- **Verdict:** Mostly supported, but overstated.
- **The mechanism:** Duan [17:58]: "proxy tasks that we use as co-training tasks… they really help the gradient flow through the network and we are able to learn the causation of all the driving decisions from the video much, much more precisely." The heads on the slide are action, panoptic segmentation, 3D occupancy, 3D detection, human mesh, keypoint tracking and text recognition. The list covers 14 task types, including optical flow and depth.
- **Where "show its work" comes from:** Elluswamy's framing, not Duan's. Elluswamy's slide reads "Interpretability and safety guarantees: Chain-of-thought and process verification to the rescue." He calls the outputs "reasoning traces."
- **What Tesla does not claim:** that the tasks *solved* the problem ("help"). Curation and RL also carry weight.

**5. Side-task work wasn't wasted, but the on-car model doesn't use most of it.**
- **Verdict:** Supported in substance. The "~90%" is not in the source.
- **Evidence:** Duan [17:58]: the modular-era tasks "come in very handy". Duan [18:48]: action at test time, "But at the training time we predict all the tasks". In the Q&A [24:45–24:59], 3D ground truth comes from existing teacher models.
- **Unresolved:** Elluswamy says language reasoning "can be at test time helping the model make more accurate decisions". What actually runs on the car is not settled by the public record.
- **Separate item:** HW3 "FSD v14 Lite" is press-reported as distilled from the HW4 network (Electrek, 29 June 2026). It is a secondary source and is not the same thing as dropped proxy heads.

**Also in the talks, and highly relevant:**

- **Runtime safety layer (Duan Q&A [25:57]):** "we bake in the collision check during the training through reinforcement learning… the collision check serves as a verifiable reward… [at test time / at Tesla] we actually just mostly rely on the model to do that." The bracketed words are an ASR disagreement: local whisper hears "at test time", Gemini hears "at Tesla".
- **Hardware redundancy (Elluswamy):** two AI4 chips each run a copy of the same network and "keep checking each other". That redundancy covers hardware faults, not a shared functional insufficiency.
- **Evaluation (Elluswamy's slide):** "Even with a high quality dataset, loss isn't a sufficient indicator of performance. Good open-loop performance does not guarantee great closed-loop results… Needs balanced and thorough evaluation sets."
- **World simulator (Elluswamy):** the neural closed-loop simulator is trained on "the same dataset that we can use to train the policy on". Synthetic adversarial cases are made "close to the manifold of data support."

## 3. Independent corroboration of the mechanism

All of these are peer-reviewed or primary research, and none depends on Tesla.

- **PilotNet (Bojarski et al., NVIDIA, arXiv:1604.07316, 2016), §5.1:** "To remove a bias towards driving straight the training data includes a higher proportion of frames that represent road curves." The degeneracy has been known since the first modern end-to-end driving paper.
- **Codevilla et al., "Exploring the Limitations of Behavior Cloning for Autonomous Driving" (arXiv:1904.08980, ICCV 2019), §3.2 and §5:**
  - The "inertia problem": when stopped, "the probability it stays static is indeed overwhelming in the training data. This creates a spurious correlation between low speed and no acceleration."
  - Figure 4 shows the bias can get *worse* with more data.
  - Seed-to-seed variance: "Repeatability of the training process is crucial for enhancing trust in end-to-end models."
  - An auxiliary speed-prediction branch helps "thanks to its regularization effect" but "is, however, not a final solution".
- **Li et al., "Is Ego Status All You Need for Open-Loop End-to-End Autonomous Driving?" (arXiv:2312.03031, CVPR 2024), §1:** "73.9% of the nuScenes data involve scenarios of driving straightforwardly… maintaining the current velocity, direction, or turning rate can be sufficient most of the time." Open-loop planning metrics could be matched without using perception. This is the benchmark-level version of Tesla's `<drive straight>` slide.
- **Waymo EMMA (Hwang et al., arXiv:2410.23262):** "co-training EMMA with planner trajectories, object detection, and road graph tasks yields improvements across all three domains."

## 4. Counter-positions from other leading developers

These are vendor statements, not evidence.

- **Waymo, "Demonstrably Safe AI for Autonomous Driving" (9 Dec 2025):**
  - Waymo's foundation model uses "compact, materialized structured representations like objects, semantic attributes, and roadgraph elements".
  - Teacher models are offboard and distilled into onboard students.
  - A "separate and rigorous onboard validation layer" "verifies the trajectories produced by the Driver's generative ML model."
  - <https://waymo.com/blog/2025/12/demonstrably-safe-ai-for-autonomous-driving/>
- **Waymo, "10 AI Lessons from Driving 200+ Million Fully Autonomous Miles" (Srikanth Thirumalai, 26 Aug 2026):**
  - "Pure end-to-end (E2E) neural architectures… run the risk of black box failures."
  - On the independent onboard validation layer: "This architectural choice is non-negotiable for safely scaling at L4."
  - It calls L2-to-L4 improvement "a false summit".
  - <https://waymo.com/blog/2026/08/10ailessons/>. The Gemini-supplied URL `/10-ai-lessons/` returns 404.
- **Mobileye, "A Safety Architecture for Self-Driving Systems" (Shalev-Shwartz et al., 2024, 17 pp., PDF), §3.2 and §5:**
  - Primary-Guardian-Fallback (PGF) fusion.
  - An end-to-end policy network is used only as a bounded Fallback: "limiting its output to only allow mild braking".
  - In the lane system: "We require that the end-to-end network also outputs the geometry of the most relevant lane." A separate discriminative "lane validator", fed lidar and imaging-radar channels, approves or rejects that lane.
  - <https://static.mobileye.com/website/us/corporate/files/SDS_Safety_Architecture.pdf>

## 5. Does this alter or invalidate the project's direction?

**It does not invalidate it.** It strengthens the core argument and exposes one framing that needs sharpening.

**Why it doesn't invalidate it:**
- Tesla's case for end-to-end is about driving performance and scaling. The paper's question is what evidence lets a learned component take a hazardous action.
- Tesla's own list of the three main challenges includes "interpretability and safety guarantees" and "evaluation". The leading end-to-end developer concedes the problem this project addresses.
- Tesla's evaluation slide independently states the paper's positions: loss and open-loop scores are insufficient, and closed-loop, balanced evaluation is needed. These are the ACAS Xu and partitioned-evaluation lessons.

**What should change:**

1. **The "end-to-end removes the interfaces" sentence is too binary.**
   - Whitepaper §5 "The architecture tension" and episode 2 §5 say an end-to-end design "removes most" evidence-attachment points. In 2026 practice the intermediate representations still exist; their role changed.
   - At Tesla they are training scaffolding and offline diagnostics, not run-time interfaces.
   - At Waymo they are materialized and checked by an onboard validation layer.
   - At Mobileye an end-to-end output is made checkable by an independent guardian.
   - The better engineering question for each intermediate output:
     - Is it in the action's causal path at run time?
     - Does anything independent observe or check it?
     - Is it evaluated as evidence, or only as a training aid?
   - This is more precise than "modular versus end-to-end", and it is what a manager can put to a supplier.
2. **Proxy heads are not interfaces in this paper's sense.**
   - A head sharing an encoder with the action head, whose output does not feed the action, can be right while the action is wrong, and the reverse.
   - Duan says a better proxy metric need not mean better driving [09:51, 28:23–28:40]. Proxy-task accuracy is therefore not safety evidence.
   - Its assurance role is diagnosis and challenge, the "interpretability" row in the paper's method table, bounded by [C-EVID-006].
   - Tesla's "chain-of-thought and process verification" language needs the same boundary. A plausible trace is not shown to be a faithful one.
   - Lead: capture a primary source on chain-of-thought faithfulness before saying this in print. Candidates are Turpin et al. 2023 and Anthropic 2025. Neither was inspected in this pass.
3. **Monitor independence is the real industry split.**
   - Tesla: collision avoidance is trained in via an RL reward and the model is relied on at run time. Its redundancy is two copies of the same network.
   - Waymo: an independent onboard validation layer, called "non-negotiable".
   - Mobileye: guardian and fallback with 2-out-of-3 sensor checks.
   - The paper already says a monitor that shares the perception path shares its blind spot [C-016], and that runtime assurance holds only under its premises [C-EVID-005]. The three developers are a dated, concrete illustration of that lever. This is the strongest use of the Tesla material.
4. **The degeneracy is a gift for the traps table and the video.**
   - Evidence: the `<drive straight>` slide; 90% of random fleet data being straight highway; PilotNet's curve oversampling; Codevilla's inertia problem worsening with data; and 73.9% of nuScenes being straight driving.
   - Together they show why an aggregate score can pass a model that never looked at the road. That is the paper's case for encounter-partitioned evaluation and its averaging point [C-RISK-004].
   - It suits episode 2 or 3 as a visual beat: four scenes, one label.
5. **The deployed artifact must equal the evaluated artifact.**
   - Dropping pure leaf heads leaves the action function unchanged, if the manifest proves the trunk and action head are identical. But nothing auxiliary is then available at run time for monitoring or in-service evidence.
   - A distilled student (HW3 "v14 Lite", press-reported; Waymo's student, per Waymo) is a new function, and teacher evidence does not transfer.
   - The paper's release manifest already covers this. One explicit sentence would help engineers.
6. **The simulator shares a common cause with the policy.**
   - A neural world simulator trained on the policy's own data is weakest exactly where the policy is weakest. Elluswamy himself bounds synthetic cases to near the data manifold.
   - This is a concrete mechanism for the simulator-credibility boundary [C-EVID-003] [C-PRAC-004].
7. **Aviation is unaffected, and the contrast sharpens episode 3.**
   - ED-324 issue 1, as presented, covers non-adaptive supervised ML to DAL C, and reinforcement learning is deferred to issue 2 [C-STAT-002] [C-STAT-003].
   - EASA's proposal excludes AI directly contributing to fatalities [C-CHAL-004].
   - A Tesla-style policy (imitation plus RL fine-tuning, full authority) has no public aviation path. Road and air diverge on architecture because of assurance, not capability.
8. **Keep vendor safety statistics as context.** Tesla's "2x safer" and its 10-billion-mile figures remain context, not evidence, per the technical reference's denominator section. Waymo's "false summit" remark is a competitor's opinion.

## 6. Adjacent lead for the ROAD lane

RDW, 10 April 2026: "RDW explanation of European type approval Tesla with provisional validity in the Netherlands": <https://www.rdw.nl/en/news/2026/rdw-explanation-of-european-type-approval-tesla-with-provisional-validity-in-the-netherlands>.
- It approves "FSD Supervised" as a driver assistance system in which the driver "remains responsible".
- It is currently valid only in the Netherlands, with EU-wide validity pending a Commission and member-state vote.
- It cites more than 1.5 years of track and public-road testing.
- The RDW page itself does not cite the regulation or article. Press reports say UN R171 plus an Article 39 exemption under EU 2018/858; this is unverified.
- The page says nothing about how the learned component was assessed.

This is a live example of a pre-approval regime approving an end-to-end learned L2 function without disclosing learned-component evidence: "permission is not proof" again. If it is used, the paper's road-regime paragraph and the open-items register should be updated.

## 7. Proposed claims (unregistered)

| Proposed ID | Draft text | Source and locator | Kind |
|---|---|---|---|
| C-E2E-001 | In a June 2026 CVPR workshop keynote, a Tesla engineering director described FSD's input as 36 Hz high-resolution video from eight cameras and its output as mostly two degrees of freedom, steering angle and acceleration, and called the problem massively underconstrained. | S-E2E-001, Duan talk 14:37 slide, 15:53–16:20 | vendor statement |
| C-E2E-002 | The same talk illustrated that visually different scenes often share the action "drive straight", and said a naively trained model can learn that driving straight is right for most cases. | S-E2E-001, 16:29–16:58 | vendor statement |
| C-E2E-003 | Tesla described co-training its end-to-end model on modular-era "proxy" tasks (segmentation, occupancy, detection, depth, flow, OCR and others) to aid gradient flow and learning of causation, while at test time the model's output used is the driving action. | S-E2E-001, 17:58–19:04 | vendor statement |
| C-E2E-004 | Asked about a runtime collision-check layer, Tesla's speaker said collision checks are built in during training as a reinforcement-learning verifiable reward and that Tesla mostly relies on the model. | S-E2E-001, 25:57–26:16 | vendor statement |
| C-E2E-005 | Tesla's VP of AI listed interpretability and safety guarantees, and evaluation, as two of three main challenges of learning pixels to control, and stated that good open-loop performance does not guarantee closed-loop results. | S-E2E-002, Elluswamy WAD talk 11:09, 15:53, 18:05 | vendor statement |
| C-E2E-006 | Codevilla et al. identified an "inertia problem" in behavior cloning: a spurious correlation between low speed and no acceleration that more training data did not remove. | S-E2E-003, §3.2, §5, Fig. 4 | peer-reviewed research |
| C-E2E-007 | Li et al. found that 73.9% of nuScenes data involve straight driving and that open-loop planning metrics can be dominated by ego status. | S-E2E-004, §1 | peer-reviewed research |
| C-E2E-008 | Waymo describes a separate onboard validation layer that verifies trajectories from its generative driving model, and calls this choice non-negotiable for L4. | S-E2E-005 and S-E2E-006 | vendor statement |
| C-E2E-009 | Mobileye's published safety architecture uses an end-to-end policy network only as a bounded fallback, and requires it to output lane geometry that an independent guardian network checks with additional sensor channels. | S-E2E-007, §5.1–5.2 | vendor technical paper |

Also consider (NVIDIA research, not Tesla): C-E2E-010. PilotNet oversampled curves "to remove a bias towards driving straight" (§5.1).

## 8. Retrieval log and limits

- **Duan audio:** fetched with a scratch-venv yt-dlp 2026.08.19; the local install, 2026.03.17, could not fetch formats. No captions exist on YouTube. Only two passages were transcribed locally, with faster-whisper *small*; the cached *medium* model is incomplete.
- **Gemini runs:** `gemini-3.8-flash` (D-024) produced the grounded pass (thinking high) and the video transcripts (thinking low, from the YouTube URL). Two claims in the grounded pass were **not** confirmed and must not be used:
  - "FSD v14 Lite at ~15% parameter capacity";
  - the Waymo URL.
  - The grounded pass also missed the Duan talk entirely and attributed the "99%/degeneracy" idea only to academic literature.
- **Secondary sources:**
  - ofweek (7 Aug 2026, Chinese) summarizes the Duan talk and matches the transcript. It is not needed as a source.
  - thinkautonomous.ai reproduces the "Video Foundation Model" slide.
- **Not inspected:** Elluswamy's ICCV 2025 X thread; chain-of-thought faithfulness papers; the primary basis of Tesla's HW3 distillation.

### Snapshot hashes (SHA-256, under the `out/` directory above)

```
5e8c1d2d34164add13ddd433104ea3498e5a590548e8745108b91cd11f04b082  duan_cvpr2026_drivex.md (Gemini transcript)
247191d3739fbf87ca12b327a7e2d4c936f82adb8a74b1c46d57fe4201d67d6b  elluswamy_cvpr2026_wad.md (Gemini transcript)
ddd98ec3e3786dad387c4a85ebb21d8ed4e5d2bbf8d3f55b230298d60c0bcd2d  grounded_response.md (Gemini grounded pass)
732f6cce215803ba3cf9c5d3f5e18ca14485ca5759b79c5d363b75b70b75a48b  snapshots/duan_cvpr2026_14m00-19m30_fasterwhisper-small.txt
080aaa8a442c782eb834bc4c015730b3ea3707975f4fbb7a4d8045f0d35d2dc1  snapshots/duan_cvpr2026_25m30-29m10_fasterwhisper-small.txt
1be2d560d0934954843e55f0d4e41b29d804fc23d43a86c3bcdd1a756dc76bff  snapshots/elluswamy_wdfm-eai_youtube-autocaptions.txt
c02b15a05434388b443b8f9a89ac37821eec91b9cd305c2c63ffa51fa2fdb123  snapshots/pilotnet_1604.07316.pdf
263508045450e05e3bd3f6a9fce6d5b240d17a728dd268c59eed1b868a716ed8  snapshots/codevilla_1904.08980.pdf
c289b8904ce05ee3503dd67d3765d9d93da61493a4cf6c2c861a08f4466e7899  snapshots/li_egostatus_2312.03031.pdf
ffd8a4ef41ba356ae1bd9243ed3c5be40652bfb5ed30e7d8a4c2fe2a617c6c84  snapshots/mobileye_sds_safety_architecture.pdf
```
