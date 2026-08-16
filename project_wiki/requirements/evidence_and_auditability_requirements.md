# Evidence and Auditability Requirements

## Requirement

The verification compiler shall package verification outputs as evidence records, including the requirement checked, method used, source evidence, reviewer or model unit, assumptions, result, and review status.

## Rationale

The whitepaper's proposed system should mirror safety-critical verification as an evidence-producing process. Agent outputs should become auditable records rather than unstructured chat answers.

## Source Support

- Rierson describes verification as including reviews, analyses, and tests, beginning with plans and continuing through reported and reviewed verification results. See Rierson Markdown line 4295.
- Rierson describes software verification planning as covering review processes, checklists, traceability, pass/fail criteria, and result documentation. See Rierson Markdown line 6042.
- FAA AC 20-115D frames DO-178C use around satisfying objectives and producing life cycle data. See `faa_ac_20_115d.txt` line 143.
- NPR 7150.2D requires project access to verification activities, audits, traceability, change tracking, nonconformances, and source code. See `npr_7150_2d.txt` line 840.

## Verification Method

- Review generated evidence packages for required fields.
- Confirm evidence records point to source artifacts and traceability links.
- Confirm independent review status can be represented separately from the model's answer.

## Open Questions

- What is the minimal evidence package for the Stage 2 prototype?
- Should model transcript excerpts be stored, summarized, or hash-linked?
