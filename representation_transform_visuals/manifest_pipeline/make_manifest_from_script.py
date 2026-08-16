from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
SCRIPT = ROOT / "drafts" / "script.md"
MANIFEST = ROOT / "production_manifest.json"


VISUAL_CLASS_BY_SECTION = {
    1: "S01TransformCivilization",
    2: "S02PatternPipeline",
    3: "S03LanguageVectors",
    4: "S03bWordVectorAnalogy",
    5: "S05CodeAndLoss",
    6: "S05bMultimodalAnalogy",
    7: "S05CodeAndLoss",
    8: "S06cGameTechTree3D",
    9: "S09LimitTrends",
    10: "S10ValidationVerification",
    11: "S11SelfInhabitingCompute",
    12: "S12OuterExperimentLoop",
    13: "S13BusinessPipelines",
    14: "S14EndingTechTreeZoomOut",
}


PROMPT_BY_SECTION = {
    1: "Opening transform-history composition: signals, Laplace/control, DCT/image compression, and first technology-tree growth.",
    2: "Concrete transform pipeline: representation in, transform space, computation, representation out.",
    3: "Language enters the pattern: tokens become vectors in a dark high-dimensional computational space.",
    4: "Word vectors: king-man+woman≈queen plus a simple semantic-search idea.",
    5: "Pseudocode to code as lossy transform: intent becomes code and hidden assumptions become executable.",
    6: "Multimodal bridge: text encoder, shared representation space, image decoder.",
    7: "Semantic transform loss: preservation, invention, and loss; missing context becomes executable assumptions.",
    8: "3D strategy-game-like technology tree showing classical and learned-transform unlocks.",
    9: "Thinking in the limit method: accuracy up, complexity up, generation cost down.",
    10: "Validation and verification become the work: artifact abundance flows into evidence gate.",
    11: "Self-inhabiting compute: runtime state enters transform, executable behavior runs, telemetry feeds back.",
    12: "Outer experiment loop: hypothesis to procedure to measurement to evidence to updated representation.",
    13: "Business as transform pipeline: intent to strategy to design to tickets to code to product, with compressed handoffs.",
    14: "Final zoom out on the technology tree as new branches light up.",
}


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_")
    return slug[:44].strip("_")


def parse_script() -> list[dict]:
    text = SCRIPT.read_text(encoding="utf-8")
    match = re.search(r"## Draft Narration\n(?P<body>.*?)(?:\n## Citation Notes|\Z)", text, re.S)
    if not match:
        raise SystemExit("Could not find Draft Narration section.")
    body = match.group("body")
    section_re = re.compile(r"^### (?P<num>\d+)\. (?P<title>.+?)\n(?P<body>.*?)(?=^### \d+\. |\Z)", re.M | re.S)
    sections = []
    for m in section_re.finditer(body):
        num = int(m.group("num"))
        title = m.group("title").strip()
        narration = m.group("body").strip()
        section_id = f"{num:02d}_{slugify(title)}"
        visual_class = VISUAL_CLASS_BY_SECTION.get(num)
        if not visual_class:
            raise SystemExit(f"No visual mapping for section {num}: {title}")
        sections.append(
            {
                "id": section_id,
                "title": title,
                "type": "manim_or_placeholder",
                "narration_text": narration,
                "audio": {
                    "human_path": f"representation_transform_visuals/assets/human_audio/{section_id}.wav",
                    "scratch_path": f"representation_transform_visuals/manifest_pipeline/out/audio/{section_id}.wav",
                },
                "visual": {
                    "kind": "existing_video",
                    "path": f"representation_transform_visuals/prototype_pipeline/out/manim_media/videos/storyboard_sections/480p15/{visual_class}.mp4",
                    "fallback_kind": "visual_placeholder",
                    "prompt": PROMPT_BY_SECTION.get(num, title),
                },
                "review_keyframes": ["start", "middle", "end"],
                "human_assets": [
                    {
                        "kind": "human_narration",
                        "path": f"representation_transform_visuals/assets/human_audio/{section_id}.wav",
                        "prompt": f"Record section {num}: {title}.",
                    }
                ],
            }
        )
    return sections


def main() -> None:
    manifest = {
        "project": "representation_transform_visuals",
        "title": "The New Transform Space",
        "version": "prototype-manifest-003-script-v2",
        "prototype_defaults": {
            "width": 854,
            "height": 480,
            "fps": 24,
            "scratch_tts_model": "gemini-3.1-flash-tts-preview",
            "scratch_tts_voice": "Kore",
            "scratch_tts_style": (
                "Read this clearly and naturally, like a thoughtful technical YouTube narrator. "
                "Keep the pace calm, curious, and slightly bold."
            ),
        },
        "notes": [
            "Generated from drafts/script.md by manifest_pipeline/make_manifest_from_script.py.",
            "Human audio remains local by default. Scratch TTS may use approved script text.",
            "Use image_review_pipeline with --model auto for generated visual review.",
        ],
        "sections": parse_script(),
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(MANIFEST)


if __name__ == "__main__":
    main()
