"""Build SRT captions for "The Compiler For Trust" from the local timing tables.

Caption text comes from `drafts/script.md` as carried in `out/timing/*.timing.json`
(the locked script), not from ASR output, so terms like "Verification Query
Package" cannot be mangled. Times come from the local faster-whisper alignment
already used to time the animation.

Nothing here touches the cloud; the human audio never leaves the machine.

Section offsets are the cumulative *render* durations from
`out/final/assembly_report.json`. `pipeline/assemble.py` joins sections with
ffmpeg's concat demuxer and inserts no padding, so those offsets are exact.
"""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
VIDEO = HERE.parent

# Subtitle readability, not the on-screen caption rule (CAPTION_MIN_HOLD).
MIN_DUR = 1.4       # stretch a short cue up to here if the gap allows
MAX_DUR = 6.5
MAX_CHARS = 80      # across at most two lines, with slack for the wrap point
MAX_LINE = 42
MAX_GAP = 1.2       # a longer pause starts a new cue


def wrap(text: str) -> str:
    if len(text) <= MAX_LINE:
        return text
    # Minimise the longest of the two lines. Scoring on the balance alone meant a
    # line with no split under MAX_LINE fell through unwrapped.
    words, best, best_score = text.split(), None, None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        score = (max(len(a), len(b)), abs(len(a) - len(b)))
        if best_score is None or score < best_score:
            best, best_score = (a, b), score
    return "\n".join(best) if best else text


def split_long(start: float, end: float, text: str) -> list[tuple[float, float, str]]:
    """A single narration line can exceed both caps on its own. Split it at word
    boundaries into the fewest pieces that fit, sharing the time by character
    count so each piece stays under the spoken words it covers."""
    n = max(
        1,
        -(-len(text) // MAX_CHARS),            # ceil by characters
        -(-int((end - start) * 100) // int(MAX_DUR * 100)),  # ceil by duration
    )
    if n == 1:
        return [(start, end, wrap(text))]

    words = text.split()
    target = len(text) / n
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        if len(" ".join(cur)) >= target and len(chunks) < n - 1:
            chunks.append(" ".join(cur))
            cur = []
    if cur:
        chunks.append(" ".join(cur))

    total = sum(len(c) for c in chunks)
    out, t = [], start
    for i, chunk in enumerate(chunks):
        share = (end - start) * (len(chunk) / total)
        t_end = end if i == len(chunks) - 1 else t + share
        out.append((t, t_end, wrap(chunk)))
        t = t_end
    return out


def ts(t: float) -> str:
    if t < 0:
        t = 0.0
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def build_cues() -> list[tuple[float, float, str]]:
    report = json.loads((VIDEO / "out/final/assembly_report.json").read_text())
    cues: list[tuple[float, float, str]] = []
    offset = 0.0

    for entry in report:
        section = entry["section"]
        span = entry["render"]
        timing = json.loads((VIDEO / "out/timing" / f"{section}.timing.json").read_text())

        group: list[dict] = []

        def flush() -> None:
            if not group:
                return
            text = " ".join(l["text"].strip() for l in group)
            start = offset + group[0]["start"]
            end = offset + min(group[-1]["end"], span)
            cues.extend(split_long(start, max(end, start + 0.4), text))
            group.clear()

        for line in timing["lines"]:
            if group:
                gap = line["start"] - group[-1]["end"]
                merged = sum(len(l["text"]) + 1 for l in group) + len(line["text"])
                dur = line["end"] - group[0]["start"]
                if gap > MAX_GAP or merged > MAX_CHARS or dur > MAX_DUR:
                    flush()
            group.append(line)
        flush()
        offset += span

    # Stretch cues that are too brief to read, but never into the next cue.
    for i, (start, end, text) in enumerate(cues):
        if end - start >= MIN_DUR:
            continue
        limit = cues[i + 1][0] if i + 1 < len(cues) else end + MIN_DUR
        cues[i] = (start, min(start + MIN_DUR, limit), text)
    return cues


def write_srt(cues, path: Path, speed: float) -> None:
    out = []
    for i, (start, end, text) in enumerate(cues, 1):
        out.append(f"{i}\n{ts(start / speed)} --> {ts(end / speed)}\n{text}\n")
    path.write_text("\n".join(out), encoding="utf-8")


def main() -> None:
    cues = build_cues()
    for speed, name in ((1.0, "captions_en_1x.srt"), (1.15, "captions_en_1.15x.srt")):
        write_srt(cues, HERE / name, speed)
        print(f"{name}: {len(cues)} cues, ends {cues[-1][1] / speed:.1f}s")

    overlaps = sum(1 for a, b in zip(cues, cues[1:]) if a[1] > b[0] + 1e-6)
    longest = max(len(l) for _, _, t in cues for l in t.split("\n"))
    over_dur = sum(1 for s, e, _ in cues if e - s > MAX_DUR + 0.01)
    print(f"overlaps: {overlaps} | longest line: {longest} chars | cues over {MAX_DUR}s: {over_dur}")


if __name__ == "__main__":
    main()
