"""
3D scenes with declarative camera moves.

The artifact graph is the one idea in this video that genuinely wants depth: it
is a layered structure — requirements above, code below, evidence behind — and a
pan through it says "this is one connected object" faster than any flat diagram.

Camera moves are declared against narration anchors like everything else, so a
pull-back lands on the line that motivates it.

Two Manim traps this module exists to prevent, both of which cost video 1 a pass:
  - fixed-in-frame mobjects leak into later scenes and reappear during 3D moves;
  - text in a 3D scene tilts with the camera and becomes unreadable unless it is
    explicitly pinned to the frame.
"""
from __future__ import annotations

from dataclasses import dataclass

from manim import *

from . import stage, style
from .beats import BeatScene


@dataclass
class CameraMove:
    """A camera state to move to, cued to narration."""

    anchor: str
    phi: float = 65        # degrees from +z
    theta: float = -45     # degrees around z
    zoom: float = 1.0
    run_time: float = 2.0
    note: str = ""


class Beat3DScene(ThreeDScene, BeatScene):
    """
    A 3D section.

    Text placed with `self.pin()` stays flat and upright regardless of camera
    angle, and is tracked so it can be removed cleanly — the leak that made
    fixed-frame labels bleed into later scenes in video 1.
    """

    initial_phi: float = 62
    initial_theta: float = -48

    def setup(self):
        super().setup()
        self._pinned: list[Mobject] = []

    def construct(self):
        self.set_camera_orientation(phi=self.initial_phi * DEGREES,
                                    theta=self.initial_theta * DEGREES)
        super().construct()

    def pin(self, mob: Mobject) -> Mobject:
        """
        Pin a mobject to the camera frame (flat, upright, unaffected by camera).

        Note: add_fixed_in_frame_mobjects adds at full opacity immediately, so
        anything that should appear later must be animated in with
        `.animate.set_opacity(1)` from 0 — a plain FadeIn would fade 0 -> 0.
        """
        self.add_fixed_in_frame_mobjects(mob)
        self._pinned.append(mob)
        return mob

    def unpin_all(self, run_time: float = 0.35):
        """Clear every pinned mobject. Call before any section transition."""
        live = [m for m in self._pinned if m in self.mobjects]
        if live:
            self.play(*[FadeOut(m) for m in live], run_time=run_time)
        for m in self._pinned:
            self.remove_fixed_in_frame_mobjects(m)
        self._pinned.clear()

    def move(self, mv: CameraMove, window: float):
        rt = min(mv.run_time, max(window - 0.1, 0.3))
        self.move_camera(phi=mv.phi * DEGREES, theta=mv.theta * DEGREES,
                         zoom=mv.zoom, run_time=rt)


def layered_graph(layers: dict[str, list[tuple[str, str]]], spacing: float = 1.9,
                  radius: float = 3.1) -> tuple[VGroup, dict[str, VGroup]]:
    """
    Build the artifact graph as stacked planes in z.

    `layers` maps a layer name to a list of (kind, label). Requirements sit on
    top, evidence at the bottom, so a pull-back reads as "everything traces
    downward to evidence" without a word of narration.
    """
    nodes: dict[str, VGroup] = {}
    group = VGroup()
    for i, (layer_name, specs) in enumerate(layers.items()):
        z = (len(layers) - 1) / 2 * spacing - i * spacing
        n = len(specs)
        for j, (kind, label) in enumerate(specs):
            angle = TAU * j / max(n, 1)
            pos = np.array([radius * np.cos(angle), radius * np.sin(angle), z])
            node = style.node(kind, label, size=0.95)
            node.move_to(pos)
            node.rotate(PI / 2, axis=RIGHT)   # stand the plate up to face the camera
            nodes[label] = node
            group.add(node)
        plane = Rectangle(width=radius * 2.6, height=radius * 2.6,
                          color=style.GRID, stroke_width=1.2, stroke_opacity=0.5)
        plane.rotate(PI / 2, axis=RIGHT).shift(OUT * 0 + np.array([0, 0, z]))
        plane.set_fill(style.PANEL, opacity=0.10)
        group.add(plane)
    return group, nodes


def edge3d(a, b, color: str = style.CYAN, width: float = 3.0) -> VMobject:
    """
    A connector between two nodes in a 3D graph, on the connector layer.

    `Line3D` reports `shade_in_3d = False`, so ThreeDCamera's depth sort gives it
    the same "draw last" key as everything else and falls back to scene order —
    which means a 3D connector created during a beat is drawn *in front of* the
    nodes it joins and then appears to drop behind them the moment anything else
    arrives. The 2D connectors have carried the edge layer for two passes; the 3D
    ones never did, and that is the blink in sections 4 and 6.

    Accepts mobjects or raw points, so a scene can join a node to a coordinate.
    """
    pa = a if isinstance(a, np.ndarray) else a.get_center()
    pb = b if isinstance(b, np.ndarray) else b.get_center()
    line = Line3D(pa, pb, color=color, thickness=width * 0.006)
    line.qa_role = "edge"
    line.qa_layer = "edge"
    line.set_z_index(style.Z_EDGE, family=True)
    return line
