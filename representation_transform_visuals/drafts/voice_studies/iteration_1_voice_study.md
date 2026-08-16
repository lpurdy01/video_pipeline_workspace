# Iteration 1 Voice Study

Source:

- `assets/human_audio/iteration_1_commentary/transcripts/commentary_transcript.md`

Purpose: guide the next script rewrite so the script is easier for the user to say naturally.

## Main Diagnosis

The hot open was hard because it begins in polished explainer mode:

```text
Every so often, a new kind of transform changes what civilization can build.
```

That line is good as a claim, but it starts too high above the runway. The user's natural voice usually begins with orientation:

```text
This is an idea I've been thinking about...
I think the useful mental model is...
The thing I'm trying to get at is...
```

Then the argument climbs toward the big claim after a concrete example.

## Natural Voice Pattern

The user's strongest explanatory mode is:

1. name the mental model;
2. give a familiar technical analogy;
3. qualify the analogy;
4. show the concrete workplace example;
5. then make the philosophical claim.

The script should avoid opening with the philosophical claim before the listener has a foothold.

## Opening Strategy For Next Draft

Better structure:

```text
I've been trying to find a way to explain why LLMs feel bigger than chatbots.

The mental model I keep coming back to is transforms.

Not because an LLM is literally a Fourier transform for language. It is not that clean. It is trained, approximate, and lossy.

But it belongs in the same broad category of idea: you take a representation, move it into another space, do useful computation there, and transform it back out.
```

This gives the user room to sound like himself before the video scales up to civilization and technology trees.

## Sentence Shape

The user tends to sound most natural in medium-length explanatory sentences followed by short corrective sentences.

Pattern:

```text
This is the useful version of the claim.
Not the magic version.
Not the exact version.
The useful version.
```

Good script rhythm:

- one sentence to introduce;
- one sentence to qualify;
- one concrete example;
- one sentence to name the implication.

Avoid long front-loaded sentences with multiple abstract nouns before the verb.

## Caveats Should Arrive Early

The user naturally caveats bold claims near the claim:

- "not perfectly";
- "not magically";
- "not safely by default";
- "not the same kind of transform";
- "not as clean, not as exact";
- "this is a useful mental model";
- "meaning-like matters here."

The script should not wait until later to say these things. It should put the caveat immediately after the bold claim so the user does not feel like he is overclaiming while narrating.

## Words And Phrases That Fit

Strong phrases from the commentary:

- "a new paradigm, a new regime"
- "compute on intent"
- "meaning-like relationships"
- "not perfectly, not magically, but practically"
- "not thinking, relational, transformative"
- "the shape of the thing"
- "the word Python is operating on the rest of the intent"
- "a transform into vector space, do mathematics within vector space, and transform out"
- "transforming something that isn't specific into something that is absolutely specific"
- "the transform preserves some things, invents some things, loses others"
- "missing context becomes executable assumptions"
- "language is becoming a computable material"
- "not perfectly, not safely by default, and not without loss, but enough to matter"

## Phrases To Avoid Or Use Carefully

These felt less natural or were explicitly rejected:

- "calculus over concepts";
- "a Python script is not halfway between...";
- "legal contract derivative";
- generic lists that blur distinct ideas;
- "vector space literally contains human meaning";
- cold philosophical open without setup.

## Explanation Moves That Work

### Start With The Practical Example

The pseudocode-to-code example makes the whole idea feel real.

The user naturally says:

```text
As a programmer, this is the one I run into all the time.
```

This is a strong transition because it moves from grand theory into lived experience.

### Say What Something Is Not

The user often clarifies by subtraction:

```text
That is not code. That's not even a full specification.
```

This is useful and should stay.

### Use "Because" Often

The natural explanatory style leans on causal bridges:

```text
Because in vector space...
Because the input is missing information...
Because each representation is targeted at the next audience...
```

This helps the narration feel like thinking in motion.

### Use Correction As A Feature

The commentary often improves the idea through correction:

```text
No, that's not quite it.
The better version is...
```

The final script should not include messy corrections, but it can preserve the energy:

```text
The tempting way to say this is X.
But I think the more useful way is Y.
```

## Hot Open Alternatives

### Version A: Personal Mental Model

```text
I've been trying to find a way to explain why LLMs feel bigger than chatbots.

The mental model I keep coming back to is transforms.
```

Why it works:

- easy to say;
- starts in the user's actual thinking process;
- avoids sounding like a manifesto in the first sentence.

### Version B: Programmer Doorway

```text
If you write code with an LLM, you have probably felt the strange part already.

You type a vague English description, and a few seconds later you have something much more specific: Python, TypeScript, SQL, tests, documentation.
```

Why it works:

- concrete immediately;
- lets the transform concept emerge from a lived example;
- good for a YouTube audience of engineers.

### Version C: Transform First, But Softer

```text
There is a pattern in engineering that I think matters for understanding AI.

You take a problem in one representation, move it into another space, do useful work there, and then transform it back.
```

Why it works:

- keeps the current structure;
- less abrupt than "civilization can build";
- still sets up Fourier/Laplace/DCT.

## Recommended Opening For Next Draft

Use Version A into Version C:

```text
I've been trying to find a way to explain why LLMs feel bigger than chatbots.

The mental model I keep coming back to is transforms.

There is a pattern in engineering where you take a problem in one representation, move it into another space, do useful work there, and transform it back.
```

Then bring in Fourier/Laplace/DCT.

Save the civilization-scale line for after the listener sees the pattern:

```text
When a transform makes a new space computable, the technology tree changes.
```

## Limit Section Voice

The "thinking in the limit" sections should be methodical but not stiff.

Use this verbal structure:

```text
So let's push the trend.

Accuracy keeps going up.
The complexity of what models can handle keeps going up.
And the cost of generation keeps going down.

If you push those trends far enough, X stops being the bottleneck. Y becomes the bottleneck.
```

This sounds more like the user's commentary than the current abstract script.

## Script Rewrite Rules

1. Start sections with orientation, not conclusion.
2. Use the big philosophical line after the concrete example.
3. Keep caveats adjacent to claims.
4. Prefer "I think" when introducing a mental model, then remove it when stating mechanical facts.
5. Use shorter sentences around speculative claims.
6. Let the central code example do more work.
7. Use "not X, but Y" structures.
8. Keep the vocabulary technical enough for engineers, but avoid sounding like a paper abstract.
9. Treat "in the limit" as a deliberate method, not a vibe.
10. Put pronunciation-sensitive words in simple surroundings: Fourier, Laplace, PTX, validation, verification.
