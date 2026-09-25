# Job: 2026-09-15-assurance-authority-map

Status: integrated

- Owner and session: unassigned
- Coordinator: integrator
- Lane and ID prefixes: `assurance_authority`; `S-AUTH-*`, `C-AUTH-*`
- Objective and bounded research/challenge question: Build a primary-source matrix of current aviation and road authority/standard material that applies to frozen trained components. What is binding, accepted guidance, proposed guidance, voluntary consensus work, or a limited authorization?
- Why this matters to the road-to-air example: It prevents the paper from claiming that an operating permit, equipment authorization or proposed AI paper proves a general learned-model safety process.
- Exact allowed write paths: `research/contributions/assurance_authority/`, `coordination/handoffs/assurance_authority/2026-09-15-assurance-authority-map/`
- Handoff directory: `coordination/handoffs/assurance_authority/2026-09-15-assurance-authority-map/`
- Shared workspace or worktree/branch: shared workspace with exclusive paths
- Base commit: record at start
- Dirty input files and SHA-256 values: record the source/claim registries and retrieved source snapshots used
- Source/claim/compiler input baseline: record compiler report at start
- Required source jurisdictions, dates and document types: FAA and EASA AI material; US road authority material; ISO/PAS 8800 and UL 4600 status pages; exact editions/current dates; original issuer where possible
- Dependencies or answers needed from another lane: no factual conclusions from other lanes required
- Out of scope: asserting compliance with a licensed standard without inspected clause text; inferring proprietary implementation evidence

## Deliverables

- `sources.json`, `claims.json`, and `findings.md` under the assigned contribution directory.
- A matrix recording source status, jurisdiction, subject, trained-versus-in-service-learning scope, vehicle/system/operation scope, and exact unresolved access limits.
- One contrary finding or limitation for every source family.

## Acceptance checks

- Follow `coordination/tasks/job_template.md` and preserve source context, dates, versions and counterevidence.
- State what a document does **not** establish beside what it does establish.
- Do not convert a proposed or voluntary document into a certification requirement.
