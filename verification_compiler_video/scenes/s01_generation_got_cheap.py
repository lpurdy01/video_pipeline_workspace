"""
Section 01 — Cold Open: Generation Got Cheap.

The longest section (153s, 33 narration lines) and the one that has to earn the
viewer. Reworked 2026-08-28 against the new cold open.

The old version *built* to the flood over thirty-six seconds: one square, a
review above it, then multiplication, then rain. The new open has to **start** in
the flood — motion in frame one — put the stakes on screen by fourteen seconds,
and reach the thesis by thirty-four. The argument is still a shape:

    flood -> the reason it matters (a plane, a device) -> the wall it cannot
    cross -> a gate in the wall -> the compiler that gets it through

Built from the beat proposals in out/storyboard/01_beat_proposals.md, then
rewritten for the locked cold open in drafts/script.md.
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

# The wall the flood cannot cross, in the cold open. Right of centre, so the
# pile-up has room to be genuinely large before it hits.
WALL_X = 2.35


# ------------------------------------------------------------- flood tiles --
# Wordless artifact tiles. No label means no legibility risk in a flood, but the
# *shape and colour* still carry the grammar — the cold open is where a viewer
# learns it, four seconds in, off the words "code, tests, docs, a migration plan".
# Tiles are filled with their own colour, not with the panel black the rest of
# the video uses. A flood built from 2px outlines on a near-black ground reads as
# scattered confetti at 480p, however many tiles are in it — the density that is
# supposed to be the whole point of the first eight seconds simply does not
# arrive. A tinted body at 0.18 costs nothing and makes the frame full.
TILE_FILL = 0.18


def chip(color: str, size: float = 0.42) -> VGroup:
    """Code: a square."""
    box = Square(side_length=size, color=color, stroke_width=2.4)
    box.set_fill(color, opacity=TILE_FILL)
    return VGroup(box)


def dot(color: str, r: float = 0.21) -> Circle:
    """Test: a circle."""
    c = Circle(radius=r, color=color, stroke_width=2.4)
    c.set_fill(color, opacity=TILE_FILL)
    return c


def doc(color: str = style.VIOLET, size: float = 0.42) -> VGroup:
    """Source document: a tall slice."""
    d = RoundedRectangle(corner_radius=0.05, width=size * 0.78, height=size * 1.15,
                         color=color, stroke_width=2.4)
    d.set_fill(color, opacity=TILE_FILL)
    return VGroup(d)


def rec(color: str = style.GREEN, size: float = 0.42) -> VGroup:
    """Evidence record: a wide card."""
    r = RoundedRectangle(corner_radius=0.07, width=size * 1.3, height=size * 0.72,
                         color=color, stroke_width=2.4)
    r.set_fill(color, opacity=TILE_FILL)
    return VGroup(r)


# ----------------------------------------------------------- the pictogram --
def brackets(mob: Mobject, color: str = style.VIOLET, arm: float = 0.28,
             width: float = 5.5, pad: float = 0.20) -> VGroup:
    """
    Four corner marks around something, as a cursor.

    A ring would be simpler and is wrong: in this grammar a circle is a test, so
    a violet circle drawn round a code square says "a test", which is not what
    marking one tile out of sixty is supposed to say. Corner brackets are not a
    node shape and cannot be read as one.
    """
    x0, x1 = mob.get_left()[0] - pad, mob.get_right()[0] + pad
    y0, y1 = mob.get_bottom()[1] - pad, mob.get_top()[1] + pad
    g = VGroup()
    for cx, cy, sx, sy in ((x0, y1, 1, 1), (x1, y1, -1, 1),
                           (x0, y0, 1, -1), (x1, y0, -1, -1)):
        mark = VMobject(color=color, stroke_width=width)
        mark.set_points_as_corners([
            np.array([cx, cy - sy * arm, 0.0]),
            np.array([cx, cy, 0.0]),
            np.array([cx + sx * arm, cy, 0.0]),
        ])
        g.add(mark)
    return g


def flood_tile(rng: random.Random, size: float = 0.42) -> VGroup:
    """
    One tile of the flood, drawn in the grammar.

    Picking a random *colour* for a square is how the flood ended up full of
    cyan and green squares — two combinations the grammar has already spent, on
    tests (cyan circles) and evidence (green records). A viewer who has just been
    taught the shapes in the first eight seconds is then shown thirty tiles that
    contradict them. The flood is a mix of kinds, not a mix of colours.
    """
    r = rng.random()
    if r < 0.46:
        tile, kind = chip(style.BLUE, size), "code"
    elif r < 0.70:
        tile, kind = VGroup(dot(style.CYAN, size * 0.5)), "test"
    elif r < 0.87:
        tile, kind = doc(style.VIOLET, size), "source"
    else:
        tile, kind = rec(style.GREEN, size), "evidence"
    tile.tile_kind = kind
    return tile


def plane(size: float = 1.6, color: str = style.WHITE) -> VGroup:
    """
    A side-view aircraft silhouette, nose to the right.

    Deliberately not a `style.node`: it is not an artifact, it is the thing the
    artifacts end up inside. So it carries no grammar colour until it fails, and
    then it carries RED like every other failure in this video.
    """
    outline = [
        (1.00, 0.02), (0.78, 0.16), (-0.30, 0.18), (-0.52, 0.18),
        (-0.78, 0.60), (-0.94, 0.60), (-1.00, 0.14), (-1.02, -0.10),
        (-0.60, -0.14), (-0.30, -0.14), (-0.46, -0.62), (-0.16, -0.62),
        (0.18, -0.16), (0.80, -0.12),
    ]
    body = Polygon(*[np.array([x, y, 0.0]) * size for x, y in outline],
                   color=color, stroke_width=3.6)
    body.set_fill(style.PANEL, opacity=0.95)
    return VGroup(body)


def heartbeat(width: float, height: float = 0.42, cycles: int = 2,
              color: str = style.GREEN) -> VMobject:
    """
    A device output trace — the medical half of the stakes, in the same line
    idiom as everything else on this stage.

    The point of drawing it is that it can *stop*, which is a failure a viewer
    reads instantly and which does not need a body attached to it.
    """
    profile = [0.0, 0.0, 0.12, 0.0, -0.20, 1.0, -0.38, 0.0, 0.16, 0.0]
    step = width / (cycles * len(profile))
    x = -width / 2
    pts = []
    for _ in range(cycles):
        for p in profile:
            pts.append(np.array([x, p * height, 0.0]))
            x += step
    m = VMobject(color=color, stroke_width=4.5)
    m.set_points_as_corners(pts)
    return m


class S01GenerationGotCheap(BeatScene):
    section_id = "01_generation_got_cheap"
    # No section title. Every other section opens on one; this one opens on the
    # flood already falling. A card reading "Generation got cheap" as frame one
    # is a build, and it spends the first half-second of the video telling the
    # viewer the thing the next eight seconds are supposed to show them.
    title = ""
    timing_dir = Path(__file__).resolve().parents[1] / "out" / "timing"

    def storyboard(self) -> list[Beat]:
        return [
            # -- the hook: eight seconds, and it opens in motion ---------------
            Beat("Your agent wrote four thousand lines this week", self.b00_flood_arrives,
                 note="8.1s — the flood is falling before the first word lands, then "
                      "one typed family per named artifact"),
            Beat("How much of it did you read", self.b01_one_reader),
            # -- the stakes, on screen by 0:14 --------------------------------
            Beat("There is a whole category of software that AI is not allowed to write",
                 self.b02_plane_level,
                 note="the pictogram: a plane flying level, code streaming into it"),
            Beat("Aircraft. Medical devices.", self.b03_plane_goes_in,
                 note="hard and fast — the dive, the impact, the device trace stopping"),
            Beat("Not because the models are bad at it", self.b04_code_is_fine),
            Beat("Because nobody can check the work fast enough", self.b05_wall),
            Beat("AI made writing code cheap", self.b06_cheap_not_trusted),
            Beat("And that is a verification problem", self.b07_solvable,
                 note="the thesis at 0:34 — a gate opens in the wall"),
            # -- the industry-scale version of the same picture ---------------
            Beat("This is not a thought experiment, either", self.b08_industry),
            Beat("Pull requests arrive faster than any team can actually read them",
                 self.b09_reviewers_struck),
            Beat("The pace becomes the product, and review is the thing that gets crushed",
                 self.b10_buried),
            # -- what serious software is -------------------------------------
            Beat("Because serious software is not just software that runs", self.b11_clean_slate),
            Beat("Serious software is software where someone can explain", self.b12_build_chain,
                 note="15.3s line — one node per clause the narrator names"),
            # -- the two worlds ------------------------------------------------
            Beat("Let me be concrete about what I mean", self.b13_divide),
            Beat("In one of them, quality is a business problem", self.b14_web_stack),
            Beat("A web application has to be reliable enough that customers do not leave",
                 self.b15_revenue),
            Beat("If something breaks on Monday, you ship a fix on Tuesday", self.b16_break_fix),
            Beat("In the other one, software flies aircraft", self.b17_focus_right),
            Beat("It keeps satellites talking to the ground", self.b18_second_chain),
            Beat("It decides how hard your car brakes", self.b19_third_chain),
            Beat("That software is certified before it is allowed to run", self.b20_seal,
                 note="10.4s line — the seal draws, then who is accountable, and they stay"),
            # -- the bottleneck ------------------------------------------------
            Beat("AI has made generation faster", self.b21_pile_up),
            Beat("It has not automatically made verification faster", self.b22_static),
            Beat("So the bottleneck moves", self.b23_push_in),
            Beat("Not to the editor", self.b24_not_editor),
            Beat("Not to the model", self.b25_not_model),
            Beat("To trust", self.b26_trust),
            # -- the answer ----------------------------------------------------
            Beat("And that is why I have been thinking about something I call a Verification Compiler",
                 self.b27_compiler),
            Beat("The goal is not to bring AI into safety-critical work for the sake of it",
                 self.b28_frame_turns),
            Beat("The goal is to automate the verification scaffolding", self.b29_fold,
                 note="9.5s line — scaffolding snaps on, then folds into the package"),
            Beat("It is a process, not a shortcut", self.b30_through_gate),
            Beat("Or, less formally", self.b31_beat, lead=0.55),
            Beat("a compiler for trust", self.b32_title),
        ]

    # ============================================================ the hook ====
    def b00_flood_arrives(self, ctx):
        """
        Eight seconds, and the first two are the whole retention problem.

        No build, no title, no single square: the code is already falling when
        the narrator says "four thousand lines". Then the four families named in
        the second half of the line land as four shapes, which is how the grammar
        gets taught before the viewer knows they are being taught anything.
        """
        # The flood overflows the frame's normal bounds, because that is what a
        # flood does. This section carries no title, so the title lane is
        # provably empty for its whole length and the open can run full-bleed —
        # and the frame settling back into its usual letterbox at b02 is the cut
        # from "too much of it" to "here is the thing that matters".
        ctx.lopsided("the open deliberately fills the frame top to bottom")
        ctx.waive("title_lane_intrusion",
                  "the cold open runs full-bleed; this section sets no title, so "
                  "the lane is unused for its whole length")
        OPEN = stage.Region("open", stage.STAGE.left, stage.STAGE.right,
                            stage.STAGE.bottom, stage.TITLE.top - 0.12)
        rng = random.Random(4000)
        placed: list[Mobject] = []

        def wave(maker, count, region=OPEN, pad=0.22):
            group = VGroup()
            for pos in stage.free_points(count, placed, rng, region=region, pad=pad):
                m = maker()
                m.move_to(pos)
                group.add(m)
                placed.append(m)
            return group

        code = wave(lambda: chip(style.BLUE, 0.42), 32)
        self._own("code_rain", code)
        # Falling, not fading: the shift is what makes frame one read as motion.
        #
        # The first half-second carries the whole retention problem, so the
        # opening slam lands twelve tiles in 0.45s rather than easing 26 in over
        # a second and a half. At the gentler rate the frame at t=0.5 held eight
        # faint outlines, which is a video that has not started yet.
        # Every other tile, not the first fifteen. free_points places tiles in
        # order and the first run of them lands in whatever corner it found room
        # in first, so `code[:15]` slammed a cluster into one part of the frame
        # and left the rest black. Parity spreads the slam over the whole width.
        slam, rest = code[::2], code[1::2]
        ctx.play(LaggedStart(*[FadeIn(c, shift=DOWN * 1.1) for c in slam],
                             lag_ratio=0.05), run_time=0.45)
        ctx.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.85) for c in rest],
                             lag_ratio=0.04), run_time=0.95)
        ctx.hold(0.5)

        # "Code," — the rain the viewer is already looking at *is* the code.
        ctx.play(*[c[0].animate.set_stroke(style.BLUE, width=3.4) for c in code],
                 run_time=0.35)
        ctx.hold(0.45)

        named = [
            ("tests", lambda: dot(style.CYAN, 0.21), 13),
            ("docs", lambda: doc(style.VIOLET, 0.42), 13),
            ("plan", lambda: rec(style.GREEN, 0.42), 12),
        ]
        families = VGroup()
        for tag, maker, count, in named:
            group = wave(maker, count)
            families.add(group)
            ctx.play(LaggedStart(*[FadeIn(m, shift=DOWN * 0.55) for m in group],
                                 lag_ratio=0.05), run_time=0.8)
            ctx.hold(0.5)
        self._own("families", families)

        # It keeps arriving after the sentence ends. A frozen flood is not a flood.
        ctx.play(VGroup(code, families).animate.shift(DOWN * 0.22), run_time=0.7)

    def b01_one_reader(self, ctx):
        """One person, under all of it."""
        ctx.waive("title_lane_intrusion",
                  "the open's flood is still on screen, dimmed, and still full-bleed")
        flood = VGroup(self._owned["code_rain"], self._owned["families"])
        reader = style.node("review", "", size=1.05)
        reader.move_to(np.array([0.0, stage.STAGE.bottom + 0.62, 0.0]))
        self._own("reader", reader)
        # Hard dim, not a polite one. At 0.42 the flood was still the brightest
        # thing on the frame and the one person under it did not read as alone.
        ctx.play(flood.animate.set_opacity(0.26), FadeIn(reader, scale=1.35), run_time=0.6)
        # And the line answers itself: one tile out of sixty gets a cursor on it.
        # A lone reviewer under a dimmed flood says "this is a lot"; a cursor
        # sitting on exactly one square says how much of it was read.
        read = self._owned["code_rain"][3]
        cursor = brackets(read, color=style.VIOLET)
        self._own("cursor", cursor)
        # The tile keeps the flood's dim. Re-lighting it in the play after the
        # group dim made the geometry recorder see it leave and come back — the
        # group was wrapped for the dim animation and the child was animated
        # out from under the wrapper. The ring is what marks it; it does not
        # need the tile to be brighter than everything it is being counted
        # against, and arguably it should not be.
        ctx.play(*style.highlight(reader, style.VIOLET),
                 Create(cursor), run_time=0.55)
        ctx.hold(0.6)

    # ========================================================== the stakes ====
    def b02_plane_level(self, ctx):
        """
        The pictogram. A plane, flying level, being loaded with code.

        Everything here is drawn in the grammar the last eight seconds taught:
        the code going in is the same blue square that was falling.
        """
        ctx.lopsided("a plane with sky above it and ground below is not a centred composition")
        ctx.clear_stage(run_time=0.45)
        ground = Line(np.array([stage.STAGE.left + 0.2, stage.STAGE.bottom + 0.18, 0.0]),
                      np.array([stage.STAGE.right - 0.2, stage.STAGE.bottom + 0.18, 0.0]),
                      color=style.GRID, stroke_width=2.5)
        ctx.show(ground, tag="ground", anim=lambda m: Create(m), run_time=0.4)

        p = plane(1.6)
        p.move_to(np.array([-4.1, 0.85, 0.0]))
        self._own("plane", p)
        ctx.play(FadeIn(p, shift=RIGHT * 1.2), run_time=0.5)
        ctx.play(p.animate.move_to(np.array([-0.9, 0.95, 0.0])), run_time=0.9)

        # Code streaming in. Each square flies the flight line and is absorbed.
        loads = VGroup()
        for i in range(5):
            c = chip(style.BLUE, 0.62)
            # Inside the frame, spaced right of the stage edge. Spawning them
            # off-frame to the left read as a stream and gated as three shapes
            # sitting outside the picture for a second and a half.
            c.move_to(np.array([stage.STAGE.left + 0.45 + i * 0.74, 0.85, 0.0]))
            loads.add(c)
        ctx.play(LaggedStart(*[FadeIn(c) for c in loads], lag_ratio=0.1), run_time=0.5)
        # Into the tail, not the centre, and lagged enough that three are in
        # flight at once. A tight lag absorbed them one at a time and the frame
        # held a plane with a single small square beside it.
        entry = p.get_center() + LEFT * 0.35
        ctx.play(LaggedStart(*[
            c.animate.move_to(entry).scale(0.25).set_opacity(0.0)
            for c in loads], lag_ratio=0.22), run_time=1.7)
        self.remove(loads)
        ctx.hold(0.5)

    def b03_plane_goes_in(self, ctx):
        """
        Hard, fast, and over before it becomes tasteless. It is the reason the
        rest of the video exists, not a joke — so it gets three seconds and no
        lingering on the wreck.
        """
        ctx.lopsided("the descent is the composition — the frame empties from the top down")
        p = self._owned["plane"]
        # The bad code arrives the same way the good code did, and is the only
        # thing on screen that changed.
        bad = VGroup(*[chip(style.RED, 0.62) for _ in range(3)])
        for i, c in enumerate(bad):
            c.move_to(np.array([stage.STAGE.left + 0.45 + i * 0.74, 0.85, 0.0]))
        ctx.play(LaggedStart(*[FadeIn(c) for c in bad], lag_ratio=0.12), run_time=0.35)
        ctx.play(*[c.animate.move_to(p.get_center() + LEFT * 0.35).scale(0.25)
                   .set_opacity(0.0) for c in bad], run_time=0.45)
        self.remove(bad)

        impact = np.array([1.6, stage.STAGE.bottom + 0.18, 0.0])
        ctx.play(p.animate.set_stroke(style.RED, width=4.0), run_time=0.2)
        ctx.play(p.animate.rotate(-52 * DEGREES).move_to(impact + UP * 0.55),
                 run_time=0.85, rate_func=rush_into)
        # Splayed lines, not a ring. A red circle drawn round the wreck reads as
        # a prohibition sign — the "no" symbol — which is the wrong sentence
        # entirely. Lines thrown up and out of the impact point read as impact.
        shards = VGroup(*[
            Line(impact, impact + np.array([np.cos(a), np.sin(a), 0.0]) * 0.45,
                 color=style.RED, stroke_width=5)
            for a in np.linspace(25 * DEGREES, 155 * DEGREES, 7)
        ])
        self.add(shards)
        ctx.play(FadeOut(p, scale=0.7),
                 shards.animate.scale(3.0, about_point=impact).set_stroke(opacity=0.0),
                 self._owned["ground"].animate.set_stroke(style.RED, width=4),
                 run_time=0.45)
        self.remove(shards)
        self._owned.pop("plane", None)

        # "Medical devices." The same failure, a different domain — a device
        # output that simply stops.
        good = heartbeat(5.0, height=0.62, cycles=2, color=style.GREEN)
        good.move_to(np.array([-0.7, 0.75, 0.0]))
        tail = VMobject(color=style.RED, stroke_width=4.5)
        end = good.get_points()[-1]
        tail.set_points_as_corners([
            end, end + np.array([0.42, 0.46, 0.0]), end + np.array([0.75, -0.24, 0.0]),
            end + np.array([1.08, 0.0, 0.0]), end + np.array([2.1, 0.0, 0.0]),
        ])
        self._own("trace", VGroup(good, tail))
        ctx.play(Create(good), run_time=0.55)
        ctx.play(Create(tail), run_time=0.45)

    def b04_code_is_fine(self, ctx):
        """The code was never the problem. Show it clean and well-formed."""
        ctx.clear_stage(run_time=0.35)
        row = VGroup(*[chip(style.BLUE, 0.92) for _ in range(5)]).arrange(RIGHT, buff=0.5)
        row.move_to(np.array([0.0, 0.35, 0.0]))
        self._own("row", row)
        ctx.play(LaggedStart(*[FadeIn(c, scale=0.75) for c in row], lag_ratio=0.1),
                 run_time=0.7)
        ctx.play(*[c[0].animate.set_stroke(style.BLUE, width=5.0)
                   .set_fill(style.BLUE, opacity=0.22) for c in row], run_time=0.4)

    # =========================================================== the wall =====
    def b05_wall(self, ctx):
        """The standard, and the flood that cannot get through it."""
        ctx.lopsided("the flood piles on one side of the standard — the asymmetry is the point")
        wall = Rectangle(width=0.38, height=stage.STAGE.height - 0.06,
                         color=style.GOLD, stroke_width=4.0)
        wall.set_fill(style.GOLD, opacity=0.18)
        wall.move_to(np.array([WALL_X, stage.STAGE.center[1], 0.0]))
        self._own("wall", wall)
        tag = style.label_text("the standard", color=style.GOLD, size="tiny")
        tag.move_to(np.array([WALL_X + 1.5, stage.STAGE.top - 0.35, 0.0]))
        ctx.play(Create(wall), FadeIn(tag), run_time=0.7)
        self._own("wall_tag", tag)

        # The tidy row breaks up and joins a pile against the wall.
        rng = random.Random(55)
        pile_region = stage.Region("pile", stage.STAGE.left + 0.3, WALL_X - 0.35,
                                   stage.STAGE.bottom + 0.3, stage.STAGE.top - 0.3)
        pile = VGroup()
        placed = list(self._owned["row"])
        for pos in stage.free_points(18, placed, rng, region=pile_region, pad=0.26):
            c = flood_tile(rng, 0.38)
            c.move_to(pos)
            pile.add(c)
            placed.append(c)
        self._own("pile", pile)
        # Scatter the tidy row into the pile. Shrinking it and parking it in the
        # middle left a neat line of five sitting inside a random scatter, which
        # reads as a separate object rather than as the same code, multiplied.
        scatter = stage.free_points(len(self._owned["row"]), placed, rng,
                                    region=pile_region, pad=0.3)
        ctx.play(*[c.animate.scale(0.48).move_to(pos)
                   for c, pos in zip(self._owned["row"], scatter)], run_time=0.55)
        ctx.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.3) for c in pile],
                             lag_ratio=0.035), run_time=1.4)

        checker = style.node("review", "", size=0.72)
        checker.move_to(np.array([WALL_X + 1.0, -0.7, 0.0]))
        self._own("checker", checker)
        ctx.play(FadeIn(checker, scale=1.2), run_time=0.45)
        ctx.hold(0.5)

    def b06_cheap_not_trusted(self, ctx):
        """Generation is cheap; trust is not. One record gets across, and one only."""
        ctx.lopsided("a full left and an almost-empty right is the claim this line makes")
        rng = random.Random(66)
        pile_region = stage.Region("pile", stage.STAGE.left + 0.3, WALL_X - 0.35,
                                   stage.STAGE.bottom + 0.3, stage.STAGE.top - 0.3)
        placed = list(self._owned["pile"]) + list(self._owned["row"])
        more = VGroup()
        for pos in stage.free_points(14, placed, rng, region=pile_region, pad=0.24):
            c = flood_tile(rng, 0.38)
            c.move_to(pos)
            more.add(c)
            placed.append(c)
        self._own("more_pile", more)
        ctx.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.25) for c in more],
                             lag_ratio=0.025), run_time=1.2)

        # And one thing gets through. One.
        crossing = rec(style.GREEN, 0.42)
        crossing.move_to(np.array([WALL_X - 0.9, 0.9, 0.0]))
        self._own("crossed", crossing)
        ctx.play(FadeIn(crossing), run_time=0.3)
        ctx.play(*style.highlight(self._owned["checker"], style.VIOLET), run_time=0.35)
        ctx.play(crossing.animate.move_to(np.array([WALL_X + 1.9, 0.9, 0.0])),
                 run_time=0.9)
        ctx.hold(1.0)

    def b07_solvable(self, ctx):
        """The thesis, at 0:34. The wall does not come down — a gate opens in it."""
        # The wall opens. Laying a diamond over an unbroken barrier is a badge
        # stuck on a wall, and the line is about the wall becoming passable.
        wall = self._owned["wall"]
        gap_mid, gap_half = 0.15, 0.62
        top, bottom = wall.get_top()[1], wall.get_bottom()[1]

        def half(y_lo, y_hi):
            r = Rectangle(width=wall.width, height=y_hi - y_lo,
                          color=style.GOLD, stroke_width=4.0)
            r.set_fill(style.GOLD, opacity=0.18)
            r.move_to(np.array([WALL_X, (y_lo + y_hi) / 2, 0.0]))
            return r

        halves = VGroup(half(gap_mid + gap_half, top), half(bottom, gap_mid - gap_half))
        gate = style.node("review", "", size=0.95)
        gate.move_to(np.array([WALL_X, gap_mid, 0.0]))
        self._own("gate", gate)
        ctx.play(ReplacementTransform(wall, halves), run_time=0.55)
        # The transform replaced what the tag points at, so re-point it rather
        # than claiming the tag twice.
        self._owned["wall"] = halves
        ctx.play(FadeIn(gate, scale=1.3), run_time=0.4)

        crossed = VGroup()
        for i in range(3):
            r = rec(style.GREEN, 0.42)
            r.move_to(np.array([WALL_X - 1.0, 0.15, 0.0]))
            crossed.add(r)
        self._own("crossed_more", crossed)
        ctx.play(LaggedStart(*[FadeIn(r) for r in crossed], lag_ratio=0.12), run_time=0.5)
        targets = [np.array([WALL_X + 1.15 + i * 0.75, -1.55, 0.0]) for i in range(3)]
        ctx.play(LaggedStart(*[r.animate.move_to(t) for r, t in zip(crossed, targets)],
                             lag_ratio=0.2), run_time=1.4)
        ctx.play(*style.highlight(self._owned["gate"], style.VIOLET), run_time=0.4)
        ctx.hold(0.8)

    # ======================================================== the industry ====
    def b08_industry(self, ctx):
        ctx.clear_stage(run_time=0.6)
        rng = random.Random(7)
        flood = VGroup()
        for _ in range(34):
            c = flood_tile(rng, 0.38)
            c.move_to(np.array([rng.uniform(stage.STAGE.left + 0.4, stage.STAGE.right - 0.4),
                                rng.uniform(0.9, stage.STAGE.top - 0.85), 0.0]))
            flood.add(c)
        self._own("flood", flood)
        ctx.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.5) for c in flood], lag_ratio=0.02),
                 run_time=1.5)
        ctx.play(flood.animate.shift(DOWN * 1.5), run_time=0.9)
        ctx.hold(0.8)
        second = VGroup()
        for _ in range(14):
            c = flood_tile(rng, 0.38)
            c.move_to(np.array([rng.uniform(stage.STAGE.left + 0.4, stage.STAGE.right - 0.4),
                                rng.uniform(1.1, stage.STAGE.top - 0.4), 0.0]))
            second.add(c)
        self._own("flood2", second)
        ctx.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.5) for c in second], lag_ratio=0.03),
                 run_time=1.1)

    def b09_reviewers_struck(self, ctx):
        ctx.lopsided("the flood is above and the reviewers are under it — that is the picture")
        revs = VGroup(*[style.node("review", "", size=0.62) for _ in range(4)])
        revs.arrange(RIGHT, buff=0.9)
        revs.move_to(np.array([0.0, stage.STAGE.bottom + 0.75, 0.0]))
        self._own("revs", revs)
        ctx.play(FadeIn(revs), run_time=0.4)
        ctx.play(VGroup(self._owned["flood"], self._owned["flood2"]).animate.shift(DOWN * 1.1),
                 run_time=0.7)
        ctx.play(*[r.animate.shift(DOWN * 0.22).set_opacity(0.7) for r in revs], run_time=0.5)
        ctx.hold(0.6)

    def b10_buried(self, ctx):
        ctx.lopsided("everything has settled to the bottom of the frame, on purpose")
        rng = random.Random(11)
        pile = VGroup()
        for _ in range(26):
            c = flood_tile(rng, 0.38)
            c.move_to(np.array([rng.uniform(stage.STAGE.left + 0.5, stage.STAGE.right - 0.5),
                                rng.uniform(stage.STAGE.bottom + 0.25, stage.STAGE.bottom + 1.4),
                                0.0]))
            pile.add(c)
        self._own("pile2", pile)
        ctx.play(LaggedStart(*[FadeIn(c) for c in pile], lag_ratio=0.03), run_time=1.1)
        ctx.play(self._owned["revs"].animate.set_opacity(0.14), run_time=0.6)
        ctx.hold(0.8)

    # ------------------------------------------------ what serious software is --
    def b11_clean_slate(self, ctx):
        ctx.clear_stage(run_time=0.7)
        sq = style.node("code", "code", size=1.25)
        sq.move_to(stage.STAGE.center)
        ctx.show(sq, tag="core", anim=lambda m: FadeIn(m, scale=0.85), run_time=0.5)

    def b12_build_chain(self, ctx):
        """Fifteen seconds. One node per clause the narrator names."""
        ctx.lopsided("the chain is named clause by clause, so it is top-heavy "
                     "until the lower half of the list arrives")
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
        # Beside the curve's low end, not above its bbox: the curve rises to the
        # right, so "above the bounding box" is exactly where the stroke ends up.
        tag.move_to(base + np.array([-2.15, 0.45, 0.0]))
        ctx.show(curve, tag="revenue", anim=lambda m: Create(m), run_time=0.6)
        ctx.show(tag, tag="revenue_tag", run_time=0.3)

    def b16_break_fix(self, ctx):
        mid = self._owned["stack"][1]
        ctx.play(mid[0].animate.set_stroke(style.RED, width=3.2), run_time=0.4)
        ctx.hold(0.7)
        ctx.play(mid[0].animate.set_stroke(style.BLUE, width=2.4), run_time=0.4)
        ctx.play(self._owned["revenue"].animate.set_stroke(style.GREEN, width=5), run_time=0.35)

    def b17_focus_right(self, ctx):
        """
        "In the other one, software flies aircraft." The business world leaves
        here, on the line that leaves it — not two lines later. Dimmed and kept,
        a customer-growth curve sat on the left through the satellite line and
        the braking line, which reads as a frame nobody updated.

        The divide goes with it: a line with nothing on one side has stopped
        dividing anything. It comes back in b21, when the flood arrives.
        """
        leaving = [self._owned[t] for t in
                   ("stack", "revenue", "revenue_tag", "divide") if t in self._owned]
        for tag in ("stack", "revenue", "revenue_tag", "divide"):
            self._owned.pop(tag, None)
        block = VGroup(self._owned["core"], self._owned["chain"])
        ctx.play(*[FadeOut(m) for m in leaving],
                 block.animate.scale(1.5).move_to(stage.STAGE.center), run_time=0.6)
        ctx.play(*style.highlight(self._owned["core"], style.BLUE), run_time=0.45)

    def b18_second_chain(self, ctx):
        ctx.lopsided("the first chain moves up before the second lands under it — "
                     "the frame is top-heavy for the length of that move")
        block = VGroup(self._owned["core"], self._owned["chain"])
        # Work out the room for three rows *before* anything moves. Arriving at
        # full size and shrinking afterwards put the stack in the title lane for
        # most of a second — a defect the viewer sees, and the fix is simply to
        # compute first and animate once. Spacing the rows from the block's own
        # measured height means they cannot overlap however the chain is later
        # restyled.
        self._row_gap = block.height + 0.34
        k = min(1.0, stage.STAGE.height / (3 * self._row_gap + 0.9))
        self._row_gap *= k
        second = block.copy().scale(k).set_opacity(0.85)
        for sub in second.get_family():
            if getattr(sub, "text", None):
                sub.set_opacity(0)   # set_opacity on the copy revived the labels
        second.move_to(stage.STAGE.center)
        ctx.play(block.animate.scale(k).move_to(stage.STAGE.center + UP * self._row_gap),
                 run_time=0.5)
        ctx.show(second, tag="chain2", anim=lambda m: FadeIn(m, shift=UP * 0.2), run_time=0.5)

    def b19_third_chain(self, ctx):
        third = self._owned["chain2"].copy()
        third.move_to(stage.STAGE.center + DOWN * self._row_gap)
        ctx.show(third, tag="chain3", anim=lambda m: FadeIn(m, shift=UP * 0.2), run_time=0.55)
        # The stack plus the seal drawn round it in the next beat must clear the
        # title lane, so shrink the whole block to the room actually available.
        block = VGroup(self._owned["core"], self._owned["chain"],
                       self._owned["chain2"], self._owned["chain3"])
        room = (stage.STAGE.height - 0.9) / max(block.height, 1e-6)
        if room < 1.0:
            ctx.play(block.animate.scale(room).move_to(stage.STAGE.center), run_time=0.5)

    def b20_seal(self, ctx):
        """
        Ten seconds: the perimeter draws, then who is accountable for it.

        The three answers arrive one at a time and then *stay*. Cycling them
        through a single slot gave each about two seconds, which is under the
        time it takes to read fifteen characters — and they are a list of who is
        accountable, not three successive answers. Standing them in the column
        the business world has just vacated also gives the line something on the
        left of the frame, which the seal beat did not have.
        """
        block = VGroup(self._owned["core"], self._owned["chain"],
                       self._owned["chain2"], self._owned["chain3"])
        seal = SurroundingRectangle(block, color=style.GOLD, stroke_width=3.5, buff=0.3)
        ctx.show(seal, tag="seal", anim=lambda m: Create(m), run_time=1.0)
        ctx.hold(0.5)
        # Slide right to open the left half for the three answers. Doing it after
        # the seal is drawn keeps the seal glued to what it encloses.
        ctx.play(VGroup(block, seal).animate.move_to(RIGHT_COL.center), run_time=0.5)
        label = style.label_text("signed off before it runs", color=style.GOLD, size="tiny")
        label.next_to(seal, DOWN, buff=0.26)
        ctx.show(label, tag="seal_label", run_time=0.45)
        ctx.hold(0.4)

        stamps = [style.label_text(w, color=style.GOLD, size="label")
                  for w in ("an organization", "a process", "a regulator")]
        rows = style.text_rows(*stamps, buff=0.42)
        rows.move_to(LEFT_COL.center)
        self._own("accountable", rows)
        for s in stamps:
            ctx.play(FadeIn(s, shift=RIGHT * 0.18), run_time=0.32)
            ctx.hold(0.85)
        ctx.play(seal.animate.set_stroke(style.GOLD, width=5), run_time=0.5)
        ctx.hold(0.6)

    # --------------------------------------------------------- the bottleneck --
    def b21_pile_up(self, ctx):
        """Generation floods the world that has to be accountable for it."""
        ctx.lopsided("the left overflows while the right stays fixed — deliberately unequal")
        ctx.retire("accountable", run_time=0.35)
        divide = DashedLine(np.array([DIVIDE_X, stage.STAGE.bottom, 0.0]),
                            np.array([DIVIDE_X, stage.STAGE.top, 0.0]),
                            color=style.GRID, stroke_width=3, dash_length=0.16)
        ctx.show(divide, tag="divide", anim=lambda m: Create(m), run_time=0.4)
        rng = random.Random(23)
        more = VGroup()
        for _ in range(24):
            c = flood_tile(rng, 0.38)
            c.move_to(np.array([rng.uniform(stage.STAGE.left + 0.4, DIVIDE_X - 0.5),
                                rng.uniform(stage.STAGE.bottom + 0.4, stage.STAGE.top - 0.35), 0.0]))
            more.add(c)
        self._own("more", more)
        ctx.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.25) for c in more], lag_ratio=0.028),
                 run_time=1.5)

    def b22_static(self, ctx):
        ctx.lopsided("the contrast between a full left and an unmoved right is the claim")
        ctx.play(self._owned["divide"].animate.set_stroke(style.RED, width=5), run_time=0.5)
        ctx.hold(0.7)
        ctx.play(*[c.animate.shift(RIGHT * 0.16) for c in self._owned["more"]], run_time=0.6)
        ctx.hold(0.4)

    def b23_push_in(self, ctx):
        going = [self._owned[t] for t in ("seal", "seal_label", "chain2", "chain3")
                 if t in self._owned]
        if going:
            ctx.play(*[FadeOut(m) for m in going], run_time=0.5)
        for tag in ("seal", "seal_label", "chain2", "chain3"):
            self._owned.pop(tag, None)
        # The line says the bottleneck moves, so it has to move. A 6% scale on
        # a static frame while the right-hand clutter disappears is a beat that
        # says nothing; the flood advancing on the divide says the thing.
        ctx.play(self._owned["more"].animate.scale(1.08).shift(RIGHT * 0.7),
                 self._owned["divide"].animate.shift(RIGHT * 0.45),
                 run_time=0.6)

    def _light(self, ctx, kinds: tuple[str, ...]):
        """Brighten every tile of the given kinds, in place and in its own colour."""
        hit = [c for c in self._owned["more"]
               if getattr(c, "tile_kind", None) in kinds]
        ctx.play(*[c[0].animate.set_stroke(width=4.4).set_fill(opacity=0.36)
                   for c in hit], run_time=0.45)

    def b24_not_editor(self, ctx):
        # Brightened, not recoloured: restroking half the flood cyan and the
        # other half violet turned a pile of code squares into a pile of things
        # the grammar calls tests and sources, on a line about neither.
        #
        # And the two lines light different *kinds*, not two arbitrary slices of
        # the same list. Slices gave b24 and b25 near-identical frames, so the
        # second line landed on a picture that had not changed.
        self._light(ctx, ("code",))

    def b25_not_model(self, ctx):
        self._light(ctx, ("test", "source", "evidence"))

    def b26_trust(self, ctx):
        gate = style.node("review", "", size=1.5)
        # On the divide as it now stands — b23 pushed it right, and a gate that
        # lands beside the line instead of in it is a gate in a wall with a hole
        # next to it.
        gate.move_to(np.array([self._owned["divide"].get_center()[0],
                               stage.STAGE.center[1], 0.0]))
        ctx.show(gate, tag="gate2", anim=lambda m: FadeIn(m, scale=1.4), run_time=0.45)

    # ------------------------------------------------------------ the answer --
    def b27_compiler(self, ctx):
        ctx.clear_stage("gate2", run_time=0.7)
        frame = RoundedRectangle(corner_radius=0.12, width=5.2, height=2.9,
                                 color=style.VIOLET, stroke_width=3)
        frame.move_to(stage.STAGE.center)
        gate = self._owned["gate2"]
        ctx.play(gate.animate.move_to(frame.get_right()), Create(frame), run_time=0.8)
        name = style.label_text("Verification Compiler", color=style.VIOLET)
        name.next_to(frame, UP, buff=0.3)
        ctx.show(name, tag="name", run_time=0.5)
        self._own("frame", frame)

    def b28_frame_turns(self, ctx):
        ctx.play(self._owned["frame"].animate.set_stroke(style.VIOLET, width=5), run_time=0.5)
        ctx.hold(0.4)
        ctx.play(self._owned["frame"].animate.set_stroke(style.VIOLET, width=3), run_time=0.5)

    def b29_fold(self, ctx):
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
        joins = VGroup()
        for n in scaffold:
            a, b = n.get_center(), unit.get_center()
            d = (b - a) / np.linalg.norm(b - a)
            # Stop short of both ends. A join drawn to the unit's *centre* runs
            # through the word inside it, which is the outline_over_text defect
            # and reads as a line scribbled across the label.
            joins.add(Line(a + d * 0.34, b - d * 0.52,
                           color=style.DIM, stroke_width=2.0))
        ctx.play(LaggedStart(*[Create(j) for j in joins], lag_ratio=0.18), run_time=0.7)
        ctx.hold(0.4)
        # The label goes before the fold. Transforming a labelled unit into the
        # packet sweeps the joins across the word "code" for half a second, and
        # the unit is about to stop being a code node anyway.
        ctx.play(unit.qa_label.animate.set_opacity(0.0), run_time=0.25)
        packet = style.node("vqp", "VQP", size=1.5)
        packet.move_to(frame.get_center())
        ctx.play(ReplacementTransform(VGroup(unit, scaffold, joins), packet), run_time=0.9)
        self._own("packet", packet)
        ctx.play(*style.highlight(packet, style.GREEN), run_time=0.4)
        ctx.hold(0.5)
        ctx.play(*style.restroke(packet, style.GREEN, 2.6), run_time=0.4)

    def b30_through_gate(self, ctx):
        gate = self._owned["gate2"]
        ctx.play(self._owned["packet"].animate.next_to(gate, LEFT, buff=0.28), run_time=0.7)
        ctx.play(*style.highlight(gate, style.GOLD), run_time=0.4)

    def b31_beat(self, ctx):
        final = style.title_text("a compiler for trust")
        final.move_to(stage.STAGE.center)
        leaving = [self._owned[t] for t in ("packet", "name", "frame", "gate2")
                   if t in self._owned]
        for tag in ("packet", "name", "frame", "gate2"):
            self._owned.pop(tag, None)
        self.remove(*leaving)
        ctx.show(final, tag="final", anim=lambda m: FadeIn(m, scale=0.92), run_time=0.25)

    def b32_title(self, ctx):
        # The closing words are already up — this line lands on them rather than
        # introducing them. Introduced here they had 1.3 seconds before the
        # section ended, which is half the time it takes to read them.
        ctx.play(self._owned["final"].animate.scale(1.06), run_time=0.5)
