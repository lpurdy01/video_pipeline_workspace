# Research Prompt: Representation Transform Technology Tree

We are making a public-facing 3Blue1Brown-style YouTube video for smart
generalists and engineers. The core claim is:

`representation -> vector/transform space -> computation -> representation`

The user rejected a row-based technology-tree graphic because it implied false
lineage, especially that speech/audio agents descend from Fourier. We need a
clearer concept lineage that distinguishes:

- classical mathematical transforms such as Fourier, Laplace, and DCT;
- compression/control/signal-processing applications unlocked by those
  transforms;
- learned representation systems: embeddings, neural networks, transformers,
  contrastive multimodal spaces, diffusion/generative decoders;
- practical LLM workflows: code agents, research assistants, V&V systems,
  speech/audio agents, multimodal tools;
- speculative civilization-scale branches, clearly marked as speculative.

Please produce a concise technical lineage review for the visual design:

1. Which edges are accurate enough for a high-level visual?
2. Which edges are misleading and should be avoided?
3. What should the graph show as convergent prerequisites rather than direct
   descent?
4. Suggest a Mermaid DAG with 25-35 nodes and edge labels where helpful.
5. Keep language careful: metaphorical lineage is okay, exact mathematical
   descent should not be overstated.
