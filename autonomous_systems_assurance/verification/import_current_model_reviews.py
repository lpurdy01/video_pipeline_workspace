#!/usr/bin/env python3
"""Import only digest-current model-review candidates through the compiler gate.

Raw candidates stay in ignored ``verification/out``.  This tool refuses stale
candidates and preserves existing review IDs, so it can be run repeatedly as a
batch finishes.
"""
from __future__ import annotations

import argparse
import json
import sys
import importlib.util
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
OUT = PROJECT / "verification/out/first_pass_model_reviews"
COMPILER = PROJECT / "verification/compile.py"
SPEC = importlib.util.spec_from_file_location("assurance_compiler", COMPILER)
compiler = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(compiler)


def current_pairs() -> set[tuple[str, str]]:
    result = compiler.compile_project(PROJECT)
    return {(item["package_id"], item["input_digest"]) for item in result["queue"]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    pairs = current_pairs()
    imported, skipped = [], []
    existing = {path.stem for path in (PROJECT / "verification/reviews").glob("*.json")}
    for candidate in sorted(OUT.glob("R-MODEL-*-D*.json")):
        record = json.loads(candidate.read_text(encoding="utf-8"))
        key = (record.get("package_id"), record.get("input_digest"))
        destination = PROJECT / "verification/reviews" / (str(record.get("id")) + ".json")
        if key not in pairs:
            skipped.append({"file": candidate.name, "reason": "stale_or_unknown_package"})
            continue
        if destination.exists() or record.get("id") in existing:
            skipped.append({"file": candidate.name, "reason": "already_imported"})
            continue
        if args.limit is not None and len(imported) >= args.limit:
            break
        compiler.check_review(record)
        merged = [compiler.read_json(path) for path in sorted((PROJECT / "verification/reviews").glob("*.json"))]
        compiler.validate_reviews(compiler.indexed(merged + [record], "reviews"))
        with destination.open("x", encoding="utf-8") as handle:
            handle.write(json.dumps(record, indent=2) + "\n")
        existing.add(record["id"])
        imported.append(candidate.name)
    # A final compile detects concurrent mutation and writes the canonical queue.
    compiler.write_outputs(PROJECT, compiler.compile_project(PROJECT))
    print(json.dumps({"imported": imported, "skipped": skipped}, indent=2))


if __name__ == "__main__":
    main()
