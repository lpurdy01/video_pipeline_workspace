# Verification as Evidence Production

## Definition

Verification is the structured activity of producing evidence that implementation artifacts satisfy requirements. It includes review, analysis, and testing, with records that can be audited.

## Why It Matters

The whitepaper's verification compiler should not merely ask agents whether a requirement is satisfied. It should compile evidence: what was checked, by whom or what, under which assumptions, against which source, and with what result.

## Related Claims

- [Verification Requires Review, Analysis, and Test](../claims/verification_requires_review_analysis_and_test.md)
- [Safety-Critical Verification Depends on Traceability](../claims/safety_critical_verification_depends_on_traceability.md)

## Source Support

- Rierson summarizes DO-178C verification as an integral process from plan verification through reporting and review of verification results, including reviews, analyses, and tests. See Rierson Markdown line 4295.
- Rierson describes software verification plans as specifying how reviews, analyses, tests, checklists, traceability, pass/fail criteria, and results are handled. See Rierson Markdown line 6042.
- FAA AC 20-115D frames DO-178C compliance through applicable objectives and associated life cycle data. See `faa_ac_20_115d.txt` line 143.
- NPR 7150.2D requires review/audit access to verification activities, development processes, traceability, change tracking, and nonconformances. See `npr_7150_2d.txt` line 840.

## Open Questions

- Which evidence artifacts should Stage 2 generate first: trace links, review checklists, agent transcripts, or requirement test matrices?
