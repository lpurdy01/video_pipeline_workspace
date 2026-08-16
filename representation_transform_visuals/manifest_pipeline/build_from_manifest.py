from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
OUT = ROOT / "manifest_pipeline" / "out"


@dataclass
class SectionBuild:
    section_id: str
    title: str
    audio_path: Path
    audio_source: str
    video_source_path: Path
    video_source: str
    clip_path: Path
    duration_seconds: float
    start_seconds: float
    end_seconds: float


def repo_path(path: str | Path) -> Path:
    path = Path(path)
    if path.is_absolute():
        return path
    return (REPO_ROOT / path).resolve()


def run(cmd: list[str]) -> None:
    print(" ".join(shlex.quote(part) for part in cmd))
    subprocess.run(cmd, check=True)


def media_duration(path: Path) -> float:
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


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(path.as_posix(), size=size)
    return ImageFont.load_default()


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    text: str,
    xy: tuple[int, int],
    font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
    fill: tuple[int, int, int],
    max_chars: int,
    line_gap: int = 8,
) -> int:
    x, y = xy
    for line in wrap(text, width=max_chars):
        draw.text((x, y), line, font=font, fill=fill)
        bbox = draw.textbbox((x, y), line, font=font)
        y += (bbox[3] - bbox[1]) + line_gap
    return y


def make_placeholder_still(section: dict, out: Path, width: int, height: int) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (width, height), (2, 3, 8))
    draw = ImageDraw.Draw(image)
    title_font = load_font(max(26, width // 28))
    small_font = load_font(max(15, width // 58))
    mono_font = load_font(max(13, width // 66))

    accent = (0, 230, 255)
    pink = (255, 55, 170)
    green = (115, 255, 164)
    dim = (135, 150, 170)
    white = (230, 238, 255)

    # Soft grid.
    for x in range(0, width, max(38, width // 22)):
        draw.line((x, 0, x, height), fill=(7, 12, 24), width=1)
    for y in range(0, height, max(34, height // 14)):
        draw.line((0, y, width, y), fill=(7, 12, 24), width=1)

    visual = section.get("visual", {})
    kind = visual.get("kind", "visual_placeholder")
    margin = max(32, width // 18)

    if kind == "talking_head_placeholder":
        box_w = int(width * 0.34)
        box_h = int(height * 0.58)
        box_x = margin
        box_y = int(height * 0.22)
        draw.rounded_rectangle(
            (box_x, box_y, box_x + box_w, box_y + box_h),
            radius=12,
            outline=accent,
            width=3,
            fill=(5, 9, 18),
        )
        draw.ellipse(
            (box_x + box_w * 0.38, box_y + box_h * 0.14, box_x + box_w * 0.62, box_y + box_h * 0.31),
            outline=white,
            width=3,
        )
        draw.line(
            (box_x + box_w * 0.5, box_y + box_h * 0.34, box_x + box_w * 0.5, box_y + box_h * 0.75),
            fill=white,
            width=3,
        )
        draw.rounded_rectangle(
            (box_x + box_w * 0.63, box_y + box_h * 0.48, box_x + box_w * 0.76, box_y + box_h * 0.66),
            radius=8,
            outline=pink,
            width=3,
        )
        draw.text((box_x, box_y - 34), "HUMAN CAMERA SEGMENT", font=mono_font, fill=green)
        text_x = box_x + box_w + margin
    else:
        cx = width // 2
        cy = height // 2
        radius = min(width, height) // 5
        for i, color in enumerate([accent, pink, green]):
            offset = (i - 1) * radius * 0.75
            draw.ellipse(
                (cx - radius + offset, cy - radius, cx + radius + offset, cy + radius),
                outline=color,
                width=3,
            )
        for i in range(9):
            x1 = int(cx - radius * 2.2 + i * radius * 0.55)
            y1 = int(cy + (i % 3 - 1) * radius * 0.45)
            draw.line((x1, y1, x1 + radius, y1 - radius * 0.35), fill=(55, 90, 125), width=2)
            draw.ellipse((x1 - 4, y1 - 4, x1 + 4, y1 + 4), fill=accent if i % 2 else pink)
        text_x = margin

    draw.text((text_x, margin), section["title"], font=title_font, fill=white)
    prompt = visual.get("prompt", "Placeholder visual.")
    draw_wrapped(draw, prompt, (text_x, margin + 58), small_font, dim, max_chars=44 if kind == "talking_head_placeholder" else 72)
    draw.text((margin, height - margin - 22), section["id"], font=mono_font, fill=(90, 110, 135))
    image.save(out)


def make_video_from_still(still: Path, out: Path, duration: float, width: int, height: int, fps: int) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "warning",
            "-y",
            "-loop",
            "1",
            "-i",
            still.as_posix(),
            "-t",
            f"{duration:.3f}",
            "-vf",
            f"scale={width}:{height},fps={fps}",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            out.as_posix(),
        ]
    )


def mux_video_audio(video: Path, audio: Path, out: Path, target_duration: float, width: int, height: int, fps: int) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    # Each manim scene is now rendered to match the section's audio duration
    # (via scene_durations.json), so we no longer loop the source. If the
    # render is still slightly short due to render rounding, tpad clones the
    # final frame to fill the gap instead of looping back to a fade-in.
    scale_filter = (
        f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
        f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,"
        f"tpad=stop_mode=clone:stop_duration={target_duration:.3f},"
        f"fps={fps}"
    )
    run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "warning",
            "-y",
            "-i",
            video.as_posix(),
            "-i",
            audio.as_posix(),
            "-t",
            f"{target_duration:.3f}",
            "-vf",
            scale_filter,
            "-c:v",
            "libx264",
            "-c:a",
            "aac",
            "-b:a",
            "128k",
            "-pix_fmt",
            "yuv420p",
            "-shortest",
            out.as_posix(),
        ]
    )


def concat_clips(clips: list[Path], out: Path, width: int, height: int, fps: int) -> None:
    concat_list = OUT / "concat_list.txt"
    concat_list.parent.mkdir(parents=True, exist_ok=True)
    concat_list.write_text(
        "".join(f"file '{clip.resolve().as_posix()}'\n" for clip in clips),
        encoding="utf-8",
    )
    run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "warning",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            concat_list.as_posix(),
            "-vf",
            f"scale={width}:{height},fps={fps},format=yuv420p",
            "-c:v",
            "libx264",
            "-c:a",
            "aac",
            "-b:a",
            "128k",
            "-pix_fmt",
            "yuv420p",
            out.as_posix(),
        ]
    )


def generate_scratch_tts(text_path: Path, out_path: Path, model: str, voice: str, style: str) -> None:
    sys.path.insert(0, (ROOT / "narration_pipeline").as_posix())
    from gemini_tts import DEFAULT_MODEL, DEFAULT_VOICE, extract_audio_bytes, write_wav
    from google import genai
    from google.genai import types

    sys.path.insert(0, str(REPO_ROOT))
    from workspace_credentials import require

    api_key = require("GEMINI_API_KEY")

    text = text_path.read_text(encoding="utf-8")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model or DEFAULT_MODEL,
        contents=f"{style}\n\n{text}",
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=voice or DEFAULT_VOICE)
                )
            ),
        ),
    )
    write_wav(out_path, extract_audio_bytes(response))


def choose_audio(section: dict, defaults: dict, text_path: Path, generate_tts: bool) -> tuple[Path, str]:
    audio = section["audio"]
    human_path = repo_path(audio["human_path"])
    scratch_path = repo_path(audio["scratch_path"])
    if human_path.exists():
        return human_path, "human"
    if not scratch_path.exists():
        if not generate_tts:
            raise RuntimeError(f"Missing scratch audio and --no-generate-tts was used: {scratch_path}")
        print(f"Generating scratch TTS for {section['id']}")
        generate_scratch_tts(
            text_path,
            scratch_path,
            defaults.get("scratch_tts_model", ""),
            defaults.get("scratch_tts_voice", ""),
            defaults.get("scratch_tts_style", ""),
        )
    return scratch_path, "scratch_tts"


def choose_video(section: dict, duration: float, width: int, height: int, fps: int) -> tuple[Path, str]:
    visual = section.get("visual", {})
    kind = visual.get("kind", "visual_placeholder")

    if kind == "talking_head_placeholder":
        human_video = repo_path(visual.get("human_video_path", ""))
        if human_video.exists():
            return human_video, "human_video"

    if kind == "existing_video":
        path = repo_path(visual.get("path", ""))
        if path.exists():
            return path, "existing_video"

    still = OUT / "stills" / f"{section['id']}.png"
    placeholder = OUT / "video_sources" / f"{section['id']}_placeholder.mp4"
    make_placeholder_still(section, still, width, height)
    make_video_from_still(still, placeholder, duration, width, height, fps)
    return placeholder, "placeholder"


def write_script_chunks(manifest: dict) -> dict[str, Path]:
    script_dir = OUT / "script_chunks"
    script_dir.mkdir(parents=True, exist_ok=True)
    paths: dict[str, Path] = {}
    for section in manifest["sections"]:
        path = script_dir / f"{section['id']}.txt"
        path.write_text(section["narration_text"].strip() + "\n", encoding="utf-8")
        paths[section["id"]] = path
    return paths


def write_asset_checklist(manifest: dict, builds: list[SectionBuild], out: Path) -> None:
    by_id = {build.section_id: build for build in builds}
    lines: list[str] = [
        "# Human Asset Checklist",
        "",
        f"Manifest: `{ROOT / 'production_manifest.json'}`",
        f"Prototype video: `{OUT / 'complete_prototype.mp4'}`",
        "",
        "Use this as the recording and asset punch list. The build uses human files when present and scratch placeholders otherwise.",
        "",
    ]
    for section in manifest["sections"]:
        build = by_id[section["id"]]
        lines.extend(
            [
                f"## {section['id']} - {section['title']}",
                "",
                f"- Current audio source: `{build.audio_source}`",
                f"- Current visual source: `{build.video_source}`",
                f"- Duration: `{build.duration_seconds:.2f}s`",
                "",
                "Narration chunk:",
                "",
                "```text",
                section["narration_text"].strip(),
                "```",
                "",
                "Needed human assets:",
            ]
        )
        for asset in section.get("human_assets", []):
            path = repo_path(asset["path"])
            status = "present" if path.exists() else "missing"
            lines.append(f"- [{status}] `{asset['kind']}`: `{asset['path']}`")
            lines.append(f"  Prompt: {asset.get('prompt', '').strip()}")
        lines.append("")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")


def build(manifest_path: Path, generate_tts: bool) -> list[SectionBuild]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    defaults = manifest.get("prototype_defaults", {})
    width = int(defaults.get("width", 854))
    height = int(defaults.get("height", 480))
    fps = int(defaults.get("fps", 24))
    script_paths = write_script_chunks(manifest)

    builds: list[SectionBuild] = []
    cursor = 0.0
    for section in manifest["sections"]:
        text_path = script_paths[section["id"]]
        audio_path, audio_source = choose_audio(section, defaults, text_path, generate_tts)
        duration = media_duration(audio_path)
        start = cursor
        end = start + duration
        video_path, video_source = choose_video(section, duration, width, height, fps)
        clip_path = OUT / "section_clips" / f"{section['id']}.mp4"
        mux_video_audio(video_path, audio_path, clip_path, duration, width, height, fps)
        builds.append(
            SectionBuild(
                section_id=section["id"],
                title=section["title"],
                audio_path=audio_path,
                audio_source=audio_source,
                video_source_path=video_path,
                video_source=video_source,
                clip_path=clip_path,
                duration_seconds=duration,
                start_seconds=start,
                end_seconds=end,
            )
        )
        cursor = end

    final_video = OUT / "complete_prototype.mp4"
    concat_clips([build.clip_path for build in builds], final_video, width, height, fps)
    write_asset_checklist(manifest, builds, OUT / "human_asset_checklist.md")
    resolved = {
        "manifest": manifest_path.as_posix(),
        "final_video": final_video.as_posix(),
        "sections": [
            {
                "id": build.section_id,
                "title": build.title,
                "duration_seconds": build.duration_seconds,
                "start_seconds": build.start_seconds,
                "end_seconds": build.end_seconds,
                "audio_source": build.audio_source,
                "audio_path": build.audio_path.as_posix(),
                "video_source": build.video_source,
                "video_source_path": build.video_source_path.as_posix(),
                "clip_path": build.clip_path.as_posix(),
            }
            for build in builds
        ],
    }
    (OUT / "resolved_manifest.json").write_text(json.dumps(resolved, indent=2), encoding="utf-8")
    return builds


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a modular prototype video from production_manifest.json.")
    parser.add_argument("--manifest", type=Path, default=ROOT / "production_manifest.json")
    parser.add_argument("--no-generate-tts", action="store_true", help="Require audio files to already exist.")
    args = parser.parse_args()

    builds = build(args.manifest.resolve(), generate_tts=not args.no_generate_tts)
    print("")
    print(f"Built {len(builds)} sections")
    print(OUT / "complete_prototype.mp4")
    print(OUT / "human_asset_checklist.md")


if __name__ == "__main__":
    main()
