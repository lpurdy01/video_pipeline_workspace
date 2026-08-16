from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCES = ROOT / "source_videos.json"
DEFAULT_OUT = ROOT / "assets" / "reference_frames" / "youtube_sources"
WORK = ROOT / "source_frame_pipeline" / "out" / "downloads"


def run(cmd: list[str]) -> None:
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)


def require_tool(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise SystemExit(
            f"Missing required tool: {name}. Install it, then rerun this script. "
            "For yt-dlp: python3 -m pip install --user yt-dlp"
        )
    return path


def load_sources(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("videos", [])


def download_video(video: dict, force: bool) -> Path:
    require_tool("yt-dlp")
    WORK.mkdir(parents=True, exist_ok=True)
    out_template = WORK / f"{video['id']}.%(ext)s"
    expected = WORK / f"{video['id']}.mp4"
    if expected.exists() and not force:
        return expected
    run(
        [
            "yt-dlp",
            "--no-playlist",
            "-f",
            "bv*[height<=720][ext=mp4]+ba[ext=m4a]/b[height<=720][ext=mp4]/best[height<=720]",
            "--merge-output-format",
            "mp4",
            "-o",
            out_template.as_posix(),
            video["url"],
        ]
    )
    if not expected.exists():
        matches = sorted(WORK.glob(f"{video['id']}.*"))
        if not matches:
            raise FileNotFoundError(f"yt-dlp did not create a download for {video['id']}")
        return matches[0]
    return expected


def capture_at(video_path: Path, out_path: Path, timestamp: str) -> None:
    require_tool("ffmpeg")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-ss",
            timestamp,
            "-i",
            video_path.as_posix(),
            "-frames:v",
            "1",
            "-update",
            "1",
            out_path.as_posix(),
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Capture internal reference frames from approved YouTube source videos.")
    parser.add_argument("--sources", type=Path, default=DEFAULT_SOURCES)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--timestamps", nargs="*", default=["00:00:08", "00:00:20", "00:00:40"])
    parser.add_argument("--video-id", help="Only process one source_videos.json id.")
    parser.add_argument("--force-download", action="store_true")
    args = parser.parse_args()

    sources = load_sources(args.sources)
    if args.video_id:
        sources = [video for video in sources if video["id"] == args.video_id]
    if not sources:
        raise SystemExit("No matching source videos found.")

    manifest_path = args.out_dir / "frames_manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    else:
        manifest = []
    for video in sources:
        video_path = download_video(video, args.force_download)
        for timestamp in args.timestamps:
            safe_time = timestamp.replace(":", "-")
            out_path = args.out_dir / video["id"] / f"{safe_time}.png"
            capture_at(video_path, out_path, timestamp)
            record = {
                "source_id": video["id"],
                "url": video["url"],
                "focus": video.get("focus", ""),
                "timestamp": timestamp,
                "path": out_path.as_posix(),
            }
            manifest = [item for item in manifest if item.get("path") != record["path"]]
            manifest.append(record)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    manifest.sort(key=lambda item: (item.get("source_id", ""), item.get("timestamp", "")))
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(manifest_path)


if __name__ == "__main__":
    main()
