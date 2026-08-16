from __future__ import annotations

import os
from pathlib import Path

from google import genai


ROOT = Path(__file__).resolve().parents[1]


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and value and key not in os.environ:
            os.environ[key] = value


def main() -> None:
    load_env_file(ROOT / ".env")
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise SystemExit("Set GEMINI_API_KEY in your shell or local .env before running.")

    client = genai.Client(api_key=api_key)
    for model in client.models.list():
        name = getattr(model, "name", "")
        display_name = getattr(model, "display_name", "") or getattr(model, "displayName", "")
        methods = getattr(model, "supported_actions", None) or getattr(model, "supported_generation_methods", None) or []
        print(f"{name}\t{display_name}\t{methods}")


if __name__ == "__main__":
    main()
