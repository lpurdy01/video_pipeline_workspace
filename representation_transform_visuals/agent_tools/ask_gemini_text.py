"""Ask Gemini a text-only planning, critique, or rewrite question.

This helper is intentionally narrow: it sends text artifacts only. Do not pass
raw human audio, human voice timing JSON, or private biometric voice material.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "whitepaper" / "gemini_tools"))

from gemini_client import generate_content, generate_thinking  # noqa: E402


DEFAULT_MODEL = "models/gemini-3.1-pro-preview"


def read_context(paths: list[Path]) -> str:
    chunks: list[str] = []
    for path in paths:
        if not path.exists():
            raise SystemExit(f"Missing context file: {path}")
        chunks.append(f"--- {path.as_posix()} ---\n{path.read_text(encoding='utf-8')}")
    return "\n\n".join(chunks)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompt", default="", help="Inline question or task for Gemini.")
    parser.add_argument("--prompt-file", type=Path, help="Read the prompt from a text file.")
    parser.add_argument("--context-file", action="append", type=Path, default=[],
                        help="Text artifact to include as context. Repeatable.")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--thinking", action="store_true",
                        help="Use the SDK thinking path for complex reasoning.")
    parser.add_argument("--thinking-level", default="HIGH", choices=["LOW", "MEDIUM", "HIGH"])
    parser.add_argument("--out", type=Path, help="Optional output markdown/text file.")
    args = parser.parse_args()

    prompt = args.prompt
    if args.prompt_file:
        if not args.prompt_file.exists():
            raise SystemExit(f"Missing prompt file: {args.prompt_file}")
        prompt = args.prompt_file.read_text(encoding="utf-8")
    if not prompt.strip():
        raise SystemExit("Provide --prompt or --prompt-file.")

    context = read_context(args.context_file)
    full_prompt = prompt.strip()
    if context:
        full_prompt += "\n\nContext files:\n\n" + context

    if args.thinking:
        answer = generate_thinking(full_prompt, model=args.model, thinking_level=args.thinking_level)
    else:
        answer = generate_content(args.model, [{"text": full_prompt}], timeout=300)

    answer = answer.strip()
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(answer + "\n", encoding="utf-8")
        print(args.out)
    else:
        print(answer)
    return 0


if __name__ == "__main__":
    sys.exit(main())
