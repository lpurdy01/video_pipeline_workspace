from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "manifest_pipeline" / "out"
PRODUCTION_MANIFEST = ROOT / "production_manifest.json"


def run(cmd: list[str]) -> None:
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)


def _fmt_hms(seconds: float) -> str:
    s = max(0.0, float(seconds))
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    sec = s - h * 3600 - m * 60
    return f"{h:02d}:{m:02d}:{sec:05.2f}"


def _narration_excerpt(text: str, position_ratio: float, window_chars: int = 320) -> str:
    """Pull a short excerpt of narration centered on the given ratio (0..1)
    along the section's narration text. The text is split into "lines" so we
    don't cut in the middle of a sentence; we walk lines until we span roughly
    `window_chars` around the target position."""
    if not text:
        return ""
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if not lines:
        return ""
    # Cumulative char length per line
    cum = []
    total = 0
    for ln in lines:
        total += len(ln) + 1
        cum.append(total)
    target = max(0, min(total - 1, int(total * position_ratio)))

    # Find center line
    center_idx = 0
    for i, c in enumerate(cum):
        if c >= target:
            center_idx = i
            break

    # Expand outward until we've collected roughly window_chars
    lo = center_idx
    hi = center_idx
    accum = len(lines[center_idx])
    while accum < window_chars and (lo > 0 or hi < len(lines) - 1):
        if lo > 0:
            lo -= 1
            accum += len(lines[lo]) + 1
            if accum >= window_chars:
                break
        if hi < len(lines) - 1:
            hi += 1
            accum += len(lines[hi]) + 1

    excerpt = "\n  ".join(lines[lo:hi + 1])
    prefix = "…" if lo > 0 else ""
    suffix = "…" if hi < len(lines) - 1 else ""
    return prefix + "\n  " + excerpt + "\n  " + suffix


def write_review_context(frames_manifest: Path, out: Path) -> None:
    manifest = json.loads(PRODUCTION_MANIFEST.read_text(encoding="utf-8"))
    frames = json.loads(frames_manifest.read_text(encoding="utf-8"))
    sections = {section["id"]: section for section in manifest.get("sections", [])}
    lines = [
        f"Project title: {manifest.get('title', 'Untitled')}",
        "",
        "Each frame below is paired with the elapsed timestamp in the prototype and the",
        "narration excerpt playing at approximately that moment. Use it to judge whether",
        "the visual matches the narration at that beat.",
        "",
        "Frame/section context:",
    ]
    for idx, frame in enumerate(frames, start=1):
        section = sections.get(frame["section_id"], {})
        visual = section.get("visual", {})
        section_start = frame.get("section_start", 0.0)
        section_end = frame.get("section_end", section_start + 1.0)
        section_duration = max(0.01, section_end - section_start)
        ts = float(frame["timestamp_seconds"])
        position_ratio = max(0.0, min(1.0, (ts - section_start) / section_duration))
        narration_excerpt = _narration_excerpt(
            section.get("narration_text", ""), position_ratio, window_chars=300
        )
        in_section = max(0.0, ts - section_start)
        lines.extend(
            [
                "",
                f"Frame {idx}: {Path(frame['path']).name}",
                f"- Section: {frame['section_id']} - {frame.get('title', section.get('title', ''))}",
                f"- Elapsed (overall): {_fmt_hms(ts)}    in-section: {_fmt_hms(in_section)} of {_fmt_hms(section_duration)}",
                f"- Cue: {frame.get('cue')}",
                f"- Intended visual: {visual.get('prompt', '')}",
                f"- Narration at this moment (approx.): {narration_excerpt}",
            ]
        )
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract manifest review frames and send them to Gemini visual review.")
    parser.add_argument("--frames-dir", type=Path, default=OUT / "review_frames")
    parser.add_argument("--out", type=Path, default=OUT / "manifest_visual_review.md")
    parser.add_argument("--todos-out", type=Path, default=OUT / "manifest_visual_todos.md")
    parser.add_argument("--context-out", type=Path, default=OUT / "manifest_review_context.md")
    parser.add_argument(
        "--model",
        default="auto",
        help="Gemini model id, or 'auto' to use the strongest available preferred visual review model.",
    )
    parser.add_argument(
        "--dense", type=float, default=0.0,
        help="If >0, additionally sample one frame every N seconds within each section. "
             "Forwarded to extract_review_frames.py.",
    )
    args = parser.parse_args()

    extractor = ROOT / "manifest_pipeline" / "extract_review_frames.py"
    reviewer = ROOT / "image_review_pipeline" / "review_keyframes.py"
    todos = ROOT / "manifest_pipeline" / "review_to_todos.py"
    if args.frames_dir.exists():
        shutil.rmtree(args.frames_dir)
    extract_cmd = [sys.executable, extractor.as_posix(), "--out-dir", args.frames_dir.as_posix()]
    if args.dense > 0:
        extract_cmd.extend(["--dense", str(args.dense)])
    run(extract_cmd)
    images = sorted(args.frames_dir.glob("*.png"))
    if not images:
        raise SystemExit(f"No frames extracted in {args.frames_dir}")
    write_review_context(args.frames_dir / "frames_manifest.json", args.context_out)
    run(
        [
            sys.executable,
            reviewer.as_posix(),
            "--images",
            *[image.as_posix() for image in images],
            "--model",
            args.model,
            "--out",
            args.out.as_posix(),
            "--context-file",
            args.context_out.as_posix(),
        ]
    )
    run(
        [
            sys.executable,
            todos.as_posix(),
            "--review",
            args.out.as_posix(),
            "--frames",
            (args.frames_dir / "frames_manifest.json").as_posix(),
            "--out",
            args.todos_out.as_posix(),
        ]
    )
    print(args.out)
    print(args.todos_out)


if __name__ == "__main__":
    main()
