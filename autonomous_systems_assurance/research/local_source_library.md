# Local primary-source library

This index points to native-format copies retained in the workspace. Source records, exact locators, hashes, scope, and claim links remain in the lane-owned `sources.json` files and the [retrieval status](retrieval_status.md). Files under `out/` are intentionally ignored by Git so the repository does not redistribute material without a release-rights decision.

## Core whitepaper methods and authority material

| Source | Local native document | Main use in the review draft |
|---|---|---|
| AMLAS v1.1, University of York | [PDF](contributions/assurance_challenge/out/amlas-v1.1.pdf) | lifecycle plus data requirements (PDF pp. 21–23), overfitting/leakage (pp. 33–35), and independent verification (pp. 40–41) |
| *Deep Learning*, Goodfellow, Bengio and Courville | [official captured HTML, Chapter 5](../out/sources/deep_learning_book/site/contents/ml.html) | Section 5.2 and Figure 5.3 explain underfitting/overfitting as a general model-capacity illustration; not safety evidence |
| MAA/RN/2025/04, UK Military Aviation Authority | [PDF](contributions/assurance_challenge/out/maa-rn-2025-04.pdf) | case-specific UK military AI path |
| EASA NPA 2025-07(B) | [PDF](contributions/assurance_challenge/out/easa-npa-2025-07b.pdf) | proposed civil DS.AI framework and scope boundary |
| NIST AI RMF 1.0 | [PDF](contributions/assurance_evidence/out/sources/nist-ai-rmf-100-1.pdf) | lifecycle/risk-management evidence role |
| NIST combinatorial autonomy methods | [PDF](contributions/assurance_evidence/out/sources/nist-assured-autonomy-combinatorial.pdf) | selected scenario-factor coverage |
| Rare-event autonomous-vehicle testing | [PDF](contributions/assurance_evidence/out/sources/okelly-rare-event-simulation.pdf) | conditional simulation estimates |
| Neural-network calibration | [PDF](contributions/assurance_evidence/out/sources/guo-calibration.pdf) | calibrated-confidence limitations |
| NASA runtime assurance for autonomous UAS | [PDF](contributions/assurance_evidence/out/sources/nasa-rta-uas.pdf) | conditional monitor/recovery argument |
| Saliency-map sanity checks | [PDF](contributions/assurance_evidence/out/sources/adebayo-saliency-sanity-checks.pdf) | interpretability challenge |
| Neuron coverage and AV testing | [PDF](contributions/assurance_evidence/out/sources/nist-neuron-coverage-av-testing.pdf) | test-adequacy limitation |

## FAA, DAA, road-operation, and aviation records

| Source | Local native document | Notes |
|---|---|---|
| FAA AI Safety Assurance Roadmap | [PDF](../verification/out/sources/retrieval_check/faa_ai_roadmap.pdf) | retained 31-page PDF; selected roadmap regions now have full local context, while unrelated regions may still be limited |
| NASA *Verification of Autonomous Systems* | [PDF](source_recovery/out/nasa_simplex_slides/snapshot.pdf) | retained NASA presentation; source record promotes the inspected Simplex overview on slide 12 only |
| ANSI/UL 4600 Edition 3 public scope | [captured HTML](source_recovery/out/ul_4600/snapshot.html) | retained public status/scope page; it is not the licensed standard text |
| FAA AC 25.1309-1A, System Design and Analysis | [PDF](contributions/risk_evidence/out/sources/ac-25-1309-1a.pdf) | historical severity/likelihood system-safety context; not a learned-model acceptance method |
| FAA AI/ML technical discipline | [captured HTML](contributions/standards_authority/out/sources/faa_ai_discipline.html) | current collaboration and certification-framework activity page, not a standard or approval |
| EASA RMT.0742 / DS.AI status | [captured HTML](contributions/standards_authority/out/sources/easa_crt.html) | time-sensitive rulemaking-status capture; refresh before publication |
| EASA NPA 2025-07(B), risk tables | [PDF](contributions/risk_evidence/out/sources/easa-npa-2025-07b.pdf) | retained proposal copy used for its proposed authority and risk-table claims; not final rule text |
| NHTSA ADS 2.0, *A Vision for Safety* | [PDF](contributions/assurance_authority/out/sources/ads2-vision-for-safety.pdf) | original 36-page NHTSA guidance, fetched from public mirror after the official host returned 403; source-record integration deferred to the next coordinated review refresh; byte identity with NHTSA-hosted copy unconfirmed |
| NHTSA Standing General Order data dictionary | [PDF](contributions/direction_evidence/out/sources/nhtsa_sgo_data_dictionary.pdf) | reporting dataset definitions and explicit comparability limits; not an autonomous-vehicle safety rate |
| NHTSA quiet-car final rule (2016) | [PDF](contributions/direction_evidence/out/sources/nhtsa_quiet_cars_final_rule.pdf) | historic EV/hybrid pedestrian-risk analysis and its VMT-denominator limitation |
| NCEES PE examination information | [captured HTML](contributions/direction_evidence/out/sources/ncees_pe_exam.html) | current examination taxonomy; supports only the narrow observation that it has no separate ML examination |
| FAA TSO-C211a, Detect and Avoid Systems | [PDF](../verification/out/sources/book_intake/authority/faa-tso-c211a-detect-and-avoid-2026.pdf) | effective TSO; does not itself show installation or operational approval |
| Zipline Exemption 19111B | [PDF](../verification/out/sources/book_intake/authority/faa-2020-0499-0033-zipline-exemption-19111b.pdf) | user-supplied decision, official docket page also captured |
| Zipline Exemption 19111C | [PDF](../verification/out/sources/book_intake/authority/faa-2020-0499-0034-zipline-exemption-19111c.pdf) | user-supplied decision, official docket page also captured |
| Amazon Prime Air Exemption 19031B | [PDF](../verification/out/sources/book_intake/authority/faa-19031b-amazon-prime-air-2023.pdf) | historical decision, not a general model-safety conclusion |
| NHTSA AQ26002 opening resume | [PDF](../verification/out/sources/book_intake/authority/nhtsa-aq26002-opening-resume-2026.pdf) | investigation opening record only |
| EASA AI Concept Paper Issue 2 | [PDF](../verification/out/sources/retrieval_check/easa_issue2.pdf) | retrieved background material |
| EASA AI Concept Paper Proposed Issue 3 | [PDF](../verification/out/sources/retrieval_check/easa_issue3.pdf) | retrieved background material |
| UK CAA CAP3127 DAA policy consultation response | [PDF](../verification/out/sources/retrieval_check/caa_cap3127.pdf) | retrieved policy material |
| NASA RTA UAS record 20240007986 | [PDF](../verification/out/sources/retrieval_check/nasa_rta_20240007986.pdf) | earlier retrieved version; do not count independently from related NASA material |

The NHTSA 2025 interpretation and SAE J3321 public-scope page are browser-inspected research records but do not yet have retained full local snapshots; both remain context-limited until lawful capture succeeds. Their direct links and retrieval details are in [the standards-authority source record](contributions/standards_authority/sources.json).

## User-supplied books and reference PDFs

These are in [book_dump](../book_dump) and normalized copies are in [`out/sources/books`](../out/sources/books). Consult [book inventory](books_inventory.md) for edition, rights, duplication, and provisional-status notes.

* [Autonomous Driving / Springer open-access copy](../out/sources/books/autonomous_driving_springer_oa.pdf)
* [Engineering a Safer World](../out/sources/books/engineering_a_safer_world.pdf)
* [Verifiable Autonomous Systems](../out/sources/books/verifiable_autonomous_systems.pdf)
* [Probabilistic Robotics early draft](../out/sources/books/probabilistic_robotics_draft.pdf)

## Following a specific assertion

1. Start in [whitepaper.md](../resource_composition/whitepaper.md) or the [interactive prototype](../resource_composition/review_prototype/index.html); bracketed claim IDs identify factual assertions.
2. Find the claim in the appropriate lane `claims.json`, then follow its `region_id` to the lane `sources.json` record for source URL, locator, source status, inspection scope, and local context/snapshot path.
3. Read the native PDF above, then compare the cited locator and captured context. The compiler’s [review package output](../verification/out/review_packages.json) shows exactly which source region and manuscript uses a model reviewer saw.

An absent local PDF does not mean the source is absent from the research register. It can mean the source is a web page, licensed material not retained locally, or an uncompleted retrieval target.

## Portable e-ink review

For a readable Xteink X4 Pro copy of any text-bearing PDF in this library, use the [CrossPoint PDF review toolkit](../resource_composition/crosspoint_review/README.md). It produces an EPUB with a chapter per original PDF page and an adjacent digest manifest; it does not replace the native PDF for visual-layout checks. Generated EPUBs, previews, and manifests remain in ignored `out/` paths.
