"""
Turn a local commentary transcript into structured review notes.

Input is the word-level JSON produced by the local faster-whisper pass. Nothing
here touches the network: raw voice, word timings, and this transcript all stay
on the machine, per the repo's human-audio policy.

The recording is a read-through with spoken interruptions. Two jobs:
  1. find the spoken markers (COMMENT / REWRITE / CUT / MOVE / KEEP / ALT HOOK);
  2. anchor each one to a script section, by matching the surrounding read-through
     against the script text.
"""
from __future__ import annotations

import argparse
import json
import re
from difflib import SequenceMatcher
from pathlib import Path

HERE = Path(__file__).resolve().parent
VIDEO = HERE.parent

MARKERS = ["COMMENT", "REWRITE", "CUT", "MOVE", "KEEP", "ALT HOOK"]
# Spoken forms drift from the written convention; accept the natural variants.
MARKER_PATTERNS = {
    "COMMENT": r"\bcomments?\b",
    "REWRITE": r"\bre-?writes?\b",
    "CUT": r"\bcuts?\b",
    "MOVE": r"\bmoves?\b",
    "KEEP": r"\bkeeps?\b",
    "ALT HOOK": r"\balt(?:ernate)?\s+hooks?\b",
}


def normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9 ]+", " ", text.lower()).strip()


def script_sections(script: Path) -> list[tuple[str, str]]:
    body = script.read_text(encoding="utf-8").split("## Full Narration Draft", 1)[1]
    out = []
    for block in re.split(r"\n### ", body)[1:]:
        heading, _, rest = block.partition("\n")
        out.append((heading.strip(), normalize(rest)))
    return out


def best_section(window: str, sections: list[tuple[str, str]]) -> tuple[str, float]:
    """Which script section does this stretch of read-through belong to?"""
    probe = normalize(window)
    if len(probe) < 25:
        return ("(unanchored)", 0.0)
    best, score = "(unanchored)", 0.0
    for heading, text in sections:
        ratio = SequenceMatcher(None, probe, text).find_longest_match(
            0, len(probe), 0, len(text)
        ).size / max(len(probe), 1)
        if ratio > score:
            best, score = heading, ratio
    return best, round(score, 3)


def find_markers(segments: list[dict]) -> list[dict]:
    hits = []
    for i, seg in enumerate(segments):
        text = seg["text"]
        for marker, pattern in MARKER_PATTERNS.items():
            m = re.search(pattern, text, re.I)
            if not m:
                continue
            # Only treat it as a marker if it opens a clause — "comment, this line
            # feels formal" — rather than appearing mid-sentence as an ordinary word.
            if m.start() > 24:
                continue
            body = [text[m.end():].lstrip(" ,.:;-")]
            for nxt in segments[i + 1: i + 5]:
                if any(re.search(p, nxt["text"][:24], re.I) for p in MARKER_PATTERNS.values()):
                    break
                body.append(nxt["text"])
            hits.append({
                "marker": marker,
                "start": seg["start"],
                "segment_index": i,
                "text": " ".join(b.strip() for b in body if b.strip()),
            })
            break
    return hits


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--words", type=Path, required=True)
    ap.add_argument("--script", type=Path, default=VIDEO / "drafts" / "script.md")
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    data = json.loads(args.words.read_text())
    segments = data["segments"]
    sections = script_sections(args.script)

    # A readable plain transcript is useful on its own.
    plain = args.out.with_suffix(".transcript.txt")
    plain.write_text(
        "\n".join(f"[{s['start']:7.1f}]  {s['text']}" for s in segments),
        encoding="utf-8",
    )

    hits = find_markers(segments)
    for hit in hits:
        i = hit["segment_index"]
        window = " ".join(s["text"] for s in segments[max(0, i - 6): i])
        hit["section"], hit["confidence"] = best_section(window, sections)

    lines = [
        "# Review notes — first-pass commentary",
        "",
        f"Source: `{data['audio']}` ({data['duration'] / 60:.1f} min, "
        f"transcribed locally with whisper `{data['model']}`)",
        "",
        f"Markers found: {len(hits)}",
        "",
        "Section anchoring is a text match against the read-through preceding each",
        "marker; low confidence means the marker was spoken away from script text.",
        "",
    ]
    for n, hit in enumerate(hits, 1):
        mm, ss = divmod(int(hit["start"]), 60)
        lines += [
            f"## Comment {n}",
            "",
            f"Section: {hit['section']}  (match {hit['confidence']})",
            f"Marker: {hit['marker']}",
            f"Timestamp: {mm:d}:{ss:02d}",
            f"Transcript excerpt: {hit['text']}",
            "Interpretation: ",
            "Suggested edit: ",
            "Status: open",
            "",
        ]
    args.out.write_text("\n".join(lines), encoding="utf-8")
    print(f"transcript -> {plain}")
    print(f"review notes -> {args.out}  ({len(hits)} markers)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
