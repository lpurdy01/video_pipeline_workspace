# Tech Tree Concept Art Review

Generated concepts:

- `representation_transform_visuals/agent_tools/out/tech_tree_concepts/01_circular_radial_wedge_map.png`
- `representation_transform_visuals/agent_tools/out/tech_tree_concepts/02_circular_3d_orbital_skill_tree.png`
- `representation_transform_visuals/agent_tools/out/tech_tree_concepts/03_rectangular_research_atlas_board.png`

## Best Overall Direction

Use the circular radial wedge map as the base structure. It most directly matches the user direction: a blank center origin, real category-start nodes around it, wedge categories resized to fit contents, and capabilities spinning outward.

The 3D orbital version contributes two strong ideas:

- Treat the frontier as a translucent outer shell rather than a wedge.
- Draw convergence edges, especially neural SSMs, as elevated bridges that pass over category boundaries.

The rectangular atlas is clearer for reading individual chains, but it feels less like a skill tree. It may be useful for an article figure or fallback explanatory diagram, not the flagship video visual.

## What To Borrow

- Four large wedges: signal/media, dynamics/control, learned representations, language/code/verification.
- A faint outer frontier ring/shell with low-contrast speculative nodes.
- A small unlabeled center origin; do not call it "representation transforms" or "origin visual" on screen.
- Color-coded wedge arcs with radial depth rings.
- Neural SSMs as a glowing bridge between state-space/control and transformer/LLM sequence models.
- Sparse labels at first, then staged label reveal as narration discusses each branch.

## What To Avoid

- Do not show every node at once in the video.
- Do not duplicate nodes in multiple positions unless it is intentionally a convergence marker.
- Do not label the center as a concept.
- Do not make the frontier look like a fifth normal category.
- Do not let 3D perspective make text unreadable.
- Do not imply exact lineage where the relationship is analogy or convergence.

## Manim Implementation Direction

Start with a 2D radial scene:

1. Place a tiny center point.
2. Allocate wedge angles by node count:
   - Signal/media: large wedge because Fourier plus DCT has many concrete payoffs.
   - Dynamics/control: medium wedge.
   - Learned representation spaces: large wedge.
   - Language/code/verification: medium wedge.
3. Draw radial rings for depth from foundational transforms to modern capabilities.
4. Use Bezier or arc edges inside wedges.
5. Use dashed or elevated-looking curves for convergence edges.
6. Add a translucent frontier halo outside the final ring.

Then experiment with a 3D variant:

1. Keep the main tree readable in a near-flat disk.
2. Raise convergence bridges slightly on the z-axis.
3. Raise or wrap the frontier as a translucent outer shell.
4. Use camera motion sparingly: a small orbit to reveal depth, then settle back to a readable top-down view.

## Open Design Questions

- Is brushless motor control the right concrete payoff for Laplace/control, or should flight/robotics stability become the primary visible payoff?
- Should DCT be visually a sibling of Fourier or a practical sub-branch in the same signal/media wedge?
- Should V&V/evidence systems be in the main video tree or reserved for the article?
- How much of the frontier should be readable versus only hinted?
