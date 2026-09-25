"""
Section 08 — Evidence Cards, Not Conversations.

Per the 2026-08-23 commentary the field list is a *visual*, not narration: the
table carries the names, the narrator points at it. So the card fills field by
field while the narrator talks about what those fields are for.

Then the append-only argument: nothing is edited, records accumulate, and the
history is the audit trail.
"""
from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from verification_compiler_video.pipeline import stage, style
from verification_compiler_video.pipeline.beats import Beat, BeatScene

FIELDS = [
    ("result", "PASS", style.GREEN),
    ("rationale", "clamp bounds input", style.WHITE),
    ("citations", "ICD §4.2 · TEST-04", style.CYAN),
    ("reviewer", "human:lpurdy", style.VIOLET),
    ("version", "code a81f3c", style.GOLD),
]


class S08EvidenceCards(BeatScene):
    section_id = "08_evidence_cards"
    title = "Evidence, not conversation"
    timing_dir = Path(__file__).resolve().parents[1] / "out" / "timing"

    def storyboard(self) -> list[Beat]:
        return [
            Beat("The output should not be a chat bubble", self.b00_bubble),
            Beat("It should be an evidence record", self.b01_card),
            Beat("And a record has fields", self.b02_fields_open),
            Beat("Every one of those fields answers a question you would otherwise",
                 self.b03_fill, note="13.3s — one field per question the narrator names"),
            Beat("And once that record exists, it should not be edited in place", self.b04_sealed),
            Beat("If the code changes, the old evidence does not disappear", self.b05_code_changes),
            Beat("It becomes stale", self.b06_stale),
            Beat("If the source document changes, links depending on that source",
                 self.b07_source_changes),
            Beat("If a human overrides a model result, both records stay visible",
                 self.b08_override),
            Beat("This is how you get an audit trail instead of a pile of confident text",
                 self.b09_trail),
            Beat("The point is not that every record is true forever", self.b10_not_forever),
            Beat("The point is that every record has provenance", self.b11_provenance),
        ]

    # ----------------------------------------------------------------- beats --
    def b00_bubble(self, ctx):
        text = style.caption_text("Looks good", color=style.MUTED)
        bub = RoundedRectangle(corner_radius=0.22, width=text.width + 0.8, height=1.15,
                               color=style.BLUE, stroke_width=2.4)
        bub.set_fill(style.PANEL, opacity=0.97)
        text.move_to(bub)
        grp = VGroup(bub, text).move_to(np.array([-3.9, 1.5, 0.0]))
        ctx.show(grp, tag="bubble", anim=lambda m: FadeIn(m, shift=DOWN * 0.15), run_time=0.5)

    def b01_card(self, ctx):
        ctx.play(self._owned["bubble"].animate.set_opacity(0.22), run_time=0.4)
        card = RoundedRectangle(corner_radius=0.12, width=7.4, height=3.5,
                                color=style.GREEN, stroke_width=2.8)
        card.set_fill(style.PANEL, opacity=0.98)
        card.move_to(np.array([1.1, -0.15, 0.0]))
        ctx.show(card, tag="card", anim=lambda m: FadeIn(m, scale=0.94), run_time=0.5)

    def b02_fields_open(self, ctx):
        head = style.label_text("evidence record", color=style.GREEN, size="tiny")
        head.next_to(self._owned["card"].get_top(), DOWN, buff=0.2)
        ctx.show(head, tag="cardhead", run_time=0.35)

    def b03_fill(self, ctx):
        """Thirteen seconds — one field lands per question the narrator asks."""
        card = self._owned["card"]
        rows = VGroup()
        for i, (name, value, colour) in enumerate(FIELDS):
            key = style.mono_text(name, color=style.MUTED, size="tiny")
            val = style.mono_text(value, color=colour, size="tiny")
            key.move_to(card.get_center() + UP * (0.95 - i * 0.5))
            key.align_to(np.array([card.get_left()[0] + 0.35, 0, 0]), LEFT)
            val.move_to(key.get_center())
            val.align_to(np.array([card.get_left()[0] + 2.5, 0, 0]), LEFT)
            row = VGroup(key, val)
            rows.add(row)
            ctx.play(FadeIn(row, shift=RIGHT * 0.14), run_time=0.35)
            ctx.hold(1.85)
        self._own("rows", rows)

    def b04_sealed(self, ctx):
        seal = VGroup(
            Circle(radius=0.4, color=style.GOLD, stroke_width=3).set_fill("#2A2105", opacity=0.95),
            style.mono_text("#", color=style.GOLD, size="field"),
        )
        seal.next_to(self._owned["card"], RIGHT, buff=0.3)
        ctx.show(seal, tag="seal", anim=lambda m: FadeIn(m, scale=0.75), run_time=0.45)
        ctx.hold(0.8)
        ctx.play(self._owned["card"].animate.set_stroke(style.GOLD, width=3.4), run_time=0.5)
        ctx.hold(0.7)
        tag = style.label_text("append only", color=style.GOLD, size="tiny")
        tag.next_to(self._owned["card"], DOWN, buff=0.22)
        ctx.show(tag, tag="append", run_time=0.4)

    def b05_code_changes(self, ctx):
        ctx.retire("bubble", run_time=0.25)
        chg = style.node("code", "a81f → c93d", size=2.3)
        chg.move_to(np.array([-4.6, 1.15, 0.0]))
        ctx.show(chg, tag="change", anim=lambda m: FadeIn(m, shift=RIGHT * 0.2), run_time=0.5)
        ctx.play(*style.highlight(chg, style.RED), run_time=0.4)

    def b06_stale(self, ctx):
        tag = style.label_text("STALE", color=style.RED)
        tag.next_to(self._owned["card"], UP, buff=0.22)
        ctx.show(tag, tag="stale", anim=lambda m: FadeIn(m, scale=1.2), run_time=0.4)
        ctx.play(self._owned["card"].animate.set_stroke(style.RED, width=3), run_time=0.3)

    def b07_source_changes(self, ctx):
        doc = style.node("source", "ICD", size=1.6)
        doc.move_to(np.array([-4.6, -1.3, 0.0]))
        ctx.show(doc, tag="doc", run_time=0.4)
        link = style.connect(doc, self._owned["card"], style.VIOLET, width=2.4)
        ctx.show(link, tag="doclink", anim=lambda m: Create(m), run_time=0.4)
        ctx.hold(0.5)
        ctx.play(link.animate.set_color(style.RED), run_time=0.4)
        tag = style.label_text("recheck", color=style.RED, size="tiny")
        tag.next_to(doc, DOWN, buff=0.2)
        ctx.show(tag, tag="recheck", run_time=0.35)

    def b08_override(self, ctx):
        # "doclink" points at the card, and the card is about to move — an arrow
        # left behind aims at the space where its target used to be.
        ctx.retire("stale", "recheck", "doclink", run_time=0.3)
        # Retire the header *before* the card shrinks. Doing it afterwards leaves
        # it sitting across the rows for the whole of the move.
        ctx.retire("cardhead", run_time=0.25)
        ctx.play(self._owned["card"].animate.scale(0.62).move_to(
            np.array([1.1, 1.35, 0.0])).set_opacity(0.5),
            self._owned["rows"].animate.scale(0.62).move_to(
                np.array([1.1, 1.35, 0.0])).set_opacity(0.5),
            run_time=0.55)
        newer = RoundedRectangle(corner_radius=0.12, width=4.6, height=1.5,
                                 color=style.GREEN, stroke_width=2.8)
        newer.set_fill(style.PANEL, opacity=0.98)
        newer.move_to(np.array([1.1, -1.05, 0.0]))
        lab = style.mono_text("v2 · human override", color=style.GREEN, size="tiny").move_to(newer)
        ctx.show(newer, lab, tag="v2", anim=lambda m: FadeIn(m, shift=UP * 0.2), run_time=0.5)

    def b09_trail(self, ctx):
        spine = Line(np.array([-1.6, 1.75, 0.0]), np.array([-1.6, -1.6, 0.0]),
                     color=style.GOLD, stroke_width=3)
        ctx.show(spine, tag="spine", anim=lambda m: Create(m), run_time=0.5)
        tag = style.label_text("audit trail", color=style.GOLD, size="tiny")
        tag.next_to(spine, LEFT, buff=0.25)
        ctx.show(tag, tag="trail", run_time=0.35)

    def b10_not_forever(self, ctx):
        ctx.play(self._owned["card"].animate.set_stroke(style.MUTED, width=2), run_time=0.45)

    def b11_provenance(self, ctx):
        tag = style.label_text("provenance", color=style.GREEN)
        stage.fit(tag, stage.CAPTION)
        ctx.show(tag, tag="prov", run_time=0.5)
        ctx.play(*style.highlight(self._owned["seal"], style.GOLD), run_time=0.4)
