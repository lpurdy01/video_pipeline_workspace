# Source Frame Pipeline

This folder captures internal reference frames from the YouTube videos listed in
`../source_videos.json`.

The goal is reference and study only: use frames to understand visual language,
composition, timing, and educational techniques. Do not copy source frames into
final public assets unless rights are clear.

```bash
python3 source_frame_pipeline/capture_youtube_frames.py
```

Useful variants:

```bash
python3 source_frame_pipeline/capture_youtube_frames.py --video-id vector_embedding_reference --timestamps 00:01:10 00:02:25 00:03:40
python3 source_frame_pipeline/capture_youtube_frames.py --force-download
```

Outputs:

- `assets/reference_frames/youtube_sources/<source-id>/*.png`
- `assets/reference_frames/youtube_sources/frames_manifest.json`
