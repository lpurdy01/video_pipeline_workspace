"""
Automated quality gate.

The expensive part of video 1 was a human finding problems a machine could have
found: text over text, an element off the edge, a label too small to read, an
arrowhead landing in the middle of a word. Every one of those is geometry, and
geometry is checkable.

`QASceneMixin` hooks Manim's per-frame update and records the bounding box of
every visible text mobject at every frame — including the frames *inside* an
animation, which is where crossover collisions actually happen and where
keyframe sampling always missed them. The recording is then checked offline and
any violation is rendered as an annotated PNG.

Nothing here needs a model. It runs in seconds and it runs before a human looks.
"""
from __future__ import annotations

import json
import zlib
from dataclasses import dataclass, field, asdict
from pathlib import Path

import numpy as np
from manim import *

from . import stage, style


# The checks, and why each one exists.
CHECKS = {
    "text_overlap": "two text mobjects overlap on screen",
    "out_of_frame": "a mobject reaches outside the safe area",
    "text_too_small": "rendered text is below the legible minimum",
    "caption_intrusion": "non-caption content entered the caption lane while a caption was up",
    "arrow_into_label": "an arrowhead lands on top of a text mobject",
    "offscreen_text": "text is fully outside the camera frame but still added",
    "flicker": "a mobject vanished and came back — the classic FadeIn-to-zero-opacity bug",
    "caption_stack": "two captions occupied the caption lane at once",
    "dead_air": "nothing on screen changed for longer than the dead-air budget",
    "node_overlap": "two artifact nodes overlap on screen",
    "edge_through_node": "a connector passes through a node it does not connect",
    "label_orphaned": "a node's label vanished while the node itself stayed on screen",
    "shape_over_text": "a shape or stroke sits across text",
    "title_lane_intrusion": "content entered the reserved title lane",
    "low_contrast": "text does not contrast enough with what is behind it",
    "node_off_frame": "a node or shape is partly outside the frame",
    "stroke_over_text": "a line or outline is drawn across text",
    "text_crowding": "two texts are legible but sit too close to read as separate",
    "z_order_flip": "a connector changed layer relative to a node mid-scene",
    "text_stroked": "text has a heavy stroke on it, which thickens the letterforms",
    "stage_imbalance": "the composition is bunched into part of the stage, leaving dead space",
    "outline_over_text": "a shape's own outline runs through text, cutting the letterforms",
    "text_too_brief": "text was on screen too briefly to read",
    "partial_dim": "part of a group was dimmed and the connectors joining it were not",
    "layer_transient": "a connector was drawn in front and then dropped behind",
    "words_merged": "the gap between two words is too small to read them apart",
    "arrow_to_nowhere": "an arrow points at empty space — what it aimed at has gone",
}

# Texts need air between them, not merely an absence of overlap. Below this gap
# two lines read as one block. Defined in style so the placement helper that
# prevents this and the check that catches it cannot disagree.
MIN_TEXT_GAP = style.MIN_TEXT_GAP

# WCAG contrast ratios. Large text (>=24pt here) is legible at a lower ratio than
# body text, which is why the two thresholds differ.
MIN_CONTRAST_BODY = 4.5
MIN_CONTRAST_LARGE = 3.0
LARGE_TEXT_PT = 24.0

# Composition balance. Gemini's first pass over the rendered frames said the same
# thing about ten consecutive beats — "everything is shoved to the right, the left
# half is a dead region" — which is a mechanical enough observation that it should
# not have needed a model to make it. Content whose centre of mass sits this far
# from the middle of the stage, for this long, is a composition nobody chose.
MAX_CENTROID_OFFSET = 0.30      # as a fraction of the stage half-width/height
IMBALANCE_SETTLE_SECONDS = 2.5  # a transit across the stage is not an imbalance

# Two nodes this far apart along the view axis are occluding each other, which is
# what depth looks like. Closer than this and they are simply in the same place.
DEPTH_SEPARATION = 0.45

# Reading speed for on-screen text, in characters per second, plus the fixed cost
# of noticing that something appeared at all. Deliberately generous: a viewer is
# listening to narration at the same time and is not giving the label their full
# attention. Judged at EXPORT_SPEED, since the cut ships sped up.
READ_CHARS_PER_SECOND = 11.0
READ_FIXED_COST = 0.75
EXPORT_SPEED = 1.25

# A shape's outline passing this close to the middle of a text's box cuts through
# the letters rather than framing them.
OUTLINE_TEXT_PAD = 0.02

# Review renders are 854px across a 14.222-unit frame, so a scene unit is about
# 60 pixels. Below this many pixels a word space stops separating anything and
# two words read as one — "makes an" rendering as "makesan". Judged at review
# resolution because that is what gets watched.
REVIEW_PX_PER_UNIT = 60.0
MIN_WORD_GAP_PX = 4.5

# How close an arrowhead has to land to something before it counts as pointing
# at it. Generous: an arrow that stops short of its target still reads as aimed
# at it, and the defect this catches is an arrow aimed at nothing at all.
ARROW_TARGET_PAD = 0.55

# Nodes may touch, but a real overlap hides one behind the other.
NODE_OVERLAP_TOLERANCE = 0.10

# How long two nodes must stay overlapped before it counts. Below this it is a
# transform passing through, which is what a transform is supposed to look like.
OVERLAP_SETTLE_SECONDS = 0.35

# Overlap is measured as intersection area over the area of the *smaller* box, so
# a small label sitting inside a big one still trips even though its IoU is tiny.
OVERLAP_TOLERANCE = 0.06

# Legibility is a property of the type size, not of which letters happen to be in
# the word: "an answer" has no ascenders and so measures shorter than "which
# version?" at the identical font size. Measuring the bounding box therefore
# produces false alarms on some words and misses on others. Manim's `font_size`
# tracks through scaling, so it is the honest signal.
MIN_FONT_SIZE_RENDERED = 15.0

# How long a type size must persist before it counts as something the viewer
# actually had to read, rather than a frame an animation passed through.
SETTLED_SECONDS = 0.4

# The activity signature is a float sum over the whole scene; it jitters by
# thousandths frame to frame. Anything below this is not a visible change.
SIG_TOLERANCE = 0.05


@dataclass
class Sample:
    t: float
    boxes: list[dict] = field(default_factory=list)
    sig: float = 0.0


def _is_text(mob: Mobject) -> bool:
    return isinstance(mob, (Text, MarkupText, Tex, MathTex, SingleStringMathTex))


def _visible(mob: Mobject) -> bool:
    """
    Is this drawn at all?

    Opacity and points only — deliberately not size. Size was measured in *scene*
    coordinates, and a 3D scene stands its nodes upright by rotating them into
    the XZ plane, which makes their y-extent exactly zero. Requiring a non-zero
    height therefore excluded every node in both 3D sections from every check:
    sections 04 and 06 were passing the gate on one recorded mobject apiece. The
    same test also discarded any horizontal rule in a flat scene. Degenerate
    geometry is rejected later, from the projected box, where "has no size" means
    what it says.
    """
    if getattr(mob, "fill_opacity", 0) == 0 and getattr(mob, "stroke_opacity", 0) == 0:
        return False
    try:
        # Own points *or* children. A node is a VGroup whose geometry lives in
        # its children and it is the VGroup that carries the role tag, so a
        # container has to pass — but asking get_all_points() here vstacks the
        # whole subtree once per family member, which is quadratic in the size of
        # the scene and took a 34-second 3D render past fifteen minutes.
        # Genuinely empty geometry is rejected below, from the projected box.
        return len(mob.points) > 0 or bool(mob.submobjects)
    except Exception:
        return False


def _hex(mob: Mobject) -> str:
    """
    The colour the viewer actually sees.

    `Text.get_color()` returns the stroke colour, which for Manim text is
    `#000000` — so contrast measured from it says every caption is invisible
    against every background. The fill is what is painted.
    """
    # Manim keeps a Text's colour on its glyph submobjects; the Text container
    # itself reports #000000 from both get_color() and get_fill_colors(). Reading
    # the container made every caption look like black-on-black.
    for sub in mob.get_family():
        try:
            if not len(getattr(sub, "points", [])):
                continue
            cols = sub.get_fill_colors()
            if cols and float(getattr(sub, "fill_opacity", 0) or 0) > 0:
                return str(cols[0]).upper()[:7]
        except Exception:
            continue
    try:
        return str(mob.get_color()).upper()[:7]
    except Exception:
        return ""


def _fill_hex(mob: Mobject) -> str:
    """The colour actually painted behind anything sitting on this mobject."""
    for sub in mob.get_family():
        try:
            # Containers report a child's opacity but their own default white,
            # which made every panel look like a white background and every
            # label on one look unreadable.
            if not len(getattr(sub, "points", [])):
                continue
            if float(getattr(sub, "fill_opacity", 0) or 0) > 0.5:
                cols = sub.get_fill_colors()
                if cols:
                    return str(cols[0]).upper()[:7]
        except Exception:
            continue
    return ""


def _luminance(hex_colour: str) -> float | None:
    """WCAG relative luminance."""
    h = (hex_colour or "").lstrip("#")
    if len(h) != 6:
        return None
    try:
        rgb = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    except ValueError:
        return None
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast_ratio(fg: str, bg: str) -> float | None:
    lf, lb = _luminance(fg), _luminance(bg)
    if lf is None or lb is None:
        return None
    hi, lo = max(lf, lb), min(lf, lb)
    return (hi + 0.05) / (lo + 0.05)


def _has_points(mob: Mobject) -> bool:
    try:
        return len(mob.get_family()) > 0 and any(
            len(getattr(s, "points", [])) for s in mob.get_family())
    except Exception:
        return False


def _effective_opacity(mob: Mobject) -> float:
    """How visible is this mobject, counting its children?"""
    best = 0.0
    for sub in mob.get_family():
        best = max(best,
                   float(getattr(sub, "fill_opacity", 0.0) or 0.0),
                   float(getattr(sub, "stroke_opacity", 0.0) or 0.0))
    return round(best, 3)


def _diag(mob: Mobject) -> float:
    """Extent of a mobject's own geometry, independent of orientation."""
    pts = mob.get_all_points()
    if not len(pts):
        return 0.0
    return float(np.linalg.norm(pts.max(axis=0) - pts.min(axis=0)))


def _rendered_pt(mob: Mobject) -> float | None:
    """
    How large this text actually renders, in font-size units.

    Manim derives ``Text.font_size`` from the mobject's *height*, so standing a
    label upright in a 3D scene — a rotation into the XZ plane — reports it as
    0.0pt, and every label in both 3D sections read as illegible for the whole
    section. Comparing the current point-cloud diagonal against the one measured
    at construction is rotation-invariant and still tracks scaling, which is what
    the legibility check actually cares about.
    """
    pt0 = getattr(mob, "qa_pt0", None)
    d0 = getattr(mob, "qa_diag0", None)
    if pt0 and d0:
        return float(pt0) * (_diag(mob) / float(d0))
    try:
        return float(mob.font_size)
    except Exception:
        return None


def _screen(mob: Mobject, camera=None) -> tuple[tuple[float, float, float, float], float]:
    """
    Screen box and camera depth, from a single projection.

    Projecting a mobject's point cloud is the expensive part of recording a
    frame, so the box and the depth come out of one call rather than two.
    """
    if camera is not None and hasattr(camera, "project_points"):
        try:
            pts = mob.get_all_points()
            if len(pts):
                proj = camera.project_points(np.asarray(pts))
                xs, ys, zs = proj[:, 0], proj[:, 1], proj[:, 2]
                return ((float(xs.min()), float(xs.max()),
                         float(ys.min()), float(ys.max())),
                        float(zs.mean()))
        except Exception:
            pass
    return ((float(mob.get_left()[0]), float(mob.get_right()[0]),
             float(mob.get_bottom()[1]), float(mob.get_top()[1])), 0.0)


def _bbox(mob: Mobject, camera=None) -> tuple[float, float, float, float]:
    """
    Axis-aligned bounding box in *screen* coordinates.

    In a 3D scene, world coordinates say nothing about what the viewer sees — a
    node behind the camera and one in front of it can share an x. Projecting
    through the camera first is what lets every 2D check work unchanged on a 3D
    scene, instead of 3D scenes shipping with no checking at all.
    """
    if camera is not None and hasattr(camera, "project_points"):
        try:
            pts = mob.get_all_points()
            if len(pts):
                proj = camera.project_points(np.array(pts))
                xs, ys = proj[:, 0], proj[:, 1]
                return (float(xs.min()), float(xs.max()),
                        float(ys.min()), float(ys.max()))
        except Exception:
            pass
    return (
        float(mob.get_left()[0]), float(mob.get_right()[0]),
        float(mob.get_bottom()[1]), float(mob.get_top()[1]),
    )


def _overlap_fraction(a: tuple, b: tuple) -> float:
    ax0, ax1, ay0, ay1 = a
    bx0, bx1, by0, by1 = b
    ix = max(0.0, min(ax1, bx1) - max(ax0, bx0))
    iy = max(0.0, min(ay1, by1) - max(ay0, by0))
    inter = ix * iy
    if inter <= 0:
        return 0.0
    area_a = max((ax1 - ax0) * (ay1 - ay0), 1e-9)
    area_b = max((bx1 - bx0) * (by1 - by0), 1e-9)
    return inter / min(area_a, area_b)


class QASceneMixin:
    """
    Mix into a Scene to record per-frame geometry.

    Sampling every frame is affordable because we record boxes, not pixels: a
    60-second scene at 30fps with 40 text mobjects is well under a megabyte.
    """

    qa_sample_every: int = 1        # frames
    qa_enabled: bool = True

    def setup(self):
        super().setup()
        self._qa_samples: list[Sample] = []
        self._qa_ids: dict[int, int] = {}
        self._qa_keep: list = []
        self._qa_frame_no = 0
        self._qa_labels: dict[int, str] = {}

    # Manim calls this once per rendered frame, after mobjects have been updated.
    def update_to_time(self, t):
        super().update_to_time(t)
        if not self.qa_enabled:
            return
        self._qa_frame_no += 1
        if self._qa_frame_no % self.qa_sample_every:
            return
        self._qa_capture(float(getattr(self.renderer, "time", t)))

    def wait(self, duration=1.0, stop_condition=None, frozen_frame=None):
        """
        Sample around every hold.

        Manim optimises a static wait into a single frozen frame, so
        `update_to_time` never fires for its duration. Without this, a scene that
        arranges a broken layout and then simply holds it would sail through QA —
        which is exactly the kind of frame a human ends up catching. Sampling the
        start and end of each hold closes that hole.
        """
        if self.qa_enabled:
            self._qa_capture(float(getattr(self.renderer, "time", 0.0)))
        super().wait(duration, stop_condition=stop_condition, frozen_frame=frozen_frame)
        if self.qa_enabled:
            self._qa_capture(float(getattr(self.renderer, "time", 0.0)))

    def _qa_camera(self):
        """The camera to project through, or None for a flat scene."""
        cam = getattr(self, "camera", None)
        return cam if hasattr(cam, "project_points") else None

    def _qa_fixed_ids(self) -> set:
        """
        Mobjects pinned to the camera frame.

        These are drawn without the camera transform, so their coordinates are
        already screen coordinates — projecting them again would move them
        somewhere the viewer never sees them.
        """
        ids = set()
        for m in getattr(self, "_pinned", []) or []:
            for sub in m.get_family():
                ids.add(id(sub))
        return ids

    def _qa_uid(self, sub) -> int:
        """
        A stable per-scene id for a mobject.

        CPython reuses id() once an object is freed, which would splice two
        different mobjects into one timeline and invent flickers. Holding a
        reference alongside the id keeps them distinct for the whole render.
        """
        key = id(sub)
        uid = self._qa_ids.get(key)
        if uid is None:
            uid = len(self._qa_ids)
            self._qa_ids[key] = uid
            self._qa_keep.append(sub)
        return uid

    def _qa_draw_order(self) -> list[tuple[Mobject, Mobject]]:
        """
        The order the renderer actually paints in, as (top_level, member) pairs.

        Manim flattens the whole scene, keeps the *last* occurrence of anything
        added twice, and then stable-sorts the result by ``z_index``. Recording
        plain scene-traversal order instead describes a layering the viewer never
        sees, so every layer check would be judging the wrong picture — and would
        keep reporting a flip after the fix that removed it.
        """
        pairs: list[tuple[Mobject, Mobject]] = []
        seen: dict[int, int] = {}
        for mob in self.mobjects:
            for sub in mob.get_family():
                key = id(sub)
                if key in seen:
                    pairs[seen[key]] = (None, None)     # last occurrence wins
                seen[key] = len(pairs)
                pairs.append((mob, sub))
        pairs = [p for p in pairs if p[0] is not None]
        pairs.sort(key=lambda pair: getattr(pair[1], "z_index", 0))
        return pairs

    def _qa_claimed(self) -> set:
        """
        Ids that belong to something already recorded as a whole.

        A node's inner shapes, an arrow's head, a Text's glyph paths: recording
        those separately would double-count the thing they are part of. Anything
        drawn that is *not* in here is a shape in its own right.
        """
        claimed = set()
        for mob in self.mobjects:
            for sub in mob.get_family():
                # A dashed outline is one shape drawn as twenty-six pieces.
                # Recording each dash separately turned a single ghost outline
                # into twenty-six "shapes crossing the label", and the end card
                # reported two hundred of them.
                if getattr(sub, "qa_role", None) in ("node", "edge") or _is_text(sub) \
                        or isinstance(sub, (Arrow, Vector, DashedVMobject)):
                    for kid in sub.get_family():
                        if kid is not sub:
                            claimed.add(id(kid))
        return claimed

    def _qa_capture(self, t: float):
        boxes = []
        order = 0
        camera = self._qa_camera()
        fixed = self._qa_fixed_ids() if camera is not None else set()
        claimed = self._qa_claimed()
        for mob, sub in self._qa_draw_order():
            order += 1
            if not _visible(sub) or getattr(sub, "qa_ignore", False):
                continue          # review-only furniture, not composition
            is_text = _is_text(sub)
            is_arrow = isinstance(sub, (Arrow, Vector))
            role = getattr(sub, "qa_role", None)
            # Plain geometry counts too. A SurroundingRectangle drawn across
            # the title is not a node, not an edge and not text, so with only
            # role-tagged mobjects recorded it was invisible to every check.
            # Own points, not family points: a VGroup is a container with no
            # geometry of its own, and recording it as a shape made every
            # container look like a filled slab sitting across the text of
            # its own children.
            # Any drawn shape that is not part of something already recorded.
            #
            # The previous rule required the shape to *be* the top-level scene
            # mobject (`sub is mob`), so anything one level down inside a plain
            # VGroup was invisible — which is every chip(), dot(), bar and tile
            # in the video, because those helpers wrap their Square in a VGroup
            # and the VGroup itself carries no points. Thirty-four falling chips
            # could appear, move and vanish and the recorder logged two boxes.
            # That is why the flood blipping out went unreported.
            is_top_shape = (not is_text and not is_arrow and role is None
                            and len(getattr(sub, "points", [])) > 0
                            and id(sub) not in claimed)
            if not (is_text or is_arrow or role in ("node", "edge") or is_top_shape):
                continue
            (x0, x1, y0, y1), depth = _screen(
                sub, None if id(sub) in fixed else camera)
            if (x1 - x0) < 1e-4 and (y1 - y0) < 1e-4:
                continue          # no size on screen, whatever it is
            record = {
                "id": self._qa_uid(sub),
                "kind": ("text" if is_text
                         else "node" if role == "node"
                         else "arrow" if is_arrow
                         else "edge" if role == "edge" else "shape"),
                "box": [x0, x1, y0, y1],
                # Render order. Manim draws in the order mobjects were added,
                # so this says which of two things is in front.
                "z": order,
                # A VGroup carries no fill of its own — its children do — so
                # reading fill_opacity off the group reports 0 for every node
                # and silently excludes it from every check.
                "opacity": (float(getattr(sub, "fill_opacity", 1.0) or 0.0)
                            if is_text else _effective_opacity(sub)),
            }
            if camera is not None and id(sub) not in fixed:
                record["depth"] = round(depth, 3)
            if camera is not None and id(sub) not in fixed:
                record["depth"] = round(depth, 3)
            if is_text:
                record["text"] = str(getattr(sub, "text", ""))[:60]
                record["colour"] = _hex(sub)
                record["stroke"] = max(
                    (float(getattr(s, "stroke_width", 0) or 0)
                     for s in sub.get_family()), default=0.0)
                record["height"] = y1 - y0
                # font_size, not bbox height: "an answer" has no ascenders and
                # measures shorter than "which version?" at the same size.
                record["font_size"] = _rendered_pt(sub)
                # Scale-invariant at construction, so scale it the same way the
                # point size is scaled.
                gap0 = getattr(sub, "qa_word_gap0", None)
                d0 = getattr(sub, "qa_diag0", None)
                if gap0 is not None and d0:
                    record["word_gap"] = round(gap0 * (_diag(sub) / float(d0)), 4)
                # Deliberate overlaps (a stamp over a quote) are declared on
                # the mobject so the checker can tell intent from accident.
                allow = getattr(sub, "qa_allow_overlap", None)
                if allow:
                    record["allow_overlap"] = list(allow)
            if is_arrow or role == "edge":
                try:
                    record["tip"] = [float(v) for v in sub.get_end()[:2]]
                    record["tail"] = [float(v) for v in sub.get_start()[:2]]
                except Exception:
                    # A container with no points of its own: nothing to check.
                    continue
            if role == "node" or is_top_shape:
                record["colour"] = _hex(sub)
                record["fill_colour"] = _fill_hex(sub)
                record["fill"] = max(
                    (float(getattr(s, "fill_opacity", 0.0) or 0.0)
                     for s in sub.get_family()), default=0.0)
            if role == "node":
                record["node_kind"] = getattr(sub, "qa_kind", "")
                lbl = getattr(sub, "qa_label", None)
                record["label"] = str(getattr(lbl, "text", "")) if lbl is not None else ""
                record["label_visible"] = bool(
                    lbl is not None and float(getattr(lbl, "fill_opacity", 0) or 0) > 0.35)
            boxes.append(record)
        self._qa_samples.append(Sample(t=t, boxes=boxes, sig=self._qa_signature()))

    def _qa_signature(self) -> float:
        """
        A cheap aggregate of everything that affects how the frame looks.

        Bounding boxes alone cannot tell that a node is pulsing: a highlight
        changes stroke weight and colour while every box stays put, and the
        dead-air check would call that a frozen frame. Folding stroke, opacity
        and colour into one number lets it tell "nothing moved" from "nothing
        happened at all".
        """
        total = 0.0
        for mob in self.mobjects:
            for sub in mob.get_family():
                try:
                    fill = float(getattr(sub, "fill_opacity", 0.0) or 0.0)
                    stroke = float(getattr(sub, "stroke_opacity", 0.0) or 0.0)
                    # Only what is actually visible. Manim adds and drops
                    # zero-opacity family members during a hold; counting those
                    # made the signature drift and the dead-air check miss a
                    # seven-second frozen frame.
                    if max(fill, stroke) < 0.02:
                        continue
                    total += float(getattr(sub, "stroke_width", 0.0) or 0.0)
                    total += 10.0 * fill
                    total += 7.0 * stroke
                    colour = getattr(sub, "color", None)
                    if colour is not None:
                        # crc32, not hash(): Python randomises string hashing per
                        # process, so hash() made this signature differ between
                        # renders of the identical scene — and the dead-air check
                        # that compares signatures fired or not depending on the
                        # seed. A check that works only sometimes is worse than
                        # no check, because it is trusted.
                        total += (zlib.crc32(str(colour).encode()) % 997) * 1e-3
                except Exception:
                    continue
        return round(total, 3)

    def tear_down(self):
        self.qa_write()
        super().tear_down()

    def qa_write(self, out_dir: Path | None = None):
        if not self.qa_enabled or not getattr(self, "_qa_samples", None):
            return
        out_dir = out_dir or Path("out/qa")
        out_dir.mkdir(parents=True, exist_ok=True)
        dest = out_dir / f"{type(self).__name__}.geometry.json"
        try:
            bg = str(self.camera.background_color).upper()[:7]
        except Exception:
            bg = "#00020A"
        dest.write_text(json.dumps(
            {"scene": type(self).__name__,
             "background": bg,
             "has_title": getattr(self, "_title", None) is not None,
             "is_3d": self._qa_camera() is not None,
             "waivers": list(getattr(self, "_qa_waivers", [])),
             "samples": [asdict(s) for s in self._qa_samples]},
        ))

    def qa_waive(self, check: str, start: float, end: float, reason: str):
        """
        Declare that a check does not apply between two times.

        Same principle as style.allow_overlap: a composition that is lopsided on
        purpose — a flood piling up against a wall, where the whole point is that
        one side is overwhelmed — should be declared, not accommodated by loosening
        the threshold until the check stops finding anything.
        """
        if not hasattr(self, "_qa_waivers"):
            self._qa_waivers = []
        self._qa_waivers.append(
            {"check": check, "start": round(start, 3), "end": round(end, 3),
             "reason": reason})


# ------------------------------------------------------------------ checks --
def _contiguous(times: list[float], gap: float = 2.5) -> list[tuple[float, float]]:
    """
    Split a sorted list of sample times into unbroken runs.

    The gap has to exceed the sampling interval, which is coarse during a static
    hold — Manim freezes those frames, so only the two ends get sampled and
    consecutive samples can be seconds apart while nothing is wrong.
    """
    if not times:
        return []
    runs, start, prev = [], times[0], times[0]
    for t in times[1:]:
        if t - prev > gap:
            runs.append((start, prev))
            start = t
        prev = t
    runs.append((start, prev))
    return runs


def _gap(a: list, b: list) -> float | None:
    """Shortest clearance between two axis-aligned boxes; None if they overlap."""
    dx = max(a[0] - b[1], b[0] - a[1], 0.0)
    dy = max(a[2] - b[3], b[2] - a[3], 0.0)
    if dx == 0.0 and dy == 0.0:
        return None          # overlapping — a different check owns that
    return (dx ** 2 + dy ** 2) ** 0.5


def _allowed(a: dict, b: dict) -> bool:
    """Was this overlap declared deliberate by the scene?"""
    return (b.get("text", "") in a.get("allow_overlap", [])
            or a.get("text", "") in b.get("allow_overlap", []))


def check_geometry(path: Path, min_font_size: float = MIN_FONT_SIZE_RENDERED) -> list[dict]:
    """
    Run every geometric check over a recorded scene. Returns violations, each
    with the timestamp so the offending frame can be re-rendered and annotated.
    """
    data = json.loads(Path(path).read_text())
    scene = data["scene"]
    violations: list[dict] = []
    seen: set[tuple] = set()

    def add(kind: str, t: float, detail: str, boxes: list, key: tuple):
        # Report the first frame of a violation, not all 40 frames of it.
        if key in seen:
            return
        seen.add(key)
        violations.append({"scene": scene, "check": kind, "t": round(t, 3),
                           "detail": detail, "boxes": boxes})

    for sample in data["samples"]:
        t = sample["t"]
        texts = [b for b in sample["boxes"] if b["kind"] == "text" and b["opacity"] > 0.35]
        arrows = [b for b in sample["boxes"] if b["kind"] == "arrow"]

        for i, a in enumerate(texts):
            # Too small to read. Only judged once the text has settled: a
            # mobject caught mid-transform is briefly any size, and flagging
            # those buries the real defects in noise.
            # Legibility is judged separately, over settled runs — see below. A
            # FadeIn(scale=0.85) passes through every size on its way in, and
            # flagging those transients buries the real defects in noise.
            # outside the safe area
            x0, x1, y0, y1 = a["box"]
            if (x0 < stage.STAGE.left - 0.02 or x1 > stage.STAGE.right + 0.02
                    or y0 < -stage.FRAME_H / 2 + 0.05 or y1 > stage.FRAME_H / 2 - 0.05):
                add("out_of_frame", t, f"{a['text']!r} reaches outside the safe area",
                    [a["box"]], ("oof", a["text"]))
            # text over text
            for b in texts[i + 1:]:
                if _allowed(a, b):
                    continue
                frac = _overlap_fraction(tuple(a["box"]), tuple(b["box"]))
                if frac > OVERLAP_TOLERANCE:
                    add("text_overlap", t,
                        f"{a['text']!r} overlaps {b['text']!r} ({frac:.0%} of the smaller box)",
                        [a["box"], b["box"]], ("ovl", *sorted([a["text"], b["text"]])))

        # arrowheads landing on words
        for arrow in arrows:
            tip = arrow.get("tip")
            if not tip:
                continue
            for a in texts:
                x0, x1, y0, y1 = a["box"]
                if x0 - 0.04 <= tip[0] <= x1 + 0.04 and y0 - 0.04 <= tip[1] <= y1 + 0.04:
                    add("arrow_into_label", t, f"an arrowhead lands on {a['text']!r}",
                        [a["box"]], ("arrow", a["text"]))


    # --- legibility, judged only where a size actually persists ---
    runs: dict[tuple, list[float]] = {}
    for sample in data["samples"]:
        for b in sample["boxes"]:
            # Anything a viewer can actually see counts. 0.85-opacity text is
            # plainly readable; only genuinely ghosted, de-emphasised text is
            # exempt. An earlier 0.9 threshold let a whole diagram of 7.5pt
            # labels through because a copy had set the group to 0.85.
            if b["kind"] != "text" or b["opacity"] <= 0.5:
                continue
            fs = b.get("font_size")
            if fs is None:
                continue
            runs.setdefault((b["id"], round(fs, 1)), []).append(sample["t"])
    for (mid, fs), times in runs.items():
        if fs >= min_font_size:
            continue
        # Contiguous runs only. A mobject animated twice passes through the same
        # size at both ends, and treating those scattered samples as one span
        # reported a half-minute of illegible text that never existed.
        times.sort()
        for start, end in _contiguous(times):
            held = end - start
            if held < SETTLED_SECONDS:
                continue      # a size the animation merely passed through
            label = next((b.get("text", "") for s in data["samples"]
                          for b in s["boxes"] if b["id"] == mid), "?")
            add("text_too_small", start,
                f"{label!r} sits at {fs:.1f}pt for {held:.1f}s (min {min_font_size:.0f}pt)",
                [], ("small", label, fs, round(start, 1)))

    return violations



def _seg_hits_box(p0, p1, box, pad: float = 0.04) -> bool:
    """Does segment p0->p1 pass through an axis-aligned box? (slab method)"""
    x0, x1, y0, y1 = box[0] - pad, box[1] + pad, box[2] - pad, box[3] + pad
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    t_enter, t_exit = 0.0, 1.0
    for delta, lo, hi, start in ((dx, x0, x1, p0[0]), (dy, y0, y1, p0[1])):
        if abs(delta) < 1e-9:
            if start < lo or start > hi:
                return False
            continue
        t1, t2 = (lo - start) / delta, (hi - start) / delta
        if t1 > t2:
            t1, t2 = t2, t1
        t_enter, t_exit = max(t_enter, t1), min(t_exit, t2)
        if t_enter > t_exit:
            return False
    return True


def _border_crosses(shape_box, text_box, pad: float = OUTLINE_TEXT_PAD) -> bool:
    """
    Does the shape's own outline run through the text?

    A card behind a label is the visual language and is fine — the label sits
    *inside* the shape, clear of its edges. What is not fine is a boundary
    passing between the letters: the gold circle drawn a little too small around
    "traversal", the diamond vertex punching up through "reviewer", the bottom
    edge of a code square landing across "coordination". In every one of those
    the text box straddles one of the shape's four sides, and the stroke is drawn
    through the letterforms whichever way the z-order happens to fall.
    """
    sx0, sx1, sy0, sy1 = shape_box
    tx0, tx1, ty0, ty1 = text_box
    # No relationship at all if the boxes do not meet.
    if tx1 < sx0 - pad or tx0 > sx1 + pad or ty1 < sy0 - pad or ty0 > sy1 + pad:
        return False
    # A vertical side of the shape falling strictly inside the text's width.
    for side in (sx0, sx1):
        if tx0 + pad < side < tx1 - pad and ty0 < sy1 and ty1 > sy0:
            return True
    # A horizontal side falling strictly inside the text's height.
    for side in (sy0, sy1):
        if ty0 + pad < side < ty1 - pad and tx0 < sx1 and tx1 > sx0:
            return True
    return False


def _near(point, box, pad: float = 0.28) -> bool:
    """Is this point at (or just outside) the box — i.e. plausibly an endpoint?"""
    return (box[0] - pad <= point[0] <= box[1] + pad
            and box[2] - pad <= point[1] <= box[3] + pad)


def _node_moving(track: list, at: float, window: float = 0.5,
                 threshold: float = 0.06) -> bool:
    """Did this node's box change appreciably around time `at`?"""
    near = [box for t, box in track if abs(t - at) <= window]
    if len(near) < 2:
        return False
    for k in range(4):
        vals = [b[k] for b in near]
        if max(vals) - min(vals) > threshold:
            return True
    return False


def check_structure(path: Path) -> list[dict]:
    """
    Checks over the diagram itself rather than its text.

    Text-vs-text overlap was never the whole story: two nodes stacked on each
    other, or a connector drawn straight through a node it has nothing to do
    with, are just as wrong and were previously invisible to every check here.
    Roles are tagged at construction, so this reads intent rather than guessing
    it from geometry.
    """
    data = json.loads(Path(path).read_text())
    scene = data["scene"]
    # The outline check assumes a flat composition, where the author chose both
    # where the shape is and where the label is. In a 3D scene the camera decides
    # what crosses what from one frame to the next, and a node passing behind a
    # label at a different depth is perspective rather than a collision — the two
    # 3D sections produced three hundred such reports and not one of them was a
    # defect. Legibility there is covered by text_too_small and node_off_frame.
    is_3d = bool(data.get("is_3d"))
    waivers = data.get("waivers", [])
    violations: list[dict] = []
    seen: set[tuple] = set()

    def waived(kind: str, t: float) -> bool:
        return any(w["check"] == kind and w["start"] <= t <= w["end"] for w in waivers)

    def add(kind: str, t: float, detail: str, boxes: list, key: tuple):
        if key in seen or waived(kind, t):
            return
        seen.add(key)
        violations.append({"scene": scene, "check": kind, "t": round(t, 3),
                           "detail": detail, "boxes": boxes})

    label_state: dict[int, list[tuple[float, bool, str]]] = {}
    pending: dict[tuple, list] = {}
    shape_pending: dict[tuple, list] = {}
    contrast_pending: dict[int, list] = {}
    clip_pending: dict[int, list] = {}
    stroke_pending: dict[tuple, list] = {}
    crowd_pending: dict[tuple, list] = {}
    border_pending: dict[tuple, list] = {}
    life: dict[int, list] = {}
    dim_pending: dict[tuple, list] = {}
    merge_pending: dict[int, list] = {}
    nowhere_pending: dict[int, list] = {}
    aimed: set = set()
    stroked_pending: dict[int, list] = {}
    layer_pending: dict[tuple, list] = {}
    scene_bg = data.get("background", "#00020A")
    lane_pending: dict[int, list] = {}
    node_boxes: dict[int, list[tuple[float, list]]] = {}

    for sample_no, sample in enumerate(sorted(data["samples"], key=lambda s: s["t"])):
        t = sample["t"]
        nodes = [b for b in sample["boxes"] if b["kind"] == "node" and b["opacity"] > 0.5]
        edges = [b for b in sample["boxes"]
                 if b["kind"] in ("edge", "arrow") and b["opacity"] > 0.5 and b.get("tail")]

        for i, a in enumerate(nodes):
            for b in nodes[i + 1:]:
                # In a 3D scene two nodes at different depths overlapping on
                # screen is perspective doing its job, not a layout mistake.
                # Only nodes at effectively the same depth are colliding.
                if abs(a.get("depth", 0.0) - b.get("depth", 0.0)) > DEPTH_SEPARATION:
                    continue
                frac = _overlap_fraction(tuple(a["box"]), tuple(b["box"]))
                if frac > NODE_OVERLAP_TOLERANCE:
                    key = tuple(sorted([a["id"], b["id"]]))
                    pending.setdefault(key, []).append(
                        (t, frac, a.get("label") or a.get("node_kind") or "node",
                         b.get("label") or b.get("node_kind") or "node",
                         a["box"], b["box"]))

        for e in edges:
            for n in nodes:
                if _near(e["tip"], n["box"]) or _near(e["tail"], n["box"]):
                    continue          # this node is one of its endpoints
                # Same rule as node_overlap: in a 3D scene a connector passing
                # across a node at a different depth is the camera doing
                # perspective, not a line drawn through something.
                if abs(e.get("depth", 0.0) - n.get("depth", 0.0)) > DEPTH_SEPARATION:
                    continue
                if _seg_hits_box(e["tail"], e["tip"], n["box"]):
                    name = n.get("label") or n.get("node_kind") or "a node"
                    add("edge_through_node", t,
                        f"a connector crosses {name}, which it does not connect",
                        [n["box"]], ("etn", str(e["id"]), str(n["id"])))

        shapes = [b for b in sample["boxes"]
                  if b["kind"] in ("shape", "node") and b["opacity"] > 0.5]
        texts_here = [b for b in sample["boxes"]
                      if b["kind"] == "text" and b["opacity"] > 0.5]

        for sh in shapes:
            for tx in texts_here:
                # A node's own label lives inside it by design.
                if sh["kind"] == "node" and tx.get("text", "") == sh.get("label", ""):
                    continue
                if _allowed(sh, tx):
                    continue
                # An outline *around* text is a frame and reads fine — the text
                # shows straight through it. Only a filled shape buries it. And
                # measure the fraction of the TEXT covered, not of the smaller
                # box: a thin line's bounding box is tiny, so the min-area ratio
                # called every passing stroke a burial.
                if sh.get("fill", 0.0) < 0.35:
                    continue
                # Text sitting *on* a panel is a card, not a burial — that is the
                # whole visual language. Only a shape drawn in front of the text
                # actually hides it.
                if sh.get("z", 0) < tx.get("z", 0):
                    continue
                x0, x1, y0, y1 = tx["box"]
                area = max((x1 - x0) * (y1 - y0), 1e-9)
                sx0, sx1, sy0, sy1 = sh["box"]
                inter = (max(0.0, min(x1, sx1) - max(x0, sx0))
                         * max(0.0, min(y1, sy1) - max(y0, sy0)))
                frac = inter / area
                if frac > 0.55:
                    shape_pending.setdefault((sh["id"], tx["id"]), []).append(
                        (t, tx.get("text", ""), tx["box"], sh["box"]))

        for b in sample["boxes"]:
            if b["opacity"] <= 0.5 or b.get("is_title"):
                continue
            if b["kind"] == "text" and b["box"][3] > stage.TITLE.bottom \
                    and b["box"][2] > stage.TITLE.bottom - 0.05:
                continue          # the title itself
            if b["box"][3] > stage.TITLE.bottom + 0.05 and b["kind"] != "text":
                lane_pending.setdefault(b["id"], []).append((t, b["box"], b["kind"]))

        # Clipping was only ever checked for text, so a node sliding off the
        # bottom of a 3D scene passed cleanly.
        for b in sample["boxes"]:
            if b["kind"] not in ("node", "shape") or b["opacity"] <= 0.5:
                continue
            x0, x1, y0, y1 = b["box"]
            if (x0 < -stage.FRAME_W / 2 + 0.06 or x1 > stage.FRAME_W / 2 - 0.06
                    or y0 < -stage.FRAME_H / 2 + 0.06 or y1 > stage.FRAME_H / 2 - 0.06):
                clip_pending.setdefault(b["id"], []).append(
                    (t, b["box"], b.get("label") or b.get("node_kind") or b["kind"]))

        # A stroke drawn across text strikes it through — the outline case the
        # filled-shape check deliberately ignores.
        strokes = [b for b in sample["boxes"]
                   if b["kind"] in ("edge", "arrow") and b["opacity"] > 0.5 and b.get("tail")]
        for st in strokes:
            for tx in texts_here:
                if st.get("z", 0) < tx.get("z", 0):
                    continue          # behind the text, which is where edges belong
                if _seg_hits_box(st["tail"], st["tip"], tx["box"], pad=0.0):
                    stroke_pending.setdefault((st["id"], tx["id"]), []).append(
                        (t, tx.get("text", ""), tx["box"]))

        # A connector left bright while the nodes it joins are dimmed. Fading a
        # group to the background is how this video says "this is context now",
        # and an edge that does not fade with it stays at full strength across a
        # picture that is meant to have receded — which is exactly what makes a
        # dimmed diagram read as clutter rather than as background.
        bright_edges = [b for b in sample["boxes"]
                        if b["kind"] in ("edge", "arrow") and b["opacity"] > 0.55
                        and b.get("tail")]
        # Clearly dim, not merely mid-fade. A node caught at 0.45 on its way down
        # is a frame of an animation, and complaining about it reports defects
        # that exist for two sampled instants and never appear on screen.
        faded = [b for b in sample["boxes"]
                 if b["kind"] in ("node", "shape") and 0.05 < b["opacity"] <= 0.35]
        lit = [b for b in sample["boxes"]
               if b["kind"] in ("node", "shape") and b["opacity"] > 0.5]
        for e in bright_edges:
            # Both ends land on something dimmed, and neither end lands on
            # anything still lit. A bright connector between a bright node and a
            # dimmed one is a live edge into receded context — which is the
            # normal way this video shows a slice against its background, and
            # counting it made every petal in the VQP scene a violation.
            def ends_on(pool):
                return (any(_near(e["tip"], n["box"], pad=0.3) for n in pool),
                        any(_near(e["tail"], n["box"], pad=0.3) for n in pool))
            tip_dim, tail_dim = ends_on(faded)
            tip_lit, tail_lit = ends_on(lit)
            if tip_dim and tail_dim and not tip_lit and not tail_lit:
                dim_pending.setdefault(e["id"], []).append((t, 2))

        # A shape's own boundary running through the letters. Unlike
        # shape_over_text this ignores z-order entirely: a stroke drawn behind
        # text still collides with it visually, because the letters are thin and
        # the line is solid.
        for sh in (sample["boxes"] if not is_3d else ()):
            if sh["kind"] not in ("node", "shape") or sh["opacity"] <= 0.35:
                continue
            for tx in texts_here:
                if sh["id"] == tx["id"]:
                    continue
                if tx.get("allow_overlap"):
                    continue
                # A node's own label. If it does not fit, text_too_small and the
                # constructor's own size check already say so; reporting the
                # node's outline as crossing its own text says it twice and
                # buries everything else.
                if sh.get("label") and sh["label"] == tx.get("text"):
                    continue
                # In a 3D scene an outline crossing a label from a different
                # depth is the camera doing perspective, not a collision. Only
                # things at the same depth are actually touching. Without this
                # the two 3D sections reported one label 126 times.
                if abs(sh.get("depth", 0.0) - tx.get("depth", 0.0)) > DEPTH_SEPARATION:
                    continue
                if _border_crosses(sh["box"], tx["box"]):
                    border_pending.setdefault((sh["id"], tx["id"]), []).append(
                        (t, tx.get("text", ""), tx["box"], sh["box"]))

        # An arrow whose tip lands on nothing. This happens when the thing it
        # pointed at moves and the arrow does not go with it — the connector is
        # left hanging into empty space, aimed at a memory.
        for e in [b for b in sample["boxes"]
                  if b["kind"] in ("edge", "arrow") and b["opacity"] > 0.6
                  and b.get("tip")]:
            targets = [b for b in sample["boxes"]
                       if b["kind"] in ("node", "shape", "text")
                       and b["opacity"] > 0.25 and b["id"] != e["id"]]
            if len(targets) < 2:
                continue                  # an almost-empty stage says nothing
            hit = any(_near(e["tip"], t["box"], pad=ARROW_TARGET_PAD) for t in targets)
            if hit:
                aimed.add(e["id"])
            elif e["id"] in aimed:
                # Only an arrow that *was* pointing at something and now is not.
                # An arrow that never had a target is a deliberate marker — the
                # chevron pointing at the bottom of the frame to mean "down in
                # the description" is aimed at nothing on purpose.
                nowhere_pending.setdefault(e["id"], []).append((t, e["tip"]))

        # Two words rendering as one.
        for tx in texts_here:
            gap = tx.get("word_gap")
            if gap is not None and gap * REVIEW_PX_PER_UNIT < MIN_WORD_GAP_PX:
                merge_pending.setdefault(tx["id"], []).append(
                    (t, tx.get("text", ""), gap))

        # How long is each piece of text actually up for? Recorded by sample
        # *index*, not by time: a static hold is frozen into two samples that can
        # be six seconds apart, so grouping by elapsed time chops a caption that
        # never left the screen into a string of imaginary flashes.
        for tx in texts_here:
            if tx.get("is_title"):
                continue                  # a title is scenery, not a caption
            life.setdefault(tx["id"], []).append((sample_no, t, tx.get("text", "")))

        # Crowding: legible on their own, unreadable as a pair.
        for i, a in enumerate(texts_here):
            for b in texts_here[i + 1:]:
                gap = _gap(a["box"], b["box"])
                if gap is not None and 0 < gap < MIN_TEXT_GAP:
                    crowd_pending.setdefault(
                        tuple(sorted([a["id"], b["id"]])), []).append(
                        (t, a.get("text", ""), b.get("text", ""), gap, a["box"], b["box"]))

        # Heavy stroke on a letterform closes its counters.
        for tx in texts_here:
            if float(tx.get("stroke", 0) or 0) > 2.0:
                stroked_pending.setdefault(tx["id"], []).append(
                    (t, tx.get("text", ""), tx["stroke"], tx["box"]))

        # A connector drawn *over* the node it attaches to. Comparing every
        # edge against every node instead flagged hundreds of harmless
        # reorderings, because index interleaving shifts constantly as mobjects
        # come and go while the visible layering never changes.
        for st in strokes:
            for n in nodes:
                if not (_near(st["tip"], n["box"], pad=0.2)
                        or _near(st["tail"], n["box"], pad=0.2)):
                    continue
                if st.get("z", 0) > n.get("z", 0):
                    layer_pending.setdefault((st["id"], n["id"]), []).append(
                        (t, n.get("label") or n.get("node_kind") or "a node"))

        for n in nodes:
            node_boxes.setdefault(n["id"], []).append((t, n["box"]))
            if n.get("label"):
                label_state.setdefault(n["id"], []).append(
                    (t, bool(n.get("label_visible")), n["label"]))

    # Two nodes converging mid-transform overlap for a moment by definition —
    # that is what a transform looks like. Only an overlap that persists is a
    # layout mistake the viewer gets time to notice.
    for key, hits in pending.items():
        held = hits[-1][0] - hits[0][0]
        if held < OVERLAP_SETTLE_SECONDS:
            continue
        # If both nodes are in motion throughout, this is a transform converging,
        # not two things parked on top of each other.
        mid = hits[len(hits) // 2][0]
        if (_node_moving(node_boxes.get(key[0], []), mid)
                and _node_moving(node_boxes.get(key[1], []), mid)):
            continue
        t0, frac, na, nb, box_a, box_b = max(hits, key=lambda h: h[1])
        add("node_overlap", hits[0][0],
            f"{na} and {nb} overlap for {held:.1f}s (up to {frac:.0%} of the smaller)",
            [box_a, box_b], ("nov", *map(str, key)))

    # --- contrast: is this text readable against what is behind it? ---
    for sample in sorted(data["samples"], key=lambda s: s["t"]):
        texts_here = [b for b in sample["boxes"]
                      if b["kind"] == "text" and b["opacity"] > 0.5]
        panels = [b for b in sample["boxes"]
                  if b["kind"] in ("node", "shape") and b.get("fill", 0) > 0.5
                  and b["opacity"] > 0.5]
        for tx in texts_here:
            fg = tx.get("colour") or ""
            # Whatever filled shape sits under the text is its background;
            # otherwise the text is on the scene's own ground.
            bg = scene_bg
            for pl in panels:
                if (pl["box"][0] <= tx["box"][0] and pl["box"][1] >= tx["box"][1]
                        and pl["box"][2] <= tx["box"][2] and pl["box"][3] >= tx["box"][3]):
                    bg = pl.get("fill_colour") or bg
                    break
            ratio = contrast_ratio(fg, bg)
            if ratio is None:
                continue
            need = (MIN_CONTRAST_LARGE if (tx.get("font_size") or 0) >= LARGE_TEXT_PT
                    else MIN_CONTRAST_BODY)
            if ratio < need:
                contrast_pending.setdefault(tx["id"], []).append(
                    (sample["t"], tx.get("text", ""), ratio, need, fg, bg, tx["box"]))

    for mid, hits in contrast_pending.items():
        held = hits[-1][0] - hits[0][0]
        if held < OVERLAP_SETTLE_SECONDS:
            continue
        t0, text, ratio, need, fg, bg, box = hits[0]
        add("low_contrast", t0,
            f"{text!r} is {ratio:.1f}:1 against {bg} (needs {need}:1) for {held:.1f}s",
            [box], ("contrast", str(mid)))

    for mid, hits in clip_pending.items():
        held = hits[-1][0] - hits[0][0]
        if held < OVERLAP_SETTLE_SECONDS:
            continue
        t0, box, name = hits[0]
        add("node_off_frame", t0,
            f"{name} is outside the frame for {held:.1f}s",
            [box], ("clip", str(mid)))

    for key, hits in stroke_pending.items():
        held = hits[-1][0] - hits[0][0]
        if held < OVERLAP_SETTLE_SECONDS:
            continue
        t0, text, box = hits[0]
        add("stroke_over_text", t0,
            f"a line is drawn across {text!r} for {held:.1f}s", [box],
            ("stroke", *map(str, key)))

    for eid, hits in nowhere_pending.items():
        times = [h[0] for h in hits]
        runs = [(a, b) for a, b in _contiguous(times)
                if b - a >= 1.0 and sum(1 for t in times if a <= t <= b) >= 3]
        if not runs:
            continue
        a, b = max(runs, key=lambda r: r[1] - r[0])
        add("arrow_to_nowhere", a,
            f"an arrow pointed at empty space for {b - a:.1f}s — whatever it "
            "aimed at is no longer there",
            [], ("nowhere", str(eid)))

    for tid, hits in merge_pending.items():
        runs = _contiguous([h[0] for h in hits])
        if not runs or max(b - a for a, b in runs) < OVERLAP_SETTLE_SECONDS:
            continue
        t0, text, gap = hits[0]
        add("words_merged", t0,
            f"{text!r} has only {gap * REVIEW_PX_PER_UNIT:.1f}px between two of its "
            f"words at review size (want {MIN_WORD_GAP_PX}px) — they read as one word",
            [], ("merge", str(tid)))

    # Contiguous runs, not first-hit to last-hit. One frame during the fade and
    # one during the fade back are seven seconds apart and describe nothing; read
    # as a single run they invent a seven-second defect that never existed. This
    # is the same mistake the legibility and dead-air checks each made once.
    for eid, hits in dim_pending.items():
        times = [h[0] for h in hits]
        runs = [(a, b) for a, b in _contiguous(times)
                # Three samples minimum: two isolated frames cannot describe a
                # state the picture was actually in.
                if b - a >= 1.0 and sum(1 for t in times if a <= t <= b) >= 3]
        if not runs:
            continue
        a, b = max(runs, key=lambda r: r[1] - r[0])
        add("partial_dim", a,
            f"a connector stayed at full strength for {b - a:.1f}s while the "
            "shapes it joins were dimmed to background",
            [], ("dim", str(eid)))

    # An outline through the letters is legible for exactly as long as it takes
    # to notice; unlike a layout overlap it does not need to settle to be wrong,
    # but a shape passing across a label mid-transform is not the complaint.
    for key, hits in border_pending.items():
        by_time = {h[0]: h for h in hits}
        runs = [(a, b) for a, b in _contiguous([h[0] for h in hits])
                if b - a >= OVERLAP_SETTLE_SECONDS]
        if not runs:
            continue
        # One report per pair — the worst run. The same shape crossing the same
        # label in eleven separate stretches is one thing to fix, and listing it
        # eleven times drowns the rest of the report.
        a, b = max(runs, key=lambda r: r[1] - r[0])
        _t, text, tbox, sbox = by_time[a]
        add("outline_over_text", a,
            f"a shape's outline runs through {text!r} for {b - a:.1f}s"
            + (f" (and {len(runs) - 1} shorter stretches)" if len(runs) > 1 else ""),
            [tbox, sbox], ("bord", *map(str, key)))

    # Was there time to read it? Reading speed, not a fixed minimum: "REQ-17" and
    # "a rendered screen, a captured output, a physical test trace" do not need
    # the same number of seconds, and holding both to one threshold either lets
    # the long one flash past or complains about every short identifier.
    for tid, hits in life.items():
        text = hits[0][2]
        if len(text) < 12:
            continue                      # an identifier is taken in at a glance
        need = (READ_FIXED_COST + len(text) / READ_CHARS_PER_SECOND) * EXPORT_SPEED
        run_start_t = hits[0][1]
        prev_no, prev_t = hits[0][0], hits[0][1]
        runs: list[tuple[float, float]] = []
        for no, tt, _txt in hits[1:]:
            if no != prev_no + 1:
                runs.append((run_start_t, prev_t))
                run_start_t = tt
            prev_no, prev_t = no, tt
        runs.append((run_start_t, prev_t))
        for a, b in runs:
            shown = b - a
            if shown + 1e-6 < need:
                add("text_too_brief", a,
                    f"{text!r} was up for {shown:.1f}s; {len(text)} characters "
                    f"needs about {need:.1f}s to read at {EXPORT_SPEED}x",
                    [], ("brief", str(tid), f"{a:.1f}"))

    for key, hits in crowd_pending.items():
        held = hits[-1][0] - hits[0][0]
        if held < OVERLAP_SETTLE_SECONDS:
            continue
        t0, ta, tb, gap, box_a, box_b = hits[0]
        add("text_crowding", t0,
            f"{ta!r} and {tb!r} sit {gap:.2f} apart (want {MIN_TEXT_GAP}) for {held:.1f}s",
            [box_a, box_b], ("crowd", *map(str, key)))

    for mid, hits in stroked_pending.items():
        held = hits[-1][0] - hits[0][0]
        if held < 0.8:      # a transform briefly shares the target's stroke
            continue
        t0, text, width, box = hits[0]
        add("text_stroked", t0,
            f"{text!r} carries a {width:.1f}-wide stroke for {held:.1f}s", [box],
            ("stroked", str(mid)))

    for key, hits in layer_pending.items():
        held = hits[-1][0] - hits[0][0]
        if held >= 0.8:
            t0, name = hits[0]
            add("z_order_flip", t0,
                f"a connector is drawn on top of {name}, which it attaches to, "
                f"for {held:.1f}s", [], ("zflip", *map(str, key)))
        elif hits[0][0] > 0.05:
            # Short, and therefore *visible as a change*: the line appears in
            # front and then drops behind, which reads as a blink. The duration
            # threshold above was written for persistent mislayering and let this
            # whole class through — the reviewer caught five of them by eye.
            t0, name = hits[0]
            add("layer_transient", t0,
                f"a connector is drawn in front of {name} for {held:.2f}s and "
                "then drops behind it — visible as a blink",
                [], ("ztrans", *map(str, key)))

    for key, hits in shape_pending.items():
        held = hits[-1][0] - hits[0][0]
        if held < OVERLAP_SETTLE_SECONDS:
            continue
        t0, text, tbox, sbox = hits[0]
        add("shape_over_text", t0,
            f"a shape sits across {text!r} for {held:.1f}s",
            [tbox, sbox], ("sot", *map(str, key)))

    # No title, no title lane. The 3D sections carry their captions pinned to the
    # camera and use the full height of the frame deliberately; policing a
    # reserved strip that nothing is reserved for reported 76 seconds of
    # "intrusion" into empty space.
    for mid, hits in (lane_pending.items() if data.get("has_title", True) else []):
        held = hits[-1][0] - hits[0][0]
        if held < OVERLAP_SETTLE_SECONDS:
            continue
        t0, box, kind = hits[0]
        add("title_lane_intrusion", t0,
            f"a {kind} reached into the title lane for {held:.1f}s",
            [box], ("lane", str(mid)))

    # A label that evaporates while its node stays put reads as a rendering
    # glitch even when the code meant it. If the node is going, the label should
    # go with it.
    for nid, events in label_state.items():
        was_visible = False
        for i, (t, visible, text) in enumerate(events):
            if was_visible and not visible:
                stayed = events[-1][0] - t
                # If the node is transforming at that moment, the label leaving
                # with it reads as intent. It only looks like a glitch when the
                # text evaporates off a shape that just sits there.
                moving = _node_moving(node_boxes.get(nid, []), t)
                if stayed > 1.5 and not moving:
                    add("label_orphaned", t,
                        f"{text!r} vanished off a stationary node, which then "
                        f"stayed on screen for another {stayed:.1f}s",
                        [], ("orphan", str(nid)))
                break
            was_visible = was_visible or visible

    return violations


def check_motion(path: Path, flicker_gap: float = 1.6, dead_air: float = 5.0) -> list[dict]:
    """
    Checks that need the whole timeline, not one frame.

    Video 1's review post-mortem named this as its blind spot: a still frame
    cannot show that a label flickered out and back, or that nothing moved for
    eight seconds. Both are obvious in the recorded geometry.
    """
    data = json.loads(Path(path).read_text())
    scene = data["scene"]
    violations: list[dict] = []

    # Waits are sampled at both ends, so two samples can share a timestamp — the
    # state just before a hold and just after it. Collapsing them loses the
    # transition and turns real flickers into zero-length ones; dropping either
    # invents flickers that never happened. Keep both, in capture order (sorted
    # is stable), so a run spans from the last frame something was visible to the
    # first frame it is visible again.
    samples = sorted(data["samples"], key=lambda s: s["t"])

    # --- flicker: visible -> gone -> visible again, quickly ---
    # Walked as a single ordered pass. Presence and absence events at the same
    # timestamp (the two ends of a hold) must keep their capture order, or a real
    # disappearance collapses to zero length and goes unreported.
    known: set[int] = set()
    labels: dict[int, str] = {}
    tracks: dict[int, list[tuple[float, bool]]] = {}
    for s in samples:
        here = {b["id"]: b for b in s["boxes"] if b["opacity"] > 0.35}
        known |= set(here)
        for mid, b in here.items():
            labels.setdefault(mid, b.get("text", "") or f"<{mid}>")
        for mid in known:
            tracks.setdefault(mid, []).append((s["t"], mid in here))

    for mid, events in tracks.items():
        runs: list[list] = []
        for t_, on in events:
            if not runs or runs[-1][0] != on:
                runs.append([on, t_, t_])
            else:
                runs[-1][2] = t_
        for i in range(1, len(runs) - 1):
            on, r_start, r_end = runs[i]
            if on or not (runs[i - 1][0] and runs[i + 1][0]):
                continue
            # Span from last seen to next seen — the true invisible interval.
            gone_for = runs[i + 1][1] - runs[i - 1][2]
            if 0.12 < gone_for < flicker_gap:
                violations.append({
                    "scene": scene, "check": "flicker", "t": round(r_start, 3),
                    "detail": f"{labels.get(mid, '?')!r} disappeared for "
                              f"{gone_for:.2f}s and came back",
                    "boxes": [],
                })
                break

    # --- caption lane must hold at most one thing ---
    for s in samples:
        in_lane = [b for b in s["boxes"]
                   if b["kind"] == "text" and b["opacity"] > 0.35
                   and b["box"][2] >= stage.CAPTION.bottom - 0.1
                   and b["box"][3] <= stage.CAPTION.top + 0.1]
        if len(in_lane) > 1:
            names = ", ".join(repr(b.get("text", "")) for b in in_lane[:3])
            violations.append({
                "scene": scene, "check": "caption_stack", "t": round(s["t"], 3),
                "detail": f"{len(in_lane)} captions in the lane at once: {names}",
                "boxes": [b["box"] for b in in_lane],
            })
            break

    # --- dead air: no geometry changed at all ---
    def boxes_of(s):
        return tuple(sorted((b["id"], tuple(round(v, 2) for v in b["box"]))
                            for b in s["boxes"]))

    def unchanged(a, b) -> bool:
        """
        Did the frame stay the same?

        The activity signature carries floating-point noise of a few thousandths
        between frames, so exact equality never holds and the check silently
        never fires. A change worth calling movement is far larger than that.
        """
        if boxes_of(a) != boxes_of(b):
            return False
        return abs(a.get("sig", 0.0) - b.get("sig", 0.0)) < SIG_TOLERANCE

    def flush(start, end):
        if start is not None and end is not None and end - start > dead_air:
            violations.append({
                "scene": scene, "check": "dead_air", "t": round(start, 3),
                "detail": f"nothing changed for {end - start:.1f}s",
                "boxes": [],
            })

    # A run begins at the *earlier* of the two matching samples, and the run in
    # progress when the samples run out still counts. The first version did
    # neither: it dated the run from the second sample and only reported on the
    # third, so a static hold — which Manim freezes into exactly two samples —
    # was invisible, and the last hold of any scene was never reported at all.
    # Sections 04, 06 and 09 each sat on a frozen frame for six seconds and the
    # check said nothing.
    run_start = None
    prev = None
    for s in samples:
        if prev is not None and unchanged(s, prev):
            if run_start is None:
                run_start = prev["t"]
        else:
            flush(run_start, prev["t"] if prev is not None else None)
            run_start = None
        prev = s
    flush(run_start, prev["t"] if prev is not None else None)

    return violations


def check_balance(path: Path) -> list[dict]:
    """
    Is the picture using the stage, or huddling in a corner of it?

    Deliberately blunt: the area-weighted centre of the visible composition,
    compared against the middle of the stage. It has no taste, and it is not
    supposed to — it catches the one compositional failure that is objective,
    which is content occupying a third of the frame while the rest sits empty.
    A frame that is *meant* to be off-centre (one node alone, a title card)
    passes, because a small composition has a small footprint and its centroid
    is wherever it is; what fails is a large body of content parked to one side.

    Judged only on runs long enough to read. Content sliding across the stage
    passes through every offset there is on the way.
    """
    data = json.loads(Path(path).read_text())
    scene = data["scene"]
    waived = [w for w in data.get("waivers", []) if w["check"] == "stage_imbalance"]
    half_w = (stage.STAGE.right - stage.STAGE.left) / 2
    half_h = (stage.STAGE.top - stage.STAGE.bottom) / 2
    cx0, cy0 = stage.STAGE.center[0], stage.STAGE.center[1]

    offenders: list[tuple[float, float, float, float]] = []
    for sample in data["samples"]:
        if any(w["start"] <= sample["t"] <= w["end"] for w in waived):
            continue
        boxes = [b for b in sample["boxes"]
                 if b["opacity"] > 0.35 and not b.get("is_title")
                 and b["box"][3] <= stage.TITLE.bottom + 0.05]
        if len(boxes) < 4:
            continue                      # too little on stage to have a balance
        total = 0.0
        sx = sy = 0.0
        spread_x0, spread_x1 = 1e9, -1e9
        for b in boxes:
            x0, x1, y0, y1 = b["box"]
            area = max((x1 - x0) * (y1 - y0), 1e-6)
            total += area
            sx += area * (x0 + x1) / 2
            sy += area * (y0 + y1) / 2
            spread_x0, spread_x1 = min(spread_x0, x0), max(spread_x1, x1)
        if total <= 0:
            continue
        off_x = abs(sx / total - cx0) / half_w
        off_y = abs(sy / total - cy0) / half_h
        # Content that spans the stage is balanced whatever its centroid says —
        # a wide row with a heavy end is not a huddle.
        if (spread_x1 - spread_x0) / (2 * half_w) > 0.72:
            off_x = 0.0
        if max(off_x, off_y) > MAX_CENTROID_OFFSET:
            offenders.append((sample["t"], off_x, off_y, len(boxes)))

    violations: list[dict] = []
    for a, b in _contiguous([o[0] for o in offenders]):
        held = b - a
        if held < IMBALANCE_SETTLE_SECONDS:
            continue
        worst = max((o for o in offenders if a <= o[0] <= b),
                    key=lambda o: max(o[1], o[2]))
        axis = "right/left" if worst[1] >= worst[2] else "up/down"
        violations.append({
            "scene": scene, "check": "stage_imbalance", "t": round(a, 3),
            "detail": (f"the composition sits {max(worst[1], worst[2]):.0%} off centre "
                       f"({axis}) for {held:.1f}s — {worst[3]} elements bunched into "
                       "part of the stage"),
            "boxes": [],
        })
    return violations


def check_all(path: Path, **kw) -> list[dict]:
    """Every check, geometric and motion-based."""
    return (check_geometry(path, **{k: v for k, v in kw.items() if k == "min_font_size"})
            + check_motion(path, **{k: v for k, v in kw.items()
                                    if k in ("flicker_gap", "dead_air")})
            + check_structure(path)
            + check_balance(path))


def report(violations: list[dict]) -> str:
    if not violations:
        return "PASS — no geometric violations"
    by_check: dict[str, int] = {}
    for v in violations:
        by_check[v["check"]] = by_check.get(v["check"], 0) + 1
    lines = [f"FAIL — {len(violations)} violation(s)", ""]
    for check, n in sorted(by_check.items(), key=lambda kv: -kv[1]):
        lines.append(f"  {n:>3}  {check}  — {CHECKS.get(check, '')}")
    lines.append("")
    for v in violations:
        lines.append(f"  [{v['t']:7.2f}s] {v['check']}: {v['detail']}")
    return "\n".join(lines)
