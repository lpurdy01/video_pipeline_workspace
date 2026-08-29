"""
Section 03 — Safety-Critical Software Already Has The Shape.

33 beats over two minutes. The argument climbs: standards exist, they demand
traceability, that traceability is expensive, and the reason it exists is that
nobody — human or model — can review a whole system at once.

Layout borrows the banded-zone device from the whitepaper's Figure 3: labelled
columns do most of the explaining before a single edge is read.
"""
from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from verification_compiler_video.pipeline import stage, style
from verification_compiler_video.pipeline.beats import Beat, BeatScene


class S03TraceabilityShape(BeatScene):
    section_id = "03_traceability_shape"
    title = "The shape already exists"
    timing_dir = Path(__file__).resolve().parents[1] / "out" / "timing"

    def storyboard(self) -> list[Beat]:
        return [
            Beat("High-assurance software has been dealing with this", self.b00_decades),
            Beat("And I think most developers have no idea this world exists", self.b01_unseen),
            Beat("There are entire standards governing how this software", self.b02_standards),
            Beat("DO-178C in aerospace", self.b03_do178),
            Beat("ISO 26262, and ASIL levels, in automotive", self.b04_iso),
            Beat("There are more, industry by industry", self.b05_more),
            Beat("The details vary, and the standards themselves are careful", self.b06_dim),
            Beat("But the broad pattern is simple enough to see", self.b07_pattern),
            Beat("You do not just write code and hope", self.b08_code_alone),
            Beat("You maintain traceability", self.b09_traceability),
            Beat("A requirement traces to design", self.b10_req_design),
            Beat("Design traces to code", self.b11_design_code),
            Beat("Code traces to tests", self.b12_code_test),
            Beat("Tests trace to results", self.b13_test_result),
            Beat("Results trace to review records", self.b14_result_review),
            Beat("And all of that has to stay tied to the version", self.b15_version),
            Beat("That can sound like bureaucracy from the outside", self.b16_bureaucracy),
            Beat("And I want to be honest about it: it is a lot of overhead work",
                 self.b17_overhead),
            Beat("It is part of why the same function can cost a hundred times more",
                 self.b18_cost),
            Beat("But the deeper idea is not bureaucracy", self.b19_not_bureaucracy),
            Beat("It is coordination", self.b20_coordination),
            Beat("It is a way for a large group of limited humans", self.b21_many_hands),
            Beat("And reviewable is the word that matters", self.b22_reviewable),
            Beat("Nobody can look at a whole system at once", self.b23_too_big),
            Beat("It is too big. That is true of every engineer on the team", self.b24_human),
            Beat("It is just as true of an AI model asked to do the same thing", self.b25_model),
            Beat("So you break it apart", self.b26_break),
            Beat("You verify the small units first", self.b27_units),
            Beat("Unit tests. Integration tests. System tests", self.b28_ladder),
            Beat("And the requirements stack the same way", self.b29_req_stack),
            Beat("You climb that ladder until the system is as true", self.b30_climb),
            Beat("And that is the clue for AI-assisted software", self.b31_clue),
            Beat("If models are going to generate more artifacts, faster", self.b32_finish),
        ]

    # -------------------------------------------------------- the standards --
    def b00_decades(self, ctx):
        axis = Line(np.array([stage.STAGE.left + 0.9, 0.0, 0.0]),
                    np.array([stage.STAGE.right - 0.9, 0.0, 0.0]),
                    color=style.GRID, stroke_width=3)
        marks = VGroup()
        for i, year in enumerate(("1992", "2011", "2018", "now")):
            x = stage.STAGE.left + 1.4 + i * ((stage.STAGE.width - 2.8) / 3)
            tick = Line(np.array([x, -0.16, 0]), np.array([x, 0.16, 0]),
                        color=style.MUTED, stroke_width=3)
            lab = style.label_text(year, color=style.MUTED, size="tiny")
            lab.next_to(tick, DOWN, buff=0.18)
            marks.add(tick, lab)
        ctx.show(axis, tag="axis", anim=lambda m: Create(m), run_time=0.7)
        ctx.show(marks, tag="marks", run_time=0.6)

    def b01_unseen(self, ctx):
        # Fade the timeline rather than covering it: a filled rectangle over text
        # is text buried, however it was meant.
        ctx.play(self._owned["marks"].animate.set_opacity(0.18),
                 self._owned["axis"].animate.set_stroke(opacity=0.25), run_time=0.5)
        tag = style.label_text("most of us never see it", color=style.MUTED, size="tiny")
        tag.move_to(stage.STAGE.center + DOWN * 1.6)
        ctx.show(tag, tag="veiltag", run_time=0.4)

    def b02_standards(self, ctx):
        ctx.retire("veiltag", "axis", "marks", run_time=0.4)
        docs = VGroup(*[style.node("source", "", size=1.5) for _ in range(3)])
        docs.arrange(RIGHT, buff=1.3)
        docs.move_to(stage.STAGE.center + UP * 0.35)
        ctx.show(docs, tag="docs", anim=lambda m: FadeIn(m, shift=UP * 0.2), run_time=0.7)

    def _name_doc(self, ctx, i: int, name: str, tag: str):  # noqa: D401
        doc = self._owned["docs"][i]
        lab = style.label_text(name, color=style.VIOLET, size="tiny")
        # Stagger the captions: three documents side by side put their labels
        # within a few hundredths of each other, which reads as one smear.
        lab.next_to(doc, DOWN, buff=0.28 + 0.42 * (i % 2))
        ctx.play(*style.highlight(doc, style.VIOLET), run_time=0.3)
        ctx.show(lab, tag=tag, run_time=0.35)

    def b03_do178(self, ctx):
        self._name_doc(ctx, 0, "DO-178C · aerospace", "d0")

    def b04_iso(self, ctx):
        self._name_doc(ctx, 1, "ISO 26262 · automotive", "d1")

    def b05_more(self, ctx):
        self._name_doc(ctx, 2, "IEC 62443 · industrial", "d2")

    def b06_dim(self, ctx):
        ctx.play(self._owned["docs"].animate.set_opacity(0.5), run_time=0.5)

    def b07_pattern(self, ctx):
        ctx.retire("d0", "d1", "d2", run_time=0.3)
        ctx.play(self._owned["docs"].animate.scale(0.5).move_to(
            np.array([stage.STAGE.left + 1.5, stage.STAGE.top - 0.9, 0.0])), run_time=0.6)

    # ------------------------------------------------------- the trace chain --
    def b08_code_alone(self, ctx):
        code = style.node("code", "clamp()", size=1.35)
        code.move_to(stage.STAGE.center + DOWN * 0.2)
        ctx.show(code, tag="n2", anim=lambda m: FadeIn(m, scale=0.9), run_time=0.5)

    def b09_traceability(self, ctx):
        tag = style.label_text("traceability", color=style.GOLD)
        tag.move_to(np.array([0.0, stage.STAGE.top - 0.55, 0.0]))
        ctx.show(tag, tag="tracelabel", run_time=0.4)

    def _chain_slot(self, i: int) -> np.ndarray:
        xs = [-5.3, -2.65, 0.0, 2.65, 5.3]
        return np.array([xs[i], -0.2, 0.0])

    def b10_req_design(self, ctx):
        ctx.play(self._owned["n2"].animate.move_to(self._chain_slot(2)), run_time=0.45)
        req = style.node("requirement", "REQ-17", size=1.35).move_to(self._chain_slot(0))
        des = style.node("source", "design", size=1.35).move_to(self._chain_slot(1))
        ctx.show(req, tag="n0", run_time=0.35)
        ctx.show(des, tag="n1", run_time=0.35)
        ctx.show(style.connect(req, des, style.GOLD), tag="e0",
                 anim=lambda m: Create(m), run_time=0.3)

    def b11_design_code(self, ctx):
        ctx.show(style.connect(self._owned["n1"], self._owned["n2"], style.VIOLET),
                 tag="e1", anim=lambda m: Create(m), run_time=0.4)

    def b12_code_test(self, ctx):
        test = style.node("test", "TC-001", size=1.35).move_to(self._chain_slot(3))
        ctx.show(test, tag="n3", run_time=0.35)
        ctx.show(style.connect(self._owned["n2"], test, style.BLUE), tag="e2",
                 anim=lambda m: Create(m), run_time=0.3)

    def b13_test_result(self, ctx):
        res = style.node("evidence", "TR-001", size=1.35).move_to(self._chain_slot(4))
        ctx.show(res, tag="n4", run_time=0.35)
        ctx.show(style.connect(self._owned["n3"], res, style.CYAN), tag="e3",
                 anim=lambda m: Create(m), run_time=0.3)

    def b14_result_review(self, ctx):
        rev = style.node("review", "signed", size=1.35)
        rev.move_to(self._chain_slot(4) + DOWN * 1.85)
        ctx.show(rev, tag="n5", run_time=0.35)
        ctx.show(style.connect(self._owned["n4"], rev, style.GREEN), tag="e4",
                 anim=lambda m: Create(m), run_time=0.3)

    def b15_version(self, ctx):
        chain = VGroup(*[self._owned[f"n{i}"] for i in range(6)])
        tag = style.mono_text("git a1b2c3", color=style.GOLD, size="tiny")
        tag.move_to(np.array([0.0, stage.STAGE.bottom + 0.55, 0.0]))
        band = SurroundingRectangle(chain, color=style.GOLD, stroke_width=2,
                                    buff=0.3).set_stroke(opacity=0.5)
        ctx.show(band, tag="vband", anim=lambda m: Create(m), run_time=0.6)
        ctx.show(tag, tag="vtag", run_time=0.4)

    # ------------------------------------------------------------- the cost --
    def b16_bureaucracy(self, ctx):
        # This is where the chain recedes, and it has to take its connectors with
        # it. Dimming only the shapes left five bright arrows drawn across a
        # picture that had supposedly stepped back — which is what made the cost
        # comparison that follows read as cluttered.
        ctx.recede(*[f"n{i}" for i in range(6)], *[f"e{i}" for i in range(5)],
                   opacity=0.35, run_time=0.5)

    def b17_overhead(self, ctx):
        tag = style.label_text("it really is a lot of work", color=style.AMBER, size="tiny")
        tag.next_to(self._owned["vtag"], UP, buff=0.3)
        ctx.show(tag, tag="honest", run_time=0.4)

    def b18_cost(self, ctx):
        ctx.retire("honest", "vband", "vtag", run_time=0.3)
        # The connectors have to recede with the nodes; leaving them lit was
        # the "shapes fade but the arrows don't" note. Name the edge tags
        # explicitly — the scene knows them, and relying on geometry to find
        # them is guesswork the scene does not need to do.
        ctx.recede(*[f"n{i}" for i in range(6)], *[f"e{i}" for i in range(5)],
                   opacity=0.16, run_time=0.35)
        small = Rectangle(width=0.55, height=0.42, color=style.BLUE, stroke_width=2.5)
        small.set_fill(style.PANEL, opacity=0.9)
        big = Rectangle(width=5.6, height=0.42, color=style.AMBER, stroke_width=2.5)
        big.set_fill(style.PANEL, opacity=0.9)
        small.move_to(np.array([-2.0, 1.35, 0.0]), aligned_edge=LEFT)
        big.move_to(np.array([-2.0, 0.45, 0.0]), aligned_edge=LEFT)
        l1 = style.label_text("drone", color=style.BLUE, size="tiny").next_to(small, LEFT, buff=0.3)
        l2 = style.label_text("aircraft", color=style.AMBER, size="tiny").next_to(big, LEFT, buff=0.3)
        ctx.show(small, l1, tag="bar1", run_time=0.4)
        ctx.play(GrowFromEdge(big, LEFT), FadeIn(l2), run_time=0.7)
        self._own("bar2", VGroup(big, l2))
        x100 = style.label_text("100x", color=style.AMBER)
        x100.next_to(big, RIGHT, buff=0.3)
        ctx.show(x100, tag="x100", run_time=0.35)

    def b19_not_bureaucracy(self, ctx):
        ctx.retire("bar1", "bar2", "x100", run_time=0.4)
        # Bring the connectors back up with the nodes, or the chain returns as a
        # set of bright shapes joined by ghosts.
        ctx.play(*[self._owned[f"n{i}"].animate.set_opacity(1.0) for i in range(6)],
                 *[self._owned[f"e{i}"].animate.set_opacity(1.0) for i in range(5)],
                 run_time=0.5)

    def b20_coordination(self, ctx):
        tag = style.label_text("coordination", color=style.CYAN)
        tag.move_to(np.array([0.0, stage.STAGE.bottom + 1.45, 0.0]))
        ctx.show(tag, tag="coord", run_time=0.4)

    def b21_many_hands(self, ctx):
        hands = VGroup(*[style.node("review", "", size=0.5) for _ in range(7)])
        hands.arrange(RIGHT, buff=0.34)
        hands.move_to(np.array([0.0, stage.STAGE.bottom + 0.55, 0.0]))
        ctx.show(hands, tag="hands", anim=lambda m: FadeIn(m, shift=UP * 0.2), run_time=0.6)
        for h in hands:
            ctx.play(*style.highlight(h, style.VIOLET), run_time=0.14)

    def b22_reviewable(self, ctx):
        ctx.retire("coord", "hands", run_time=0.25)
        tag = style.label_text("reviewable", color=style.GOLD)
        tag.move_to(np.array([0.0, stage.STAGE.bottom + 1.45, 0.0]))
        ctx.show(tag, tag="reviewable", run_time=0.4)

    # --------------------------------------------------------- the argument --
    def b23_too_big(self, ctx):
        ctx.clear_stage("tracelabel", run_time=0.5)
        blob = VGroup()
        rng = __import__("random").Random(5)
        for _ in range(46):
            c = Square(side_length=0.3, color=style.BLUE, stroke_width=1.6)
            c.set_fill(style.PANEL, opacity=0.85)
            c.move_to(np.array([rng.uniform(-3.2, 3.2), rng.uniform(-1.5, 1.5), 0.0]))
            blob.add(c)
        blob.move_to(stage.STAGE.center + UP * 0.15)
        ctx.show(blob, tag="blob", anim=lambda m: FadeIn(m, scale=0.9), run_time=0.8)

    def b24_human(self, ctx):
        h = style.node("review", "human", size=1.15)
        h.move_to(np.array([stage.STAGE.left + 1.4, stage.STAGE.bottom + 0.95, 0.0]))
        ctx.show(h, tag="human", run_time=0.4)

    def b25_model(self, ctx):
        m = style.node("review", "model", size=1.15)
        m.move_to(np.array([stage.STAGE.right - 1.4, stage.STAGE.bottom + 0.95, 0.0]))
        ctx.show(m, tag="model", run_time=0.4)
        # Violet, not red. Red means anomaly in this grammar, and colouring the
        # two reviewers red says they are the fault rather than the pair of
        # actors the section is about.
        ctx.play(*style.highlight(m, style.VIOLET),
                 *style.highlight(self._owned["human"], style.VIOLET), run_time=0.4)

    def b26_break(self, ctx):
        blob = self._owned["blob"]
        groups = [VGroup(*blob[i::4]) for i in range(4)]
        anims = []
        for i, g in enumerate(groups):
            anims.append(g.animate.shift(RIGHT * (i - 1.5) * 1.05))
        ctx.play(*anims, run_time=0.7)

    def b27_units(self, ctx):
        ctx.play(self._owned["blob"].animate.set_opacity(0.3), run_time=0.4)
        unit = style.node("code", "one unit", size=1.75)
        unit.move_to(stage.STAGE.center + UP * 0.2)
        ctx.show(unit, tag="unit", anim=lambda m: FadeIn(m, scale=0.85), run_time=0.45)

    def b28_ladder(self, ctx):
        rungs = ["unit", "integration", "system", "verification"]
        ladder = VGroup()
        for i, name in enumerate(rungs):
            bar = RoundedRectangle(corner_radius=0.06, width=3.2 + i * 0.55, height=0.44,
                                   color=style.CYAN, stroke_width=2.2)
            bar.set_fill(style.PANEL, opacity=0.95)
            lab = style.label_text(f"{name} tests", color=style.WHITE, size="tiny").move_to(bar)
            ladder.add(VGroup(bar, lab))
        ladder.arrange(UP, buff=0.2)
        ladder.move_to(stage.STAGE.center + DOWN * 0.1)
        ctx.retire("unit", run_time=0.25)
        for rung in ladder:
            ctx.play(FadeIn(rung, shift=UP * 0.18), run_time=0.28)
            ctx.hold(0.32)
        self._own("ladder", ladder)

    def b29_req_stack(self, ctx):
        ctx.retire("human", "model", run_time=0.3)
        ctx.play(self._owned["ladder"].animate.move_to(
            np.array([stage.STAGE.left + 3.3, 0.0, 0.0])), run_time=0.5)
        tree = VGroup()
        top = style.node("requirement", "SR-1", size=1.15)
        mids = VGroup(*[style.node("requirement", f"HL-{i}", size=1.0) for i in (1, 2)])
        mids.arrange(RIGHT, buff=0.7)
        lows = VGroup(*[style.node("requirement", f"LL-{i}", size=0.9) for i in (1, 2, 3)])
        lows.arrange(RIGHT, buff=0.45)
        col = VGroup(top, mids, lows).arrange(DOWN, buff=0.55)
        col.move_to(np.array([stage.STAGE.right - 2.6, 0.0, 0.0]))
        for row in (top, mids, lows):
            ctx.play(FadeIn(row, shift=DOWN * 0.14), run_time=0.32)
            ctx.hold(0.4)
        tree.add(top, mids, lows)
        self._own("tree", tree)

    def b30_climb(self, ctx):
        for rung in self._owned["ladder"]:
            ctx.play(*style.highlight(rung, style.GREEN), run_time=0.22)
            ctx.hold(0.24)
        tag = style.label_text("as true as you can make it", color=style.GREEN, size="tiny")
        tag.move_to(np.array([0.0, stage.STAGE.bottom + 0.5, 0.0]))
        ctx.show(tag, tag="astrue", run_time=0.4)

    def b31_clue(self, ctx):
        ctx.retire("astrue", "tree", run_time=0.4)
        ctx.play(self._owned["ladder"].animate.move_to(stage.STAGE.center + UP * 0.2),
                 run_time=0.5)

    def b32_finish(self, ctx):
        ctx.retire("blob", run_time=0.4)
        rng = __import__("random").Random(9)
        flood = VGroup()
        # Fill the space that is free, and stay behind what is already there.
        # Scattering uniformly put a dozen of these on top of the test ladder.
        spots = stage.free_points(26, list(self.mobjects), rng)
        for spot in spots:
            c = Square(side_length=0.26, color=style.CYAN, stroke_width=1.6)
            c.set_fill(style.PANEL, opacity=0.85)
            c.set_z_index(style.Z_BACKDROP, family=True)
            c.move_to(spot)
            flood.add(c)
        ctx.play(LaggedStart(*[FadeIn(c, scale=0.7) for c in flood], lag_ratio=0.03),
                 run_time=1.2)
        self._own("flood", flood)
        ctx.hold(0.6)
        ctx.play(*style.restroke(self._owned["ladder"], style.GOLD, 4), run_time=0.5)
        need = style.label_text("an even stronger structure", color=style.GOLD)
        need.move_to(np.array([0.0, stage.STAGE.bottom + 0.55, 0.0]))
        ctx.show(need, tag="need", run_time=0.5)
        for rung in self._owned["ladder"]:
            ctx.play(*style.highlight(rung, style.GOLD), run_time=0.2)
            ctx.hold(0.25)
        ctx.play(self._owned["flood"].animate.set_opacity(0.35), run_time=0.5)
