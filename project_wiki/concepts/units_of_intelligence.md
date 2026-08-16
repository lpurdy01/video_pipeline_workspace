# Units of Intelligence

## Definition

A unit of intelligence is any entity — human, model, tool, team, or organization — that receives information, applies some form of reasoning or processing, and produces outputs. The concept is useful because it creates a common vocabulary for comparing humans and AI systems as participants in verification workflows.

## Properties

### Capacity

The amount of information a unit can actively reason over at one time. For humans, this is analogous to working memory — the set of facts, constraints, and relationships that can be held in mind simultaneously. For language model agents, this is the context window.

Capacity is finite for all units. This is not a weakness to overcome but a design constraint to plan around. The verification compiler's graph traversal is the primary mechanism for managing capacity: each verification query is sized to fit within the context window of the model evaluating it, just as a human reviewer is assigned a bounded review packet rather than the entire codebase at once.

### Accuracy

The degree to which the unit produces correct judgments. Accuracy is not a single global property — it is task-specific. A model may be highly accurate at identifying whether a function's documented pre/post conditions are satisfied by its implementation, and less accurate at reasoning about timing behavior in an interrupt-driven embedded system.

Accuracy is the key input to the verification compiler's confidence score. The overall codebase confidence is computed from per-query results weighted by the model's demonstrated accuracy profile for that task type. This means model evaluation is not just a research question — it is a component of the system's output.

### Adaptability

The degree to which the unit adjusts its behavior in response to new information, examples, corrections, and changed context. For humans, adaptability operates at multiple timescales: moment-to-moment reasoning adjustment, day-to-day learning, and career-length accumulation of domain expertise. For language models, adaptability within a context window (in-context learning) is strong; accumulating experience across sessions without retraining is not.

One useful framing: building a foundation model is more like recreating the structures developed through biological evolution — the substrate for learning — than like a human brain adapting. Humans arrive with enormous prebuilt structure that enables fast adaptation from relatively little experience. This distinction matters for how models should be deployed: they may be best used within well-defined, stable task contexts where their in-context adaptability is sufficient, rather than in open-ended tasks requiring long-term accumulation.

*(Citation target: Dario Amodei or Anthropic writing on model capabilities, adaptation, and the distinction between training-time and inference-time learning.)*

### Specialization

The degree to which the unit is optimized for a particular class of tasks. Specialization and capacity interact: a specialized unit can often accomplish more within a given capacity than a generalist, because it brings relevant priors, vocabulary, and heuristics to the task.

In the verification compiler, specialization is managed through task framing: prompts, contexts, and tool access are tuned for specific verification task types (requirements consistency checking, test coverage analysis, datasheet constraint verification, etc.). A model doing requirements consistency checking is not the same unit-in-practice as the same model doing memory-safety analysis, even if it is the same base model.

### Reviewability

The degree to which a unit's work can be inspected, challenged, reproduced, or validated by another unit. This is a structural property of the unit's output, not just a property of the unit itself.

Human review outputs (code review comments, test results) are partially reviewable — they record conclusions but not always full reasoning chains. Language model outputs can be made highly reviewable if the system requires structured output: specific claims, evidence citations, confidence levels, and reasoning traces. This is a design choice in the verification compiler — outputs must include enough structure to be independently evaluated.

Reviewability is also what enables dual-mode operation: LLM outputs and human outputs use the same evidence structure, so either can be reviewed by the other.

### Qualification

The degree to which the unit has been validated as capable of performing a specific delegated task. Qualification is not a global property — it is task- and context-specific. An engineer qualified to review flight software may not be qualified to review medical device firmware, even if both are safety-critical.

For model units, qualification is inspired by the DO-330 tool qualification pattern (see [Model or Tool Qualification](model_or_tool_qualification.md)):
- Define the task type and the acceptable failure rate
- Evaluate model accuracy on representative examples
- Establish usage boundaries (what inputs are in scope, what are not)
- Require human review gates for results that fall below confidence thresholds

Qualification records are attached to model units, not to models in the abstract. A new prompt structure, a new tool chain, or a new task type requires re-qualification.

## How These Properties Interact in the Verification Compiler

The verification compiler is explicitly designed around these properties:

| Property | How the compiler handles it |
|---|---|
| Capacity | Graph traversal produces verification queries sized to fit within model context windows |
| Accuracy | Task-specific accuracy profiles weight the per-query results into a composite confidence score |
| Adaptability | Stable, well-defined task types are used so in-context adaptability is sufficient |
| Specialization | Prompts and tool access are tuned per task type, not left as open-ended general queries |
| Reviewability | Structured output format required: claim, evidence, confidence, reasoning trace |
| Qualification | Models are evaluated on representative tasks; qualification records track task type and conditions |

## Organizations as Units

Human organizations are composite units of intelligence. They accomplish work that exceeds the capacity of any individual by decomposing tasks, specializing roles, establishing review structures, and coordinating through shared process standards. Safety-critical engineering standards (DO-178C, ISO 26262, IEC 62443) are mature coordination patterns for human units operating in high-stakes environments.

The verification compiler applies the same decomposition logic to hybrid human-model organizations: some queries go to models, some to humans, and the graph structure ensures that neither is asked to reason over more than its capacity allows.

## Open Questions

- What is the right unit of accuracy measurement for a model doing requirements verification? (Pass/fail per query? Per requirement? Per code module?)
- How should the system represent a model that is accurate on average but fails unpredictably on edge cases?
- What is the minimum qualification evidence needed before a model's outputs enter the evidence graph?
- How do accuracy profiles degrade over time as models are updated or as codebase complexity increases?
