from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from narration_align import find_phrase_match


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ALIGN_DIR = ROOT / "manifest_pipeline" / "out" / "alignments"
DEFAULT_ANCHORS = ROOT / "narration_pipeline" / "anchor_phrases.json"


def load_anchors(path: Path | None) -> dict[str, list[str | list[str]]]:
    if path is None:
        path = DEFAULT_ANCHORS
    data = json.loads(path.read_text(encoding="utf-8"))
    return {str(section): list(phrases) for section, phrases in data.items()}


def main() -> int:
    parser = argparse.ArgumentParser(description="Check that phrase anchors exist in local alignment JSON.")
    parser.add_argument("--anchors", type=Path, help="Optional JSON mapping section_id -> list of phrases.")
    parser.add_argument("--align-dir", type=Path, default=DEFAULT_ALIGN_DIR)
    parser.add_argument("--no-fuzzy", action="store_true")
    parser.add_argument("--min-score", type=float, default=0.74)
    args = parser.parse_args()

    missing: list[tuple[str, str]] = []
    for section_id, phrases in load_anchors(args.anchors).items():
        print(section_id)
        for phrase in phrases:
            variants = phrase if isinstance(phrase, list) else [phrase]
            match = find_phrase_match(
                section_id,
                variants,
                align_dir=args.align_dir,
                fuzzy=not args.no_fuzzy,
                min_score=args.min_score,
            )
            if match is None:
                print(f"  MISSING  {phrase}")
                missing.append((section_id, " / ".join(variants)))
            else:
                detail = f"{match['method']} score={match['score']:.2f}"
                if match["method"] == "fuzzy":
                    detail += f" matched={match['matched_text']!r}"
                print(f"  {match['start']:7.2f}s  {variants[0]}  ({detail})")
    if missing:
        print("\nMissing phrase anchors:", file=sys.stderr)
        for section_id, phrase in missing:
            print(f"- {section_id}: {phrase}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
