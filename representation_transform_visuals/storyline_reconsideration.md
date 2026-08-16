# Storyline Reconsideration From Reference Frames

Status: working direction after reviewing the dense frame capture from
`https://www.youtube.com/shorts/FJtFZwbvkI4`.

The Short is the strongest reference so far for the exact visual grammar we want:
words become vectors, relationship vectors become reusable directions, and
simple vector arithmetic becomes visible in a dark coordinate space.

Use it as motion/composition study only. Do not copy source frames directly into
final public assets unless rights are clear.

## Main Conclusion

Our current prototype jumps too quickly from "tokens become vectors" to "a big
LLM computation cloud." The reference makes the missing middle obvious:

```text
words are points
relationships are directions
directions can be moved, added, and subtracted
therefore language has become partially computable geometry
```

That should become the emotional and explanatory center of the first half of the
video. The viewer needs to see this before we talk about code, image generation,
or the larger technology tree.

## Story Spine Revision

### 1. Historical Transforms

Keep this, but make it faster and less text-heavy. Its job is only to establish
that transforms open technology branches.

Current risk: we are spending visual complexity on Fourier/Laplace before the
viewer knows why they should care.

Revision: one strong transform aperture, three fast examples, then move on.

### 2. The General Pattern

Keep the reusable pattern:

```text
representation -> transform space -> computation -> representation
```

Revision: make this more iconic and less like a four-column slide. Use objects
that move through the pipeline instead of lists of examples.

### 3. Language Enters

Split the current "language vectors" section into three separate beats:

1. A sentence becomes tokens.
2. Tokens become numerical vectors.
3. Vectors become points and directions in a visible space.

Reference frames:

- `assets/reference_frames/youtube_sources/short_transform_reference/00-00-18.png`
- `assets/reference_frames/youtube_sources/short_transform_reference/00-00-21.png`
- `assets/reference_frames/youtube_sources/short_transform_reference/00-00-24.png`
- `assets/reference_frames/youtube_sources/short_transform_reference/00-00-27.png`

### 4. Word Vectors As A Tiny Window

This should become its own hero section, not a minor example.

Proposed narration:

> Before, words were mostly symbols on a page. Now they can also be locations,
> directions, neighborhoods, distances, and transformations. The famous toy
> example is not magic, and it is not a guarantee. But it shows the shape of the
> new thing: relationships can become directions.

Visual sequence:

1. Show `king`, `man`, `woman`, and `queen` as labeled glowing points.
2. Draw the vector from `man` to `king`.
3. Copy that vector so it starts at `woman`.
4. Let the endpoint land near `queen`.
5. Only then reveal:

```text
king - man + woman ~= queen
```

Reference frames:

- `assets/reference_frames/youtube_sources/short_transform_reference/00-00-39.png`
- `assets/reference_frames/youtube_sources/short_transform_reference/00-00-42.png`
- `assets/reference_frames/youtube_sources/short_transform_reference/00-00-45.png`
- `assets/reference_frames/youtube_sources/short_transform_reference/00-00-48.png`
- `assets/reference_frames/youtube_sources/short_transform_reference/00-00-57.png`

Caveat on screen:

```text
illustrative projection, not an exact guarantee
```

### 5. From Word Arithmetic To Work

After the analogy lands, zoom back out:

```text
relationship-as-direction
  -> task-as-direction
  -> intent-to-code
  -> text-to-image
  -> transcript-to-plan
```

This is the conceptual bridge from the toy example to useful work. It should
replace the current abrupt jump from vector cloud to outputs.

### 6. Pseudocode To Code

Keep this as the main concrete example, but stage it using the same visual
language as the vector analogy.

Revision:

- Human intent is a point or short path in representation space.
- Missing constraints are not bullet lists; they are dim axes or invisible
  dimensions that light up when the model has to guess.
- Code appears as the decoded representation at the end of the transform.

### 7. Multimodal Alignment

Bring this back after code. The point is not "text-to-image is neat"; it is:

```text
compatible vector spaces let one representation decode into another form
```

This should be one clean shared-space visual, not a list of examples.

### 8. Loss

Keep semantic transform loss, but tie it directly to the vector-scene caveat:

```text
if the geometry is approximate, the decoded output inherits those approximations
```

Revision:

- The loss scene should show a copied relationship vector landing near the
  intended point, then missing slightly.
- Then connect that miss to code assumptions and hallucinated constraints.

### 9. Technology Tree

Keep the tech tree, but make the root explicitly depend on the new middle:

```text
representations become computable geometry
```

Branches should grow from that root, not from "chatbots."

### 10. Closing

The closing question should follow from the vector caveat:

```text
what survives the transformation, and what must be verified after decoding?
```

This makes the eventual bridge to verifiability compiler ideas much cleaner
without making this video about the compiler.

## Asset Implications

### New Primary Manim Assets

- `S04TokenToVectorColumns`: sentence -> tokens -> numerical vector columns.
- `S05WordAnalogyVectors`: king/man/woman/queen relationship arithmetic.
- `S06RelationshipToWork`: relationship vectors expand into task/work vectors.
- `S08SemanticLossGeometry`: approximate landing / semantic drift in vector space.

### Existing Assets To Rework

- `S03LanguageVectors`: should become less dense and should stop trying to show
  tokenization, vectors, model computation, and multimodal outputs all at once.
- `S05CodeAndLoss`: should inherit the visual grammar from the analogy scene
  rather than using text lists for assumptions.
- `S02PatternPipeline`: should use moving objects instead of stacked words.

### Human Review Assets

The next human review should include:

- the contact sheet from the Short
- the new token-to-vector scene
- the new king/queen vector arithmetic scene
- a one-paragraph explanation of why the toy analogy is illustrative but not
  a guarantee

## Immediate Next Build Target

Before expanding the whole video again, build a short 20-30 second Manim test:

```text
tokens -> vector columns -> 3D points -> man-to-king arrow copied to woman -> queen
```

This should become the benchmark for the rest of the visual language. If this
scene works, the rest of the video can orbit around it.
