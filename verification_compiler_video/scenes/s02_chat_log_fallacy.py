"""
Section 02 — The Hidden Cost Of "Looks Good".

Reference implementation of the beat pipeline: 21 narration lines, 21 beats.
Every line changes the picture, and no beat decides its own timing.
"""
from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from verification_compiler_video.pipeline import stage, style
from verification_compiler_video.pipeline.beats import Beat, BeatScene


LEFT_COL, RIGHT_COL = stage.columns(2, gap=0.7)


class S02ChatLogFallacy(BeatScene):
    section_id = "02_chat_log_fallacy"
    title = "A chat log is not evidence"
    timing_dir = Path(__file__).resolve().parents[1] / "out" / "timing"

    def storyboard(self) -> list[Beat]:
        return [
            Beat("Here is the trap", self.b_trap,
                 note="empty stage, one word — let the line land"),
            Beat("You ask a model to write some code", self.b_prompt),
            Beat("Then you ask the same model whether the code satisfies", self.b_ask_again,
                 note="the loop closes on itself — same model, both roles"),
            Beat("It says yes, with a calm and often genuinely useful", self.b_answer),
            Beat("But what do you actually have", self.b_isolate),
            Beat("No proof. No certification. No audit trail", self.b_three_nos),
            Beat("You have a chat transcript", self.b_transcript),
            Beat("And a chat transcript is not evidence", self.b_stamp),
            Beat("For a quick iteration, that may be fine", self.b_fine),
            Beat("Where failure actually matters", self.b_switch_side),
            Beat("The question is", self.b_question_header),
            Beat("which requirement is being checked", self.b_q1),
            Beat("Which code version", self.b_q2),
            Beat("Which test result", self.b_q3),
            Beat("Which source document", self.b_q4),
            Beat("Which review rule", self.b_q5),
            Beat("Which human accepted it", self.b_q6),
            Beat("And can we reproduce what was reviewed later", self.b_q7),
            Beat("That is the gap", self.b_gap),
            Beat("The model can generate an answer", self.b_answer_chip),
            Beat("But the answer still has to be turned into evidence", self.b_become_evidence),
        ]

    # ---------------------------------------------------------------- beats --
    def b_trap(self, ctx):
        word = style.title_text("the trap")
        word.move_to(stage.STAGE.center)
        ctx.show(word, tag="trap", anim=lambda m: FadeIn(m, scale=0.9), run_time=0.5)

    def b_prompt(self, ctx):
        ctx.retire("trap", run_time=0.3)
        prompt = style.node("code", "write code", size=1.7)
        stage.fit(prompt, LEFT_COL)
        prompt.shift(UP * 1.2)
        ctx.show(prompt, tag="prompt", run_time=0.45)

    def b_ask_again(self, ctx):
        prompt = self._owned["prompt"]
        ask = style.node("review", "satisfies\nREQ-17?", size=1.5)
        ask.next_to(prompt, DOWN, buff=1.0)
        loop = CurvedArrow(prompt.get_left() + LEFT * 0.15, ask.get_left() + LEFT * 0.15,
                           color=style.MUTED, angle=1.6, stroke_width=3)
        same = style.label_text("same model", color=style.MUTED, size="tiny")
        same.next_to(loop, LEFT, buff=0.12)
        ctx.show(ask, loop, same, tag="ask", run_time=0.55)

    def b_answer(self, ctx):
        yes = style.caption_text("“Yes — it satisfies the requirement.”", color=style.WHITE)
        bubble = RoundedRectangle(corner_radius=0.2, width=yes.width + 0.7, height=1.15,
                                  color=style.BLUE, stroke_width=2.6).set_fill(style.PANEL, opacity=0.98)
        group = VGroup(bubble, yes)
        yes.move_to(bubble)
        stage.fit(group, RIGHT_COL)
        group.shift(UP * 1.0)
        ctx.show(group, tag="bubble", anim=lambda m: FadeIn(m, shift=LEFT * 0.2), run_time=0.5)
        # This line is long; a single fade would leave the frame static for five
        # seconds. Let the answer keep elaborating, the way the model would.
        ctx.hold(0.6)
        calm = style.label_text("…and here is why, in four tidy paragraphs.",
                                color=style.MUTED, size="tiny")
        calm.next_to(group, DOWN, buff=0.42)
        ctx.show(calm, tag="calm", run_time=0.45)
        ctx.play(*style.highlight(group, style.BLUE), run_time=0.4)

    def b_isolate(self, ctx):
        ctx.retire("prompt", "ask", run_time=0.4)
        ctx.play(self._owned["bubble"].animate.move_to(stage.STAGE.center + UP * 1.1),
                 run_time=0.5)

    def b_three_nos(self, ctx):
        ctx.waive("outline_over_text",
                  "the red lines are intentional strike-throughs on the missing evidence words")
        chips = VGroup(*[
            self._struck(text) for text in ("proof", "certification", "audit trail")
        ]).arrange(RIGHT, buff=0.5)
        chips.next_to(self._owned["calm"], DOWN, buff=0.55)
        ctx.show(chips, tag="nos", run_time=0.55)

    def b_transcript(self, ctx):
        ctx.retire("nos", run_time=0.3)
        label = style.label_text("chat transcript", color=style.BLUE)
        label.next_to(self._owned["bubble"], DOWN, buff=0.95)
        ctx.show(label, tag="tlabel", run_time=0.35)

    def b_stamp(self, ctx):
        stamp = style.caption_text("NOT EVIDENCE", color=style.RED)
        box = SurroundingRectangle(stamp, color=style.RED, stroke_width=3, buff=0.22)
        group = VGroup(box, stamp).rotate(-0.12)
        group.move_to(self._owned["bubble"].get_center() + DOWN * 0.15 + RIGHT * 0.4)
        # The stamp is *supposed* to land across the quote — that is the beat.
        style.allow_overlap(group, self._owned["bubble"],
                            reason="stamp deliberately overprints the model's answer")
        ctx.show(group, tag="stamp", anim=lambda m: FadeIn(m, scale=1.25), run_time=0.4)
        ctx.play(self._owned["bubble"].animate.set_opacity(0.45), run_time=0.25)

    def b_fine(self, ctx):
        ok = style.label_text("quick iteration", color=style.MUTED, size="tiny")
        # Hang it off the transcript label, not off the stamp. The stamp is
        # placed relative to the bubble's centre, so "below the stamp" and
        # "below the bubble" resolve to the same strip of screen and the two
        # labels land on top of each other.
        ok.next_to(self._owned["tlabel"], DOWN, buff=0.42)
        ctx.show(ok, tag="fine", run_time=0.35)

    def b_switch_side(self, ctx):
        ctx.retire("stamp", "tlabel", "fine", "calm", run_time=0.35)
        group = VGroup(self._owned["bubble"])
        ctx.play(group.animate.scale(0.72).move_to(LEFT_COL.center + UP * 1.9).set_opacity(0.35),
                 run_time=0.5)
        # Name the stakes one at a time rather than holding a still frame.
        stakes = ["aircraft", "vehicles", "implants"]
        chips = VGroup(*[style.node("anomaly", s, size=1.55) for s in stakes])
        chips.arrange(RIGHT, buff=0.45)
        chips.move_to(np.array([LEFT_COL.center[0], stage.STAGE.bottom + 0.95, 0.0]))
        self._own("stakes", chips)
        for chip in chips:
            ctx.play(FadeIn(chip, shift=UP * 0.15), run_time=0.3)
            ctx.hold(0.3)
        # Keep the stakes moving through the rest of the line rather than
        # freezing on them — the dead-air check is right that a still frame here
        # is five seconds of nothing while the narrator is still talking.
        for _ in range(2):
            for chip in chips:
                ctx.play(*style.highlight(chip, style.RED), run_time=0.24)
                ctx.hold(0.18)

    # The seven questions are the spine of the section, so they get the middle of
    # the stage rather than a column on the right — and each one is bulleted with
    # the shape it is actually asking about, so the grammar the rest of the video
    # depends on is taught here instead of asserted later.
    Q_LEFT = -2.55
    Q_TOP = 1.42
    Q_STEP = 0.54

    def b_question_header(self, ctx):
        ctx.retire("stakes", "bubble", run_time=0.3)
        head = style.label_text("what an auditor has to be able to ask", color=style.GOLD)
        head.move_to(np.array([0.0, 2.02, 0.0]))
        ctx.show(head, tag="qhead", run_time=0.4)
        self._q_y = self.Q_TOP

    def _question(self, ctx, text: str, tag: str, kind: str):
        row = style.label_text(text, color=style.WHITE, size="node")
        bullet = style.node(kind, "", size=0.34)
        group = VGroup(bullet, row).arrange(RIGHT, buff=0.26)
        group.move_to(np.array([0.0, self._q_y, 0.0]))
        group.align_to(np.array([self.Q_LEFT, 0.0, 0.0]), LEFT)
        self._q_y -= self.Q_STEP
        ctx.show(group, tag=tag, anim=lambda m: FadeIn(m, shift=RIGHT * 0.18), run_time=0.32,
                 nudge=False)

    def b_q1(self, ctx): self._question(ctx, "which requirement?", "q1", "requirement")
    def b_q2(self, ctx): self._question(ctx, "which code version?", "q2", "code")
    def b_q3(self, ctx): self._question(ctx, "which test result?", "q3", "test")
    def b_q4(self, ctx): self._question(ctx, "which source document?", "q4", "source")
    def b_q5(self, ctx): self._question(ctx, "which review rule?", "q5", "review")
    def b_q6(self, ctx): self._question(ctx, "which human accepted it?", "q6", "review")
    def b_q7(self, ctx): self._question(ctx, "reproducible later?", "q7", "evidence")

    def b_gap(self, ctx):
        rows = VGroup(*[self._owned[f"q{i}"] for i in range(1, 8)])
        brace = Brace(rows, direction=LEFT, color=style.RED)
        label = style.label_text("the gap", color=style.RED)
        label.next_to(brace, LEFT, buff=0.2)
        ctx.show(brace, label, tag="gap", run_time=0.45)

    def b_answer_chip(self, ctx):
        chip = style.node("code", "an answer", size=1.7)
        chip.move_to(np.array([4.55, 0.35, 0.0]))
        ctx.show(chip, tag="chip", run_time=0.4)

    def b_become_evidence(self, ctx):
        chip = self._owned.pop("chip")
        card = style.node("evidence", "evidence", size=1.7)
        card.move_to(chip.get_center())
        ctx.play(ReplacementTransform(chip, card), run_time=0.6)
        self._own("evidence", card)
        ctx.play(*style.highlight(card, style.GREEN), run_time=0.3)

    # ---------------------------------------------------------------- utils --
    def _struck(self, text: str) -> VGroup:
        label = style.label_text(text, color=style.MUTED, size="node")
        line = Line(label.get_left(), label.get_right(), color=style.RED, stroke_width=3)
        return VGroup(label, line)
