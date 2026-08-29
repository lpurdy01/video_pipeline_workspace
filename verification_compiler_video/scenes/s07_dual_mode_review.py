"""
Section 07 — Same Package, Two Review Modes.

The reviewer slot holds still; only its occupant changes. That is the whole
argument, and it only lands if the package and the result schema visibly do not
move while the reviewer swaps.

Carries the 2026-08-24 note that the human gets the package rendered as something
readable rather than raw JSON.
"""
from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from verification_compiler_video.pipeline import stage, style
from verification_compiler_video.pipeline.beats import Beat, BeatScene


class S07DualModeReview(BeatScene):
    section_id = "07_dual_mode_review"
    title = "Same package. Different authority."
    timing_dir = Path(__file__).resolve().parents[1] / "out" / "timing"

    def storyboard(self) -> list[Beat]:
        return [
            Beat("This also gives us a cleaner way to talk about AI review", self.b00_open),
            Beat("The same package can go to a model", self.b01_to_model),
            Beat("The same package can go to a human", self.b02_to_human),
            Beat("The input structure is the same", self.b03_same_input),
            Beat("The output schema is the same", self.b04_same_output),
            Beat("But the authority is not the same", self.b05_authority),
            Beat("In development, a model can review packages quickly", self.b06_fast),
            Beat("It can flag missing evidence", self.b07_flag_missing),
            Beat("It can notice mismatches", self.b08_mismatch),
            Beat("It can say: this requirement looks only partially covered", self.b09_partial),
            Beat("That is valuable", self.b10_valuable),
            Beat("But it is developmental review", self.b11_developmental),
            Beat("For certification-facing decisions, a human reviewer", self.b12_human_swap,
                 note="11.8s — the swap, then the package rendered as a readable page"),
            Beat("If the model and the human disagree, the disagreement", self.b13_disagree),
            Beat("It becomes part of the evidence history", self.b14_history),
            Beat("It can update the model's suitability for that kind of task", self.b15_suitability),
            Beat("The system is not trying to pretend the model is a perfect certifier",
                 self.b16_not_pretend),
            Beat("It is trying to make model assistance fit inside a review structure",
                 self.b17_close),
        ]

    # ------------------------------------------------------------------ rig --
    def b00_open(self, ctx):
        pkg = style.node("vqp", "VQP", size=1.7)
        pkg.move_to(np.array([-5.0, 0.35, 0.0]))
        slot = RoundedRectangle(corner_radius=0.12, width=3.4, height=1.7,
                                color=style.GRID, stroke_width=2.6)
        slot.set_fill("#060B18", opacity=1).move_to(np.array([-0.6, 0.55, 0.0]))
        tag = style.label_text("reviewer", color=style.MUTED, size="tiny")
        # The occupant of this slot is a diamond, and a diamond's top vertex
        # reaches above the slot it sits in — 0.2 of clearance put the label
        # straight onto that vertex for most of the section.
        tag.next_to(slot, UP, buff=0.55)
        ctx.show(pkg, tag="pkg", anim=lambda m: FadeIn(m, shift=RIGHT * 0.2), run_time=0.5)
        ctx.show(slot, tag="slot", run_time=0.4)
        ctx.show(tag, tag="slottag", run_time=0.3)

    def b01_to_model(self, ctx):
        edge = style.connect(self._owned["pkg"], self._owned["slot"], style.GREEN)
        ctx.show(edge, tag="in", anim=lambda m: Create(m), run_time=0.4)
        m = style.node("review", "model", size=2.0).move_to(self._owned["slot"].get_center())
        ctx.show(m, tag="occupant", anim=lambda m: FadeIn(m, scale=0.85), run_time=0.45)

    def b02_to_human(self, ctx):
        ctx.play(*style.highlight(self._owned["occupant"], style.CYAN), run_time=0.4)

    def b03_same_input(self, ctx):
        ctx.play(*style.highlight(self._owned["pkg"], style.GREEN), run_time=0.4)

    def b04_same_output(self, ctx):
        card = self._schema_card()
        card.move_to(np.array([4.6, 0.35, 0.0]))
        edge = style.connect(self._owned["slot"], card, style.VIOLET)
        ctx.show(edge, tag="out", anim=lambda m: Create(m), run_time=0.35)
        ctx.show(card, tag="schema", anim=lambda m: FadeIn(m, shift=LEFT * 0.15), run_time=0.5)

    def _schema_card(self) -> VGroup:
        box = RoundedRectangle(corner_radius=0.1, width=3.9, height=2.5,
                               color=style.VIOLET, stroke_width=2.4)
        box.set_fill(style.PANEL, opacity=0.97)
        rows = style.text_rows(*[
            style.mono_text(f, color=style.WHITE, size="tiny")
            for f in ("verdict", "rationale", "citations", "reviewer", "authority")
        ])
        rows.move_to(box)
        return VGroup(box, rows)

    def b05_authority(self, ctx):
        stamp = style.label_text("developmental", color=style.CYAN, size="tiny")
        stamp.next_to(self._owned["schema"], UP, buff=0.22)
        ctx.show(stamp, tag="stamp", run_time=0.4)

    # -------------------------------------------------- what the model gives --
    def b06_fast(self, ctx):
        # Smaller and tucked into the bottom-left corner: the findings list grows
        # across this strip, and at the old size and position the rows were
        # written straight through the row of packages.
        ticks = VGroup(*[style.node("vqp", "", size=0.42) for _ in range(5)])
        ticks.arrange(RIGHT, buff=0.22)
        ticks.move_to(np.array([-4.9, stage.STAGE.bottom + 0.5, 0.0]))
        for tk in ticks:
            ctx.play(FadeIn(tk, scale=0.7), run_time=0.16)
        self._own("batch", ticks)

    def b07_flag_missing(self, ctx):
        self._finding(ctx, "missing evidence", style.RED, 0, "f1")

    def b08_mismatch(self, ctx):
        self._finding(ctx, "version mismatch", style.AMBER, 1, "f2")

    def b09_partial(self, ctx):
        self._finding(ctx, "REQ-17 partially covered", style.AMBER, 2, "f3")

    def _finding(self, ctx, text: str, colour: str, i: int, tag: str):
        row = style.mono_text(f"• {text}", color=colour, size="tiny")
        row.move_to(np.array([0.6, stage.STAGE.bottom + 1.65 - i * 0.5, 0.0]))
        row.align_to(np.array([-1.9, 0, 0]), LEFT)
        ctx.show(row, tag=tag, anim=lambda m: FadeIn(m, shift=RIGHT * 0.15), run_time=0.32)

    def b10_valuable(self, ctx):
        ctx.play(*[self._owned[t].animate.set_opacity(1) for t in ("f1", "f2", "f3")],
                 run_time=0.3)
        ctx.play(*style.highlight(self._owned["occupant"], style.CYAN), run_time=0.35)

    def b11_developmental(self, ctx):
        ctx.play(self._owned["stamp"].animate.set_color(style.CYAN), run_time=0.35)
        ctx.hold(0.4)
        ctx.play(*style.highlight(self._owned["occupant"], style.MUTED), run_time=0.35)

    # ------------------------------------------------------------- the swap --
    def b12_human_swap(self, ctx):
        ctx.retire("f1", "f2", "f3", "batch", run_time=0.35)
        human = style.node("review", "human", size=2.0)
        human.move_to(self._owned["slot"].get_center())
        old = self._owned.pop("occupant")
        ctx.play(ReplacementTransform(old, human), run_time=0.7)
        self._own("occupant", human)
        ctx.hold(0.5)
        # The human does not read raw JSON — the same package, rendered.
        page = RoundedRectangle(corner_radius=0.1, width=3.4, height=2.0,
                                color=style.GOLD, stroke_width=2.4)
        page.set_fill(style.PANEL, opacity=0.97)
        lines = VGroup(*[Line(LEFT * 1.2, RIGHT * 1.2, color=style.GOLD,
                              stroke_width=2, stroke_opacity=0.55) for _ in range(4)])
        lines.arrange(DOWN, buff=0.22).move_to(page)
        rendered = VGroup(page, lines)
        rendered.move_to(np.array([-0.6, stage.STAGE.bottom + 1.25, 0.0]))
        ctx.show(rendered, tag="page", anim=lambda m: FadeIn(m, shift=UP * 0.2), run_time=0.5)
        cap = style.label_text("rendered to read, not raw JSON",
                               color=style.GOLD, size="tiny")
        cap.next_to(rendered, DOWN, buff=0.2)
        ctx.show(cap, tag="pagecap", run_time=0.4)
        ctx.hold(0.4)
        # Twelve seconds on this line. Read the page the way the human would —
        # one line at a time — rather than showing a finished page and holding
        # it for nine.
        for row in lines:
            ctx.play(row.animate.set_stroke(style.GOLD, opacity=1, width=3),
                     run_time=0.45)
            ctx.hold(0.5)
            ctx.play(row.animate.set_stroke(style.GOLD, opacity=0.55, width=2),
                     run_time=0.35)
        ctx.play(*style.highlight(self._owned["occupant"], style.GOLD), run_time=0.4)
        ctx.play(self._owned["stamp"].animate.set_color(style.GOLD), run_time=0.4)

    def b13_disagree(self, ctx):
        ctx.retire("page", "pagecap", run_time=0.35)
        m = style.node("review", "model", size=1.6)
        h = style.node("review", "human", size=1.6)
        m.move_to(np.array([-3.6, stage.STAGE.bottom + 1.05, 0.0]))
        h.move_to(np.array([-0.2, stage.STAGE.bottom + 1.05, 0.0]))
        ctx.show(m, tag="dm", run_time=0.3)
        ctx.show(h, tag="dh", run_time=0.3)
        clash = style.connect(m, h, style.RED, width=2.6)
        ctx.show(clash, tag="clash", anim=lambda m: Create(m), run_time=0.35)

    def b14_history(self, ctx):
        rows = VGroup(*[
            style.mono_text(txt, color=colour, size="tiny")
            for txt, colour in (("v1 model: PASS", style.CYAN),
                                ("v2 human: FAIL", style.GOLD))
        ]).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        rows.move_to(np.array([4.4, stage.STAGE.bottom + 1.05, 0.0]))
        ctx.show(rows, tag="hist", anim=lambda m: FadeIn(m, shift=RIGHT * 0.15), run_time=0.45)

    def b15_suitability(self, ctx):
        bar = RoundedRectangle(corner_radius=0.05, width=2.6, height=0.26,
                               color=style.GRID, stroke_width=1.6)
        bar.set_fill("#071021", opacity=1)
        fill = RoundedRectangle(corner_radius=0.05, width=1.5, height=0.26,
                                color=style.AMBER, stroke_width=0)
        fill.set_fill(style.AMBER, opacity=0.85)
        bar.move_to(np.array([4.4, stage.STAGE.bottom + 0.25, 0.0]))
        fill.align_to(bar, LEFT).set_y(bar.get_y())
        lab = style.label_text("model suitability", color=style.MUTED, size="tiny")
        lab.next_to(bar, LEFT, buff=0.22)
        ctx.show(bar, fill, lab, tag="suit", run_time=0.45)
        ctx.play(fill.animate.stretch_to_fit_width(0.95).align_to(bar, LEFT), run_time=0.4)

    def b16_not_pretend(self, ctx):
        ctx.play(*style.highlight(self._owned["occupant"], style.GOLD), run_time=0.4)
        ctx.hold(0.5)
        ctx.play(*style.restroke(self._owned["schema"], style.GOLD, 3.4), run_time=0.4)

    def b17_close(self, ctx):
        tag = style.label_text("a structure humans can audit", color=style.GOLD)
        # The top of the stage is where the slot and its occupant live. The
        # caption lane is reserved and empty by now.
        stage.fit(tag, stage.CAPTION)
        ctx.show(tag, tag="final", run_time=0.5)
        ctx.hold(0.6)
        ctx.play(*style.highlight(self._owned["pkg"], style.GREEN), run_time=0.4)
