# Handoff: 2026-09-15-assurance-authority-map / v1

- Author/session and role: `/root/assurance_authority`; authority/standards researcher
- Date/time with timezone: 2026-09-16 America/Phoenix
- Job card: [authority-map task](../../../tasks/2026-09-15-assurance-authority-map.md)
- Input baseline and hashes: Git `ab5bf71abcab3d873c541679199d89c3b300223b`; prior compiler report: 71 sources, 71 claims, 389 blockers, structural pass. Read the required project and coordination files before research.
- Output file paths and SHA-256 values: `sources.json` `729e02351a09ceb529e37c5dded5cf7b5f46a9ea2caeadc69b48631ee25e5363`; `claims.json` `b6208ff29c6bf2289bc01c0803f6fd836754a3a7a355c3da6d2d85ac27762fef`; `findings.md` `dc94dfb06e54bf508f9b5fb718a0adfb5a8ff27019e2f66a4ce02cf487be6986`. The handoff hash changes with this update.
- Completion state and blocked deliverables: complete. Full FAA/EASA PDFs were inspected from existing ignored retrieval storage. Licensed ISO/PAS 8800 and UL 4600 full texts remain unavailable.
- Writes paused for integration: yes

## Findings and proposed changes

Changed only assigned paths:

- `research/contributions/assurance_authority/sources.json`: `S-AUTH-001` through `S-AUTH-007`.
- `research/contributions/assurance_authority/claims.json`: `C-AUTH-001` through `C-AUTH-009`.
- `research/contributions/assurance_authority/findings.md`: status matrix, direct findings and counterevidence.

FAA, EASA, ISO and UL show that public assurance methods and candidate structures exist; no source in this pass supports a universal, final, public recipe for flight-critical frozen learned behavior. FAA Version I's industry-method-gap statement is dated and must not be elevated into a current worldwide-absence claim. [C-AUTH-001] [C-AUTH-004] [C-AUTH-005] [C-AUTH-006] [C-AUTH-007]

NHTSA's public VSSA route is voluntary and not federal approval. Its July 2026 announcement covers planned standards/guidance and a limited exemption, not a disclosed learned-model assurance case. [C-AUTH-008] [C-AUTH-009]

Existing `S-METHOD2-*` and `S-AIR2-*` entries overlap some issuer families. Retain the new full-PDF inspection provenance for FAA/EASA where useful, map or retire duplicates deliberately, and do not count duplicate document families as independent corroboration.

## Search and inspection record

Search date: 2026-09-16. Queries covered FAA AI roadmap learned static-version assurance; EASA Issue 2 and Proposed Issue 3; ISO/PAS 8800 trained model status; UL 4600 current status; NHTSA ADS guidance, VSSA and AV standards.

| Source | Status/jurisdiction | Inspection result |
|---|---|---|
| FAA Roadmap Version I | Regulator roadmap, US civil aviation, 2024 | Complete local PDF inspected; SHA-256 in source regions |
| EASA Issue 02 | Concept guidance, EASA civil aviation, 2024 | Complete local PDF inspected; SHA-256 in source regions |
| EASA Proposed Issue 03 | Proposed concept guidance, EASA civil aviation, 2026 | Complete local PDF inspected; SHA-256 in source regions |
| ISO/PAS 8800 | Published PAS, road vehicles, 2024 | Official product-page abstract/status; licensed text unavailable |
| ANSI/UL 4600 Edition 3 | Active ANSI consensus standard, 2023 | Official public scope/status; licensed text and proposal text unavailable |
| NHTSA ADS page | Voluntary US federal guidance | Official current page inspected |
| NHTSA July 2026 AV announcement | US federal policy announcement | Official full announcement inspected |

Deliberate contrary search found ISO/PAS 8800, UL 4600 and EASA material, disproving any claim of a complete assurance vacuum. No public FAA high-criticality learned-model certification basis, final RMT.0742 output, or publicly inspectable complete assurance package was found in this bounded pass; this is not an absence finding.

## Review provenance

No formal source-support, challenge, cross-artifact or human-disposition record was created. This handoff is research provenance only and does not satisfy compiler review gates. Assign independent challenge research on post-2024 FAA developments, final EASA RMT.0742 outputs and actual public certification bases.

## Verification

`python3 -m json.tool` parsed both contribution registries. A shared-workspace diagnostic `python3 autonomous_systems_assurance/verification/compile.py` returned structural pass: 89 sources, 94 claims, 561 blockers, 376 planned reviews, zero review records. Other workers may have written their exclusive inputs during that run, so the counts are diagnostic rather than an integration baseline. Release blockers remain expected for short-excerpt evidence and absent reviews.

## Impact and next action

The paper should use a status-labelled evidence matrix and a proposed assurance-case composition. The video can use road deployment as an opener only if it immediately separates operating scope from trained-model evidence. The road-to-air scene should distinguish state/federal road operations from aviation equipment, installation, aircraft and operational approvals.

Integrator next action: reconcile contribution overlap, preserve the NHTSA 2026-versus-ADS-2.0 status tension, compile against a frozen input set, then assign an independent challenge before accepting authority conclusions for publication.
