# Self-Inhabiting Compute Research Notes

Status: early research pass for the "thinking in the limit" section.

Purpose: make the self-inhabiting compute idea novel and technically grounded enough for the next script pass without pretending the claim is already an established field.

## Core Claim To Develop

The novel idea is not "runtime code generation exists."

That already exists in many forms:

- JIT compilation;
- dynamic linking;
- runtime CUDA compilation;
- self-modifying code;
- reflective systems;
- optimizing compilers;
- evolutionary code search.

The stronger limit thought is:

```text
learned representation transform
-> low-level executable representation
-> immediate execution on the compute substrate
-> telemetry/state/performance returns to the transform
-> the system generates the next executable behavior
```

In the limit, software stops being only an artifact that the machine runs. It becomes part of a live representational feedback loop in which the machine can transform its own state, goals, constraints, and execution traces into new executable behavior.

Working phrase:

```text
self-inhabiting compute
```

## Technical Anchors

### PTX Is An Intermediate Execution Representation

NVIDIA describes PTX as a low-level parallel-thread-execution virtual machine and instruction set architecture that exposes the GPU as a data-parallel computing device.

Source:

- NVIDIA PTX ISA documentation: https://docs.nvidia.com/cuda/archive/10.2/parallel-thread-execution/index.html

Implication for script:

- Do not describe PTX as literal hardware machine code.
- Better wording: "a PTX-like intermediate execution layer" or "a low-level executable representation that can be compiled onto the hardware."
- PTX is useful because it already sits near the boundary between symbolic code and hardware execution.

### Runtime Compilation Already Exists

NVIDIA's NVRTC is a runtime compilation library for CUDA C++. Its documentation says the generated PTX string can be loaded through CUDA driver APIs and linked with other modules.

Source:

- NVIDIA NVRTC documentation: https://docs.nvidia.com/cuda/archive/11.0/nvrtc/index.html

CUDA tooling also supports JIT compilation from PTX at runtime.

Source:

- NVIDIA CUDA compiler documentation: https://docs.nvidia.com/cuda/cuda-compiler-driver-nvcc/

Implication for script:

- The grounded comparison is: current systems can generate/compile specialized code at runtime.
- The limit thought is: learned transforms could decide, generate, validate, and execute those specializations as part of an adaptive loop.

### LLVM ORC JIT Shows The General Pattern

LLVM's ORC JIT is designed to JIT arbitrary LLVM IR and emulate linker/symbol-resolution behavior used by static and dynamic linkers.

Source:

- LLVM ORC documentation: https://llvm.org/docs/ORCv2.html

Implication for script:

- The JIT world already treats code as something that can be materialized during execution.
- The transform hypothesis asks what happens when the generator is not only a compiler pipeline, but a model operating over intent, constraints, runtime traces, and performance feedback.

### Autonomous Code Search Is Already Pointing At The Loop

Google DeepMind describes AlphaEvolve as a Gemini-powered evolutionary coding agent for algorithm discovery and optimization. It pairs LLM generation with automated evaluators and an evolutionary framework.

Source:

- Google DeepMind AlphaEvolve blog: https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/

Implication for script:

- This is not self-inhabiting compute, but it is a nearby pattern: generate candidate code, evaluate it, keep the better ones, repeat.
- The limit version tightens the loop until generation, execution, evaluation, and revision become part of the system's own runtime.

### Self-Driving Labs Show The Same Shape In The Physical World

The A-Lab autonomous laboratory integrates robotics, databases, ML interpretation, text-mined synthesis heuristics, and active learning to optimize materials synthesis. The Nature paper reports that failed recipes trigger active-learning follow-up recipes.

Source:

- A-Lab Nature paper: https://www.nature.com/articles/s41586-023-06734-w

A Nature Synthesis review frames self-driving labs as integrating machine learning, lab automation, and robotics.

Source:

- Self-driving labs review: https://www.nature.com/articles/s44160-022-00231-0

Implication for script:

- Autonomous experiment loops are not novel by themselves.
- They become interesting here as the outward-facing version of the same loop:

```text
representation -> generation -> execution -> measurement -> updated representation
```

If self-inhabiting compute is the machine turning the loop inward, autonomous experiment loops are the machine turning the loop outward into the world.

### V&V Is The Containing Structure

NASA's Systems Engineering Handbook distinguishes verification and validation clearly:

- verification: whether the product was done right;
- validation: whether the right product was done.

Source:

- NASA Systems Engineering Handbook: https://www.nasa.gov/sites/default/files/atoms/files/nasa_systems_engineering_handbook_0.pdf

NIST maintains AI risk-management guidance and a generative AI profile for identifying and managing generative AI risks.

Source:

- NIST AI Risk Management Framework: https://www.nist.gov/itl/ai-risk-management-framework

Implication for script:

- V&V is not a boring safety-process detour.
- It is the thing that makes the far-out limit survivable.
- If generation becomes cheap and live, validation and verification become the boundary between useful adaptive systems and uncontrolled plausible behavior.

## Revised Limit Arc

### Section A: V&V Becomes The Work

Trend:

```text
generation cost down
accuracy up
complexity up
```

Limit:

```text
plausible artifacts become abundant
validated artifacts become scarce
```

Point:

Before going to the far-out sections, establish that generation without validation is not civilization-scale progress. It is output pressure.

### Section B: Self-Inhabiting Compute

Trend:

```text
accuracy up enough for constrained low-level generation
complexity up enough to reason over hardware/runtime state
generation cost down enough to regenerate behavior continuously
```

Limit:

```text
the machine can transform state and intent into executable behavior inside its own runtime loop
```

Point:

Source code, compilers, binaries, and human inspection do not vanish. They become safety boundaries, audit surfaces, and sometimes optional intermediate representations.

### Section C: Autonomous Experiment Loops

Trend:

```text
generation cost down for hypotheses, simulations, procedures, and analysis
complexity up across entire experimental workflows
accuracy up enough to preserve scientific constraints
```

Limit:

```text
question -> experiment -> measurement -> updated question becomes a compressed loop
```

Point:

This is not just "robot labs exist." The bigger claim is that the same transform loop can be turned outward, so that compute systems generate actions in the world, observe what survives contact with reality, and transform the evidence back into the next representation.

## Novel Framing

The script should frame these as two nested loops around the same transform:

```text
inner loop:
runtime state -> executable behavior -> runtime state

outer loop:
hypothesis/intent -> experiment/action -> measurement/evidence -> updated hypothesis/intent
```

V&V surrounds both loops:

```text
validate the goal
verify the generated behavior
measure the result
feed evidence back in
```

This is more novel than saying:

- "AI will do science."
- "AI will write code."
- "AI will control robots."

The actual claim is:

```text
When representation transforms become cheap, accurate, and capable enough,
the important systems become closed loops of transformation, execution, evidence, and correction.
```

## Script Cautions

- Do not say PTX is the hardware ISA.
- Do not imply that self-modifying code is new.
- Do not imply that JIT compilation is itself AI.
- Do not make the loop sound safe by default.
- Do not make autonomous labs sound universally solved.
- Keep "in the limit" tied to the three trends: accuracy, complexity, cost.

## Possible Narration

```text
So the weirdest version is not that a model writes Python.

The weirdest version is that the machine has a representation of what it is doing, what it is trying to optimize, and what constraints it is not allowed to violate. It transforms that state into a low-level executable representation, runs it, measures what happened, and feeds that evidence back into the next transform.

That is not just software generation. That is a computer beginning to inhabit its own execution loop.
```

```text
And once you see that loop, the same shape appears outside the machine.

A hypothesis becomes an experiment. The experiment becomes a lab procedure or simulation. The measurement becomes evidence. The evidence becomes the next hypothesis.

The limit is not "AI gives better answers." The limit is compressed loops from representation to action to evidence and back.
```
