# Visual Storyboard

Status: expanded storyboard revision for iteration 2 script.

Target: roughly 12 to 18 minute narrated video, 3Blue1Brown-inspired but with its own voice. The viewer should leave with one mental model:

```text
representation -> transform space -> computation -> representation
```

Reference-driven revision:

After reviewing the dense frame capture from
`assets/reference_frames/youtube_sources/short_transform_reference/contact_sheet.png`,
the most important change is to slow down the middle of the argument. The video
should not jump directly from "tokens become vectors" to "LLMs do useful work."
It needs a visible intermediate step:

```text
words are points -> relationships are directions -> directions can be computed on
```

See `storyline_reconsideration.md` for the current revised spine.

## Iteration 2 Visual Spine

The script is longer than the first estimate, so the video needs a real visual composition system rather than a few reusable animations.

The strongest recurring visual should be a **video-game-like technology tree**:

- dark 3D space;
- glowing research nodes;
- dependency lines between concepts;
- opacity states for unlocked, emerging, and speculative branches;
- camera zooms/reframes that let narration discuss different branches;
- a final zoom-out showing the tree extending beyond the first applications.

The tree should remind viewers of strategy games where a player chooses what to research next. The point is not literal game UI, but the felt idea that fundamental transforms unlock downstream technologies.

### Core Tech Tree Visual Rules

- **Unlocked:** bright, solid nodes with clear dependency lines.
- **Emerging:** bright but slightly translucent nodes.
- **Speculative/locked:** dim, ghosted nodes with faint rings.
- **Dependencies:** visible lines; downstream nodes should clearly require upstream conceptual unlocks.
- **Camera:** move through the tree rather than cutting to static diagrams.
- **Labels:** sparse, readable, and anchored to nodes.

### Expanded Section Needs

1. **Opening / classical transforms**
   - Use concrete, real-feeling signals, equations, and image/compression visuals.
   - Do not over-explain Fourier or Laplace; let the visuals justify significance.

2. **Classic transform pattern**
   - Reuse the signal-to-frequency pipeline.
   - Add a clear sense of "math happens here."

3. **Language/vector transform**
   - Tokens become points.
   - Points become clusters.
   - Outputs should be visually distinct: text, code, image, plan.

4. **Word vector analogy**
   - Keep the polished vector arithmetic scene.
   - Replace the hard-to-say semantic-search example with a simple visual example such as "big cat with a mane" -> "lion."

5. **Pseudocode to code**
   - Needs a real-looking code artifact, not a generic slide.
   - Show assumptions entering the output: framework, schema, active subscription, missing errors.

6. **Multimodal transforms**
   - Show encoder/shared-space/decoder as a transform bridge.
   - Examples should use real-feeling outputs when possible: generated-looking image tile, camera-to-robot-action, sketch-to-interface.

7. **Semantic transform loss**
   - Make this stronger by tying it to the code example.
   - Show "active subscription" branching into multiple possible implementations.
   - Visually distinguish preservation, invention, and loss.

8. **Technology tree**
   - Must be upgraded from a flat tree into the central 3D tech-tree visual.
   - Classical transform branches and learned-transform branches should coexist in the same space.

9. **Thinking in the limit**
   - Introduce it as a method:

```text
trend -> asymptote -> implication
```

   - Use three simultaneous trend graphs:
     - accuracy up;
     - complexity up;
     - generation cost down.

10. **Validation and verification**
    - Show artifact abundance colliding with an evidence gate.
    - Requirements, traces, tests, reviews, monitors, and proofs should be visible as the load-bearing infrastructure.

11. **Self-inhabiting compute**
    - Show the executing state of an agent/machine entering a learned transform.
    - The transform outputs executable behavior.
    - The hardware runs it.
    - Telemetry feeds back into the transform.
    - External validators surround the loop.

12. **Outer experiment loop**
    - Show question -> action -> evidence -> updated question.
    - Use lab/simulation/robot protocol visuals as concrete outputs.
    - This should feel like the same loop turned outward into the world.

13. **Businesses as transform pipelines**
    - Show intent -> strategy deck -> product brief -> design -> tickets -> code -> product.
    - Then show some handoffs compressing.
    - Make clear that humans add context and judgment, not just noise.

14. **Ending**
    - Return to the 3D tech tree.
    - Zoom out as new branches light up beyond the currently unlocked nodes.
    - End on the transform-space mental model, not on a generic AI automation claim.

## Scene 1: Civilization Gets a New Transform

Narration beat:

"Every so often, a new kind of transform changes what civilization can build."

Visual:

- Black background or clean grid.
- A messy time signal, a differential equation, and a blocky image appear as separate objects.
- Each passes through a glowing "transform" aperture.
- The transformed versions appear: frequency spikes, algebraic transfer-function diagram, DCT block coefficients.

Purpose:

Establish the pattern before mentioning AI.

## Scene 2: Transform Spaces Unlock Branches

Narration beat:

"Each of these transforms is more than a math trick. It is a doorway into a branch of the technology tree."

Visual:

- A tree trunk labeled "representation transforms."
- Branches grow quickly:
  - Fourier: radio, audio, MRI, image filtering, telecommunications.
  - Laplace / z-transform: controls, circuits, robotics, aircraft stability.
  - DCT / wavelets: JPEG, video compression, streaming media.
  - Linear algebra: PCA, search ranking, recommendations.

Animation note:

Keep this fast. The audience does not need a Fourier lecture; they need to feel the scale of downstream technology.

## Scene 3: The Pattern

Narration beat:

"This is one of the deep patterns of engineering: representation in, transform space, computation, representation out."

Visual:

```text
world representation -> transform space -> operation -> useful output
```

Examples slide through the same pipeline:

- signal -> frequency -> filter -> cleaned signal
- dynamics -> Laplace domain -> controller -> stable system
- pixels -> DCT -> discard coefficients -> compressed image

Purpose:

Give the viewer a reusable template.

## Scene 4: Language Enters the Pipeline

Narration beat:

"What makes modern AI strange is that language is now part of this pattern."

Visual:

- A sentence breaks into tokens.
- Tokens become vectors.
- Vectors become points in a high-dimensional space, shown as a projected 3D cloud.
- The cloud bends into a computation layer and returns as text, code, image, or plan.

On-screen text:

```text
language -> tokens -> vectors -> model computation -> representation out
```

Tone:

Bold, but include one spoken caveat: "not perfectly, not magically, but practically."

## Scene 5: Word Vectors as a Tiny Window

Narration beat:

"Before, words were mostly symbols on a page. Now they can also be locations, directions, neighborhoods, distances, and transformations."

Visual:

- 2D projected embedding space.
- Points labeled king, man, woman, queen.
- Animate a vector operation:

```text
king - man + woman ~= queen
```

Expanded animation sequence:

1. Start with a dark 3D vector space, then flatten to a readable 2D projection so the viewer can see the geometry.
2. Place `king`, `man`, `woman`, and `queen` as glowing labeled points. Keep labels fixed to camera and very readable.
3. Draw the relationship vector from `man` to `king`; label it lightly as a role/status direction, not as a literal semantic axis.
4. Copy that same arrow so it starts at `woman`. Its endpoint lands near `queen`.
5. Show the equation only after the motion makes the geometry obvious:

```text
king - man + woman ~= queen
```

6. Fade the equation back down and leave the viewer with the key intuition: relationships can become directions.

Purpose:

Use the familiar analogy as the smallest visible example of relationship-as-direction.

Caveat:

Show a small footnote-style label: "illustrative projection, not an exact guarantee."

Reference frames:

- `assets/reference_frames/youtube_sources/vector_embedding_reference/00-06-30.png` is a useful style reference for showing a word vector as a direction in a low-dimensional grid.
- `assets/reference_frames/youtube_sources/short_transform_reference/contact_sheet.png` is the best current reference for the exact embedding/vector-arithmetic visual language.
- `assets/reference_frames/youtube_sources/short_transform_reference/00-00-39.png`, `00-00-42.png`, `00-00-45.png`, and `00-00-57.png` are especially relevant for relationship vectors and analogy arithmetic.
- The source reference explains `bank` disambiguation rather than the king/queen analogy; the final animation should use the reference for grammar of motion and composition, then implement our own original king/queen vector arithmetic scene.

## Scene 6: Pseudocode to Code

Narration beat:

"The example most people are already touching is code."

Visual:

Left side:

```text
Build an API endpoint that checks whether a user has an active subscription and returns a usage limit.
```

Pipeline:

```text
intent -> model representation -> code-shaped search -> Python / TypeScript / tests
```

Right side:

- Code appears.
- Then hidden assumption tags appear around it:
  - framework?
  - schema?
  - error behavior?
  - what does active mean?

Purpose:

Make the central example feel concrete and slightly dangerous in the productive sense.

## Scene 7: Multimodal Alignment

Narration beat:

"Once you see the pattern, text-to-image stops feeling like a separate miracle."

Visual:

- Text prompt enters a text encoder.
- It lands in a shared or aligned vector space.
- An image generator decodes from that space into pixels.

Examples:

- text -> image
- image -> caption
- code -> explanation
- meeting transcript -> action items
- sketch -> interface

Purpose:

Show that the real claim is about representation compatibility, not chatbots.

## Scene 8: The Loss

Narration beat:

"Every powerful transform has assumptions."

Visual:

Three quick panels:

- JPEG: original image versus compressed image with exaggerated block artifacts.
- Laplace/control: clean transfer-function diagram with "model assumptions" and "initial conditions" tags off to the side.
- LLM code generation: vague prompt becomes plausible code, with missing constraints highlighted.

On-screen phrase:

```text
semantic transform loss
```

Supporting terms orbit around it:

- semantic compression
- semantic drift
- context degradation
- confabulation
- lossy compression
- information bottleneck

Purpose:

Name the tradeoff without making the whole video a failure taxonomy.

## Scene 9: The New Technology Tree

Narration beat:

"The full story is the technology tree that grows after people learn how to think in that space."

Visual:

Return to the technology tree. Add a new trunk/branch:

```text
learned representation transforms
```

Branches:

- coding assistants
- semantic search
- multimodal design
- AI tutors
- agent workflows
- requirements to tests
- automated research assistants
- simulation interfaces
- creative tools
- decision support

Purpose:

Make the ending expansive and civilizational.

## Scene 10: Closing Question

Narration beat:

"I do not think the right question is simply: what can AI automate? That question is too small."

Visual:

Pipeline freezes:

```text
human intent -> transform space -> generated artifact
```

Then questions appear one at a time:

- What survives the transformation?
- What gets compressed away?
- What assumptions get added?
- What new workflows become possible?

Final line on screen:

```text
When a civilization gets a new transform space, the technology tree changes.
```

## Article Companion Structure

The LinkedIn/article version can mirror the video:

1. A new transform changes the technology tree.
2. Fourier, Laplace, DCT as prior examples.
3. Learned vector spaces as the new transform space.
4. Pseudocode-to-code as the everyday workplace example.
5. Multimodal generation as representation compatibility.
6. Semantic transform loss and related research terms.
7. Why decision makers need this mental model.
