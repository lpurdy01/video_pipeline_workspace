"""
Render a polished whitepaper diagram from a matplotlib wireframe PNG + spec.

Usage:
    python3 whitepaper/gemini_tools/diagram_render.py \
        --wireframe whitepaper/diagram1_artifact_graph.png \
        --spec "Artifact graph: three zones (Requirements blue, Code Units purple, \
                Verification Evidence green) linked by typed edges..." \
        --out whitepaper/diagram1_rendered.png \
        [--model gemini-3-pro-image]

The wireframe is sent as a visual reference. The spec drives content and layout intent.
The model generates a cleaner, publication-quality diagram and writes it as a PNG.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from gemini_client import generate_image, image_part

DEFAULT_MODEL = "models/gemini-3-pro-image"

SYSTEM_PROMPT = """You are producing a clean, publication-quality technical diagram for a \
whitepaper about a software verification system called the Verification Compiler.

Style requirements:
- White or very light gray background (suitable for print / PDF embedding).
- Clear zone boundaries — use light filled rectangles with distinct colors per zone.
- Readable sans-serif labels, minimum 11pt equivalent, no overlapping text.
- Typed arrows with arrowheads: solid for primary relationships, dashed for references.
- Include a compact legend if more than two edge types are used.
- No decorative gradients or shadows — clean technical illustration style.
- Aspect ratio 4:3 or 16:9, minimum 1200×900 px output.

Use the wireframe image as a layout and content reference. Improve composition, \
readability, and visual hierarchy. Output ONLY the diagram — no surrounding text."""


def render(wireframe: Path, spec: str, out: Path, model: str) -> None:
    parts = [
        {"text": SYSTEM_PROMPT},
        {"text": f"Diagram specification:\n{spec}"},
        {"text": "Wireframe reference (use as layout guide):"},
        image_part(wireframe),
        {"text": "Generate the polished diagram now."},
    ]
    image_bytes = generate_image(model, parts)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(image_bytes)
    print(f"Saved: {out}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a polished diagram from wireframe + spec via Gemini.")
    parser.add_argument("--wireframe", type=Path, required=True, help="Matplotlib wireframe PNG.")
    parser.add_argument("--spec", type=str, default="", help="Text spec describing diagram content and intent.")
    parser.add_argument("--spec-file", type=Path, help="Read spec from a text file instead of --spec.")
    parser.add_argument("--out", type=Path, required=True, help="Output PNG path.")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    args = parser.parse_args()

    if not args.wireframe.exists():
        raise SystemExit(f"Wireframe not found: {args.wireframe}")
    spec = args.spec_file.read_text(encoding="utf-8") if args.spec_file else args.spec
    render(args.wireframe, spec, args.out, args.model)


if __name__ == "__main__":
    main()
