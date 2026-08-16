# Prototype Pipeline

This folder contains the first lightweight production-pipeline experiment.

It intentionally does not require Manim yet. The first pass uses:

- Python
- Pillow
- NumPy
- system `ffmpeg`
- ffmpeg's built-in `flite` speech synthesis for scratch narration

The generated narration is only timing scaffolding. It is meant to be replaced with human narration later.

## Run

From the repo root:

```bash
python3 representation_transform_visuals/prototype_pipeline/render_prototype.py
```

Expected outputs:

```text
representation_transform_visuals/prototype_pipeline/out/
  prototype_visuals.mp4
  scratch_narration.wav
  representation_transform_pipeline_prototype.mp4
  frames/
```

## Manim Prototype Path

After Manim is installed:

```bash
bash representation_transform_visuals/manim_prototypes/render_manim_prototype.sh
python3 representation_transform_visuals/prototype_pipeline/render_manim_with_audio.py
```

Expected Manim output:

```text
representation_transform_visuals/prototype_pipeline/out/
  new_transform_space_manim_with_scratch_audio.mp4
  manim_scratch_narration.wav
  manim_media/
```

To mux a rendered Manim video with any narration audio:

```bash
python3 representation_transform_visuals/prototype_pipeline/mux_manim_audio.py \
  --audio representation_transform_visuals/narration_pipeline/out/gemini_demo_narration.wav \
  --out representation_transform_visuals/prototype_pipeline/out/new_transform_space_manim_gemini_tts.mp4
```

## Why This Pipeline

This lets us validate the production loop before choosing the final animation stack:

1. script excerpt
2. visual sequence
3. scratch narration
4. stitched video
5. review and iterate

Manim can still become the final animation tool for polished math/vector scenes. This script is for moving quickly and proving the pipeline.
