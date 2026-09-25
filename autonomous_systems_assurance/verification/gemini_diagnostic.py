#!/usr/bin/env python3
"""Perform one minimal Gemini health check without exposing credentials.

This checks the same credential and SDK path used by the project reviewers. It
does not upload project material. The JSON result is written under ignored out/
and records only model, outcome, time, error type and message.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
WORKSPACE = PROJECT.parent
OUT = PROJECT / "verification" / "out" / "gemini_diagnostic"
sys.path.insert(0, str(WORKSPACE))

from workspace_credentials import require  # noqa: E402
from google import genai  # noqa: E402


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    result = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "model": "gemini-3.1-pro-preview",
        "request": "minimal health check; no project content uploaded",
    }
    try:
        client = genai.Client(api_key=require("GEMINI_API_KEY"))
        response = client.models.generate_content(
            model=result["model"], contents="Reply with exactly: ok"
        )
        result.update({"outcome": "success", "response_text": (response.text or "")[:100]})
        code = 0
    except Exception as exc:  # Store provider diagnostics without keys or payloads.
        result.update({"outcome": "failure", "error_type": type(exc).__name__, "message": str(exc)[:2000]})
        code = 1
    path = OUT / "api_health.json"
    path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "response_text"}, indent=2))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
