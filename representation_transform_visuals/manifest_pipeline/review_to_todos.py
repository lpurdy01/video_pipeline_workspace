from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "manifest_pipeline" / "out"


FRAME_HEADER = re.compile(r"^### Frame\s+(\d+):\s*(.+?)\s*$", re.MULTILINE)


def split_frame_sections(review: str) -> dict[int, str]:
    matches = list(FRAME_HEADER.finditer(review))
    sections: dict[int, str] = {}
    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else review.find("## Highest Priority Fixes", start)
        if end == -1:
            end = len(review)
        sections[int(match.group(1))] = review[start:end].strip()
    return sections


def extract_named_block(text: str, labels: list[str]) -> list[str]:
    marker = ""
    start = -1
    for label in labels:
        marker = f"**{label}:**"
        start = text.find(marker)
        if start != -1:
            break
    if start == -1:
        return []
    body = text[start + len(marker) :]
    next_numbered = re.search(r"\n\d+\.\s+\*\*", body)
    if next_numbered:
        body = body[: next_numbered.start()]
    next_heading = re.search(r"\n###|\n##", body)
    if next_heading:
        body = body[: next_heading.start()]
    lines = []
    for raw in body.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("*"):
            line = "- " + line.lstrip("*").strip()
        lines.append(line)
    return lines


def extract_highest_priority(review: str) -> str:
    marker = "## Highest Priority Fixes"
    start = review.find(marker)
    if start == -1:
        return ""
    return review[start + len(marker) :].strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert Gemini manifest visual review into section-level TODOs.")
    parser.add_argument("--review", type=Path, default=OUT / "manifest_visual_review.md")
    parser.add_argument("--frames", type=Path, default=OUT / "review_frames" / "frames_manifest.json")
    parser.add_argument("--out", type=Path, default=OUT / "manifest_visual_todos.md")
    args = parser.parse_args()

    review = args.review.read_text(encoding="utf-8")
    frames = json.loads(args.frames.read_text(encoding="utf-8"))
    frame_sections = split_frame_sections(review)
    by_section: dict[str, list[tuple[dict, list[str], list[str]]]] = defaultdict(list)

    for idx, frame in enumerate(frames, start=1):
        text = frame_sections.get(idx, "")
        issues = extract_named_block(text, ["Concrete Visual Issues", "Visual Issues"])
        fixes = extract_named_block(text, ["Manim Fixes", "Suggest specific fixes for the Manim scene"])
        by_section[frame["section_id"]].append((frame, issues, fixes))

    lines = [
        "# Manifest Visual TODOs",
        "",
        f"Source review: `{args.review}`",
        f"Frame manifest: `{args.frames}`",
        "",
        "This file is generated from Gemini's keyframe review. It is a working repair list, not final creative direction.",
        "",
        "## Highest Priority",
        "",
    ]
    priority = extract_highest_priority(review)
    if priority:
        lines.append(priority)
    else:
        lines.append("- No highest-priority section found in review.")
    lines.append("")

    lines.append("## Section TODOs")
    lines.append("")
    for section_id, items in by_section.items():
        title = items[0][0]["title"]
        lines.append(f"### {section_id} - {title}")
        lines.append("")
        for frame, issues, fixes in items:
            cue = frame["cue"]
            timestamp = frame["timestamp_seconds"]
            path = frame["path"]
            lines.append(f"Frame cue `{cue}` at `{timestamp:.2f}s`: `{path}`")
            if issues:
                lines.append("")
                lines.append("Issues:")
                lines.extend(issues)
            if fixes:
                lines.append("")
                lines.append("Suggested fixes:")
                lines.extend(fixes)
            lines.append("")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines), encoding="utf-8")
    print(args.out)


if __name__ == "__main__":
    main()
