"""One grounded adversarial Gemini pass; raw API output remains ignored under out/."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

SPACE = Path(__file__).resolve().parent
ROOT = SPACE.parents[2]
sys.path.insert(0, str(ROOT))

from workspace_credentials import require  # noqa: E402
from google import genai  # noqa: E402
from google.genai import types  # noqa: E402

PROMPT = """Act as a skeptical research referee. Use Google Search grounding and prioritize
original papers (not secondary summaries). Challenge this proposed 'engineering of
intelligence' hypothesis, with 2026 literature if available:

For a specified task distribution, loss, sensor/tokenizer, architecture family and
training recipe, a multiscale, task-conditional grammar/assembly profile (shortest
reusable description of observation-history-to-action relation + exception cost,
with motif copy counts) might predict the parameter/data scaling frontier better
than raw sensor size or raw assembly index. Pilot runs must calibrate the numerical
map. Hardware fit then depends on token count, compute work, weight precision,
traffic, bandwidth and deadline. There is no universal model-size law.

Specific questions:
1. Is the July 2026 claim that string assembly index equals smallest straight-line
program size valid only under a particular primitive/concatenation definition?
Give the original proof URL and any serious contrary result. Be exact about what
is proven versus contested.
2. Find any primary research that *already* links a task-conditional grammar,
minimum description length, algorithmic complexity, or assembly-style measure to
observed neural scaling exponent or minimum model size across tasks. If none
found, say so. Do not invent a formula.
3. Find strong counterexamples to the proposed descriptor: same raw data with
changed labels; parity/compositional generalization; shortcut learning; code
length that does not correspond to network trainability; sample rarity.
4. Challenge the current prototype: it uses illustrative saturation coverage
curves, a lossy-pooling feature heuristic, a 2P FLOPs/token dense-transformer work
approximation, one weight read during prefill and one per output step, and a
roofline max of compute and bandwidth time. Identify assumptions that most risk
false inference, and concrete safer UI wording.
5. Recommend a falsifiable three-task experimental protocol and the most useful
baselines, metrics, and held-out tests. Distinguish theorem, observed data,
inference and our hypothesis. Name 6-10 original sources with direct URLs and
precise inspected locator where search provides it.

The answer must be concise, adversarial, and candid about what remains unknown.
"""


def main() -> None:
    out = SPACE / 'out'
    out.mkdir(exist_ok=True)
    client = genai.Client(api_key=require('GEMINI_API_KEY'))
    response = client.models.generate_content(
        model='gemini-3.8-flash',
        contents=PROMPT,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())],
            thinking_config=types.ThinkingConfig(thinking_level='HIGH'),
            temperature=0.2,
        ),
    )
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    (out / f'assembly_prompt_{stamp}.txt').write_text(PROMPT, encoding='utf-8')
    (out / f'assembly_response_{stamp}.md').write_text(response.text or '', encoding='utf-8')
    (out / f'assembly_response_{stamp}.json').write_text(
        json.dumps(response.model_dump(mode='json', exclude_none=True), indent=2),
        encoding='utf-8',
    )
    print(f'Saved assembly challenge to {out} ({stamp})')


if __name__ == '__main__':
    main()
