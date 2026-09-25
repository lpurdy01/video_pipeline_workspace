# Thumbnail and Packaging A/B Cases

Workspace: `verification_compiler_video/thumbnail_ab_codex/`

Generated 2026-08-28 for **The Compiler For Trust**.

## What Changed From The Previous Video

The previous launch kit for "LLMs Aren't Chatbots - They're a Transform" worked
best when it used:

- real rendered frames, not AI-generated texture;
- one sharp thesis on the thumbnail;
- huge high-contrast text;
- a curiosity gap that stayed close to the video promise.

This round pushes harder on emotional immediacy. The prior strongest thumbnail
was a conceptual reframing: "LLMs aren't chatbots." The stronger move here is a
workplace anxiety the viewer already feels: "AI can write it. Who checks it?"

## Gemini Review Summary

Initial review file:
`gemini_thumbnail_review_2026-08-28.md`

Final spot review file:
`gemini_thumbnail_review_final_2026-08-28.md`

Cleanup review file:
`gemini_thumbnail_cleanup_review_2026-08-29.md`

Gemini ranked the initial concepts:

1. **A - Who Checks It?** Best cold-feed hook. Broad anxiety, high urgency.
2. **B - Chat Is Not Evidence.** Strong contrarian hook. Best thesis match.
3. **C - Trust Is The Bottleneck.** Accurate but too B2B/abstract.
4. **D - Compiler For Trust.** Accurate but too solution-first for cold viewers.

Those rankings applied to the v1 art, which was rejected. See `REBUILD_NOTES.md`
for what was wrong and how the current v2 thumbnails were rebuilt. The Gemini
reviews remain useful only as mobile-readability checks; they drove the rejected
cleanup pass and should not be treated as the authority on taste.

Current on-thumbnail text:

- **A:** WHO CHECKS / THE CODE? + chip "AI CAN WRITE IT"
- **B:** CHAT IS NOT / EVIDENCE + chip "NO AUDIT TRAIL"
- **C:** TRUST IS / THE BOTTLENECK + chip "GENERATION GOT CHEAP"
- **D:** COMPILER / FOR TRUST + chip "AI WRITES IT. HUMANS SIGN IT."

## Recommended A/B Test

Run **A vs B**.

These test different click motives, not cosmetic variations:

- **A tests anxiety/overwhelm:** "My agent is producing more code than my team
  can review."
- **B tests rigor/contrarian standards:** "A confident chatbot answer is not an
  engineering evidence record."

Given the current preference for B and D, a second viable test is **B vs D**:

- **B tests the problem/friction:** chat is not evidence.
- **D tests the named solution:** a compiler-like workflow involving AI review,
  human authority, and preserved evidence.

Gemini still expects A/B to win the cold feed. B/D is the better test if the
goal is to learn whether the audience responds more to the critique or to the
architecture itself.

## Case A - Broad Hook

Thumbnail:
`thumb_A_who_checks_it.png`

On-thumbnail text:

```text
WHO CHECKS
THE CODE?

AI CAN WRITE IT
```

Primary title:

```text
AI Can Write Code. Who Checks It?
```

Alternate titles:

```text
AI Made Coding Cheap. Trust Is Still Expensive.
The AI Code Review Bottleneck
The Verification Problem AI Did Not Solve
```

Best use:
Default public launch. This is the strongest top-of-funnel packaging because it
names the pain before introducing the solution.

## Case B - Rigor Hook

Thumbnail:
`thumb_B_chat_not_evidence.png`

On-thumbnail text:

```text
CHAT IS NOT
EVIDENCE

NO AUDIT TRAIL
```

Primary title:

```text
A Chat Transcript Is Not Evidence
```

Alternate titles:

```text
AI Code Review Needs Evidence, Not Vibes
The Problem With Letting AI Check Its Own Work
The Compiler For Trust
```

Best use:
Niche/credibility test. This may attract fewer casual viewers than A, but it
matches the whitepaper thesis more precisely and should resonate with assurance,
verification, and senior engineering audiences.

## Case D - Architecture Hook

Thumbnail:
`thumb_D_compiler_for_trust.png`

On-thumbnail text:

```text
COMPILER
FOR TRUST

AI REVIEW + HUMAN
```

Primary title:

```text
The Compiler For Trust
```

Alternate titles:

```text
An AI Workflow For Evidence, Not Vibes
What Comes After AI Code Generation?
From AI Review To Human Sign-Off
```

Best use:
Architecture-forward test. This is less visceral than A or B, but it now shows
the actual mechanism: requirements/code/tests become a VQP, AI participates in
review, humans retain authority, and the system preserves evidence.

## Description Draft - Case A

Use with title: `AI Can Write Code. Who Checks It?`

```text
Your agent wrote code, tests, docs, and a migration plan this week.

How much of it did you actually read?

AI made generating software cheap. It did not make trusting software cheap. This video is about the bottleneck that appears next: verification.

In high-assurance software, serious work is not just code that runs. It is code tied to requirements, tests, results, source documents, review records, versions, and human authority. That structure is what keeps aircraft, medical devices, vehicles, and other high-stakes systems reviewable.

The idea I am exploring here is a Verification Compiler: a process that turns a project into an artifact graph, traverses that graph deterministically, assembles bounded Verification Query Packages, lets models help during development, keeps humans authoritative where it matters, and records the result as inspectable evidence.

Not "trust the AI."

Trust the evidence surface.

WHITEPAPER AND RESOURCES
[whitepaper/resources link]

CHAPTERS
0:00 Generation got cheap
TBD The hidden cost of "looks good"
TBD Safety-critical software already has the shape
TBD Artifacts become a graph
TBD Compilation means traversal
TBD The Verification Query Package
TBD Same package, two review modes
TBD Evidence cards, not conversations
TBD Verification readiness is a map, not magic
TBD The future is evidence generation

NOTES
This is a whitepaper-level idea and prototype direction, not a finished product or a claim that AI can certify safety-critical software. Model review is developmental unless a qualified human process promotes it. The goal is to preserve and accelerate verification scaffolding, not bypass it.

KEYWORDS
AI agents, software verification, software assurance, requirements traceability, LLM evaluation, safety-critical software, DO-178C, ISO 26262, evidence generation
```

## Description Draft - Case B

Use with title: `A Chat Transcript Is Not Evidence`

```text
You can ask a model to write code.

You can ask the same model whether the code satisfies the requirement.

It may give you a calm, useful answer. But what do you actually have?

No reproducible package. No versioned test result. No source-region citation. No structured reviewer record. No audit trail.

You have a chat transcript.

And a chat transcript is not evidence.

This video is about the verification problem that appears as AI-generated software gets cheaper: how do we turn fast generation into reviewable, inspectable evidence?

The proposed answer is a Verification Compiler: an artifact graph, deterministic traversal, bounded Verification Query Packages, developmental model review, human authority where it matters, and durable evidence records that can go stale without disappearing.

Not "trust the AI."

Trust the evidence surface.

WHITEPAPER AND RESOURCES
[whitepaper/resources link]

CHAPTERS
0:00 Generation got cheap
TBD The hidden cost of "looks good"
TBD Safety-critical software already has the shape
TBD Artifacts become a graph
TBD Compilation means traversal
TBD The Verification Query Package
TBD Same package, two review modes
TBD Evidence cards, not conversations
TBD Verification readiness is a map, not magic
TBD The future is evidence generation

NOTES
This is not a shortcut around certification. It is a proposal for making AI-assisted development more reviewable by preserving requirements, versions, test evidence, citations, reviewer identity, and authority boundaries.
```

## Pinned Comment

```text
The core claim: as generation gets cheap, verification becomes the bottleneck. The question is not "can AI write code?" It is "can we produce evidence a human can inspect, reproduce, and trust?" Whitepaper/resources are in the description.
```

## LinkedIn Post

```text
AI made generating code cheap.

It did not make trusting code cheap.

That is the bottleneck I keep coming back to. Agentic development can produce code, tests, docs, migration plans, and review notes faster than a team can actually inspect them. But serious software is not just software that runs. It is software where someone can explain what requirement it satisfies, what test verified it, what version the result belongs to, what evidence was produced, and who accepted it.

I made a video and whitepaper around an idea I am calling a Verification Compiler.

The rough shape:

- turn the project into an artifact graph;
- traverse that graph deterministically;
- assemble bounded Verification Query Packages;
- let models help during development;
- keep humans authoritative where it matters;
- preserve the result as evidence.

Not "trust the AI."

Trust the evidence surface.

The thing I want to test next is whether this can become practical engineering infrastructure, not just a good diagram.

Video: [link]
Whitepaper/resources: [link]

#AI #SoftwareEngineering #Verification #SoftwareAssurance #AIAgents #RequirementsEngineering
```

## Files

- `make_thumbnails.py` - deterministic generator.
- `review_thumbnails.py` - Gemini review wrapper using existing repo Gemini helper.
- `thumbnail_manifest.json` - generated candidate metadata.
- `thumbnail_contact_sheet.jpg` - 2x2 full-size candidate sheet.
- `thumbnail_mobile_preview.jpg` - small feed-size preview.
- `thumb_A_who_checks_it.png` - recommended A.
- `thumb_B_chat_not_evidence.png` - recommended B.
- `thumb_C_bottleneck_trust.png` - backup, too abstract for launch.
- `thumb_D_compiler_for_trust.png` - redesigned architecture-forward option
  with explicit AI/human/evidence path.
