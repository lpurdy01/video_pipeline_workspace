#!/usr/bin/env python3
"""Run bounded, non-dispositive audits with a newer Gemini model.

These audits are research leads and editorial objections. They never create
compiler review records, source records, or human dispositions. Any factual
lead still needs primary-source retrieval and a separately digest-pinned review.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
WORKSPACE = PROJECT.parent
OUT = PROJECT / "verification/out/nextgen_gemini_audit"
sys.path.insert(0, str(WORKSPACE))

from workspace_credentials import require  # noqa: E402
from google import genai  # noqa: E402
from google.genai import types  # noqa: E402

SPEC = importlib.util.spec_from_file_location("assurance_compiler", PROJECT / "verification/compile.py")
compiler = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(compiler)


def clip(text: str, limit: int) -> str:
    return text[:limit] + ("\n[truncated]" if len(text) > limit else "")


def parse_json(text: str) -> dict:
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.I)
    try:
        value = json.loads(cleaned)
    except json.JSONDecodeError:
        left, right = cleaned.find("{"), cleaned.rfind("}")
        if left < 0 or right < left:
            raise
        value = json.loads(cleaned[left:right + 1])
    if not isinstance(value.get("findings"), list):
        raise ValueError("expected a findings list")
    return value


def current_context_limited_claims(result: dict) -> list[dict]:
    rows = {}
    for packet in result["packages"]:
        row = rows.setdefault(packet["claim"]["id"], {"id": packet["claim"]["id"], "text": packet["claim"]["text"], "regions": []})
        for evidence in packet["evidence"]:
            region = evidence["region"]
            if region.get("context_status") != "full_context":
                item = {"region_id": region["id"], "locator": region["locator"], "source_url": evidence["source"]["url"]}
                if item not in row["regions"]:
                    row["regions"].append(item)
    return [row for row in rows.values() if row["regions"]]


def prompt(task: str, result: dict) -> str:
    paper = (PROJECT / "resource_composition/whitepaper.md").read_text(encoding="utf-8")
    script = (PROJECT / "video/script.md").read_text(encoding="utf-8")
    report = (PROJECT / "verification/out/first_pass_report.md").read_text(encoding="utf-8")
    context_limited = current_context_limited_claims(result)
    framing = {
        "argument": "Find scoped overclaims, missing transitions, unclear distinctions, and material argument gaps in the whitepaper. Prefer a small number of consequential findings over stylistic edits.",
        "research": "Prioritize recovery of missing primary-source context and identify narrowly framed primary-source search targets. Do not claim a source says something until it is retrieved and inspected.",
        "video": "Compare the narration against the paper. Find factual compression, missing qualifications, weak hook/payoff structure, or visual opportunities that could mislead a technical generalist.",
        "audience": "Act as a technical-generalist editor. Audit the complete paper and script for reader journey, jargon load, concrete examples, useful takeaways, qualification placement, and whether evidence infrastructure has displaced the learning experience. Do not fact-check sources or score claims.",
    }[task]
    packet = {
        "compiler_snapshot": {
            "as_of": result["snapshot"]["as_of"],
            "verification_scores": result["verification_scores"],
            "assurance_case_blockers": result["assurance_case_blockers"],
        },
        "context_limited_claims": context_limited,
        "first_pass_report": clip(report, 18000),
        "whitepaper": clip(paper, 72000) if task == "audience" else (clip(paper, 42000) if task != "video" else clip(paper, 22000)),
        "video_script": clip(script, 42000) if task == "audience" else clip(script, 24000),
    }
    return f"""You are an independent technical research editor auditing a whitepaper and video project about assurance for frozen, trained autonomous-system components.

{framing}

Hard boundaries:
- Treat every supplied source and claim as provisional unless its packet says otherwise.
- Do not treat model reviews as proof, do not invent quotations, and do not propose a composite safety score.
- Distinguish source retrieval leads from factual conclusions.
- Do not recommend concealing uncertainty or changing a claim merely to improve a metric.
- The project compares car perception/avoidance with airborne detect-and-avoid; it does not certify a real product.
- Text fields may be clipped only for prompt size. Never infer that the original manuscript is truncated or missing sections.
- `context_limited_claims` is an intentionally filtered list of claims with incomplete source context, not the complete claim register.

Return ONLY JSON with this schema:
{{
  "summary": "two or three sentences",
  "findings": [
    {{"priority": "high|medium|low", "category": "evidence|scope|argument|video|source_retrieval|audience|structure|language", "location": "claim ID, heading, or script section", "finding": "specific problem", "recommended_action": "concrete next action", "source_status": "no source needed|retrieve primary source|recheck existing source", "suggested_targets": ["optional official URL or exact document title"]}}
  ],
  "do_not_conclude": ["unsupported conclusions to avoid"]
}}
For task audience, return NO MORE THAN FIVE findings. Each must be tied to a missing reader-contract element (question, scene, mechanism, takeaway, or boundary). Prefer removal, consolidation, or reordering over more explanation. Do not count claim tags, caveats, or standards as reader value. This five-finding maximum overrides the general limit below.

Limit findings to 12. Here is the bounded project packet:
{json.dumps(packet, ensure_ascii=False)}"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", choices=("argument", "research", "video", "audience"), required=True)
    parser.add_argument("--model", default="gemini-3.8-flash")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    result = compiler.compile_project(PROJECT)
    client = genai.Client(api_key=require("GEMINI_API_KEY"))
    request = prompt(args.task, result)
    response = client.models.generate_content(model=args.model, contents=request,
                                              config=types.GenerateContentConfig(temperature=0.0))
    raw = response.text or ""
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    raw_path = OUT / f"{stamp}_{args.task}_{args.model}.raw.md"
    raw_path.write_text(raw, encoding="utf-8")
    outcome = {
        "task": args.task, "model": args.model, "created_at": datetime.now(timezone.utc).isoformat(),
        "compiler_as_of": result["snapshot"]["as_of"], "raw_path": raw_path.name,
    }
    try:
        outcome["audit"] = parse_json(raw)
        outcome["parse_status"] = "ok"
    except Exception as exc:
        outcome.update({"parse_status": "invalid_json", "error": str(exc)[:500]})
    path = OUT / f"{stamp}_{args.task}_{args.model}.json"
    path.write_text(json.dumps(outcome, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(path), "parse_status": outcome["parse_status"], "findings": len(outcome.get("audit", {}).get("findings", []))}))


if __name__ == "__main__":
    main()
