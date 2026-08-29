"""
Send the A/B/C candidate keyframes to Gemini for structured selection critique.

Per section: the narration text + nine keyframes (three per candidate). Gemini is
asked to pick the candidate that best serves *that narration*, list concrete
defects, and propose a hybrid. Its output is developmental input to a human
choice, not the choice itself.

Only rendered frames and script text leave the machine. No audio, ever.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
VIDEO = HERE.parent
REPO = VIDEO.parent
sys.path.insert(0, str(REPO / "whitepaper" / "gemini_tools"))

from gemini_client import generate_content, image_part  # noqa: E402

MODEL = "models/gemini-3.1-pro-preview"
CANDIDATES = HERE / "out" / "candidates"
OUT_DIR = HERE / "out" / "reviews"

SECTION_TO_SCRIPT = {
    "01_generation_got_cheap": "1. Cold Open: Generation Got Cheap",
    "02_chat_log_fallacy": '2. The Hidden Cost Of "Looks Good"',
    "03_traceability_shape": "3. Safety-Critical Software Already Has The Shape",
    "04_artifact_graph": "4. Artifacts Become A Graph",
    "05_compilation_traversal": "5. Compilation Means Traversal",
    "06_vqp": "6. The Verification Query Package",
    "07_dual_mode_review": "7. Same Package, Two Review Modes",
    "08_evidence_cards": "8. Evidence Cards, Not Conversations",
    "09_readiness_map": "9. Verification Readiness Is A Map, Not Magic",
    "10_evidence_surface": "10. Closing: The Future Is Evidence Generation",
}

VISUAL_LANGUAGE = """
Project visual language (fixed — critique against it, do not propose replacing it):
- Near-black background. Sparse on-screen text; the narration carries the words.
- Bright accents on dark: cyan, blue, violet, gold, green; red for anomaly/stale.
- Stable shape grammar: requirement = hexagon, code = square, test = circle,
  result/evidence = rounded record, source region = document slice,
  review = diamond, VQP = folded packet.
- Closer to 3Blue1Brown mathematical animation than to a slide deck.
- Everything is rendered deterministically in Manim. Nothing is image-generated.
"""

BRIEF = """
You are helping select between three competing visual treatments for one section
of a technical explainer video about the "Verification Compiler" — a system that
turns a software project into an artifact graph, traverses it deterministically to
assemble bounded Verification Query Packages, has those reviewed by a model
(developmental) or a human (certification-facing), and records the outcome as
immutable evidence, producing a Verification Readiness Metric.

The three candidate sets each make a different bet:
- Set A — diagrammatic: state the idea as a clean labelled diagram.
- Set B — mechanistic: show the process happening (rates diverging, a walk, a fold, a swap).
- Set C — concrete: put the real artifact on screen (actual JSON, trace tables, terminals).

You are shown three keyframes from each candidate, in order A1 A2 A3, B1 B2 B3, C1 C2 C3,
sampled at 25%, 55% and 90% through each clip.
"""

TASK = """
Answer in this exact structure, in markdown:

## Recommendation
One of A, B, or C, plus one sentence saying why it serves THIS narration best.

## Ranking
A ranked list of all three with a half-sentence each.

## Defects
For EACH candidate (A, B, C), list concrete, fixable defects. Be specific and
visual — name the element and what is wrong with it. Look hard for:
- text overlapping other text or leaving the frame;
- elements crowded into one region leaving large dead space;
- arrowheads landing on top of node labels;
- text too small to read at 480p, or too dense to absorb in the time available;
- a visual that illustrates a *different* claim than the narration makes;
- shape grammar violations against the project visual language;
- anything that reads as decorative rather than explanatory.
If a candidate has no defect in some category, do not invent one.

## Hybrid
The single best combination: which candidate to build on, and precisely which
element to import from the others. Be concrete enough to implement.

## Narration mismatch
Any place where the strongest visual still does not match what the narrator says
at that moment, including lines that have no visual support at all.
"""


def section_narration(section: str) -> str:
    script = (VIDEO / "drafts" / "script.md").read_text(encoding="utf-8")
    heading = SECTION_TO_SCRIPT[section]
    body = script.split("## Full Narration Draft", 1)[1]
    blocks = re.split(r"\n### ", body)
    for block in blocks:
        if block.strip().startswith(heading):
            return block.strip()
    raise SystemExit(f"could not find narration for {section}")


def review_section(section: str, entry: dict) -> str:
    parts: list[dict] = [{"text": BRIEF}, {"text": VISUAL_LANGUAGE}]
    parts.append({"text": f"\n## Narration for this section\n\n{section_narration(section)}\n"})
    for set_name in "ABC":
        info = entry[set_name]
        parts.append({"text": f"\n--- Candidate {set_name}: {info['scene']} "
                              f"({info['duration']}s) ---"})
        for frame in info["frames"]:
            parts.append(image_part(CANDIDATES / frame))
    parts.append({"text": TASK})
    return generate_content(model=MODEL, parts=parts, timeout=300)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--section", action="append", default=[],
                        help="Section id to review. Repeatable. Default: all.")
    args = parser.parse_args()

    index = json.loads((CANDIDATES / "index.json").read_text())
    sections = args.section or list(index)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for section in sections:
        print(f"reviewing {section} …", flush=True)
        try:
            text = review_section(section, index[section])
        except Exception as exc:  # noqa: BLE001 — one bad section must not kill the batch
            print(f"  FAILED: {type(exc).__name__}: {exc}")
            continue
        dest = OUT_DIR / f"{section}.md"
        dest.write_text(f"# Candidate review — {section}\n\n"
                        f"Model: {MODEL} · {date.today().isoformat()}\n\n{text}\n")
        print(f"  -> {dest.relative_to(HERE)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
