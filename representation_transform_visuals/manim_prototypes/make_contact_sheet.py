from __future__ import annotations

import argparse
import math
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def video_duration(path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=nk=1:nw=1",
            path.as_posix(),
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    return float(result.stdout.strip())


def extract_frame(video: Path, timestamp: float, out: Path) -> None:
    run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-ss",
            f"{timestamp:.3f}",
            "-i",
            video.as_posix(),
            "-frames:v",
            "1",
            out.as_posix(),
        ]
    )


def build_sheet(frames: list[tuple[float, Path]], out: Path, columns: int, thumb_width: int) -> None:
    loaded = [Image.open(path).convert("RGB") for _, path in frames]
    if not loaded:
        raise SystemExit("No frames extracted.")

    ratio = loaded[0].height / loaded[0].width
    thumb_height = int(thumb_width * ratio)
    label_height = 26
    rows = math.ceil(len(loaded) / columns)
    sheet = Image.new("RGB", (columns * thumb_width, rows * (thumb_height + label_height)), "#050711")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()

    for idx, ((timestamp, _), image) in enumerate(zip(frames, loaded)):
        col = idx % columns
        row = idx // columns
        x = col * thumb_width
        y = row * (thumb_height + label_height)
        resized = image.resize((thumb_width, thumb_height), Image.Resampling.LANCZOS)
        sheet.paste(resized, (x, y + label_height))
        draw.rectangle((x, y, x + thumb_width, y + label_height), fill="#0B1020")
        draw.text((x + 8, y + 7), f"{timestamp:05.2f}s", fill="#D6E6FF", font=font)

    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)


def parse_timestamps(raw: str | None, duration: float, every: float) -> list[float]:
    if raw:
        return [float(item.strip()) for item in raw.split(",") if item.strip()]
    count = int(duration // every) + 1
    times = [min(duration - 0.05, idx * every) for idx in range(count)]
    return [time for time in times if time >= 0]


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract review frames and build a labeled contact sheet.")
    parser.add_argument("video", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--timestamps", help="Comma-separated timestamps in seconds.")
    parser.add_argument("--every", type=float, default=1.0, help="Sampling interval when --timestamps is omitted.")
    parser.add_argument("--columns", type=int, default=3)
    parser.add_argument("--thumb-width", type=int, default=360)
    args = parser.parse_args()

    duration = video_duration(args.video)
    timestamps = parse_timestamps(args.timestamps, duration, args.every)
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        frames: list[tuple[float, Path]] = []
        for idx, timestamp in enumerate(timestamps):
            frame_path = tmpdir / f"frame_{idx:03d}.png"
            extract_frame(args.video, timestamp, frame_path)
            frames.append((timestamp, frame_path))
        build_sheet(frames, args.out, args.columns, args.thumb_width)


if __name__ == "__main__":
    main()
