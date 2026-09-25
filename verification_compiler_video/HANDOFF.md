# Handoff — video 2, *The Compiler For Trust*

Written 2026-08-28, at the end of the section 1 cold-open rework.

This file is the thing the other docs do not cover: **how to work on this**, and
what is true right now. It is written for an agent picking the work up cold.

- `README.md` — the output policy. Non-negotiable, read it first.
- `pipeline/README.md` — the architecture: four layers, the timing chain, the
  checks, how a scene is structured. Read before writing any scene code.
- `PIPELINE_STATUS.md` — what changed in each review pass, and why. The running
  log. Append to it; do not rewrite history in it.
- **this file** — method and live state.

## Follow-up status — human-audio final cuts

The cleaned human narration is now integrated. Section `04_05` was split at
67.720s into `04_artifact_graph.wav` and `05_compilation_traversal.wav`; all 11
sections have local faster-whisper word tables and timing tables in
`out/timing/`.

The review-marked full cuts are:

- `out/review/full_cut_human_review_marks_1x.mp4` — 796.3s
- `out/review/full_cut_human_review_marks_1x_1.25x.mp4` — 637.3s

The slate-free 1080p30 delivery cuts are:

- `out/final/compiler_for_trust_clean_1080p30_1x.mp4` — 796.4s
- `out/final/compiler_for_trust_clean_1080p30_1x_1.15x.mp4` — 692.7s

Timing audit: 240 beats / 240 narration lines, 100% coverage, no duplicate line
hits, no unresolved anchors. The only low-confidence line left is section 3 line
0, where STT clipped "High-assurance" to "Assurance"; the timing still lands on
the correct opening phrase. One aligner fix was added so script `Datasheets`
matches spoken `data sheets` in section 4.

Visual QA is still failing, but on visual/readability findings rather than
timing drift. The latest marked render has per-section drift within 0.05s.

---

## 1. Hard constraints

These are the user's, not mine. Do not relax them, and do not ask an agent
downstream to relax them either.

1. **Raw human audio never leaves this machine.** No voice recordings,
   voiceprints, speaker embeddings, or timing-rich narration artifacts to Gemini
   or any cloud API, ever, without explicit per-request approval. Script text,
   review notes, and rendered frames are approved for Gemini. The
   `assets/human_audio/` directory is gitignored for this reason as well as its
   size — it is the user's own voice.
2. **Nothing model-generated ships in the final video.** Visuals are rendered
   (Manim), not generated. Narration is real human speech; Gemini TTS is scratch
   audio for timing only. No generated video. No music.
3. **Credentials live in `~/.config/video-pipeline/credentials.env`** (mode
   0600), never in the repo. Load them with
   `set -a && source ~/.config/video-pipeline/credentials.env && set +a`.
4. **The script is locked for recording.** `drafts/script.md` is what the user
   is reading aloud. Do not change narration text without asking. The previous
   version is `drafts/script_v3_before_coldopen.md`.
5. **`stage_imbalance` is not a priority.** The user said so explicitly. Report
   it, waive it where the asymmetry is deliberate, never spend a pass on it.

---

## 2. Where it stands right now

**Branch `video2-section1-hook`, commit `33971c2`, not pushed.** It stacks on
`video2-pipeline-review-passes`, which the user has pushed to origin. The last
push attempt was declined by the permission prompt — ask before pushing.

**Uncommitted and NOT ours** — leave these alone, they are the user's in-flight
whitepaper release work:

- `whitepaper/build_pdf.py` (modified)
- `whitepaper/verification_compiler_whitepaper.md` (new)
- `verification_compiler_resources/` (new)

**Section 1 is done and clean**: 33 beats, one per narration line, 100%
coverage, drift −0.05s, gate PASS with 0 violations, 154.0s.

**Sections 2–11 are untouched this pass** and carry 29 findings between them,
16 of which are `stage_imbalance`. The other 13 are short transients — mostly a
0.5–2s outline crossing a label during an animation. The per-section table is in
`PIPELINE_STATUS.md` under "Where it stands".

**Review videos** (regenerable, under gitignored `out/`):

- `out/review/S01_hook_REVIEW_1.25x.mp4` — 2:03, the one to watch. 1.25× is the
  speed the cut ships at.
- `out/review/S01_hook_REVIEW.mp4` — 2:34, same thing at 1.0×.
- `out/review/S01_generation_got_cheap_REVIEW.mp4` — **stale**, the old
  section 1 from before the rework.
- `out/review/full_cut.mp4` — **stale**, predates the rework.

The full cut was deliberately not regenerated: sections 2–11 were last rendered
by `gate_all.py` with `VC_REVIEW_SLATE=1`, so they have the beat slate burned
into the corner while section 1 does not. Concatenating now gives a cut that is
slated for twelve minutes and clean for the first two. Re-render 2–11 slate-free
before assembling anything for the user.

A frame-by-frame walkthrough of the new hook is published at
<https://claude.ai/code/artifact/1cee17d8-be04-4277-bc72-5f5fe4673c54>.

---

## 3. How to work on this

### The gate is necessary and nowhere near sufficient

27 checks, each proven by a planted defect. It answers exactly one question:
*is anything broken?* It cannot answer *is it any good?*, and the difference
matters more than it sounds.

The version of section 1 where the plane was half its final size, the flood was
2px outlines that read as scattered confetti, and the "clean code" beat was five
dark boxes — **passed the gate with zero violations.** Everything that made the
hook actually work came from rendering frames and looking at them.

So the loop is:

```
change  ->  gate (is it broken?)  ->  extract frames  ->  LOOK  ->  Gemini  ->  repeat
```

Never skip the looking step. Never report a beat as good because the gate is
green.

### Extracting frames and looking at them

```bash
cd verification_compiler_video
M=scenes/media/videos/s01_generation_got_cheap/480p15/S01GenerationGotCheap.mp4
for t in 0.5 2.2 5.0 7.4; do
  ffmpeg -v error -ss $t -i $M -frames:v 1 /tmp/f$t.png -y
done
```

Then tile them into a contact sheet with PIL and read the sheet — nine frames at
0.62 scale in a 3×3 grid is a good ratio for spotting composition problems. Pull
a single frame at full resolution when you need to judge stroke weight or
legibility; the downscale in a contact sheet makes every stroke look thinner
than it is, and I nearly "fixed" a stroke that was already fine because of it.

Render **without** the slate when you are judging the picture
(`manim -ql --format=mp4 --disable_caching --media_dir scenes/media ...`), and
**with** it (`VC_REVIEW_SLATE=1` via `gate_all.py`) when you need to map a frame
back to a beat.

### The Gemini layer, and how to read it

```bash
set -a && source ~/.config/video-pipeline/credentials.env && set +a
rm -rf out/review/frames
python3 -u pipeline/gemini_review.py --only 01 --batch 6 --out out/review/gemini_s01.md
```

It sends **one settled frame per beat** — the frame at the end of the beat —
paired with the narration line. That sampling shapes everything it can and
cannot see:

- **It cannot see motion.** It will report "the code streaming into the plane is
  missing" when the settled frame is simply *after* the code was absorbed, and
  "the frame is static, showing neither the break nor the fix" when the beat does
  both and restores. Check the beat source before acting on a "missing motion"
  finding.
- **It gets the grammar wrong sometimes.** It asserted that squares are cyan;
  `style.NODE_KINDS` says code is a **blue** square and cyan is a **test
  circle**. Always check `NODE_KINDS` before acting on a grammar finding.
- **But when it says the same thing in two passes, it is usually right.** It
  flagged the gold-lit review diamond, the untyped flood colours, and the stale
  customer-growth chart in both passes. All three were real and all three were
  mine.
- **It will find things it just caused you to break.** My first fix for "how
  much did you read" was a violet ring around one tile. The next pass correctly
  pointed out that a circle is a *test* in this grammar. It is corner brackets
  now.

`pipeline/rank_findings.py` turns ~100 findings into ~20 distinct decisions when
you are reviewing the whole cut. For a single section the raw report is short
enough to read directly.

### Changing narration means rebuilding timing

Every visual cue is anchored to a *line of the script*, never to a hand-tuned
run_time. If the script changes, the timing table is stale and every beat after
the edit is cued to the wrong moment.

```bash
set -a && source ~/.config/video-pipeline/credentials.env && set +a
cd /home/lpurdy/repos/verifiability_compiler
python3 -m verification_compiler_video.pipeline.timing \
  --section 01_generation_got_cheap --heading "1. Cold Open" --refresh
```

`--refresh` is what makes it re-synthesize; without it, cached scratch audio and
transcript are reused, which is what makes the iteration loop cheap and is
exactly wrong after a script edit. The CLI drops the section heading line, which
had previously been synthesized as spoken narration.

Then verify every anchor resolves 1:1 before rendering — an ambiguous or
unmatched anchor is a build failure, but a *silently duplicated* one is worse.
See the verification snippet in §6.

### When the human take arrives

Point the same command at the real audio with `--audio <file>`. The timing table
rebuilds and every cue re-times itself. **No scene edits.** That is the whole
point of the architecture — do not hand-adjust run_times to fit a take.

Remember constraint 1: the human take is transcribed **locally**
(`transcribe_words.py`, faster-whisper, `--device cpu`). It does not go to a
cloud API.

---

## 4. Traps that cost me real time

### Working directory

Commands are run from `verification_compiler_video/`. The shell's cwd **resets**
after some tool calls, and `python3 pipeline/gate_all.py` from the repo root
fails with a confusing "No such file". `cd` to the video root at the start of
every command that needs it, and pass absolute paths to `build.py --scene-file`
(it resolves relative paths against a different cwd and looks for
`scenes/scenes/...`).

### Animating a child of a group you just wrapped

```python
flood = VGroup(self._owned["a"], self._owned["b"])   # ad-hoc wrapper
ctx.play(flood.animate.set_opacity(0.26), ...)       # play 1
ctx.play(tile.animate.set_opacity(1.0), ...)         # play 2 — tile is inside flood
```

This produces a `flicker` violation: the geometry recorder sees the child leave
the scene and come back. Manim's `add` absorbs children when an ad-hoc `VGroup`
wrapper arrives, and `BeatScene.play` restores them afterwards; animating a child
out from under that is not safe. Either animate the members individually from
the start, or do not re-light the child at all.

### `_own` raises on a tag that already exists

`ReplacementTransform` replaces what a tag points at. Re-point it directly —
`self._owned["wall"] = halves` — rather than calling `self._own("wall", ...)`,
which raises `tag 'wall' is already on stage`.

### `set_opacity(1.0)` resurrects stripped labels

`style.strip_labels()` zeroes label opacity. A later `set_opacity` on the group
or on a `.copy()` brings them back. Zero the labels on the copy explicitly:

```python
for sub in second.get_family():
    if getattr(sub, "text", None):
        sub.set_opacity(0)
```

### Text needs time, and the maths is not intuitive

`text_too_brief` uses `len(text)/11 + 0.75`, scaled by `EXPORT_SPEED = 1.25`.
"an organization" is fifteen characters and needs **2.6s on screen**. Cycling
three labels through one slot at 2.0s each fails, and looks rushed even where the
check does not fire. Stand them up as a list that stays.

### `ctx.hold()` clamps to the beat window, not to time remaining

A beat whose run_times plus holds exceed its window will overrun and push
everything after it late. `ctx.budget()` scales run_times; holds it does not.
Add the numbers up when a beat is dense.

### Composition rules I had to learn from frames, not from checks

- **Fill the tiles.** A flood of unfilled 2px outlines on a near-black ground
  reads as scattered confetti however many tiles are in it. `TILE_FILL = 0.18`
  in the tile's own colour.
- **Frame one has to be busy.** Easing 26 tiles in over 1.5s left eight faint
  outlines at t=0.5 — a video that has not started. 15 tiles inside 0.45s.
- **Spread the opening slam.** `code[:15]` takes whatever corner `free_points`
  filled first. `code[::2]` spreads it across the frame.
- **A red circle round a wreck reads as a prohibition sign.** Splayed lines read
  as impact.
- **Emphasis must never change a type.** Lighting a review diamond gold says it
  became a requirement. Brighten a node in its own colour.

---

## 5. Open decisions — the user's, not ours

1. **The shape-grammar question**, unresolved across two review passes and the
   single biggest theme in the Gemini findings. Gemini reads the `source` node
   (a tall rounded rect) as a plain rectangle, the `vqp` node (a clipped-corner
   polygon) as a document slice, and the gold barrier labelled "the standard" as
   a mis-typed requirement. Answering it changes roughly thirty places across the
   whole video. **Do not start it without an explicit decision from the user.**
2. **Pushing.** `video2-section1-hook` is committed and unpushed; the previous
   push was declined at the prompt.
3. **The composition pass.** `stage_imbalance` plus Gemini's "dead space" theme
   are the same finding from two directions. Deprioritized by the user.

Decided, and deliberately left alone:

- The closing card shows "a compiler for trust" one line early. Gemini flagged
  it in both passes. It has to: the last line's window is 1.8s and the phrase
  needs ~3.2s to read at 1.25×.
- Section 1 sets no title and its open runs full-bleed, with
  `title_lane_intrusion` waived on two beats. Both are deliberate; the reasons
  are in the code and in `PIPELINE_STATUS.md`.

---

## 6. Command cookbook

All from `verification_compiler_video/` unless stated.

```bash
# Gate one section (with the beat slate burned in, for mapping frames to beats)
VC_REVIEW_SLATE=1 python3 -u pipeline/gate_all.py --only 01

# Gate everything — 11 renders, about 10 minutes
VC_REVIEW_SLATE=1 python3 -u pipeline/gate_all.py

# Render one section clean, for looking at
manim -ql --format=mp4 --disable_caching --media_dir scenes/media \
  scenes/s01_generation_got_cheap.py S01GenerationGotCheap

# Inspect violations in detail — the summary elides the bounding boxes, and the
# boxes are what tell you *which* shape crossed *which* label. The file only
# exists for a section that failed; a clean section leaves only .result.json.
python3 -c "
import json; print(json.dumps(json.load(open('scenes/out/qa/S02ChatLogFallacy.violations.json')), indent=1))"

# Prove the checks still work — render first, then run
manim -ql --disable_caching --media_dir pipeline/media \
  pipeline/selftest_qa.py DeliberatelyBroken
python3 pipeline/selftest_qa.py      # -> SELFTEST PASS

# Rebuild timing after a script edit (from the REPO root)
python3 -m verification_compiler_video.pipeline.timing \
  --section 01_generation_got_cheap --heading "1. Cold Open" --refresh

# Verify every anchor resolves, one per line, before rendering (from REPO root)
python3 -c "
import ast, sys; from pathlib import Path
sys.path.insert(0,'.')
from verification_compiler_video.pipeline import timing as T
V = Path('verification_compiler_video')
lines = T.load('01_generation_got_cheap', V/'out'/'timing')
tree = ast.parse((V/'scenes'/'s01_generation_got_cheap.py').read_text())
anchors = [n.args[0].value for n in ast.walk(tree)
           if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
           and n.func.id == 'Beat' and n.args and isinstance(n.args[0], ast.Constant)]
seen = {}
for a in anchors:
    l = T.resolve_anchor(a, lines)
    if l.index in seen: print('DUP', l.index, repr(a[:40]), 'and', repr(seen[l.index][:40]))
    seen[l.index] = a
print(len(anchors), 'anchors,', len(lines), 'lines, uncovered:',
      [l.index for l in lines if l.index not in seen])"

# Gemini frame review of one section
set -a && source ~/.config/video-pipeline/credentials.env && set +a
rm -rf out/review/frames
python3 -u pipeline/gemini_review.py --only 01 --batch 6 --out out/review/gemini_s01.md

# A full review pass: gate, assemble, Gemini, rank, dashboard
bash pipeline/review_pass.sh

# Mux a section with its scratch narration so it can actually be reviewed
# (the raw manim render is video-only)
ffmpeg -y -v error \
  -i scenes/media/videos/s01_generation_got_cheap/480p15/S01GenerationGotCheap.mp4 \
  -i out/timing/01_generation_got_cheap.scratch.wav \
  -c:v libx264 -preset veryfast -crf 20 -c:a aac -b:a 128k -pix_fmt yuv420p \
  -vf "scale=854:480:force_original_aspect_ratio=decrease,pad=854:480:(ow-iw)/2:(oh-ih)/2,fps=15" \
  out/review/S01_hook_REVIEW.mp4
```

---

## 7. Still to do on the video as a whole

1. Review the slate-free 1.15x delivery cut for final content/visual notes.
2. Fix any remaining review-blocking visual findings the user calls out.
3. The shape-grammar decision, if and when the user makes it.
