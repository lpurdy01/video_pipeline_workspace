# Transform Tech Tree Design Brief

## Project Context

This is for the public-facing Representation Transform Visuals project: a narrated, 3Blue1Brown-style video and companion article for smart generalists, engineers, and YouTube viewers. The core mental model is:

`representation -> vector/transform space -> computation -> representation`

The tech tree should make that idea feel civilizationally important without claiming a precise historical dependency graph. It is a visual metaphor for families of representation-transform capabilities that unlock new kinds of computation.

## Preferred Visual Metaphor

The current direction is a skill-tree / tech-tree map:

- A small neutral center origin connects to the first real category nodes.
- The center is not itself a technology, claim, or breakthrough.
- Each category becomes a wedge, resized to fit its contents.
- Capabilities spin outward from the center.
- Cross-category convergence edges should feel special, not like ordinary parent-child edges.
- The frontier is not a wedge. It is an outer fog-of-war region, shell, or halo where not-yet-clear research directions live.

This could become a 2D radial Manim scene, a 2.5D rotating map, or a true 3D tree/shell where outer frontier nodes float beyond the researched layer.

## Current Category Wedges

### Classical Signal And Media Transforms

Purpose: show the familiar pattern where a transform makes hidden structure computable.

Nodes:

- Fourier transform.
- Frequency-domain view.
- Signal processing.
- Wireless communication.
- Compressed audio such as MP3 and AAC.
- Spectral imaging / MRI.
- Discrete cosine transform.
- Block frequency bases.
- JPEG image compression.
- Video codecs such as MPEG, H.26x, and AV1.

Design note: Fourier and DCT should be visibly related but not collapsed. DCT can look like a practical compression side branch from the same broader signal/media family.

### Dynamics, Stability, And Control

Purpose: show transforms and state representations making dynamic behavior analyzable and controllable.

Nodes:

- Laplace transform.
- Transfer functions.
- Stability and control.
- Feedback controllers.
- Brushless motor control.
- Flight / robotics stability.
- State-space models.
- Neural SSMs: S4 / Mamba.

Design note: Laplace should lead to a vivid practical payoff. Brushless motor control is concrete; flight/robotics stability may be more visually legible. Neural SSMs should be a highlighted bridge between the control wedge and learned sequence-model wedge.

### Learned Representation Spaces

Purpose: show the modern learned-transform family: data becomes a manipulable latent or embedding space, then gets transformed back into text, images, audio, tools, or actions.

Nodes:

- Neural networks.
- Embeddings.
- Transformer sequence models.
- Large language models.
- Contrastive multimodal spaces.
- Autoencoders / GANs.
- Neural codecs such as EnCodec.
- Discrete audio tokens.
- Speech / audio agents.
- Multimodal tools.

Design note: This wedge should feel like the modern expansion of the tree. It can visually “reach across” to other wedges.

### Language, Code, And Verification

Purpose: keep the central practical example: English-to-code and agentic tool use, while showing why reliability/evidence becomes part of the story.

Nodes:

- Software as formal representation.
- Classical expert systems.
- Blackboard architectures.
- SMT / Dafny / proof tools.
- Autonomous code agents.
- Research assistants.
- V&V / evidence systems.
- Reliable agent workflows.

Design note: This wedge should not look like the verifiability compiler project taking over the video. It is one branch of the broader representation-transform story.

### Outer Frontier Layer

Purpose: hint at speculative or unrevealed territory without making it look like a normal category.

Nodes:

- Transform-native organizations.
- Self-inhabiting compute.
- Autonomous experiment loops.
- Discrete-event world models.
- Closed-loop R&D.

Design note: This layer should be visually separated: fog, shell, faint outer ring, dashed outlines, or elevated 3D surface. It should communicate "we cannot fully see this yet."

## Style Direction

- Dark, high-contrast, Manim-friendly visual language.
- Crisp geometric labels and glowing edges, but not fantasy ornamentation.
- Think mathematical atlas, not game UI chrome.
- Color-code wedges with distinct hues.
- Use clear topology and depth cues over dense text.
- Preserve enough whitespace that labels could later be selectively animated.
- Avoid implying exact mathematical equivalence between classical transforms and LLM representations.
- Keep the phrase "frontier" visual and spatial, not categorical.

## Manim Implications

Useful outputs from concept art:

- How to allocate wedge angles based on branch size.
- How to draw cross-category bridges, especially neural SSMs.
- Whether the frontier works better as a flat fog ring, a higher 3D shell, or a distant rectangular region.
- How much text can survive on screen before the diagram needs staged reveals.
- Whether 3D helps orientation or just creates clutter.
