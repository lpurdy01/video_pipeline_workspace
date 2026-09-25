"""
Section 11 — End card.

A landing, not another diagram. It reuses the grammar the video spent fourteen
minutes teaching rather than introducing anything new: the evidence record is
the last thing section 10 leaves on screen, so this picks it up there and takes
it apart into what happens next.

The "not a product, not finished" beat is drawn as a blueprint — the same shapes
in dashed outline — and the build beat fills that outline in. That is the whole
idea of the card: the thing you have just watched is the drawing, and the next
video is the object.

No platform logos and no borrowed branding: the ask is made in the video's own
type and shapes.
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from verification_compiler_video.pipeline import stage, style
from verification_compiler_video.pipeline.beats import Beat, BeatScene


def blueprint(mob: Mobject) -> VGroup:
    """A dashed ghost of a shape — drawn, not built."""
    out = VGroup()
    for sub in mob.get_family():
        if not len(getattr(sub, "points", [])) or getattr(sub, "text", None):
            continue
        try:
            dash = DashedVMobject(sub.copy().set_fill(opacity=0)
                                  .set_stroke(style.MUTED, width=2.2),
                                  num_dashes=26, dashed_ratio=0.55)
        except Exception:
            continue
        # A ghost is scenery, not composition. Copying an arrow copies its
        # qa_role with it, so without this every dashed outline of a connector
        # is recorded as a connector — a hundred of them, all pointing at the
        # invisible shapes they were traced from.
        for part in dash.get_family():
            part.qa_ignore = True
            for attr in ("qa_role", "qa_layer", "qa_kind", "qa_label"):
                if hasattr(part, attr):
                    delattr(part, attr)
        out.add(dash)
    return out


class S11EndCard(BeatScene):
    section_id = "11_end_card"
    title = "Thank you for listening"
    timing_dir = Path(__file__).resolve().parents[1] / "out" / "timing"

    def storyboard(self) -> list[Beat]:
        return [
            Beat("Thank you for sitting through my thinking on this",
                 self.b00_thanks,
                 note="pick up exactly where section 10 left off — the evidence record"),
            Beat("The full whitepaper that goes with this video is in the description",
                 self.b01_paper,
                 note="6s — the paper, then the references behind it"),
            Beat("And if you are an agentic developer", self.b02_agent,
                 note="10.5s — the invitation: an agent building its own compiler"),
            Beat("What tagging system did you use", self.b03_questions,
                 note="10.5s — three open questions, one per clause"),
            Beat("I wanted to publish this idea so that other people could start expanding",
                 self.b04_expand,
                 note="8.3s — one graph becomes many"),
            Beat("I want to be straight about what this is", self.b05_blueprint,
                 note="7s — the picture admits it is a drawing"),
            Beat("So the next thing I am going to do is build it", self.b06_build,
                 note="13s — the drawing fills in, then the rough edges show"),
            Beat("If you want to know when that lands", self.b07_subscribe),
            Beat("And if you know someone working on this problem", self.b08_send_on,
                 note="9s — one diamond becomes two, then the title returns"),
        ]

    # ------------------------------------------------------------- beats --
    def b00_thanks(self, ctx):
        card = style.node("evidence", "evidence", size=2.3)
        card.move_to(stage.STAGE.center + UP * 0.35)
        ctx.show(card, tag="card", anim=lambda m: FadeIn(m, scale=0.92), run_time=0.6)
        ctx.play(*style.highlight(card, style.GREEN), run_time=0.4)

    def b01_paper(self, ctx):
        """The whitepaper itself, and the references behind it, in the description."""
        card = self._owned["card"]
        # Scaling the card scales its label to 12pt. The shape and the colour
        # carry the meaning from here — that is what the grammar is for.
        style.strip_labels(card)
        ctx.play(card.animate.scale(0.62).move_to(np.array([-4.4, 1.5, 0.0])),
                 run_time=0.5)
        paper = style.node("source", "", size=2.4)
        paper.move_to(np.array([0.0, 1.05, 0.0]))
        ctx.show(paper, tag="paper", anim=lambda m: FadeIn(m, shift=UP * 0.2),
                 run_time=0.5)
        # The name goes beside the shape, not inside it. Inside, it is scaled and
        # receded repeatedly, and a label that is stripped, revived by an opacity
        # change and stripped again is a bug waiting to happen.
        name = style.label_text("the whitepaper", color=style.VIOLET)
        name.next_to(paper, LEFT, buff=0.4)
        ctx.show(name, tag="papername", run_time=0.35)
        refs = VGroup(*[style.node("source", "", size=0.62) for _ in range(3)])
        refs.arrange(RIGHT, buff=0.42)
        refs.next_to(paper, RIGHT, buff=0.9)
        ctx.show(refs, tag="refs",
                 anim=lambda m: LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in m],
                                            lag_ratio=0.2),
                 run_time=0.6)
        ctx.hold(0.6)
        for r in refs:
            ctx.play(*style.highlight(r, style.VIOLET), run_time=0.22)
            ctx.hold(0.18)
        arrow = style.glow_arrow(
            np.array([0.0, stage.STAGE.bottom + 1.15, 0.0]),
            np.array([0.0, stage.STAGE.bottom + 0.42, 0.0]),
            color=style.VIOLET, width=3.2)
        ctx.show(arrow, tag="down", anim=lambda m: Create(m), run_time=0.35)
        here = style.label_text("description", color=style.MUTED)
        here.move_to(np.array([0.0, stage.STAGE.bottom + 0.2, 0.0]))
        ctx.show(here, tag="here", run_time=0.4)
        ctx.hold(1.4)

    def b02_agent(self, ctx):
        """
        Ten seconds, and the ask that matters: build your own.

        An agent takes the paper and produces its own compiler — drawn as the
        same shapes assembling on the other side of the frame, because the point
        is that the reader ends up with the thing, not with the description.
        """
        ctx.retire("down", "here", run_time=0.3)
        agent = style.node("review", "your agent", size=1.9)
        agent.move_to(np.array([0.0, -1.55, 0.0]))
        ctx.show(agent, tag="agent", anim=lambda m: FadeIn(m, scale=0.85), run_time=0.5)
        feed = style.connect(self._owned["paper"], agent, style.VIOLET, width=2.6)
        ctx.show(feed, tag="feed", anim=lambda m: Create(m), run_time=0.45)
        ctx.hold(0.6)
        # It builds its own graph, one artifact at a time.
        built = VGroup()
        for kind, x in (("requirement", 2.9), ("code", 4.1), ("test", 5.3)):
            n = style.node(kind, "", size=0.72)
            n.move_to(np.array([x, -1.55, 0.0]))
            built.add(n)
            ctx.play(FadeIn(n, scale=0.75), run_time=0.32)
            ctx.hold(0.3)
        self._own("built", built)
        link = style.connect(agent, built[0], style.GREEN, width=2.4)
        ctx.show(link, tag="buildlink", anim=lambda m: Create(m), run_time=0.4)
        tag = style.label_text("build your own", color=style.GREEN)
        tag.move_to(np.array([3.6, -0.4, 0.0]))
        ctx.show(tag, tag="own", run_time=0.4)
        # Keep the built graph alive to the end of the line rather than holding a
        # finished picture for seven seconds.
        for _ in range(3):
            for n in built:
                ctx.play(*style.highlight(n, style.GREEN), run_time=0.22)
                ctx.hold(0.2)
                ctx.play(*style.restroke(n, style.MUTED, 2.2), run_time=0.18)

    def b03_questions(self, ctx):
        """Ten seconds, three questions — one per clause, each held to be read."""
        # A clean stage for the questions. They are the ask; nothing else needs
        # to be on screen, and anything that is will end up crossing them.
        ctx.retire("own", "papername", "refs", "card", "feed", "buildlink",
                   "built", "agent", run_time=0.4)
        ctx.play(self._owned["paper"].animate.scale(0.5)
                 .move_to(np.array([-5.5, 1.85, 0.0])).set_opacity(0.3), run_time=0.4)
        asks = [
            ("tagging system?", style.GOLD),
            ("requirements and sub-requirements?", style.CYAN),
            ("unique IDs?", style.VIOLET),
        ]
        tell = style.label_text("in the comments", color=style.MUTED)
        stage.fit(tell, stage.CAPTION)
        ctx.show(tell, tag="tell", run_time=0.35, nudge=False)
        rows = VGroup()
        for i, (text, colour) in enumerate(asks):
            row = style.label_text(text, color=colour)
            row.move_to(np.array([0.35, 0.95 - i * 0.8, 0.0]))
            rows.add(row)
            ctx.show(row, tag=f"q{i}", anim=lambda m: FadeIn(m, shift=RIGHT * 0.2),
                     run_time=0.4, nudge=False)
            ctx.hold(2.4)
        self._own("asks", rows)

    def b04_expand(self, ctx):
        """Eight seconds: one idea, taken up in several directions at once."""
        ctx.retire("q0", "q1", "q2", "tell", run_time=0.45)
        # Strip before scaling: at 0.75 the label lands at 12pt, which is below
        # the legible minimum and reads as texture rather than a word.
        ctx.play(self._owned["paper"].animate.set_opacity(1.0)
                 .scale(0.75).move_to(stage.STAGE.center + UP * 0.75), run_time=0.5)
        excited = style.label_text("see where it goes", color=style.GREEN)
        stage.fit(excited, stage.CAPTION)
        ctx.show(excited, tag="goes", run_time=0.35, nudge=False)
        rng = random.Random(5)
        branches = VGroup()
        spots = [np.array([x, y, 0.0]) for x, y in
                 ((-4.6, -1.35), (-2.3, -1.85), (0.0, -1.6), (2.3, -1.85), (4.6, -1.35))]
        for i, spot in enumerate(spots):
            kind = ("requirement", "code", "test", "evidence", "vqp")[i]
            n = style.node(kind, "", size=0.78)
            n.move_to(spot)
            branches.add(n)
            edge = style.connect(self._owned["paper"], n,
                                 style.NODE_KINDS[kind]["color"], width=2.2)
            ctx.play(FadeIn(n, scale=0.75), Create(edge), run_time=0.34)
            self._own(f"br{i}", edge)
        self._own("branches", branches)
        ctx.hold(0.4)
        # Each in its own colour, not all in green: the grammar is the one thing
        # this card should not break on its way out.
        kinds = ("requirement", "code", "test", "evidence", "vqp")
        for _ in range(2):
            for n, kind in zip(branches, kinds):
                ctx.play(*style.highlight(n, style.NODE_KINDS[kind]["color"]),
                         run_time=0.16)
        ctx.hold(0.8)

    def b05_blueprint(self, ctx):
        """Seven seconds. The picture admits it is a drawing."""
        ctx.retire("goes", run_time=0.35)
        ctx.waive("partial_dim", "the solid shapes fade into their own blueprint on purpose")
        ctx.waive("outline_over_text", "dashed ghost outlines lie over their own labels")
        solid = VGroup(self._owned["paper"], self._owned["branches"],
                       *[self._owned[f"br{i}"] for i in range(5)])
        ghost = blueprint(solid)
        self._own("ghost", ghost)
        ctx.play(FadeIn(ghost), solid.animate.set_opacity(0.0), run_time=0.7)
        ctx.hold(0.4)
        cap = style.label_text("an idea", color=style.MUTED)
        stage.fit(cap, stage.CAPTION)
        ctx.show(cap, tag="wp", run_time=0.45, nudge=False)
        ctx.hold(1.6)
        ctx.retire("wp", run_time=0.3)
        cap2 = style.label_text("not a product · not finished", color=style.AMBER)
        stage.fit(cap2, stage.CAPTION)
        ctx.show(cap2, tag="np", run_time=0.45, nudge=False)
        ctx.hold(0.8)
        for _ in range(2):
            ctx.play(ghost.animate.set_stroke(style.MUTED, width=3.0), run_time=0.4)
            ctx.play(ghost.animate.set_stroke(style.MUTED, width=2.2), run_time=0.4)

    def b06_build(self, ctx):
        """
        Thirteen seconds, and the argument of the card: the drawing becomes the
        thing. It fills in one piece at a time, then the corners that do not fit
        light up, because that is what the next year of work is.
        """
        ctx.retire("np", run_time=0.35)
        building = style.label_text("next: build it", color=style.CYAN)
        stage.fit(building, stage.CAPTION)
        ctx.show(building, tag="build", run_time=0.45, nudge=False)
        ctx.hold(0.5)

        order = [self._owned["paper"], *self._owned["branches"],
                 *[self._owned[f"br{i}"] for i in range(5)]]
        for piece in order:
            ctx.play(piece.animate.set_opacity(1.0), run_time=0.26)
            # set_opacity(1.0) resurrects a label that strip_labels zeroed.
            style.strip_labels(piece)
            ctx.hold(0.2)
        ctx.play(self._owned["ghost"].animate.set_opacity(0.16), run_time=0.4)
        ctx.hold(0.5)

        ctx.retire("build", run_time=0.3)
        rough = style.label_text("and find the rough edges", color=style.AMBER)
        stage.fit(rough, stage.CAPTION)
        ctx.show(rough, tag="rough", run_time=0.45, nudge=False)
        for _ in range(2):
            for r in self._owned["branches"]:
                ctx.play(*style.highlight(r, style.AMBER), run_time=0.2)
                ctx.hold(0.12)
                ctx.play(*style.restroke(r, style.MUTED, 2.2), run_time=0.18)
        ctx.hold(0.4)

    def b07_subscribe(self, ctx):
        ctx.retire("rough", "ghost", run_time=0.4)
        ctx.recede("branches", *[f"br{i}" for i in range(5)], opacity=0.22,
                   run_time=0.4)
        ask = style.label_text("like · subscribe", color=style.GOLD)
        stage.fit(ask, stage.CAPTION)
        ctx.show(ask, tag="ask", run_time=0.45, nudge=False)
        ctx.play(*style.highlight(self._owned["paper"], style.GOLD), run_time=0.4)

    def b08_send_on(self, ctx):
        """Nine seconds: one reader becomes two, and the title returns."""
        ctx.retire("branches", *[f"br{i}" for i in range(5)], run_time=0.4)
        ctx.play(self._owned["paper"].animate.scale(0.9)
                 .move_to(np.array([-2.6, 0.75, 0.0])), run_time=0.5)
        mate = style.node("review", "", size=1.5)
        mate.move_to(np.array([2.6, 0.75, 0.0]))
        ctx.show(mate, tag="mate", anim=lambda m: FadeIn(m, scale=0.8), run_time=0.45)
        pass_it = style.connect(self._owned["paper"], mate, style.GOLD, width=3.0)
        ctx.show(pass_it, tag="pass", anim=lambda m: Create(m), run_time=0.5)
        ctx.hold(0.4)
        ctx.retire("ask", run_time=0.3)
        who = style.label_text("who has to certify it", color=style.MUTED)
        stage.fit(who, stage.CAPTION)
        ctx.show(who, tag="who", run_time=0.45, nudge=False)
        ctx.hold(2.6)
        ctx.retire("who", run_time=0.4)
        final = style.title_text("a compiler for trust")
        final.move_to(np.array([0.0, stage.STAGE.bottom + 0.95, 0.0]))
        ctx.show(final, tag="final", anim=lambda m: FadeIn(m, scale=0.94), run_time=0.6)
        ctx.play(*style.highlight(self._owned["paper"], style.GREEN),
                 *style.highlight(mate, style.GOLD), run_time=0.5)
