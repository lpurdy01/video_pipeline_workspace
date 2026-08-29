"""
Self-test for the quality gate.

A checker nobody has watched fail is not a checker. This renders a scene built
from known defects — one per check — and asserts every one is caught. Run it
whenever the QA rules change; a check that stops firing here has silently
stopped protecting the video.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from verification_compiler_video.pipeline import qa, stage, style


class DeliberatelyBroken(qa.QASceneMixin, Scene):
    """Every frame of this scene is wrong on purpose."""

    def construct(self):
        self.camera.background_color = style.BG
        # The title lane only exists in a titled scene, and title_lane_intrusion
        # is skipped without one — so this scene has to have a title for that
        # planted defect to mean anything.
        self._title = style.title_text("SELFTEST")
        stage.fit(self._title, stage.TITLE)
        self.add(self._title)

        # 1. two texts straight on top of each other
        a = Text("OVERLAP ME", font_size=28, color=style.WHITE).move_to(UP * 1.5)
        b = Text("OVER ME TOO", font_size=28, color=style.GOLD).move_to(UP * 1.55)
        self.add(a, b)
        self.wait(1.0)

        # 2. text below the legible floor
        tiny = Text("far too small to read", font_size=7, color=style.WHITE).move_to(DOWN * 0.4)
        self.add(tiny)
        self.wait(1.0)

        # 3. text pushed outside the frame
        escapee = Text("off the edge", font_size=24, color=style.CYAN).move_to(RIGHT * 9.5)
        self.add(escapee)
        self.wait(1.0)

        # 4. an arrowhead landing in the middle of a word
        target = Text("PIERCED", font_size=26, color=style.WHITE).move_to(DOWN * 2.2)
        arrow = Arrow(LEFT * 4 + DOWN * 2.2, target.get_center(), color=style.RED, buff=0)
        self.add(target, arrow)
        self.wait(1.0)

        # 5. flicker — visible, gone, back again
        blink = Text("blink", font_size=26, color=style.VIOLET).move_to(UP * 0.2)
        self.add(blink)
        self.wait(0.6)
        self.remove(blink)
        self.wait(0.6)
        self.add(blink)
        self.wait(0.6)

        # 6. two nodes stacked on each other
        n1 = style.node("code", "ALPHA", size=1.6).move_to(LEFT * 4.6 + UP * 2.0)
        n2 = style.node("test", "BETA", size=1.6).move_to(LEFT * 4.3 + UP * 1.85)
        self.add(n1, n2)
        self.wait(1.0)

        # 7. a connector drawn straight through an unrelated node
        src = style.node("requirement", "SRC", size=1.5).move_to(LEFT * 5.4 + DOWN * 0.9)
        mid = style.node("code", "MID", size=1.5).move_to(LEFT * 1.9 + DOWN * 0.9)
        dst = style.node("evidence", "DST", size=1.5).move_to(RIGHT * 1.7 + DOWN * 0.9)
        self.add(src, mid, dst)
        self.add(style.connect(src, dst, color=style.CYAN))
        self.wait(1.0)

        # 8. a label that evaporates while its node stays
        ghost = style.node("review", "GHOST", size=1.7).move_to(RIGHT * 5.0 + UP * 1.2)
        self.add(ghost)
        self.wait(1.0)
        ghost.qa_label.set_opacity(0)
        self.wait(2.5)

        # 9. a plain shape drawn straight across text
        victim = Text("BURIED UNDER A BOX", font_size=26, color=style.WHITE)
        victim.move_to(RIGHT * 2.4 + DOWN * 2.6)
        slab = Rectangle(width=victim.width + 0.5, height=1.0,
                         color=style.VIOLET, stroke_width=3).move_to(victim)
        slab.set_fill(style.VIOLET, opacity=0.9)   # a filled slab, not a frame
        self.add(victim, slab)
        self.wait(1.2)

        # 10. content reaching into the reserved title lane
        intruder = Rectangle(width=3.0, height=1.4, color=style.GOLD,
                             stroke_width=3).move_to(UP * 3.4)
        self.add(intruder)
        self.wait(1.2)

        # 11. text with barely any contrast against the ground
        faint = Text("almost invisible", font_size=22, color="#0E1220")
        faint.move_to(LEFT * 3.2 + DOWN * 3.0)
        self.add(faint)
        self.wait(1.2)

        # 12. a node hanging off the edge of the frame
        runaway = style.node("evidence", "GONE", size=1.6).move_to(RIGHT * 7.6 + DOWN * 1.2)
        self.add(runaway)
        self.wait(1.2)

        # 13. a line struck straight through a word
        struck = Text("STRUCK THROUGH", font_size=24, color=style.WHITE)
        struck.move_to(RIGHT * 2.2 + UP * 3.0)
        rule = style.glow_arrow(struck.get_left() + LEFT * 1.2,
                                struck.get_right() + RIGHT * 1.2, color=style.CYAN)
        self.add(struck, rule)
        self.wait(1.2)

        # 14. two captions almost touching
        near_a = Text("first line", font_size=22, color=style.WHITE).move_to(LEFT * 5.0 + DOWN * 1.6)
        near_b = Text("second line", font_size=22, color=style.WHITE)
        near_b.next_to(near_a, DOWN, buff=0.04)
        self.add(near_a, near_b)
        self.wait(1.2)

        # 15. text fattened by a heavy stroke
        fat = Text("OVERSTROKED", font_size=26, color=style.GOLD).move_to(RIGHT * 4.6 + DOWN * 2.6)
        fat.set_stroke(style.GOLD, width=6)
        self.add(fat)
        self.wait(1.2)

        # 16. a connector drawn on top of the node it attaches to
        za = style.node("code", "FROM", size=1.4).move_to(LEFT * 2.4 + UP * 3.1)
        zb = style.node("test", "TO", size=1.4).move_to(RIGHT * 1.4 + UP * 3.1)
        self.add(za, zb)
        over = style.connect(za, zb, color=style.CYAN)
        Scene.add(self, over)          # bypass the layering rule, on purpose
        # bring_to_front is no longer enough to plant this: connectors carry
        # Z_EDGE, and the renderer's z_index sort outranks sibling order. Forcing
        # the z_index is now the only way to build the defect at all, which is
        # the point — the helper cannot produce it by accident any more.
        over.set_z_index(style.Z_NODE + 1, family=True)
        self.wait(1.5)

        # 17. a composition huddled into one corner of the stage
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.3)
        huddle = VGroup(*[style.node("code", "", size=0.5) for _ in range(6)])
        huddle.arrange_in_grid(rows=2, buff=0.25)
        huddle.move_to(np.array([4.9, -1.5, 0.0]))
        self.add(huddle)
        self.wait(4.0)
        self.remove(huddle)

        # 18. a shape's outline drawn through the middle of a word
        cut = Text("CUT THROUGH", font_size=22, color=style.WHITE)
        cut.move_to(LEFT * 4.6 + UP * 1.2)
        ring = Circle(radius=0.62, color=style.GOLD, stroke_width=3).move_to(cut)
        self.add(cut, ring)
        self.wait(1.4)

        # 19. a caption that flashes past faster than it can be read
        flash = Text("a long line nobody could possibly read this fast",
                     font_size=20, color=style.WHITE).move_to(DOWN * 3.0)
        self.add(flash)
        self.wait(0.4)
        self.remove(flash)

        # 20. a connector left bright while the nodes it joins are dimmed
        da = style.node("code", "", size=0.9).move_to(RIGHT * 1.0 + DOWN * 1.4)
        db = style.node("test", "", size=0.9).move_to(RIGHT * 4.2 + DOWN * 1.4)
        bright = style.connect(da, db, color=style.CYAN)
        self.add(da, db, bright)
        da.set_opacity(0.25)
        db.set_opacity(0.25)
        # Animated, not held: a static wait is frozen into two samples, and the
        # check needs three before it will believe a state was really on screen.
        marker = Dot(color=style.GOLD).move_to(RIGHT * 1.0 + DOWN * 2.6)
        self.add(marker)
        self.play(marker.animate.shift(RIGHT * 3.0), run_time=1.8)
        self.remove(da, db, bright, marker)

        # 21. a connector drawn in front and then dropped behind — a blink
        ta = style.node("code", "FRONT2", size=1.2).move_to(LEFT * 4.0 + DOWN * 2.4)
        tb = style.node("test", "TO2", size=1.2).move_to(LEFT * 1.0 + DOWN * 2.4)
        self.add(ta, tb)
        blink = style.connect(ta, tb, color=style.GREEN)
        Scene.add(self, blink)
        blink.set_z_index(style.Z_NODE + 1, family=True)
        self.wait(0.4)
        blink.set_z_index(style.Z_EDGE, family=True)
        self.wait(1.0)

        # 22. two words rendering as one at review size
        # 16pt on purpose. The type scale no longer offers it — that is the fix
        # for this defect class — so the plant has to reach past the scale to
        # keep proving the check still fires.
        merged = style._stamp(
            Text("every generation makes an obligation", color=style.MUTED, font_size=16),
            "every generation makes an obligation")
        merged.move_to(RIGHT * 3.0 + UP * 2.0)
        self.add(merged)
        self.wait(1.4)
        self.remove(merged)

        # 23. an arrow left pointing at empty space after its target moved
        anchor = style.node("code", "", size=0.9).move_to(LEFT * 5.6 + UP * 0.4)
        target = style.node("test", "", size=0.9).move_to(LEFT * 2.6 + UP * 0.4)
        self.add(anchor, target)
        hang = style.connect(anchor, target, color=style.RED)
        self.add(hang)
        self.wait(0.4)
        self.remove(target)               # the arrow stays, aimed at nothing
        drift = Dot(color=style.CYAN).move_to(LEFT * 5.6 + DOWN * 0.6)
        self.add(drift)
        self.play(drift.animate.shift(RIGHT * 2.0), run_time=1.6)
        self.remove(anchor, hang, drift)

        # 24. dead air — nothing changes for a long time. Needs something on
        # stage to be still: an empty frame is a cut, not a stalled one.
        self.add(style.node("code", "STILL", size=1.4).move_to(ORIGIN))
        self.wait(7.0)


EXPECTED = {"text_overlap", "text_too_small", "out_of_frame",
            "arrow_into_label", "flicker", "dead_air",
            "node_overlap", "edge_through_node", "label_orphaned",
            "shape_over_text", "title_lane_intrusion", "low_contrast", "node_off_frame",
            "stroke_over_text", "text_crowding", "text_stroked",
            "z_order_flip", "stage_imbalance", "outline_over_text",
            "text_too_brief", "partial_dim", "layer_transient", "words_merged",
            "arrow_to_nowhere"}


def main() -> int:
    geo = Path("out/qa/DeliberatelyBroken.geometry.json")
    if not geo.exists():
        print(f"render first:\n  manim -ql --disable_caching {__file__} DeliberatelyBroken")
        return 2
    violations = qa.check_all(geo)
    found = {v["check"] for v in violations}
    print(qa.report(violations))
    print()
    missing = EXPECTED - found
    spurious = found - EXPECTED
    for check in sorted(EXPECTED):
        print(f"  {'caught' if check in found else 'MISSED':>7}  {check}")
    if spurious:
        print(f"\n  unexpected: {sorted(spurious)}")
    if missing:
        print(f"\nSELFTEST FAIL — these checks did not fire: {sorted(missing)}")
        return 1
    print("\nSELFTEST PASS — every check fired on its planted defect")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
