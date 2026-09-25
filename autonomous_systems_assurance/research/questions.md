# Research questions and evidence needed

| Workstream | Question | Evidence that would resolve it |
|---|---|---|
| Road perception | What does a representative autonomy stack estimate, and what uncertainty survives into planning? | Versioned technical papers and documented sensor/planner interfaces; avoid inferring a deployed stack from a demo |
| Approval taxonomy | Exactly what was authorized, for whom, where, and subject to what limitations? | Decision/grant, revision, jurisdiction, hardware/software configuration and ODD |
| GA-ASI | Were C211/C212 authorizations issued, for which models, and when? | FAA authorization records; independent authority confirmation; distinguish aircraft MTC |
| Other DAA | Which systems use radar, acoustic or camera perception in permitted operations? | FAA exemption/waiver letters and technical records; investigate Zipline, Iris/Casia, ACAS Xu and ground-based DAA separately |
| Cars | What do federal self-certification, Texas operational permission, California permits and CPUC authority each establish? | Current primary rules and individual dated grants; separate FSD supervision from Cybercab operations |
| Learning | What changes when the deployed model is frozen, retrained offline or adapts during a mission? | FAA/EASA guidance, assurance lifecycle records and change/revalidation examples |
| Lifecycle crosswalk | Which project evidence contracts are covered by AMLAS, MAA case-specific guidance and EASA's proposed DS.AI, and where do their scopes stop? | Exact artefact/objective mapping, document status, hazard/authority boundary and contrary review; do not conflate proposal, guidance and approval |
| Aviation baseline | Which system-level objectives sit above software assurance? | Current ARP4754/ARP4761 and authority guidance; licensed access limits explicit |
| Data | What defines representative coverage rather than merely dataset size? | ODD/scenario taxonomy, provenance, splits, leakage analysis, sensor conditions and rare encounters |
| Testing | What do simulation and operational statistics establish? | Simulator validation, encounter distributions, dependence assumptions, exposure and uncertainty intervals |
| Formal assurance | Which exact properties are provable and under which models/input sets? | Property statements, proof obligations, counterexamples and implementation correspondence |
| Runtime assurance | Can the monitor detect danger before recovery becomes impossible? | Sensor observability, error/latency bounds, reachable safe set and fallback authority |
| Sensor fusion | How does shared weather, occlusion or bad calibration affect apparently diverse channels? | Common-cause analysis, disagreement behavior and fault-injection/encounter evidence |
| Interpretability | Does an explanation predict failures under intervention? | Causal tests, held-out environments, false reassurance cases and coverage limitations |
| Simplification | Does compression preserve rare safety-relevant behavior? | Distillation/pruning counterexamples, property-preservation arguments and retesting |
| Physics discovery | Under what conditions can compact equations replace learned behavior? | SINDy/symbolic regression identification assumptions and out-of-sample validation |
| Taking off | Which assumptions change from road avoidance to air conflict avoidance? | Matched scenarios with explicit dynamics, sensing, traffic cooperation and fallback conditions |

Prioritize original research and authority records. Track counterevidence and unsuccessful searches. Fetch standard editions and clause text before assigning compliance obligations. Do not turn a minimum performance standard number into a universal probability-of-safety requirement.
