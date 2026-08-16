from __future__ import annotations

import argparse
import os
import sys
import wave
from pathlib import Path

from google import genai
from google.genai import types

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from workspace_credentials import require  # noqa: E402


DEFAULT_MODEL = "gemini-3.1-flash-tts-preview"
DEFAULT_VOICE = "Kore"
ROOT = Path(__file__).resolve().parents[1]


def write_wav(path: Path, pcm: bytes, channels: int = 1, rate: int = 24000, sample_width: int = 2) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(path.as_posix(), "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)


def extract_audio_bytes(response) -> bytes:
    chunks: list[bytes] = []
    candidates = getattr(response, "candidates", []) or []
    for candidate in candidates:
        content = getattr(candidate, "content", None)
        for part in getattr(content, "parts", []) or []:
            inline = getattr(part, "inline_data", None)
            if inline and getattr(inline, "data", None):
                chunks.append(inline.data)
    if not chunks:
        raise RuntimeError("Gemini response did not include inline audio data.")
    return b"".join(chunks)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate scratch narration using Gemini native TTS.")
    parser.add_argument("--text", help="Text to speak.")
    parser.add_argument("--text-file", type=Path, help="Text file to speak.")
    parser.add_argument("--out", type=Path, required=True, help="Output WAV path.")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--voice", default=DEFAULT_VOICE)
    parser.add_argument("--style", default="Read this clearly and naturally, like a thoughtful technical YouTube narrator.")
    args = parser.parse_args()

    api_key = require("GEMINI_API_KEY")

    if args.text_file:
        text = args.text_file.read_text(encoding="utf-8")
    elif args.text:
        text = args.text
    else:
        raise SystemExit("Provide --text or --text-file.")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=args.model,
        contents=f"{args.style}\n\n{text}",
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=args.voice)
                )
            ),
        ),
    )
    pcm = extract_audio_bytes(response)
    write_wav(args.out, pcm)
    print(args.out)


if __name__ == "__main__":
    main()
