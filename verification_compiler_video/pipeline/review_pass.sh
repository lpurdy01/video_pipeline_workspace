#!/usr/bin/env bash
# One command for a full review pass: gate every section, assemble the cut,
# ask Gemini about the frames, rank what comes back, build the dashboard.
#
# Each step is separately runnable — this is the order, not a wrapper that hides
# them. Stops at the first hard failure except the gate, which is allowed to
# report violations and continue, because a pass with findings is the normal
# case and the point is to see them.
set -uo pipefail
cd "$(dirname "$0")/.."

echo "== gate =="
VC_REVIEW_SLATE=1 python3 -u pipeline/gate_all.py || true

echo "== assemble =="
python3 pipeline/assemble.py --out out/review/full_cut.mp4 || exit 1

echo "== gemini =="
rm -rf out/review/frames
python3 pipeline/gemini_review.py --batch 6 || exit 1

REPORT="out/review/gemini_frame_review_$(date +%F).md"
echo "== rank =="
python3 pipeline/rank_findings.py --report "$REPORT" --top 20 || exit 1

echo "== dashboard =="
python3 pipeline/build_dashboard.py --gemini "$REPORT" --top 20 || exit 1

echo
echo "cut:       out/review/full_cut.mp4"
echo "dashboard: out/review/dashboard.html"
