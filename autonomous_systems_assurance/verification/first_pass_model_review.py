#!/usr/bin/env python3
"""Create conservative Gemini first-pass review records for worked-case claims.

The script writes candidates under ignored verification/out/.  Candidates are
imported only through compile.py, which rechecks their package digest.  It does
not create human-disposition records: those require a real human reviewer.
"""
from __future__ import annotations

import importlib.util
import argparse
import json
import re
import sys
import time
import unicodedata
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Event, Lock
from datetime import date
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
WORKSPACE = PROJECT.parent
OUT = PROJECT / "verification/out/first_pass_model_reviews"
TASKS = ("source_support", "challenge", "cross_artifact")
MODEL = "gemini-3.1-pro-preview"
PROMPT_VERSION = "assurance-first-pass-v2-local-context"

sys.path.insert(0, str(WORKSPACE))
from workspace_credentials import require  # noqa: E402
from google import genai  # noqa: E402
from google.genai import types  # noqa: E402

SPEC = importlib.util.spec_from_file_location("assurance_compiler", PROJECT / "verification/compile.py")
compiler = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(compiler)


def clipped(value: str | None, limit: int) -> str:
    value = value or "[no full local context captured]"
    return value[:limit] + ("\n[truncated]" if len(value) > limit else "")


def context_for_region(item: dict, limit: int = 9000) -> str:
    """Prefer the PDF pages named by the region locator over an arbitrary prefix."""
    context = item.get("context") or "[no full local context captured]"
    locator = item["region"].get("locator", "")
    match = re.search(r"PDF p(?:p?\.)?\s*(\d+)(?:\s*[-–]\s*(\d+))?", locator, re.IGNORECASE)
    pages = context.split("\f")
    if match and len(pages) > 1:
        start = int(match.group(1))
        end = int(match.group(2) or start)
        if 1 <= start <= len(pages):
            selected = "\f".join(pages[start - 1:min(end, len(pages))])
            return clipped(selected, limit)
    # The official Deep Learning HTML chapter is long; the cited underfit/overfit
    # figure is well beyond its first 9,000 characters. Preserve the full captured
    # source on disk, but send the actual cited section to the reviewer.
    if item["region"].get("id") == "S-020-R3":
        normalized = unicodedata.normalize("NFKC", context)
        anchor = normalized.find("Figure 5.3")
        if anchor >= 0:
            return clipped(normalized[max(0, anchor - 2000):anchor + 5500], limit)
    return clipped(context, limit)


def relevant_use_text(content: str, claim_id: str, limit: int = 12000) -> str:
    """Show every tagged use, including uses late in a long manuscript."""
    tag = f"[{claim_id}]"
    positions = [match.start() for match in re.finditer(re.escape(tag), content)]
    if not positions:  # The manifest may bind a figure through explicit claim_ids.
        return clipped(content, limit)
    windows = []
    for pos in positions:
        start, end = max(0, pos - 360), min(len(content), pos + len(tag) + 1050)
        if windows and start <= windows[-1][1]:
            windows[-1] = (windows[-1][0], max(end, windows[-1][1]))
        else:
            windows.append((start, end))
    excerpts = [f"[claim-use {i + 1}/{len(windows)} at character {start}]\n{content[start:end]}"
                for i, (start, end) in enumerate(windows)]
    return clipped("\n...\n".join(excerpts), limit)


def compact_packet(packet: dict) -> dict:
    evidence = []
    for item in packet["evidence"]:
        evidence.append({
            "relation": item["relation"],
            "source": {key: item["source"].get(key) for key in
                       ("id", "title", "publisher", "url", "published_at", "jurisdiction", "inspection_scope", "limitations")},
            "region": {key: item["region"].get(key) for key in ("id", "locator", "excerpt", "context_status")},
            "captured_context": context_for_region(item),
        })
    uses = [{"path": item["path"], "text": relevant_use_text(item["text"], packet["claim"]["id"])}
            for item in packet["artifact_uses"]]
    return {
        "package_id": packet["id"], "task": packet["task"], "claim": packet["claim"],
        "evidence": evidence, "artifact_uses": uses,
        "assurance_case_links": packet["assurance_case_links"],
        "method_crosswalk_links": packet["method_crosswalk_links"],
    }


def prompt_for(packet: dict) -> str:
    task = packet["task"]
    instructions = {
        "source_support": "Assess whether the inspected original context supports the exact claim text, scope, date and status. Do not upgrade a proposed/guidance/research source into approval. Use uncertain when full context is absent or inadequate.",
        "challenge": "Actively seek an alternative interpretation, primary counterevidence, scope limit or current-status change that could defeat the claim. A claim survives only within its stated scope; do not treat failure to find a source as proof of absence.",
        "cross_artifact": "Assess whether every supplied artifact use preserves the claim's scope and limitations. Flag omitted qualifications, changed status, or an inference presented as authority evidence.",
    }[task]
    return f"""You are an independent reviewer for a research verification compiler.

Task: {task}
{instructions}

Return ONLY a JSON object with exactly these fields:
{{
  "verdict": "pass" | "fail" | "uncertain",
  "rationale": "concise explanation tied to claim wording and supplied material",
  "evidence_locators": ["specific source page/section/URL or artifact path"],
  "limitations": ["remaining limitation or search boundary"]
}}

Artifact-use text is excerpted around every occurrence of this claim tag when an artifact is long. Never infer that an omitted section is absent from the full artifact. Review every supplied occurrence, especially later manuscript and narration uses.

`pass` means this review task found the claim accurately supported/challenged/preserved within its stated boundary. It never means the autonomous system is safe. `fail` means the material conflicts with the claim or its use. `uncertain` means the evidence or review search is insufficient. Never invent quotations, a certification, or a human review.

REVIEW PACKET:
{json.dumps(compact_packet(packet), ensure_ascii=False)}"""


def parse_response(text: str) -> dict:
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.IGNORECASE)
    try:
        value = json.loads(cleaned)
    except json.JSONDecodeError:
        start, end = cleaned.find("{"), cleaned.rfind("}")
        if start < 0 or end < start:
            raise
        value = json.loads(cleaned[start:end + 1])
    if value.get("verdict") not in ("pass", "fail", "uncertain"):
        raise ValueError("invalid Gemini verdict")
    if not isinstance(value.get("rationale"), str) or not value["rationale"].strip():
        raise ValueError("missing Gemini rationale")
    for key in ("evidence_locators", "limitations"):
        if not isinstance(value.get(key), list) or not all(isinstance(item, str) for item in value[key]):
            raise ValueError(f"invalid Gemini {key}")
    if not value["evidence_locators"]:
        value["evidence_locators"] = ["Model review packet; no more specific locator returned"]
    return value


def model_slug(model: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "-", model).strip("-")


def record_path(packet: dict, model: str) -> Path:
    return OUT / record_id(packet, model)


def record_id(packet: dict, model: str) -> str:
    """Keep distinct model opinions and stale candidates append-only."""
    return ("R-MODEL-" + model_slug(model) + "-" + packet["id"].removeprefix("P-")
            + "-V" + model_slug(PROMPT_VERSION) + "-D" + packet["input_digest"][:12] + ".json")


def has_current_candidate(packet: dict, model: str) -> bool:
    path = record_path(packet, model)
    if not path.exists():
        return False
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    return (value.get("package_id") == packet["id"]
            and value.get("input_digest") == packet["input_digest"]
            and value.get("prompt_version") == PROMPT_VERSION)


class RequestPacer:
    """Serialize request starts without serializing response processing."""
    def __init__(self, min_interval: float) -> None:
        self.min_interval = min_interval
        self.lock = Lock()
        self.halted = Event()
        self.next_start = 0.0

    def wait(self) -> None:
        if self.halted.is_set():
            raise RuntimeError("Batch stopped after provider quota response; no request sent")
        with self.lock:
            now = time.monotonic()
            delay = max(0.0, self.next_start - now)
            self.next_start = max(now, self.next_start) + self.min_interval
        if delay:
            time.sleep(delay)
        if self.halted.is_set():
            raise RuntimeError("Batch stopped after provider quota response; no request sent")


def review_packet(packet: dict, api_key: str, model: str, pacer: RequestPacer) -> dict:
    pacer.wait()
    client = genai.Client(api_key=api_key)
    prompt = prompt_for(packet)
    # The primary Pro reviewer supports explicit high reasoning; the stable Flash
    # fallback rejects that option. Both retain the same conservative prompt.
    config = (types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="HIGH"), temperature=0.0,
    ) if model == MODEL else types.GenerateContentConfig(temperature=0.0))
    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=config,
        )
    except Exception as exc:
        message = str(exc).lower()
        if "429" in message or "resource_exhausted" in message or "quota" in message:
            pacer.halted.set()
        raise
    raw = response.text or ""
    (OUT / record_id(packet, model).replace(".json", ".raw.md")).write_text(raw, encoding="utf-8")
    try:
        assessment = parse_response(raw)
    except (ValueError, json.JSONDecodeError) as exc:
        assessment = {
            "verdict": "uncertain",
            "rationale": f"Model response could not be parsed as the required review schema: {exc}",
            "evidence_locators": ["raw response retained beside candidate"],
            "limitations": ["No automatic verdict inferred from malformed output"],
        }
    record = {
        "id": record_id(packet, model).removesuffix(".json"),
        "package_id": packet["id"], "input_digest": packet["input_digest"],
        "task": packet["task"], "reviewer_id": "gemini-first-pass", "reviewer_kind": "model",
        "model_id": model, "prompt_version": PROMPT_VERSION,
        "verdict": assessment["verdict"], "created_at": date.today().isoformat(),
        "rationale": assessment["rationale"], "evidence_locators": assessment["evidence_locators"],
        "limitations": assessment["limitations"], "resolves": [],
    }
    record_path(packet, model).write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {"record": record_path(packet, model).name, "package_id": packet["id"], "verdict": record["verdict"]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=1, choices=range(1, 5),
                        help="Concurrent Gemini requests; use a small value to respect provider limits.")
    parser.add_argument("--limit", type=int, default=None,
                        help="Maximum number of not-yet-current candidate records to generate in this run.")
    parser.add_argument("--claim", action="append", default=[],
                        help="Restrict this run to one or more claim IDs; repeat the option as needed.")
    parser.add_argument("--task", action="append", choices=TASKS,
                        help="Restrict to one or more review tasks; repeat as needed.")
    parser.add_argument("--used-by", action="append", default=[],
                        help="Restrict to claims used by one or more manifested artifact paths; repeat as needed.")
    parser.add_argument("--all-claims", action="store_true",
                        help="Review all active claims instead of only claims linked to the worked assurance case.")
    parser.add_argument("--model", default=MODEL,
                        help="Gemini model identifier. A distinct model produces a separately identified second opinion.")
    parser.add_argument("--min-request-interval", type=float, default=15.0,
                        help="Minimum seconds between Gemini request starts across workers (default: 15.0).")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    result = compiler.compile_project(PROJECT)
    worked_ids = {item["claim_id"] for item in result["queue"] if item["claim_id"] in {
        cid for cid, links in ((p["claim"]["id"], p["assurance_case_links"]) for p in result["packages"])
        if links
    }}
    selected_ids = ({packet["claim"]["id"] for packet in result["packages"]}
                    if args.all_claims else worked_ids)
    selected_tasks = set(args.task or TASKS)
    selected_paths = set(args.used_by)
    packets = [packet for packet in result["packages"]
               if packet["claim"]["id"] in selected_ids and packet["task"] in selected_tasks
               and not has_current_candidate(packet, args.model)
               and (not args.claim or packet["claim"]["id"] in set(args.claim))
               and (not selected_paths or any(use["path"] in selected_paths for use in packet["artifact_uses"]))]
    if args.limit is not None:
        packets = packets[:args.limit]
    if args.min_request_interval < 0:
        raise ValueError("--min-request-interval must be nonnegative")
    api_key = require("GEMINI_API_KEY")
    pacer = RequestPacer(args.min_request_interval)
    manifest, errors = [], []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(review_packet, packet, api_key, args.model, pacer): packet for packet in packets}
        for future in as_completed(futures):
            packet = futures[future]
            try:
                manifest.append(future.result())
            except Exception as exc:  # Completed candidates remain importable after a provider limit.
                errors.append({"package_id": packet["id"], "error_type": type(exc).__name__, "message": str(exc)[:500]})
    manifest.sort(key=lambda item: item["package_id"])
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (OUT / "errors.json").write_text(json.dumps(errors, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"candidates": len(manifest), "errors": len(errors), "output": str(OUT)}, indent=2))


if __name__ == "__main__":
    main()
