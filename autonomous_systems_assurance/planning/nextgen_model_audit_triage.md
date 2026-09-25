# Newer-Gemini audit triage

**Audit:** `20260925T170449Z_argument_gemini-3.8-flash.json`  
**Model:** Gemini 3.8 Flash  
**Purpose:** independent editorial and research-lead review, not evidence, a compiler verdict, or a human disposition.

The audit packet explicitly allowed clipped manuscript fields. Its earlier run incorrectly inferred that clipped text was missing from the manuscript; that defect was corrected before this run. Each finding below was checked against the local source records and current prose before being accepted as work.

| Finding | Triage | Action / boundary |
|---|---|---|
| EASA NPA high-consequence boundary | Partly already addressed; retain a narrower statement | The paper already names the scope exclusion and says the applicability of a DAA function depends on a system-level failure-condition allocation. Do **not** replace that with the stronger, unsupported assertion that every DAA function is categorically out of scope. |
| Airborne recovery asymmetry | Accepted | Refine `AS-AIR-004`, `EA-AIR-004`, `O-AIR-006`, the architecture, crosswalk, paper and script so an active escape requires its own evidence-backed traffic-and-clearance observation path. A later landing/diversion contingency cannot stand in for immediate collision avoidance. |
| GA-ASI as learned-system example | Accepted as a qualification | The script now says inspected public material describes sensor fusion and does not establish a trained neural-network component. GA-ASI remains an integration/authorization-boundary example, not learned-perception evidence. |
| Zipline BVLOS authorization | Already addressed | The script and paper distinguish a scoped operational permission from an equipment authorization or disclosed learned-perception case. Avoid treating waiver/process language as technical ML evidence. |
| Full context for five aviation claims | Accepted research queue | Recover or promote official source context for `C-AIR2-002`, `C-AIR2-005`, `C-AIR2-006`, `C-AIR2-008`, and `C-AIR2-011` before stronger public claims. Current wording remains limited. |
| 75% score could look like safety maturity | Already addressed; monitor presentation | The dashboard and current report state 100% pre-human automated review coverage and 75% all-gate completion separately, alongside unresolved assumptions/artifacts and 0% human disposition. The score is never a safety probability. |
| Professional-qualification explanation | Already addressed | The paper explicitly rejects the proposed causal story as unsupported and turns it into a case-specific competence obligation. No added claim. |
| SINDy as perception interpretability | Rejected as obsolete packet lead | The current whitepaper and script do not make the asserted SINDy/perception analogy. No change. |
| California permit record reconciliation | Accepted as time-sensitive research lead | Do not add an unverified current permit status to the long-form paper. Recheck primary CPUC material close to publication. |
| Texas/Cybercab authorization wording | Already bounded | The current video frames the NHTSA audit query as an inquiry and does not claim Cybercab commercial operating approval. Recheck before publication because authorization status is time-sensitive. |

## Verification consequence

The accepted worked-case graph refinement is deliberately material: it changes the evidence proposition that reviewers see. Existing digest-pinned reviews are stale until the corresponding fresh packages complete. This is an expected compiler result, not a regression in the hypothetical case or a safety conclusion. The next refresh is serialized and rate-limited.

## Research order

1. Promote full local context already captured for FAA roadmap and UK CAA material where the exact source record supports it.
2. Recover FAA Order 8100.18A, draft TSO-C212a, and the FAA/GA-ASI validation report from authoritative repositories; preserve status and locator.
3. Recheck live CPUC and Texas authorization records only during a publication-status pass.
4. Treat any new Gemini discovery output as a lead list, then retrieve and inspect primary material locally.
