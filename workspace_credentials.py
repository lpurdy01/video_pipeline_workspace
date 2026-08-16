"""
Single credential loader for every pipeline in this workspace.

Credentials live in the *user profile*, never in the repo:

    ~/.config/video-pipeline/credentials.env      (mode 0600)

Format is plain ``KEY=value``, one per line, ``#`` for comments.

Usage from any script in this repo::

    from workspace_credentials import load, require

    load()                          # populate os.environ (idempotent)
    key = require("GEMINI_API_KEY") # or fail with an actionable message

Scripts nested in subdirectories need the repo root on sys.path first::

    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from workspace_credentials import require

Precedence, highest first:

1. Whatever is already exported in the environment (one-off overrides win).
2. A repo-local ``.env``, if present — for temporarily testing another key
   without editing the profile store.
3. The user profile store.

Nothing here ever writes a credential back to disk or logs a value.
"""
from __future__ import annotations

import os
from pathlib import Path

__all__ = ["load", "require", "store_path", "REPO_ROOT", "STORE_PATH"]

REPO_ROOT = Path(__file__).resolve().parent


def store_path() -> Path:
    """Path to the user profile credential store, honouring XDG_CONFIG_HOME."""
    config_home = os.environ.get("XDG_CONFIG_HOME")
    base = Path(config_home) if config_home else Path.home() / ".config"
    return base / "video-pipeline" / "credentials.env"


STORE_PATH = store_path()

# Repo-local override file, checked before the profile store. Gitignored.
LOCAL_ENV = REPO_ROOT / "representation_transform_visuals" / ".env"

_loaded = False


def _parse_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.is_file():
        return values
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and value:
            values[key] = value
    return values


def load(force: bool = False) -> None:
    """
    Merge credential files into os.environ. Idempotent; safe to call from every
    entry point. Existing environment variables are never overwritten.
    """
    global _loaded
    if _loaded and not force:
        return

    # Lowest precedence first, so later sources fill only what is still missing.
    for source in (store_path(), LOCAL_ENV):
        for key, value in _parse_env_file(source).items():
            os.environ.setdefault(key, value)

    _loaded = True


def require(name: str) -> str:
    """Return credential ``name``, or exit with a message that says how to fix it."""
    load()
    value = os.environ.get(name)
    if not value:
        raise SystemExit(
            f"Missing credential {name}.\n"
            f"  Add a line `{name}=...` to {store_path()}\n"
            f"  (or export {name} in your shell for a one-off run)."
        )
    return value
