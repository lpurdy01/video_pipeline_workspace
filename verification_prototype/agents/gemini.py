"""
Gemini verification agent — submits VQPs to Gemini and returns structured results.

Reuses gemini_client.py from whitepaper/gemini_tools/.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "whitepaper" / "gemini_tools"))

from gemini_client import generate_content, generate_thinking  # noqa: E402

EVAL_MODEL = "models/gemini-3.1-pro-preview"
THINKING_MODEL = "models/gemini-3.1-pro-preview"


class QuotaExhaustedError(RuntimeError):
    """Raised when the daily per-model quota is exhausted (HTTP 429 RESOURCE_EXHAUSTED).

    The run aborts immediately — cached results from this session are preserved.
    Re-run without --force after the quota resets (~24h).
    """
# REST model for image/visual calls (visual_review.py)
REST_MODEL = "models/gemini-3.1-pro-preview"
PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def _load_prompt(name: str) -> str:
    return (PROMPTS_DIR / f"{name}.txt").read_text(encoding="utf-8")


def _fill_template(template: str, **kwargs: str) -> str:
    """Replace {key} placeholders without interpreting JSON braces as format fields."""
    result = template
    for key, value in kwargs.items():
        result = result.replace("{" + key + "}", value)
    return result


def _parse_json_response(raw: str) -> dict[str, Any]:
    """Extract JSON from Gemini response, handling markdown code blocks."""
    text = raw.strip()
    # Strip markdown code fences if present
    if text.startswith("```"):
        lines = text.split("\n")
        # Remove first and last fence lines
        inner = [l for l in lines if not l.startswith("```")]
        text = "\n".join(inner).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to find JSON object in the response
        start = text.find("{")
        end = text.rfind("}") + 1
        if start >= 0 and end > start:
            try:
                return json.loads(text[start:end])
            except json.JSONDecodeError:
                pass
        return {
            "verdict": "uncertain",
            "confidence": 0.0,
            "rationale": f"Could not parse Gemini response as JSON. Raw: {raw[:300]}",
            "parse_error": True,
        }


def verify_citation(vqp: dict) -> dict:
    """Run a Type A citation verification VQP through Gemini."""
    p = vqp["payload"]

    # Format whitepaper context
    section_parts = []
    for sec in p.get("whitepaper_sections", []):
        section_parts.append(
            f"--- Section: {sec['section_title']} ---\n{sec['text'][:1500]}"
        )
    wp_context = "\n\n".join(section_parts) if section_parts else "(no section context available)"

    prompt_tmpl = _load_prompt("citation_verification")
    prompt = _fill_template(
        prompt_tmpl,
        claim_title=p["claim_title"],
        claim_text=p["claim_text"],
        support_type=p["support_type"],
        evidence_note=p["evidence_note"],
        source_title=p["source_title"],
        source_key_content=p["source_key_content"][:2000],
        whitepaper_context=wp_context[:3000],
    )

    raw = generate_content(model=EVAL_MODEL, parts=[{"text": prompt}], timeout=120)
    result = _parse_json_response(raw)
    result["vqp_id"] = vqp["id"]
    result["vqp_type"] = "citation_verification"
    result["claim_id"] = p["claim_id"]
    result["source_id"] = p["source_id"]
    return result


def verify_coverage(vqp: dict) -> dict:
    """Run a Type B requirement coverage VQP through Gemini."""
    p = vqp["payload"]

    section_parts = []
    for sec in p.get("candidate_sections", []):
        section_parts.append(
            f"--- Section: {sec['section_title']} ---\n{sec['text']}"
        )
    section_texts = "\n\n".join(section_parts) if section_parts else "(no candidate sections found)"

    prompt_tmpl = _load_prompt("requirement_coverage")
    prompt = _fill_template(
        prompt_tmpl,
        requirement_id=p["requirement_id"],
        requirement_title=p["requirement_title"],
        req_num=p["req_num"],
        requirement_text=p["requirement_text"][:2000],
        section_texts=section_texts,
    )

    raw = generate_content(model=EVAL_MODEL, parts=[{"text": prompt}], timeout=120)
    result = _parse_json_response(raw)
    result["vqp_id"] = vqp["id"]
    result["vqp_type"] = "requirement_coverage"
    result["requirement_id"] = p["requirement_id"]
    result["requirement_title"] = p["requirement_title"]
    return result


def run_all_vqps(
    vqps: list[dict],
    results_dir: Path,
    delay_seconds: float = 2.0,
    skip_existing: bool = True,
) -> list[dict]:
    """
    Run all VQPs through Gemini.

    Args:
        vqps: list of VQP dicts from traverser output
        results_dir: where to save individual result JSON files
        delay_seconds: pause between API calls to avoid rate limiting
        skip_existing: if True, skip VQPs with an existing result file

    Returns:
        list of result dicts
    """
    results_dir.mkdir(parents=True, exist_ok=True)
    all_results = []

    type_a = [v for v in vqps if v["vqp_type"] == "citation_verification"]
    type_b = [v for v in vqps if v["vqp_type"] == "requirement_coverage"]
    type_c = [v for v in vqps if v["vqp_type"] == "orphan_detection"]

    print(f"VQPs: {len(type_a)} citation, {len(type_b)} coverage, {len(type_c)} orphan")

    # Type C: no Gemini call needed
    for vqp in type_c:
        result = {
            "vqp_id": vqp["id"],
            "vqp_type": "orphan_detection",
            "findings": vqp["payload"]["findings"],
        }
        _save_result(result, results_dir)
        all_results.append(result)

    total = len(type_a) + len(type_b)
    done = 0

    for vqp in type_a:
        result_path = results_dir / f"{_safe_filename(vqp['id'])}.json"
        if skip_existing and result_path.exists():
            print(f"  [skip] {vqp['id'][:60]}")
            all_results.append(json.loads(result_path.read_text()))
            done += 1
            continue

        done += 1
        print(f"  [{done}/{total}] A: {vqp['id'][:70]}")
        try:
            result = verify_citation(vqp)
        except Exception as e:
            err_str = str(e)
            if "429" in err_str and ("RESOURCE_EXHAUSTED" in err_str or "quota" in err_str.lower()):
                print(f"\n  [QUOTA EXHAUSTED] Daily limit reached after {done-1} VQPs.")
                print(f"  Cached results from this session are preserved.")
                print(f"  Re-run without --force after the quota resets (~24h).")
                raise QuotaExhaustedError(err_str) from e
            result = {
                "vqp_id": vqp["id"],
                "vqp_type": "citation_verification",
                "verdict": "uncertain",
                "confidence": 0.0,
                "rationale": f"API error: {e}",
                "claim_id": vqp["payload"]["claim_id"],
                "source_id": vqp["payload"]["source_id"],
                "api_error": True,
            }
        _save_result(result, results_dir)
        all_results.append(result)
        time.sleep(delay_seconds)

    for vqp in type_b:
        result_path = results_dir / f"{_safe_filename(vqp['id'])}.json"
        if skip_existing and result_path.exists():
            print(f"  [skip] {vqp['id'][:60]}")
            all_results.append(json.loads(result_path.read_text()))
            done += 1
            continue

        done += 1
        print(f"  [{done}/{total}] B: {vqp['id'][:70]}")
        try:
            result = verify_coverage(vqp)
        except Exception as e:
            err_str = str(e)
            if "429" in err_str and ("RESOURCE_EXHAUSTED" in err_str or "quota" in err_str.lower()):
                print(f"\n  [QUOTA EXHAUSTED] Daily limit reached after {done-1} VQPs.")
                print(f"  Cached results from this session are preserved.")
                print(f"  Re-run without --force after the quota resets (~24h).")
                raise QuotaExhaustedError(err_str) from e
            result = {
                "vqp_id": vqp["id"],
                "vqp_type": "requirement_coverage",
                "verdict": "uncertain",
                "confidence": 0.0,
                "rationale": f"API error: {e}",
                "requirement_id": vqp["payload"]["requirement_id"],
                "requirement_title": vqp["payload"]["requirement_title"],
                "api_error": True,
            }
        _save_result(result, results_dir)
        all_results.append(result)
        time.sleep(delay_seconds)

    return all_results


def _safe_filename(vqp_id: str) -> str:
    import re
    return re.sub(r"[^a-zA-Z0-9_-]", "_", vqp_id)[:80]


def _save_result(result: dict, results_dir: Path) -> None:
    fname = _safe_filename(result["vqp_id"]) + ".json"
    (results_dir / fname).write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )
