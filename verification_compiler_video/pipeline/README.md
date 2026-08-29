# Video 2 pipeline

Built to answer one complaint about video 1: *"I had to make a lot of passes for
simple stuff."* The filesystem records roughly thirty review/patch cycles, and
ten rounds on a single graphic. Almost every one was a human finding something a
machine could have found.

The design principle here is **push each class of defect to the earliest stage
that can catch it**, and make the later stages structurally unable to see it.

```
     script line
         │
         ▼
   scratch TTS ──► local STT ──► fuzzy align ──► timing table
         │                                            │
         │                                            ▼
         │                                     beats resolve anchors
         │                                            │
         ▼                                            ▼
   beat proposals (Gemini) ──────────────────►  scene renders
                                                      │
                                     per-frame geometry recorded
                                                      │
                                                      ▼
                                        automated gate: overlap, clipping,
                                        legibility, arrowheads, flicker,
                                        dead air, drift, line coverage
                                                      │
                                            (fails → nobody looks yet)
                                                      │
                                                      ▼
                                          beat review page ──► human
```

## Four layers, four kinds of failure

| Layer | Catches | When |
|---|---|---|
| `style.node()` | a label that cannot fit its shape | constructing |
| `stage.fit()` | content scaled below legibility, lane intrusion | laying out |
| `qa` recorder | overlap, clipping, arrowheads, flicker, dead air | rendering |
| `build.gate()` | timing drift, missing beats, unresolved anchors | before review |

The layers overlap on purpose. `style.node()` cannot know that a later `fit()`
will shrink its label to 11pt; `fit()` cannot know that an animation will move
two labels across each other three seconds later. Each layer catches what the one
above it structurally cannot see. Both of those were real defects caught during
the first end-to-end run of this pipeline.

## Timing: the audio is the clock

Video 1's scenes waited for narration phrases by exact string match, and could
only ever *insert* time. Once a scene fell behind it stayed behind, drift
compounded, and the overrun was then silently cut by ffmpeg's `-t` — one section
shipped with 1.6 seconds of its ending missing and nothing said so.

Here:

- The timing table comes from aligning the script against **spoken word
  timestamps**, using a diff over word sequences. Rewording a line does not break
  its cue, because matching is fuzzy and gaps are interpolated.
- A beat declares *what* changes and on *which line*. It never declares when.
- `ctx.budget()` **compresses** a beat's animations to fit its window. Beats can
  catch up, not just fall behind.
- Rendered duration is measured against narration duration and drift beyond
  0.25s **fails the build**. Silent truncation is no longer possible.
- Swapping scratch TTS for the human take re-runs the same alignment. Every cue
  re-times itself; no scene is edited.

Measured on section 02: **-0.06s drift across 63.7 seconds.**

## Beats: the unit of visual change

The brief is that almost every line of narration should change the picture. That
is only tractable if "a change" is an object:

```python
Beat("a chat transcript is not evidence", self.b_stamp,
     note="stamp lands across the model's answer")
```

The scene is a list of these. Coverage — the fraction of narration lines with a
beat cued to them — is reported by the gate, so storyboard thinness is a number
rather than an impression. Section 02 currently runs 95.2%.

`propose_beats.py` closes the loop: it sends the narration, timing, and existing
beats to Gemini and asks for concrete proposals for the uncovered lines, plus the
three lines that most deserve an ambitious visual. It proposes; the gate
measures; a human decides.

## Ownership, and why transitions are declared

Two Manim traps cost video 1 repeated passes:

- `FadeOut` on an already-removed mobject **re-adds it at full opacity** and
  flashes it into frame;
- `FadeIn` fades to a mobject's *current* opacity, so anything pre-hidden at
  opacity 0 fades 0 → 0 and never appears.

Both are consequences of the scene not knowing what is on stage. So the stage
tracks it. A beat introduces content under a tag and retires it by tag;
`ctx.retire()` ignores what is already gone, which makes the first bug
unwritable. `camera3d.pin()` tracks fixed-frame mobjects for the same reason —
they leaked into later scenes in video 1.

Transitions are functions on the stage rather than hand-rolled fade sequences,
because the grammar should be consistent and changeable in one place:

- `cut` — everything leaves. Use between unrelated ideas.
- `settle` — everything leaves *except* what carries the argument forward. Use
  when the next section builds on this picture. Video 1 had no transitions at
  all: every section boundary was a dip to black, and the review tooling had a
  special case to skip past the fade-in.
- `pull_back` — a 3D camera move that reveals the thing just examined is part of
  something larger. This is the section-to-section move the artifact graph wants.

## Scene structure

```
pipeline/
  style.py       palette, type scale, shape grammar, node/arrow constructors
  stage.py       frame lanes (title / stage / caption), fit(), columns(), rows()
  timing.py      TTS -> STT -> fuzzy alignment -> timing table; anchor resolution
  beats.py       Beat, BeatContext, BeatScene, transitions
  camera3d.py    Beat3DScene, declarative camera moves, layered graph builder
  qa.py          per-frame geometry recorder + every check
  build.py       render, measure, gate one section
  gate_all.py    gate all ten, one table, render timestamps on every row
  propose_beats.py   Gemini storyboard densifier
  gemini_review.py   one settled frame per beat -> Gemini, for what geometry cannot judge
  review_notes.py    joins the gate's violations to Gemini's judgements, by theme
  build_review_page.py   beat-by-beat review artifact
  selftest_qa.py     plants one defect per check and asserts each fires
  selftest_3d.py     proves recorded geometry follows the camera
scenes/
  s02_chat_log_fallacy.py    reference implementation, 21 beats
```

A scene is a `storyboard()` returning beats plus one small method per beat.
Video 1's scene file was 3,999 lines with ~1,100 lines of dead code and
`construct()` methods up to 557 lines long; nothing in it could be tested or
reused.

## The self-test matters

`selftest_qa.py` renders a scene built from deliberate defects — overlapping
text, 7pt type, an element off the edge, an arrowhead in a word, a flicker, seven
seconds of dead air — and asserts that every check fires. A checker nobody has
watched fail is not a checker.

It has since caught the worst bug the pipeline has had, which was in the checker
rather than in a scene. `_visible()` decided whether to record a mobject by
measuring its width and height in *scene* coordinates — and a 3D scene stands its
nodes upright by rotating them into the XZ plane, which makes their y-extent
exactly zero. Both 3D sections were therefore recording one mobject apiece and
passing the gate on it. Fixing the test surfaced twenty-five real defects in
section 6 that had been invisible for the whole build. The same measurement bug
had a second head: `Text.font_size` in Manim is derived from the mobject's
height, so every upright label reported 0.0pt.

This caught three real bugs in the checks themselves during development: a
legibility test that measured glyph bounding boxes (so "an answer", having no
ascenders, read as too small while being perfectly legible); a flicker detector
that sorted presence and absence events separately and collapsed real gaps to
zero; and — most importantly — the discovery that Manim optimises a static
`wait()` into a single frozen frame, so **no frames inside a hold were being
sampled at all**. A scene that arranged a broken layout and simply held it would
have passed silently. That is precisely the frame a human ends up catching.

## The checks

Thirteen, each proven by a planted defect in `selftest_qa.py`:

| Check | Catches |
|---|---|
| `text_overlap` | two texts on top of each other |
| `text_too_small` | type below 15pt, held long enough to read |
| `out_of_frame` | text outside the safe area |
| `node_off_frame` | a node or shape past the frame edge |
| `node_overlap` | two artifact nodes stacked |
| `edge_through_node` | a connector crossing a node it does not connect |
| `shape_over_text` | a *filled* shape drawn in front of text |
| `title_lane_intrusion` | anything reaching into the reserved title lane |
| `label_orphaned` | a label vanishing off a stationary node |
| `low_contrast` | text below WCAG against what is behind it |
| `flicker` | something gone and back inside 1.6s |
| `dead_air` | no visible change for over 5s |
| plus the gate | timing drift, beat coverage, unresolved anchors |

Four rules keep them honest, all learned by getting them wrong first:

1. **Judge settled state, not transients.** A `FadeIn(scale=0.85)` passes through
   every size on the way in; a transform converges before it separates. Every
   check that measures a property requires it to *persist*.
2. **Contiguous runs.** A mobject animated twice hits the same intermediate size
   at both ends. Merging those scattered samples once reported half a minute of
   illegible text that never existed.
3. **Read the geometry, not the container.** A VGroup reports a child's opacity
   and its own default white; `Text` keeps its colour on the glyphs. Reading the
   container made every caption look black-on-black and every panel white.
4. **Determinism.** The activity signature used Python's `hash()`, which is
   randomised per process, so `dead_air` fired or not depending on the run. A
   check that works only sometimes is worse than none, because it is trusted.

## 3D

`Beat3DScene` records geometry **projected through the camera**, so every check
above applies unchanged — world coordinates say nothing about what the viewer
sees. `selftest_3d.py` proves it: two nodes 3.0 apart in z overlap 100% head-on
and 0% after the camera swings. Camera-pinned labels are exempt from projection,
since they are already in frame coordinates.

Sections 04 and 06 are 3D.

## Reading the checks

Twenty-three now. The five added in review pass 5 all came from the same place:
a reviewer watched the cut and named nineteen defects by their slate code, and
the instruction was to make the gate find them *before* fixing them. Thirteen of
the nineteen were caught by the new checks on the existing geometry, without a
re-render.

That exercise found more bugs in the checker than in the scenes. The worst was
that the recorder could not see a shape unless it was a top-level scene mobject —
so every `chip()`, `dot()` and bar, all of which wrap their geometry in a plain
VGroup, was invisible. Thirty-four falling tiles could appear, move and blink out
while the recorder logged two boxes.

Three checks also measured a defect's duration as first-hit minus last-hit rather
than as contiguous runs. One frame during a fade and one during the fade back are
seven seconds apart and describe nothing; read as a single run they invent a
seven-second defect that never appeared on screen. Whenever a check counts how
long something lasted, it has to group by contiguous run — that is now three
separate occasions the same mistake has been made here.

## Two layers, deliberately different in kind

The gate answers *is anything broken?* — eighteen checks, each proven by a
planted defect. It is not allowed an opinion.

`gemini_review.py` answers *is it any good?* It sends one settled frame per beat,
paired with the narration line that cues it, and is told what the gate has
already covered so it does not spend its attention there. Its first pass returned
228 judgements across 234 beats, and — more usefully — the same complaint about
ten consecutive beats of section 2, which is how a systemic composition problem
announces itself. `review_notes.py` groups them by theme so a hundred bullets
become five decisions.

One of those themes turned out to be mechanical enough to promote into the gate:
`stage_imbalance`, which measures the area-weighted centre of the composition
against the middle of the stage. A beat that is lopsided on purpose declares it
with `ctx.lopsided(reason)`, the same way a deliberate overlap declares itself.

## What is not solved yet

- **Semantic mismatch** — a visual that illustrates a different claim than the
  narration makes — is not machine-checkable and stays with Gemini and the human.
- **Aesthetic judgement** beyond balance. The gate still has no opinion about
  whether a metaphor lands.
- Everything renders at 480p15 for the iteration loop; the delivery render at
  1080p30 has not been done.

## Running it

A whole review pass is `pipeline/review_pass.sh` — gate, assemble, ask Gemini,
rank, dashboard. The individual steps:

```bash
# 1. timing for a section (generates scratch TTS on first run)
python3 -c "..."      # see timing.build()

# 2. where is the storyboard thin?
python3 pipeline/propose_beats.py --section 01_generation_got_cheap \
    --heading "1. Cold Open" --out out/storyboard/01_beat_proposals.md

# 3. render + gate (non-zero exit on any violation)
python3 pipeline/build.py --section 02_chat_log_fallacy \
    --scene-file scenes/s02_chat_log_fallacy.py --scene S02ChatLogFallacy

# 4. build the review page a human actually looks at
python3 pipeline/build_review_page.py --scene S02ChatLogFallacy \
    --section "02 · The Hidden Cost Of Looks Good" \
    --video scenes/media/videos/s02_chat_log_fallacy/480p15/S02ChatLogFallacy.mp4 \
    --beats out/beats/S02ChatLogFallacy.beats.json \
    --result scenes/out/qa/S02ChatLogFallacy.result.json \
    --out out/review/S02_beats.html

# 5. confirm the gate still works
python3 pipeline/selftest_qa.py
```
