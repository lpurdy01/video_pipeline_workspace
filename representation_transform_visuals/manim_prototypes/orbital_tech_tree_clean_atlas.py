from __future__ import annotations

import math

import numpy as np
from manim import *

from orbital_tech_tree_data import BRIDGES, EDGES, FRONTIER, NODES, WEDGES
from visual_style import BG, BLUE, CYAN, GOLD, GREEN, GRID, VIOLET, WHITE


Y_SCALE = 0.56
R_SCALE = 0.92


def bridge_key(source: str, target: str) -> str:
    return f"{source}->{target}"


def point_for(key: str) -> np.ndarray:
    spec = NODES[key]
    angle = math.radians(spec.angle_deg)
    radius = spec.radius * R_SCALE
    return np.array([math.cos(angle) * radius, math.sin(angle) * radius * Y_SCALE, 0.0])


def radial_point(angle_deg: float, radius: float) -> np.ndarray:
    angle = math.radians(angle_deg)
    r = radius * R_SCALE
    return np.array([math.cos(angle) * r, math.sin(angle) * r * Y_SCALE, 0.0])


def glow_path(path: Mobject, color: str, width: float = 3.0, opacity: float = 1.0) -> VGroup:
    halo = path.copy().set_stroke(color, width=width * 4.2, opacity=0.18 * opacity)
    core = path.copy().set_stroke(color, width=width, opacity=opacity)
    return VGroup(halo, core)


def glow_text(text: str, color: str, font_size: int = 22) -> VGroup:
    core = Text(text, color=color, font_size=font_size, line_spacing=0.78)
    mask = BackgroundRectangle(core, color=BG, fill_opacity=0.88, buff=0.065)
    mask.set_stroke(BG, width=0, opacity=0)
    shadow = core.copy().set_stroke(BG, width=4.0, opacity=0.96, background=True)
    shine = core.copy().set_stroke(color, width=0.9, opacity=0.42, background=True)
    label = VGroup(mask, shadow, shine, core)
    for index, part in enumerate(label):
        part.set_z_index(28 + index)
    label.set_z_index(32)
    return label


class CleanOrbitalAtlas:
    """A cleaner orbital skill-tree map.

    This version avoids fog, hidden low-opacity text, and labels inside the
    node network. It uses revealed geometry plus callout labels.
    """

    def __init__(self):
        self.base = VGroup()
        self.nodes: dict[str, VGroup] = {}
        self.edges: dict[str, VGroup] = {}
        self.bridges: dict[str, VGroup] = {}
        self.labels: dict[str, VGroup] = {}
        self.callouts: dict[str, VGroup] = {}
        self.frontier_particles = VGroup()
        self._build()

    def _build(self) -> None:
        self.base = VGroup(self._rings(), self._wedge_lanes(), self._frontier_shell(), self._origin())
        self.nodes = {key: self._node(key) for key in NODES}
        self.edges = {bridge_key(edge.source, edge.target): self._edge(edge.source, edge.target, edge.color) for edge in EDGES}
        self.bridges = {bridge_key(edge.source, edge.target): self._bridge(edge.source, edge.target, edge.color) for edge in BRIDGES}
        self.labels = {key: self._label(key) for key in NODES}
        self.callouts = {key: self._callout(key) for key in self.labels}

    def _rings(self) -> VGroup:
        rings = VGroup()
        for radius, opacity, width in [
            (1.0, 0.13, 1.0),
            (1.75, 0.16, 1.0),
            (2.55, 0.18, 1.1),
            (3.35, 0.15, 1.1),
            (4.25, 0.22, 1.4),
        ]:
            ring = Circle(radius=radius * R_SCALE, color=GRID, stroke_width=width)
            ring.stretch(Y_SCALE, dim=1)
            ring.set_stroke(GRID, opacity=opacity)
            rings.add(ring)
        return rings

    def _wedge_lanes(self) -> VGroup:
        lanes = VGroup()
        for spec in WEDGES.values():
            for radius, opacity in [(1.55, 0.16), (2.55, 0.20), (3.55, 0.20)]:
                arc = Arc(
                    radius=radius * R_SCALE,
                    start_angle=math.radians(spec.start_deg),
                    angle=math.radians(spec.end_deg - spec.start_deg),
                    color=spec.color,
                    stroke_width=2.1,
                )
                arc.stretch(Y_SCALE, dim=1)
                lanes.add(arc.set_stroke(spec.color, opacity=opacity))
            start = Line(radial_point(spec.start_deg, 0.82), radial_point(spec.start_deg, 4.15), color=spec.color)
            end = Line(radial_point(spec.end_deg, 0.82), radial_point(spec.end_deg, 4.15), color=spec.color)
            lanes.add(start.set_stroke(spec.color, width=1.2, opacity=0.18))
            lanes.add(end.set_stroke(spec.color, width=1.2, opacity=0.18))
        return lanes

    def _frontier_shell(self) -> VGroup:
        shell = Circle(radius=4.8 * R_SCALE, color=FRONTIER, stroke_width=2.0)
        shell.stretch(Y_SCALE, dim=1)
        shell_glow = shell.copy().set_stroke(FRONTIER, width=10, opacity=0.10)
        shell.set_stroke(FRONTIER, opacity=0.45)

        rng = np.random.default_rng(42)
        particles = VGroup()
        for i in range(90):
            angle = i / 90 * TAU + rng.uniform(-0.018, 0.018)
            radius = rng.uniform(4.45, 4.95)
            point = np.array([math.cos(angle) * radius * R_SCALE, math.sin(angle) * radius * R_SCALE * Y_SCALE, 0.0])
            color = [FRONTIER, CYAN, VIOLET, GOLD][i % 4]
            dot = Dot(point, radius=rng.uniform(0.010, 0.024), color=color).set_opacity(rng.uniform(0.28, 0.72))
            particles.add(dot)
        self.frontier_particles = particles
        return VGroup(shell_glow, shell, particles)

    def _origin(self) -> VGroup:
        pulse = Circle(radius=0.20, color=WHITE, stroke_width=1.8).set_stroke(WHITE, opacity=0.56)
        dot = Dot(ORIGIN, radius=0.030, color=WHITE).set_opacity(0.88)
        spokes = VGroup()
        for spec in WEDGES.values():
            middle = (spec.start_deg + spec.end_deg) / 2
            spokes.add(Line(ORIGIN, radial_point(middle, 0.76), color=spec.color).set_stroke(spec.color, width=2.0, opacity=0.34))
        return VGroup(spokes, pulse, dot)

    def _node(self, key: str) -> VGroup:
        spec = NODES[key]
        point = point_for(key)
        radius = 0.066 if spec.level != "frontier" else 0.052
        halo = Dot(point, radius=radius * 4.0, color=spec.color).set_opacity(0.22)
        ring = Circle(radius=radius * 2.2, color=spec.color, stroke_width=1.4).move_to(point)
        ring.set_stroke(spec.color, opacity=0.78)
        core = Dot(point, radius=radius, color=spec.color).set_opacity(0.98)
        return VGroup(halo, ring, core)

    def _edge(self, source: str, target: str, color: str) -> VGroup:
        start = point_for(source)
        end = point_for(target)
        source_spec = NODES[source]
        target_spec = NODES[target]
        mid_angle = (source_spec.angle_deg + target_spec.angle_deg) / 2
        mid_radius = max(source_spec.radius, target_spec.radius) * 0.92
        control = radial_point(mid_angle, mid_radius)
        path = CubicBezier(start, control, control, end)
        return glow_path(path, color, width=2.2, opacity=0.88)

    def _bridge(self, source: str, target: str, color: str) -> VGroup:
        start = point_for(source)
        end = point_for(target)
        midpoint = (start + end) / 2
        lift = UP * (0.65 + 0.10 * np.linalg.norm(end - start))
        path = CubicBezier(start, start + (midpoint - start) * 0.55 + lift, end + (midpoint - end) * 0.55 + lift, end)
        group = glow_path(path, color, width=3.6, opacity=0.96)
        highlight = path.copy().set_stroke(WHITE, width=0.9, opacity=0.30)
        group.add(highlight)
        return group

    def _label_position(self, key: str) -> np.ndarray:
        positions = {
            "fourier": np.array([-4.30, 1.52, 0]),
            "signal_processing": np.array([-4.35, 0.70, 0]),
            "dct": np.array([-2.66, 2.42, 0]),
            "video_codecs": np.array([-1.18, 2.52, 0]),
            "laplace": np.array([1.74, 2.38, 0]),
            "stability": np.array([3.28, 1.72, 0]),
            "state_space": np.array([4.02, 0.96, 0]),
            "neural_ssm": np.array([4.10, -0.26, 0]),
            "embeddings": np.array([3.42, -0.98, 0]),
            "transformers": np.array([4.06, -1.62, 0]),
            "llms": np.array([3.62, -2.30, 0]),
            "code_agents": np.array([-3.36, -1.78, 0]),
            "vv": np.array([-4.28, -2.42, 0]),
            "self_compute": np.array([-2.50, 3.02, 0]),
            "experiment_loops": np.array([2.80, 2.88, 0]),
        }
        return positions.get(key, point_for(key) + RIGHT * 0.5)

    def _label(self, key: str) -> VGroup:
        spec = NODES[key]
        color = WHITE if spec.level == "frontier" else spec.color
        label = glow_text(spec.label, color, font_size=20 if spec.level != "frontier" else 18)
        label.move_to(self._label_position(key))
        return label

    def _callout(self, key: str) -> VGroup:
        label = self.labels[key]
        start = label.get_center()
        end = point_for(key)
        line = Line(start, end, color=NODES[key].color, stroke_width=1.2)
        line.set_stroke(NODES[key].color, opacity=0.58)
        line.set_z_index(12)
        return VGroup(line, label)

    def mobjects_for_nodes(self, keys: set[str]) -> list[Mobject]:
        return [self.nodes[key] for key in keys]

    def mobjects_for_edges(self, keys: set[str]) -> list[Mobject]:
        items: list[Mobject] = []
        for key in keys:
            if key in self.edges:
                items.append(self.edges[key])
            elif key in self.bridges:
                items.append(self.bridges[key])
        return items

    def mobjects_for_labels(self, keys: set[str]) -> list[Mobject]:
        return [self.callouts[key] for key in keys if key in self.callouts]


class OrbitalTechTreeCleanAtlasPrototype(MovingCameraScene):
    """Second attempt: no fog blanket, no labels inside the node network."""

    def setup(self):
        super().setup()
        self.camera.background_color = BG

    def construct(self):
        atlas = CleanOrbitalAtlas()
        self.add(atlas.base)

        shown_nodes: set[str] = set()
        shown_edges: set[str] = set()
        shown_labels: set[str] = set()

        def reveal(nodes: set[str], labels: set[str], run_time: float = 1.2):
            new_nodes = nodes - shown_nodes
            new_edges = {
                bridge_key(edge.source, edge.target)
                for edge in EDGES
                if edge.source in nodes and edge.target in nodes
            } - shown_edges
            new_bridges = {
                bridge_key(edge.source, edge.target)
                for edge in BRIDGES
                if edge.source in nodes and edge.target in nodes
            } - shown_edges
            new_labels = labels - shown_labels
            animations: list[Animation] = []
            animations.extend(Create(mob) for mob in atlas.mobjects_for_edges(new_edges | new_bridges))
            animations.extend(FadeIn(mob, scale=0.72) for mob in atlas.mobjects_for_nodes(new_nodes))
            animations.extend(FadeIn(mob, shift=UP * 0.10) for mob in atlas.mobjects_for_labels(new_labels))
            shown_nodes.update(new_nodes)
            shown_edges.update(new_edges | new_bridges)
            shown_labels.update(new_labels)
            if animations:
                self.play(LaggedStart(*animations, lag_ratio=0.035), run_time=run_time)

        self.camera.frame.set(width=12.2)
        self.camera.frame.move_to(ORIGIN)
        self.play(Rotate(atlas.frontier_particles, angle=10 * DEGREES, about_point=ORIGIN), run_time=1.4)

        classical = {
            "fourier", "frequency", "signal_processing", "wireless", "compressed_audio",
            "spectral_imaging", "dct", "jpeg", "video_codecs", "laplace", "transfer",
            "stability", "feedback", "motors", "flight", "state_space",
        }
        self.play(self.camera.frame.animate.move_to(UP * 0.58 + LEFT * 0.20).set(width=10.9), run_time=1.0)
        reveal(classical, {"fourier", "dct", "signal_processing", "video_codecs", "laplace", "stability"}, run_time=2.0)
        self.play(Rotate(atlas.frontier_particles, angle=9 * DEGREES, about_point=ORIGIN), run_time=1.0)

        modern = {
            "neural_networks", "embeddings", "transformers", "llms", "contrastive",
            "autoencoders", "neural_codecs", "audio_tokens", "multimodal",
            "software_form", "code_agents", "research_agents", "vv", "proof_tools",
            "expert", "blackboard",
        }
        self.play(self.camera.frame.animate.move_to(DOWN * 0.48 + RIGHT * 0.12).set(width=11.0), run_time=1.0)
        reveal(modern, {"embeddings", "transformers", "llms", "code_agents", "vv"}, run_time=2.1)
        self.play(Rotate(atlas.frontier_particles, angle=9 * DEGREES, about_point=ORIGIN), run_time=1.0)

        convergence = classical | modern | {"neural_ssm", "reliable"}
        self.play(self.camera.frame.animate.move_to(RIGHT * 0.18 + DOWN * 0.03).set(width=11.6), run_time=1.0)
        reveal(convergence, {"state_space", "neural_ssm", "llms", "code_agents", "vv"}, run_time=1.8)
        self.play(*[Indicate(atlas.bridges[key], color=WHITE, scale_factor=1.02) for key in atlas.bridges], run_time=1.4)

        final_nodes = set(NODES)
        final_labels = {
            "fourier", "dct", "signal_processing", "video_codecs", "laplace", "stability",
            "state_space", "neural_ssm", "llms", "code_agents", "vv", "self_compute",
            "experiment_loops",
        }
        self.play(self.camera.frame.animate.move_to(ORIGIN).set(width=12.8), run_time=1.25)
        reveal(final_nodes, final_labels, run_time=1.9)
        self.play(Rotate(atlas.frontier_particles, angle=14 * DEGREES, about_point=ORIGIN), run_time=1.5)
        self.wait(0.4)


class OrbitalTechTreeCleanAtlasFinalStill(Scene):
    def setup(self):
        self.camera.background_color = BG

    def construct(self):
        atlas = CleanOrbitalAtlas()
        self.add(atlas.base)
        for edge in EDGES:
            self.add(atlas.edges[bridge_key(edge.source, edge.target)])
        for edge in BRIDGES:
            self.add(atlas.bridges[bridge_key(edge.source, edge.target)])
        self.add(*atlas.nodes.values())
        final_labels = {
            "fourier", "dct", "signal_processing", "video_codecs", "laplace", "stability",
            "state_space", "neural_ssm", "llms", "code_agents", "vv", "self_compute",
            "experiment_loops",
        }
        self.add(*atlas.mobjects_for_labels(final_labels))
