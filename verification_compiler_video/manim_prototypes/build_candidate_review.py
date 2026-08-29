"""
Assemble the candidate review set.

For each script section, gather the three candidate renders (A/B/C), pull three
keyframes from each, and build a side-by-side 3-up comparison clip so a human can
choose. Keyframes are what gets sent to Gemini for critique — never audio.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
MEDIA = HERE / "media" / "videos"
OUT = HERE / "out" / "candidates"

# section id -> (A scene, B scene, C scene)
SECTIONS = {
    "01_generation_got_cheap":  ("S01GenerationGate",    "B01RateDivergence",     "C01ReviewQueue"),
    "02_chat_log_fallacy":      ("S02ChatLogFallacy",    "B02TwoColumnLedger",    "C02TranscriptVsRecord"),
    "03_traceability_shape":    ("S03TraceabilityChain", "B03ReverseAudit",       "C03TraceTable"),
    "04_artifact_graph":        ("S04ArtifactGraph",     "B04ChainsBecomeGraph",  "C04TableLiftsToGraph"),
    "05_compilation_traversal": ("S05TraversalCompiler", "B05TraversalWalk",      "C05TwoCompilers"),
    "06_vqp":                   ("S06VQPPackage",        "B06FoldPackage",        "C06VQPDocument"),
    "07_dual_mode_review":      ("S07DualModeReview",    "B07ReviewerSwap",       "C07IdenticalSchema"),
    "08_evidence_cards":        ("S08EvidenceCards",     "B08VersionLedger",      "C08HashMismatch"),
    "09_readiness_map":         ("S09ReadinessMap",      "B09ReadinessTrend",     "C09CIOutput"),
    "10_evidence_surface":      ("S10EvidenceSurface",   "B10TheLoop",            "C10DecisionSurface"),
}

SET_SOURCE = {"A": "storyboard_scenes", "B": "candidates_b", "C": "candidates_c"}
FRACTIONS = [0.25, 0.55, 0.90]


def find_render(module: str, scene: str) -> Path:
    hits = sorted((MEDIA / module).rglob(f"{scene}.mp4"))
    if not hits:
        raise SystemExit(f"missing render: {module}/{scene}.mp4 — render it first")
    return hits[-1]


def duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(out.stdout.strip())


def keyframes(path: Path, out_dir: Path, stem: str) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    total = duration(path)
    made = []
    for i, frac in enumerate(FRACTIONS):
        dest = out_dir / f"{stem}_{i + 1}.png"
        subprocess.run(
            ["ffmpeg", "-y", "-ss", f"{total * frac:.2f}", "-i", str(path),
             "-frames:v", "1", "-q:v", "2", str(dest)],
            capture_output=True, check=True,
        )
        made.append(dest)
    return made


def label(path: Path, text: str, out: Path) -> Path:
    """Burn a set label onto a clip so the 3-up is unambiguous."""
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(path),
         "-vf", f"drawtext=text='{text}':fontcolor=white:fontsize=26:x=14:y=12:"
                f"box=1:boxcolor=black@0.65:boxborderw=8",
         "-an", str(out)],
        capture_output=True, check=True,
    )
    return out


def three_up(clips: list[Path], out: Path) -> Path:
    """hstack three clips, padding the short ones to the longest duration."""
    longest = max(duration(c) for c in clips)
    inputs = []
    for c in clips:
        inputs += ["-i", str(c)]
    filt = (
        f"[0:v]tpad=stop_mode=clone:stop_duration={longest:.2f}[a];"
        f"[1:v]tpad=stop_mode=clone:stop_duration={longest:.2f}[b];"
        f"[2:v]tpad=stop_mode=clone:stop_duration={longest:.2f}[c];"
        f"[a][b][c]hstack=inputs=3[v]"
    )
    subprocess.run(
        ["ffmpeg", "-y", *inputs, "-filter_complex", filt, "-map", "[v]",
         "-t", f"{longest:.2f}", "-pix_fmt", "yuv420p", str(out)],
        capture_output=True, check=True,
    )
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = OUT / "_tmp"
    tmp.mkdir(exist_ok=True)
    index: dict[str, dict] = {}

    for section, scenes in SECTIONS.items():
        entry: dict[str, dict] = {}
        labelled = []
        for set_name, scene in zip("ABC", scenes):
            src = find_render(SET_SOURCE[set_name], scene)
            frames = keyframes(src, OUT / "frames" / section, f"{set_name}_{scene}")
            entry[set_name] = {
                "scene": scene,
                "render": str(src.relative_to(HERE)),
                "duration": round(duration(src), 2),
                "frames": [str(f.relative_to(OUT)) for f in frames],
            }
            labelled.append(label(src, f"{set_name}  {scene}", tmp / f"{section}_{set_name}.mp4"))
        combined = three_up(labelled, OUT / f"{section}_ABC.mp4")
        entry["comparison"] = combined.name
        index[section] = entry
        print(f"built {section}  ->  {combined.name}")

    (OUT / "index.json").write_text(json.dumps(index, indent=2) + "\n")
    print(f"\nindex written to {OUT / 'index.json'}")


if __name__ == "__main__":
    main()
