"""
One page a human can actually work from: gate status plus the model's opinions.

The gate produces a list of violations and Gemini produces a list of judgements,
and neither is useful on its own — the first says nothing about whether the video
is any good, and the second is 200 items long with no way to tell a systemic
problem from a one-off. This joins them and groups the second by theme, which is
what turns "228 findings" into "five things to fix".
"""
from __future__ import annotations

import argparse
import collections
import json
import re
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
VIDEO = HERE.parent

THEMES = [
    ("Shape grammar — the wrong shape for the artifact",
     r"shape grammar|document slice|drawn as (a )?(plain|simple|tall|wide)|"
     r"plain (vertical |tall )?rectangles?"),
    ("Colour grammar — a colour used for something it does not mean",
     r"gold \(|violet \(|cyan \(|red is reserved|colou?r grammar|reserved for"),
    ("Stale frame — the line changed but the picture did not",
     r"\bstale\b|unchanged from the previous|zero visual change|no visual change"),
    ("Dead space — the composition huddles in part of the stage",
     r"dead region|dead space|unbalanced|shoved|pushed entirely"),
    ("Full sentences on screen where an identifier belongs",
     r"full sentence|short identifiers"),
    ("Missed concrete detail the narration names",
     r"missed opportunity|explicitly (names|mentions|states|refers)"),
]


def parse_findings(report: Path) -> list[tuple[str, str, str]]:
    """(section, beat, text) for every bullet in the Gemini report."""
    out: list[tuple[str, str, str]] = []
    section = beat = ""
    for line in report.read_text().splitlines():
        if line.startswith("## "):
            section, beat = line[3:].strip(), ""
            continue
        m = re.match(r"\*{0,2}(?:Beat\s+)?(\d\d b\d\d)", line.strip())
        if m:
            beat = m.group(1)
            continue
        if re.match(r"\s*[-*]\s", line) and section:
            out.append((section, beat, re.sub(r"^\s*[-*]+\s*", "", line).strip()))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--gemini", type=Path,
                    default=VIDEO / "out" / "review" /
                    f"gemini_frame_review_{date.today().isoformat()}.md")
    ap.add_argument("--out", type=Path,
                    default=VIDEO / "out" / "review" / "REVIEW_NOTES.md")
    args = ap.parse_args()

    qa_dir = VIDEO / "scenes" / "out" / "qa"
    results = []
    for f in sorted(qa_dir.glob("*.result.json")):
        results.append(json.loads(f.read_text()))

    lines = [f"# Review notes — {date.today().isoformat()}", "",
             "## Gate", "",
             "| section | gate | violations | drift | line coverage |",
             "|---|---|---|---|---|"]
    for r in results:
        lines.append(f"| {r['scene']} | {'PASS' if r['ok'] else 'FAIL'} | "
                     f"{r['violations']} | {r['drift']:+.2f}s | {r['coverage']:.0%} |")

    outstanding = collections.Counter()
    detail: list[str] = []
    for f in sorted(qa_dir.glob("*.violations.json")):
        for v in json.loads(f.read_text()):
            outstanding[v["check"]] += 1
            detail.append(f"- `{v['scene']}` **{v['check']}** at {v['t']:.1f}s — {v['detail']}")
    lines += ["", "### Outstanding machine-detected violations", ""]
    if outstanding:
        for check, n in outstanding.most_common():
            lines.append(f"- **{check}** × {n}")
        lines += ["", "<details><summary>every one, with a timestamp</summary>", ""]
        lines += detail
        lines += ["", "</details>"]
    else:
        lines.append("None. Every section is clean.")

    if args.gemini.exists():
        findings = parse_findings(args.gemini)
        lines += ["", f"## Gemini frame review — {len(findings)} judgements", "",
                  "Grouped by theme. These are opinions, not defects: the gate had already",
                  "cleared everything it can see before these frames were sent. Beat codes",
                  "match the amber identifier in the top-left of the frame.", ""]
        claimed: set[int] = set()
        for title, pattern in THEMES:
            hits = [(i, f) for i, f in enumerate(findings)
                    if i not in claimed and re.search(pattern, f[2], re.I)]
            if not hits:
                continue
            claimed |= {i for i, _ in hits}
            lines += [f"### {title} — {len(hits)}", ""]
            by_section: dict[str, list[str]] = collections.defaultdict(list)
            for _, (sec, beat, text) in hits:
                by_section[sec].append(f"  - `{beat or '?'}` {text}")
            for sec in sorted(by_section, key=lambda s: s):
                lines.append(f"- **{sec}**")
                lines += by_section[sec][:8]
                if len(by_section[sec]) > 8:
                    lines.append(f"  - _...and {len(by_section[sec]) - 8} more_")
            lines.append("")
        rest = [f for i, f in enumerate(findings) if i not in claimed]
        lines += [f"### Everything else — {len(rest)}", "",
                  "<details><summary>ungrouped findings</summary>", ""]
        lines += [f"- `{b or '?'}` ({s}) {t}" for s, b, t in rest]
        lines += ["", "</details>", ""]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines) + "\n")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
