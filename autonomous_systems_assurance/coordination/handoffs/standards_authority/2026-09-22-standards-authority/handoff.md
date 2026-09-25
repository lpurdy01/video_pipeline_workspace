# Handoff — standards and authority status

**Job:** 2026-09-22-standards-authority  
**Owner:** standards_authority  
**Completed:** 2026-09-22  
**Base commit:** 62f05a4af55491230c0b66f5d7db634ea0d847f6  
**Exclusive output path:** research/contributions/standards_authority/

## Deliverables

| File | SHA-256 |
|---|---|
| sources.json | 7bb92abcf9fde112e16c6707a0fcd6411570a56a0e8214ad009380b2bb457d3a |
| claims.json | 15a33ed5fa9952fa0cac8eb9811d1dd391e6900eea4d3e2e50337b77e9706846 |
| findings.md | 5db406012769e2556a30c755fbe23e913b03a61ce50bbb872f9f8a72d969d999 |

Five primary-authority / standards-body records and five provisional C-STD claims were added.

## Main conclusion

The project should not say “no method exists.” It should say that the inspected public record has methods and pathways with materially different status:

- AMLAS is an ML-component methodology, not a whole-system approval method. [C-CHAL-006]
- FAA describes active collaborative method development, but the current FAA program page is not a completed standard or approval. [C-STD-001]
- EASA DS.AI remains a proposed rulemaking package on the captured current CRT page. [C-STD-002]
- U.S. road self-certification is certification to applicable FMVSS, subject to reasonable care and false/misleading limits; it is not a certification that a trained model is safe in every possible scene. [C-STD-003]
- SAE J3321 is current AI/ML V&V material, but public scope calls it an information report with no mandatory requirements. [C-STD-005]

The source record does not support causal narration about a lack of mathematically rigorous methods or a shortage of qualified people. Preserve those as hypotheses only if a later primary-source or carefully scoped evidence base supports them.

## Retrieval

Full original snapshots and extracted contexts are retained under the ignored lane out/ path for FAA, EASA CRT and 49 U.S.C. § 30115. NHTSA returned HTTP 403 and SAE timed out when retrieved directly. Both were inspected through browser renderings but stay short-context / release-blocking until a full source snapshot or authorized text is acquired.

## Verification

- Both JSON files: python json.tool passed.
- Project compiler: structural_compile pass after automatic discovery of this lane.
- Observed global compiler state at the run: 99 sources, 105 claims, 420 planned packages, 669 blockers. The review score remained 0 because the parent manuscript revision had invalidated the prior review baseline; this handoff did not alter review records.

## Integration notes

No shared manifest, paper, video, wiki, canonical registry or review records were edited. The integrator can cite the C-STD IDs in a manuscript/video proposal after deciding the precise language. Refresh C-STD-002 just before publication; use it only with its captured-date label.

