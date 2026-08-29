# The Compiler For Trust - Third-Pass Script

Status: third pass, revised against the 2026-08-24 spoken commentary.
See `narration_review/out/review_notes_2026_08_23.md` and
`review_notes_2026_08_24.md` for what changed and why.

Target length: roughly 10 minutes. See the length note at the end of this file.

Working title:

**The Compiler For Trust**

Alternate titles:

- The Verification Compiler
- AI Can Write Code. Who Checks It?
- The Bottleneck Is Verification
- From Code Generation To Evidence Generation

## Voice Notes

The voice should feel like an engineer thinking out loud, not like a compliance
webinar. The key emotional motion is:

```text
excitement about AI generation -> discomfort about verification -> relief that
the problem has a shape -> ambition around evidence generation
```

Avoid saying that AI certifies safety-critical software. LLM review is
developmental unless a human promotes it. The final authority remains human.

Concretely: safety-critical software is signed off today by humans who verify it
and carry the responsibility for it. Be precise about the shape of that: it is
not a professional-engineer stamp the way civil or mechanical engineering works.
It is organizational and process-driven — the FAA signs off on it. That endpoint
does not move. We cannot hand-wave and say the AI did it.

But two things are still true. During development, a signal of how much human
verification is still ahead of you is genuinely useful. And for teams who are not
going for full certification and do not have the budget to verify everything, a
readiness metric is a code quality signal richer than anything we have today.

The video also has to work for people who do not write embedded software. Every
abstract claim needs a "so what" — a concrete piece of the world it touches.

## Full Narration Draft

### 1. Cold Open: Generation Got Cheap

AI made writing code cheap.

But it did not make trusting code cheap.

That is the part I think people are still underestimating.

If a model can write a function in ten seconds, that is impressive.

If it can write the tests, the documentation, the migration plan, the review
summary, and the issue comment in another ten seconds, that is even more
impressive.

But now you have a new problem.

Who checks all of it?

And this is not a thought experiment.

Across the industry, more and more of the work happens agentically.

Pull requests arrive faster than any team can actually read them.

The pace becomes the product, and review is the thing that gets crushed
underneath it.

Because serious software is not just software that runs.

Serious software is software where someone can explain what it is supposed to
do, what requirement it satisfies, what test verified it, what version the test
ran against, what evidence was produced, and who accepted the result.

Let me be concrete about what I mean, because there are really two different
worlds here.

In one of them, quality is a business problem.

A web application has to be reliable enough that customers do not leave.

If something breaks on Monday, you ship a fix on Tuesday, and life goes on.

In the other one, software flies aircraft.

It keeps satellites talking to the ground.

It decides how hard your car brakes when a child steps into the road.

That software is certified before it is allowed to run, and somebody has to be
accountable for it — an organization, a process, a regulator signing off.

Right now that second world is almost closed to AI-assisted development.

Not because the models write bad code.

Because nobody can check the flood fast enough to keep the standards intact.

AI has made generation faster.

It has not automatically made verification faster.

So the bottleneck moves.

Not to the editor.

Not to the model.

To trust.

And that is why I have been thinking about something I call a Verification
Compiler.

The goal is not to bring AI into safety-critical work for the sake of it.

The goal is to automate the verification scaffolding during development, so that
the standards that keep that software safe stay fully intact while you move
faster.

It is a process, not a shortcut.

Or, less formally:

a compiler for trust.

### 2. The Hidden Cost Of "Looks Good"

Here is the trap.

You ask a model to write some code.

Then you ask the same model whether the code satisfies the requirement.

It says yes, with a calm and often genuinely useful explanation.

But what do you actually have?

No proof. No certification. No audit trail.

You have a chat transcript.

And a chat transcript is not evidence.

For a quick iteration, that may be fine.

Where failure actually matters, the question is not whether the answer sounds
reasonable.

The question is:

which requirement is being checked?

Which code version?

Which test result?

Which source document?

Which review rule?

Which human accepted it?

And can we reproduce what was reviewed later?

That is the gap.

The model can generate an answer.

But the answer still has to be turned into evidence.

### 3. Safety-Critical Software Already Has The Shape

High-assurance software has been dealing with this kind of problem for decades.

And I think most developers have no idea this world exists.

There are entire standards governing how this software is allowed to be built.

DO-178C in aerospace.

ISO 26262, and ASIL levels, in automotive.

There are more, industry by industry.

The details vary, and the standards themselves are careful legal and engineering
documents.

But the broad pattern is simple enough to see.

You do not just write code and hope.

You maintain traceability.

A requirement traces to design.

Design traces to code.

Code traces to tests.

Tests trace to results.

Results trace to review records.

And all of that has to stay tied to the version of the system being evaluated.

That can sound like bureaucracy from the outside.

And I want to be honest about it: it is a lot of overhead work.

It is part of why the same function can cost a hundred times more to ship on an
aircraft than on a drone.

But the deeper idea is not bureaucracy.

It is coordination.

It is a way for a large group of limited humans to make a complicated system
reviewable.

And reviewable is the word that matters.

Nobody can look at a whole system at once and pronounce it good.

It is too big. That is true of every engineer on the team.

It is just as true of an AI model asked to do the same thing.

So you break it apart.

You verify the small units first.

Unit tests. Integration tests. System tests. Verification tests.

And the requirements stack the same way, sub-requirements rolling up into the
requirements that actually matter.

You climb that ladder until the system is as true as you can make it, before
anyone's life depends on it.

And that is the clue for AI-assisted software.

If models are going to generate more artifacts, faster, then the project needs
an even stronger structure for knowing what those artifacts mean.

### 4. Artifacts Become A Graph

The first move is to stop thinking of a project as a folder full of files.

For verification, a project is a graph.

Every important thing becomes a node.

Requirements.

Source code units.

Tests.

Test results.

Static analysis results.

Datasheets.

Interface control documents.

Physical test records.

Model review outputs.

Human review outputs.

Even specific sections of source documents become nodes, because a citation that
only says "see the standard" is not precise enough.

Then the relationships become edges.

This requirement traces to that code.

This test verifies that behavior.

This result was produced against this version.

This source region supports this claim.

Now the project has a shape.

And once it has a shape, you can ask structural questions.

Is there code with no requirement?

Is there a requirement with no implementation?

Is there a test result tied to an old version?

Is there a model review that disagrees with a human review?

Those are not philosophical questions anymore.

They are graph questions.

### 5. Compilation Means Traversal

This is where the compiler analogy starts to matter.

A normal compiler takes source code, walks a structured representation, and
emits something else.

It turns one representation into another representation through a defined
process.

A Verification Compiler would not compile code into a binary.

It would compile an artifact graph into verification work.

Start with a top-level requirement.

Traverse the graph.

Collect the code units that matter.

Collect the linked requirements.

Collect the tests.

Collect the results.

Collect the relevant source text.

Collect the static analysis output.

Then assemble that into a bounded review package.

Same graph state.

Same traversal rule.

Same package.

That deterministic assembly is the point.

The model might be probabilistic.

The human might be inconsistent.

But the package they receive should not be a vibe.

It should be a reproducible artifact.

### 6. The Verification Query Package

I have been calling that artifact a Verification Query Package. A VQP.

The name is clunky, but the idea is useful.

A Verification Query Package is the smallest unit of verification work that can
stand on its own.

It includes the code under review.

It includes the requirements that code is supposed to satisfy.

It includes the tests and results attached to the same version.

It includes the source-region text that supports the claim being checked.

It includes the review instructions.

And it is bounded.

Small enough for a model to analyze.

Small enough for a human to inspect.

But complete enough that the reviewer is not guessing what context matters.

And a package does not have to be text.

[VISUAL: a VQP opening to show a rendered screenshot and a captured waveform
alongside the code and requirement panes.]

A rendered screen, a captured output, a physical test trace — if it is evidence
about the thing being checked, it belongs in the package.

That matters well beyond aerospace, though aerospace is where the standards are
strictest, and that is the case this is built for.

This is one of the important shifts.

Instead of asking a model to review an entire project, or asking a human to
search through a pile of artifacts, the graph assembles the relevant slice.

The huge problem becomes many smaller review packages.

And each package can leave behind a structured result.

### 7. Same Package, Two Review Modes

This also gives us a cleaner way to talk about AI review.

The same package can go to a model.

The same package can go to a human.

The input structure is the same.

The output schema is the same.

But the authority is not the same.

In development, a model can review packages quickly.

It can flag missing evidence.

It can notice mismatches.

It can say: this requirement looks only partially covered.

That is valuable.

But it is developmental review.

For certification-facing decisions, a human reviewer can inspect the same
package — rendered into something actually readable, a page rather than a blob of
JSON — and produce the accepted result.

If the model and the human disagree, the disagreement is not swept away.

It becomes part of the evidence history.

It can update the model's suitability for that kind of task.

The system is not trying to pretend the model is a perfect certifier.

It is trying to make model assistance fit inside a review structure that humans
can audit.

### 8. Evidence Cards, Not Conversations

The output should not be a chat bubble.

It should be an evidence record.

And a record has fields.

[VISUAL: evidence card — Result, Rationale, Citations, Reviewer, Version. The
table carries the field names; do not read them aloud.]

Every one of those fields answers a question you would otherwise have to walk
over and ask somebody: what was decided, why, what supports it, who decided, and
against which version of the code.

And once that record exists, it should not be edited in place.

If the code changes, the old evidence does not disappear.

It becomes stale.

If the source document changes, links depending on that source region need to be
rechecked.

If a human overrides a model result, both records stay visible.

This is how you get an audit trail instead of a pile of confident text.

The point is not that every record is true forever.

The point is that every record has provenance.

### 9. Verification Readiness Is A Map, Not Magic

Once the project is a graph and the reviews are structured, you can zoom out.

You can ask:

how much of the graph has been reviewed?

Which requirements have current evidence?

Which evidence is stale?

Which parts are missing tests?

Which model results are below the suitability threshold for this task?

Which areas still need human attention?

That gives you something like a Verification Readiness Metric.

But this is important:

it is not a magic safety score.

It does not say the system is safe because the number is high.

It says the evidence surface is more or less complete, more or less current,
more or less reviewed.

It makes the gaps visible.

That is what readiness means here.

Not certainty.

Visibility.

And one more distinction, because the two words get used interchangeably and
they are not the same thing.

Verification is checking that you built the thing you meant to build.

Validation is checking that the thing you built is the thing you should have
built — that it actually holds up out in the world.

Those are two separate processes.

The Verification Compiler is aimed squarely at the first one.

It will not tell you that you designed the right system.

It tells you whether you can show that you built the system you specified.

### 10. Closing: The Future Is Evidence Generation

I think this is where AI software is going.

Not because models will magically replace verification.

They will not.

But because generation is getting cheaper, and every cheap generation step
creates a verification obligation.

Another function.

Another test.

Another design note.

Another claim.

Another assumption.

The bottleneck becomes:

what can we trust enough to connect back into the world?

The Verification Compiler is one answer to that bottleneck.

Turn the project into a graph.

Traverse the graph deterministically.

Assemble bounded review packages.

Let models help during development.

Let humans retain authority where it matters.

And preserve the result as evidence.

Not "trust the AI."

Trust the evidence surface.

Because the future of AI software is not just generating code.

It is generating evidence we can actually inspect.


### 11. End Card

Thank you for sitting through my thinking on this.

The full whitepaper that goes with this video is in the description, along with the references behind the follow-on work.

And if you are an agentic developer, use those resources to have your agent build its own version of a Verification Compiler. Then tell me in the comments how the experiment went.

What tagging system did you use? How did you specify requirements and sub-requirements? What did you use for unique, hyperlinkable IDs — if you even found that you needed them?

I wanted to publish this idea so that other people could start expanding on what is possible with it. I am genuinely excited to see where it goes.

I want to be straight about what this is, though. It is a whitepaper-level idea. It is not a product, and it is not finished.

So the next thing I am going to do is build it. I want to practise implementing this, refine it, and find the rough edges — because the rough edges are where an idea like this either holds up or quietly falls apart.

If you want to know when that lands, like the video and subscribe.

And if you know someone working on this problem — someone who has to get software through a certification process — send it to them. That is the conversation I am hoping to start.


---

## Length Note (second pass, 2026-08-23)

At 150 wpm this draft reads **13.4 minutes**, against a 10-minute target. The
first pass was 10.4. The commentary asked for material that necessarily adds
time — the "so what" grounding, the standards context, the decomposition
argument, and the verification/validation split — so the overage is the cost of
those notes, not padding that crept in.

Where the time went:

| Section | Was | Now |
|---|---|---|
| 1. Cold Open | 70s | 161s |
| 3. Already Has The Shape | 63s | 132s |
| 9. Readiness Is A Map | 52s | 90s |
| everything else | ~10s net cut |

Three ways to get back toward ten minutes, in the order I would try them:

1. **Split the cold open.** Section 1 is now 2:41, which is long for an opening.
   The two-worlds contrast (web software vs. certified software) could move into
   section 3, where the standards discussion already lives. Saves ~50s and gives
   section 1 a single job again.
2. **Compress the test ladder.** "Unit tests. Integration tests. System tests.
   Verification tests." plus the sub-requirements sentence is the most
   compressible new material — the visual can carry the ladder while the
   narration states only the principle. Saves ~25s.
3. **Trim sections 4-7.** These are untouched from the first pass and are the
   most abstract stretch of the video. Roughly 10% could come out of each without
   losing an argument. Saves ~25s.

Applying all three lands near 11 minutes. Getting under 10 would mean cutting an
argument, not tightening prose — that is a call for the next pass.
