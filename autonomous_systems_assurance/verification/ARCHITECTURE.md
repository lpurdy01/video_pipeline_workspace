# Research verification compiler and LLM wiki

This is the project's production assurance system. It is separate from the autonomous-system architecture under study.

## Implemented foundation

The standard-library `compile.py` loads the seed registries and independently owned research contributions, validates IDs and references, derives exact claim uses from tagged artifacts, creates versioned review packages, computes a dependency graph, reports changed/affected nodes against a prior build, and detects stale or missing review records. It performs no model calls and grants no certification authority.

```text
primary source + context + version
       ↓
source region ← research lane contributions
       ↓
claim + support/challenge distinction
       ↓
wiki / architecture / paper / narration / figure description
       ↓
bounded review packages + append-only review records
       ↓
coverage, blockers, change impact, eventual release evidence
```

Synthesis cross-links can have cycles. Directed build dependencies cannot. Source IDs resolve exactly; a missing reference fails compilation. Nothing is silently truncated, fuzzy-matched, or treated as reviewed because no result exists.

## Concurrent authorship

Seed registries are integrator-owned. Each research lane owns `research/contributions/<lane>/sources.json`, `claims.json` and notes. The compiler merges these inputs deterministically and rejects duplicate IDs; agents do not race to edit one shared JSON file. Use allocated prefixes such as `S-ROAD-001` and `C-ROAD-001`.

`artifacts.json` is the integrator-owned input manifest. Paper and video authors own different Markdown files with `[C-...]` annotations. Lane drafts may be added to this manifest once ready for a review build. The compiler requires a stable input set during each run; use an integration freeze or isolated worktree and bind handoffs to a revision. See [coordination](../coordination/README.md).

## Review contract

For every claim, produce four packages:

| Task | Reviewer question |
|---|---|
| `source_support` | Does original context support this precise wording, scope and date? For proposals, does it accurately describe the prior work? |
| `challenge` | What primary evidence, counterexample or alternative interpretation could defeat it? |
| `cross_artifact` | Do the included manuscript, narration and visual-description uses preserve its meaning and limits? |
| `human_disposition` | Has the human inspected the evidence and resolved the recorded uncertainty for publication? |

All packages pin claim, source/region/context and artifact-use hashes, plus the task/prompt contract version. The input digest also includes the compiler implementation hash, so changing compiler semantics invalidates older reviews. An existing record for another digest is stale. Reviewer identity and prompt/model metadata are mandatory; model confidence is not converted into a safety probability.

Original-source snapshots live under ignored `out/sources/`. For release eligibility, each region requires `snapshot_path`, matching `snapshot_sha256`, UTF-8 `context_path`, and `context_status: full_context`. A locator and a 15-word excerpt alone are not adequate context. Context is hashed into packages; the compiler checks file consistency, while the reviewer must check that extraction and boundaries faithfully represent the original. A malicious or incomplete extraction cannot be detected by a hash.

Review records are JSON files under `verification/reviews/`. Import with the CLI to prevent overwriting an existing ID. Required fields: `id`, `package_id`, `input_digest`, `task`, `reviewer_id`, `reviewer_kind` (`human` or `model`), `verdict` (`pass`, `fail`, `uncertain`), `created_at` (ISO date or timestamp), `rationale`, `evidence_locators`, `limitations`, and `resolves` (list of earlier review IDs). Model reviews also record `model_id` and `prompt_version`. A human must own `human_disposition`. This is provenance by declaration, not cryptographic identity authentication.

A non-pass review remains blocking until a current human disposition explicitly lists it in `resolves` and explains the decision. Evidence-source independence is not automatically established by distinct reviewers. The queue presents that work; an integrator must assess actual provenance and challenge quality.

Human-disposition packages include the current preceding review results and historical objections; a new review invalidates the earlier disposition. Incoming resolution references are checked against the merged record set before persistence. Review-package digests include transitive artifact dependency hashes, including manifest changes, so impact reporting and review invalidation agree.

## Status and release meaning

Structural validity, contextual source completeness, review coverage and publication readiness are separate outputs. Initial short excerpts deliberately leave context blockers. A successful normal compile means the graph is structurally readable, not that its claims are true. `--release` exits nonzero while any blocker remains.

The initial release check concerns the manifested **research/composition inputs only**. It is not a final video/package shipping gate: rendered assets, audio, captions, timing, permission/rights checks and public-link validation must be added with their own review tasks before production release.

## Design still to complete

- Automated primary-source capture/extraction with persistent region addressing and correction history.
- Model execution adapters, retries, cost accounting, independent challenge retrieval and blinded human review UI.
- Crosswalk ingestion that turns an inspected external method's named artefacts/objectives into reviewed graph links rather than manually maintained comparison prose.
- A compiler gate that requires a hazard's declared obligations to have an evidence-completeness disposition before a worked case is marked closed; the present gate intentionally reports declared blockers without calculating safety probability.
- Fine-grained section/beat nodes; current artifact invalidation is conservative at file level.
- Frozen public release bundles with accessible source context subject to rights restrictions.
- Integration with Manim, local narration alignment and delivery-format inspection.

This foundation provides real queues and change propagation without pretending the larger compiler or the research is finished.

## Worked-case graph: implemented initial schema

`assurance/assurance_case.json` provides an explicit graph for the first hypothetical road encounter. Its node types are `system_release`, `assumption`, `hazard`, `evidence_artifact`, `risk_context` and `obligation`. A risk context binds a hazard to its scenario/exposure assumptions, evidence artifacts, risk statement and metric limit; it deliberately cannot collapse performance, reliability, residual risk and safety into one score. Every obligation names its hazards, assumptions, planned evidence artifacts and relevant research claims. Claims linked from an obligation, risk context or evidence artifact carry those nodes and hashes into their review packages, so a changed ODD assumption, metric limit or recovery obligation invalidates affected claim reviews and propagates impact to dependent paper/video artifacts.

The worked case accepts only `frozen_trained` releases. A release that is merely defined, an open/invalidated assumption, a planned/missing evidence artifact, or an open/in-progress obligation is a separate assurance-case blocker. The compiler does not claim those blockers are the complete safety case; it makes their declared absence visible and prevents a structurally green release check. JSON node validation and review-invalidation behavior are covered by compiler tests.

`assurance/method_crosswalk.json` adds typed external-method and method-to-obligation mapping nodes. Each mapping records whether the inspected method covers an obligation directly, partially, only as a proposal, or outside its scope. The mapping's cited claims and node hashes are added to affected review packages. This permits change impact when a method's status, scope or interpretation changes, while the compiler continues to distinguish a guidance crosswalk from evidence that closes a hazard.
