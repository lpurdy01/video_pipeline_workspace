"""
Gemini 2.5 Pro architectural consultation on Verification Compiler discoveries.
Reads 4 source files, builds prompt, calls API, saves response.
"""
import sys
import os
from pathlib import Path

# Allow importing gemini_client from whitepaper/gemini_tools
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "whitepaper" / "gemini_tools"))
import gemini_client

REPO = Path(__file__).resolve().parents[1]

# --- Read source files ---
learnings = (REPO / "verification_prototype" / "data" / "learnings.md").read_text(encoding="utf-8")
report = (REPO / "verification_prototype" / "data" / "verification_report.md").read_text(encoding="utf-8")
requirements = (REPO / "project_wiki" / "requirements" / "verification_compiler_requirements.md").read_text(encoding="utf-8")

# Whitepaper excerpt: Introduction (lines 1-200) + Concept section (~lines 102-200 already in intro)
# We read the full file and extract three regions:
#   1. Introduction + everything up to line 200 (covers intro + Concept: Verification Compiler start)
#   2. ~150 lines from "## Concept: Verification Compiler" heading
#   3. ~50 lines from "### Verification Readiness Metric"
wp_lines = (REPO / "Introductory_composition.md").read_text(encoding="utf-8").splitlines()

def extract_section(lines, heading, n_lines):
    """Return up to n_lines starting from the first line matching heading."""
    for i, line in enumerate(lines):
        if line.strip().startswith(heading):
            return "\n".join(lines[i : i + n_lines])
    return f"[Section '{heading}' not found]"

intro_excerpt = "\n".join(wp_lines[:200])
concept_excerpt = extract_section(wp_lines, "## Concept: Verification Compiler", 150)
vrm_excerpt = extract_section(wp_lines, "### Verification Readiness Metric", 50)

whitepaper_excerpt = (
    "=== INTRODUCTION (first 200 lines) ===\n\n"
    + intro_excerpt
    + "\n\n=== CONCEPT: VERIFICATION COMPILER (150 lines from heading) ===\n\n"
    + concept_excerpt
    + "\n\n=== VERIFICATION READINESS METRIC (50 lines from heading) ===\n\n"
    + vrm_excerpt
)

# --- Build prompt using string replace (not str.format) ---
PROMPT_TEMPLATE = """You are a senior software architect and verification systems researcher. You are reviewing a research project called the "Verification Compiler" — a hierarchical artifact graph system that decomposes software verification into bounded, independently-auditable queries evaluated by LLMs or human reviewers, producing a Verification Readiness Metric (VRM) on every commit.

The team has just run a prototype of this concept — they applied the verification compiler to verify the whitepaper describing the concept itself. This is a self-referential proof-of-concept run. The results and learnings are in the bundled materials below.

Three key architectural discoveries emerged from the prototype run that the team wants to reason through carefully:

## Discovery 1: Source citations need stable, retrievable region pointers

In the prototype, source citations were stored as prose labels (e.g., "Rierson DO-178C") that were keyword-matched to source summary nodes. This produced 3 of 5 citation failures as builder artifacts — the wrong source was resolved. More fundamentally: the Verification Query Package assembled for a citation check needs to include the ACTUAL TEXT of the cited source region, not just a summary. Without a stable, machine-readable pointer to the exact region being cited, the VQP assembler cannot retrieve the right evidence.

For a code verification system, this is the code unit itself (file path + function name + version hash → deterministic text retrieval). The equivalent for source documents is needed.

Questions for you:
- How should source region identifiers be specified in a verification compiler? What properties must they have (stability, granularity, retrievability)?
- What is the minimum viable source addressing scheme that would work for (a) academic papers, (b) engineering standards (DO-178C), (c) internal project documents?
- How should the artifact graph represent the relationship between a claim and the specific source region that supports it — what schema captures this without becoming unwieldy?

## Discovery 2: Coverage has two dimensions that VRM currently conflates

The prototype VRM formula was: `0.5 × citation_score + 0.5 × coverage_score`. This conflates:
- **Horizontal coverage**: What fraction of in-scope nodes have been evaluated at all?
- **Vertical coverage** (evidence completeness): For evaluated nodes, how complete is the evidence chain? (Has requirement link? Has test artifact? Has test result? Has static analysis result? Are all evidence pieces version-consistent?)

A codebase with 100% horizontal coverage but missing test results everywhere should score differently from 50% horizontal coverage where every evaluated node has a complete evidence chain.

Questions for you:
- How should horizontal and vertical coverage be separately quantified and combined in the VRM?
- What is the right model for "evidence completeness" per node? Should it be binary (complete/incomplete), fractional (N of M required evidence types present), or weighted by evidence type criticality?
- How should version consistency factor in (evidence from a different code version than the one under review)?

## Discovery 3: Model confidence needs empirical calibration, not self-reporting

The prototype used Gemini's self-reported confidence scores. LLMs are known to be poorly calibrated (overconfident on uncertain assessments). The LLM overcorrection finding (arXiv:2603.00539) shows that false positive rate and false negative rate are asymmetric for requirement conformance tasks — models flag correct code as non-compliant more often than they fail to flag non-compliant code. This asymmetry means a single "confidence" number is inadequate.

The VRM should weight each LLM result by:
- The model's empirically measured false negative rate for this specific task type (probability of passing bad code)
- The model's empirically measured false positive rate (probability of flagging good code as bad)
- These rates are task-type specific, not global

But the chicken-and-egg problem: how do you build an accuracy profile for task types the model has never been benchmarked on?

Questions for you:
- What is the right architecture for task-specific model accuracy profiles in a verification compiler? How are they initialized, updated, and used in the VRM formula?
- How should the VRM formula incorporate directional error rates (FPR, FNR) rather than a single confidence number?
- What is the minimum viable approach to bootstrap model accuracy profiles before empirical data is available?
- How does the canary query mechanism (known-negative test injection) fit into this accuracy profile architecture?

## Overall synthesis question:

Given these three discoveries, what changes to the Verification Compiler's core data structures and VRM formula would you recommend? Specifically:
- What nodes and edge types need to be added or modified?
- What is a better VRM formula that properly accounts for coverage dimensionality and calibrated model accuracy?
- What are the 3 most important architectural decisions the team needs to make before Stage 2 implementation that are not yet resolved in the current requirements document?

Please be specific and technical. The team is building an actual system, not just theorizing. Where possible, suggest concrete schemas, formulas, or algorithms. Note where you are speculating vs. where established verification research supports your recommendations.

---

BUNDLED MATERIALS:

[LEARNINGS FROM PROTOTYPE RUN]
LEARNINGS_PLACEHOLDER

[VERIFICATION REPORT (VRM=0.581)]
REPORT_PLACEHOLDER

[SYSTEM REQUIREMENTS]
REQUIREMENTS_PLACEHOLDER

[WHITEPAPER EXCERPT — Key Sections]
WHITEPAPER_PLACEHOLDER"""

prompt = PROMPT_TEMPLATE
prompt = prompt.replace("LEARNINGS_PLACEHOLDER", learnings)
prompt = prompt.replace("REPORT_PLACEHOLDER", report)
prompt = prompt.replace("REQUIREMENTS_PLACEHOLDER", requirements)
prompt = prompt.replace("WHITEPAPER_PLACEHOLDER", whitepaper_excerpt)

print(f"Prompt length: {len(prompt):,} characters")
print("Calling Gemini 3.1 Pro (timeout=300s)...")

response = gemini_client.generate_content(
    model="models/gemini-3.1-pro-preview",
    parts=[{"text": prompt}],
    timeout=300,
)

# Save response
out_path = REPO / "verification_prototype" / "data" / "gemini_architecture_consultation.md"
out_path.write_text(response, encoding="utf-8")
print(f"\nSaved to: {out_path}")
print("\n" + "=" * 80)
print(response)
