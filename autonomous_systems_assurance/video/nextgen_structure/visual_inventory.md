# Visual and diagram inventory — long-form learned-systems assurance video

**Status:** design specification only. All diagrams are project proposals unless a claim tag identifies a factual source-backed statement. No visual may imply approval, certification, measured reliability, independence, or a safety probability without a reviewed claim and explicit scope.

## Visual grammar

| Element | Meaning | Do not let it imply |
|---|---|---|
| Solid blue node | Declared component or evidence object | Sufficient evidence or certification |
| Green solid edge | Evidence link currently asserted by a source or project proposal | A completed review or closed obligation |
| Amber dashed edge | Assumption, premise, planned evidence, or limited source status | A quantified confidence value |
| Red pulse | Defeating trace / hazard propagating through the system | A real incident reconstruction |
| Grey shell | Context or conventional system layer | Independence from the learned component |
| Hash label | Frozen model/release identity | Assurance completion |
| Source-status card | Published / proposed / voluntary / military / historical / vendor | A hierarchy of safety quality |

The rendering uses plain language in the first half. Technical terms appear only after the picture has introduced their role.

## Primary diagram inventory

| ID | Time | Diagram | Narrative job | Claim/support | Review limits |
|---|---:|---|---|---|---|
| VNG-01 | 00:00 | **Two worlds / same system state** | Establish shared-input monitor failure in the hook. | Project reasoning [C-016] | Label illustrative; no real product or incident. |
| VNG-02 | 02:30 | **Designed chain → learned implementation → evidence bridge** | Explain FAA traceability framing without claiming all traceability vanishes. | [C-AUTH-010] | Keep “FAA framing” and source title in lower third. |
| VNG-03 | 06:30 | **Road permission stack** | Separate authorization/permit/service/compliance/evidence. | [C-ROAD2-001] [C-ROAD2-006] [C-ROAD2-008] [C-ROAD2-014] | Date/state cards; never use stack height as safety ranking. |
| VNG-04 | 10:30 | **Authority-and-risk coverage map** | Show AMLAS, MAA, FAA, EASA and NHTSA as different coverage shapes, then show EASA’s proposed authority/risk boundary. | [C-RISK-006] [C-RISK-007] [C-CHAL-001] [C-CHAL-006] [C-AUTH-010] [C-DIR-003] | Proposed and military labels must persist. Level 3B is reserved, not an approved no-human category. A colored risk cell is not approval. |
| VNG-05 | 16:00 | **Conditional-risk ledger** | Explain why inputs travel with a simulation/risk estimate. | [C-EVID-003] | No numerical result unless new source/evidence is added. |
| VNG-06 | 17:40 | **Metric lenses** | Separate coverage, calibration, interpretability, formal verification, and their limits. | [C-EVID-002] [C-EVID-004] [C-EVID-006] [C-EVID-007] [C-METHOD2-013] | Never display lens outputs as one score. |
| VNG-07 | 21:30 | **Certified-stack shells** | Show learned component within a safety-critical system and expose each evidence obligation. | Project proposal [C-015] [C-METHOD2-018] | It is not a claim that a real stack is certified or that a shell guarantees safety. |
| VNG-08 | 24:30 | **Deterministic wrapper stress test** | Show monitor/recovery premises and why shared blindness defeats the wrapper. | [C-EVID-005] [C-METHOD2-003] [C-016] | “Deterministic” is not synonymous with safe. |
| VNG-09 | 27:30 | **Road-to-air invariant graph** | Carry evidence contracts into flight and change assumptions one by one. | Project comparison [C-015] | No road-versus-air safety ranking. |
| VNG-10 | 29:40 | **DAA approval scope ladder** | Separate architecture, equipment, installation, aircraft, operational authorization. | [C-AIR2-001] [C-AIR2-003] [C-INTAKE-003] | Do not imply GA-ASI approval status beyond exact claims. |
| VNG-11 | 32:00 | **Change-impact graph** | Show a changed model/sensor/ODD reopening specific evidence links. | Project proposal [C-015] [C-METHOD2-018] | No “compiler certifies safety” language. |

## VNG-04: authority-and-risk coverage map — detailed specification

### Purpose

Make the phrase “unfinished and fragmented public pathway” visible without claiming an assurance vacuum or presenting any source as a safety league table. The visual begins with each document's role, then enlarges EASA's proposed boundary because it is the source in the retained corpus that makes both delegated authority and a scenario-risk matrix explicit.

### Animation sequence

1. Place **AMLAS** as a component-lifecycle band. Its boundary stops before whole-system authority, operation and approval. [C-CHAL-006]
2. Place the **UK MAA notice** as a military, applicant-specific band for fixed supervised models in a defined operating domain. [C-CHAL-001]
3. Place the **FAA roadmap** as a research/problem-framing band. It explains why learned implementation adds evidence needs; do not draw it as a final acceptance process. [C-AUTH-010] [C-RISK-002]
4. Place **NHTSA incident reporting** as oversight/discovery data. Its data dictionary visibly carries the labels *incomplete/unverified*, *possible duplicate reports*, and *not normalized*. [C-DIR-003]
5. Zoom to **EASA proposed DS.AI**. Reveal Levels 1A–3A, then stop at a locked amber/red Level 3B card labelled **reserved**. [C-RISK-006]
6. Reveal the risk grid. H1/potential-fatality cells are all red/unacceptable in this proposal. State the operational-hour likelihood bands in voice and hold a persistent **PROPOSED — NOT AN APPROVAL RULE** chip. [C-RISK-007]
7. Finish on the proposed project evidence graph, with dashed edges for release-specific evidence still required.

### Non-negotiable visual labels

- `EASA NPA 2025-07(B) — PROPOSED`
- `Level 3B — RESERVED (no authority/responsibility assigned)`
- `H1 potential fatalities — unacceptable in this proposed matrix`
- `Incident reports ≠ normalized crash rate`
- `Project evidence graph — proposal, not certification`

Do not use **“AI is not accepted”**, **“Level 3B is banned”**, **“the green cells are safe”**, or **“NHTSA incident counts prove a crash rate.”**

## VNG-07: certified-stack shells — detailed specification

### Purpose

Give the viewer a correct mental model: the learned component is **inside** a larger system already subject to ordinary engineering and operational constraints. The visual is titled **“Proposed assurance layers for a trained component”**, not “the certified AI stack.” The requested phrase “certified stack” describes the visual context, but the image must not assert certification of the hypothetical stack.

### Static layout

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│  1. Operation and hazard boundary                                            │
│  ODD • operating rules • hazard allocation • allowed decision authority      │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ 2. Physical platform and conventional assurance                         │  │
│  │ sensors • compute • actuators • deterministic constraints • dynamics  │  │
│  │ ┌───────────────────────────────────────────────────────────────────┐ │  │
│  │ │ 3. Sensing and health evidence                                     │ │  │
│  │ │ calibration • latency • degradation • common-cause analysis        │ │  │
│  │ │ ┌───────────────────────────────────────────────────────────────┐ │ │  │
│  │ │ │ 4. Frozen learned release                                      │ │ │  │
│  │ │ │ data lineage • learning configuration • weights • interfaces   │ │ │  │
│  │ │ │ ┌───────────────────────────────────────────────────────────┐ │ │ │  │
│  │ │ │ │ 5. Authority and action constraints                        │ │ │ │  │
│  │ │ │ │ uncertainty policy • planner envelope • deterministic ctrl │ │ │ │  │
│  │ │ │ └───────────────────────────────────────────────────────────┘ │ │ │  │
│  │ │ └───────────────────────────────────────────────────────────────┘ │ │  │
│  │ └───────────────────────────────────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│  6. Monitor / switch / recovery / in-service change control cross-cut layers │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Animation sequence

1. **Start from the center.** A model hash and “perception output” appear. Voice says it is a frozen release, not an online learner. [C-AUTH-002]
2. **Grow outward one shell at a time.** Each shell asks a single plain-language question: “what does it see?”, “what is it allowed to decide?”, “what happens when it is wrong?”
3. **Overlay the evidence bridge.** Small tags map shells to `O-001` through `O-008`, but numbers appear after the simple question has landed. [C-015]
4. **Animate a red occlusion trace.** It enters through sensing, crosses perception and planner, then stops at a monitor sharing the same state. The monitor shell turns amber: *observation premise open.* [C-016]
5. **Show three possible responses, none automatically sufficient:** another observation path, lower authority/restricted ODD, or block release. [C-METHOD2-019]
6. **End with version change.** A new model hash changes the frozen release shell, turns data/performance/monitor evidence edges amber, and introduces change-impact review. [C-AUTH-002] [C-METHOD2-018]

### Evidence-meaning guardrails

- The platform shell is not a claim that the sensors, actuation, controller or vehicle are already certified.
- The learned-release shell is not a claim that version control proves behavioral safety.
- The authority shell must explicitly say “proposed restriction,” unless a later real system evidence package exists.
- The monitor shell must show assumptions: relevant observation, detection time, switch time, recovery state, and controller capability. [C-EVID-005]
- Do not use independent-looking spatial separation to imply sensor independence. The diagram shows a dashed **shared failure analysis required** link wherever monitoring draws on common sensing. [C-016]

## VNG-08: deterministic safety wrapper — detailed specification

### Core picture

```text
environment → sensors → learned perception → world state → advanced planner ─┐
                  │                                         │                │
                  ├── safety observations → monitor ─────────┴→ authority ───→ actuation
                  │                                      ▲
                  └──── shared-cause / missing-object analysis required      │
                                                                recovery ctrl ─┘
```

### Three animated cases

| Case | What changes | Correct takeaway |
|---|---|---|
| A. Observable early | Safety observation identifies the relevant hazard with enough margin; monitor switches; recovery remains feasible. | A runtime-assurance argument can begin only after its premises are demonstrated. [C-EVID-005] |
| B. Detected too late | The model or monitor eventually detects the object, but no recoverable state remains. | Correct detection alone does not establish safe closed-loop outcome. [C-METHOD2-003] |
| C. Shared blind spot | Monitor uses the same absent world-state fact as the planner. | No downstream deterministic logic can react differently to indistinguishable inputs. [C-016] |

Use **“conditional runtime assurance”**, not **“failsafe shell.”** The advanced/planner controller can be represented as learned or conventional only when the narration identifies which case is being discussed; do not imply the cited RTA research validates a specific autonomy architecture.

## VNG-05: certainty, reliability, safety — the requested graph without a false composite

The user requested a graph of tradeoffs between certainty, reliability, and safety. The video should **not** draw a triangle that suggests a universal conversion between them. Instead, render a three-panel dependency graph:

```text
scenario partition + release + sensor configuration
             │
             ├──► measured reliability / error evidence
             │
             ├──► uncertainty / calibration evidence ──► authority restriction policy
             │
             └──► hazard + time + dynamics + recovery margin ──► safety argument
```

**Narration meaning:** Reliability is observed behavior under defined conditions. Certainty is the system’s estimated uncertainty/calibration under a defined evaluation setting. Safety is a system-level claim that depends on the hazard, allowed action, timing, dynamics, and recovery as well as component behavior. [C-EVID-003] [C-EVID-004] [C-EVID-005]

The only line that joins all panels is an amber evidence edge, not a formula. A metric may strengthen a particular premise while leaving the overall claim open.

## Supporting visual inventory

| Asset | Use | Source/rights status |
|---|---|---|
| Existing learned-traceability-gap SVG | Opening Section 2 reference; rebuild as video-native geometry later. | Project-created. [C-AUTH-010] |
| Existing evidence-bridge-ladder SVG | Reuse its six plain-language questions, then expand to eight contracts. | Project-created; proposal. |
| Road occlusion scene | Hook, monitor test, ODD restriction explanation. | Original deterministic illustration; must label illustrative. |
| Standards status cards | Method chapter. | Original typography using source titles/status; cite exact project claims. |
| Conditional simulation ledger | Probability chapter. | Original explanatory diagram; no numeric risk claim. |
| Generic model evaluation plot | Teach ROC/confusion-matrix grammar only if helpful. | Original synthetic data or licensed/new source; do not borrow the supplied medical figure as autonomy evidence. |
| Road-to-air morph | Transfer chapter. | Original deterministic animation; hypothetical. |
| DAA layer ladder | Approval-scope distinction. | Original diagram based on precise scope claims. |

## Render and review requirements for later production

1. For every frame that contains a factual label, retain its claim ID in the scene manifest and source card metadata.
2. Keep persistent status chips for **proposed**, **military**, **voluntary**, **historical**, **vendor-described**, and **not established by inspected source**.
3. Run visual review on settled frames and transitions: the road-to-air morph, nested-shell reveal, common-cause arrow, and DAA approval ladder are semantically dense.
4. Test readability at phone width and 1080p. The eight-contract graph must split into two beats if labels become less legible than narration.
5. No visual uses colored “green” to mean safe, approved, or release-ready. Green only denotes a described/claimed evidence link; its source-status card still governs meaning.
