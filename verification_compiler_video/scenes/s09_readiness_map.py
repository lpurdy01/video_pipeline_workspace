"""
Section 09 — Verification Readiness Is A Map, Not Magic.

Two halves. First the readiness view: the graph becomes a heat map and the
metric decomposes into the things it is actually made of. Then the V&V
distinction from the 2026-08-23 commentary — the highest-value correction in
that recording, because without it the metric over-claims.
"""
from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from verification_compiler_video.pipeline import stage, style
from verification_compiler_video.pipeline.beats import Beat, BeatScene


class S09ReadinessMap(BeatScene):
    section_id = "09_readiness_map"
    title = "Readiness is visibility"
    timing_dir = Path(__file__).resolve().parents[1] / "out" / "timing"

    def storyboard(self) -> list[Beat]:
        return [
            Beat("Once the project is a graph and the reviews are structured", self.b00_zoom_out),
            Beat("You can ask:", self.b01_ask),
            Beat("how much of the graph has been reviewed", self.b02_reviewed),
            Beat("Which requirements have current evidence", self.b03_current),
            Beat("Which evidence is stale", self.b04_stale),
            Beat("Which parts are missing tests", self.b05_missing),
            Beat("Which model results are below the suitability threshold", self.b06_suitability),
            Beat("Which areas still need human attention", self.b07_attention),
            Beat("That gives you something like a Verification Readiness Metric", self.b08_metric),
            Beat("But this is important:", self.b09_but),
            Beat("it is not a magic safety score", self.b10_not_magic),
            Beat("It does not say the system is safe because the number is high",
                 self.b11_not_safe),
            Beat("It says the evidence surface is more or less complete", self.b12_decompose,
                 note="6s — the single number splits into what it is made of"),
            Beat("It makes the gaps visible", self.b13_gaps),
            Beat("That is what readiness means here", self.b14_means),
            Beat("Not certainty", self.b15_not_certainty),
            Beat("Visibility", self.b16_visibility),
            Beat("And one more distinction, because the two words get used", self.b17_two_words),
            Beat("Verification is checking that you built the thing you meant to build",
                 self.b18_verification),
            Beat("Validation is checking that the thing you built is the thing you should",
                 self.b19_validation),
            Beat("Those are two separate processes", self.b20_separate),
            Beat("The Verification Compiler is aimed squarely at the first one", self.b21_aimed),
            Beat("It will not tell you that you designed the right system", self.b22_not_right),
            Beat("It tells you whether you can show that you built the system you specified",
                 self.b23_close),
        ]

    # ------------------------------------------------------------- the map --
    def _cells(self):
        return self._owned["map"]

    def b00_zoom_out(self, ctx):
        grid = VGroup()
        for r in range(4):
            for c in range(9):
                cell = RoundedRectangle(corner_radius=0.05, width=0.72, height=0.52,
                                        color=style.GRID, stroke_width=1.5)
                cell.set_fill(style.PANEL, opacity=0.9)
                cell.move_to(np.array([-3.6 + c * 0.86, 1.35 - r * 0.66, 0.0]))
                grid.add(cell)
        grid.move_to(np.array([-1.4, 0.35, 0.0]))
        ctx.show(grid, tag="map", anim=lambda m: FadeIn(m, scale=0.94), run_time=0.9)

    def b01_ask(self, ctx):
        tag = style.label_text("what can you ask it?", color=style.MUTED, size="tiny")
        tag.next_to(self._cells(), UP, buff=0.25)
        ctx.show(tag, tag="ask", run_time=0.35)

    def _paint(self, ctx, idxs, colour, run_time=0.4):
        ctx.play(*[self._cells()[i].animate.set_stroke(colour, width=2.4)
                   .set_fill(colour, opacity=0.30) for i in idxs], run_time=run_time)

    def b02_reviewed(self, ctx):
        self._paint(ctx, range(0, 14), style.GREEN, 0.5)

    def b03_current(self, ctx):
        self._paint(ctx, range(14, 20), style.GREEN, 0.45)

    def b04_stale(self, ctx):
        self._paint(ctx, (20, 21, 22, 27), style.AMBER, 0.4)

    def b05_missing(self, ctx):
        self._paint(ctx, (23, 24, 30), style.RED, 0.4)

    def b06_suitability(self, ctx):
        self._paint(ctx, (25, 26, 31), style.VIOLET, 0.45)
        ctx.hold(0.5)
        ctx.play(*[self._cells()[i].animate.set_stroke(width=3.4) for i in (25, 26, 31)],
                 run_time=0.4)

    def b07_attention(self, ctx):
        self._paint(ctx, (28, 29, 32, 33, 34, 35), style.GOLD, 0.5)

    def b08_metric(self, ctx):
        ctx.retire("ask", run_time=0.25)
        num = style.title_text("0.62")
        num.move_to(np.array([4.8, 0.9, 0.0]))
        lab = style.label_text("VRM", color=style.GOLD, size="tiny")
        lab.next_to(num, DOWN, buff=0.2)
        ctx.show(num, lab, tag="vrm", anim=lambda m: FadeIn(m, scale=0.85), run_time=0.55)

    def b09_but(self, ctx):
        ctx.play(*style.highlight(self._owned["vrm"], style.GOLD), run_time=0.35)

    def b10_not_magic(self, ctx):
        warn = style.label_text("not a safety score", color=style.RED, size="tiny")
        warn.move_to(np.array([4.8, -0.35, 0.0]))
        ctx.show(warn, tag="warn", run_time=0.4)

    def b11_not_safe(self, ctx):
        cross = VGroup(
            Line(UL * 0.34, DR * 0.34, color=style.RED, stroke_width=5),
            Line(UR * 0.34, DL * 0.34, color=style.RED, stroke_width=5),
        ).move_to(self._owned["vrm"])
        ctx.show(cross, tag="cross", anim=lambda m: Create(m), run_time=0.45)
        ctx.hold(0.6)
        ctx.play(FadeOut(cross), run_time=0.35)
        self._owned.pop("cross", None)

    def b12_decompose(self, ctx):
        """Six seconds — the one number opens into what it is actually made of."""
        parts = [("complete", 0.72, style.GREEN), ("current", 0.54, style.CYAN),
                 ("reviewed", 0.61, style.VIOLET)]
        bars = VGroup()
        for i, (name, frac, colour) in enumerate(parts):
            base = RoundedRectangle(corner_radius=0.05, width=2.4, height=0.24,
                                    color=style.GRID, stroke_width=1.5)
            base.set_fill("#071021", opacity=1)
            fill = RoundedRectangle(corner_radius=0.05, width=2.4 * frac, height=0.24,
                                    color=colour, stroke_width=0)
            fill.set_fill(colour, opacity=0.85)
            base.move_to(np.array([5.0, -0.95 - i * 0.55, 0.0]))
            fill.align_to(base, LEFT).set_y(base.get_y())
            lab = style.label_text(name, color=colour, size="tiny").next_to(base, LEFT, buff=0.22)
            row = VGroup(base, fill, lab)
            bars.add(row)
            ctx.play(FadeIn(row, shift=LEFT * 0.12), run_time=0.35)
            ctx.hold(1.2)
        self._own("bars", bars)

    def b13_gaps(self, ctx):
        gaps = [23, 24, 30]
        ctx.play(*[self._cells()[i].animate.set_stroke(style.RED, width=4) for i in gaps],
                 run_time=0.45)

    def b14_means(self, ctx):
        ctx.play(*style.highlight(self._owned["vrm"], style.WHITE), run_time=0.4)

    def b15_not_certainty(self, ctx):
        ctx.retire("warn", run_time=0.25)
        tag = style.label_text("not certain", color=style.MUTED, size="tiny")
        tag.move_to(np.array([4.8, -0.35, 0.0]))
        ctx.show(tag, tag="notcert", run_time=0.35)

    def b16_visibility(self, ctx):
        # "Not certainty" goes when "visibility" arrives — they occupy the same
        # column, and keeping both pushed "visibility" into the score readout.
        # Two words at 1.7s is under the reading budget and stays on the list.
        ctx.retire("notcert", run_time=0.2)

        tag = style.label_text("visibility", color=style.GREEN)
        tag.move_to(np.array([4.8, -0.35, 0.0]))
        ctx.show(tag, tag="vis", anim=lambda m: FadeIn(m, scale=1.15), run_time=0.4)

    # --------------------------------------------------- verification vs validation --
    def b17_two_words(self, ctx):
        ctx.clear_stage(run_time=0.6)
        left, right = stage.columns(2, gap=0.8)
        self._cols = (left, right)
        divider = DashedLine(np.array([0.0, stage.STAGE.bottom + 0.2, 0.0]),
                             np.array([0.0, stage.STAGE.top - 0.2, 0.0]),
                             color=style.GRID, stroke_width=2.6, dash_length=0.16)
        ctx.show(divider, tag="divider", anim=lambda m: Create(m), run_time=0.6)
        # The line is long enough that the divider alone freezes the frame; let
        # the two words that are about to be distinguished arrive here.
        ctx.hold(0.5)
        pair = VGroup(style.label_text("verification", color=style.MUTED, size="node"),
                      style.label_text("validation", color=style.MUTED, size="node"))
        pair[0].move_to(np.array([self._cols[0].center[0], 0.0, 0.0]))
        pair[1].move_to(np.array([self._cols[1].center[0], 0.0, 0.0]))
        for word in pair:
            ctx.play(FadeIn(word, shift=UP * 0.14), run_time=0.4)
            ctx.hold(0.6)
        self._own("pair", pair)
        ctx.play(pair.animate.set_opacity(0), run_time=0.4)

    def b18_verification(self, ctx):
        left = self._cols[0]
        head = style.label_text("verification", color=style.CYAN)
        head.move_to(np.array([left.center[0], stage.STAGE.top - 0.55, 0.0]))
        body = style.label_text("built the thing\nyou meant to build",
                                color=style.WHITE, size="node")
        body.move_to(np.array([left.center[0], 0.7, 0.0]))
        ctx.show(head, tag="vhead", run_time=0.4)
        ctx.show(body, tag="vbody", anim=lambda m: FadeIn(m, shift=UP * 0.12), run_time=0.45)

    def b19_validation(self, ctx):
        right = self._cols[1]
        head = style.label_text("validation", color=style.AMBER)
        head.move_to(np.array([right.center[0], stage.STAGE.top - 0.55, 0.0]))
        body = style.label_text("built the thing\nyou should have built",
                                color=style.WHITE, size="node")
        body.move_to(np.array([right.center[0], 0.7, 0.0]))
        ctx.show(head, tag="vahead", run_time=0.4)
        ctx.show(body, tag="vabody", anim=lambda m: FadeIn(m, shift=UP * 0.12), run_time=0.45)
        ctx.hold(0.6)
        world = style.label_text("does it work in the world?", color=style.AMBER, size="tiny")
        world.move_to(np.array([right.center[0], -0.6, 0.0]))
        ctx.show(world, tag="world", run_time=0.4)

    def b20_separate(self, ctx):
        ctx.play(self._owned["divider"].animate.set_stroke(style.WHITE, width=3.4),
                 run_time=0.45)

    def b21_aimed(self, ctx):
        left = self._cols[0]
        box = RoundedRectangle(corner_radius=0.12, width=left.width - 0.5,
                               height=3.4, color=style.CYAN, stroke_width=3.4)
        box.move_to(np.array([left.center[0], 0.35, 0.0]))
        ctx.show(box, tag="aim", anim=lambda m: Create(m), run_time=0.6)
        ctx.play(VGroup(self._owned["vahead"], self._owned["vabody"],
                        self._owned["world"]).animate.set_opacity(0.3), run_time=0.4)

    def b22_not_right(self, ctx):
        tag = style.label_text("not: did you design the right system",
                               color=style.MUTED, size="tiny")
        # Into the reserved caption lane, which is the one strip of the frame
        # nothing else is allowed to occupy — and it stays rather than being
        # replaced, because thirty-six characters need four seconds and this
        # line is under three.
        stage.fit(tag, stage.CAPTION)
        ctx.show(tag, tag="notright", run_time=0.45)

    def b23_close(self, ctx):
        tag = style.label_text("can you show what you built?", color=style.CYAN)
        tag.move_to(np.array([0.0, stage.STAGE.bottom + 0.75, 0.0]))
        ctx.show(tag, tag="final", anim=lambda m: FadeIn(m, scale=0.94), run_time=0.5)
