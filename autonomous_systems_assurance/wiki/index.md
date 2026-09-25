# Wiki index

- [Architecture vocabulary](concepts/assurance_vocabulary.md): distinctions needed to explain the case accurately.
- [Open tensions](concepts/open_tensions.md): competing explanations and failure cases to preserve.
- [Frozen learned-systems next steps](../planning/learned_systems_assurance_next_steps.md): project claim, evidence contracts, research gates and compiler extension plan.
- [Gemini integration status](../planning/gemini_integration_status.md): sanitized API health check, current quota diagnosis and safe retry sequence.
- [Vision-training source findings](../research/contributions/training_case/findings.md): AMLAS data, learning and independent-verification failure modes plus the textbook underfit/overfit distinction.
- [AMLAS/MAA/EASA crosswalk](../assurance/amlas_maa_easa_crosswalk.md): comparison to the eight evidence contracts and their boundaries.
- [Machine-readable method crosswalk](../assurance/method_crosswalk.json): typed method-to-obligation mappings and stated coverage limits.
- [Figure plan](../resource_composition/figures.md): rendered and planned figures, their claim links, and their visual limits.
- [Whitepaper reader contract](../resource_composition/reader_contract.md): section-level audience acceptance map, separate from claim verification.
- [Technical reference](../resource_composition/technical_reference.md): detailed companion preserving the full methods, case, compiler and source-card argument.
- [Long-form project flow](../planning/longform_project_flow.md): evidence gates, 14-part reader journey and 30+ minute video/paper targets.
- [Editorial audience gate](../planning/editorial_audience_gate.md): artifact-level reader contract and advisory audience audit, kept separate from claim verification coverage.
- [Long-form video proposal](../video/nextgen_structure/README.md): isolated 34-minute treatment, visual inventory and claim map pending formal review.
- [Direction/risk coverage integration](../research/integration_round5.md): EASA proposed authority/risk boundaries, NHTSA incident-data limits, EV denominator limits and the professional-qualification finding.
- [Recording-feedback script](../video/script.md): claim-tagged long-form narration draft with local feedback pauses.
- [Verification dashboard](../verification/dashboard.md): local static reader for current source, claim, paper, script and review status.
- [Worked assurance-case graph](../assurance/assurance_case.json): machine-readable hypothetical road release, hazards, assumptions, obligations and planned evidence.
- [Log](log.md): chronological research and decision history.

Canonical records outside the wiki: [source register](../research/sources.json), [claims](../verification/claims.json), [initial findings](../research/initial_findings.md), [worked architecture](../assurance/architecture.md), [verification architecture](../verification/ARCHITECTURE.md).

Integrated research contributions: [Texas authorization and road-to-air handoff](../research/contributions/road_air/findings.md), with independently owned source/claim records included by the compiler. Integration is structural; its factual claims remain provisional.

Current round-2 integration: [research integration report](../research/integration_round2.md), covering ROAD, AIR and METHOD handoffs, duplicate URLs, conflicts and next retrieval tasks.

Current round-3 integration: [learned-systems assurance research](../research/integration_round3.md), covering the authority, evidence-method and adversarial challenge lanes plus Gemini lead triage.

Current round-4 integration: [standards status and risk evidence](../research/integration_round4.md), covering the public-method status ladder, the FMVSS self-certification boundary, risk-context evidence and unresolved source retrieval.

Authority-document and browser intake: [intake findings](../research/contributions/intake_20260915/findings.md), with public FAA decision letters, TSO-C211a and a dated TxMCCS lookup captured in an independently owned contribution.

Supporting-document status: [retrieval report](../research/retrieval_status.md), including SHA-256 hashes for acquired PDFs/pages and the records requiring a human browser or rights decision.

Native-source navigation: [local source library](../research/local_source_library.md), with direct links to retained PDFs and the path from claims to source records and review packages.

Source capture staging: [source-context recovery](../research/source_recovery/README.md), with the official-source retrieval process and its current limits.

Portable e-ink review: [CrossPoint PDF review toolkit](../resource_composition/crosspoint_review/README.md), which creates source-page-located EPUB packages and manifests for Xteink X4 Pro review. It is a reading surface, not a review-disposition system.

Book intake: [book inventory and verification](../research/books_inventory.md), including local format conversions, source limitations, and the remaining aviation-book gaps.

The wiki is a maintained synthesis view. It may not silently promote a claim's review status or substitute itself for its original source.

## [2026-09-22] implement | Current review dashboard and recording script

Added a claim-tagged, eight-part narration draft for local voice feedback and made it a manifested artifact, so paper and script uses now participate in the same digest-pinned review packages. Added a static local dashboard generated from the compiler graph. It links every displayed claim to its recorded primary source URL and region, shows whitepaper/script use, distinguishes current model pass/uncertain/open outcomes, and excludes stale review records from current counts.

The first fresh Gemini source-support pass against the post-script baseline returned both passes and uncertainty. Uncertainty is retained where the captured local source context does not support a confident source decision; it is not converted to a passing gate. Four current source-support claims were additionally subjected to model challenge and cross-artifact review. The dashboard's generated counts are the authority for the live result; no human dispositions have been recorded.

## [2026-09-22] integrate | Coverage-map and risk-metric correction

Added a source-scoped public-assurance coverage map for paper/video. It distinguishes documents that address an ML component, a case-specific military path, a research roadmap, proposed civil authority/risk material, or incident reporting. The retained EASA NPA confirms that proposed Level 3B is reserved and that its proposed H1/potential-fatality row is unacceptable at every likelihood band; it does not support a general claim that all organizations reject every AI risk or that Level 3B is an approved autonomous mode.

Added full-context NHTSA sources that prevent two misleading comparisons: incident reports are not normalized crash rates, and an older EV/hybrid rulemaking lacked powertrain-specific VMT for a direct pedestrian/pedalcyclist per-mile comparison. A current NCEES page lists no ML PE specialty, but this narrow taxonomy observation does not establish the proposed causal explanation about professional maturity or qualified people. Those claims stay deferred pending focused historical and international evidence.
