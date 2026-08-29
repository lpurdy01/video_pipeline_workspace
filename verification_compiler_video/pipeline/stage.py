"""
The stage: reserved regions with guaranteed clearance.

Video 1's recurring failure was a caption at the bottom of the frame colliding
with diagram text that happened to reach down there. Detecting that after the
fact meant a render/review/fix cycle per collision.

Here the frame is divided into named lanes that own their vertical space. Content
is *fitted* into a lane — scaled down if it does not fit — so a diagram can never
grow into the caption lane in the first place. QA still checks, but as a backstop
for genuine bugs rather than as the primary defence.

    ┌──────────────────────────────────┐
    │ TITLE            (top, reserved) │
    ├──────────────────────────────────┤
    │                                  │
    │ STAGE            (diagram space) │
    │                                  │
    ├──────────────────────────────────┤
    │ CAPTION       (bottom, reserved) │
    └──────────────────────────────────┘
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from manim import *

from . import style


FRAME_W = 14.222  # manim default 16:9 frame width
FRAME_H = 8.0
SAFE_MARGIN = 0.42  # nothing renders outside this inset — broadcast-style safe area


@dataclass(frozen=True)
class Region:
    """An axis-aligned box in scene coordinates."""

    name: str
    left: float
    right: float
    bottom: float
    top: float

    @property
    def width(self) -> float:
        return self.right - self.left

    @property
    def height(self) -> float:
        return self.top - self.bottom

    @property
    def center(self) -> np.ndarray:
        return np.array([(self.left + self.right) / 2, (self.bottom + self.top) / 2, 0.0])

    def contains(self, mob: Mobject, tol: float = 1e-3) -> bool:
        return (
            mob.get_left()[0] >= self.left - tol
            and mob.get_right()[0] <= self.right + tol
            and mob.get_bottom()[1] >= self.bottom - tol
            and mob.get_top()[1] <= self.top + tol
        )

    def box(self, color: str = style.GRID) -> Rectangle:
        """A debug outline of this region."""
        return Rectangle(width=self.width, height=self.height,
                         color=color, stroke_width=1).move_to(self.center)


_HALF_W = FRAME_W / 2 - SAFE_MARGIN
_HALF_H = FRAME_H / 2 - SAFE_MARGIN

TITLE = Region("title", -_HALF_W, _HALF_W, _HALF_H - 0.95, _HALF_H)
CAPTION = Region("caption", -_HALF_W, _HALF_W, -_HALF_H, -_HALF_H + 0.95)
STAGE = Region("stage", -_HALF_W, _HALF_W, CAPTION.top + 0.28, TITLE.bottom - 0.28)

# Sub-regions of STAGE, for two- and three-column compositions.
def columns(n: int, gap: float = 0.45, region: Region = STAGE) -> list[Region]:
    """Split a region into n equal columns."""
    total_gap = gap * (n - 1)
    w = (region.width - total_gap) / n
    out = []
    for i in range(n):
        left = region.left + i * (w + gap)
        out.append(Region(f"{region.name}.col{i}", left, left + w, region.bottom, region.top))
    return out


def rows(n: int, gap: float = 0.35, region: Region = STAGE) -> list[Region]:
    total_gap = gap * (n - 1)
    h = (region.height - total_gap) / n
    out = []
    for i in range(n):
        top = region.top - i * (h + gap)
        out.append(Region(f"{region.name}.row{i}", region.left, region.right, top - h, top))
    return out


MIN_LEGIBLE_FONT_SIZE = 15.0


def fit(mob: Mobject, region: Region, pad: float = 0.18, align=None,
        allow_illegible: bool = False) -> Mobject:
    """
    Scale (never up) and position `mob` so it sits inside `region`.

    This is the core guarantee: content placed through fit() cannot reach into a
    neighbouring lane, so a caption and a diagram cannot collide by construction.

    Shrinking is where legibility quietly dies — a node built at a readable size
    can be scaled to 11pt by a fit() call and nothing at construction time knows.
    So fit() refuses to make text illegible, and says what to do about it. That
    moves the failure from "spotted in review" to "cannot be written".
    """
    max_w = region.width - 2 * pad
    max_h = region.height - 2 * pad
    if mob.width > max_w or mob.height > max_h:
        scale = min(max_w / mob.width, max_h / mob.height)
        if not allow_illegible:
            smallest = min(
                (float(s.font_size) * scale for s in mob.get_family()
                 if getattr(s, "text", None) and hasattr(s, "font_size")),
                default=None,
            )
            if smallest is not None and smallest < MIN_LEGIBLE_FONT_SIZE:
                raise ValueError(
                    f"fitting into {region.name} would scale text to "
                    f"{smallest:.1f}pt (min {MIN_LEGIBLE_FONT_SIZE:.0f}pt). "
                    f"The content is too big for the region: use fewer elements, "
                    f"a larger region, or shorter labels."
                )
        mob.scale(scale)
    mob.move_to(region.center)
    if align is not None:
        mob.align_to(_edge_point(region, align), align)
        # nudge back inside the pad
        if align is LEFT:
            mob.shift(RIGHT * pad)
        elif align is RIGHT:
            mob.shift(LEFT * pad)
        elif align is UP:
            mob.shift(DOWN * pad)
        elif align is DOWN:
            mob.shift(UP * pad)
    return mob


def _edge_point(region: Region, direction) -> np.ndarray:
    c = region.center
    return c + np.array([direction[0] * region.width / 2,
                         direction[1] * region.height / 2, 0.0])


def stack(mobs: list[Mobject], region: Region, buff: float = 0.22,
          direction=DOWN) -> VGroup:
    """Arrange mobjects in a region, fitting the whole group."""
    group = VGroup(*mobs).arrange(direction, buff=buff)
    fit(group, region)
    return group


def grid(mobs: list[Mobject], region: Region, cols: int, buff: float = 0.4) -> VGroup:
    n_rows = (len(mobs) + cols - 1) // cols
    group = VGroup(*mobs).arrange_in_grid(rows=n_rows, cols=cols, buff=buff)
    fit(group, region)
    return group


def zone(region: Region, label: str, color: str, fill_opacity: float = 0.055) -> VGroup:
    """
    A tinted, headed band — the organising device from the whitepaper figures.

    Figure 3 splits the artifact graph into REQUIREMENTS / CODE UNITS /
    VERIFICATION EVIDENCE columns, and that banding does most of the explaining
    before a single edge is read. A loose cloud of correctly-shaped nodes does
    not; the zones are what make it legible at a glance.

    The header sits inside the band's own top, so it never competes with the
    title lane.
    """
    from . import style

    band = RoundedRectangle(
        corner_radius=0.1, width=region.width, height=region.height,
        color=color, stroke_width=1.6, stroke_opacity=0.55,
    ).move_to(region.center)
    band.set_fill(color, opacity=fill_opacity)

    head = Text(label, color=color, font_size=style.TYPE["tiny"], weight=BOLD)
    head.next_to(band.get_top(), DOWN, buff=0.16)
    if head.width > region.width - 0.3:
        head.scale((region.width - 0.3) / head.width)
    # A band is scenery. Push it behind the connector layer so a zone added
    # after an edge cannot swallow it.
    band.set_z_index(style.Z_BACKDROP, family=True)
    head.set_z_index(style.Z_BACKDROP, family=True)
    return VGroup(band, head)


def zone_body(region: Region, top_pad: float = 0.62) -> Region:
    """The part of a zone below its header, where content actually goes."""
    return Region(f"{region.name}.body", region.left, region.right,
                  region.bottom, region.top - top_pad)


def _boxes_gap(a, b) -> float | None:
    """Clearance between two bounding boxes, or None when they overlap."""
    ax0, ax1, ay0, ay1 = a
    bx0, bx1, by0, by1 = b
    dx = max(bx0 - ax1, ax0 - bx1)
    dy = max(by0 - ay1, ay0 - by1)
    if dx < 0 and dy < 0:
        return None
    return max(dx, dy, 0.0)


def _box(mob) -> tuple[float, float, float, float]:
    return (mob.get_left()[0], mob.get_right()[0],
            mob.get_bottom()[1], mob.get_top()[1])


def _separation(a, b) -> tuple[float, float]:
    """Signed clearance on each axis. Negative means the boxes overlap there."""
    ax0, ax1, ay0, ay1 = a
    bx0, bx1, by0, by1 = b
    return (max(bx0 - ax1, ax0 - bx1), max(by0 - ay1, ay0 - by1))


def _inside(inner, outer, slack: float = 0.06) -> bool:
    """Is `inner` wholly within `outer`? Then the pairing is deliberate."""
    ix0, ix1, iy0, iy1 = inner
    ox0, ox1, oy0, oy1 = outer
    return (ix0 >= ox0 - slack and ix1 <= ox1 + slack
            and iy0 >= oy0 - slack and iy1 <= oy1 + slack)


def clear_of(mob, others, min_gap: float | None = None, limit: float = 0.75,
             region: Region = STAGE, crossing_only: bool = False) -> float:
    """
    Nudge `mob` until it has air around every mobject in `others`.

    Three of the last four layout defects were the same story: one beat places a
    label with `next_to(box, DOWN, buff=0.22)`, a different beat placed another
    label near the same box, and the two land 0.12 apart — legible on their own,
    a smudge together. Nobody wrote a bad number; the two beats simply could not
    see each other.

    Two boxes are clear of each other as soon as they are separated on *either*
    axis, so the nudge picks whichever axis is cheaper to satisfy — the first
    version picked the axis with the largest centre offset instead, which
    happily slid a wide caption sideways underneath a short label it entirely
    spanned, moving it 0.23 and separating it by nothing.

    Nudging is deliberately small and deliberately capped. A 0.04 deficit is a
    rounding accident and should be absorbed silently; a 2.0 deficit means the
    composition wants two things in the same place, which is a decision for the
    storyboard, not for a nudge. Past `limit` this raises instead of quietly
    producing a layout nobody chose.

    Returns the distance moved, so a caller can tell "fine" from "only just".
    """
    if min_gap is None:
        min_gap = style.MIN_TEXT_GAP + style.PLACEMENT_MARGIN
    others = [o for o in others if o is not mob and len(o.get_all_points())]
    if not others:
        return 0.0

    moved = 0.0
    for _ in range(8):
        worst = None
        for other in others:
            if crossing_only and _inside(_box(mob), _box(other)):
                # A label drawn inside a card, or inside a SurroundingRectangle
                # put there to frame it, is a composition — not a collision.
                # Only a label straddling the boundary gets the stroke drawn
                # through its letters, and only that needs moving.
                continue
            sep_x, sep_y = _separation(_box(mob), _box(other))
            if max(sep_x, sep_y) >= min_gap - 1e-6:
                continue                      # already clear on one axis
            cost_x = min_gap - sep_x
            cost_y = min_gap - sep_y
            axis, cost = (0, cost_x) if cost_x <= cost_y else (1, cost_y)
            if worst is None or cost > worst[1]:
                worst = (axis, cost, other)
        if worst is None:
            return moved
        axis, cost, other = worst
        delta = mob.get_center()[axis] - other.get_center()[axis]
        sign = 1.0 if delta >= 0 else -1.0
        step = np.zeros(3)
        step[axis] = sign * cost
        moved += cost
        if moved > limit:
            raise ValueError(
                f"cannot place {_describe(mob)} clear of {_describe(other)} without "
                f"moving it {moved:.2f} (limit {limit}). Two beats are competing for "
                "the same strip of screen — retire one, or give them separate lanes."
            )
        mob.shift(step)
        clamp_into(mob, region)
    return moved


def clamp_into(mob, region: Region = STAGE, pad: float = 0.12):
    """
    Shift `mob` back inside `region` if it has strayed out — and only then.

    fit() is the wrong tool here: it recentres unconditionally, so calling it
    inside a nudge loop teleports the label to the middle of the stage on every
    pass and the loop never converges.
    """
    dx = dy = 0.0
    if mob.get_left()[0] < region.left + pad:
        dx = region.left + pad - mob.get_left()[0]
    elif mob.get_right()[0] > region.right - pad:
        dx = region.right - pad - mob.get_right()[0]
    if mob.get_bottom()[1] < region.bottom + pad:
        dy = region.bottom + pad - mob.get_bottom()[1]
    elif mob.get_top()[1] > region.top - pad:
        dy = region.top - pad - mob.get_top()[1]
    if dx or dy:
        mob.shift(np.array([dx, dy, 0.0]))
    return mob


def _describe(mob) -> str:
    text = getattr(mob, "text", None)
    if text:
        return repr(str(text)[:40])
    kids = [str(getattr(k, "text", "")) for k in mob.get_family()
            if getattr(k, "text", None)]
    return repr(" ".join(kids)[:40]) if kids else type(mob).__name__


def free_points(n: int, avoid, rng, region: Region = STAGE,
                pad: float = 0.34, tries: int = 400) -> list:
    """
    Scatter `n` positions in `region` that miss everything in `avoid`.

    Uniform random placement over the whole stage is how a "flood of artifacts"
    beat ends up with a dozen tiles sitting on top of the diagram the flood is
    supposed to be arriving around. The tiles are meant to fill the space that is
    free, which is a thing the scene can simply check.

    Falls back to the least-bad position rather than looping forever, because a
    stage with no room left is a composition problem and should look like one
    rather than hanging the render.
    """
    boxes = []
    for m in avoid:
        try:
            boxes.append((m.get_left()[0] - pad, m.get_right()[0] + pad,
                          m.get_bottom()[1] - pad, m.get_top()[1] + pad))
        except Exception:
            continue

    def clash(x, y):
        return sum(1 for x0, x1, y0, y1 in boxes if x0 <= x <= x1 and y0 <= y <= y1)

    out = []
    for _ in range(n):
        best, best_score = None, 10 ** 9
        for _ in range(max(tries // n, 12)):
            x = rng.uniform(region.left + 0.4, region.right - 0.4)
            y = rng.uniform(region.bottom + 0.4, region.top - 0.4)
            score = clash(x, y)
            if score == 0:
                best = (x, y)
                break
            if score < best_score:
                best, best_score = (x, y), score
        out.append(np.array([best[0], best[1], 0.0]))
    return out
