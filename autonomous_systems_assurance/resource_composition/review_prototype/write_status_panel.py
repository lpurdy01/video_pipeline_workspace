#!/usr/bin/env python3
"""Write a renderer-only current compiler-status panel for the review edition."""
from __future__ import annotations
import html
import importlib.util
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("assurance_compiler", PROJECT / "verification/compile.py")
compiler = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(compiler)
result = compiler.compile_project(PROJECT)
score = result["verification_scores"]
case = result["assurance_case_blockers"]
out = Path(__file__).resolve().parent / "out/current_status_panel.html"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(f'''<section class="live-status" aria-label="Current verification status">
<h2>Current compiler status</h2>
<p>This renderer-generated panel is the current status authority for this review edition. It supersedes the static manuscript snapshot in Appendix A when the two differ.</p>
<ul>
<li><strong>Worked-case gate completion:</strong> {score["worked_case_verification_coverage_percent"]:.1f}% ({score["worked_case_passing_packages"]} passing gates of {score["worked_case_packages"]}).</li>
<li><strong>Automated pre-human review:</strong> {score["automated_review_coverage_percent"]:.1f}%.</li>
<li><strong>Human disposition:</strong> {score["human_disposition_coverage_percent"]:.1f}%.</li>
<li><strong>Open case blockers:</strong> {len(case)}.</li>
</ul>
<p>{html.escape(score["label"])}</p>
<p>See the local verification dashboard and report for the package-level queue, retained objections, and source-context limits.</p>
</section>\n''', encoding="utf-8")
