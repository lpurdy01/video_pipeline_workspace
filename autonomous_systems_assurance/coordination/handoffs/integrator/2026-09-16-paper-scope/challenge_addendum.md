# Digest-pinned challenge pass — addendum

Reviewed: 2026-09-16. This pass covers the 14 claims linked by the current worked assurance case. It uses the compiler package snapshot written at **13:33:18** after the final narrow factual-scope manuscript revision. Candidate records are intentionally not imported.

## Candidate set

- 14 valid JSON review candidates in `challenge_candidates/`.
- 10 `pass`, 4 `uncertain`, 0 `fail`.
- Local validation confirms every candidate `package_id` and `input_digest` equals the current `verification/out/review_packages.json` package value at handoff time.
- Reviewer declaration: `paper-scope-challenge-agent`, `gpt-5.6-luna`, prompt `paper-scope-digest-pinned-challenge-v1`.

## Uncertain challenges that should remain visible

| Claim | Why it remains uncertain | Required next evidence / wording boundary |
|---|---|---|
| `C-002` | The retained FAA source is short-context only. | Capture and inspect full current FAA TSO context; retain the narrow TSO-versus-install/use distinction. |
| `C-AUTH-002` | FAA roadmap context is short-only and a later FAA position was not checked. | Keep it as Version I roadmap discussion, not a means of compliance; retrieve full context and refresh policy. |
| `C-AUTH-008` | NHTSA ADS 2.0 regions are short-only and do not resolve later enforcement, exemption, state, or product-specific questions. | Name ADS 2.0 and its voluntary US scope; capture full context and audit current material separately. |
| `C-CHAL-004` | The EASA exclusion wording is supported, but no aircraft-level functional-hazard/failure-condition allocation maps the hypothetical DAA role into that exclusion. | Do not call the flight case catastrophic or categorically outside DS.AI; use a conditional boundary until allocation exists. |

## Passing claims, with preserved limits

`C-CHAL-001`, `C-CHAL-002`, and `C-CHAL-003` pass only as current/proposed, jurisdiction-bounded method descriptions. `C-CHAL-006` passes only as ML-component AMLAS guidance. `C-EVID-001` through `C-EVID-005` and `C-EVID-007` pass only as scoped research/method evidence, not a transport safety threshold, certification basis, model safety score, or evidence for either hypothetical release.

## Import instructions

The integrator should first verify that the package digests still match; any manuscript, source, compiler, or manifest change invalidates these candidates. Then import only candidates that remain current through the compiler CLI. These model challenge records do not resolve the four uncertainties, do not substitute for source-context completion, and do not replace human disposition.
