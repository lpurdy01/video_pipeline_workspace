"""
Section 06 — The Verification Query Package. **3D.**

The payoff scene. Scaffolding assembles around one code unit and then folds, in
depth, into a single packet — which is the moment the whole idea becomes an
object you could hold. Doing that fold flat robs it of the thing that makes it
read as a fold.

Also carries the multimedia point from the 2026-08-24 commentary: a package is
not necessarily text.
"""
from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from verification_compiler_video.pipeline import camera3d, stage, style
from verification_compiler_video.pipeline.beats import Beat
from verification_compiler_video.pipeline.camera3d import Beat3DScene


class S06VQP(Beat3DScene):
    section_id = "06_vqp"
    title = ""
    timing_dir = Path(__file__).resolve().parents[1] / "out" / "timing"
    initial_phi = 58
    initial_theta = -88

    def storyboard(self) -> list[Beat]:
        return [
            Beat("I have been calling that artifact a Verification Query Package", self.b00_name),
            Beat("The name is clunky, but the idea is useful", self.b01_clunky),
            Beat("A Verification Query Package is the smallest unit of verification",
                 self.b02_smallest),
            Beat("It includes the code under review", self.b03_code),
            Beat("It includes the requirements that code is supposed to satisfy", self.b04_reqs),
            Beat("It includes the tests and results attached to the same version", self.b05_tests),
            Beat("It includes the source-region text that supports the claim", self.b06_source),
            Beat("It includes the review instructions", self.b07_instructions),
            Beat("And it is bounded", self.b08_bounded),
            Beat("Small enough for a model to analyze", self.b09_model_size),
            Beat("Small enough for a human to inspect", self.b10_human_size),
            Beat("But complete enough that the reviewer is not guessing", self.b11_complete),
            Beat("And a package does not have to be text", self.b12_not_text),
            Beat("A rendered screen, a captured output, a physical test trace", self.b13_media,
                 note="8.9s — the media kinds arrive one at a time"),
            Beat("That matters well beyond aerospace", self.b14_beyond),
            Beat("This is one of the important shifts", self.b15_shift),
            Beat("Instead of asking a model to review an entire project", self.b16_whole_project,
                 note="8.9s — the whole graph, then the slice the traversal picks"),
            Beat("The huge problem becomes many smaller review packages", self.b17_many),
            Beat("And each package can leave behind a structured result", self.b18_result),
        ]

    # --------------------------------------------------------------- helpers --
    def upright(self, mob: Mobject) -> Mobject:
        return mob.rotate(PI / 2, axis=RIGHT)

    def caption3d(self, text: str, color: str = style.WHITE):
        cap = style.caption_text(text, color=color)
        stage.fit(cap, stage.CAPTION)
        cap.set_opacity(0)
        self.pin(cap)
        return cap

    # ----------------------------------------------------------------- beats --
    def b00_name(self, ctx):
        packet = self.upright(style.node("vqp", "VQP", size=2.1))
        packet.move_to(ORIGIN)
        ctx.show(packet, tag="packet", anim=lambda m: FadeIn(m, scale=0.8), run_time=0.6)
        cap = self.caption3d("Verification Query Package", style.GREEN)
        ctx.play(cap.animate.set_opacity(1), run_time=0.45)
        self._own("cap", cap)
        # Six seconds naming one object. Turn it in the light rather than
        # presenting it and waiting — this is the first time the packet appears
        # and it is worth looking at from more than one side.
        self.move_camera(phi=58 * DEGREES, theta=-58 * DEGREES,
                         run_time=max(ctx.window - 2.0, 0.8))

    def b01_clunky(self, ctx):
        ctx.play(self._owned["cap"].animate.set_opacity(0), run_time=0.3)
        # The whole line, not a second of it. Six seconds of held frame while the
        # narrator is still speaking reads as a stall, and a slow orbit is what
        # this shot is for.
        self.move_camera(phi=64 * DEGREES, theta=-72 * DEGREES,
                         run_time=max(ctx.window - 0.5, 0.6))

    def b02_smallest(self, ctx):
        # The packet becomes a token up in the corner here, and a label scaled to
        # 9.4pt with it is not a label — it is texture. Drop it; the shape and the
        # colour already say what it is, which is what the grammar is for.
        style.strip_labels(self._owned["packet"])
        ctx.play(self._owned["packet"].animate.scale(0.55).move_to(np.array([0.0, 0.0, 2.4])),
                 run_time=0.7)
        unit = self.upright(style.node("code", "clamp()", size=1.3))
        unit.move_to(ORIGIN)
        ctx.show(unit, tag="unit", anim=lambda m: FadeIn(m, scale=0.8), run_time=0.5)
        ctx.hold(0.4)
        self.move_camera(phi=60 * DEGREES, theta=-80 * DEGREES,
                         run_time=min(max(ctx.window - 1.6, 0.4), 2.2))
        halo = Circle(radius=1.15, color=style.BLUE, stroke_width=3)
        self.upright(halo).move_to(unit.get_center())
        ctx.show(halo, tag="halo", anim=lambda m: Create(m), run_time=0.5)
        ctx.hold(0.4)
        ctx.play(halo.animate.scale(1.25).set_stroke(opacity=0.35), run_time=0.6)

    def _petal(self, ctx, kind: str, offset, tag: str, run_time: float = 0.45):
        n = self.upright(style.node(kind, "", size=0.8))
        n.move_to(self._owned["unit"].get_center() + offset)
        # camera3d.edge3d, not a bare Line3D: the bare line carries no layer, so
        # it draws in front of the node it joins and drops behind the moment
        # anything else arrives. That is the blink at 06 b07.
        edge = camera3d.edge3d(n, self._owned["unit"],
                               color=style.NODE_KINDS[kind]["color"], width=2.0)
        ctx.show(n, edge, tag=tag, anim=lambda m: FadeIn(m, scale=0.7), run_time=run_time)
        return n

    def b03_code(self, ctx):
        ctx.play(*style.highlight(self._owned["unit"], style.BLUE), run_time=0.4)

    def b04_reqs(self, ctx):
        self._petal(ctx, "requirement", np.array([-2.6, -1.5, 0.9]), "p_req")

    def b05_tests(self, ctx):
        self._petal(ctx, "test", np.array([2.6, 1.5, 0.9]), "p_test")
        self._petal(ctx, "evidence", np.array([2.6, -1.1, -0.9]), "p_res", run_time=0.4)

    def b06_source(self, ctx):
        n = self._petal(ctx, "source", np.array([-2.6, 1.1, -0.9]), "p_src")
        # The line keeps going after the node lands; slice the document while it
        # does rather than holding a still frame.
        for i in range(3):
            s = Rectangle(width=0.42, height=0.1, color=style.VIOLET, stroke_width=2)
            s.set_fill(style.PANEL, opacity=0.95)
            self.upright(s).move_to(n.get_center() + np.array([0.0, 0.0, 0.2 - i * 0.2]))
            ctx.show(s, tag=f"slice{i}", anim=lambda m: FadeIn(m, scale=0.7), run_time=0.3)
            ctx.hold(0.55)

    def b07_instructions(self, ctx):
        self._petal(ctx, "review", np.array([0.0, -0.4, -2.1]), "p_rev")

    def b08_bounded(self, ctx):
        ring = Circle(radius=3.5, color=style.GREEN, stroke_width=3.5)
        self.upright(ring).move_to(self._owned["unit"].get_center())
        ctx.show(ring, tag="ring", anim=lambda m: Create(m), run_time=0.6)

    def b09_model_size(self, ctx):
        m = self.upright(style.node("review", "", size=0.75))
        m.move_to(np.array([-5.1, 0.0, 2.0]))
        ctx.show(m, tag="mrev", run_time=0.4)

    def b10_human_size(self, ctx):
        h = self.upright(style.node("review", "", size=0.75))
        h.move_to(np.array([5.1, 0.0, 2.0]))
        ctx.show(h, tag="hrev", run_time=0.4)

    def b11_complete(self, ctx):
        cap = self.caption3d("everything needed, nothing else", style.GREEN)
        ctx.play(cap.animate.set_opacity(1), run_time=0.4)
        self._own("cap2", cap)
        for tag in ("p_req", "p_test", "p_res", "p_src", "p_rev"):
            ctx.play(*style.highlight(self._owned[tag][0], style.GREEN), run_time=0.2)
            ctx.hold(0.18)

    # -------------------------------------------------- packages are not text --
    def b12_not_text(self, ctx):
        ctx.play(self._owned["cap2"].animate.set_opacity(0), run_time=0.25)
        ctx.play(self._owned["ring"].animate.set_stroke(style.GREEN, width=2, opacity=0.4),
                 run_time=0.35)

    def b13_media(self, ctx):
        """A screen, a waveform, a physical trace — evidence that is not prose."""
        screen = Rectangle(width=1.5, height=0.95, color=style.CYAN, stroke_width=2.6)
        screen.set_fill(style.PANEL, opacity=0.96)
        bars = VGroup(*[Line(LEFT * 0.5, RIGHT * 0.5, color=style.CYAN, stroke_width=2)
                        .set_length(0.9 - i * 0.2) for i in range(3)])
        bars.arrange(DOWN, buff=0.19).move_to(screen)
        shot = VGroup(screen, bars)
        self.upright(shot).move_to(np.array([-3.4, 0.0, -3.0]))

        wave = VMobject(color=style.AMBER, stroke_width=3)
        pts = [np.array([x * 0.13, 0.0, 0.32 * np.sin(x * 0.9)]) for x in range(-6, 7)]
        wave.set_points_as_corners(pts)
        wave.move_to(np.array([0.0, 0.0, -3.0]))

        trace = VGroup(
            Rectangle(width=1.3, height=0.85, color=style.RED, stroke_width=2.6)
            .set_fill(style.PANEL, opacity=0.96),
            Line(LEFT * 0.45, RIGHT * 0.45, color=style.RED, stroke_width=2.5),
        )
        self.upright(trace).move_to(np.array([3.4, 0.0, -3.0]))

        for mob, tag in ((shot, "m_shot"), (wave, "m_wave"), (trace, "m_trace")):
            ctx.show(mob, tag=tag, anim=lambda m: FadeIn(m, scale=0.75), run_time=0.45)
            ctx.hold(0.7)
            ctx.play(*style.highlight(mob, style.GREEN), run_time=0.35)
            ctx.hold(0.6)
        for tag in ("m_shot", "m_wave", "m_trace"):
            ctx.play(self._owned[tag].animate.shift(np.array([0.0, 0.0, 0.28])),
                     run_time=0.3)

    def b14_beyond(self, ctx):
        cap = self.caption3d("strictest case", style.GOLD)
        ctx.play(cap.animate.set_opacity(1), run_time=0.35)
        self._own("cap3", cap)
        # Use the window. Capping the move at 1.8s of a 7.9s line left four
        # seconds of parked camera with the narrator still talking.
        self.move_camera(phi=70 * DEGREES, theta=-100 * DEGREES,
                         run_time=max(ctx.window - 2.5, 0.8))
        for tag in ("mrev", "hrev"):
            ctx.play(*style.highlight(self._owned[tag], style.GOLD), run_time=0.3)
            ctx.hold(0.5)

    # ------------------------------------------------------------- the shift --
    def b15_shift(self, ctx):
        ctx.play(self._owned["cap3"].animate.set_opacity(0), run_time=0.3)
        ctx.retire("m_shot", "m_wave", "m_trace", run_time=0.4)

    def b16_whole_project(self, ctx):
        """The whole graph, then the slice the traversal actually hands over."""
        # A crowd is the argument here: this is what a whole project looks like
        # before the traversal picks a slice out of it. Nodes jostling at this
        # camera angle is density, not a layout mistake — and the beat dims the
        # cloud to 16% two seconds later precisely so the slice can be read
        # against it.
        ctx.waive("node_overlap", "a deliberately dense cloud — the whole project at once")
        rng = __import__("random").Random(4)
        cloud = VGroup()
        # A jittered grid, not uniform random. Thirty nodes scattered freely over
        # this area collide constantly — the check was right, and a cloud where
        # half the nodes sit on top of each other does not read as "a whole
        # project" so much as a mess.
        # Three depth layers, not one sheet. The whole point of doing this shot
        # in 3D is that a project has depth; laying every node on y=0 made the
        # camera moves reveal nothing and left the frame reading as clutter.
        cells = [(cx, cz, cy) for cy in range(3)
                 for cz in range(3) for cx in range(4)]
        for cx, cz, cy in cells:
            n = self.upright(style.node(
                rng.choice(["requirement", "code", "test", "evidence"]), "", size=0.42))
            n.move_to(np.array([-4.2 + cx * 2.8 + rng.uniform(-0.25, 0.25),
                                -2.6 + cy * 2.6 + rng.uniform(-0.3, 0.3),
                                -2.0 + cz * 2.0 + rng.uniform(-0.15, 0.15)]))
            cloud.add(n)
        ctx.play(LaggedStart(*[FadeIn(c, scale=0.7) for c in cloud], lag_ratio=0.02),
                 run_time=1.3)
        self._own("cloud", cloud)
        ctx.hold(0.8)
        ctx.play(cloud.animate.set_opacity(0.16), run_time=0.6)
        ctx.play(self._owned["ring"].animate.set_stroke(style.GREEN, width=5, opacity=1),
                 run_time=0.6)
        # Nearly nine seconds on this line. Sweep the camera across the dimmed
        # cloud so the slice the ring picks out is read against the whole graph,
        # which is the point being made, rather than stated once and then held.
        self.move_camera(theta=-64 * DEGREES, phi=58 * DEGREES,
                         run_time=max(ctx.window - 3.6, 0.8))

    def b17_many(self, ctx):
        # The cloud has made its point; it is the backdrop for the slice, not for
        # the packages. Leaving it up put four more shapes into an already full
        # frame, which is the clutter at 06 b19.
        ctx.retire("cloud", run_time=0.4)
        packs = VGroup()
        # Staggered in depth as well as across: four identical packages on one
        # plane read as a row of icons, four at different distances read as many.
        for i, (x, y) in enumerate(((-4.0, -1.8), (-1.35, 0.6), (1.35, -0.6), (4.0, 1.8))):
            pk = self.upright(style.node("vqp", "", size=1.05))
            pk.move_to(np.array([x, y, -1.9]))
            packs.add(pk)
        ctx.show(packs, tag="packs", anim=lambda m: FadeIn(m, scale=0.7), run_time=0.7)
        self.move_camera(phi=64 * DEGREES, theta=-90 * DEGREES,
                         run_time=min(ctx.window - 1.0, 1.4))

    def b18_result(self, ctx):
        cap = self.caption3d("review result", style.GREEN)
        ctx.play(cap.animate.set_opacity(1), run_time=0.45)
        self._own("cap4", cap)
        for pk in self._owned["packs"]:
            ctx.play(*style.highlight(pk, style.GREEN), run_time=0.22)
