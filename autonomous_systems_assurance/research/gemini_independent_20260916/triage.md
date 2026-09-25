# Gemini grounded discovery: integrator triage

Run date: 2026-09-16. The raw prompt, response and grounding metadata are retained under ignored `out/`. Gemini supplied leads only; none of its statements are project evidence until the original source is independently retrieved, hashed and inspected.

| Gemini lead | Triage | Reason |
|---|---|---|
| AMLAS | Captured independently as `S-CHAL-004` / `C-CHAL-006` | The challenge lane retrieved the University of York Version 1.1 document and recorded its scope limits. Gemini's arXiv link and licence assertion are not used. |
| ASTM F3269-17 runtime-assurance practice | Retrieval candidate | The Gemini statement about withdrawal and scope needs ASTM-source verification; it may be valuable for the aviation monitor/recovery comparison. |
| SaFAD consortium paper | Retrieval candidate | Potential road-safety-case baseline and visual reference. It is industry material, not authority evidence. |
| Mobileye RSS paper | Retrieval candidate | Potential formal authority-allocation comparison. Its perception and actor assumptions must be kept explicit. |
| VNN-COMP 2024 | Retrieval candidate | Potential evidence about what neural-network verification benchmarks actually establish and their scalability limits. |
| Waymo safety reports | Existing company family; refresh candidate | Useful only as a dated vendor safety-case disclosure; it cannot establish external approval or be generalized to a different stack. |
| BSI PAS 1881 and ISO/TR 4804 | Access/status candidates | Full-text availability, edition status and road-only scope require lawful primary-source inspection. |

Gemini also proposed diagrams and other visual material. No external visual is approved for reuse. Any future use requires direct asset provenance, a visible-claim review, and a licence or permission check; an attractive lifecycle diagram is not evidence by itself.

