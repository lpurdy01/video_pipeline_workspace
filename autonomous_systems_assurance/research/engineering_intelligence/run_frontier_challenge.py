"""Grounded Gemini challenge on best-achievable capacity limits; raw output stays ignored."""
from __future__ import annotations
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
SPACE=Path(__file__).resolve().parent
sys.path.insert(0,str(SPACE.parents[2]))
from workspace_credentials import require
from google import genai
from google.genai import types
PROMPT='''You are an adversarial research mathematician. Use Google Search grounding and cite direct ORIGINAL paper/theorem URLs, exact sections, hypotheses and counterexamples. Date context: September 2026.

We are defining a task-specific best-achievable frontier F*(P,C|task,R,D)=sup fitness over allowed frozen models with at most P parameters and inference compute budget C, fixed observation representation R and data allowance D. The engineering objective is to estimate a NECESSARY model/compute budget for a specified target including hard task slices, not merely explain variation among badly trained models. A published successful model is a lower bound on F* at its budget, not proof that smaller models cannot succeed.

Investigate primary mathematical and empirical sources for:
1. Nontrivial upper bounds on achievable fitness / lower bounds on required model size or computation for specified tasks and architecture classes. Distinguish precise circuit-complexity, approximation-theory, memory/communication, information-theory, streaming, and rate-distortion results from sample-complexity/VC bounds that do not bound representational capacity. Find direct theorems, do not overgeneralize.
2. Model-class approximation + observation Bayes floor + inference roofline as separate necessary constraints. Can these be combined without double counting? Which input quantities are measurable?
3. Empirical upper envelopes or scaling-law extrapolation methods across model size, data and compute, especially image classification, detection, face verification, speech/language and control. How to get uncertainty on unseen best-achievable frontier given a finite architecture/recipe search? Which impossibility conclusions remain unjustified?
4. Could task-conditioned shortest grammar, assembly index/copy number, skill-frequency distribution, or manifold dimension predict frontier location or slope? Identify original assembly paper, critique, MDL and neural-scaling papers. Provide a concrete falsifiable experiment versus task-aware MDL/compression and pilot-only baselines. The same images with changed labels must change the descriptor.
5. Formulate a candidate metatheory in at most 5 precise equations, each labeled theorem under assumptions, measured empirical fit, or new hypothesis. Explain why increasing an at-most-P budget cannot worsen F* but may not improve observed lower-tail performance. What could falsify the proposed task descriptor?

Return at most 15 high-quality primary sources with direct URLs, exact locators and one-sentence scope. Clearly flag any unverified lead. Do not produce numerical parameter minima for real driving/DAA without a validated task specification or bound. Challenge the false step from a best-observed envelope to a universal capacity ceiling.'''

def main():
 out=SPACE/'out';out.mkdir(exist_ok=True)
 client=genai.Client(api_key=require('GEMINI_API_KEY'))
 response=client.models.generate_content(model='gemini-3.8-flash',contents=PROMPT,config=types.GenerateContentConfig(tools=[types.Tool(google_search=types.GoogleSearch())],thinking_config=types.ThinkingConfig(thinking_level='HIGH'),temperature=0.1))
 stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
 (out/f'frontier_prompt_{stamp}.txt').write_text(PROMPT)
 (out/f'frontier_response_{stamp}.md').write_text(response.text or '')
 (out/f'frontier_response_{stamp}.json').write_text(json.dumps(response.model_dump(mode='json',exclude_none=True),indent=2))
 print(f'Saved frontier challenge under {out} ({stamp})')
if __name__=='__main__':main()
