"""
Candidate set C — show the real artifact.

Set A states the idea as a diagram, set B shows the mechanism in motion. Set C
puts the actual thing on screen: real trace rows, real JSON, a real terminal.
The bet is that a technical audience trusts a concrete artifact more than a
shape, and that seeing an actual VQP explains it faster than any metaphor.
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

MONO = "DejaVu Sans Mono"


class VCScene(Scene):
    def setup(self):
        self.camera.background_color = BG

    def pause(self, t: float = 0.5):
        self.wait(t)


def mono(text: str, size: int = 18, color: str = WHITE) -> Text:
    return Text(text, font=MONO, font_size=size, color=color)


def terminal(lines: list[tuple[str, str]], width: float = 6.4, height: float = 3.4,
             title: str = "", color: str = GRID) -> VGroup:
    """A terminal panel. `lines` is a list of (text, color)."""
    box = RoundedRectangle(corner_radius=0.08, width=width, height=height, color=color, stroke_width=2.0)
    box.set_fill("#04070F", opacity=0.99)
    bar = Rectangle(width=width, height=0.34, color=color, stroke_width=0)
    bar.set_fill("#0A1120", opacity=1).align_to(box, UP)
    dots = VGroup(*[Circle(radius=0.055, color=c, stroke_width=0).set_fill(c, opacity=0.85)
                    for c in (RED, AMBER, GREEN)]).arrange(RIGHT, buff=0.11)
    dots.move_to(bar.get_left() + RIGHT * 0.42)
    head = Text(title, font=MONO, font_size=15, color=MUTED).move_to(bar)
    parts = []
    for text, color in lines:
        if text.strip():
            parts.append(mono(text, 16, color))
        else:
            # blank line: an invisible spacer, since Text("") is not renderable
            parts.append(Rectangle(width=0.01, height=0.22, stroke_width=0, fill_opacity=0))
    body = VGroup(*parts).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
    # Pango strips leading whitespace, so indentation has to be re-applied by
    # shifting each line right by its original indent depth.
    char_w = 0.098  # approx advance width of the mono face at font_size 16
    for part, (text, _) in zip(parts, lines):
        indent = len(text) - len(text.lstrip(" "))
        if indent:
            part.shift(RIGHT * indent * char_w)
    body.next_to(bar, DOWN, buff=0.24).align_to(box.get_left() + RIGHT * 0.32, LEFT)
    return VGroup(box, bar, dots, head, body)


class C01ReviewQueue(VCScene):
    """Real pull requests pile up faster than any human column can drain them."""

    def construct(self):
        safe_title(self, "The queue is the story")

        merged = terminal(
            [
                ("feat: add rate limiter          +182 -4", CYAN),
                ("feat: retry with backoff        +96  -12", CYAN),
                ("test: limiter edge cases        +240 -0", CYAN),
                ("docs: update ICD section 4.2    +58  -6", CYAN),
                ("refactor: extract clamp()       +74  -91", CYAN),
                ("fix: off-by-one in window       +12  -12", CYAN),
            ],
            width=6.6,
            height=3.5,
            title="generated today",
            color=CYAN,
        ).shift(LEFT * 3.15 + DOWN * 0.35)
        self.play(FadeIn(merged, shift=RIGHT * 0.15), run_time=0.9)

        reviewed = terminal(
            [
                ("feat: add rate limiter    reviewing…", GOLD),
                ("", MUTED),
                ("", MUTED),
                ("", MUTED),
                ("", MUTED),
                ("", MUTED),
            ],
            width=5.6,
            height=3.5,
            title="actually verified today",
            color=GOLD,
        ).shift(RIGHT * 3.55 + DOWN * 0.35)
        self.play(FadeIn(reviewed, shift=LEFT * 0.15), run_time=0.7)

        counter_a = Text("6", color=CYAN, font_size=46, weight=BOLD).next_to(merged, UP, buff=0.16)
        counter_b = Text("1", color=GOLD, font_size=46, weight=BOLD).next_to(reviewed, UP, buff=0.16)
        self.play(FadeIn(counter_a, scale=0.7), FadeIn(counter_b, scale=0.7), run_time=0.5)

        note = Text("and tomorrow it is sixty.", color=RED, font_size=26, weight=BOLD)
        note.to_edge(DOWN, buff=0.3)
        self.play(Write(note), run_time=0.6)
        self.pause(0.9)


class C02TranscriptVsRecord(VCScene):
    """The literal transcript beside the literal record it fails to be."""

    def construct(self):
        safe_title(self, "One of these can be audited")

        chat = terminal(
            [
                ("> does clamp() satisfy REQ-17?", MUTED),
                ("", WHITE),
                ("Yes — the function bounds the", WHITE),
                ("input to the configured range,", WHITE),
                ("so the requirement is met.", WHITE),
                ("", WHITE),
                ("Let me know if you want tests!", MUTED),
            ],
            width=6.0,
            height=3.9,
            title="chat transcript",
            color=BLUE,
        ).shift(LEFT * 3.35 + DOWN * 0.4)
        self.play(FadeIn(chat), run_time=0.8)

        record = terminal(
            [
                ('{', MUTED),
                ('  "requirement": "REQ-17",', GOLD),
                ('  "code_unit": "clamp@a81f3c",', BLUE),
                ('  "test": "TEST-04",', CYAN),
                ('  "verdict": "PASS",', GREEN),
                ('  "reviewer": "human:lpurdy",', VIOLET),
                ('  "authority": "accepted"', GREEN),
                ('}', MUTED),
            ],
            width=6.0,
            height=3.9,
            title="evidence record",
            color=GREEN,
        ).shift(RIGHT * 3.35 + DOWN * 0.4)
        self.play(FadeIn(record), run_time=0.8)

        x = VGroup(
            Line(UL * 0.32, DR * 0.32, color=RED, stroke_width=6),
            Line(UR * 0.32, DL * 0.32, color=RED, stroke_width=6),
        ).next_to(chat, UP, buff=0.1)
        check = Text("✓", color=GREEN, font_size=42, weight=BOLD).next_to(record, UP, buff=0.05)
        self.play(Create(x), FadeIn(check, scale=0.7), run_time=0.6)
        self.pause(0.9)


class C03TraceTable(VCScene):
    """The trace matrix that safety-critical projects already maintain."""

    def construct(self):
        safe_title(self, "This table already exists")

        headers = ["requirement", "code", "test", "result", "accepted by"]
        rows = [
            ["REQ-17", "clamp() a81f", "TEST-04", "PASS", "lpurdy"],
            ["REQ-18", "window() c93d", "TEST-07", "PASS", "lpurdy"],
            ["REQ-19", "retry() 4b2e", "TEST-11", "FAIL", "—"],
            ["REQ-20", "—", "—", "—", "—"],
        ]
        col_x = [-5.0, -2.6, -0.2, 1.7, 3.7]

        head_group = VGroup()
        for text, x in zip(headers, col_x):
            t = mono(text, 18, GOLD).move_to(RIGHT * x + UP * 1.55, aligned_edge=LEFT)
            head_group.add(t)
        rule = Line(LEFT * 5.3, RIGHT * 5.6, color=GRID, stroke_width=2).next_to(head_group, DOWN, buff=0.22)
        self.play(FadeIn(head_group), Create(rule), run_time=0.7)

        row_groups = VGroup()
        for i, row in enumerate(rows):
            rg = VGroup()
            for text, x in zip(row, col_x):
                color = WHITE
                if text == "FAIL":
                    color = RED
                elif text == "PASS":
                    color = GREEN
                elif text == "—":
                    color = MUTED
                rg.add(mono(text, 17, color).move_to(RIGHT * x + UP * (0.85 - i * 0.65), aligned_edge=LEFT))
            row_groups.add(rg)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.12) for r in row_groups], lag_ratio=0.18), run_time=1.1)

        gap = SurroundingRectangle(row_groups[3], color=RED, stroke_width=2.6, buff=0.14)
        gap_tag = mono("nothing links to it", 18, RED).next_to(gap, DOWN, buff=0.22)
        self.play(Create(gap), FadeIn(gap_tag), run_time=0.6)

        note = tiny_text("hand-maintained, always stale", font_size=21, color=AMBER).to_edge(DOWN, buff=0.28)
        self.play(Write(note), run_time=0.55)
        self.pause(0.8)


class C04TableLiftsToGraph(VCScene):
    """The same rows, re-read as edges."""

    def construct(self):
        safe_title(self, "The table was a graph in disguise")

        row = VGroup(
            mono("REQ-17", 19, GOLD),
            mono("clamp() a81f", 19, BLUE),
            mono("TEST-04", 19, CYAN),
            mono("PASS", 19, GREEN),
        ).arrange(RIGHT, buff=1.15).shift(UP * 1.9)
        self.play(FadeIn(row), run_time=0.6)

        nodes = VGroup(
            artifact_node("requirement", "REQ-17", GOLD, size=0.85, font_size=14),
            artifact_node("code", "clamp", BLUE, size=0.85, font_size=14),
            artifact_node("test", "TEST-04", CYAN, size=0.85, font_size=13),
            artifact_node("evidence", "PASS", GREEN, size=0.85, font_size=14),
        )
        for n, src in zip(nodes, row):
            n.move_to(src.get_center() + DOWN * 2.2)
        self.play(LaggedStart(*[TransformFromCopy(row[i], nodes[i]) for i in range(4)], lag_ratio=0.12), run_time=1.1)

        edges = VGroup(*[connect(nodes[i], nodes[i + 1], color=MUTED) for i in range(3)])
        self.play(LaggedStart(*[Create(e) for e in edges], lag_ratio=0.12), run_time=0.7)

        extra = artifact_node("requirement", "REQ-22", GOLD, size=0.85, font_size=13)
        extra.move_to(nodes[1].get_center() + DOWN * 1.85)
        link = glow_arrow(extra.get_top(), nodes[1].get_bottom(), color=GOLD, width=2.6)
        self.play(FadeIn(extra, scale=0.9), Create(link), run_time=0.7)

        note = tiny_text("rows cannot express this. edges can.", font_size=21, color=WHITE).to_edge(DOWN, buff=0.28)
        self.play(Write(note), run_time=0.55)
        self.pause(0.8)


class C05TwoCompilers(VCScene):
    """gcc above, vc below. Same posture, different output."""

    def construct(self):
        safe_title(self, "Two compilers")

        gcc = terminal(
            [
                ("$ gcc -c limiter.c -o limiter.o", WHITE),
                ("", WHITE),
                ("  parse  →  AST", MUTED),
                ("  walk   →  IR", MUTED),
                ("  emit   →  limiter.o", GREEN),
            ],
            width=6.1,
            height=2.55,
            title="known",
            color=BLUE,
        ).shift(LEFT * 3.4 + UP * 1.15)
        self.play(FadeIn(gcc, shift=DOWN * 0.12), run_time=0.8)

        vc = terminal(
            [
                ("$ vc build --graph project.json", WHITE),
                ("", WHITE),
                ("  parse  →  artifact graph", MUTED),
                ("  walk   →  bounded subgraphs", MUTED),
                ("  emit   →  17 VQPs", GREEN),
            ],
            width=6.1,
            height=2.55,
            title="proposed",
            color=VIOLET,
        ).shift(LEFT * 3.4 + DOWN * 1.85)
        self.play(FadeIn(vc, shift=UP * 0.12), run_time=0.8)

        out = VGroup(*[
            card(f"VQP-{i:02d}", width=1.9, height=0.5, color=GREEN, font_size=17)
            for i in range(1, 6)
        ]).arrange(DOWN, buff=0.17).shift(RIGHT * 4.3 + DOWN * 0.35)
        more = tiny_text("… 12 more", font_size=18, color=MUTED).next_to(out, DOWN, buff=0.15)
        arrow = glow_arrow(vc.get_right(), out.get_left(), color=GREEN, width=3)
        self.play(Create(arrow), LaggedStart(*[FadeIn(o, shift=LEFT * 0.12) for o in out], lag_ratio=0.1),
                  FadeIn(more), run_time=1.0)

        note = tiny_text("deterministic: same graph, same 17 packages", font_size=21, color=WHITE)
        note.to_edge(DOWN, buff=0.22)
        self.play(Write(note), run_time=0.55)
        self.pause(0.8)


class C06VQPDocument(VCScene):
    """The package, as a document you could actually open."""

    def construct(self):
        safe_title(self, "Open one and look")

        doc = terminal(
            [
                ('{', MUTED),
                ('  "vqp_id": "VQP-04",', WHITE),
                ('  "question": "does clamp() satisfy REQ-17?",', GOLD),
                ('  "code_unit": {', BLUE),
                ('     "symbol": "clamp", "hash": "a81f3c" },', BLUE),
                ('  "requirements": ["REQ-17", "REQ-22"],', GOLD),
                ('  "source_region": "ICD §4.2 lines 88-114",', VIOLET),
                ('  "tests": ["TEST-04"],', CYAN),
                ('  "results": ["run-2291: PASS"],', GREEN),
                ('  "review_instructions": "cite every claim"', WHITE),
                ('}', MUTED),
            ],
            width=8.4,
            height=4.6,
            title="VQP-04.json",
            color=GREEN,
        ).shift(LEFT * 1.15 + DOWN * 0.35)
        self.play(FadeIn(doc), run_time=1.0)

        callouts = [
            ("the question", GOLD, 1.30),
            ("the evidence", CYAN, -0.35),
            ("the rules", WHITE, -1.35),
        ]
        tags = VGroup()
        for text, color, y in callouts:
            t = tiny_text(text, font_size=19, color=color).move_to(RIGHT * 4.55 + UP * y)
            tags.add(t)
        self.play(LaggedStart(*[FadeIn(t, shift=LEFT * 0.15) for t in tags], lag_ratio=0.15), run_time=0.8)

        note = tiny_text("everything needed, nothing else", font_size=21, color=WHITE).to_edge(DOWN, buff=0.22)
        self.play(Write(note), run_time=0.55)
        self.pause(0.8)


class C07IdenticalSchema(VCScene):
    """Two returned records. Diff them: only the last two fields move."""

    def construct(self):
        safe_title(self, "Diff the two answers")

        left = terminal(
            [
                ('"vqp_id": "VQP-04",', MUTED),
                ('"verdict": "PASS",', GREEN),
                ('"rationale": "clamp bounds…",', WHITE),
                ('"citations": ["ICD §4.2"],', WHITE),
                ('"reviewer": "model:g3.1-pro",', CYAN),
                ('"authority": "developmental"', CYAN),
            ],
            width=6.0,
            height=3.4,
            title="nightly CI run",
            color=CYAN,
        ).shift(LEFT * 3.35 + DOWN * 0.35)

        right = terminal(
            [
                ('"vqp_id": "VQP-04",', MUTED),
                ('"verdict": "PASS",', GREEN),
                ('"rationale": "clamp bounds…",', WHITE),
                ('"citations": ["ICD §4.2"],', WHITE),
                ('"reviewer": "human:lpurdy",', GOLD),
                ('"authority": "accepted"', GOLD),
            ],
            width=6.0,
            height=3.4,
            title="certification pass",
            color=GOLD,
        ).shift(RIGHT * 3.35 + DOWN * 0.35)

        self.play(FadeIn(left), FadeIn(right), run_time=0.9)

        same = SurroundingRectangle(VGroup(left[4][1], left[4][2], left[4][3]), color=GREEN,
                                    stroke_width=2.2, buff=0.1)
        same2 = SurroundingRectangle(VGroup(right[4][1], right[4][2], right[4][3]), color=GREEN,
                                     stroke_width=2.2, buff=0.1)
        same_tag = tiny_text("identical", font_size=19, color=GREEN).next_to(same, UP, buff=0.12)
        self.play(Create(same), Create(same2), FadeIn(same_tag), run_time=0.6)

        diff = SurroundingRectangle(VGroup(left[4][4], left[4][5]), color=RED, stroke_width=2.2, buff=0.1)
        diff2 = SurroundingRectangle(VGroup(right[4][4], right[4][5]), color=RED, stroke_width=2.2, buff=0.1)
        diff_tag = tiny_text("only this differs", font_size=19, color=RED).next_to(diff, DOWN, buff=0.14)
        self.play(Create(diff), Create(diff2), FadeIn(diff_tag), run_time=0.6)
        self.pause(0.9)


class C08HashMismatch(VCScene):
    """The record is fine. The code moved. That is what staleness actually is."""

    def construct(self):
        safe_title(self, "Staleness is a hash mismatch")

        rec = terminal(
            [
                ('"verdict": "PASS",', GREEN),
                ('"code_hash": "a81f3c",', GOLD),
                ('"reviewed": "2026-08-14"', MUTED),
            ],
            width=5.4,
            height=2.0,
            title="evidence record",
            color=GREEN,
        ).shift(LEFT * 3.3 + UP * 1.15)
        self.play(FadeIn(rec), run_time=0.7)

        diff = terminal(
            [
                ("- if (v > hi) v = hi;", RED),
                ("+ if (v >= hi) v = hi;", GREEN),
            ],
            width=5.4,
            height=1.6,
            title="git diff limiter.c",
            color=BLUE,
        ).shift(RIGHT * 3.4 + UP * 1.25)
        self.play(FadeIn(diff, shift=LEFT * 0.15), run_time=0.7)

        now = mono('code_hash now: c93d0e', 21, RED).shift(RIGHT * 3.4 + DOWN * 0.35)
        was = mono('record says:   a81f3c', 21, GOLD).next_to(now, UP, buff=0.22)
        self.play(FadeIn(was), FadeIn(now), run_time=0.6)

        verdict = Text("STALE — not wrong, just no longer about this code",
                       color=RED, font_size=25, weight=BOLD)
        verdict.to_edge(DOWN, buff=0.5)
        self.play(rec.animate.set_opacity(0.45), Write(verdict), run_time=0.8)
        self.pause(0.9)


class C09CIOutput(VCScene):
    """The readiness metric as it would actually land in a CI log."""

    def construct(self):
        safe_title(self, "What lands in CI")

        out = terminal(
            [
                ("$ vc verify --all", WHITE),
                ("", WHITE),
                ("REQ-17  clamp()     PASS   evidence current", GREEN),
                ("REQ-18  window()    PASS   evidence current", GREEN),
                ("REQ-19  retry()     FAIL   test failing", RED),
                ("REQ-20  —           GAP    no code linked", AMBER),
                ("REQ-21  parse()     STALE  code changed", AMBER),
                ("", WHITE),
                ("VRM 0.62   (18/29 requirements covered)", GOLD),
                ("2 orphan artifacts   1 open anomaly", MUTED),
            ],
            width=8.6,
            height=4.5,
            title="ci · nightly",
            color=GRID,
        ).shift(DOWN * 0.45)
        self.play(FadeIn(out), run_time=1.0)

        box = SurroundingRectangle(out[4][8], color=GOLD, stroke_width=2.6, buff=0.12)
        self.play(Create(box), run_time=0.5)

        note = Text("a number you can move tomorrow", color=WHITE, font_size=25, weight=BOLD)
        note.to_edge(DOWN, buff=0.22)
        self.play(Write(note), run_time=0.6)
        self.pause(0.9)


class C10DecisionSurface(VCScene):
    """The human sits at the end, and the open gaps stay visible."""

    def construct(self):
        safe_title(self, "The last signature is human")

        queue = VGroup(
            card("VQP-04  ready", width=3.3, height=0.56, color=GREEN, font_size=18),
            card("VQP-07  ready", width=3.3, height=0.56, color=GREEN, font_size=18),
            card("VQP-11  uncertain", width=3.3, height=0.56, color=AMBER, font_size=18),
            card("VQP-19  no evidence", width=3.3, height=0.56, color=RED, font_size=18),
        ).arrange(DOWN, buff=0.24).shift(LEFT * 3.75 + DOWN * 0.3)
        self.play(LaggedStart(*[FadeIn(q, shift=RIGHT * 0.15) for q in queue], lag_ratio=0.14), run_time=1.0)

        desk = RoundedRectangle(corner_radius=0.12, width=4.6, height=3.3, color=GOLD, stroke_width=2.6)
        desk.set_fill(PANEL, opacity=0.97).shift(RIGHT * 3.35 + DOWN * 0.3)
        desk_head = label_text("human decision", font_size=22, color=GOLD).next_to(desk.get_top(), DOWN, buff=0.22)
        options = VGroup(
            mono("[ accept ]", 20, GREEN),
            mono("[ reject ]", 20, RED),
            mono("[ send back ]", 20, AMBER),
        ).arrange(DOWN, buff=0.3).next_to(desk_head, DOWN, buff=0.4)
        self.play(FadeIn(desk), FadeIn(desk_head), FadeIn(options), run_time=0.8)

        flow = VGroup(*[glow_arrow(q.get_right(), desk.get_left(), color=GREEN, width=2.2) for q in queue[:2]])
        self.play(LaggedStart(*[Create(f) for f in flow], lag_ratio=0.12), run_time=0.6)

        held = SurroundingRectangle(VGroup(queue[2], queue[3]), color=RED, stroke_width=2.4, buff=0.14)
        held_tag = tiny_text("still open — and still visible", font_size=19, color=RED)
        held_tag.next_to(held, DOWN, buff=0.18)
        self.play(Create(held), FadeIn(held_tag), run_time=0.6)

        final = Text("Generate evidence we can inspect.", color=WHITE, font_size=26, weight=BOLD)
        final.to_edge(DOWN, buff=0.2)
        self.play(Write(final), run_time=0.65)
        self.pause(0.8)
