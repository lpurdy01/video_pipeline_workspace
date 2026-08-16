"""
Validation pass using the Gemini Deep Research Max agent.

Submits the whitepaper to deep-research-max-preview-04-2026, which conducts
autonomous web research and produces a comprehensive validation report.

Usage:
    python3 deep_research_validation.py            # submit + poll until done
    python3 deep_research_validation.py --submit   # submit only (saves ID to state file)
    python3 deep_research_validation.py --poll     # poll existing interaction from state file
    python3 deep_research_validation.py --id <ID>  # poll a specific interaction ID

Output is saved to whitepaper/out/deep_research_validation.md
State (interaction ID) is saved to whitepaper/out/deep_research_state.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from datetime import datetime

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "whitepaper" / "gemini_tools"))
sys.path.insert(0, str(REPO / "representation_transform_visuals"))

from gemini_client import api_key
from google import genai

STATE_FILE = REPO / "whitepaper" / "out" / "deep_research_state.json"
OUT_FILE = REPO / "whitepaper" / "out" / "deep_research_validation.md"
WHITEPAPER = REPO / "Introductory_composition.md"

AGENT = "deep-research-max-preview-04-2026"

VALIDATION_PROMPT = """\
I am building a research prototype called the "Verification Compiler" — a graph-based architecture \
for continuous, LLM-assisted verification of safety-critical software. The full Stage 1 research \
whitepaper is pasted below. Please conduct a thorough independent validation of this work by \
researching the existing literature, relevant safety standards, and current tooling.

I need answers to these specific validation questions:

1. NOVELTY: What existing tools, systems, or academic approaches already address continuous \
requirements-to-code traceability verification? Is the artifact graph + VQP decomposition concept \
genuinely novel, or does it closely replicate existing work (e.g., SCADE, Parasoft, Polarion, \
academic traceability tools)? What is the delta from prior art?

2. REGULATORY FEASIBILITY: Is the claim that the deterministic graph traversal and query assembly \
components can be qualified under DO-330 TQL-5 well-founded? What does DO-330 actually require for \
TQL-5, and does this architecture meet those criteria? What would the real qualification pathway \
look like in practice?

3. LLM INTEGRATION: Is the architectural separation — deterministic qualified components + \
non-qualified LLM developmental aid — currently accepted by regulatory bodies (FAA, EASA) as a \
viable model? What do AC 20-115D, any FAA guidance on AI/ML, EASA AI roadmap documents, and \
emerging standards (DO-178C amendments, EUROCAE WG-114) say about this?

4. VRM SCORING: Is the VRM formula design (horizontal coverage × vertical completeness × model \
accuracy weights) statistically defensible? Are there known problems with this type of composite \
metric in verification contexts? How does it compare to coverage metrics used in DO-178C MC/DC \
coverage analysis?

5. WEAKNESSES AND BLIND SPOTS: What are the fundamental assumptions this design makes that could \
fail in practice? What does the whitepaper not acknowledge that a domain expert would immediately \
flag?

6. MISSING CITATIONS: What relevant papers, standards, or prior art should this whitepaper \
cite but currently does not?

Please research each question thoroughly using current literature, then synthesize your findings \
into a structured validation report with a clear verdict on each question.

---

WHITEPAPER TEXT FOLLOWS:

{whitepaper_text}
"""


def load_whitepaper() -> str:
    text = WHITEPAPER.read_text(encoding="utf-8")
    # Strip non-content sections
    import re
    text = re.sub(r"## Expansion Areas.*", "", text, flags=re.DOTALL)
    text = re.sub(r"## Working Title\n\n.*?\n\n", "", text, count=1)
    return text.strip()


def submit(client: genai.Client) -> str:
    whitepaper_text = load_whitepaper()
    prompt = VALIDATION_PROMPT.format(whitepaper_text=whitepaper_text)

    print(f"Whitepaper: {len(whitepaper_text):,} chars")
    print(f"Total prompt: {len(prompt):,} chars")
    print(f"Submitting to {AGENT}...")

    interaction = client.interactions.create(
        agent=AGENT,
        input=prompt,
        background=True,
        agent_config={
            "type": "deep-research",
            "thinking_summaries": "auto",
        },
    )

    STATE_FILE.parent.mkdir(exist_ok=True)
    state = {
        "interaction_id": interaction.id,
        "submitted_at": datetime.utcnow().isoformat(),
        "agent": AGENT,
    }
    STATE_FILE.write_text(json.dumps(state, indent=2))

    print(f"Submitted. Interaction ID: {interaction.id}")
    print(f"State saved to: {STATE_FILE}")
    return interaction.id


def extract_output(interaction) -> str:
    """Extract the final report text from the interaction's steps."""
    # Collect all model_output steps
    output_parts = []
    for step in interaction.steps:
        if step.type == "model_output":
            for item in step.content:
                if item.type == "text" and item.text:
                    output_parts.append(item.text)
    return "\n\n".join(output_parts)


def poll(client: genai.Client, interaction_id: str, interval: int = 30) -> str:
    print(f"Polling interaction {interaction_id} every {interval}s...")
    start = time.time()

    while True:
        result = client.interactions.get(interaction_id)
        elapsed = int(time.time() - start)
        status = result.status
        steps_done = len(result.steps)

        print(f"  [{elapsed:4d}s] status={status}  steps={steps_done}")

        if status == "completed":
            print("Done.")
            return extract_output(result)
        elif status in ("failed", "cancelled"):
            raise RuntimeError(f"Interaction {status}: {result}")

        time.sleep(interval)


def save_output(text: str, interaction_id: str) -> None:
    header = f"""# Deep Research Validation Report
Agent: {AGENT}
Interaction ID: {interaction_id}
Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}

---

"""
    OUT_FILE.write_text(header + text, encoding="utf-8")
    print(f"Saved to: {OUT_FILE}")


def main():
    parser = argparse.ArgumentParser(description="Run deep research validation on the whitepaper")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--submit", action="store_true", help="Submit only, don't poll")
    group.add_argument("--poll", action="store_true", help="Poll existing interaction from state file")
    group.add_argument("--id", metavar="INTERACTION_ID", help="Poll a specific interaction ID")
    parser.add_argument("--interval", type=int, default=30, help="Poll interval in seconds (default: 30)")
    args = parser.parse_args()

    key = api_key()
    client = genai.Client(api_key=key)

    if args.id:
        interaction_id = args.id
        output = poll(client, interaction_id, args.interval)
        save_output(output, interaction_id)

    elif args.poll:
        if not STATE_FILE.exists():
            print(f"No state file found at {STATE_FILE}. Run without --poll to submit first.")
            sys.exit(1)
        state = json.loads(STATE_FILE.read_text())
        interaction_id = state["interaction_id"]
        print(f"Resuming interaction {interaction_id} (submitted {state['submitted_at']})")
        output = poll(client, interaction_id, args.interval)
        save_output(output, interaction_id)

    elif args.submit:
        submit(client)
        print("Run with --poll to retrieve results when ready.")

    else:
        # Submit and poll
        interaction_id = submit(client)
        print()
        output = poll(client, interaction_id, args.interval)
        save_output(output, interaction_id)


if __name__ == "__main__":
    main()
