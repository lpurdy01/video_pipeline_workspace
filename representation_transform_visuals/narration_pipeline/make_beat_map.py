from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_MARKERS = [
    ("classic_transform", "transform"),
    ("new_space", "new space"),
    ("signals_to_spectra", "signals"),
    ("fourier_laplace", "Fourier"),
    ("language_vectors", "language"),
    ("vectors", "vectors"),
    ("learned_transform", "learned transform"),
    ("pseudocode_to_code", "pseudocode"),
    ("semantic_loss", "loss"),
    ("assumptions", "assumptions"),
    ("technology_tree", "technology tree"),
]


def normalize(text: str) -> str:
    return "".join(ch.lower() for ch in text if ch.isalnum() or ch.isspace()).strip()


def find_phrase(words: list[dict], phrase: str) -> int | None:
    target = normalize(phrase).split()
    if not target:
        return None
    normalized_words = [normalize(word["word"]) for word in words]
    for idx in range(0, len(words) - len(target) + 1):
        if normalized_words[idx : idx + len(target)] == target:
            return idx
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Create rough animation beat map from word timestamps.")
    parser.add_argument("--words", type=Path, required=True, help="JSON from transcribe_words.py")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    data = json.loads(args.words.read_text(encoding="utf-8"))
    words = data["words"]

    starts = []
    for beat_id, phrase in DEFAULT_MARKERS:
        idx = find_phrase(words, phrase)
        if idx is not None:
            starts.append((beat_id, idx, words[idx]["start"], phrase))

    starts.sort(key=lambda item: item[2])
    beats = []
    for i, (beat_id, idx, start, phrase) in enumerate(starts):
        next_idx = starts[i + 1][1] if i + 1 < len(starts) else len(words) - 1
        end_word = max(idx, next_idx - 1)
        beats.append(
            {
                "id": beat_id,
                "marker_phrase": phrase,
                "start_word": idx,
                "end_word": end_word,
                "start": words[idx]["start"],
                "end": words[end_word]["end"],
            }
        )

    result = {
        "audio": data["audio"],
        "duration": data["duration"],
        "beats": beats,
        "words": words,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(args.out)


if __name__ == "__main__":
    main()
