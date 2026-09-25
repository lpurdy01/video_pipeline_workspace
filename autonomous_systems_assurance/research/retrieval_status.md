# Supporting-document retrieval status

Retrieval attempts: 2026-09-08 and 2026-09-15. Files remain under ignored `verification/out/sources/`. The 2026-09-15 intake promoted the supplied FAA decision letters, current TSO-C211a and the TxMCCS lookup into separately owned source records with full snapshots and UTF-8 context. Other retrieved PDFs still require source-context promotion.

Related provisional claims: [C-AIR2-009] [C-AIR2-010] [C-AIR2-012] [C-AIR2-013] [C-AIR2-014] [C-ROAD2-001] [C-ROAD2-003] [C-ROAD2-004] [C-METHOD2-005] [C-METHOD2-006] [C-METHOD2-007] [C-INTAKE-001] [C-INTAKE-002] [C-INTAKE-003] [C-INTAKE-004] [C-INTAKE-005]. These tags identify source-status work; they do not constitute review.

## Retrieved successfully

| Document | Local file | SHA-256 | What was retrieved |
|---|---|---|---|
| FAA Roadmap for Artificial Intelligence Safety Assurance, Version I | `verification/out/sources/retrieval_check/faa_ai_roadmap.pdf` | `b8683625358a9f624aaf1567c0b083ad22235d3b518684f499b1e9c588fc4908` | Full 31-page PDF |
| EASA AI Concept Paper Issue 2 | `verification/out/sources/retrieval_check/easa_issue2.pdf` | `daa1525eb50fd31c3bad8928c012324a002cacffb9e4ac52591f7913e0b342ed` | Full 285-page PDF; landing page also saved |
| EASA AI Concept Paper Proposed Issue 3 | `verification/out/sources/retrieval_check/easa_issue3.pdf` | `439655adb56e98d69c7501e66ced7eaaaa285bb29bd27e3dcea7aad590951a77` | Full 239-page proposed PDF; landing page also saved |
| UK CAA CAP3127 DAA Policy Concept consultation response | `verification/out/sources/retrieval_check/caa_cap3127.pdf` | `85a72defeb2cb96225f632e46742786789448fe7aa7b10f3c9d2374de16aa217` | Full 26-page PDF |
| FAA/GA-ASI DAA Sensor Model Validation Flight Test, ASI-23126 Rev A | `verification/out/sources/retrieval_check/faa_ga_asi.html` | `6d1fdffa2cea8f93ca640f16a7c4d6b552e5255f1ecd2a4724c224f212f9f540` | Full PDF returned by the FAA page; filename is historical/misleading and should be renamed during a controlled cleanup |
| NASA Verification Framework for Runtime Assurance of Autonomous UAS, NTRS 20240007986 | `verification/out/sources/retrieval_check/nasa_rta_20240007986.pdf` | `0f393969de4473d7a75375bddcf26100937eca601a9d93dab5ed75f070b0fa6d` | Full PDF plus NTRS HTML record |
| FAA GA-ASI DAA page | `verification/out/sources/retrieval_check/ga_asi_daa.html` | `8fbb377565aa1b90eee9bb2fd47868c68591b7361bcc3e67869cf1e8ded6e3f0` | Current JavaScript page response; no authorization record established |
| Texas TxDMV AV program | `verification/out/sources/retrieval_check/txdmv_avprogram.html` | `515740a471264cab5206a8855a2567c8de76181a580110c76048f3bd41985ff9` | Current program page |
| UK Protector announcement | `verification/out/sources/retrieval_check/protector_uk.html` | `5a17765b6b7cc4bf8fb6af0e8ab5b73b4dbc8ed5e816840ad57e52214bd3c705` | Government HTML announcement, not the underlying Military Type Certificate |
| NASA formal-runtime-assurance NTRS record, 20240006522 | `verification/out/sources/retrieval_check/nasa_rta_20240006522.html` | `c80e882d68d602553e499dae68bac93b8d26202a9e71e8bb0c337c01da683c3a` | NTRS HTML record; linked PDF not downloaded in this pass |
| FAA Zipline Exemption 19111B, docket FAA-2020-0499-0033 | `verification/out/sources/book_intake/authority/faa-2020-0499-0033-zipline-exemption-19111b.pdf` | `099f0c9a7a155beb9742d17b2b6c59613826e1e40183d7ece8aa781e0c2416e9` | Full 28-page decision supplied by the user; Chromium independently loaded the official docket page and its attachment label |
| FAA Zipline Exemption 19111C, docket FAA-2020-0499-0034 | `verification/out/sources/book_intake/authority/faa-2020-0499-0034-zipline-exemption-19111c.pdf` | `f7d9c270fc191d3261310dbfb8e2cd8069654114dd381ec912921e498f0c8e55` | Full 19-page decision supplied by the user; Chromium independently loaded the official docket page and its attachment label |
| FAA TSO-C211a, Detect and Avoid Systems | `verification/out/sources/book_intake/authority/faa-tso-c211a-detect-and-avoid-2026.pdf` | `f9cd209f7e69058504bd2a7904d47fd599d6dd004d86badd83f5e382c2e6435f` | Full 15-page effective TSO supplied by the user |
| FAA Exemption 19031B, Amazon Prime Air | `verification/out/sources/book_intake/authority/faa-19031b-amazon-prime-air-2023.pdf` | `40d6bd6f8230abd971936e871b68122f5ee7578079a722fbc97dae4872ba3e81` | Full six-page historical decision supplied by the user |
| NHTSA AQ26002 opening resume | `verification/out/sources/book_intake/authority/nhtsa-aq26002-opening-resume-2026.pdf` | `48b37f751f82ca5f544d42a73e0c30293f6a2e38805e0dfeba0554a27c471061` | Full one-page opening resume supplied by the user; promoted into existing ROAD source context |
| TxMCCS Tesla Robotaxi, LLC live operator record | `verification/out/sources/browser_20260915/txdmv_operator_detail.html` | `8ef57af44bbc81e30c96a913196ad8a1e3162dcbabd61fd1d161d25ca5c7c901` | Chromium search and detail-page capture on 2026-09-15; record includes a live status and vehicle table |
| FAA TSO-C212a draft | Web reader inspection only | n/a | The official page exposes a nine-page draft with placeholder effective dates. Chromium's direct request received HTTP 403, so this draft was not promoted to full-context source status. |

The retrieved FAA GA-ASI response is a PDF despite its `.html` filename; preserve its hash and rename only through a later documented integration change. The CAA, EASA and NASA PDFs can now support a full-context extraction pass.

## Requires human attention

| Document or record | Failure | Human action |
|---|---|---|
| NHTSA AQ26002 associated-record page beyond its opening resume | Chromium still receives an NHTSA access-denied response for the dynamic AQ page | The opening resume is now acquired. Recheck later submissions and a final disposition only if the road case is used in publication |
| EASA source-context promotion | PDFs are acquired, but relevant sections have not yet been extracted and checked | Human or assigned source reviewer should select exact page ranges and verify qualifications before updating `sources.json` |
| FAA/GA-ASI TSO authorization status | Public product/report files do not establish an article-specific current TSO authorization | Search FAA DRS/authorization records interactively or obtain an authority confirmation; do not infer absence from this pass |
| UK Protector MTC | Government announcement is not the certificate or complete scope | Obtain the UK Military Aviation Authority certificate/scope if publicly releasable; distinguish military type certification from civil operation and DAA equipment approval |

## Access and rights notes

The downloaded EASA, FAA, NASA and CAA files are retained for research under ignored output. Before a public resource package is built, check redistribution rights and link to the publisher rather than copying licensed material. Do not upload private credentials or human audio. A Chromium session was used only on public pages and required no account credentials.

## Next controlled action

Extract text and page ranges from the remaining retrieved PDFs into ignored UTF-8 context files, update only the corresponding contribution records after checking locators, and rerun the compiler. Keep later NHTSA AQ material, GA-ASI authorization status and the Protector certificate as explicit blockers until their underlying records are acquired or the paper describes them only as unresolved searches.
