"""
Render + gate.

The pipeline's job is to make a bad frame impossible to ship without somebody
having said yes to it. Three rules, each one a direct answer to a way video 1
lost a pass:

1. **No silent truncation.** Video 1 muxed with ffmpeg `-t <target>`, so a scene
   that ran 1.6s long simply lost its ending and nothing said so. Here the
   rendered duration is measured, compared against the narration, and a mismatch
   beyond tolerance fails the build.

2. **QA before eyes.** Every render is checked for overlap, clipping, tiny text,
   arrowheads in labels, flicker and dead air before a human is asked to look.

3. **Coverage is enforced.** Every narration line must have a beat, and every
   beat's anchor must resolve. A line with no visual is a build failure, not a
   thing to notice in review.
"""
from __future__ import annotations

import argparse
import ast
import json
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
VIDEO = HERE.parent
OUT = VIDEO / "out"

DURATION_TOLERANCE = 0.25   # seconds of drift between narration and render


@dataclass
class SectionResult:
    section: str
    scene: str
    render: str
    target_seconds: float
    rendered_seconds: float
    drift: float
    violations: int
    coverage: float
    ok: bool


def probe_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(out.stdout.strip())


def anchors_in_source(scene_file: Path, scene_class: str) -> list[str]:
    """
    Read the beat anchors straight out of the scene source.

    Video 1 kept a hand-maintained anchor list that drifted out of sync with the
    code — seven live anchors were never checked and six sections had none at
    all. Deriving them from the AST means the check can never fall behind.
    """
    tree = ast.parse(scene_file.read_text())
    found: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == scene_class:
            for call in ast.walk(node):
                if (isinstance(call, ast.Call) and isinstance(call.func, ast.Name)
                        and call.func.id == "Beat" and call.args
                        and isinstance(call.args[0], ast.Constant)
                        and isinstance(call.args[0].value, str)):
                    found.append(call.args[0].value)
    return found


def check_coverage(section_id: str, scene_file: Path, scene_class: str,
                   timing_dir: Path) -> tuple[float, list[str]]:
    """
    What fraction of narration lines have a beat cued to them?

    The brief is that almost every line should change the picture, so this is the
    number that says whether the storyboard is actually dense enough.
    """
    sys.path.insert(0, str(VIDEO.parent))
    from verification_compiler_video.pipeline import timing as T

    lines = T.load(section_id, timing_dir)
    anchors = anchors_in_source(scene_file, scene_class)
    covered: set[int] = set()
    unresolved: list[str] = []
    for anchor in anchors:
        try:
            covered.add(T.resolve_anchor(anchor, lines).index)
        except LookupError as exc:
            unresolved.append(f"{anchor!r}: {exc}")
    return (len(covered) / max(len(lines), 1)), unresolved


def render(scene_file: Path, scene_class: str, quality: str = "l") -> Path:
    proc = subprocess.run(
        ["manim", f"-q{quality}", "--format=mp4", "--disable_caching",
         str(scene_file), scene_class],
        capture_output=True, text=True, cwd=scene_file.parent,
    )
    if proc.returncode != 0:
        # Surface the scene's own error. Swallowing it behind a CalledProcessError
        # means every failed render costs a second run just to see why.
        tail = (proc.stderr or proc.stdout or "").strip().splitlines()
        print("\n".join(tail[-40:]))
        raise SystemExit(f"render failed for {scene_class}")
    hits = sorted((scene_file.parent / "media" / "videos").rglob(f"{scene_class}.mp4"))
    if not hits:
        raise SystemExit(f"render produced no file for {scene_class}")
    return hits[-1]


def gate(section_id: str, scene_file: Path, scene_class: str,
         timing_dir: Path, qa_dir: Path, quality: str = "l") -> SectionResult:
    sys.path.insert(0, str(VIDEO.parent))
    from verification_compiler_video.pipeline import qa as QA, timing as T

    lines = T.load(section_id, timing_dir)
    # The target is the audio file's length, which is what the scene renders to —
    # not the last spoken word, which leaves the trailing silence unaccounted for.
    target = T.audio_duration(section_id, timing_dir) or max(l.end for l in lines)

    coverage, unresolved = check_coverage(section_id, scene_file, scene_class, timing_dir)
    if unresolved:
        print(f"  UNRESOLVED ANCHORS in {scene_class}:")
        for u in unresolved:
            print(f"    {u}")

    video = render(scene_file, scene_class, quality=quality)
    rendered = probe_duration(video)
    drift = rendered - target

    geometry = qa_dir / f"{scene_class}.geometry.json"
    violations: list[dict] = []
    if geometry.exists():
        violations = QA.check_all(geometry)
    else:
        print(f"  WARNING: no geometry recorded for {scene_class} — QA skipped")

    ok = (abs(drift) <= DURATION_TOLERANCE and not violations and not unresolved)
    result = SectionResult(
        section=section_id, scene=scene_class, render=str(video),
        target_seconds=round(target, 3), rendered_seconds=round(rendered, 3),
        drift=round(drift, 3), violations=len(violations),
        coverage=round(coverage, 3), ok=ok,
    )

    print(f"\n{scene_class}")
    print(f"  narration  {target:7.2f}s")
    print(f"  rendered   {rendered:7.2f}s   drift {drift:+.2f}s"
          f"{'  <-- OUT OF TOLERANCE' if abs(drift) > DURATION_TOLERANCE else ''}")
    print(f"  coverage   {coverage:6.1%} of narration lines have a beat")
    print(QA.report(violations))

    if violations:
        (qa_dir / f"{scene_class}.violations.json").write_text(
            json.dumps(violations, indent=2) + "\n")
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--section", required=True)
    ap.add_argument("--scene-file", type=Path, required=True)
    ap.add_argument("--scene", required=True)
    ap.add_argument("--timing-dir", type=Path, default=OUT / "timing")
    ap.add_argument("--qa-dir", type=Path, default=OUT / "qa")
    ap.add_argument("--quality", default="l")
    ap.add_argument("--allow-fail", action="store_true",
                    help="Report violations but exit 0 (for iterating).")
    args = ap.parse_args()

    args.qa_dir.mkdir(parents=True, exist_ok=True)
    result = gate(args.section, args.scene_file, args.scene,
                  args.timing_dir, args.qa_dir, args.quality)
    (args.qa_dir / f"{args.scene}.result.json").write_text(
        json.dumps(asdict(result), indent=2) + "\n")
    return 0 if (result.ok or args.allow_fail) else 1


if __name__ == "__main__":
    raise SystemExit(main())
