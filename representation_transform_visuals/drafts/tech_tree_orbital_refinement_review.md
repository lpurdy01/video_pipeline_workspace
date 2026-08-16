# Orbital Tech Tree Refinement Review

Generated refinement frames:

- `representation_transform_visuals/agent_tools/out/tech_tree_orbital_refinements/01_opening_fog_glimpse.jpg`
- `representation_transform_visuals/agent_tools/out/tech_tree_orbital_refinements/02_classical_foundation_region.jpg`
- `representation_transform_visuals/agent_tools/out/tech_tree_orbital_refinements/03_modern_region_without_full_reveal.jpg`
- `representation_transform_visuals/agent_tools/out/tech_tree_orbital_refinements/04_convergence_bridge_partial_pullback.jpg`
- `representation_transform_visuals/agent_tools/out/tech_tree_orbital_refinements/05_final_full_reveal.jpg`
- `representation_transform_visuals/agent_tools/out/tech_tree_orbital_implementation/01_manim_progressive_reveal_blueprint.jpg`
- `representation_transform_visuals/agent_tools/out/tech_tree_orbital_implementation/02_fog_and_mask_layout_study.jpg`

## Big Takeaway

The image generator is useful for broad spatial composition, but it must be constrained hard around reveal timing. It tends to show too much too early and keeps labeling the center. For Manim, the design should be driven by a canonical hidden full map plus explicit reveal masks/camera states.

## Fog Feasibility

We can do fog in Manim, but it should be fake fog:

- Camera-locked haze overlays.
- Radial vignette/dark masks.
- Dotted orbit rings to imply the outer shell.
- Low-opacity drift particles near frame edges.
- Partial annular sectors to hide unrevealed wedges.

Avoid relying on a true transparent 3D shell for the main effect. It may be useful as a final-reveal accent, but it is risky for depth sorting and text readability.

## Best Output From This Round

The most useful structural image is `04_convergence_bridge_partial_pullback.jpg`.

Why:

- It shows only a partial pullback, not the full tree.
- Bridges become the hero.
- Fog hides the left/classical side while keeping the learned/control/software relationships legible.
- It fits sections 8-10 better than the prettier full-shell images.

The most useful implementation image is `02_fog_and_mask_layout_study.jpg`.

Why:

- It suggests using dark side masks and a camera vignette rather than a physical fog sphere.
- It shows a readable center-region view where only convergence labels appear.
- It implies a practical Manim layer order: disk, bridges, labels, masks, haze.

## Reveal Strategy

Use one canonical orbital map, but never show it all until the end.

Reveal states:

1. **Opening glimpse:** mostly fog and partial arcs; no center label; maybe Fourier/Laplace/DCT fragments.
2. **Classical foundation:** crop to signal/media and dynamics/control; keep lower/modern regions masked.
3. **Modern region:** crop to learned and software regions; classical branches become offscreen memory, not visible map.
4. **Convergence pullback:** show three regions at once, but hide one side and frontier labels with fog/masks.
5. **Final reveal:** show the full disk and shell for the first time.

## Layout Decisions For Manim

- Use a blank center point or small unlabelled ring. Never label the center.
- Put signal/media and dynamics/control in the upper half for early readability.
- Put learned representation spaces and language/code/verification in the lower/right regions for the mid-video transition.
- Keep neural SSMs near the boundary between dynamics/control and learned representation spaces.
- Keep LLMs near the learned/software boundary so the LLM-to-code bridge is short and narratively obvious.
- Draw convergence bridges as raised Bezier curves with glow, but keep ordinary branch edges flat.
- Treat the frontier shell as a late-stage overlay outside the disk, not as a fifth category wedge.

## Layer Order For Prototype

1. Background grid/space.
2. Flat wedge sectors and radial rings.
3. Ordinary branch edges.
4. Nodes.
5. Raised bridge curves.
6. Active labels.
7. Dark masks/crop overlays.
8. Fog/haze/vignette overlays.
9. Optional final-reveal frontier shell.

## Prompt Lessons

Useful prompt constraints:

- "The full tree must not be readable until the ending."
- "The center has no label."
- "Show crop boundaries, 2D fog overlays, dark masks, and partial arcs."
- "Prioritize layout and reveal mechanics over beauty."

Constraints that need to be repeated every time:

- No center label.
- No full disk in early/middle views.
- Sparse labels only where the camera has settled.

## Next Prototype Recommendation

Build the Manim test as a reveal-state machine, not as separate one-off scenes:

- `state_opening_glimpse`
- `state_classical_foundation`
- `state_modern_region`
- `state_convergence_pullback`
- `state_final_reveal`

Each state controls:

- active wedges;
- visible nodes;
- visible labels;
- camera frame;
- mask positions;
- fog opacity;
- bridge height/opacity.

This will make the map reusable throughout the video without showing too much too early.
