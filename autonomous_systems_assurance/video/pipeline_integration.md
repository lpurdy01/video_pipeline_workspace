# Pipeline reuse without old-project coupling

Existing implementation references:

- `../../verification_compiler_video/pipeline/style.py`, `stage.py`, `beats.py`, `camera3d.py`: scene/layout primitives; parameterize palette/grammar and project paths.
- `../../verification_compiler_video/pipeline/timing.py`: script/audio alignment; inspect project-specific constants before reuse.
- `../../verification_compiler_video/pipeline/build.py`, `qa.py`, `gate_all.py`: geometry, readability and duration checks; retain planted-defect tests.
- `../../representation_transform_visuals/narration_pipeline/transcribe_words.py`: local transcription of human recordings.
- `../../verification_compiler_video/pipeline/gemini_review.py`: visual review mechanism; extend settled-frame sampling with transition frames and narrative context.
- `../../verification_compiler_video/launch/make_captions.py`: script wording with aligned times; regenerate against final playback speed.

Do not invoke these entry points on the new project until inputs/outputs are explicitly parameterized. The new `storyboard.md` is not a runnable production manifest. A renderer-compatible manifest will be created after scene and narration contracts are settled.

Compiler integration should bind: source claim → exact script section and figure description → beat/scene → audio/script versions → rendered clip hash → caption timing → delivery hash. A script or speed edit invalidates timing-dependent output; a factual edit invalidates affected narration/visual review even if the render is geometrically unchanged.

Before human review: structural checks, readable keyframes, semantic/source review of visual claims, and motion/transition review. Passing any one does not stand in for the others.
