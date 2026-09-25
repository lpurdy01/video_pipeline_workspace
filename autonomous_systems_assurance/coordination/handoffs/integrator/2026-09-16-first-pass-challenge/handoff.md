# First-pass challenge handoff

**Owner:** `first-pass-challenge-agent`  
**Date:** 2026-09-16  
**Write scope:** `verification/out/first_pass_candidates/challenge/` and this handoff only.  
**Input:** compiler review packages generated with `python3 verification/compile.py --root autonomous_systems_assurance` on 2026-09-16.

## Delivered candidates

Fourteen model-review candidate records cover every `challenge` package with
an `assurance_case_links` entry:

| Claim | Candidate | Verdict |
|---|---|---|
| C-002 | R-FIRSTPASS-C-002-challenge | pass |
| C-AUTH-002 | R-FIRSTPASS-C-AUTH-002-challenge | pass |
| C-AUTH-008 | R-FIRSTPASS-C-AUTH-008-challenge | pass |
| C-CHAL-001 | R-FIRSTPASS-C-CHAL-001-challenge | pass |
| C-CHAL-002 | R-FIRSTPASS-C-CHAL-002-challenge | pass |
| C-CHAL-003 | R-FIRSTPASS-C-CHAL-003-challenge | pass |
| C-CHAL-004 | R-FIRSTPASS-C-CHAL-004-challenge | pass |
| C-CHAL-006 | R-FIRSTPASS-C-CHAL-006-challenge | pass |
| C-EVID-001 | R-FIRSTPASS-C-EVID-001-challenge | pass |
| C-EVID-002 | R-FIRSTPASS-C-EVID-002-challenge | pass |
| C-EVID-003 | R-FIRSTPASS-C-EVID-003-challenge | pass |
| C-EVID-004 | R-FIRSTPASS-C-EVID-004-challenge | pass |
| C-EVID-005 | R-FIRSTPASS-C-EVID-005-challenge | pass |
| C-EVID-007 | R-FIRSTPASS-C-EVID-007-challenge | pass |

Each candidate pins the compiled package digest, records the required model
metadata, gives source locators, retains limitations, and has no `resolves`.
They have **not** been imported into `verification/reviews/`.

## Challenge findings

1. **Frozen learned releases are a real regulator distinction, not merely the
   project vocabulary.** FAA Version I defines learned AI as static in operation
   and says a deployed updated version is subject to safety assurance again
   (FAA Roadmap, PDF p. 10). This is direction-setting material, not a means of
   compliance.
2. **The road-policy hook remains limited.** NHTSA's live ADS page continues to
   describe ADS 2.0 as voluntary, without federal approval of assessments, even
   while the page also presents AV 3.0 and AV 4.0. It does not establish a
   certification criterion for a learned model.
3. **The MAA notice supports the project’s frozen-model/ODD framing but not a
   civil equivalence claim.** It recommends fixed supervised models for early
   applications and MCRI agreement for certified military systems; it is
   informative UK military guidance and the underlying MCRI cases were not
   acquired.
4. **EASA DS.AI is a serious candidate framework, but its direct-fatality
   exclusion means it cannot be represented as a complete path for the most
   demanding flight-critical case without an aircraft-level failure-condition
   allocation.** The reviewed item remains NPA 2025-07(B), proposed material.
5. **NIST AI RMF 1.0 has a freshness blocker.** The current NIST framework page
   says 1.0 is being revised. The existing claim survives only as a claim about
   the 1.0 edition; refresh it before publication.
6. **No numeric proxy passed as a safety result.** Combinatorial coverage,
   rare-event simulation, calibration, runtime-assurance theorems and neuron
   coverage retain their stated premises and scope. In particular, a runtime
   monitor cannot rescue a miss it cannot observe early enough.

## Integration instructions

1. Freeze inputs and recompile. For each candidate, compare `input_digest` with
   the current package digest; do not import a stale record.
2. Import only through `python3 verification/compile.py --root
   autonomous_systems_assurance --import-review <candidate>`. The import command
   will reject duplicate IDs and changed package inputs.
3. Keep the listed local-context blockers. A challenge `pass` is not
   `source_support`, `cross_artifact`, or `human_disposition`, and it cannot
   close an evidence-artifact or assurance-obligation blocker.
4. Before public use, refresh C-EVID-001 against NIST’s successor or record a
   dated decision to cite AI RMF 1.0 historically. Obtain/rebuild full local
   source context for C-002, C-AUTH-002 and C-AUTH-008 if release readiness is
   sought.

## Verification performed

- Built the compiler once at the recorded input state: structural compile pass;
  14 case-linked claims and 56 case-linked review packages; prior review count
  zero.
- Inspected all cited full local contexts where present and the cited official
  FAA, NHTSA and NIST public pages for current/status alternatives.
- This handoff intentionally did not edit shared registries, import review
  records, or convert review coverage into a safety score.
