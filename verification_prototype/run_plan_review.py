"""One-shot script: send PLAN.md to Gemini 2.5 Pro for structured review."""
import sys
from pathlib import Path

# Add gemini_tools to path
REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "whitepaper" / "gemini_tools"))

from gemini_client import generate_content  # noqa: E402

PLAN_PATH = Path(__file__).parent / "PLAN.md"
OUTPUT_PATH = Path(__file__).parent / "plan_review_gemini.md"

REVIEW_PROMPT = """\
You are reviewing an implementation plan for a "Verification Compiler Prototype" — a self-referential system that applies the Verification Compiler concept (described in a whitepaper) to verify the whitepaper itself.

The plan is below. Review it and provide structured feedback on:

1. **Schema completeness**: Are the node types and edge types sufficient to build the described verification queries? What's missing?

2. **Query design**: Are the 3 VQP types (Citation Verification, Requirement Coverage, Orphan Detection) the right decomposition? What edge cases are unhandled?

3. **Builder feasibility**: Is parsing the existing wiki/markdown files into a graph practical without significant ambiguity? What parsing challenges do you anticipate?

4. **Gemini-as-agent design**: Will the prompt design for Type A and Type B queries produce reliably structured JSON? What prompt engineering concerns are there?

5. **VRM formula**: Is the 50/50 weighting appropriate for a prototype? What would a better formula account for?

6. **Missing verification types**: What important correctness properties of the whitepaper are NOT covered by these 3 VQP types?

7. **Critical risks**: What is the single biggest risk to this prototype producing useful results?

Rate each area: Good / Needs Work / Critical Gap.
End with a 3-bullet executive summary.
"""

plan_text = PLAN_PATH.read_text(encoding="utf-8")

parts = [
    {"text": REVIEW_PROMPT},
    {"text": "\n\n---\n\n## PLAN TO REVIEW\n\n" + plan_text},
]

print("Sending to Gemini 2.5 Pro — this may take up to 2 minutes...")
response = generate_content(model="models/gemini-2.5-pro", parts=parts, timeout=180)

print("\n" + "=" * 80)
print(response)
print("=" * 80 + "\n")

OUTPUT_PATH.write_text(response, encoding="utf-8")
print(f"Saved to: {OUTPUT_PATH}")
