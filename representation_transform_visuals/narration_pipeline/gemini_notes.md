# Gemini API Notes

## Key Handling

The Gemini API key must only live in local environment variables or ignored `.env` files.

Do not paste it into scripts, Markdown, shell history snippets, or committed config.

Use:

```bash
export GEMINI_API_KEY="..."
```

## Python SDK

Use the official `google-genai` package:

```python
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
```

## Useful Model Categories

Based on current official docs:

- **Gemini text/multimodal models:** script refinement, visual prompt drafting, source summarization, article edits.
- **Gemini native TTS models:** scratch narration with a more natural voice than `ffmpeg`/flite.
- **Gemini audio understanding:** useful for high-level transcript review, but not ideal as the primary word-level timestamp engine.

## Recommendation

Use Gemini for:

- better scratch narration;
- alternate narration takes;
- script compression/expansion;
- storyboard critique;
- generating candidate visual prompts and beat descriptions.

Use local `faster-whisper` for:

- word-level timestamps from your actual recorded narration;
- beat map generation;
- aligning Manim animation timing to your delivery.

## Sources

- Gemini API docs: https://ai.google.dev/gemini-api/docs
- Gemini speech generation docs: https://ai.google.dev/gemini-api/docs/speech-generation
- Gemini API reference: https://ai.google.dev/api

