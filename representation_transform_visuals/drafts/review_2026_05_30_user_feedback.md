# User clip-level feedback — 2026-05-30

Source: live review of `complete_prototype_review.mp4` with section/elapsed overlay.

Status legend: `[ ]` pending, `[~]` in progress, `[x]` done

## Section 01 — Opening

- [x] **01 — layout**: move `ẋ = Ax + Bu` so it sits across from its Laplace transform (right of the gate), not in the bottom-left corner. → equation now at `LEFT * 2.8 + UP * 2.2`, mirror of `H(s)` at `RIGHT * 2.8 + UP * 2.2`.
- [x] **01 — symbology**: the symbol above the transform barrier read as a Laplace `ℒ`, but the scene shows a Fourier-style transform. → gate label changed from `ℒ` to neutral `transform`.
- [x] **01 @ 00:00:18.95** — when the other transform elements get their highlight pulse, `H(s)` doesn't pulse. → added `pulse(transfer, CYAN, scale=1.10)` to the Fourier highlight beat.
- [x] **01 @ 00:00:20.583** — DCT icon just slides right slightly with no transformation demo. → replaced with a 7×7 image-patch → 2D DCT-style frequency surface → high-freq cells dimmed (`toss the bits the eye won't notice`).
- [x] **01 @ 00:00:28.750** — `streaming` text overlaps the frequency-transform geometry. → apps now sit in a horizontal row below the signal (not fanned around the tree root) so they never reach the bars.
- [x] **01 @ 00:00:40.333** — `learned representation transform` label sits on top of the diagram. → relabel centered at `(2.50, -3.80)` in the empty lower-center band; clipped-edge issue (`...trans`) also fixed.
- [ ] **01 @ 00:00:58.792** — narration is about what DCT enables. Cutaway scene with JPEG-style demo. → partially addressed via the new DCT beat (above); a dedicated cutaway is still a follow-up.
- [x] **01 @ 00:01:09.667** — narration lists radio, rockets, aircraft stability, streaming, etc. → 7-app horizontal row pops in matching narration density (radio · MRI · robotics · aircraft control · video streaming · JPEG/MPEG · audio codecs), dot to the LEFT of each label so dots don't overlap text.
- [ ] **01 @ 00:01:20.7** — `take a representation, move it into another space, do work, transform back out` — still needs a dedicated rep-in/rep-out graphic. Follow-up.

## Section 02 — The Classic Pattern

- [x] **02 @ 00:01:47.37** — signal symbol cut off at the left edge. → signal curve offset moved from `LEFT*5.0` to `LEFT*4.5` + narrower `t_vals` range; left edge now inside the frame safe area.
- [x] **02 @ 00:01:52.4** — `filter cutoff` placement vertical. → DashedLine flipped vertical at `x ≈ 1.5` (between bar 2 and bar 3); added `kept` / `discarded` labels on either side.
- [ ] **02 @ 00:02:25.7** — split `representation in → transform space → computation → back out` into its own scene. Follow-up (would require splitting the audio segment).

## Section 03 — The New Thing

- [x] **03 @ 00:03:00.250** — top-pop-in text disappears too quickly to read. → added `wait(1.6)` after sentence FadeIn, `wait(1.4)` after tokens FadeIn, `wait(1.2)` before they fade out.
- [ ] **03 @ 00:03:32.792** — dedicated scene for "sentence → tokens" beat. Follow-up.

## Section 04 — Word Vectors

- [x] **04 @ 00:05:04.250** — point labels (`tiger`, `cat`, `mane`, etc.) overlap the gold ring. → labels now placed OUTSIDE the ring at `radius=3.05` with a short colored tether from dot → label.

## Section 05 — Pseudocode To Code

- [x] **05 @ 00:05:44.208** — top-right matrix overlap. → matrix is `add_fixed_in_frame` (no 3D tilt) and scaled to 0.85 from 0.62.
- [x] **05 @ 00:05:58.6** — fork (`billing table` / `Stripe API` / `cached flag`) overlaps the intent column. → fork pushed right (`fork_origin = LEFT*3.30`, options at `LEFT*1.55–1.70`), chosen Stripe arrow now starts at `LEFT*0.40`. Connector lines shortened so they no longer pierce the assumption labels.
- [ ] **05 @ 00:07:16.00** — failure-modes-list scene. Follow-up.

## Section 06 — Multimodal Transforms

- [x] **06 @ 00:07:52.9** — decoder label moved ABOVE the triangle (was `next_to(tri, DOWN)`); output tiles repositioned into a tight 2×2 grid at `(2.10/3.80, -1.20/-2.20)` away from the text encoder/decoder area; redundant text-to-text / image-to-image mini rows collapsed into a single `trivial: text→text · image→image` hint. `reveal` caption is faded BEFORE the narration walk so they don't stack.

## Section 07 — The Loss

- [x] **07 @ 00:09:02.417** — discarded-detail cut now VERTICAL between bar 2 and bar 3; `← kept` and `discarded →` labels positioned ABOVE the `frequency-like components` text so the three don't stack.
- [ ] **07 @ 00:09:40.625** — outro animation transition. Follow-up.

## Section 08 — Why This Changes the Tech Tree

- [x] **08 @ 00:11:06.667** — subtitle vs tree collision. → column headers shifted from `y=2.95` to `y=2.55`; subtitle is faded OUT when the additive overlay tree starts so the two don't compete.
- [x] **08 @ 00:11:15.833** — rim hatch lines that read as glitches. → diagonal `lock_bar` replaced with a `DashedVMobject` outline (dashed border = clearly "speculative").
- [x] **08 @ 00:11:35.792** — connector lines piercing the right-column card text. → edge endpoint offset increased from `±LEFT/RIGHT * 0.78` to `±LEFT/RIGHT * 1.35` so connectors stop OUTSIDE the card boundary.
- [ ] **08 @ 00:12:08.5** — cutaway scene with workflow examples popping in. Follow-up.

## Section 10 — Validation & Verification

- [x] **10 @ 00:13:57.3** — bottom-text vs caption overlap. → `evidence becomes the work` is faded out before the narration walk starts; walk uses the slot it just vacated.
- [ ] **10 @ 00:14:40.167** — scene transition + arc geometry. Follow-up (would require redesigning the fountain beat).

## Section 11 — Self-Inhabiting Compute

- [x] **11 @ 00:15:39.25** — bottom captions overlap. → `telemetry_label` and gate labels (`tests`/`monitors`/`proofs`) are faded to low opacity before the narration walk so the bottom captions have a clear slot.

## Section 13 — Businesses Are Transform Pipelines

- [x] **13 @ 00:19:32.857** — symbols behind text. → `many` caption is faded out before the narration walk; walk-pos at `DOWN*3.30` (no longer overlaps zone labels at `y=-2.30`).
- [x] **13 @ 00:19:39.417** — arrow/box overlap. → handled by faded background flow + clear-slot walk.
- [x] **13 @ 00:20:14** — idea-dot color sync. → morph_path waypoints rebuilt so the dot color matches the boundary it JUST crossed: `CYAN→VIOLET→GOLD→GREEN→#FF8FB0`.

## Section 14 — Ending

- [x] **14 @ 00:21:25.7** — inherits tech-tree fixes. → same dashed-outline rim, same column-header shift, same connector-endpoint buffer.

## Outstanding (follow-up — not addressed this pass)

These are larger "new scene needed" items that require splitting the audio or adding new sections to the manifest. They're tracked here for the next iteration:

- 02 @ 00:02:25.7 — pipeline step split into own scene  *(remains open — addressed conceptually by S01 rep-in/transform/out below, but S02 itself still has a single-frame summary at the end)*
- 07 @ 00:09:40.625 — scene transition before the outro animation

## Round-3 user feedback (post-overlay-review, 2026-05-30)

User flagged that the previous round still had two issues + asked me to revisit deferred new-scene work:

- [x] **10 @ 00:14:45.208** — V-model arcs still don't read geometrically. → REPLACED the half-arc fountain with a literal trapezoidal **funnel**: wide cheap-generation pool at the bottom, narrowing through 4 stages (`generated artifacts → traces → tests → evidence → shipped`) with throughput-loss dots that fall away at each filter. V-model title + subtitle now fully fade so the new beat is a clean slate. [storyboard_sections.py:2474-2570](representation_transform_visuals/manim_prototypes/storyboard_sections.py#L2474-L2570)
- [x] **13 @ 00:19:49.0** — arrows overlap weird in the context of the diagram. → flowchart arrows now FADE OUT COMPLETELY when the compression beat starts (they pointed at the old box positions and looked broken once the boxes moved). The transform-boundary beat that follows also fully fades the original flowchart before drawing the boundaries. [storyboard_sections.py:2949 + 2992-3006](representation_transform_visuals/manim_prototypes/storyboard_sections.py)
- [x] **NEW SCENES BUILT — clear-screen-and-build-new pattern** the user asked for:
  - **S01 @ 1:20 — "the deep pattern"** rep-in / transform space / computation / rep-out: clears everything in the opening, builds a 4-stage left-to-right pipeline with named glyphs (wave → aperture → matrix → wave), arrows, and a glowing particle that travels the full pipeline color-shifting at each stage boundary. [storyboard_sections.py:445-516](representation_transform_visuals/manim_prototypes/storyboard_sections.py#L445-L516)
  - **S03 @ 3:32 — "a sentence becomes vectors"**: clears the 3D cluster, shows the literal sentence, breaks it into colored tokens, each token gets wrapped as a `Dot + Arrow + label` vector glyph, then all collapse into a relational-space cluster. [storyboard_sections.py:799-867](representation_transform_visuals/manim_prototypes/storyboard_sections.py#L799-L867)
  - **S05 @ 7:16 — "the transform can fail four different ways"**: clears the pseudocode beat entirely (including the `prompt` "intent / active subscription / usage limit" text that user feedback showed was bleeding), builds a 2×2 grid of named failure modes (HELPFUL / WRONG / INEVITABLE / INVISIBLE) each in its own colored panel with a tagline, plus a summary footer. [storyboard_sections.py:1273-1331](representation_transform_visuals/manim_prototypes/storyboard_sections.py#L1273-L1331)
  - **S08 @ 12:08 — "any workflow where humans pass around intent"**: clears the entire tech tree (grid + additive overlay), shows a 2×3 grid of glowing workflow icons (writing / programming / design / research / planning / review) with a coda. [storyboard_sections.py:2322-2380](representation_transform_visuals/manim_prototypes/storyboard_sections.py#L2322-L2380)

## Pattern observations (for autoreview workflow tuning)

Most of these are **layout / overlap** failures the Gemini review should catch. The reasons it was missing them:
1. We only sampled start/middle/end of each section → we miss specific timestamps where the problems actually appear (e.g. mid-animation states).
2. The prompt was general "look for issues" — it didn't force the model to enumerate text↔text, text↔line, text↔shape overlap pairs, or to check edge clipping.
3. The model can't see motion — it can't catch "label doesn't pulse with the others," "animation fades to nothing," or "dot color doesn't update across boundary." That requires sequential frame comparison.
4. The narration was given as a giant blob — it didn't know which line was playing at the sampled timestamp, so it couldn't flag "narration mentions X but the visual doesn't show X."

## Autoreview workflow upgrade — 2026-05-30

Implemented:
- **Dense frame sampling**: `extract_review_frames.py --dense N` now also samples one frame every N seconds within each section, in addition to manifest cues. De-dupes frames within 0.6s. `review_manifest_build.py --dense N` forwards the flag.
- **Per-frame narration excerpt**: context file now includes the narration line(s) at each frame's timestamp (estimated by linear time ratio within the section) instead of dumping the whole section's narration.
- **Per-frame elapsed timestamps**: each frame now has `Elapsed (overall) HH:MM:SS.ss` and `in-section: MM:SS.ss of total` so issues can be referenced the same way the human does.
- **Overlap-detection checklist**: prompt now requires the model to walk an A–I letter-coded checklist for every frame (text-text overlap, text-line strike, edge clip, arrow-on-letter, text-on-symbol, boxed-text-in-3D, stacked captions, mismatched glyph, dim text on black) plus a J–L narrative checklist (narration↔visual match, dead-end animation, missed metaphor).

Smoke test at `--dense 15` on the current prototype produced 127 frames and caught essentially every issue the human reviewer flagged (Frame 1 J: Fourier-with-Laplace-symbol, Frame 2 A: streaming overlap, Frame 36 B: Stripe arrow overlap, Frame 47 A: text decoder overlap, etc.). Saved to `manifest_pipeline/out/visual_review_dense_smoke.md` for reference.

Still missing — known limitations:
- Motion across frames (e.g. "this label fades out and back in around 00:06:00", "the idea-dot color doesn't update at boundary crossings"). Would require feeding short clip GIFs or paired-frame comparisons.
- Highlight-pulse-omission ("the other elements pulse but H(s) doesn't"). Same root cause — single frames can't show that something is or isn't moving.
