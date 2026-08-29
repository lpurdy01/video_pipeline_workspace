"""
Section 05 — Compilation Means Traversal.

The analogy section. A familiar compiler runs along the top; the verification
compiler is built underneath it, step for step, so the viewer gets the shape for
free. Then a traversal walk fills a package one artifact at a time — one beat per
"Collect the …" line, which is what those short lines are for.
"""
from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from verification_compiler_video.pipeline import stage, style
from verification_compiler_video.pipeline.beats import Beat, BeatScene

TOP_Y, BOT_Y = 1.35, -1.55


class S05CompilationTraversal(BeatScene):
    section_id = "05_compilation_traversal"
    title = "Compilation means traversal"
    timing_dir = Path(__file__).resolve().parents[1] / "out" / "timing"

    def storyboard(self) -> list[Beat]:
        return [
            Beat("This is where the compiler analogy starts to matter", self.b00_open),
            Beat("A normal compiler takes source code, walks a structured", self.b01_gcc,
                 note="6.1s — parse, walk, emit arrive as the narrator names them"),
            Beat("It turns one representation into another representation", self.b02_transform),
            Beat("A Verification Compiler would not compile code into a binary", self.b03_not_binary),
            Beat("It would compile an artifact graph into verification work", self.b04_vc_row),
            Beat("Start with a top-level requirement", self.b05_start),
            Beat("Traverse the graph", self.b06_walk),
            Beat("Collect the code units that matter", self.b07_code),
            Beat("Collect the linked requirements", self.b08_reqs),
            Beat("Collect the tests", self.b09_tests),
            Beat("Collect the results", self.b10_results),
            Beat("Collect the relevant source text", self.b11_source),
            Beat("Collect the static analysis output", self.b12_static),
            Beat("Then assemble that into a bounded review package", self.b13_assemble),
            Beat("Same graph state", self.b14_same_state),
            Beat("Same traversal rule", self.b15_same_rule),
            Beat("Same package", self.b16_same_package),
            Beat("That deterministic assembly is the point", self.b17_determinism),
            Beat("The model might be probabilistic", self.b18_probabilistic),
            Beat("The human might be inconsistent", self.b19_inconsistent),
            Beat("But the package they receive should not be a vibe", self.b20_not_vibe),
            Beat("It should be a reproducible artifact", self.b21_reproducible),
        ]

    # ------------------------------------------------------- the known case --
    def b00_open(self, ctx):
        src = style.node("code", "limiter.c", size=1.6)
        src.move_to(np.array([-4.9, TOP_Y, 0.0]))
        ctx.show(src, tag="src", anim=lambda m: FadeIn(m, shift=RIGHT * 0.2), run_time=0.5)

    def b01_gcc(self, ctx):
        steps = ["parse", "walk", "emit"]
        xs = [-2.0, 0.7, 3.4]
        made = VGroup()
        prev = self._owned["src"]
        for name, x in zip(steps, xs):
            n = style.node("source", name, size=1.5)
            n.move_to(np.array([x, TOP_Y, 0.0]))
            edge = style.connect(prev, n, style.MUTED, width=2.4)
            made.add(n, edge)
            ctx.play(FadeIn(n, scale=0.85), Create(edge), run_time=0.45)
            ctx.hold(0.75)
            prev = n
        self._own("gcc", made)
        out = style.node("evidence", "limiter.o", size=1.6)
        out.move_to(np.array([5.6, TOP_Y, 0.0]))
        ctx.show(out, tag="obj", run_time=0.4)
        ctx.show(style.connect(prev, out, style.GREEN, width=2.4), tag="objedge",
                 anim=lambda m: Create(m), run_time=0.3)

    def b02_transform(self, ctx):
        tag = style.label_text("one representation into another",
                               color=style.MUTED, size="tiny")
        tag.move_to(np.array([0.0, TOP_Y - 1.15, 0.0]))
        ctx.show(tag, tag="transform", run_time=0.4)
        # Six seconds on this line. Walk the transformation the words describe —
        # source, then the process, then the output — instead of lighting the
        # end of it once and holding a frozen frame for five.
        for tagname, colour in (("src", style.VIOLET), ("gcc", style.CYAN),
                                ("obj", style.GREEN)):
            ctx.play(*style.highlight(self._owned[tagname], colour), run_time=0.4)
            ctx.hold(0.35)
        ctx.play(*style.restroke(self._owned["obj"], style.GREEN, 4.2), run_time=0.4)
        ctx.hold(0.4)
        ctx.play(*style.restroke(self._owned["obj"], style.GREEN, 2.6), run_time=0.4)

    # -------------------------------------------------- the proposed case --
    def b03_not_binary(self, ctx):
        ctx.retire("transform", run_time=0.25)
        ctx.play(VGroup(self._owned["src"], self._owned["gcc"], self._owned["obj"],
                        self._owned["objedge"]).animate.set_opacity(0.32), run_time=0.5)
        cross = VGroup(
            Line(UL * 0.3, DR * 0.3, color=style.RED, stroke_width=5),
            Line(UR * 0.3, DL * 0.3, color=style.RED, stroke_width=5),
        ).move_to(self._owned["obj"])
        ctx.show(cross, tag="cross", anim=lambda m: Create(m), run_time=0.4)

    def b04_vc_row(self, ctx):
        ctx.retire("cross", run_time=0.25)
        graph = style.node("source", "graph", size=1.7)
        graph.move_to(np.array([-4.4, BOT_Y, 0.0]))
        trav = style.node("code", "traversal", size=1.8)
        trav.move_to(np.array([-0.4, BOT_Y, 0.0]))
        ctx.show(graph, tag="graph", anim=lambda m: FadeIn(m, shift=UP * 0.2), run_time=0.45)
        ctx.show(trav, tag="trav", anim=lambda m: FadeIn(m, shift=UP * 0.2), run_time=0.45)
        ctx.show(style.connect(graph, trav, style.CYAN), tag="ge",
                 anim=lambda m: Create(m), run_time=0.3)

    # ------------------------------------------------------------ the walk --
    def b05_start(self, ctx):
        packet = RoundedRectangle(corner_radius=0.1, width=3.5, height=3.3,
                                  color=style.GREEN, stroke_width=2.6)
        packet.set_fill(style.PANEL, opacity=0.97)
        packet.move_to(np.array([4.6, 0.15, 0.0]))
        head = style.label_text("package", color=style.GREEN, size="tiny")
        head.next_to(packet.get_top(), DOWN, buff=0.16)
        ctx.show(packet, tag="packet", run_time=0.45)
        ctx.show(head, tag="packhead", run_time=0.3)
        self._slot = 0
        cursor = style.cursor_for(self._owned["graph"])
        ctx.show(cursor, tag="cursor", anim=lambda m: Create(m), run_time=0.35)

    def _collect(self, ctx, label: str, colour: str):
        row = style.mono_text(f"+ {label}", color=colour, size="tiny")
        row.move_to(self._owned["packet"].get_center()
                    + UP * (0.82 - self._slot * 0.42) + LEFT * 0.15)
        row.align_to(np.array([self._owned["packet"].get_left()[0] + 0.28, 0, 0]), LEFT)
        self._slot += 1
        self._owned["cursor"].become(style.cursor_for(self._owned["trav"]))
        ctx.play(self._owned["cursor"].animate.move_to(self._owned["trav"].get_center()),
                 run_time=0.18)
        ctx.play(FadeIn(row, shift=RIGHT * 0.15), run_time=0.22)
        self._own(f"row{self._slot}", row)

    def b06_walk(self, ctx):
        self._owned["cursor"].become(style.cursor_for(self._owned["trav"]))
        ctx.play(self._owned["cursor"].animate.move_to(self._owned["trav"].get_center()),
                 run_time=0.4)

    def b07_code(self, ctx):
        self._collect(ctx, "code unit", style.BLUE)

    def b08_reqs(self, ctx):
        self._collect(ctx, "requirements", style.GOLD)

    def b09_tests(self, ctx):
        self._collect(ctx, "tests", style.CYAN)

    def b10_results(self, ctx):
        self._collect(ctx, "results", style.GREEN)

    def b11_source(self, ctx):
        self._collect(ctx, "source region", style.VIOLET)

    def b12_static(self, ctx):
        self._collect(ctx, "static analysis", style.AMBER)

    def b13_assemble(self, ctx):
        ctx.retire("cursor", run_time=0.25)
        ctx.play(self._owned["packet"].animate.set_stroke(style.GREEN, width=5),
                 run_time=0.5)
        tag = style.label_text("bounded", color=style.GREEN, size="tiny")
        tag.next_to(self._owned["packet"], DOWN, buff=0.22)
        ctx.show(tag, tag="bounded", run_time=0.35)

    # ---------------------------------------------------------- determinism --
    def b14_same_state(self, ctx):
        ctx.play(*style.highlight(self._owned["graph"], style.CYAN), run_time=0.35)

    def b15_same_rule(self, ctx):
        ctx.play(*style.highlight(self._owned["trav"], style.CYAN), run_time=0.35)

    def b16_same_package(self, ctx):
        ctx.play(self._owned["packet"].animate.set_stroke(style.CYAN, width=5), run_time=0.3)

    def b17_determinism(self, ctx):
        tag = style.label_text("same graph → same package", color=style.CYAN)
        # Bottom + 0.35 is inside the row of nodes below; the reserved caption
        # lane is the one strip nothing else is allowed to occupy.
        stage.fit(tag, stage.CAPTION)
        ctx.show(tag, tag="det", run_time=0.45)
        ctx.hold(0.5)
        ctx.play(self._owned["packet"].animate.set_stroke(style.GREEN, width=4), run_time=0.4)

    def b18_probabilistic(self, ctx):
        ctx.retire("det", run_time=0.2)
        # Retire the traversal row rather than shifting it up. Shifted, it landed
        # on top of the reviewers that arrive next and the lower half of the
        # frame became a pile — and the argument has moved on from how the walk
        # works to who reviews the result.
        ctx.retire("graph", "trav", "ge", run_time=0.4)
        m = style.node("review", "model", size=1.5)
        m.move_to(np.array([-4.4, stage.STAGE.bottom + 0.95, 0.0]))
        ctx.show(m, tag="model", run_time=0.4)
        ctx.play(*style.highlight(m, style.AMBER), run_time=0.3)

    def b19_inconsistent(self, ctx):
        h = style.node("review", "human", size=1.5)
        h.move_to(np.array([-1.2, stage.STAGE.bottom + 0.95, 0.0]))
        ctx.show(h, tag="human", run_time=0.4)
        ctx.play(*style.highlight(h, style.AMBER), run_time=0.3)

    def b20_not_vibe(self, ctx):
        ctx.play(*style.highlight(self._owned["packet"], style.GREEN), run_time=0.4)
        ctx.hold(0.5)
        ctx.play(self._owned["model"].animate.set_opacity(0.4),
                 self._owned["human"].animate.set_opacity(0.4), run_time=0.4)

    def b21_reproducible(self, ctx):
        tag = style.label_text("reproducible", color=style.GREEN)
        stage.fit(tag, stage.CAPTION)
        ctx.show(tag, tag="repro", run_time=0.45)
