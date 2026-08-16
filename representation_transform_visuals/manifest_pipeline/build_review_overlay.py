"""Add a section-ID + timestamp overlay to complete_prototype.mp4 so the
prototype can be reviewed clip-by-clip.

Top-left corner of every frame shows:
    SS  <section_id>          — current section number + slug
    elapsed HH:MM:SS.ms        — absolute time in the prototype

Time-gated `drawtext` filters switch the section label at each cut. The
output goes to `complete_prototype_review.mp4` next to the original.
"""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "manifest_pipeline" / "out"


def find_font() -> str:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for c in candidates:
        if Path(c).exists():
            return c
    raise SystemExit("No DejaVu font found — install fonts-dejavu.")


def drawtext_escape(text: str) -> str:
    """Escape characters that have special meaning inside drawtext text=..."""
    # Backslash first
    text = text.replace("\\", "\\\\")
    text = text.replace(":", r"\:")
    text = text.replace("'", r"\'")
    text = text.replace("%", r"\%")
    return text


def build_filter(sections: list[dict], font: str) -> str:
    parts: list[str] = [
        # Translucent dark band so the overlay reads on any background.
        "drawbox=x=10:y=8:w=520:h=70:color=black@0.55:t=fill",
    ]

    # Per-section section-id labels (time-gated so only the current one shows)
    for i, s in enumerate(sections, start=1):
        start = s["start_seconds"]
        end = s["end_seconds"]
        section_id = s["id"]
        label = f"{i:02d}  {section_id}"
        text = drawtext_escape(label)
        parts.append(
            "drawtext="
            f"fontfile='{font}':"
            f"text='{text}':"
            "x=22:y=16:"
            "fontsize=22:"
            "fontcolor=white@0.96:"
            f"enable='between(t,{start:.3f},{end:.3f})'"
        )

    # Absolute elapsed timestamp (always visible). %{pts\:hms} produces
    # HH:MM:SS.mmm. The user can scrub to that time in their player.
    parts.append(
        "drawtext="
        f"fontfile='{font}':"
        "text='elapsed  %{pts\\:hms}':"
        "x=22:y=46:"
        "fontsize=18:"
        "fontcolor=#FFD56A"
    )

    return ",".join(parts)


def run(cmd: list[str]) -> None:
    print(" ".join(shlex.quote(part) for part in cmd))
    subprocess.run(cmd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", type=Path, default=OUT / "complete_prototype.mp4")
    parser.add_argument("--manifest", type=Path, default=OUT / "resolved_manifest.json")
    parser.add_argument("--out", type=Path, default=OUT / "complete_prototype_review.mp4")
    args = parser.parse_args()

    sections = json.loads(args.manifest.read_text(encoding="utf-8"))["sections"]
    font = find_font()
    vf = build_filter(sections, font)

    run([
        "ffmpeg",
        "-hide_banner",
        "-loglevel", "warning",
        "-y",
        "-i", args.video.as_posix(),
        "-vf", vf,
        "-c:v", "libx264",
        "-c:a", "copy",
        "-pix_fmt", "yuv420p",
        args.out.as_posix(),
    ])
    print(args.out)


if __name__ == "__main__":
    main()
