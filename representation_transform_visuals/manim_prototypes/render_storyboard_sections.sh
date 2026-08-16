#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

manim -ql --format=mp4 --media_dir ../prototype_pipeline/out/manim_media \
  storyboard_sections.py \
  S01TransformCivilization \
  S02PatternPipeline \
  S03LanguageVectors \
  S04HumanClaimBridge \
  S05CodeAndLoss \
  S06TechnologyTree
