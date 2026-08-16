"""
Shared Gemini API helpers.

Two interfaces:
  generate_content()        REST-based, for standard calls and image parts (visual_review.py)
  generate_thinking()       google-genai SDK, uses gemini-3.1-pro-preview with HIGH thinking
                            — use this for deep reasoning, architectural review, second opinions
"""
from __future__ import annotations

import base64
import json
import mimetypes
import os
from pathlib import Path

import requests

ENV_FILE = Path(__file__).resolve().parents[2] / "representation_transform_visuals" / ".env"


def load_env_file(path: Path = ENV_FILE) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and value and key not in os.environ:
            os.environ[key] = value


def api_key() -> str:
    load_env_file()
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise SystemExit("Set GEMINI_API_KEY in representation_transform_visuals/.env or your shell.")
    return key


def image_part(path: Path) -> dict:
    mime, _ = mimetypes.guess_type(path.as_posix())
    return {
        "inline_data": {
            "mime_type": mime or "image/png",
            "data": base64.b64encode(path.read_bytes()).decode("ascii"),
        }
    }


def generate_content(model: str, parts: list[dict], timeout: int = 120) -> str:
    """Send a generateContent request and return the text response."""
    url = f"https://generativelanguage.googleapis.com/v1beta/{model}:generateContent"
    response = requests.post(
        url,
        headers={"Content-Type": "application/json", "X-goog-api-key": api_key()},
        data=json.dumps({"contents": [{"parts": parts}]}),
        timeout=timeout,
    )
    if response.status_code >= 400:
        raise RuntimeError(f"Gemini API error {response.status_code}: {response.text[:500]}")
    payload = response.json()
    chunks = []
    for candidate in payload.get("candidates", []):
        for part in candidate.get("content", {}).get("parts", []):
            if "text" in part:
                chunks.append(part["text"])
    if not chunks:
        raise RuntimeError(f"No text in response: {json.dumps(payload)[:500]}")
    return "\n".join(chunks)


def generate_thinking(
    prompt: str,
    model: str = "models/gemini-3.1-pro-preview",
    thinking_level: str = "HIGH",
) -> str:
    """
    Call Gemini with extended thinking enabled using the google-genai SDK.

    Use this for deep reasoning tasks: architectural review, second opinions,
    complex synthesis, plan evaluation.

    Args:
        prompt: The full text prompt to send.
        model: Gemini model that supports thinking_config (default: gemini-3.1-pro-preview).
        thinking_level: "LOW", "MEDIUM", or "HIGH" (default: HIGH).

    Returns:
        The full text response (thinking tokens are consumed server-side, not returned).
    """
    load_env_file()
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise SystemExit("Set GEMINI_API_KEY in representation_transform_visuals/.env or your shell.")

    from google import genai
    from google.genai import types

    client = genai.Client(api_key=key)
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_level=thinking_level),
        ),
    )
    return response.text


def generate_image(model: str, parts: list[dict], timeout: int = 180) -> bytes:
    """Send a generateContent request and return raw image bytes from the first inline_data part."""
    url = f"https://generativelanguage.googleapis.com/v1beta/{model}:generateContent"
    response = requests.post(
        url,
        headers={"Content-Type": "application/json", "X-goog-api-key": api_key()},
        data=json.dumps({
            "contents": [{"parts": parts}],
            "generationConfig": {"responseModalities": ["IMAGE", "TEXT"]},
        }),
        timeout=timeout,
    )
    if response.status_code >= 400:
        raise RuntimeError(f"Gemini API error {response.status_code}: {response.text[:500]}")
    payload = response.json()
    for candidate in payload.get("candidates", []):
        for part in candidate.get("content", {}).get("parts", []):
            if "inlineData" in part:
                return base64.b64decode(part["inlineData"]["data"])
    raise RuntimeError(f"No image data in response: {json.dumps(payload)[:500]}")
