# Verification Compiler Video Outline - First Pass

## Purpose

This is a first-pass creative outline for a shorter, roughly 10-minute video
about why the Verification Compiler matters.

It builds on `video_production_plan.md` and incorporates a Gemini 3.1 Pro
thinking-mode brainstorm saved locally at:

```text
representation_transform_visuals/agent_tools/out/vc_video_outline_brainstorm_gemini.md
```

The useful creative move from the brainstorm is this:

```text
AI makes generation cheap. Verification does not automatically get cheap.
The Verification Compiler is a way to turn messy project artifacts into
bounded, inspectable evidence.
```

The video should not feel like a product demo or standards lecture. It should
feel like a visual argument: the next bottleneck in AI-assisted software is not
writing more code, but proving what the code satisfies.

## Working Title

Recommended:

**The Compiler For Trust**

Alternates:

- The Verification Compiler
- AI Can Write Code. Who Checks It?
- The Bottleneck Is Verification
- When AI Has To Prove Its Work
- From Code Generation To Evidence Generation

## Core Thesis

AI changes the economics of software generation. A model can produce code,
tests, documentation, and plans faster than humans can inspect them.

That creates a verification bottleneck.

The Verification Compiler is a proposed architecture for that bottleneck. It
treats requirements, code, tests, source documents, static analysis, reviews,
and physical results as a typed artifact graph. Then it deterministically
traverses that graph to assemble bounded verification packages and structured
evidence records.

The point is not "AI certifies software." The point is:

```text
AI can help produce developmental review signals,
but trust comes from traceable, reviewable, versioned evidence.
```

## Best Hook Direction

Use the **generation vs. verification asymmetry** as the opening. It is simple,
visual, and emotionally legible.

Opening line candidates:

1. "AI made writing code cheap. It did not make trusting code cheap."
2. "The dangerous part of AI coding is not that it writes bad code. It is that
   it writes too much code to check."
3. "A chat transcript is not evidence."
4. "The next software bottleneck is not generation. It is verification."
5. "If code can appear in seconds, proof has to become a system."

Recommended opening:

```text
AI made writing code cheap.

But it did not make trusting code cheap.

And if we are about to generate ten times more software,
we cannot verify it with the same old pile of chat logs,
manual checklists, and scattered test reports.

We need something stranger:

a compiler for trust.
```

Visual:

```text
dark screen
one prompt appears
code blocks multiply rapidly
tests, docs, and diagrams also multiply
camera pulls back
everything flows toward a tiny gate labeled VERIFICATION
the gate clogs
screen cuts to title: The Compiler For Trust
```

## Hook Menu

### Hook A: The Verification Bottleneck

First 20 seconds:

```text
AI made writing code cheap.

But it did not make trusting code cheap.

That means the bottleneck moves.

Not to the model.
Not to the editor.

To verification.
```

Visual:

```text
rapid code generation waterfall
many artifacts: code, tests, docs, diagrams, logs
all converge on one narrow verification gate
gate glows red as backlog piles up
```

Use when:

- we want the clearest broad-audience hook
- we want to connect to AI coding immediately

### Hook B: The Chat Log Fallacy

First 20 seconds:

```text
If a model writes code, and then explains why the code is safe,
what do you have?

Not proof.

Not certification.

Not an audit trail.

You have a chat transcript.
```

Visual:

```text
friendly chat bubbles say "Looks safe"
cross-section scan reveals missing requirements, stale tests, no code hash
chat bubbles collapse into strict evidence-card fields
```

Use when:

- we want a punchier, contrarian opening
- we want the video to attack a common workflow mistake

### Hook C: The Orphan Code Hunt

First 20 seconds:

```text
The scariest code is not always the code with a bug.

Sometimes it is the code that works perfectly,
but no one can explain why it exists.

In safety-critical software, that is an orphan.

AI is about to create a lot of orphans.
```

Visual:

```text
starfield of code nodes
green requirement lines connect most nodes
radar sweep finds isolated nodes
isolated nodes pulse red: ORPHAN CODE
```

Use when:

- we want a more memorable safety/traceability hook
- we want a strong Short

### Hook D: The New Compiler

First 20 seconds:

```text
The old compiler turns source code into machine instructions.

But that is not the hard part anymore.

The hard part is turning a project into evidence.

Requirements. Code. Tests. Reviews. Results.

All compiled into something a human can actually inspect.
```

Visual:

```text
left: C source transforms into binary
right: messy project artifacts transform into an artifact graph
artifact graph folds into evidence packages
```

Use when:

- we want the name "Verification Compiler" to make immediate sense

### Hook E: The Airplane Zoom

First 20 seconds:

```text
When software flies an airplane,
the question is not just "does the code run?"

The question is:

which requirement does this line satisfy?
which test proved it?
which result belongs to this version?
and who reviewed the evidence?
```

Visual:

```text
minimal wireframe airplane
zoom into avionics box
zoom into source file
source file expands into graph of requirements, code, tests, evidence
```

Use when:

- we want an aerospace-flavored opening
- use carefully: avoid implying this project is certification-ready

## Recommended 10-Minute Outline

### 0:00-0:45 - Cold Open: Generation Got Cheap

Purpose:

Establish the central asymmetry. AI can generate artifacts faster than humans
can validate them.

Narration beats:

- AI made writing code cheap.
- It did not make trusting code cheap.
- The bottleneck moves from generation to verification.
- The thing we need is not another chatbot. It is a compiler for trust.

Visuals:

- prompt appears
- code blocks multiply
- tests, docs, diagrams, issue comments, and logs multiply too
- everything flows into a narrow verification gate
- gate clogs and heats up
- title appears

On-screen text:

```text
Generation got cheap.
Verification did not.
```

### 0:45-1:45 - The Hidden Cost Of "Looks Good"

Purpose:

Make "chat transcript is not evidence" intuitive.

Narration beats:

- A model can explain why its output is correct.
- That explanation is useful, but it is not an audit trail.
- Safety-critical review needs links: requirement, code version, test, result,
  reviewer, rationale.
- The problem is not that AI is useless. The problem is that useful output has
  to be turned into evidence.

Visuals:

- chat bubble says "This implementation satisfies the requirement"
- scanner overlays missing fields: no requirement ID, no code hash, no linked
  test, no result version
- bubble dissolves into an evidence-card template with empty slots

On-screen text:

```text
Useful answer != auditable evidence
```

### 1:45-2:45 - Safety-Critical Software Already Has The Shape

Purpose:

Introduce traceability as coordination machinery, not bureaucracy.

Narration beats:

- High-assurance software has lived with this problem for decades.
- You do not just ask whether code works.
- You ask what requirement it traces to, what verifies it, and what evidence
  belongs to the current version.
- That structure is the clue.

Visuals:

- simple chain appears:

```text
Requirement -> Code -> Test -> Result -> Review -> Evidence
```

- each node has a stable shape:
  - requirement: hexagon
  - code: square
  - test: circle
  - result: rounded record
  - review: diamond
  - evidence package: card
- chain duplicates into several branches

On-screen text:

```text
Traceability is the shape of trust.
```

### 2:45-3:55 - Artifacts Become A Graph

Purpose:

Introduce the artifact graph as the core visual object.

Narration beats:

- A real project is not one chain.
- It is a graph.
- Requirements link to child requirements, code, tests, static analysis,
  source-region references, physical results, model reviews, and human reviews.
- The graph is not decoration. It defines what must be checked.

Visuals:

- several traceability chains bend and merge into a typed DAG
- node colors encode artifact type
- edges carry relation labels briefly, then fade to clean geometry
- orphan nodes glow red

On-screen text:

```text
Every artifact becomes a typed node.
Every dependency becomes a typed edge.
```

### 3:55-5:10 - Compilation Means Traversal

Purpose:

Explain the compiler analogy.

Narration beats:

- A normal compiler traverses source code and emits a machine artifact.
- A verification compiler traverses an artifact graph and emits review
  packages.
- The important part is deterministic assembly.
- Same graph state, same package.

Visuals:

- left side: source code passes through compiler, binary falls out
- right side: artifact graph passes through traversal beam, VQP packets fall out
- golden/cyan beam moves from top requirement through relevant subgraph
- selected subgraph is lassoed

On-screen text:

```text
Graph state -> deterministic traversal -> review package
```

### 5:10-6:25 - The Verification Query Package

Purpose:

Show the thing the system actually produces.

Narration beats:

- Each package is bounded enough for a reviewer.
- It contains the code, linked requirements, source text, tests, results, and
  instructions.
- This is the unit of work for both humans and models.
- It is how a huge verification problem becomes many inspectable problems.

Visuals:

- lassoed graph folds into a VQP card
- card opens like a clean technical dossier:
  - code unit
  - requirement text
  - source-region excerpt
  - tests
  - test results
  - analysis outputs
  - review instructions
- token/context boundary shown as a subtle frame

On-screen text:

```text
One bounded package.
All relevant evidence.
```

### 6:25-7:25 - Same Package, Two Review Modes

Purpose:

State the human/LLM boundary clearly.

Narration beats:

- The package can go to a model for fast developmental review.
- The same package can go to a human for certification-facing review.
- The schema is the same.
- The authority is not the same.
- Humans can promote, reject, or override model outputs.

Visuals:

- VQP duplicates
- one path moves fast through "developmental model review"
- one path moves through "human review gate"
- both produce the same structured result shape
- human result has final gate authority

On-screen text:

```text
Same package.
Different authority.
```

### 7:25-8:25 - Evidence Cards, Not Conversations

Purpose:

Make structured evidence feel concrete.

Narration beats:

- The output is not a chat log.
- It is a versioned evidence record.
- It includes result, rationale, citations, reviewer ID, prompt version, model
  version if applicable, timestamp, and code hash.
- If the code changes, the old evidence does not disappear. It becomes stale.

Visuals:

- result card fills in fields
- hash seals onto card
- source node changes
- card cracks or dims as stale
- new package is queued

On-screen text:

```text
Evidence must survive audit.
```

### 8:25-9:20 - Verification Readiness Is A Map, Not Magic

Purpose:

Explain VRM without making it a false truth score.

Narration beats:

- The system can show coverage, evidence completeness, staleness, and reviewer
  suitability.
- This is not a magic safety score.
- It tells you where the evidence surface is strong, weak, stale, or missing.
- That is what makes the project navigable.

Visuals:

- zoom out to graph heat map
- green: reviewed and current
- gray: unevaluated
- amber: stale
- red: anomaly
- dashboard shows separate bars, not one giant truth number:
  - coverage
  - evidence completeness
  - staleness
  - model suitability

On-screen text:

```text
Readiness is visibility, not certainty.
```

### 9:20-10:00 - Closing: The Future Is Evidence Generation

Purpose:

Land the philosophical point and set up future work.

Narration beats:

- AI will keep making artifact generation cheaper.
- The scarce resource becomes trustworthy review.
- The Verification Compiler is a proposal for making review structured,
  repeatable, and inspectable.
- Not "trust the AI."
- Trust the evidence surface.

Visuals:

- artifact graph stabilizes into a clean evidence surface
- final VQP drops into a human decision gate
- unresolved red/amber nodes remain visible, not hidden
- title card

Final line:

```text
The future of AI software is not just generating code.
It is generating evidence we can actually inspect.
```

## Recurring Visual Motifs

### 1. Shape Language

Use stable artifact shapes throughout:

- requirement: hexagon
- code unit: square
- test: circle
- result: small record card
- source region: document slice
- review: diamond
- evidence package: sealed card
- VQP: folded packet/dossier

This lets the viewer learn the diagram language once and read it quickly later.

### 2. The Verification Gate

A narrow gate converts "artifact flood" into "reviewed evidence." Early in the
video, it clogs. By the end, it becomes a structured traversal system.

### 3. The Traversal Beam

A bright deterministic beam walks the graph. This is the opposite of the usual
blurry AI visual language. It says: fixed graph state, fixed traversal, fixed
package.

### 4. Lasso And Fold

The selected subgraph is lassoed, lifted, and folded into a Verification Query
Package. This makes decomposition physical and memorable.

### 5. Staleness As Fracture

When code or source text changes, evidence cards do not vanish. They crack,
dim, or lose their seal. The old record still exists, but it no longer applies
cleanly.

### 6. Heat Map Of Trust

The final graph becomes a map:

- green paths are current and reviewed
- gray regions are untouched
- amber regions are stale
- red regions are anomalous

The point is visibility.

## Shorts Concepts

### Short 1: The AI Coding Trap

Length:

45-55 seconds

Hook:

```text
AI can write code faster than you can read it.
That is not just a productivity boost.
That is a verification problem.
```

Beat structure:

```text
0-5s:
AI prompt appears. Code floods the screen.
Caption: AI made generation cheap.

5-15s:
Human review gate clogs.
Caption: Trust did not get cheap.

15-28s:
Traceability chain appears:
Requirement -> Code -> Test -> Result
Caption: Safety-critical software needs links.

28-43s:
Chain expands into artifact graph.
Traversal beam selects a subgraph.
Caption: Compile artifacts into review packages.

43-55s:
VQP folds into evidence card.
Caption: The future bottleneck is evidence.
```

Voiceover draft:

```text
AI can write code faster than you can read it.

That sounds like productivity.

But in serious software, the question is not just:
does the code run?

It is:
what requirement does it satisfy,
what test verified it,
what result belongs to this version,
and who reviewed the evidence?

That is why I am working on a Verification Compiler:
a system that turns messy project artifacts into bounded review packages.

Because the future bottleneck is not generating code.
It is generating evidence.
```

### Short 2: A Chat Log Is Not Evidence

Length:

40-55 seconds

Hook:

```text
If an AI tells you its code is safe, what do you have?
Not proof.
A chat log.
```

Beat structure:

```text
0-6s:
Chat bubble says "This code is safe."
Caption: Not proof.

6-16s:
Scanner overlays missing fields:
requirement ID, code hash, linked test, result version.
Caption: A chat log is not evidence.

16-30s:
Graph appears with requirement, code, test, result nodes.
Caption: Evidence needs structure.

30-44s:
Subgraph folds into VQP.
Caption: Bounded review package.

44-55s:
Evidence card seals with hash and reviewer fields.
Caption: Trust the evidence, not the transcript.
```

Voiceover draft:

```text
If an AI tells you its code is safe,
what do you have?

Not proof.

A chat log.

Real evidence needs structure:
the requirement,
the code version,
the test,
the result,
the reviewer,
and the rationale.

The Verification Compiler idea is to assemble all of that automatically
into bounded review packages.

Not so the AI can certify the code.

So humans can inspect the evidence.
```

### Short 3: The Orphan Code Problem

Length:

45-60 seconds

Hook:

```text
The most dangerous code might not be buggy.
It might be orphaned.
```

Beat structure:

```text
0-6s:
Code node floats alone in dark graph.
Caption: Orphan code.

6-18s:
Requirement links appear for other nodes, but not this one.
Caption: No requirement. No trace.

18-30s:
AI-generated code blocks multiply, some disconnected.
Caption: AI can create more orphans.

30-45s:
Artifact graph scan highlights orphan requirements and orphan code.
Caption: Verification starts with visibility.

45-60s:
Traversal routes connected nodes into evidence packages; orphan remains red.
Caption: You cannot verify what you cannot trace.
```

Voiceover draft:

```text
The most dangerous code might not be buggy.

It might be orphaned.

Code with no requirement.
No test.
No reason anyone can point to.

AI coding makes this worse,
because it can generate plausible code faster than teams can trace it.

A Verification Compiler treats the project as an artifact graph.

Connected nodes can become evidence.

Orphans stay red until someone explains why they exist.
```

## Claim Safety Rules

Use these rules in script review:

1. Do not say AI certifies safety-critical software.
2. Say "developmental review" for LLM review outputs.
3. Say "human certification-facing review" for final authority.
4. Do not imply VRM is a safety score.
5. Say VRM exposes coverage, completeness, staleness, and suitability.
6. Do not claim compliance with DO-178C, ISO 26262, IEC 62443, or any licensed
   standard.
7. Say the architecture is inspired by traceability and evidence practices in
   high-assurance engineering.
8. Show failure modes on screen: stale evidence, orphan code, missing tests,
   and human/model disagreement.
9. Keep source-region and code-hash visuals prominent so the video feels
   auditable rather than magical.

## First Three Visuals To Prototype

### Visual 1: Artifact Flood Into Verification Gate

Why first:

This is the emotional hook. If it works, the video has a reason to exist.

Prototype elements:

- generated code blocks
- test/doc/log blocks
- narrow verification gate
- backlog pileup
- title transition

### Visual 2: Artifact Graph And Orphan Highlight

Why first:

This defines the core object of the whole video.

Prototype elements:

- typed node shapes
- clean DAG layout
- relation edges
- orphan node pulse
- graph heat-map colors

### Visual 3: Lasso And Fold Into VQP

Why first:

This explains "compiler" better than narration can.

Prototype elements:

- traversal beam
- selected subgraph
- lasso boundary
- fold/transform into VQP packet
- packet opens into evidence-card fields

## Immediate Production Recommendation

Start with Hook A and make a 90-second animatic before writing the full script.

The animatic should include:

1. artifact flood;
2. clogged verification gate;
3. traceability chain;
4. graph morph;
5. traversal beam;
6. VQP fold;
7. evidence card.

If those seven visuals read clearly without polished narration, the 10-minute
video has a strong spine.
