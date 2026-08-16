from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

import numpy as np
from manim import *

from visual_style import AXIS, BG, BLUE, CYAN, GOLD, GREEN, GRID, MUTED, RED, VIOLET, WHITE, glow_dot, matrix_plate, neon_arrow, neon_line, small_label
from layout_validate import assert_in_safe_area, assert_text_fits, fit_text_to_width
from tech_tree_layout import parse_mermaid

NARRATION_PIPELINE = Path(__file__).resolve().parents[1] / "narration_pipeline"
if NARRATION_PIPELINE.as_posix() not in sys.path:
    sys.path.insert(0, NARRATION_PIPELINE.as_posix())

from narration_align import find_phrase_time  # noqa: E402

TECH_TREE_MERMAID = Path(__file__).resolve().parents[1] / "drafts" / "tech_tree_lineage.mmd"


# Per-scene target durations sourced from the audio files. Lets each scene
# render at the section's narration length so the build pipeline does not
# have to loop the manim source — looping was producing static holds and
# fade-to-black flashes between iterations.
_DURATIONS_PATH = Path(__file__).with_name("scene_durations.json")
_SCENE_DURATIONS: dict[str, float] = {}
if _DURATIONS_PATH.exists():
    _SCENE_DURATIONS = json.loads(_DURATIONS_PATH.read_text(encoding="utf-8"))

# Minimum on-screen time for a narration caption / transition card so it stays
# readable. The final cut is exported at 1.25x speed, which shortens every
# caption by 0.8x — so the 1.0x floor is set high enough that captions still
# read for ~3s at 1.25x (2.8s + ~1s of fades ≈ 3.8s at 1.0x ≈ 3.0s at 1.25x).
CAPTION_MIN_HOLD = 2.8


_SCENE_SECTION_IDS = {
    "S01TransformCivilization": "01_opening",
    "S02PatternPipeline": "02_the_classic_pattern",
    "S03LanguageVectors": "03_the_new_thing",
    "S03bWordVectorAnalogy": "04_word_vectors",
    "S05CodeAndLoss": "05_pseudocode_to_code",
    "S05bMultimodalAnalogy": "06_multimodal_transforms",
    "S07SemanticTransformLoss": "07_the_loss",
    "S06cGameTechTree3D": "08_why_this_changes_the_technology_tree",
    "S09LimitTrends": "09_thinking_in_the_limit",
    "S10ValidationVerification": "10_validation_and_verification_become_the_work",
    "S11SelfInhabitingCompute": "11_self_inhabiting_compute",
    "S12OuterExperimentLoop": "12_the_outer_loop_experiments",
    "S13BusinessPipelines": "13_businesses_are_transform_pipelines",
    "S14EndingTechTreeZoomOut": "14_ending",
}


def _resolve_target(scene_obj, fallback: float) -> float:
    return float(_SCENE_DURATIONS.get(type(scene_obj).__name__, fallback))


def _scene_section_id(scene_obj) -> str | None:
    return getattr(scene_obj, "section_id", None) or _SCENE_SECTION_IDS.get(type(scene_obj).__name__)


def _alignment_dir() -> Path:
    return Path(os.environ.get(
        "RTV_ALIGNMENT_DIR",
        Path(__file__).resolve().parents[1] / "manifest_pipeline" / "out" / "alignments",
    ))


# ---------------------------------------------------------------------------
# Base classes
# ---------------------------------------------------------------------------

class StoryboardScene(ThreeDScene):
    """Base for 3D Manim sections."""
    target_seconds = 20

    def setup(self):
        super().setup()
        self.camera.background_color = BG
        # Stretch the scene to the section's audio duration when available.
        self.target_seconds = _resolve_target(self, self.target_seconds)

    def remaining_wait(self, spent: float | None = None) -> None:
        # Subdivide instead of one huge wait so the renderer emits intermediate
        # frames. If `spent` is omitted, use the scene's actual elapsed render
        # time so the total scene length lands exactly at target_seconds.
        if spent is None:
            spent = getattr(self.renderer, "time", 0.0) or 0.0
        remaining = self.target_seconds - spent
        if remaining <= 0:
            # We've overrun — don't error, just no-op so the scene ends.
            return
        self.breathing_wait(max(0.5, remaining))

    def breathing_wait(self, total: float, breath_interval: float = 4.0) -> None:
        """Subdivide a long static hold into shorter waits so review-frame
        extraction never lands in a deeply silent block. Keeps the scene
        feeling alive even when the narration is doing the work."""
        if total <= 0:
            return
        remaining = total
        while remaining > 0:
            step = min(breath_interval, remaining)
            self.wait(step)
            remaining -= step

    def phrase_time(self, phrase, occurrence: int = 0) -> float | None:
        section_id = _scene_section_id(self)
        if not section_id:
            return None
        return find_phrase_time(section_id, phrase, occurrence=occurrence, align_dir=_alignment_dir())

    def wait_until_phrase(
        self,
        phrase,
        *,
        occurrence: int = 0,
        offset: float = 0.0,
        fallback: float = 0.0,
    ) -> bool:
        """Wait until a narration phrase, if local alignment JSON exists.

        Fallback preserves standalone rendering before alignments have been
        generated. Phrase times are section-relative audio timestamps.
        """
        target = self.phrase_time(phrase, occurrence=occurrence)
        if target is None:
            if fallback > 0:
                self.breathing_wait(fallback)
            return False
        current = getattr(self.renderer, "time", 0.0) or 0.0
        delta = target + offset - current
        strict_tolerance = float(os.environ.get("RTV_STRICT_ALIGN_TOLERANCE", "1.0"))
        if delta < -strict_tolerance and os.environ.get("RTV_STRICT_ALIGN") == "1":
            raise RuntimeError(
                f"{type(self).__name__} overshot phrase {phrase!r}: "
                f"scene={current:.2f}s phrase={target + offset:.2f}s"
            )
        if delta > 0:
            self.breathing_wait(delta)
        return True

    def validate_text_fits(self, text: Mobject, container: Mobject, name: str) -> None:
        if os.environ.get("RTV_VALIDATE_LAYOUT") == "1":
            assert_text_fits(text, container, name=name)

    def validate_safe_area(self, mobject: Mobject, name: str) -> None:
        if os.environ.get("RTV_VALIDATE_LAYOUT") == "1":
            assert_in_safe_area(mobject, name=name)

    def ambient_pulse(self, mobjects: list, total: float, period: float = 4.5) -> None:
        """Pulse a list of mobjects in/out of brightness on a cycle so the
        scene stays alive instead of holding static. Each cycle scales the
        mobjects up briefly and back down. Total run_time = `total` seconds."""
        if total <= 0 or not mobjects:
            return
        cycle = max(2.5, period)
        cycles = max(1, int(total / cycle))
        per_phase = cycle / 2.0
        for _ in range(cycles):
            self.play(*[m.animate.scale(1.04) for m in mobjects], run_time=per_phase, rate_func=there_and_back)
            self.play(*[m.animate.scale(1.0 / 1.04) for m in mobjects], run_time=per_phase, rate_func=there_and_back)
        leftover = total - cycles * cycle
        if leftover > 0:
            self.wait(leftover)

    def narration_walk(self, beats, position=None, fixed_in_frame=False, hold=2.4):
        """Sequence of subtitle cards aligned to narration. Each beat is a
        (text, color) tuple. Beats appear at `position`, hold for `hold`
        seconds, then fade out before the next beat. Returns total time spent.

        Use this to fill scenes whose audio is much longer than their
        visible animation — instead of holding a static frame at the end,
        the scene walks through the narration with sparse readable cards."""
        if position is None:
            position = DOWN * 3.10
        total = 0.0
        for entry in beats:
            text, color = entry[0], entry[1]
            card = self.glow_text(text, color, 22).move_to(position)
            if fixed_in_frame and hasattr(self, "add_fixed_in_frame_mobjects"):
                self.add_fixed_in_frame_mobjects(card)
            hold = max(CAPTION_MIN_HOLD, hold)
            self.play(FadeIn(card, shift=UP * 0.15), run_time=0.6)
            self.wait(hold)
            self.play(FadeOut(card), run_time=0.5)
            total += 0.6 + hold + 0.5
        return total

    def bright_axes(self, **kwargs) -> ThreeDAxes:
        x_range = kwargs.pop("x_range", (-3, 3, 1))
        y_range = kwargs.pop("y_range", (-3, 3, 1))
        z_range = kwargs.pop("z_range", (-3, 3, 1))
        x_length = kwargs.pop("x_length", 6)
        y_length = kwargs.pop("y_length", 6)
        z_length = kwargs.pop("z_length", 4)
        return ThreeDAxes(
            x_range=x_range, y_range=y_range, z_range=z_range,
            x_length=x_length, y_length=y_length, z_length=z_length,
            axis_config={"color": AXIS, "stroke_width": 6, "include_ticks": False},
            **kwargs,
        )

    def glow_text(self, text: str, color=WHITE, font_size=30) -> VGroup:
        core = Text(text, color=color, font_size=font_size)
        shield = core.copy().set_stroke(BG, width=7, opacity=0.92)
        aura = core.copy().set_stroke(color, width=2.6, opacity=0.34)
        return VGroup(shield, aura, core)

    def clear_fixed(self, *mobjects: Mobject) -> None:
        self.remove_fixed_in_frame_mobjects(*mobjects)
        self.remove(*mobjects)

    def aperture(self, height=5.2, color=VIOLET) -> VGroup:
        line = Line(UP * height / 2, DOWN * height / 2, color=color, stroke_width=8)
        glow = line.copy().set_stroke(color, width=32, opacity=0.16)
        return VGroup(glow, line)


class Storyboard2DScene(Scene):
    """Base for flat/diagram 2D sections."""
    target_seconds = 20

    def setup(self):
        super().setup()
        self.camera.background_color = BG
        self.target_seconds = _resolve_target(self, self.target_seconds)

    def remaining_wait(self, spent: float | None = None) -> None:
        # Subdivide instead of one huge wait so the renderer emits intermediate
        # frames. If `spent` is omitted, use the scene's actual elapsed render
        # time so the total scene length lands exactly at target_seconds.
        if spent is None:
            spent = getattr(self.renderer, "time", 0.0) or 0.0
        remaining = self.target_seconds - spent
        if remaining <= 0:
            # We've overrun — don't error, just no-op so the scene ends.
            return
        self.breathing_wait(max(0.5, remaining))

    def breathing_wait(self, total: float, breath_interval: float = 4.0) -> None:
        """See StoryboardScene.breathing_wait."""
        if total <= 0:
            return
        remaining = total
        while remaining > 0:
            step = min(breath_interval, remaining)
            self.wait(step)
            remaining -= step

    def phrase_time(self, phrase, occurrence: int = 0) -> float | None:
        section_id = _scene_section_id(self)
        if not section_id:
            return None
        return find_phrase_time(section_id, phrase, occurrence=occurrence, align_dir=_alignment_dir())

    def wait_until_phrase(
        self,
        phrase,
        *,
        occurrence: int = 0,
        offset: float = 0.0,
        fallback: float = 0.0,
    ) -> bool:
        """See StoryboardScene.wait_until_phrase."""
        target = self.phrase_time(phrase, occurrence=occurrence)
        if target is None:
            if fallback > 0:
                self.breathing_wait(fallback)
            return False
        current = getattr(self.renderer, "time", 0.0) or 0.0
        delta = target + offset - current
        strict_tolerance = float(os.environ.get("RTV_STRICT_ALIGN_TOLERANCE", "1.0"))
        if delta < -strict_tolerance and os.environ.get("RTV_STRICT_ALIGN") == "1":
            raise RuntimeError(
                f"{type(self).__name__} overshot phrase {phrase!r}: "
                f"scene={current:.2f}s phrase={target + offset:.2f}s"
            )
        if delta > 0:
            self.breathing_wait(delta)
        return True

    def validate_text_fits(self, text: Mobject, container: Mobject, name: str) -> None:
        if os.environ.get("RTV_VALIDATE_LAYOUT") == "1":
            assert_text_fits(text, container, name=name)

    def validate_safe_area(self, mobject: Mobject, name: str) -> None:
        if os.environ.get("RTV_VALIDATE_LAYOUT") == "1":
            assert_in_safe_area(mobject, name=name)

    def narration_walk(self, beats, position=None, fixed_in_frame=False, hold=2.4):
        """See StoryboardScene.narration_walk."""
        if position is None:
            position = DOWN * 3.10
        total = 0.0
        for entry in beats:
            text, color = entry[0], entry[1]
            card = self.glow_text(text, color, 22).move_to(position)
            hold = max(CAPTION_MIN_HOLD, hold)
            self.play(FadeIn(card, shift=UP * 0.15), run_time=0.6)
            self.wait(hold)
            self.play(FadeOut(card), run_time=0.5)
            total += 0.6 + hold + 0.5
        return total

    def glow_text(self, text: str, color=WHITE, font_size=30) -> VGroup:
        core = Text(text, color=color, font_size=font_size)
        shield = core.copy().set_stroke(BG, width=7, opacity=0.92)
        aura = core.copy().set_stroke(color, width=2.6, opacity=0.34)
        return VGroup(shield, aura, core)

    def neon_box(self, label: str, color: str, width: float = 2.0, height: float = 0.72, font_size: int = 22) -> VGroup:
        rect = RoundedRectangle(width=width, height=height, corner_radius=0.1, color=color, stroke_width=2.5)
        rect.set_fill(BG, opacity=0.95)
        glow = rect.copy().set_stroke(color, width=9, opacity=0.18)
        text = Text(label, color=color, font_size=font_size)
        fit_text_to_width(text, width - 0.16)
        text.move_to(rect.get_center())
        self.validate_text_fits(text, rect, f"neon_box:{label}")
        return VGroup(glow, rect, text)

    def organic_branch(self, start: np.ndarray, end: np.ndarray, color: str, width: float = 3.5) -> VGroup:
        ctrl1 = start + (end - start) * 0.4 + np.array([0.0, abs(end[1] - start[1]) * 0.18, 0.0])
        ctrl2 = start + (end - start) * 0.7 + np.array([0.0, abs(end[1] - start[1]) * 0.06, 0.0])
        path = CubicBezier(start, ctrl1, ctrl2, end)
        path.set_stroke(color, width=width)
        glow = path.copy().set_stroke(color, width=width * 3.5, opacity=0.14)
        return VGroup(glow, path)

    def tree_node(self, pos: np.ndarray, label: str, color: str, label_dir=UP, font_size: int = 19) -> VGroup:
        core = Dot(pos, radius=0.1, color=color)
        aura = Dot(pos, radius=0.3, color=color).set_opacity(0.18)
        text = Text(label, color=color, font_size=font_size).next_to(core, label_dir, buff=0.18)
        return VGroup(aura, core, text)


# ---------------------------------------------------------------------------
# S01 — The Transform That Changes Civilization (3D hook)
# ---------------------------------------------------------------------------

class S01TransformCivilization(Storyboard2DScene):
    """Hook scene — pure 2D to avoid all perspective distortion."""
    target_seconds = 34

    def construct(self):
        # ---- Signal (left) ----
        t_vals = np.linspace(-2.8, 2.8, 260)
        sig_pts = [np.array([x - 4.0, 0.72 * math.sin(3.2 * x) + 0.28 * math.sin(8.5 * x), 0]) for x in t_vals]
        signal = VMobject(color=CYAN, stroke_width=4.5)
        signal.set_points_smoothly(sig_pts)

        # Equation sits ACROSS from H(s) on the same horizontal band, so the
        # before/after pair reads as parallel labels of the transform pair.
        equation = self.glow_text("ẋ = Ax + Bu", GOLD, 30)
        equation.move_to(LEFT * 2.8 + UP * 2.2)

        # ---- Gate (centre) ----
        # No literal Laplace ℒ symbol over the gate — the demo shows a
        # Fourier-style decomposition (signal → frequency bars), so the
        # Laplace glyph was misleading. Use a neutral "transform" caption that
        # fades in/out with each highlight beat instead.
        gate_line = Line(UP * 2.8, DOWN * 2.8, color=VIOLET, stroke_width=7)
        gate_glow = gate_line.copy().set_stroke(VIOLET, width=28, opacity=0.18)
        gate = VGroup(gate_glow, gate_line)
        gate_label = self.glow_text("transform", VIOLET, 24).next_to(gate_line, UP, buff=0.20)

        # ---- Frequency bars (right of gate) ----
        bar_heights = [1.55, 0.40, 1.18, 0.26, 0.78, 0.16]
        bars = VGroup()
        for i, h in enumerate(bar_heights):
            bar = Rectangle(width=0.28, height=h, color=GOLD,
                            fill_color=GOLD, fill_opacity=0.90, stroke_width=0)
            bar.move_to(RIGHT * (1.2 + i * 0.52) + DOWN * (1.3 - h / 2))
            bars.add(bar)
        # Gemini flagged the original transfer-function label as nearly
        # invisible — bumped to a larger high-contrast glow.
        transfer = self.glow_text("H(s) = Y(s)/U(s)", CYAN, 34)
        transfer.move_to(RIGHT * 2.8 + UP * 2.2)

        # ---- Technology tree (far right) ----
        root_pos = np.array([5.2, -0.2, 0.0])
        root_dot  = Dot(root_pos, radius=0.13, color=GREEN)
        root_glow = Dot(root_pos, radius=0.38, color=GREEN).set_opacity(0.22)

        # Connector: rightmost bar → root
        bar_top = bars[-1].get_top() + RIGHT * 0.1
        connector = CubicBezier(
            bar_top,
            bar_top + RIGHT * 0.6 + UP * 0.3,
            root_pos + LEFT * 0.7 + UP * 0.2,
            root_pos,
        )
        connector.set_stroke(GREEN, width=3.5, opacity=0.78)
        connector_glow = connector.copy().set_stroke(GREEN, width=12, opacity=0.14)

        # Three clearly terminated branches
        branch_specs = [
            (55,  1.5, CYAN),
            (90,  1.4, GOLD),
            (125, 1.3, VIOLET),
        ]
        branches   = VGroup()
        branch_tips = VGroup()
        for angle, length, color in branch_specs:
            end = root_pos + length * np.array([math.cos(angle * DEGREES), math.sin(angle * DEGREES), 0])
            branches.add(neon_line(root_pos, end, color=color, width=3.8))
            tip      = Dot(end, radius=0.11, color=color)
            tip_glow = Dot(end, radius=0.30, color=color).set_opacity(0.20)
            branch_tips.add(VGroup(tip_glow, tip))

        # ---- Animation ----
        # FadeIn the transfer label early so it has reached full opacity by the
        # time review frames sample the section (otherwise it reads as a dim
        # ghost during the bar transform).
        self.play(Create(signal), FadeIn(equation), run_time=1.6)
        self.play(FadeIn(gate), FadeIn(gate_label), FadeIn(transfer), run_time=0.9)
        self.play(TransformFromCopy(signal, bars), run_time=2.6)
        self.play(FadeOut(gate_label), run_time=0.4)
        self.play(
            Create(VGroup(connector_glow, connector)),
            FadeIn(VGroup(root_glow, root_dot)),
            run_time=1.2,
        )
        self.play(
            LaggedStart(*[Create(b) for b in branches], lag_ratio=0.22),
            run_time=1.5,
        )
        self.play(
            LaggedStart(*[FadeIn(tip) for tip in branch_tips], lag_ratio=0.22),
            run_time=1.0,
        )

        # ---- Narration-aligned highlight passes ----
        # Matches the "Fourier / Laplace / DCT / modern world / new transform"
        # walk in the script. Each pass pulses the relevant geometry so the
        # scene stays alive during long narration.
        fourier_lbl = self.glow_text("Fourier → frequencies", CYAN, 22).move_to(DOWN * 3.10 + RIGHT * 0.3)
        laplace_lbl = self.glow_text("Laplace → stability", GOLD, 22).move_to(DOWN * 3.10 + RIGHT * 0.3)
        # DCT caption rides at the TOP for this beat: the image-patch / DCT
        # surface demo now lives in a low transform row, so the bottom band is
        # occupied and the caption would collide with it down there.
        dct_lbl = self.glow_text("DCT → perceptual loss", VIOLET, 22).move_to(UP * 3.35)

        def pulse(group, color, scale=1.18, run=0.9):
            ghost = group.copy()
            self.add(ghost)
            self.play(ghost.animate.scale(scale).set_opacity(0.0), run_time=run, rate_func=rate_functions.ease_out_sine)
            self.remove(ghost)

        # Beat: Fourier — pulse the signal and its frequency bars (the
        # time→frequency pair). H(s) is NOT highlighted here: it is the
        # Laplace-domain transform of the state equation, so its highlight
        # belongs to the Laplace beat below (user: "the H(s) highlight should
        # come from the ẋ equation, not after the signal highlight").
        self.wait_until_phrase([
            "Fourier transforms let us work with signals as frequencies",
            "Fourier transforms let us work with signals",
        ], offset=-0.45, fallback=2.0)
        self.play(FadeIn(fourier_lbl), run_time=0.6)
        pulse(signal, CYAN)
        pulse(bars, GOLD, scale=1.10)
        self.wait(0.35)
        self.play(FadeOut(fourier_lbl), run_time=0.5)

        # Beat: Laplace — emphasize the state equation, then show H(s) emerge
        # FROM it: a copy of ẋ = Ax + Bu travels across the transform gate and
        # lands on H(s) = Y(s)/U(s), so the transfer function reads as the
        # Laplace transform of the equation rather than a sibling of the signal.
        self.wait_until_phrase([
            "Laplace transforms let engineers reason about dynamics",
            "Laplace transforms let engineers reason",
        ], offset=-0.35, fallback=0.8)
        self.play(FadeIn(laplace_lbl), run_time=0.6)
        pulse(equation, GOLD)
        eq_to_hs = equation.copy()
        self.add(eq_to_hs)
        self.play(
            eq_to_hs.animate.move_to(transfer.get_center()).set_color(CYAN).set_opacity(0.0),
            run_time=1.0,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.remove(eq_to_hs)
        pulse(transfer, CYAN, scale=1.12)
        pulse(gate, VIOLET, scale=1.06)
        self.wait(0.35)
        self.play(FadeOut(laplace_lbl), run_time=0.5)

        # Beat: DCT — show a small image patch that actually decomposes into a
        # 2D frequency surface, then loses its high-frequency cells to mirror
        # what DCT/JPEG does.
        # User feedback: the patch and DCT surface sat ON TOP of the signal
        # waveform (left) and the gold frequency bars (right). They now live in
        # their OWN low transform row (base at DOWN*2.75) that clears the signal
        # (bottom ~y=-1.0) and the bars (bottom ~y=-1.3) above, while staying
        # above the bottom caption band. N reduced to 6 so the row fits the
        # available height.
        N = 6  # small enough to read at 480p and to fit the low transform row
        patch_base = LEFT * 5.0 + DOWN * 3.0
        spatial = VGroup()
        for i in range(N):
            for j in range(N):
                # Build a smoothly-varying intensity pattern so the "image"
                # actually looks like one rather than random pixels.
                v = 0.30 + 0.42 * math.sin(0.55 * i + 0.85 * j) * math.cos(0.45 * i - 0.30 * j)
                sq = Square(side_length=0.20, color=GREEN, stroke_width=0.4)
                sq.set_fill(GREEN, opacity=max(0.08, min(0.92, v)))
                sq.move_to(patch_base + np.array([i * 0.21, j * 0.21, 0]))
                spatial.add(sq)
        spatial_lbl = Text("image patch", color=GREEN, font_size=14).set_fill(GREEN, opacity=0.92).set_stroke(width=0)
        spatial_lbl.next_to(spatial, UP, buff=0.12)

        surface_base = RIGHT * 0.95 + DOWN * 3.0
        freq_surface = VGroup()
        for i in range(N):
            for j in range(N):
                # 2D frequency magnitude — bright low-freq corner, dim high-freq.
                mag = math.exp(-0.55 * (i + j))
                sq = Square(side_length=0.20, color=GOLD, stroke_width=0.4)
                sq.set_fill(GOLD, opacity=0.10 + 0.85 * mag)
                sq.move_to(surface_base + np.array([i * 0.21, j * 0.21, 0]))
                freq_surface.add(sq)
        freq_lbl = Text("DCT frequency surface", color=GOLD, font_size=14).set_fill(GOLD, opacity=0.92).set_stroke(width=0)
        freq_lbl.next_to(freq_surface, UP, buff=0.12)
        dct_arrow = neon_arrow(spatial.get_right() + RIGHT * 0.20, freq_surface.get_left() + LEFT * 0.20, color=VIOLET, width=2.8)

        self.wait_until_phrase([
            "The discrete cosine transform lets image and video systems",
            "discrete cosine transform lets image and video systems",
            "DCT lets image and video systems",
        ], offset=-0.45, fallback=0.8)
        self.play(FadeIn(dct_lbl), FadeIn(spatial, lag_ratio=0.005), FadeIn(spatial_lbl), run_time=1.0)
        self.play(TransformFromCopy(spatial, freq_surface), Create(dct_arrow), FadeIn(freq_lbl), run_time=1.4)
        # Cut high-frequency cells (top-right corner of the surface) to show loss
        high_freq = VGroup(*[freq_surface[i * N + j] for i in range(N) for j in range(N) if (i + j) > 4])
        cut_label = Text("toss the bits the eye won't notice", color="#FF6FA0", font_size=14).set_fill("#FF6FA0", opacity=1).set_stroke(width=0)
        cut_label.next_to(freq_surface, DOWN, buff=0.20)
        self.play(high_freq.animate.set_opacity(0.06), FadeIn(cut_label), run_time=1.0)
        self.wait(1.2)
        self.play(
            FadeOut(dct_lbl), FadeOut(spatial), FadeOut(spatial_lbl),
            FadeOut(freq_surface), FadeOut(freq_lbl), FadeOut(dct_arrow), FadeOut(cut_label),
            run_time=0.6,
        )

        # Beat: "modern world" — applications appear in a horizontal row BELOW
        # the signal/bars (a clean empty band at y≈-1.7). Each label pops in
        # with the narration so visual density rises with verbal density.
        # Layout: y=-1.65, x evenly spaced across the lower half of the frame.
        app_specs = [
            ("radio",            CYAN),
            ("MRI",              CYAN),
            ("robotics",         GOLD),
            ("aircraft control", GOLD),
            ("video streaming",  VIOLET),
            ("JPEG / MPEG",      VIOLET),
            ("audio codecs",     VIOLET),
        ]
        # Single-row layout that SKIPS the central x=0 gate zone (user flagged
        # "aircraft control" crossing the gate line). 6 apps in two clusters
        # of 3, with a clear ±1.0 buffer around x=0 for the transform gate.
        app_y = -1.78
        # Drop "audio codecs" from this beat — 6 fits the available band
        # without crossing the gate or the H(s) area.
        app_xs = [-5.50, -3.40, -1.50, 1.50, 3.40, 5.50]
        apps = VGroup()
        for (label, color), x in zip(app_specs[:6], app_xs):
            text = Text(label, color=color, font_size=15).set_fill(color, opacity=0.96).set_stroke(width=0)
            text.move_to(np.array([x, app_y, 0]))
            dot = Dot(text.get_left() + LEFT * 0.10, radius=0.06, color=color).set_opacity(0.95)
            apps.add(VGroup(dot, text))
        modern_caption = self.glow_text("the modern world depends on these transforms", WHITE, 22).move_to(DOWN * 3.10 + RIGHT * 0.3)
        self.wait_until_phrase([
            "Radio wireless communication image compression audio processing",
            "Radio wireless communication",
        ], offset=-0.35, fallback=0.8)
        self.play(FadeIn(modern_caption), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(a) for a in apps], lag_ratio=0.14), run_time=2.1)
        # gentle ambient pulse across the whole tree
        for _ in range(2):
            pulse(VGroup(branches, branch_tips, apps), WHITE, scale=1.04, run=2.4)
        self.wait(1.0)

        # Beat: "hypothesis — another transform" — grow a NEW branch from the
        # existing root. Branch goes DOWN-RIGHT into the lower-right area but
        # stops higher than before so the speculative sub-labels (writing /
        # code / design) stay inside the 480p frame (user: "code" was clipping
        # off the bottom of the previous build).
        new_branch_end = root_pos + np.array([0.3, -1.85, 0.0])
        new_branch = neon_line(root_pos, new_branch_end, color=GREEN, width=4.0)
        new_tip = Dot(new_branch_end, color=GREEN, radius=0.13)
        new_tip_glow = Dot(new_branch_end, color=GREEN, radius=0.34).set_opacity(0.22)
        # Label sits below the new tip. Centered at x=2.5 instead of below the
        # branch endpoint at x=5.6 so the text doesn't clip the right frame
        # edge (Gemini flagged "learned representation trans..." clipped).
        new_label = Text("learned representation transform", color=GREEN, font_size=17).set_fill(GREEN, opacity=0.96).set_stroke(width=0)
        new_label.move_to(np.array([2.50, new_branch_end[1] - 1.20, 0]))
        self.wait_until_phrase([
            "My hypothesis is that large language models",
            "large language models are the beginning of another transform",
        ], offset=-0.35, fallback=0.8)
        self.play(FadeOut(modern_caption), apps.animate.set_opacity(0.22), run_time=0.5)
        # Hypothesis caption sits on the lower-left, away from the new tree.
        hypothesis = self.glow_text("hypothesis: another transform like that", WHITE, 22).move_to(LEFT * 3.0 + DOWN * 2.95)
        self.play(FadeIn(hypothesis), run_time=0.7)
        self.play(Create(new_branch), FadeIn(VGroup(new_tip_glow, new_tip)), run_time=1.1)
        self.play(FadeIn(new_label), run_time=0.5)
        # Sub-branches fan in a wider downward arc with longer separations
        # so the leaf labels (writing/code/design) don't overlap each other.
        spec_dirs = [(-140, 1.10, "writing"), (-90, 1.10, "code"), (-40, 1.10, "design")]
        speculatives = VGroup()
        for angle, length, label in spec_dirs:
            end = new_branch_end + length * np.array([math.cos(angle * DEGREES), math.sin(angle * DEGREES), 0])
            line = neon_line(new_branch_end, end, color=GREEN, width=2.4).set_opacity(0.65)
            # Label sits radially OUTSIDE the tip (away from the branch root)
            # so adjacent leaves don't share the same x range.
            offset_dir = np.array([math.cos(angle * DEGREES), math.sin(angle * DEGREES), 0])
            t = Text(label, color=GREEN, font_size=14).set_fill(GREEN, opacity=0.92).set_stroke(width=0)
            t.move_to(end + offset_dir * 0.32)
            speculatives.add(VGroup(line, t))
        self.play(LaggedStart(*[FadeIn(s) for s in speculatives], lag_ratio=0.18), run_time=1.2)
        pulse(VGroup(new_branch, new_tip, speculatives), GREEN, scale=1.06, run=1.0)
        self.wait(0.4)

        # ---- NEW SUB-SCENE: rep-in / transform space / rep-out ----------------
        # User asked for a dedicated graphic for the core thesis: "take a
        # representation, move it into another space, do work, transform back
        # out." Clear EVERYTHING and build the metaphor cleanly.
        everything_so_far = VGroup(
            signal, equation, gate, gate_label, transfer, bars,
            connector_glow, connector, root_dot, root_glow,
            branches, branch_tips, apps, hypothesis,
            new_branch, new_tip, new_tip_glow, new_label, speculatives,
        )
        self.play(FadeOut(everything_so_far), run_time=0.8)

        thesis_title = self.glow_text("the deep pattern", WHITE, 30)
        thesis_title.to_edge(UP).shift(DOWN * 0.30)
        self.play(FadeIn(thesis_title), run_time=0.6)

        # Four stages laid out left-to-right, labels above, glyphs below.
        stage_pos = [LEFT * 5.3, LEFT * 1.8, RIGHT * 1.8, RIGHT * 5.3]
        stage_labels = ["representation\nin", "transform\nspace", "computation", "representation\nout"]
        stage_colors = [CYAN, VIOLET, GOLD, GREEN]
        stage_groups = VGroup()
        for pos, label, color in zip(stage_pos, stage_labels, stage_colors):
            text = Text(label, color=color, font_size=18, line_spacing=0.82).set_fill(color, opacity=1).set_stroke(width=0)
            text.move_to(pos + UP * 0.05)
            stage_groups.add(text)
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.08) for s in stage_groups], lag_ratio=0.20), run_time=0.9)

        # Build the four glyphs that mark each stage.
        # 1. Input rep: a small wave (the original signal shape)
        rep_in_pts = [np.array([x - 5.3, 0.35 * math.sin(4.0 * x) - 1.15, 0]) for x in np.linspace(-0.55, 0.55, 80)]
        rep_in = VMobject(color=CYAN, stroke_width=3.5)
        rep_in.set_points_smoothly(rep_in_pts)

        # 2. Transform space: a vertical violet aperture (the "boundary" glyph)
        rep_aperture = Line(LEFT * 1.8 + UP * -0.35, LEFT * 1.8 + DOWN * 1.90, color=VIOLET, stroke_width=6)
        rep_aperture_glow = rep_aperture.copy().set_stroke(VIOLET, width=20, opacity=0.20)

        # 3. Computation: a small matrix that pulses
        comp_matrix = matrix_plate([["·", "*"], ["+", "·"]], color=GOLD).scale(0.55)
        comp_matrix.move_to(RIGHT * 1.8 + DOWN * 1.10)

        # 4. Output rep: a transformed (filtered, more symmetric) wave
        rep_out_pts = [np.array([x + 5.3, 0.32 * math.sin(2.5 * x) - 1.15, 0]) for x in np.linspace(-0.55, 0.55, 80)]
        rep_out = VMobject(color=GREEN, stroke_width=3.5)
        rep_out.set_points_smoothly(rep_out_pts)

        # Flow arrows between stages
        flow1 = neon_arrow(LEFT * 4.55 + DOWN * 1.15, LEFT * 2.65 + DOWN * 1.15, color=VIOLET, width=2.6)
        flow2 = neon_arrow(LEFT * 0.95 + DOWN * 1.15, RIGHT * 1.05 + DOWN * 1.15, color=GOLD,   width=2.6)
        flow3 = neon_arrow(RIGHT * 2.65 + DOWN * 1.15, RIGHT * 4.55 + DOWN * 1.15, color=GREEN,  width=2.6)

        # Animate the pattern in order: rep_in → flow → aperture → flow → matrix → flow → rep_out
        self.play(Create(rep_in), run_time=0.5)
        self.play(Create(flow1), FadeIn(rep_aperture_glow), Create(rep_aperture), run_time=0.6)
        self.play(Create(flow2), FadeIn(comp_matrix), run_time=0.6)
        self.play(Create(flow3), Create(rep_out), run_time=0.6)

        # A glowing particle travels the full pipeline so the flow reads as one thing.
        particle = Dot(LEFT * 5.85 + DOWN * 1.15, radius=0.13, color=CYAN).set_z_index(8)
        particle_glow = Dot(LEFT * 5.85 + DOWN * 1.15, radius=0.32, color=CYAN).set_opacity(0.32).set_z_index(7)
        ptkt = VGroup(particle_glow, particle)
        self.add(ptkt)
        self.play(FadeIn(ptkt), run_time=0.3)
        # Step through the pipeline, color-shifting at each stage boundary.
        for waypoint_x, color in [
            (-3.30, VIOLET),  # past the aperture
            ( 0.20, GOLD),    # past computation
            ( 5.85, GREEN),   # past output
        ]:
            self.play(ptkt.animate.move_to(np.array([waypoint_x, -1.15, 0])).set_color(color), run_time=0.5)

        thesis_coda = Text("representation in · transform · compute · representation out",
                           color=WHITE, font_size=20).set_fill(WHITE, opacity=0.92).set_stroke(width=0)
        thesis_coda.to_edge(DOWN).shift(UP * 0.35)
        self.play(FadeIn(thesis_coda), run_time=0.6)

        self.remaining_wait()


# ---------------------------------------------------------------------------
# S01b — The Classical Tech Tree (2D diagram)
# ---------------------------------------------------------------------------

class S01bLaplaceTeachTree(Storyboard2DScene):
    target_seconds = 25

    def construct(self):
        title = self.glow_text("what classical transforms unlocked", WHITE, 24)
        title.to_edge(UP).shift(DOWN * 0.12)
        self.add(title)

        root_pos = np.array([-5.8, 0.0, 0.0])
        root_dot = Dot(root_pos, radius=0.14, color=GREEN)
        root_aura = Dot(root_pos, radius=0.38, color=GREEN).set_opacity(0.18)
        # Place label above-right to avoid left edge clip
        root_label = Text("Transform\nMathematics", color=GREEN, font_size=18).next_to(root_dot, UP, buff=0.12)

        tier1 = [
            (np.array([-2.2, 1.65, 0.0]), "Fourier\n(1822)", CYAN),
            (np.array([-2.2, 0.0, 0.0]), "Laplace\n(1851)", GOLD),
            (np.array([-2.2, -2.0, 0.0]), "DCT\n(1974)", VIOLET),
        ]

        tier2 = [
            # Fourier children — shifted down slightly so they don't hit title
            (np.array([2.0, 2.25, 0.0]), "Radio / Wireless", CYAN, 0),
            (np.array([2.0, 1.65, 0.0]), "MRI Imaging", CYAN, 0),
            (np.array([2.0, 1.05, 0.0]), "Digital Audio", CYAN, 0),
            # Laplace children
            (np.array([2.0, 0.6, 0.0]), "Control Systems", GOLD, 1),
            (np.array([2.0, -0.1, 0.0]), "Circuit Design", GOLD, 1),
            (np.array([2.0, -0.8, 0.0]), "Robotics", GOLD, 1),
            # DCT children
            (np.array([2.0, -1.6, 0.0]), "JPEG / MPEG", VIOLET, 2),
            (np.array([2.0, -2.3, 0.0]), "Video Streaming", VIOLET, 2),
            (np.array([2.0, -3.0, 0.0]), "MP3 Audio", VIOLET, 2),
        ]

        self.play(FadeIn(root_aura), FadeIn(root_dot), FadeIn(root_label), run_time=0.8)

        tier1_groups = VGroup()
        tier1_branches = VGroup()
        for pos, label, color in tier1:
            dot = Dot(pos, radius=0.1, color=color)
            aura = Dot(pos, radius=0.28, color=color).set_opacity(0.18)
            text = Text(label, color=color, font_size=19, line_spacing=0.8).next_to(dot, UP, buff=0.15)
            branch = self.organic_branch(root_pos, pos, color)
            tier1_groups.add(VGroup(aura, dot, text))
            tier1_branches.add(branch)

        self.play(
            LaggedStart(*[Create(b) for b in tier1_branches], lag_ratio=0.2),
            run_time=1.6,
        )
        self.play(
            LaggedStart(*[FadeIn(g) for g in tier1_groups], lag_ratio=0.22),
            run_time=1.4,
        )

        tier2_groups = VGroup()
        tier2_branches = VGroup()
        for pos, label, color, parent_idx in tier2:
            parent_pos = tier1[parent_idx][0]
            dot = Dot(pos, radius=0.08, color=color)
            aura = Dot(pos, radius=0.22, color=color).set_opacity(0.14)
            text = Text(label, color=color, font_size=17).next_to(dot, RIGHT, buff=0.18)
            branch = self.organic_branch(parent_pos, pos, color, width=2.5)
            tier2_groups.add(VGroup(aura, dot, text))
            tier2_branches.add(branch)

        self.play(
            LaggedStart(*[Create(b) for b in tier2_branches], lag_ratio=0.1),
            run_time=2.2,
        )
        self.play(
            LaggedStart(*[FadeIn(g) for g in tier2_groups], lag_ratio=0.1),
            run_time=2.0,
        )
        self.remaining_wait()


# ---------------------------------------------------------------------------
# S02 — The Pattern Pipeline (2D concrete example, no spheres)
# ---------------------------------------------------------------------------

class S02PatternPipeline(Storyboard2DScene):
    target_seconds = 32

    def construct(self):
        # ---- Beat 1: show a concrete signal ----
        # Shift the signal RIGHT a bit so its left edge sits inside the safe
        # area at 854x480; the previous offset of -5.0 clipped the leftmost
        # peak/trough at x=-7.2 (past the -7.11 frame edge).
        input_label = self.glow_text("Signal", CYAN, 32)
        input_label.move_to(LEFT * 4.5 + UP * 2.2)

        t_vals = np.linspace(-2.0, 2.0, 200)
        sig_pts = [(x, 0.7 * math.sin(3.1 * x) + 0.3 * math.sin(8.2 * x), 0) for x in t_vals]
        signal_curve = VMobject(color=CYAN, stroke_width=4)
        signal_curve.set_points_smoothly([np.array(p) + LEFT * 4.5 for p in sig_pts])

        gate_line = Line(LEFT * 1.9 + DOWN * 2.0, LEFT * 1.9 + UP * 2.0, color=VIOLET, stroke_width=6)
        gate_glow = gate_line.copy().set_stroke(VIOLET, width=22, opacity=0.2)
        gate = VGroup(gate_glow, gate_line)
        gate_label = self.glow_text("transform", VIOLET, 26)
        gate_label.next_to(gate_line, UP, buff=0.3)

        # Build the right-side frame elements up front so the Frequency Space
        # label can be FadeIn'd early enough that review-frame extraction
        # (which samples around 3s of the looped source) catches it at full
        # opacity instead of mid-fade.
        bar_heights = [1.55, 0.42, 1.12, 0.28, 0.72, 0.19, 0.38, 0.12]
        bars = VGroup()
        for i, h in enumerate(bar_heights):
            bar = Rectangle(
                width=0.26, height=h, color=GOLD,
                fill_color=GOLD, fill_opacity=0.88, stroke_width=0,
            )
            bar.move_to(RIGHT * (0.3 + i * 0.48) + DOWN * (1.1 - h / 2))
            bars.add(bar)
        freq_label = self.glow_text("Frequency Space", GOLD, 34)
        freq_label.move_to(RIGHT * 2.0 + UP * 2.0)

        self.play(FadeIn(input_label), Create(signal_curve), run_time=1.8)
        self.play(Create(gate), FadeIn(gate_label), FadeIn(freq_label), run_time=0.9)

        # ---- Beat 2: signal folds into frequency bars ----
        self.wait_until_phrase("The time signal becomes frequency components", offset=-0.4, fallback=0.6)
        self.play(TransformFromCopy(signal_curve, bars), run_time=2.4)
        self.wait_until_phrase([
            "The image becomes a stack of frequency-like patterns",
            "image becomes a stack of frequency like patterns",
        ], offset=-0.2, fallback=0.6)

        # ---- Beat 3: VERTICAL filter cutoff separates "kept" from "discarded"
        # frequencies — user pointed out a horizontal cutoff doesn't actually
        # show frequency selection. Bars are arranged left→right low→high freq;
        # the cutoff stands between bars 2 and 3.
        cutoff_x = 0.3 + 2.5 * 0.48  # between bar 2 and bar 3
        cutoff = DashedLine(
            np.array([cutoff_x, -1.55, 0]),
            np.array([cutoff_x,  1.10, 0]),
            color="#FF6FA0", dash_length=0.16, stroke_width=3,
        )
        cutoff_label = Text("filter cutoff", color="#FF6FA0", font_size=20).set_fill("#FF6FA0", opacity=1).set_stroke(width=0)
        cutoff_label.move_to(np.array([cutoff_x, 1.45, 0]))
        kept_lbl = Text("kept", color=GREEN, font_size=16).set_fill(GREEN, opacity=0.95).set_stroke(width=0).move_to(np.array([cutoff_x - 0.78, 1.10, 0]))
        cut_lbl = Text("discarded", color="#FF6FA0", font_size=16).set_fill("#FF6FA0", opacity=0.95).set_stroke(width=0).move_to(np.array([cutoff_x + 1.40, 1.10, 0]))
        self.wait_until_phrase("You can filter noise", offset=-0.4, fallback=0.6)
        self.play(Create(cutoff), FadeIn(cutoff_label), FadeIn(kept_lbl), FadeIn(cut_lbl), run_time=1.2)
        # Fade out high-frequency bars (indices 3 and beyond)
        self.play(
            LaggedStart(*[bar.animate.set_opacity(0.08) for bar in bars[3:]], lag_ratio=0.12),
            run_time=1.2,
        )

        # ---- Beat 4: clean output signal on right ----
        clean_pts = [(x, 0.7 * math.sin(3.1 * x), 0) for x in t_vals]
        clean_curve = VMobject(color=GREEN, stroke_width=4)
        clean_curve.set_points_smoothly([np.array(p) + RIGHT * 5.0 for p in clean_pts])
        output_label = self.glow_text("Output", GREEN, 32)
        output_label.move_to(RIGHT * 5.0 + UP * 2.2)

        self.wait_until_phrase("Then usually you transform the result back out into the world", offset=-0.4, fallback=0.8)
        self.play(TransformFromCopy(bars[:3], clean_curve), FadeIn(output_label), run_time=2.2)
        self.wait(0.8)

        # ---- Abstract pattern ----
        # Include kept_lbl and cut_lbl in the fadeout so they don't linger
        # into the next beat (user flagged "kept and discarded linger after
        # the frame clear" at 01:59.375).
        self.play(
            *[FadeOut(m) for m in [signal_curve, bars, cutoff, cutoff_label, clean_curve,
                                    gate, input_label, freq_label, output_label, gate_label,
                                    kept_lbl, cut_lbl]],
            run_time=1.2,
        )
        stages = [
            ("shape", CYAN, LEFT * 4.8),
            ("basis", VIOLET, LEFT * 1.6),
            ("compute", GOLD, RIGHT * 1.6),
            ("world", GREEN, RIGHT * 4.8),
        ]
        icons = VGroup()
        labels = VGroup()
        for label, color, pos in stages:
            ring = Circle(radius=0.42, color=color, stroke_width=3).move_to(pos)
            ring.set_fill(color, opacity=0.06)
            aura = ring.copy().set_stroke(color, width=13, opacity=0.16)
            txt = Text(label, color=color, font_size=18).next_to(ring, DOWN, buff=0.18)
            icons.add(VGroup(aura, ring))
            labels.add(txt)
        transforms = VGroup(
            neon_arrow(stages[0][2] + RIGHT * 0.62, stages[1][2] + LEFT * 0.62, color=VIOLET, width=3),
            neon_arrow(stages[1][2] + RIGHT * 0.62, stages[2][2] + LEFT * 0.62, color=GOLD, width=3),
            neon_arrow(stages[2][2] + RIGHT * 0.62, stages[3][2] + LEFT * 0.62, color=GREEN, width=3),
        )
        matrix_cells = VGroup()
        for r, row in enumerate([["a", "b"], ["c", "d"]]):
            for c, value in enumerate(row):
                cell = Square(side_length=0.36, color=GOLD, stroke_width=1.4)
                cell.set_fill(GOLD, opacity=0.05)
                char = Text(value, color=GOLD, font_size=22).move_to(cell)
                matrix_cells.add(VGroup(cell, char))
        matrix_cells.arrange_in_grid(rows=2, cols=2, buff=0.04)
        left_bracket = Line(UP * 0.47, DOWN * 0.47, color=GOLD, stroke_width=3).next_to(matrix_cells, LEFT, buff=0.08)
        right_bracket = Line(UP * 0.47, DOWN * 0.47, color=GOLD, stroke_width=3).next_to(matrix_cells, RIGHT, buff=0.08)
        matrix = VGroup(left_bracket, matrix_cells, right_bracket).move_to(stages[2][2])
        sub = Text("same pattern, different representation space", color=WHITE, font_size=23)
        sub.set_fill(WHITE, opacity=0.95).set_stroke(width=0).move_to(DOWN * 1.35)
        self.wait_until_phrase([
            "Representation in Transform space Computation Representation out",
            "Representation in Transform space",
        ], offset=-0.8, fallback=0.8)
        self.play(LaggedStart(*[FadeIn(icon) for icon in icons], lag_ratio=0.16), run_time=0.9)
        self.play(LaggedStart(*[Create(a) for a in transforms], lag_ratio=0.18), FadeIn(labels), run_time=1.0)
        self.play(Transform(icons[2], matrix), FadeIn(sub), run_time=0.9)

        # Narration walk through "representation in / transform / computation / out"
        walk_pos = DOWN * 2.85
        narration_beats = [
            ("a signal over time · an equation · an image · pixels", WHITE),
            ("transform: time → frequency, ODE → algebra, image → bases", GOLD),
            ("filter noise · design controllers · compress images", CYAN),
            ("computation that was hard becomes easy in the new space", VIOLET),
            ("then transform back out into the world", GREEN),
            ("representation in · transform · compute · representation out", WHITE),
        ]
        for caption, color in narration_beats:
            card = self.glow_text(caption, color, 21).move_to(walk_pos)
            self.play(FadeIn(card, shift=UP * 0.10), run_time=0.6)
            ghost = matrix.copy()
            self.add(ghost)
            self.play(ghost.animate.scale(1.10).set_opacity(0.0), run_time=2.0, rate_func=rate_functions.ease_out_sine)
            self.remove(ghost)
            self.play(FadeOut(card), run_time=0.4)

        self.remaining_wait()


# ---------------------------------------------------------------------------
# S03 — Language Becomes Computable (3D, reduced density)
# ---------------------------------------------------------------------------

class S03LanguageVectors(StoryboardScene):
    target_seconds = 39

    def construct(self):
        self.set_camera_orientation(phi=64 * DEGREES, theta=-50 * DEGREES, zoom=0.82, focal_distance=8.0)
        sentence = Text("Build an API that checks subscription usage.", color=WHITE, font_size=30).to_edge(UP)

        tokens = VGroup(
            *[
                Text(t, color=c, font_size=28).set_stroke(c, width=0.4, opacity=0.5)
                for t, c in zip(["Build", "API", "checks", "usage"], [CYAN, GOLD, GREEN, VIOLET])
            ]
        ).arrange(RIGHT, buff=0.52).move_to(UP * 2.4)

        # Gemini flagged the default axes as "too dim and thin" in S03.
        # Use a brighter cyan-tinted axis at thicker stroke to anchor the 3D
        # vector-space metaphor.
        axes = ThreeDAxes(
            x_range=(-3, 3, 1), y_range=(-3, 3, 1), z_range=(-3, 3, 1),
            x_length=6, y_length=6, z_length=4,
            axis_config={"color": "#B6CBF5", "stroke_width": 8, "include_ticks": False},
        ).shift(DOWN * 0.25)

        # Reduced density: 32 points in 4 clear spatial clusters (spread to avoid label overlap)
        rng = np.random.default_rng(42)
        cluster_centers = [
            (np.array([1.8, 1.6, 0.5]), CYAN),     # text cluster
            (np.array([1.8, -1.2, -0.5]), GOLD),   # code cluster
            (np.array([-1.8, -1.0, 0.4]), GREEN),  # image cluster
            (np.array([-1.8, 1.2, -0.4]), VIOLET), # plan cluster
        ]
        points = VGroup()
        for center, color in cluster_centers:
            for _ in range(8):
                offset = rng.normal(scale=0.28, size=3)
                p = center + offset
                points.add(glow_dot(axes.c2p(p[0], p[1], p[2]), color, radius=0.055))

        # Arcs between cluster centers
        output_specs = [
            ("text", CYAN, axes.c2p(*cluster_centers[0][0])),
            ("code", GOLD, axes.c2p(*cluster_centers[1][0])),
            ("image", GREEN, axes.c2p(*cluster_centers[2][0])),
            ("plan", VIOLET, axes.c2p(*cluster_centers[3][0])),
        ]
        outputs = VGroup()
        output_links = VGroup()
        for label, color, pos in output_specs:
            text = self.glow_text(label, color, 28).move_to(pos + UP * 0.52)
            text.set_opacity(0)  # start hidden; FadeIn below reveals them
            outputs.add(text)
            self.add_fixed_orientation_mobjects(text)
            output_links.add(neon_line(axes.c2p(0, 0, 0), pos, color=color, width=2).set_opacity(0.45))

        # Cross-cluster arcs to show relationships
        arcs = VGroup()
        arc_pairs = [(0, 1, CYAN), (0, 3, VIOLET), (1, 3, GOLD)]
        for i, j, color in arc_pairs:
            a = axes.c2p(*cluster_centers[i][0])
            b = axes.c2p(*cluster_centers[j][0])
            mid = (a + b) / 2 + np.array([0, 0, 0.5])
            arc = CubicBezier(a, a + (mid - a) * 0.6, b + (mid - b) * 0.6, b)
            arc.set_stroke(color, width=2.5, opacity=0.55)
            arc_glow = arc.copy().set_stroke(color, width=8, opacity=0.14)
            arcs.add(VGroup(arc_glow, arc))

        intro = Text("language enters the transform pattern", color=WHITE, font_size=30)
        intro.set_fill(WHITE, opacity=0.96).set_stroke(width=0).to_edge(UP).shift(DOWN * 0.25)
        self.add_fixed_in_frame_mobjects(intro)
        self.play(FadeIn(intro), run_time=0.8)

        self.wait_until_phrase("And I mean more than language", offset=-0.25, fallback=4.8)
        modality_labels = [
            ("text", CYAN), ("code", GOLD), ("images", GREEN), ("audio", VIOLET),
            ("diagrams", WHITE), ("sensors", "#FF8FB0"), ("constraints", BLUE), ("tasks", RED),
        ]
        modality_tiles = VGroup()
        for label, color in modality_labels:
            tile = RoundedRectangle(width=2.05, height=0.56, corner_radius=0.08, color=color, stroke_width=2)
            tile.set_fill(BG, opacity=0.72)
            text = Text(label, color=color, font_size=21).set_fill(color, opacity=0.95).set_stroke(width=0)
            modality_tiles.add(VGroup(tile, text.move_to(tile.get_center())))
        modality_tiles.arrange_in_grid(rows=2, cols=4, buff=(0.24, 0.22)).move_to(UP * 0.55)
        self.add_fixed_in_frame_mobjects(modality_tiles)
        self.play(FadeOut(intro), FadeIn(modality_tiles, lag_ratio=0.08), run_time=0.9)
        self.clear_fixed(intro)

        self.wait_until_phrase("Text code images audio diagrams sensor readings", offset=0.45, fallback=1.2)
        for tile in modality_tiles:
            self.play(tile.animate.scale(1.07), run_time=0.18, rate_func=there_and_back)

        self.wait_until_phrase("Anything that can be represented", offset=-0.35, fallback=3.0)
        representable = self.glow_text("anything representable can enter the system", CYAN, 24)
        representable.to_edge(DOWN).shift(UP * 0.45)
        self.add_fixed_in_frame_mobjects(representable)
        self.play(FadeIn(representable, shift=UP * 0.12), run_time=0.6)
        self.wait_until_phrase("Not perfectly", offset=-0.15, fallback=1.2)
        caveat = self.glow_text("not perfectly, not magically, but practically", GOLD, 22)
        caveat.next_to(representable, DOWN, buff=0.20)
        self.add_fixed_in_frame_mobjects(caveat)
        self.play(FadeIn(caveat), run_time=0.5)
        self.wait(0.9)
        self.play(FadeOut(modality_tiles), FadeOut(representable), FadeOut(caveat), run_time=0.7)
        self.clear_fixed(modality_tiles, representable, caveat)

        # ---- NEW SUB-SCENE: clear screen, show sentence → tokens → vectors ----
        # User asked for a dedicated visualization of the "sentence broken into
        # tokens" beat. Clear the entire vector cloud, build a new diagram.
        self.wait_until_phrase([
            "A sentence can be broken into tokens",
            "sentence can be broken into tokens",
        ], offset=-0.6, fallback=0.8)
        self.stop_ambient_camera_rotation()
        # Reset camera back to flat 2D-ish view so the new scene reads cleanly.
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.0, run_time=0.8)
        # NOTE: the 3D vector cloud (points / axes / arcs / output_links / outputs)
        # built at the top of this scene is never actually faded in by the
        # current design — the modality tiles + sentence→vectors sub-scenes
        # replaced it. FadeOut-ing those never-shown mobjects was ADDING them at
        # full opacity for the transition, flashing the 3D axes/dots onto screen
        # for ~0.8s (user: "weird flash of a vector-space 3D graph"). Removed.

        sub_title = Text("a sentence becomes vectors", color=WHITE, font_size=26).set_fill(WHITE, opacity=0.95).set_stroke(width=0)
        sub_title.to_edge(UP).shift(DOWN * 0.30)
        self.add_fixed_in_frame_mobjects(sub_title)
        self.play(FadeIn(sub_title), run_time=0.5)

        # Step 1: the literal sentence appears
        sentence_text = "Build an API that checks subscription usage."
        sentence_obj = Text(sentence_text, color=WHITE, font_size=28).set_fill(WHITE, opacity=1).set_stroke(width=0)
        sentence_obj.move_to(UP * 1.6)
        self.add_fixed_in_frame_mobjects(sentence_obj)
        self.play(FadeIn(sentence_obj), run_time=0.6)
        self.wait(0.8)

        # Step 2: split into tokens — show each word as a separate Text in a row
        tokens_list = ["Build", "an", "API", "that", "checks", "subscription", "usage", "."]
        token_colors = [CYAN, WHITE, GOLD, WHITE, GREEN, VIOLET, "#FF8FB0", WHITE]
        token_group = VGroup()
        for word, color in zip(tokens_list, token_colors):
            t = Text(word, color=color, font_size=24).set_fill(color, opacity=1).set_stroke(width=0)
            token_group.add(t)
        token_group.arrange(RIGHT, buff=0.30).move_to(UP * 0.30)
        self.add_fixed_in_frame_mobjects(token_group)
        self.wait_until_phrase([
            "Those tokens can be turned into vectors",
            "tokens can be turned into vectors",
        ], offset=-0.35, fallback=0.6)
        self.play(FadeOut(sentence_obj), FadeIn(token_group, shift=DOWN * 0.5), run_time=0.9)
        self.wait(0.6)

        # Step 3: each token gets wrapped in a vector "box" — a small dot + arrow
        # representing its embedding. They float down into a horizontal row.
        vectors_group = VGroup()
        for i, (word, color) in enumerate(zip(tokens_list, token_colors)):
            x = -5.5 + i * 1.40
            dot = Dot(np.array([x, -1.10, 0]), radius=0.10, color=color)
            arrow_end = np.array([x + 0.30, -0.60, 0])
            vec_arrow = Arrow(np.array([x, -1.10, 0]), arrow_end, color=color, stroke_width=4, buff=0.0, max_tip_length_to_length_ratio=0.30)
            mini_label = Text(word, color=color, font_size=13).set_fill(color, opacity=0.92).set_stroke(width=0)
            mini_label.move_to(np.array([x, -1.55, 0]))
            vectors_group.add(VGroup(dot, vec_arrow, mini_label))
        self.add_fixed_in_frame_mobjects(vectors_group)
        self.play(FadeIn(vectors_group, lag_ratio=0.10), run_time=1.4)
        self.wait(1.0)

        # Step 4: spread the vectors out into a wider "relational space"
        # cluster so the labels stay legible (previous version compacted them
        # into an unreadable clump — Gemini flagged it as vector arrows
        # overlapping the tokens, which was really mini-labels overlapping
        # each other in the tight cluster). Spread across a 7×1.4 zone at
        # the bottom of the screen.
        anims = []
        for i, grp in enumerate(vectors_group):
            # Each grp keeps its column position but gets nudged down into
            # the lower band, so the cluster reads as a bottom row.
            target_x = -5.10 + i * 1.55 + rng.normal(scale=0.18)
            target_y = -2.55 + rng.normal(scale=0.22)
            anims.append(grp.animate.move_to(np.array([target_x, target_y, 0])).scale(0.70))
        relational = Text("…land at positions in a relational space", color=CYAN, font_size=20).set_fill(CYAN, opacity=1).set_stroke(width=0)
        relational.move_to(DOWN * 3.55)
        self.add_fixed_in_frame_mobjects(relational)
        self.wait_until_phrase("relationships between words concepts code images and tasks", offset=-0.6, fallback=0.6)
        self.play(*anims, FadeIn(relational), run_time=1.6)
        self.wait(2.0)

        late_beats = [
            ("English Python an image a plan a shell command", "English · Python · image · plan · command", GOLD),
            ("machines that can move human representations into a space", "meaning-like relationships become computable", GREEN),
            ("preserves enough relationship structure to be useful", "preserves enough relationship structure", WHITE),
        ]
        for phrase, caption, color in late_beats:
            self.wait_until_phrase(phrase, offset=-0.45, fallback=0.6)
            card = self.glow_text(caption, color, 22).to_edge(DOWN).shift(UP * 0.20)
            self.add_fixed_in_frame_mobjects(card)
            self.play(FadeIn(card, shift=UP * 0.15), run_time=0.6)
            self.wait(CAPTION_MIN_HOLD)
            self.play(FadeOut(card), run_time=0.5)
            self.clear_fixed(card)

        self.remaining_wait()


# ---------------------------------------------------------------------------
# S03b — Word Vector Analogy: king − man + woman ≈ queen (2D)
# ---------------------------------------------------------------------------

class S03bWordVectorAnalogy(Storyboard2DScene):
    target_seconds = 30

    def construct(self):
        title = self.glow_text("relationships become directions", MUTED, 26)
        title.to_edge(UP).shift(DOWN * 0.1)

        # Slanted parallelogram layout: relationship is a direction, not a y-axis category.
        man_pos   = np.array([ 2.45, -1.45, 0.0])
        king_pos  = np.array([ 1.55,  1.45, 0.0])
        woman_pos = np.array([-2.25, -1.15, 0.0])
        queen_pos = woman_pos + (king_pos - man_pos)

        def point_group(pos, label, color, label_dir=RIGHT) -> VGroup:
            core = Dot(pos, radius=0.13, color=color)
            aura = Dot(pos, radius=0.36, color=color).set_opacity(0.2)
            text = Text(label, color=color, font_size=34).next_to(core, label_dir, buff=0.22)
            return VGroup(aura, core, text)

        man_g   = point_group(man_pos,   "man",   BLUE)
        king_g  = point_group(king_pos,  "king",  GOLD)
        woman_g = point_group(woman_pos, "woman", VIOLET, LEFT)
        queen_g = point_group(queen_pos, "queen", GREEN,  LEFT)

        # Relationship arrow man → king. Wider stroke + brighter glow so the
        # arrow doesn't read as dim brown at small viewer sizes.
        rel_arrow = Arrow(man_pos, king_pos, color=GOLD, stroke_width=8, buff=0.15)
        rel_glow  = rel_arrow.copy().set_stroke(GOLD, width=26, opacity=0.32)
        rel_label_text = self.glow_text("social status →", GOLD, 28)
        rel_label_text.next_to(rel_arrow, RIGHT, buff=0.26).shift(UP * 0.10)
        rel_label_shield = BackgroundRectangle(rel_label_text, color=BG, fill_opacity=0.88, buff=0.10)
        rel_label = VGroup(rel_label_shield, rel_label_text).set_z_index(8)

        # Copy arrow woman → prediction
        pred_arrow = Arrow(woman_pos, queen_pos, color=GREEN, stroke_width=5, buff=0.15)
        pred_glow  = pred_arrow.copy().set_stroke(GREEN, width=18, opacity=0.2)
        guide = DashedLine(king_pos, queen_pos, color=MUTED, dash_length=0.18, stroke_width=2).set_opacity(0.32)
        guide2 = DashedLine(man_pos, woman_pos, color=MUTED, dash_length=0.18, stroke_width=2).set_opacity(0.32)

        # Equation
        eq_parts = [("king", GOLD), (" − ", WHITE), ("man", BLUE),
                    (" + ", WHITE), ("woman", VIOLET), ("  ≈  ", WHITE), ("queen", GREEN)]
        equation = VGroup(*[Text(t, color=c, font_size=30) for t, c in eq_parts])
        equation.arrange(RIGHT, buff=0.04).to_edge(DOWN).shift(UP * 0.5)

        footnote = Text("illustrative projection — not a formal guarantee", color=MUTED, font_size=18)
        footnote.to_edge(DOWN).shift(UP * 0.1)

        self.play(FadeIn(title), run_time=0.7)
        self.play(LaggedStart(FadeIn(man_g), FadeIn(king_g), FadeIn(woman_g), lag_ratio=0.25), run_time=1.5)
        self.wait(0.5)
        # Anchor the analogy build to the "king minus man plus woman" narration
        # so the whole scene tracks the human take (it had no anchors before, so
        # it played in ~30s then froze for the rest of the 57s audio).
        self.wait_until_phrase(["King minus man plus woman", "King minus man"], offset=-0.5, fallback=0.5)
        self.play(Create(VGroup(rel_glow, rel_arrow)), FadeIn(rel_label), run_time=1.4)
        # Fade out the title so the step captions don't stack on it
        # (user flagged "text overlap at the top of the frame" at 04:50.5).
        self.play(FadeOut(title), run_time=0.4)
        # Hold the labeled relationship arrow so the viewer reads the cue
        # before it's translated. Gemini said the addition felt too fast to
        # parse — pacing it out makes the geometry explicit.
        step1 = self.glow_text("(1) read the direction:  king − man", GOLD, 20).move_to(UP * 3.30)
        self.play(FadeIn(step1), run_time=0.6)
        self.wait(1.6)
        self.play(FadeOut(rel_label), FadeOut(step1), run_time=0.4)
        # Step 2: explicit translation of the relationship vector from man → woman
        step2 = self.glow_text("(2) place the same direction at  woman", GREEN, 20).move_to(UP * 3.30)
        self.play(FadeIn(step2), run_time=0.6)
        copied_arrow = VGroup(rel_glow.copy(), rel_arrow.copy())
        copied_arrow.set_z_index(4)
        trail = VGroup()
        for alpha in np.linspace(0.18, 0.82, 4):
            ghost = rel_arrow.copy().shift((woman_pos - man_pos) * alpha)
            ghost.set_stroke(GREEN, width=3.0, opacity=0.10 + 0.08 * alpha)
            trail.add(ghost)
        self.play(
            LaggedStart(*[FadeIn(g) for g in trail], lag_ratio=0.12),
            copied_arrow.animate.shift(woman_pos - man_pos),
            run_time=2.4,
        )
        self.wait(1.0)
        self.play(FadeOut(step2), run_time=0.4)
        step3 = self.glow_text("(3) tip lands at  queen", VIOLET, 20).move_to(UP * 3.30)
        self.play(FadeIn(step3), run_time=0.6)
        self.play(
            FadeIn(queen_g),
            Create(VGroup(guide, guide2)),
            Create(VGroup(pred_glow, pred_arrow)),
            FadeOut(copied_arrow),
            FadeOut(trail),
            run_time=1.2,
        )
        self.wait(0.8)
        self.play(FadeOut(step3), run_time=0.4)
        self.play(FadeIn(equation), run_time=1.2)
        self.play(FadeIn(footnote), run_time=0.8)
        # Dwell on the finished analogy while the narration says "words can become
        # locations, relationships can become directions" (user: sit longer on the
        # completed diagram before cutting to the search beat).
        self.wait_until_phrase(["words can become locations", "relationships can become directions"], offset=-0.3, fallback=2.2)
        self.wait(1.2)
        # A second, less algebraic semantic-search beat: concept neighborhoods.
        left_group = VGroup(man_g, king_g, woman_g, queen_g, rel_arrow, rel_glow, pred_arrow, pred_glow, guide, guide2, equation, footnote)
        # Transition on "similarity can become distance / search can become geometry".
        self.wait_until_phrase(["Similarity can become distance", "similarity can become distance"], offset=-0.6, fallback=1.0)
        self.play(FadeOut(left_group), FadeOut(title), run_time=0.7)
        search_title = self.glow_text("the same arithmetic does semantic search", MUTED, 24)
        search_title.to_edge(UP).shift(DOWN * 0.18)
        query = Text('"big cat with a mane"', color=CYAN, font_size=26).move_to(LEFT * 4.3 + UP * 0.4)
        lion_center = RIGHT * 1.2 + DOWN * 0.1
        lion = Text("lion", color=GOLD, font_size=42).move_to(lion_center)
        # Neighbors arranged radially around lion. Dots sit INSIDE the search
        # ring (showing they're in the semantic neighborhood), but labels are
        # placed radially OUTSIDE the ring so they don't strike through the
        # ring stroke (user flagged this overlap in the v13 review).
        neighbor_specs = [
            ("tiger",   VIOLET, np.array([ 1.8,  1.05, 0])),
            ("cat",     GREEN,  np.array([ 2.0, -0.05, 0])),
            ("savanna", WHITE,  np.array([ 1.55,-1.15, 0])),
            ("mane",    GOLD,   np.array([-1.85,-1.10, 0])),
            ("roar",    CYAN,   np.array([-1.75, 0.95, 0])),
        ]
        ring_radius = 2.6
        label_radius = 3.05  # outside the ring stroke
        neighbors = VGroup()
        for label, color, offset in neighbor_specs:
            dot_pos = lion_center + offset
            dot = Dot(dot_pos, radius=0.07, color=color)
            aura = Dot(dot_pos, radius=0.20, color=color).set_opacity(0.18)
            # Place the label at the same angle as the dot from the centre,
            # but at radius `label_radius` (outside the ring).
            offset_dir = offset / (np.linalg.norm(offset[:2]) + 1e-9)
            label_pos = lion_center + offset_dir * label_radius
            text = Text(label, color=color, font_size=20).set_fill(color, opacity=1).set_stroke(width=0)
            text.move_to(label_pos)
            # A faint short tether from dot → label so the pairing reads clearly.
            tether = Line(dot_pos + offset_dir * 0.15, label_pos - offset_dir * 0.32,
                          color=color, stroke_width=1.4).set_opacity(0.45)
            neighbors.add(VGroup(aura, dot, tether, text))
        # Stop the arrow head well clear of the lion letter "l" — Gemini flagged
        # this as overlapping the glyph in the previous pass.
        search_arrow = neon_arrow(query.get_right() + RIGHT * 0.18, lion.get_left() + LEFT * 0.40, color=CYAN, width=3.0)
        search_ring = Circle(radius=2.6, color=GOLD, stroke_width=2.2).move_to(lion_center)
        search_glow = search_ring.copy().set_stroke(GOLD, width=18, opacity=0.13)
        # Show the search "space" (the ring) first; the captions below are each
        # anchored to their exact narration line so they no longer drift (user:
        # "similarity can become distance" and others were out of sync).
        self.play(FadeIn(search_title), Create(VGroup(search_glow, search_ring)), run_time=1.0)

        walk_pos = DOWN * 3.30

        def walk_caption(text, color, hold=2.2):
            card = self.glow_text(text, color, 21).move_to(walk_pos)
            self.play(FadeIn(card, shift=UP * 0.10), run_time=0.5)
            ghost = search_ring.copy()
            self.add(ghost)
            self.play(ghost.animate.scale(1.08).set_opacity(0.0), run_time=hold, rate_func=rate_functions.ease_out_sine)
            self.remove(ghost)
            self.play(FadeOut(card), run_time=0.4)

        # "similarity can become distance" → ring = a distance space
        walk_caption("similarity becomes distance", GOLD)
        # "search can become geometry"
        self.wait_until_phrase(["Search can become geometry", "search can become geometry"], offset=-0.3, fallback=0.3)
        walk_caption("search becomes geometry", CYAN)

        # The concrete lion search lands on "big cat with a mane".
        self.wait_until_phrase(["big cat with a mane"], offset=-0.5, fallback=0.4)
        self.play(FadeIn(query), Create(search_arrow), FadeIn(lion), run_time=1.0)
        self.play(FadeIn(neighbors, lag_ratio=0.12), run_time=1.2)

        # Closing captions, anchored to the final two lines.
        self.wait_until_phrase(["points neighborhoods directions", "neighborhoods directions and transformations"], offset=-0.3, fallback=1.0)
        walk_caption("words → points, neighborhoods, directions", VIOLET)
        self.wait_until_phrase(["a new domain for computation"], offset=-0.3, fallback=0.3)
        walk_caption("a new domain for computation", GREEN)

        self.remaining_wait()


# ---------------------------------------------------------------------------
# S04 — The Human Claim (title card, placeholder for camera segment)
# ---------------------------------------------------------------------------

class S04HumanClaimBridge(Storyboard2DScene):
    target_seconds = 20

    def construct(self):
        claim_title = self.glow_text("the human claim", WHITE, 38)
        claim_title.move_to(UP * 1.4)

        line1 = Text("the claim is not that AI contains human meaning", color=WHITE, font_size=25).set_fill(WHITE, opacity=0.86).set_stroke(width=0)
        line1.move_to(UP * 0.2)
        line2 = self.glow_text("that enough structure survives the transform", CYAN, 28)
        line2.move_to(DOWN * 0.7)
        line3 = Text("to make new kinds of work possible", color=WHITE, font_size=24)
        line3.move_to(DOWN * 1.55)

        placeholder = Text("[replace with direct-to-camera recording]", color=MUTED, font_size=18)
        placeholder.to_edge(DOWN).shift(UP * 0.3)

        self.play(FadeIn(claim_title), run_time=1.2)
        self.play(FadeIn(line1), run_time=1.0)
        self.play(FadeIn(line2), run_time=1.0)
        self.play(FadeIn(line3), run_time=0.8)
        self.play(FadeIn(placeholder), run_time=0.6)
        self.remaining_wait()


# ---------------------------------------------------------------------------
# S05 — Pseudocode to Code Is a Lossy Transform (3D, two distinct beats)
# ---------------------------------------------------------------------------

class S05CodeAndLoss(StoryboardScene):
    target_seconds = 44

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-43 * DEGREES, zoom=0.82, focal_distance=8.0)

        # ---- BEAT 1 (0–22s): intent → transform → lossy cloud ----
        prompt = VGroup(
            Text("intent", color=CYAN, font_size=30),
            Text("active subscription", color=WHITE, font_size=22),
            Text("usage limit", color=WHITE, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(LEFT).shift(RIGHT * 0.3 + UP * 1.1)
        self.add_fixed_in_frame_mobjects(prompt)

        axes = self.bright_axes().shift(RIGHT * 0.25)
        # Build the matrix as a 2D fixed-in-frame element so the 3D camera
        # angle doesn't tilt it into an unreadable skew (Gemini called this
        # out as "tilted at an extreme angle, unreadable").
        # 2x2 abstract matrix. User flagged the previous "?, schema, plan, ?"
        # version as having cells overflow their boxes (the word "schema" is
        # too wide for the 0.58-unit cell). Use single-glyph entries that fit
        # the cells, with "?" symbolizing the missing-information slots.
        transform = matrix_plate([["?", "·"], ["·", "?"]], color=VIOLET)
        transform.scale(1.05).to_edge(RIGHT).shift(LEFT * 0.30 + UP * 1.35)

        rng = np.random.default_rng(31)
        source = VGroup()
        target = VGroup()
        for i in range(40):
            p = rng.normal(size=3)
            p = p / np.linalg.norm(p) * (0.9 + rng.random() * 1.5)
            source.add(glow_dot(axes.c2p(p[0], p[1], p[2]), BLUE, radius=0.048))
            q = np.array([p[0] * 0.8 + p[1] * 0.5, p[1] * 0.55 - p[2] * 0.2, p[2] * 0.45])
            target.add(glow_dot(axes.c2p(q[0], q[1], q[2]), RED if i % 7 == 0 else CYAN, radius=0.052))

        transform_arrow = neon_arrow(LEFT * 1.4 + UP * 1.0, RIGHT * 1.9 + UP * 1.0, color=GOLD, width=5)
        # User feedback: this scene was using the phrase "semantic transform
        # loss" before the narration introduces it (that term doesn't appear
        # until S07). Replaced with a label that matches what S05's narration
        # is actually about at this beat: the output contains assumptions.
        loss_label = self.glow_text("the output contains assumptions", "#FF7FA8", 28)
        loss_label.to_edge(DOWN).shift(UP * 0.42 + RIGHT * 0.0)
        self.add_fixed_in_frame_mobjects(loss_label)

        self.play(FadeIn(prompt), Create(axes), FadeIn(source, lag_ratio=0.01), run_time=2.4)
        # Mark the matrix as fixed-in-frame so the 3D camera tilt doesn't skew it.
        self.add_fixed_in_frame_mobjects(transform)
        transform.set_opacity(0)
        self.play(transform.animate.set_opacity(1), Create(transform_arrow), run_time=1.2)
        self.play(Transform(source, target), axes.animate.set_opacity(0.22), run_time=2.4)
        self.play(FadeOut(transform), FadeOut(transform_arrow), run_time=0.8)
        self.play(FadeIn(loss_label), run_time=0.9)
        self.begin_ambient_camera_rotation(rate=0.04)
        self.wait_until_phrase("A model can transform that intent", offset=-0.8, fallback=8.0)
        self.stop_ambient_camera_rotation()

        # ---- BEAT 2 (22–44s): code with highlighted assumptions ----
        self.play(
            FadeOut(source),
            FadeOut(axes),
            FadeOut(loss_label),
            run_time=1.2,
        )
        self.remove_fixed_in_frame_mobjects(loss_label)

        # Drop the rounded-rect "UI panel" backdrop — Gemini called it out as
        # a slide-deck artifact. Let the code text float as glowing syntax.
        # Pin the code further left so it doesn't overlap the assumptions
        # column and so the connecting links are short and readable.
        code_lines = VGroup(
            Text("def usage_limit(user_id):", color=GREEN, font_size=22, weight=BOLD),
            Text("  user = db.get(user_id)", color=WHITE, font_size=20),
            Text("  if user.active_subscription:", color=WHITE, font_size=20),
            Text("    return user.plan.limit", color=GOLD, font_size=20, weight=BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to(RIGHT * 1.00 + UP * 0.85)
        code_panel = VGroup(code_lines)
        self.add_fixed_in_frame_mobjects(code_panel)
        # Keep the code hidden until its FadeIn below. add_fixed_in_frame_mobjects
        # adds it at full opacity immediately, so without this the code appeared,
        # then the later FadeIn(code_lines) blinked it out and back in (user:
        # "extra appear, fade out, then fade back in on def usage_limit").
        code_lines.set_opacity(0)

        # Keep the transform mechanic visible in the code beat so review frames
        # do not collapse into a plain code slide.
        rng2 = np.random.default_rng(71)
        mini_source = VGroup()
        mini_target = VGroup()
        for _ in range(24):
            p = np.array([-5.05 + rng2.normal(scale=0.28), -0.16 + rng2.normal(scale=0.34), 0])
            q = np.array([-2.08 + rng2.normal(scale=0.26), -0.16 + rng2.normal(scale=0.32), 0])
            mini_source.add(glow_dot(p, CYAN, radius=0.034))
            mini_target.add(glow_dot(q, RED if rng2.random() < 0.22 else GOLD, radius=0.034))
        mini_matrix = matrix_plate([["?", "x"], ["w", "!"]], color=VIOLET)
        mini_matrix.scale(0.44).move_to(LEFT * 3.55 + DOWN * 0.16)
        mini_shield = BackgroundRectangle(mini_matrix, color=BG, fill_opacity=0.94, buff=0.04)
        mini_flow_1 = neon_arrow(LEFT * 4.56 + DOWN * 0.16, LEFT * 4.18 + DOWN * 0.16, color=CYAN, width=2.4)
        mini_flow_2 = neon_arrow(LEFT * 2.94 + DOWN * 0.16, LEFT * 2.52 + DOWN * 0.16, color=GOLD, width=2.4)
        mini_caption = Text("intent vectors → transform → code", color=WHITE, font_size=17)
        mini_caption.move_to(LEFT * 3.65 + DOWN * 1.32)
        mini_transform = VGroup(mini_source, mini_shield, mini_matrix, mini_target, mini_flow_1, mini_flow_2, mini_caption)
        self.add_fixed_in_frame_mobjects(mini_transform)

        # Assumption annotations live in a separate right column. This avoids
        # the most common failure mode: red critique text overwriting code.
        annotation_specs = [
            ("framework unknown", code_lines[0]),
            ("schema assumed", code_lines[1]),
            ("'active' undefined", code_lines[2]),
            ("no error handling", code_lines[3]),
        ]
        assumptions = VGroup()
        assumption_links = VGroup()
        for text, line in annotation_specs:
            # Drop the pill backdrops — Gemini called them UI buttons. Use
            # floating pink-red text with a thin connecting line, larger so
            # it actually reads at 480p. Left-align all labels at the same x
            # so the right edge of the longest one doesn't push off-frame.
            ann = Text(text, color="#FF7FA8", font_size=17)
            ann.set_fill("#FF7FA8", opacity=1)
            ann.set_stroke(width=0)
            # Anchor the LEFT edge of every label at x=4.10 so they line up
            # cleanly and the longest one ("'active' undefined") doesn't clip.
            ann_y = line.get_center()[1]
            ann.move_to(np.array([4.10 + ann.width / 2, ann_y, 0]))
            assumptions.add(VGroup(ann))
            # Stop the connector well clear of BOTH endpoints so the line
            # doesn't pierce the code line on the left or the assumption text
            # on the right (Gemini flagged "pink lines penetrate text boxes").
            assumption_links.add(Line(line.get_right() + RIGHT * 0.18, ann.get_left() + LEFT * 0.22, color="#FF4F8B", stroke_width=1.7).set_opacity(0.82))
        assumption_title = Text("implicit assumptions", color="#FF4F8B", font_size=17).next_to(assumptions, UP, buff=0.16)
        assumption_title.set_fill("#FF4F8B", opacity=1)
        assumption_title.set_stroke(width=0)
        assumption_column = VGroup(assumption_links, assumption_title, assumptions)
        self.add_fixed_in_frame_mobjects(assumption_column)

        # Note: the "active subscription" fork (billing table / Stripe API /
        # cached flag) was removed from this scene per user feedback. Those
        # specific resolution options belong to S07 narration, not S05.
        # Keeping S05 focused on the intent → code → assumptions narrative.
        fork = VGroup()  # empty placeholder so downstream FadeOut still works

        lost_particles = VGroup()
        for i in range(18):
            color = RED if i % 3 == 0 else MUTED
            dot = Dot(LEFT * 2.72 + np.array([0.0, -0.92 + 0.06 * i, 0]), radius=0.025, color=color)
            dot.set_opacity(0.28)
            lost_particles.add(dot)
        self.add_fixed_in_frame_mobjects(lost_particles)

        # Same rewording — S05 doesn't get to call this "semantic transform
        # loss" (that's S07's vocabulary). Stay in the language the S05
        # narration actually uses.
        loss_label2 = self.glow_text("the output contains assumptions", "#FF7FA8", 28)
        loss_label2.to_edge(DOWN).shift(UP * 0.42)
        self.add_fixed_in_frame_mobjects(loss_label2)

        self.play(FadeIn(mini_source), FadeIn(mini_matrix), Create(mini_flow_1), run_time=0.8)
        # Reveal the code by animating opacity 0 -> 1. (FadeIn fades to the
        # mobject's CURRENT opacity, which is 0 here because we hid it above, so
        # FadeIn(code_lines) would fade 0 -> 0 and the code never appears.)
        self.play(TransformFromCopy(mini_source, mini_target), Create(mini_flow_2), code_lines.animate.set_opacity(1), run_time=1.4)
        # (Fork removed — was previously a FadeIn here)
        self.play(
            LaggedStart(*[particle.animate.shift(DOWN * 0.35 + RIGHT * (0.08 * math.sin(i))) for i, particle in enumerate(lost_particles)], lag_ratio=0.03),
            run_time=0.9,
        )
        self.play(FadeIn(mini_caption), run_time=0.5)
        self.wait_until_phrase("Because the input is missing information", offset=-0.35, fallback=7.0)
        self.play(
            LaggedStart(
                FadeIn(assumption_links[0], assumptions[0], shift=LEFT * 0.1),
                FadeIn(assumption_links[1], assumptions[1], shift=LEFT * 0.1),
                FadeIn(assumption_links[2], assumptions[2], shift=LEFT * 0.1),
                FadeIn(assumption_links[3], assumptions[3], shift=LEFT * 0.1),
                lag_ratio=0.25,
            ),
            run_time=2.4,
        )
        self.play(FadeIn(assumption_title), run_time=0.4)
        self.play(FadeIn(loss_label2), run_time=0.9)

        # Phrase-anchored cards. The previous fixed 3.6s loop drifted badly
        # from the scratch narration, so these now wait for exact transcript
        # phrases before appearing.
        walk_pos = DOWN * 3.40
        narration_beats = [
            ("the output has to contain assumptions", "#FF7FA8", "the output has to contain assumptions"),
        ]
        for caption, color, phrase in narration_beats:
            self.wait_until_phrase(phrase, offset=-0.15, fallback=0.3)
            card = self.glow_text(caption, color, 22).move_to(walk_pos)
            self.add_fixed_in_frame_mobjects(card)
            self.play(FadeIn(card, shift=UP * 0.15), run_time=0.6)
            self.wait(CAPTION_MIN_HOLD)
            self.play(FadeOut(card), run_time=0.4)
            self.clear_fixed(card)

        # ---- NEW SUB-SCENE: failure modes get their own panels ---------------
        # User asked for each failure mode (helpful / wrong / inevitable /
        # invisible) to be a discrete visual beat instead of a list. Clear the
        # entire pseudocode beat — including the `prompt` (intent / active
        # subscription / usage limit) text that user feedback showed was
        # bleeding into the new failure-modes scene.
        self.play(
            FadeOut(code_panel), FadeOut(assumptions), FadeOut(assumption_links),
            FadeOut(assumption_title), FadeOut(mini_transform),
            FadeOut(lost_particles), FadeOut(loss_label2),
            FadeOut(prompt),
            run_time=1.0,
        )
        self.remove_fixed_in_frame_mobjects(code_panel, assumptions, assumption_links, assumption_title, mini_transform, lost_particles, loss_label2, prompt)

        modes_title = Text("the transform can fail four different ways", color=WHITE, font_size=26).set_fill(WHITE, opacity=0.95).set_stroke(width=0)
        modes_title.to_edge(UP).shift(DOWN * 0.30)
        self.add_fixed_in_frame_mobjects(modes_title)
        self.play(FadeIn(modes_title), run_time=0.6)

        # 2x2 grid of failure-mode panels. Each: a glyph + a name + a tagline.
        # User feedback: the top row (HELPFUL / WRONG) overlapped the bottom
        # row (INEVITABLE / INVISIBLE). Each lane is 2.30 tall centered at
        # pos+DOWN*0.05, so the old top row at UP*0.70 (lane bottom -0.50) ran
        # into the bottom row at DOWN*1.50 (lane top -0.40). Lift the top row to
        # UP*1.15 so the two rows clear each other with a ~0.35 gap while the
        # top glyph glow still sits below the title.
        mode_specs = [
            ("HELPFUL",    GREEN,    LEFT * 3.20 + UP * 1.15,
             "sometimes the assumption is exactly\nwhat we needed"),
            ("WRONG",      "#FF3B6F", RIGHT * 3.20 + UP * 1.15,
             "sometimes it ships the wrong\ninterpretation"),
            ("INEVITABLE", GOLD,     LEFT * 3.20 + DOWN * 1.50,
             "sometimes there is no\ncomplete specification"),
            ("INVISIBLE",  VIOLET,   RIGHT * 3.20 + DOWN * 1.50,
             "sometimes you don't see it\nfor months"),
        ]
        mode_groups = VGroup()
        for name, color, pos, tagline in mode_specs:
            # Glyph dot above the name
            glyph = Dot(pos + UP * 0.65, radius=0.18, color=color).set_opacity(0.95)
            glyph_glow = Dot(pos + UP * 0.65, radius=0.48, color=color).set_opacity(0.22)
            name_text = Text(name, color=color, font_size=24).set_fill(color, opacity=1).set_stroke(width=0)
            name_text.move_to(pos + UP * 0.12)
            tag_text = Text(tagline, color=WHITE, font_size=15, line_spacing=0.85).set_fill(WHITE, opacity=0.88).set_stroke(width=0)
            tag_text.move_to(pos + DOWN * 0.42)
            # Subtle bounding lane to anchor each panel
            lane = Rectangle(width=4.20, height=2.30, color=color, stroke_width=1.6).set_opacity(0.30)
            lane.set_fill(color, opacity=0.04)
            lane.move_to(pos + DOWN * 0.05)
            mode_groups.add(VGroup(lane, glyph_glow, glyph, name_text, tag_text))
        self.add_fixed_in_frame_mobjects(mode_groups)

        # Animate each panel on the same phrase anchors used above. If the
        # phrase has already passed, wait_until_phrase no-ops and the panels
        # still render without stalling.
        mode_phrases = [
            "Sometimes those assumptions are helpful",
            "Sometimes they are wrong",
            "Sometimes they are inevitable",
            "Sometimes they are invisible",
        ]
        for mode_grp, phrase in zip(mode_groups, mode_phrases):
            self.wait_until_phrase(phrase, offset=0.10, fallback=0.2)
            self.play(FadeIn(mode_grp, shift=UP * 0.10), run_time=0.6)
            self.wait(0.4)

        # Final summary card under the grid
        final_tag = Text("preserves some · invents some · loses some · hides some",
                         color="#FF7FA8", font_size=18).set_fill("#FF7FA8", opacity=1).set_stroke(width=0)
        final_tag.to_edge(DOWN).shift(UP * 0.30)
        self.add_fixed_in_frame_mobjects(final_tag)
        self.play(FadeIn(final_tag), run_time=0.6)

        self.remaining_wait()


# ---------------------------------------------------------------------------
# S05b — The Multimodal Analogy (2D)
# ---------------------------------------------------------------------------

class S05bMultimodalAnalogy(Storyboard2DScene):
    target_seconds = 30

    def construct(self):
        title = self.glow_text("the vector space is the adapter", WHITE, 30)
        title.to_edge(UP).shift(DOWN * 0.1)
        self.play(FadeIn(title), run_time=0.8)

        rng = np.random.default_rng(12)

        def cloud(center: np.ndarray, color: str, count: int = 24, spread: float = 0.36) -> VGroup:
            dots = VGroup()
            for _ in range(count):
                offset = np.array([rng.normal(scale=spread), rng.normal(scale=spread * 0.65), 0])
                dots.add(glow_dot(center + offset, color, radius=0.035))
            return dots

        def funnel(center: np.ndarray, color: str, label: str, flip: bool = False) -> VGroup:
            sign = -1 if flip else 1
            tri = Polygon(
                center + np.array([-0.5 * sign, 0.7, 0]),
                center + np.array([-0.5 * sign, -0.7, 0]),
                center + np.array([0.55 * sign, 0.0, 0]),
                color=color,
                stroke_width=3,
            )
            tri.set_fill(color, opacity=0.08)
            glow = tri.copy().set_stroke(color, width=12, opacity=0.16)
            # Label sits ABOVE the funnel so the decoder_swap arrows below
            # don't slice through it (user flagged that the "decoder" label
            # was being hit by the green arrows in the previous build).
            text = Text(label, color=color, font_size=18).set_fill(color, opacity=1).set_stroke(width=0).next_to(tri, UP, buff=0.18)
            return VGroup(glow, tri, text)

        text_cloud = cloud(LEFT * 4.9 + UP * 0.8, CYAN)
        image_cloud = cloud(RIGHT * 4.9 + UP * 0.8, VIOLET)
        shared_cloud = cloud(UP * 0.8, GREEN, count=34, spread=0.55)

        text_label = self.glow_text("text", CYAN, 24).next_to(text_cloud, UP, buff=0.12)
        image_label = self.glow_text("image", VIOLET, 24).next_to(image_cloud, UP, buff=0.12)
        shared_label = self.glow_text("shared vector space", GREEN, 24).next_to(shared_cloud, UP, buff=0.22)

        text_encoder = funnel(LEFT * 2.7 + UP * 0.8, CYAN, "encoder")
        image_decoder = funnel(RIGHT * 2.7 + UP * 0.8, VIOLET, "decoder", flip=True)
        flow1 = neon_arrow(LEFT * 4.1 + UP * 0.8, LEFT * 3.2 + UP * 0.8, color=CYAN, width=3)
        flow2 = neon_arrow(LEFT * 2.1 + UP * 0.8, LEFT * 0.9 + UP * 0.8, color=GREEN, width=3)
        flow3 = neon_arrow(RIGHT * 0.9 + UP * 0.8, RIGHT * 2.1 + UP * 0.8, color=GREEN, width=3)
        flow4 = neon_arrow(RIGHT * 3.2 + UP * 0.8, RIGHT * 4.1 + UP * 0.8, color=VIOLET, width=3)

        # User removed the "trivial: text→text · image→image" hint entirely
        # (it was a vestige from earlier iterations and added noise).
        text_to_text = VGroup()
        image_to_image = VGroup()

        reveal = self.glow_text("swap the decoder, cross the modality", GOLD, 24)
        reveal.to_edge(DOWN).shift(UP * 0.26)

        # Output tiles arrayed BELOW the main encoder/decoder/cloud row, in a
        # tight 2x2 grid on the right half. Y values are clear of both the
        # main diagram (y≈0.8) and the trivial hint (y=-2.5), and the X
        # values don't collide with image_cloud (x≈4.9 spread 0.36).
        output_tiles = VGroup()
        tile_specs = [
            ("image",       VIOLET, RIGHT * 2.10 + DOWN * 1.20),
            ("UI",          GREEN,  RIGHT * 3.80 + DOWN * 1.20),
            ("robot path",  GOLD,   RIGHT * 2.10 + DOWN * 2.20),
            ("code",        CYAN,   RIGHT * 3.80 + DOWN * 2.20),
        ]
        for label, color, pos in tile_specs:
            tile = RoundedRectangle(width=1.55, height=0.55, corner_radius=0.08, color=color, stroke_width=2.2)
            tile.set_fill(BG, opacity=0.92)
            glow = tile.copy().set_stroke(color, width=9, opacity=0.20)
            text = Text(label, color=color, font_size=18).move_to(tile)
            text.set_fill(color, opacity=1)
            text.set_stroke(width=0)
            output_tiles.add(VGroup(glow, tile, text).move_to(pos).set_z_index(6))
        decoder_swap = VGroup()
        # Arrows fan from the bottom of the shared cloud to each tile so they
        # never strike through text encoder/decoder labels above.
        fan_origin = shared_cloud.get_center() + DOWN * 0.45
        for tile in output_tiles:
            arrow = neon_arrow(fan_origin, tile.get_top() + UP * 0.22, color=GREEN, width=1.35)
            arrow.set_z_index(1).set_opacity(0.62)
            decoder_swap.add(arrow)

        self.play(FadeIn(text_to_text), FadeIn(image_to_image), run_time=1.2)
        self.play(
            LaggedStart(FadeIn(text_cloud), FadeIn(text_label), FadeIn(text_encoder), Create(flow1), lag_ratio=0.18),
            run_time=1.4,
        )
        self.play(Create(flow2), FadeIn(shared_cloud), FadeIn(shared_label), run_time=1.4)
        self.play(Create(flow3), FadeIn(image_decoder), run_time=1.0)
        self.play(Create(flow4), FadeIn(image_cloud), FadeIn(image_label), run_time=1.2)
        self.play(FadeIn(reveal), run_time=0.9)
        self.play(LaggedStart(*[Create(a) for a in decoder_swap], lag_ratio=0.08), LaggedStart(*[FadeIn(t) for t in output_tiles], lag_ratio=0.10), run_time=1.4)
        self.play(decoder_swap.animate.set_opacity(0.78), run_time=0.6)
        # Clear the "swap the decoder, cross the modality" reveal text before
        # the narration walk starts so the bottom captions don't stack on it.
        self.play(FadeOut(reveal), run_time=0.5)

        # Narration walk: text↔image↔caption↔code↔robot action
        walk_pos = DOWN * 3.30
        narration_beats = [
            ("text → image", VIOLET),
            ("image → caption", CYAN),
            ("camera view → robot action", GOLD),
            ("sketch → interface", GREEN),
            ("the boundaries between modalities start to blur", WHITE),
            ("what survives the trip across modalities?", "#FF7FA8"),
        ]
        for caption, color in narration_beats:
            card = self.glow_text(caption, color, 22).move_to(walk_pos)
            self.play(FadeIn(card, shift=UP * 0.10), run_time=0.5)
            # Pulse the shared cloud (the adapter) during each card
            ghost = shared_cloud.copy()
            self.add(ghost)
            self.play(ghost.animate.scale(1.06).set_opacity(0.0), run_time=2.4, rate_func=rate_functions.ease_out_sine)
            self.remove(ghost)
            self.play(FadeOut(card), run_time=0.4)

        self.remaining_wait()


# ---------------------------------------------------------------------------
# S07 — Semantic Transform Loss (2D analogy: compression → assumptions)
# ---------------------------------------------------------------------------

class S07SemanticTransformLoss(Storyboard2DScene):
    target_seconds = 48

    def construct(self):
        # Gemini's review called this scene "massively overloaded" — three
        # separate diagrams shared one screen. Split into three clean beats.
        title = self.glow_text("loss is not just error", WHITE, 30)
        title.to_edge(UP).shift(DOWN * 0.12)
        self.play(FadeIn(title), run_time=0.8)

        rng = np.random.default_rng(404)

        # ---- BEAT 1: JPEG/frequency analogy centered ----
        image_pixels = VGroup()
        for i in range(7):
            for j in range(5):
                color = [CYAN, GREEN, GOLD, VIOLET][(i + j) % 4]
                sq = Square(side_length=0.32, color=color, stroke_width=0.8)
                sq.set_fill(color, opacity=0.16 + 0.12 * rng.random())
                sq.move_to(LEFT * 4.4 + np.array([i * 0.34, j * 0.34, 0]) + DOWN * 0.05)
                image_pixels.add(sq)
        image_label = Text("image", color=CYAN, font_size=22).next_to(image_pixels, UP, buff=0.22)

        freq_tiles = VGroup()
        for i, h in enumerate([1.18, 0.78, 0.58, 0.32, 0.22, 0.14]):
            bar = Rectangle(width=0.32, height=h, color=GOLD, stroke_width=0)
            bar.set_fill(GOLD, opacity=0.85 if i < 3 else 0.40)
            bar.move_to(LEFT * 0.6 + RIGHT * i * 0.48 + UP * (h / 2 - 0.55))
            freq_tiles.add(bar)
        freq_label = Text("frequency-like components", color=GOLD, font_size=20).next_to(freq_tiles, UP, buff=0.28)
        beat1_arrow = neon_arrow(LEFT * 2.55 + DOWN * 0.05, LEFT * 1.20 + DOWN * 0.05, color=VIOLET, width=3.0)

        # VERTICAL cut line — separates low-freq bars (kept, left of the line)
        # from high-freq bars (discarded, right of the line). User flagged the
        # earlier horizontal cut as geometrically nonsensical for frequency
        # decomposition. Bars 0–2 stay bright; bars 3+ dim.
        hot_red = "#FF3B6F"
        # Cut sits between bar 2 (x=0.36) and bar 3 (x=0.84). Use x=0.62.
        cut_x = 0.62
        loss_cut = DashedLine(
            np.array([cut_x, -0.82, 0]),
            np.array([cut_x,  0.92, 0]),
            color=hot_red, dash_length=0.14, stroke_width=3.4,
        )
        loss_cut_glow = loss_cut.copy().set_stroke(hot_red, width=10, opacity=0.22)
        # Push kept/discarded labels above the freq-label so the three don't
        # stack on top of each other near the top of the bars.
        loss_cut_label = self.glow_text("discarded →", hot_red, 18)
        loss_cut_label.move_to(np.array([cut_x + 1.05, 1.62, 0]))
        kept_lbl = Text("← kept", color=GREEN, font_size=18).set_fill(GREEN, opacity=1).set_stroke(width=0)
        kept_lbl.move_to(np.array([cut_x - 1.00, 1.62, 0]))

        compressed = VGroup()
        for i in range(7):
            for j in range(5):
                color = CYAN if j > 1 else GREEN
                sq = Square(side_length=0.32, color=color, stroke_width=0.8)
                sq.set_fill(color, opacity=0.12 + 0.05 * ((i + j) % 2))
                sq.move_to(RIGHT * 3.4 + np.array([i * 0.34, j * 0.34, 0]) + DOWN * 0.05)
                compressed.add(sq)
        compressed_label = Text("meaning survives,\ntexture changes", color=GREEN, font_size=20, line_spacing=0.82).next_to(compressed, UP, buff=0.22)
        beat1_arrow_2 = neon_arrow(LEFT * 0.10 + UP * 0.10, RIGHT * 2.65 + UP * 0.10, color=VIOLET, width=3.0)

        self.play(FadeIn(image_pixels), FadeIn(image_label), run_time=1.0)
        self.play(TransformFromCopy(image_pixels, freq_tiles), FadeIn(freq_label), Create(beat1_arrow), run_time=1.4)
        self.wait_until_phrase("JPEG compression", offset=-0.8, fallback=0.4)
        self.play(Create(loss_cut), FadeIn(loss_cut_glow), FadeIn(loss_cut_label), FadeIn(kept_lbl), freq_tiles[3:].animate.set_opacity(0.08), run_time=1.2)
        self.play(TransformFromCopy(freq_tiles[:3], compressed), FadeIn(compressed_label), Create(beat1_arrow_2), run_time=1.4)
        self.wait_until_phrase("With LLMs I think the loss is often semantic", offset=-0.4, fallback=2.5)

        # ---- BEAT 2: intent cluster passes through a transform filter ----
        beat1_group = VGroup(image_pixels, image_label, freq_tiles, freq_label, beat1_arrow, loss_cut, loss_cut_glow, loss_cut_label, kept_lbl, compressed, compressed_label, beat1_arrow_2)
        self.play(FadeOut(beat1_group), run_time=0.9)

        intent_cloud = VGroup()
        for _ in range(60):
            offset = np.array([rng.normal(scale=0.55), rng.normal(scale=0.42), 0])
            intent_cloud.add(glow_dot(LEFT * 4.6 + offset + DOWN * 0.05, CYAN, radius=0.045))
        intent_label = Text("human intent", color=CYAN, font_size=24).next_to(intent_cloud, UP, buff=0.32)
        gate_line = Line(UP * 1.7, DOWN * 1.7, color=VIOLET, stroke_width=7)
        gate_glow = gate_line.copy().set_stroke(VIOLET, width=28, opacity=0.20)
        gate = VGroup(gate_glow, gate_line)
        gate_label = Text("learned transform", color=VIOLET, font_size=20).next_to(gate_line, UP, buff=0.30)

        output_cloud = VGroup()
        for i in range(60):
            offset = np.array([rng.normal(scale=0.50), rng.normal(scale=0.38), 0])
            color = RED if i % 6 == 0 else GOLD
            output_cloud.add(glow_dot(RIGHT * 4.6 + offset + DOWN * 0.05, color, radius=0.045))
        output_label = Text("executable output", color=GOLD, font_size=24).next_to(output_cloud, UP, buff=0.32)
        flow_in = neon_arrow(LEFT * 3.10 + DOWN * 0.05, LEFT * 0.55 + DOWN * 0.05, color=CYAN, width=3.4)
        flow_out = neon_arrow(RIGHT * 0.55 + DOWN * 0.05, RIGHT * 3.10 + DOWN * 0.05, color=GOLD, width=3.4)

        self.play(FadeIn(intent_cloud, lag_ratio=0.02), FadeIn(intent_label), run_time=1.2)
        self.play(FadeIn(gate), FadeIn(gate_label), Create(flow_in), run_time=1.0)
        self.play(TransformFromCopy(intent_cloud, output_cloud), Create(flow_out), FadeIn(output_label), run_time=1.6)
        self.wait_until_phrase("Sometimes the model preserves", offset=-0.3, fallback=2.5)

        # ---- BEAT 3: legend — preserved / invented / lost ----
        beat2_group = VGroup(intent_cloud, intent_label, gate, gate_label, output_cloud, output_label, flow_in, flow_out)
        self.play(FadeOut(beat2_group), run_time=0.9)

        legend_title = self.glow_text("the same output carries three kinds of dots", WHITE, 24)
        legend_title.next_to(title, DOWN, buff=0.45)

        preserved = VGroup()
        invented = VGroup()
        lost = VGroup()
        for _ in range(36):
            offset = np.array([rng.normal(scale=0.55), rng.normal(scale=0.40), 0])
            preserved.add(glow_dot(LEFT * 4.0 + DOWN * 0.6 + offset, GREEN, radius=0.05))
        for _ in range(22):
            offset = np.array([rng.normal(scale=0.55), rng.normal(scale=0.40), 0])
            invented.add(glow_dot(DOWN * 0.6 + offset, RED, radius=0.05))
        for i in range(22):
            offset = np.array([rng.normal(scale=0.55), rng.normal(scale=0.40), 0])
            # Use a light slate so the "lost" dots stay readable on a dim
            # monitor — pure MUTED grey was disappearing into the background.
            d = glow_dot(RIGHT * 4.0 + DOWN * 0.6 + offset, "#9FB1C8", radius=0.05)
            d.set_opacity(0.78)
            lost.add(d)

        preserved_label = self.glow_text("preserved structure", GREEN, 22).move_to(LEFT * 4.0 + UP * 1.05)
        invented_label = self.glow_text("invented assumptions", RED, 22).move_to(UP * 1.05)
        lost_label = self.glow_text("lost constraints", "#9FB1C8", 22).move_to(RIGHT * 4.0 + UP * 1.05)

        self.play(FadeIn(legend_title), run_time=0.6)
        self.play(FadeIn(preserved, lag_ratio=0.04), FadeIn(preserved_label), run_time=1.0)
        self.play(FadeIn(invented, lag_ratio=0.04), FadeIn(invented_label), run_time=1.0)
        self.play(FadeIn(lost, lag_ratio=0.04), FadeIn(lost_label), run_time=1.0)

        # Narration walk slowed down (user: "text runs way too fast relative
        # to the voice"). Each caption now holds 6s instead of 3.6s, giving
        # the viewer time to read AND match it to the audio.
        walk_pos = DOWN * 3.25
        narration_beats = [
            ("'active subscription' → boolean? join? Stripe call?", "#FF7FA8", "active subscription might become"),
            ("the model must choose some version", GOLD, "The model has to choose some version"),
            ("that choice is where loss and invention enter", "#FF3B6F", "That choice is where loss and invention"),
            ("call it semantic transform loss", WHITE, "semantic transform loss"),
            ("missing context becomes executable assumptions", CYAN, "Missing context can become executable assumptions"),
        ]
        for idx, (caption, color, phrase) in enumerate(narration_beats):
            self.wait_until_phrase(phrase, offset=-0.2, fallback=0.5)
            card = self.glow_text(caption, color, 20).move_to(walk_pos)
            self.play(FadeIn(card, shift=UP * 0.15), run_time=0.7)
            # Linger until just before the NEXT narration line instead of a fixed
            # short hold, so a caption stays up while the narrator is still on it
            # (user: the "active subscription → boolean/join/Stripe/cached" line
            # should stay until "a call to Stripe" is finished). Clamped to a
            # readable minimum and a sane maximum so it never flashes or freezes.
            hold = CAPTION_MIN_HOLD
            if idx + 1 < len(narration_beats):
                t_next = self.phrase_time(narration_beats[idx + 1][2])
                t_now = getattr(self.renderer, "time", 0.0) or 0.0
                if t_next is not None:
                    hold = min(7.0, max(CAPTION_MIN_HOLD, t_next - t_now - 0.7))
            self.breathing_wait(hold)
            self.play(FadeOut(card), run_time=0.5)

        # Spread the legend dots outward for a final "settling" beat
        self.play(
            preserved.animate.shift(LEFT * 0.3),
            invented.animate.shift(UP * 0.0),
            lost.animate.shift(RIGHT * 0.3),
            run_time=1.6,
        )
        self.remaining_wait()


# ---------------------------------------------------------------------------
# S06 — The Technology Tree (2D radial, lightly updated)
# ---------------------------------------------------------------------------

class S06TechnologyTree(Storyboard2DScene):
    target_seconds = 31

    def construct(self):
        root_pos = DOWN * 2.35
        root = Dot(root_pos, color=GREEN, radius=0.11)
        root_glow = Dot(root_pos, color=GREEN, radius=0.38).set_opacity(0.14)
        root_label = self.glow_text("learned representation transforms", GREEN, 24)
        root_label.next_to(root, DOWN, buff=0.25)

        branches = [
            ("research\nassistants", np.array([-2.85, -0.95, 0]), VIOLET),
            ("requirements\nto tests", np.array([-3.65, 0.25, 0]), GREEN),
            ("agent\nworkflows", np.array([-2.25, 1.42, 0]), CYAN),
            ("AI\ntutors", np.array([0.0, 2.05, 0]), GOLD),
            ("multimodal\ndesign", np.array([2.25, 1.42, 0]), VIOLET),
            ("semantic\nsearch", np.array([3.65, 0.25, 0]), BLUE),
            ("coding\nassistants", np.array([2.85, -0.95, 0]), CYAN),
        ]
        branch_groups = VGroup()
        labels = VGroup()
        for label, end, color in branches:
            root_to_end = end - root_pos
            mid = root_pos + root_to_end * 0.42 + UP * 0.48
            path = CubicBezier(root_pos, mid, mid + UP * 0.45, end)
            path.set_stroke(color, width=4)
            glow = path.copy().set_stroke(color, width=14, opacity=0.16)
            node = Dot(end, color=color, radius=0.07)
            node_glow = Dot(end, color=color, radius=0.25).set_opacity(0.16)
            label_shift = UP * 0.3
            if end[0] < -2.5:
                label_shift += LEFT * 0.25
            elif end[0] > 2.5:
                label_shift += RIGHT * 0.25
            text = Text(label, color=color, font_size=16, line_spacing=0.82).move_to(end + label_shift)
            branch_groups.add(VGroup(glow, path, node_glow, node))
            labels.add(text)

        question = self.glow_text("what survives the transformation?", WHITE, 26)
        question.to_edge(UP).shift(DOWN * 0.08)

        self.play(FadeIn(root_glow), FadeIn(root), FadeIn(root_label), run_time=1.0)
        self.play(LaggedStart(*[Create(group) for group in branch_groups], lag_ratio=0.12), run_time=4.2)
        self.play(LaggedStart(*[FadeIn(label, shift=UP * 0.08) for label in labels], lag_ratio=0.08), run_time=1.5)
        self.play(FadeIn(question), run_time=1.0)
        self.remaining_wait()


# ---------------------------------------------------------------------------
# S06b — The Transformer Tech Tree (2D hierarchical, deeper)
# ---------------------------------------------------------------------------

class S06bTransformerTechTree(Storyboard2DScene):
    target_seconds = 32

    def construct(self):
        title = self.glow_text("The New Technology Tree", WHITE, 30)
        title.to_edge(UP).shift(DOWN * 0.1)
        self.play(FadeIn(title), run_time=0.7)

        root_pos = np.array([0.0, -2.85, 0.0])
        root = Dot(root_pos, radius=0.14, color=GREEN)
        root_aura = Dot(root_pos, radius=0.4, color=GREEN).set_opacity(0.2)
        root_label = self.glow_text("learned representation transforms", GREEN, 19)
        root_label.next_to(root, DOWN, buff=0.12)

        # Tier 1 nodes
        tier1_data = [
            (np.array([-4.3, -1.15, 0.0]), "Language\nModels", CYAN),
            (np.array([ 0.0, -1.15, 0.0]), "Code\nAgents",    GOLD),
            (np.array([ 4.3, -1.15, 0.0]), "Multimodal",      VIOLET),
        ]

        # Tier 2 nodes: each family gets its own vertical column so labels cannot collide.
        tier2_data = [
            (np.array([-5.9, 0.45, 0.0]), "Research\nAssistants", CYAN,   0),
            (np.array([-4.3, 1.38, 0.0]), "Writing &\nEducation",  CYAN,   0),
            (np.array([-2.7, 0.45, 0.0]), "Decision\nSupport",     CYAN,   0),
            (np.array([-1.35, 0.45, 0.0]), "Test\nGeneration",     GOLD,   1),
            (np.array([ 0.0, 1.38, 0.0]), "Code\nReview",         GOLD,   1),
            (np.array([ 1.35, 0.45, 0.0]), "Formal\nVerification", GOLD,   1),
            (np.array([ 2.7, 0.45, 0.0]), "Image\nGeneration",    VIOLET, 2),
            (np.array([ 4.3, 1.38, 0.0]), "Scientific\nDiscovery", VIOLET, 2),
            (np.array([ 5.9, 0.45, 0.0]), "Interface\nDesign",    VIOLET, 2),
        ]

        self.play(FadeIn(root_aura), FadeIn(root), FadeIn(root_label), run_time=0.8)

        t1_nodes = VGroup()
        t1_branches = VGroup()
        for pos, label, color in tier1_data:
            branch = self.organic_branch(root_pos, pos, color)
            dot = Dot(pos, radius=0.11, color=color)
            aura = Dot(pos, radius=0.3, color=color).set_opacity(0.18)
            text = Text(label, color=color, font_size=20, line_spacing=0.85)
            text.move_to(pos + UP * 0.5)
            t1_branches.add(branch)
            t1_nodes.add(VGroup(aura, dot, text))

        self.play(LaggedStart(*[Create(b) for b in t1_branches], lag_ratio=0.25), run_time=1.6)
        self.play(LaggedStart(*[FadeIn(n) for n in t1_nodes], lag_ratio=0.25), run_time=1.4)

        t2_nodes = VGroup()
        t2_branches = VGroup()
        for pos, label, color, parent_idx in tier2_data:
            parent_pos = tier1_data[parent_idx][0]
            branch = self.organic_branch(parent_pos, pos, color, width=2.5)
            dot = Dot(pos, radius=0.08, color=color)
            aura = Dot(pos, radius=0.22, color=color).set_opacity(0.14)
            text = Text(label, color=color, font_size=13, line_spacing=0.82)
            text.next_to(dot, UP, buff=0.12)
            t2_branches.add(branch)
            t2_nodes.add(VGroup(aura, dot, text))

        self.play(LaggedStart(*[Create(b) for b in t2_branches], lag_ratio=0.08), run_time=2.4)
        self.play(LaggedStart(*[FadeIn(n) for n in t2_nodes], lag_ratio=0.08), run_time=2.0)

        # Special highlight: Formal Verification node
        fv_node = t2_nodes[5]
        fv_ring = Circle(radius=0.32, color=GREEN, stroke_width=3).move_to(tier2_data[5][0])
        fv_ring_glow = fv_ring.copy().set_stroke(GREEN, width=10, opacity=0.2)
        self.play(Create(VGroup(fv_ring_glow, fv_ring)), run_time=0.8)

        self.remaining_wait()


# ---------------------------------------------------------------------------
# S07 — Thinking in the Limit (2D loss curve)
# ---------------------------------------------------------------------------

class S07ThinkingInLimit(Storyboard2DScene):
    target_seconds = 44

    def construct(self):
        title = self.glow_text("what if semantic transform loss keeps falling?", WHITE, 28)
        title.to_edge(UP).shift(DOWN * 0.14)
        self.play(FadeIn(title), run_time=0.9)

        # Axes — X is model/tooling maturity, Y is semantic transform loss.
        ax = Axes(
            x_range=[0, 8, 1],
            y_range=[0, 10, 2],
            x_length=9.0,
            y_length=5.0,
            axis_config={"color": AXIS, "stroke_width": 3.5, "include_ticks": False},
            tips=False,
        ).shift(DOWN * 0.45 + LEFT * 0.2)

        x_label = Text("model + tooling maturity", color=MUTED, font_size=18)
        x_label.next_to(ax.x_axis, DOWN, buff=0.32)
        y_label = Text("semantic transform loss", color=MUTED, font_size=18)
        y_label.rotate(90 * DEGREES).next_to(ax.y_axis, LEFT, buff=0.32)

        def loss_curve(x):
            return 8.8 * math.exp(-0.34 * x) + 0.45

        curve = ax.plot(loss_curve, x_range=[0.25, 7.65, 0.1], color=CYAN, stroke_width=4.5)
        curve_glow = curve.copy().set_stroke(CYAN, width=13, opacity=0.20)

        self.play(Create(ax), FadeIn(x_label), FadeIn(y_label), run_time=1.2)
        self.play(Create(VGroup(curve_glow, curve)), run_time=1.8)

        # Milestones on x-axis with faint vertical tick lines.
        scale_marks = [
            (0.9, "manual\nverify"),
            (2.3, "drafts"),
            (3.8, "code\nat scale"),
            (5.45, "proofs"),
            (7.1, "direct\nmachine code"),
        ]
        tick_group = VGroup()
        for x_val, label in scale_marks:
            tick = DashedLine(
                ax.c2p(x_val, 0), ax.c2p(x_val, 9.2),
                color=AXIS, stroke_width=1.2, dash_length=0.22,
            ).set_opacity(0.22)
            t = Text(label, color=MUTED, font_size=13, line_spacing=0.82)
            t.next_to(ax.c2p(x_val, 0), DOWN, buff=0.22)
            tick_group.add(VGroup(tick, t))
        self.play(LaggedStart(*[FadeIn(m) for m in tick_group], lag_ratio=0.1), run_time=1.0)

        # Mark "today" with a gold dot.
        today_pt = ax.c2p(3.6, loss_curve(3.6))
        today_dot  = Dot(today_pt, radius=0.13, color=GOLD)
        today_glow = Dot(today_pt, radius=0.36, color=GOLD).set_opacity(0.26)
        today_lbl  = Text("← you are here", color=GOLD, font_size=17)
        today_lbl.next_to(today_pt, RIGHT, buff=0.22)
        self.play(FadeIn(VGroup(today_glow, today_dot)), FadeIn(today_lbl), run_time=0.9)
        self.wait(0.8)

        # Capability thresholds: lower loss crosses new reliability bands.
        thresholds = [
            (6.6, "helpful suggestions", WHITE),
            (4.5, "reliable drafts", CYAN),
            (2.8, "trustworthy code at scale", GOLD),
            (1.65, "automated formal proofs", WHITE),
            (0.85, "direct machine code?", RED),
        ]
        for idx, (y_val, label, color) in enumerate(thresholds):
            line = DashedLine(ax.c2p(0.25, y_val), ax.c2p(7.75, y_val), color=color, stroke_width=2.2, dash_length=0.16)
            line.set_opacity(0.52)
            text = Text(label, color=color, font_size=20)
            text.set_stroke(BG, width=6, opacity=0.9)
            if idx == 0:
                text.next_to(line.get_left(), RIGHT, buff=0.18).shift(UP * 0.22)
            elif idx == 1:
                text.next_to(line.get_right(), LEFT, buff=0.18).shift(UP * 0.24)
            elif idx == 2:
                text.next_to(line.get_left(), RIGHT, buff=0.18).shift(DOWN * 0.25)
            elif idx == 3:
                text.next_to(line.get_right(), LEFT, buff=0.18).shift(UP * 0.28)
            else:
                text.next_to(line.get_right(), LEFT, buff=0.18).shift(DOWN * 0.32)
            self.play(Create(line), FadeIn(text), run_time=0.9)
            self.wait(0.5)

        near_zero = ax.c2p(7.65, loss_curve(7.65))
        limit_dot = Dot(near_zero, radius=0.12, color=RED)
        limit_glow = Dot(near_zero, radius=0.38, color=RED).set_opacity(0.25)
        self.play(FadeIn(VGroup(limit_glow, limit_dot)), run_time=0.5)

        reframe = self.glow_text(
            "as loss approaches zero, bridges become optional", WHITE, 23,
        )
        reframe.next_to(ax, DOWN, buff=0.42)
        self.play(FadeIn(reframe), run_time=1.0)
        self.remaining_wait()


# ---------------------------------------------------------------------------
# S07b — What the Limit Actually Looks Like (2D, pipeline collapse)
# ---------------------------------------------------------------------------

class S07bLimitExamples(Storyboard2DScene):
    """Intermediate representations collapse as direct transforms improve."""
    target_seconds = 45

    def construct(self):
        header = self.glow_text("every intermediate representation is a bridge", WHITE, 27)
        header.to_edge(UP).shift(DOWN * 0.18)
        self.play(FadeIn(header), run_time=0.8)

        def node(pos: np.ndarray, label: str, color: str, size: int = 20) -> VGroup:
            core = Circle(radius=0.34, color=color, stroke_width=3).move_to(pos)
            core.set_fill(color, opacity=0.06)
            aura = core.copy().set_stroke(color, width=12, opacity=0.16)
            text = Text(label, color=color, font_size=size, line_spacing=0.82).move_to(pos + DOWN * 0.72)
            return VGroup(aura, core, text)

        positions = [
            np.array([-5.4, 0.8, 0.0]),
            np.array([-2.7, 0.8, 0.0]),
            np.array([0.0, 0.8, 0.0]),
            np.array([2.7, 0.8, 0.0]),
            np.array([5.4, 0.8, 0.0]),
        ]
        labels = ["intent", "source\ncode", "compiler\nIR", "machine\ncode", "execute"]
        colors = [CYAN, GOLD, VIOLET, GREEN, WHITE]
        nodes = VGroup(*[node(p, l, c) for p, l, c in zip(positions, labels, colors)])
        bridges = VGroup(
            *[neon_arrow(positions[i] + RIGHT * 0.38, positions[i + 1] + LEFT * 0.38, color=colors[i + 1], width=3.2) for i in range(4)]
        )
        why = Text("bridges exist because the direct transform fails", color=MUTED, font_size=21)
        why.move_to(DOWN * 1.65)

        self.play(LaggedStart(*[FadeIn(n) for n in nodes], lag_ratio=0.13), run_time=1.7)
        self.play(LaggedStart(*[Create(b) for b in bridges], lag_ratio=0.15), FadeIn(why), run_time=1.8)
        self.wait(1.6)

        direct_arc = CubicBezier(
            positions[0] + UP * 0.45,
            positions[0] + UP * 2.2 + RIGHT * 1.5,
            positions[3] + UP * 2.2 + LEFT * 1.5,
            positions[3] + UP * 0.45,
        )
        direct_arc.set_stroke(CYAN, width=4.4)
        direct_glow = direct_arc.copy().set_stroke(CYAN, width=17, opacity=0.18)
        direct_label = self.glow_text("low-loss direct transform", CYAN, 21)
        direct_label.move_to(UP * 2.25)

        middle_layers = VGroup(nodes[1], nodes[2], bridges[0], bridges[1], bridges[2])
        self.play(middle_layers.animate.set_opacity(0.18), run_time=1.2)
        self.play(Create(VGroup(direct_glow, direct_arc)), FadeIn(direct_label), run_time=1.7)
        self.wait(1.6)

        self.play(FadeOut(why), FadeOut(direct_label), run_time=0.6)
        examples_title = self.glow_text("same mechanic, different domains", WHITE, 24)
        examples_title.move_to(DOWN * 1.05)
        self.play(FadeIn(examples_title), run_time=0.8)

        domain_rows = [
            ("protein target", "drug", VIOLET),
            ("hypothesis", "formal proof", GREEN),
            ("chip spec", "silicon", GOLD),
        ]
        row_groups = VGroup()
        for i, (left, right, color) in enumerate(domain_rows):
            y = -1.75 - i * 0.55
            left_text = Text(left, color=color, font_size=17).move_to(np.array([-3.3, y, 0]))
            right_text = Text(right, color=color, font_size=17).move_to(np.array([3.3, y, 0]))
            bridge = neon_arrow(np.array([-2.1, y, 0]), np.array([2.1, y, 0]), color=color, width=2.4)
            faint_mid = Text("intermediate layers", color=MUTED, font_size=13).move_to(np.array([0.0, y + 0.22, 0]))
            faint_mid.set_opacity(0.32)
            row_groups.add(VGroup(left_text, bridge, right_text, faint_mid))

        self.play(LaggedStart(*[FadeIn(row) for row in row_groups], lag_ratio=0.18), run_time=1.8)
        self.play(LaggedStart(*[row[-1].animate.set_opacity(0.04) for row in row_groups], lag_ratio=0.1), run_time=1.0)
        coda = self.glow_text("as the transform stops failing, the layers stop being necessary", RED, 22)
        coda.to_edge(DOWN).shift(UP * 0.12)
        self.play(FadeIn(coda), run_time=1.0)
        self.remaining_wait()


# ---------------------------------------------------------------------------
# S06c — Video-game-like 3D technology tree
# ---------------------------------------------------------------------------

class S06cGameTechTree3D(StoryboardScene):
    target_seconds = 42

    def construct(self):
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=0.66, focal_distance=9)

        title = self.glow_text("civilization's representation tech tree", WHITE, 27).to_edge(UP).shift(DOWN * 0.1)
        # Brighter, color-coded subtitle so the legend reads on dark background.
        # Original MUTED grey was disappearing into the near-black BG.
        subtitle_parts = VGroup(
            Text("unlocked", color=CYAN, font_size=20).set_fill(CYAN, opacity=1).set_stroke(width=0),
            Text("|", color=WHITE, font_size=20).set_fill(WHITE, opacity=0.7).set_stroke(width=0),
            Text("emerging", color=GREEN, font_size=20).set_fill(GREEN, opacity=1).set_stroke(width=0),
            Text("|", color=WHITE, font_size=20).set_fill(WHITE, opacity=0.7).set_stroke(width=0),
            Text("speculative", color="#FF8FB0", font_size=20).set_fill("#FF8FB0", opacity=1).set_stroke(width=0),
        ).arrange(RIGHT, buff=0.28).next_to(title, DOWN, buff=0.14)
        subtitle = subtitle_parts
        self.add_fixed_in_frame_mobjects(title, subtitle)

        columns = [
            ("Classical", -5.1, "#1E3A5F"),
            ("Computable\nMeaning", -2.1, "#303069"),
            ("AI Workflows", 1.1, "#2D4A31"),
            ("Civilization\nScale", 4.4, "#55324E"),
        ]
        rows = [
            ("Signals", 2.0),
            ("Control", 0.95),
            ("Media", -0.1),
            ("Software", -1.15),
            ("Science", -2.2),
        ]

        # Brighten the column band fill so the category headers read against
        # the dark background. The original opacity 0.09 made the bands all
        # but invisible and the headers ghost-white.
        column_label_colors = [CYAN, VIOLET, GREEN, "#FF8FB0"]
        lanes = VGroup()
        for (heading, x, color), accent in zip(columns, column_label_colors):
            band = Rectangle(width=2.65, height=5.75, color=color, stroke_width=1.6)
            band.set_fill(color, opacity=0.22)
            band.move_to(np.array([x, -0.25, -0.08]))
            label_core = Text(heading, color=accent, font_size=22, line_spacing=0.65)
            label_core.set_fill(accent, opacity=1)
            label_core.set_stroke(width=0)
            label_core.move_to(np.array([x, 3.10, 0]))
            label_glow = label_core.copy().set_stroke(accent, width=6, opacity=0.30)
            lanes.add(VGroup(band, label_glow, label_core))

        row_labels = VGroup()
        for label, y in rows:
            line = Line(np.array([-6.55, y - 0.48, -0.12]), np.array([5.85, y - 0.48, -0.12]), color=GRID, stroke_width=1.4)
            text = Text(label, color=WHITE, font_size=18).move_to(np.array([-6.9, y, 0]))
            text.set_fill(WHITE, opacity=0.86)
            row_labels.add(line, text)

        hot_red = "#ff4f8b"
        nodes = {
            # Classical column (original three + lambda calculus and stats which
            # ground the software and science rows so the tree doesn't look
            # half-populated).
            "fourier":     (-5.1,  2.0,   "Fourier",                   CYAN,   1.0),
            "laplace":     (-5.1,  0.95,  "Laplace",                   GOLD,   1.0),
            "dct":         (-5.1, -0.1,   "DCT",                       VIOLET, 1.0),
            "lambda":      (-5.1, -1.15,  "Lambda\ncalculus",          BLUE,   1.0),
            "doe":         (-5.1, -2.20,  "Statistics\n+ DOE",         GOLD,   1.0),
            # Computable Meaning column
            "frequency":   (-2.1,  2.0,   "frequency\nspace",          CYAN,   1.0),
            "stability":   (-2.1,  0.95,  "stability\nalgebra",        GOLD,   1.0),
            "compression": (-2.1, -0.1,   "perceptual\ncompression",   VIOLET, 1.0),
            "embeddings":  (-2.1, -1.15,  "embedding\nspace",          GREEN,  0.94),
            "sciml":       (-2.1, -2.20,  "neural ODEs\n· PINNs",      CYAN,   0.94),
            # AI Workflows column — added speech/audio and research assistants
            "audio":       ( 1.1,  2.0,   "speech &\naudio agents",    CYAN,   0.92),
            "vv":          ( 1.1,  0.95,  "V&V\nsystems",              GREEN,  0.74),
            "multimodal":  ( 1.1, -0.1,   "multimodal\nmodels",        VIOLET, 0.82),
            "code":        ( 1.1, -1.15,  "code\nagents",              CYAN,   0.86),
            "research":    ( 1.1, -2.20,  "research\nassistants",      GOLD,   0.88),
            # Civilization Scale column — added ambient monitoring + media
            "monitoring":  ( 4.4,  2.0,   "ambient\ninfrastructure",   CYAN,   0.55),
            "orgs":        ( 4.4,  0.95,  "transform-native\norganizations", GREEN, 0.55),
            "media":       ( 4.4, -0.1,   "synthetic\nmedia stacks",   VIOLET, 0.50),
            "self":        ( 4.4, -1.15,  "self-inhabiting\ncompute",  hot_red, 0.48),
            "labs":        ( 4.4, -2.2,   "autonomous\nexperiment loops", GOLD, 0.45),
        }
        edges = [
            # Classical → Computable
            ("fourier", "frequency"),
            ("laplace", "stability"),
            ("dct", "compression"),
            ("lambda", "embeddings"),
            ("doe", "sciml"),
            # Cross-pollination inside Computable
            ("frequency", "embeddings"),
            ("stability", "embeddings"),
            ("compression", "multimodal"),
            # Computable → AI Workflows
            ("frequency", "audio"),
            ("embeddings", "audio"),
            ("embeddings", "code"),
            ("embeddings", "multimodal"),
            ("embeddings", "research"),
            ("sciml", "research"),
            ("stability", "vv"),
            ("code", "vv"),
            # AI Workflows → Civilization Scale
            ("audio", "monitoring"),
            ("vv", "orgs"),
            ("vv", "self"),
            ("code", "self"),
            ("multimodal", "media"),
            ("multimodal", "labs"),
            ("vv", "labs"),
            ("research", "labs"),
        ]

        def p(key: str) -> np.ndarray:
            x, y, _, _, _ = nodes[key]
            return np.array([x, y, 0])

        def tech_card(key: str) -> VGroup:
            x, y, label, color, opacity = nodes[key]
            pos = np.array([x, y, 0])
            max_line = max(len(part) for part in label.split("\n"))
            # Card / text bumped up for 480p readability — original size was
            # leaving Gemini calling the tree "tiny text on tiny boxes".
            w = min(2.55, max(1.65, 0.14 * max_line + 0.66))
            h = 0.66 if "\n" not in label else 0.84
            plate = RoundedRectangle(width=w, height=h, corner_radius=0.08, color=color, stroke_width=2.2)
            plate.set_fill(BG, opacity=0.95)
            plate.set_opacity(0.34 + opacity * 0.66)
            plate.shift(IN * 0.03)
            plate.set_z_index(1)
            shadow = plate.copy().set_fill(color, opacity=0.10).set_stroke(color, width=11, opacity=0.12 + 0.14 * opacity)
            shadow.shift(IN * 0.08)
            shadow.set_z_index(0)
            icon = Dot(LEFT * (w / 2 - 0.22), radius=0.085, color=color).set_opacity(0.65 + 0.35 * opacity)
            icon.shift(OUT * 0.06)
            icon.set_z_index(3)
            text_size = 15 if max_line > 13 else 17
            text = Text(label, color=WHITE, font_size=text_size, line_spacing=0.78)
            text.set_fill(WHITE, opacity=1)
            text.set_stroke(width=0)
            fit_text_to_width(text, w - 0.52)
            text.move_to(RIGHT * 0.16)
            self.validate_text_fits(text, plate, f"tech_card:{key}")
            text.shift(OUT * 0.07)
            text.set_z_index(4)
            card = VGroup(shadow, plate, icon, text).move_to(pos)
            if opacity < 0.92:
                plate.set_opacity(0.70)
                shadow.set_opacity(0.16)
                icon.set_opacity(0.68)
                text.set_opacity(0.78)
            return card

        edge_groups = VGroup()
        for a, b in edges:
            color = nodes[b][3]
            opacity = min(nodes[a][4], nodes[b][4])
            # Stop the edge clearly OUTSIDE the destination card so the line
            # doesn't run into the text inside it. With max card width 2.55,
            # half-width is 1.27; we end at 1.35 from center to leave a small
            # buffer. (Previously 0.78 was inside the card for wider labels.)
            start = p(a) + RIGHT * 1.35
            end = p(b) + LEFT * 1.35
            mid1 = np.array([(start[0] + end[0]) / 2, start[1], 0])
            mid2 = np.array([(start[0] + end[0]) / 2, end[1], 0])
            path = CubicBezier(start, mid1, mid2, end)
            path.set_stroke(color, width=2.0, opacity=0.34 + 0.50 * opacity)
            glow = path.copy().set_stroke(color, width=8, opacity=0.06 + 0.09 * opacity)
            edge_groups.add(VGroup(glow, path))

        node_groups = VGroup(*[tech_card(key) for key in nodes])
        speculative = VGroup()
        for key in ["self", "labs", "orgs"]:
            ring = SurroundingRectangle(node_groups[list(nodes).index(key)], color=nodes[key][3], buff=0.07, stroke_width=2.0)
            ring.set_opacity(nodes[key][4])
            speculative.add(ring)

        # Locked / not-yet-unlocked nodes: laid out as a clear horizontal
        # "speculative rim" below the Science row, where there's empty space.
        # No collision with Civilization Scale column cards now.
        rim_y = -3.40
        # Box width is 3.40 units. At font_size=19 each char is ~0.13 units,
        # so any label longer than ~26 chars overflows. The previous
        # "closed-loop civilization R&D" label at 27 chars literally could
        # not fit and was the recurring overflow the user flagged 3 times.
        # Shortened labels (each ≤21 chars) now fit cleanly in the 3.40 box.
        locked_specs = [
            (-3.6, rim_y, "native scientific loops",    CYAN),
            ( 0.6, rim_y, "model-designed interfaces", VIOLET),
            ( 4.6, rim_y, "closed-loop civ. R&D",      GOLD),
        ]
        # Pulled the rim label slightly to the right + bigger font so it
        # doesn't clip at the left edge at the final zoom-out.
        rim_label = Text("speculative — not yet unlocked", color="#FF8FB0", font_size=18).set_fill("#FF8FB0", opacity=1).set_stroke(width=0)
        rim_label.move_to(np.array([-5.10, rim_y + 0.65, 0]))
        locked_nodes = VGroup(rim_label)
        locked_edges = VGroup()
        for x, y, label, color in locked_specs:
            pos = np.array([x, y, 0])
            # Use a DASHED outline as the "speculative" cue instead of the
            # internal diagonal hatch line (the hatch looked like a render
            # glitch through the box text per user feedback).
            outline = DashedVMobject(
                RoundedRectangle(width=3.80, height=0.72, corner_radius=0.10, color=color, stroke_width=2.6),
                num_dashes=42,
                dashed_ratio=0.55,
            )
            outline.set_stroke(color, opacity=0.94)
            bg = RoundedRectangle(width=3.80, height=0.72, corner_radius=0.10, color=color, stroke_width=0)
            bg.set_fill(BG, opacity=0.94)
            text = Text(label, color=color, font_size=19).move_to(ORIGIN)
            text.set_fill(color, opacity=1.0)
            text.set_stroke(width=0)
            fit_text_to_width(text, 3.80 - 0.18)
            text_shield = BackgroundRectangle(text, color=BG, fill_opacity=0.96, buff=0.04)
            outline.set_z_index(1)
            text_shield.set_z_index(2)
            text.set_z_index(3)
            self.validate_text_fits(text, bg, f"locked_node:{label}")
            locked_nodes.add(VGroup(bg, outline, text_shield, text).move_to(pos))
            col4_x_for_y = {-3.6: -5.1, 0.6: 1.1, 4.6: 4.4}
            connector_start = np.array([col4_x_for_y[x], -2.62, 0])
            connector_end = pos + UP * 0.40
            locked_edges.add(DashedLine(connector_start, connector_end, color=color, dash_length=0.16, stroke_width=2.0).set_opacity(0.55))

        unlock_pulses = VGroup()
        for i, edge in enumerate(edge_groups):
            dot_color = nodes[edges[i][1]][3]
            pulse = Dot(edge[1].get_start(), radius=0.045, color=dot_color)
            pulse.set_opacity(0.0)
            unlock_pulses.add(pulse)
        self.add(unlock_pulses)

        self.play(FadeIn(lanes), FadeIn(row_labels), FadeIn(title), FadeIn(subtitle), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(node_groups[i]) for i in range(7)], lag_ratio=0.07), run_time=1.5)
        self.play(LaggedStart(*[Create(edge_groups[i]) for i in range(7)], lag_ratio=0.06), run_time=1.6)
        for pulse in unlock_pulses[:7]:
            pulse.set_opacity(0.92)
        self.play(
            LaggedStart(*[MoveAlongPath(unlock_pulses[i], edge_groups[i][1]) for i in range(7)], lag_ratio=0.08),
            run_time=1.7,
            rate_func=linear,
        )
        for pulse in unlock_pulses[:7]:
            pulse.set_opacity(0.0)
        self.move_camera(frame_center=np.array([-3.5, 0.2, 0]), zoom=0.90, run_time=2.0)
        self.play(LaggedStart(*[FadeIn(node_groups[i]) for i in range(7, len(node_groups))], lag_ratio=0.08), run_time=1.7)
        self.play(LaggedStart(*[Create(edge_groups[i]) for i in range(7, len(edge_groups))], lag_ratio=0.07), FadeIn(speculative), run_time=2.1)
        for pulse in unlock_pulses[7:]:
            pulse.set_opacity(0.92)
        self.play(
            LaggedStart(*[MoveAlongPath(unlock_pulses[i], edge_groups[i][1]) for i in range(7, len(edge_groups))], lag_ratio=0.05),
            run_time=2.0,
            rate_func=linear,
        )
        for pulse in unlock_pulses[7:]:
            pulse.set_opacity(0.0)
        self.move_camera(frame_center=np.array([2.4, -0.55, 0]), zoom=0.98, run_time=3.2)
        self.play(FadeIn(locked_edges), FadeIn(locked_nodes), run_time=1.2)
        self.play(edge_groups[-4:].animate.set_opacity(1.0), speculative.animate.set_opacity(0.9), run_time=1.2)
        self.play(locked_nodes.animate.set_opacity(0.58), locked_edges.animate.set_opacity(0.42), run_time=0.8)
        self.move_camera(frame_center=ORIGIN, zoom=0.70, run_time=3.0)

        # ---- ADDITIVE BEAT: organic branching tree overlay ----
        # User feedback (and Gemini in three rounds) said the grid above reads
        # as a spreadsheet. Add a complementary beat that shows the SAME
        # transforms as an organic glowing tree growing root → branches →
        # leaves, so the viewer gets both the structured table and the tree.
        # Push the grid much further back so the overlay tree reads as the
        # foreground figure. Light grid behind, glowing tree in front.
        self.play(
            node_groups.animate.set_opacity(0.0),
            edge_groups.animate.set_opacity(0.025),
            speculative.animate.set_opacity(0.0),
            locked_nodes.animate.set_opacity(0.06),
            locked_edges.animate.set_opacity(0.04),
            lanes.animate.set_opacity(0.04),
            row_labels.animate.set_opacity(0.0),
            run_time=1.4,
        )

        overlay_subtitle = Text(
            "the same tree, drawn as it grows",
            color=WHITE, font_size=20,
        ).set_fill(WHITE, opacity=0.92).set_stroke(width=0)
        self.add_fixed_in_frame_mobjects(overlay_subtitle)
        overlay_subtitle.next_to(title, DOWN, buff=0.14)
        # Fade the original "unlocked | emerging | speculative" legend on the
        # overlay beat so the two subtitles don't stack — user flagged that
        # collision at 11:06.667.
        self.play(FadeOut(subtitle), FadeIn(overlay_subtitle), run_time=0.6)

        def organic_branch_3d(start_p, end_p, color, width=3.5):
            ctrl1 = start_p + (end_p - start_p) * 0.4 + np.array([0.0, abs(end_p[1] - start_p[1]) * 0.18, 0.0])
            ctrl2 = start_p + (end_p - start_p) * 0.7 + np.array([0.0, abs(end_p[1] - start_p[1]) * 0.06, 0.0])
            path = CubicBezier(start_p, ctrl1, ctrl2, end_p)
            path.set_stroke(color, width=width)
            glow = path.copy().set_stroke(color, width=width * 3.5, opacity=0.14)
            return VGroup(glow, path)

        # The grown tree lives at z=0.5 so it sits visually in front of the
        # faded grid. Root is in the lower-left empty corner so its label
        # doesn't sit on a grid card. Each node is a glow dot.
        grown_root_pos = np.array([-5.6, -2.6, 0.50])
        grown_root = VGroup(
            Dot(grown_root_pos, radius=0.20, color=GREEN).set_z_index(5),
            Dot(grown_root_pos, radius=0.52, color=GREEN).set_opacity(0.28).set_z_index(4),
        )
        grown_root_label = Text("transform\nmathematics", color=GREEN, font_size=18, line_spacing=0.8)
        grown_root_label.set_fill(GREEN, opacity=1).set_stroke(width=0)
        grown_root_label.move_to(grown_root_pos + np.array([0.0, -0.85, 0]))

        # Tier 1: three classical roots branching up-right. Shift x slightly
        # left of the grid's column centers so labels read cleanly.
        tier1_specs = [
            (np.array([-3.4,  2.30, 0.50]), "Fourier",  CYAN),
            (np.array([-3.4,  0.40, 0.50]), "Laplace",  GOLD),
            (np.array([-3.4, -1.50, 0.50]), "DCT",      VIOLET),
        ]
        tier1_nodes = VGroup()
        tier1_branches = VGroup()
        for pos, label, color in tier1_specs:
            branch = organic_branch_3d(grown_root_pos, pos, color, width=4.0)
            for sub in branch:
                sub.set_z_index(3)
            dot = Dot(pos, radius=0.13, color=color).set_z_index(5)
            aura = Dot(pos, radius=0.40, color=color).set_opacity(0.25).set_z_index(4)
            text = Text(label, color=color, font_size=19).set_fill(color, opacity=1).set_stroke(width=0)
            text.move_to(pos + np.array([0.0, 0.46, 0]))
            tier1_nodes.add(VGroup(aura, dot, text))
            tier1_branches.add(branch)

        # Tier 2: classical → learned representation transforms (the new root)
        learned_pos = np.array([0.5, 0.50, 0.50])
        learned_dot = Dot(learned_pos, radius=0.17, color=GREEN).set_z_index(5)
        learned_aura = Dot(learned_pos, radius=0.52, color=GREEN).set_opacity(0.30).set_z_index(4)
        learned_label = Text("learned representation\ntransforms", color=GREEN, font_size=18, line_spacing=0.78)
        learned_label.set_fill(GREEN, opacity=1).set_stroke(width=0)
        # Move the label OFF the central node so the converging Bezier branches
        # don't strike through it. Park it above-right of the hub instead.
        learned_label.move_to(learned_pos + np.array([1.95, 1.05, 0]))
        learned_label.set_z_index(8)
        # Small dark shield behind the label so any remaining branch passing
        # through reads as "behind" the text, not "cutting" it.
        learned_shield = BackgroundRectangle(learned_label, color=BG, fill_opacity=0.85, buff=0.10).set_z_index(7)
        learned_branches = VGroup()
        for tier1_pos, _, color in tier1_specs:
            branch = organic_branch_3d(tier1_pos, learned_pos, color, width=3.0)
            for sub in branch:
                sub.set_z_index(2)
                sub.set_stroke(color, width=3.0, opacity=0.55)
            learned_branches.add(branch)

        # Tier 3: emerging AI-workflow leaves (cyan), and speculative civ-scale tips (pink)
        leaf_specs = [
            (np.array([ 4.8,  2.50, 0.50]), "code agents",        CYAN, 1.0),
            (np.array([ 5.4,  1.25, 0.50]), "multimodal models",  VIOLET, 1.0),
            (np.array([ 5.6,  0.00, 0.50]), "V&V systems",        GREEN, 0.85),
            (np.array([ 5.4, -1.30, 0.50]), "self-inhabiting\ncompute", "#FF8FB0", 0.55),
            (np.array([ 4.8, -2.60, 0.50]), "autonomous\nexperiment loops", GOLD, 0.55),
        ]
        leaf_branches = VGroup()
        leaves = VGroup()
        for pos, label, color, opacity in leaf_specs:
            branch = organic_branch_3d(learned_pos, pos, color, width=2.6)
            for sub in branch:
                sub.set_z_index(2)
                sub.set_stroke(color, opacity=0.40 + 0.35 * opacity)
            dot = Dot(pos, radius=0.10, color=color).set_opacity(opacity).set_z_index(5)
            aura = Dot(pos, radius=0.30, color=color).set_opacity(0.16 * opacity).set_z_index(4)
            text = Text(label, color=color, font_size=15, line_spacing=0.78).set_fill(color, opacity=opacity).set_stroke(width=0)
            # Push the labels above the dot with a larger gap (was 0.40/0.52,
            # now 0.62/0.80) so the incoming Bezier branch's tail doesn't
            # graze the label bottom edge. Each label also gets a higher
            # z_index than the branch so it wins any visual overlap.
            text.set_z_index(6)
            text.move_to(pos + np.array([0.0, 0.62 if "\n" not in label else 0.80, 0]))
            leaf_branches.add(branch)
            leaves.add(VGroup(aura, dot, text))

        # Grow the tree root → tier1 → learned → leaves
        self.play(FadeIn(grown_root), FadeIn(grown_root_label), run_time=0.9)
        self.play(LaggedStart(*[Create(b) for b in tier1_branches], lag_ratio=0.15), run_time=1.6)
        self.play(LaggedStart(*[FadeIn(n) for n in tier1_nodes], lag_ratio=0.15), run_time=1.2)
        self.play(LaggedStart(*[Create(b) for b in learned_branches], lag_ratio=0.12), run_time=1.6)
        self.play(FadeIn(VGroup(learned_aura, learned_dot, learned_shield, learned_label)), run_time=0.9)
        self.play(LaggedStart(*[Create(b) for b in leaf_branches], lag_ratio=0.12), run_time=1.6)
        self.play(LaggedStart(*[FadeIn(l) for l in leaves], lag_ratio=0.12), run_time=1.4)
        # Pulse the whole tree once to make the "growth" reading land
        self.play(
            VGroup(tier1_nodes, leaves, VGroup(learned_aura, learned_dot)).animate.scale(1.04),
            run_time=0.8,
        )
        self.play(
            VGroup(tier1_nodes, leaves, VGroup(learned_aura, learned_dot)).animate.scale(1 / 1.04),
            run_time=0.8,
        )

        # ---- RESEARCHED LINEAGE BEAT ------------------------------------------
        # The first table-like grid is useful for overview, but the user kept
        # pushing for a real technology tree. This beat is sourced from the
        # Mermaid lineage draft and shows ancestry/branching rather than rows.
        try:
            mermaid_labels, _ = parse_mermaid(TECH_TREE_MERMAID)
        except Exception:
            mermaid_labels = {}

        short_labels = {
            "representation": "world rep",
            "vector_space": "transform",
            "fourier_laplace": "Fourier/Laplace",
            "dct": "DCT",
            "embeddings": "embeddings",
            "transformers": "transformer",
            "llms": "LLMs",
            "code_agents": "code",
            "formal_verifiers": "proof tools",
            "vv_systems": "V&V",
            "reliable_agents": "reliable",
            "civ_rd": "civ R&D",
        }
        lineage_specs = {
            "representation":   (-5.75,  0.75, WHITE),
            "vector_space":     (-4.25,  0.75, GREEN),
            "fourier_laplace":  (-3.15,  1.85, CYAN),
            "dct":              (-3.15, -0.35, VIOLET),
            "embeddings":       (-2.40,  0.75, GREEN),
            "transformers":     (-0.95,  0.75, GOLD),
            "llms":             ( 0.35,  0.75, GOLD),
            "code_agents":      ( 1.62,  0.75, CYAN),
            "formal_verifiers": ( 1.62, -0.78, GREEN),
            "vv_systems":       ( 3.05,  0.05, GREEN),
            "reliable_agents":  ( 4.28,  0.05, GREEN),
            "civ_rd":           ( 5.48,  0.05, GOLD),
        }
        lineage_edges = [
            ("representation", "vector_space"),
            ("vector_space", "fourier_laplace"),
            ("vector_space", "dct"),
            ("vector_space", "embeddings"),
            ("embeddings", "transformers"),
            ("transformers", "llms"),
            ("llms", "code_agents"),
            ("formal_verifiers", "vv_systems"),
            ("code_agents", "vv_systems"),
            ("vv_systems", "reliable_agents"),
            ("reliable_agents", "civ_rd"),
        ]

        def lineage_pos(key: str) -> np.ndarray:
            x, y, _ = lineage_specs[key]
            return np.array([x, y, 0.62])

        def lineage_node(key: str) -> VGroup:
            x, y, color = lineage_specs[key]
            label = short_labels.get(key) or mermaid_labels.get(key, key.replace("_", " "))
            pos = np.array([x, y, 0.62])
            max_line = max(len(part) for part in label.split("\n"))
            width = min(1.88, max(1.10, 0.11 * max_line + 0.52))
            plate = RoundedRectangle(width=width, height=0.48, corner_radius=0.08, color=color, stroke_width=1.7)
            plate.set_fill(BG, opacity=0.94).set_z_index(6)
            plate.move_to(pos)
            glow = plate.copy().set_stroke(color, width=7, opacity=0.16).set_z_index(5)
            dot = Dot(pos + LEFT * (width / 2 - 0.16), radius=0.055, color=color).set_z_index(8)
            text = Text(label, color=WHITE, font_size=14, line_spacing=0.82)
            text.set_fill(WHITE, opacity=0.98).set_stroke(width=0)
            fit_text_to_width(text, width - 0.34)
            text.move_to(pos + RIGHT * 0.08)
            text.set_z_index(8)
            return VGroup(glow, plate, dot, text)

        lineage_edge_groups = VGroup()
        for src, dst in lineage_edges:
            start = lineage_pos(src)
            end = lineage_pos(dst)
            line = Line(start, end, color=lineage_specs[dst][2], stroke_width=2.3)
            line.set_opacity(0.58)
            glow = line.copy().set_stroke(lineage_specs[dst][2], width=8, opacity=0.12)
            lineage_edge_groups.add(VGroup(glow, line))
        lineage_node_groups = VGroup(*[lineage_node(key) for key in lineage_specs])
        lineage_title = Text("actual lineage: math, media, software, agents, organizations",
                             color=WHITE, font_size=22)
        lineage_title.set_fill(WHITE, opacity=0.96).set_stroke(width=0)
        lineage_title.to_edge(UP).shift(DOWN * 0.58)
        self.add_fixed_in_frame_mobjects(lineage_title)

        self.play(
            VGroup(grown_root, grown_root_label, tier1_nodes, tier1_branches,
                   VGroup(learned_aura, learned_dot, learned_shield, learned_label),
                   learned_branches, leaf_branches, leaves).animate.set_opacity(0.0),
            FadeOut(title),
            FadeOut(overlay_subtitle),
            FadeIn(lineage_title),
            run_time=0.9,
        )
        self.play(LaggedStart(*[Create(edge) for edge in lineage_edge_groups], lag_ratio=0.035), run_time=2.0)
        self.play(LaggedStart(*[FadeIn(node) for node in lineage_node_groups], lag_ratio=0.035), run_time=2.0)
        self.wait(1.2)

        # ---- NEW SUB-SCENE: workflow examples pop in --------------------------
        # User asked for "every workflow where humans pass around representation
        # of intent" to get a dedicated visualization with concrete examples.
        # Clear EVERYTHING (the entire tree + overlay), then pop in 6 named
        # workflows as glowing icon-dots.
        self.wait_until_phrase(
            "writing programming design research planning review coordination education",
            offset=-0.5,
            fallback=0.5,
        )
        all_tree = VGroup(
            node_groups, edge_groups, speculative, locked_nodes, locked_edges,
            lanes, row_labels,
            grown_root, grown_root_label,
            tier1_nodes, tier1_branches,
            VGroup(learned_aura, learned_dot, learned_shield, learned_label),
            learned_branches, leaf_branches, leaves,
            lineage_title, lineage_edge_groups, lineage_node_groups,
            overlay_subtitle, title,
        )
        self.play(FadeOut(all_tree), run_time=1.0)
        self.clear_fixed(title, subtitle, overlay_subtitle)

        workflow_title = Text("any workflow where humans pass around intent",
                              color=WHITE, font_size=26).set_fill(WHITE, opacity=0.95).set_stroke(width=0)
        workflow_title.to_edge(UP).shift(DOWN * 0.32)
        self.add_fixed_in_frame_mobjects(workflow_title)
        self.play(FadeIn(workflow_title), run_time=0.6)

        workflow_specs = [
            ("writing",     CYAN,   LEFT * 4.40 + UP * 0.90),
            ("programming", GOLD,   ORIGIN + UP * 0.90),
            ("design",      VIOLET, RIGHT * 4.40 + UP * 0.90),
            ("research",    GREEN,  LEFT * 4.40 + DOWN * 0.90),
            ("planning",    "#FF8FB0", ORIGIN + DOWN * 0.90),
            ("review",      CYAN,   RIGHT * 4.40 + DOWN * 0.90),
        ]
        workflow_icons = VGroup()
        for label, color, pos in workflow_specs:
            glow = Dot(pos, radius=0.50, color=color).set_opacity(0.18)
            inner = Dot(pos, radius=0.18, color=color).set_opacity(0.92)
            text = Text(label, color=color, font_size=22).set_fill(color, opacity=1).set_stroke(width=0)
            text.move_to(pos + DOWN * 0.62)
            workflow_icons.add(VGroup(glow, inner, text))
        self.add_fixed_in_frame_mobjects(workflow_icons)
        for icon in workflow_icons:
            self.play(FadeIn(icon, shift=UP * 0.12), run_time=0.5)
            self.wait(0.35)

        self.wait_until_phrase("Any workflow where humans pass around", offset=-0.25, fallback=0.4)
        coda = Text("…all touch the new transform layer", color=GREEN, font_size=20).set_fill(GREEN, opacity=1).set_stroke(width=0)
        coda.to_edge(DOWN).shift(UP * 0.35)
        self.add_fixed_in_frame_mobjects(coda)
        self.play(FadeIn(coda), run_time=0.6)

        self.remaining_wait()


class S09LimitTrends(Storyboard2DScene):
    target_seconds = 34

    def construct(self):
        title = self.glow_text("thinking in the limit", WHITE, 32).to_edge(UP).shift(DOWN * 0.12)
        method = Text("find the trends  →  project them toward their asymptotes", color=WHITE, font_size=20).set_fill(WHITE, opacity=0.86).set_stroke(width=0)
        method.next_to(title, DOWN, buff=0.18)
        self.play(FadeIn(title), FadeIn(method), run_time=1.0)

        axes_group = VGroup()
        cards = [
            ("accuracy", "up", GREEN, lambda x: 1 - math.exp(-0.55 * x)),
            ("complexity", "up", VIOLET, lambda x: 0.10 * x ** 1.55),
            ("generation cost", "down", GOLD, lambda x: math.exp(-0.55 * x)),
        ]
        for i, (label, trend, color, fn) in enumerate(cards):
            ax = Axes(x_range=[0, 5, 1], y_range=[0, 1.2, 0.2], x_length=3.2, y_length=2.2,
                      axis_config={"color": AXIS, "stroke_width": 2, "include_ticks": False}, tips=False)
            ax.move_to(np.array([-4.1 + i * 4.1, -0.25, 0]))
            curve = ax.plot(lambda x, f=fn: min(1.05, max(0.03, f(x))), x_range=[0.1, 4.7, 0.1],
                            color=color, stroke_width=4)
            curve_glow = curve.copy().set_stroke(color, width=12, opacity=0.18)
            text = Text(label, color=color, font_size=22).next_to(ax, UP, buff=0.24)
            arrow = Text("↑" if trend == "up" else "↓", color=color, font_size=34).next_to(text, RIGHT, buff=0.12)
            axes_group.add(VGroup(ax, curve_glow, curve, text, arrow))

        self.play(LaggedStart(*[FadeIn(g[0], g[3], g[4]) for g in axes_group], lag_ratio=0.16), run_time=1.4)
        self.play(LaggedStart(*[Create(VGroup(g[1], g[2])) for g in axes_group], lag_ratio=0.18), run_time=2.1)

        bottleneck = self.glow_text("when those move far enough, the bottleneck changes", CYAN, 24)
        bottleneck.to_edge(DOWN).shift(UP * 0.62)
        self.play(FadeIn(bottleneck), run_time=0.9)

        questions = VGroup(
            Text("generate?", color=WHITE, font_size=26).set_fill(WHITE, opacity=0.85).set_stroke(width=0),
            Text("validate?", color=GREEN, font_size=30).set_fill(GREEN, opacity=1).set_stroke(width=0),
            Text("verify?", color=GOLD, font_size=30).set_fill(GOLD, opacity=1).set_stroke(width=0),
            Text("trust?", color=CYAN, font_size=30).set_fill(CYAN, opacity=1).set_stroke(width=0),
        ).arrange(RIGHT, buff=0.65)
        questions.move_to(DOWN * 1.55)
        # Stagger AND hold each question on screen long enough to read aloud
        # (user: "text on screen way too short to read"). Each question gets
        # a deliberate 1.6s reveal + 1.4s solo hold before the next.
        for q in questions:
            self.play(FadeIn(q, shift=UP * 0.10), run_time=0.7)
            self.wait(1.4)
        artifact_flood = VGroup()
        rng = np.random.default_rng(109)
        for i in range(72):
            x = rng.uniform(-5.7, -2.2)
            y = rng.uniform(-2.8, -1.55)
            color = CYAN if i % 2 else VIOLET
            dot = Dot(np.array([x, y, 0]), radius=rng.uniform(0.018, 0.034), color=color).set_opacity(0.0)
            artifact_flood.add(dot)
        self.add(artifact_flood)
        evidence_gate = VGroup(
            # Vertical glowing threshold instead of a UI button — Gemini called
            # the rounded rect "a UI button". The threshold reads as a field
            # that artifacts have to cross, not a clickable widget.
            Line(UP * 0.45, DOWN * 0.45, color=GOLD, stroke_width=6),
            Text("evidence\ngate", color=GOLD, font_size=20, line_spacing=0.78).set_fill(GOLD, opacity=1).set_stroke(width=0).shift(RIGHT * 0.85),
        ).move_to(RIGHT * 3.8 + DOWN * 2.14)
        gate_glow = evidence_gate[0].copy().set_stroke(GOLD, width=12, opacity=0.14)
        gate = VGroup(gate_glow, evidence_gate)
        pressure = neon_arrow(LEFT * 2.0 + DOWN * 2.14, RIGHT * 2.9 + DOWN * 2.14, color=GOLD, width=3.2)
        self.play(FadeOut(questions), bottleneck.animate.shift(DOWN * 0.18).set_opacity(0.72), FadeIn(gate), Create(pressure), run_time=0.8)
        self.play(
            LaggedStart(*[d.animate.set_opacity(0.75).shift(RIGHT * rng.uniform(1.8, 4.2)) for d in artifact_flood], lag_ratio=0.008),
            run_time=2.0,
        )
        self.play(gate.animate.scale(1.08), pressure.animate.set_stroke(width=5.0), run_time=0.6)
        self.play(gate.animate.scale(0.94), run_time=0.5)

        # Narration walk: accuracy / complexity / cost / new bottleneck
        walk_pos = DOWN * 3.20
        narration_beats = [
            ("accuracy keeps going up", GREEN),
            ("complexity keeps going up", VIOLET),
            ("the cost of another artifact keeps going down", GOLD),
            ("paragraph · image · program · test · design · experiment", CYAN),
            ("the question shifts: what can we validate?", GREEN),
            ("what can we verify? what can we trust enough to ship?", GOLD),
        ]
        for caption, color in narration_beats:
            card = self.glow_text(caption, color, 21).move_to(walk_pos)
            self.play(FadeIn(card, shift=UP * 0.10), run_time=0.6)
            # Pulse the evidence gate during each card
            ghost = gate[0].copy()
            self.add(ghost)
            self.play(ghost.animate.scale(1.10).set_opacity(0.0), run_time=2.4, rate_func=rate_functions.ease_out_sine)
            self.remove(ghost)
            self.play(FadeOut(card), run_time=0.4)

        self.remaining_wait()


class S10ValidationVerification(Storyboard2DScene):
    target_seconds = 45

    def construct(self):
        title = self.glow_text("validation + verification", WHITE, 31).to_edge(UP).shift(DOWN * 0.12)
        subtitle = Text("the classic V-model becomes the bottleneck", color=WHITE, font_size=19).set_fill(WHITE, opacity=0.86).set_stroke(width=0)
        subtitle.next_to(title, DOWN, buff=0.12)
        self.play(FadeIn(title), FadeIn(subtitle), run_time=0.9)

        left_specs = [
            ("requirement\nspecification", GREEN, np.array([-4.7, 2.05, 0])),
            ("high level\ndesign", CYAN, np.array([-3.45, 1.08, 0])),
            ("detail\ndesign", VIOLET, np.array([-2.25, 0.08, 0])),
            ("program\nspecification", GOLD, np.array([-1.10, -0.98, 0])),
        ]
        right_specs = [
            ("user acceptance\ntesting", GREEN, np.array([4.75, 2.05, 0])),
            ("system\ntesting", CYAN, np.array([3.50, 1.08, 0])),
            ("integration\ntesting", VIOLET, np.array([2.32, 0.08, 0])),
            ("unit\ntesting", GOLD, np.array([1.15, -0.98, 0])),
        ]

        left_nodes = VGroup()
        right_nodes = VGroup()

        def v_node(label: str, color: str, pos: np.ndarray, width: float = 1.9) -> VGroup:
            plate = RoundedRectangle(width=width, height=0.68, corner_radius=0.06, color=color, stroke_width=2.1)
            plate.set_fill(BG, opacity=0.96)
            glow = plate.copy().set_stroke(color, width=9, opacity=0.14)
            text = Text(label, color=WHITE, font_size=15, line_spacing=0.76)
            text.set_fill(WHITE, opacity=1)
            text.set_stroke(width=0)
            fit_text_to_width(text, width - 0.18)
            text.move_to(plate)
            self.validate_text_fits(text, plate, f"v_node:{label}")
            glow.set_z_index(0)
            plate.set_z_index(1)
            text.set_z_index(2)
            return VGroup(glow, plate, text).move_to(pos)

        for label, color, pos in left_specs:
            left_nodes.add(v_node(label, color, pos))

        for label, color, pos in right_specs:
            right_nodes.add(v_node(label, color, pos))

        impl = v_node("coding", RED, np.array([0.0, -2.16, 0]), width=1.65)

        left_centers = [pos for _, _, pos in left_specs]
        right_centers = [pos for _, _, pos in right_specs]
        left_path = VGroup(*[
            neon_line(a + RIGHT * 0.56 + DOWN * 0.05, b + LEFT * 0.56 + UP * 0.05, color=CYAN, width=2.8)
            for a, b in zip(left_centers, left_centers[1:] + [impl.get_center()])
        ])
        right_path = VGroup(*[
            neon_line(a + RIGHT * 0.56 + UP * 0.05, b + LEFT * 0.56 + DOWN * 0.05, color=GOLD, width=2.8)
            for a, b in zip([impl.get_center()] + list(reversed(right_centers))[1:], list(reversed(right_centers)))
        ])

        trace_lines = VGroup()
        for left, right, (_, color, _) in zip(left_centers, right_centers, right_specs):
            line = Arrow(left + RIGHT * 0.98, right + LEFT * 0.98, color=color, stroke_width=2.0, buff=0.08, max_tip_length_to_length_ratio=0.035)
            line.set_opacity(0.72)
            trace_lines.add(line)

        verify_axis = VGroup(
            Line(np.array([-5.75, 1.75, 0]), np.array([-0.78, -2.58, 0]), color=GREEN, stroke_width=4),
            Arrow(np.array([-5.75, 1.75, 0]), np.array([-0.78, -2.58, 0]), color=GREEN, stroke_width=0, buff=0, max_tip_length_to_length_ratio=0.04),
        )
        verify_axis[0].set_opacity(0.68)
        validate_axis = VGroup(
            Line(np.array([0.78, -2.58, 0]), np.array([5.75, 1.75, 0]), color=GREEN, stroke_width=4),
            Arrow(np.array([0.78, -2.58, 0]), np.array([5.75, 1.75, 0]), color=GREEN, stroke_width=0, buff=0, max_tip_length_to_length_ratio=0.04),
        )
        validate_axis[0].set_opacity(0.68)
        # Gemini called the rotated axis labels a "formatting error" — keep the
        # spatial cue but read them flat. Pulled inside the safe area so they
        # don't clip at the prototype's 854px width.
        verify_label = self.glow_text("verification", GREEN, 22).move_to(LEFT * 4.90 + UP * 2.55)
        validate_label = self.glow_text("validation", GREEN, 22).move_to(RIGHT * 4.90 + UP * 2.55)
        v_model = VGroup(verify_axis, validate_axis, left_nodes, right_nodes, impl, left_path, right_path, trace_lines, verify_label, validate_label)

        self.play(Create(verify_axis), Create(validate_axis), FadeIn(verify_label), FadeIn(validate_label), run_time=1.1)
        self.play(LaggedStart(*[FadeIn(n) for n in left_nodes], lag_ratio=0.13), run_time=1.5)
        self.play(LaggedStart(*[Create(edge) for edge in left_path], lag_ratio=0.15), FadeIn(impl), run_time=1.8)
        self.play(LaggedStart(*[Create(edge) for edge in right_path], lag_ratio=0.15), LaggedStart(*[FadeIn(n) for n in reversed(right_nodes)], lag_ratio=0.12), run_time=2.0)
        self.play(LaggedStart(*[Create(t) for t in trace_lines], lag_ratio=0.10), run_time=1.6)
        # Requirements and evidence are animated as packets traveling through
        # the V, so this reads as an active workflow rather than a static chart.
        req_packets = VGroup(*[Dot(left_path[0][1].get_start(), radius=0.05, color=GREEN).set_opacity(0.0) for _ in left_path])
        ev_packets = VGroup(*[Dot(right_path[0][1].get_start(), radius=0.05, color=GOLD).set_opacity(0.0) for _ in right_path])
        trace_packets = VGroup(*[Dot(t.get_start(), radius=0.04, color=t.get_color()).set_opacity(0.0) for t in trace_lines])
        self.add(req_packets, ev_packets, trace_packets)
        for packet in req_packets:
            packet.set_opacity(0.95)
        self.play(
            LaggedStart(*[MoveAlongPath(packet, edge[1]) for packet, edge in zip(req_packets, left_path)], lag_ratio=0.18),
            run_time=1.7,
            rate_func=linear,
        )
        for packet in req_packets:
            packet.set_opacity(0.0)
        for packet in trace_packets:
            packet.set_opacity(0.95)
        self.play(
            LaggedStart(*[MoveAlongPath(packet, line) for packet, line in zip(trace_packets, trace_lines)], lag_ratio=0.10),
            run_time=1.4,
            rate_func=linear,
        )
        for packet in trace_packets:
            packet.set_opacity(0.0)
        for packet in ev_packets:
            packet.set_opacity(0.95)
        self.play(
            LaggedStart(*[MoveAlongPath(packet, edge[1]) for packet, edge in zip(ev_packets, right_path)], lag_ratio=0.18),
            run_time=1.7,
            rate_func=linear,
        )
        for packet in ev_packets:
            packet.set_opacity(0.0)
        self.play(v_model.animate.scale(1.05).shift(UP * 0.05), run_time=1.4)
        self.play(v_model.animate.scale(0.92).shift(UP * 0.02), run_time=1.2)

        rng = np.random.default_rng(22)
        artifacts = VGroup()
        for i in range(44):
            color = CYAN if i % 3 else VIOLET
            dot = Dot(np.array([rng.uniform(-0.8, 0.8), rng.uniform(-2.55, -1.75), 0]), radius=rng.uniform(0.025, 0.045), color=color)
            aura = Dot(dot.get_center(), radius=dot.radius * 3.2, color=color).set_opacity(0.20)
            artifacts.add(VGroup(aura, dot))

        flood = Text("generation gets cheap", color=CYAN, font_size=21).move_to(DOWN * 3.08)
        scarce = self.glow_text("evidence becomes the work", GOLD, 24).move_to(DOWN * 3.08)
        self.play(FadeIn(artifacts, lag_ratio=0.01), FadeIn(flood), run_time=1.2)
        self.play(
            artifacts.animate.scale(1.25).shift(UP * 0.24).set_opacity(0.24),
            trace_lines.animate.set_stroke(width=3.4),
            run_time=1.4,
        )
        self.play(Transform(flood, scarce), run_time=0.8)
        # Hold "evidence becomes the work" long enough to read — it was faded
        # almost immediately after the morph (user: "doesn't appear long
        # enough"). Linger until just before the narration walk's first line.
        t_next = self.phrase_time("It can satisfy the prompt and fail the purpose")
        t_now = getattr(self.renderer, "time", 0.0) or 0.0
        hold = CAPTION_MIN_HOLD if t_next is None else min(6.0, max(CAPTION_MIN_HOLD, t_next - t_now - 0.6))
        self.breathing_wait(hold)

        # Fade the "evidence becomes the work" caption before the narration
        # walk starts so the bottom captions don't stack on it.
        self.play(FadeOut(flood), run_time=0.4)
        # Narration walk through "you need requirements / traces / tests / reviews / evidence"
        walk_pos = DOWN * 3.08  # the slot that just vacated
        narration_beats = [
            ("a model can satisfy the prompt and fail the purpose", "#FF7FA8", "It can satisfy the prompt and fail the purpose"),
            ("plausible output becomes abundant", VIOLET, "plausible output becomes abundant"),
            ("trustworthy output becomes scarce", GOLD,
             ["Trustworthy output that still fits its purpose becomes scarce",
              "Trustworthy output", "Trustworthy output becomes scarce"]),
            ("requirements · traces · tests · reviews · monitors", WHITE, "You need requirements"),
            ("when generation gets cheap, evidence becomes the work", GOLD, "When generation is expensive"),
        ]
        for idx, (caption, color, phrase) in enumerate(narration_beats):
            self.wait_until_phrase(phrase, offset=-0.2, fallback=0.2)
            card = self.glow_text(caption, color, 21).move_to(walk_pos)
            self.play(FadeIn(card, shift=UP * 0.15), run_time=0.6)
            # Linger each caption until just before the next narration line; the
            # final "evidence becomes the work" caption lingers until the funnel
            # transition ("When generation becomes cheap") so it isn't cut before
            # it's readable (user flagged it getting clipped by the scene change).
            next_phrase = narration_beats[idx + 1][2] if idx + 1 < len(narration_beats) else "When generation becomes cheap"
            t_next = self.phrase_time(next_phrase)
            t_now = getattr(self.renderer, "time", 0.0) or 0.0
            # The last caption ("evidence becomes the work") fills its gap right
            # up to the funnel transition so it's readable even at 1.25x speed.
            margin = 0.15 if idx + 1 >= len(narration_beats) else 0.6
            hold = CAPTION_MIN_HOLD if t_next is None else min(7.0, max(CAPTION_MIN_HOLD, t_next - t_now - margin))
            self.breathing_wait(hold)
            self.play(FadeOut(card), run_time=0.4)

        # Send another evidence pulse up the validation side for closure
        ev_packets_b = VGroup(*[Dot(right_path[0][1].get_start(), radius=0.06, color=GOLD).set_opacity(0.95) for _ in right_path])
        self.add(ev_packets_b)
        self.play(
            LaggedStart(*[MoveAlongPath(packet, edge[1]) for packet, edge in zip(ev_packets_b, right_path)], lag_ratio=0.18),
            run_time=2.4,
            rate_func=linear,
        )
        for packet in ev_packets_b:
            packet.set_opacity(0.0)

        # ---- ADDITIVE BEAT: fountain of generated artifacts filtered upward ----
        # Gemini wanted the V-model replaced with this geometric metaphor.
        # CLEAR THE SCREEN entirely (V-model fades out fully, INCLUDING title
        # and subtitle) and build a fresh geometric metaphor. User feedback:
        # the half-arcs were geometrically confusing AND the V-model title
        # stack collided with the new funnel header.
        self.wait_until_phrase("When generation becomes cheap", offset=-0.4, fallback=0.6)
        self.play(
            v_model.animate.set_opacity(0.0),
            artifacts.animate.set_opacity(0.0),
            flood.animate.set_opacity(0.0),
            title.animate.set_opacity(0.0),
            subtitle.animate.set_opacity(0.0),
            run_time=1.0,
        )

        funnel_title = Text("when generation is cheap, evidence is the work",
                            color=WHITE, font_size=24).set_fill(WHITE, opacity=0.95).set_stroke(width=0)
        funnel_title.to_edge(UP).shift(DOWN * 0.18)
        self.play(FadeIn(funnel_title), run_time=0.6)

        # Funnel geometry: trapezoidal stages stacked vertically. Each stage
        # has a top width (smaller) and a bottom width (larger) and a "gate"
        # label. Generation flows UP through them.
        gen_rng = np.random.default_rng(311)

        # Y bands (bottom→top): pool → traces → tests → evidence → shipped
        stages = [
            # (bottom_y, top_y, bottom_w, top_w, label, color)
            (-2.95, -1.85, 6.40, 4.00, "generated artifacts (cheap)", CYAN),
            (-1.85, -0.50, 4.00, 2.60, "traces",                       CYAN),
            (-0.50,  0.85, 2.60, 1.60, "tests",                        VIOLET),
            ( 0.85,  2.20, 1.60, 0.90, "evidence",                     GOLD),
        ]
        funnel_walls = VGroup()
        funnel_labels = VGroup()
        for bot_y, top_y, bot_w, top_w, label, color in stages:
            # Left and right diagonal walls of this stage
            left_wall = Line(
                np.array([-bot_w / 2, bot_y, 0]),
                np.array([-top_w / 2, top_y, 0]),
                color=color, stroke_width=3,
            ).set_opacity(0.85)
            right_wall = Line(
                np.array([ bot_w / 2, bot_y, 0]),
                np.array([ top_w / 2, top_y, 0]),
                color=color, stroke_width=3,
            ).set_opacity(0.85)
            # Stage gate label on the right outside the wall
            tag = Text(label, color=color, font_size=16).set_fill(color, opacity=1).set_stroke(width=0)
            tag.move_to(np.array([bot_w / 2 + 1.10, (bot_y + top_y) / 2, 0]))
            funnel_walls.add(left_wall, right_wall)
            funnel_labels.add(tag)
        self.play(
            LaggedStart(*[Create(w) for w in funnel_walls], lag_ratio=0.06),
            run_time=1.6,
        )
        self.play(LaggedStart(*[FadeIn(t) for t in funnel_labels], lag_ratio=0.15), run_time=1.0)

        reject_label = Text("dim dots = filtered out before evidence", color="#FF8FB0", font_size=17)
        reject_label.set_fill("#FF8FB0", opacity=1).set_stroke(width=0)
        reject_label.move_to(np.array([-3.55, -3.48, 0]))
        self.play(FadeIn(reject_label), run_time=0.5)

        # Dots start in a wide pool at the bottom and flow up through the funnel.
        # Throughput at each stage drops, so fewer dots survive each gate.
        pool = VGroup()
        for _ in range(120):
            x = gen_rng.uniform(-3.0, 3.0)
            y = gen_rng.uniform(-3.40, -2.95)
            color = CYAN if gen_rng.random() < 0.55 else VIOLET
            d = Dot(np.array([x, y, 0]), radius=gen_rng.uniform(0.030, 0.055), color=color).set_opacity(0.0)
            pool.add(d)
        self.add(pool)
        self.play(FadeIn(pool, lag_ratio=0.005), run_time=1.2)

        # At each stage transition, lift the surviving dots to its top width
        # and reject the rest (they fall away below the funnel base).
        alive = list(pool.submobjects)
        for (bot_y, top_y, bot_w, top_w, _label, color), throughput in zip(stages, [0.85, 0.55, 0.40, 0.25]):
            if not alive:
                break
            keep = max(1, int(len(alive) * throughput))
            gen_rng.shuffle(alive)
            survivors = alive[:keep]
            lost = alive[keep:]
            anims = []
            half_w = top_w / 2
            for d in survivors:
                # Distribute survivors evenly across the stage top width.
                tx = gen_rng.uniform(-half_w * 0.85, half_w * 0.85)
                anims.append(d.animate.move_to(np.array([tx, top_y - 0.06, 0])).set_color(color))
            for d in lost:
                # Rejected dots peel OUTWARD through the sides and dim (stay
                # visible at 0.22), instead of plunging straight down to the
                # bottom. The downward plunge fought the upward survivor flow and
                # made the whole path read top→down; now the only strong vertical
                # motion is dots rising up the funnel, with rejects spilling out
                # the sides at each gate (user: "wouldn't they start at the
                # bottom and go up instead of start at the top and go down?").
                cx = d.get_center()
                side = 1.0 if cx[0] >= 0 else -1.0
                out_x = side * gen_rng.uniform(4.6, 6.2)
                out_y = cx[1] - gen_rng.uniform(0.2, 0.8)
                anims.append(d.animate.move_to(np.array([out_x, out_y, 0])).set_opacity(0.22).scale(0.55))
            if anims:
                self.play(*anims, run_time=1.4, rate_func=rate_functions.ease_in_out_sine)
            alive = survivors

        # The handful of survivors land at the tip — "shipped" cluster.
        if alive:
            survivors_final = VGroup(*alive)
            anims = []
            for d in survivors_final:
                tx = gen_rng.uniform(-0.30, 0.30)
                anims.append(d.animate.move_to(np.array([tx, 2.55, 0])).set_color(GREEN).set_opacity(1))
            self.play(*anims, run_time=0.9)
        shipped_label = Text("survivors: passed every evidence gate",
                             color=GREEN, font_size=19).set_fill(GREEN, opacity=1).set_stroke(width=0)
        shipped_label.move_to(np.array([4.55, 2.55, 0]))
        shipped_shield = BackgroundRectangle(shipped_label, color=BG, fill_opacity=0.92, buff=0.06)
        self.play(FadeIn(shipped_shield), FadeIn(shipped_label), run_time=0.7)

        self.remaining_wait()


class S11SelfInhabitingCompute(StoryboardScene):
    target_seconds = 52

    def construct(self):
        self.set_camera_orientation(phi=56 * DEGREES, theta=-68 * DEGREES, zoom=0.72, focal_distance=9)
        title = self.glow_text("self-inhabiting compute", WHITE, 30).to_edge(UP).shift(DOWN * 0.08)
        self.add_fixed_in_frame_mobjects(title)
        self.play(FadeIn(title), run_time=0.8)

        axes = self.bright_axes(x_range=(-2.5, 2.5, 1), y_range=(-2.2, 2.2, 1), z_range=(-1.8, 1.8, 1), x_length=3.8, y_length=3.4, z_length=2.6)
        axes.shift(LEFT * 4.0 + DOWN * 0.15)
        state_cloud = VGroup()
        rng = np.random.default_rng(13)
        for _ in range(34):
            p = rng.normal(scale=0.62, size=3)
            state_cloud.add(glow_dot(axes.c2p(p[0], p[1], p[2]), CYAN, radius=0.045))

        transform_core = Sphere(radius=0.46, resolution=(18, 36), color=VIOLET)
        transform_core.set_opacity(0.30).move_to(LEFT * 0.55 + UP * 0.02)
        transform_ring = Torus(major_radius=0.78, minor_radius=0.018, color=VIOLET).move_to(transform_core)
        transform_glow = Sphere(radius=0.82, resolution=(12, 24), color=VIOLET).set_opacity(0.08).move_to(transform_core)
        # Push the core label higher and use brighter VIOLET so it sits cleanly
        # above the sphere instead of overlapping its glow.
        core_label = Text("learned transform", color=VIOLET, font_size=20).set_fill(VIOLET, opacity=1).set_stroke(width=0).move_to(transform_core.get_center() + UP * 2.05)
        self.add_fixed_orientation_mobjects(core_label)

        # Gemini called the original solid cubes "minecraft-y". Render the
        # substrate as glowing wireframe nodes connected by faint lines so it
        # reads as an abstract execution lattice instead of physical blocks.
        hardware = VGroup()
        for i in range(4):
            for j in range(3):
                pos = RIGHT * 3.05 + np.array([i * 0.42, j * 0.42, 0.08 * ((i + j) % 2)]) + DOWN * 0.55
                core = Sphere(radius=0.07, resolution=(8, 12), color=GREEN).set_opacity(0.55).move_to(pos)
                halo = Sphere(radius=0.12, resolution=(6, 10), color=GREEN).set_opacity(0.16).move_to(pos)
                hardware.add(VGroup(halo, core))
        memory_grid = VGroup()
        for i in range(6):
            for j in range(4):
                cell = Square(side_length=0.13, color=BLUE, stroke_width=0.7)
                cell.set_fill(BLUE, opacity=0.05 + 0.05 * ((i + j) % 2))
                cell.move_to(RIGHT * 3.68 + DOWN * 1.36 + np.array([i * 0.16, j * 0.16, 0.04]))
                memory_grid.add(cell)
        hw_label = Text("execution\nsubstrate", color=GREEN, font_size=17, line_spacing=0.84).move_to(RIGHT * 4.25 + UP * 1.50)
        self.add_fixed_orientation_mobjects(hw_label)

        arrow1 = neon_arrow(LEFT * 2.75 + DOWN * 0.03, LEFT * 1.08 + DOWN * 0.03, color=CYAN, width=4)
        arrow2 = neon_arrow(RIGHT * 0.05 + DOWN * 0.03, RIGHT * 2.64 + DOWN * 0.03, color=GOLD, width=4)
        feedback = CubicBezier(
            RIGHT * 3.95 + DOWN * 1.25,
            RIGHT * 2.9 + DOWN * 3.18,
            LEFT * 2.9 + DOWN * 3.18,
            LEFT * 4.05 + DOWN * 1.42,
        )
        feedback.set_stroke(RED, width=4.0)
        feedback_glow = feedback.copy().set_stroke(RED, width=15, opacity=0.16)

        axes.set_opacity(0.58)
        state_label_text = Text("runtime state\n+ constraints", color=CYAN, font_size=17, line_spacing=0.84).move_to(LEFT * 6.00 + UP * 2.72)
        state_label_text.set_fill(CYAN, opacity=1).set_stroke(width=0)
        state_label = VGroup(BackgroundRectangle(state_label_text, color=BG, fill_opacity=0.88, buff=0.08), state_label_text).set_z_index(9)
        exec_label = Text("executable\nbehavior", color=GOLD, font_size=16, line_spacing=0.84).move_to(RIGHT * 2.35 + UP * 1.98)
        # Push telemetry label well clear of the "monitors" gate label below
        # the feedback curve — Gemini flagged the original placement as having
        # "monitors" colliding with the glowing red feedback line.
        telemetry_label = Text("feedback telemetry", color="#FF6FA0", font_size=18).set_fill("#FF6FA0", opacity=1).set_stroke(width=0).move_to(DOWN * 3.65 + RIGHT * 2.85)
        for label in [state_label, exec_label, telemetry_label]:
            self.add_fixed_orientation_mobjects(label)

        gate_specs = [
            ("tests", LEFT * 2.40 + DOWN * 2.0, CYAN),
            ("monitors", DOWN * 2.42, GREEN),
            ("proofs", RIGHT * 2.40 + DOWN * 2.0, GOLD),
        ]
        gates = VGroup()
        gate_labels = VGroup()
        for label, pos, color in gate_specs:
            gate = Rectangle(width=0.46, height=0.72, color=color, stroke_width=2.2)
            gate.set_fill(BG, opacity=0.82).move_to(pos)
            gate_glow = gate.copy().set_stroke(color, width=10, opacity=0.12)
            gate_text = Text(label, color=color, font_size=18).move_to(pos + DOWN * 0.76)
            gate_text.set_fill(color, opacity=1)
            gate_text.set_stroke(width=0)
            gates.add(VGroup(gate_glow, gate))
            gate_labels.add(gate_text)
            self.add_fixed_orientation_mobjects(gate_text)

        self.play(Create(axes), FadeIn(state_cloud), FadeIn(state_label), run_time=1.6)
        self.play(FadeIn(transform_glow), FadeIn(transform_core), FadeIn(transform_ring), FadeIn(core_label), Create(arrow1), run_time=1.2)
        self.play(Create(arrow2), FadeIn(hardware), FadeIn(memory_grid), FadeIn(hw_label), FadeIn(exec_label), run_time=1.4)
        self.play(Create(VGroup(feedback_glow, feedback)), FadeIn(gates), FadeIn(gate_labels), FadeIn(telemetry_label), run_time=1.5)

        pulse = VGroup(transform_glow.copy(), transform_ring.copy()).set_opacity(0.35)
        self.play(pulse.animate.scale(1.22).set_opacity(0.05), run_time=1.1)
        self.remove(pulse)
        feedback_packet = Dot(feedback.get_start(), radius=0.07, color=RED)
        feedback_packet_glow = Dot(feedback.get_start(), radius=0.22, color=RED).set_opacity(0.20)
        packet = VGroup(feedback_packet_glow, feedback_packet)
        self.add(packet)
        self.play(MoveAlongPath(packet, feedback), run_time=2.2, rate_func=linear)
        self.play(
            LaggedStart(*[cell.animate.set_fill(BLUE, opacity=0.18).set_stroke(BLUE, opacity=0.65) for cell in memory_grid[::3]], lag_ratio=0.04),
            run_time=1.0,
        )
        self.move_camera(phi=50 * DEGREES, theta=-48 * DEGREES, zoom=0.82, frame_center=LEFT * 0.10 + DOWN * 0.20, run_time=3.0)
        self.play(Rotate(transform_ring, angle=TAU, axis=UP, about_point=transform_core.get_center()), run_time=3.0, rate_func=linear)
        self.move_camera(phi=56 * DEGREES, theta=-66 * DEGREES, zoom=0.74, frame_center=ORIGIN, run_time=2.4)

        # Fade the static telemetry label + gate labels for the walk so the
        # narration cards have a clear slot at the bottom (user flagged the
        # caption overlap throughout this scene).
        self.play(
            # Keep tests/monitors/proofs visible (user flagged them as too
            # dark to read). Only the static telemetry caption needs to clear
            # to make room for the narration walk.
            telemetry_label.animate.set_opacity(0.0),
            run_time=0.5,
        )
        # Narration walk through the self-inhabiting compute argument. Cards
        # are fixed in frame so they read flat regardless of 3D rotation.
        walk_pos = DOWN * 3.30
        narration_beats = [
            ("runtime state · constraints · feedback", CYAN),
            ("intent → executable behavior", GOLD),
            ("hardware runs it · system measures what happened", GREEN),
            ("measurement feeds the next transform", RED),
            ("software becomes part of the machine's feedback loop", VIOLET),
            ("the computer starts to inhabit its own execution", WHITE),
            ("safety boundary can no longer be a human reading every line", "#FF7FA8"),
            ("external validators · constrained sandboxes · proofs · monitors", GREEN),
            ("source code as audit surface, not the only bridge", GOLD),
        ]
        for caption, color in narration_beats:
            card = self.glow_text(caption, color, 20).move_to(walk_pos)
            self.add_fixed_in_frame_mobjects(card)
            self.play(FadeIn(card, shift=UP * 0.10), run_time=0.6)
            self.wait(4.0)
            self.play(FadeOut(card), run_time=0.4)
            self.clear_fixed(card)

        # Send another feedback pulse through the loop and ring-pulse the
        # transform core a few times, so the tail isn't dead time.
        for _ in range(3):
            packet_b = Dot(feedback.get_start(), radius=0.08, color=RED)
            packet_b_glow = Dot(feedback.get_start(), radius=0.22, color=RED).set_opacity(0.20)
            pkt = VGroup(packet_b_glow, packet_b)
            self.add(pkt)
            self.play(MoveAlongPath(pkt, feedback), run_time=2.2, rate_func=linear)
            ring_ghost = transform_ring.copy().set_opacity(0.4)
            self.add(ring_ghost)
            self.play(ring_ghost.animate.scale(1.4).set_opacity(0.0), run_time=1.0)
            self.remove(ring_ghost, pkt)

        self.remaining_wait()


class S12OuterExperimentLoop(Storyboard2DScene):
    target_seconds = 48

    def construct(self):
        title = self.glow_text("the outward loop", WHITE, 31).to_edge(UP).shift(DOWN * 0.1)
        title_shield = BackgroundRectangle(title, color=BG, fill_opacity=0.96, buff=0.10)
        title_shield.set_z_index(20)
        title.set_z_index(21)
        self.play(FadeIn(title_shield), FadeIn(title), run_time=0.8)

        # Use a regular pentagon (not the squashed ellipse Gemini flagged).
        # Center the loop near origin with vertices on a circle of radius 2.6.
        _pent_r = 2.60
        _pent_cx, _pent_cy = 0.0, -0.20
        positions = {
            "hypothesis":  np.array([_pent_cx + _pent_r * math.cos(math.radians( 90)),
                                     _pent_cy + _pent_r * math.sin(math.radians( 90)), 0]),
            "procedure":   np.array([_pent_cx + _pent_r * math.cos(math.radians( 18)),
                                     _pent_cy + _pent_r * math.sin(math.radians( 18)), 0]),
            "measurement": np.array([_pent_cx + _pent_r * math.cos(math.radians(-54)),
                                     _pent_cy + _pent_r * math.sin(math.radians(-54)), 0]),
            "evidence":    np.array([_pent_cx + _pent_r * math.cos(math.radians(234)),
                                     _pent_cy + _pent_r * math.sin(math.radians(234)), 0]),
            "update":      np.array([_pent_cx + _pent_r * math.cos(math.radians(162)),
                                     _pent_cy + _pent_r * math.sin(math.radians(162)), 0]),
        }
        labels = {
            "hypothesis": ("hypothesis", CYAN),
            "procedure": ("procedure", GOLD),
            "measurement": ("measurement", GREEN),
            "evidence": ("evidence", VIOLET),
            "update": ("update", RED),
        }
        node_groups = {}
        for key, pos in positions.items():
            label, color = labels[key]
            ring = Circle(radius=0.34, color=color, stroke_width=3).move_to(pos)
            ring.set_fill(color, opacity=0.06)
            glow = ring.copy().set_stroke(color, width=12, opacity=0.14)
            # Hypothesis top, far-side outward, bottom OUTWARD-DOWN so the
            # labels never compete with the narration captions at y=-3.65.
            label_dir = UP if key == "hypothesis" else (RIGHT if pos[0] > 3.5 else LEFT if pos[0] < -3.5 else DOWN)
            text = Text(label, color=WHITE, font_size=18, line_spacing=0.82).next_to(ring, label_dir, buff=0.18)
            text.set_fill(WHITE, opacity=1)
            text.set_stroke(width=0)
            node_groups[key] = VGroup(glow, ring, text)

        order = ["hypothesis", "procedure", "measurement", "evidence", "update", "hypothesis"]
        loop_path = VMobject()
        loop_path.set_points_smoothly([positions[key] for key in order])
        loop_path.set_stroke(WHITE, width=2.0, opacity=0.24)
        loop_glow = loop_path.copy().set_stroke(CYAN, width=13, opacity=0.10)
        arrows = VGroup()
        for a, b in zip(order, order[1:]):
            start = positions[a]
            end = positions[b]
            color = labels[b][1]
            # Larger buff so arrowheads land on the ring border, not on the
            # label text inside / next to the target node (Gemini flagged this).
            arrows.add(neon_arrow(start, end, color=color, width=3.0, buff=0.78))

        self.play(LaggedStart(*[FadeIn(node_groups[k]) for k in positions], lag_ratio=0.12), run_time=1.8)
        self.play(Create(loop_glow), Create(loop_path), LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.18), run_time=2.2)

        orbit = Circle(radius=1.1, color=WHITE, stroke_width=1.4)
        orbit.set_fill(BG, opacity=0.0)
        orbit.set_stroke(WHITE, opacity=0.25)
        orbit_glow = orbit.copy().set_stroke(CYAN, width=8, opacity=0.08)
        inner_core = VGroup(
            Dot(ORIGIN, radius=0.10, color=WHITE),
            Text("model", color=WHITE, font_size=22).set_fill(WHITE, opacity=1).set_stroke(width=0).next_to(ORIGIN, DOWN, buff=0.22),
        )
        particles = VGroup()
        for i, color in enumerate([CYAN, GOLD, GREEN, VIOLET, RED]):
            dot = glow_dot(np.array([math.cos(i * TAU / 5), math.sin(i * TAU / 5), 0]) * 1.1, color, radius=0.045)
            particles.add(dot)
        loop_pulse = glow_dot(positions["hypothesis"], CYAN, radius=0.055)
        self.play(FadeIn(orbit_glow), Create(orbit), FadeIn(inner_core), FadeIn(particles), FadeIn(loop_pulse), run_time=1.2)

        action_targets = [
            ("simulation", np.array([5.15, 0.95, 0]), CYAN),
            ("robot", np.array([5.42, -0.78, 0]), GOLD),
            ("lab", np.array([-5.35, -0.82, 0]), GREEN),
            ("notebook", np.array([-5.0, 0.92, 0]), VIOLET),
        ]
        action_sources = [
            positions["procedure"] + RIGHT * 0.45 + UP * 0.18,
            positions["measurement"] + RIGHT * 0.42,
            positions["evidence"] + LEFT * 0.42,
            positions["update"] + LEFT * 0.45 + UP * 0.18,
        ]
        branches = VGroup()
        action_nodes = VGroup()
        for (label, target, color), start in zip(action_targets, action_sources):
            outward = RIGHT if target[0] > 0 else LEFT
            ctrl1 = start + outward * 0.85 + UP * 0.38
            ctrl2 = target - outward * 0.85 + UP * 0.12
            branches.add(CubicBezier(start, ctrl1, ctrl2, target).set_stroke(color, width=2.5, opacity=0.72))
            # Replace line-art clip-art icons with simple glowing nodes — keeps
            # the visual language consistent with the rest of the video.
            icon = Dot(target, radius=0.13, color=color).set_z_index(6)
            icon_glow = Dot(target, radius=0.36, color=color).set_opacity(0.30).set_z_index(5)
            txt = Text(label, color=color, font_size=18).next_to(icon, DOWN, buff=0.16)
            txt.set_fill(color, opacity=1)
            txt.set_stroke(width=0)
            action_nodes.add(VGroup(icon_glow, icon, txt))
        self.play(LaggedStart(*[Create(b) for b in branches], lag_ratio=0.12), LaggedStart(*[FadeIn(n) for n in action_nodes], lag_ratio=0.10), run_time=1.7)
        full_loop = VGroup(*node_groups.values(), loop_glow, loop_path, arrows, orbit, orbit_glow, inner_core, particles, branches, action_nodes, loop_pulse)
        self.play(full_loop.animate.scale(1.08), run_time=1.4)
        self.play(
            Rotate(particles, angle=TAU, about_point=ORIGIN),
            MoveAlongPath(loop_pulse, loop_path),
            run_time=4.0,
            rate_func=linear,
        )
        self.play(full_loop.animate.scale(0.94).shift(DOWN * 0.06), run_time=1.4)

        # Narration walk: the outward (experiment) loop parallels the inward
        # (self-inhabiting compute) loop. Walk the viewer through it while
        # cycling the loop pulse for visible motion. Walk_pos pushed to the
        # very bottom edge so it doesn't crowd the evidence/measurement
        # labels which hang DOWN from the bottom ring nodes.
        walk_pos = DOWN * 3.65
        narration_beats = [
            ("hypothesis → procedure → measurement → evidence", CYAN),
            ("autonomous labs already point this direction", GOLD),
            ("but it's not just AI does science", VIOLET),
            ("transforms compress question → action → evidence → next", GREEN),
            ("simulation · robot · lab · notebook all become reachable", WHITE),
            ("a cheap accurate-enough loop outpaces manual translation", "#FF7FA8"),
            ("representation · action · measurement · updated representation", WHITE),
        ]
        for caption, color in narration_beats:
            card = self.glow_text(caption, color, 21).move_to(walk_pos)
            self.play(FadeIn(card, shift=UP * 0.10), run_time=0.6)
            # While the card is up, run a loop_pulse cycle so the pentagon
            # visibly rotates instead of holding static.
            self.play(MoveAlongPath(loop_pulse, loop_path), run_time=3.6, rate_func=linear)
            self.play(FadeOut(card), run_time=0.4)

        # Final acceleration: spin the particles faster
        self.play(Rotate(particles, angle=TAU, about_point=ORIGIN), run_time=3.0, rate_func=linear)
        self.remaining_wait()


class S13BusinessPipelines(Storyboard2DScene):
    target_seconds = 42

    def construct(self):
        title = self.glow_text("businesses are transform pipelines", WHITE, 30).to_edge(UP).shift(DOWN * 0.12)
        self.play(FadeIn(title), run_time=0.8)

        stages = [
            ("intent", CYAN),
            ("strategy\ndeck", VIOLET),
            ("product\nbrief", GOLD),
            ("design", GREEN),
            ("tickets", CYAN),
            ("code", GOLD),
            ("product", WHITE),
        ]
        xs = np.linspace(-5.5, 5.5, len(stages))
        groups = VGroup()
        arrows = VGroup()
        for i, ((label, color), x) in enumerate(zip(stages, xs)):
            box = self.neon_box(label, color, width=1.35, height=0.78, font_size=17)
            box[-1].set_color(WHITE)
            box.move_to(np.array([x, 0.7 if i % 2 == 0 else -0.05, 0]))
            # Each stage gets a tiny artifact glyph so the pipeline feels like
            # real work products being translated, not generic rectangles.
            glyph = VGroup()
            if "deck" in label or "brief" in label:
                glyph.add(Rectangle(width=0.26, height=0.34, color=color, stroke_width=1.0))
                glyph.add(Line(LEFT * 0.08 + UP * 0.06, RIGHT * 0.08 + UP * 0.06, color=color, stroke_width=0.8))
                glyph.add(Line(LEFT * 0.08 + DOWN * 0.04, RIGHT * 0.08 + DOWN * 0.04, color=color, stroke_width=0.8))
            elif label == "code":
                glyph.add(Text("{ }", color=color, font_size=12))
            elif label == "product":
                glyph.add(RoundedRectangle(width=0.30, height=0.22, corner_radius=0.04, color=color, stroke_width=1.0))
                glyph.add(Line(LEFT * 0.08, RIGHT * 0.08, color=color, stroke_width=0.8))
            else:
                glyph.add(Dot(radius=0.08, color=color))
            # The tiny glyphs repeatedly read as symbols behind/over text in
            # 480p review frames. Keep the stage boxes text-only here; the
            # moving handoff packets carry the work-product motion cue.
            groups.add(box)
            if i > 0:
                arrows.add(neon_arrow(groups[i - 1].get_right() + RIGHT * 0.05, box.get_left() + LEFT * 0.05, color=color, width=2.8))

        self.play(LaggedStart(*[FadeIn(g) for g in groups], lag_ratio=0.12), run_time=1.8)
        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.12), run_time=1.6)
        handoff_packets = VGroup()
        for i, arrow in enumerate(arrows):
            packet = Dot(arrow[1].get_start(), radius=0.045, color=stages[i + 1][1]).set_opacity(0.0)
            handoff_packets.add(packet)
        self.add(handoff_packets)
        for packet in handoff_packets:
            packet.set_opacity(0.9)
        self.play(
            LaggedStart(*[MoveAlongPath(packet, arrow[1]) for packet, arrow in zip(handoff_packets, arrows)], lag_ratio=0.12),
            run_time=1.7,
            rate_func=linear,
        )
        for packet in handoff_packets:
            packet.set_opacity(0.0)

        audience = VGroup(
            Text("each representation is shaped for its next audience", color=WHITE, font_size=22).set_fill(WHITE, opacity=0.86).set_stroke(width=0),
            Text("customer ≠ code     executive ≠ every ticket     compiler ≠ strategy deck", color=WHITE, font_size=18),
        ).arrange(DOWN, buff=0.22).move_to(DOWN * 1.55)
        self.play(FadeIn(audience), run_time=1.1)

        compressed = self.glow_text("automation compresses some handoffs", GREEN, 25).move_to(DOWN * 2.65)
        compressed_xs = np.linspace(-4.55, 4.55, len(groups))
        compressed_targets = [
            np.array([x, 0.18 + 0.12 * math.sin(i * 0.9), 0])
            for i, x in enumerate(compressed_xs)
        ]
        # The "product" box (rightmost in the compressed pipeline) sits at
        # x=4.55 with width ~1.4, so its right edge is at x=5.25. A circle
        # at x=5.45 r=0.44 overlapped from 5.01 to 5.25 — the recurring
        # bug the user flagged 3 times. Move circle to x=6.30 (left edge
        # 5.86, clear of product at 5.25 by 0.61 units). Also shrink so
        # it fits inside the frame edge at x=7.11.
        # The circle was radius 0.38 — too small for the word "transform", which
        # overflowed both sides of the bubble (user: "AI transform bubble text
        # overlaps with the edges"). Enlarge to 0.64 so the two-line label sits
        # fully inside the circle. At x=6.20 the right edge is 6.84 (clear of the
        # x=7.11 frame edge) and the left edge 5.56 stays clear of the product box.
        compression_core = VGroup(
            Circle(radius=0.64, color=GREEN, stroke_width=3).set_fill(GREEN, opacity=0.07),
            Text("AI\ntransform", color=GREEN, font_size=13, line_spacing=0.78).set_fill(GREEN, opacity=1).set_stroke(width=0),
        ).move_to(RIGHT * 6.20 + UP * 1.55)
        compression_glow = compression_core[0].copy().set_stroke(GREEN, width=13, opacity=0.14)
        compressed_spine = neon_line(LEFT * 5.10 + DOWN * 0.42, RIGHT * 5.10 + DOWN * 0.42, color=GREEN, width=3.2)
        compressed_spine.set_z_index(-2)
        # Fade the original handoff arrows COMPLETELY when compression starts —
        # they pointed at the old box positions and look broken once the boxes
        # have moved (user feedback at 19:49 "arrows overlapping weird").
        self.play(FadeOut(audience), FadeOut(arrows), FadeIn(compressed), FadeIn(compression_glow), FadeIn(compression_core), run_time=1.0)
        self.play(
            *[group.animate.move_to(target).scale(0.82) for group, target in zip(groups, compressed_targets)],
            Create(compressed_spine),
            run_time=1.8,
        )
        parallel = VGroup()
        for row in range(3):
            y = -1.82 - row * 0.34
            line = Line(LEFT * 4.7 + UP * y, RIGHT * 4.7 + UP * y, color=[CYAN, GOLD, VIOLET][row], stroke_width=1.6)
            dots = VGroup(*[Dot(np.array([x, y, 0]), radius=0.025, color=[CYAN, GOLD, VIOLET][row]) for x in np.linspace(-4.7, 4.7, 8)])
            parallel.add(VGroup(line, dots).set_opacity(0.32))
        many = Text("one pipeline becomes a pattern across the company", color=WHITE, font_size=20)
        many.set_fill(WHITE, opacity=0.92).set_stroke(width=0).move_to(DOWN * 2.75)
        # Fade `compressed` as `many` appears — both sit at the bottom
        # (DOWN*2.65 / DOWN*2.75) and otherwise overlap (user flagged at 17:51).
        self.play(FadeOut(compressed), FadeIn(parallel), FadeIn(many), run_time=1.2)
        self.play(parallel.animate.set_opacity(0.62).shift(UP * 0.06), run_time=1.1)

        # Fade `many` before the walk starts so the walk has a clean bottom slot.
        # (`compressed` was already faded out when `many` appeared.)
        self.play(FadeOut(many), run_time=0.4)
        # Narration walk through "every handoff transforms the thing"
        walk_pos = DOWN * 3.30
        narration_beats = [
            ("intent → strategy → brief → design → tickets → code → product", WHITE),
            ("every handoff is an intermediate representation", CYAN),
            ("each representation is shaped for its next audience", GOLD),
            ("the customer shouldn't read code", VIOLET),
            ("the compiler shouldn't read a strategy deck", GREEN),
            ("automated transforms compress some handoffs", "#FF7FA8"),
            ("humans stay where context, judgment, and constraints carry", WHITE),
            ("valuable work moves toward choosing the right intent", CYAN),
        ]
        # Hold each caption longer so they don't visually stack with the
        # next one (user feedback: walks were too close together). Each card
        # is fully OUT before the next fades in.
        for caption, color in narration_beats:
            card = self.glow_text(caption, color, 20).move_to(walk_pos)
            self.play(FadeIn(card, shift=UP * 0.10), run_time=0.6)
            self.wait(4.4)
            # Pulse the compression core during each card so the diagram stays alive
            ghost = compression_glow.copy()
            self.add(ghost)
            self.play(ghost.animate.scale(1.18).set_opacity(0.0), run_time=1.4, rate_func=rate_functions.ease_out_sine)
            self.remove(ghost)
            self.play(FadeOut(card), run_time=0.5)

        # ---- NEW BEAT: clear screen + show pipeline as transform boundaries ---
        # User feedback: arrows from the old flowchart still bled into the new
        # boundary beat. Fade EVERYTHING to zero so the boundary metaphor has
        # a clean slate. (Was previously left at 0.10 opacity — still visible.)
        # Only fade what is actually still on screen. `arrows`, `compressed` and
        # `many` were already faded out earlier, and FadeOut-ing a removed mobject
        # re-adds it at full opacity for the fade — which flashed the old
        # flowchart arrows back in right before this transition (user: "pops in a
        # bunch of arrows and junk right before fading out").
        self.play(
            FadeOut(groups),
            FadeOut(parallel),
            FadeOut(compression_core),
            FadeOut(compression_glow),
            FadeOut(compressed_spine),
            run_time=1.0,
        )

        boundary_title = self.glow_text("each handoff is a transform boundary", WHITE, 22)
        boundary_title.to_edge(UP).shift(DOWN * 0.78)
        self.play(FadeIn(boundary_title), run_time=0.6)

        # Build five vertical aperture lines, color-keyed by the boundary they
        # represent. The colors here MUST match the order the idea-dot's
        # `morph_path` reads them — user flagged that after the dot crossed
        # boundary 1 it was the wrong color in the previous build.
        boundary_xs = np.linspace(-3.2, 3.2, 5)
        boundary_colors = [CYAN, VIOLET, GOLD, GREEN, "#FF8FB0"]
        boundary_set = VGroup()
        for x, color in zip(boundary_xs, boundary_colors):
            line = Line(UP * 1.4, DOWN * 1.4, color=color, stroke_width=6)
            line.move_to(np.array([x, 0.0, 0]))
            glow = line.copy().set_stroke(color, width=18, opacity=0.20)
            boundary_set.add(VGroup(glow, line))

        self.play(LaggedStart(*[Create(b) for b in boundary_set], lag_ratio=0.18), run_time=1.4)

        zone_labels = VGroup()
        zone_label_specs = [
            ("intent",       CYAN,   -4.30),
            ("strategy",     VIOLET, -2.40),
            ("brief",        GOLD,   -1.20),
            ("design",       GREEN,   0.00),
            ("tickets",      CYAN,    1.20),
            ("code",         GOLD,    2.40),
            ("product",      WHITE,   4.30),
        ]
        for label, color, x in zone_label_specs:
            t = Text(label, color=color, font_size=18).set_fill(color, opacity=1).set_stroke(width=0)
            t.move_to(np.array([x, -2.30, 0]))
            zone_labels.add(t)
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in zone_labels], lag_ratio=0.10), run_time=1.4)

        # Glowing idea-object passes through every boundary, morphing color.
        idea = Dot(np.array([-4.50, 0.0, 0]), radius=0.18, color=CYAN).set_z_index(8)
        idea_glow = Dot(np.array([-4.50, 0.0, 0]), radius=0.46, color=CYAN).set_opacity(0.32).set_z_index(7)
        idea_group = VGroup(idea_glow, idea)
        self.add(idea_group)
        self.play(FadeIn(idea_group), run_time=0.4)

        # Each waypoint sits JUST PAST one boundary, with the color of THAT
        # boundary — so the idea-dot takes on the color of the boundary it
        # just crossed (the visual "shaped for the next audience" beat).
        # Boundaries at x = -3.2, -1.6, 0.0, 1.6, 3.2 (colors CYAN, VIOLET,
        # GOLD, GREEN, pink).
        morph_path = [
            (-2.40, CYAN),       # past boundary 1 (CYAN)
            (-0.80, VIOLET),     # past boundary 2 (VIOLET)
            ( 0.80, GOLD),       # past boundary 3 (GOLD)
            ( 2.40, GREEN),      # past boundary 4 (GREEN)
            ( 4.50, "#FF8FB0"),  # past boundary 5 (pink) — final product
        ]
        for x, color in morph_path:
            self.play(
                idea_group.animate.move_to(np.array([x, 0.0, 0])).set_color(color),
                run_time=0.6,
            )
            # Tiny pulse on the just-crossed boundary
            self.wait(0.10)

        compression_note = self.glow_text("AI compresses some boundaries — the rest stay human", CYAN, 22)
        compression_note.to_edge(DOWN).shift(UP * 0.30)
        self.play(FadeIn(compression_note), run_time=0.6)
        # Collapse the middle three boundaries to show compression
        self.play(
            boundary_set[1].animate.shift(RIGHT * 0.8).set_opacity(0.35),
            boundary_set[2].animate.shift(RIGHT * 0.4).set_opacity(0.35),
            run_time=1.4,
        )
        self.play(idea_group.animate.move_to(np.array([4.50, 0.0, 0])).set_color(GREEN), run_time=0.8)

        self.remaining_wait()


class S14EndingTechTreeZoomOut(S06cGameTechTree3D):
    target_seconds = 34

    def construct(self):
        # Differentiated ending: reuse the same tree layout but show it as an
        # *already-grown* whole and walk through it row-by-row, then pull back.
        # No row-stagger reveals, no per-edge unlocks — this is a "look at the
        # forest you just grew" beat, not the same growth animation as S08.
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=0.66, focal_distance=9)

        title = self.glow_text("language is a computable material", WHITE, 28).to_edge(UP).shift(DOWN * 0.10)
        subtitle = self.glow_text("when civilization gets a new transform, the tree changes", WHITE, 18).next_to(title, DOWN, buff=0.16)
        self.add_fixed_in_frame_mobjects(title, subtitle)
        self.play(FadeIn(title), FadeIn(subtitle), run_time=0.9)

        # Build the column bands + row markers exactly as in the main tree.
        columns = [
            ("Classical",            -5.1, "#1E3A5F", CYAN),
            ("Computable\nMeaning",  -2.1, "#303069", VIOLET),
            ("AI Workflows",          1.1, "#2D4A31", GREEN),
            ("Civilization\nScale",   4.4, "#55324E", "#FF8FB0"),
        ]
        rows = [("Signals", 2.0), ("Control", 0.95), ("Media", -0.1), ("Software", -1.15), ("Science", -2.2)]

        lanes = VGroup()
        for heading, x, color, accent in columns:
            band = Rectangle(width=2.65, height=5.75, color=color, stroke_width=1.6)
            band.set_fill(color, opacity=0.22)
            band.move_to(np.array([x, -0.25, -0.08]))
            label_core = Text(heading, color=accent, font_size=22, line_spacing=0.65).set_fill(accent, opacity=1).set_stroke(width=0)
            label_core.move_to(np.array([x, 3.10, 0]))
            lanes.add(VGroup(band, label_core))

        row_labels = VGroup()
        row_lines = VGroup()
        for label, y in rows:
            line = Line(np.array([-6.55, y - 0.48, -0.12]), np.array([5.85, y - 0.48, -0.12]), color=GRID, stroke_width=1.4)
            text = Text(label, color=WHITE, font_size=18).move_to(np.array([-6.9, y, 0]))
            text.set_fill(WHITE, opacity=0.86)
            row_labels.add(text)
            row_lines.add(line)

        hot_red = "#ff4f8b"
        # Same node dict as S06cGameTechTree3D — kept in sync manually so a
        # change here forces a re-render of both. (If you change one, change both.)
        nodes = {
            "fourier":     (-5.1,  2.0,   "Fourier",                    CYAN,   1.0),
            "laplace":     (-5.1,  0.95,  "Laplace",                    GOLD,   1.0),
            "dct":         (-5.1, -0.1,   "DCT",                        VIOLET, 1.0),
            "lambda":      (-5.1, -1.15,  "Lambda\ncalculus",           BLUE,   1.0),
            "doe":         (-5.1, -2.20,  "Statistics\n+ DOE",          GOLD,   1.0),
            "frequency":   (-2.1,  2.0,   "frequency\nspace",           CYAN,   1.0),
            "stability":   (-2.1,  0.95,  "stability\nalgebra",         GOLD,   1.0),
            "compression": (-2.1, -0.1,   "perceptual\ncompression",    VIOLET, 1.0),
            "embeddings":  (-2.1, -1.15,  "embedding\nspace",           GREEN,  0.94),
            "sciml":       (-2.1, -2.20,  "neural ODEs\n· PINNs",       CYAN,   0.94),
            "audio":       ( 1.1,  2.0,   "speech &\naudio agents",     CYAN,   0.92),
            "vv":          ( 1.1,  0.95,  "V&V\nsystems",               GREEN,  0.74),
            "multimodal":  ( 1.1, -0.1,   "multimodal\nmodels",         VIOLET, 0.82),
            "code":        ( 1.1, -1.15,  "code\nagents",               CYAN,   0.86),
            "research":    ( 1.1, -2.20,  "research\nassistants",       GOLD,   0.88),
            "monitoring":  ( 4.4,  2.0,   "ambient\ninfrastructure",    CYAN,   0.55),
            "orgs":        ( 4.4,  0.95,  "transform-native\norganizations", GREEN, 0.55),
            "media":       ( 4.4, -0.1,   "synthetic\nmedia stacks",    VIOLET, 0.50),
            "self":        ( 4.4, -1.15,  "self-inhabiting\ncompute",   hot_red, 0.48),
            "labs":        ( 4.4, -2.2,   "autonomous\nexperiment loops", GOLD, 0.45),
        }
        edges = [
            ("fourier", "frequency"), ("laplace", "stability"), ("dct", "compression"),
            ("lambda", "embeddings"), ("doe", "sciml"),
            ("frequency", "embeddings"), ("stability", "embeddings"), ("compression", "multimodal"),
            ("frequency", "audio"), ("embeddings", "audio"), ("embeddings", "code"),
            ("embeddings", "multimodal"), ("embeddings", "research"), ("sciml", "research"),
            ("stability", "vv"), ("code", "vv"),
            ("audio", "monitoring"), ("vv", "orgs"), ("vv", "self"), ("code", "self"),
            ("multimodal", "media"), ("multimodal", "labs"), ("vv", "labs"), ("research", "labs"),
        ]

        def p(key):
            x, y, _, _, _ = nodes[key]
            return np.array([x, y, 0])

        def tech_card(key):
            x, y, label, color, opacity = nodes[key]
            pos = np.array([x, y, 0])
            max_line = max(len(part) for part in label.split("\n"))
            w = min(2.55, max(1.65, 0.14 * max_line + 0.66))
            h = 0.66 if "\n" not in label else 0.84
            plate = RoundedRectangle(width=w, height=h, corner_radius=0.08, color=color, stroke_width=2.2)
            plate.set_fill(BG, opacity=0.95)
            plate.set_opacity(0.34 + opacity * 0.66)
            plate.set_z_index(1)
            icon = Dot(LEFT * (w / 2 - 0.22), radius=0.085, color=color).set_opacity(0.65 + 0.35 * opacity)
            icon.set_z_index(3)
            text_size = 15 if max_line > 13 else 17
            text = Text(label, color=WHITE, font_size=text_size, line_spacing=0.78).set_fill(WHITE, opacity=1).set_stroke(width=0)
            text.move_to(RIGHT * 0.16)
            text.set_z_index(4)
            card = VGroup(plate, icon, text).move_to(pos)
            if opacity < 0.92:
                plate.set_opacity(0.70)
                icon.set_opacity(0.72)
                text.set_opacity(0.82)
            return card

        node_cards = {k: tech_card(k) for k in nodes}
        edge_paths = VGroup()
        for a, b in edges:
            color = nodes[b][3]
            opacity = min(nodes[a][4], nodes[b][4])
            start = p(a) + RIGHT * 1.35
            end = p(b) + LEFT * 1.35
            mid1 = np.array([(start[0] + end[0]) / 2, start[1], 0])
            mid2 = np.array([(start[0] + end[0]) / 2, end[1], 0])
            path = CubicBezier(start, mid1, mid2, end)
            path.set_stroke(color, width=2.0, opacity=0.40 + 0.45 * opacity)
            edge_paths.add(path)

        # Speculative locked rim (horizontal band below Science row), same
        # layout as the main tech tree scene so the ending is consistent.
        rim_y = -3.40
        # Box width is 3.40 units. At font_size=19 each char is ~0.13 units,
        # so any label longer than ~26 chars overflows. The previous
        # "closed-loop civilization R&D" label at 27 chars literally could
        # not fit and was the recurring overflow the user flagged 3 times.
        # Shortened labels (each ≤21 chars) now fit cleanly in the 3.40 box.
        locked_specs = [
            (-3.6, rim_y, "native scientific loops",    CYAN),
            ( 0.6, rim_y, "model-designed interfaces", VIOLET),
            ( 4.6, rim_y, "closed-loop civ. R&D",      GOLD),
        ]
        rim_label = Text("speculative — not yet unlocked", color="#FF8FB0", font_size=18).set_fill("#FF8FB0", opacity=1).set_stroke(width=0)
        rim_label.move_to(np.array([-5.10, rim_y + 0.65, 0]))
        locked_nodes = VGroup(rim_label)
        locked_edges = VGroup()
        for x, y, label, color in locked_specs:
            pos = np.array([x, y, 0])
            # Use a DASHED outline as the "speculative" cue instead of the
            # internal diagonal hatch line (the hatch looked like a render
            # glitch through the box text per user feedback).
            outline = DashedVMobject(
                RoundedRectangle(width=3.80, height=0.72, corner_radius=0.10, color=color, stroke_width=2.6),
                num_dashes=42,
                dashed_ratio=0.55,
            )
            outline.set_stroke(color, opacity=0.94)
            bg = RoundedRectangle(width=3.80, height=0.72, corner_radius=0.10, color=color, stroke_width=0)
            bg.set_fill(BG, opacity=0.94)
            text = Text(label, color=color, font_size=19).move_to(ORIGIN)
            text.set_fill(color, opacity=1.0)
            text.set_stroke(width=0)
            fit_text_to_width(text, 3.80 - 0.18)
            text_shield = BackgroundRectangle(text, color=BG, fill_opacity=0.96, buff=0.04)
            outline.set_z_index(1)
            text_shield.set_z_index(2)
            text.set_z_index(3)
            self.validate_text_fits(text, bg, f"ending_locked_node:{label}")
            locked_nodes.add(VGroup(bg, outline, text_shield, text).move_to(pos))
            col4_x_for_y = {-3.6: -5.1, 0.6: 1.1, 4.6: 4.4}
            connector_start = np.array([col4_x_for_y[x], -2.62, 0])
            connector_end = pos + UP * 0.40
            locked_edges.add(DashedLine(connector_start, connector_end, color=color, dash_length=0.16, stroke_width=2.0).set_opacity(0.55))

        # Whole tree in at once, very quickly — this is a "complete the picture"
        # ending, not a reveal.
        all_nodes_group = VGroup(*node_cards.values())
        self.play(FadeIn(lanes), FadeIn(row_lines), FadeIn(row_labels), run_time=0.8)
        self.play(FadeIn(all_nodes_group, lag_ratio=0.02), Create(edge_paths, lag_ratio=0.02), run_time=2.0)
        self.wait(0.5)

        # Row-by-row spotlight: highlight one row at a time so the viewer can
        # read each band of nodes without scanning the whole grid at once.
        row_ys = [2.0, 0.95, -0.1, -1.15, -2.20]
        row_keys_by_y = {
            2.0:   ["fourier", "frequency", "audio", "monitoring"],
            0.95:  ["laplace", "stability", "vv", "orgs"],
            -0.1:  ["dct", "compression", "multimodal", "media"],
            -1.15: ["lambda", "embeddings", "code", "self"],
            -2.20: ["doe", "sciml", "research", "labs"],
        }
        for y in row_ys:
            keys = row_keys_by_y[y]
            highlight = VGroup(*[node_cards[k].copy() for k in keys])
            highlight.set_z_index(10)
            # Build a soft glow ring around each highlighted card
            rings = VGroup()
            for k in keys:
                ring = SurroundingRectangle(node_cards[k], color=WHITE, buff=0.10, stroke_width=3, corner_radius=0.10)
                ring.set_opacity(0.95)
                rings.add(ring)
            self.play(FadeIn(rings), run_time=0.4)
            self.wait(0.9)
            self.play(FadeOut(rings), run_time=0.4)

        # Reveal the locked speculative rim before the zoom-out. Fade the
        # column bands + row line markers so the rim text has clean black
        # space below the grid (Gemini flagged that grid + rim text were
        # competing for the same pixels in the final shot).
        self.play(
            Create(locked_edges, lag_ratio=0.18),
            lanes.animate.set_opacity(0.10),
            row_lines.animate.set_opacity(0.05),
            run_time=1.0,
        )
        self.play(FadeIn(locked_nodes, lag_ratio=0.18), run_time=1.2)

        # Small pull-back so the speculative rim is visible but text still reads.
        # 0.55 was too aggressive — locked-node labels became unreadable.
        self.move_camera(zoom=0.68, run_time=2.0)
        spec_keys = ["monitoring", "orgs", "media", "self", "labs"]
        spec_group = VGroup(*[node_cards[k] for k in spec_keys])
        for _ in range(2):
            self.play(
                spec_group.animate.scale(1.05),
                locked_nodes.animate.scale(1.05),
                run_time=0.7, rate_func=there_and_back,
            )

        self.remaining_wait()
