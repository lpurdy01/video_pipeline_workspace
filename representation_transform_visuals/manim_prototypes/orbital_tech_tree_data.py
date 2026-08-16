from __future__ import annotations

from dataclasses import dataclass

from visual_style import BLUE, CYAN, GOLD, GREEN, VIOLET, WHITE


FRONTIER = "#FF8FB0"


@dataclass(frozen=True)
class WedgeSpec:
    key: str
    label: str
    color: str
    start_deg: float
    end_deg: float


@dataclass(frozen=True)
class NodeSpec:
    key: str
    label: str
    wedge: str
    angle_deg: float
    radius: float
    color: str
    level: str


@dataclass(frozen=True)
class EdgeSpec:
    source: str
    target: str
    color: str
    kind: str = "flat"


WEDGES = {
    "signal": WedgeSpec("signal", "signal + media transforms", CYAN, 92, 180),
    "dynamics": WedgeSpec("dynamics", "dynamics + control", GOLD, 8, 92),
    "learned": WedgeSpec("learned", "learned representation spaces", VIOLET, 270, 360),
    "software": WedgeSpec("software", "language, code + verification", GREEN, 180, 270),
}


NODES = {
    # Classical signal/media.
    "fourier": NodeSpec("fourier", "Fourier", "signal", 138, 1.35, CYAN, "classical"),
    "frequency": NodeSpec("frequency", "frequency\nview", "signal", 135, 2.05, CYAN, "classical"),
    "signal_processing": NodeSpec("signal_processing", "signal\nprocessing", "signal", 130, 2.80, CYAN, "classical"),
    "wireless": NodeSpec("wireless", "wireless", "signal", 115, 3.55, CYAN, "classical"),
    "compressed_audio": NodeSpec("compressed_audio", "compressed\naudio", "signal", 148, 3.60, CYAN, "classical"),
    "spectral_imaging": NodeSpec("spectral_imaging", "spectral\nimaging", "signal", 166, 3.20, CYAN, "classical"),
    "dct": NodeSpec("dct", "DCT", "signal", 102, 1.65, VIOLET, "classical"),
    "jpeg": NodeSpec("jpeg", "JPEG", "signal", 100, 2.60, VIOLET, "classical"),
    "video_codecs": NodeSpec("video_codecs", "video\ncodecs", "signal", 96, 3.40, VIOLET, "classical"),
    # Dynamics/control.
    "laplace": NodeSpec("laplace", "Laplace", "dynamics", 70, 1.30, GOLD, "classical"),
    "transfer": NodeSpec("transfer", "transfer\nfunctions", "dynamics", 62, 2.05, GOLD, "classical"),
    "stability": NodeSpec("stability", "stability\ncontrol", "dynamics", 50, 2.70, GOLD, "classical"),
    "feedback": NodeSpec("feedback", "feedback\ncontrollers", "dynamics", 42, 3.35, GOLD, "classical"),
    "motors": NodeSpec("motors", "brushless\nmotors", "dynamics", 28, 3.65, GOLD, "classical"),
    "flight": NodeSpec("flight", "flight +\nrobotics", "dynamics", 16, 3.50, GOLD, "classical"),
    "state_space": NodeSpec("state_space", "state-space\nmodels", "dynamics", 34, 2.45, GOLD, "convergence"),
    "neural_ssm": NodeSpec("neural_ssm", "neural\nSSMs", "dynamics", 15, 2.75, VIOLET, "convergence"),
    # Learned representations.
    "neural_networks": NodeSpec("neural_networks", "neural\nnetworks", "learned", 330, 1.20, VIOLET, "modern"),
    "embeddings": NodeSpec("embeddings", "embeddings", "learned", 338, 1.92, VIOLET, "modern"),
    "transformers": NodeSpec("transformers", "transformers", "learned", 320, 2.40, VIOLET, "modern"),
    "llms": NodeSpec("llms", "LLMs", "learned", 305, 2.95, VIOLET, "modern"),
    "contrastive": NodeSpec("contrastive", "contrastive\nspaces", "learned", 292, 3.45, VIOLET, "modern"),
    "autoencoders": NodeSpec("autoencoders", "autoencoders", "learned", 276, 2.50, VIOLET, "modern"),
    "neural_codecs": NodeSpec("neural_codecs", "neural\ncodecs", "learned", 282, 3.15, VIOLET, "modern"),
    "audio_tokens": NodeSpec("audio_tokens", "audio\ntokens", "learned", 298, 3.75, VIOLET, "modern"),
    "multimodal": NodeSpec("multimodal", "multimodal\ntools", "learned", 318, 3.85, VIOLET, "modern"),
    # Software / verification.
    "software_form": NodeSpec("software_form", "software as\nrepresentation", "software", 225, 1.35, GREEN, "software"),
    "expert": NodeSpec("expert", "expert\nsystems", "software", 212, 2.20, BLUE, "software"),
    "blackboard": NodeSpec("blackboard", "blackboard\narchitectures", "software", 222, 2.85, BLUE, "software"),
    "code_agents": NodeSpec("code_agents", "code\nagents", "software", 242, 2.60, CYAN, "software"),
    "research_agents": NodeSpec("research_agents", "research\nassistants", "software", 252, 3.25, CYAN, "software"),
    "proof_tools": NodeSpec("proof_tools", "proof\ntools", "software", 205, 3.15, GREEN, "software"),
    "vv": NodeSpec("vv", "V&V /\nevidence", "software", 230, 3.65, GREEN, "software"),
    "reliable": NodeSpec("reliable", "reliable\nworkflows", "software", 248, 4.10, GREEN, "software"),
    # Frontier shell.
    "self_compute": NodeSpec("self_compute", "self-inhabiting\ncompute", "frontier", 112, 4.95, FRONTIER, "frontier"),
    "experiment_loops": NodeSpec("experiment_loops", "autonomous\nexperiment loops", "frontier", 40, 4.95, GOLD, "frontier"),
    "world_models": NodeSpec("world_models", "discrete-event\nworld models", "frontier", 326, 4.95, FRONTIER, "frontier"),
    "closed_loop_rd": NodeSpec("closed_loop_rd", "closed-loop\nR&D", "frontier", 250, 4.95, GOLD, "frontier"),
    "orgs": NodeSpec("orgs", "transform-native\norganizations", "frontier", 175, 4.85, FRONTIER, "frontier"),
}


EDGES = [
    EdgeSpec("fourier", "frequency", CYAN),
    EdgeSpec("frequency", "signal_processing", CYAN),
    EdgeSpec("signal_processing", "wireless", CYAN),
    EdgeSpec("signal_processing", "compressed_audio", CYAN),
    EdgeSpec("signal_processing", "spectral_imaging", CYAN),
    EdgeSpec("dct", "jpeg", VIOLET),
    EdgeSpec("jpeg", "video_codecs", VIOLET),
    EdgeSpec("laplace", "transfer", GOLD),
    EdgeSpec("transfer", "stability", GOLD),
    EdgeSpec("stability", "feedback", GOLD),
    EdgeSpec("feedback", "motors", GOLD),
    EdgeSpec("feedback", "flight", GOLD),
    EdgeSpec("stability", "state_space", GOLD),
    EdgeSpec("neural_networks", "embeddings", VIOLET),
    EdgeSpec("embeddings", "transformers", VIOLET),
    EdgeSpec("transformers", "llms", VIOLET),
    EdgeSpec("llms", "contrastive", VIOLET),
    EdgeSpec("autoencoders", "neural_codecs", VIOLET),
    EdgeSpec("neural_codecs", "audio_tokens", VIOLET),
    EdgeSpec("audio_tokens", "multimodal", VIOLET),
    EdgeSpec("software_form", "code_agents", GREEN),
    EdgeSpec("expert", "blackboard", BLUE),
    EdgeSpec("blackboard", "vv", BLUE),
    EdgeSpec("proof_tools", "vv", GREEN),
    EdgeSpec("code_agents", "vv", GREEN),
    EdgeSpec("vv", "reliable", GREEN),
    EdgeSpec("reliable", "self_compute", FRONTIER),
    EdgeSpec("reliable", "experiment_loops", GOLD),
    EdgeSpec("experiment_loops", "world_models", GOLD),
    EdgeSpec("world_models", "closed_loop_rd", FRONTIER),
    EdgeSpec("reliable", "orgs", FRONTIER),
]


BRIDGES = [
    EdgeSpec("state_space", "neural_ssm", VIOLET, "bridge"),
    EdgeSpec("neural_ssm", "llms", VIOLET, "bridge"),
    EdgeSpec("llms", "code_agents", GOLD, "bridge"),
    EdgeSpec("code_agents", "vv", GREEN, "bridge"),
]


REVEAL_STATES = {
    "opening_glimpse": {
        "wedges": {"signal": 0.15, "dynamics": 0.12, "learned": 0.10, "software": 0.04},
        "nodes": {"fourier", "laplace", "dct"},
        "labels": set(),
        "bridges": set(),
        "fog": 0.92,
        "frontier": 0.02,
    },
    "classical_foundation": {
        "wedges": {"signal": 0.42, "dynamics": 0.42, "learned": 0.04, "software": 0.04},
        "nodes": {
            "fourier", "frequency", "signal_processing", "wireless", "compressed_audio",
            "spectral_imaging", "dct", "jpeg", "video_codecs", "laplace", "transfer",
            "stability", "feedback", "motors", "flight", "state_space",
        },
        "labels": {
            "fourier", "signal_processing", "wireless",
            "dct", "video_codecs", "laplace", "stability", "motors", "flight",
        },
        "bridges": set(),
        "fog": 0.58,
        "frontier": 0.04,
    },
    "modern_region": {
        "wedges": {"signal": 0.04, "dynamics": 0.08, "learned": 0.46, "software": 0.38},
        "nodes": {
            "neural_networks", "embeddings", "transformers", "llms", "contrastive",
            "autoencoders", "neural_codecs", "audio_tokens", "multimodal",
            "software_form", "code_agents", "research_agents", "vv",
        },
        "labels": {"embeddings", "transformers", "llms", "code_agents", "vv"},
        "bridges": {"llms->code_agents"},
        "fog": 0.46,
        "frontier": 0.03,
    },
    "convergence_pullback": {
        "wedges": {"signal": 0.10, "dynamics": 0.34, "learned": 0.44, "software": 0.40},
        "nodes": {
            "state_space", "neural_ssm", "llms", "code_agents", "vv", "reliable",
            "neural_networks", "embeddings", "transformers", "software_form",
            "research_agents",
        },
        "labels": {"state_space", "neural_ssm", "llms", "code_agents", "vv"},
        "bridges": {"state_space->neural_ssm", "neural_ssm->llms", "llms->code_agents", "code_agents->vv"},
        "fog": 0.44,
        "frontier": 0.14,
    },
    "final_reveal": {
        "wedges": {"signal": 0.38, "dynamics": 0.38, "learned": 0.40, "software": 0.38},
        "nodes": set(NODES),
        "labels": {
            "fourier", "laplace", "dct", "neural_ssm", "llms", "code_agents", "vv",
            "experiment_loops", "self_compute",
        },
        "bridges": {"state_space->neural_ssm", "neural_ssm->llms", "llms->code_agents", "code_agents->vv"},
        "fog": 0.20,
        "frontier": 0.26,
    },
}


STATE_CAMERA = {
    "opening_glimpse": {"center": (0.05, 0.08), "scale": 1.20},
    "classical_foundation": {"center": (-0.42, 0.62), "scale": 0.78},
    "modern_region": {"center": (0.34, -0.46), "scale": 0.82},
    "convergence_pullback": {"center": (0.32, -0.04), "scale": 1.02},
    "final_reveal": {"center": (0.0, 0.0), "scale": 1.28},
}


SECTION_TO_STATE = {
    "01_opening": "opening_glimpse",
    "02_the_classic_pattern": "classical_foundation",
    "03_the_new_thing": "modern_region",
    "04_word_vectors": "modern_region",
    "05_pseudocode_to_code": "modern_region",
    "06_multimodal_transforms": "modern_region",
    "07_the_loss": "modern_region",
    "08_why_this_changes_the_technology_tree": "convergence_pullback",
    "09_thinking_in_the_limit": "convergence_pullback",
    "10_validation_and_verification_become_the_work": "convergence_pullback",
    "11_self_inhabiting_compute": "convergence_pullback",
    "12_the_outer_loop_experiments": "convergence_pullback",
    "13_businesses_are_transform_pipelines": "convergence_pullback",
    "14_ending": "final_reveal",
}
