#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

SCENES=(
  S01GenerationGate
  S02ChatLogFallacy
  S03TraceabilityChain
  S04ArtifactGraph
  S05TraversalCompiler
  S06VQPPackage
  S07DualModeReview
  S08EvidenceCards
  S09ReadinessMap
  S10EvidenceSurface
)

for scene in "${SCENES[@]}"; do
  manim -ql --format=mp4 --flush_cache --disable_caching storyboard_scenes.py "$scene"
done

