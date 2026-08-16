from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from faster_whisper import WhisperModel


def main() -> None:
    parser = argparse.ArgumentParser(description="Transcribe audio into word-level timestamps.")
    parser.add_argument("--audio", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--model", default=os.environ.get("WHISPER_MODEL", "small"))
    parser.add_argument("--device", default=os.environ.get("WHISPER_DEVICE", "auto"))
    parser.add_argument("--compute-type", default="int8")
    args = parser.parse_args()

    if not args.audio.exists():
        raise SystemExit(f"Missing audio file: {args.audio}")

    model = WhisperModel(args.model, device=args.device, compute_type=args.compute_type)
    segments, info = model.transcribe(
        args.audio.as_posix(),
        word_timestamps=True,
        vad_filter=True,
    )

    words = []
    segment_records = []
    for segment in segments:
        segment_words = []
        for word in segment.words or []:
            record = {
                "word": word.word.strip(),
                "start": round(float(word.start), 3),
                "end": round(float(word.end), 3),
                "probability": round(float(word.probability), 4),
            }
            words.append(record)
            segment_words.append(record)
        segment_records.append(
            {
                "id": segment.id,
                "start": round(float(segment.start), 3),
                "end": round(float(segment.end), 3),
                "text": segment.text.strip(),
                "words": segment_words,
            }
        )

    result = {
        "audio": args.audio.as_posix(),
        "language": info.language,
        "language_probability": round(float(info.language_probability), 4),
        "duration": round(float(info.duration), 3),
        "model": args.model,
        "segments": segment_records,
        "words": words,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(args.out)


if __name__ == "__main__":
    main()

