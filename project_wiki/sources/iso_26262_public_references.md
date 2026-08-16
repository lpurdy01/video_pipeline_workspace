# ISO 26262 Public References Source Note

## Provenance

raw_file: null
raw_url: https://www.iso.org/standard/68383.html
summary_method: llm-from-url
summary_verified: false

## Source

ISO 26262, "Road vehicles — Functional safety," is a licensed standard (ISO). These public references serve as citable proxies, following the same strategy as DO-178C (represented via NASA/FAA docs rather than the licensed RTCA standard itself).

## Public References

### U.S. Government (High Citability)

**Volpe National Transportation Systems Center (U.S. DOT)**
- Assessment of the ISO 26262 Standard, "Road Vehicles — Functional Safety"
- Publisher: U.S. Department of Transportation, John A. Volpe National Transportation Systems Center
- URL: https://www.volpe.dot.gov/sites/volpe.dot.gov/files/docs/Assessment%20of%20the%20ISO%2026262%20Standard,%20%E2%80%9CRoad%20Vehicles%20%E2%80%93%20Functional%20Safety%E2%80%9D.pdf
- Coverage: Direct government assessment of ISO 26262 structure, ASIL levels, verification requirements, explicit comparison with DO-178C and MIL-STD-882E

**NHTSA Safety Standards Assessment**
- "Assessment of Safety Standards for Automotive Electronic Control Systems"
- Publisher: National Highway Traffic Safety Administration (U.S. DOT)
- URL: https://www.nhtsa.gov/document/assessment-safety-standards-automotive-electronic-control-systems
- Coverage: Comprehensive comparison of ISO 26262 against DO-178C, MIL-STD-882E, and IEC 61508; ASIL determination methodology; hazard analysis methods; verification evidence types

**NHTSA System-Specific Functional Safety Assessments (DOT HS series)**

These apply ISO 26262 Concept Phase methodology to real automotive systems, documenting the evidence artifacts the standard requires:

- DOT HS 812 574 — Generic Hydraulic Braking System: https://www.nhtsa.gov/sites/nhtsa.gov/files/documents/13497a_812574_hydraulicbrakingsystem.pdf
- DOT HS 812 573 — Automated Lane Centering System: https://www.nhtsa.gov/sites/nhtsa.gov/files/documents/13498a_812_573_alcsystemreport.pdf
- DOT HS 812 575 — Electric Power Steering: https://www.nhtsa.gov/sites/nhtsa.gov/files/documents/13501_812575_electricpowersteeringreport.pdf
- DOT HS 812 576 — Steer-by-Wire System: https://www.nhtsa.gov/sites/nhtsa.gov/files/documents/13502_812576_steerbywire.pdf

## Why It Matters

ISO 26262 is the dominant safety standard for automotive systems and is one of the three standards explicitly named in the Beningo "embedded moats" counterargument (alongside DO-178C and IEC 62443). Having public-citeable references for all three allows the whitepaper to argue that the evidence-structure argument applies across multiple regulated safety domains, not just aerospace.

The Volpe/NHTSA documents are especially valuable because they make cross-standard comparisons explicit — particularly the comparison between ISO 26262's ASIL levels and DO-178C's DAL (Design Assurance Level) levels.

## Key Ideas

- ISO 26262 uses ASIL (Automotive Safety Integrity Level) A–D to classify safety requirements by risk, determined by three factors: Severity (S), Exposure (E), and Controllability (C).
- The standard requires a structured safety case: bidirectional traceability from safety goals through design, implementation, verification, and validation evidence.
- Verification evidence types include: hazard analysis records, functional safety requirements with traceability matrices, design specifications, test plans, test results, code review records, and configuration management records.
- The Volpe/NHTSA assessments explicitly note that ISO 26262, like DO-178C, centers verification on evidence production and traceability rather than on any specific technology or method.

## Useful Claims

- ISO 26262 defines safety integrity levels (ASIL A–D) analogous to DO-178C's Design Assurance Levels (DAL A–E); both tie verification rigor to hazard severity.
- Both standards define verification as producing auditable life-cycle evidence — the method of producing that evidence is not specified, only the objective and evidence structure.
- Government assessment of ISO 26262 (Volpe/NHTSA) is publicly available and citable as the primary proxy for the licensed standard text, paralleling NASA/FAA as proxy for DO-178C.

## Requirements Impact

- The verification compiler's evidence model should generalize across ASIL and DAL levels, not only DO-178C DAL assumptions.
- The whitepaper can argue that the structured-evidence-production approach applies to automotive safety software, not just aerospace, broadening the thesis.
- Source notes should track which claims come from NHTSA/Volpe proxy sources vs. licensed ISO 26262 text.

## Follow-Up Questions

- Has NHTSA or any U.S. regulator published formal guidance on AI/ML tool use under ISO 26262 (analogous to the DO-178C supplement DO-333 for formal methods)?
- Does the Volpe comparison of ISO 26262 and DO-178C identify any structural differences in their evidence requirements that matter for the verification compiler design?
- Which ASIL level is the right target for the whitepaper's initial scope (likely ASIL B or C as a starting point, not ASIL D)?
