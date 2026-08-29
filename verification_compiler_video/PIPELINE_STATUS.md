# Video 2 — status at 2026-08-25 (review pass 4)

## What changed this pass

### Four reviewer-reported defects, fixed at the source

1. **Thick text highlights.** `style.highlight` and `.animate.set_stroke` on a
   group reached the glyphs and closed up the letterforms. `highlight` now skips
   text; `style.restroke()` does the same job on arbitrary groups; a new
   `text_stroked` check catches any recurrence.
2. **Shapes over text.** New `stroke_over_text` — an outline or rule drawn across
   text, which the filled-shape check deliberately ignores.
3. **Captions too close.** New `text_crowding` (under 0.16 apart), plus
   `stage.clear_of()`, which nudges a standalone label clear of text already on
   stage at construction time. Beats are written independently and cannot see
   each other's placements, which is how two labels land 0.12 apart with nobody
   having written a bad number.
4. **Connectors on top, blinking back.** The real fix is a z-index ladder in
   `style.py`. Manim flattens the scene and stable-sorts by `z_index`, so that is
   the only way to state a layering rule that survives group boundaries —
   sibling reordering cannot put an edge inside a `chain` VGroup behind a node
   that lives in a different top-level group.

### The review slate

`VC_REVIEW_SLATE=1` burns `SS bNN  T.Ts` into the top-left in amber, outside the
composition and excluded from every check. The same codes key the Gemini report
and the dashboard.

### Checker bugs found and fixed

- **`_visible()` measured size in scene coordinates.** A 3D scene stands its
  nodes upright by rotating them into the XZ plane, so their y-extent is exactly
  zero and every one was excluded from every check. Both 3D sections had been
  passing the gate on one recorded mobject each. Fixing it surfaced 25 real
  defects in section 6. The same bug also hid every horizontal rule in flat
  scenes, and made `Text.font_size` — which Manim derives from height — report
  0.0pt for every upright label.
- **`dead_air` needed three samples to fire.** It dated a run from the second
  matching sample and only reported on the third, so a static hold — which Manim
  freezes into exactly two samples — was invisible, and the last hold of any
  scene was never reported. Six real dead-air stretches were hiding behind it.
- **The geometry recorder logged scene-traversal order, not draw order.** Every
  layer check was judging a picture the viewer never sees.
- **`resolve_anchor` had no tie-break.** "The question is" matched both line 9
  and line 10 at 100%, the earlier won on stable-sort order, and line 10 silently
  lost its beat. Now tie-broken by how much of the *line* the anchor accounts for.
- **The placer aimed exactly at the crowding threshold** and floating point put
  three labels a hair under it. It now aims past the bar.
- **`_visible` was quadratic** once it used `get_all_points()` on every family
  member — it took a 34-second 3D render past fifteen minutes.

### Two new checks — 18 total, each proven by a planted defect

- `stage_imbalance` — the area-weighted centre of the composition against the
  middle of the stage. Promoted into the gate because Gemini made the same
  observation about ten consecutive beats of section 2, which is mechanical
  enough that it should not have needed a model.
- Waivers: `ctx.waive(check, reason)` and `ctx.lopsided(reason)`. A flood piling
  against a wall it cannot cross is lopsided on purpose; declaring it keeps the
  check strict everywhere else instead of loosening a threshold until it stops
  finding anything.

### The Gemini review layer

`pipeline/gemini_review.py` sends one settled frame per beat with the narration
line it is cued to, and the grammar as the rubric, told what the gate already
covers. 234 beats, 228 judgements. `build_dashboard.py` groups them by theme.

## Review pass 5 — the reviewer's nineteen

Nineteen specific defects, cited by slate code. The instruction was to make the
checks find them first, then fix them — so that the class stays fixed rather than
the instance.

**Five new checks, each proven by a planted defect (23 total):**

| check | what it catches | reviewer notes it covers |
|---|---|---|
| `outline_over_text` | a shape's own boundary running through letters, whatever the z-order | 03 b22, 03 b23, 05 b09, 05 b18, 07 b03, 07 b10, 08 b12 |
| `text_too_brief` | text up for less than its reading time, computed from length | 04 b14, 05 b22, 06 b15 |
| `partial_dim` | a connector left bright while the shapes it joins recede | 03 b19, 05 b22 |
| `layer_transient` | a connector drawn in front and then dropped behind — a blink | 04 b16, 06 b07 |
| `words_merged` | a word gap too small to separate the words at review size | 10 b06 |

**Four bugs in the recorder and the scene machinery:**

1. **The recorder could not see nested shapes.** It required a shape to *be* a
   top-level scene mobject, so anything inside a plain VGroup — which is every
   `chip()`, `dot()`, bar and tile in the video — was invisible. Thirty-four
   falling chips appeared, moved and vanished while the recorder logged two
   boxes. That is why the flood blinking out (01 b09) went unreported.
2. **Removing a duplicate wrapper removed its children.** Manim's `add` absorbs
   the children when an ad-hoc `VGroup(...)` wrapper arrives, so dropping the
   wrapper dropped them too, and they stayed gone until a later beat happened to
   re-add them. That is 01 b09 and 01 b27, one cause. The fix puts the children
   back at the index the wrapper occupied, which preserves layering as well as
   presence.
3. **Three checks measured first-hit to last-hit rather than contiguous runs.**
   One frame during a fade and one during the fade back are seven seconds apart
   and describe nothing; read as one run they invent a seven-second defect.
4. **Pango's space advance rounds down below 17pt.** Every multi-word label set
   at `tiny` (16pt) rendered with a ~3.5px word gap at review size and read as
   one word. At 17pt the same phrases come out at 6px. `TYPE["tiny"]` is now 17.

**Three systemic fixes rather than instance fixes:**

- `ctx.show()` now nudges a standalone label clear of *shapes*, not only of other
  text — a label whose box straddles a card's edge gets that edge drawn through
  its letters. A label wholly inside a shape is exempt: that is a composition.
- `ctx.recede(*tags)` dims content *and* its connectors, and takes strokes lower
  than fills — a filled node at 35% washes out, a one-pixel saturated line at 35%
  still reads as a bright line drawn across the picture.
- `stage.free_points()` scatters into the space that is actually free, so a
  "flood of artifacts" beat stops landing tiles on the diagram.

**Content fix:** section 4 asked "is there code with no requirement?" over a
graph in which every code unit had one. There are now a genuinely orphaned code
unit and a genuinely unimplemented requirement for those questions to point at.

**Added:** section 11, the end card (43.5s).

## Review pass 6 — depth, and ten more defects

**The 3D scenes were not 3D.** Every node in sections 4 and 6 sat at `y = 0`, so
both were flat planes seen at an angle and the camera moves had nothing to
reveal. Nodes now carry real depth: section 6's project cloud is three layers
deep, its packages are staggered in distance, and section 4's artifact families
sit at different y within their planes. The perspective does the work the camera
moves were already asking it to do.

**3D connectors were never on the connector layer.** `Line3D` reports
`shade_in_3d = False`, so ThreeDCamera's depth sort gives it the same key as
everything else and falls back to scene order — a 3D connector drawn during a
beat sits in front of the nodes it joins and drops behind the moment anything
else arrives. The 2D connectors have carried the edge layer for three passes;
the 3D ones now do too. That is the blink at 04 b16 and 06 b07.

**New check — `arrow_to_nowhere`** (24 total). An arrow whose target moves away
is left aiming at the space where it used to be (08 b09). It only fires on an
arrow that *was* pointing at something: an arrow that never had a target is a
deliberate marker, like a chevron aimed at the bottom of the frame to mean "in
the description".

**Two checks made depth-aware.** `edge_through_node` joined `node_overlap` in
ignoring pairs at clearly different depths — in a 3D scene a line crossing a node
from another distance is perspective, not a line drawn through something.
`partial_dim` now requires *both* ends of a bright connector to land on dimmed
shapes and neither on a lit one; a bright edge from a lit node into receded
context is how this video shows a slice against its background.

**Content fixes:** the orphan requirement in section 4 collided with the
interface control document, so the ring meant to say "nothing implements this"
landed on the document; flags now clear one another so exactly one question is
lit at a time. Section 5 retires the traversal row instead of shifting it onto
the reviewers. Section 7's findings list no longer grows through the row of
packages.

**The end card is rebuilt** around the new narration: the whitepaper and its
references in the description, the invitation for an agentic developer to have
their agent build its own compiler, the three questions to answer in the
comments, and one idea branching into several.

## Cold open, reworked 2026-08-28 — SCRIPT LOCKED FOR RECORDING

The reviewer is recording the human take against `drafts/script.md` as it now
stands. **Do not change narration text without asking.** The previous version is
`drafts/script_v3_before_coldopen.md`.

The problem it solves: the old open spent its first ten seconds on an abstract
cheap/trust inversion, the stakes (aircraft, brakes, a child in the road) arrived
at 82s, and the words "Verification Compiler" at 127s. The new open puts a direct
question at 5.6s, the "AI is not allowed to write this" claim at 8.6s, the stakes
at 14s and the thesis at 31s.

Trimmed with it: three lines around b21-b23 that the new open made near-verbatim
repeats ("not because the models write bad code", "nobody can check the flood
fast enough"), and the open's own stakes line shortened to "Aircraft. Medical
devices." so the child-in-the-road sentence stays the only place that image
lands. Section 1: 151.6s -> ~143s estimated.

### Owed on section 1's animation — not started, by request

Beats whose anchor line no longer exists, so they need rewriting when section 1
is reanimated: `b01_review_above`, `b02_strain`, `b03_multiply`,
`b04_artifact_web`, `b05_stop`, `b06_lone_reviewer`, and the three in the trimmed
b21-b23 stretch.

The visual arc has to invert. The old one *built* to the flood over 36 seconds;
the new open has to *start* in it:

| line | visual |
|---|---|
| four thousand lines | the flood arrives immediately — the old beat 9's rain, moved to beat 1 |
| code, tests, docs, a migration plan | artifact families land as each is named |
| how much did you read | one reviewer, dwarfed |
| not allowed to write | **the plane pictogram — see below** |
| aircraft, medical devices | the stakes, held |
| nobody can check fast enough | the wall and the flood that cannot cross it |

**The reviewer asked for an aggressive open with a plane pictogram**: a small
plane flying level, code streaming through it, the code going bad, the plane
losing altitude and going in. Hard and fast, over before it becomes tasteless —
it is the reason the rest of the video exists, not a joke. Drawn in the shape
grammar: silhouette plane, the same cyan squares the flood uses for the code, RED
for the failure. The direction is also recorded as a [VISUAL:] note against the
opening in `drafts/script.md`.

## Where it stands

11 sections, 100% line coverage everywhere, drift within 0.07s, 14.7 minutes
including the end card. 23 machine findings outstanding across the whole cut,
all of them short transients (mostly 0.5-2s outlines crossing a label during an
animation) — down from the 200 the same checks found before this pass.

`stage_imbalance` is reported but not treated as blocking: the reviewer said
explicitly that composition balance is not a priority for this iteration.

See `out/review/dashboard.html` for the gate, the ranked model findings, and the
frame behind each one.

## Next

1. The composition pass: `stage_imbalance` and Gemini's "dead space" theme are
   the same finding from two directions. Several beats put everything in the
   upper two-thirds and leave the bottom empty.
2. Shape-grammar consistency — 38 findings. Standards drawn as plain rectangles
   where the grammar says document slice; generic bullets where a typed shape
   belongs.
3. Stale frames — 14 beats where the line changed and the picture did not. Worth
   a `beat_no_change` check: compare each beat's settled frame to the previous.
4. The delivery render at 1080p30, and the human narration take replacing the
   scratch TTS (the timing table rebuilds from the real audio with no scene edits).
