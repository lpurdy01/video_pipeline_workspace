# Manifest Pipeline

This is the modular production spine for the video.

It reads `../production_manifest.json`, then builds each section as an independent unit:

1. write the section narration into `out/script_chunks/`;
2. use human audio from `../assets/human_audio/` when present;
3. otherwise generate scratch Gemini TTS audio;
4. use human video or a rendered/source clip when present;
5. otherwise create a dark placeholder clip;
6. mux each section into `out/section_clips/`;
7. concatenate the complete prototype video;
8. write `out/human_asset_checklist.md`.

Run:

```bash
python3 representation_transform_visuals/manifest_pipeline/build_from_manifest.py
```

Useful outputs:

- `out/complete_prototype.mp4`: current full prototype render.
- `out/human_asset_checklist.md`: recording and human asset punch list.
- `out/resolved_manifest.json`: exact audio/video source used per section.
- `out/script_chunks/`: one narration text file per section.
- `out/review_frames/`: manifest-defined review frames extracted from the assembled prototype.
- `out/manifest_visual_review.md`: Gemini visual review of the extracted frames.
- `out/manifest_visual_todos.md`: generated section-by-section TODOs from the review.

The pipeline is designed so narration can be recorded one section at a time. Drop a real WAV into `../assets/human_audio/` using the manifest filename and rerun the build; that section will automatically switch from scratch TTS to human narration.

Direct-to-camera sections work the same way. Drop the expected MP4 into `../assets/human_video/` and rerun the build; the placeholder will be replaced by the human footage.

## Extract Review Frames

```bash
python3 representation_transform_visuals/manifest_pipeline/extract_review_frames.py
```

The extractor reads `review_keyframes` from `../production_manifest.json` and section timing from `out/resolved_manifest.json`.

## Gemini Review

The user has approved uploading generated frames from this project to Gemini for visual review.

```bash
python3 representation_transform_visuals/manifest_pipeline/review_manifest_build.py
```

The manifest review defaults to `--model auto`, which selects the strongest available preferred Gemini visual-review model. Pin a model only for reproduction or comparison.

To regenerate TODOs from an existing review without calling Gemini:

```bash
python3 representation_transform_visuals/manifest_pipeline/review_to_todos.py
```
