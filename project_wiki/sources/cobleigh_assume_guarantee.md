# Cobleigh, Giannakopoulou & Pasăreanu — Learning Assumptions for Compositional Verification (2002)

## Provenance

raw_file: refrence_literature/raw/extracted_markdown/cobleigh_assume_guarantee_ntrs.txt
raw_url: https://ntrs.nasa.gov/citations/20030017771
summary_method: llm-from-url
summary_verified: true

Note: Full PDF is image-based (scanned). Source note derived from abstract + NTRS metadata.
Full PDF is publicly downloadable at ntrs.nasa.gov (Public Use Permitted).

## Source

Cobleigh, J. M., Giannakopoulou, D., & Pasăreanu, C. S., & Clancy, D. (2002).
"Learning Assumptions for Compositional Verification."
NASA/RIACS Technical Report RIACS-TR-02.09. NASA NTRS 20030017771.
Research Institute for Advanced Computer Science, Ames Research Center.

Also presented as: TACAS 2003, Lecture Notes in Computer Science vol. 2619, pp. 331–346.

## Why It Matters

Provides formal methods lineage for the Verification Compiler's compositional decomposition. The state explosion problem in model checking (you cannot verify a large system in a single pass because the full state space is too large) is the formal methods equivalent of the context window constraint in LLM-based verification. Assume-guarantee reasoning solves this by decomposing a large system into bounded components, each verified against interface assumptions — exactly the structural principle behind VQP boundaries and DAG edges.

## Key Ideas

- **State explosion problem**: model checking for large systems is computationally intractable because the full state space cannot be held in memory simultaneously. Same constraint motivates LLM-based decomposition.

- **Assume-guarantee reasoning**: to verify composite system M = M1 || M2:
  1. Verify M1 against assumption A (what M1 expects from its environment)
  2. Verify M2 under constraint that it satisfies A
  3. If both hold → full system satisfies the target property
  Each component is verified independently against bounded interface specifications.

- **Automated assumption learning**: rather than requiring humans to specify assumptions manually, the framework uses a learning algorithm that iteratively refines assumptions through counterexamples from model checking — reducing the annotation burden.

- **Validation**: implemented in the LTSA (Labeled Transition System Analyzer) tool and validated on a NASA system, establishing aerospace applicability.

## Connection to Verification Compiler

The VQP boundary in the VC plays the role of the assume-guarantee interface:
- Each code unit (component M_i) is verified against its requirement chain and interface specifications (assumption A_i)
- The DAG edges encode which components' outputs serve as inputs/assumptions for which other components
- The VRM aggregates component-level verification verdicts into a system-level confidence score — the same compositional aggregation that assume-guarantee reasoning performs formally
