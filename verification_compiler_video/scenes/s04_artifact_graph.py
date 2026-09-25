"""
Section 04 — Artifacts Become A Graph. **3D.**

This is the one idea in the video that genuinely wants depth. A project is not a
flat diagram; it is a layered structure — requirements above, code in the middle,
evidence below — and a camera move through it says "this is one connected object"
faster than any amount of narration.

Every label is pinned to the camera frame so it stays upright and readable as the
camera swings. Geometry is recorded through the camera projection, so the same
overlap, clipping and contrast checks apply here as anywhere else.
"""
from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from verification_compiler_video.pipeline import camera3d, stage, style
from verification_compiler_video.pipeline.beats import Beat
from verification_compiler_video.pipeline.camera3d import Beat3DScene

# Depth planes. Requirements sit above the code they govern; evidence below it.
Z_REQ, Z_CODE, Z_EVID = 1.55, 0.0, -1.55


class S04ArtifactGraph(Beat3DScene):
    section_id = "04_artifact_graph"
    title = ""            # the 3D camera owns the frame; no fixed title bar
    timing_dir = Path(__file__).resolve().parents[1] / "out" / "timing"
    initial_phi = 0
    initial_theta = -90

    def storyboard(self) -> list[Beat]:
        return [
            Beat("The first move is to stop thinking of a project as a folder", self.b00_folder),
            Beat("For verification, a project is a graph", self.b01_tilt),
            Beat("Every important thing becomes a node", self.b02_first_node),
            Beat("Requirements", self.b03_requirements),
            Beat("Source code units", self.b04_code),
            Beat("Tests", self.b05_tests),
            Beat("Test results", self.b06_results),
            Beat("Static analysis results", self.b07_static),
            Beat("Datasheets", self.b08_datasheets),
            Beat("Interface control documents", self.b09_icd),
            Beat("Physical test records", self.b10_physical),
            Beat("Model review outputs", self.b11_model_review),
            Beat("Human review outputs", self.b12_human_review),
            Beat("Even specific sections of source documents become nodes", self.b13_regions,
                 note="9s line — the document splits into addressable regions"),
            Beat("Then the relationships become edges", self.b14_edges),
            Beat("This requirement traces to that code", self.b15_traces),
            Beat("This test verifies that behavior", self.b16_verifies),
            Beat("This result was produced against this version", self.b17_version),
            Beat("This source region supports this claim", self.b18_supports),
            Beat("Now the project has a shape", self.b19_orbit),
            Beat("And once it has a shape, you can ask structural questions", self.b20_questions),
            Beat("Is there code with no requirement", self.b21_orphan_code),
            Beat("Is there a requirement with no implementation", self.b22_orphan_req),
            Beat("Is there a test result tied to an old version", self.b23_stale),
            Beat("Is there a model review that disagrees with a human review", self.b24_disagree),
            Beat("Those are not philosophical questions anymore", self.b25_settle),
            Beat("They are graph questions", self.b26_close),
        ]

    # --------------------------------------------------------------- helpers --
    def place(self, kind: str, x: float, z: float, size: float = 0.85,
              y: float = 0.0) -> VGroup:
        """A node standing upright on its depth plane, facing the camera."""
        n = style.node(kind, "", size=size)
        n.rotate(PI / 2, axis=RIGHT)
        n.move_to(np.array([x, y, z]))
        return n

    def caption3d(self, text: str, color: str = style.WHITE):
        """A caption pinned flat to the frame, in the reserved caption lane."""
        cap = style.caption_text(text, color=color)
        stage.fit(cap, stage.CAPTION)
        cap.set_opacity(0)
        self.pin(cap)
        return cap

    # ----------------------------------------------------------------- beats --
    def b00_folder(self, ctx):
        files = VGroup(*[
            Rectangle(width=1.5, height=0.34, color=style.MUTED, stroke_width=2)
            .set_fill(style.PANEL, opacity=0.95)
            for _ in range(6)
        ]).arrange(DOWN, buff=0.19)
        files.rotate(PI / 2, axis=RIGHT)
        files.move_to(ORIGIN)
        ctx.show(files, tag="files", anim=lambda m: FadeIn(m, shift=UP * 0.3), run_time=0.8)
        cap = self.caption3d("a folder full of files")
        ctx.play(cap.animate.set_opacity(1), run_time=0.4)
        self._own("cap", cap)
        # Five and a half seconds on this line. Let the flat stack of files read
        # as flat — a slow drift across it — before the next beat tilts the
        # world and shows there was structure hiding in it all along.
        self.move_camera(phi=74 * DEGREES, theta=-96 * DEGREES,
                         run_time=max(ctx.window - 1.9, 0.8))

    def b01_tilt(self, ctx):
        ctx.retire("files", run_time=0.4)
        ctx.play(self._owned["cap"].animate.set_opacity(0), run_time=0.25)
        self.move_camera(phi=66 * DEGREES, theta=-88 * DEGREES, zoom=0.82,
                         run_time=min(ctx.window - 0.2, 1.4))

    def b02_first_node(self, ctx):
        # Faint planes at each depth. Without them the tiers read as a diagonal
        # scatter rather than requirements-above-code-above-evidence.
        planes = VGroup()
        for z, colour in ((Z_REQ, style.GOLD), (Z_CODE, style.BLUE), (Z_EVID, style.GREEN)):
            plane = Rectangle(width=11.4, height=2.6, color=colour,
                              stroke_width=1.2, stroke_opacity=0.30)
            plane.set_fill(colour, opacity=0.035)
            plane.rotate(PI / 2, axis=RIGHT).move_to(np.array([0.0, 0.0, z]))
            planes.add(plane)
        ctx.show(planes, tag="planes", run_time=0.5)
        n = self.place("code", 0.0, Z_CODE, size=1.0)
        ctx.show(n, tag="seed", anim=lambda m: FadeIn(m, scale=0.8), run_time=0.45)

    def _family(self, ctx, tag: str, kind: str, xs: list[float], z: float,
                run_time: float = 0.4, ys: list[float] | None = None):
        ys = ys or [0.0] * len(xs)
        group = VGroup(*[self.place(kind, x, z, y=y) for x, y in zip(xs, ys)])
        ctx.show(group, tag=tag, anim=lambda m: FadeIn(m, scale=0.75), run_time=run_time)
        return group

    def b03_requirements(self, ctx):
        # Four, not three. The last one is deliberately never implemented — the
        # narration later asks "is there a requirement with no implementation?"
        # and the graph has to be able to answer it. Ringing a requirement that
        # visibly *has* an implementation edge says the opposite of the line.
        self._family(ctx, "reqs", "requirement", [-3.6, -1.8, 0.4, 2.2], Z_REQ, 0.4,
                     ys=[-1.2, 0.4, -0.6, 1.3])

    def b04_code(self, ctx):
        # Likewise: the third code unit has no requirement above it, so "is there
        # code with no requirement?" has something true to point at.
        self._family(ctx, "code", "code", [-2.6, 1.6, 4.4], Z_CODE, 0.35,
                     ys=[0.9, -1.0, 0.5])

    def b05_tests(self, ctx):
        self._family(ctx, "tests", "test", [-3.1, -0.9], Z_EVID, 0.3, ys=[-0.8, 0.7])

    def b06_results(self, ctx):
        self._family(ctx, "results", "evidence", [1.1], Z_EVID, 0.3)

    def b07_static(self, ctx):
        self._family(ctx, "static", "evidence", [3.1], Z_EVID, 0.3)

    def b08_datasheets(self, ctx):
        self._family(ctx, "sheets", "source", [5.5], Z_REQ, 0.3, ys=[-1.8])

    def b09_icd(self, ctx):
        self._family(ctx, "icd", "source", [3.4], Z_REQ, 0.3, ys=[0.9])

    def b10_physical(self, ctx):
        self._family(ctx, "physical", "evidence", [4.85], Z_EVID, 0.3)

    def b11_model_review(self, ctx):
        self._family(ctx, "mrev", "review", [-4.2], Z_EVID, 0.3)

    def b12_human_review(self, ctx):
        self._family(ctx, "hrev", "review", [-4.2], Z_REQ, 0.3)

    def b13_regions(self, ctx):
        """Nine seconds: one document splits into separately addressable slices."""
        doc = self._owned["icd"][0]
        ctx.play(*style.highlight(doc, style.VIOLET), run_time=0.4)
        ctx.hold(0.6)
        slices = VGroup()
        for i in range(4):
            s = Rectangle(width=0.62, height=0.16, color=style.VIOLET, stroke_width=2)
            s.set_fill(style.PANEL, opacity=0.95)
            s.rotate(PI / 2, axis=RIGHT)
            s.move_to(doc.get_center() + np.array([0.0, 0.0, 0.42 - i * 0.28]))
            slices.add(s)
            ctx.play(FadeIn(s, scale=0.7), run_time=0.3)
            ctx.hold(0.55)
        self._own("slices", slices)
        cap = self.caption3d("§4.2, lines 88-114 — not “see the standard”", style.VIOLET)
        ctx.play(cap.animate.set_opacity(1), run_time=0.45)
        self._own("cap2", cap)
        # Thirty-six characters. It was up for a second and a quarter, which is
        # about a third of the time it takes to read — and it is the concrete
        # detail the whole beat exists to deliver.
        ctx.hold(4.9)
        ctx.play(cap.animate.set_opacity(0), run_time=0.4)
        # Nine seconds. Drift in on the sliced document so the point — that a
        # citation addresses a region, not a file — stays in motion to the end
        # of the line.
        self.move_camera(phi=62 * DEGREES, theta=-84 * DEGREES,
                         run_time=max(ctx.window - 10.5, 0.6))

    def _edge(self, a, b, color, tag):
        # edge3d, not a bare Line3D: a bare line carries no layer and is drawn in
        # front of the nodes it joins until something else arrives, at which
        # point it drops behind them. That is the blink at 04 b16.
        line = camera3d.edge3d(a, b, color=color, width=2.3)
        self._own(tag, line)
        return line

    def b14_edges(self, ctx):
        e = self._edge(self._owned["reqs"][0], self._owned["code"][0], style.GOLD, "e0")
        ctx.play(Create(e), run_time=0.5)

    def b15_traces(self, ctx):
        e = self._edge(self._owned["reqs"][1], self._owned["seed"], style.GOLD, "e1")
        e2 = self._edge(self._owned["reqs"][2], self._owned["code"][1], style.GOLD, "e2")
        ctx.play(Create(e), Create(e2), run_time=0.55)

    def b16_verifies(self, ctx):
        e = self._edge(self._owned["seed"], self._owned["tests"][1], style.CYAN, "e3")
        e2 = self._edge(self._owned["code"][0], self._owned["tests"][0], style.CYAN, "e4")
        ctx.play(Create(e), Create(e2), run_time=0.55)

    def b17_version(self, ctx):
        e = self._edge(self._owned["tests"][1], self._owned["results"][0], style.GREEN, "e5")
        ctx.play(Create(e), run_time=0.45)
        cap = self.caption3d("tied to git a1b2c3", style.GREEN)
        ctx.play(cap.animate.set_opacity(1), run_time=0.35)
        self._own("cap3", cap)

    def b18_supports(self, ctx):
        ctx.play(self._owned["cap3"].animate.set_opacity(0), run_time=0.25)
        e = self._edge(self._owned["icd"][0], self._owned["code"][1], style.VIOLET, "e6")
        ctx.play(Create(e), run_time=0.5)

    def b19_orbit(self, ctx):
        # Spend the whole window on the move. A camera that arrives early leaves
        # the graph parked in a fixed view for the rest of the line, which is
        # the one thing a 3D scene should never do.
        self.move_camera(theta=-108 * DEGREES, phi=58 * DEGREES, zoom=0.82,
                         run_time=max(ctx.window - 0.15, 0.6))

    def b20_questions(self, ctx):
        cap = self.caption3d("structural questions", style.GOLD)
        ctx.play(cap.animate.set_opacity(1), run_time=0.4)
        self._own("cap4", cap)
        # Settle into the reading angle across the rest of the line rather than
        # holding the previous framing for four seconds.
        self.move_camera(phi=56 * DEGREES, theta=-96 * DEGREES, zoom=0.9,
                         run_time=max(ctx.window - 0.9, 0.6))

    def _flag(self, ctx, node, colour, tag, clear: str | None = None):
        """
        Ring the node this question is about — and only that one.

        The rings used to accumulate, so by the fourth question five of them were
        lit at once and the frame no longer said which node the narrator was
        asking about. One question, one ring.
        """
        if clear:
            ctx.retire(clear, run_time=0.2)
        ring = style.cursor_for(node, color=colour, width=5.0, pad=0.16)
        ring.rotate(PI / 2, axis=RIGHT).move_to(node.get_center())
        ctx.show(ring, tag=tag, anim=lambda m: Create(m), run_time=0.35)

    def b21_orphan_code(self, ctx):
        ctx.play(self._owned["cap4"].animate.set_opacity(0), run_time=0.2)
        self._flag(ctx, self._owned["code"][2], style.RED, "f1")

    def b22_orphan_req(self, ctx):
        self._flag(ctx, self._owned["reqs"][3], style.RED, "f2", clear="f1")

    def b23_stale(self, ctx):
        self._flag(ctx, self._owned["results"][0], style.AMBER, "f3", clear="f2")

    def b24_disagree(self, ctx):
        self._flag(ctx, self._owned["mrev"][0], style.VIOLET, "f4", clear="f3")
        self._flag(ctx, self._owned["hrev"][0], style.VIOLET, "f5")
        # The two reviews argue with each other for the rest of the line, rather
        # than the frame freezing once both rings are drawn.
        link = Line3D(self._owned["mrev"][0].get_center(),
                      self._owned["hrev"][0].get_center(),
                      color=style.VIOLET, thickness=0.012)
        ctx.show(link, tag="argue", anim=lambda m: Create(m), run_time=0.5)
        for _ in range(2):
            ctx.play(*style.highlight(self._owned["mrev"][0], style.RED), run_time=0.3)
            ctx.play(*style.highlight(self._owned["hrev"][0], style.GOLD), run_time=0.3)

    def b25_settle(self, ctx):
        self.move_camera(phi=70 * DEGREES, theta=-90 * DEGREES, zoom=0.86,
                         run_time=max(ctx.window - 1.4, 0.6))
        # The closing words land here, not on the last line: the last line has
        # 1.7 seconds before the section ends, and two words still need two and a
        # half to be read.
        cap = self.caption3d("graph questions", style.WHITE)
        ctx.play(cap.animate.set_opacity(1), run_time=0.45)
        self._own("cap5", cap)

    def b26_close(self, ctx):
        ctx.play(self._owned["cap5"].animate.scale(1.12), run_time=0.5)
