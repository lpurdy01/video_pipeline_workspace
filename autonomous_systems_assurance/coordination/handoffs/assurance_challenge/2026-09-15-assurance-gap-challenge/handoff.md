# Handoff: 2026-09-15-assurance-gap-challenge / 1

- Author/session and role: `/root/assurance_challenge`, independent adversarial researcher
- Date/time with timezone: 2026-09-16, America/Phoenix
- Job card: [`2026-09-15-assurance-gap-challenge.md`](../../../tasks/2026-09-15-assurance-gap-challenge.md)
- Input baseline and hashes: base commit `ab5bf71abcab3d873c541679199d89c3b300223b`; `research/sources.json` `1dbe7b18059dfe43dfbaace1bec1d65f7ab510c7ad4ff153d5561760324434e2`; `verification/claims.json` `df12a3a0aa71bb32805ee2be847594ab1d337ce4254ffa18c35ef8c4d0ea46c7`; `research/contributions/method_round2/sources.json` `fd97e1bebdaa5c0dd5679091da42ab1c4baa41f0c76ff3c709353670d518e066`; `research/contributions/air_round2/sources.json` `88c30e9ba4d2d3ec0fe45311ceeb0ae9127cb5f16b61c6f191845ece6de8ef71`.
- Source/claim/compiler input baseline: normal compile at start: structural pass; 389 blockers; 71 sources; 71 claims; 15 artifacts; 284 planned reviews; no reviews.
- Output file paths and SHA-256 values: `research/contributions/assurance_challenge/sources.json` `5b732d220c05a7b85e45c99e93c4066fc2eb8cef6026e5e5d80fa13d8bee9000`; `claims.json` `6d4d53027483f733d460fc61bce2b575346aaa9c92a13a142364dd3cf81df855`; `findings.md` `33f90c9a5d135bd7ce73396e996371f6a5ade3508959aaca4833e03740cdc03b`; `negative_search_log.md` `4b5824bc7444910d3bccc83f50e35d843732dd1672361fae193f738e6bc8a7db`.
- Completion state and any blocked deliverables: complete. No final civil approval record or completed public MCRI was found; this is a scoped negative result, documented separately from the positive findings.
- Writes paused for integration: yes

## Findings and proposed changes

### Defeating evidence retained

1. `S-CHAL-001` / `C-CHAL-001`: UK MAA/RN/2025/04 is an **effective current military authority path**, not mere academic work. It calls for an MCRI agreed with MAA for certified systems and recommends fixed supervised models within a defined ODD for early safety-related ML. This defeats the proposition that no defined assurance process exists anywhere.
2. `S-CHAL-002` / `C-CHAL-003`: EASA NPA 2025-07(B) is a serious proposed civil lifecycle, covering OD, risk, system process, learning assurance, configuration/life-cycle data and in-service monitoring. The project must compare its proposed contracts to it instead of treating the contracts as novel.
3. `S-CHAL-004` / `C-CHAL-006`: AMLAS is an already-published six-stage methodology for the frozen/offline-supervised ML component. The project's core graph should map, extend or challenge AMLAS artefacts, not rebrand their basic lifecycle.

### What remains open

- `C-CHAL-002`: MAA itself states its current route is not prescriptive without architectural mitigation; its system safety case is case-specific.
- `C-CHAL-004`: EASA's proposal excludes AI directly contributing to fatalities or multiple life-threatening injuries and is not final. It is relevant to lower delegated authority and perception/assistance examples but does not close the project's hardest flight-critical case by itself.
- `C-CHAL-005`: EUROCAE's current WG-114 page lists ED-324 as draft, target publication 31 December 2026. Do not report it as an existing published standard or final EASA-recognised means of compliance.

### Integration recommendation

Accept the source/claim contribution structurally, retain all contrary evidence, and revise shared framing only after the other three lanes are frozen:

- replace any phrase such as “no process exists” or “partial toolkit” with a scoped comparison finding;
- adopt AMLAS as the learned-component lifecycle baseline;
- compare MAA's MCRI/ODD/architectural-mitigation approach and EASA's proposed DS.AI requirements against the project graph;
- limit the final literature finding to: *the inspected public material contains mature methods and case-specific authority pathways, but this search did not locate a final, publicly inspectable civil lifecycle closing the project's most demanding high-criticality trained-model case.*

The direct framing proposal is `C-CHAL-007`.

## Search and inspection record

Full dated queries, outcomes and explicit negative/inaccessible categories are in [`negative_search_log.md`](../../../../research/contributions/assurance_challenge/negative_search_log.md). Sources were retrieved from their original publishers. The source snapshot manifest is:

| Local preserved context | SHA-256 |
| --- | --- |
| `out/maa-rn-2025-04.pdf` | `203733969cf4e24d87bf4ed4d734c309fb63db15fbfbc42aa67ce6ea096eb497` |
| `out/maa-rn-2025-04.txt` | `8f141be160c50527883cb70e34305de397e1cee152108b9ceff9a1e0ec06f884` |
| `out/easa-npa-2025-07b.pdf` | `a42ac47d3eb3129667bdefe104da634960260788f0d3a8f8400f2d943d22fb1f` |
| `out/easa-npa-2025-07b.txt` | `d3357c902ae5e6f0f29277ce73c70783e643983fba19c9ac952a96a324227357` |
| `out/eurocae-wg114.html` | `6ec9597e8643771f0342866aa507012c05c29eca07aae2695af16feae272d67b` |
| `out/amlas-v1.1.pdf` | `18eab2179ccd2c8d6aeb651099c72536d192dddb58094bf2b440de5885322429` |
| `out/amlas-v1.1.txt` | `26404250ab655940194a3aeb3bb82aa922b38700c97e3fa514e119ed4a54d132` |

`S-CHAL-001` is an authority notice but explicitly characterises itself as informative guidance. `S-CHAL-002` is explicitly an NPA/proposal. `S-CHAL-003` is a standards work-program page. `S-CHAL-004` is academic guidance. They are not treated as independent product evidence or certification decisions.

## Review provenance

No compiler-schema review was performed. This was an independent challenge search by the named agent, not a human disposition and not a substitute for source-support or human review packages.

## Verification

- `python3 -m json.tool research/contributions/assurance_challenge/sources.json`
- `python3 -m json.tool research/contributions/assurance_challenge/claims.json`
- `python3 verification/compile.py`

At the frozen output, the compiler reports structural pass; 444 blockers; 75 sources; 78 claims; 15 artifacts; 312 planned reviews; no reviews. The increased blocker count is expected from the seven new provisional claims and their review requirements. Snapshot/context hashes were checked by the compiler. Structural parsing does not validate truth or promote the claims.

## Impact and next action

Likely affected shared material after integration: `PROJECT_BRIEF.md`, `planning/learned_systems_assurance_next_steps.md`, `assurance/architecture.md`, `research/questions.md`, source/citation planning, whitepaper thesis and video wording. The visual narrative should show that the same trained-model lifecycle can be credible inside a bounded authority allocation while the airborne transfer reveals missing independent monitor, high-criticality and authority-acceptance evidence.

First integration action: build an explicit crosswalk from the project's eight evidence contracts to AMLAS stages and the inspectable portions of MAA/EASA material. Treat any unmatched project contract as a candidate contribution and any unmatched external requirement as a graph obligation. Refresh EASA/ED-324 status before any public draft.
