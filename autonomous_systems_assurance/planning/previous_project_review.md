# Previous project: research to release

Review date: 2026-09-08. Based on local source, code, generated reports, handoff notes, release package and the user's analytics. This is a process reconstruction, not a rerun of every historical build. Existing uncommitted work was left in place.

## 1. Research and whitepaper construction

[`WHITEPAPER_STAGE_1_STRUCTURE.md`](../../WHITEPAPER_STAGE_1_STRUCTURE.md) began with source collection, concepts, evidence-bearing claims, requirements, and an outline. [`source_inventory.md`](../../refrence_literature/source_notes/source_inventory.md) records public FAA/NASA PDFs and extracted text, with licensed standards treated separately. The local LLM-wiki reference informed the separation of raw sources, maintained synthesis, and publication.

[`PROJECT_WIKI_SCHEMA.md`](../../project_wiki/PROJECT_WIKI_SCHEMA.md) defined source, concept, claim and requirement pages, an index, an ingest workflow and a log. [`graphify_workflow.md`](../../project_wiki/graphify_workflow.md) used Graphify to discover candidate relationships; only inspected links were to enter the claim map. This promotion boundary is useful and should remain.

The argument developed through `Introductory_composition.md`, wiki requirements and source-to-claim mapping. Diagram specifications and rendering lived under `whitepaper/`. [`build_pdf.py`](../../whitepaper/build_pdf.py) uses Markdown, HTML/CSS and WeasyPrint, with report/conference layouts and figure injection. The later release source is [`verification_compiler_whitepaper.md`](../../whitepaper/verification_compiler_whitepaper.md). That distinction matters: some earlier tools still point at the earlier composition file.

## 2. Cross-verification and revision

[`verification_prototype/`](../../verification_prototype/PLAN.md) implements graph building, deterministic traversal into citation/coverage/orphan packages, Gemini review, structured results and reporting. The original builder used source-name heuristics, section hints and truncation. [`learnings.md`](../../verification_prototype/data/learnings.md) and [`project_wiki/log.md`](../../project_wiki/log.md) document wrong source matches, missing support edges, stale cached results, and content hidden by traversal. One early run's apparent success excluded citation work that should have run.

The saved 2026-05-30 [report](../../verification_prototype/data/verification_report.md) reports 27/27 citation passes, 30 covered requirements and one partial, with VRM 0.992. This is a historical model-review result. It is not a probability the paper is correct, and it is not a review of every later release byte. The public [prototype notes](../../verification_compiler_resources/evidence/prototype_notes.md) explicitly say much verification used curated source notes rather than original sources.

The separate saved `whitepaper/out/deep_research_validation.md` challenged the metric, prior art and missing coupling/object-code concerns; `coherency_review.md` identified duplication, structure and citation issues. These show a useful distinction between content evidence, adversarial research and editorial review. Model statements about novelty or qualification remain claims to verify, even when a review labels them confidently.

**Carry forward:** stable IDs, original-source regions, exact artifact versions, planned-versus-completed review counts, explicit missing work, independent evidence searches, and human disposition. **Change:** eliminate fuzzy evidence binding, silent truncation, cache reuse by filename alone, and a headline scalar that can hide unreviewed obligations.

## 3. Video construction

The [video workspace](../../verification_compiler_video/README.md) separated script, storyboard, modular manifest, Manim scenes, review and recordings. Final policy was rendered visuals, real narration, no generated video and no music; TTS served drafts.

[`pipeline/README.md`](../../verification_compiler_video/pipeline/README.md) explains the mature approach: spoken audio is the clock; local word timestamps align script lines; each beat anchors a visual change to a line; timing budgets compress animation to fit. Style constructors, stage layout, per-frame geometry checks and build checks catch different defects. Planted-defect self-tests caught failures in the checkers themselves, including geometry disappearing from 3D checks.

[`HANDOFF.md`](../../verification_compiler_video/HANDOFF.md) and [`PIPELINE_STATUS.md`](../../verification_compiler_video/PIPELINE_STATUS.md) record geometry QA, frame inspection, Gemini settled-frame critique, grouped findings and human review. Settled frames cannot verify motion. Passing geometry cannot establish composition quality or whether a graphic says something false.

The final logged integration uses 240 narration lines/beat anchors, local human alignment and drift within 0.05 seconds for the marked cut. The delivery log identifies 1080p30, 796.4-second 1x and 692.7-second 1.15x outputs. Those are recorded measurements, not new measurements in this review.

**Carry forward:** reusable style/stage/beat/timing/QA mechanisms, short per-scene implementations, review frames plus transition samples, local human audio and separate scratch/final states. Add source-claim links to narration and visual assertions before animation work begins.

## 4. Resource composition and publication

The companion package is a separate nested Git repository, [`verification_compiler_resources/`](../../verification_compiler_resources/README.md). Its latest local commit is `065f716` (2026-08-29), removing internal publishing plans. It contains PDF/Markdown/HTML, figures, bibliography, requirements, claim maps, prototype limitations, MIT license, citation metadata, a concept map, boundaries, and compact agent entry points. [`LINKS.md`](../../verification_compiler_resources/LINKS.md) centralizes outward-facing URLs.

The [launch kit](../../verification_compiler_video/launch/LAUNCH.md) bundles delivery selection, captions, title/thumbnail variants, chapters, description, pinned comment and LinkedIn copy. Captions use script wording plus local aligned timing, including speed-adjusted variants. This prevents technical terminology from being replaced by ASR guesses.

The user confirms the published video and resource GitHub. The local launch notes identify `https://github.com/lpurdy01/verification_compiler_resources`; a browser fetch was unsuccessful in this review, so current anonymous accessibility and byte-for-byte remote equivalence were not independently established.

## 5. Release consistency issues to design out

- Working-title references to *The Compiler For Trust* coexist with the user's published title *The Software AI Isn't Allowed To Write*.
- Some launch QA counts predate the later readability triage in `PIPELINE_STATUS.md`.
- The prototype report predates the final video and packaged whitepaper. No complete immutable release-to-evidence binding was established by this inspection.
- Some historical notes disagree about the reviewer model/version. Preserve records and use actual run metadata when reporting a run.
- Launch advice about social algorithms is editorial folklore unless independently measured; do not encode it as a production invariant.

These are process lessons, not an attempt to repair the released project. The next release should have one manifest binding the source revision, review records, paper, narration, visuals, captions and public links.

## 6. Audience feedback as a design input

See [analytics baseline](analytics_baseline.md). Prioritize an early concrete mechanism, repeated visual explanations, and an integrated resource invitation. Treat the retention interpretation as a hypothesis from one video; the supplied overview contains inconsistent aggregate values and is not a controlled experiment.
