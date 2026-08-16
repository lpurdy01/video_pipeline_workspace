"""Submit or poll a Gemini Deep Research interaction for this project.

Use for text-only research and planning. Keep human voice/audio artifacts out
of prompts unless the user gives explicit per-request approval.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ROOT = REPO / "representation_transform_visuals"
sys.path.insert(0, str(REPO / "whitepaper" / "gemini_tools"))

from gemini_client import api_key  # noqa: E402
from google import genai  # noqa: E402


DEFAULT_AGENT = "deep-research-max-preview-04-2026"
OUT_DIR = ROOT / "agent_tools" / "out"
STATE_FILE = OUT_DIR / "deep_research_state.json"
OUT_FILE = OUT_DIR / "deep_research_report.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def read_prompt(args: argparse.Namespace) -> str:
    prompt = args.prompt or ""
    if args.prompt_file:
        if not args.prompt_file.exists():
            raise SystemExit(f"Missing prompt file: {args.prompt_file}")
        prompt = args.prompt_file.read_text(encoding="utf-8")
    if not prompt.strip():
        raise SystemExit("Provide --prompt or --prompt-file.")
    return prompt.strip()


def submit(client: genai.Client, prompt: str, agent: str) -> str:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    interaction = client.interactions.create(
        agent=agent,
        input=prompt,
        background=True,
        agent_config={
            "type": "deep-research",
            "thinking_summaries": "auto",
        },
    )
    state = {
        "interaction_id": interaction.id,
        "submitted_at": utc_now(),
        "agent": agent,
        "out_file": OUT_FILE.as_posix(),
    }
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")
    print(f"Submitted {interaction.id}")
    print(STATE_FILE)
    return interaction.id


def extract_output(interaction) -> str:
    output_parts: list[str] = []
    for step in interaction.steps:
        if step.type != "model_output":
            continue
        for item in step.content:
            if item.type == "text" and item.text:
                output_parts.append(item.text)
    return "\n\n".join(output_parts).strip()


def poll(client: genai.Client, interaction_id: str, interval: int) -> str:
    print(f"Polling {interaction_id} every {interval}s")
    while True:
        result = client.interactions.get(interaction_id)
        print(f"status={result.status} steps={len(result.steps)}")
        if result.status == "completed":
            return extract_output(result)
        if result.status in ("failed", "cancelled"):
            raise RuntimeError(f"Interaction {result.status}: {result}")
        time.sleep(interval)


def save_report(text: str, interaction_id: str, agent: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    header = (
        "# Gemini Deep Research Report\n"
        f"Agent: {agent}\n"
        f"Interaction ID: {interaction_id}\n"
        f"Generated: {utc_now()}\n\n"
        "---\n\n"
    )
    OUT_FILE.write_text(header + text + "\n", encoding="utf-8")
    print(OUT_FILE)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--submit", action="store_true", help="Submit and save state; do not poll.")
    mode.add_argument("--poll", action="store_true", help="Poll the state file interaction.")
    mode.add_argument("--id", metavar="INTERACTION_ID", help="Poll a specific interaction.")
    parser.add_argument("--prompt", default="")
    parser.add_argument("--prompt-file", type=Path)
    parser.add_argument("--agent", default=DEFAULT_AGENT)
    parser.add_argument("--interval", type=int, default=30)
    args = parser.parse_args()

    client = genai.Client(api_key=api_key())

    if args.poll:
        if not STATE_FILE.exists():
            raise SystemExit(f"No state file: {STATE_FILE}")
        state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        interaction_id = state["interaction_id"]
        agent = state.get("agent", args.agent)
        text = poll(client, interaction_id, args.interval)
        save_report(text, interaction_id, agent)
        return 0

    if args.id:
        text = poll(client, args.id, args.interval)
        save_report(text, args.id, args.agent)
        return 0

    prompt = read_prompt(args)
    interaction_id = submit(client, prompt, args.agent)
    if args.submit:
        return 0
    text = poll(client, interaction_id, args.interval)
    save_report(text, interaction_id, args.agent)
    return 0


if __name__ == "__main__":
    sys.exit(main())
