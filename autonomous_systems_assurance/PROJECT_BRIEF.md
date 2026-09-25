# Project brief

The previous project asked how to organize verification of software and its artifacts when AI makes generation cheap. This project asks how to build an assurance argument when learned behavior is inside the operational system itself.

The research should produce a practical architecture whose evidence obligations a reader can inspect. Start with a car perceiving its surroundings, navigating and avoiding a hazard. Toward the end, let that same visual vehicle take off and ask which assumptions actually change. The argument must survive the difficult aviation case: detect an aircraft soon enough to select and execute an avoidance maneuver, including when a camera misses it, acoustic conditions change, or sensors disagree.

## Working thesis — a proposal to test

Assurance must cover the chain from operating assumptions and sensor information through learned behavior, decision authority, fallback, and change control. Traceability can organize that evidence, but cannot supply missing evidence about what happens in the world.

The first assurance target is a **frozen, versioned trained model**: training may be stochastic, but the released inference behavior and its configuration are controlled. A system that changes its model during operation is a distinct, harder case. It belongs in the comparison and future-work discussion, not in the first claim of adequacy.

The project does not begin from an assurance vacuum. It will use AMLAS as a public learned-component lifecycle baseline, compare it with case-specific military guidance and proposed civil methods, then make the missing system, operational and authority evidence visible in a worked road-to-air case. [C-CHAL-001] [C-CHAL-003] [C-CHAL-006]

Do not preselect the conclusion that interpretability solves certification, that aviation prohibits AI, that cars have no assurance obligations, or that a safety monitor can always rescue a bad perception result.

## Outputs

1. A whitepaper with a worked assurance case, primary-source support, competing architectures, unresolved obligations, and a dated regulatory comparison.
2. An accessible narrated video that introduces the practical mechanism within 15–20 seconds, develops it through a car's perception and avoidance, then carries the architecture into flight.
3. A public resource package containing readable and agent-usable versions, source/claim traceability, bounded review records, architecture diagrams, and reproducible demonstrations if developed.
4. A small verification compiler plus maintained wiki that makes changes and unsupported claims visible across all three outputs.

## Scope

- DAA sensing: camera, microphone array, radar, cooperative surveillance, fusion, uncertainty, latency, false negatives and false positives.
- Learned perception versus learned planning/control; frozen models versus in-service adaptation.
- Aviation equipment, installation, aircraft and operational approvals; military versus civil scope.
- US autonomous-road-vehicle compliance, state deployment permissions and passenger-service permissions, with FAA/EASA/UK material explicitly scoped.
- Data and learning assurance, scenario evidence, simulation validity, formal methods, runtime assurance, interpretability, compression and symbolic system identification.
- Accountability for retraining, changes to sensor hardware, software, environment, and the operational domain.

## Initial exclusions

No attempt to certify a real vehicle, infer private model internals, reproduce proprietary DAA designs, or pronounce an investigated product unsafe from the existence of an investigation. No claims of exhaustive worldwide certification coverage from a web search.

## Definition of a useful first milestone

A reviewer can inspect a road encounter and its aviation counterpart, their assumptions, competing architectural responses, the evidence each would need, and failures that defeat each response. The paper and video should share that worked example without requiring the audience to learn our production tooling. The result is a proposed, inspectable assurance case for a bounded trained-model role; it is not a declaration that a universal certification recipe already exists or a claim about a proprietary vehicle's evidence.

Levi's DAA experience is approximately five years old. Treat it as motivation and a source of questions, not evidence of present capabilities. No employer or program names were supplied for publication.
