# IEC 62443 Public References Source Note

## Provenance

raw_file: null
raw_url: https://www.iec.ch/homepage
summary_method: llm-from-url
summary_verified: false

## Source

IEC 62443 is a series of licensed standards (IEC/ISA) for industrial automation and control systems (IACS) cybersecurity. These public references serve as citable proxies, following the same strategy used for DO-178C and ISO 26262.

## Public References

### U.S. Government (High Citability)

**CISA Cybersecurity Performance Goals (CPG) Report**
- Publisher: Cybersecurity and Infrastructure Security Agency, U.S. Department of Homeland Security
- CPG 2.0: https://www.cisa.gov/sites/default/files/2025-12/CPG_Report_2.0_508c.pdf
- CPG 1.0.1: https://www.cisa.gov/sites/default/files/2023-03/CISA_CPG_REPORT_v1.0.1_FINAL.pdf
- Landing page: https://www.cisa.gov/cross-sector-cybersecurity-performance-goals
- Coverage: Extensive explicit mapping to IEC 62443-2-1 and IEC 62443-3-3; describes verification objectives, security levels (SL1–SL4), foundational requirements (FR1–FR7); governance and implementation documentation requirements
- Citability: Very high — CISA is the federal agency responsible for critical infrastructure cybersecurity

**NIST SP 800-82 Revision 3 — Guide to Operational Technology (OT) Security**
- Publisher: National Institute of Standards and Technology
- Publication page: https://csrc.nist.gov/pubs/sp/800/82/r3/final
- Coverage: OT/ICS security guidance; explicit alignment with IEC 62443 framework; security assessment methodologies; evidence and documentation requirements
- Citability: Very high — foundational federal guidance referenced across critical infrastructure sectors

**NIST SP 800-53 Revision 5 — Security and Privacy Controls**
- Publisher: NIST
- URL: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf
- Coverage: Security control catalogue with implementation evidence requirements; applicable to ICS/OT environments; traceable control structure
- Citability: High — cross-referenced by IEC 62443 implementation guidance

### Industry/Standards Body (Medium-High Citability)

**ISA (International Society of Automation) — IEC 62443 Series Overview**
- Publisher: ISA (the U.S. standards development organization for IEC 62443; ISA/IEC 62443 is the joint designation)
- URL: https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards
- Secondary: https://isagca.org/isa-iec-62443-standards
- Coverage: Series structure overview, foundational requirements FR1–FR7, security levels, certification pathway
- Citability: High — ISA is the authoring SDO; its public summaries are authoritative descriptions of the standard's structure

**SANS Institute Whitepapers**
- "Effective ICS Cybersecurity Using the IEC 62443 Standard": https://www.sans.org/white-papers/39960
- "Managing ICS Security with IEC 62443": https://www.sans.org/white-papers/39990
- Coverage: Detailed FR1–FR7 walkthrough, security level methodology, verification and assessment procedures
- Citability: Medium-high — industry-standard technical education; useful for explanatory claims, secondary to government sources

## Why It Matters

IEC 62443 is one of the three standards explicitly named in the Beningo "embedded moats" counterargument. It covers industrial automation and control systems — a distinct domain from aerospace (DO-178C) and automotive (ISO 26262), but with the same structural feature: a tiered safety/security level system that determines verification rigor and required evidence.

Critically, IEC 62443's security levels and foundational requirements are defined around *what an attacker can do*, not around a specific technology — which means the standard already separates verification objectives from implementation method, providing support for the argument that AI-generated artifacts can satisfy those objectives if the verification evidence is properly structured.

## Key Ideas

**Seven Foundational Requirements (FR1–FR7) per IEC 62443-1-1:**
- FR1: Identification and Authentication Control
- FR2: Use Control
- FR3: System Integrity
- FR4: Data Confidentiality
- FR5: Restricted Data Flow
- FR6: Timely Response to Events
- FR7: Resource Availability

**Security Levels (SL1–SL4) per IEC 62443-3-3:**
- SL1: Protection against casual/coincidental violations
- SL2: Protection against intentional violation using simple means
- SL3: Protection against intentional violation using sophisticated means
- SL4: Protection against nation-state level sophisticated attacks

**Verification evidence types under IEC 62443:**
- Security design specifications with control mappings to foundational requirements
- Threat analysis and risk assessment (TARA) documentation
- Security test plans and test results
- Architecture review records
- Configuration management and change control records

## Useful Claims

- IEC 62443, ISO 26262, and DO-178C all share the same structural pattern: tiered severity/security levels, defined verification objectives per level, and required evidence artifacts — not a specified implementation method.
- This structural commonality supports the whitepaper's core argument: what changes with a verification compiler is *who or what produces the evidence*, not the evidence structure itself.
- CISA and NIST have published free government documents that describe IEC 62443's framework in enough detail to cite without accessing the licensed standard.

## Requirements Impact

- The verification compiler's evidence schema should accommodate security-level–driven verification (IEC 62443 SL1–4) in addition to safety-level–driven verification (DO-178C DAL, ISO 26262 ASIL).
- The whitepaper can argue the evidence-structure approach generalizes across at least three major regulated domains: aerospace, automotive, and industrial/OT.
- CISA and NIST sources should be cited for any IEC 62443 evidence-requirement claims.

## Follow-Up Questions

- Has CISA or NIST published specific guidance on AI/ML use in ICS/OT systems under the IEC 62443 framework?
- Does IEC 62443-4-1 (secure product development lifecycle) have any publicly available interpretation that maps to software assurance objectives?
- How does the IEC 62443 zone/conduit model differ from DO-178C's system/software boundary concept, and does that difference matter for the verification compiler scope?
