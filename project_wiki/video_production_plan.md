# Verification Compiler Video Production Plan

## Purpose

This document translates the production workflow learned from the
`representation_transform_visuals/` video into a staged plan for a second video
about the Verification Compiler project.

The first video proved a reusable pipeline:

```text
concept -> sources -> script -> storyboard -> manifest -> scratch narration
-> Manim sections -> assembled prototype -> review frames -> visual critique
-> fixes -> human narration/assets -> final render
```

The second video should reuse that production logic, but not the same thesis or
approval assumptions. This project is about assurance, traceability,
requirements, evidence, and bounded review. Its video needs a more disciplined
claim surface than the representation-transform project.

## What We Learned From The First Video

The first video did not start as a finished production pipeline. It moved
through a series of development stages, visible in the current files and commit
history.

### 1. Concept Scaffold

Initial artifacts established the thesis, audience, sources, script, visual
storyboard, and production process.

Key files:

- `representation_transform_visuals/concept_brief.md`
- `representation_transform_visuals/visual_storyboard.md`
- `representation_transform_visuals/tech_tree.md`
- `representation_transform_visuals/sources.md`
- `representation_transform_visuals/production_process.md`
- `representation_transform_visuals/drafts/script.md`

Lesson: start with a clear mental model before writing scenes. The first
video's reusable core was "representation -> transform space -> computation ->
representation." The second video needs an equally compact spine.

Candidate spine:

```text
requirements -> artifact graph -> bounded review packages -> evidence graph
-> verification readiness
```

### 2. Source And Claim Discipline

The first project separated metaphor from technical claim and developed source
ledgers, review notes, loss-term research, and later deep-research-assisted
lineage work.

Key files:

- `representation_transform_visuals/loss_terms_research.md`
- `representation_transform_visuals/source_videos.json`
- `representation_transform_visuals/drafts/tech_tree_research_prompt.md`
- `representation_transform_visuals/drafts/tech_tree_lineage_review.md`

Lesson: the video can be bold, but the claims need lanes:

- visual metaphor
- supported technical claim
- speculative implication

For the Verification Compiler video, this is more important because standards,
certification, and AI assurance are easy to overstate.

### 3. Reference Frame And Visual Language Study

The first project captured source-video frames, built contact sheets, studied
visual language, and used those references to steer Manim composition.

Key files:

- `representation_transform_visuals/source_frame_pipeline/`
- `representation_transform_visuals/assets/reference_frames/`
- `representation_transform_visuals/visual_language.md`
- `representation_transform_visuals/manim_prototypes/make_contact_sheet.py`

Lesson: visual direction should be explicit before scene implementation. The
second video should develop a visual language around graphs, evidence packets,
review gates, source-region addressing, and readiness dashboards instead of
generic AI imagery.

### 4. Script And Article Co-Development

The first project targeted both a narrated video and a LinkedIn/article-style
whitepaper. The script went through voice notes and rewrites rather than being
treated as a transcript of the article.

Key files:

- `representation_transform_visuals/drafts/script.md`
- `representation_transform_visuals/drafts/whitepaper_section.md`
- `representation_transform_visuals/drafts/voice_studies/`
- `representation_transform_visuals/drafts/review_2026_05_30_user_feedback.md`

Lesson: draft the article and video together, but let them specialize. The
article can carry caveats and source detail; the video should carry the mental
model and the felt need.

### 5. Rough Prototype Before Final Tooling

Before the polished Manim path, the first project used a quick Pillow/NumPy and
ffmpeg prototype renderer. That validated the production loop before finalizing
animation architecture.

Key files:

- `representation_transform_visuals/prototype_pipeline/render_prototype.py`
- `representation_transform_visuals/prototype_pipeline/README.md`

Lesson: early prototype quality can be low as long as it validates section
order, narration length, and scene transitions. Do this before spending days
on beautiful Manim.

### 6. Manim-First Scene System

The final direction became Manim-first: shared palette, helpers, scene rules,
section scene classes, contact sheets, and scene-specific render scripts.

Key files:

- `representation_transform_visuals/manim_prototypes/visual_style.py`
- `representation_transform_visuals/manim_prototypes/storyboard_sections.py`
- `representation_transform_visuals/manim_prototypes/MANIM_SCENE_RULES.md`
- `representation_transform_visuals/manim_prototypes/render_storyboard_sections.sh`
- `representation_transform_visuals/manim_prototypes/scene_durations.json`

Lesson: Manim worked best once the video was broken into named sections with a
shared visual grammar and scene-quality rules.

### 7. Manifest As Production Spine

The first video became much easier to manage once `production_manifest.json`
defined each section's title, narration, audio paths, visual source, review
keyframes, and human asset checklist entries.

Key files:

- `representation_transform_visuals/production_manifest.json`
- `representation_transform_visuals/production_manifest_1080.json`
- `representation_transform_visuals/manifest_pipeline/build_from_manifest.py`
- `representation_transform_visuals/manifest_pipeline/extract_review_frames.py`
- `representation_transform_visuals/manifest_pipeline/review_manifest_build.py`
- `representation_transform_visuals/manifest_pipeline/review_to_todos.py`

Lesson: the manifest should be introduced early for the second video. It
prevents the project from becoming a pile of disconnected scenes.

### 8. Scratch Narration And Timing

The first project used scratch TTS for timing, then added local transcription,
word timestamps, beat maps, phrase anchors, and strict alignment checks.

Key files:

- `representation_transform_visuals/narration_pipeline/gemini_tts.py`
- `representation_transform_visuals/narration_pipeline/transcribe_words.py`
- `representation_transform_visuals/narration_pipeline/make_beat_map.py`
- `representation_transform_visuals/narration_pipeline/narration_align.py`
- `representation_transform_visuals/narration_pipeline/HUMAN_ALIGNMENT_WORKFLOW.md`
- `representation_transform_visuals/narration_pipeline/anchor_phrases.json`

Lesson: animation timing should eventually be phrase-driven, not hand-tuned
with arbitrary waits. Scratch narration is enough for early structure, but
final scene timing should align to recorded or approved narration.

### 9. Automated Visual Review And TODO Conversion

For the first video, generated frames were extracted and reviewed by Gemini,
then converted into section-level TODOs.

Key files:

- `representation_transform_visuals/image_review_pipeline/review_keyframes.py`
- `representation_transform_visuals/manifest_pipeline/review_manifest_build.py`
- `representation_transform_visuals/manifest_pipeline/review_to_todos.py`

Lesson: external visual critique is useful when it receives scene intent and
multiple keyframes. For the Verification Compiler video, this requires a new
approval decision. The Gemini upload approval documented in `AGENTS.md` is
specific to `representation_transform_visuals/`, not automatically to this
project's generated frames or source material.

### 10. Layout Validation And Render Quality Gates

The first video added layout checks after repeated readability issues.

Key files:

- `representation_transform_visuals/manim_prototypes/layout_validate.py`
- `representation_transform_visuals/drafts/workflow_plan_2026_05_31.md`

Lesson: text-heavy technical scenes need validation hooks. The second video is
even more likely to fail through tiny labels, overloaded graphs, and crowded
evidence tables, so layout validation should be part of the first Manim pass.

### 11. Human Asset Handoff

The manifest build produced human asset checklists and allowed human audio or
talking-head video to replace placeholders section by section.

Key files:

- `representation_transform_visuals/assets/human_audio/README.md`
- `representation_transform_visuals/assets/human_video/README.md`
- `representation_transform_visuals/manifest_pipeline/out/human_asset_checklist.md`

Lesson: final production should not require recording the whole video at once.
Keep per-section narration and asset replacement from the beginning.

### 12. Final Render And Publish Pass

The last stage added final 1080 manifest support, SRT generation, phrase anchor
checks, visual readability repair, and final publish-ready output.

Key files:

- `representation_transform_visuals/production_manifest_1080.json`
- `representation_transform_visuals/manifest_pipeline/build_srt.py`
- `representation_transform_visuals/narration_pipeline/check_phrase_anchors.py`
- `representation_transform_visuals/manim_prototypes/scene_durations.json`

Lesson: final rendering is a separate stage, not just a bigger version of the
prototype. It needs subtitle generation, audio timing, visual polish, and
explicit publish gates.

## Second Video Working Thesis

Working title:

**The Verification Compiler**

Alternate titles:

- The Compiler For Trust
- When AI Has To Prove Its Work
- The Bottleneck Is Verification
- From Requirements To Evidence
- The System That Turns AI Review Into Audit Trails

Core thesis:

```text
AI makes it cheaper to generate software artifacts. The hard problem becomes
proving what those artifacts satisfy. A verification compiler treats
requirements, code, tests, sources, reviews, and physical evidence as a typed
artifact graph, then compiles that graph into bounded review packages and
auditable evidence.
```

Important boundaries:

- This is not a claim that LLMs can certify safety-critical software.
- LLM results should be framed as developmental review unless promoted by a
  human reviewer.
- The deterministic parts are the graph, traversal, package assembly, evidence
  records, and review workflow.
- The human-reviewed evidence package remains the certification-facing object.
- Public FAA/NASA/EASA/NHTSA/CISA sources can support broad framing, but
  licensed standards should not be quoted or treated as directly available
  unless the project has rights to use them.

Primary audience:

- engineers interested in AI-assisted software development
- safety-critical and embedded software people
- technical leaders thinking about verification cost
- AI builders who need a mental model for trustworthy automation

Tone:

- clear, sober, and ambitious
- less mystical than the representation-transform video
- visually elegant, but grounded in auditability and traceability
- the excitement comes from making verification legible, not from replacing
  experts

## Proposed Story Spine

### 1. Opening: Generation Is Getting Cheap

Show code, tests, documents, diagrams, and plans being produced quickly.
Narration lands the bottleneck: if generation gets cheap, trust does not
automatically get cheap.

Visual:

```text
artifact flood -> narrow verification gate
```

### 2. Safety-Critical Software Already Knows This Problem

Introduce traceability, requirements, review, analysis, tests, and evidence as
coordination machinery, not bureaucracy for its own sake.

Visual:

```text
requirement -> design -> code -> test -> result -> evidence record
```

### 3. The Missing Shape: Artifacts As A Graph

Show requirements, source regions, code units, tests, static analysis, physical
test records, model outputs, and human reviews as typed nodes and edges.

Visual:

```text
typed artifact DAG with orphan/anomaly highlighting
```

### 4. Compilation Means Traversal

Explain the compiler analogy: not a code compiler, but a deterministic process
that traverses the graph and emits review packages.

Visual:

```text
top-level requirement -> traversal beam -> bounded verification query packages
```

### 5. The Verification Query Package

Open one package. It contains the code unit, linked requirements, relevant
source-region text, tests, results, analysis, and instructions.

Visual:

```text
VQP packet unfolding into labeled panes
```

### 6. Same Package, Two Review Modes

Show model review and human review receiving the same package and producing the
same structured result schema.

Visual:

```text
one VQP -> LLM developmental review
        -> human certification-facing review
```

### 7. Evidence Records, Not Chat Transcripts

Emphasize structured outputs: pass/fail/uncertain, rationale, citations,
reviewer ID, prompt version, model version, timestamp, code hash.

Visual:

```text
chat bubble dissolves -> immutable evidence card
```

### 8. Readiness Is A Measured Surface

Introduce VRM as a dashboard, not a magic truth score. Separate coverage,
evidence completeness, staleness, and model suitability.

Visual:

```text
coverage map + stale evidence dimming + readiness dashboard
```

### 9. What Goes Wrong

Show orphan requirements, orphan code, stale source-region hashes, mismatched
test versions, low model suitability, and human/model disagreement.

Visual:

```text
artifact graph with red anomaly pulses and routed review queues
```

### 10. The End State

The goal is not "AI says it is safe." The goal is a navigable evidence surface
where humans can inspect exactly what was checked, by whom or what, against
which artifacts, and with what unresolved gaps.

Visual:

```text
artifact graph -> evidence package -> human decision surface
```

## Planned Project Stages

### Stage 0: Project Boundary And Folder Setup

Goal: create a dedicated production area for the Verification Compiler video
without mixing it into `representation_transform_visuals/`.

Recommended folder:

```text
verification_compiler_video/
  README.md
  concept_brief.md
  drafts/
    script.md
    article.md
    storyboard.md
  assets/
    human_audio/
    human_video/
    reference_frames/
  manim_prototypes/
  manifest_pipeline/
  narration_pipeline/
  image_review_pipeline/
  production_manifest.json
```

Do not create this folder until the initial concept plan is accepted. For now,
this wiki page is the planning anchor.

Deliverable:

- accepted folder and asset policy

Gate:

- user confirms whether external visual review APIs are approved for generated
  VC video artifacts

### Stage 1: Thesis And Claim Map

Goal: define the compact thesis and identify every claim that needs evidence.

Inputs:

- `project_wiki/concepts/verification_compiler.md`
- `project_wiki/concepts/safety_critical_traceability.md`
- `project_wiki/concepts/verification_as_evidence_production.md`
- `project_wiki/concepts/model_or_tool_qualification.md`
- `project_wiki/requirements/verification_compiler_requirements.md`
- `project_wiki/traceability/source_to_claim_matrix.md`
- `WHITEPAPER_STAGE_1_STRUCTURE.md`

Deliverables:

- `concept_brief.md`
- claim-lane table: metaphor / supported claim / speculation
- 8 to 12 scene story spine

Gate:

- no unsupported certification claim remains in the story spine

### Stage 2: Source And Evidence Pass

Goal: prepare citation-safe source support for the video and article.

Work:

- verify which claims are already supported by `source_to_claim_matrix.md`
- mark weak claims as "visual metaphor" or remove them
- collect exact source pages/sections for article citations
- avoid licensed-standard overreach
- identify any new sources needed for final claims

Likely source clusters:

- DO-178C public summaries and FAA AC 20-115D
- NASA software assurance and software engineering requirements
- requirements traceability and ambiguity sources
- task-specific LLM accuracy and overcorrection sources
- decomposition / bounded query literature
- regulatory AI roadmap context, with caveats

Deliverables:

- source ledger for video claims
- list of claims retired from narration
- article citation skeleton

Gate:

- every technical claim in narration has either a supporting source, a caveat,
  or a deliberate "metaphor only" label

### Stage 3: Visual Language And Reference Study

Goal: define how this project looks on screen.

Candidate visual grammar:

- dark background with bright evidence paths
- graph nodes as typed artifacts
- requirements as stable anchors
- source-region nodes as document AST slices
- traversal as a deterministic scanning beam
- VQPs as packets or bundles
- human review gates as explicit checkpoints
- stale evidence as fading or hash-mismatch fractures
- dashboards as restrained engineering UI, not marketing UI

Deliverables:

- `visual_language.md`
- 6 to 10 still-frame sketches
- first Manim style helper or adaptation plan from prior `visual_style.py`

Gate:

- one static storyboard pass can explain the whole video without narration

### Stage 4: Script And Companion Article Draft

Goal: produce a narration script and article that share the same argument but
serve different reading modes.

Video script target:

- 6 to 9 minutes
- 10 to 12 sections
- short sentences and visual beats
- repeated core pattern: requirement -> graph -> package -> review -> evidence

Article target:

- 1,500 to 2,500 words
- carries citations, caveats, definitions, and regulatory boundaries
- can link back to project wiki pages

Deliverables:

- `drafts/script.md`
- `drafts/article.md`
- `drafts/storyboard.md`

Gate:

- read-aloud pass confirms the script sounds like a person, not a standard
  compliance memo

### Stage 5: Manifest Spine

Goal: introduce the manifest before heavy rendering.

Work:

- split the script into section objects
- add scratch audio path per section
- add expected human audio path per section
- add visual source per section: Manim scene, existing clip, or placeholder
- add review keyframes per section
- add human asset checklist prompts

Deliverables:

- `production_manifest.json`
- manifest build script, adapted from the first video if appropriate
- generated script chunks
- generated human asset checklist

Gate:

- one command can build a complete low-resolution placeholder prototype

### Stage 6: Scratch Narration And Rough Prototype

Goal: validate timing, scene order, and narrative continuity.

Options:

- use local/simple scratch narration if external TTS is not approved
- use Gemini scratch TTS only if approval is explicitly extended to this project
- use the existing narration pipeline pattern once policy is settled

Deliverables:

- complete low-resolution prototype
- per-section durations
- first subtitle draft if practical

Gate:

- prototype is coherent even with placeholder visuals

### Stage 7: Manim Section Implementation

Goal: implement the core diagrams as named Manim scenes.

Priority scenes:

1. artifact flood into verification bottleneck
2. traceability chain
3. artifact graph / DAG
4. traversal into VQP packages
5. VQP unfolding
6. dual-mode model/human review
7. immutable evidence records
8. VRM/dashboard breakdown
9. anomaly detection
10. final evidence surface

Implementation rules from the first video:

- use shared style helpers early
- keep text sparse and large
- validate safe areas and text fit
- render contact sheets for each scene
- avoid dense full-graph diagrams at 480p
- use section-specific simplifications rather than showing every node

Deliverables:

- first Manim scene set
- contact sheets
- layout validation hooks
- updated manifest with rendered scene paths

Gate:

- each scene has start/middle/end review frames that are readable at 480p

### Stage 8: Review Loop

Goal: critique the prototype before human review spends attention on fine
details.

Local review checklist:

- does every scene have one visual focus?
- can labels be read on laptop and mobile?
- are certification boundaries stated correctly?
- does the graph metaphor remain deterministic and auditable?
- does any scene imply "LLM certifies safety"?
- are source claims still supported?

Optional external review:

- generated frames may be sent to Gemini only after explicit approval for this
  project
- raw human audio and human timing artifacts should remain local unless
  explicitly approved

Deliverables:

- review frames
- visual review notes
- section-level TODOs
- revised script if review finds conceptual confusion

Gate:

- no high-severity conceptual or readability issues remain

### Stage 9: Human Narration And Timing Alignment

Goal: replace scratch narration with human narration and align animation beats.

Work:

- record one section per file
- keep raw human audio local
- transcribe locally with faster-whisper
- generate word timestamps and beat maps locally
- use phrase anchors for key animations

Deliverables:

- human audio files
- local word timestamp JSON
- local beat maps
- phrase anchor file
- strict alignment preflight

Gate:

- section renders match narration without awkward waits or cutoffs

### Stage 10: Final Polish, Subtitles, And 1080 Render

Goal: produce the publish-ready video.

Work:

- create 1080 manifest
- render full-resolution Manim scenes
- build SRT subtitles
- mux final audio
- review final keyframes and full video
- export article stills if useful

Deliverables:

- final 1080 video
- SRT captions
- article stills
- companion article draft
- release checklist

Gate:

- final review confirms visual readability, audio timing, source boundaries,
  and no hidden placeholder assets

## First Implementation Milestones

1. Write `verification_compiler_video/concept_brief.md`.
2. Draft the 10-section story spine from this page into `drafts/storyboard.md`.
3. Build a claim-lane table from `source_to_claim_matrix.md`.
4. Sketch the first three visuals: artifact flood, traceability chain, artifact
   graph.
5. Create the first `production_manifest.json`.
6. Build a placeholder prototype before implementing polished Manim.

## Reuse Candidates From The First Video

Strong candidates to adapt:

- manifest schema and build loop
- review frame extraction
- human asset checklist generation
- Manim visual style helper pattern
- layout validation helper
- narration alignment and phrase anchors
- SRT builder

Use with care:

- Gemini TTS and visual review scripts, because approval was project-specific
- tech-tree visual vocabulary, because this video needs graph/evidence
  vocabulary instead
- philosophical narration voice, because this topic needs more assurance
  discipline

Do not reuse:

- representation-transform thesis or folder
- source-video frame assets
- generated output paths from `representation_transform_visuals/`

## Open Decisions

- Should the second video be public-facing YouTube first, article first, or a
  whitepaper explainer with video support?
- Should we create a new top-level `verification_compiler_video/` folder, or
  place production assets under a `video/` subfolder of the wiki/project?
- Is Gemini approved for generated VC keyframe review and scratch narration, or
  should the first prototype use only local tooling?
- Should the video show the existing self-referential prototype and VRM results,
  or stay conceptual until the prototype is cleaned up?
- How much standards language should appear in narration versus the companion
  article?

## Immediate Recommendation

Use the first video's pipeline, but start smaller:

1. produce a concept brief and claim-lane table;
2. draft a 10-section script;
3. build a manifest-backed placeholder prototype;
4. implement only three high-value Manim scenes first:
   artifact graph, VQP assembly, and dual-mode review;
5. review those scenes for visual clarity and claim safety before expanding the
   full video.

This preserves the best lesson from the first project: build the production
spine early, then let individual scenes mature inside it.
