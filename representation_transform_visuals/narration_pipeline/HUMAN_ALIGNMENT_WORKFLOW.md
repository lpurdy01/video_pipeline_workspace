# Human Narration Alignment Workflow

Human recordings stay local. Do not upload raw human audio, voiceprints, or
word-level human timing artifacts to cloud APIs unless the user explicitly
approves that exact upload.

## Before Rendering With Human Audio

1. Put recordings in:

   ```bash
   representation_transform_visuals/assets/human_audio/
   ```

   File names should match the manifest, for example `01_opening.wav`.

2. Resolve the manifest so the build knows which sections use human audio:

   ```bash
   python3 representation_transform_visuals/manifest_pipeline/build_from_manifest.py --no-generate-tts
   ```

3. Build local word timestamps from the resolved audio:

   ```bash
   python3 representation_transform_visuals/narration_pipeline/build_alignments.py \
     --source resolved \
     --allow-human \
     --force \
     --model small \
     --device auto \
     --compute-type int8
   ```

4. Check anchor resilience:

   ```bash
   python3 representation_transform_visuals/narration_pipeline/check_phrase_anchors.py
   ```

   The checker accepts minor wording drift using fuzzy phrase matching. Exact
   matches are best; fuzzy matches are acceptable when the matched text is the
   same intended beat. Missing anchors should be fixed before rendering.

## How Scenes Use The Alignment

Manim scenes call `wait_until_phrase(...)`. The phrase matcher first tries
exact word alignment, then fuzzy variants from `anchor_phrases.json`. This lets
a human take say, for example, "the DCT" instead of "the discrete cosine
transform" without losing the visual beat.

For strict validation renders:

```bash
cd representation_transform_visuals/manim_prototypes
env RTV_STRICT_ALIGN=1 RTV_VALIDATE_LAYOUT=1 manim -ql --format=mp4 \
  --media_dir ../prototype_pipeline/out/manim_media storyboard_sections.py S01TransformCivilization
```

Use `RTV_ALIGNMENT_DIR=/path/to/alignments` if testing an alternate alignment
folder.
