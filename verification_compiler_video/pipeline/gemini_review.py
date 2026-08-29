"""
Aesthetic and semantic review of rendered beats, by Gemini.

The geometry gate answers "is anything broken?" — boxes overlapping, text too
small, a connector on the wrong layer. It has no opinion about whether the
picture is any good, or whether it illustrates the sentence being spoken over
it. Those are the two failures the README has listed as unsolved since the
pipeline was built, and they are the ones that cost review passes.

So: one settled frame per beat, paired with the line of narration it is cued to,
sent to a vision model with the storyboard's own rules as the rubric. What comes
back is a list of beats worth looking at, which is a much shorter list than 234.

Only rendered frames and script text leave the machine. Narration audio never
does.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
VIDEO = HERE.parent
REPO = VIDEO.parent
sys.path.insert(0, str(REPO / "whitepaper" / "gemini_tools"))

from gemini_client import generate_content, image_part  # noqa: E402

DEFAULT_MODEL = "models/gemini-3.1-pro-preview"

SECTIONS = [
    ("01_generation_got_cheap", "S01GenerationGotCheap", "1 · Generation Got Cheap"),
    ("02_chat_log_fallacy", "S02ChatLogFallacy", "2 · The Hidden Cost Of Looks Good"),
    ("03_traceability_shape", "S03TraceabilityShape", "3 · The Shape Of Traceability"),
    ("04_artifact_graph", "S04ArtifactGraph", "4 · The Artifact Graph"),
    ("05_compilation_traversal", "S05CompilationTraversal", "5 · Compilation As Traversal"),
    ("06_vqp", "S06VQP", "6 · The Verification Query Package"),
    ("07_dual_mode_review", "S07DualModeReview", "7 · Dual-Mode Review"),
    ("08_evidence_cards", "S08EvidenceCards", "8 · Evidence Records"),
    ("09_readiness_map", "S09ReadinessMap", "9 · The Readiness Map"),
    ("10_evidence_surface", "S10EvidenceSurface", "10 · The Evidence Surface"),
    ("11_end_card", "S11EndCard", "11 · End Card"),
]

RUBRIC = """\
You are reviewing frames from an explainer video called "The Compiler For Trust",
about a Verification Compiler for safety-critical software. Each frame is one
"beat": a single visual change cued to one line of narration. You are given the
line and the frame that is on screen while it is spoken.

The visual system, which you should hold the frames to:
- Dark navy background. Cyan = code, gold = requirements, violet = review/source,
  green = evidence/result, red = anomaly. Shape carries meaning: hexagon =
  requirement, square = code, circle = test, document slice = source, rounded
  record = evidence, diamond = review, packet = verification query package.
- Sparse on-screen text. The narration carries the words; the picture carries
  the structure. Labels are short identifiers, not sentences.
- Three reserved lanes: a title strip at the top, the stage in the middle, a
  caption lane at the bottom. Nothing should cross between them.
- A small amber code in the TOP LEFT corner (e.g. "02 b07   14.3s") is a review
  identifier, not part of the composition. Ignore it when judging the frame, but
  DO cite it when reporting a problem.

An automated geometry gate has already checked, and cleared, all of: text
overlap, text below 15pt, content outside the frame, arrowheads landing inside
labels, flicker, dead air, node overlap, edges crossing nodes, orphaned labels,
shapes over text, title-lane intrusion, WCAG colour contrast, nodes off frame,
strokes across text, texts crowded closer than 0.16 units, connector layering,
and over-stroked text. Do not report those categories — they are covered, and
repeating them buries the findings that are not.

Report ONLY:
1. SEMANTIC MISMATCH — the picture illustrates a different claim than the line
   says, or the shape grammar is used wrongly (a test drawn as a hexagon), or
   the frame is stale: it still shows the previous beat's idea.
2. COMPOSITION — badly balanced, everything drifting to one side, a large dead
   region, elements at arbitrary-looking positions, a frame that reads as
   cluttered even though nothing technically overlaps.
3. LEGIBILITY IN PRACTICE — text that is technically large enough but hard to
   read against what is behind it, too many simultaneous colours, a label whose
   meaning is unclear.
4. MISSED OPPORTUNITY — the line describes something concrete (a number, a
   named artifact, a motion) that the frame does not show at all.

Be specific and cite the beat code. "02 b07 — the line names three standards but
only two chips are on screen" is useful. "Looks good" is not. If a beat is fine,
do not mention it at all.

Format every finding as a single line, exactly:

    BEAT | SEVERITY | CATEGORY | one sentence

where SEVERITY is one of:

  BLOCKING   a viewer would see this as a mistake — the picture contradicts the
             narration, an element is unreadable, or the frame still shows the
             previous idea. Reserve this for things that are wrong, not things
             that could be better.
  WORTH-FIX  the frame works but a specific, named change would clearly improve
             it. Name the change.
  POLISH     taste. Say it once and move on.

and CATEGORY is one of: MISMATCH, COMPOSITION, LEGIBILITY, MISSED.

Nothing else on the line. No headings, no bullets, no bold. One line per finding,
at most three findings per beat, and prefer none to a weak one.
"""


def frame_at(video: Path, t: float, out: Path) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-y", "-ss", f"{t:.3f}", "-i", str(video), "-frames:v", "1",
         "-q:v", "2", str(out)],
        check=True, capture_output=True,
    )
    return out


def beat_frames(scene: str, section_id: str, frames_dir: Path) -> list[tuple[dict, Path]]:
    """One settled frame per beat: late in the beat's window, after it has landed."""
    beats = json.loads((VIDEO / "out" / "beats" / f"{scene}.beats.json").read_text())["beats"]
    hits = sorted((VIDEO / "scenes" / "media" / "videos").rglob(f"{scene}.mp4"))
    if not hits:
        raise SystemExit(f"{scene} has not been rendered")
    video = hits[-1]
    out: list[tuple[dict, Path]] = []
    prefix = section_id.split("_")[0]
    # 1-based, to match the review slate burned into the frame. A reviewer
    # reading "01 b13" off the screen must find b13 in this report.
    for n, beat in enumerate(beats, 1):
        # 75% through the window: past the animation, before the next cue.
        t = beat["start"] + min(beat["window"] * 0.75, max(beat["window"] - 0.15, 0.05))
        path = frames_dir / f"{prefix}_b{n:02d}.jpg"
        if not path.exists():
            frame_at(video, t, path)
        beat = dict(beat, code=f"{prefix} b{n:02d}", t=round(t, 2))
        out.append((beat, path))
    return out


def review_section(scene: str, section_id: str, title: str, model: str,
                   batch: int, frames_dir: Path) -> str:
    pairs = beat_frames(scene, section_id, frames_dir)
    chunks: list[str] = []
    for i in range(0, len(pairs), batch):
        group = pairs[i:i + batch]
        parts: list[dict] = [{"text": f"{RUBRIC}\n\nSection: {title}\n"}]
        for beat, path in group:
            parts.append({"text":
                          f"\n--- beat {beat['code']} (at {beat['t']}s) ---\n"
                          f"narration: {beat['line']}\n"
                          + (f"storyboard intent: {beat['note']}\n" if beat.get("note") else "")})
            parts.append(image_part(path))
        parts.append({"text": "Report only real problems in these beats, one line each, "
                              "in the BEAT | SEVERITY | CATEGORY | sentence format. "
                              "No preamble and no summary."})
        print(f"  {scene} beats {i}-{i + len(group) - 1} ...", flush=True)
        chunks.append(generate_content(model, parts, timeout=300))
    return "\n\n".join(chunks)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--only", nargs="*", help="section prefixes, e.g. 01 04")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--batch", type=int, default=6)
    ap.add_argument("--out", type=Path,
                    default=VIDEO / "out" / "review" / f"gemini_frame_review_{date.today().isoformat()}.md")
    args = ap.parse_args()

    wanted = SECTIONS
    if args.only:
        wanted = [s for s in SECTIONS if any(s[0].startswith(p) for p in args.only)]

    frames_dir = VIDEO / "out" / "review" / "frames"
    report = [f"# Gemini frame review — {date.today().isoformat()}",
              "", f"Model: `{args.model}`  ",
              "One settled frame per beat, paired with the narration line it is cued to.",
              "The geometry gate had already passed every section clean, so everything",
              "below is a judgement call rather than a defect.", ""]

    for section_id, scene, title in wanted:
        print(f"{scene} ...", flush=True)
        try:
            body = review_section(scene, section_id, title, args.model, args.batch, frames_dir)
        except Exception as exc:                     # noqa: BLE001
            body = f"REVIEW FAILED: {exc}"
            print(f"  failed: {exc}", flush=True)
        report += [f"## {title}", "", body, ""]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(report) + "\n")
    print(f"\nwrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
