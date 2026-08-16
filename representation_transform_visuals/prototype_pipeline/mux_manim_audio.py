from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "prototype_pipeline" / "out"
VIDEO_DIR = OUT / "manim_media" / "videos" / "new_transform_space"
VIDEO_CANDIDATES = [
    VIDEO_DIR / "720p30" / "NewTransformSpacePrototype.mp4",
    VIDEO_DIR / "1080p60" / "NewTransformSpacePrototype.mp4",
    VIDEO_DIR / "480p15" / "NewTransformSpacePrototype.mp4",
]


def run(cmd: list[str]) -> None:
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)


def duration(path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            path.as_posix(),
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    return float(result.stdout.strip())


def default_video() -> Path:
    for candidate in VIDEO_CANDIDATES:
        if candidate.exists():
            return candidate
    raise SystemExit("Missing Manim video. Run manim_prototypes/render_manim_prototype.sh first.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Mux Manim prototype video with narration audio.")
    parser.add_argument("--video", type=Path, default=None)
    parser.add_argument("--audio", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--duration", choices=["video", "audio", "longest"], default="longest")
    args = parser.parse_args()

    video = args.video or default_video()
    if not args.audio.exists():
        raise SystemExit(f"Missing audio: {args.audio}")

    video_duration = duration(video)
    audio_duration = duration(args.audio)
    if args.duration == "video":
        target_duration = video_duration
    elif args.duration == "audio":
        target_duration = audio_duration
    else:
        target_duration = max(video_duration, audio_duration)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    run(
        [
            "ffmpeg",
            "-y",
            "-stream_loop",
            "-1",
            "-i",
            video.as_posix(),
            "-i",
            args.audio.as_posix(),
            "-af",
            "apad",
            "-t",
            f"{target_duration:.3f}",
            "-c:v",
            "libx264",
            "-c:a",
            "aac",
            "-b:a",
            "128k",
            "-pix_fmt",
            "yuv420p",
            args.out.as_posix(),
        ]
    )
    print(args.out)


if __name__ == "__main__":
    main()

