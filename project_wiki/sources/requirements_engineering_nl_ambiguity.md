# Requirements Engineering — Natural Language Specification Problems

## Provenance

raw_file: null
raw_url: https://doi.org/10.1145/237432.237434
summary_method: llm-from-url
summary_verified: true

## Source

**Primary:** Zave, P., & Jackson, M. (1997). "Four Dark Corners of Requirements Engineering." *ACM Transactions on Software Engineering and Methodology (TOSEM)*, 6(1), pp. 1–30. DOI: https://doi.org/10.1145/237432.237434. PDF: https://cse.msu.edu/~chengb/RE-491/Papers/dark-corners-re-zave-jackson.pdf

**Secondary:** Davis, A. M. (1993). *Software Requirements: Objects, Functions, and States.* Prentice-Hall. ISBN 978-0137431755.

**Tertiary (if needed):** Berry, D. M., & Kamsties, E. (2009). "Ambiguity in Natural Language Requirements Specifications." In *Formal Methods for Requirements Engineering*, Springer. https://link.springer.com/chapter/10.1007/978-3-540-89778-1_1

## Why It Matters

The Verification Compiler exists specifically because natural language requirements are structurally insufficient — they embed implicit assumptions that are never written down, and those assumptions cause implementations to diverge from intent. These sources establish this as a recognized, studied problem in the requirements engineering literature, not just a practical observation. They ground the "English as a Specification Medium" motivation in peer-reviewed research.

## Key Ideas

**Zave & Jackson (1997):** Requirements expressed in natural language cannot be evaluated for correctness without reference to unstated domain assumptions the authors held when writing them. The "four dark corners" are: (1) requirements presupposing unstated domain properties, (2) domain properties that appear only implicitly in requirements, (3) requirements that inadvertently constrain the domain, (4) domain properties that inadvertently constrain requirements. Each corner is a class of specification gap that neither author nor reviewer will notice without a structured process.

**Davis (1993):** Ambiguity, incompleteness, and inconsistency are the three canonical defects of natural-language requirements documents, and they are the primary cause of mismatches between stakeholder intent and delivered systems.

## Useful Claims

- "Natural-language specifications are ambiguous, allow implicit assumptions, and cause implementation drift from intent" — Zave & Jackson (1997) is the primary citation; Davis (1993) supports the ambiguity/incompleteness bullets specifically.
- The word "drift" is well-captured by Zave & Jackson's framing: the implementation satisfies the stated requirements while violating the unstated domain assumptions the requirements author held.

## Requirements Impact

Justifies the Verification Compiler's requirement that all requirement-to-code trace links be explicit graph edges (not implicit or assumed). The graph traversal only works if implicit assumptions are surfaced as explicit nodes; these sources explain why that requirement is non-trivial.

## Follow-Up Questions

- Is there a Zave & Jackson follow-up or a safety-specific requirements engineering paper (e.g., Leveson *Engineering a Safer World*, 2012) that directly addresses this problem in safety-critical contexts? The current citations are general RE; a safety-domain source would strengthen the claim for this audience.
- How does the Verification Compiler handle requirements that cannot be expressed as explicit graph nodes — are those out of scope for Stage 1?
