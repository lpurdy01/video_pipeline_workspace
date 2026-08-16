# Manim Scene Rules Learned From Vector Analogy

## Agent Instructions

**Always use the best available Gemini model for visual review. Cost is not a concern; quality is.**

- Visual review default: `auto`, currently resolving to the strongest available preferred critique model. Prefer `gemini-3.1-pro-preview` when available, then newer Pro aliases/previews, then `gemini-2.5-pro` as fallback.
- TTS/narration: `gemini-3.1-flash-tts-preview`
- Do not default to lighter models like `gemini-2.5-flash` without a reason.

Run reviews via the manifest pipeline:

```bash
python3 representation_transform_visuals/manifest_pipeline/review_manifest_build.py \
  --out representation_transform_visuals/manifest_pipeline/out/manifest_visual_review_roundN.md \
  --todos-out representation_transform_visuals/manifest_pipeline/out/manifest_visual_todos_roundN.md \
  --model auto
```



These notes capture the practical rules that got `vector_analogy_benchmark.py`
from a flat, glitchy prototype to a cleaner 3Blue1Brown-style scene.

## Visual Language Rules

- Let narration carry explanation. On-screen text should be sparse: labels,
  equations, or one short phrase that must be seen.
- Use a black or near-black background, bright colored geometry, and thin glows.
  The scene should feel like math in space, not like a slide.
- Keep labels larger than feels necessary in still code review. Oblique 3D camera
  angles, compression, and motion all make text harder to read.
- Avoid visible instructional text such as "this is a vector space" when motion
  can communicate the same thing.
- Use color consistently as semantic identity:
  - `king`: gold
  - `man`: blue
  - `woman`: violet
  - `queen`: green
  - prediction / computed target: cyan
  - relationship transform arrow: gold
- Fade supporting geometry down once it has done its job. Axes and grids should
  establish dimensionality, then recede so the relationship arrows can dominate.

## Manim Tools That Worked

- `ThreeDScene` for the vector-space sections.
- `ThreeDAxes` for dimensional context, with `include_ticks: False` to avoid
  graph-paper clutter when exact coordinates are not important.
- `NumberPlane` as a dim back-plane only, not as the main visual layer.
- `Line3D` for position vectors from the origin. It avoids arrowheads that can
  look like stray dots when viewed head-on.
- `Arrow3D` for relationship vectors where direction matters, such as
  `man -> king` and the copied direction from `woman -> prediction`.
- `Dot3D` for anchor points after vectors fade out. Small dots work better than
  large spheres because they mark position without becoming visual clutter.
- `add_fixed_orientation_mobjects(...)` for labels that should face camera
  movement while staying tied to their 3D locations.
- `add_fixed_in_frame_mobjects(...)` only for true overlay phases, such as the
  initial word boxes and vector tables.
- `move_camera(...)` near the end to prove dimensionality after the core diagram
  is already legible.

## Manim Pitfalls We Hit

- Fixed-frame objects can leak into later 3D scenes after transforms. When
  leaving a 2D overlay beat, remove them with both:

  ```python
  self.remove_fixed_in_frame_mobjects(tokens, columns, arrows, dots)
  self.remove(tokens, columns, arrows, dots)
  self.clear()
  ```

- `FadeOut` on nested children of a parent group can appear to fail if the parent
  group is still being rendered. For clean transitions, fade out the whole group
  and fade in a fresh object for the next visual role.
- `Indicate(...)` on complex table/vector-column groups created a white/gray
  block artifact in the render. A small scale pulse was more stable:

  ```python
  self.play(col.animate.scale(1.035), run_time=0.32)
  self.play(col.animate.scale(1 / 1.035), run_time=0.32)
  ```

- 3D arrowheads can masquerade as dots depending on camera angle. Use arrowheads
  only when the viewer needs direction, not for every vector from the origin.
- Labels that look fine in one still frame can collide during camera motion.
  Review labels across a contact sheet, not only at the final frame.
- Axis ticks add visual noise fast. If the numbers are not part of the argument,
  remove ticks and lower axis opacity.

## Scene Structure Pattern

The vector analogy scene now follows this beat pattern:

1. Word tokens appear as clean 2D overlays.
2. Tokens map into numeric vector columns.
3. Columns collapse to simple colored points.
4. The 2D overlay layer is explicitly cleared.
5. A 3D space appears with word points and labels.
6. Origin-to-word vectors briefly establish coordinate meaning.
7. Origin vectors fade out, leaving anchor points and labels.
8. A relationship arrow appears from `man` to `king`.
9. The relationship arrow is copied/transformed to start at `woman`.
10. The computed prediction appears near `queen`, with a dashed error/approximation
    gap.
11. The equation appears after the geometry has done the work.
12. A subtle camera move confirms that the scene is spatial.

This pattern is more robust than trying to keep every visual layer alive at once.
Each layer earns its moment, then gets dimmed or removed.

## Review Workflow

- Render without cache when chasing artifacts:

  ```bash
  manim -ql --format=mp4 --flush_cache --disable_caching --media_dir ../prototype_pipeline/out/manim_media vector_analogy_benchmark.py VectorAnalogyBenchmark
  ```

- Generate a contact sheet after each meaningful visual change:

  ```bash
  python3 make_contact_sheet.py ../prototype_pipeline/out/manim_media/videos/vector_analogy_benchmark/480p15/VectorAnalogyBenchmark.mp4 --out out/vector_analogy_contact_sheet.png --every 1 --columns 4 --thumb-width 320
  ```

- Review the contact sheet locally before sending frames to Gemini. The contact
  sheet catches:
  - blink frames;
  - stale fixed-frame objects;
  - label collisions over time;
  - camera motion that destroys readability;
  - scene beats that happen too quickly.
- Send Gemini both the scene intent and multiple frames. Treat Gemini as an
  external critic, not as ground truth. Its most useful feedback is concrete:
  "label overlaps," "axis ticks add clutter," "arrows do not read as parallel."

## Quality Bar Before Human Review

Before asking for human review, check that:

- no fixed-frame artifacts survive into the 3D scene;
- no text label sits directly on top of an active arrow or axis;
- relationship arrows read as direction, not just lines;
- the point-cloud phase is visually distinct from the origin-vector phase;
- final camera motion improves dimensionality without making the equation or
  labels unreadable;
- the contact sheet tells the story even without narration.
