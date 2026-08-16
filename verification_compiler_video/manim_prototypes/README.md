# Manim Prototypes

Rough Manim scenes for **The Compiler For Trust**.

The scenes are intentionally simple first-pass prototypes. Each scene should
prove one visual idea before we spend time on polish.

Run all scenes:

```bash
bash verification_compiler_video/manim_prototypes/render_storyboard_sections.sh
```

Render one scene:

```bash
cd verification_compiler_video/manim_prototypes
manim -ql --format=mp4 --flush_cache --disable_caching storyboard_scenes.py S01GenerationGate
```

Scene list:

- `S01GenerationGate`
- `S02ChatLogFallacy`
- `S03TraceabilityChain`
- `S04ArtifactGraph`
- `S05TraversalCompiler`
- `S06VQPPackage`
- `S07DualModeReview`
- `S08EvidenceCards`
- `S09ReadinessMap`
- `S10EvidenceSurface`

