"""
Assemble the sections into one cut.

Each section is muxed with the narration named in its timing table and the pieces
are concatenated in order. The rendered length of every scene is checked against
its narration before anything is joined — video 1 concatenated first and
discovered a truncated section never, because ffmpeg's `-t` had quietly cut it.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
VIDEO = HERE.parent

SECTIONS = [
    ("01_generation_got_cheap", "s01_generation_got_cheap", "S01GenerationGotCheap"),
    ("02_chat_log_fallacy", "s02_chat_log_fallacy", "S02ChatLogFallacy"),
    ("03_traceability_shape", "s03_traceability_shape", "S03TraceabilityShape"),
    ("04_artifact_graph", "s04_artifact_graph", "S04ArtifactGraph"),
    ("05_compilation_traversal", "s05_compilation_traversal", "S05CompilationTraversal"),
    ("06_vqp", "s06_vqp", "S06VQP"),
    ("07_dual_mode_review", "s07_dual_mode_review", "S07DualModeReview"),
    ("08_evidence_cards", "s08_evidence_cards", "S08EvidenceCards"),
    ("09_readiness_map", "s09_readiness_map", "S09ReadinessMap"),
    ("10_evidence_surface", "s10_evidence_surface", "S10EvidenceSurface"),
    ("11_end_card", "s11_end_card", "S11EndCard"),
]

TOLERANCE = 0.25


def probe(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def narration_for(section_id: str) -> Path:
    timing_path = VIDEO / "out" / "timing" / f"{section_id}.timing.json"
    if not timing_path.exists():
        raise SystemExit(f"{section_id} has no timing table")
    data = json.loads(timing_path.read_text())
    raw = data.get("audio")
    if not raw:
        raise SystemExit(f"{section_id} timing table does not name an audio file")
    audio = Path(raw)
    if not audio.is_absolute():
        audio = VIDEO.parent / audio
    if not audio.exists():
        raise SystemExit(f"{section_id} narration file is missing: {audio}")
    return audio


def latest_render(scene: str) -> Path:
    hits = sorted((VIDEO / "scenes" / "media" / "videos").rglob(f"{scene}.mp4"))
    if not hits:
        raise SystemExit(f"{scene} has not been rendered")
    return max(hits, key=lambda p: p.stat().st_mtime)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, default=VIDEO / "out" / "review" / "full_cut.mp4")
    ap.add_argument("--speed", type=float, default=1.0,
                    help="Export speed; the final cut ships sped up.")
    ap.add_argument("--width", type=int, default=854)
    ap.add_argument("--height", type=int, default=480)
    ap.add_argument("--fps", type=int, default=15)
    ap.add_argument("--crf", type=int, default=23)
    ap.add_argument("--audio-bitrate", default="128k")
    args = ap.parse_args()

    tmp = args.out.parent / "_sections"
    tmp.mkdir(parents=True, exist_ok=True)
    clips, report = [], []

    for section_id, module, scene in SECTIONS:
        video = latest_render(scene)
        audio = narration_for(section_id)
        v_len, a_len = probe(video), probe(audio)
        drift = v_len - a_len
        status = "ok" if abs(drift) <= TOLERANCE else "DRIFT"
        report.append((section_id, a_len, v_len, drift, status))

        clip = tmp / f"{section_id}.mp4"
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(video), "-i", str(audio),
             "-c:v", "libx264", "-preset", "veryfast", "-crf", str(args.crf),
             "-c:a", "aac", "-b:a", args.audio_bitrate, "-pix_fmt", "yuv420p",
             "-vf", f"scale={args.width}:{args.height}:force_original_aspect_ratio=decrease,"
                    f"pad={args.width}:{args.height}:(ow-iw)/2:(oh-ih)/2,"
                    f"fps={args.fps}",
             str(clip)],
            check=True, capture_output=True)
        clips.append(clip)

    listing = tmp / "concat.txt"
    # Absolute paths: ffmpeg's concat demuxer resolves relative entries against
    # the *listing's* directory, so a relative --out turned every clip path into
    # out/review/_sections/out/review/_sections/... and the mux died.
    listing.write_text("".join(f"file '{c.resolve()}'\n" for c in clips))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listing),
                    "-c", "copy", str(args.out)], check=True, capture_output=True)

    if args.speed != 1.0:
        fast = args.out.with_name(args.out.stem + f"_{args.speed}x.mp4")
        subprocess.run(["ffmpeg", "-y", "-i", str(args.out),
                        "-vf", f"setpts=PTS/{args.speed}", "-af", f"atempo={args.speed}",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", str(args.crf),
                        "-c:a", "aac", "-b:a", args.audio_bitrate,
                        "-pix_fmt", "yuv420p", str(fast)], check=True, capture_output=True)
        print(f"sped-up export: {fast}")

    total_a = sum(r[1] for r in report)
    print(f"{'section':<28}{'narration':>10}{'render':>10}{'drift':>9}")
    for sid, a, v, d, s in report:
        print(f"{sid:<28}{a:>9.2f}s{v:>9.2f}s{d:>+8.2f}s  {s}")
    print(f"{'TOTAL':<28}{total_a:>9.2f}s  ({total_a / 60:.1f} min)")
    print(f"\nfull cut: {args.out}  ({probe(args.out):.1f}s)")
    (args.out.parent / "assembly_report.json").write_text(json.dumps(
        [{"section": s, "narration": a, "render": v, "drift": d} for s, a, v, d, _ in report],
        indent=2) + "\n")
    return 0 if all(r[4] == "ok" for r in report) else 1


if __name__ == "__main__":
    raise SystemExit(main())
