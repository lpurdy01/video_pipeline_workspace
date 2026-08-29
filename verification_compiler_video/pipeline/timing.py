"""
Narration-driven timing.

Every visual event in this video is anchored to a *line of the script*, not to a
hand-tuned `run_time`. The chain is:

    script line  ->  scratch TTS  ->  local STT with word timestamps
                 ->  fuzzy align script words to spoken words
                 ->  (start, end) for every line
                 ->  beats resolve their anchors against that table

The fuzzy step is what makes this survive editing. Video 1 matched anchor
phrases exactly, so rewording a line silently broke its cue and the fix was a
manual pass. Here a line still aligns after a rewrite, a filler word, or an STT
mishearing, because alignment is a diff over word sequences rather than a lookup.

When the real human take replaces the scratch TTS, the same alignment runs
against the human audio and every cue re-times itself. No scene edits.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import dataclass, asdict
from difflib import SequenceMatcher
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
VIDEO = Path(__file__).resolve().parents[1]
TTS_SCRIPT = REPO / "representation_transform_visuals" / "narration_pipeline" / "gemini_tts.py"
STT_SCRIPT = REPO / "representation_transform_visuals" / "narration_pipeline" / "transcribe_words.py"


@dataclass
class Line:
    index: int
    text: str
    start: float
    end: float
    confidence: float

    @property
    def duration(self) -> float:
        return self.end - self.start


def normalize(word: str) -> str:
    return re.sub(r"[^a-z0-9]", "", word.lower())


def script_lines(section_text: str) -> list[str]:
    """
    Narration lines, in speaking order.

    The script is written one thought per line separated by blank lines, so a
    paragraph is a line. Visual cues in [VISUAL: ...] brackets are not spoken and
    are dropped here — they are read separately by the storyboard.
    """
    # A section ends at the next top-level heading or horizontal rule. Without
    # this, the last section swallowed the Length Note appended to the script and
    # synthesised three extra minutes of narration nobody wrote.
    section_text = re.split(r"\n---\s*\n|\n## ", section_text)[0]
    body = re.sub(r"\[VISUAL:.*?\]", "", section_text, flags=re.S)
    out = []
    for block in body.split("\n\n"):
        text = " ".join(block.split())
        if not text or text.startswith("#"):
            continue
        out.append(text)
    return out


def synthesize(text: str, out_wav: Path, voice: str = "Kore", style: str | None = None) -> Path:
    """Scratch TTS for the whole section, one call, so prosody is continuous."""
    out_wav.parent.mkdir(parents=True, exist_ok=True)
    tmp = out_wav.with_suffix(".txt")
    tmp.write_text(text, encoding="utf-8")
    cmd = [sys.executable, str(TTS_SCRIPT), "--text-file", str(tmp), "--out", str(out_wav)]
    if style:
        cmd += ["--style", style]
    cmd += ["--voice", voice]
    subprocess.run(cmd, check=True, capture_output=True)
    tmp.unlink(missing_ok=True)
    return out_wav


def transcribe(audio: Path, out_json: Path, model: str = "small") -> Path:
    """Local STT. Human audio never leaves the machine; scratch TTS need not either."""
    out_json.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [sys.executable, str(STT_SCRIPT), "--audio", str(audio),
         "--out", str(out_json), "--model", model, "--device", "cpu"],
        check=True, capture_output=True,
    )
    return out_json


def align(lines: list[str], words_json: Path) -> list[Line]:
    """
    Fuzzy-align script lines to spoken words.

    Both sides are reduced to normalized word sequences and diffed. Matching
    blocks give exact anchors; the gaps between them are filled by proportional
    interpolation, so an unmatched line still lands in the right place instead of
    falling back to zero.
    """
    data = json.loads(Path(words_json).read_text())
    spoken = [w for w in data["words"] if normalize(w["word"])]
    spoken_norm = [normalize(w["word"]) for w in spoken]

    script_words: list[str] = []
    owner: list[int] = []           # which line each script word belongs to
    for i, line in enumerate(lines):
        for w in line.split():
            n = normalize(w)
            if n:
                script_words.append(n)
                owner.append(i)

    matcher = SequenceMatcher(None, script_words, spoken_norm, autojunk=False)
    # script word index -> spoken word index
    mapping: dict[int, int] = {}
    for a, b, size in matcher.get_matching_blocks():
        for k in range(size):
            mapping[a + k] = b + k

    total_audio = float(data.get("duration") or (spoken[-1]["end"] if spoken else 0.0))

    def time_for(idx: int, which: str) -> tuple[float, float]:
        """Time of script word `idx`, and how confident we are in it."""
        if idx in mapping:
            w = spoken[mapping[idx]]
            return float(w[which]), 1.0
        # interpolate between the nearest matched neighbours
        before = max((i for i in mapping if i < idx), default=None)
        after = min((i for i in mapping if i > idx), default=None)
        if before is None and after is None:
            frac = idx / max(len(script_words) - 1, 1)
            return frac * total_audio, 0.0
        if before is None:
            w = spoken[mapping[after]]
            return float(w["start"]), 0.35
        if after is None:
            w = spoken[mapping[before]]
            return float(w["end"]), 0.35
        wb, wa = spoken[mapping[before]], spoken[mapping[after]]
        span = after - before
        frac = (idx - before) / span if span else 0.0
        t = float(wb["end"]) + frac * (float(wa["start"]) - float(wb["end"]))
        return t, 0.5

    out: list[Line] = []
    for i, line in enumerate(lines):
        idxs = [k for k, o in enumerate(owner) if o == i]
        if not idxs:
            continue
        start, c1 = time_for(idxs[0], "start")
        end, c2 = time_for(idxs[-1], "end")
        if end <= start:
            end = start + 0.35
        out.append(Line(index=i, text=line, start=round(start, 3),
                        end=round(end, 3), confidence=round((c1 + c2) / 2, 2)))

    # Enforce monotonicity — a mis-alignment must never send a cue backwards.
    for a, b in zip(out, out[1:]):
        if b.start < a.start:
            b.start = a.start + 0.05
        if b.end <= b.start:
            b.end = b.start + 0.3
    return out


def resolve_anchor(anchor: str, lines: list[Line], min_ratio: float = 0.55) -> Line:
    """
    Find the line a beat is cued to, by fuzzy phrase match.

    A beat says `on("a chat transcript is not evidence")`. That phrase does not
    have to be an exact substring — it has to be the best match, well enough
    above the runner-up that the cue is unambiguous.
    """
    probe = " ".join(normalize(w) for w in anchor.split())
    scored = []
    for line in lines:
        hay = " ".join(normalize(w) for w in line.text.split())
        m = SequenceMatcher(None, probe, hay, autojunk=False)
        block = m.find_longest_match(0, len(probe), 0, len(hay))
        # Two scores, and the second one matters. "The question is" is the whole
        # of line 10 and also sits inside line 9 ("...the question is not whether
        # the answer sounds reasonable"). Both score 100% on "how much of the
        # anchor did I find", so the earlier line won on stable-sort order and
        # line 10 silently lost its beat. How much of the *line* the anchor
        # accounts for breaks the tie the way a reader would: an anchor that is
        # the entire line is the cue, not the same words buried in a longer one.
        scored.append((block.size / max(len(probe), 1),
                       block.size / max(len(hay), 1), line))
    scored.sort(key=lambda s: (-s[0], -s[1]))
    best_ratio, best_cover, best = scored[0]
    if len(scored) > 1:
        runner_ratio, runner_cover, runner = scored[1]
        if (abs(best_ratio - runner_ratio) < 0.02
                and abs(best_cover - runner_cover) < 0.05):
            raise LookupError(
                f"anchor {anchor!r} is ambiguous: it fits {best.text[:50]!r} and "
                f"{runner.text[:50]!r} equally well. Lengthen it so it can only "
                "mean one line."
            )
    if best_ratio < min_ratio:
        raise LookupError(
            f"anchor {anchor!r} matched no narration line above {min_ratio:.0%} "
            f"(best was {best_ratio:.0%}: {best.text[:60]!r}). "
            "Fix the anchor, or the script line moved."
        )
    return best


def build(section_id: str, section_text: str, out_dir: Path,
          audio: Path | None = None, model: str = "small") -> list[Line]:
    """
    Produce the timing table for one section.

    Pass `audio` to align against a real human take; omit it to synthesize
    scratch TTS first. Either way the output shape is identical, which is what
    lets the human take drop in without touching a scene.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    lines = script_lines(section_text)
    spoken_text = "\n\n".join(lines)

    if audio is None:
        audio = out_dir / f"{section_id}.scratch.wav"
        if not audio.exists():
            synthesize(spoken_text, audio)

    words = out_dir / f"{section_id}.words.json"
    if not words.exists():
        transcribe(audio, words, model=model)

    timed = align(lines, words)
    # The clip must run for the whole audio file, not just to the last spoken
    # word: a take normally has a little silence after it, and ending the visuals
    # early leaves a frozen frame under the tail.
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(audio)], capture_output=True, text=True, check=True)
    audio_duration = round(float(probe.stdout.strip()), 3)
    (out_dir / f"{section_id}.timing.json").write_text(
        json.dumps({"section": section_id, "audio": str(audio),
                    "audio_duration": audio_duration,
                    "lines": [asdict(l) for l in timed]}, indent=2) + "\n"
    )
    return timed


def load(section_id: str, out_dir: Path) -> list[Line]:
    data = json.loads((out_dir / f"{section_id}.timing.json").read_text())
    return [Line(**l) for l in data["lines"]]


def audio_duration(section_id: str, out_dir: Path) -> float | None:
    """Length of the narration file, including any silence after the last word."""
    data = json.loads((out_dir / f"{section_id}.timing.json").read_text())
    return data.get("audio_duration")
