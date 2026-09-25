# Training failure modes for the shared vision case

Inspected the locally retained original AMLAS v1.1 PDF and the official online *Deep Learning* Chapter 5. These sources are method and textbook evidence, not road or air product evidence.

- AMLAS makes sensor viewpoint, lighting, partial-occlusion labels, data completeness and balance concrete design questions. [C-TRAIN-001]
- Its model-learning stage names overfitting, simulator artifacts, internal-test leakage and documented selection choices. [C-TRAIN-002]
- Its independent verification stage looks for realistic failure classes and performance under unseen/adverse conditions. A held-out result remains limited by the scenario distribution and cannot establish universal generalization. [C-TRAIN-003]
- The textbook supplies the narrow underfitting/overfitting capacity distinction. The project uses this to explain why both an insufficient model and an apparently high-scoring memorizer can fail the vision task. [C-TRAIN-004]

The project's proposed training regime and road-to-air interface are explicit design propositions. They are not asserted as prescribed by AMLAS or accepted by a regulator.
