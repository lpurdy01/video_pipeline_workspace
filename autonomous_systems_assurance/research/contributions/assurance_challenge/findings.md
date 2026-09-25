# Independent challenge findings

## Result

The broad idea that assurance practice contains only disconnected fragments is **too strong**. Three substantial public baselines exist:

1. The UK MAA has a current, effective AI guidance path for military safety-related aviation systems. It calls for applicant-specific MCRI agreement, a defined operating context and evidence proportionate to risk. It recommends frozen supervised models and traditional safety-monitor architecture for early applications. [C-CHAL-001]
2. EASA has proposed a much more detailed civil framework: operational domain, risk assessment, system development assurance, learning assurance, configuration/life-cycle data and in-service monitoring. [C-CHAL-003]
3. AMLAS already supplies a public six-stage ML-component assurance methodology and safety-case patterns. [C-CHAL-006]

Those findings change the project. It should **not** present its evidence-contract architecture as the first lifecycle for trained learned systems.

## What did not defeat the narrower gap

No inspected source supplies a final, publicly inspectable, one-size-fits-all civil certification lifecycle for the project's hardest case: a trained model whose failure contributes directly to a potentially catastrophic autonomous flight decision.

- The MAA route is military, case-specific, and explicitly non-prescriptive where architectural mitigation is needed. [C-CHAL-001] [C-CHAL-002]
- EASA DS.AI is an NPA, not final material. It is confined to Level 1/2 cases and expressly excludes systems directly contributing to fatalities or multiple life-threatening injuries. [C-CHAL-003] [C-CHAL-004]
- The proposed EASA material refers to ED-324/ARP6983 for supervised-ML learning assurance, but EUROCAE's own current status page lists ED-324 as a draft targeted for publication on 31 December 2026. [C-CHAL-005]
- AMLAS explicitly needs complementary system and domain assurance and does not demonstrate regulator acceptance or a specific aircraft/vehicle approval. [C-CHAL-006]

This supports a defensible, carefully limited eventual finding: **within this dated, public search, we found mature assurance methods and authority pathways, but not a final publicly inspectable civil lifecycle that closes the hardest high-criticality trained-model case.** It does not support the claim that no such process exists.

## Required change to the project framing

Treat AMLAS as the baseline for the learned-component lifecycle. Treat MAA/RN/2025/04 as a live authority example of case-specific assurance. Treat EASA NPA 2025-07(B) as the most important emerging civil framework and track its adoption.

The project's distinct work can be:

- map AMLAS artefacts and EASA/MAA obligations onto a shared evidence graph;
- make scope, model version, operational domain, authority allocation, monitor observability and unresolved assumptions machine-checkable;
- use the road case and the airborne DAA transfer to show precisely where a learned-component safety case stops and system/operational evidence begins; and
- make missing evidence and changes visible, rather than claiming that a model confidence score settles safety.

`C-CHAL-007` is the resulting framing proposal.
