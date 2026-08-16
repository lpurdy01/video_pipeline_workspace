# The Compiler For Trust - Storyboard

This storyboard follows the first-pass script and maps every section to a
prototype visual scene.

## Section Map

| ID | Title | Prototype Scene | Core Visual |
|---|---|---|---|
| 01 | Cold Open: Generation Got Cheap | `S01GenerationGate` | artifact flood into verification gate |
| 02 | The Hidden Cost Of "Looks Good" | `S02ChatLogFallacy` | chat bubble dissolves into evidence fields |
| 03 | Safety-Critical Software Already Has The Shape | `S03TraceabilityChain` | requirement-code-test-result-review chain |
| 04 | Artifacts Become A Graph | `S04ArtifactGraph` | typed DAG with orphan highlight |
| 05 | Compilation Means Traversal | `S05TraversalCompiler` | graph traversal beam assembles packages |
| 06 | The Verification Query Package | `S06VQPPackage` | selected subgraph folds into dossier |
| 07 | Same Package, Two Review Modes | `S07DualModeReview` | VQP branches to model and human review |
| 08 | Evidence Cards, Not Conversations | `S08EvidenceCards` | immutable evidence record and staleness crack |
| 09 | Verification Readiness Is A Map, Not Magic | `S09ReadinessMap` | graph heat map plus separated readiness bars |
| 10 | Closing: The Future Is Evidence Generation | `S10EvidenceSurface` | graph stabilizes into human decision surface |

## Visual Language

Stable artifact shapes:

- requirement: hexagon
- code unit: square
- test: circle
- result: rounded record
- source region: document slice
- review: diamond
- evidence package: sealed card
- VQP: folded packet/dossier

Stable colors:

- requirement: gold
- code: blue
- test: cyan
- result/evidence: green
- review: violet
- stale or anomaly: red
- dormant/unevaluated: muted gray

## Section Details

### 01 - Cold Open: Generation Got Cheap

Narration purpose:

Show that AI changes the economics of generation, but not automatically the
economics of trust.

Visual beats:

1. A prompt line appears.
2. Many code/test/doc/log cards multiply.
3. Cards stream toward a narrow verification gate.
4. The gate clogs and glows red.
5. Title appears: `The Compiler For Trust`.

Review question:

Does the viewer understand the bottleneck before any architecture appears?

### 02 - The Hidden Cost Of "Looks Good"

Narration purpose:

Attack the false comfort of model explanations.

Visual beats:

1. Chat bubble says `Looks good`.
2. Scanner overlays missing audit fields.
3. Bubble dissolves into a structured evidence card with empty slots.

Review question:

Does this make "chat transcript is not evidence" obvious without sounding
anti-AI?

### 03 - Safety-Critical Software Already Has The Shape

Narration purpose:

Introduce traceability as coordination, not bureaucracy.

Visual beats:

1. Requirement hexagon.
2. Code square.
3. Test circle.
4. Result record.
5. Review diamond.
6. Evidence card.
7. Chain duplicates into multiple branches.

Review question:

Does the traceability chain feel elegant rather than administrative?

### 04 - Artifacts Become A Graph

Narration purpose:

Move from chain to graph.

Visual beats:

1. Multiple chains bend into a DAG.
2. Typed nodes appear.
3. Edges glow by relation.
4. Orphan code and orphan requirement pulse red.

Review question:

Can the viewer see the artifact graph as the central object?

### 05 - Compilation Means Traversal

Narration purpose:

Make the compiler analogy concrete.

Visual beats:

1. Source code to binary on left.
2. Artifact graph to review package on right.
3. Traversal beam moves through graph.
4. Selected nodes brighten.
5. VQP packets emerge.

Review question:

Does "compilation" mean deterministic traversal, not AI magic?

### 06 - The Verification Query Package

Narration purpose:

Show the unit of verification work.

Visual beats:

1. Selected subgraph is lassoed.
2. Lasso folds into VQP packet.
3. Packet opens into dossier panes:
   - code
   - requirements
   - source region
   - tests
   - results
   - instructions

Review question:

Does the package feel complete but bounded?

### 07 - Same Package, Two Review Modes

Narration purpose:

Clarify that humans and models can review the same package, but with different
authority.

Visual beats:

1. VQP duplicates.
2. One path goes to `developmental model review`.
3. One path goes to `human certification-facing review`.
4. Both produce same schema.
5. Human result passes through final authority gate.

Review question:

Is the LLM/human boundary unmistakable?

### 08 - Evidence Cards, Not Conversations

Narration purpose:

Make structured evidence records tangible.

Visual beats:

1. Evidence card fills fields.
2. Code hash seals onto card.
3. Code node changes.
4. Evidence card cracks/dims as stale.
5. New VQP is queued.

Review question:

Does stale evidence read as "still preserved, no longer current"?

### 09 - Verification Readiness Is A Map, Not Magic

Narration purpose:

Introduce readiness as visibility, not certainty.

Visual beats:

1. Full graph becomes heat map.
2. Green reviewed/current paths.
3. Amber stale paths.
4. Red anomalies.
5. Four separate bars: coverage, completeness, staleness, suitability.

Review question:

Does the section avoid implying a magic safety score?

### 10 - Closing: The Future Is Evidence Generation

Narration purpose:

Land the thesis.

Visual beats:

1. Artifact graph stabilizes.
2. VQPs flow into evidence surface.
3. Human decision gate remains visible.
4. Unresolved red/amber nodes remain visible.
5. Final title.

Review question:

Does the final image say "trust the evidence surface"?

