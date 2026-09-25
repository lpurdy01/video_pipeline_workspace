from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path


HERE = Path(__file__).resolve().parent
VIDEO = HERE.parent
REPO = VIDEO.parent
sys.path.insert(0, str(REPO / "whitepaper" / "gemini_tools"))

from gemini_client import generate_content, image_part  # noqa: E402


MODEL = "models/gemini-3.1-pro-preview"

PROMPT = """\
You are reviewing YouTube thumbnail and packaging candidates for a technical
explainer video called "The Compiler For Trust".

The video's core idea:
- AI made generating code cheap.
- It did not make trusting code cheap.
- High-assurance software needs traceability: requirement -> design/code -> test
  -> result -> review -> evidence.
- The proposed Verification Compiler turns project artifacts into a graph,
  traverses that graph deterministically, assembles bounded Verification Query
  Packages, lets models help during development and humans retain authority where
  it matters, then records the result as evidence.
- Important boundary: this is not "trust the AI"; it is "trust the evidence
  surface".

Audience:
- agentic developers;
- senior engineers and engineering managers;
- safety-critical/software-assurance people;
- technically curious YouTube viewers who may not know certification workflows.

Previous video lesson:
The prior launch kit used real rendered frames plus large overlaid text, not AI
image generation. Gemini ranked the most successful thumbnails as those with:
one sharp thesis, very large readable type, high contrast, and a curiosity gap
that was not too abstract. We want to improve on that by making the hook more
emotionally immediate while still respecting the technical thesis.

Review goals:
1. Rank the candidates for expected click-through from a cold YouTube feed.
2. Separately rank them for promise-match with the video.
3. Check mobile legibility at small size.
4. Identify the best A/B test pairing, meaning two variants that test genuinely
   different viewer motivations rather than minor copy differences.
5. Recommend exact fixes before final export.

Constraints:
- These thumbnails are deterministic composites from existing rendered material.
- Do not suggest photorealistic people, facial expressions, or generic AI art.
- Keep thumbnail text short. Prefer 2-5 words on the thumbnail.
- Be blunt about abstract or boring candidates.

Answer in markdown with:
## CTR Ranking
## Promise-Match Ranking
## Mobile Legibility
## Best A/B Test
## Fixes
## Final Recommendation
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default=MODEL)
    parser.add_argument("--out", type=Path, default=HERE / f"gemini_thumbnail_review_{date.today().isoformat()}.md")
    args = parser.parse_args()

    manifest = json.loads((HERE / "thumbnail_manifest.json").read_text(encoding="utf-8"))
    parts: list[dict] = [{"text": PROMPT}]
    parts.append({"text": "\nCandidate manifest:\n\n```json\n" + json.dumps(manifest["cases"], indent=2) + "\n```"})

    prev = REPO / "representation_transform_visuals" / "manifest_pipeline" / "out" / "launch_assets"
    for p in ["thumb_A_chatbots.png", "thumb_B_autocomplete.png", "thumb_C_fourways.png"]:
        path = prev / p
        if path.exists():
            parts.append({"text": f"\nPrevious video launch thumbnail for comparison: {p}"})
            parts.append(image_part(path))

    parts.append({"text": "\nCurrent candidates, A through D:"})
    for case in manifest["cases"]:
        path = HERE / case["thumbnail"]
        parts.append({"text": f"\nCandidate {case['key']}: {case['thumbnail']}\nTitle angle: {case['title']}\nPackaging angle: {case['angle']}"})
        parts.append(image_part(path))

    mobile = HERE / manifest["mobile_preview"]
    if mobile.exists():
        parts.append({"text": "\nMobile-size preview contact sheet:"})
        parts.append(image_part(mobile))

    text = generate_content(args.model, parts, timeout=300)
    args.out.write_text(f"# Gemini thumbnail review - {date.today().isoformat()}\n\nModel: `{args.model}`\n\n{text}\n", encoding="utf-8")
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
