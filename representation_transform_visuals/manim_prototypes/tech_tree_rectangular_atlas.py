from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from manim import *

from visual_style import BG, BLUE, CYAN, GOLD, GREEN, GRID, MUTED, VIOLET, WHITE


FRONTIER = "#FF8FB0"
CARD_FILL = "#00020A"
CARD_FILL_DIM = "#01040C"
CONNECTOR_GAP = 0.07
DEFAULT_TARGET_SECONDS = 24.0

_DURATIONS_PATH = Path(__file__).with_name("scene_durations.json")
_SCENE_DURATIONS: dict[str, float] = {}
if _DURATIONS_PATH.exists():
    _SCENE_DURATIONS = json.loads(_DURATIONS_PATH.read_text(encoding="utf-8"))


@dataclass(frozen=True)
class RectNode:
    key: str
    label: str
    lane: str
    x: float
    y: float
    color: str
    width: float = 1.24
    height: float = 0.52


LANES = {
    "signal": ("signal", CYAN, 2.55),
    "control": ("control", GOLD, 1.08),
    "learned": ("learned", VIOLET, -0.58),
    "software": ("code", GREEN, -2.12),
}


NODES = {
    # Signal/media transforms.
    "fourier": RectNode("fourier", "Fourier", "signal", -4.85, 2.70, CYAN, 1.04),
    "frequency": RectNode("frequency", "frequency\nview", "signal", -3.35, 2.70, CYAN, 1.10),
    "signal_processing": RectNode("signal_processing", "signal\nprocessing", "signal", -1.75, 2.70, CYAN, 1.24),
    "wireless": RectNode("wireless", "wireless", "signal", -0.06, 2.70, CYAN, 1.05),
    "compressed_audio": RectNode("compressed_audio", "compressed\naudio", "signal", 1.38, 2.70, CYAN, 1.25),
    "dct": RectNode("dct", "DCT", "signal", -3.35, 2.04, VIOLET, 0.86),
    "jpeg": RectNode("jpeg", "JPEG", "signal", -1.75, 2.04, VIOLET, 0.90),
    "video_codecs": RectNode("video_codecs", "video\ncodecs", "signal", -0.06, 2.04, VIOLET, 1.04),
    # Dynamics/control.
    "laplace": RectNode("laplace", "Laplace", "control", -4.85, 1.08, GOLD, 1.04),
    "transfer": RectNode("transfer", "transfer\nfunctions", "control", -3.35, 1.08, GOLD, 1.26),
    "stability": RectNode("stability", "stability\ncontrol", "control", -1.75, 1.08, GOLD, 1.22),
    "feedback": RectNode("feedback", "feedback\ncontrollers", "control", -0.06, 1.08, GOLD, 1.36),
    "motors": RectNode("motors", "brushless\nmotors", "control", 1.62, 1.36, GOLD, 1.22),
    "flight": RectNode("flight", "flight +\nrobotics", "control", 1.62, 0.80, GOLD, 1.18),
    "state_space": RectNode("state_space", "state-space\nmodels", "control", 3.34, 1.08, GOLD, 1.34),
    "neural_ssm": RectNode("neural_ssm", "neural\nSSMs", "control", 5.05, 0.48, VIOLET, 1.05),
    # Learned representation spaces.
    "neural_networks": RectNode("neural_networks", "neural\nnetworks", "learned", -4.85, -0.58, VIOLET, 1.16),
    "embeddings": RectNode("embeddings", "embeddings", "learned", -3.28, -0.58, VIOLET, 1.18),
    "transformers": RectNode("transformers", "transformers", "learned", -1.58, -0.58, VIOLET, 1.36),
    "llms": RectNode("llms", "LLMs", "learned", 0.05, -0.58, VIOLET, 0.90),
    "contrastive": RectNode("contrastive", "contrastive\nspaces", "learned", 1.56, -0.25, VIOLET, 1.28),
    "autoencoders": RectNode("autoencoders", "autoencoders", "learned", 1.56, -0.90, VIOLET, 1.34),
    "neural_codecs": RectNode("neural_codecs", "neural\ncodecs", "learned", 3.14, -0.90, VIOLET, 1.14),
    "multimodal": RectNode("multimodal", "multimodal\ntools", "learned", 3.14, -0.25, VIOLET, 1.24),
    # Language/code/verification.
    "software_form": RectNode("software_form", "software as\nrepresentation", "software", -4.85, -2.12, GREEN, 1.44),
    "expert": RectNode("expert", "expert\nsystems", "software", -3.26, -2.58, BLUE, 1.08),
    "blackboard": RectNode("blackboard", "blackboard\narchitectures", "software", -1.70, -2.58, BLUE, 1.38),
    "proof_tools": RectNode("proof_tools", "proof\ntools", "software", -1.70, -1.76, GREEN, 1.00),
    "code_agents": RectNode("code_agents", "code\nagents", "software", 0.02, -2.12, CYAN, 1.00),
    "vv": RectNode("vv", "V&V /\nevidence", "software", 1.62, -2.12, GREEN, 1.10),
    "reliable": RectNode("reliable", "reliable\nworkflows", "software", 3.20, -2.12, GREEN, 1.24),
    # Frontier is a region, not a category.
    "self_compute": RectNode("self_compute", "self-\ninhabiting\ncompute", "frontier", 5.15, 2.20, FRONTIER, 1.46, 0.68),
    "experiment_loops": RectNode("experiment_loops", "autonomous\nexperiment loops", "frontier", 5.15, 1.36, FRONTIER, 1.62),
    "world_models": RectNode("world_models", "discrete-event\nworld models", "frontier", 5.15, -0.80, FRONTIER, 1.60),
    "closed_loop_rd": RectNode("closed_loop_rd", "closed-loop\nR&D", "frontier", 5.15, -1.56, FRONTIER, 1.22),
}


EDGES = [
    ("fourier", "frequency", CYAN),
    ("frequency", "signal_processing", CYAN),
    ("signal_processing", "wireless", CYAN),
    ("signal_processing", "compressed_audio", CYAN),
    ("dct", "jpeg", VIOLET),
    ("jpeg", "video_codecs", VIOLET),
    ("laplace", "transfer", GOLD),
    ("transfer", "stability", GOLD),
    ("stability", "feedback", GOLD),
    ("feedback", "motors", GOLD),
    ("feedback", "flight", GOLD),
    ("stability", "state_space", GOLD),
    ("neural_networks", "embeddings", VIOLET),
    ("embeddings", "transformers", VIOLET),
    ("transformers", "llms", VIOLET),
    ("llms", "contrastive", VIOLET),
    ("autoencoders", "neural_codecs", VIOLET),
    ("neural_codecs", "multimodal", VIOLET),
    ("software_form", "code_agents", GREEN),
    ("expert", "blackboard", BLUE),
    ("blackboard", "vv", BLUE),
    ("proof_tools", "vv", GREEN),
    ("code_agents", "vv", GREEN),
    ("vv", "reliable", GREEN),
    ("reliable", "self_compute", FRONTIER),
    ("reliable", "experiment_loops", FRONTIER),
    ("experiment_loops", "world_models", FRONTIER),
    ("world_models", "closed_loop_rd", FRONTIER),
]


BRIDGES = [
    ("state_space", "neural_ssm", VIOLET),
    ("neural_ssm", "llms", VIOLET),
    ("llms", "code_agents", GOLD),
    ("code_agents", "vv", GREEN),
]


REVEALS = [
    (
        {"fourier", "frequency", "signal_processing", "wireless", "compressed_audio", "dct", "jpeg", "video_codecs"},
        {"fourier", "frequency", "signal_processing", "dct", "jpeg", "video_codecs"},
        1.5,
    ),
    (
        {"laplace", "transfer", "stability", "feedback", "motors", "flight", "state_space", "neural_ssm"},
        {"laplace", "transfer", "stability", "feedback", "state_space", "neural_ssm"},
        1.6,
    ),
    (
        {"neural_networks", "embeddings", "transformers", "llms", "contrastive", "autoencoders", "neural_codecs", "multimodal"},
        {"neural_networks", "embeddings", "transformers", "llms", "multimodal"},
        1.7,
    ),
    (
        {"software_form", "expert", "blackboard", "proof_tools", "code_agents", "vv", "reliable"},
        {"software_form", "code_agents", "vv", "reliable"},
        1.6,
    ),
    (
        {"self_compute", "experiment_loops", "world_models", "closed_loop_rd"},
        {"self_compute", "experiment_loops"},
        1.5,
    ),
]


def point_of(node: RectNode) -> np.ndarray:
    return RIGHT * node.x + UP * node.y


def as_point(x: float, y: float) -> np.ndarray:
    return RIGHT * x + UP * y


def path_from_points(points: list[np.ndarray]) -> VGroup:
    deduped: list[np.ndarray] = []
    for point in points:
        if not deduped or np.linalg.norm(point - deduped[-1]) > 0.01:
            deduped.append(point)
    segments = VGroup()
    for start, end in zip(deduped, deduped[1:]):
        segment = Line(start, end)
        segment.set_fill(opacity=0.0)
        segment.set_stroke(opacity=0.0)
        segments.add(segment)
    return segments


def glow_line(path: Mobject, color: str, width: float = 3.0, opacity: float = 1.0) -> VGroup:
    halo = path.copy().set_stroke(color, width=width * 3.2, opacity=0.18 * opacity)
    core = path.copy().set_stroke(color, width=width, opacity=opacity)
    halo.set_fill(opacity=0.0)
    core.set_fill(opacity=0.0)
    halo.set_z_index(-30)
    core.set_z_index(-25)
    group = VGroup(halo, core)
    group.set_z_index(-30, family=True)
    return group


def card(node: RectNode, show_label: bool = True) -> VGroup:
    position = point_of(node)
    box = RoundedRectangle(corner_radius=0.08, width=node.width, height=node.height, color=node.color, stroke_width=2.0)
    box.set_fill(CARD_FILL, opacity=1.0)
    mask = RoundedRectangle(corner_radius=0.06, width=node.width - 0.05, height=node.height - 0.05, stroke_width=0)
    mask.set_fill(CARD_FILL, opacity=1.0)
    glow = box.copy().set_fill(CARD_FILL, opacity=0.0).set_stroke(node.color, width=7.0, opacity=0.15)
    box.move_to(position)
    mask.move_to(position)
    glow.move_to(position)
    if show_label:
        line_count = node.label.count("\n") + 1
        if line_count >= 3:
            font_size = 11
        else:
            font_size = 15 if "\n" not in node.label and len(node.label) <= 12 else 13
        label = Text(node.label, color=WHITE, font_size=font_size, line_spacing=0.78, font="DejaVu Sans")
        # Long single-line labels ("embeddings", "transformers", "autoencoders")
        # were rendering WIDER than their card, so the text spilled out of the
        # box and collided with the purple connector lines (user: "overlapping
        # text in the purple boxes"). Scale any label down to fit inside the
        # card width so text always stays within its box.
        max_label_width = node.width - 0.18
        if label.width > max_label_width:
            label.scale(max_label_width / label.width)
        label.move_to(position)
        label.set_fill(WHITE, opacity=1.0).set_stroke(width=0)
    else:
        label = Dot(position, radius=0.035, color=node.color)
    glow.set_z_index(340)
    box.set_z_index(420)
    mask.set_z_index(460)
    label.set_z_index(500)
    group = VGroup(glow, box, mask, label)
    group.set_z_index(420)
    return group


def right_edge(node: RectNode) -> np.ndarray:
    return point_of(node) + RIGHT * (node.width / 2)


def left_edge(node: RectNode) -> np.ndarray:
    return point_of(node) + LEFT * (node.width / 2)


def top_edge(node: RectNode) -> np.ndarray:
    return point_of(node) + UP * (node.height / 2)


def bottom_edge(node: RectNode) -> np.ndarray:
    return point_of(node) + DOWN * (node.height / 2)


def rail_y_for(source: RectNode, target: RectNode) -> float:
    if source.lane == "learned" or target.lane == "learned":
        return min(source.y - source.height / 2, target.y - target.height / 2) - 0.16
    if source.lane == "software" or target.lane == "software":
        return min(source.y - source.height / 2, target.y - target.height / 2) - 0.17
    if source.lane == "signal" and source.y > 2.3 and target.y > 2.3:
        return source.y + source.height / 2 + 0.15
    if source.lane == "control" or target.lane == "control":
        return max(source.y + source.height / 2, target.y + target.height / 2) + 0.14
    return source.y


def routed_same_lane(source: RectNode, target: RectNode) -> VGroup:
    start = right_edge(source) + RIGHT * CONNECTOR_GAP
    end = left_edge(target) + LEFT * CONNECTOR_GAP
    if source.lane == "learned" and source.y > -0.75:
        rail_y = max(source.y + source.height / 2, target.y + target.height / 2) + 0.16
    else:
        rail_y = rail_y_for(source, target)
    jog = 0.12 if end[0] >= start[0] else -0.12
    return path_from_points(
        [
            start,
            as_point(start[0] + jog, start[1]),
            as_point(start[0] + jog, rail_y),
            as_point(end[0] - jog, rail_y),
            as_point(end[0] - jog, end[1]),
            end,
        ]
    )


def edge_path(source_key: str, target_key: str) -> Mobject:
    source = NODES[source_key]
    target = NODES[target_key]

    if source_key == "neural_ssm" and target_key == "llms":
        start = left_edge(source) + LEFT * CONNECTOR_GAP
        end = top_edge(target) + UP * CONNECTOR_GAP
        return path_from_points(
            [
                start,
                as_point(3.95, start[1]),
                as_point(3.95, -0.05),
                as_point(end[0], -0.05),
                end,
            ]
        )

    if source_key == "llms" and target_key == "code_agents":
        return path_from_points([bottom_edge(source) + DOWN * CONNECTOR_GAP, top_edge(target) + UP * CONNECTOR_GAP])

    if source_key == "blackboard" and target_key == "vv":
        start = right_edge(source) + RIGHT * CONNECTOR_GAP
        end = left_edge(target) + LEFT * CONNECTOR_GAP
        rail_y = min(source.y - source.height / 2, target.y - target.height / 2) - 0.15
        return path_from_points([start, as_point(start[0] + 0.16, rail_y), as_point(end[0] - 0.16, rail_y), end])

    if abs(source.y - target.y) < 0.08 and target.x > source.x and source.lane == "learned":
        return routed_same_lane(source, target)

    if abs(source.y - target.y) < 0.08 and target.x > source.x:
        return path_from_points([right_edge(source) + RIGHT * CONNECTOR_GAP, left_edge(target) + LEFT * CONNECTOR_GAP])

    if abs(source.x - target.x) < 0.08 and source.lane == "frontier" and target.lane == "frontier":
        start = right_edge(source) + RIGHT * CONNECTOR_GAP
        end = right_edge(target) + RIGHT * CONNECTOR_GAP
        rail_x = max(start[0], end[0]) + 0.28
        return path_from_points([start, as_point(rail_x, start[1]), as_point(rail_x, end[1]), end])

    if abs(source.x - target.x) < 0.08:
        if target.y > source.y:
            start = top_edge(source) + UP * CONNECTOR_GAP
            end = bottom_edge(target) + DOWN * CONNECTOR_GAP
        else:
            start = bottom_edge(source) + DOWN * CONNECTOR_GAP
            end = top_edge(target) + UP * CONNECTOR_GAP
        rail_x = source.x + max(source.width, target.width) / 2 + 0.22
        return path_from_points([start, as_point(rail_x, start[1]), as_point(rail_x, end[1]), end])

    if target.x >= source.x:
        start = right_edge(source) + RIGHT * CONNECTOR_GAP
        end = left_edge(target) + LEFT * CONNECTOR_GAP
    else:
        start = left_edge(source) + LEFT * CONNECTOR_GAP
        end = right_edge(target) + RIGHT * CONNECTOR_GAP
    middle_x = (start[0] + end[0]) / 2
    return path_from_points([start, as_point(middle_x, start[1]), as_point(middle_x, end[1]), end])


class RectangularTechTreeAtlas(Scene):
    """A rectangular, lane-based tech-tree attempt."""

    def setup(self):
        self.camera.background_color = BG
        self.target_seconds = float(_SCENE_DURATIONS.get(type(self).__name__, DEFAULT_TARGET_SECONDS))

    def remaining_wait(self) -> None:
        elapsed = getattr(self.renderer, "time", 0.0) or 0.0
        remaining = self.target_seconds - elapsed
        while remaining > 0:
            step = min(4.0, remaining)
            self.wait(step)
            remaining -= step

    def construct(self):
        lane_groups = self.build_lanes()
        frontier = self.build_frontier_region()
        self.add(lane_groups, frontier)

        cards = {key: card(node, show_label=True) for key, node in NODES.items()}
        edges = {
            f"{source}->{target}": glow_line(edge_path(source, target), color, width=2.0, opacity=0.86)
            for source, target, color in EDGES
        }
        bridges = {
            f"{source}->{target}": glow_line(edge_path(source, target), color, width=2.7, opacity=0.92)
            for source, target, color in BRIDGES
        }
        for edge in list(edges.values()) + list(bridges.values()):
            edge.set_opacity(0.0)
        self.add(*edges.values(), *bridges.values())

        revealed: set[str] = set()
        revealed_edges: set[str] = set()
        intro_time = min(1.6, max(0.8, self.target_seconds * 0.025))
        reveal_budget = max(8.0, self.target_seconds * 0.72)
        reveal_weight_total = sum(reveal[2] for reveal in REVEALS)
        highlight_time = min(2.4, max(0.8, self.target_seconds * 0.025))
        self.play(FadeIn(lane_groups), FadeIn(frontier), run_time=intro_time)

        for nodes, label_nodes, run_weight in REVEALS:
            run_time = reveal_budget * (run_weight / reveal_weight_total)
            revealed |= nodes
            edge_keys = {
                f"{source}->{target}"
                for source, target, _ in EDGES
                if source in revealed and target in revealed
            }
            bridge_keys = {
                f"{source}->{target}"
                for source, target, _ in BRIDGES
                if source in revealed and target in revealed
            }
            new_edge_keys = (edge_keys | bridge_keys) - revealed_edges
            revealed_edges |= new_edge_keys

            edge_animations: list[Animation] = []
            card_animations: list[Animation] = []
            for key in new_edge_keys:
                if key in edges:
                    edge_animations.append(edges[key].animate.set_opacity(1.0))
                if key in bridges:
                    edge_animations.append(bridges[key].animate.set_opacity(1.0))
            for key in nodes:
                card_animations.append(FadeIn(cards[key], shift=RIGHT * 0.05))
            card_time = min(2.0, max(0.8, run_time * 0.22))
            edge_time = max(0.8, run_time - card_time)
            if card_animations:
                self.play(LaggedStart(*card_animations, lag_ratio=0.035), run_time=card_time)
            if edge_animations:
                self.bring_to_front(*[cards[key] for key in revealed])
                self.play(LaggedStart(*edge_animations, lag_ratio=0.035), run_time=edge_time)
                self.bring_to_front(*[cards[key] for key in revealed])
            if label_nodes:
                self.play(*[Circumscribe(cards[key][1], color=NODES[key].color, fade_out=True) for key in label_nodes], run_time=highlight_time)
                self.bring_to_front(*[cards[key] for key in revealed])

        path = ["state_space->neural_ssm", "neural_ssm->llms", "llms->code_agents", "code_agents->vv"]
        self.play(
            *[Indicate(bridges[key], color=WHITE, scale_factor=1.01) for key in path],
            run_time=min(5.5, max(1.4, self.target_seconds * 0.06)),
        )
        self.remaining_wait()

    def build_lanes(self) -> VGroup:
        lanes = VGroup()
        for key, (label, color, y) in LANES.items():
            band = Rectangle(width=11.45, height=1.12, stroke_width=0).set_fill(color, opacity=0.035)
            band.move_to(RIGHT * -0.22 + UP * y)
            line = Line(LEFT * 5.95 + UP * (y - 0.54), RIGHT * 5.60 + UP * (y - 0.54), color=color, stroke_width=1.4)
            line.set_stroke(color, opacity=0.34)
            title = Text(label, color=color, font_size=14, font="DejaVu Sans")
            title.move_to(LEFT * 6.26 + UP * (y + 0.38))
            title.set_stroke(BG, width=3.0, opacity=0.9, background=True)
            lanes.add(band, line, title)
        return lanes

    def build_frontier_region(self) -> VGroup:
        region = RoundedRectangle(corner_radius=0.08, width=2.10, height=6.35, color=FRONTIER, stroke_width=1.5)
        region.move_to(RIGHT * 5.15 + UP * 0.15)
        region.set_fill(FRONTIER, opacity=0.045)
        region.set_stroke(FRONTIER, opacity=0.38)
        label = Text("frontier", color=FRONTIER, font_size=17)
        label.move_to(RIGHT * 5.15 + UP * 3.70)
        label.set_stroke(BG, width=3.0, opacity=0.9, background=True)
        label_back = SurroundingRectangle(label, corner_radius=0.04, color=BG, buff=0.055, stroke_width=0)
        label_back.set_fill(BG, opacity=1.0)
        label_back.set_z_index(30)
        label.set_z_index(35)
        dots = VGroup()
        for i in range(34):
            x = 4.38 + (i % 5) * 0.36
            y = -2.86 + (i // 5) * 0.78
            dot = Dot(RIGHT * x + UP * y, radius=0.016 + 0.004 * (i % 3), color=[FRONTIER, CYAN, GOLD, VIOLET][i % 4])
            dot.set_opacity(0.28 + 0.08 * (i % 4))
            dots.add(dot)
        return VGroup(region, dots, label_back, label)


class RectangularTechTreeEnding(RectangularTechTreeAtlas):
    """Closing beat for section 14.

    Reuses the *exact* rectangular atlas layout from section 08 instead of the
    old grid tech-tree (user flagged the old tree still showing at the end).
    Rather than re-running the staged growth animation, this presents the tree
    as an already-grown whole, then pulls back while the closing titles fade in:
    "look at the forest you just grew".
    """

    def title_card(self, text: str, color: str, font_size: int, y: float) -> VGroup:
        core = Text(text, color=color, font_size=font_size, font="DejaVu Sans")
        core.move_to(UP * y)
        core.set_fill(color, opacity=1.0).set_stroke(width=0)
        back = SurroundingRectangle(core, corner_radius=0.08, color=BG, buff=0.12, stroke_width=0)
        back.set_fill(BG, opacity=0.92)
        back.set_z_index(900)
        core.set_z_index(905)
        return VGroup(back, core)

    def construct(self):
        lanes = self.build_lanes()
        frontier = self.build_frontier_region()
        cards = {key: card(node, show_label=True) for key, node in NODES.items()}
        edges = [
            glow_line(edge_path(source, target), color, width=2.0, opacity=0.86)
            for source, target, color in EDGES
        ]
        bridges = [
            glow_line(edge_path(source, target), color, width=2.7, opacity=0.92)
            for source, target, color in BRIDGES
        ]

        # Everything that makes up the tree pulls back together; titles stay put.
        tree = VGroup(lanes, frontier, *edges, *bridges, *cards.values())

        # 1) Establish the lanes and frontier region.
        self.play(FadeIn(lanes), FadeIn(frontier), run_time=1.2)

        # 2) Drop in the whole grown tree at once (a fast "complete the picture"
        #    reveal, not the section-08 row-by-row growth).
        self.play(
            LaggedStart(*[FadeIn(c, shift=UP * 0.04) for c in cards.values()], lag_ratio=0.02),
            run_time=2.6,
        )
        for edge in edges + bridges:
            edge.set_opacity(0.0)
        self.add(*edges, *bridges)
        self.bring_to_front(*cards.values())
        self.play(
            LaggedStart(*[e.animate.set_opacity(1.0) for e in edges + bridges], lag_ratio=0.03),
            run_time=2.4,
        )
        self.bring_to_front(*cards.values())
        self.wait(0.6)

        # 3) Gentle pull-back FIRST so the frame reads as zooming out on the
        #    grown forest and, critically, clears space at the top. Doing this
        #    before the titles keeps the (pink) subtitle from competing with the
        #    full-size pink "frontier" label and pulls the frontier box in off
        #    the right edge (both flagged by Gemini on the title-first cut).
        self.play(tree.animate.scale(0.9).shift(DOWN * 0.18), run_time=2.4)

        # 4) Closing titles fade into the now-clear top band.
        title = self.title_card("language is a computable material", WHITE, 30, 3.55)
        subtitle = self.title_card(
            "when civilization gets a new transform, the tree changes", FRONTIER, 19, 3.08
        )
        self.play(FadeIn(title), run_time=1.0)
        self.play(FadeIn(subtitle), run_time=0.9)
        self.wait(0.8)

        # 5) Frontier nodes breathe for the remainder so the closing hold stays
        #    alive instead of freezing on a static frame.
        frontier_keys = ["self_compute", "experiment_loops", "world_models", "closed_loop_rd"]
        frontier_cards = VGroup(*[cards[k] for k in frontier_keys])
        elapsed = getattr(self.renderer, "time", 0.0) or 0.0
        remaining = self.target_seconds - elapsed
        while remaining > 1.8:
            self.play(frontier_cards.animate.scale(1.05), run_time=1.6, rate_func=there_and_back)
            remaining -= 1.6
        self.remaining_wait()
