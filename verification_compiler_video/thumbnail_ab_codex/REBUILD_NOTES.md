# Thumbnail Rebuild Notes (v2)

Date: 2026-08-29. Supersedes `HANDOFF_FOR_NEXT_MODEL.md` (deleted).
The rejected v1 pass is preserved in `rejected_v1/` for comparison.

## The Criticism v1 Earned

- All four got worse in the "cleanup" pass.
- **A:** read as visual chaos.
- **B:** lost the enticing text contrast between a chat log and a requirements
  record. The fix needed was to make meaningful text *fit the shapes*, not to
  replace it with abstract skeleton bars.
- **C:** weird diagonal lines of shapes, unexplained.
- **D:** did not make sense as a picture.

## Root Causes Found

### 1. The diagonal shape-chains were an arithmetic bug, not a style choice

v1 placed the artifact field with:

```python
x = 760 + ((i * 83) % 445)
y = 90  + ((i * 47) % 505)
```

Both coordinates are linear in `i`, so every consecutive shape steps a constant
`(+83, +47)` until it wraps. That draws literal diagonal lines of shapes. It was
used as a stand-in for randomness and is why A looked like noise and C looked
decorative and strange.

**Fix:** placement is now either an explicit layout or a seeded `random.Random`
draw. No modular-arithmetic scattering anywhere in the file.

### 2. Text was dropped because it overflowed, instead of being fitted

v1 responded to "unreadable at mobile size" by deleting the content. The actual
constraint was that nothing measured the text against the shape holding it.

**Fix:** `fit_font(draw, text, max_w, max_h, start, ...)` returns the largest
size that measures inside the box, and anything that still cannot fit is
recorded in `OVERFLOWS` and printed at the end of every run. The run now ends
with `text fit: all boxed text fits` or an explicit list of failures. Row and
bubble heights are also *derived* from panel geometry rather than hardcoded, so
adding a fifth evidence row cannot silently push it through the panel floor.

### 3. Photographic base frames bled through the composites

v1 composited rendered video stills under the panels, and the source captions
("input to the configured range...") showed through B's artwork.

**Fix:** every thumbnail is pure vector on a faint grid. No base frames.

### 4. Glyph centering was off

PIL's `anchor="mm"` centers on the font's ascender/descender span, not the glyph
box, so `?` and checkmarks sat visibly high in their containers. `glyph_centered()`
measures the real glyph bbox instead.

## What Each Thumbnail Is Now

### A - `thumb_A_who_checks_it.png`
Calm and iconic instead of dense. One stack of generated code cards, running off
both frame edges to imply the queue continues; one arrow; one gate; and past the
gate a **dashed empty slot with a `?` in it** - the checker's seat, unfilled.
Shape count went from 54 scattered artifacts to a single column of 7.

### B - `thumb_B_chat_not_evidence.png`
Meaningful text restored and fitted. Left panel is a chat log with ragged,
unstructured bubbles: `looks good` / `probably passes` / `want tests?`. Right
panel is a record with uniform rows, a mono key/value per row, a green rail, and
a per-row check: `REQ-17 linked`, `TEST PASS`, `HUMAN REVIEW`, `VERSION a81f`.
The X and check are demoted to header badges so they support the contrast
instead of dominating it.

### C - `thumb_C_bottleneck_trust.png`
Rebuilt as two rates, per the guidance. Same lane, same card pitch, both inside
the frame: `GENERATED` is packed to nine, `VERIFIED` holds two. The only variable
is fill, so the empty lane carries the whole message. No diagonal chains.

### D - `thumb_D_compiler_for_trust.png`
Rebuilt as one legible pipeline instead of a graph cluster. Full-width hook on
top, then `AI CODE` -> `VERIFY` -> `EVIDENCE` left to right, with `AI REVIEW` and
`HUMAN SIGN-OFF` as equal-sized chips inside the VERIFY machine. AI involvement
is explicit; the human is the signer, not the AI.

## Workflow Notes For Next Time

- `python3 make_thumbnails.py` regenerates all four plus the contact sheet, the
  246px mobile preview, and `thumbnail_manifest.json`. Check the text-fit line at
  the end of the run.
- Read `thumbnail_mobile_preview.jpg` before judging anything. It is the size the
  thumbnail is actually consumed at.
- Gemini review (`review_thumbnails.py`) is useful for catching mobile
  readability problems and nothing else. It over-weights cold-feed CTR heuristics
  and it recommended the changes that produced the rejected v1 pass. Treat it as
  one signal after the concept already looks right to a human, never as the
  authority on taste or conceptual coherence.
- When a review says text is unreadable, the response is to make it bigger or
  shorter. Deleting the idea is not a fix.
