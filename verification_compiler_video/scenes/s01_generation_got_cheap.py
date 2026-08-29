"""
Section 01 — Cold Open: Generation Got Cheap.

The longest section (151s, 36 narration lines) and the one that has to earn the
viewer. Its argument is a shape: one square, then a flood, then a wall the flood
cannot cross, then the compiler that gets it through.

Built from the beat proposals in out/storyboard/01_beat_proposals.md.
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from verification_compiler_video.pipeline import stage, style
from verification_compiler_video.pipeline.beats import Beat, BeatScene

LEFT_COL, RIGHT_COL = stage.columns(2, gap=0.55)
DIVIDE_X = (LEFT_COL.right + RIGHT_COL.left) / 2


def chip(color: str, size: float = 0.34) -> VGroup:
    """A wordless artifact tile. No label means no legibility risk in a flood."""
    box = Square(side_length=size, color=color, stroke_width=2.0)
    box.set_fill(style.PANEL, opacity=0.9)
    return VGroup(box)


def dot(color: str, r: float = 0.17) -> Circle:
    c = Circle(radius=r, color=color, stroke_width=2.0)
    c.set_fill(style.PANEL, opacity=0.9)
    return c


class S01GenerationGotCheap(BeatScene):
    section_id = "01_generation_got_cheap"
    title = "Generation got cheap"
    timing_dir = Path(__file__).resolve().parents[1] / "out" / "timing"

    def storyboard(self) -> list[Beat]:
        return [
            Beat("AI made writing code cheap", self.b00_one_square,
                 note="one square: the whole video starts from a single unit of code"),
            Beat("But it did not make trusting code cheap", self.b01_review_above),
            Beat("That is the part I think people are still underestimating", self.b02_strain),
            Beat("If a model can write a function in ten seconds", self.b03_multiply),
            Beat("If it can write the tests, the documentation", self.b04_artifact_web,
                 note="9.4s line — the artifacts have to keep arriving as they are named"),
            Beat("But now you have a new problem", self.b05_stop),
            Beat("Who checks all of it", self.b06_lone_reviewer),
            Beat("And this is not a thought experiment", self.b07_widen),
            Beat("Across the industry, more and more of the work happens agentically",
                 self.b08_rain),
            Beat("Pull requests arrive faster than any team can actually read them",
                 self.b09_reviewers_struck),
            Beat("The pace becomes the product, and review is the thing that gets crushed",
                 self.b10_buried),
            Beat("Because serious software is not just software that runs", self.b11_clean_slate),
            Beat("Serious software is software where someone can explain", self.b12_build_chain,
                 note="13.8s line — one artifact snaps in per clause the narrator names"),
            Beat("Let me be concrete about what I mean", self.b13_divide),
            Beat("In one of them, quality is a business problem", self.b14_web_stack),
            Beat("A web application has to be reliable enough that customers do not leave",
                 self.b15_revenue),
            Beat("If something breaks on Monday, you ship a fix on Tuesday", self.b16_break_fix),
            Beat("In the other one, software flies aircraft", self.b17_focus_right),
            Beat("It keeps satellites talking to the ground", self.b18_second_chain),
            Beat("It decides how hard your car brakes", self.b19_third_chain),
            Beat("That software is certified before it is allowed to run", self.b20_seal,
                 note="9.1s line — the seal draws, then the accountability label lands"),
            Beat("Right now that second world is almost closed to AI-assisted development",
                 self.b21_bounce),
            Beat("Not because the models write bad code", self.b22_identical),
            Beat("Because nobody can check the flood fast enough", self.b23_pressure),
            Beat("AI has made generation faster", self.b24_pile_up),
            Beat("It has not automatically made verification faster", self.b25_static),
            Beat("So the bottleneck moves", self.b26_push_in),
            Beat("Not to the editor", self.b27_not_editor),
            Beat("Not to the model", self.b28_not_model),
            Beat("To trust", self.b29_trust),
            Beat("And that is why I have been thinking about something I call a Verification Compiler",
                 self.b30_compiler),
            Beat("The goal is not to bring AI into safety-critical work for the sake of it",
                 self.b31_frame_turns),
            Beat("The goal is to automate the verification scaffolding", self.b32_fold,
                 note="8.8s line — scaffolding snaps on, then folds into the package"),
            Beat("It is a process, not a shortcut", self.b33_through_gate),
            Beat("Or, less formally", self.b34_beat),
            Beat("a compiler for trust", self.b35_title),
        ]

    # ------------------------------------------------------- one unit of code --
    def b00_one_square(self, ctx):
        sq = style.node("code", "code", size=1.25)
        sq.move_to(stage.STAGE.center)
        ctx.show(sq, tag="code", anim=lambda m: FadeIn(m, scale=0.85), run_time=0.55)

    def b01_review_above(self, ctx):
        rev = style.node("review", "checked?", size=1.5)
        rev.move_to(stage.STAGE.center + UP * 1.72)
        link = DashedLine(rev.get_bottom(), self._owned["code"].get_top(),
                          color=style.MUTED, stroke_width=3, dash_length=0.12)
        ctx.show(rev, link, tag="review", run_time=0.5)

    def b02_strain(self, ctx):
        ctx.play(*style.highlight(self._owned["review"][0], style.GOLD), run_time=0.45)
        ctx.hold(0.4)
        ctx.play(*style.restroke(self._owned["review"][0], style.GOLD, 3), run_time=0.3)

    def b03_multiply(self, ctx):
        row = VGroup(*[chip(style.BLUE, 0.6) for _ in range(4)]).arrange(RIGHT, buff=0.34)
        row.move_to(stage.STAGE.center + DOWN * 0.15)
        style.strip_labels(self._owned["code"])
        ctx.play(self._owned["code"].animate.scale(0.55).move_to(row.get_left() + LEFT * 0.95),
                 run_time=0.45)
        ctx.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in row], lag_ratio=0.16),
                 run_time=0.8)
        self._own("row", row)

    def b04_artifact_web(self, ctx):
        """Nine and a half seconds. One family of artifact per clause, as named."""
        anchor = self._owned["row"]
        families = [
            (style.CYAN, dot, UP * 1.5),
            (style.VIOLET, lambda c: chip(c, 0.42), UP * 0.75 + RIGHT * 3.4),
            (style.GREEN, lambda c: chip(c, 0.42), DOWN * 1.35),
            (style.GOLD, lambda c: chip(c, 0.42), DOWN * 0.85 + LEFT * 3.6),
            (style.AMBER, dot, UP * 1.35 + LEFT * 3.2),
        ]
        web = VGroup()
        for color, maker, offset in families:
            cluster = VGroup(*[maker(color) for _ in range(3)]).arrange(RIGHT, buff=0.24)
            cluster.move_to(anchor.get_center() + offset)
            links = VGroup(*[
                Line(c.get_center(), anchor.get_center(), color=color,
                     stroke_width=1.4, stroke_opacity=0.35) for c in cluster
            ])
            web.add(cluster, links)
            ctx.play(FadeIn(cluster, scale=0.8), Create(links), run_time=0.5)
            ctx.hold(0.55)
        self._own("web", web)
        # The line keeps listing artifacts after the families have landed, so the
        # web keeps thickening rather than freezing.
        for cluster_index in (0, 2, 4, 1, 3):
            group = web[cluster_index * 2]
            ctx.play(*[c.animate.set_stroke(width=3.4) for c in group], run_time=0.32)
            ctx.hold(0.3)

    def b05_stop(self, ctx):
        ctx.play(self._owned["web"].animate.set_opacity(0.45), run_time=0.5)

    def b06_lone_reviewer(self, ctx):
        rev = self._owned["review"][0]
        style.strip_labels(rev)
        ctx.play(rev.animate.scale(0.55).move_to(stage.STAGE.center + UP * 1.95),
                 self._owned["review"][1].animate.set_opacity(0.0), run_time=0.55)

    def b07_widen(self, ctx):
        ctx.clear_stage("review", run_time=0.5)

    # ------------------------------------------------------------- the flood --
    def b08_rain(self, ctx):
        rng = random.Random(7)
        flood = VGroup()
        for _ in range(34):
            c = chip(rng.choice([style.BLUE, style.CYAN, style.GREEN]), 0.3)
            c.move_to(np.array([rng.uniform(stage.STAGE.left + 0.4, stage.STAGE.right - 0.4),
                                rng.uniform(0.9, stage.STAGE.top - 0.85), 0.0]))
            flood.add(c)
        self._own("flood", flood)
        ctx.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.5) for c in flood], lag_ratio=0.02),
                 run_time=1.5)
        ctx.play(flood.animate.shift(DOWN * 1.5), run_time=0.9)

    def b09_reviewers_struck(self, ctx):
        revs = VGroup(*[style.node("review", "", size=0.62) for _ in range(4)])
        revs.arrange(RIGHT, buff=0.9)
        revs.move_to(np.array([0.0, stage.STAGE.bottom + 0.75, 0.0]))
        self._own("revs", revs)
        ctx.play(FadeIn(revs), run_time=0.4)
        ctx.play(self._owned["flood"].animate.shift(DOWN * 1.25), run_time=0.7)
        ctx.play(*[r.animate.shift(DOWN * 0.22).set_opacity(0.7) for r in revs], run_time=0.5)

    def b10_buried(self, ctx):
        rng = random.Random(11)
        pile = VGroup()
        for _ in range(26):
            c = chip(rng.choice([style.BLUE, style.CYAN, style.GREEN]), 0.3)
            c.move_to(np.array([rng.uniform(stage.STAGE.left + 0.5, stage.STAGE.right - 0.5),
                                rng.uniform(stage.STAGE.bottom + 0.25, stage.STAGE.bottom + 1.4),
                                0.0]))
            pile.add(c)
        self._own("pile", pile)
        ctx.play(LaggedStart(*[FadeIn(c) for c in pile], lag_ratio=0.03), run_time=1.1)
        ctx.play(self._owned["revs"].animate.set_opacity(0.14), run_time=0.6)

    # ------------------------------------------------ what serious software is --
    def b11_clean_slate(self, ctx):
        ctx.clear_stage(run_time=0.7)
        sq = style.node("code", "code", size=1.25)
        sq.move_to(stage.STAGE.center)
        ctx.show(sq, tag="core", anim=lambda m: FadeIn(m, scale=0.85), run_time=0.5)

    def b12_build_chain(self, ctx):
        """Thirteen point eight seconds. One node per clause the narrator names."""
        core = self._owned["core"]
        specs = [
            ("requirement", "REQ", UP * 1.55 + LEFT * 3.1),
            ("test", "TEST", UP * 1.55 + RIGHT * 3.1),
            ("source", "v4.2", DOWN * 1.55 + RIGHT * 3.1),
            ("evidence", "EVID", DOWN * 1.55 + LEFT * 3.1),
            ("review", "OK", UP * 0.0 + LEFT * 5.15),
        ]
        chain = VGroup()
        for kind, label, offset in specs:
            n = style.node(kind, label, size=1.5)
            n.move_to(core.get_center() + offset)
            edge = style.connect(n, core, color=style.NODE_KINDS[kind]["color"], width=2.6)
            chain.add(n, edge)
            ctx.play(FadeIn(n, scale=0.85), Create(edge), run_time=0.55)
            ctx.hold(0.9)
            ctx.play(*style.highlight(n, style.NODE_KINDS[kind]["color"]), run_time=0.3)
            ctx.hold(0.6)
        self._own("chain", chain)

    # -------------------------------------------------------- the two worlds --
    def b13_divide(self, ctx):
        line = DashedLine(np.array([DIVIDE_X, stage.STAGE.bottom, 0.0]),
                          np.array([DIVIDE_X, stage.STAGE.top, 0.0]),
                          color=style.GRID, stroke_width=3, dash_length=0.16)
        ctx.show(line, tag="divide", anim=lambda m: Create(m), run_time=0.5)
        whole = VGroup(self._owned["core"], self._owned["chain"])
        style.strip_labels(whole)
        ctx.play(whole.animate.scale(0.36).move_to(RIGHT_COL.center + UP * 1.45), run_time=0.9)

    def b14_web_stack(self, ctx):
        stack = VGroup(*[chip(style.BLUE, 0.62) for _ in range(3)]).arrange(DOWN, buff=0.26)
        stack.move_to(LEFT_COL.center + DOWN * 0.85)
        ctx.show(stack, tag="stack", run_time=0.5)

    def b15_revenue(self, ctx):
        axes_w, axes_h = 3.0, 1.15
        base = LEFT_COL.center + UP * 1.55
        curve = VMobject(color=style.GREEN, stroke_width=4)
        curve.set_points_as_corners([
            base + np.array([-axes_w / 2, -axes_h / 2, 0]),
            base + np.array([-axes_w / 6, -axes_h / 6, 0]),
            base + np.array([axes_w / 6, axes_h / 8, 0]),
            base + np.array([axes_w / 2, axes_h / 2, 0]),
        ])
        tag = style.label_text("customers", color=style.MUTED, size="tiny")
        tag.next_to(curve, UP, buff=0.16)
        ctx.show(curve, tag="revenue", anim=lambda m: Create(m), run_time=0.6)
        ctx.show(tag, tag="revenue_tag", run_time=0.3)

    def b16_break_fix(self, ctx):
        mid = self._owned["stack"][1]
        ctx.play(mid[0].animate.set_stroke(style.RED, width=3.2), run_time=0.4)
        ctx.hold(0.7)
        ctx.play(mid[0].animate.set_stroke(style.CYAN, width=2.4), run_time=0.4)
        ctx.play(self._owned["revenue"].animate.set_stroke(style.GREEN, width=5), run_time=0.35)

    def b17_focus_right(self, ctx):
        left = VGroup(self._owned["stack"], self._owned["revenue"],
                      self._owned["revenue_tag"])
        ctx.play(left.animate.set_opacity(0.42), run_time=0.5)
        ctx.play(*style.highlight(self._owned["core"], style.GOLD), run_time=0.45)

    def b18_second_chain(self, ctx):
        block = VGroup(self._owned["core"], self._owned["chain"])
        # Space the three rows from the block's measured height, so they cannot
        # overlap however the chain above is later restyled.
        self._row_gap = block.height + 0.34
        # Move the first chain up and bring the second in on the same breath.
        # Doing it in two steps left the stage holding one small graph in the
        # top corner with the rest of the frame empty, for seven seconds.
        ctx.play(block.animate.move_to(RIGHT_COL.center + UP * self._row_gap), run_time=0.45)
        second = block.copy().set_opacity(0.85)
        for sub in second.get_family():
            if getattr(sub, "text", None):
                sub.set_opacity(0)   # set_opacity on the copy revived the labels
        # Work out the room for three rows *before* anything is shown. Arriving
        # at full size and shrinking afterwards put the stack in the title lane
        # for most of a second — a defect the viewer sees and the fix is simply
        # to compute first and animate once.
        needed = 3 * self._row_gap + 0.9
        if needed > stage.STAGE.height:
            k = stage.STAGE.height / needed
            self._row_gap *= k
            block = VGroup(self._owned["core"], self._owned["chain"])
            second.scale(k)
            ctx.play(block.animate.scale(k).move_to(RIGHT_COL.center + UP * self._row_gap),
                     run_time=0.45)
        second.move_to(RIGHT_COL.center)
        ctx.show(second, tag="chain2", anim=lambda m: FadeIn(m, shift=UP * 0.2), run_time=0.5)

    def b19_third_chain(self, ctx):
        third = self._owned["chain2"].copy()
        third.move_to(RIGHT_COL.center + DOWN * self._row_gap)
        ctx.show(third, tag="chain3", anim=lambda m: FadeIn(m, shift=UP * 0.2), run_time=0.55)
        # The stack plus the seal drawn round it in the next beat must clear the
        # title lane, so shrink the whole block to the room actually available.
        block = VGroup(self._owned["core"], self._owned["chain"],
                       self._owned["chain2"], self._owned["chain3"])
        room = (stage.STAGE.height - 0.9) / max(block.height, 1e-6)
        if room < 1.0:
            ctx.play(block.animate.scale(room).move_to(RIGHT_COL.center), run_time=0.5)

    def b20_seal(self, ctx):
        """Nine seconds: the perimeter draws, then who is accountable for it."""
        block = VGroup(self._owned["core"], self._owned["chain"],
                       self._owned["chain2"], self._owned["chain3"])
        seal = SurroundingRectangle(block, color=style.GOLD, stroke_width=3.5, buff=0.3)
        ctx.show(seal, tag="seal", anim=lambda m: Create(m), run_time=1.1)
        ctx.hold(0.9)
        label = style.label_text("signed off before it runs", color=style.GOLD, size="tiny")
        label.next_to(seal, DOWN, buff=0.3)
        ctx.show(label, tag="seal_label", run_time=0.5)
        ctx.hold(0.8)
        ctx.play(seal.animate.set_stroke(style.GOLD, width=5), run_time=0.6)
        ctx.hold(0.5)
        # All three at once, and they stay. Cycling them gave each about a
        # second, which is a third of the time it takes to read one — and they
        # are a list of who is accountable, not three successive answers.
        # One at a time, each held long enough to read. The stack and the row
        # both fight the seal for space; the cycle does not, and the line is nine
        # seconds long, which is room for three labels at reading speed.
        for word in ("an organization", "a process", "a regulator"):
            stamp = style.label_text(word, color=style.GOLD, size="tiny")
            # Above the seal, not below the label: below the label is the caption
            # lane, and only one thing is allowed in there at a time.
            stamp.next_to(seal, UP, buff=0.22)
            ctx.play(FadeIn(stamp, shift=UP * 0.1), run_time=0.3)
            ctx.hold(2.0)
            ctx.play(FadeOut(stamp), run_time=0.25)

    # --------------------------------------------------------- the bottleneck --
    def b21_bounce(self, ctx):
        ctx.lopsided("the flood piles on the left and cannot cross — the lopsidedness is the point")
        rng = random.Random(3)
        stream = VGroup()
        for i in range(7):
            c = chip(style.CYAN, 0.34)
            c.move_to(np.array([stage.STAGE.left + 0.4,
                                rng.uniform(stage.STAGE.bottom + 0.6, stage.STAGE.top - 0.6), 0.0]))
            stream.add(c)
        self._own("stream", stream)
        ctx.play(LaggedStart(*[FadeIn(c) for c in stream], lag_ratio=0.06), run_time=0.5)
        ctx.play(*[c.animate.shift(RIGHT * (DIVIDE_X - 0.55 - c.get_center()[0]))
                   for c in stream], run_time=0.9)
        ctx.play(self._owned["divide"].animate.set_stroke(style.RED, width=4), run_time=0.4)

    def b22_identical(self, ctx):
        probe = self._owned["stream"][3]
        ctx.play(probe[0].animate.set_stroke(style.CYAN, width=4).scale(1.2), run_time=0.4)
        tag = style.label_text("same code", color=style.MUTED, size="tiny")
        tag.next_to(probe, LEFT, buff=0.22)
        ctx.show(tag, tag="same", run_time=0.35)

    def b23_pressure(self, ctx):
        ctx.lopsided("pressure builds on one side of the divide")
        ctx.retire("same", run_time=0.25)
        ctx.play(self._owned["seal"].animate.set_stroke(style.RED, width=5), run_time=0.5)
        ctx.play(*[c.animate.shift(RIGHT * 0.18) for c in self._owned["stream"]], run_time=0.5)

    def b24_pile_up(self, ctx):
        ctx.lopsided("the left overflows while the right stays fixed — deliberately unequal")
        rng = random.Random(23)
        more = VGroup()
        for _ in range(22):
            c = chip(style.CYAN, 0.3)
            c.move_to(np.array([rng.uniform(stage.STAGE.left + 0.4, DIVIDE_X - 0.5),
                                rng.uniform(stage.STAGE.bottom + 0.4, stage.STAGE.top - 0.35), 0.0]))
            more.add(c)
        self._own("more", more)
        ctx.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in more], lag_ratio=0.03),
                 run_time=1.2)

    def b25_static(self, ctx):
        ctx.lopsided("the contrast between a full left and an unmoved right is the claim")
        ctx.play(self._owned["seal"].animate.set_stroke(style.GOLD, width=5), run_time=0.5)
        ctx.hold(0.5)
        ctx.play(self._owned["divide"].animate.set_stroke(style.RED, width=6), run_time=0.5)

    def b26_push_in(self, ctx):
        keep = VGroup(self._owned["divide"], self._owned["more"], self._owned["stream"])
        ctx.play(FadeOut(self._owned["seal"]), FadeOut(self._owned["seal_label"]),
                 FadeOut(self._owned["chain2"]), FadeOut(self._owned["chain3"]),
                 FadeOut(self._owned["stack"]), FadeOut(self._owned["revenue"]),
                 FadeOut(self._owned["revenue_tag"]),
                 run_time=0.6)
        for tag in ("seal", "seal_label", "chain2", "chain3", "stack",
                    "revenue", "revenue_tag"):
            self._owned.pop(tag, None)
        ctx.play(keep.animate.scale(1.06), run_time=0.5)

    def b27_not_editor(self, ctx):
        ctx.play(*[c[0].animate.set_stroke(style.CYAN, width=3.4)
                   for c in self._owned["more"][:8]], run_time=0.45)

    def b28_not_model(self, ctx):
        ctx.play(*[c[0].animate.set_stroke(style.VIOLET, width=3.4)
                   for c in self._owned["more"][8:16]], run_time=0.45)

    def b29_trust(self, ctx):
        gate = style.node("review", "", size=1.5)
        gate.move_to(np.array([DIVIDE_X, stage.STAGE.center[1], 0.0]))
        ctx.show(gate, tag="gate", anim=lambda m: FadeIn(m, scale=1.4), run_time=0.45)

    # ------------------------------------------------------------ the answer --
    def b30_compiler(self, ctx):
        ctx.clear_stage("gate", run_time=0.7)
        frame = RoundedRectangle(corner_radius=0.12, width=5.2, height=2.9,
                                 color=style.VIOLET, stroke_width=3)
        frame.move_to(stage.STAGE.center)
        gate = self._owned["gate"]
        ctx.play(gate.animate.move_to(frame.get_right()), Create(frame), run_time=0.8)
        name = style.label_text("Verification Compiler", color=style.VIOLET)
        name.next_to(frame, UP, buff=0.3)
        ctx.show(name, tag="name", run_time=0.5)
        self._own("frame", frame)

    def b31_frame_turns(self, ctx):
        ctx.play(self._owned["frame"].animate.set_stroke(style.VIOLET, width=5), run_time=0.5)
        ctx.hold(0.4)
        ctx.play(self._owned["frame"].animate.set_stroke(style.VIOLET, width=3), run_time=0.5)

    def b32_fold(self, ctx):
        """Scaffolding snaps around one unit of code, then folds into a package."""
        frame = self._owned["frame"]
        unit = style.node("code", "code", size=0.85)
        unit.move_to(frame.get_center() + LEFT * 0.55)
        ctx.play(FadeIn(unit, shift=RIGHT * 0.6), run_time=0.5)
        scaffold = VGroup()
        for kind, offset in (("requirement", UP * 1.25), ("test", RIGHT * 1.7),
                             ("evidence", DOWN * 1.25), ("source", LEFT * 1.7)):
            n = style.node(kind, "", size=0.6)
            n.move_to(unit.get_center() + offset)
            scaffold.add(n)
            ctx.play(FadeIn(n, scale=0.7), run_time=0.28)
            ctx.hold(0.32)
        ctx.hold(0.5)
        # Draw the scaffolding closing around the unit before it folds, so the
        # nine-second line keeps moving instead of resolving in the first four
        # and holding a frozen packet for the rest.
        # Plain lines, not connectors: an arrowhead aimed at a node this small
        # lands inside its label, which is the arrow_into_label defect.
        joins = VGroup(*[Line(n.get_center(), unit.get_center(),
                              color=style.DIM, stroke_width=2.0)
                         for n in scaffold])
        ctx.play(LaggedStart(*[Create(j) for j in joins], lag_ratio=0.18), run_time=0.7)
        ctx.hold(0.4)
        packet = style.node("vqp", "VQP", size=1.5)
        packet.move_to(frame.get_center())
        ctx.play(ReplacementTransform(VGroup(unit, scaffold, joins), packet), run_time=0.9)
        self._own("packet", packet)
        ctx.play(*style.highlight(packet, style.GREEN), run_time=0.4)
        ctx.hold(0.5)
        ctx.play(*style.restroke(packet, style.GREEN, 2.6), run_time=0.4)

    def b33_through_gate(self, ctx):
        gate = self._owned["gate"]
        ctx.play(self._owned["packet"].animate.next_to(gate, LEFT, buff=0.28), run_time=0.7)
        ctx.play(*style.highlight(gate, style.GOLD), run_time=0.4)

    def b34_beat(self, ctx):
        ctx.retire("packet", "name", run_time=0.4)
        ctx.retire("frame", "gate", run_time=0.35)
        final = style.title_text("a compiler for trust")
        final.move_to(stage.STAGE.center)
        ctx.show(final, tag="final", anim=lambda m: FadeIn(m, scale=0.92), run_time=0.55)

    def b35_title(self, ctx):
        # The closing words are already up — this line lands on them rather than
        # introducing them. Introduced here they had 1.3 seconds before the
        # section ended, which is half the time it takes to read them.
        ctx.play(self._owned["final"].animate.scale(1.06), run_time=0.5)
