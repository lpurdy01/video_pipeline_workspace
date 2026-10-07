"""One bounded, search-grounded literature scout; raw output stays under out/."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPACE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent))

from workspace_credentials import require  # noqa: E402
from google import genai  # noqa: E402
from google.genai import types  # noqa: E402


PROMPT = """Act as a skeptical research scout for a preliminary 'engineering of intelligence'
research note. Use Google Search grounding. Find original papers and primary research
pages, with stable direct URLs and precise equations or sections where possible.

Question: Can one estimate the model capacity, data and compute needed for a specified
task at a specified generalization/error target, and then bound what a given model
could possibly achieve? Treat this as a conditional, empirical engineering problem,
not a universal law. Contrast low-dimensional known state-space control with learned
vision-to-control and language. Distinguish representation capacity, sample
complexity, optimization compute, deployment compute/latency, and statistical
assurance of rare hazardous events. Do not equate parameter count with intelligence.

Investigate and challenge these candidate bridges:
1. task complexity and inductive bias: rate-distortion / information bottleneck,
   conditional entropy or minimum description length, intrinsic dimension and
   effective rank, compositionality and repetitive structure;
2. empirical neural scaling laws: parameter count, distinct useful examples,
   training FLOPs, data quality, irreducible loss and broken or shifted scaling;
3. learning-theory bounds: VC/PAC/Rademacher, no-free-lunch and why naive parameter
   count can mispredict modern neural generalization;
4. chaos and partial observability: Lyapunov growth and prediction horizon,
   observability, state estimation and feedback; carefully identify where these
   are relevant and where they are a misleading metaphor;
5. assembly theory, if any rigorous connection to engineered model sizing exists;
   report a negative finding explicitly if not;
6. ROC/precision-recall, prevalence/base rates, calibration, selective prediction,
   and one-sided confidence bounds for rare-event miss rates, including closed-loop
   effects. Explain why these do not imply certified system safety.

Prioritize original work by authors or publishers. Search for counterexamples such
as shortcut learning, underspecification, data repetition, scaling discontinuities,
OOD failure, and methods that beat larger models through structure or data curation.
Separate theorem, within-family empirical fit, proposed hypothesis, and unsupported
analogy. Identify 10-15 high-value sources. For each: title, author/publisher, year,
direct original URL, inspected locator if available, bounded finding, limitation,
and which candidate bridge it informs. Do not invent quotations or equations.

Finish with a proposed *testable* resource-estimation framework: inputs, outputs,
minimal equations, a small experiment spanning a known linear state-space task,
chaotic partially observed task, and visual rare-event control task, and falsifiers.
Do not claim a universal parameter-count formula. Return links as full URLs.
"""


def main() -> None:
    out = SPACE / "out"
    out.mkdir(parents=True, exist_ok=True)
    client = genai.Client(api_key=require("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=PROMPT,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())],
            thinking_config=types.ThinkingConfig(thinking_level="HIGH"),
            temperature=0.2,
        ),
    )
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    (out / f"prompt_{stamp}.txt").write_text(PROMPT, encoding="utf-8")
    (out / f"response_{stamp}.md").write_text(response.text or "", encoding="utf-8")
    (out / f"response_{stamp}.json").write_text(
        json.dumps(response.model_dump(mode="json", exclude_none=True), indent=2),
        encoding="utf-8",
    )
    print(f"Saved grounded Gemini scout output under {out} ({stamp})")


if __name__ == "__main__":
    main()
