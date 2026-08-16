# Manim Prototypes

This directory is for early animation experiments.

The target visual style is Manim-first, inspired by 3Blue1Brown: dark background, sparse labels, bright vector geometry, animated axes, matrix-like transforms, and motion carrying the concept instead of slide text.

## Current Prototype

```bash
manim -ql new_transform_space.py NewTransformSpacePrototype
```

Or:

```bash
bash render_manim_prototype.sh
```

## Install Notes

See [SYSTEM_REQUIREMENTS.md](SYSTEM_REQUIREMENTS.md). Manim is not just a Python wheel; it needs Cairo/Pango native dependencies on WSL.

The older `representation_transform_scene.py` file is a simple first smoke test. The newer `new_transform_space.py` file is the direction to develop.

## Vector Analogy Review Loop

`vector_analogy_benchmark.py` is the focused scene for the `king - man + woman ~= queen`
embedding analogy. Render it without Manim cache when investigating visual artifacts:

```bash
manim -ql --format=mp4 --flush_cache --disable_caching --media_dir ../prototype_pipeline/out/manim_media vector_analogy_benchmark.py VectorAnalogyBenchmark
```

Then make a contact sheet for quick human/Gemini review:

```bash
python3 make_contact_sheet.py ../prototype_pipeline/out/manim_media/videos/vector_analogy_benchmark/480p15/VectorAnalogyBenchmark.mp4 --out out/vector_analogy_contact_sheet.png --every 1
```

Manim lessons learned so far:

- Fixed-frame mobjects can survive transforms in surprising ways; explicitly remove them with both `remove_fixed_in_frame_mobjects(...)` and `remove(...)` before moving from a 2D overlay beat into 3D space.
- `FadeOut` of nested `Dot3D` children may not visually remove them if the parent group is still being rendered; for a clean handoff, fade out the parent group and fade in fresh label-only or point-only mobjects.
- 3D arrowheads viewed close to head-on can read as stray dots. Use `Line3D` for position vectors and reserve `Arrow3D` for relationship vectors where direction matters.
- Labels in 3D are fragile under oblique camera angles. Prefer sparse labels, larger offsets, lower axis/grid opacity during relationship beats, and contact-sheet review across the whole motion arc.
- Gemini review is most useful when it receives scene intent plus multiple keyframes. It can still misidentify transitional frames, so pair it with local contact sheets and direct frame inspection.

See [MANIM_SCENE_RULES.md](MANIM_SCENE_RULES.md) for the fuller set of scene
quality rules, Manim pitfalls, and review workflow learned from this iteration.
