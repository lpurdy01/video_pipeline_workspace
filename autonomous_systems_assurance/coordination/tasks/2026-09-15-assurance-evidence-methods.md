# Job: 2026-09-15-assurance-evidence-methods

Status: integrated

- Owner and session: unassigned
- Coordinator: integrator
- Lane and ID prefixes: `assurance_evidence`; `S-EVID-*`, `C-EVID-*`
- Objective and bounded research/challenge question: Identify what data/training lineage, scenario/statistical testing, uncertainty, formal analysis, runtime assurance, interpretability and change-control methods can actually establish for a frozen trained component—and their failure conditions.
- Why this matters to the road-to-air example: It turns “more data,” “a score,” or “AI inspection” into explicit evidence obligations that can be tested against an occluded-conflict scenario.
- Exact allowed write paths: `research/contributions/assurance_evidence/`, `coordination/handoffs/assurance_evidence/2026-09-15-assurance-evidence-methods/`
- Handoff directory: `coordination/handoffs/assurance_evidence/2026-09-15-assurance-evidence-methods/`
- Shared workspace or worktree/branch: shared workspace with exclusive paths
- Base commit: record at start
- Dirty input files and SHA-256 values: record the source/claim registries and retrieved source snapshots used
- Source/claim/compiler input baseline: record compiler report at start
- Required source jurisdictions, dates and document types: primary papers plus authority guidance; stable methods rather than company demonstrations
- Dependencies or answers needed from another lane: use the planned contract names in `planning/learned_systems_assurance_next_steps.md`
- Out of scope: designing a real vehicle controller; treating a method paper as evidence of deployed certification

## Deliverables

- `sources.json`, `claims.json`, and `findings.md` under the assigned contribution directory.
- One method-to-contract mapping for each selected source, including assumptions, missing evidence and a practical counterexample.
- A recommendation for the minimum evidence needed for the road worked case.

## Acceptance checks

- Follow `coordination/tasks/job_template.md` and preserve source context, dates, versions and counterevidence.
- Distinguish a measured performance result from a probability-of-safe-operation claim.
- Do not endorse a composite safety score unless a source supplies and defends its complete assumptions.
