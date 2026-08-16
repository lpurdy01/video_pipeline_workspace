from __future__ import annotations

from manim import *


BG = "#00020A"
PANEL = "#050A18"
GRID = "#1F2B42"
WHITE = "#F4F7FF"
MUTED = "#8791A8"
CYAN = "#20F7D2"
BLUE = "#4D8DFF"
VIOLET = "#B45CFF"
GOLD = "#FFCB4D"
RED = "#FF4D6D"
GREEN = "#49F28D"
AMBER = "#FF9E45"


def title_text(text: str, font_size: int = 44) -> Text:
    return Text(text, color=WHITE, font_size=font_size, weight=BOLD)


def label_text(text: str, font_size: int = 24, color: str = WHITE) -> Text:
    return Text(text, color=color, font_size=font_size)


def tiny_text(text: str, font_size: int = 18, color: str = MUTED) -> Text:
    return Text(text, color=color, font_size=font_size)


def glow_line(start, end, color: str = CYAN, width: float = 4) -> VGroup:
    aura = Line(start, end, color=color, stroke_width=width * 3.0).set_opacity(0.18)
    core = Line(start, end, color=color, stroke_width=width)
    return VGroup(aura, core)


def glow_arrow(start, end, color: str = CYAN, width: float = 4, buff: float = 0.12) -> VGroup:
    aura = Arrow(start, end, color=color, stroke_width=width * 2.7, buff=buff).set_opacity(0.15)
    core = Arrow(start, end, color=color, stroke_width=width, buff=buff)
    return VGroup(aura, core)


def artifact_shape(kind: str, color: str, size: float = 0.92) -> VMobject:
    if kind == "requirement":
        shape = RegularPolygon(n=6, radius=size / 2, color=color)
    elif kind == "code":
        shape = Square(side_length=size, color=color)
    elif kind == "test":
        shape = Circle(radius=size / 2, color=color)
    elif kind == "review":
        shape = Square(side_length=size * 0.78, color=color).rotate(PI / 4)
    elif kind == "source":
        shape = Rectangle(width=size * 0.85, height=size * 1.05, color=color)
    else:
        shape = RoundedRectangle(corner_radius=0.08, width=size * 1.25, height=size * 0.76, color=color)
    shape.set_fill(PANEL, opacity=0.95)
    shape.set_stroke(color, width=2.6)
    return shape


def artifact_node(kind: str, text: str, color: str, size: float = 0.92, font_size: int = 18) -> VGroup:
    shape = artifact_shape(kind, color, size)
    label = Text(text, color=WHITE, font_size=font_size, weight=MEDIUM)
    label.move_to(shape)
    aura = shape.copy().set_stroke(color, width=8, opacity=0.13)
    return VGroup(aura, shape, label)


def card(text: str, width: float = 3.1, height: float = 1.15, color: str = CYAN, font_size: int = 22) -> VGroup:
    box = RoundedRectangle(corner_radius=0.08, width=width, height=height, color=color, stroke_width=2.4)
    box.set_fill(PANEL, opacity=0.97)
    aura = box.copy().set_stroke(color, width=9, opacity=0.10)
    label = Text(text, color=WHITE, font_size=font_size, weight=MEDIUM).move_to(box)
    return VGroup(aura, box, label)


def field_card(title: str, lines: list[str], width: float = 4.5, height: float = 2.8, color: str = GREEN) -> VGroup:
    box = RoundedRectangle(corner_radius=0.08, width=width, height=height, color=color, stroke_width=2.4)
    box.set_fill(PANEL, opacity=0.97)
    aura = box.copy().set_stroke(color, width=9, opacity=0.10)
    heading = Text(title, color=color, font_size=22, weight=BOLD)
    body = VGroup(*[Text(line, color=WHITE, font_size=18) for line in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
    content = VGroup(heading, body).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    content.move_to(box).shift(UP * 0.05)
    return VGroup(aura, box, content)


def connect(left: Mobject, right: Mobject, color: str = CYAN) -> VGroup:
    return glow_arrow(left.get_right(), right.get_left(), color=color, buff=0.18)


def safe_title(scene: Scene, text: str) -> Text:
    title = title_text(text, font_size=38).to_edge(UP, buff=0.35)
    scene.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.45)
    return title


def status_bar(label: str, value: float, color: str, width: float = 3.4) -> VGroup:
    base = RoundedRectangle(corner_radius=0.06, width=width, height=0.28, color=GRID, stroke_width=1.5)
    base.set_fill("#071021", opacity=1)
    fill = RoundedRectangle(corner_radius=0.06, width=width * value, height=0.28, color=color, stroke_width=0)
    fill.set_fill(color, opacity=0.85)
    fill.align_to(base, LEFT)
    text = Text(label, color=WHITE, font_size=18).next_to(base, LEFT, buff=0.22)
    pct = Text(f"{int(value * 100)}%", color=color, font_size=18).next_to(base, RIGHT, buff=0.18)
    return VGroup(text, base, fill, pct)

