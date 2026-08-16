# Human Narration Chunks

Record one audio file per section listed in `../production_manifest.json`.

Human voice recordings are local-first assets. Do not upload raw recordings, human narration chunks, speaker embeddings, voiceprints, or timing-rich human narration artifacts to Gemini or other cloud APIs unless the user explicitly approves that specific upload.

Default workflow:

1. Store recordings in this folder.
2. Transcribe locally with `../../narration_pipeline/transcribe_words.py`.
3. Keep `.words.json`, beat maps, and raw audio local.
4. Use text transcripts and commentary summaries for script revision.

The current prototype expects:

- `01_hook_transform_tree.wav`
- `02_pattern.wav`
- `03_language_vectors.wav`
- `04_talking_head_claim.wav`
- `05_code_and_loss.wav`
- `06_technology_tree.wav`

You do not need to record the full script in one take. The manifest pipeline treats each chunk independently, then stitches the sections into a complete video.
