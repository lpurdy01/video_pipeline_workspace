#!/usr/bin/env python3
"""Build a YouTube .srt from the local word alignments.

Word times are section-relative; offset each by the section start, then divide
by the export speed (the final cut is 1.2x). Group words into readable cues
(break on sentence punctuation / pauses / length).
"""
import json
import re
from pathlib import Path

OUT = Path(__file__).resolve().parent / "out"
ALIGN = OUT / "alignments"
SPEED = 1.2
MAX_LINE = 42          # chars per line
MAX_CUE_CHARS = 70     # keep a cue within 2 lines after word wrapping
MAX_CUE_SECS = 5.5     # in final (sped) seconds
GAP_BREAK = 0.55       # pause (sped secs) that forces a new cue

# High-confidence ASR fixes for this script (whisper mis-hears these). The user
# should still proofread the file before publishing.
WORD_FIXES = {"foyer": "Fourier"}
TEXT_FIXES = [("PTX -like", "PTX-like")]


def fmt(t):
    if t < 0:
        t = 0
    h = int(t // 3600); m = int((t % 3600) // 60); s = int(t % 60); ms = int(round((t - int(t)) * 1000))
    if ms == 1000:
        s += 1; ms = 0
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def wrap(text):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > MAX_LINE:
            lines.append(cur); cur = w
        else:
            cur = f"{cur} {w}".strip()
        if len(lines) == 1 and len(cur) > MAX_LINE:  # safety
            lines.append(cur); cur = ""
    if cur:
        lines.append(cur)
    return "\n".join(lines[:2])


def main():
    manifest = json.loads((OUT / "resolved_manifest.json").read_text())
    sections = manifest["sections"]

    # Build a flat list of words with absolute (sped) start/end.
    words = []
    for s in sections:
        sid, start = s["id"], s["start_seconds"]
        path = ALIGN / f"{sid}.json"
        if not path.exists():
            continue
        for w in json.loads(path.read_text()).get("words", []):
            tok = (w.get("word") or "").strip()
            if not tok:
                continue
            tok = WORD_FIXES.get(tok.lower(), tok)
            words.append({
                "t": (start + float(w["start"])) / SPEED,
                "e": (start + float(w.get("end", w["start"]))) / SPEED,
                "w": tok,
            })

    # Group into cues.
    cues = []
    cur = []
    for i, w in enumerate(words):
        cur.append(w)
        text = " ".join(x["w"] for x in cur)
        dur = cur[-1]["e"] - cur[0]["t"]
        ends_sentence = bool(re.search(r"[.?!]\"?$", w["w"])) and len(cur) >= 3
        nxt_gap = (words[i + 1]["t"] - w["e"]) if i + 1 < len(words) else 99
        if (ends_sentence or len(text) >= MAX_CUE_CHARS or dur >= MAX_CUE_SECS
                or nxt_gap >= GAP_BREAK):
            cues.append(cur); cur = []
    if cur:
        cues.append(cur)

    # Emit, clamping each cue to end before the next starts.
    out = []
    for idx, cue in enumerate(cues, 1):
        start = cue[0]["t"]
        end = cue[-1]["e"]
        if idx < len(cues):
            nxt = cues[idx][0]["t"]
            end = min(end, nxt - 0.05)
        if end - start < 0.7:
            end = start + 0.7
        text = wrap(" ".join(x["w"] for x in cue))
        out.append(f"{idx}\n{fmt(start)} --> {fmt(end)}\n{text}\n")

    srt = "\n".join(out)
    for a, b in TEXT_FIXES:
        srt = srt.replace(a, b)
    dest = OUT / "launch_assets" / "captions_en_1.2x.srt"
    dest.parent.mkdir(exist_ok=True)
    dest.write_text(srt, encoding="utf-8")
    print(f"wrote {dest} ({len(cues)} cues, last end {fmt(cues[-1][-1]['e'])})")


if __name__ == "__main__":
    main()
