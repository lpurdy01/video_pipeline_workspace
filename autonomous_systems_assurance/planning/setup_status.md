# Setup status — 2026-09-08

## Ready to use

- Separate research, resource-composition, video, assurance, verification, wiki, coordination and publication areas.
- Previous-project retrospective covering source gathering, wiki maintenance, verification iterations, paper construction, video QA, resource export and launch. Historical limitations and stale release metadata are recorded.
- User-confirmed audience and practical architecture focus, with the car perceiving/navigating/avoiding before taking off near the end.
- Three independent research lanes (ROAD, AIR, METHOD), separate PAPER and VIDEO writers, an integrator, job/handoff templates and baseline rules. This session's four slots support an integrator plus three workers; five specialist workers at once require additional capacity/sessions or waves.
- Initial primary-source research plus four separate research handoffs: **61 source records, 66 provisional claims, 15 manifested research/composition artifacts**. Three URLs repeat across lanes and are treated as related evidence, not independent corroboration.
- Executable compiler: exact ID resolution, contribution merging, source-snapshot hash checks, explicit claim-use mapping, dependency-cycle checks, bounded packages, review import, persistent objections, stale-review detection and transitive change impact.
- Paper outline and short opening draft; figure plan, hook, storyboard and scoped video-pipeline reuse plan. No script lock or render yet.

## Validation performed

**15 tests passed**, covering duplicate IDs, missing/empty evidence, untagged content, dangling claim tags, cycles, source hash mismatches, transitive dependency changes, preserved objections, invalidated human dispositions, input mutation, invalid review imports, resolution scope/chronology, role checks and path containment. The round-2 handoffs were structurally validated and each lane's JSON passed its local validation.

Normal compilation passes structural checks. The composition release check returns exit code 2 with **93 unique blockers**, comprising incomplete source context and missing review tasks. It plans **76 review packages** (four per claim) and records **zero completed review records**. No human or independent content-review verdicts were invented.

The parallel code reviewer found failures in stale-review handling, dependency binding, concurrent-read detection, empty-scope handling and review import preflight. These were corrected and covered by seeded tests. The reviewer did not certify the tool or independently verify every research claim.

## Still open

- Capture full original source context; current short excerpts/locators are useful research anchors but insufficient release evidence.
- Obtain GA-ASI authorization records, Zipline's underlying grants, EASA Proposed Issue 3 PDF and current standard publication status. Preserve failed retrievals and jurisdiction limits.
- Run source support, independent challenge and cross-artifact reviews, then obtain real human dispositions.
- Implement model execution adapters, detailed hazard/obligation/test nodes, finer section/beat dependencies, and the final media/publication gate.
- Integrate renderer inputs explicitly; existing earlier-project entry points contain project-specific paths and must not be run blindly against this workspace.
- File ownership and integration freezes are coordination conventions, not a distributed locking service. Immutable review import protects the CLI path; direct filesystem edits still require Git/process controls.
- The compiler only reviews manifested, explicitly tagged uses. It cannot discover every untagged factual assertion or verify source-extraction fidelity by hashing; editorial/source review must address those gaps.
- Retrieval pass completed: full EASA Issue 2/Proposed Issue 3, FAA AI roadmap, CAA CAP3127, NASA RTA, FAA/GA-ASI validation, Texas TxDMV and UK Protector announcement files are in ignored output with hashes. Zipline approval letters, NHTSA AQ26002 files, the Texas operator lookup, and the actual GA-ASI authorization record still require human browser/docket retrieval or authority confirmation. See [retrieval status](../research/retrieval_status.md).

No new GitHub repository, external publication, human-audio upload or finished media artifact was produced. Existing previous-project edits remain untouched; only root project-navigation instructions were updated alongside this new workspace.

Next useful work: assign a separate challenge wave to the round-2 records, retrieve full source context for the highest-value authority and technical claims, then integrate the reviewed evidence into the shared car-to-air architecture while PAPER and VIDEO develop separate drafts against a pinned baseline.
