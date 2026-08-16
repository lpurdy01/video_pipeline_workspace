# Workspace Instructions

This workspace has two distinct projects:

1. **Verifiability Compiler**
   - Use `project_wiki/`, `WHITEPAPER_STAGE_1_STRUCTURE.md`, `graphify-corpus/`, `graphify-out/`, and `refrence_literature/`.
   - Focus on requirements, traceability, validation evidence, software assurance, and agent/tool qualification.

2. **Representation Transform Visuals**
   - Use `representation_transform_visuals/`.
   - Treat this as a separate public-facing concept project.
   - Target smart generalists, engineers, and YouTube viewers.
   - Favor bold philosophical framing over deep implementation detail.
   - Build toward two outputs: a narrated 3Blue1Brown-style video and a LinkedIn/article-style whitepaper.

Do not merge the representation-transform project into the verifiability compiler wiki unless explicitly asked. It can be referenced later as conceptual background, but it should stand alone.

For the representation-transform project:

- Fourier, Laplace, z-transform, DCT, and related concepts may be invoked at a high level with strong visuals rather than full derivations.
- The core mental model is `representation -> vector/transform space -> computation -> representation`.
- English-to-code should be treated as the central practical example because it is familiar to programmers, coding assistants, and "vibe coding" workflows.
- Keep a clear distinction between useful metaphor and exact mathematical claim.
- Treat LLM-style transformation as powerful, approximate, and lossy; develop language around the specific kind of loss without prematurely claiming a settled technical term.
- Keep generated media and API outputs under ignored `out/` directories unless the user explicitly asks to preserve a particular artifact.
- Keep real API keys only in ignored `.env` files or shell environment variables. `.env.example` must remain placeholder-only.
- Use `narration_pipeline/` for TTS, transcription, word timestamps, and beat maps.
- Keep the user's real voice recordings local by default. Use local transcription/alignment tools such as `narration_pipeline/transcribe_words.py` and faster-whisper for human recordings. Do not upload raw human audio, derived voiceprints, or timing-rich human narration artifacts to Gemini or other cloud APIs unless the user gives explicit per-request approval.
- Text-based artifacts derived from the project, including scripts, transcript text, commentary summaries, and rewrite notes, may be sent to approved compute APIs such as Gemini for script refinement, scratch TTS, and analysis. Prefer sending edited text excerpts rather than raw audio.
- Use `image_review_pipeline/` to run Gemini visual review on keyframes before asking for human visual review.
- Use `production_manifest.json` and `manifest_pipeline/` for modular video builds. Each manifest section may have its own script chunk, scratch or human narration, Manim/existing/placeholder visual source, talking-head footage, and human asset checklist entry.

Current tool inventory:

- `representation_transform_visuals/manim_prototypes/new_transform_space.py`: Manim-first prototype scene.
- `representation_transform_visuals/manim_prototypes/visual_style.py`: shared Manim palette and neon/glow helpers.
- `representation_transform_visuals/manim_prototypes/render_manim_prototype.sh`: render the Manim prototype.
- `representation_transform_visuals/production_manifest.json`: section manifest for modular rendering, chunked narration, visual source selection, and human asset tracking.
- `representation_transform_visuals/manifest_pipeline/build_from_manifest.py`: builds a complete low-resolution prototype video from the manifest, using human assets when present and scratch placeholders/TTS when missing.
- `representation_transform_visuals/manifest_pipeline/extract_review_frames.py`: extracts `review_keyframes` from the completed manifest prototype using resolved section timing.
- `representation_transform_visuals/manifest_pipeline/review_manifest_build.py`: extracts review frames and sends them through the Gemini visual review pipeline.
- `representation_transform_visuals/manifest_pipeline/review_to_todos.py`: converts Gemini's manifest review into section-level visual TODOs.
- `representation_transform_visuals/manifest_pipeline/out/human_asset_checklist.md`: generated recording and asset punch list after a manifest build.
- `representation_transform_visuals/prototype_pipeline/mux_manim_audio.py`: mux Manim video with a selected narration file.
- `representation_transform_visuals/prototype_pipeline/render_manim_with_audio.py`: scratch-audio Manim mux helper.
- `representation_transform_visuals/prototype_pipeline/render_prototype.py`: older Pillow/NumPy prototype renderer for quick rough cuts only.
- `representation_transform_visuals/narration_pipeline/gemini_tts.py`: Gemini TTS generation.
- `representation_transform_visuals/narration_pipeline/transcribe_words.py`: faster-whisper word timestamps.
- `representation_transform_visuals/narration_pipeline/make_beat_map.py`: beat timing JSON from word timestamps.
- `representation_transform_visuals/image_review_pipeline/review_keyframes.py`: Gemini keyframe review. Its default `--model auto` resolves the strongest available preferred visual-review model; use Pro-class Gemini 3.1 review when available rather than older 2.5 defaults.

Before freerunning on a full prototype video, useful infrastructure candidates are:

- per-section Manim scene classes that replace the current existing-video reuse in `production_manifest.json`;
- optional manifest steps for transcription and beat-map generation;
- a keyframe extractor that samples every scene boundary automatically from the beat map;
- a visual regression folder of accepted keyframes for comparing style drift between renders;
- a pronunciation dictionary for technical words such as Fourier, Laplace, spectra, embeddings, and Manim/TTS voice quirks;
- a lightweight review summarizer that turns Gemini's keyframe critique into actionable TODOs by file/scene.

## Representation Transform Gemini Approvals

For the `representation_transform_visuals/` project, the user has explicitly approved using the Google Gemini API as an external feedback and generation path.

Approved uploads to Gemini:

- generated visual artifacts from this pipeline, including keyframes, stills, and prototype-render frames, for automated visual review;
- demo narration and script text from this project, including `representation_transform_visuals/prototype_pipeline/out/manim_scratch_narration.txt`, for scratch TTS generation and related narration workflow experiments.
- text-based project artifacts, including script drafts, transcript text, commentary summaries, rewrite plans, visual prompts, and article drafts, for analysis and editing.

Not approved by default:

- raw human voice recordings;
- human narration audio chunks;
- voiceprints, speaker embeddings, or other biometric voice representations;
- word-level timing artifacts from human narration when they could reveal the cadence of a private voice sample.

Default audio workflow:

1. Store human recordings under `representation_transform_visuals/assets/human_audio/`.
2. Transcribe locally with `representation_transform_visuals/narration_pipeline/transcribe_words.py` / faster-whisper.
3. Use local transcript text and local timing JSON for script rewrite and animation alignment.
4. Send only text excerpts or summaries to Gemini unless the user explicitly approves uploading the audio itself.

Rationale from the user: the finished project is intended for YouTube, a Google platform, and Gemini is considered acceptable for this project's intellectual-property risk profile.

Still do not commit real API keys. Store keys only in ignored `.env` files or shell environment variables.
