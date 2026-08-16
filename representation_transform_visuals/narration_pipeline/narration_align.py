from __future__ import annotations

import json
import re
from difflib import SequenceMatcher
from functools import lru_cache
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ALIGN_DIR = ROOT / "manifest_pipeline" / "out" / "alignments"


def normalize_token(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def normalize_phrase(text: str) -> list[str]:
    return [tok for tok in (normalize_token(part) for part in text.split()) if tok]


@lru_cache(maxsize=64)
def load_alignment(section_id: str, align_dir: str | Path = DEFAULT_ALIGN_DIR.as_posix()) -> dict:
    path = Path(align_dir) / f"{section_id}.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _normalized_words(words: list[dict]) -> list[str]:
    return [normalize_token(word.get("word", "")) for word in words]


def _exact_phrase_window(words: list[dict], target: list[str], occurrence: int = 0) -> tuple[int, int] | None:
    normalized_words = _normalized_words(words)
    matches_seen = 0
    target_len = len(target)
    for idx in range(0, len(normalized_words) - target_len + 1):
        if normalized_words[idx: idx + target_len] != target:
            continue
        if matches_seen == occurrence:
            return idx, idx + target_len
        matches_seen += 1
    return None


def _window_score(target: list[str], candidate: list[str]) -> float:
    if not target or not candidate:
        return 0.0
    seq_score = SequenceMatcher(None, target, candidate).ratio()
    target_set = set(target)
    candidate_set = set(candidate)
    overlap = len(target_set & candidate_set) / max(1, len(target_set | candidate_set))
    return (0.72 * seq_score) + (0.28 * overlap)


def find_phrase_match(
    section_id: str,
    phrase: str | Iterable[str],
    *,
    occurrence: int = 0,
    align_dir: str | Path = DEFAULT_ALIGN_DIR,
    fuzzy: bool = True,
    min_score: float = 0.74,
) -> dict | None:
    """Return the best local alignment match for a phrase or phrase variants.

    Human narration often changes a few words. The exact pass handles scratch
    TTS and verbatim reads; the fuzzy pass tolerates small substitutions,
    skipped function words, and short insertions without uploading audio.
    """
    data = load_alignment(section_id, Path(align_dir).as_posix())
    words = data.get("words") or []
    phrases = [phrase] if isinstance(phrase, str) else list(phrase)
    if not words or not phrases:
        return None

    normalized_words = _normalized_words(words)
    best: dict | None = None
    for raw_phrase in phrases:
        target = normalize_phrase(raw_phrase)
        if not target:
            continue
        exact_window = _exact_phrase_window(words, target, occurrence=occurrence)
        if exact_window is not None:
            start_idx, end_idx = exact_window
            exact = float(words[start_idx]["start"])
            return {
                "start": exact,
                "end": float(words[end_idx - 1].get("end", exact)),
                "score": 1.0,
                "method": "exact",
                "phrase": raw_phrase,
                "matched_text": raw_phrase,
            }

        if not fuzzy:
            continue

        target_len = len(target)
        min_len = max(1, target_len - max(2, target_len // 3))
        max_len = min(len(normalized_words), target_len + max(2, target_len // 2))
        for start_idx in range(len(normalized_words)):
            for window_len in range(min_len, max_len + 1):
                end_idx = start_idx + window_len
                if end_idx > len(normalized_words):
                    break
                candidate = normalized_words[start_idx:end_idx]
                score = _window_score(target, candidate)
                if score < min_score:
                    continue
                if best is None or score > best["score"]:
                    best = {
                        "start": float(words[start_idx]["start"]),
                        "end": float(words[end_idx - 1].get("end", words[start_idx]["start"])),
                        "score": round(score, 4),
                        "method": "fuzzy",
                        "phrase": raw_phrase,
                        "matched_text": " ".join(word.get("word", "") for word in words[start_idx:end_idx]),
                    }
    if best is not None:
        return best
    return None


def find_phrase_time(
    section_id: str,
    phrase: str | Iterable[str],
    *,
    occurrence: int = 0,
    align_dir: str | Path = DEFAULT_ALIGN_DIR,
    fuzzy: bool = True,
    min_score: float = 0.74,
) -> float | None:
    match = find_phrase_match(
        section_id,
        phrase,
        occurrence=occurrence,
        align_dir=align_dir,
        fuzzy=fuzzy,
        min_score=min_score,
    )
    if match is None:
        return None
    return float(match["start"])


def phrase_exists(section_id: str, phrase: str, *, align_dir: str | Path = DEFAULT_ALIGN_DIR) -> bool:
    return find_phrase_time(section_id, phrase, align_dir=align_dir) is not None


def first_available_phrase_time(
    section_id: str,
    phrases: Iterable[str],
    *,
    align_dir: str | Path = DEFAULT_ALIGN_DIR,
) -> tuple[str, float] | None:
    for phrase in phrases:
        start = find_phrase_time(section_id, phrase, align_dir=align_dir)
        if start is not None:
            return phrase, start
    return None
