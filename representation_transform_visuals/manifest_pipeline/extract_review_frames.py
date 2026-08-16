from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "manifest_pipeline" / "out"


def run(cmd: list[str]) -> None:
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def cue_timestamp(cue: str | int | float, start: float, end: float) -> float:
    duration = max(0.01, end - start)
    if isinstance(cue, (int, float)):
        return clamp(start + float(cue), start + 0.25, end - 0.25)

    normalized = str(cue).strip().lower()
    if normalized == "start":
        # Most Manim sections open with a short fade from black. Sample after
        # the first visual beat has landed so automated review judges the
        # scene composition instead of a transition frame.
        return clamp(start + min(3.0, duration * 0.15), start + 0.1, end - 0.1)
    if normalized == "middle":
        return start + duration * 0.5
    if normalized == "end":
        return clamp(end - min(1.0, duration * 0.15), start + 0.1, end - 0.1)
    if normalized.endswith("%"):
        percent = float(normalized[:-1]) / 100.0
        return clamp(start + duration * percent, start + 0.1, end - 0.1)
    return clamp(start + float(normalized), start + 0.25, end - 0.25)


def extract_frame(video: Path, timestamp: float, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-ss",
            f"{timestamp:.3f}",
            "-i",
            video.as_posix(),
            "-frames:v",
            "1",
            "-update",
            "1",
            out.as_posix(),
        ]
    )


def build_frame_plan(manifest: dict, resolved: dict, dense_interval: float = 0.0) -> list[dict]:
    """Build the list of (section, timestamp) frames to extract.

    - For each manifest section, always emit the explicit cues (start/middle/end
      or numeric offsets) from `review_keyframes`.
    - If `dense_interval > 0`, ALSO emit one frame every `dense_interval`
      seconds within the section. These catch mid-animation overlap problems
      that start/middle/end miss.
    """
    sections_by_id = {section["id"]: section for section in resolved["sections"]}
    frames: list[dict] = []
    for section in manifest["sections"]:
        resolved_section = sections_by_id[section["id"]]
        start_s = resolved_section["start_seconds"]
        end_s = resolved_section["end_seconds"]
        seen: list[float] = []

        def _add(cue, timestamp: float) -> None:
            # De-duplicate near-identical timestamps (cues + interval often
            # land on the same frame).
            for existing in seen:
                if abs(existing - timestamp) < 0.6:
                    return
            seen.append(timestamp)
            frames.append({
                "section_id": section["id"],
                "title": section["title"],
                "cue": cue,
                "timestamp_seconds": timestamp,
                "section_start": start_s,
                "section_end": end_s,
            })

        cues = section.get("review_keyframes") or ["middle"]
        for cue in cues:
            _add(cue, cue_timestamp(cue, start_s, end_s))

        if dense_interval > 0:
            t = start_s + dense_interval * 0.6  # nudge past the section fade-in
            n = 0
            while t < end_s - 0.5:
                n += 1
                _add(f"dense_{n}", t)
                t += dense_interval
    return frames


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract manifest-defined keyframes from a complete prototype video.")
    parser.add_argument("--manifest", type=Path, default=ROOT / "production_manifest.json")
    parser.add_argument("--resolved", type=Path, default=OUT / "resolved_manifest.json")
    parser.add_argument("--video", type=Path, default=OUT / "complete_prototype.mp4")
    parser.add_argument("--out-dir", type=Path, default=OUT / "review_frames")
    parser.add_argument(
        "--dense", type=float, default=0.0,
        help="If >0, additionally sample one frame every N seconds within each section "
             "(in addition to manifest cues). Catches mid-animation issues.",
    )
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    resolved = json.loads(args.resolved.read_text(encoding="utf-8"))
    frames = build_frame_plan(manifest, resolved, dense_interval=args.dense)

    output_records = []
    for idx, frame in enumerate(frames, start=1):
        safe_cue = str(frame["cue"]).replace("%", "pct").replace(".", "_")
        out = args.out_dir / f"{idx:02d}_{frame['section_id']}_{safe_cue}.png"
        extract_frame(args.video, frame["timestamp_seconds"], out)
        output_records.append({**frame, "path": out.as_posix()})

    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "frames_manifest.json").write_text(json.dumps(output_records, indent=2), encoding="utf-8")
    print(args.out_dir)
    print(args.out_dir / "frames_manifest.json")


if __name__ == "__main__":
    main()
