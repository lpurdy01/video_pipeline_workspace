# NASA-STD-8739.8B Source Note

## Provenance

raw_file: refrence_literature/raw/extracted_markdown/nasa_std_8739_8b.txt
raw_url: https://standards.nasa.gov/standard/nasa/nasa-std-87398b
summary_method: llm-extract-from-raw
summary_verified: false

## Source

NASA-STD-8739.8B, `Software Assurance and Software Safety Standard`, approved September 8, 2022.

Local files:

- `refrence_literature/raw/pdfs/nasa_std_8739_8b.pdf`
- `refrence_literature/raw/extracted_markdown/nasa_std_8739_8b.txt`

Public URL:

https://sma.nasa.gov/docs/default-source/policies/nasa-std-8739-8b.pdf

## Why It Matters

This is a public NASA technical standard for software assurance and software safety. It supports the whitepaper's claims about traceability, IV&V, hazard linkage, requirements quality, code-to-requirement relationships, tests, objective criteria, and audit participation.

## Key Ideas

- IV&V providers must ensure known software-based hazard causes, contributors, and controls are identified, documented, and trace to project requirements.
- In-scope software and system requirements are expected to be correct, consistent, complete, accurate, readable, traceable, and testable.
- IV&V includes validating relationships between requirements and architecture, design, code, tests, and results.
- Evaluating relationships among source code, design, and requirements provides evidence that only specified capabilities are in the system.
- Test artifacts should contain objective acceptance criteria supporting verification under nominal and off-nominal conditions.
- Test analysis includes traceability between tests and requirements.

## Useful Claims

- Public NASA assurance guidance supports the idea that traceability is an evidence-producing relationship, not merely documentation.
- Hazard-related software assurance depends on linking hazards, controls, requirements, implementation, tests, and results.
- IV&V provides a useful model for independent model-agent review or challenge in a verification compiler.

## Requirements Impact

- Verification compiler trace links should support hazard/control/requirement relationships.
- Evidence records should support objective acceptance criteria.
- Independent review and challenge should be represented as first-class evidence states.
- Traceability should connect requirements to architecture, design, code, tests, and results where available.

## Follow-Up Questions

- Which NASA-STD requirements should become direct Stage 2 prototype requirements?
- Should the project create a hazard/control traceability page even before it has implementation code?
