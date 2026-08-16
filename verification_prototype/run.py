"""
Main orchestrator for the whitepaper verification prototype.

Usage:
    python3 verification_prototype/run.py                   # full run
    python3 verification_prototype/run.py --build-only      # build graph + VQPs, no Gemini
    python3 verification_prototype/run.py --report-only     # re-generate report from existing results
    python3 verification_prototype/run.py --delay 3         # seconds between API calls
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE / "graph"))
sys.path.insert(0, str(HERE / "agents"))
sys.path.insert(0, str(HERE / "evidence"))

from schema import Graph
from builder import build
from traverser import traverse, save_vqps
from gemini import run_all_vqps, QuotaExhaustedError
from reporter import generate_report, load_results


DATA = HERE / "data"
RESULTS_DIR = DATA / "results"
GRAPH_PATH = DATA / "graph.json"
VQPS_PATH = DATA / "vqps.json"
REPORT_PATH = DATA / "verification_report.md"


def cmd_build(args: argparse.Namespace) -> None:
    print("=== Phase 1: Build artifact graph ===")
    graph = build()
    graph.save(GRAPH_PATH)
    print(f"Graph saved → {GRAPH_PATH}")

    print("\n=== Phase 2: Traverse graph → VQPs ===")
    vqps = traverse(graph)
    save_vqps(vqps, VQPS_PATH)
    counts: dict[str, int] = {}
    for v in vqps:
        counts[v.vqp_type] = counts.get(v.vqp_type, 0) + 1
    print(f"VQPs: {counts}")
    print(f"VQPs saved → {VQPS_PATH}")


def cmd_run(args: argparse.Namespace) -> None:
    cmd_build(args)

    print("\n=== Phase 3: Run VQPs through Gemini ===")
    vqps_raw = json.loads(VQPS_PATH.read_text())
    quota_exhausted = False
    try:
        results = run_all_vqps(
            vqps_raw,
            RESULTS_DIR,
            delay_seconds=args.delay,
            skip_existing=not args.force,
        )
        print(f"\nResults saved → {RESULTS_DIR} ({len(results)} files)")
    except QuotaExhaustedError:
        quota_exhausted = True
        print(f"\n[Partial run] Quota exhausted. Generating report from cached results.")

    print("\n=== Phase 4: Generate report ===")
    all_results = load_results(RESULTS_DIR)
    report = generate_report(all_results, REPORT_PATH)
    print(f"Report → {REPORT_PATH}")
    # Print VRM
    from reporter import compute_vrm
    scores = compute_vrm(all_results)
    print(f"\n{'='*40}")
    if quota_exhausted:
        print(f"  [PARTIAL — quota exhausted, re-run after reset]")
    print(f"  VRM = {scores['vrm']:.3f}")
    print(f"  Citation score: {scores['citation_score']:.2f} ({scores['citation_pass']}/{scores['citation_total']})")
    print(f"  Coverage score: {scores['coverage_score']:.2f} ({scores['covered']} covered, {scores['partial']} partial, {scores['missing']} missing)")
    print(f"  Orphan findings: {scores['orphan_findings']}")
    print(f"{'='*40}")


def cmd_report(args: argparse.Namespace) -> None:
    print("=== Generate report from existing results ===")
    all_results = load_results(RESULTS_DIR)
    if not all_results:
        print(f"No results found in {RESULTS_DIR}")
        sys.exit(1)
    report = generate_report(all_results, REPORT_PATH)
    print(f"Report → {REPORT_PATH}")
    from reporter import compute_vrm
    scores = compute_vrm(all_results)
    print(f"VRM = {scores['vrm']:.3f}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Whitepaper verification prototype")
    parser.add_argument("--build-only", action="store_true", help="Build graph + VQPs only")
    parser.add_argument("--report-only", action="store_true", help="Regenerate report from existing results")
    parser.add_argument("--delay", type=float, default=2.0, help="Seconds between API calls")
    parser.add_argument("--force", action="store_true", help="Re-run all VQPs even if results exist")
    args = parser.parse_args()

    if args.report_only:
        cmd_report(args)
    elif args.build_only:
        cmd_build(args)
    else:
        cmd_run(args)


if __name__ == "__main__":
    main()
