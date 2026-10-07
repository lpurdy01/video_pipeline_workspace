"""One grounded cross-domain source scout; raw response remains ignored under out/."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

SPACE = Path(__file__).resolve().parent
sys.path.insert(0, str(SPACE.parents[2]))
from workspace_credentials import require  # noqa: E402
from google import genai  # noqa: E402
from google.genai import types  # noqa: E402

PROMPT = """You are an adversarial research librarian for a proposed engineering-of-intelligence
fitment explorer. Use Google Search grounding. Find *primary* original papers,
official model documentation, vendor technical specifications, and government
research reports. Search current material through September 2026. Return DIRECT
source URLs and exact table/section or abstract locators. Never infer a deployed
system's learned-model size or certified safety from chip specifications.

We need at least 40 real numeric, citable datapoints for graphs, including at least
10 widely recognizable cases, across groups that must stay separate:
A. Comparable ImageNet-1K model accuracy vs parameter count and GFLOPs for AlexNet,
VGG, ResNet, MobileNet, EfficientNet, ViT, Swin, ConvNeXt, etc. Prefer official
TorchVision weight metadata/table and record weights version, input resolution,
accuracy definition, FLOPs scope. A model variant can be a point.
B. Face-recognition verification, e.g. DeepFace, FaceNet, ArcFace, MobileFaceNet.
Only report TAR/FAR or LFW accuracy with its actual protocol; parameter/FLOP/latency
when source actually supplies it. Do not compare these accuracy percentages to ImageNet.
C. Detect-and-avoid or aircraft detection vision pipelines: find original NASA,
FAA, Air Force, journal or conference reports with explicit sensor resolution,
detection range, frame rate, latency, recall/FAR, or model size. Separate
cooperative surveillance, radar, optical, and learned perception. Do not
substitute ACAS-X logic for camera ML.
D. Tesla FSD Computer HW3, HW4/AI4, proposed HW5/AI5: official Tesla statements
or public company filings only for quantitative specs, with year/date and whether
system-level, per-chip, estimated, claimed, or hypothesized. Include chip TOPS,
compute power, camera resolution/count, bandwidth/DRAM if actually public. Report
unknowns and contradictions; no guessed network parameters. Also NVIDIA automotive
or Jetson and other independently spec'd inference hardware as reference.

For every point: case_id, name, domain, metric name, numeric value and unit,
model/hardware version, evaluation/input condition, source title/URL and precise
locator, source status, and what cannot be concluded. Give candidate video-ready
pairs/graphs that preserve metric comparability. Flag sources that are only
abstracts, search snippets, paywalled, or marketing. Distinguish published
observations, vendor specs, estimates, and explicit hypotheses.

Finally challenge the metatheory: identify 5 confounds that defeat naive
complexity-to-parameter extrapolation; recommend an auditable data schema and
which axes deserve separate panels. If 40 points cannot be substantiated from
primary material, give fewer and say so. No invented values, no substituted URLs.
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
            temperature=0.1,
        ),
    )
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    (out/f'cross_domain_prompt_{stamp}.txt').write_text(PROMPT,encoding='utf-8')
    (out/f'cross_domain_response_{stamp}.md').write_text(response.text or '',encoding='utf-8')
    (out/f'cross_domain_response_{stamp}.json').write_text(json.dumps(response.model_dump(mode='json',exclude_none=True),indent=2),encoding='utf-8')
    print(f'Saved cross-domain scout under {out} ({stamp})')

if __name__=='__main__':
    main()
