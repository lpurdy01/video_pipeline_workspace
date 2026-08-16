# Representation Transform Visuals

## Purpose

This folder develops the visual argument that tokenization, embeddings, transformers, and generative models are part of a broader family of representation transforms.

The working claim is that LLMs are transformative because they let language, code, images, sounds, workflows, and other symbolic or perceptual representations be mapped into computational vector spaces, manipulated there, and mapped back into useful output forms.

This workstream is meant to support:

- a standalone whitepaper or LinkedIn article
- a series of diagrams and visualizations
- a narrated 3Blue1Brown-style YouTube video
- reusable conceptual groundwork that can be referenced by other projects later

## Working Artifacts

- [concept_brief.md](concept_brief.md): first-pass thesis, analogies, limits, and claims.
- [visual_storyboard.md](visual_storyboard.md): candidate graphics and video beats.
- [storyline_reconsideration.md](storyline_reconsideration.md): revised story spine after reviewing source frames.
- [tech_tree.md](tech_tree.md): rough transform-driven technology tree.
- [sources.md](sources.md): initial source ledger and references to review.
- [loss_terms_research.md](loss_terms_research.md): research note on names for LLM-style transform loss.
- [production_process.md](production_process.md): workflow for turning the idea into a document and short video.
- [production_manifest.json](production_manifest.json): modular section manifest for script chunks, audio chunks, visuals, talking-head placeholders, and human asset requirements.
- [source_videos.json](source_videos.json): source video reference ledger for frame capture and visual study.
- [manifest_pipeline/](manifest_pipeline/): one-command manifest build pipeline.
- [manim_prototypes/](manim_prototypes/): prototype animation scenes, likely using Manim.
- [prototype_pipeline/](prototype_pipeline/): render and stitch prototype videos.
- [narration_pipeline/](narration_pipeline/): TTS, speech-to-text, word timestamps, and beat-map tooling.
- [image_review_pipeline/](image_review_pipeline/): Gemini visual review for keyframes and rendered scenes.
- [source_frame_pipeline/](source_frame_pipeline/): YouTube reference frame capture for internal visual study.

## Current Status

This is an exploratory concept scaffold for smart generalists, engineers, and YouTube viewers. The tone should be bold and philosophical: the point is to communicate the civilizational significance of a new kind of transform, not to teach transformer internals.

The analogy to Fourier and Laplace transforms should be visually powerful without pretending learned vector representations have the same exact mathematical guarantees as analytic transforms.

This project is separate from the verifiability compiler. It may become a reference for that work later, but it should stand alone.

## Tooling Loop

```text
draft script
  -> split into manifest sections
  -> generate scratch narration or use per-section human audio
  -> render/select visuals per section
  -> stitch prototype video
  -> produce human asset checklist
  -> transcribe human audio locally to word timestamps and create beat maps as needed
  -> extract keyframes
  -> Gemini image review
  -> patch visuals
  -> human review
```

Real API keys should live in ignored `.env` files, not in committed examples or docs.

## Tool Inventory

### Manim

- [manim_prototypes/new_transform_space.py](manim_prototypes/new_transform_space.py): Manim-first prototype scene.
- [manim_prototypes/visual_style.py](manim_prototypes/visual_style.py): shared color palette and glow helpers.
- [manim_prototypes/render_manim_prototype.sh](manim_prototypes/render_manim_prototype.sh): renders the Manim prototype.
- [manim_prototypes/SYSTEM_REQUIREMENTS.md](manim_prototypes/SYSTEM_REQUIREMENTS.md): WSL dependency notes for Manim.

### Prototype Rendering

- [production_manifest.json](production_manifest.json): current modular video manifest.
- [manifest_pipeline/build_from_manifest.py](manifest_pipeline/build_from_manifest.py): builds a complete prototype video from the manifest.
- [manifest_pipeline/extract_review_frames.py](manifest_pipeline/extract_review_frames.py): extracts manifest-defined review frames from the assembled prototype.
- [manifest_pipeline/review_manifest_build.py](manifest_pipeline/review_manifest_build.py): runs extraction plus Gemini visual review.
- [manifest_pipeline/review_to_todos.py](manifest_pipeline/review_to_todos.py): converts the Gemini review into section-level visual TODOs.
- [manifest_pipeline/README.md](manifest_pipeline/README.md): manifest pipeline usage notes.
- [prototype_pipeline/mux_manim_audio.py](prototype_pipeline/mux_manim_audio.py): muxes a rendered Manim video with arbitrary narration audio.
- [prototype_pipeline/render_manim_with_audio.py](prototype_pipeline/render_manim_with_audio.py): simple scratch-narration mux helper.
- [prototype_pipeline/render_prototype.py](prototype_pipeline/render_prototype.py): older Pillow/NumPy renderer for quick rough cuts and fallback storyboard renders.

### Narration and Timing

- [narration_pipeline/gemini_tts.py](narration_pipeline/gemini_tts.py): Gemini scratch narration generation.
- [narration_pipeline/transcribe_words.py](narration_pipeline/transcribe_words.py): faster-whisper word-level timestamps.
- [narration_pipeline/make_beat_map.py](narration_pipeline/make_beat_map.py): beat timing JSON from word timestamps.
- [narration_pipeline/list_gemini_models.py](narration_pipeline/list_gemini_models.py): Gemini model availability probe.

### Visual Review

- [image_review_pipeline/review_keyframes.py](image_review_pipeline/review_keyframes.py): uploads approved generated keyframes/stills to Gemini for visual review. Manifest reviews include section narration, intended visual prompt, and larger story context so Gemini can critique missing beats and overloaded visualizations, not just composition.

### Source Frame Capture

- [source_videos.json](source_videos.json): reference source ledger.
- [source_frame_pipeline/capture_youtube_frames.py](source_frame_pipeline/capture_youtube_frames.py): uses `yt-dlp` and `ffmpeg` to capture internal reference frames from the source videos.

## Current Manifest Outputs

After running the manifest build:

- `manifest_pipeline/out/complete_prototype.mp4`: complete low-resolution prototype video.
- `manifest_pipeline/out/human_asset_checklist.md`: per-section recording and human asset punch list.
- `manifest_pipeline/out/resolved_manifest.json`: exact audio and visual source used for each section.
- `manifest_pipeline/out/script_chunks/`: one narration text file per section.
- `manifest_pipeline/out/review_frames/`: section-aware review frames.
- `manifest_pipeline/out/manifest_visual_review.md`: Gemini visual review of those frames.
- `manifest_pipeline/out/manifest_visual_todos.md`: generated scene/section TODOs from the review.
- `manifest_pipeline/out/manifest_review_context.md`: section narration and intended visual context passed into Gemini review.

To replace scratch narration, record a section into `assets/human_audio/` using the filename listed in the manifest and rerun the build. To replace the talking-head placeholder, place the expected MP4 in `assets/human_video/`.

## Next Infrastructure Candidates

- **Per-section Manim scenes:** replace current placeholder/existing-video reuse with real section-specific Manim scene classes.
- **Manifest timing hooks:** add optional transcription, beat-map generation, and cue-word alignment per section.
- **Visual review TODOs:** convert Gemini review findings into a small scene-by-scene fix list.
- **Visual regression set:** store a small accepted-keyframe gallery so future renders can be compared against the intended style.
- **Pronunciation dictionary:** keep TTS/STT hints for Fourier, Laplace, spectra, embeddings, tokenization, and other technical terms.
- **Review-to-TODO converter:** turn Gemini visual reviews into actionable TODOs grouped by scene/file.

## Agent Model Selection

**Always use the best available Gemini model for each task.** Cost is not a concern; quality is.

| Task | Recommended model |
|---|---|
| Visual review (keyframes, storyboard critique) | `auto`, currently expected to resolve to `gemini-3.1-pro-preview` when available |
| Scratch TTS narration | `gemini-3.1-flash-tts-preview` |
| Script refinement / narration editing | strongest available Pro model |
| Quick iteration / spot checks | current Flash model only when speed matters |

When calling visual review scripts, prefer `--model auto`. Pin a model only when comparing review quality or reproducing a prior result.

The `review_keyframes.py` and `review_manifest_build.py` scripts default to `auto`, which lists the Gemini models available to the configured key and selects the strongest preferred visual-review model.

## Gemini Approval Scope

For this project, the user has approved sending generated visual artifacts and demo narration/script text to the Google Gemini API for visual review, scratch TTS, and workflow experiments.

Text-based project artifacts may also be sent to approved compute APIs for analysis and editing. This includes script drafts, transcript text, commentary summaries, rewrite plans, article drafts, visual prompts, and generated review context.

Human voice recordings are different. Keep real user recordings local by default:

- Store them under `assets/human_audio/`.
- Transcribe with local tools, currently `narration_pipeline/transcribe_words.py` using faster-whisper.
- Use local `.words.json` and beat-map outputs for timing.
- Do not upload raw human audio, speaker embeddings, voiceprints, or timing-rich human narration artifacts to Gemini or another cloud API unless the user explicitly approves that specific upload.

Do not commit real API keys. Keep them in ignored `.env` files or shell environment variables.
