"""
Ask Gemini a focused question about one or more frames.

Designed for use by an assistant to avoid loading PNGs into its own
context. Instead of `Read`-ing a frame, run:

    python3 agent_tools/ask_gemini_about_frame.py \
        --frame manifest_pipeline/out/review_frames/frame_05.png \
        --question "Is the H(s) glow visible? Is it positioned right of x_dot = Ax + Bu?"

The answer is short (text only) and gets printed to stdout for the assistant
to read.

Multiple frames may be passed; they're labeled "Frame 1", "Frame 2", ... in
the prompt to Gemini.

Optional context snippets (e.g. narration excerpt, section ID) can be passed
via --context-file or --context.

Model defaults to gemini-3.1-pro-preview (strongest vision reasoner currently
available). Override with --model.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "whitepaper" / "gemini_tools"))

from gemini_client import generate_content, image_part  # noqa: E402


DEFAULT_MODEL = "models/gemini-3.1-pro-preview"


def build_parts(question: str, frames: list[Path], context: str) -> list[dict]:
    preface = (
        "You are reviewing one or more keyframes from a technical YouTube animation. "
        "Answer the user's question directly and concisely. If they ask a yes/no "
        "question, lead with yes or no. Cite specific frames by their label if "
        "multiple are present."
    )
    parts: list[dict] = [{"text": preface}]
    if context:
        parts.append({"text": f"Context:\n{context}"})
    parts.append({"text": f"Question:\n{question}"})
    for idx, frame in enumerate(frames, start=1):
        parts.append({"text": f"Frame {idx}: {frame.name}"})
        parts.append(image_part(frame))
    return parts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frame", action="append", default=[], type=Path,
                        help="Path to a PNG frame. Repeat for multiple frames.")
    parser.add_argument("--question", required=True, help="Focused question for Gemini.")
    parser.add_argument("--context", default="", help="Inline context string.")
    parser.add_argument("--context-file", type=Path, help="Read context from file.")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help=f"Gemini model id (default: {DEFAULT_MODEL}).")
    args = parser.parse_args()

    if not args.frame:
        print("No frames provided. Use --frame <path> at least once.", file=sys.stderr)
        return 2

    missing = [f for f in args.frame if not f.exists()]
    if missing:
        print(f"Missing frame files: {', '.join(str(m) for m in missing)}", file=sys.stderr)
        return 2

    context = args.context
    if args.context_file and args.context_file.exists():
        context = (context + "\n" + args.context_file.read_text(encoding="utf-8")).strip()

    parts = build_parts(args.question, args.frame, context)
    answer = generate_content(args.model, parts, timeout=300)
    print(answer.strip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
