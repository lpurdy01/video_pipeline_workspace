"""Generate exploratory tech-tree concept images with Gemini.

This sends text prompts only and writes generated images under agent_tools/out/.
Do not use this for human audio or timing-rich human narration artifacts.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "whitepaper" / "gemini_tools"))

from gemini_client import generate_image, image_part  # noqa: E402


DEFAULT_MODEL = "models/gemini-3-pro-image"
DEFAULT_PROMPTS = REPO / "representation_transform_visuals" / "drafts" / "tech_tree_concept_prompts.md"
DEFAULT_OUT = REPO / "representation_transform_visuals" / "agent_tools" / "out" / "tech_tree_concepts"


def image_extension(image_bytes: bytes) -> str:
    if image_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
        return ".png"
    if image_bytes.startswith(b"\xff\xd8\xff"):
        return ".jpg"
    return ".img"


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_")
    return slug or "concept"


def parse_prompts(path: Path) -> list[tuple[str, str]]:
    text = path.read_text(encoding="utf-8")
    shared_match = re.search(r"^## Shared Context\n(?P<body>.*?)(?=^## Prompt 1:)", text, re.M | re.S)
    if not shared_match:
        raise SystemExit(f"Could not find Shared Context in {path}")
    shared = shared_match.group("body").strip()

    sections = re.findall(r"^## Prompt \d+: (?P<title>.+?)\n(?P<body>.*?)(?=^## Prompt \d+:|\Z)", text, re.M | re.S)
    if not sections:
        raise SystemExit(f"No prompt sections found in {path}")

    prompts: list[tuple[str, str]] = []
    for title, body in sections:
        full_prompt = (
            shared
            + "\n\n"
            + body.strip()
            + "\n\nOutput requirements: one polished concept-art image, 16:9 landscape, "
            + "no paragraph text, no dense tiny labels, no logos, no watermark. "
            + "Prioritize layout insight for a future Manim implementation."
        )
        prompts.append((title.strip(), full_prompt))
    return prompts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--prompts", type=Path, default=DEFAULT_PROMPTS)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--only", type=int, help="Generate only one prompt by number.")
    parser.add_argument("--reference-image", action="append", type=Path, default=[],
                        help="Generated visual reference image to include. Repeatable.")
    args = parser.parse_args()

    prompts = parse_prompts(args.prompts)
    if args.only:
        if args.only < 1 or args.only > len(prompts):
            raise SystemExit(f"--only must be between 1 and {len(prompts)} for {args.prompts}")
        prompts = [prompts[args.only - 1]]

    args.out_dir.mkdir(parents=True, exist_ok=True)
    for index, (title, prompt) in enumerate(prompts, start=1):
        stem = f"{index:02d}_{slugify(title)}"
        prompt_path = args.out_dir / f"{stem}.prompt.txt"
        prompt_path.write_text(prompt + "\n", encoding="utf-8")
        parts = [{"text": prompt}]
        for reference in args.reference_image:
            if not reference.exists():
                raise SystemExit(f"Missing reference image: {reference}")
            parts.append(image_part(reference))
        image_bytes = generate_image(args.model, parts, timeout=300)
        image_path = args.out_dir / f"{stem}{image_extension(image_bytes)}"
        image_path.write_bytes(image_bytes)
        print(image_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
