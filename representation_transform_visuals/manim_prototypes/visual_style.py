from __future__ import annotations

from manim import *


BG = "#00020A"
GRID = "#1F2B42"
AXIS = "#8EA3D0"
WHITE = "#F4F7FF"
MUTED = "#8791A8"
CYAN = "#20F7D2"
BLUE = "#4D8DFF"
VIOLET = "#B45CFF"
GOLD = "#FFCB4D"
RED = "#FF4D6D"
GREEN = "#49F28D"


def glow_dot(point, color=CYAN, radius=0.055):
    core = Dot(point, radius=radius, color=color)
    aura = Dot(point, radius=radius * 3.6, color=color).set_opacity(0.32)
    return VGroup(aura, core)


def neon_line(start, end, color=CYAN, width=4):
    aura = Line(start, end, color=color, stroke_width=width * 3.4).set_opacity(0.24)
    core = Line(start, end, color=color, stroke_width=width)
    return VGroup(aura, core)


def neon_arrow(start, end, color=CYAN, width=4, buff=0):
    aura = Arrow(start, end, color=color, stroke_width=width * 3.4, buff=buff).set_opacity(0.22)
    core = Arrow(start, end, color=color, stroke_width=width, buff=buff)
    return VGroup(aura, core)


def small_label(text, color=WHITE, font_size=26):
    return Text(text, color=color, font_size=font_size)


def matrix_plate(entries, color=BLUE):
    rows = []
    for row in entries:
        cells = []
        for entry in row:
            cell = Square(side_length=0.58, color=color, stroke_width=2.6)
            aura = cell.copy().set_stroke(color, width=7, opacity=0.16)
            cell.set_fill("#030713", opacity=0.94)
            label = Text(str(entry), color=WHITE, font_size=24).move_to(cell)
            cells.append(VGroup(aura, cell, label))
        rows.append(VGroup(*cells).arrange(RIGHT, buff=0.05))
    grid = VGroup(*rows).arrange(DOWN, buff=0.05)
    bracket_l = Line(UP, DOWN, color=color, stroke_width=4).scale(1.02).next_to(grid, LEFT, buff=0.08)
    bracket_r = Line(UP, DOWN, color=color, stroke_width=4).scale(1.02).next_to(grid, RIGHT, buff=0.08)
    return VGroup(bracket_l, grid, bracket_r)
