from __future__ import annotations

from manim import *

from layout_validate import fit_text_to_width
from visual_style import BG, BLUE, CYAN, GOLD, GREEN, MUTED, RED, VIOLET, WHITE


COLORS = {
    "classical": CYAN,
    "control": GOLD,
    "learned": GREEN,
    "software": BLUE,
    "frontier": "#FF8FB0",
    "bridge": VIOLET,
}


class TechTreeReviewBase(Scene):
    def setup(self):
        self.camera.background_color = BG

    def title(self, text: str, subtitle: str) -> VGroup:
        title = Text(text, color=WHITE, font_size=24).set_fill(WHITE, opacity=0.98).set_stroke(width=0)
        sub = Text(subtitle, color=MUTED, font_size=13).set_fill(MUTED, opacity=0.92).set_stroke(width=0)
        group = VGroup(title, sub).arrange(DOWN, buff=0.12)
        group.to_edge(UP).shift(DOWN * 0.08)
        return group

    def label(self, text: str, color: str, size: int = 15) -> Text:
        return Text(text, color=color, font_size=size, line_spacing=0.78).set_fill(color, opacity=0.98).set_stroke(width=0)

    def card(
        self,
        text: str,
        color: str,
        pos,
        *,
        width: float = 1.52,
        height: float = 0.50,
        font_size: int = 12,
        opacity: float = 0.96,
    ) -> VGroup:
        pos = np.array([pos[0], pos[1], 0.0])
        shell = RoundedRectangle(width=width, height=height, corner_radius=0.075, color=color, stroke_width=1.7)
        shell.set_fill("#030814", opacity=opacity)
        glow = shell.copy().set_stroke(color, width=7, opacity=0.13)
        dot = Dot(LEFT * (width / 2 - 0.15), color=color, radius=0.045)
        label = Text(text, color=WHITE, font_size=font_size, line_spacing=0.78).set_stroke(width=0)
        fit_text_to_width(label, width - 0.34, min_scale=0.62)
        label.move_to(RIGHT * 0.08)
        return VGroup(glow, shell, dot, label).move_to(pos)

    def link(self, a: Mobject, b: Mobject, color: str, *, dashed: bool = False, width: float = 2.1, opacity: float = 0.74):
        start = a.get_right() + RIGHT * 0.035
        end = b.get_left() + LEFT * 0.035
        if dashed:
            core = DashedLine(start, end, color=color, stroke_width=width, dash_length=0.13)
        else:
            core = Line(start, end, color=color, stroke_width=width)
        core.set_opacity(opacity)
        glow = core.copy().set_stroke(color, width=width * 3.5, opacity=0.10)
        return VGroup(glow, core)

    def curve(self, a: Mobject, b: Mobject, color: str, *, dashed: bool = False, bend: float = 0.45, opacity: float = 0.72):
        start = a.get_center()
        end = b.get_center()
        delta = end - start
        ctrl1 = start + delta * 0.38 + UP * bend
        ctrl2 = start + delta * 0.68 + UP * bend
        path = CubicBezier(start, ctrl1, ctrl2, end)
        path.set_stroke(color, width=2.0, opacity=opacity)
        if dashed:
            path = DashedVMobject(path, num_dashes=32, dashed_ratio=0.62)
            path.set_stroke(color, width=2.0, opacity=opacity)
        glow = path.copy().set_stroke(color, width=7, opacity=0.09)
        return VGroup(glow, path)

    def category_band(self, name: str, color: str, y: float, *, height: float = 0.82) -> VGroup:
        band = RoundedRectangle(width=12.95, height=height, corner_radius=0.08, color=color, stroke_width=1.0)
        band.set_fill(color, opacity=0.045).set_stroke(color, opacity=0.20)
        band.move_to(np.array([0.25, y, -0.1]))
        text = Text(name, color=color, font_size=13).set_fill(color, opacity=0.95).set_stroke(width=0)
        text.move_to(np.array([-6.58, y + height * 0.20, 0]))
        return VGroup(band, text)


class TechTreeLayoutLineageBoard(TechTreeReviewBase):
    """Philosophy 1: readable rows, historical lineage first, convergence second."""

    def construct(self):
        self.add(self.title(
            "technology tree inventory - lineage board",
            "organized as families of unlocks; dashed/diagonal links show cross-category convergence",
        ))

        y = {
            "classical": 2.06,
            "control": 0.98,
            "learned": -0.12,
            "software": -1.34,
            "frontier": -2.55,
        }
        for name in ["classical", "control", "learned", "software", "frontier"]:
            self.add(self.category_band(name, COLORS[name], y[name], height=0.92 if name != "frontier" else 1.05))

        nodes = {
            "fourier": self.card("Fourier /\nLaplace", CYAN, (-4.85, y["classical"] + 0.23)),
            "dct": self.card("DCT / fixed\nfrequency bases", VIOLET, (-4.85, y["classical"] - 0.28), width=1.78, font_size=11),
            "signal": self.card("signal\nprocessing", CYAN, (-2.75, y["classical"]), width=1.35),
            "codecs": self.card("MP3 / JPEG /\nMPEG", CYAN, (-0.75, y["classical"]), width=1.55),
            "control": self.card("classical\ncontrol", GOLD, (-4.85, y["control"]), width=1.42),
            "state": self.card("state-space\nmodels", GOLD, (-2.75, y["control"]), width=1.42),
            "ssm": self.card("neural SSMs\nS4 / Mamba", VIOLET, (-0.60, y["control"]), width=1.60),
            "nn": self.card("neural\nnetworks", GREEN, (-5.15, y["learned"]), width=1.35),
            "embed": self.card("embeddings", GREEN, (-3.45, y["learned"]), width=1.28),
            "transformers": self.card("transformer\nsequence models", GOLD, (-1.55, y["learned"]), width=1.78, font_size=11),
            "llms": self.card("large language\nmodels", GOLD, (0.50, y["learned"]), width=1.62),
            "contrastive": self.card("contrastive\nmultimodal", GREEN, (-3.20, y["learned"] - 0.60), width=1.55, font_size=11),
            "auto": self.card("autoencoders /\nGANs", GREEN, (-3.20, y["learned"] + 0.56), width=1.46, font_size=11),
            "neural_codecs": self.card("neural codecs\nEnCodec", GREEN, (-1.18, y["learned"] + 0.56), width=1.52, font_size=11),
            "audio_tokens": self.card("discrete\naudio tokens", GREEN, (0.80, y["learned"] + 0.56), width=1.45, font_size=11),
            "speech": self.card("speech /\naudio agents", GREEN, (2.75, y["learned"] + 0.56), width=1.55, font_size=11),
            "multi": self.card("multimodal\ntools", GREEN, (2.75, y["learned"] - 0.30), width=1.42),
            "software": self.card("software as\nformal rep.", BLUE, (-5.25, y["software"] + 0.28), width=1.60, font_size=11),
            "expert": self.card("classical\nexpert systems", BLUE, (-5.25, y["software"] - 0.35), width=1.60, font_size=11),
            "blackboard": self.card("blackboard\narchitectures", BLUE, (-3.15, y["software"] - 0.35), width=1.58, font_size=11),
            "code_agents": self.card("autonomous\ncode agents", CYAN, (-1.15, y["software"] + 0.28), width=1.55, font_size=11),
            "research": self.card("research\nassistants", CYAN, (0.85, y["software"] + 0.28), width=1.45),
            "proof": self.card("SMT / Dafny /\nproof tools", BLUE, (-1.15, y["software"] - 0.42), width=1.65, font_size=10),
            "vv": self.card("V&V /\nevidence", GREEN, (1.55, y["software"] - 0.22), width=1.38),
            "reliable": self.card("reliable agent\nworkflows", GREEN, (3.65, y["software"] - 0.02), width=1.65, font_size=11),
            "orgs": self.card("transform-native\norganizations", COLORS["frontier"], (-3.85, y["frontier"] + 0.26), width=1.85, font_size=10),
            "self": self.card("self-inhabiting\ncompute", COLORS["frontier"], (-1.75, y["frontier"] + 0.26), width=1.68, font_size=11),
            "loops": self.card("autonomous\nexperiment loops", GOLD, (0.55, y["frontier"] + 0.26), width=1.86, font_size=10),
            "devs": self.card("discrete-event\nworld models", COLORS["frontier"], (2.85, y["frontier"] + 0.26), width=1.74, font_size=10),
            "rd": self.card("closed-loop\nR&D", GOLD, (5.05, y["frontier"] + 0.26), width=1.44),
        }
        self.add(*nodes.values())

        edges = [
            ("fourier", "signal", CYAN), ("dct", "signal", VIOLET), ("signal", "codecs", CYAN),
            ("control", "state", GOLD), ("state", "ssm", VIOLET),
            ("nn", "embed", GREEN), ("embed", "transformers", GREEN), ("transformers", "llms", GOLD),
            ("nn", "contrastive", GREEN), ("contrastive", "multi", GREEN),
            ("nn", "auto", GREEN), ("auto", "neural_codecs", GREEN), ("neural_codecs", "audio_tokens", GREEN),
            ("audio_tokens", "speech", GREEN), ("audio_tokens", "multi", GREEN),
            ("software", "code_agents", BLUE), ("expert", "blackboard", BLUE), ("blackboard", "vv", BLUE),
            ("code_agents", "vv", GREEN), ("proof", "vv", GREEN), ("vv", "reliable", GREEN),
            ("loops", "devs", GOLD), ("devs", "rd", GOLD),
        ]
        self.add(*[self.link(nodes[a], nodes[b], color) for a, b, color in edges])

        cross_edges = [
            self.curve(nodes["transformers"], nodes["ssm"], VIOLET, dashed=True, bend=0.34, opacity=0.82),
            self.curve(nodes["ssm"], nodes["llms"], VIOLET, dashed=True, bend=-0.34, opacity=0.82),
            self.curve(nodes["llms"], nodes["code_agents"], GOLD, bend=-0.35, opacity=0.75),
            self.curve(nodes["llms"], nodes["research"], GOLD, bend=-0.25, opacity=0.70),
            self.curve(nodes["reliable"], nodes["orgs"], COLORS["frontier"], bend=-0.70, opacity=0.46),
            self.curve(nodes["research"], nodes["loops"], GOLD, bend=-0.55, opacity=0.58),
            self.curve(nodes["multi"], nodes["loops"], GOLD, bend=-1.20, opacity=0.34),
            self.curve(nodes["reliable"], nodes["loops"], GOLD, bend=-0.75, opacity=0.65),
            self.curve(nodes["reliable"], nodes["self"], COLORS["frontier"], bend=-0.85, opacity=0.62),
            self.curve(nodes["orgs"], nodes["rd"], GOLD, bend=-0.55, opacity=0.38),
            self.curve(nodes["self"], nodes["rd"], COLORS["frontier"], bend=-0.52, opacity=0.36),
        ]
        self.add(*cross_edges)


class TechTreeLayoutConvergenceMap(TechTreeReviewBase):
    """Philosophy 2: center the convergences, not the timeline."""

    def construct(self):
        self.add(self.title(
            "technology tree inventory - convergence map",
            "families orbit the new bottleneck; bridges show where lineages combine",
        ))

        rings = VGroup(
            Circle(radius=0.98, color=GOLD, stroke_width=1.0).set_stroke(GOLD, opacity=0.20),
            Circle(radius=2.20, color=GREEN, stroke_width=1.0).set_stroke(GREEN, opacity=0.12),
            Circle(radius=3.55, color=BLUE, stroke_width=0.9).set_stroke(BLUE, opacity=0.10),
        ).shift(DOWN * 0.25)
        self.add(rings)

        nodes = {
            "llms": self.card("large language\nmodels", GOLD, (0.0, -0.10), width=1.70, height=0.62, font_size=13),
            "transformers": self.card("transformers", GOLD, (-1.55, 0.78), width=1.38),
            "embeddings": self.card("embeddings", GREEN, (-2.85, 1.35), width=1.28),
            "nn": self.card("neural\nnetworks", GREEN, (-3.65, 2.10), width=1.35),
            "contrastive": self.card("contrastive\nspaces", GREEN, (-1.15, 2.10), width=1.42),
            "multi": self.card("multimodal\ntools", GREEN, (1.15, 2.10), width=1.40),
            "auto": self.card("autoencoders /\nGANs", GREEN, (-2.95, 2.45), width=1.48, font_size=11),
            "neural_codecs": self.card("neural\ncodecs", GREEN, (-1.25, 2.58), width=1.20),
            "audio_tokens": self.card("audio\ntokens", GREEN, (0.30, 2.55), width=1.12),
            "speech": self.card("speech /\naudio agents", GREEN, (1.85, 2.42), width=1.55, font_size=11),
            "fourier": self.card("Fourier /\nLaplace", CYAN, (-5.15, 1.45), width=1.35),
            "dct": self.card("DCT", VIOLET, (-5.25, 0.55), width=0.94),
            "signal": self.card("signal\nprocessing", CYAN, (-4.05, 0.98), width=1.32),
            "codecs": self.card("MP3 / JPEG /\nMPEG", CYAN, (-5.20, 2.02), width=1.48, font_size=11),
            "control": self.card("classical\ncontrol", GOLD, (-5.10, -1.70), width=1.36),
            "state": self.card("state-space\nmodels", GOLD, (-3.78, -1.05), width=1.40),
            "ssm": self.card("neural SSMs\nS4 / Mamba", VIOLET, (-2.05, -0.60), width=1.58, font_size=11),
            "software": self.card("software as\nformal rep.", BLUE, (3.10, 1.72), width=1.55, font_size=11),
            "code_agents": self.card("code\nagents", CYAN, (2.28, 0.82), width=1.12),
            "research": self.card("research\nassistants", CYAN, (2.15, -0.16), width=1.35),
            "expert": self.card("expert\nsystems", BLUE, (4.62, 2.18), width=1.20),
            "blackboard": self.card("blackboard\narchitectures", BLUE, (4.58, 1.26), width=1.52, font_size=11),
            "proof": self.card("proof\ntools", BLUE, (4.72, 0.28), width=1.08),
            "vv": self.card("V&V /\nevidence", GREEN, (3.82, -0.70), width=1.28),
            "reliable": self.card("reliable agent\nworkflows", GREEN, (3.05, -1.62), width=1.62, font_size=11),
            "orgs": self.card("transform-native\norganizations", COLORS["frontier"], (4.74, -1.88), width=1.82, font_size=10),
            "self": self.card("self-inhabiting\ncompute", COLORS["frontier"], (5.05, -2.55), width=1.66, font_size=11),
            "loops": self.card("autonomous\nexperiment loops", GOLD, (2.72, -2.65), width=1.82, font_size=10),
            "devs": self.card("discrete-event\nworld models", COLORS["frontier"], (0.75, -2.78), width=1.72, font_size=10),
            "rd": self.card("closed-loop\nR&D", GOLD, (-1.10, -2.50), width=1.32),
        }
        self.add(*nodes.values())

        links = [
            ("nn", "embeddings", GREEN), ("embeddings", "transformers", GREEN), ("transformers", "llms", GOLD),
            ("nn", "contrastive", GREEN), ("contrastive", "multi", GREEN),
            ("auto", "neural_codecs", GREEN), ("neural_codecs", "audio_tokens", GREEN),
            ("audio_tokens", "speech", GREEN), ("audio_tokens", "multi", GREEN),
            ("fourier", "signal", CYAN), ("dct", "signal", VIOLET), ("signal", "codecs", CYAN),
            ("control", "state", GOLD), ("state", "ssm", VIOLET),
            ("software", "code_agents", BLUE), ("expert", "blackboard", BLUE), ("blackboard", "vv", BLUE),
            ("proof", "vv", GREEN), ("vv", "reliable", GREEN),
            ("loops", "devs", GOLD), ("devs", "rd", GOLD),
        ]
        self.add(*[self.curve(nodes[a], nodes[b], color, bend=0.12, opacity=0.66) for a, b, color in links])

        emphasized = [
            self.curve(nodes["transformers"], nodes["ssm"], VIOLET, dashed=True, bend=-0.55, opacity=0.90),
            self.curve(nodes["ssm"], nodes["llms"], VIOLET, dashed=True, bend=0.45, opacity=0.90),
            self.curve(nodes["llms"], nodes["code_agents"], GOLD, bend=0.08, opacity=0.88),
            self.curve(nodes["llms"], nodes["research"], GOLD, bend=-0.28, opacity=0.72),
            self.curve(nodes["code_agents"], nodes["vv"], GREEN, bend=-0.25, opacity=0.78),
            self.curve(nodes["reliable"], nodes["loops"], GOLD, bend=-0.10, opacity=0.80),
            self.curve(nodes["multi"], nodes["loops"], GOLD, bend=-1.35, opacity=0.52),
            self.curve(nodes["research"], nodes["loops"], GOLD, bend=-0.80, opacity=0.62),
            self.curve(nodes["reliable"], nodes["orgs"], COLORS["frontier"], bend=0.18, opacity=0.65),
            self.curve(nodes["reliable"], nodes["self"], COLORS["frontier"], bend=-0.42, opacity=0.62),
            self.curve(nodes["orgs"], nodes["rd"], GOLD, bend=-0.80, opacity=0.45),
            self.curve(nodes["self"], nodes["rd"], COLORS["frontier"], bend=-0.68, opacity=0.45),
        ]
        self.add(*emphasized)

        note = Text("dashed: cross-category convergence", color=VIOLET, font_size=15)
        note.set_fill(VIOLET, opacity=0.96).set_stroke(width=0)
        note.to_edge(DOWN).shift(UP * 0.10)
        self.add(note)
