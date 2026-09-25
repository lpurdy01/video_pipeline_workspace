# Verifiability Compiler Workspace

This repository contains three separate projects, including the new [Assurance for Learned Autonomous Systems](autonomous_systems_assurance/README.md) whitepaper/video workspace.

The new project starts with a car perceiving and avoiding hazards, then takes the same architecture into flight. It includes [research](autonomous_systems_assurance/research/initial_findings.md), [resource composition](autonomous_systems_assurance/resource_composition/README.md), [video](autonomous_systems_assurance/video/README.md), an [executable verification compiler](autonomous_systems_assurance/verification/README.md), and a [parallel-agent workflow](autonomous_systems_assurance/coordination/README.md).

## Project 1: Verifiability Compiler

The original project explores a requirements-oriented whitepaper and future prototype for a verifiability compiler: a system for turning specifications, implementation artifacts, reviews, tests, and evidence into traceable validation workflows.

Primary folders and files:

- `WHITEPAPER_STAGE_1_STRUCTURE.md`
- `project_wiki/`
- `graphify-corpus/`
- `graphify-out/`
- `refrence_literature/`

## Project 2: Representation Transform Visuals

The newer project develops a standalone public-facing concept: modern AI as a new kind of learned representation transform that maps language, code, images, sound, and other human representations into vector spaces where computation can act on relationships, then maps results back out into useful forms.

This project is intended to produce:

- a 3Blue1Brown-style narrated YouTube video;
- a LinkedIn/article-style whitepaper;
- diagrams and animations around representation transforms, technology trees, vector spaces, and lossy transformation.

Primary folder:

- `representation_transform_visuals/`

Current tooling in that folder:

- `manim_prototypes/`: Manim-first animation experiments and shared visual style helpers.
- `manifest_pipeline/`: manifest-driven section builder for modular audio/video assembly.
- `prototype_pipeline/`: render/stitch prototypes, including scratch narration muxing.
- `narration_pipeline/`: Gemini TTS experiments for scratch audio, local word-level transcription for human audio, and beat-map generation.
- `image_review_pipeline/`: Gemini visual review of generated keyframes before human review.

Current production tools:

- `manim_prototypes/new_transform_space.py`: Manim prototype scene for signal transforms, token/vector spaces, and semantic transform loss.
- `manim_prototypes/visual_style.py`: shared dark-background, neon-color Manim helpers.
- `production_manifest.json`: modular section manifest for script chunks, audio chunks, visual sources, talking-head placeholders, and human asset requirements.
- `manifest_pipeline/build_from_manifest.py`: one-command prototype builder that uses human chunks when available, scratch Gemini TTS otherwise, then writes a complete prototype and asset checklist.
- `manifest_pipeline/extract_review_frames.py`: extracts manifest-defined review frames from the assembled prototype.
- `manifest_pipeline/review_manifest_build.py`: runs frame extraction and Gemini visual review for the manifest build.
- `manifest_pipeline/review_to_todos.py`: converts Gemini review output into section-level visual TODOs.
- `prototype_pipeline/mux_manim_audio.py`: mux a rendered Manim video with narration audio.
- `prototype_pipeline/render_manim_with_audio.py`: legacy/simple Manim scratch-audio mux path.
- `prototype_pipeline/render_prototype.py`: older Pillow/NumPy prototype renderer; useful as a fallback or quick storyboard renderer, not the target final style.
- `narration_pipeline/gemini_tts.py`: Gemini TTS scratch narration generation.
- `narration_pipeline/transcribe_words.py`: local faster-whisper word timestamp transcription.
- `narration_pipeline/make_beat_map.py`: rough beat timing JSON from word timestamps.
- `narration_pipeline/list_gemini_models.py`: model availability probe for the local Gemini key.
- `image_review_pipeline/review_keyframes.py`: Gemini visual review of generated keyframes and stills.

## Relationship Between Projects

The representation-transform project is not part of the verifiability compiler project. It should remain independently understandable and publishable.

The verifiability compiler may later reference the representation-transform work as conceptual groundwork, especially for the idea that English-to-code generation is a powerful but lossy transform that needs verification discipline.

## Secret Handling

API keys and local credentials belong in the user credential store at `~/.config/video-pipeline/credentials.env`
(loaded by `workspace_credentials.py`), or in ignored `.env` files / shell environment variables.

Do not commit real keys in `.env.example`, Markdown, scripts, generated reports, or shell snippets.

## Human Audio Policy

For the representation-transform project, text-based project artifacts may be sent to approved compute APIs such as Gemini for script editing, analysis, scratch TTS, and visual-review context.

The user's real voice should stay local by default. Store recordings under `representation_transform_visuals/assets/human_audio/`, transcribe them locally with faster-whisper via `representation_transform_visuals/narration_pipeline/transcribe_words.py`, and use local word-timing artifacts for animation alignment.

Do not upload raw human voice recordings, speaker embeddings, voiceprints, or timing-rich human narration artifacts to cloud APIs unless the user explicitly approves that specific upload.
