# The Compiler For Trust - First-Pass Script

Status: first complete narration draft.

Target length: roughly 10 minutes.

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

Because serious software is not just software that runs.

Serious software is software where someone can explain what it is supposed to
do, what requirement it satisfies, what test verified it, what version the test
ran against, what evidence was produced, and who accepted the result.

AI has made generation faster.

It has not automatically made verification faster.

So the bottleneck moves.

Not to the editor.

Not to the model.

To trust.

And that is why I have been thinking about something I call a Verification
Compiler.

Or, less formally:

a compiler for trust.

### 2. The Hidden Cost Of "Looks Good"

Here is the trap.

You ask a model to write some code.

Then you ask the same model whether the code satisfies the requirement.

It says yes.

It gives you a calm explanation.

Maybe the explanation is even useful.

But what do you actually have?

You do not have proof.

You do not have certification.

You do not have an audit trail.

You have a chat transcript.

And a chat transcript is not evidence.

In a normal software project, that might be fine for a quick iteration.

But in safety-critical software, regulated software, embedded systems, or any
system where failure really matters, the question is not just:

does this answer sound reasonable?

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

The details vary by industry, and the standards themselves are careful legal and
engineering documents.

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

But the deeper idea is not bureaucracy.

It is coordination.

It is a way for a large group of limited humans to make a complicated system
reviewable.

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

I have been calling that artifact a Verification Query Package.

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
package and produce the accepted result.

If the model and the human disagree, the disagreement is not swept away.

It becomes part of the evidence history.

It can update the model's suitability for that kind of task.

The system is not trying to pretend the model is a perfect certifier.

It is trying to make model assistance fit inside a review structure that humans
can audit.

### 8. Evidence Cards, Not Conversations

The output should not be a chat bubble.

It should be an evidence record.

Result:

pass, fail, or uncertain.

Rationale:

what made the reviewer decide that?

Citations:

which requirement lines, source regions, test results, or code sections support
the result?

Reviewer:

human, model, or tool.

Version:

which code hash, which prompt version, which model version, which timestamp?

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

