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


class S01GenerationGate(VCScene):
    def construct(self):
        title = safe_title(self, "Generation got cheap")

        prompt = card('Prompt: "build the feature"', width=4.4, color=BLUE, font_size=24)
        prompt.to_edge(UP, buff=1.25)
        self.play(FadeIn(prompt, shift=DOWN * 0.2), run_time=0.5)

        labels = ["code", "tests", "docs", "logs", "plans", "reviews", "SQL", "API"]
        blocks = VGroup()
        for i, label in enumerate(labels):
            block = card(label, width=1.05, height=0.48, color=[BLUE, CYAN, GREEN, GOLD][i % 4], font_size=16)
            row = i // 4
            col = i % 4
            block.move_to(LEFT * 4.8 + RIGHT * col * 1.32 + DOWN * (0.95 + row * 0.65))
            blocks.add(block)
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.18) for b in blocks], lag_ratio=0.08), run_time=1.2)

        gate = RoundedRectangle(corner_radius=0.08, width=1.1, height=2.55, color=RED, stroke_width=3)
        gate.set_fill("#160611", opacity=0.95)
        gate_label = Text("VERIFY", color=WHITE, font_size=20).rotate(PI / 2).move_to(gate)
        gate_group = VGroup(gate, gate_label).move_to(RIGHT * 4.6 + DOWN * 0.95)
        self.play(FadeIn(gate_group, shift=LEFT * 0.2), run_time=0.5)

        arrows = VGroup(*[glow_arrow(b.get_right(), gate_group.get_left(), color=CYAN, width=2.2) for b in blocks])
        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.04), run_time=1.1)

        backlog = VGroup(*[
            RoundedRectangle(corner_radius=0.05, width=0.85, height=0.25, color=RED, stroke_width=1.5)
            .set_fill("#2A0712", opacity=1)
            .move_to(gate_group.get_left() + LEFT * (0.55 + 0.08 * i) + DOWN * (0.78 - i * 0.17))
            for i in range(8)
        ])
        self.play(FadeIn(backlog), gate.animate.set_stroke(RED, width=7), run_time=0.8)

        thesis = Text("Verification did not.", color=RED, font_size=32, weight=BOLD).next_to(title, DOWN, buff=0.25)
        self.play(Write(thesis), run_time=0.6)
        self.pause(0.8)


class S02ChatLogFallacy(VCScene):
    def construct(self):
        safe_title(self, "A chat log is not evidence")

        chat = RoundedRectangle(corner_radius=0.18, width=5.3, height=2.2, color=BLUE, stroke_width=2.8)
        chat.set_fill("#071021", opacity=0.98)
        chat_text = VGroup(
            Text("Looks good.", color=WHITE, font_size=28, weight=BOLD),
            Text("This code satisfies the requirement.", color=MUTED, font_size=20),
        ).arrange(DOWN, buff=0.18).move_to(chat)
        chat_group = VGroup(chat, chat_text).shift(LEFT * 2.7 + DOWN * 0.15)
        self.play(FadeIn(chat_group, shift=UP * 0.2), run_time=0.7)

        missing = field_card(
            "Missing audit fields",
            ["requirement ID", "code hash", "linked test", "result version"],
            width=3.4,
            height=2.6,
            color=RED,
        ).shift(RIGHT * 3.0 + DOWN * 0.15)
        scan = glow_arrow(chat_group.get_right(), missing.get_left(), color=RED)
        self.play(Create(scan), FadeIn(missing, shift=LEFT * 0.15), run_time=0.9)

        evidence = field_card(
            "Evidence record",
            ["result: ___", "rationale: ___", "citations: ___", "version: ___"],
            width=4.4,
            height=2.8,
            color=GREEN,
        ).move_to(ORIGIN + DOWN * 0.15)
        self.play(FadeOut(chat_group), FadeOut(missing), FadeOut(scan), run_time=0.45)
        self.play(FadeIn(evidence, scale=0.96), run_time=0.65)
        caption = label_text("Useful answer != auditable evidence", font_size=26, color=GOLD).next_to(evidence, DOWN, buff=0.35)
        self.play(Write(caption), run_time=0.55)
        self.pause(0.7)


class S03TraceabilityChain(VCScene):
    def construct(self):
        safe_title(self, "Traceability is the shape of trust")

        specs = [
            ("requirement", "REQ", GOLD),
            ("code", "CODE", BLUE),
            ("test", "TEST", CYAN),
            ("result", "RESULT", GREEN),
            ("review", "REVIEW", VIOLET),
            ("evidence", "EVIDENCE", GREEN),
        ]
        nodes = VGroup(*[artifact_node(kind, text, color, size=0.86, font_size=16) for kind, text, color in specs])
        nodes.arrange(RIGHT, buff=0.52).move_to(ORIGIN + DOWN * 0.2)
        arrows = VGroup(*[connect(nodes[i], nodes[i + 1], color=CYAN) for i in range(len(nodes) - 1)])

        self.play(LaggedStart(*[FadeIn(n, scale=0.96) for n in nodes], lag_ratio=0.13), run_time=1.2)
        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.12), run_time=1.0)

        branches = VGroup(nodes.copy(), nodes.copy()).scale(0.62)
        branches[0].shift(UP * 1.45)
        branches[1].shift(DOWN * 1.45)
        branches.set_opacity(0.28)
        self.play(FadeIn(branches), run_time=0.6)

        caption = tiny_text("coordination machinery, not paperwork", font_size=22, color=MUTED).to_edge(DOWN, buff=0.55)
        self.play(Write(caption), run_time=0.6)
        self.pause(0.7)


class S04ArtifactGraph(VCScene):
    def construct(self):
        safe_title(self, "A project is a graph")

        nodes = {
            "REQ-1": artifact_node("requirement", "REQ-1", GOLD),
            "REQ-2": artifact_node("requirement", "REQ-2", GOLD),
            "CODE-A": artifact_node("code", "CODE-A", BLUE),
            "CODE-B": artifact_node("code", "CODE-B", BLUE),
            "TEST": artifact_node("test", "TEST", CYAN),
            "RESULT": artifact_node("evidence", "RESULT", GREEN),
            "SRC": artifact_node("source", "SRC", VIOLET),
            "ORPHAN": artifact_node("code", "ORPHAN", RED),
        }
        positions = {
            "REQ-1": LEFT * 4.2 + UP * 1.4,
            "REQ-2": LEFT * 4.2 + DOWN * 1.0,
            "CODE-A": LEFT * 1.55 + UP * 0.8,
            "CODE-B": LEFT * 1.55 + DOWN * 1.35,
            "TEST": RIGHT * 1.1 + UP * 0.25,
            "RESULT": RIGHT * 3.5 + UP * 0.25,
            "SRC": LEFT * 1.55 + UP * 2.35,
            "ORPHAN": RIGHT * 3.5 + DOWN * 1.6,
        }
        for name, node in nodes.items():
            node.move_to(positions[name])
        node_group = VGroup(*nodes.values())
        edges = VGroup(
            connect(nodes["REQ-1"], nodes["CODE-A"], GOLD),
            connect(nodes["REQ-2"], nodes["CODE-B"], GOLD),
            connect(nodes["CODE-A"], nodes["TEST"], CYAN),
            connect(nodes["CODE-B"], nodes["TEST"], CYAN),
            connect(nodes["TEST"], nodes["RESULT"], GREEN),
            glow_arrow(nodes["SRC"].get_bottom(), nodes["CODE-A"].get_top(), color=VIOLET),
        )

        self.play(LaggedStart(*[FadeIn(n, scale=0.96) for n in node_group], lag_ratio=0.06), run_time=1.0)
        self.play(LaggedStart(*[Create(e) for e in edges], lag_ratio=0.08), run_time=1.0)
        orphan_label = Text("untraceable", color=RED, font_size=22).next_to(nodes["ORPHAN"], DOWN, buff=0.15)
        self.play(nodes["ORPHAN"].animate.scale(1.18), FadeIn(orphan_label), run_time=0.45)
        self.play(nodes["ORPHAN"].animate.scale(1 / 1.18), run_time=0.35)
        self.pause(0.7)


class S05TraversalCompiler(VCScene):
    def construct(self):
        safe_title(self, "Compilation means traversal")

        source = card("source code", width=2.15, color=BLUE).shift(LEFT * 4.6 + UP * 1.55)
        compiler = card("compiler", width=1.9, color=GOLD).shift(LEFT * 2.05 + UP * 1.55)
        binary = card("binary", width=1.65, color=GREEN).shift(RIGHT * 0.25 + UP * 1.55)
        top_flow = VGroup(source, compiler, binary, connect(source, compiler, GOLD), connect(compiler, binary, GREEN))

        graph_label = card("artifact graph", width=2.5, color=VIOLET).shift(LEFT * 4.1 + DOWN * 1.15)
        traversal = card("traversal", width=2.1, color=CYAN).shift(LEFT * 1.2 + DOWN * 1.15)
        vqp = card("VQP", width=1.35, color=GREEN).shift(RIGHT * 1.35 + DOWN * 1.15)
        bottom_flow = VGroup(graph_label, traversal, vqp, connect(graph_label, traversal, CYAN), connect(traversal, vqp, GREEN))

        self.play(FadeIn(top_flow, shift=UP * 0.15), run_time=0.8)
        self.play(FadeIn(bottom_flow, shift=UP * 0.15), run_time=0.8)

        graph_nodes = VGroup(
            artifact_node("requirement", "REQ", GOLD, size=0.55, font_size=12),
            artifact_node("code", "CODE", BLUE, size=0.55, font_size=12),
            artifact_node("test", "TEST", CYAN, size=0.55, font_size=12),
            artifact_node("evidence", "RESULT", GREEN, size=0.55, font_size=10),
        ).arrange(RIGHT, buff=0.28).next_to(graph_label, DOWN, buff=0.35)
        beam = glow_line(graph_nodes[0].get_left() + LEFT * 0.15, graph_nodes[-1].get_right() + RIGHT * 0.15, color=CYAN, width=5)
        self.play(FadeIn(graph_nodes), run_time=0.5)
        self.play(Create(beam), run_time=0.8)

        caption = tiny_text("same graph state -> same package", font_size=22, color=WHITE).to_edge(DOWN, buff=0.5)
        self.play(Write(caption), run_time=0.55)
        self.pause(0.7)


class S06VQPPackage(VCScene):
    def construct(self):
        safe_title(self, "The Verification Query Package")

        req = artifact_node("requirement", "REQ", GOLD).shift(LEFT * 4.2 + UP * 1.4)
        code = artifact_node("code", "CODE", BLUE).shift(LEFT * 2.1 + UP * 0.4)
        test = artifact_node("test", "TEST", CYAN).shift(LEFT * 4.2 + DOWN * 1.0)
        result = artifact_node("evidence", "RESULT", GREEN).shift(LEFT * 2.1 + DOWN * 1.5)
        source = artifact_node("source", "SRC", VIOLET).shift(LEFT * 0.2 + UP * 1.35)
        subgraph = VGroup(req, code, test, result, source)
        edges = VGroup(connect(req, code, GOLD), connect(test, result, GREEN), connect(code, source, VIOLET))
        self.play(FadeIn(subgraph), LaggedStart(*[Create(e) for e in edges], lag_ratio=0.12), run_time=1.0)

        lasso = RoundedRectangle(corner_radius=0.18, width=5.4, height=3.7, color=CYAN, stroke_width=3).move_to(LEFT * 2.25)
        self.play(Create(lasso), run_time=0.65)

        dossier = field_card(
            "VQP dossier",
            ["code unit", "requirements", "source region", "tests + results", "review instructions"],
            width=4.4,
            height=3.4,
            color=GREEN,
        ).shift(RIGHT * 3.0 + DOWN * 0.1)
        arrow = glow_arrow(lasso.get_right(), dossier.get_left(), color=GREEN)
        self.play(Create(arrow), TransformFromCopy(subgraph, dossier), FadeOut(lasso), run_time=1.0)
        self.pause(0.8)


class S07DualModeReview(VCScene):
    def construct(self):
        safe_title(self, "Same package. Different authority.")

        vqp = card("VQP", width=1.6, height=1.05, color=GREEN, font_size=28).shift(LEFT * 4.3)
        model = card("model review\n(developmental)", width=3.0, height=1.35, color=CYAN, font_size=20).shift(LEFT * 0.6 + UP * 1.25)
        human = card("human review\n(certification-facing)", width=3.4, height=1.35, color=GOLD, font_size=19).shift(LEFT * 0.45 + DOWN * 1.25)
        schema1 = field_card("result schema", ["pass/fail/uncertain", "rationale", "citations"], width=3.2, height=1.8, color=VIOLET).shift(RIGHT * 3.65 + UP * 1.25)
        schema2 = field_card("accepted record", ["human authority", "audit trail", "override history"], width=3.2, height=1.8, color=GREEN).shift(RIGHT * 3.65 + DOWN * 1.25)

        self.play(FadeIn(vqp), run_time=0.35)
        self.play(Create(glow_arrow(vqp.get_right(), model.get_left(), color=CYAN)), FadeIn(model), run_time=0.65)
        self.play(Create(glow_arrow(vqp.get_right(), human.get_left(), color=GOLD)), FadeIn(human), run_time=0.65)
        self.play(Create(glow_arrow(model.get_right(), schema1.get_left(), color=VIOLET)), FadeIn(schema1), run_time=0.65)
        self.play(Create(glow_arrow(human.get_right(), schema2.get_left(), color=GREEN)), FadeIn(schema2), run_time=0.65)
        gate = Text("FINAL GATE", color=GOLD, font_size=26, weight=BOLD).next_to(schema2, DOWN, buff=0.18)
        self.play(Write(gate), run_time=0.5)
        self.pause(0.7)


class S08EvidenceCards(VCScene):
    def construct(self):
        safe_title(self, "Evidence cards, not conversations")

        evidence = field_card(
            "Evidence record",
            ["result: PASS", "rationale: linked test passed", "citations: REQ-17, TEST-04", "code hash: a81f..."],
            width=5.0,
            height=3.0,
            color=GREEN,
        ).shift(LEFT * 1.7)
        self.play(FadeIn(evidence, scale=0.96), run_time=0.7)

        seal = Circle(radius=0.42, color=GOLD, stroke_width=3).set_fill("#2A2105", opacity=0.95)
        seal_text = Text("HASH", color=GOLD, font_size=17, weight=BOLD).move_to(seal)
        seal_group = VGroup(seal, seal_text).next_to(evidence, RIGHT, buff=0.35)
        self.play(FadeIn(seal_group, scale=0.8), run_time=0.5)

        code = artifact_node("code", "CODE\nchanged", RED, size=1.0, font_size=16).shift(RIGHT * 3.9 + UP * 1.1)
        self.play(FadeIn(code, shift=LEFT * 0.2), run_time=0.5)

        crack = VGroup(
            Line(UP * 0.6, DOWN * 0.15, color=RED, stroke_width=4),
            Line(DOWN * 0.15, DOWN * 0.65 + RIGHT * 0.25, color=RED, stroke_width=4),
        ).move_to(evidence).shift(RIGHT * 0.75)
        stale = Text("STALE", color=RED, font_size=30, weight=BOLD).next_to(evidence, DOWN, buff=0.25)
        self.play(Create(crack), FadeIn(stale), evidence.animate.set_opacity(0.56), run_time=0.75)
        self.pause(0.8)


class S09ReadinessMap(VCScene):
    def construct(self):
        safe_title(self, "Readiness is visibility")

        graph_nodes = []
        colors = [GREEN, GREEN, AMBER, GREEN, RED, MUTED, GREEN, AMBER, MUTED, GREEN]
        positions = [
            LEFT * 4.4 + UP * 1.45,
            LEFT * 2.7 + UP * 0.85,
            LEFT * 1.0 + UP * 1.55,
            RIGHT * 0.7 + UP * 0.75,
            RIGHT * 2.5 + UP * 1.35,
            RIGHT * 4.2 + UP * 0.65,
            LEFT * 3.4 + DOWN * 1.0,
            LEFT * 1.5 + DOWN * 0.75,
            RIGHT * 0.5 + DOWN * 1.25,
            RIGHT * 2.6 + DOWN * 0.7,
        ]
        for i, (color, pos) in enumerate(zip(colors, positions)):
            graph_nodes.append(artifact_node("evidence", str(i + 1), color, size=0.52, font_size=12).move_to(pos))
        nodes = VGroup(*graph_nodes)
        edges = VGroup(
            *[
                glow_line(graph_nodes[i].get_center(), graph_nodes[i + 1].get_center(), color=colors[i], width=2)
                for i in range(0, 5)
            ],
            *[
                glow_line(graph_nodes[i].get_center(), graph_nodes[i + 1].get_center(), color=colors[i], width=2)
                for i in range(6, 9)
            ],
        ).set_opacity(0.72)

        self.play(FadeIn(edges), LaggedStart(*[FadeIn(n) for n in nodes], lag_ratio=0.05), run_time=1.1)

        bars = VGroup(
            status_bar("coverage", 0.72, GREEN),
            status_bar("evidence", 0.58, CYAN),
            status_bar("freshness", 0.44, AMBER),
            status_bar("suitability", 0.81, VIOLET),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(bars, shift=UP * 0.2), run_time=0.8)
        note = tiny_text("not a magic safety score", font_size=22, color=RED).to_edge(RIGHT, buff=0.55).shift(DOWN * 1.7)
        self.play(Write(note), run_time=0.55)
        self.pause(0.8)


class S10EvidenceSurface(VCScene):
    def construct(self):
        safe_title(self, "Trust the evidence surface")

        graph = VGroup(
            artifact_node("requirement", "REQ", GOLD, size=0.65, font_size=14),
            artifact_node("code", "CODE", BLUE, size=0.65, font_size=14),
            artifact_node("test", "TEST", CYAN, size=0.65, font_size=14),
            artifact_node("evidence", "EV", GREEN, size=0.65, font_size=14),
        ).arrange(RIGHT, buff=0.55).shift(LEFT * 3.1 + UP * 0.95)
        graph_edges = VGroup(*[connect(graph[i], graph[i + 1], CYAN) for i in range(3)])
        self.play(FadeIn(graph), LaggedStart(*[Create(e) for e in graph_edges], lag_ratio=0.12), run_time=1.0)

        packages = VGroup(
            card("VQP 1", width=1.2, height=0.62, color=GREEN, font_size=16),
            card("VQP 2", width=1.2, height=0.62, color=AMBER, font_size=16),
            card("VQP 3", width=1.2, height=0.62, color=GREEN, font_size=16),
        ).arrange(DOWN, buff=0.18).shift(LEFT * 0.35 + DOWN * 0.65)
        self.play(TransformFromCopy(graph, packages), run_time=0.8)

        surface = field_card(
            "Evidence surface",
            ["current records", "stale records", "open anomalies", "human decisions"],
            width=3.8,
            height=2.6,
            color=GREEN,
        ).shift(RIGHT * 3.25 + DOWN * 0.25)
        arrows = VGroup(*[glow_arrow(p.get_right(), surface.get_left(), color=GREEN, width=2.4) for p in packages])
        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.08), FadeIn(surface), run_time=1.0)

        final = Text("Generate evidence we can inspect.", color=WHITE, font_size=30, weight=BOLD).to_edge(DOWN, buff=0.55)
        self.play(Write(final), run_time=0.65)
        self.pause(0.8)
