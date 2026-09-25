"""Deterministic PIL thumbnail compositor for "The Compiler For Trust".

Design rules learned from the rejected v1 pass (see rejected_v1/ and
HANDOFF_FOR_NEXT_MODEL.md):

1. Never place shapes with `i * k % span` arithmetic. Both coordinates end up
   linear in i, so consecutive shapes step a constant vector and draw visible
   diagonal chains. Placement here is either an explicit layout or a seeded
   `random.Random` draw with a spacing reject.
2. Text that lives inside a shape goes through `fit_font`, which shrinks until
   it measures inside the box. Anything that still does not fit is recorded in
   OVERFLOWS and printed at the end of the run.
3. No photographic base frames. v1 composited rendered stills under the panels
   and the source captions bled through the artwork. Everything is vector.
"""

from __future__ import annotations

import json
import math
import random
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent

W, H = 1280, 720
BG = "#00030C"
PANEL = "#070C1A"
WHITE = "#F4F7FF"
MUTED = "#8791A8"
CYAN = "#20F7D2"
BLUE = "#4D8DFF"
VIOLET = "#B45CFF"
GOLD = "#FFCB4D"
RED = "#FF5A83"
GREEN = "#49F28D"

FONT_BLACK = "LiberationSansNarrow-Bold.ttf"
FONT_BOLD = "DejaVuSans-Bold.ttf"
FONT_MONO = "DejaVuSansMono-Bold.ttf"

FONT_DIRS = [
    Path("/usr/share/fonts/truetype/dejavu"),
    Path("/usr/share/fonts/truetype/liberation"),
    Path("/usr/share/fonts/truetype/liberation2"),
]

OVERFLOWS: list[str] = []


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    for root in FONT_DIRS:
        p = root / name
        if p.exists():
            return ImageFont.truetype(str(p), size)
    raise FileNotFoundError(name)


# --------------------------------------------------------------------------
# canvas + primitives
# --------------------------------------------------------------------------


class Canvas:
    def __init__(self) -> None:
        self.img = Image.new("RGBA", (W, H), BG)
        self.draw = ImageDraw.Draw(self.img)

    def glow_line(self, pts, color: str, width: int = 5) -> None:
        for w, alpha in [(width + 16, 26), (width + 8, 58), (width, 255)]:
            layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(layer).line(pts, fill=f"{color}{alpha:02x}", width=w, joint="curve")
            self.img.alpha_composite(layer)

    def glow_rect(self, box, color: str, width: int = 5, radius: int = 14, fill=PANEL) -> None:
        for w, alpha in [(width + 12, 22), (width + 5, 50)]:
            layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(layer).rounded_rectangle(box, radius=radius, outline=f"{color}{alpha:02x}", width=w)
            self.img.alpha_composite(layer)
        self.draw.rounded_rectangle(box, radius=radius, fill=fill, outline=color, width=width)


def measure(d: ImageDraw.ImageDraw, text: str, f: ImageFont.FreeTypeFont) -> tuple[int, int]:
    l, t, r, b = d.textbbox((0, 0), text, font=f)
    return r - l, b - t


def fit_font(
    d: ImageDraw.ImageDraw,
    text: str,
    max_w: int,
    max_h: int,
    start: int,
    name: str = FONT_BOLD,
    min_size: int = 9,
    tag: str = "",
) -> ImageFont.FreeTypeFont:
    """Largest size at or below `start` whose rendered text fits (max_w, max_h)."""
    size = start
    while size >= min_size:
        f = font(name, size)
        w, h = measure(d, text, f)
        if w <= max_w and h <= max_h:
            return f
        size -= 1
    f = font(name, min_size)
    w, h = measure(d, text, f)
    if w > max_w or h > max_h:
        OVERFLOWS.append(f"{tag or text!r}: {w}x{h} does not fit {max_w}x{max_h} even at {min_size}px")
    return f


def glyph_centered(d: ImageDraw.ImageDraw, cx: float, cy: float, text: str,
                   f: ImageFont.FreeTypeFont, fill: str, **kw) -> None:
    # textbbox understands stroke_width but not stroke_fill.
    l, t, r, b = d.textbbox((0, 0), text, font=f, stroke_width=kw.get("stroke_width", 0))
    d.text((cx - (l + r) / 2, cy - (t + b) / 2), text, font=f, fill=fill, **kw)


def dashed_rect(d: ImageDraw.ImageDraw, box, color: str, width: int = 4, dash: int = 18, gap: int = 14) -> None:
    x0, y0, x1, y1 = box
    for x in range(int(x0), int(x1), dash + gap):
        xe = min(x + dash, x1)
        d.line((x, y0, xe, y0), fill=color, width=width)
        d.line((x, y1, xe, y1), fill=color, width=width)
    for y in range(int(y0), int(y1), dash + gap):
        ye = min(y + dash, y1)
        d.line((x0, y, x0, ye), fill=color, width=width)
        d.line((x1, y, x1, ye), fill=color, width=width)


def arrow(c: Canvas, x0: int, x1: int, y: int, color: str, width: int = 8) -> None:
    head = 22
    c.glow_line([(x0, y), (x1 - head, y)], color, width=width)
    c.draw.polygon([(x1, y), (x1 - head, y - head // 2 - 4), (x1 - head, y + head // 2 + 4)], fill=color)


def background(c: Canvas) -> None:
    """Faint grid + vignette. Low alpha so it reads as texture, never as content."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for x in range(0, W, 64):
        d.line((x, 0, x, H), fill=(70, 100, 170, 16), width=1)
    for y in range(0, H, 64):
        d.line((0, y, W, y), fill=(70, 100, 170, 16), width=1)
    c.img.alpha_composite(layer)

    vign = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dv = ImageDraw.Draw(vign)
    for i in range(24):
        a = int(9 * (i / 24) ** 2 * 24)
        dv.rectangle((i * 6, i * 4, W - i * 6, H - i * 4), outline=(0, 2, 8, a), width=7)
    c.img.alpha_composite(vign)


def code_card(c: Canvas, x: int, y: int, w: int, h: int, color: str, seed: int) -> None:
    """A generated-code artifact: header bar + a few code lines, seeded widths."""
    rng = random.Random(seed)
    c.draw.rounded_rectangle((x, y, x + w, y + h), radius=10, fill="#0A1020", outline=color, width=4)
    c.draw.rounded_rectangle((x + 16, y + 16, x + 16 + int(w * 0.34), y + 27), radius=6, fill=color)
    ly = y + 44
    while ly + 12 < y + h - 12:
        frac = rng.uniform(0.32, 0.80)
        c.draw.rounded_rectangle((x + 16, ly, x + 16 + int((w - 32) * frac), ly + 10), radius=5, fill="#31415F")
        ly += 20


# --------------------------------------------------------------------------
# shared hook block
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class ThumbSpec:
    key: str
    file: str
    hook: list[tuple[str, str]]
    subhead: str
    title_case: str
    description_angle: str
    accent: str
    hook_x: int = 54
    hook_y: int = 62
    hook_w: int = 600
    hook_size: int = 150
    brand: bool = True


def draw_hook(c: Canvas, spec: ThumbSpec) -> int:
    x, y = spec.hook_x, spec.hook_y
    for text, color in spec.hook:
        f = fit_font(c.draw, text, spec.hook_w, 400, spec.hook_size, name=FONT_BLACK, min_size=40, tag=f"{spec.key} hook")
        c.draw.text((x + 5, y + 6), text, font=f, fill=(0, 0, 0), stroke_width=10, stroke_fill=(0, 0, 0))
        c.draw.text((x, y), text, font=f, fill=color, stroke_width=3, stroke_fill=(0, 0, 0))
        y += measure(c.draw, text, f)[1] + 18

    label = spec.subhead.upper()
    sf = fit_font(c.draw, label, spec.hook_w - 40, 44, 34, name=FONT_BOLD, tag=f"{spec.key} subhead")
    tw, th = measure(c.draw, label, sf)
    y += 14
    c.draw.rounded_rectangle((x, y, x + tw + 34, y + th + 26), radius=10, fill="#080F1E", outline=spec.accent, width=3)
    c.draw.text((x + 17, y + 13 + th // 2), label, font=sf, fill=spec.accent, anchor="lm")
    return y + th + 26


def draw_brand(c: Canvas, y: int = H - 50) -> None:
    f = font(FONT_BOLD, 23)
    label = "THE COMPILER FOR TRUST"
    tw, _ = measure(c.draw, label, f)
    c.draw.text((W - tw - 42, y), label, font=f, fill=(168, 178, 206))


# --------------------------------------------------------------------------
# A - calm gate. one stack, one gate, one empty checker slot.
# --------------------------------------------------------------------------


def build_A(c: Canvas) -> None:
    for i, y in enumerate(range(-34, 700, 118)):
        code_card(c, 672, y, 202, 104, BLUE, seed=11 + i)

    arrow(c, 886, 966, 352, RED, width=13)

    for bx in (986, 1030):
        c.glow_line([(bx, 16), (bx, 704)], GOLD, width=15)

    slot = (1068, 196, 1262, 524)
    dashed_rect(c.draw, slot, "#5A6580", width=5)
    qf = font(FONT_BLACK, 232)
    glyph_centered(c.draw, (slot[0] + slot[2]) / 2, (slot[1] + slot[3]) / 2, "?", qf, RED,
                   stroke_width=7, stroke_fill=(0, 0, 0))


# --------------------------------------------------------------------------
# B - chat vs evidence record. meaningful text, fitted to the panels.
# --------------------------------------------------------------------------

CHAT_LINES = ["looks good", "probably passes", "want tests?"]
EVIDENCE_ROWS = [("REQ-17", "linked"), ("TEST", "PASS"), ("HUMAN", "REVIEW"), ("VERSION", "a81f")]


def build_B(c: Canvas) -> None:
    left = (656, 150, 944, 632)
    right = (966, 150, 1252, 632)
    c.glow_rect(left, RED, width=4, radius=14, fill="#100811")
    c.glow_rect(right, GREEN, width=4, radius=14, fill="#06140F")

    # headers
    for box, color, name, mark in ((left, RED, "CHAT", "✕"), (right, GREEN, "EVIDENCE", "✓")):
        x0, y0, x1, _ = box
        hf = fit_font(c.draw, name, (x1 - x0) - 96, 40, 34, name=FONT_BOLD, tag=f"B header {name}")
        c.draw.text((x0 + 20, y0 + 34), name, font=hf, fill=color, anchor="lm")
        c.draw.ellipse((x1 - 62, y0 + 12, x1 - 18, y0 + 56), fill=color)
        glyph_centered(c.draw, x1 - 40, y0 + 34, mark, font(FONT_BOLD, 30), "#04070F")
        c.draw.line((x0 + 16, y0 + 68, x1 - 16, y0 + 68), fill=f"{color}55", width=2)

    # left: loose chat bubbles, ragged widths, no structure
    inner_w = (left[2] - left[0]) - 48
    top = left[1] + 96
    bh = ((left[3] - 20) - top - 2 * 30) // len(CHAT_LINES)
    chat_size = min(
        fit_font(c.draw, line, inner_w - 40, bh - 30, 46, name=FONT_BOLD, tag=f"B chat {i}").size
        for i, line in enumerate(CHAT_LINES)
    )
    f = font(FONT_BOLD, chat_size)
    by = top
    for line in CHAT_LINES:
        tw, _ = measure(c.draw, f"{line}", f)
        bw = tw + 38
        c.draw.rounded_rectangle((left[0] + 24, by, left[0] + 24 + bw, by + bh), radius=16,
                                 fill="#231020", outline="#6A2F49", width=3)
        c.draw.text((left[0] + 43, by + bh // 2), line, font=f, fill="#E4C7D6", anchor="lm")
        by += bh + 30

    # right: uniform record rows, mono labels, per-row check
    row_x0, row_x1 = right[0] + 20, right[2] - 20
    ry = right[1] + 96
    gap = 10
    avail = (right[3] - 20) - ry
    row_h = (avail - gap * (len(EVIDENCE_ROWS) - 1)) // len(EVIDENCE_ROWS)
    for i, (key, val) in enumerate(EVIDENCE_ROWS):
        c.draw.rounded_rectangle((row_x0, ry, row_x1, ry + row_h), radius=10, fill="#0A1D18", outline="#1E5A45", width=2)
        c.draw.rectangle((row_x0, ry + 10, row_x0 + 6, ry + row_h - 10), fill=GREEN)
        kf = fit_font(c.draw, key, (row_x1 - row_x0) - 74, 30, 24, name=FONT_MONO, tag=f"B key {key}")
        c.draw.text((row_x0 + 20, ry + row_h * 0.32), key, font=kf, fill="#6FD9B4", anchor="lm")
        vf = fit_font(c.draw, val, (row_x1 - row_x0) - 74, 40, 34, name=FONT_MONO, tag=f"B val {val}")
        c.draw.text((row_x0 + 20, ry + row_h * 0.70), val, font=vf, fill=WHITE, anchor="lm")
        glyph_centered(c.draw, row_x1 - 26, ry + row_h / 2, "✓", font(FONT_BOLD, 28), GREEN)
        ry += row_h + gap


# --------------------------------------------------------------------------
# C - two rates. generated lane packed, verified lane nearly empty.
# --------------------------------------------------------------------------


def build_C(c: Canvas) -> None:
    # Same lane, same card pitch, both inside the frame. The only variable is how
    # many artifacts each lane holds, so the emptiness below is the whole message.
    lane_x0, lane_x1 = 664, 1252
    lane_h = 196
    card_w, packed = 54, 9
    pitch = (lane_x1 - lane_x0 - 36 - card_w) / (packed - 1)
    for label, color, ly, count in (("GENERATED", GOLD, 150, packed), ("VERIFIED", CYAN, 448, 2)):
        lf = font(FONT_BOLD, 32)
        c.draw.text((lane_x0 + 4, ly - 24), label, font=lf, fill=color, anchor="lm")
        c.draw.rounded_rectangle((lane_x0, ly, lane_x1, ly + lane_h), radius=14, fill="#050A16", outline=f"{color}55", width=2)
        for i in range(count):
            x = int(lane_x0 + 18 + i * pitch)
            c.draw.rounded_rectangle((x, ly + 26, x + card_w, ly + lane_h - 26), radius=8, fill="#0C1526", outline=color, width=3)
            c.draw.rounded_rectangle((x + 11, ly + 42, x + 43, ly + 51), radius=4, fill=f"{color}bb")
            for k, wfrac in enumerate((0.52, 0.78, 0.40)):
                yy = ly + 64 + k * 18
                c.draw.rounded_rectangle((x + 11, yy, x + 11 + int(32 * wfrac), yy + 8), radius=3, fill="#31415F")


# --------------------------------------------------------------------------
# D - one pipeline: AI code in, verify machine, evidence out.
# --------------------------------------------------------------------------


def build_D(c: Canvas) -> None:
    y_mid = 556
    box_in = (52, 486, 372, 626)
    box_mid = (444, 442, 836, 670)
    box_out = (908, 486, 1228, 626)

    c.glow_rect(box_in, VIOLET, width=5, radius=14, fill="#140A24")
    c.glow_rect(box_out, CYAN, width=5, radius=14, fill="#06181C")
    c.glow_rect(box_mid, GREEN, width=6, radius=16, fill="#06160F")

    arrow(c, 380, 438, y_mid, VIOLET, width=8)
    arrow(c, 844, 902, y_mid, CYAN, width=8)

    f_in = fit_font(c.draw, "AI CODE", 268, 88, 78, name=FONT_BLACK, tag="D in")
    c.draw.text(((box_in[0] + box_in[2]) // 2, y_mid), "AI CODE", font=f_in, fill=VIOLET, anchor="mm")
    f_out = fit_font(c.draw, "EVIDENCE", 268, 88, 78, name=FONT_BLACK, tag="D out")
    c.draw.text(((box_out[0] + box_out[2]) // 2, y_mid), "EVIDENCE", font=f_out, fill=CYAN, anchor="mm")

    f_mid = fit_font(c.draw, "VERIFY", 330, 96, 92, name=FONT_BLACK, tag="D mid")
    c.draw.text(((box_mid[0] + box_mid[2]) // 2, 502), "VERIFY", font=f_mid, fill=GREEN, anchor="mm")

    chips = [("AI REVIEW", VIOLET), ("HUMAN SIGN-OFF", GOLD)]
    total = box_mid[2] - box_mid[0] - 40 - 14
    weights = [len(t) for t, _ in chips]
    widths = [int(total * w / sum(weights)) for w in weights]
    # One shared size so neither chip reads as the junior partner.
    size = min(
        fit_font(c.draw, t, cwidth - 22, 38, 28, name=FONT_BOLD, tag=f"D chip {t}").size
        for (t, _), cwidth in zip(chips, widths)
    )
    cf = font(FONT_BOLD, size)
    cx = box_mid[0] + 20
    for (text, color), cwidth in zip(chips, widths):
        c.draw.rounded_rectangle((cx, 574, cx + cwidth, 646), radius=10, fill="#0B1120", outline=color, width=3)
        c.draw.text((cx + cwidth // 2, 610), text, font=cf, fill=color, anchor="mm")
        cx += cwidth + 14


# --------------------------------------------------------------------------


SPECS = [
    ThumbSpec(
        key="A",
        file="thumb_A_who_checks_it.png",
        hook=[("WHO CHECKS", WHITE), ("THE CODE?", RED)],
        subhead="AI can write it",
        title_case="AI Can Write The Code. Who Checks It?",
        description_angle="Personal anxiety hook: the viewer has already accepted generated code and now has to confront that the checking seat is empty.",
        accent=RED,
        hook_w=596,
        hook_size=146,
        brand=False,
    ),
    ThumbSpec(
        key="B",
        file="thumb_B_chat_not_evidence.png",
        hook=[("CHAT IS NOT", WHITE), ("EVIDENCE", GOLD)],
        subhead="no audit trail",
        title_case="A Chat Transcript Is Not Evidence",
        description_angle="Contrarian trust hook: attacks the false comfort of asking a model to grade its own answer, and shows what a real record looks like instead.",
        accent=GOLD,
        hook_w=568,
        hook_size=140,
    ),
    ThumbSpec(
        key="C",
        file="thumb_C_bottleneck_trust.png",
        hook=[("TRUST IS", WHITE), ("THE BOTTLENECK", CYAN)],
        subhead="generation got cheap",
        title_case="The Bottleneck Is Verification",
        description_angle="Market-shift hook: the scarce thing is no longer producing artifacts but knowing which ones can be trusted.",
        accent=CYAN,
        hook_w=592,
        hook_size=132,
    ),
    ThumbSpec(
        key="D",
        file="thumb_D_compiler_for_trust.png",
        hook=[("COMPILER", WHITE), ("FOR TRUST", VIOLET)],
        subhead="AI writes it. humans sign it.",
        title_case="The Compiler For Trust",
        description_angle="Concept-name hook: turns the video title into one legible pipeline, AI in, human-signed evidence out.",
        accent=VIOLET,
        hook_x=52,
        hook_y=40,
        hook_w=760,
        hook_size=160,
        brand=False,
    ),
]

BUILDERS = {"A": build_A, "B": build_B, "C": build_C, "D": build_D}


def render(spec: ThumbSpec) -> Path:
    c = Canvas()
    background(c)
    BUILDERS[spec.key](c)
    draw_hook(c, spec)
    if spec.brand:
        draw_brand(c)
    out = HERE / spec.file
    c.img.convert("RGB").save(out, optimize=True)
    return out


def make_contact(paths: list[Path], out: Path) -> None:
    tw, th = 640, 360
    sheet = Image.new("RGB", (2 * tw, 2 * (th + 40)), (3, 5, 12))
    d = ImageDraw.Draw(sheet)
    lf = font(FONT_BOLD, 24)
    for i, p in enumerate(paths):
        im = Image.open(p).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        x, y = (i % 2) * tw, (i // 2) * (th + 40)
        sheet.paste(im, (x, y))
        d.text((x + 18, y + th + 8), p.name, font=lf, fill=WHITE)
    sheet.save(out, quality=93)


def make_mobile_preview(paths: list[Path], out: Path) -> None:
    """246px wide is roughly the YouTube mobile feed read."""
    sw, sh = 246, 138
    sheet = Image.new("RGB", (4 * sw + 20, sh + 42), (3, 5, 12))
    d = ImageDraw.Draw(sheet)
    lf = font(FONT_BOLD, 15)
    for i, p in enumerate(paths):
        im = Image.open(p).convert("RGB").resize((sw, sh), Image.Resampling.LANCZOS)
        x = i * (sw + 5) + 4
        sheet.paste(im, (x, 6))
        d.text((x + 2, sh + 16), p.name.replace("thumb_", "").replace(".png", ""), font=lf, fill=WHITE)
    sheet.save(out, quality=93)


def main() -> None:
    outputs = [render(s) for s in SPECS]
    make_contact(outputs, HERE / "thumbnail_contact_sheet.jpg")
    make_mobile_preview(outputs, HERE / "thumbnail_mobile_preview.jpg")
    manifest = {
        "generated": [p.name for p in outputs],
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
        print(p.name)
    if OVERFLOWS:
        print("\nTEXT FIT WARNINGS:")
        for o in OVERFLOWS:
            print("  -", o)
    else:
        print("\ntext fit: all boxed text fits")


if __name__ == "__main__":
    main()
