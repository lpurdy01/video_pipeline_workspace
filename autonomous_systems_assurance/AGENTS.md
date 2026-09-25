# Project instructions

This is a separate project about assurance for learned autonomous systems. Do not merge its wiki into `project_wiki/` or `representation_transform_visuals/`. Reuse the earlier production mechanisms with explicit project paths; do not copy old claims, certification conclusions, or release statuses into this project.

- Read `PROJECT_BRIEF.md`, `planning/decisions.md`, `wiki/index.md`, `verification/ARCHITECTURE.md`, and `coordination/README.md` before extending the project. Concurrent agents require exclusive write paths and ID namespaces; no shared registry edits by research workers.
- Maintain original sources separately from synthesis. Stable IDs and source locators are mandatory for factual claims intended for publication. Record inspection scope, jurisdiction, document status, date, and uncertainty.
- The seed source register is `research/sources.json`; seed claims are in `verification/claims.json`. Research lanes own `research/contributions/<lane>/sources.json` and `claims.json`; the compiler merges them and rejects duplicate IDs. Tag manuscript and narration uses with `[C-NNN]` or namespaced IDs such as `[C-AIR-001]`. Synthesis pages may cross-link cyclically; build dependencies must remain bounded and versioned.
- Keep support, contradiction, background, and inference distinct. An LLM verdict, two agreeing models, a vendor announcement, and an authority decision are different kinds of evidence.
- Never upgrade a source's scope: a planned standard is not published, a TSO authorization is not installation approval, military certification is not civil certification, and operational permission is not proof of unrestricted model safety.
- Treat models learned before deployment separately from systems that learn during operation; stochastic training does not imply random inference.
- Preserve unsettled claims and counterexamples. The title, narration, captions, diagrams and launch copy all require factual review.
- Keep generated media, downloaded full sources, and raw API outputs under ignored `out/`. Preserve selected release artifacts only through an explicit release inventory. Do not redistribute licensed standards.
- Keep human recordings under `video/assets/human_audio/`; local transcription and alignment only. No voice, speaker embeddings, or timing-rich human artifacts to a cloud service without explicit per-request permission.
- Credentials use the existing `workspace_credentials.require("NAME")` mechanism. Never place keys in tracked files.
- Cloud review/generation permission is recorded in `planning/decisions.md`; earlier project-specific permissions alone do not settle it for this new project.
- Proposed production baseline: deterministic rendered visuals, human final narration, scratch TTS only for drafts, no music. These are carried-forward working defaults, not newly confirmed requirements.
- No autonomous system developed here is authorized for physical deployment. Toy examples must state assumptions and evidence limits.
- Update `wiki/index.md` for maintained wiki pages and append to `wiki/log.md` for substantive research and decision updates.
