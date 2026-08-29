"""
Gate every section in one command.

Running the ten sections by hand is how a stale pass gets mistaken for a fresh
one: sections 06-10 sat at "PASS" for a day after the pipeline changed
underneath them, because nobody re-ran them. This prints one table with the
render timestamp on every row, so "not re-gated since the fix" is visible
rather than assumed.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
VIDEO = HERE.parent

SECTIONS = [
    ("01_generation_got_cheap", "s01_generation_got_cheap.py", "S01GenerationGotCheap"),
    ("02_chat_log_fallacy", "s02_chat_log_fallacy.py", "S02ChatLogFallacy"),
    ("03_traceability_shape", "s03_traceability_shape.py", "S03TraceabilityShape"),
    ("04_artifact_graph", "s04_artifact_graph.py", "S04ArtifactGraph"),
    ("05_compilation_traversal", "s05_compilation_traversal.py", "S05CompilationTraversal"),
    ("06_vqp", "s06_vqp.py", "S06VQP"),
    ("07_dual_mode_review", "s07_dual_mode_review.py", "S07DualModeReview"),
    ("08_evidence_cards", "s08_evidence_cards.py", "S08EvidenceCards"),
    ("09_readiness_map", "s09_readiness_map.py", "S09ReadinessMap"),
    ("10_evidence_surface", "s10_evidence_surface.py", "S10EvidenceSurface"),
    ("11_end_card", "s11_end_card.py", "S11EndCard"),
]

QA_DIR = VIDEO / "scenes" / "out" / "qa"


def run_one(section: str, scene_file: str, scene: str, quality: str) -> dict:
    # Clear the previous verdict so a crashed render cannot be read as a pass.
    for suffix in ("result", "violations", "geometry"):
        (QA_DIR / f"{scene}.{suffix}.json").unlink(missing_ok=True)
    t0 = time.time()
    proc = subprocess.run(
        [sys.executable, str(HERE / "build.py"),
         "--section", section,
         "--scene-file", str(VIDEO / "scenes" / scene_file),
         "--scene", scene,
         "--qa-dir", str(QA_DIR),
         "--quality", quality,
         "--allow-fail"],
        cwd=str(VIDEO), capture_output=True, text=True,
    )
    print(proc.stdout[-4000:])
    if proc.returncode != 0:
        print(proc.stderr[-3000:])
    result_path = QA_DIR / f"{scene}.result.json"
    if not result_path.exists():
        return {"scene": scene, "ok": False, "violations": -1, "drift": 0.0,
                "coverage": 0.0, "error": "render or gate crashed",
                "seconds": round(time.time() - t0, 1)}
    data = json.loads(result_path.read_text())
    data["seconds"] = round(time.time() - t0, 1)
    return data


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--only", nargs="*", help="section id prefixes, e.g. 01 06")
    ap.add_argument("--quality", default="l")
    args = ap.parse_args()

    wanted = SECTIONS
    if args.only:
        wanted = [s for s in SECTIONS if any(s[0].startswith(p) for p in args.only)]

    QA_DIR.mkdir(parents=True, exist_ok=True)
    results = [run_one(*s, quality=args.quality) for s in wanted]

    print("\n" + "=" * 74)
    print(f"{'scene':28} {'gate':6} {'viol':>5} {'drift':>7} {'cover':>7} {'render':>8}")
    print("-" * 74)
    for r in results:
        print(f"{r['scene']:28} {'PASS' if r['ok'] else 'FAIL':6} "
              f"{r['violations']:5} {r['drift']:+7.2f} {r['coverage']:6.1%} "
              f"{r['seconds']:7.1f}s")
    bad = [r for r in results if not r["ok"]]
    print("=" * 74)
    print(f"{len(results) - len(bad)}/{len(results)} sections clean")

    for r in bad:
        vpath = QA_DIR / f"{r['scene']}.violations.json"
        if vpath.exists():
            viol = json.loads(vpath.read_text())
            kinds: dict[str, int] = {}
            for v in viol:
                kinds[v["check"]] = kinds.get(v["check"], 0) + 1
            print(f"  {r['scene']}: " + ", ".join(f"{k}×{n}" for k, n in kinds.items()))
        elif r.get("error"):
            print(f"  {r['scene']}: {r['error']}")
        elif abs(r["drift"]) > 0.25:
            print(f"  {r['scene']}: drift {r['drift']:+.2f}s")

    (VIDEO / "out" / "qa_summary.json").write_text(json.dumps(results, indent=2) + "\n")
    return 0 if not bad else 1


if __name__ == "__main__":
    raise SystemExit(main())
