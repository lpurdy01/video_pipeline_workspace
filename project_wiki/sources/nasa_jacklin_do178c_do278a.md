# NASA Jacklin DO-178C and DO-278A Source Note

## Provenance

raw_file: refrence_literature/raw/extracted_markdown/nasa_ntrs_20120016835_jacklin_do178c.txt
raw_url: https://ntrs.nasa.gov/citations/20120016835
summary_method: llm-extract-from-raw
summary_verified: false

## Source

Stephen A. Jacklin, NASA Ames Research Center, `Certification of Safety-Critical Software Under DO-178C and DO-278A`, NASA NTRS citation 20120016835.

Local files:

- `refrence_literature/raw/pdfs/nasa_ntrs_20120016835_jacklin_do178c.pdf`
- `refrence_literature/raw/extracted_markdown/nasa_ntrs_20120016835_jacklin_do178c.txt`

Public URL:

https://ntrs.nasa.gov/api/citations/20120016835/downloads/20120016835.pdf

## Why It Matters

This NASA paper provides a public secondary overview of the DO-178C document family, including DO-330 tool qualification and supplements. It is especially useful because the actual RTCA standards are licensed.

## Key Ideas

- DO-178C was released with companion documents: DO-248C, DO-330, DO-331, DO-332, and DO-333.
- DO-178B/DO-178C are framed around producing life-cycle evidence that high-quality software development processes were appropriately implemented.
- DO-178C emphasizes two-way or bidirectional traceability across requirements, code, tests, procedures, and test results.
- The paper links traceability to avoiding orphan/dead source code.
- Tools used to generate or verify software must themselves be qualified, with levels tied to use and software assurance level.
- DO-330 provides guidance for tools used to create software and tools used to verify software, and includes tool operational requirements.

## Useful Claims

- Bidirectional traceability is a public NASA-supported description of DO-178C expectations.
- Tool qualification is project/use-context dependent; a tool qualified for one project is not automatically qualified for another.
- Tool qualification can inspire model-unit qualification, but the analogy must remain explicit and limited.

## Requirements Impact

- Trace links should be bidirectional, verifiable, and capable of revealing orphan artifacts.
- Model-unit qualification should include task context and operational assumptions.
- A verification compiler should link requirements to implementation checks, tests, procedures, and results as different node types.

## Follow-Up Questions

- Can the verification compiler's trace graph detect "orphan code" or "orphan claim" analogues in research artifacts?
- How should tool operational requirements map onto "model operational requirements" for agent units?
