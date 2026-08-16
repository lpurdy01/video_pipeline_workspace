from __future__ import annotations

import numpy as np
from manim import *

from visual_style import AXIS, BG, BLUE, CYAN, GOLD, GREEN, VIOLET, WHITE, glow_dot


class VectorAnalogyBenchmark(ThreeDScene):
    """Benchmark scene for the core mental model: words become computable geometry."""

    def setup(self):
        super().setup()
        self.camera.background_color = BG

    def glow_text(self, text: str, color=WHITE, font_size=28) -> VGroup:
        core = Text(text, color=color, font_size=font_size)
        aura = core.copy().set_stroke(color, width=1.4, opacity=0.28)
        return VGroup(aura, core)

    def token_box(self, text: str, color=CYAN) -> VGroup:
        label = Text(text, color=WHITE, font_size=22)
        box = RoundedRectangle(
            width=max(0.9, label.width + 0.34),
            height=0.44,
            corner_radius=0.06,
            color=color,
            stroke_width=2.4,
        )
        box.set_fill("#030713", opacity=0.82)
        glow = box.copy().set_stroke(color, width=8, opacity=0.16)
        return VGroup(glow, box, label)

    def vector_column(self, values: list[float], color=BLUE) -> VGroup:
        rows = VGroup()
        for value in values:
            label = Text(f"{value:.1f}", color=WHITE, font_size=25)
            cell = Rectangle(width=0.82, height=0.46, color=color, stroke_width=3.0)
            cell.set_fill("#071126", opacity=0.96)
            rows.add(VGroup(cell, label))
        rows.arrange(DOWN, buff=0.045)
        bracket_l = Line(UP, DOWN, color=color, stroke_width=4.4).match_height(rows).next_to(rows, LEFT, buff=0.08)
        bracket_r = Line(UP, DOWN, color=color, stroke_width=4.4).match_height(rows).next_to(rows, RIGHT, buff=0.08)
        glow = VGroup(bracket_l.copy(), bracket_r.copy()).set_stroke(color, width=13, opacity=0.24)
        return VGroup(glow, bracket_l, rows, bracket_r)

    def point_label(self, text: str, color: str, label_offset=UP * 0.34, font_size=32) -> VGroup:
        halo = Dot3D(radius=0.18, color=color, resolution=(12, 12)).set_opacity(0.28)
        dot = Dot3D(radius=0.085, color=color, resolution=(18, 18))
        dot.set_stroke(WHITE, width=0.35, opacity=0.55)
        label = Text(text, color=color, font_size=font_size)
        label_group = VGroup(label).move_to(dot.get_center() + label_offset)
        return VGroup(halo, dot, label_group)

    def spatial_label(self, text: str, color: str, font_size=34) -> VGroup:
        core = Text(text, color=color, font_size=font_size)
        shield = core.copy().set_stroke(BG, width=8, opacity=0.95)
        glow = core.copy().set_stroke(color, width=3.4, opacity=0.42)
        return VGroup(shield, glow, core)

    def equation_group(self) -> VGroup:
        pieces = [
            ("king", GOLD),
            (" - ", WHITE),
            ("man", BLUE),
            (" + ", WHITE),
            ("woman", VIOLET),
            (" \u2248 ", WHITE),
            ("queen", GREEN),
        ]
        group = VGroup(*[Text(text, color=color, font_size=31) for text, color in pieces])
        group.arrange(RIGHT, buff=0.035)
        return group

    def vector_arrow3d(self, start, end, color=GOLD, thickness=0.018, height=0.18, base_radius=0.055) -> Arrow3D:
        return Arrow3D(
            start=start,
            end=end,
            thickness=thickness,
            height=height,
            base_radius=base_radius,
            color=color,
            resolution=(8, 8),
        )

    def vector_line3d(self, start, end, color=GOLD, thickness=0.018) -> Line3D:
        return Line3D(start=start, end=end, thickness=thickness, color=color)

    def construct(self):
        self.set_camera_orientation(phi=62 * DEGREES, theta=-46 * DEGREES, zoom=0.76, focal_distance=8.0)

        tokens = VGroup(
            self.token_box("king", GOLD),
            self.token_box("man", BLUE),
            self.token_box("woman", VIOLET),
            self.token_box("queen", GREEN),
        ).arrange(RIGHT, buff=0.24).move_to(UP * 1.45)
        tokens.set_opacity(0)
        self.add_fixed_in_frame_mobjects(tokens)
        self.play(LaggedStart(*[token.animate.set_opacity(1).shift(UP * 0.08) for token in tokens], lag_ratio=0.1), run_time=1.0)
        self.play(tokens.animate.shift(DOWN * 0.08), run_time=0.2)

        numeric_values = [
            [0.9, 0.2, 0.8, -0.1, 0.5],
            [0.2, 0.0, 0.1, 0.9, -0.3],
            [-0.1, 0.8, 0.2, 0.7, 0.3],
            [0.6, 0.9, 0.7, -0.2, 0.4],
        ]
        columns = VGroup(
            *[
                self.vector_column(values, color)
                for values, color in zip(numeric_values, [GOLD, BLUE, VIOLET, GREEN])
            ]
        ).arrange(RIGHT, buff=0.42).move_to(DOWN * 0.55)
        columns.set_opacity(0)
        self.add_fixed_in_frame_mobjects(columns)
        arrows_down = VGroup(
            *[
                Arrow(token.get_bottom() + DOWN * 0.05, col.get_top() + UP * 0.06, color=WHITE, stroke_width=4.2, buff=0)
                for token, col in zip(tokens, columns)
            ]
        )
        arrows_down.set_opacity(0)
        self.add_fixed_in_frame_mobjects(arrows_down)
        self.play(LaggedStart(*[arrow.animate.set_opacity(1) for arrow in arrows_down], lag_ratio=0.08), run_time=0.45)
        self.play(columns.animate.set_opacity(1), run_time=0.75)
        self.play(LaggedStart(*[col.animate.scale(1.035) for col in columns], lag_ratio=0.08), run_time=0.32)
        self.play(LaggedStart(*[col.animate.scale(1 / 1.035) for col in columns], lag_ratio=0.08), run_time=0.32)

        condensed_dots = VGroup(
            *[
                glow_dot(col.get_center(), color, radius=0.085)
                for col, color in zip(columns, [GOLD, BLUE, VIOLET, GREEN])
            ]
        )
        condensed_dots.set_opacity(0)
        self.add_fixed_in_frame_mobjects(condensed_dots)
        self.play(
            LaggedStart(
                *[
                    ReplacementTransform(col, dot.set_opacity(1))
                    for col, dot in zip(columns, condensed_dots)
                ],
                lag_ratio=0.08,
            ),
            FadeOut(arrows_down),
            FadeOut(tokens, shift=UP * 0.16),
            run_time=1.2,
        )
        self.wait(0.25)
        self.play(FadeOut(condensed_dots, scale=0.65), run_time=0.35)
        self.remove_fixed_in_frame_mobjects(tokens, columns, arrows_down, condensed_dots)
        self.remove(tokens, columns, arrows_down, condensed_dots)
        self.remove_fixed_in_frame_mobjects(condensed_dots)
        self.remove(condensed_dots)
        self.clear()

        axes = ThreeDAxes(
            x_range=(-3, 3, 1),
            y_range=(-2.4, 2.6, 1),
            z_range=(-2, 2, 1),
            x_length=6.5,
            y_length=5.2,
            z_length=4.0,
            axis_config={"color": AXIS, "stroke_width": 7.5, "include_ticks": False},
        ).shift(DOWN * 0.4)
        grid = NumberPlane(
            x_range=(-3, 3, 1),
            y_range=(-2.5, 2.5, 1),
            x_length=6.5,
            y_length=5.2,
            background_line_style={"stroke_color": "#31476D", "stroke_width": 1.5, "stroke_opacity": 0.58},
            axis_config={"stroke_opacity": 0},
        ).rotate(90 * DEGREES, axis=RIGHT).move_to(axes.c2p(0, 0, -1.05))

        coords = {
            "man": (-2.25, -1.15, 0.05),
            "king": (-0.55, 1.20, 0.60),
            "woman": (0.35, -1.25, -0.25),
            "prediction": (2.05, 1.10, 0.30),
            "queen": (2.35, 1.30, 0.52),
        }
        colors = {"king": GOLD, "man": BLUE, "woman": VIOLET, "prediction": CYAN, "queen": GREEN}
        label_offsets = {
            "man": LEFT * 0.70 + UP * 1.04,
            "king": RIGHT * 0.56 + UP * 0.84,
            "woman": LEFT * 1.04 + DOWN * 0.96,
            "prediction": RIGHT * 0.62 + DOWN * 1.18,
            "queen": RIGHT * 0.70 + UP * 0.76,
        }
        word_points = VGroup()
        for word in ["man", "king", "woman", "queen"]:
            coord = coords[word]
            group = self.point_label(word, colors[word], label_offsets[word])
            group.move_to(axes.c2p(*coord))
            group.set_opacity(0)
            word_points.add(group)
            self.add_fixed_orientation_mobjects(group[2])

        self.play(Create(grid), Create(axes), run_time=1.1)
        self.play(
            LaggedStart(
                *[FadeIn(point.set_opacity(1), scale=1.2) for point in word_points],
                lag_ratio=0.12,
            ),
            run_time=1.8,
        )

        origin = axes.c2p(0, 0, 0)
        position_vectors = VGroup(
            self.vector_line3d(origin, axes.c2p(*coords["man"]), BLUE, thickness=0.018),
            self.vector_line3d(origin, axes.c2p(*coords["king"]), GOLD, thickness=0.018),
            self.vector_line3d(origin, axes.c2p(*coords["woman"]), VIOLET, thickness=0.018),
            self.vector_line3d(origin, axes.c2p(*coords["queen"]), GREEN, thickness=0.018),
        )
        self.play(LaggedStart(*[Create(vector) for vector in position_vectors], lag_ratio=0.08), run_time=1.15)
        clean_word_labels = VGroup()
        for word in ["man", "king", "woman", "queen"]:
            label = self.spatial_label(word, colors[word], font_size=34)
            label.move_to(axes.c2p(*coords[word]) + label_offsets[word])
            label.set_opacity(0)
            clean_word_labels.add(label)
            self.add_fixed_orientation_mobjects(label)
        self.play(FadeOut(word_points, scale=0.72), FadeIn(clean_word_labels), run_time=0.55)
        self.remove(word_points)
        clean_word_labels.set_opacity(1)
        self.add_fixed_orientation_mobjects(*clean_word_labels)
        self.add(clean_word_labels)
        word_points = clean_word_labels

        anchor_points = VGroup(
            Dot3D(point=axes.c2p(*coords["man"]), radius=0.055, color=BLUE, resolution=(12, 12)),
            Dot3D(point=axes.c2p(*coords["king"]), radius=0.055, color=GOLD, resolution=(12, 12)),
            Dot3D(point=axes.c2p(*coords["woman"]), radius=0.055, color=VIOLET, resolution=(12, 12)),
            Dot3D(point=axes.c2p(*coords["queen"]), radius=0.055, color=GREEN, resolution=(12, 12)),
        )
        anchor_points.set_opacity(0)
        self.play(FadeOut(position_vectors), FadeIn(anchor_points.set_opacity(1), scale=1.2), run_time=0.5)
        self.play(
            axes.animate.set_opacity(0.28),
            grid.animate.set_opacity(0.08),
            anchor_points.animate.set_opacity(1),
            run_time=0.45,
        )

        man = axes.c2p(*coords["man"])
        king = axes.c2p(*coords["king"])
        woman = axes.c2p(*coords["woman"])
        queen = axes.c2p(*coords["queen"])
        prediction = axes.c2p(*coords["prediction"])
        role_arrow = self.vector_arrow3d(man, king, color=GOLD, thickness=0.018, height=0.13, base_radius=0.04)
        copied_arrow = self.vector_arrow3d(woman, prediction, color=GOLD, thickness=0.018, height=0.13, base_radius=0.04)
        self.play(Create(role_arrow), run_time=1.2)
        self.play(Indicate(word_points[2], color=VIOLET, scale_factor=1.08), run_time=0.7)
        moving_copy = role_arrow.copy()
        self.play(TransformFromCopy(role_arrow, moving_copy), run_time=0.6)
        self.play(Transform(moving_copy, copied_arrow), run_time=1.0)

        predicted_point = self.spatial_label("pred.", CYAN, font_size=34).move_to(prediction + label_offsets["prediction"])
        predicted_point.set_opacity(0)
        self.add_fixed_orientation_mobjects(predicted_point)
        near_line = DashedLine(prediction, queen, color=GREEN, stroke_width=6.0, dash_length=0.07).set_opacity(0.95)
        near_line_glow = near_line.copy().set_stroke(GREEN, width=13, opacity=0.18)
        self.play(
            FadeIn(predicted_point.set_opacity(1), scale=1.18),
            Create(near_line_glow),
            Create(near_line),
            Indicate(word_points[3], color=GREEN, scale_factor=1.08),
            run_time=1.05,
        )

        equation = self.equation_group()
        equation.scale(0.98).to_edge(DOWN).shift(UP * 0.58)
        for piece in equation:
            piece.set_opacity(0)
        self.add_fixed_in_frame_mobjects(*equation)
        self.play(
            LaggedStart(
                *[FadeIn(piece.set_opacity(1), shift=UP * 0.06) for piece in equation],
                lag_ratio=0.12,
            ),
            run_time=1.05,
        )

        self.move_camera(phi=68 * DEGREES, theta=-60 * DEGREES, zoom=0.84, focal_distance=8.0, run_time=2.2)
        self.wait(0.5)
