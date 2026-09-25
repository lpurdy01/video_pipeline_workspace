#!/usr/bin/env python3
"""Render a local, static verification dashboard from the compiler's live graph."""
from __future__ import annotations

import html
import importlib.util
import json
from collections import defaultdict
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
OUT = PROJECT / "verification/out/dashboard"
SPEC = importlib.util.spec_from_file_location("assurance_compiler", PROJECT / "verification/compile.py")
compiler = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(compiler)


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def status_for(records: list[dict]) -> str:
    verdicts = {record["verdict"] for record in records}
    if "pass" in verdicts:
        return "pass"
    if "fail" in verdicts:
        return "fail"
    if "uncertain" in verdicts:
        return "uncertain"
    return "open"


def main() -> None:
    result = compiler.compile_project(PROJECT)
    OUT.mkdir(parents=True, exist_ok=True)
    reviews = []
    for path in sorted((PROJECT / "verification/reviews").glob("*.json")):
        reviews.append(json.loads(path.read_text(encoding="utf-8")))
    current = defaultdict(list)
    package_by_id = {packet["id"]: packet for packet in result["packages"]}
    for record in reviews:
        packet = package_by_id.get(record["package_id"])
        if packet and packet["input_digest"] == record["input_digest"]:
            current[record["package_id"]].append(record)

    per_claim: dict[str, dict] = {}
    for packet in result["packages"]:
        claim = packet["claim"]
        row = per_claim.setdefault(claim["id"], {
            "id": claim["id"], "text": claim["text"], "scope": claim["scope"],
            "sources": [], "uses": [], "tasks": {}, "worked": bool(packet["assurance_case_links"]),
        })
        for item in packet["evidence"]:
            source = item["source"]
            key = (source["id"], item["region"]["id"])
            if key not in {(x["id"], x["region"]) for x in row["sources"]}:
                row["sources"].append({"id": source["id"], "region": item["region"]["id"], "title": source["title"],
                                       "url": source["url"], "context": item["region"].get("context_status", "unknown"),
                                       "locator": item["region"].get("locator", "")})
        for use in packet["artifact_uses"]:
            if use["path"] not in row["uses"]:
                row["uses"].append(use["path"])
        row["tasks"][packet["task"]] = status_for(current[packet["id"]])

    rows = sorted(per_claim.values(), key=lambda item: item["id"])
    paper_rows = [row for row in rows if "resource_composition/whitepaper.md" in row["uses"]]
    script_rows = [row for row in rows if "video/script.md" in row["uses"]]
    all_contexts = [source["context"] for row in rows for source in row["sources"]]
    task_counts = {task: sum(row["tasks"].get(task) == "pass" for row in rows) for task in compiler.TASKS}
    source_count = sum(len(row["sources"]) for row in rows)
    full_context = sum(value == "full_context" for value in all_contexts)

    data = {"as_of": result["snapshot"]["as_of"], "counts": result["counts"], "verification_scores": result["verification_scores"],
            "rows": rows, "task_counts": task_counts, "source_regions_referenced": source_count,
            "full_context_regions_referenced": full_context, "blockers": result["blockers"],
            "assurance_case_blockers": result["assurance_case_blockers"]}
    (OUT / "data.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    def badge(value: str) -> str:
        return f'<span class="badge {esc(value)}">{esc(value.replace("_", " "))}</span>'
    table_rows = []
    for row in rows:
        sources = "<br>".join(
            f'<a href="{esc(source["url"])}" target="_blank" rel="noreferrer">{esc(source["id"])}: {esc(source["title"])}</a><small>{esc(source["region"])} · {esc(source["context"])} · {esc(source["locator"])}</small>'
            for source in row["sources"])
        uses = "<br>".join(f'<code>{esc(use)}</code>' for use in row["uses"]) or "—"
        task_badges = " ".join(f'{esc(task)} {badge(row["tasks"].get(task, "open"))}' for task in compiler.TASKS)
        filters = " ".join([row["id"], *row["uses"], *[source["context"] for source in row["sources"]], *row["tasks"].values()])
        table_rows.append(f'<tr data-filter="{esc(filters.lower())}"><td><strong>{esc(row["id"])}</strong><br><small>{esc(row["scope"])}</small></td><td>{esc(row["text"])}</td><td>{sources or "—"}</td><td>{uses}</td><td>{task_badges}</td></tr>')

    score = result["verification_scores"]
    document = f"""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Learned Systems Assurance — Verification Dashboard</title>
<style>
:root{{color-scheme:dark;--bg:#101722;--panel:#182231;--line:#2c3b50;--text:#e7eef8;--muted:#9eb0c5;--good:#2cb67d;--warn:#f6bd60;--bad:#ef6f6c;}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font:15px system-ui,sans-serif;line-height:1.45}}main{{max-width:1600px;margin:auto;padding:28px}}h1{{margin:.1rem 0}}p,.note{{color:var(--muted)}}.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px;margin:22px 0}}.card{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:15px}}.num{{font-size:1.75rem;font-weight:700;color:var(--text)}}.label{{font-size:.82rem;color:var(--muted)}}.badge{{display:inline-block;padding:2px 7px;border-radius:999px;font-size:.75rem;margin:1px 2px 1px 0;background:#354254}}.pass{{background:#164d3b;color:#c5f4dd}}.open{{background:#51431c;color:#ffe6a6}}.uncertain{{background:#51431c;color:#ffe6a6}}.fail{{background:#5b292d;color:#ffd6d5}}.controls{{display:flex;gap:8px;flex-wrap:wrap;margin:20px 0}}input{{padding:9px;min-width:290px;border:1px solid var(--line);border-radius:6px;background:#0e1520;color:var(--text)}}button{{padding:8px 10px;border:1px solid var(--line);border-radius:6px;background:var(--panel);color:var(--text)}}table{{border-collapse:collapse;width:100%;background:var(--panel);font-size:.86rem}}th,td{{border:1px solid var(--line);padding:10px;vertical-align:top;text-align:left}}th{{position:sticky;top:0;background:#223047}}small{{display:block;color:var(--muted);margin:3px 0}}a{{color:#82c7ff}}code{{font-size:.79rem}}details{{margin:18px 0;padding:12px;background:var(--panel);border:1px solid var(--line);border-radius:8px}}@media(max-width:800px){{main{{padding:14px}}table{{font-size:.78rem}}th,td{{min-width:150px}}.tablewrap{{overflow:auto}}}}</style>
<main><h1>Verification dashboard</h1><p>As of {esc(result['snapshot']['as_of'])}. This reports research-review completion only. It is <strong>not a safety score</strong>, a certification finding, or a release authorization.</p>
<div class="cards"><div class="card"><div class="num">{result['counts']['claims']}</div><div class="label">active source claims</div></div><div class="card"><div class="num">{len(paper_rows)}</div><div class="label">claims used in whitepaper</div></div><div class="card"><div class="num">{len(script_rows)}</div><div class="label">claims used in recording script</div></div><div class="card"><div class="num">{full_context}/{source_count}</div><div class="label">referenced source regions with full local context</div></div><div class="card"><div class="num">{score['automated_review_coverage_percent']}%</div><div class="label">worked-case pre-human model review</div></div><div class="card"><div class="num">{score['worked_case_verification_coverage_percent']}%</div><div class="label">worked-case review coverage including human gate</div></div></div>
<p class="note">Current pass counts by task: source support {task_counts['source_support']}; adversarial challenge {task_counts['challenge']}; cross-artifact consistency {task_counts['cross_artifact']}; human disposition {task_counts['human_disposition']}. Older reviews whose input changed are deliberately excluded from these current counts.</p>
<div class="controls"><input id="filter" placeholder="Filter claims, sources, paths, statuses …"><button onclick="document.getElementById('filter').value='resource_composition/whitepaper.md';run()">Whitepaper</button><button onclick="document.getElementById('filter').value='video/script.md';run()">Script</button><button onclick="document.getElementById('filter').value='full_context';run()">Full context</button><button onclick="document.getElementById('filter').value='';run()">Reset</button></div>
<div class="tablewrap"><table><thead><tr><th>Claim</th><th>Exact claim</th><th>Primary source and region</th><th>Used by</th><th>Current review tasks</th></tr></thead><tbody>{''.join(table_rows)}</tbody></table></div>
<details><summary>What remains blocked ({len(result['blockers']) + len(result['assurance_case_blockers'])})</summary><ul>{''.join(f'<li>{esc(item)}</li>' for item in (result['assurance_case_blockers'] + result['blockers']))}</ul></details>
<p class="note">Generated locally by <code>verification/render_dashboard.py</code>. Machine-readable data: <a href="data.json">data.json</a>.</p></main>
<script>const q=document.getElementById('filter');function run(){{const v=q.value.toLowerCase();document.querySelectorAll('tbody tr').forEach(r=>r.hidden=!r.dataset.filter.includes(v));}}q.addEventListener('input',run);</script></html>"""
    (OUT / "index.html").write_text(document, encoding="utf-8")
    print(f"Wrote {OUT / 'index.html'}")


if __name__ == "__main__":
    main()
