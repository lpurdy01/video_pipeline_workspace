# Orbital Tech Tree Scene Integration Plan

## Principle

The orbital tree should become a recurring map, but the full map must not be readable until the ending. Earlier sections reveal only local geography, using particles, masks, and camera crops to imply more structure beyond the frame.

The old storyboard has a large tech-tree moment in section 8 (`S06cGameTechTree3D`) and a final zoom-out in section 14 (`S14EndingTechTreeZoomOut`). The new orbital tree should replace those old tree scenes and add smaller visual echoes in early/mid sections.

## Section Placement

| Manifest Section | Existing Storyboard Scene | Orbital Tree Role | Placement Logic |
| --- | --- | --- | --- |
| 01 Opening | `S01TransformCivilization` | Fog glimpse only. | The narration says the transform pattern changed the technology tree before. Show partial glowing arcs and particles, not a readable map. This plants the map as a mystery. |
| 02 Classic Pattern | `S02PatternPipeline` | Classical foundation region. | As Fourier, Laplace, and DCT are named, reveal only the signal/media and dynamics/control regions. This connects the abstract pipeline to concrete branches. |
| 03 The New Thing | `S03LanguageVectors` | Learned-region handoff. | When language enters the transform pattern, cut from classical branches to the learned wedge. Do not show the full disk. |
| 04 Word Vectors | `S03bWordVectorAnalogy` | Local inset, not full map. | Begin/end with the embeddings node color or node glyph, but keep the vector-space explanation as its own scene. |
| 05 Pseudocode To Code | `S05CodeAndLoss` | LLM-to-code bridge echo. | Use the map briefly to show LLMs near the software boundary, then the existing code/loss visual carries the details. |
| 06 Multimodal Transforms | `S05bMultimodalAnalogy` | Learned-region expansion. | Light contrastive spaces, neural codecs, audio tokens, and multimodal tools locally. Still no full disk. |
| 07 The Loss | `S07SemanticTransformLoss` | Edge-tradeoff motif. | Use particle fog/dimming along the LLM-to-code edge as a short bridge into semantic transform loss. The core loss scene stays local. |
| 08 Why This Changes The Technology Tree | `S06cGameTechTree3D` | First large partial pullback. | Replace old grid/tree scene with an orbital partial reveal. Show classical, learned, and software regions belong to one map, but keep a side hidden by fog. |
| 09 Thinking In The Limit | `S09LimitTrends` | Frontier pressure. | Trends push from known disk toward particle fog. This turns the limit idea into spatial pressure without naming every frontier node. |
| 10 Validation And Verification | `S10ValidationVerification` | Load-bearing bridge. | Highlight code agents -> V&V/evidence -> reliable workflows as a scaffold near the frontier. Existing V-model can remain as a local inset. |
| 11 Self-Inhabiting Compute | `S11SelfInhabitingCompute` | Frontier inward loop. | A frontier node glows in the fog, connected back to reliable workflows. Then cut to the self-inhabiting compute loop. |
| 12 Outer Loop Experiments | `S12OuterExperimentLoop` | Frontier outward loop. | Particle orbit and experiment-loop node live in the shell. Then cut to the experiment cycle scene. |
| 13 Businesses Are Transform Pipelines | `S13BusinessPipelines` | Organizational overlay or optional echo. | This section may not need the tree. If used, keep it as a dim map underneath the pipeline to show workflows as transform paths. |
| 14 Ending | `S14EndingTechTreeZoomOut` | First complete reveal. | Replace old ending tree with the full orbital disk and frontier shell. This is the first time all wedges and bridges are readable together. |

## Five Reusable Reveal States

The Manim implementation should expose these states:

- `opening_glimpse`: particles and partial arcs; almost no labels; center blank.
- `classical_foundation`: signal/media and dynamics/control; Fourier, Laplace, DCT branches; modern regions masked.
- `modern_region`: learned/software regions; embeddings, transformers, LLMs, code agents; classical offscreen.
- `convergence_pullback`: multiple regions visible, raised bridges highlighted, one side still masked/fogged.
- `final_reveal`: full researched disk and frontier shell, still with sparse labels.

## Particle Fog Direction

Since the user wants maximum animation, particle fog should carry the reveal:

- Use many small low-opacity particles drifting around hidden regions.
- Particles should be color-tinted by nearby wedge identity, not just gray smoke.
- Opening: particles dominate; arcs are barely visible.
- Middle: particles act as masks at crop boundaries.
- Frontier: particles orbit as a shell and become a visual metaphor for not-yet-legible branches.
- Final: particles recede enough to show the whole disk while keeping frontier nodes uncertain.

## Implementation Shape

Create a reusable `OrbitalTechTreeMap` component and keep it separate from storyboard scenes.

Suggested files:

- `orbital_tech_tree_data.py`: node, wedge, edge, bridge, and reveal-state definitions.
- `orbital_tech_tree_map.py`: Manim component builder, fog particles, masks, reveal-state controls.
- `orbital_tech_tree_scenes.py`: prototype scenes and section-specific wrappers.

Do not wire it into `production_manifest.json` until the visual prototype passes keyframe review.

## Immediate Prototype

Build one prototype scene first:

1. Opening fog glimpse.
2. Classical foundation reveal.
3. Modern region reveal.
4. Convergence partial pullback with raised bridges.
5. Final reveal.

Render stills/keyframes, then use `image_review_pipeline/review_keyframes.py` with `--model auto`.
