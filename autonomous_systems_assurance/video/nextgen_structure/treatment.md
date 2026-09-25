# Video treatment: *Can We Build a Safety Case for a Machine That Learned?*

**Provisional runtime:** 34:00, excluding end screen.  
**Audience:** technical generalists and engineers.  
**Form:** a visual explanatory essay that starts with one road encounter, follows the evidence problem outward into standards and risk, then returns to a constructive road-to-air assurance architecture.  
**Claim baseline:** existing project claims only, all currently provisional.  
**Not a product assessment:** no named vehicle, aircraft, operator, or DAA product is presented as safe, unsafe, certified, or approved by implication.

## The promise in the first 20 seconds

A car approaches a partly hidden road user. Its learned perception system says the lane is clear. The deterministic planner then does exactly what it was designed to do: maintain the planned path. A safety monitor receives the same incomplete world state. It agrees. The core mechanism is on screen before the title:

> A learned model can be frozen, tested, and versioned. But if the critical object is missing from every input the decision system sees, no downstream deterministic box can recover that missing information. The question is not “is the neural network magic?” It is: what evidence lets it take this action in this operating domain? [C-016] [C-METHOD2-019]

This is a project reasoning example under a shared-input failure assumption. It is neither a reconstruction of a real crash nor a statement about a named company.

## Editorial thesis

Conventional assurance can trace a designed implementation down through lower-level requirements. For a trained model, the learned weights are implementation details that engineers did not write as requirements; the FAA identifies the resulting break in direct lower-level requirement traceability. [C-AUTH-010] The response is not a single accuracy number, a pile of driving miles, an interpretability picture, or a monitor drawn beside the model. It is an inspectable **evidence bridge**: bounded operation, sensing limits, exact release, scenario-conditioned performance, closed-loop margin, useful intervention, whole-system composition, and change control. This bridge is the project’s proposal. [C-015] [C-METHOD2-018]

The film does not claim that no methods exist. AMLAS is a public ML-component assurance method; the UK MAA has a case-specific military path; EASA has proposed detailed civil material; road standards and voluntary safety-case material exist. Their status, scope, and gaps differ. [C-CHAL-001] [C-CHAL-003] [C-CHAL-004] [C-CHAL-006] [C-AUTH-006] [C-AUTH-007]

## Viewer journey

| Time | Section | What the viewer understands on exit | Evidence posture |
|---:|---|---|---|
| 00:00–02:30 | **1. The missing object** | A monitor that receives the same blind world model may share the model’s failure. | Project reasoning, explicitly conditional. [C-016] |
| 02:30–06:30 | **2. Why trained implementation changes the assurance task** | Requirements and conventional engineering still matter; direct requirement-to-weight explanation is the gap. | FAA framing; limited to learned-AI discussion. [C-AUTH-010] [C-AUTH-002] |
| 06:30–10:30 | **3. What “allowed to operate” actually means** | An operating permission, equipment authorization, installation approval, and model evidence answer different questions. | Scope-controlled road and aviation examples. [C-INTAKE-003] [C-ROAD2-014] |
| 10:30–16:00 | **4. The standards landscape is structure, not a finished answer** | AMLAS, MAA, EASA, ISO/PAS 8800, UL 4600, and NHTSA material meet different parts of the problem. | Document status and jurisdiction remain on screen. [C-CHAL-001] [C-CHAL-003] [C-CHAL-006] [C-AUTH-006] [C-AUTH-008] |
| 16:00–21:30 | **5. Risk evidence is conditional** | Testing, coverage, simulation, calibration and inspection inform a case but do not each yield a general safety probability. | Method limits lead every metric. [C-EVID-002]–[C-EVID-007] |
| 21:30–27:30 | **6. Wrap the learned component in evidence-bearing safety layers** | Bounded authority and runtime assurance help only when sensing, timing and recovery premises hold. | Conditional RTA research plus project architecture. [C-EVID-005] [C-METHOD2-003] [C-METHOD2-019] |
| 27:30–32:00 | **7. Let the car take off** | The same questions transfer to DAA, while time, sensing, recovery and approval layers change. | Hypothetical comparison; careful DAA scope. [C-AIR2-001] [C-AIR2-003] [C-INTAKE-003] |
| 32:00–34:00 | **8. The proposed evidence graph** | A safety case is a collection of challengeable links, not an AI safety score. | Project proposal and compiler process. [C-015] [C-METHOD2-018] |

## Story structure

### 1. Begin with a failure of information, not a lecture about AI

The first scene makes the issue concrete. Two physical worlds look identical to the planner: in one the near lane is empty; in the other an occluded actor exists. The precise claim is narrow: if the monitor and planner depend only on that same failed perception output, they cannot use it to distinguish the worlds. [C-016] The viewer sees why adding a deterministic supervisor may be necessary but cannot automatically be sufficient.

This avoids an unhelpful “AI is nondeterministic” premise. The initial target is a frozen, versioned trained model. Stochastic training is distinct from a model that keeps learning in operation, and an updated learned model needs a new safety-assurance treatment. [C-AUTH-002] [C-AIR2-007]

### 2. Explain the gap in plain engineering language

Use the FAA framing to show three columns: designed implementation, learned implementation, and the proposed evidence bridge. In conventional systems, a team can derive lower-level implementation requirements and connect them to higher-level requirements. The FAA says the same direct derivation and coverage explanation does not describe a learned algorithm’s weights. [C-AUTH-010]

The film immediately prevents an overstatement: the aircraft/vehicle requirements, sensors, compute platform, interfaces, conventional control software, and operational limitations still need ordinary engineering evidence. The problem is not that all traceability disappeared. The problem is that a trained component needs additional kinds of evidence for the behaviors that its weights encode. [C-AUTH-010]

### 3. Separate access from proof

The road chapter uses a simple “permission stack,” rather than treating a robotaxi story as a verdict on any model. The current project evidence says that Texas commercial authorization, California DMV permit types, CPUC passenger-service layers, NHTSA federal compliance activity, and a product’s learned-behavior evidence are separate matters. [C-ROAD2-001] [C-ROAD2-006] [C-ROAD2-008] [C-ROAD2-014] A dated Cybercab inquiry is a useful example of self-certification being examined, not a safety conclusion. [C-ROAD2-004] [C-ROAD2-005]

The aviation version is sharper: an FAA Technical Standard Order establishes an article’s minimum-performance authorization for manufacture; it is distinct from installation approval and operation. [C-INTAKE-003] [C-AIR2-004] A visible product page or a public operational permission cannot be used to infer the contents of its learned-model safety case. [C-AIR2-003] [C-INTAKE-001]

### 4. Make the standards landscape legible

The center of the film is a map, not a ranking. AMLAS provides a six-stage ML-component assurance lifecycle but says it is not sufficient alone and focuses primarily on offline supervised learning. [C-CHAL-006] The UK MAA notice is a current, applicant-specific military path that recommends fixed supervised models in a defined ODD for early safety-related applications and retains architectural mitigation where prescriptive resolution is unavailable. [C-CHAL-001] [C-CHAL-002]

EASA’s detailed NPA 2025-07(B) is proposed, not final. It spans operational domain, risk assessment, development assurance, supervised-ML learning assurance, lifecycle data and in-service monitoring. Its stated scope boundary matters for the most demanding imagined flight use, but a real function would require an aircraft-level failure-condition allocation before the boundary is applied. [C-CHAL-003] [C-CHAL-004] Road material has its own structure: ISO/PAS 8800’s public scope includes trained AI models and safety-assurance claims; UL 4600 describes a goal-based autonomous-product safety argument; NHTSA ADS material is voluntary, not federal approval. [C-AUTH-006] [C-AUTH-007] [C-AUTH-008]

The conclusion is deliberately modest: existing material refutes an assurance vacuum. The public record in this project has not yet produced a final, publicly inspectable civil lifecycle that closes the highest-consequence hypothetical case; that is a dated, bounded retrieval finding, not evidence about private programs or every jurisdiction. [C-CHAL-003] [C-CHAL-004] [C-CHAL-006]

### 5. Reframe probability as an evidence question

The risk chapter treats probability as conditional bookkeeping, not a magic threshold. A rare-event result estimates a selected risk only under its simulator, traffic distribution, and hazard threshold. [C-EVID-003] Scenario coverage tells us about selected scenario factors; calibration tells us whether a confidence score matched outcomes on a tested distribution; neither proves safe operation by itself. [C-EVID-002] [C-EVID-004]

Interpretability and neuron-coverage visuals are introduced here, after the viewer knows what they would need to prove. Saliency can look persuasive without reliably explaining the model, and the inspected neuron-coverage study does not establish a consistent causal test-adequacy measure. [C-EVID-006] [C-EVID-007] Formal neural-network verification and model reduction are worth showing as bounded tools, because their guarantees depend on plant, abstraction, model and data assumptions. [C-METHOD2-013] [C-METHOD2-015]

No current project claim supports an accident-rate comparison of electric cars, a universal model-safety probability, a DAL mapping for trained components, or a present FAA acceptable-risk threshold for AI. Those topics remain research cards rather than narration.

### 6. Build the safety layers, then test their weakest link

This is the film’s constructive heart. The learned component does not sit alone in a binary “trusted/untrusted” box. It sits inside layers that each carry a different proof obligation:

1. operational limits and hazard allocation;
2. sensing and health evidence;
3. a frozen, identified learned release;
4. uncertainty and authority restrictions;
5. constrained decision and deterministic control limits;
6. a monitor with relevant observations and bounded timing;
7. a recovery controller with a reachable safe state; and
8. change control that reopens affected evidence.

This is a project proposal based on the evidence-contract architecture. [C-015] [C-METHOD2-018] A Simplex-style pattern permits an advanced component to act while a monitor can transfer authority to a trusted controller. The actual safety implication requires stated safe-start, monitor/timing, recovery-state and fallback-controller premises. [C-METHOD2-001] [C-METHOD2-003] [C-EVID-005]

The decisive visual uses nested shells and then breaks one shell at a time. A deterministic safety controller may constrain allowed actions; it does not create an unseen aircraft, pedestrian, or obstacle. If the relevant difference cannot be observed early enough, the honest response is to restrict the ODD or authority, improve the independent-enough observation path, or block release. [C-016] [C-METHOD2-019]

### 7. Carry the same graph into flight

The car rises from a road cross-section into an airspace diagram while its eight evidence nodes stay visible. The viewer sees what changes: closing speeds, separation rather than stopping distance, cooperative/noncooperative traffic, tracking and alert latency, maneuver envelope, and the fact that a landing is not an immediate collision-avoidance response. These are features of the project’s hypothetical comparison, not comparative safety rankings. [C-015]

The film can show that GA-ASI publicly describes a DAA architecture with cooperative surveillance sources and air-to-air radar for noncooperative traffic. [C-AIR2-001] It must then immediately keep the scope card on screen: the inspected public pages did not establish a DAA/ATAR TSO authorization, and in any case a TSO is distinct from installation and operation. [C-AIR2-003] [C-INTAKE-003] A scoped BVLOS authorization likewise does not establish an unrestricted DAA equipment authorization. [C-AIR2-012] [C-INTAKE-001]

### 8. End with a useful standard of progress

The ending replaces “when will AI be certified?” with a sharper question: **which observable condition and which recovery margin would let this exact, versioned system take this action in this domain?** An evidence graph makes every answer inspectable: hazard, assumption, model release, scenario evidence, monitor premise, recovery premise, authority scope, source, and change impact. [C-015] [C-METHOD2-018]

The paper’s verification compiler is mentioned only as a transparency device. It can tell us when the project’s source context, claim wording, diagram, and narration have diverged. It does not calculate safety, grant approval, or replace authority review.

## Tone and language rules

- Say **trained model** or **learned component**, unless discussing actual in-service learning. Avoid treating stochastic training as random deployed execution. [C-AUTH-002]
- Say **scope**, **evidence**, **assumption**, **premise**, and **open obligation** before using specialist terms such as ODD, TEVV, runtime assurance, or traceability.
- When a document is proposed, voluntary, military-only, product-specific, or dated, show that modifier in the voiceover and on the source card. [C-CHAL-001] [C-CHAL-003] [C-AUTH-008]
- Make uncertainty visual. Grey dotted edges mean “not yet demonstrated,” not “low confidence.”
- Do not call the project’s evidence graph a standard, method of compliance, certification recipe, score, or proof that a model is safe.

## Research-dependent sections that must remain placeholders

| Desired topic | What existing claims safely support | What is still needed before factual narration |
|---|---|---|
| “No formal method exists” | FAA’s 2024 roadmap said industry lacked an AI safety-assurance method; AMLAS/MAA/EASA show methods and candidate paths exist. [C-AUTH-001] [C-CHAL-001] [C-CHAL-003] [C-CHAL-006] | Dated primary-source search for final standards, accepted means of compliance and public certification bases. |
| Automotive barrier versus aviation barrier | Different US road authorization/self-certification/permit layers and aviation article/installation/operation layers. [C-ROAD2-014] [C-INTAKE-003] | A careful comparative legal/regulatory analysis; do not describe one as objectively “lower” without defined criterion. |
| Why standards development is slow or lacks experienced people | Nothing suitable for that causal claim. | Primary standards-body, regulator or industry evidence; interviews would need attribution and review. |
| DALs, acceptable-risk thresholds and AI roles currently permitted/off-limits | EASA proposal has a scope exclusion; FAA roadmap is a research/roadmap document. [C-CHAL-004] [C-AUTH-001] | Authoritative certification/safety assessment material and a scoped mapping to the hypothetical function. |
| Electric-car accident rates | Nothing in current claim set. | A clear numerator/denominator/ODD comparison using primary crash and exposure data; distinguish EV powertrain from ADS. |
| Tesla internal vector layers or learned-model assurance | Public Tesla architecture description only. [C-ROAD2-010] | Do not infer private internal validation, certification evidence, or Cybercab-specific implementation. |
