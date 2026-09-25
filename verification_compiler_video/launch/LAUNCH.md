# Launch kit — *The Compiler For Trust*

Everything needed to publish video 2. Written 2026-08-29.

| File | Use |
|---|---|
| `../out/final/compiler_for_trust_clean_1080p30_1x_1.15x.mp4` | **The video to upload** (1920×1080, 30fps, 1.15×, 11:32) |
| `../out/final/compiler_for_trust_clean_1080p30_1x.mp4` | 1.0× master (13:16). Editing baseline; upload only if you reject the 1.15× |
| `captions_en_1.15x.srt` | English captions for the 1.15× cut — **upload this one** |
| `captions_en_1x.srt` | English captions for the 1.0× master |
| `../thumbnail_ab_codex/thumb_A_who_checks_it.png` | Thumbnail A — "Who Checks The Code?" |
| `../thumbnail_ab_codex/thumb_B_chat_not_evidence.png` | Thumbnail B — "Chat Is Not Evidence" |
| `../thumbnail_ab_codex/thumb_C_bottleneck_trust.png` | Thumbnail C — "Trust Is The Bottleneck" |

Captions are built from the locked script text in `drafts/script.md` carried
through `out/timing/*.timing.json`, not from ASR, so "Verification Query Package"
and "Verification Readiness Metric" cannot come out mangled. Times come from the
local faster-whisper alignment. Regenerate with `python3 make_captions.py`.
222 cues, no overlaps, ≤2 lines, ≤6.5s each. Still skim it once.

---

## ⚠ Decide before you upload

**Visual QA has not passed.** Sections 2–11 carry 29 findings: 16 are
`stage_imbalance` (which you deprioritised) and 13 are short transients, mostly
a 0.5–2s outline crossing a label mid-animation. Section 1 is clean. None of
this is a timing or audio problem — the cut is coherent end to end — but it is
your call whether the 13 transients ship. See `PIPELINE_STATUS.md`.

**Confirm the companion repo is public.** Every link in the description points at
`github.com/lpurdy01/verification_compiler_resources`. It is committed and in
sync with origin (`065f716`), and all 13 linked paths exist in the working tree —
but I can't check its visibility setting from here. If it is still private, every
link in the description 404s for viewers on launch day. Open it in a logged-out
browser before you publish.

---

## Upload checklist

1. Upload `compiler_for_trust_clean_1080p30_1x_1.15x.mp4`. Visibility **Unlisted**
   first, watch it once end to end, then Public or scheduled (Tue–Thu, ~9–11am ET).
2. Title: one fixed title for the whole test — see below.
3. Paste the description below. Chapters auto-detect from it — confirm the chapter
   strip appears on the watch page before making it public.
4. Subtitles → English → upload `captions_en_1.15x.srt`.
5. Thumbnails: Studio → *Test & compare* → upload A, B and C (see below).
6. Playlist: add to **The Compiler For Trust** or a "Verification" playlist —
   frames this as a series alongside the transform video.
7. Audience: **"No, it's not made for kids."**
8. End screen: last ~20s of the end card. Add a *Subscribe* element and a
   *Video/playlist → Most recent upload* element.
9. Pin the comment below immediately after publishing.
10. Post the LinkedIn within 30–60 minutes and reply to early comments.

---

## Title (one, fixed across the test)

*Test & compare* varies the thumbnail against **one** title, so there is a single
title to choose — and it should not repeat what the thumbnail already says. The
thumbnail and title are two slots; spending both on the same sentence wastes one.
Each thumbnail here already states a thesis, so the title's job is to add the
idea none of them carry: that there is a category of software AI is *barred*
from, and it is barred for a reason.

**Recommended:**

```text
The Software AI Isn't Allowed To Write
```

It is the video's own opening line ("there is a whole category of software that
AI is not allowed to write"), so the payoff lands in the first fifteen seconds.
It shares no words with any of the three thumbnails, and it opens a question none
of them ask — *which* software, and who decided?

How it reads against each thumbnail:

| Thumbnail | Says | Title adds |
|---|---|---|
| A — WHO CHECKS THE CODE? | nobody is auditing the volume | …and some of it is off-limits entirely |
| B — CHAT IS NOT EVIDENCE | approval is not a record | …which is why some domains won't take it |
| C — TRUST IS THE BOTTLENECK | the scarce thing is verification | …enforced as a hard line in some fields |

**Alternates**, roughly in the order I'd try them:

```text
Aviation Solved This Decades Ago. Software Didn't.
Your Agent Wrote 4,000 Lines This Week
AI Code Doesn't Need Review. It Needs Receipts.
From Code Generation To Evidence Generation
```

- *Aviation…* — strongest curiosity gap after the recommendation, and it sets up
  the traceability argument. Slightly narrower: it signals "aerospace video" to
  people who aren't sure they care.
- *Your Agent Wrote 4,000 Lines…* — the most relatable and the literal first line
  of the video, but it leans the same direction as thumbnail A, so the pairing
  gets redundant on one of the three.
- *…It Needs Receipts.* — punchiest and most modern, but "receipts" may read as
  flip to the certification audience you're trying to reach.
- *From Code Generation To Evidence Generation* — the truest summary and the
  weakest cold hook. Good candidate if you re-title later for search.

Avoid `The Compiler For Trust` as the published title — it is the series/brand
name and means nothing to someone who hasn't watched. Keep it for the playlist.

---

## YouTube description (copy-paste)

```text
There is a whole category of software that AI is not allowed to write. Aircraft. Medical devices. Not because the models are bad at it — because nobody can check the work fast enough to keep the standards intact.

AI made writing code cheap. It did not make trusting code cheap. That's a verification problem, which means I think it's solvable.

If an agent wrote four thousand lines this week, the bottleneck is no longer writing the next four thousand — it's showing that any of it does what you said it would. This video works through a proposal I've been calling the Verification Compiler: turn a project into a graph of artifacts, traverse it deterministically to assemble bounded review packages, let models help during development, keep humans in authority, and preserve the result as evidence you can inspect.

The core move: a chat transcript is not an audit trail. "Looks good to me" from a model is a developmental signal, not a record. An evidence card — which requirement, which artifact version, which check, which result, who reviewed it — is a record.

Safety-critical software already has this shape — avionics and automotive have carried requirement-to-evidence traceability for decades. The argument is that as generation gets cheaper, ordinary software needs the same shape, and the tooling to produce it can finally be built.

CHAPTERS
0:00 Generation got cheap
1:50 The hidden cost of "looks good"
2:34 Safety-critical software already has the shape
4:21 Artifacts become a graph
5:20 Compilation means traversal
6:10 The Verification Query Package
7:16 Same package, two review modes
8:05 Evidence cards, not conversations
8:45 Verification readiness is a map, not magic
9:48 The future is evidence generation
10:30 Where this goes next

COMPANION REPO — whitepaper, evidence, and agent handoff
https://github.com/lpurdy01/verification_compiler_resources

Whitepaper (PDF)
https://github.com/lpurdy01/verification_compiler_resources/blob/main/whitepaper/verification_compiler_whitepaper.pdf

Whitepaper (Markdown — best for GitHub or agent context)
https://github.com/lpurdy01/verification_compiler_resources/blob/main/whitepaper/verification_compiler_whitepaper.md

The concept map, one page
https://github.com/lpurdy01/verification_compiler_resources/blob/main/CONCEPT_MAP.md

What this is NOT — boundaries, please read before quoting me
https://github.com/lpurdy01/verification_compiler_resources/blob/main/BOUNDARIES.md

BUILD YOUR OWN VERSION
If you work with coding agents, point one at these and have it build its own version. Tell me in the comments how it went.

Agent handoff
https://github.com/lpurdy01/verification_compiler_resources/blob/main/FOR_AGENTS.md

Agent brief
https://github.com/lpurdy01/verification_compiler_resources/blob/main/agent_resources/agent_brief.md

Implementation conversation guide
https://github.com/lpurdy01/verification_compiler_resources/blob/main/agent_resources/implementation_conversation_guide.md

Critique checklist
https://github.com/lpurdy01/verification_compiler_resources/blob/main/agent_resources/critique_checklist.md

Open questions — what I have not solved
https://github.com/lpurdy01/verification_compiler_resources/blob/main/agent_resources/open_questions.md

EVIDENCE TRAIL
I ran the idea against its own whitepaper as a self-verification prototype:

Evidence bundle
https://github.com/lpurdy01/verification_compiler_resources/tree/main/evidence

Claim support summary
https://github.com/lpurdy01/verification_compiler_resources/blob/main/evidence/claim_support_summary.md

Source-to-claim matrix
https://github.com/lpurdy01/verification_compiler_resources/blob/main/evidence/source_to_claim_matrix.md

Prototype verification report
https://github.com/lpurdy01/verification_compiler_resources/blob/main/evidence/verification_report.md

A NOTE ON TERMS
"Verification Compiler," "Verification Query Package (VQP)," "evidence card," and "Verification Readiness Metric" are my own framings, not established industry jargon. I use them to make the idea concrete enough to argue with.

WHAT THIS IS NOT
This is a Stage 1 research and discussion package, not a product and not a certified process. Nothing here claims an LLM can certify safety-critical software, or that a readiness number means a system is safe. Sign-off stays organisational and process-driven — the regulator signs off, and that endpoint does not move. A readiness metric says the evidence surface is more or less complete, current, and reviewed. It makes gaps visible. That is all it does, and it is still worth having.

Verification is checking you built the thing you specified. Validation is checking it was the right thing to build. This is aimed at the first one.

—
Next up: I'm going to build it. Subscribe if you want to know when that lands, and if you know someone who has to get software through a certification process, send this to them — that's the conversation I'm hoping to start.
```

*(4942 characters — YouTube's limit is 5000, so there is room for about 55 more
if you want to add a line. The chapter block must keep a 0:00 entry or the
strip will not render.)*

### Chapters for the 1.0× master

Only if you upload `compiler_for_trust_clean_1080p30_1x.mp4` instead:

```text
0:00 Generation got cheap
2:07 The hidden cost of "looks good"
2:58 Safety-critical software already has the shape
5:00 Artifacts become a graph
6:08 Compilation means traversal
7:05 The Verification Query Package
8:22 Same package, two review modes
9:18 Evidence cards, not conversations
10:04 Verification readiness is a map, not magic
11:16 The future is evidence generation
12:05 Where this goes next
```

---

## Pinned comment

```text
The whole argument in one line: a chat transcript is not an audit trail, and as generation gets cheaper the scarce thing becomes evidence you can inspect.

If you work with coding agents, the repo has an agent handoff written for exactly this — point one at it and have it build its own Verification Compiler:
https://github.com/lpurdy01/verification_compiler_resources/blob/main/FOR_AGENTS.md

Then tell me how it went. I genuinely want to know: what tagging system did you use? How did you specify requirements and sub-requirements? Did you end up needing unique hyperlinkable IDs, or did you get away without them?
```

---

## Tags / keywords

Paste into the tag field, comma separated:

```text
verification compiler, AI code review, software verification, requirements traceability, safety critical software, DO-178C, ISO 26262, IEC 61508, AI generated code, LLM code review, evidence based development, technical debt, verification and validation, software engineering, AI engineering, agentic coding, code quality, audit trail, certification, embedded software
```

---

## LinkedIn post

Two variants. They pair with the title/thumbnail A/B — post the one that matches
what you actually publish, so the feed and the watch page tell the same story.

**Post the link in the first comment, not the body.** LinkedIn suppresses reach
on posts with an outbound link. Both variants below end on the question and say
"link in the comments"; the comment text is at the bottom of this section. Post
it within a minute of publishing, then edit the post to add nothing — editing
after the fact also costs reach.

First line is everything: it is all that shows before "…see more" on mobile.
Do not merge it into the paragraph below it.

---

### Variant A — rigor / contrarian (pairs with title A, thumbnail B)

```text
Your agent wrote four thousand lines this week. How much of it did you read?

AI made generating code, tests, and docs cheap. It did not make trusting them cheap. That asymmetry is where I think the next few years of software engineering actually happen.

Here is the uncomfortable part. When we ask a model "does this look right?" and it says "looks good," we have produced a feeling, not a record. A chat transcript is not an audit trail. It carries no requirement ID, no artifact version, no reviewer, and no way to tell six months from now whether the thing it approved has changed underneath you.

Safety-critical software worked out the shape of this problem decades ago. Avionics, medical devices, automotive — they carry traceability from requirement to evidence because they have to. My argument is that as generation gets cheaper, ordinary software starts to need the same shape, and that the tooling to produce it is finally buildable.

So I wrote up a proposal I have been calling the Verification Compiler:

→ turn the project into a graph of artifacts
→ traverse it deterministically to assemble bounded review packages
→ let models review those packages during development
→ keep humans in authority where it matters
→ preserve the result as evidence, not conversation

I want to be straight about what this is: a whitepaper-level idea, not a product, and not a claim that an LLM can certify anything. Human sign-off does not move. But a signal of how much verification is still ahead of you is genuinely useful — and for teams who will never chase certification, it is a code quality signal richer than anything we have today.

New video walks through the whole argument, with a companion repo: the whitepaper, the evidence trail from running the idea against its own paper, and an agent handoff so you can point your own coding agent at it and have it build a version.

When generation is nearly free, what becomes scarce? My bet is evidence you can inspect. What is yours?

Link in the comments.

#AI #SoftwareEngineering #Verification #AIEngineering #SafetyCritical
```

---

### Variant B — market shift (pairs with title B, thumbnail C)

Shorter, less inside-baseball, aimed past the embedded crowd.

```text
Generation got cheap. Verification didn't.

That is the whole thing, really. An agent can write four thousand lines this week. Nobody made it four thousand lines cheaper to check them.

And "I asked the model and it said it looks good" is not checking. That is a chat transcript — no requirement ID, no version, no reviewer, nothing you can hand to anyone six months later.

Safety-critical software has had the answer to this shape for decades. Requirement to design to code to test to result to review record, all of it pinned to a version. Expensive, unglamorous, and increasingly the thing ordinary software is missing.

So I published a proposal: the Verification Compiler. Treat the project as a graph of artifacts, traverse it deterministically to assemble bounded review packages, let models help during development, keep humans in authority where it matters, and preserve the output as evidence instead of conversation.

Not a product. Not a claim that an LLM can certify anything. A whitepaper-level idea I would like people to argue with.

Video, whitepaper, and an agent handoff so you can have your own agent build a version of it. Link in the comments.

What do you think becomes scarce when generation is free?

#AI #SoftwareEngineering #AIEngineering #Verification
```

---

### First comment (post immediately, both variants)

```text
Video: [YOUTUBE LINK]

Companion repo — whitepaper, evidence trail, and an agent handoff written so you can point a coding agent at it and have it build its own version:
https://github.com/lpurdy01/verification_compiler_resources

If you try that, I want to hear how it went — what tagging system you used, how you specified sub-requirements, and whether you ended up needing unique hyperlinkable IDs.
```

---

### Notes

- **Do not name the runtime in the post.** The video is 11:32 at 1.15×; if you
  end up shipping the 1.0× master it is 13:16, and a stale "~12 minute" line is
  the kind of small wrong detail that costs credibility for no benefit.
- **Reply to every comment in the first 90 minutes.** That window sets the
  distribution, and this post ends on a real question, so answers should come.
- **Tag nobody.** No @-mentions of companies or standards bodies — DO-178C and
  ISO 26262 appear in the video description and the repo, which is the right
  place for them.
- **Reshare into relevant groups** only after the post has been live an hour.

---

## Thumbnails — A / B / C test

All three are 1280×720 and well under YouTube's 2 MB limit. They test three
different click motives, which is the point — a three-way test of near-identical
art tells you nothing.

- **A — `thumb_A_who_checks_it.png`** ("WHO CHECKS THE CODE?") — broad anxiety,
  the widest cold-feed appeal and the least inside-baseball. A stack of generated
  code, one gate, and an empty checker's seat.
- **B — `thumb_B_chat_not_evidence.png`** ("CHAT IS NOT EVIDENCE") — rigor and
  contrarian standards. Carries the most conceptual signal: a vague chat log
  beside a structured evidence record. Closest match to the video's thesis.
- **C — `thumb_C_bottleneck_trust.png`** ("TRUST IS THE BOTTLENECK") — market
  shift, and the cleanest read at feed size. One packed lane, one nearly empty.

**Reading the result.** Let it run until Studio calls it, or ~2 weeks minimum —
a three-way split needs more impressions per arm than a two-way, so give it
longer than you would a straight A/B. If it comes back inconclusive, that is a
real answer: keep B, which is the one that best matches what the video delivers,
so it earns the most watch time from the clicks it gets.

D (`thumb_D_compiler_for_trust.png`) is the backup — the architecture/pipeline
angle, most useful if you re-cut this for an audience already sold on the
problem. Regenerate any of them with
`python3 ../thumbnail_ab_codex/make_thumbnails.py`; check
`thumbnail_mobile_preview.jpg` before judging.
