"""
Visual system for The Compiler For Trust.

One source of truth for palette, type scale, and shape grammar. Scenes never
hardcode a colour or a font size — they ask for a role. That is what makes a
global restyle a one-file change instead of a thirty-file change.
"""
from __future__ import annotations

from manim import *

# ---------------------------------------------------------------- palette ---
BG = "#00020A"
PANEL = "#070C1A"
PANEL_HI = "#0C1426"
GRID = "#1F2B42"
WHITE = "#F4F7FF"
MUTED = "#8791A8"
DIM = "#4A5468"

CYAN = "#20F7D2"
BLUE = "#4D8DFF"
VIOLET = "#B45CFF"
GOLD = "#FFCB4D"
RED = "#FF4D6D"
GREEN = "#49F28D"
AMBER = "#FF9E45"

# Shape grammar — the contract the storyboard promises the viewer.
NODE_KINDS = {
    "requirement": {"color": GOLD, "shape": "hexagon"},
    "code": {"color": BLUE, "shape": "square"},
    "test": {"color": CYAN, "shape": "circle"},
    "result": {"color": GREEN, "shape": "record"},
    "evidence": {"color": GREEN, "shape": "record"},
    "source": {"color": VIOLET, "shape": "document"},
    "review": {"color": VIOLET, "shape": "diamond"},
    "vqp": {"color": GREEN, "shape": "packet"},
    "anomaly": {"color": RED, "shape": "square"},
}

# ------------------------------------------------------------- type scale ---
# Sizes are in Manim font_size units, tuned so the smallest is still legible
# after a 480p preview downscale. QA enforces MIN_FONT_SIZE.
TYPE = {
    "title": 40,
    "caption": 28,
    "label": 22,
    "node": 17,
    "field": 17,
    # 17, not 16. Pango's space advance rounds down a whole pixel below 17pt, so
    # every multi-word label set at 16 rendered with a ~3.5px word gap at review
    # size and read as one word — "makes an" as "makesan". At 17 the same phrases
    # come out at 6px. One point of type size, and a whole class of defect.
    "tiny": 17,
}
MIN_FONT_SIZE = 15
MONO = "DejaVu Sans Mono"

# Texts need air between them, not merely an absence of overlap. Below this gap
# two lines read as one block. Both the placement helper and the gate use this
# number, so a layout that satisfies the placer cannot fail the gate.
MIN_TEXT_GAP = 0.16

# The placer aims for MIN_TEXT_GAP + this, never for MIN_TEXT_GAP itself. Aiming
# exactly at a threshold lands on the wrong side of it about half the time once
# floating point is involved: the first version placed three labels at a
# computed 0.16 and the gate read all three back as 0.15999 and failed them.
PLACEMENT_MARGIN = 0.03

# ----------------------------------------------------------- draw layers ---
# Manim's renderer flattens the whole scene and sorts it by ``z_index`` with a
# *stable* sort, so a z_index is the only way to state a layering rule that
# holds across group boundaries. Sibling reordering cannot: an edge living
# inside a `chain` VGroup will always draw over a node that sits in a different
# top-level group, however carefully the two groups sort their own children.
# That is exactly the bug that put connectors on top of the code node for 23
# seconds in section 1.
#
# Lower draws earlier, i.e. further back.
Z_BACKDROP = -20   # zone bands, grids, anything content sits on top of
Z_EDGE = -10       # connectors: never in front of what they join
Z_NODE = 0         # shapes, cards, labels — the default
Z_SLATE = 50       # the review identifier, above everything


def _word_metrics(t: Text, source: str) -> tuple[float, float]:
    """
    (smallest gap between words, median gap between letters) — in scene units.

    Counting glyphs to find the word boundaries is the obvious approach and it is
    wrong: Pango ligates some pairs, so "verification" renders as eleven glyphs
    for twelve characters and every boundary after it is off by one. That made
    the check measure the gap between two letters and report the phrase as
    merged when it was fine.

    So don't rely on the mapping. There are exactly as many word gaps as there
    are spaces, and a word gap is normally wider than a letter gap — so take the
    N widest gaps as the word gaps. The estimate can only be too generous, which
    makes the check conservative: it under-reports rather than inventing faults.
    """
    import numpy as _np
    glyphs = [g for g in t.submobjects if len(g.get_all_points())]
    n_spaces = source.count(" ")
    if len(glyphs) < 2 or n_spaces == 0:
        return (99.0, 0.0)
    gaps = sorted(
        (glyphs[i + 1].get_left()[0] - glyphs[i].get_right()[0]
         for i in range(len(glyphs) - 1)), reverse=True)
    n = min(n_spaces, len(gaps))
    return (float(gaps[n - 1]), float(_np.median(gaps[n:])) if len(gaps) > n else 0.0)


def _stamp(t: Text, source: str | None = None) -> Text:
    """
    Remember how big this text was built, and how big its geometry was then.

    Manim computes ``Text.font_size`` from the mobject's height, which a 3D
    scene's upright rotation drives to zero. The pair recorded here lets QA
    recover the rendered size from the point cloud instead, which rotation
    cannot disturb and scaling still moves.
    """
    import numpy as _np
    pts = t.get_all_points()
    t.qa_pt0 = float(t.font_size)
    t.qa_diag0 = (float(_np.linalg.norm(pts.max(axis=0) - pts.min(axis=0)))
                  if len(pts) else 0.0)
    t.qa_word_gap0, t.qa_letter_gap0 = _word_metrics(t, source if source is not None else "")
    return t


def title_text(text: str) -> Text:
    return _stamp(Text(text, color=WHITE, font_size=TYPE["title"], weight=BOLD), text)


def caption_text(text: str, color: str = WHITE) -> Text:
    return _stamp(Text(text, color=color, font_size=TYPE["caption"], weight=MEDIUM), text)


def label_text(text: str, color: str = WHITE, size: str = "label") -> Text:
    return _stamp(Text(text, color=color, font_size=TYPE[size]), text)


def mono_text(text: str, color: str = WHITE, size: str = "field") -> Text:
    return _stamp(Text(text, font=MONO, color=color, font_size=TYPE[size]), text)


# ----------------------------------------------------------------- shapes ---
def _base_shape(kind: str, color: str, size: float) -> VMobject:
    shape_name = NODE_KINDS.get(kind, {}).get("shape", "record")
    if shape_name == "hexagon":
        shape = RegularPolygon(n=6, radius=size / 2, color=color)
    elif shape_name == "square":
        shape = Square(side_length=size, color=color)
    elif shape_name == "circle":
        shape = Circle(radius=size / 2, color=color)
    elif shape_name == "diamond":
        shape = Square(side_length=size * 0.8, color=color).rotate(PI / 4)
    elif shape_name == "document":
        shape = RoundedRectangle(corner_radius=0.05, width=size * 0.86, height=size * 1.1, color=color)
    elif shape_name == "packet":
        # a folded packet: rectangle with a clipped corner
        w, h = size * 1.35, size * 0.9
        fold = size * 0.26
        shape = Polygon(
            [-w / 2, h / 2, 0], [w / 2 - fold, h / 2, 0], [w / 2, h / 2 - fold, 0],
            [w / 2, -h / 2, 0], [-w / 2, -h / 2, 0], color=color,
        )
    else:
        shape = RoundedRectangle(corner_radius=0.07, width=size * 1.3, height=size * 0.8, color=color)
    shape.set_fill(PANEL, opacity=0.96)
    shape.set_stroke(color, width=2.6)
    return shape


def node(kind: str, text: str = "", size: float = 1.0, color: str | None = None,
         font_size: int | None = None) -> VGroup:
    """
    An artifact node. Returns VGroup(aura, shape, label) — always that order, so
    highlight helpers can stroke the shape without mangling the label.

    The label is auto-fitted inside the shape; a label that cannot fit at the
    minimum legible size raises, rather than silently overflowing.
    """
    color = color or NODE_KINDS.get(kind, {}).get("color", WHITE)
    shape = _base_shape(kind, color, size)
    aura = shape.copy().set_stroke(color, width=9, opacity=0.12).set_fill(opacity=0)
    group = VGroup(aura, shape)
    group.qa_role = "node"
    group.qa_kind = kind
    if text:
        fs = font_size or TYPE["node"]
        label = _stamp(Text(text, color=WHITE, font_size=fs, weight=MEDIUM), text)
        inner = shape.width * 0.78
        if label.width > inner:
            scale = inner / label.width
            if fs * scale < MIN_FONT_SIZE:
                raise ValueError(
                    f"node({kind!r}, {text!r}) cannot fit its label at >= "
                    f"{MIN_FONT_SIZE}pt inside size={size}. Shorten the label or grow the node."
                )
            label.scale(scale)
        label.move_to(shape)
        label.qa_role = "label"
        group.qa_label = label
        group.add(label)
    return group


def highlight(n: Mobject, color: str = GOLD):
    """
    Animations that light a mobject without touching any text inside it.

    Nodes made by `node()` are VGroup(aura, shape, label) and get the aura
    treatment; anything else — a plain rectangle, a packet outline — just gets a
    heavier stroke. Assuming the node shape and indexing blindly turned every
    highlight on a plain shape into a render-time crash.
    """
    if getattr(n, "qa_role", None) == "node" and len(n.submobjects) >= 2:
        return [
            n[0].animate.set_stroke(color, width=13, opacity=0.6),
            n[1].animate.set_stroke(color, width=4),
        ]
    # Never stroke text. `set_stroke` on a group reaches the glyphs too, and a
    # 5-wide stroke on a letterform closes up its counters — the text goes bold,
    # muddy and harder to read, which is the opposite of highlighting it.
    targets = [s for s in n.get_family()
               if not _is_text_like(s) and len(getattr(s, "points", []))]
    if not targets:
        return [n.animate.set_color(color)]
    return [s.animate.set_stroke(color, width=5) for s in targets]


def _is_text_like(mob: Mobject) -> bool:
    if getattr(mob, "text", None) is not None:
        return True
    parent_text = getattr(mob, "qa_role", None) == "label"
    return parent_text or type(mob).__name__.startswith("VMobjectFromSVGPath")


def glow_arrow(start, end, color: str = CYAN, width: float = 3.4, buff: float = 0.16) -> VGroup:
    aura = Arrow(start, end, color=color, stroke_width=width * 2.6, buff=buff).set_opacity(0.16)
    core = Arrow(start, end, color=color, stroke_width=width, buff=buff)
    group = VGroup(aura, core)
    # Tag only the stroke that actually has points. The wrapping VGroup has none,
    # and asking it for an endpoint raises.
    core.qa_role = "edge"
    group.qa_layer = "edge"      # the stage sends these to the back on show
    # Belt and braces: the back-seating below is a scene-order fix, this is a
    # renderer-order fix, and only the second one survives being re-parented
    # into somebody else's VGroup.
    group.set_z_index(Z_EDGE, family=True)
    return group


def connect(a: Mobject, b: Mobject, color: str = CYAN, width: float = 3.4) -> VGroup:
    """
    Arrow between two mobjects, anchored on the line between their centres so the
    head always lands on the boundary it is pointing at — never inside the label.
    """
    start = a.get_center()
    end = b.get_center()
    direction = end - start
    norm = np.linalg.norm(direction)
    if norm < 1e-6:
        raise ValueError("connect() needs two mobjects at different positions")
    unit = direction / norm
    return glow_arrow(
        a.get_boundary_point(unit) + unit * 0.06,
        b.get_boundary_point(-unit) - unit * 0.06,
        color=color, width=width, buff=0.0,
    )


def text_rows(*mobs: Mobject, buff: float | None = None, align=LEFT) -> VGroup:
    """
    Stack label rows with a gap the crowding check will accept.

    Writing `arrange(DOWN, buff=MIN_TEXT_GAP)` looks exactly right and fails:
    the rows land at precisely the threshold, and the gate reads the same
    distance back as 0.15999. Rows built through here clear the bar instead of
    balancing on it.
    """
    if buff is None:
        buff = MIN_TEXT_GAP + PLACEMENT_MARGIN
    return VGroup(*mobs).arrange(DOWN, buff=buff, aligned_edge=align)


def cursor_for(mob: Mobject, color: str = GOLD, width: float = 4.0,
               pad: float = 0.22) -> Circle:
    """
    A ring that actually goes round the thing it marks.

    A fixed-radius circle marks a one-word node and cuts straight through a
    longer one — "traversal" spent fifteen seconds with a gold line through the
    middle of it. Size the ring from the node, not from a constant.
    """
    r = max(mob.width, mob.height) / 2 + pad
    ring = Circle(radius=r, color=color, stroke_width=width)
    ring.move_to(mob.get_center())
    return ring


def allow_overlap(mob: Mobject, *others: Mobject, reason: str = ""):
    """
    Declare that `mob` is *meant* to sit over `others`.

    A stamp landing across a quote is a deliberate composition, not a layout bug.
    Declaring it keeps the overlap checker strict everywhere else instead of
    forcing the tolerance up globally, which is how these checks stop working.
    """
    def texts(m):
        return [str(getattr(s, "text", "")) for s in m.get_family()
                if getattr(s, "text", None)]

    mine = texts(mob)
    theirs = [t for o in others for t in texts(o)]
    for sub in mob.get_family():
        if getattr(sub, "text", None):
            sub.qa_allow_overlap = theirs
            sub.qa_allow_reason = reason
    for o in others:
        for sub in o.get_family():
            if getattr(sub, "text", None):
                sub.qa_allow_overlap = mine
                sub.qa_allow_reason = reason
    return mob


def strip_labels(*nodes: Mobject) -> None:
    """
    Remove the text from nodes, immediately and permanently.

    Deliberately not an animation. Two reasons, both learned the hard way:

    * `FadeOut` on a label is a no-op that then *restores* the opacity, because
      the label is a submobject the scene does not hold directly.
    * Returning `.animate` chains puts two animations on one family; the group's
      own `.animate.scale(...)` captured its target before the opacity changed,
      so it faithfully restored every label it was supposed to remove.

    Call this immediately before the play that moves or scales the node, so the
    text goes as the shape transforms. A label evaporating off a shape that then
    sits still reads as a rendering glitch — and the QA gate will say so.
    """
    for node in nodes:
        for sub in node.get_family():
            if getattr(sub, "text", None):
                sub.set_opacity(0)


def restroke(mob: Mobject, color: str, width: float = 3.0):
    """
    Change a mobject's stroke without touching any text inside it.

    `mob.animate.set_stroke(...)` reaches every submobject, so calling it on a
    node group strokes the label as well and thickens the letterforms until they
    are hard to read. Use this anywhere a group might contain text.
    """
    targets = [s for s in mob.get_family()
               if not _is_text_like(s) and len(getattr(s, "points", []))]
    if not targets:
        return [mob.animate.set_color(color)]
    return [s.animate.set_stroke(color, width=width) for s in targets]
