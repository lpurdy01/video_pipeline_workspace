# Parallel work protocol

This project supports independent research, whitepaper composition and video development. File ownership is the coordination mechanism: an active job has one writer, bounded output paths and a recorded input baseline. Agents exchange handoffs rather than editing one another's work.

Read the project [brief](../PROJECT_BRIEF.md), [decisions](../planning/decisions.md), [wiki index](../wiki/index.md) and [compiler architecture](../verification/ARCHITECTURE.md) before starting. [lanes.json](lanes.json) assigns default namespaces and write boundaries; the [job template](tasks/job_template.md) records each concrete assignment. The inventory is a planned allocation, not a lock service or proof that an agent is running.

## Default team

| Lane | Independent work | Exclusive outputs |
|---|---|---|
| ROAD | Road permissions, learned driving systems, Cybercab inquiry, operating scope | `research/contributions/road/` |
| AIR | DAA capability, equipment versus operation approvals, aviation AI guidance | `research/contributions/air/` |
| METHOD | Learning assurance, runtime assurance, interpretability, system identification | `research/contributions/method/` |
| PAPER | Worked argument, whitepaper prose and figure specifications | `resource_composition/` |
| VIDEO | Hook, narrative, storyboard, scene and production work | `video/` |
| INTEGRATOR | Resolve proposals, update shared knowledge, compile and choose review baselines | Canonical registers, wiki, architecture, coordination and publication |

All workers may read the entire project. Read permission does not make a live file a stable input. All default output boundaries are relative to `autonomous_systems_assurance/`. A job may narrow a lane's ownership, but expanding it requires the coordinator to check that no other active writer owns the new paths. Only the integrator changes `lanes.json` or shared job assignments while workers run. Workers write their progress and results under `coordination/handoffs/<lane>/<job-id>/`.

At this session's four-agent limit, an integrator can run three research agents together. Three researchers plus paper and video writers require at least five worker slots; a concurrently active integrator makes six. Additional sessions can supply those workers, or jobs can run in waves. Git worktrees isolate files but do not increase the tool's agent limit. This setup does not launch background workers or create worktrees by itself.

## Start a job

1. The coordinator copies the [template](tasks/job_template.md), gives it a unique job ID and assigns an owner/session, namespace and exact write paths. Check existing active jobs before assignment.
2. Record the starting commit plus hashes of the actual relevant files. A commit alone is insufficient in a dirty shared workspace. Include the source/claim baseline and the paper/video files the job depends on.
3. The worker acknowledges those boundaries in its own handoff directory. Capture search date, query, original publisher and retrieval outcome for web work; record failed retrievals and negative searches without interpreting them as proof of absence.
4. Research workers create `sources.json` and `claims.json` in their contribution directory using the current canonical schema. Use `S-ROAD-001` / `C-ROAD-001`, `S-AIR-001` / `C-AIR-001`, or `S-METHOD-001` / `C-METHOD-001`; region IDs follow the source, for example `S-AIR-001-R1`. Never repurpose an existing ID for a different proposition or source.
5. Preserve full permitted downloads and generated/API output beneath ignored `out/` directories; structured source records retain actual snapshot paths and hashes. Do not invent snapshot hashes, quotations or review provenance. Human audio and timing remain local under the project rules.
6. Finish with a handoff specifying changed files, input/output hashes, proposed claims, contrary findings, verification performed and unresolved work. The integrator freezes that handoff before review and integration.

If two people need to research the same lane simultaneously, the coordinator creates distinct directories and ID prefixes first, such as `air_approvals` / `AIRAPP` and `air_sensing` / `AIRSENSE`. These remain one directory level below `research/contributions/` so the compiler's `research/contributions/*/sources.json` and `claims.json` discovery finds them.

## Shared workspace or worktrees

**Shared workspace:** exclusive files avoid lost updates. Do not run repository-wide formatters, mass renames, destructive resets or cleanup of another worker's output. Reading a file during its writer's save can expose an incomplete JSON document; compiler discovery is not an atomic transaction across files. Integrate only completed handoffs, pause writes to the selected inputs, and rerun compilation against the frozen set. A report produced from moving inputs is a draft diagnostic.

**Separate worktrees/sessions:** give each job a separate branch/worktree and the same ownership/namespace boundaries. Record the common base commit and actual dirty input hashes where relevant. Downloads in ignored `out/` will not arrive through a commit; transfer required local snapshots through an explicit manifest and verify hashes at the destination. The integrator reviews patches and merges or cherry-picks one job at a time, resolves conflicts, then recompiles. Do not assume a clean Git merge proves semantic consistency.

Both modes use the same handoff format. Avoid shared external build destinations, filenames or cache writes: use a job-specific `out/<job-id>/` path when a tool permits it. If a reused pipeline has a fixed output directory, give that build a single owner until its paths are parameterized.

## Deterministic integration

1. Select completed handoffs in an explicit recorded order. Pin their input/output manifests and reviewer tasks. Reject missing files, duplicate IDs and namespace violations before content promotion.
2. Check duplicate URLs, editions, source regions and originating evidence. Two sources with distinct IDs may repeat one announcement; preserve their actual independence group. Resolve semantic duplicates with an explicit ID mapping and update references instead of silently overwriting records.
3. Review scope and exact source context. Preserve contradictions and rejected propositions in the handoff history. An abstract, vendor statement, government announcement and actual approval document have different evidentiary scope.
4. Keep accepted contribution registries in place as compiler inputs, or move selected records into canonical registers and remove those exact records from the contribution registry in the same integration change. Never leave an ID in both locations. Integration into canonical storage is distinct from claim acceptance.
5. Apply approved synthesis changes to the wiki and architecture, then reconcile paper/video proposals. Record changed claim text and affected uses. Run the compiler after the full change set is stable and inspect validation failures, review queues and downstream impact.
6. Attach review records using the compiler's implemented schema and exact review-package digest. Record human disposition separately from model feedback. Publish a new authoring baseline only after its limitations and unresolved claims are visible.

Compiler validation cannot establish file ownership, source independence, exhaustive research or truth by itself. This protocol supplies human/agent coordination around the checks; it does not claim a distributed transactional build service exists.

## Paper and video coordination

The paper and video owners can draft simultaneously against the same pinned claim baseline. The paper develops the argument and qualifications; the video develops an accessible road encounter that becomes airborne near the end. Neither author owns the other output, the shared architecture or canonical claim wording.

Each author tags factual uses with the exact claim ID, including prefixed IDs such as `[C-AIR-001]`. New claims, simplifications that change scope, figure assertions and changes to the shared worked example go in a handoff proposal. The integrator resolves the proposal and asks both authors to update affected uses. An approved claim is not automatic approval of every paraphrase, visual or title.

The executable manifest is `verification/artifacts.json`; new prose is outside artifact-use review until the integrator adds it there. Compilation discovers contribution registries automatically, but does not automatically discover every draft Markdown file. Existing `research/contributions/road_air/` records are a setup contribution with their own `ROAD-AIR` prefix, not an active assignment to either future default research lane.

Before recording narration or locking a render, use the [baseline template](baselines/template.json) to pin the actual paper, script, storyboard, figures, claim/source inputs and compiler report. The template's null values are deliberate: it is not an existing approved baseline. If a shared claim or scenario assumption changes, identify both paper and video dependencies, regenerate affected review packages and rebuild affected scenes. Preserve unresolved differences until a named person resolves them; do not silently let the manuscript and narration tell different stories.

## Independent challenge

Have another worker inspect consequential claims against their original context and search for defeating evidence. Assign a challenge question, not an instruction to validate the author's conclusion. Record reviewer/session identity, model/provider when applicable, search path, exact input digest, supporting and contrary source regions, result, limitations and human disposition.

Different agents or models reading the same source provide reviewer diversity, not independent evidence. Shared training data, search results or a syndicated vendor statement can correlate their answers. Neither a majority vote nor two matching model verdicts upgrades an authority's actual scope or closes a missing-evidence obligation. Detailed machine-consumable review records must follow the compiler contract; a narrative handoff is useful provenance but does not automatically satisfy its review gate.

The implemented tasks are `source_support`, `challenge`, `cross_artifact` and `human_disposition`; the last requires a human reviewer. Import real records through `compile.py --import-review <file>` so an existing review ID cannot be overwritten by that command. Context completion requires an actual source snapshot, its SHA-256, an inspected UTF-8 context file and `context_status: full_context`; a short excerpt is not sufficient. The compiler's normal successful exit establishes structural compilation. Its `--release` check covers the manifested research/composition inputs, with final media and public-package checks still to be added.
