#!/usr/bin/env python3
"""Run PDF conversion followed by a source-fidelity review packet.

This is the non-device portion of the end-to-end loop. Follow it with
crosspoint_simulator.py prepare/build/capture, then re-run agentic_review.py
with simulator screenshots added by the forthcoming visual-review adapter.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from pdf_to_crosspoint_epub import safe_stem


HERE = Path(__file__).resolve().parent


def run(args: list[str]) -> None:
    completed = subprocess.run(args, check=False)
    if completed.returncode:
        raise RuntimeError(f"stage failed ({completed.returncode}): {' '.join(args[:2])}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("out/crosspoint_review"))
    parser.add_argument("--title")
    parser.add_argument("--author")
    parser.add_argument("--language", default="en")
    parser.add_argument("--stem")
    parser.add_argument("--model-review", action="store_true")
    parser.add_argument("--allow-cloud-content", action="store_true")
    parser.add_argument("--max-model-pages", type=int, default=8)
    args = parser.parse_args()
    if args.model_review and not args.allow_cloud_content:
        parser.error("--model-review requires --allow-cloud-content")
    output = args.output_dir.resolve()
    stem = safe_stem(args.stem or args.pdf.stem)
    convert = [sys.executable, str(HERE / "pdf_to_crosspoint_epub.py"), str(args.pdf), "--output-dir", str(output), "--overwrite", "--language", args.language]
    if args.title:
        convert += ["--title", args.title]
    if args.author:
        convert += ["--author", args.author]
    if args.stem:
        convert += ["--stem", args.stem]
    try:
        run(convert)
        review = [sys.executable, str(HERE / "agentic_review.py"), str(args.pdf), str(output / f"{stem}-review.manifest.json"), "--output-dir", str(output / f"{stem}-agentic-review")]
        if args.model_review:
            review += ["--model-review", "--allow-cloud-content", "--max-model-pages", str(args.max_model_pages)]
        run(review)
    except RuntimeError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print("Next simulator step:")
    print(f"  {sys.executable} {HERE / 'crosspoint_simulator.py'} prepare {output / f'{stem}-review.epub'} --write-config")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

