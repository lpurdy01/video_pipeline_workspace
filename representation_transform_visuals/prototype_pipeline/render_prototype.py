from __future__ import annotations

import math
import argparse
import shutil
import subprocess
import textwrap
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "prototype_pipeline" / "out"
FRAMES = OUT / "frames"

WIDTH = 1280
HEIGHT = 720
FPS = 24

BG = (0, 2, 10)
PANEL = (5, 8, 18)
PANEL_2 = (9, 13, 28)
TEXT = (244, 247, 255)
MUTED = (135, 145, 168)
TEAL = (32, 247, 210)
GOLD = (255, 203, 77)
BLUE = (77, 141, 255)
RED = (255, 77, 109)
GREEN = (73, 242, 141)
PURPLE = (180, 92, 255)


@dataclass(frozen=True)
class Scene:
    name: str
    duration: float
    narration: str


SCENES = [
    Scene(
        "transform_lens",
        8.0,
        "Every so often, a new transform changes what civilization can build. "
        "It moves a problem into a space where different operations become possible.",
    ),
    Scene(
        "technology_tree",
        8.0,
        "Fourier, Laplace, compression, and linear algebra are not just math tricks. "
        "They become branches of the technology tree.",
    ),
    Scene(
        "language_vectors",
        9.0,
        "Modern AI makes language part of this pattern. Tokens become vectors, "
        "and relationships between concepts become computational objects.",
    ),
    Scene(
        "pseudocode_to_code",
        10.0,
        "The practical example is pseudocode to code. A vague human intent becomes "
        "software, but missing details become assumptions.",
    ),
    Scene(
        "semantic_loss",
        11.0,
        "That is semantic transform loss. The output can be useful without perfectly "
        "preserving the original intent. The technology tree changes around that tradeoff.",
    ),
]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()


FONT_H1 = font(54, bold=True)
FONT_H2 = font(34, bold=True)
FONT_BODY = font(28)
FONT_SMALL = font(21)
FONT_TINY = font(17)
FONT_CODE = font(23)


def ease(x: float) -> float:
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def lerp(a: float, b: float, x: float) -> float:
    return a + (b - a) * x


def draw_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    fill=TEXT,
    font_obj=FONT_BODY,
    max_width: int | None = None,
    line_spacing: int = 8,
) -> int:
    x, y = xy
    lines: list[str] = []
    if max_width is None:
        lines = text.splitlines()
    else:
        for paragraph in text.splitlines():
            if not paragraph:
                lines.append("")
                continue
            words = paragraph.split()
            current: list[str] = []
            for word in words:
                trial = " ".join([*current, word])
                if draw.textbbox((0, 0), trial, font=font_obj)[2] <= max_width or not current:
                    current.append(word)
                else:
                    lines.append(" ".join(current))
                    current = [word]
            if current:
                lines.append(" ".join(current))

    for line in lines:
        draw.text((x, y), line, fill=fill, font=font_obj)
        bbox = draw.textbbox((x, y), line or " ", font=font_obj)
        y += bbox[3] - bbox[1] + line_spacing
    return y


def rounded(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill=PANEL, outline=None, width=2, radius=10) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], fill=TEXT, width=4) -> None:
    draw.line([start, end], fill=fill, width=width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    length = 18
    spread = 0.45
    p1 = (
        int(end[0] - length * math.cos(angle - spread)),
        int(end[1] - length * math.sin(angle - spread)),
    )
    p2 = (
        int(end[0] - length * math.cos(angle + spread)),
        int(end[1] - length * math.sin(angle + spread)),
    )
    draw.polygon([end, p1, p2], fill=fill)


def draw_wave(draw: ImageDraw.ImageDraw, x0: int, y0: int, w: int, h: int, color=TEAL, phase=0.0) -> None:
    pts = []
    for i in range(w):
        x = x0 + i
        amp = h * 0.28 * (0.65 + 0.35 * math.sin(i / 52))
        y = y0 + h / 2 + amp * math.sin(i / 18 + phase) + h * 0.1 * math.sin(i / 7 + phase * 0.4)
        pts.append((x, int(y)))
    draw.line(pts, fill=color, width=4)


def base_frame(title: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    for x in range(0, WIDTH, 64):
        draw.line((x, 0, x, HEIGHT), fill=(8, 13, 28), width=1)
    for y in range(0, HEIGHT, 64):
        draw.line((0, y, WIDTH, y), fill=(8, 13, 28), width=1)
    draw.text((46, 28), title, fill=(170, 180, 205), font=FONT_SMALL)
    return img, draw


def scene_transform_lens(t: float, duration: float) -> Image.Image:
    img, draw = base_frame("A transform moves the problem")
    labels = ["time signal", "dynamics", "pixels"]
    colors = [TEAL, GOLD, BLUE]
    y_positions = [190, 350, 510]
    progress = ease(t / duration)

    for idx, y in enumerate(y_positions):
        x_left = 80
        x_mid = 555
        x_right = 860
        rounded(draw, (x_left, y - 54, x_left + 280, y + 54), fill=PANEL, outline=colors[idx])
        draw.text((x_left + 24, y - 18), labels[idx], fill=TEXT, font=FONT_BODY)
        arrow(draw, (x_left + 300, y), (x_mid - 28, y), fill=MUTED)
        rounded(draw, (x_mid, y - 64, x_mid + 190, y + 64), fill=(28, 34, 52), outline=PURPLE)
        draw.text((x_mid + 38, y - 16), "transform", fill=PURPLE, font=FONT_SMALL)
        arrow(draw, (x_mid + 205, y), (x_right - 35, y), fill=MUTED)
        rounded(draw, (x_right, y - 54, x_right + 330, y + 54), fill=PANEL, outline=colors[idx])

        if idx == 0:
            draw_wave(draw, x_right + 22, y - 32, 200, 64, color=colors[idx], phase=t * 3)
            for k in range(6):
                bar_h = int((20 + 38 * abs(math.sin(k * 0.7 + progress * 2))) * progress)
                draw.rectangle((x_right + 240 + k * 13, y + 32 - bar_h, x_right + 248 + k * 13, y + 32), fill=colors[idx])
        elif idx == 1:
            draw.text((x_right + 26, y - 20), "algebraic\ncontrol law", fill=TEXT, font=FONT_SMALL, spacing=6)
        else:
            for row in range(4):
                for col in range(6):
                    shade = int(50 + 120 * abs(math.sin(row * 1.7 + col * 0.8 + t)))
                    draw.rectangle((x_right + 28 + col * 26, y - 38 + row * 20, x_right + 49 + col * 26, y - 22 + row * 20), fill=(shade, shade, min(255, shade + 35)))
            draw.text((x_right + 215, y - 13), "compressed", fill=TEXT, font=FONT_SMALL)

    draw_text(draw, (80, 630), "representation in -> transform space -> computation -> representation out", fill=MUTED, font_obj=FONT_SMALL)
    return img


def scene_technology_tree(t: float, duration: float) -> Image.Image:
    img, draw = base_frame("Transforms become technology trees")
    trunk_x = 640
    root_y = 610
    top_y = 150
    draw.line((trunk_x, root_y, trunk_x, top_y), fill=GOLD, width=12)
    draw.text((455, 628), "representation transforms", fill=GOLD, font=FONT_BODY)

    branches = [
        ("Fourier", "radio | audio | MRI", -360, 230, TEAL),
        ("Laplace", "controls | circuits | robotics", 290, 250, BLUE),
        ("DCT", "JPEG | video | streaming", -300, 390, GREEN),
        ("Linear algebra", "PCA | search | recommendations", 250, 430, PURPLE),
    ]
    reveal = ease(t / duration)
    for i, (name, details, dx, y, color) in enumerate(branches):
        local = ease((reveal - i * 0.13) / 0.45)
        end = (int(lerp(trunk_x, trunk_x + dx, local)), int(lerp(y + 80, y, local)))
        start = (trunk_x, y + 80)
        draw.line((start, end), fill=color, width=7)
        if local > 0.7:
            tx = end[0] - 165 if dx < 0 else end[0] + 18
            rounded(draw, (tx, end[1] - 42, tx + 290, end[1] + 58), fill=PANEL_2, outline=color)
            draw.text((tx + 18, end[1] - 30), name, fill=color, font=FONT_SMALL)
            draw.text((tx + 18, end[1] + 2), details, fill=TEXT, font=FONT_TINY)

    draw_text(draw, (74, 112), "A transform is a way of making a different kind of work easy.", fill=MUTED, font_obj=FONT_SMALL, max_width=520)
    return img


def scene_language_vectors(t: float, duration: float) -> Image.Image:
    img, draw = base_frame("Language enters vector space")
    sentence = "build an API that checks subscription status"
    tokens = sentence.split()
    y = 170
    x = 72
    for i, token in enumerate(tokens):
        local = ease((t / duration - i * 0.06) / 0.25)
        if local <= 0:
            continue
        tw = draw.textbbox((0, 0), token, font=FONT_SMALL)[2] + 28
        rounded(draw, (x, y, x + tw, y + 52), fill=PANEL, outline=TEAL)
        draw.text((x + 14, y + 13), token, fill=TEXT, font=FONT_SMALL)
        x += tw + 12

    arrow(draw, (600, 250), (600, 330), fill=MUTED)
    draw.text((536, 280), "tokens", fill=MUTED, font=FONT_TINY)

    cx, cy = 640, 475
    rng = np.random.default_rng(42)
    points = rng.normal(size=(80, 2))
    scale = np.array([185, 105])
    reveal = ease((t - 2.2) / (duration - 2.2))
    for i, p in enumerate(points):
        if i / len(points) > reveal:
            continue
        px, py = (np.array([cx, cy]) + p * scale).astype(int)
        color = [TEAL, BLUE, GOLD, PURPLE][i % 4]
        r = 3 + (i % 3)
        draw.ellipse((px - r, py - r, px + r, py + r), fill=color)
    draw.ellipse((cx - 230, cy - 135, cx + 230, cy + 135), outline=(70, 84, 120), width=2)
    draw.text((462, 622), "learned high-dimensional space, projected for us", fill=MUTED, font=FONT_SMALL)

    draw_text(draw, (860, 328), "relationships become\ncomputational objects", fill=TEXT, font_obj=FONT_BODY)
    return img


def scene_pseudocode_to_code(t: float, duration: float) -> Image.Image:
    img, draw = base_frame("Pseudocode to code is a transform")
    prompt_box = (70, 150, 465, 490)
    code_box = (805, 150, 1210, 520)
    rounded(draw, prompt_box, fill=PANEL, outline=TEAL)
    rounded(draw, code_box, fill=PANEL, outline=BLUE)
    draw.text((95, 176), "compressed intent", fill=TEAL, font=FONT_SMALL)
    prompt = "Build an API endpoint that checks whether a user has an active subscription and returns a usage limit."
    draw_text(draw, (95, 230), prompt, fill=TEXT, font_obj=FONT_BODY, max_width=330)

    arrow(draw, (485, 318), (780, 318), fill=MUTED, width=5)
    rounded(draw, (532, 246, 735, 392), fill=(28, 34, 52), outline=PURPLE)
    draw.text((560, 282), "model\nspace", fill=PURPLE, font=FONT_BODY, spacing=8)

    code = [
        "async def usage_limit(user_id):",
        "    user = await db.users.get(user_id)",
        "    if not user:",
        "        raise NotFound()",
        "    if user.subscription.active:",
        "        return user.plan.limit",
        "    return FREE_LIMIT",
    ]
    draw.text((832, 176), "formal artifact", fill=BLUE, font=FONT_SMALL)
    reveal_lines = int(lerp(0, len(code), ease((t - 2.0) / 5.0)))
    for i, line in enumerate(code[:reveal_lines]):
        draw.text((832, 228 + i * 34), line, fill=TEXT if i % 2 else (210, 226, 255), font=FONT_CODE)

    if t > duration * 0.58:
        assumptions = ["framework?", "schema?", "error behavior?", "what is active?"]
        positions = [(520, 430), (665, 492), (650, 182), (980, 560)]
        for i, label in enumerate(assumptions):
            local = ease((t - duration * 0.58 - i * 0.35) / 1.2)
            if local <= 0:
                continue
            x, y = positions[i]
            rounded(draw, (x, y, x + 168, y + 44), fill=(58, 36, 38), outline=RED)
            draw.text((x + 13, y + 11), label, fill=TEXT, font=FONT_TINY)

    draw_text(draw, (80, 600), "The output can run, but unstated details have been chosen somewhere.", fill=MUTED, font_obj=FONT_SMALL)
    return img


def scene_semantic_loss(t: float, duration: float) -> Image.Image:
    img, draw = base_frame("Semantic transform loss")
    panels = [
        (72, 158, 382, 460, "JPEG", "detail is discarded"),
        (486, 158, 796, 460, "Laplace", "assumptions matter"),
        (900, 158, 1210, 460, "LLM", "gaps become assumptions"),
    ]
    colors = [GREEN, GOLD, RED]
    for i, (x1, y1, x2, y2, title, subtitle) in enumerate(panels):
        local = ease((t / duration - i * 0.14) / 0.38)
        if local <= 0:
            continue
        rounded(draw, (x1, y1, x2, y2), fill=PANEL, outline=colors[i])
        draw.text((x1 + 24, y1 + 24), title, fill=colors[i], font=FONT_BODY)
        if title == "JPEG":
            for row in range(6):
                for col in range(6):
                    c = int(55 + 155 * ((row + col) % 2) * 0.4 + 45 * math.sin(row + t))
                    draw.rectangle((x1 + 52 + col * 34, y1 + 100 + row * 25, x1 + 82 + col * 34, y1 + 122 + row * 25), fill=(c, c, min(255, c + 20)))
        elif title == "Laplace":
            draw.line((x1 + 65, y1 + 245, x2 - 65, y1 + 245), fill=MUTED, width=3)
            draw.line((x1 + 85, y1 + 275, x1 + 85, y1 + 115), fill=MUTED, width=3)
            draw.arc((x1 + 105, y1 + 150, x2 - 80, y1 + 280), 180, 345, fill=colors[i], width=5)
            draw.text((x1 + 65, y1 + 112), "model", fill=TEXT, font=FONT_SMALL)
        else:
            draw_text(draw, (x1 + 35, y1 + 112), "intent:\nmake it robust", fill=TEXT, font_obj=FONT_SMALL)
            arrow(draw, (x1 + 90, y1 + 222), (x2 - 80, y1 + 222), fill=MUTED)
            draw.text((x1 + 35, y1 + 240), "gaps -> assumptions", fill=MUTED, font=FONT_SMALL)
            draw.text((x1 + 35, y1 + 278), "plausible defaults", fill=TEXT, font=FONT_TINY)
        if title != "LLM":
            draw.text((x1 + 24, y2 - 60), subtitle, fill=MUTED, font=FONT_SMALL)

    draw.text((378, 520), "useful does not mean lossless", fill=TEXT, font=FONT_H2)
    terms = ["semantic compression", "semantic drift", "context degradation", "confabulation"]
    for i, term in enumerate(terms):
        x = 125 + i * 285
        rounded(draw, (x, 606, x + 238, 650), fill=PANEL_2, outline=PURPLE)
        draw.text((x + 16, 618), term, fill=TEXT, font=FONT_TINY)
    return img


SCENE_RENDERERS = {
    "transform_lens": scene_transform_lens,
    "technology_tree": scene_technology_tree,
    "language_vectors": scene_language_vectors,
    "pseudocode_to_code": scene_pseudocode_to_code,
    "semantic_loss": scene_semantic_loss,
}


def write_narration_text() -> Path:
    narration = " ".join(scene.narration for scene in SCENES)
    wrapped = "\n".join(textwrap.wrap(narration, width=88))
    path = OUT / "scratch_narration.txt"
    path.write_text(wrapped + "\n", encoding="utf-8")
    return path


def render_frames() -> int:
    if FRAMES.exists():
        shutil.rmtree(FRAMES)
    FRAMES.mkdir(parents=True, exist_ok=True)

    frame_index = 0
    for scene in SCENES:
        print(f"Rendering scene: {scene.name}")
        renderer = SCENE_RENDERERS[scene.name]
        total = int(scene.duration * FPS)
        for local_frame in range(total):
            t = local_frame / FPS
            img = renderer(t, scene.duration)
            img.save(FRAMES / f"frame_{frame_index:05d}.png")
            frame_index += 1
    return frame_index


def run(cmd: list[str]) -> None:
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)


def synthesize_audio(text_path: Path) -> Path:
    audio_path = OUT / "scratch_narration.wav"
    run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"flite=textfile={text_path.as_posix()}:voice=slt",
            "-ar",
            "48000",
            audio_path.as_posix(),
        ]
    )
    return audio_path


def build_video(frame_count: int, audio_path: Path) -> Path:
    visuals = OUT / "prototype_visuals.mp4"
    final = OUT / "representation_transform_pipeline_prototype.mp4"
    run(
        [
            "ffmpeg",
            "-y",
            "-framerate",
            str(FPS),
            "-i",
            (FRAMES / "frame_%05d.png").as_posix(),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-r",
            str(FPS),
            visuals.as_posix(),
        ]
    )
    run(
        [
            "ffmpeg",
            "-y",
            "-stream_loop",
            "-1",
            "-i",
            visuals.as_posix(),
            "-i",
            audio_path.as_posix(),
            "-af",
            "apad",
            "-t",
            str(frame_count / FPS),
            "-c:v",
            "libx264",
            "-c:a",
            "aac",
            "-b:a",
            "128k",
            "-pix_fmt",
            "yuv420p",
            final.as_posix(),
        ]
    )
    return final


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="Regenerate frames even if cached frames exist.")
    args = parser.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    text_path = write_narration_text()
    print(f"Wrote narration text: {text_path}")
    existing_frames = sorted(FRAMES.glob("frame_*.png")) if FRAMES.exists() else []
    expected_frames = int(sum(scene.duration for scene in SCENES) * FPS)
    if len(existing_frames) == expected_frames and not args.force:
        frame_count = len(existing_frames)
        print(f"Reusing {frame_count} existing frames.")
    else:
        frame_count = render_frames()
        print(f"Rendered {frame_count} frames.")
    audio_path = synthesize_audio(text_path)
    final = build_video(frame_count, audio_path)
    print(f"Prototype video: {final}")


if __name__ == "__main__":
    main()
