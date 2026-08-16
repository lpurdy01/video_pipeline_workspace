# Production Process

## Goal

Produce two connected outputs:

- a standalone whitepaper or LinkedIn article explaining learned representation transforms;
- a narrated 3Blue1Brown-style explanatory video, likely 4 to 8 minutes, using diagrams, technology-tree graphics, and animation.

The target audience is smart generalists, engineers, and people who spend time with high-quality YouTube explainers. Fourier and Laplace transforms can be referenced visually and conceptually without pausing for full derivations.

## Working Loop

1. **Concept pass**
   - Clarify the core thesis.
   - Separate metaphor, technical claim, and speculative implication.
   - Decide the target audience.

2. **Source pass**
   - Watch and summarize the user-provided videos.
   - Add technical sources for citations.
   - Map sources to claims.

3. **Visual pass**
   - Sketch static diagrams first.
   - Turn strongest diagrams into animation beats.
   - Use a consistent visual grammar: input representation, transform space, computation, output representation, verification boundary.

4. **Script pass**
   - Write a 4 to 8 minute narration.
   - Keep the Fourier/Laplace analogy vivid but bounded.
   - Make the technology-tree significance the landing point.
   - Use pseudocode-to-code as the central practical example.

5. **Prototype pass**
   - Use Manim for geometry, vector spaces, arrows, transforms, and graph/tree animations.
   - Use static Markdown diagrams or Mermaid for early review before animation.
   - Export stills for the document.

6. **Review pass**
   - Check for overclaims.
   - Check that every technical claim has support.
   - Check that the concept remains standalone and does not depend on the verifiability compiler.

## Proposed Folder Roles

```text
representation_transform_visuals/
  README.md
  concept_brief.md
  visual_storyboard.md
  tech_tree.md
  sources.md
  production_process.md
  drafts/
    script.md
    whitepaper_section.md
  assets/
    exported_stills/
    sketches/
  manim_prototypes/
    representation_transform_scene.py
```

## Definition of Done for First Usable Draft

- A 1,500 to 2,500 word whitepaper section exists.
- A 6 to 10 scene storyboard exists.
- The source ledger has at least one technical citation per major claim.
- At least three diagrams are exported as stills.
- One Manim scene demonstrates the representation-transform pipeline.
- A LinkedIn-ready article draft exists.
