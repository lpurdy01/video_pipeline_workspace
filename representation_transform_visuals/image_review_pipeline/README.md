# Image Review Pipeline

## Model Selection

**Use the best available Gemini model for visual review. Cost is not a concern.**

Default is `auto`. The reviewer lists models available to the configured key and picks the strongest preferred visual-review model, currently prioritizing:

1. `gemini-3.1-pro-preview`
2. `gemini-pro-latest`
3. `gemini-3-pro-preview`
4. `gemini-2.5-pro`

Do not downgrade to Flash or Lite models without a specific speed/cost reason. Cost is not a concern for this review loop; critique quality is.

To see what model `auto` resolves to:

```bash
python3 representation_transform_visuals/image_review_pipeline/review_keyframes.py --print-model
```

This pipeline gives the animation workflow an external visual feedback path before human review.

It uses a Gemini vision-capable model to inspect keyframes or stills and identify issues such as:

- text too small, too large, tilted, or overlapping;
- low contrast or dim important objects;
- vectors, axes, matrices, or labels being hard to read;
- composition feeling too much like a slide deck;
- visual clutter or missing narrative focus;
- mismatches against the project's visual language.

## Key Handling

The script reads `GEMINI_API_KEY` from:

1. the shell environment, or
2. `representation_transform_visuals/.env`

Do not put keys in committed files. `.env.example` must stay as placeholders only.

The user has approved sending generated visual artifacts from this project to Gemini for automated visual review.

## Review Stills

```bash
python3 representation_transform_visuals/image_review_pipeline/review_keyframes.py \
  --images representation_transform_visuals/prototype_pipeline/out/manim_still_*.png \
  --out representation_transform_visuals/image_review_pipeline/out/manim_keyframe_review.md
```

You may pin a model explicitly when comparing review quality:

```bash
python3 representation_transform_visuals/image_review_pipeline/review_keyframes.py \
  --images representation_transform_visuals/manifest_pipeline/out/review_frames/01_01_hook_transform_tree_start.png \
  --model gemini-3.1-pro-preview \
  --out representation_transform_visuals/image_review_pipeline/out/model_smoke_review.md
```

## Extract and Review Video Keyframes

```bash
python3 representation_transform_visuals/image_review_pipeline/review_keyframes.py \
  --video representation_transform_visuals/prototype_pipeline/out/new_transform_space_manim_with_scratch_audio.mp4 \
  --timestamps 3 10 17 \
  --out representation_transform_visuals/image_review_pipeline/out/manim_video_review.md
```

## Intended Loop

```text
render Manim prototype
  -> extract keyframes
  -> Gemini visual review
  -> patch visual scene
  -> rerender
  -> human review
```
