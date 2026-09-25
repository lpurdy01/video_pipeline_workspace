# Research integration report — round 2

Integration date: 2026-09-08. This report records a structural integration of independent lane handoffs. It does not promote any claim to verified status. The compiler continues to require source-context completion, source/challenge review, cross-artifact review and human disposition.

## Inventory

| Input | Sources | Claims | Primary focus |
|---|---:|---:|---|
| Seed research | 15 | 16 | GA-ASI, FAA/EASA, Zipline, runtime assurance, Tesla representations, SINDy |
| `road_air` setup handoff | 2 | 3 | Texas program and first-responder listing; unresolved individual authorization |
| `road_round2` | 14 | 14 | TxDMV/NHTSA/California/CPUC layers; Tesla and Waymo public descriptions |
| `air_round2` | 13 | 14 | DAA architecture, TSO boundaries, FAA/EASA, CAA DAA metrics, Zipline, Protector |
| `method_round2` | 17 | 19 | Simplex/RTA, learning assurance, formal reachability, probabilistic evidence, interpretability, SINDy |
| **Compiler total** | **61** | **66** | Exact IDs, references and claim uses compiled together |

The seed count is 15 sources and 16 claims. Earlier setup notes described 17 sources and 19 claims; the compiler's merged count is authoritative for the current files. No lane files were overwritten.

## High-value convergences

1. **Permission is layered.** State/commercial authorization, federal vehicle self-certification and investigation, passenger-service permission, equipment performance authorization, aircraft installation/type approval and operation are different evidence objects. The paper and video should make the approval object visible each time it says “approved.” Relevant sources include [NHTSA’s Cybercab Audit Query](https://www.nhtsa.gov/press-releases/investigation-tesla-cybercab-self-certification), [California DMV’s permit categories](https://www.dmv.ca.gov/portal/vehicle-industry-services/autonomous-vehicles/), and [FAA’s TSO explanation](https://www.faa.gov/aircraft/air_cert/design_approvals/tso).
2. **A vendor system description is not an authority finding.** Tesla and Waymo descriptions are useful leads for intermediate representations, sensor fusion, and lifecycle evidence. They do not establish current configuration, quantitative error bounds, causal interpretability or compliance.
3. **DAA evidence remains scope-sensitive.** GA-ASI describes cooperative and non-cooperative traffic sensing and DAA standardization, but current authorization status must be established from FAA records. Zipline’s scoped BVLOS authorization and onboard-perception account require the underlying approval conditions before architecture claims are made. The UK Protector MTC is a military airworthiness record, not automatically a civil DAA or installation approval.
4. **The practical architecture is conditional.** NASA Simplex/runtime-assurance work supports advanced-controller/fallback patterns only under monitor timing, recoverability and trusted-controller assumptions. A monitor sharing the learned path’s missed observation needs an explicit common-cause argument.
5. **Interpretability, minimization and probabilistic testing are evidence classes.** Feature visualization, sparse equation discovery, formal reachability and statistical risk estimates each answer bounded questions. None should be presented as a universal proof that a learned controller is safe.
6. **Scenario-level evidence must survive aggregation.** The UK CAA DAA material warns that averaged risk metrics can hide deficiencies in particular encounters. This supports storing encounter-level evidence and avoiding a single “confidence” score as the project’s conclusion.

## Duplicate and related-source handling

Three URLs occur in more than one lane:

- TxDMV AV program: seed `S-ROAD-AIR-001` and `S-ROAD2-001`.
- FAA AI roadmap: `S-AIR2-007` and `S-METHOD2-005`.
- EASA Issue 2 page: `S-AIR2-008` and `S-METHOD2-006`.

These remain separate records because the lanes inspected different regions and made different uses. Their `independence_group` values show that they are not independent sources. The integrator should later consolidate exact duplicate regions or retain distinct locators with an explicit relation; no majority vote should result from repeated URLs.

## Conflicts and unresolved publication hazards

- GA-ASI pages contain both historical/forward-looking TSO language and feature-list language that can be read as authorization. Locate the actual FAA DRS authorization holder, article number, date and scope before using “certified.”
- The current CPUC table lists Waymo Driverless Deployment while an inspected 2023 certificate says it expired July 2, 2025. Obtain the current renewal/amendment record and explain the stale link before publication.
- TxDMV program pages, a Tesla operator lookup and Texas DPS first-responder listings do not establish the same thing. The current Tesla Cybercab authorization record remains unresolved.
- Zipline approval letters returned HTTP 403; EASA PDFs returned rate limiting in at least one lane. These are retrieval blockers, not negative findings.
- EUROCAE ED-324 / SAE ARP6983 publication and recognition status needs a current publisher record. A draft or target date is not a final standard.
- Five-year-old personal DAA experience remains motivation for the research, not current capability evidence. No employer or program details are included.

## Compiler state after integration

After adding the three round-2 findings to `verification/artifacts.json`, normal compilation reports:

```text
structural_compile: pass
sources: 61
claims: 66
artifacts: 13
planned_reviews: 264
current_passing_packages: 0
review_records: 0
composition_release_ready: false
blockers: 368
```

Run with:

```bash
python3 autonomous_systems_assurance/verification/compile.py
python3 -m unittest discover -s autonomous_systems_assurance/verification/tests -v
```

The 15 seeded tests pass. The normal compile’s “pass” means structural graph construction succeeded. It does not mean the research is factually verified.

## Recommended next wave

1. Assign AIR to retrieve GA-ASI/FAA authorization records and the Zipline docket letters.
2. Assign ROAD to reconcile Texas/Tesla and CPUC/Waymo current records.
3. Assign METHOD to capture full permitted FAA/EASA/NASA context and challenge the independent-observation assumption with common-mode counterexamples.
4. Have a separate challenge reviewer inspect the strongest claims against original context; do not have the authoring lane sign its own human disposition.
5. Only after that, integrate the first evidence revision into the paper and video baseline. Keep all 66 claims provisional until review records exist.
