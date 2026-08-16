# Loss Terms Research

## Question

What term is emerging for the kind of loss or distortion that occurs when LLMs transform one representation into another?

## Short Answer

There does not appear to be one settled umbrella term for this exact concept. The closest active terms are:

- **lossy compression**
- **semantic compression**
- **semantic drift**
- **context degradation**
- **confabulation**
- **information bottleneck**

For this project, the best working phrase may be **semantic transform loss** or **representational drift**. Use community terms when citing existing work, and use the project term when explaining the broader mental model.

## Candidate Terms

### Lossy Compression

This is the broadest and most intuitive analogy. Some current LLM research explicitly frames LLM training as lossy compression: models retain information relevant to their objective while discarding other detail. This aligns well with the JPEG analogy.

Use when discussing the model as a learned compressed representation of training data or task-relevant regularities.

Risk: "compression" can sound like the model stores and reconstructs documents, which is misleading if used too casually.

### Semantic Compression

This term appears in LLM research about compressing prompts, context, text, or code while preserving meaning or intent rather than exact wording.

Use when discussing summarization, context reduction, prompt compression, and the idea that exact reconstruction is less important than preserving semantic intent.

Risk: it covers a narrower technical area than the whole representation-transform argument.

### Semantic Drift

This term is useful for the way meaning shifts across repeated summaries, long conversations, agent chains, or transformations. It names the gradual movement away from the original semantic target.

Use when a requirement, plan, or concept is transformed multiple times and the output remains plausible but no longer means exactly what the input meant.

Risk: "drift" emphasizes multi-step movement over time, not one-shot transformation loss.

### Context Degradation

This term describes loss of reliability when a system's ability to represent or use critical context is impaired. It is useful for long-context and agentic systems.

Use when the loss comes from missing, diluted, corrupted, or over-compressed context.

Risk: it is broader than representation transformation and includes several failure modes.

### Confabulation

Confabulation is increasingly used as an alternative to hallucination when an LLM fills missing information with plausible fabricated content.

Use when the transform does not merely lose information but invents a coherent bridge over the gap.

Risk: it is mostly about false generated content, not all forms of transform loss.

### Information Bottleneck

This is a more technical framing: learned representations preserve task-relevant information while compressing away other detail.

Use when citing technical work, especially around training and representation learning.

Risk: too technical for the main video unless visualized simply.

## Recommended Project Language

Use this layered vocabulary:

- **lossy representation transform** for the broad analogy;
- **semantic transform loss** for the information that disappears, gets abstracted, or becomes assumption-shaped during transformation;
- **semantic drift** for cumulative meaning shift across repeated transformations;
- **confabulation** for plausible invented details that fill missing information;
- **context degradation** when the system fails because critical context is missing or diluted.

## Sources Reviewed

- Henry Gilbert, Michael Sandborn, Douglas C. Schmidt, Jesse Spencer-Smith, Jules White, ["Semantic Compression With Large Language Models"](https://arxiv.org/abs/2304.12512), arXiv, 2023. The paper frames LLM-based compression as approximate compression that may preserve semantic intent without exact recovery.
- Weizhi Fei et al., ["Extending Context Window of Large Language Models via Semantic Compression"](https://arxiv.org/abs/2312.09571), arXiv, 2023. The paper uses semantic compression to reduce semantic redundancy in long inputs.
- Henry C. Conklin et al., ["Learning is Forgetting: LLM Training As Lossy Compression"](https://arxiv.org/abs/2604.07569), arXiv, 2026. The abstract explicitly frames LLMs as lossy compression and invokes an information-theoretic framing.
- Yan Zhao, ["Distance-Based Compression Method for Large Language Models"](https://www.mdpi.com/2076-3417/15/17/9482), Applied Sciences, 2025. Uses quality/stability metrics including information loss and semantic drift for cache compression.
- ["Context Degradation in AI Systems"](https://www.emergentmind.com/topics/context-degradation), Emergent Mind, updated 2025. Summarizes context degradation, semantic drift, and fact retention metrics in LLM and agent systems.

