from __future__ import annotations

import sys
from pathlib import Path

from google import genai

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from workspace_credentials import require  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    api_key = require("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)
    for model in client.models.list():
        name = getattr(model, "name", "")
        display_name = getattr(model, "display_name", "") or getattr(model, "displayName", "")
        methods = getattr(model, "supported_actions", None) or getattr(model, "supported_generation_methods", None) or []
        print(f"{name}\t{display_name}\t{methods}")


if __name__ == "__main__":
    main()
