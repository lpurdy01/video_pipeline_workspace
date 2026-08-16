# Narration Pipeline

This pipeline is for making narration drive animation timing.

## Goals

1. Generate temporary natural-sounding scratch narration from the script.
2. Record or import real narration.
3. Transcribe narration into timestamped words.
4. Convert word timings into scene/beats that Manim can use.

## Secret Handling

Do not put API keys in scripts or committed files.

Use an environment variable:

```bash
export GEMINI_API_KEY="..."
```

Or create a local uncommitted `.env` file from:

```text
representation_transform_visuals/.env.example
```

The user has approved sending this project's demo narration text and script text to Gemini for scratch TTS and narration workflow experiments.

Human voice policy:

- Keep real user recordings local by default.
- Do not upload raw human narration, human audio chunks, speaker embeddings, voiceprints, or timing-rich human narration artifacts to Gemini or other cloud APIs unless the user explicitly approves that specific upload.
- It is acceptable to use text transcripts, commentary summaries, script excerpts, and rewrite notes with approved compute APIs.
- Prefer local transcription and alignment for real recordings.

## Recommended Architecture

```text
script.md
  -> scratch TTS audio
  -> real narration audio
  -> word-level STT alignment
  -> beat timing JSON
  -> Manim scene durations and cue points
```

## Current Tool Choices

### TTS

Best candidates:

- **Gemini native TTS:** good fit because the project already has Gemini API access and the docs describe recitation-style TTS for podcasts/audiobooks.
- **ElevenLabs:** likely best natural voice quality, but adds another paid service/key.
- **OpenAI TTS:** strong general option, but a separate API provider.
- **ffmpeg flite:** installed and free, but only useful as robotic scratch timing.

### STT / Word Timestamps

Best candidates:

- **faster-whisper:** local transcription with word timestamps; default for human recordings.
- **WhisperX:** stronger forced alignment workflow, especially if exact word timing becomes critical; heavier dependencies.
- **Google Cloud Speech-to-Text:** cloud option with word time offsets, but not the same as the Gemini Developer API.
- **Deepgram / AssemblyAI:** strong cloud transcription/timing APIs, but additional vendor keys.

For this project, use **faster-whisper first**. If word-level alignment is not tight enough for animation beats, upgrade to a local forced-alignment workflow such as WhisperX before considering any cloud alignment service. Ask before uploading real human audio.

## Human Audio Workflow

1. Put the recording in `representation_transform_visuals/assets/human_audio/`, preferably one file per manifest section or commentary session.
2. Run `transcribe_words.py` locally to produce `.words.json`.
3. Create a readable transcript `.md` from the local transcription.
4. Use transcript text for script revision and voice study.
5. Use word timings for beat maps and animation cue alignment.
6. Keep raw audio, `.words.json`, and beat maps local unless the user explicitly approves an upload.

## Scripts

```bash
python3 representation_transform_visuals/narration_pipeline/list_gemini_models.py
python3 representation_transform_visuals/narration_pipeline/gemini_tts.py --text "Language is becoming a computable material." --out representation_transform_visuals/narration_pipeline/out/test.wav
python3 representation_transform_visuals/narration_pipeline/transcribe_words.py --audio narration.wav --out word_timestamps.json
```

## Beat Timing JSON

The target timing format should look like:

```json
{
  "audio": "narration.wav",
  "duration": 42.1,
  "words": [
    {"word": "Every", "start": 0.12, "end": 0.42},
    {"word": "transform", "start": 1.8, "end": 2.2}
  ],
  "beats": [
    {"id": "classic_transform", "start_word": 0, "end_word": 24},
    {"id": "language_to_vectors", "start_word": 25, "end_word": 62}
  ]
}
```
