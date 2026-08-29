"""
Rank the model's findings so a human decides on twenty, not two hundred.

The first Gemini pass returned 228 judgements in free prose. That is a research
result, not a work queue: there is no way to tell the frame that contradicts its
own narration from the one whose spacing could be nicer, and no way to see that
the same complaint lands on nine consecutive beats.

Ranking is by four things, in order of how much they should move a decision:

  1. Severity, as the model called it.
  2. Whether the gate independently flagged the same beat. Two unrelated methods
     agreeing is the strongest signal available here.
  3. How many beats share the finding's category — a defect that repeats is a
     rule that needs changing, not nine separate fixes.
  4. How early it appears. A bad frame in the cold open costs more viewers than
     a bad frame at minute twelve.

Every ranked finding carries the frame it is about, so the decision is made
against the picture rather than against a sentence describing it.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import subprocess
from dataclasses import dataclass, asdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
VIDEO = HERE.parent
QA = VIDEO / "scenes" / "out" / "qa"

SEVERITY_WEIGHT = {"BLOCKING": 100.0, "WORTH-FIX": 45.0, "POLISH": 12.0}
GATE_AGREES_BONUS = 35.0
EARLY_WEIGHT = 18.0          # full value at the very start, 0 at the end

# A finding that repeats across many beats is one decision, not many. Ranking it
# by count put twenty phrasings of "this shape should be a document slice" in a
# top twenty that is supposed to be twenty *choices* — so repetition promotes the
# theme and demotes each individual instance of it.
RECURRING_AT = 8             # this many sharing a signature makes it systemic
RECURRING_PENALTY = 0.45     # individual instances of a systemic theme
PER_SECTION_CATEGORY_CAP = 2 # at most this many alike in the ranked list

# Words that identify what a finding is *about*, so two notes on the same
# underlying rule cluster together instead of counting twice.
TOPIC_WORDS = [
    "shape grammar", "document slice", "hexagon", "diamond", "rounded", "square",
    "circle", "packet", "colour", "color", "gold", "violet", "cyan", "green",
    "red", "stale", "dead", "unbalanced", "full sentence", "off-centre",
    "too small", "unreadable", "overlap", "crowd",
]

LINE = re.compile(
    r"^\s*\**\s*(?P<beat>\d\d\s+b\d\d)\s*\|\s*(?P<sev>BLOCKING|WORTH-FIX|POLISH)"
    r"\s*\|\s*(?P<cat>MISMATCH|COMPOSITION|LEGIBILITY|MISSED)\s*\|\s*(?P<text>.+?)\s*$",
    re.I)


@dataclass
class Finding:
    beat: str
    severity: str
    category: str
    text: str
    section: str = ""
    scene: str = ""
    t: float = 0.0
    line: str = ""
    gate_checks: tuple = ()
    score: float = 0.0
    shot: str = ""


def parse(report: Path) -> list[Finding]:
    out = []
    for raw in report.read_text().splitlines():
        m = LINE.match(raw)
        if not m:
            continue
        out.append(Finding(beat=" ".join(m.group("beat").split()).upper().replace("B", "b"),
                           severity=m.group("sev").upper(),
                           category=m.group("cat").upper(),
                           text=m.group("text")))
    return out


SECTIONS = {
    "01": ("S01GenerationGotCheap", "s01_generation_got_cheap"),
    "02": ("S02ChatLogFallacy", "s02_chat_log_fallacy"),
    "03": ("S03TraceabilityShape", "s03_traceability_shape"),
    "04": ("S04ArtifactGraph", "s04_artifact_graph"),
    "05": ("S05CompilationTraversal", "s05_compilation_traversal"),
    "06": ("S06VQP", "s06_vqp"),
    "07": ("S07DualModeReview", "s07_dual_mode_review"),
    "08": ("S08EvidenceCards", "s08_evidence_cards"),
    "09": ("S09ReadinessMap", "s09_readiness_map"),
    "10": ("S10EvidenceSurface", "s10_evidence_surface"),
    "11": ("S11EndCard", "s11_end_card"),
}


def locate(f: Finding, cache: dict) -> None:
    """Fill in the scene, the timestamp, and the narration line for a beat code."""
    sec, b = f.beat.split()
    scene = SECTIONS.get(sec, (None, None))[0]
    if scene is None:
        return
    beats = cache.get(scene)
    if beats is None:
        path = VIDEO / "out" / "beats" / f"{scene}.beats.json"
        beats = json.loads(path.read_text())["beats"] if path.exists() else []
        cache[scene] = beats
    i = int(b.lstrip("b")) - 1        # the slate is 1-based
    if 0 <= i < len(beats):
        f.scene, f.section, f.t = scene, sec, beats[i]["start"]
        f.line = beats[i]["line"]


def gate_hits() -> dict:
    """Which beats the machine checks flagged, so agreement can be scored."""
    hits = collections.defaultdict(set)
    cache: dict = {}
    for vf in QA.glob("*.violations.json"):
        scene = vf.stem.split(".")[0]
        sec = next((k for k, v in SECTIONS.items() if v[0] == scene), None)
        if sec is None:
            continue
        bp = VIDEO / "out" / "beats" / f"{scene}.beats.json"
        if not bp.exists():
            continue
        beats = cache.setdefault(scene, json.loads(bp.read_text())["beats"])
        for v in json.loads(vf.read_text()):
            if v["check"] == "stage_imbalance":
                continue              # explicitly not a priority
            for i, bt in enumerate(beats, 1):
                if bt["start"] <= v["t"] < bt["start"] + bt["window"]:
                    hits[f"{sec} b{i:02d}"].add(v["check"])
                    break
    return hits


def shot(f: Finding, out_dir: Path) -> str:
    scene = f.scene
    hits = sorted((VIDEO / "scenes" / "media" / "videos").rglob(f"{scene}.mp4"))
    if not hits:
        return ""
    dest = out_dir / f"{f.beat.replace(' ', '')}.jpg"
    if not dest.exists():
        out_dir.mkdir(parents=True, exist_ok=True)
        subprocess.run(["ffmpeg", "-y", "-ss", f"{f.t + 0.9:.3f}", "-i", str(hits[-1]),
                        "-frames:v", "1", "-vf", "scale=900:-2", "-q:v", "4", str(dest)],
                       check=True, capture_output=True)
    return str(dest)


def topic(f: Finding) -> str:
    """A coarse signature for what a finding is about."""
    low = f.text.lower()
    hits = [w for w in TOPIC_WORDS if w in low]
    return f"{f.category}:{'/'.join(hits[:2]) if hits else 'other'}"


def rank(findings: list[Finding]) -> tuple[list[Finding], list[tuple[str, int]]]:
    gate = gate_hits()
    order = sorted(SECTIONS)
    per_topic = collections.Counter(topic(f) for f in findings)
    cache: dict = {}
    for f in findings:
        locate(f, cache)
        f.gate_checks = tuple(sorted(gate.get(f.beat, ())))
        elapsed = (order.index(f.section) / max(len(order) - 1, 1)) if f.section else 0.0
        score = (SEVERITY_WEIGHT.get(f.severity, 10.0)
                 + (GATE_AGREES_BONUS if f.gate_checks else 0.0)
                 + EARLY_WEIGHT * (1.0 - elapsed))
        if per_topic[topic(f)] >= RECURRING_AT:
            score *= RECURRING_PENALTY
        f.score = score
    findings.sort(key=lambda f: (-f.score, f.beat))

    # Diversity: no more than a couple of alike findings in the ranked list, so
    # twenty rows are twenty decisions.
    seen: collections.Counter = collections.Counter()
    ranked, overflow = [], []
    for f in findings:
        key = (f.section, f.category)
        if seen[key] < PER_SECTION_CATEGORY_CAP:
            seen[key] += 1
            ranked.append(f)
        else:
            overflow.append(f)
    recurring = [(t, n) for t, n in per_topic.most_common() if n >= RECURRING_AT]
    return ranked + overflow, recurring


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--report", type=Path, required=True)
    ap.add_argument("--out", type=Path, default=VIDEO / "out" / "review" / "ranked.json")
    ap.add_argument("--shots", type=Path, default=VIDEO / "out" / "review" / "ranked_shots")
    ap.add_argument("--top", type=int, default=20)
    args = ap.parse_args()

    findings = parse(args.report)
    if not findings:
        print("no findings parsed — is the report in BEAT | SEVERITY | CATEGORY | text form?")
        return 1
    findings, recurring = rank(findings)
    for f in findings[:args.top]:
        f.shot = shot(f, args.shots)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps([asdict(f) for f in findings], indent=2) + "\n")

    (args.out.parent / "recurring.json").write_text(
        json.dumps([{"topic": t, "count": n} for t, n in recurring], indent=2) + "\n")

    sev = collections.Counter(f.severity for f in findings)
    print(f"{len(findings)} findings — " + ", ".join(f"{k} {v}" for k, v in sev.most_common()))
    if recurring:
        print("\nrecurring themes (one decision each, not one per beat):")
        for t, n in recurring:
            print(f"  {n:4}  {t}")
    print(f"\ntop {args.top}:\n")
    for n, f in enumerate(findings[:args.top], 1):
        agree = f" [gate: {', '.join(f.gate_checks)}]" if f.gate_checks else ""
        print(f"{n:2}. {f.beat}  {f.severity:9} {f.category:11} {f.text[:78]}{agree}")
    print(f"\nwrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
