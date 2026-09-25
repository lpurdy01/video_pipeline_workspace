# Next-generation video structure

This directory is an isolated VIDEO-lane proposal for a long-form companion to the learned-autonomous-systems whitepaper. It does **not** modify the active narration, storyboard, manuscript, figures, evidence registers, or production manifest.

The proposal assumes a 34-minute target, with a practical mechanism shown in the first 20 seconds and an accessible explanation that becomes more technical gradually. Every factual narration use is mapped to an existing, **provisional** project claim. Project proposals are labeled as such; research gaps are explicit rather than filled with plausible-sounding narration.

| File | Purpose |
|---|---|
| [treatment.md](treatment.md) | Story purpose, audience contract, 34-minute section architecture, and editorial guardrails. |
| [script_outline.md](script_outline.md) | Detailed beat-by-beat narration and visual outline, ready for a later script pass. |
| [visual_inventory.md](visual_inventory.md) | Visual system, diagram specifications, and review concerns. |
| [narration_evidence_map.md](narration_evidence_map.md) | Exact claim uses, source-status limits, and research-dependent language that must not be narrated as settled fact. |

## Working status

This is a composition proposal, not an approved script or a production baseline. Before it is promoted into `video/narrative.md`, `video/storyboard.md`, or a renderer manifest, an integrator should:

1. choose a frozen claim/source baseline;
2. add the selected script and visual-description artifacts to `verification/artifacts.json`;
3. create fresh source-support, challenge, and cross-artifact reviews for the selected claim uses; and
4. resolve the research gaps marked in the evidence map, especially risk/DAL material and claims about standard-setting capacity.

The project’s current human-review gate remains open. A provisional claim tag is a locator to reviewable evidence, not permission to state a result as certification fact.
