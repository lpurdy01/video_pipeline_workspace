# Traceability Link Requirements

## Requirement

The verification compiler shall represent every promoted traceability relationship as a stable link record with an ID, source node, target node, relation type, evidence location, status, and review history.

## Rationale

Graphify can discover useful candidate relationships, but its ordinary pairwise graph edges do not provide citation-grade stable link IDs by default. A verification compiler needs trace links that can be reviewed, challenged, updated, and cited without depending on graph rendering order.

## Source Support

- Rierson emphasizes documenting traceability as requirements are written and warns that correcting tracing later is virtually impossible. See Rierson Markdown line 8304.
- Rierson describes traceability analyses as ensuring complete and accurate bidirectional traceability among requirement levels and test data. See Rierson Markdown line 6073.
- NASA Jacklin describes DO-178C bidirectional traceability across requirements, source code, tests, procedures, and test results. See `nasa_ntrs_20120016835_jacklin_do178c.txt` line 255.
- NASA-STD-8739.8B requires traceability from hazard causes/controls to project requirements and validates relationships among requirements, design, code, tests, and results. See `nasa_std_8739_8b.txt` lines 2088 and 2214.

## Verification Method

- Inspect generated traceability records for required fields.
- Confirm link IDs remain stable after graph regeneration.
- Confirm each `verified` link has a checkable evidence location.
- Confirm Graphify-discovered links remain `candidate` until promoted.

## Open Questions

- Should link records be stored first in Markdown, JSON, or both?
- Should edge IDs include content hashes of source spans?
