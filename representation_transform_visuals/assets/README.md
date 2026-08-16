# Human Asset Drop Zone

This folder is for source assets that replace scratch generated pieces in the manifest-driven video pipeline.

Expected human-created assets:

- `human_audio/`: one narration recording per manifest section.
- `human_video/`: direct-to-camera segments, mic shots, or other human footage.
- `source_stills/`: reference images, hand-drawn sketches, finished stills, or production art.

The manifest records the expected filenames. The build pipeline will use a human asset when it exists, and otherwise fall back to scratch TTS or generated placeholders.

Large media files should generally stay local until we intentionally decide what belongs in git.
