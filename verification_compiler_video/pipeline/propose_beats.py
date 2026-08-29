"""
Ask Gemini where the storyboard is too thin.

The target is that almost every narration line changes the picture. The gate
already reports *coverage* — which lines have no beat — but not what the beat
should be. This closes that loop: it sends the narration, the timing table, and
the beats that already exist, and asks for concrete proposals for the gaps.

The model is not choosing anything. It proposes; the gate measures; a human
decides. Only text leaves the machine.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VIDEO = HERE.parent
REPO = VIDEO.parent
sys.path.insert(0, str(REPO / "whitepaper" / "gemini_tools"))

from gemini_client import generate_thinking  # noqa: E402

MODEL = "models/gemini-3.1-pro-preview"

VISUAL_LANGUAGE = """
Fixed visual system — propose within it, never replace it:
- Near-black ground. Sparse on-screen text; narration carries the words.
- Accents: cyan, blue, violet, gold, green; red for anomaly or staleness.
- Shape grammar: requirement = hexagon, code = square, test = circle,
  result/evidence = rounded record, source region = document slice,
  review = diamond, VQP = folded packet.
- Everything is rendered deterministically in Manim. Nothing is image-generated.
- The frame has three lanes: a title lane at the top, a reserved caption lane at
  the bottom, and the stage between them. Diagrams live on the stage only.
- A caption needs ~3.8s on screen to stay readable. Lines shorter than that must
  change the *diagram* rather than put up a caption.
"""

TASK = """
For every narration line listed as UNCOVERED, propose one beat: a specific,
renderable visual change cued to that line.

A beat is a *change*, not a scene. "Show the artifact graph" is not a beat.
"The orphan node's stroke turns red and the other edges dim" is a beat.

Rules:
- Reuse what is already on stage wherever possible — a beat that transforms an
  existing element reads better than one that clears and rebuilds.
- Respect the shape grammar above.
- Say what enters, what changes, and what leaves.
- Keep it buildable from primitives: shapes, arrows, text, transforms, camera
  moves. No photographs, no generated imagery.
- If a line genuinely wants no visual change — a beat of silence after a hard
  statement — say so and say why. A held frame is a legitimate choice when it is
  a choice; the gate flags anything over 5 seconds.

Also flag, separately:
- any line whose EXISTING beat illustrates a different claim than the line makes;
- any place where two adjacent beats would collide in the same region of frame;
- the three lines in this section that most deserve a genuinely ambitious visual
  (a 3D camera move, a morph, a full-stage recomposition), and what it should be.

Return markdown:

## Proposed beats
For each: `line index · anchor phrase` then Enters / Changes / Leaves, one line each.

## Mismatches
## Collision risks
## Three to make ambitious
"""


def section_text(script: Path, heading_prefix: str) -> str:
    body = script.read_text(encoding="utf-8").split("## Full Narration Draft", 1)[1]
    for block in re.split(r"\n### ", body)[1:]:
        if block.startswith(heading_prefix):
            return block
    raise SystemExit(f"no section starting {heading_prefix!r}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--section", required=True, help="section id, e.g. 01_generation_got_cheap")
    ap.add_argument("--heading", required=True, help="script heading prefix, e.g. '1. Cold Open'")
    ap.add_argument("--beats", type=Path, help="existing beats.json, if any")
    ap.add_argument("--timing-dir", type=Path, default=VIDEO / "out" / "timing")
    ap.add_argument("--script", type=Path, default=VIDEO / "drafts" / "script.md")
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    sys.path.insert(0, str(REPO))
    from verification_compiler_video.pipeline import timing as T

    lines = T.load(args.section, args.timing_dir)
    existing = []
    if args.beats and args.beats.exists():
        existing = json.loads(args.beats.read_text())["beats"]
    covered = set()
    for b in existing:
        try:
            covered.add(T.resolve_anchor(b["anchor"], lines).index)
        except LookupError:
            pass

    inventory = []
    for l in lines:
        mark = "covered" if l.index in covered else "UNCOVERED"
        inventory.append(f"[{l.index:2d}] ({l.duration:4.1f}s) {mark}: {l.text}")

    have = "\n".join(
        f"- {b['anchor']!r} -> {b.get('note') or '(no note)'}" for b in existing
    ) or "(none yet)"

    prompt = "\n\n".join([
        "You are a storyboard editor for a technical explainer video about the "
        "Verification Compiler — a system that turns a software project into an "
        "artifact graph, traverses it deterministically to build bounded "
        "Verification Query Packages, has them reviewed by a model "
        "(developmental) or a human (certification-facing), and keeps the result "
        "as immutable evidence.",
        VISUAL_LANGUAGE,
        f"## Section {args.section}\n\n" + section_text(args.script, args.heading),
        "## Narration lines, with timing and current coverage\n\n" + "\n".join(inventory),
        "## Beats that already exist\n\n" + have,
        TASK,
    ])

    text = generate_thinking(prompt, model=MODEL, thinking_level="HIGH")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(f"# Beat proposals — {args.section}\n\nModel: {MODEL}\n\n{text}\n")
    print(f"{args.out}  ({len(lines) - len(covered)} uncovered lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
