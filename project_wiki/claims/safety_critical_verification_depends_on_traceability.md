# Safety-Critical Verification Depends on Traceability

## Claim

Safety-critical verification depends on maintained traceability between requirements, implementation artifacts, verification activities, and verification results.

## Status

Candidate, supported by Rierson source passages. Needs additional standards or NASA/source support before final whitepaper use.

## Supporting Sources

- Rierson: traceability should be documented while requirements are written; reconstructing it later is described as virtually impossible. Source note: [Rierson DO-178C](../sources/rierson_do178c.md). Evidence location: Rierson Markdown line 8304.
- Rierson: formal requirements review includes checking that high-level software requirements trace to system requirements, with bidirectional expectations. Evidence location: Rierson Markdown line 8503.
- Rierson: verification analyses include complete and accurate bidirectional traceability among system requirements, high-level requirements, low-level requirements, and test data. Evidence location: Rierson Markdown line 6073.
- [NASA Jacklin DO-178C and DO-278A](../sources/nasa_jacklin_do178c_do278a.md): public NASA overview describes DO-178C bidirectional traceability across requirements, source code, test cases, procedures, and results. Evidence location: `nasa_ntrs_20120016835_jacklin_do178c.txt` line 255.
- [NASA-STD-8739.8B](../sources/nasa_std_8739_8b.md): IV&V requirements link hazard causes and controls to requirements, and validate relationships between requirements, architecture, code, tests, and results. Evidence locations: `nasa_std_8739_8b.txt` lines 2088, 2214.

## Challenges or Uncertainty

- Rierson and Jacklin are aviation/DO-178C-oriented sources; NASA-STD broadens support into NASA software assurance, but the whitepaper should still avoid claiming universality across all safety-critical domains.
- The project should distinguish "traceability is necessary for DO-178C-style assurance" from "traceability alone proves correctness."

## Whitepaper Use

Use in Stage 1 sections:

- `4. Safety-Critical Engineering as an Existing Coordination Pattern`
- `6. Verification Compiler Concept`
- `7. Requirements for the Stage 2 Prototype`
