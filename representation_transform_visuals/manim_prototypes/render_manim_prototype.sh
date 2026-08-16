#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

manim -qm --format=mp4 --media_dir ../prototype_pipeline/out/manim_media \
  new_transform_space.py NewTransformSpacePrototype
