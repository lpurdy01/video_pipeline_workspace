#!/usr/bin/env bash
# Regenerate all whitepaper diagrams via Nano Banana Pro.
# Edit diagram_specs/*.txt to change content, then re-run this script.
# Run from repo root: bash whitepaper/render_all_diagrams.sh

set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
TOOLS="$REPO/whitepaper/gemini_tools"
SPECS="$REPO/whitepaper/diagram_specs"
OUT="$REPO/whitepaper"
MODEL="${MODEL:-models/nano-banana-pro-preview}"

export GEMINI_API_KEY="${GEMINI_API_KEY:-$(grep GEMINI_API_KEY "$REPO/representation_transform_visuals/.env" | cut -d= -f2)}"

echo "Model: $MODEL"
echo "Output: $OUT"
echo ""

render() {
  local n="$1"
  local wireframe="$OUT/diagram${n}.png"
  local spec="$SPECS/diagram${n}_spec.txt"
  local rendered="$OUT/diagram${n}_rendered.png"

  # Fall back to wireframe name mapping
  case "$n" in
    1) wireframe="$OUT/diagram1_artifact_graph.png" ;;
    2) wireframe="$OUT/diagram2_query_assembly.png" ;;
    3) wireframe="$OUT/diagram3_dual_mode.png" ;;
    4) wireframe="$OUT/diagram4_cross_standard.png" ;;
    5) wireframe="$OUT/diagram5_units_of_intelligence.png" ;;
  esac

  if [[ ! -f "$wireframe" ]]; then
    echo "  SKIP diagram$n — wireframe not found: $wireframe"
    return
  fi

  echo "  Rendering diagram$n..."
  cd "$TOOLS"
  python3 diagram_render.py \
    --wireframe "$wireframe" \
    --spec-file "$spec" \
    --out "$rendered" \
    --model "$MODEL"
}

for n in 1 2 3 4 5; do
  render "$n"
done

echo ""
echo "Done. Rendered PNGs:"
ls -lh "$OUT"/diagram*_rendered.png 2>/dev/null || echo "(none found)"
