# Orbital Tech Tree Implementation Prompts

These prompts are a second refinement pass after reviewing the first orbital refinement outputs. The goal is not prettier concept art. The goal is to extract layout decisions that can be translated into Manim.

## Shared Context

Use the provided reference image as a structural seed, but fix these issues:

- Do not label the center. The center is a blank visual origin only.
- Do not show the full tree before the ending.
- Do not use a true opaque 3D fog ball as the main solution.
- Use crop boundaries, 2D fog overlays, dark masks, and partial arcs to hide unrevealed regions.
- Keep the researched disk mostly flat, with only bridges rising above it.
- Show labels only where a camera has settled.

The intended Manim implementation has:

- A flat radial disk of category wedges.
- Screen-facing labels.
- Raised Bezier bridges for convergence edges.
- Camera-locked fog/vignette overlays.
- Separate reveal states for opening, classical region, modern region, convergence pullback, and final reveal.

## Prompt 1: Manim Progressive Reveal Blueprint

Create a blueprint-style concept image for a Manim implementation of the orbital tech tree progressive reveal. Show the same tree as a flat 2.5D disk, but include translucent rectangular/curved crop windows or mask zones that indicate what is visible at each video phase. The image should show five labeled camera/framing states as small overlay annotations or mini-viewports: opening glimpse, classical foundation, modern region, convergence pullback, final reveal. The center has no label. Prioritize layout and reveal mechanics over beauty.

## Prompt 2: Fog And Mask Layout Study

Create a layout study for fake fog in Manim around the orbital tech tree. Show how camera-locked haze, radial vignette, dotted outer orbit lines, and dark masks can hide unrevealed wedges while leaving visible labels readable. The image should make clear where fog layers sit relative to the flat disk and raised bridges. Do not show the full readable tree; show a partial convergence-pullback view with hidden classical/frontier regions. The center has no label. Make it practical enough to translate into Manim layers.
