# First-pass cross-artifact candidate handoff

Date: 2026-09-16  
Worker: `first-pass-cross-agent`  
Task: Cross-artifact first pass for all current `cross_artifact` review packages with `assurance_case_links`.

## Input baseline

The package set was compiled before review. Its current hashes were:

| Input | SHA-256 |
|---|---|
| `verification/out/review_packages.json` | `1638e4d8beae05413da8025a74f863270f757dbcee980750f42355d8ac0e39b5` |
| `assurance/assurance_case.json` | `10768aa9a43b71617bc396cc64cac9e9824b3424e1b0bac1403cec351fcf9cb1` |
| `assurance/method_crosswalk.json` | `7176cae202ce06e9a8c0586e6ffaacd90b891fdd6f9c7546759ea17cb0cb3e01` |
| `assurance/amlas_maa_easa_crosswalk.md` | `4ee834b0096b787726834444e743767c109f76a0ec5029a234497eafddedcddc` |
| `assurance/architecture.md` | `c78fc42af747a4e99b8d034398abe27df2a51da68392df5ed707c121d2a62d1b` |
| `planning/learned_systems_assurance_next_steps.md` | `e77ec2adf6b7a1a0285ae4225570289a228947d59875746bbc34bd802ef3aca5` |

## Candidate records

Fourteen candidates were created under `verification/out/first_pass_candidates/cross_artifact/`. They are model-review candidates only; they were **not** imported into `verification/reviews/`.

| Package | Candidate | Verdict |
|---|---|---|
| `P-C-002-cross_artifact` | `R-FIRST-CROSS-C-002.json` | pass |
| `P-C-AUTH-002-cross_artifact` | `R-FIRST-CROSS-C-AUTH-002.json` | pass |
| `P-C-AUTH-008-cross_artifact` | `R-FIRST-CROSS-C-AUTH-008.json` | pass |
| `P-C-CHAL-001-cross_artifact` | `R-FIRST-CROSS-C-CHAL-001.json` | pass |
| `P-C-CHAL-002-cross_artifact` | `R-FIRST-CROSS-C-CHAL-002.json` | pass |
| `P-C-CHAL-003-cross_artifact` | `R-FIRST-CROSS-C-CHAL-003.json` | pass |
| `P-C-CHAL-004-cross_artifact` | `R-FIRST-CROSS-C-CHAL-004.json` | pass |
| `P-C-CHAL-006-cross_artifact` | `R-FIRST-CROSS-C-CHAL-006.json` | pass |
| `P-C-EVID-001-cross_artifact` | `R-FIRST-CROSS-C-EVID-001.json` | pass |
| `P-C-EVID-002-cross_artifact` | `R-FIRST-CROSS-C-EVID-002.json` | pass |
| `P-C-EVID-003-cross_artifact` | `R-FIRST-CROSS-C-EVID-003.json` | pass |
| `P-C-EVID-004-cross_artifact` | `R-FIRST-CROSS-C-EVID-004.json` | pass |
| `P-C-EVID-005-cross_artifact` | `R-FIRST-CROSS-C-EVID-005.json` | pass |
| `P-C-EVID-007-cross_artifact` | `R-FIRST-CROSS-C-EVID-007.json` | pass |

Each record declares:

- `reviewer_id: first-pass-cross-agent`
- `reviewer_kind: model`
- `model_id: gpt-5.6-luna`
- `prompt_version: first-pass-cross-v1`
- exact current package ID and digest
- artifact paths, tagged claim uses and case-node links
- a claim-specific rationale and limitations
- `resolves: []`

## Review result

The full artifact-use extracts were inspected for all fourteen packages. The reviewed text and graph uses preserve the associated claims' material limitations:

- approval object remains distinct from installation/operation;
- MAA remains applicant-specific UK military guidance;
- EASA remains proposed and excludes the stated high-consequence scope;
- AMLAS remains learned-component guidance requiring complementary system/domain assurance;
- NIST, combinatorial coverage, rare-event simulation, calibration, runtime assurance and neuron coverage remain bounded evidence methods rather than safety probabilities or approvals;
- all case evidence is labelled planned and all worked-case obligations remain open.

No reviewed use promoted a method, authorization, metric, or model review into a certification conclusion. This result does not assess source truth, source completeness, visual rendering, recording, final paper prose, or human publication disposition.

## Validation

- Candidate schema validation against `compile.py:check_review`: passed for 14/14 records.
- Candidate package ID/digest/task matching against freshly compiled packages: passed for 14/14 records.
- Selection completeness: passed; candidates exactly match all 14 current cross-artifact packages with `assurance_case_links`.
- `python3 autonomous_systems_assurance/verification/compile.py`: structural pass; no review records imported.
- `python3 -m unittest discover -s autonomous_systems_assurance/verification/tests -v`: 18 passed.

## Integration instructions

1. Recompile immediately before import. If any candidate package digest changed, do not import that candidate; regenerate its review against the changed artifact/package.
2. Inspect the candidate record and its stated limits. Import only a record the integrator accepts with:

   ```bash
   python3 autonomous_systems_assurance/verification/compile.py \
     --import-review autonomous_systems_assurance/verification/out/first_pass_candidates/cross_artifact/<candidate>.json
   ```

3. Recompile after imports. These model passes remove only their current cross-artifact queue entries. They do not satisfy source-support, challenge, human-disposition, source-context, or worked-case evidence blockers.

