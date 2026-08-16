from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from manim import *

from visual_style import AXIS, BG, BLUE, CYAN, GOLD, GREEN, GRID, MUTED, RED, VIOLET, WHITE, glow_dot, matrix_plate, neon_arrow, neon_line, small_label


class NewTransformSpacePrototype(ThreeDScene):
    """A Manim-first visual language prototype.

    This is intentionally sparse: narration carries the explanation, while the
    scene demonstrates signals becoming spectra, tokens becoming vectors, and a
    matrix-like transform acting on a vector cloud.
    """

    def construct(self):
        self.camera.background_color = BG
        self.set_camera_orientation(phi=68 * DEGREES, theta=-42 * DEGREES, zoom=0.9)

        self.signal_to_frequency()
        self.clear()
        self.language_to_vectors()
        self.clear()
        self.semantic_transform_loss()

    def signal_to_frequency(self):
        axes = ThreeDAxes(
            x_range=(-4, 4, 1),
            y_range=(-2, 2, 1),
            z_range=(-2, 2, 1),
            x_length=7,
            y_length=3,
            z_length=3,
            axis_config={"color": AXIS, "stroke_width": 4},
        ).shift(LEFT * 2.6)

        wave = ParametricFunction(
            lambda t: axes.c2p(t, 0.9 * math.sin(3 * t) + 0.38 * math.sin(8 * t), 0),
            t_range=(-3.6, 3.6, 0.03),
            color=CYAN,
            stroke_width=5,
        )
        wave_glow = wave.copy().set_stroke(CYAN, width=16, opacity=0.16)

        aperture = Rectangle(height=3.2, width=0.04, color=VIOLET, stroke_width=6).shift(RIGHT * 1.25)
        aperture_glow = aperture.copy().set_stroke(VIOLET, width=24, opacity=0.18)

        bars = VGroup()
        for i, height in enumerate([1.1, 0.35, 0.92, 0.24, 0.18]):
            bar = Rectangle(width=0.2, height=height, color=GOLD, fill_opacity=0.95, stroke_width=0)
            bar.move_to(RIGHT * (2.75 + i * 0.45) + DOWN * (1.0 - height / 2))
            bars.add(bar)
        bars_glow = bars.copy().set_opacity(0.18).scale(1.04)

        label_left = small_label("signal", CYAN, 32).next_to(wave, DOWN, buff=0.35)
        label_right = small_label("spectrum", GOLD, 32).next_to(bars, DOWN, buff=0.35)

        self.play(Create(axes), FadeIn(label_left), run_time=1.0)
        self.play(Create(wave_glow), Create(wave), run_time=1.4)
        self.play(FadeIn(aperture_glow), FadeIn(aperture), run_time=0.5)
        self.play(TransformFromCopy(wave, bars_glow), TransformFromCopy(wave, bars), FadeIn(label_right), run_time=1.8)
        self.begin_ambient_camera_rotation(rate=0.08)
        self.wait(1.7)
        self.stop_ambient_camera_rotation()

    def language_to_vectors(self):
        self.set_camera_orientation(phi=62 * DEGREES, theta=-50 * DEGREES, zoom=0.85)
        token_text = ["build", "API", "check", "subscription"]
        token_colors = [CYAN, GOLD, GREEN, VIOLET]
        token_boxes = VGroup(
            *[
                Text(text, color=color, font_size=32).set_stroke(color, width=0.35, opacity=0.5)
                for text, color in zip(token_text, token_colors)
            ]
        ).arrange(RIGHT, buff=0.48).to_edge(UP).shift(DOWN * 0.35)
        self.add_fixed_in_frame_mobjects(token_boxes)

        axes = ThreeDAxes(
            x_range=(-3, 3, 1),
            y_range=(-3, 3, 1),
            z_range=(-3, 3, 1),
            x_length=5.8,
            y_length=5.8,
            z_length=4,
            axis_config={"color": AXIS, "stroke_width": 4},
        ).shift(DOWN * 0.3)

        rng = np.random.default_rng(7)
        points = []
        colors = [CYAN, BLUE, VIOLET, GOLD, GREEN]
        for idx in range(64):
            theta = idx * 0.55
            radius = 1.15 + 0.85 * rng.random()
            z = -1.1 + 2.2 * rng.random()
            x = radius * math.cos(theta)
            y = radius * math.sin(theta)
            point = axes.c2p(x, y, z)
            points.append(glow_dot(point, colors[idx % len(colors)], radius=0.046))
        cloud = VGroup(*points)

        direction = neon_arrow(axes.c2p(-1.4, -0.7, -0.2), axes.c2p(1.35, 0.85, 0.7), color=GOLD, width=4)
        relation = small_label("relationship", GOLD, 28).next_to(direction, UP + RIGHT, buff=0.18)
        self.add_fixed_orientation_mobjects(relation)

        self.play(LaggedStart(*[FadeIn(group, shift=DOWN * 0.12) for group in token_boxes], lag_ratio=0.12), run_time=1.1)
        self.play(Create(axes), run_time=0.8)
        self.play(LaggedStart(*[TransformFromCopy(token_boxes[i % len(token_boxes)], points[i]) for i in range(28)], lag_ratio=0.025), run_time=1.8)
        self.play(FadeIn(VGroup(*points[28:]), lag_ratio=0.02), run_time=1.0)
        self.begin_ambient_camera_rotation(rate=0.11)
        self.play(Create(direction), FadeIn(relation), run_time=1.0)
        self.wait(1.8)
        self.stop_ambient_camera_rotation()

    def semantic_transform_loss(self):
        self.set_camera_orientation(phi=66 * DEGREES, theta=-35 * DEGREES, zoom=0.9)

        axes = ThreeDAxes(
            x_range=(-3, 3, 1),
            y_range=(-3, 3, 1),
            z_range=(-3, 3, 1),
            x_length=5.6,
            y_length=5.6,
            z_length=3.8,
            axis_config={"color": AXIS, "stroke_width": 4},
        ).shift(LEFT * 1.0)

        rng = np.random.default_rng(11)
        source_points = VGroup()
        target_points = VGroup()
        for i in range(34):
            p = rng.normal(size=3)
            p = p / np.linalg.norm(p) * (0.8 + rng.random() * 1.7)
            source = axes.c2p(p[0], p[1], p[2])
            q = np.array([1.15 * p[0] + 0.55 * p[1], -0.25 * p[0] + 0.72 * p[1], 0.28 * p[2]])
            target = axes.c2p(q[0], q[1], q[2])
            source_points.add(glow_dot(source, BLUE, radius=0.046))
            color = RED if i % 7 == 0 else CYAN
            target_points.add(glow_dot(target, color, radius=0.046))

        transform = matrix_plate([["1.1", ".5", "0"], ["-.2", ".7", "0"], ["0", "0", ".3"]], color=VIOLET)
        transform.scale(1.12).to_edge(RIGHT).shift(LEFT * 0.45)

        faded = VGroup()
        for i in [3, 9, 17, 24]:
            marker = Cross(source_points[i], stroke_color=RED, stroke_width=4).scale(0.75)
            faded.add(marker)

        loss_label = small_label("loss / assumptions", RED, 34).to_edge(DOWN).shift(UP * 0.26)
        arrow = neon_arrow(transform.get_left() + LEFT * 0.55, transform.get_left(), color=VIOLET, width=5)
        self.add_fixed_in_frame_mobjects(loss_label)

        self.play(Create(axes), FadeIn(source_points, lag_ratio=0.03), run_time=1.5)
        self.play(FadeIn(transform), Create(arrow), run_time=0.8)
        self.play(Transform(source_points, target_points), FadeIn(faded), FadeIn(loss_label), run_time=2.0)
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(2.0)
        self.stop_ambient_camera_rotation()


if __name__ == "__main__":
    scene = NewTransformSpacePrototype()
