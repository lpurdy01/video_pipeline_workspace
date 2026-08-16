# Safety-Critical Traceability

## Definition

Safety-critical traceability is the maintained set of relationships between requirements, design artifacts, source code, verification cases, verification procedures, verification results, and higher-level system or safety rationale.

For this project, traceability means more than hyperlinks. A trace link should be a reviewable object with source, target, relation type, evidence, and status.

## Why It Matters

The verification compiler concept depends on decomposing natural-language requirements into bounded units, delegating checks, and preserving evidence. Without durable trace links, delegated verification results cannot be assembled into a credible evidence package.

## Related Claims

- [Safety-Critical Verification Depends on Traceability](../claims/safety_critical_verification_depends_on_traceability.md)
- [Verification Requires Review, Analysis, and Test](../claims/verification_requires_review_analysis_and_test.md)

## Source Support

- Rierson states that requirements should trace to parent requirements and that traceability should be documented as requirements are written; she warns that correcting tracing later is virtually impossible. See Rierson Markdown line 8304.
- Rierson describes bidirectional traceability in requirements reviews: system-level requirements allocated to software should have high-level software requirements implementing them, and high-level requirements should trace back unless derived. See Rierson Markdown line 8503.
- Rierson describes traceability analyses as ensuring complete and accurate bidirectional traceability among system requirements, high-level requirements, low-level requirements, and test data. See Rierson Markdown line 6073.
- NASA Jacklin describes DO-178C as requiring bidirectional traceability across system requirements, software requirements, code, test cases, procedures, and results. See `nasa_ntrs_20120016835_jacklin_do178c.txt` line 255.
- NASA-STD-8739.8B requires IV&V traceability from hazard causes/controls to requirements and validates relationships among requirements, architecture, design, code, tests, and results. See `nasa_std_8739_8b.txt` lines 2088 and 2214.

## Open Questions

- What relation vocabulary should the verification compiler use for requirements, evidence, and review results?
- Should trace links be stored as Markdown records, JSON records, or both?
