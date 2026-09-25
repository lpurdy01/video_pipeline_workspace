"""
Section 10 — Closing: The Future Is Evidence Generation.

The recapitulation. Everything the video built comes back in miniature, in the
order the narrator lists it, and then the last line lands on the phrase the whole
piece has been walking toward.
"""
from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from verification_compiler_video.pipeline import stage, style
from verification_compiler_video.pipeline.beats import Beat, BeatScene


class S10EvidenceSurface(BeatScene):
    section_id = "10_evidence_surface"
    title = "Generate evidence"
    timing_dir = Path(__file__).resolve().parents[1] / "out" / "timing"

    def storyboard(self) -> list[Beat]:
        return [
            Beat("I think this is where AI software is going", self.b00_open),
            Beat("Not because models will magically replace verification", self.b01_not_magic),
            Beat("They will not", self.b02_will_not),
            Beat("But because generation is getting cheaper", self.b03_cheaper,
                 note="6.9s — the obligations start piling up as the line runs"),
            Beat("Another function", self.b04_function),
            Beat("Another test", self.b05_test),
            Beat("Another design note", self.b06_note),
            Beat("Another claim", self.b07_claim),
            Beat("Another assumption", self.b08_assumption),
            Beat("The bottleneck becomes:", self.b09_bottleneck),
            Beat("what can we trust enough to connect back into the world", self.b10_trust),
            Beat("The Verification Compiler is one answer to that bottleneck", self.b11_answer),
            Beat("Turn the project into a graph", self.b12_graph),
            Beat("Traverse the graph deterministically", self.b13_traverse),
            Beat("Assemble bounded review packages", self.b14_assemble),
            Beat("Let models help during development", self.b15_models),
            Beat("Let humans retain authority where it matters", self.b16_humans),
            Beat("And preserve the result as evidence", self.b17_preserve),
            Beat("Not \"trust the AI.\"", self.b18_not_trust_ai),
            Beat("Trust the evidence surface", self.b19_trust_surface),
            Beat("Because the future of AI software is not just generating code",
                 self.b20_not_just_code),
            Beat("It is generating evidence we can actually inspect", self.b21_final),
        ]

    # ---------------------------------------------------------------- beats --
    def b00_open(self, ctx):
        m = style.node("review", "model", size=2.0)
        m.move_to(np.array([-4.4, 0.9, 0.0]))
        ctx.show(m, tag="model", anim=lambda m_: FadeIn(m_, scale=0.85), run_time=0.5)

    def b01_not_magic(self, ctx):
        v = style.node("evidence", "verified", size=2.2)
        v.move_to(np.array([1.0, 0.9, 0.0]))
        ctx.show(v, tag="ver", run_time=0.45)
        wand = style.connect(self._owned["model"], v, style.VIOLET, width=2.6)
        ctx.show(wand, tag="wand", anim=lambda m_: Create(m_), run_time=0.4)

    def b02_will_not(self, ctx):
        cross = VGroup(
            Line(UL * 0.32, DR * 0.32, color=style.RED, stroke_width=5),
            Line(UR * 0.32, DL * 0.32, color=style.RED, stroke_width=5),
        ).move_to(self._owned["wand"])
        ctx.show(cross, tag="nope", anim=lambda m_: Create(m_), run_time=0.4)

    def b03_cheaper(self, ctx):
        ctx.retire("nope", "wand", "ver", "model", run_time=0.4)
        self._pile = VGroup()
        self._own("pile", self._pile)
        tag = style.label_text("every generation makes an obligation",
                               color=style.MUTED, size="tiny")
        tag.move_to(np.array([0.0, stage.STAGE.top - 0.4, 0.0]))
        ctx.show(tag, tag="oblig", run_time=0.45)
        ctx.hold(0.6)
        for i in range(4):
            self._add_obligation(ctx, style.CYAN, 0.55)

    def _add_obligation(self, ctx, colour, hold: float = 0.0):
        rng = __import__("random").Random(len(self._pile) * 7 + 3)
        c = Square(side_length=0.34, color=colour, stroke_width=2)
        c.set_fill(style.PANEL, opacity=0.9)
        c.move_to(np.array([rng.uniform(stage.STAGE.left + 0.6, stage.STAGE.right - 0.6),
                            rng.uniform(stage.STAGE.bottom + 0.5, 1.1), 0.0]))
        self._pile.add(c)
        ctx.play(FadeIn(c, shift=DOWN * 0.25), run_time=0.24)
        if hold:
            ctx.hold(hold)

    def b04_function(self, ctx):
        self._add_obligation(ctx, style.BLUE)

    def b05_test(self, ctx):
        self._add_obligation(ctx, style.CYAN)

    def b06_note(self, ctx):
        self._add_obligation(ctx, style.VIOLET)

    def b07_claim(self, ctx):
        self._add_obligation(ctx, style.GOLD)

    def b08_assumption(self, ctx):
        self._add_obligation(ctx, style.RED)

    def b09_bottleneck(self, ctx):
        gate = style.node("review", "", size=1.5)
        gate.move_to(np.array([0.0, stage.STAGE.bottom + 0.9, 0.0]))
        ctx.show(gate, tag="gate", anim=lambda m_: FadeIn(m_, scale=1.3), run_time=0.4)

    def b10_trust(self, ctx):
        tag = style.label_text("what can we trust?", color=style.GOLD)
        tag.next_to(self._owned["gate"], RIGHT, buff=0.4)
        ctx.show(tag, tag="q", run_time=0.45)

    # ------------------------------------------------------------- the recap --
    def b11_answer(self, ctx):
        ctx.clear_stage(run_time=0.6)
        self._steps = []

    def _step(self, ctx, kind: str, label: str, i: int, tag: str):
        n = style.node(kind, label, size=1.85)
        xs = [-5.1, -2.55, 0.0, 2.55, 5.1]
        n.move_to(np.array([xs[i], 0.55, 0.0]))
        ctx.show(n, tag=tag, anim=lambda m_: FadeIn(m_, shift=UP * 0.18), run_time=0.4)
        if self._steps:
            edge = style.connect(self._steps[-1], n, style.CYAN, width=2.4)
            ctx.show(edge, tag=f"{tag}_e", anim=lambda m_: Create(m_), run_time=0.28)
        self._steps.append(n)
        return n

    def b12_graph(self, ctx):
        self._step(ctx, "source", "graph", 0, "s_graph")

    def b13_traverse(self, ctx):
        self._step(ctx, "code", "traverse", 1, "s_trav")

    def b14_assemble(self, ctx):
        self._step(ctx, "vqp", "VQP", 2, "s_vqp")

    def b15_models(self, ctx):
        self._step(ctx, "review", "model", 3, "s_model")

    def b16_humans(self, ctx):
        n = self._step(ctx, "review", "human", 4, "s_human")
        ctx.play(*style.highlight(n, style.GOLD), run_time=0.3)

    def b17_preserve(self, ctx):
        card = style.node("evidence", "evidence", size=2.1)
        card.move_to(np.array([0.0, stage.STAGE.bottom + 1.0, 0.0]))
        ctx.show(card, tag="evid", anim=lambda m_: FadeIn(m_, shift=UP * 0.2), run_time=0.5)
        flows = VGroup(*[style.connect(self._steps[i], card, style.GREEN, width=2.0)
                         for i in (3, 4)])
        ctx.show(flows, tag="flows", anim=lambda m_: Create(m_), run_time=0.4)

    def b18_not_trust_ai(self, ctx):
        ctx.play(self._owned["s_model"].animate.set_opacity(0.35), run_time=0.4)

    def b19_trust_surface(self, ctx):
        ctx.play(*style.highlight(self._owned["evid"], style.GREEN), run_time=0.45)

    def b20_not_just_code(self, ctx):
        ctx.retire("s_graph", "s_trav", "s_vqp", "s_model", "s_human",
                   "s_trav_e", "s_vqp_e", "s_model_e", "s_human_e", "flows",
                   run_time=0.6)
        ctx.play(self._owned["evid"].animate.move_to(stage.STAGE.center + UP * 0.3),
                 run_time=0.6)
        line = style.title_text("evidence we can inspect")
        line.move_to(stage.STAGE.center + DOWN * 1.35)
        ctx.show(line, tag="final", anim=lambda m_: FadeIn(m_, scale=0.93), run_time=0.35)

    def b21_final(self, ctx):
        ctx.play(self._owned["final"].animate.scale(1.04), run_time=0.35)
        ctx.play(*style.highlight(self._owned["evid"], style.GREEN), run_time=0.4)
