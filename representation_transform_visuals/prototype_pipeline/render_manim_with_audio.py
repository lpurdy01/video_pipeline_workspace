from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "prototype_pipeline" / "out"
VIDEO_DIR = OUT / "manim_media" / "videos" / "new_transform_space"
MANIM_VIDEO_CANDIDATES = [
    VIDEO_DIR / "720p30" / "NewTransformSpacePrototype.mp4",
    VIDEO_DIR / "1080p60" / "NewTransformSpacePrototype.mp4",
    VIDEO_DIR / "480p15" / "NewTransformSpacePrototype.mp4",
]
NARRATION = OUT / "manim_scratch_narration.txt"
NARRATION_WAV = OUT / "manim_scratch_narration.wav"
FINAL = OUT / "new_transform_space_manim_with_scratch_audio.mp4"


TEXT = (
    "A transform moves a problem into a new space. "
    "Signals become spectra. Language becomes vectors. "
    "Then a learned transform acts on those vectors. "
    "Some structure survives, and some detail collapses into loss and assumptions."
)


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


def main() -> None:
    manim_video = next((path for path in MANIM_VIDEO_CANDIDATES if path.exists()), None)
    if manim_video is None:
        raise SystemExit("Missing Manim video. Run manim_prototypes/render_manim_prototype.sh first.")

    OUT.mkdir(parents=True, exist_ok=True)
    NARRATION.write_text(TEXT + "\n", encoding="utf-8")
    video_duration = duration(manim_video)

    run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"flite=textfile={NARRATION.as_posix()}:voice=slt",
            "-ar",
            "48000",
            NARRATION_WAV.as_posix(),
        ]
    )
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            manim_video.as_posix(),
            "-i",
            NARRATION_WAV.as_posix(),
            "-af",
            "apad",
            "-t",
            f"{video_duration:.3f}",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "128k",
            FINAL.as_posix(),
        ]
    )
    print(f"Final Manim prototype: {FINAL}")


if __name__ == "__main__":
    main()
