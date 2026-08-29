"""
Candidate set B — mechanism and motion.

Where set A (storyboard_scenes.py) states each idea as a finished diagram, set B
tries to *show the process*: rates diverging, a walk through a graph, a fold, a
swap, an append. One scene per script section, same ids as the manifest.
"""
from __future__ import annotations

from manim import *

from visual_style import (
    AMBER,
    BG,
    BLUE,
    CYAN,
    GOLD,
    GREEN,
    GRID,
    MUTED,
    PANEL,
    RED,
    VIOLET,
    WHITE,
    artifact_node,
    card,
    connect,
    field_card,
    glow_arrow,
    glow_line,
    label_text,
    safe_title,
    status_bar,
    tiny_text,
    title_text,
)


class VCScene(Scene):
    def setup(self):
        self.camera.background_color = BG

    def pause(self, t: float = 0.5):
        self.wait(t)


class B01RateDivergence(VCScene):
    """Generation rate and verification rate diverge; the gap is the backlog."""

    def construct(self):
        safe_title(self, "Two rates, one gap")

        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 100, 25],
            x_length=8.2,
            y_length=3.9,
            axis_config={"color": GRID, "stroke_width": 2, "include_tip": False},
        ).shift(DOWN * 0.55)
        x_label = tiny_text("time", font_size=20).next_to(axes.x_axis, DOWN, buff=0.18)
        self.play(Create(axes), FadeIn(x_label), run_time=0.7)

        gen = axes.plot(lambda x: 3.2 * x**2, x_range=[0, 5.5], color=CYAN, stroke_width=5)
        ver = axes.plot(lambda x: 9.0 * x, x_range=[0, 10], color=GOLD, stroke_width=5)
        gen_tag = label_text("generated", font_size=22, color=CYAN).next_to(gen.get_end(), UP, buff=0.14)
        ver_tag = label_text("verified", font_size=22, color=GOLD).next_to(ver.get_end(), RIGHT, buff=0.14)

        self.play(Create(gen), run_time=1.0)
        self.play(FadeIn(gen_tag), run_time=0.3)
        self.play(Create(ver), run_time=1.0)
        self.play(FadeIn(ver_tag), run_time=0.3)

        gap = axes.get_area(gen, x_range=[0, 5.5], bounded_graph=ver, color=RED, opacity=0.30)
        gap_label = Text("unverified", color=RED, font_size=26, weight=BOLD)
        gap_label.move_to(axes.c2p(4.0, 42))
        self.play(FadeIn(gap), run_time=0.7)
        self.play(Write(gap_label), run_time=0.5)
        self.pause(0.9)


class B02TwoColumnLedger(VCScene):
    """What the model said, beside what an auditor actually needs."""

    def construct(self):
        safe_title(self, "Fluent is not the same as accountable")

        said_box = RoundedRectangle(corner_radius=0.12, width=5.0, height=4.0, color=BLUE, stroke_width=2.4)
        said_box.set_fill(PANEL, opacity=0.97).shift(LEFT * 3.1 + DOWN * 0.4)
        said_head = label_text("what the model said", font_size=22, color=BLUE)
        said_head.next_to(said_box.get_top(), DOWN, buff=0.22)
        said_body = VGroup(
            Text('"Looks good."', color=WHITE, font_size=24, weight=BOLD),
            Text('"This satisfies the requirement."', color=MUTED, font_size=18),
            Text('"I checked the edge cases."', color=MUTED, font_size=18),
        ).arrange(DOWN, buff=0.26, aligned_edge=LEFT)
        said_body.next_to(said_head, DOWN, buff=0.42)
        self.play(FadeIn(said_box), FadeIn(said_head), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.1) for t in said_body], lag_ratio=0.18), run_time=0.9)

        need_box = RoundedRectangle(corner_radius=0.12, width=5.0, height=4.0, color=GOLD, stroke_width=2.4)
        need_box.set_fill(PANEL, opacity=0.97).shift(RIGHT * 3.1 + DOWN * 0.4)
        need_head = label_text("what an auditor needs", font_size=22, color=GOLD)
        need_head.next_to(need_box.get_top(), DOWN, buff=0.22)
        fields = ["requirement ID", "code version", "linked test", "result artifact", "who accepted it"]
        rows = VGroup()
        for name in fields:
            blank = Line(LEFT * 0.5, RIGHT * 0.5, color=RED, stroke_width=2.5).set_length(1.15)
            row = VGroup(Text(name, color=WHITE, font_size=19), blank).arrange(RIGHT, buff=0.3)
            rows.add(row)
        rows.arrange(DOWN, buff=0.26, aligned_edge=LEFT).next_to(need_head, DOWN, buff=0.34)
        self.play(FadeIn(need_box), FadeIn(need_head), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.14), run_time=0.9)

        empty = Text("all blank", color=RED, font_size=26, weight=BOLD)
        empty.next_to(need_box, DOWN, buff=0.22)
        self.play(Write(empty), run_time=0.5)
        self.pause(0.9)


class B03ReverseAudit(VCScene):
    """An audit question walks the chain backwards and lights every link."""

    def construct(self):
        safe_title(self, "Every answer has to walk back")

        specs = [
            ("requirement", "REQ-17", GOLD),
            ("code", "CODE", BLUE),
            ("test", "TEST", CYAN),
            ("result", "RESULT", GREEN),
            ("review", "REVIEW", VIOLET),
        ]
        nodes = VGroup(*[artifact_node(k, t, c, size=0.95, font_size=15) for k, t, c in specs])
        nodes.arrange(RIGHT, buff=0.85).shift(DOWN * 0.35)
        edges = VGroup(*[connect(nodes[i], nodes[i + 1], color=MUTED) for i in range(len(nodes) - 1)])
        self.play(FadeIn(nodes), FadeIn(edges), run_time=0.8)

        question = label_text('"what verified REQ-17?"', font_size=26, color=WHITE)
        question.next_to(nodes, UP, buff=0.75)
        self.play(Write(question), run_time=0.6)

        # Walk backwards, lighting each link. artifact_node is VGroup(aura, shape,
        # label) — stroke only the aura and shape, or the label turns into a blob.
        for i in range(len(nodes) - 1, -1, -1):
            anims = [
                nodes[i][0].animate.set_stroke(GOLD, width=12, opacity=0.55),
                nodes[i][1].animate.set_stroke(GOLD, width=4),
            ]
            if i < len(edges):
                anims.append(edges[i].animate.set_color(GOLD))
            self.play(*anims, run_time=0.28)

        answer = label_text("a chain, not an opinion", font_size=26, color=GOLD)
        answer.next_to(nodes, DOWN, buff=0.75)
        self.play(Write(answer), run_time=0.55)
        self.pause(0.8)


class B04ChainsBecomeGraph(VCScene):
    """Three requirements converge on one code unit — rows cannot say this."""

    def construct(self):
        safe_title(self, "The chains were always one graph")

        reqs = VGroup(*[
            artifact_node("requirement", tag, GOLD, size=1.15, font_size=15)
            for tag in ("REQ-1", "REQ-2", "REQ-3")
        ]).arrange(DOWN, buff=0.85).shift(LEFT * 4.6 + DOWN * 0.3)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in reqs], lag_ratio=0.16), run_time=0.9)

        shared = artifact_node("code", "clamp()", BLUE, size=1.35, font_size=16)
        shared.shift(LEFT * 1.1 + DOWN * 0.3)
        self.play(FadeIn(shared, scale=0.9), run_time=0.5)

        merges = VGroup(*[glow_arrow(r.get_right(), shared.get_left(), color=GOLD, width=2.6) for r in reqs])
        self.play(LaggedStart(*[Create(m) for m in merges], lag_ratio=0.13), run_time=0.9)

        test = artifact_node("test", "TEST", CYAN, size=1.05, font_size=15).shift(RIGHT * 1.7 + UP * 0.75)
        result = artifact_node("evidence", "RESULT", GREEN, size=1.05, font_size=13).shift(RIGHT * 1.7 + DOWN * 1.35)
        onward = VGroup(
            glow_arrow(shared.get_right(), test.get_left(), color=BLUE, width=2.6),
            glow_arrow(shared.get_right(), result.get_left(), color=BLUE, width=2.6),
        )
        self.play(FadeIn(test), FadeIn(result), LaggedStart(*[Create(o) for o in onward], lag_ratio=0.1), run_time=0.9)

        orphan = artifact_node("code", "ORPHAN", RED, size=1.05, font_size=14).shift(RIGHT * 4.6 + DOWN * 0.3)
        orphan_tag = tiny_text("nothing points here", font_size=19, color=RED).next_to(orphan, DOWN, buff=0.2)
        self.play(FadeIn(orphan, scale=0.9), FadeIn(orphan_tag), run_time=0.6)

        caption = tiny_text("one code unit answers to three requirements", font_size=22, color=WHITE)
        caption.to_edge(DOWN, buff=0.35)
        self.play(Write(caption), run_time=0.6)
        self.pause(0.8)


class B05TraversalWalk(VCScene):
    """A cursor walks the graph and the package fills as it goes."""

    def construct(self):
        safe_title(self, "Traversal fills the package")

        nodes = VGroup(
            artifact_node("requirement", "REQ", GOLD, size=0.72, font_size=13),
            artifact_node("source", "SRC", VIOLET, size=0.72, font_size=13),
            artifact_node("code", "CODE", BLUE, size=0.72, font_size=13),
            artifact_node("test", "TEST", CYAN, size=0.72, font_size=13),
            artifact_node("evidence", "RESULT", GREEN, size=0.72, font_size=11),
        )
        positions = [
            LEFT * 5.0 + UP * 1.5,
            LEFT * 5.0 + DOWN * 0.9,
            LEFT * 2.6 + UP * 0.3,
            LEFT * 0.4 + UP * 1.5,
            LEFT * 0.4 + DOWN * 0.9,
        ]
        for n, p in zip(nodes, positions):
            n.move_to(p)
        edges = VGroup(
            glow_arrow(nodes[0].get_right(), nodes[2].get_left(), color=GOLD, width=2.4),
            glow_arrow(nodes[1].get_right(), nodes[2].get_left(), color=VIOLET, width=2.4),
            glow_arrow(nodes[2].get_right(), nodes[3].get_left(), color=BLUE, width=2.4),
            glow_arrow(nodes[2].get_right(), nodes[4].get_left(), color=BLUE, width=2.4),
        )
        self.play(FadeIn(nodes), FadeIn(edges), run_time=0.8)

        packet = RoundedRectangle(corner_radius=0.1, width=3.5, height=3.6, color=GREEN, stroke_width=2.6)
        packet.set_fill(PANEL, opacity=0.97).shift(RIGHT * 4.3 + UP * 0.1)
        packet_head = label_text("package", font_size=22, color=GREEN)
        packet_head.next_to(packet.get_top(), DOWN, buff=0.2)
        self.play(FadeIn(packet), FadeIn(packet_head), run_time=0.5)

        slot_y = [0.85, 0.35, -0.15, -0.65, -1.15]
        cursor = Circle(radius=0.52, color=CYAN, stroke_width=4).move_to(nodes[0])
        self.play(Create(cursor), run_time=0.35)
        for i, n in enumerate(nodes):
            entry = tiny_text(f"+ {['requirement','source region','code unit','test','result'][i]}",
                              font_size=17, color=WHITE)
            entry.move_to(packet.get_center() + UP * slot_y[i] + LEFT * 0.35)
            entry.align_to(packet.get_left() + RIGHT * 0.25, LEFT)
            self.play(cursor.animate.move_to(n), run_time=0.26)
            self.play(FadeIn(entry, shift=RIGHT * 0.15), run_time=0.24)

        self.play(FadeOut(cursor), packet.animate.set_stroke(GREEN, width=5), run_time=0.4)
        self.pause(0.8)


class B06FoldPackage(VCScene):
    """The selected subgraph folds down into one packet, then opens into panes."""

    def construct(self):
        safe_title(self, "Bounded by construction")

        cluster = VGroup(
            artifact_node("requirement", "REQ", GOLD, size=0.72, font_size=13),
            artifact_node("code", "CODE", BLUE, size=0.72, font_size=13),
            artifact_node("test", "TEST", CYAN, size=0.72, font_size=13),
            artifact_node("evidence", "RES", GREEN, size=0.72, font_size=13),
            artifact_node("source", "SRC", VIOLET, size=0.72, font_size=13),
        ).arrange_in_grid(rows=2, cols=3, buff=0.55).shift(LEFT * 3.6 + DOWN * 0.2)
        self.play(FadeIn(cluster, scale=0.95), run_time=0.7)

        packet = RoundedRectangle(corner_radius=0.1, width=1.9, height=1.25, color=GREEN, stroke_width=3)
        packet.set_fill(PANEL, opacity=0.98).move_to(ORIGIN + DOWN * 0.2)
        packet_label = Text("VQP", color=GREEN, font_size=24, weight=BOLD).move_to(packet)
        self.play(
            ReplacementTransform(cluster, VGroup(packet, packet_label)),
            run_time=1.0,
        )

        panes = VGroup(
            card("code unit", width=2.7, height=0.62, color=BLUE, font_size=18),
            card("requirements", width=2.7, height=0.62, color=GOLD, font_size=18),
            card("source region", width=2.7, height=0.62, color=VIOLET, font_size=18),
            card("tests + results", width=2.7, height=0.62, color=CYAN, font_size=18),
            card("review question", width=2.7, height=0.62, color=GREEN, font_size=18),
        ).arrange(DOWN, buff=0.2).shift(RIGHT * 3.9 + DOWN * 0.2)
        beam = glow_arrow(packet.get_right(), panes.get_left(), color=GREEN, width=3)
        self.play(Create(beam), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.15) for p in panes], lag_ratio=0.1), run_time=1.0)

        note = tiny_text("small enough to actually review", font_size=21, color=WHITE).to_edge(DOWN, buff=0.4)
        self.play(Write(note), run_time=0.55)
        self.pause(0.8)


class B07ReviewerSwap(VCScene):
    """The package and the schema hold still. Only the reviewer swaps."""

    def construct(self):
        safe_title(self, "Swap the reviewer, not the interface")

        vqp = card("VQP", width=1.9, height=1.2, color=GREEN, font_size=28).shift(LEFT * 4.6)
        schema = field_card(
            "result schema",
            ["verdict", "rationale", "citations", "reviewer", "authority"],
            width=3.5,
            height=2.7,
            color=VIOLET,
        ).shift(RIGHT * 4.1)
        slot = RoundedRectangle(corner_radius=0.12, width=3.3, height=1.6, color=GRID, stroke_width=2.4)
        slot.set_fill("#060B18", opacity=1).move_to(ORIGIN)
        slot_tag = tiny_text("reviewer slot", font_size=19).next_to(slot, UP, buff=0.16)

        self.play(FadeIn(vqp), FadeIn(slot), FadeIn(slot_tag), FadeIn(schema), run_time=0.8)
        self.play(
            Create(glow_arrow(vqp.get_right(), slot.get_left(), color=GREEN, width=3)),
            Create(glow_arrow(slot.get_right(), schema.get_left(), color=VIOLET, width=3)),
            run_time=0.6,
        )

        model = card("model\n(developmental)", width=3.0, height=1.35, color=CYAN, font_size=19).move_to(slot)
        self.play(FadeIn(model, scale=0.92), run_time=0.5)
        stamp1 = Text("developmental", color=CYAN, font_size=22, weight=BOLD).next_to(schema, DOWN, buff=0.24)
        self.play(FadeIn(stamp1), run_time=0.35)
        self.wait(0.35)

        human = card("human\n(certification-facing)", width=3.0, height=1.35, color=GOLD, font_size=18).move_to(slot)
        stamp2 = Text("accepted", color=GOLD, font_size=22, weight=BOLD).move_to(stamp1)
        self.play(ReplacementTransform(model, human), ReplacementTransform(stamp1, stamp2), run_time=0.7)

        note = tiny_text("same evidence in, same fields out", font_size=21, color=WHITE).to_edge(DOWN, buff=0.4)
        self.play(Write(note), run_time=0.55)
        self.pause(0.8)


class B08VersionLedger(VCScene):
    """Evidence is appended, never edited. Old records grey out, they do not vanish."""

    def construct(self):
        safe_title(self, "Append, never overwrite")

        def record(tag: str, verdict: str, color: str) -> VGroup:
            box = RoundedRectangle(corner_radius=0.08, width=4.6, height=1.0, color=color, stroke_width=2.2)
            box.set_fill(PANEL, opacity=0.97)
            left = VGroup(
                Text(tag, color=color, font_size=19, weight=BOLD),
                Text(verdict, color=WHITE, font_size=17),
            ).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
            left.move_to(box.get_left() + RIGHT * 1.5)
            seal = VGroup(
                Circle(radius=0.24, color=GOLD, stroke_width=2.2).set_fill("#2A2105", opacity=1),
                Text("#", color=GOLD, font_size=17, weight=BOLD),
            )
            seal.move_to(box.get_right() + LEFT * 0.6)
            return VGroup(box, left, seal)

        r1 = record("v1  code a81f", "PASS  ·  reviewed by model", GREEN).shift(UP * 1.6 + LEFT * 1.4)
        self.play(FadeIn(r1, shift=DOWN * 0.15), run_time=0.6)

        change = card("code changes", width=2.5, height=0.7, color=RED, font_size=19).shift(RIGHT * 4.3 + UP * 0.4)
        self.play(FadeIn(change, shift=LEFT * 0.2), run_time=0.45)

        stale = Text("STALE", color=RED, font_size=22, weight=BOLD).next_to(r1, RIGHT, buff=0.3)
        self.play(r1.animate.set_opacity(0.4), FadeIn(stale), run_time=0.5)

        r2 = record("v2  code c93d", "PASS  ·  reviewed by human", GREEN).shift(DOWN * 0.1 + LEFT * 1.4)
        self.play(FadeIn(r2, shift=DOWN * 0.15), run_time=0.6)

        r3 = record("v3  code c93d", "UNCERTAIN  ·  escalated", AMBER).shift(DOWN * 1.8 + LEFT * 1.4)
        self.play(FadeIn(r3, shift=DOWN * 0.15), run_time=0.6)

        spine = glow_line(r1.get_left() + LEFT * 0.28 + UP * 0.1, r3.get_left() + LEFT * 0.28, color=GOLD, width=3)
        self.play(Create(spine), run_time=0.5)
        note = tiny_text("the history is the audit trail", font_size=21, color=GOLD).to_edge(DOWN, buff=0.35)
        self.play(Write(note), run_time=0.5)
        self.pause(0.8)


class B09ReadinessTrend(VCScene):
    """Readiness as a CI signal over commits, not a one-off score."""

    def construct(self):
        safe_title(self, "A signal you watch, not a badge you earn")

        axes = Axes(
            x_range=[0, 12, 3],
            y_range=[0, 1.0, 0.25],
            x_length=8.0,
            y_length=3.4,
            axis_config={"color": GRID, "stroke_width": 2, "include_tip": False},
        ).shift(DOWN * 0.7)
        x_tag = tiny_text("commits", font_size=20).next_to(axes.x_axis, DOWN, buff=0.18)
        y_tag = tiny_text("VRM", font_size=20).next_to(axes.y_axis, UP, buff=0.14)
        self.play(Create(axes), FadeIn(x_tag), FadeIn(y_tag), run_time=0.7)

        pts = [(0, 0.22), (1, 0.30), (2, 0.41), (3, 0.38), (4, 0.52), (5, 0.61),
               (6, 0.44), (7, 0.55), (8, 0.68), (9, 0.74), (10, 0.71), (11, 0.83)]
        line = VMobject(color=CYAN, stroke_width=5)
        line.set_points_as_corners([axes.c2p(x, y) for x, y in pts])
        self.play(Create(line), run_time=1.4)

        drop = Dot(axes.c2p(6, 0.44), color=RED, radius=0.1)
        drop_tag = tiny_text("refactor landed", font_size=19, color=RED).next_to(drop, DOWN, buff=0.2)
        self.play(FadeIn(drop, scale=0.6), FadeIn(drop_tag), run_time=0.5)

        warn = Text("not a safety score", color=RED, font_size=24, weight=BOLD)
        warn.to_edge(DOWN, buff=0.3)
        self.play(Write(warn), run_time=0.5)
        self.pause(0.9)


class B10TheLoop(VCScene):
    """Generation and verification close into one loop the human sits inside."""

    def construct(self):
        safe_title(self, "Close the loop")

        radius = 2.15
        ring = Circle(radius=radius, color=GRID, stroke_width=3).shift(DOWN * 0.35)
        self.play(Create(ring), run_time=0.7)

        stations = [
            ("generate", CYAN, UP),
            ("graph", VIOLET, RIGHT),
            ("verify", GOLD, DOWN),
            ("evidence", GREEN, LEFT),
        ]
        nodes = VGroup()
        for name, color, direction in stations:
            c = card(name, width=2.0, height=0.66, color=color, font_size=19)
            c.move_to(ring.get_center() + direction * radius)
            nodes.add(c)
        self.play(LaggedStart(*[FadeIn(n, scale=0.9) for n in nodes], lag_ratio=0.15), run_time=0.9)

        runner = Dot(color=WHITE, radius=0.11).move_to(ring.point_from_proportion(0.25))
        self.play(FadeIn(runner), run_time=0.25)
        self.play(MoveAlongPath(runner, ring), run_time=1.5, rate_func=linear)

        human = VGroup(
            Circle(radius=0.62, color=GOLD, stroke_width=3).set_fill("#2A2105", opacity=0.9),
            Text("human", color=GOLD, font_size=19, weight=BOLD),
        ).move_to(ring.get_center())
        self.play(FadeIn(human, scale=0.85), FadeOut(runner), run_time=0.6)

        final = Text("Generate evidence we can inspect.", color=WHITE, font_size=27, weight=BOLD)
        final.to_edge(DOWN, buff=0.28)
        self.play(Write(final), run_time=0.7)
        self.pause(0.8)
