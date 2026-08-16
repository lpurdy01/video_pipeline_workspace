from __future__ import annotations

import math

import numpy as np
from manim import *

from orbital_tech_tree_data import BRIDGES, EDGES, FRONTIER, NODES, REVEAL_STATES, STATE_CAMERA, WEDGES
from visual_style import BG, GRID, WHITE


Y_SCALE = 0.58
INNER_R = 0.62
OUTER_R = 4.25


LABEL_OFFSETS = {
    "fourier": np.array([-1.08, 0.22, 0]),
    "frequency": np.array([-0.08, 0.38, 0]),
    "signal_processing": np.array([0.10, -0.56, 0]),
    "wireless": np.array([0.20, 0.42, 0]),
    "compressed_audio": np.array([-0.42, 0.32, 0]),
    "spectral_imaging": np.array([-0.48, -0.10, 0]),
    "dct": np.array([-0.78, 0.38, 0]),
    "jpeg": np.array([0.12, 0.36, 0]),
    "video_codecs": np.array([0.46, 0.54, 0]),
    "laplace": np.array([0.48, -0.28, 0]),
    "transfer": np.array([0.45, 0.22, 0]),
    "stability": np.array([0.70, 0.48, 0]),
    "feedback": np.array([0.48, 0.36, 0]),
    "motors": np.array([0.74, 0.02, 0]),
    "flight": np.array([-0.35, -0.35, 0]),
    "state_space": np.array([-0.12, 0.46, 0]),
    "neural_ssm": np.array([0.88, 0.46, 0]),
    "neural_networks": np.array([-0.52, -0.26, 0]),
    "embeddings": np.array([0.04, 0.42, 0]),
    "transformers": np.array([-0.48, 0.46, 0]),
    "llms": np.array([1.25, -0.52, 0]),
    "contrastive": np.array([0.26, -0.40, 0]),
    "multimodal": np.array([0.22, -0.48, 0]),
    "software_form": np.array([-0.50, 0.10, 0]),
    "code_agents": np.array([-0.15, -0.70, 0]),
    "research_agents": np.array([-0.34, -0.46, 0]),
    "vv": np.array([-1.20, -0.82, 0]),
    "reliable": np.array([-0.42, -0.42, 0]),
    "self_compute": np.array([-1.05, 0.98, 0]),
    "experiment_loops": np.array([-0.60, 0.75, 0]),
    "world_models": np.array([0.38, -0.36, 0]),
    "closed_loop_rd": np.array([-0.40, -0.38, 0]),
    "orgs": np.array([-0.52, 0.06, 0]),
}


def polar_point(angle_deg: float, radius: float, z: float = 0.0) -> np.ndarray:
    angle = math.radians(angle_deg)
    return np.array([math.cos(angle) * radius, math.sin(angle) * radius * Y_SCALE, z])


def bridge_key(source: str, target: str) -> str:
    return f"{source}->{target}"


class OrbitalTechTreeMap:
    def __init__(self, scene: Scene, seed: int = 12):
        self.scene = scene
        self.seed = seed
        self.wedges: dict[str, VGroup] = {}
        self.nodes: dict[str, VGroup] = {}
        self.labels: dict[str, Text] = {}
        self.edges: dict[str, VGroup] = {}
        self.bridges: dict[str, VGroup] = {}
        self.frontier_nodes: dict[str, VGroup] = {}
        self.rings = VGroup()
        self.fog_particles = VGroup()
        self.haze = VGroup()
        self.masks = VGroup()
        self.root = VGroup()
        self.group = VGroup()
        self._build()

    def node_pos(self, key: str, lift: float = 0.0) -> np.ndarray:
        spec = NODES[key]
        return polar_point(spec.angle_deg, spec.radius, lift)

    def _annular_wedge(self, start_deg: float, end_deg: float, color: str) -> VGroup:
        sector = AnnularSector(
            inner_radius=INNER_R,
            outer_radius=OUTER_R,
            angle=math.radians(end_deg - start_deg),
            start_angle=math.radians(start_deg),
            color=color,
            stroke_width=1.4,
            fill_opacity=0.18,
        )
        sector.stretch(Y_SCALE, dim=1)
        sector.set_stroke(color, opacity=0.42)
        rim = Arc(
            radius=OUTER_R,
            start_angle=math.radians(start_deg),
            angle=math.radians(end_deg - start_deg),
            color=color,
            stroke_width=3,
        )
        rim.stretch(Y_SCALE, dim=1)
        rim_glow = rim.copy().set_stroke(color, width=11, opacity=0.11)
        label_angle = (start_deg + end_deg) / 2
        label = Text(WEDGES_BY_COLOR_LABEL.get(color, ""), color=color, font_size=15)
        return VGroup(sector, rim_glow, rim, label)

    def _build_wedges(self) -> VGroup:
        group = VGroup()
        for key, spec in WEDGES.items():
            sector = AnnularSector(
                inner_radius=INNER_R,
                outer_radius=OUTER_R,
                angle=math.radians(spec.end_deg - spec.start_deg),
                start_angle=math.radians(spec.start_deg),
                color=spec.color,
                stroke_width=1.2,
                fill_opacity=0.16,
            )
            sector.stretch(Y_SCALE, dim=1)
            sector.set_stroke(spec.color, opacity=0.38)
            sector.set_z_index(0)

            outer_arc = Arc(
                radius=OUTER_R,
                start_angle=math.radians(spec.start_deg),
                angle=math.radians(spec.end_deg - spec.start_deg),
                color=spec.color,
                stroke_width=2.6,
            )
            outer_arc.stretch(Y_SCALE, dim=1)
            outer_glow = outer_arc.copy().set_stroke(spec.color, width=10, opacity=0.12)
            outer_glow.set_z_index(1)
            outer_arc.set_z_index(2)
            wedge = VGroup(sector, outer_glow, outer_arc)
            self.wedges[key] = wedge
            group.add(wedge)
        return group

    def _build_rings(self) -> VGroup:
        rings = VGroup()
        for radius, opacity in [(1.25, 0.15), (2.05, 0.14), (2.85, 0.11), (3.65, 0.10), (4.85, 0.12)]:
            ring = Circle(radius=radius, color=GRID, stroke_width=1.0)
            ring.stretch(Y_SCALE, dim=1)
            ring.set_stroke(GRID, opacity=opacity)
            ring.set_z_index(-2)
            rings.add(ring)
        shell = Circle(radius=5.05, color=FRONTIER, stroke_width=1.2)
        shell.stretch(Y_SCALE, dim=1)
        shell.set_stroke(FRONTIER, opacity=0.22)
        shell_glow = shell.copy().set_stroke(WHITE, width=18, opacity=0.035)
        shell.set_z_index(-1)
        shell_glow.set_z_index(-2)
        rings.add(shell_glow, shell)
        self.rings = rings
        return rings

    def _build_node(self, key: str) -> VGroup:
        spec = NODES[key]
        pos = self.node_pos(key)
        radius = 0.060 if spec.level != "frontier" else 0.050
        glow = Dot(pos, radius=radius * 4.0, color=spec.color).set_opacity(0.18)
        dot = Dot(pos, radius=radius, color=spec.color)
        ring = Circle(radius=radius * 2.2, color=spec.color, stroke_width=1.2).move_to(pos)
        ring.set_stroke(spec.color, opacity=0.72)
        glow.set_z_index(5)
        ring.set_z_index(6)
        dot.set_z_index(7)
        label_color = WHITE if spec.level == "frontier" else spec.color
        font_size = 15 if spec.level == "frontier" else 13
        label = Text(spec.label, color=label_color, font_size=font_size, line_spacing=0.76)
        label.set_fill(label_color, opacity=0.98).set_stroke(BG, width=1.6, opacity=0.88, background=True)
        label.move_to(pos + LABEL_OFFSETS.get(key, self._label_offset(spec.angle_deg, spec.radius)))
        shield = BackgroundRectangle(label, color=BG, fill_opacity=0.0, buff=0.055)
        shield.set_stroke(BG, width=0, opacity=0.0)
        shield.set_z_index(13)
        label.set_z_index(15)
        node = VGroup(glow, ring, dot)
        full = VGroup(glow, ring, dot, shield, label)
        self.nodes[key] = full
        self.labels[key] = label
        if spec.level == "frontier":
            self.frontier_nodes[key] = full
        return full

    def _label_offset(self, angle_deg: float, radius: float) -> np.ndarray:
        angle = math.radians(angle_deg)
        base = np.array([math.cos(angle) * 0.52, math.sin(angle) * 0.36, 0])
        if radius < 1.6:
            base += UP * 0.34
        return base

    def _flat_edge(self, source: str, target: str, color: str) -> VGroup:
        start = self.node_pos(source)
        end = self.node_pos(target)
        control_radius = max(NODES[source].radius, NODES[target].radius) * 0.96
        angle_mid = (NODES[source].angle_deg + NODES[target].angle_deg) / 2
        control = polar_point(angle_mid, control_radius)
        path = CubicBezier(start, control, control, end)
        path.set_stroke(color, width=1.65, opacity=0.56)
        glow = path.copy().set_stroke(color, width=7, opacity=0.08)
        glow.set_z_index(2)
        path.set_z_index(3)
        return VGroup(glow, path)

    def _bridge(self, source: str, target: str, color: str) -> VGroup:
        start = self.node_pos(source)
        end = self.node_pos(target)
        midpoint = (start + end) / 2
        lift = UP * (0.78 + 0.12 * np.linalg.norm(end - start))
        ctrl1 = start + (midpoint - start) * 0.65 + lift
        ctrl2 = end + (midpoint - end) * 0.65 + lift
        path = CubicBezier(start, ctrl1, ctrl2, end)
        path.set_stroke(color, width=2.4, opacity=0.88)
        glow = path.copy().set_stroke(color, width=10, opacity=0.16)
        highlight = path.copy().set_stroke(WHITE, width=0.7, opacity=0.24)
        glow.set_z_index(3)
        path.set_z_index(4)
        highlight.set_z_index(4)
        return VGroup(glow, path, highlight)

    def _build_edges(self) -> VGroup:
        group = VGroup()
        for edge in EDGES:
            edge_group = self._flat_edge(edge.source, edge.target, edge.color)
            self.edges[bridge_key(edge.source, edge.target)] = edge_group
            group.add(edge_group)
        for edge in BRIDGES:
            bridge = self._bridge(edge.source, edge.target, edge.color)
            self.bridges[bridge_key(edge.source, edge.target)] = bridge
            group.add(bridge)
        return group

    def _build_particles(self) -> VGroup:
        rng = np.random.default_rng(self.seed)
        particles = VGroup()
        palette = [WHITE, "#BFD7FF", FRONTIER, "#87A7FF", "#D7F7FF"]
        for _ in range(180):
            angle = rng.uniform(0, TAU)
            radius = rng.uniform(3.65, 5.75)
            point = np.array([math.cos(angle) * radius, math.sin(angle) * radius * Y_SCALE, 0])
            color = palette[int(rng.integers(0, len(palette)))]
            dot = Dot(point, radius=rng.uniform(0.010, 0.026), color=color)
            dot.set_opacity(rng.uniform(0.10, 0.34))
            dot.set_z_index(12)
            particles.add(dot)
        self.fog_particles = particles
        return particles

    def _build_masks(self) -> VGroup:
        masks = VGroup()
        # Broad, dark camera-space curtains used as fake crop/fog boundaries.
        left = Rectangle(width=5.1, height=8.0, color=BG, stroke_width=0).set_fill(BG, opacity=0.48)
        right = left.copy()
        bottom = Rectangle(width=14.5, height=2.2, color=BG, stroke_width=0).set_fill(BG, opacity=0.42)
        left.move_to(LEFT * 5.1)
        right.move_to(RIGHT * 5.1)
        bottom.move_to(DOWN * 3.25)
        haze1 = Circle(radius=5.8, color=WHITE, stroke_width=0).stretch(Y_SCALE, dim=1)
        haze1.set_fill(WHITE, opacity=0.035)
        haze2 = Circle(radius=4.6, color=BG, stroke_width=0).stretch(Y_SCALE, dim=1)
        haze2.set_fill(BG, opacity=0.10)
        masks.add(left, right, bottom)
        masks.set_z_index(10)
        self.haze = VGroup(haze1, haze2)
        self.haze.set_z_index(11)
        self.masks = masks
        return VGroup(masks, self.haze)

    def _build(self) -> None:
        self.root = VGroup(
            Circle(radius=0.16, color=WHITE, stroke_width=1.2).set_stroke(WHITE, opacity=0.55),
            Dot(ORIGIN, radius=0.025, color=WHITE).set_opacity(0.8),
        )
        wedge_group = self._build_wedges()
        ring_group = self._build_rings()
        edge_group = self._build_edges()
        node_group = VGroup(*[self._build_node(key) for key in NODES])
        particle_group = self._build_particles()
        mask_group = self._build_masks()
        self.group = VGroup(ring_group, wedge_group, edge_group, node_group, self.root, particle_group, mask_group)
        self.apply_state("opening_glimpse", animate=False)

    def add_to_scene(self) -> None:
        self.scene.add(self.rings)
        self.scene.add(*self.wedges.values())
        self.scene.add(*self.edges.values())
        self.scene.add(*self.bridges.values())
        self.scene.add(*self.nodes.values())
        self.scene.add(self.root)
        self.scene.add(self.fog_particles)
        self.scene.add(self.masks)
        self.scene.add(self.haze)

    def state_camera(self, state: str) -> dict:
        return STATE_CAMERA[state]

    def apply_state(self, state: str, animate: bool = True, run_time: float = 0.55) -> AnimationGroup | None:
        spec = REVEAL_STATES[state]
        animations = []

        def set_or_animate(mobject: Mobject, opacity: float):
            if animate:
                animations.append(mobject.animate.set_opacity(opacity))
            else:
                mobject.set_opacity(opacity)

        for key, wedge in self.wedges.items():
            opacity = spec["wedges"].get(key, 0.02)
            set_or_animate(wedge, opacity)

        visible_nodes = spec["nodes"]
        visible_labels = spec["labels"]
        for key, node in self.nodes.items():
            target_opacity = spec["frontier"] if NODES[key].level == "frontier" else (0.96 if key in visible_nodes else 0.08)
            label_opacity = 0.98 if key in visible_labels else 0.0
            set_or_animate(VGroup(node[0], node[1], node[2]), target_opacity)
            set_or_animate(node[3], 0.0)
            set_or_animate(node[4], label_opacity)

        allowed_edges = set()
        for edge in EDGES:
            if edge.source in visible_nodes and edge.target in visible_nodes:
                allowed_edges.add(bridge_key(edge.source, edge.target))
        for key, edge in self.edges.items():
            set_or_animate(edge, 0.74 if key in allowed_edges else 0.08)

        for key, bridge in self.bridges.items():
            set_or_animate(bridge, 0.96 if key in spec["bridges"] else 0.05)

        fog = spec["fog"]
        set_or_animate(self.fog_particles, fog)
        set_or_animate(self.haze, fog)
        mask_opacity = 0.06 if state in {"opening_glimpse", "convergence_pullback"} else 0.0
        set_or_animate(self.masks, mask_opacity)
        ring_opacity = {
            "opening_glimpse": 0.08,
            "classical_foundation": 0.36,
            "modern_region": 0.26,
            "convergence_pullback": 0.34,
            "final_reveal": 0.62,
        }[state]
        set_or_animate(self.rings, ring_opacity)
        set_or_animate(self.root, 0.70 if state != "opening_glimpse" else 0.38)

        if not animate:
            return None
        return AnimationGroup(*animations, lag_ratio=0.0, run_time=run_time)

    def fog_drift_animation(self, run_time: float = 6.0) -> AnimationGroup:
        rng = np.random.default_rng(self.seed + 99)
        animations = []
        for i, dot in enumerate(self.fog_particles):
            angle = (i / max(1, len(self.fog_particles))) * TAU
            shift = np.array([
                math.cos(angle + rng.uniform(-0.5, 0.5)) * rng.uniform(0.04, 0.18),
                math.sin(angle + rng.uniform(-0.5, 0.5)) * rng.uniform(0.02, 0.10),
                0,
            ])
            animations.append(dot.animate.shift(shift))
        return AnimationGroup(*animations, lag_ratio=0.0, run_time=run_time)


# Left here only to make accidental calls to the old scratch helper fail loudly.
WEDGES_BY_COLOR_LABEL: dict[str, str] = {}
