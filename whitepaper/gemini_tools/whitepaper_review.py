"""
Submit the whitepaper draft + key wiki pages to Gemini for structured critique.

Usage:
    python3 whitepaper/gemini_tools/whitepaper_review.py \
        [--out whitepaper/gemini_tools/out/review_YYYYMMDD.md] \
        [--model gemini-2.5-pro] \
        [--focus "argument structure"]

What it bundles:
  - Introductory_composition.md   (main whitepaper draft)
  - project_wiki/concepts/        (verification_compiler, units_of_intelligence, agentic_structuring)
  - project_wiki/requirements/    (verification_compiler_requirements)
  - WHITEPAPER_STAGE_1_STRUCTURE.md
  - traceability/source_to_claim_matrix (for citation coverage check)
"""
from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from gemini_client import generate_content, generate_thinking

REPO = Path(__file__).resolve().parents[2]
DEFAULT_MODEL = "models/gemini-3.1-pro-preview"
DEFAULT_OUT = Path(__file__).parent / "out" / f"review_{date.today().isoformat()}.md"

BUNDLE_FILES = [
    "WHITEPAPER_STAGE_1_STRUCTURE.md",
    "Introductory_composition.md",
    "project_wiki/concepts/verification_compiler.md",
    "project_wiki/concepts/units_of_intelligence.md",
    "project_wiki/concepts/agentic_structuring.md",
    "project_wiki/requirements/verification_compiler_requirements.md",
    "project_wiki/traceability/source_to_claim_matrix.md",
]

REVIEW_PROMPT = """You are reviewing a whitepaper draft for a technical research project on \
agentic structuring for safety-critical software verification.

The project's core claim: a hierarchical artifact graph (the Verification Compiler) can \
decompose software verification into context-window-sized queries, each evaluated by an \
LLM or human reviewer, producing a confidence-scored evidence package that structurally \
satisfies the evidence objectives of standards like DO-178C, ISO 26262, and IEC 62443 — \
without the standard specifying reviewer identity.

Review the bundled materials below and produce a structured critique covering:

## 1. Argument Strength
- Is the core thesis clearly stated and internally consistent?
- What are the strongest parts of the argument?
- What are the weakest links — claims that rest on assertions rather than evidence?

## 2. Gaps and Missing Pieces
- What questions would a skeptical safety engineer or certifier raise that are not addressed?
- Are there structural gaps (missing sections, unexplained transitions, unsupported jumps)?

## 3. Citation Coverage
- Which major claims have adequate source support vs. which are unsupported assertions?
- Flag any specific claim that needs a citation and suggest what kind of source would satisfy it.

## 4. Clarity and Framing
- What terminology is inconsistently defined or would confuse a reader unfamiliar with the project?
- Is the "units of intelligence" framing doing useful work, or is it jargon?

## 5. Priority Recommendations
- List the 5 highest-leverage things to fix or add next, ranked by impact on the whitepaper.

Be direct and specific. Reference section names and page concepts by name when critiquing them.

---

BUNDLED MATERIALS:
"""


def build_bundle(focus: str | None) -> str:
    sections = []
    for rel in BUNDLE_FILES:
        path = REPO / rel
        if not path.exists():
            sections.append(f"\n\n=== {rel} ===\n[FILE NOT FOUND]\n")
            continue
        text = path.read_text(encoding="utf-8")
        sections.append(f"\n\n=== {rel} ===\n{text}")
    bundle = "".join(sections)
    if focus:
        bundle = f"[Reviewer focus: pay special attention to — {focus}]\n\n" + bundle
    return bundle


def main() -> None:
    parser = argparse.ArgumentParser(description="Submit whitepaper bundle to Gemini for structured review.")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--focus", type=str, default="", help="Specific aspect to emphasize (e.g. 'argument structure').")
    args = parser.parse_args()

    bundle = build_bundle(args.focus or None)
    parts = [{"text": REVIEW_PROMPT + bundle}]

    print(f"Submitting to {args.model} (HIGH thinking)...")
    review = generate_thinking(REVIEW_PROMPT + bundle, model=args.model)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(review, encoding="utf-8")
    print(f"Review saved: {args.out}")
    print("\n--- REVIEW PREVIEW (first 60 lines) ---")
    for i, line in enumerate(review.splitlines()):
        if i >= 60:
            print("...")
            break
        print(line)


if __name__ == "__main__":
    main()
