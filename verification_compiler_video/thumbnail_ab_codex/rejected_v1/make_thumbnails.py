from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


HERE = Path(__file__).resolve().parent
VIDEO = HERE.parent
REPO = VIDEO.parent

W, H = 1280, 720
BG = "#00020A"
WHITE = "#F4F7FF"
MUTED = "#8791A8"
CYAN = "#20F7D2"
BLUE = "#4D8DFF"
VIOLET = "#B45CFF"
GOLD = "#FFCB4D"
RED = "#FF5A83"
GREEN = "#49F28D"
AMBER = "#FF9E45"


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    roots = [
        Path("/usr/share/fonts/truetype/dejavu"),
        Path("/usr/share/fonts/truetype/liberation"),
        Path("/usr/share/fonts/truetype/liberation2"),
    ]
    for root in roots:
        p = root / name
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


FONT_BLACK = "LiberationSansNarrow-Bold.ttf"
FONT_BOLD = "DejaVuSans-Bold.ttf"
FONT_REG = "DejaVuSans.ttf"
FONT_MONO = "DejaVuSansMono-Bold.ttf"


@dataclass(frozen=True)
class ThumbSpec:
    key: str
    file: str
    hook: list[tuple[str, str]]
    subhead: str
    title_case: str
    description_angle: str
    base: Path | None = None
    crop: tuple[float, float, float, float] | None = None
    accent: str = CYAN
    motif: str = "storm"


SPECS = [
    ThumbSpec(
        key="A",
        file="thumb_A_who_checks_it.png",
        hook=[("WHO CHECKS", WHITE), ("THE CODE?", RED)],
        subhead="AI can write it",
        title_case="AI Can Write Code. Who Checks It?",
        description_angle="Personal anxiety hook: the viewer has already accepted generated code, and now has to confront whether anyone can audit the volume.",
        base=VIDEO / "thumbnail_ab_codex/hook_frames/hook_08_028.0s.jpg",
        accent=RED,
        motif="gate",
    ),
    ThumbSpec(
        key="B",
        file="thumb_B_chat_not_evidence.png",
        hook=[("CHAT IS NOT", WHITE), ("EVIDENCE", GOLD)],
        subhead="no audit trail",
        title_case='A Chat Transcript Is Not Evidence',
        description_angle="Contrarian trust hook: attacks the false comfort of asking a model to grade its own answer.",
        base=VIDEO / "manim_prototypes/out/_thumbs/C_C02TranscriptVsRecord_3.jpg",
        accent=GOLD,
        motif="split",
    ),
    ThumbSpec(
        key="C",
        file="thumb_C_bottleneck_trust.png",
        hook=[("TRUST IS", WHITE), ("THE BOTTLENECK", CYAN)],
        subhead="generation got cheap",
        title_case="The Bottleneck Is Verification",
        description_angle="Market-shift hook: the scarce thing is no longer producing artifacts, but knowing which artifacts can be trusted.",
        base=None,
        accent=CYAN,
        motif="storm",
    ),
    ThumbSpec(
        key="D",
        file="thumb_D_compiler_for_trust.png",
        hook=[("COMPILER", WHITE), ("FOR TRUST", VIOLET)],
        subhead="AI review + human",
        title_case="The Compiler For Trust",
        description_angle="Concept-name hook: turns the video title into a big memorable object, best for viewers already warm to software architecture.",
        base=None,
        accent=VIOLET,
        motif="compiler",
    ),
]


def cover(path: Path | None, crop: tuple[float, float, float, float] | None = None) -> Image.Image:
    base = Image.new("RGB", (W, H), BG)
    if not path or not path.exists():
        return base
    im = Image.open(path).convert("RGB")
    if crop:
        iw, ih = im.size
        box = tuple(int(v) for v in (crop[0] * iw, crop[1] * ih, crop[2] * iw, crop[3] * ih))
        im = im.crop(box)
    scale = max(W / im.width, H / im.height)
    im = im.resize((math.ceil(im.width * scale), math.ceil(im.height * scale)), Image.Resampling.LANCZOS)
    x = (W - im.width) // 2
    y = (H - im.height) // 2
    base.paste(im, (x, y))
    return base


def add_gradient(img: Image.Image, side: str = "left", strength: float = 0.92) -> None:
    overlay = Image.new("RGBA", (W, H), (0, 2, 10, 0))
    px = overlay.load()
    for x in range(W):
        if side == "left":
            a = max(0, 255 * (1 - x / (W * 0.73)) * strength)
        else:
            a = max(0, 255 * (x / W) * strength)
        for y in range(H):
            vertical = 0.8 + 0.2 * abs((y - H / 2) / (H / 2))
            px[x, y] = (0, 2, 10, int(min(238, a * vertical)))
    img.alpha_composite(overlay)


def text_size(draw: ImageDraw.ImageDraw, text: str, f: ImageFont.ImageFont) -> tuple[int, int]:
    b = draw.textbbox((0, 0), text, font=f, stroke_width=0)
    return b[2] - b[0], b[3] - b[1]


def fit_font(draw: ImageDraw.ImageDraw, text: str, max_w: int, start: int, min_size: int = 46) -> ImageFont.ImageFont:
    size = start
    while size >= min_size:
        f = font(FONT_BLACK, size)
        if text_size(draw, text, f)[0] <= max_w:
            return f
        size -= 3
    return font(FONT_BLACK, min_size)


def draw_hook(draw: ImageDraw.ImageDraw, spec: ThumbSpec) -> None:
    x = 54
    y = 74
    max_w = 560 if spec.key == "B" else 650
    line_gap = 10
    shadow = (0, 0, 0)
    for text, color in spec.hook:
        f = fit_font(draw, text, max_w, 148 if len(text) < 13 else 120)
        draw.text((x + 6, y + 7), text, font=f, fill=shadow, stroke_width=9, stroke_fill=shadow)
        draw.text((x, y), text, font=f, fill=color, stroke_width=3, stroke_fill=shadow)
        y += text_size(draw, text, f)[1] + line_gap
    sf = font(FONT_BOLD, 32 if spec.key == "D" else 28)
    draw.rounded_rectangle((x, y + 12, x + text_size(draw, spec.subhead.upper(), sf)[0] + 28, y + 62), radius=10, fill=(8, 15, 30), outline=spec.accent, width=2)
    draw.text((x + 14, y + 20), spec.subhead.upper(), font=sf, fill=spec.accent)


def draw_text_backplate(draw: ImageDraw.ImageDraw, spec: ThumbSpec) -> None:
    right = 690 if spec.key in {"A", "C", "D"} else 610
    bottom = 360 if spec.key != "D" else 382
    draw.rounded_rectangle((-28, 34, right, bottom), radius=18, fill=(0, 2, 10, 232))


def glow_line(draw: ImageDraw.ImageDraw, points: list[tuple[int, int]], color: str, width: int = 5) -> None:
    for w, alpha in [(22, 35), (12, 70), (width, 255)]:
        rgba = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(rgba)
        d.line(points, fill=color + f"{alpha:02x}", width=w, joint="curve")
        draw._image.alpha_composite(rgba)


def draw_hex(draw: ImageDraw.ImageDraw, cx: int, cy: int, r: int, color: str) -> None:
    pts = []
    for i in range(6):
        a = math.pi / 6 + i * math.pi / 3
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=(5, 10, 22), outline=color)
    draw.line(pts + [pts[0]], fill=color, width=5)


def draw_storm(draw: ImageDraw.ImageDraw, accent: str) -> None:
    # Deterministic artifact field; gives empty areas some native video grammar.
    kinds = [(BLUE, "square"), (CYAN, "circle"), (GREEN, "record"), (VIOLET, "diamond"), (GOLD, "hex")]
    for i in range(54):
        x = 760 + ((i * 83) % 445)
        y = 90 + ((i * 47) % 505)
        color, shape = kinds[i % len(kinds)]
        size = 22 + (i % 4) * 4
        if shape == "circle":
            draw.ellipse((x, y, x + size, y + size), outline=color, width=3)
        elif shape == "record":
            draw.rounded_rectangle((x, y, x + size * 1.5, y + size), radius=5, outline=color, width=3)
        elif shape == "diamond":
            pts = [(x + size / 2, y), (x + size, y + size / 2), (x + size / 2, y + size), (x, y + size / 2)]
            draw.line(pts + [pts[0]], fill=color, width=3)
        elif shape == "hex":
            draw_hex(draw, x + size // 2, y + size // 2, size // 2, color)
        else:
            draw.rectangle((x, y, x + size, y + size), outline=color, width=3)
    glow_line(draw, [(820, 510), (930, 470), (1030, 445), (1130, 418)], accent, width=5)


def draw_gate(draw: ImageDraw.ImageDraw, accent: str) -> None:
    # Mask stale in-frame labels from the source render before drawing the bold
    # thumbnail-scale barrier.
    draw.rounded_rectangle((888, 108, 1148, 190), radius=8, fill=(0, 2, 10))
    draw.line((1004, 132, 1004, 604), fill=GOLD, width=13)
    draw.line((1040, 132, 1040, 604), fill=GOLD, width=13)
    glow_line(draw, [(690, 360), (875, 360), (1008, 360)], accent, width=6)
    draw.text((1049, 325), "?", font=font(FONT_BLACK, 184), fill=RED, stroke_width=8, stroke_fill=(0, 0, 0))


def draw_split(draw: ImageDraw.ImageDraw) -> None:
    left = (700, 188, 925, 515)
    right = (965, 188, 1232, 515)
    draw.rounded_rectangle(left, radius=12, outline=RED, width=4, fill=(6, 10, 22))
    draw.rounded_rectangle(right, radius=12, outline=GREEN, width=4, fill=(6, 14, 24))
    for i, width in enumerate([142, 168, 124, 0, 130, 154]):
        if width:
            y = 224 + i * 39
            draw.rounded_rectangle((724, y, 724 + width, y + 14), radius=6, fill=(78, 88, 108))
    for i, width in enumerate([182, 118, 148, 95, 164, 138]):
        y = 224 + i * 39
        color = (47, 190, 122) if i % 2 == 0 else (126, 138, 164)
        draw.rounded_rectangle((990, y, 990 + width, y + 14), radius=6, fill=color)
    for offset, width in [(-4, 14), (4, 14), (0, 22)]:
        draw.line((734 + offset, 532, 814 + offset, 626), fill=RED, width=width)
        draw.line((814 + offset, 532, 734 + offset, 626), fill=RED, width=width)
    for offset, width in [(-4, 14), (4, 14), (0, 22)]:
        draw.line((1036 + offset, 572, 1078 + offset, 620), fill=GREEN, width=width)
        draw.line((1078 + offset, 620, 1168 + offset, 522), fill=GREEN, width=width)


def draw_compiler(draw: ImageDraw.ImageDraw) -> None:
    # Right-lane visual: graph compiles into one package, then branches into
    # AI review and human sign-off before preserving evidence.
    nf = font(FONT_BOLD, 27)
    small = font(FONT_BOLD, 28)

    graph_nodes = [
        ("REQ", 782, 165, GOLD, "hex"),
        ("CODE", 905, 238, BLUE, "square"),
        ("TEST", 782, 315, CYAN, "circle"),
    ]
    for a, b in [((820, 176), (860, 224)), ((820, 303), (860, 252))]:
        glow_line(draw, [a, b], CYAN, width=4)
    for label, x, y, color, shape in graph_nodes:
        if shape == "circle":
            draw.ellipse((x - 43, y - 43, x + 43, y + 43), outline=color, width=6, fill=(5, 10, 22))
        elif shape == "hex":
            draw_hex(draw, x, y, 49, color)
        else:
            draw.rectangle((x - 49, y - 49, x + 49, y + 49), outline=color, width=6, fill=(5, 10, 22))
        tw, th = text_size(draw, label, small)
        draw.text((x - tw / 2, y - th / 2), label, font=small, fill=WHITE)

    draw.rounded_rectangle((750, 405, 955, 506), radius=12, outline=GREEN, width=6, fill=(7, 12, 25))
    draw.text((798, 428), "VQP", font=font(FONT_BLACK, 58), fill=GREEN)
    glow_line(draw, [(902, 280), (852, 410)], GREEN, width=5)

    ai_box = (1012, 130, 1230, 238)
    human_box = (1012, 286, 1230, 394)
    draw.rounded_rectangle(ai_box, radius=12, outline=VIOLET, width=5, fill=(8, 10, 28))
    draw.rounded_rectangle(human_box, radius=12, outline=GOLD, width=5, fill=(22, 16, 6))
    draw.text((1042, 148), "AI", font=font(FONT_BLACK, 62), fill=VIOLET)
    draw.text((1120, 161), "REVIEW", font=nf, fill=WHITE)
    draw.text((1035, 306), "HUMAN", font=font(FONT_BLACK, 46), fill=GOLD)
    draw.text((1045, 350), "SIGN-OFF", font=nf, fill=WHITE)
    glow_line(draw, [(945, 440), (1008, 184)], VIOLET, width=4)
    glow_line(draw, [(945, 458), (1008, 340)], GOLD, width=4)

    draw.rounded_rectangle((910, 545, 1230, 635), radius=14, outline=GREEN, width=5, fill=(7, 16, 25))
    draw.text((942, 565), "EVIDENCE", font=font(FONT_BLACK, 54), fill=GREEN)
    glow_line(draw, [(1120, 238), (1120, 545)], VIOLET, width=3)
    glow_line(draw, [(1120, 394), (1120, 545)], GOLD, width=3)


def render(spec: ThumbSpec) -> Path:
    img = cover(spec.base, spec.crop).convert("RGBA")
    img = ImageEnhance.Contrast(img).enhance(1.25)
    img = ImageEnhance.Brightness(img).enhance(0.62)
    img = img.filter(ImageFilter.UnsharpMask(radius=1.4, percent=130))
    add_gradient(img, "left", 0.96)

    draw = ImageDraw.Draw(img)
    if spec.motif == "split":
        draw.rectangle((0, 0, W, 125), fill=(0, 2, 10))
    if spec.motif == "gate":
        draw_storm(draw, spec.accent)
        draw_gate(draw, spec.accent)
    elif spec.motif == "split":
        draw_split(draw)
    elif spec.motif == "compiler":
        draw_compiler(draw)
    else:
        draw_storm(draw, spec.accent)
    draw_text_backplate(draw, spec)
    draw_hook(draw, spec)

    # Small brand anchor, intentionally not competing with the thumbnail hook.
    if spec.key != "A":
        bf = font(FONT_BOLD, 24)
        label = "THE COMPILER FOR TRUST"
        tw, _ = text_size(draw, label, bf)
        draw.text((W - tw - 42, H - 52), label, font=bf, fill=(190, 198, 224))

    out = HERE / spec.file
    img.convert("RGB").save(out, optimize=True, quality=92)
    return out


def make_contact(paths: list[Path], out: Path) -> None:
    cols = 2
    thumb_w, thumb_h = 640, 360
    sheet = Image.new("RGB", (cols * thumb_w, 2 * (thumb_h + 40)), (3, 5, 12))
    d = ImageDraw.Draw(sheet)
    lf = font(FONT_BOLD, 24)
    for i, p in enumerate(paths):
        im = Image.open(p).convert("RGB").resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        x = (i % cols) * thumb_w
        y = (i // cols) * (thumb_h + 40)
        sheet.paste(im, (x, y))
        d.text((x + 18, y + thumb_h + 8), p.name, font=lf, fill=WHITE)
    sheet.save(out, quality=92)


def make_mobile_preview(paths: list[Path], out: Path) -> None:
    # Simulates the tiny feed read: 20% size, with labels underneath.
    cols = 4
    sw, sh = 256, 144
    sheet = Image.new("RGB", (cols * sw, sh + 46), (3, 5, 12))
    d = ImageDraw.Draw(sheet)
    lf = font(FONT_BOLD, 16)
    for i, p in enumerate(paths):
        im = Image.open(p).convert("RGB").resize((sw, sh), Image.Resampling.LANCZOS)
        x = i * sw
        sheet.paste(im, (x, 0))
        d.text((x + 6, sh + 8), p.name.replace("thumb_", "").replace(".png", ""), font=lf, fill=WHITE)
    sheet.save(out, quality=92)


def main() -> None:
    outputs = [render(s) for s in SPECS]
    make_contact(outputs, HERE / "thumbnail_contact_sheet.jpg")
    make_mobile_preview(outputs, HERE / "thumbnail_mobile_preview.jpg")
    manifest = {
        "generated": [str(p.name) for p in outputs],
        "contact_sheet": "thumbnail_contact_sheet.jpg",
        "mobile_preview": "thumbnail_mobile_preview.jpg",
        "cases": [
            {
                "key": s.key,
                "thumbnail": s.file,
                "title": s.title_case,
                "angle": s.description_angle,
                "on_thumbnail_text": " / ".join(t for t, _ in s.hook),
            }
            for s in SPECS
        ],
    }
    (HERE / "thumbnail_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    for p in outputs:
        print(p)


if __name__ == "__main__":
    main()
