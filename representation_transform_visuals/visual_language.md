# Visual Language

## Direction

The video should feel closer to a dark mathematical animation than a slide deck.

The narration should carry most of the words. The screen should carry motion, geometry, structure, and the feeling of a new computational space opening up.

## Principles

- Use a nearly black background.
- Prefer glowing geometry over panels.
- Avoid large blocks of explanatory text.
- Use labels sparingly, mostly as anchors: `signal`, `frequency`, `tokens`, `vectors`, `code`.
- Show transforms as motion through a space, not as boxes in a flowchart.
- Make vector spaces feel alive: rotating axes, points moving into clusters, arrows becoming directions, matrices acting on grids.
- Use text only when the exact phrase matters.

## Palette

```text
background: #00020A
near black: #050812
grid line:  #172033
white:      #F4F7FF
muted:      #8791A8
cyan:       #20F7D2
electric blue: #4D8DFF
violet:     #B45CFF
gold:       #FFCB4D
red:        #FF4D6D
green:      #49F28D
```

Use cyan, blue, violet, and gold as the core identity. Red should appear mainly for loss, assumptions, or distortion.

## Motion Motifs

- **Transform aperture:** objects pass through a thin luminous plane and emerge as another representation.
- **Matrix action:** a grid or vector cloud is multiplied by an animated matrix, rotating, shearing, or clustering.
- **Embedding field:** tokens become points in a 3D cloud, then relationships become arrows.
- **Technology tree:** not a flat org chart. It should feel like bright branches growing out of a dark root system.
- **Semantic loss:** parts of a representation fade, blur, or collapse into assumption markers.

## Manim First

Use Manim for:

- vector spaces
- axes
- moving dots
- arrows
- matrices
- coordinate transforms
- graph/tree growth
- glowing geometry

Use Python/Pillow only for:

- quick storyboard placeholders
- generated texture plates
- static image composites that need to match the Manim palette

## Text Rule

If narration already says it, do not put the sentence on screen.

Good:

```text
tokens -> vectors
```

Too much:

```text
Modern AI makes language part of this pattern. Tokens become vectors...
```

The video should be watchable on mute only in broad shape, but it does not need to be fully understandable without narration.

