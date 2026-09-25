# AIR round 2 research contribution

As of 2026-09-08. Provisional research for integration; all claims require independent challenge and human disposition. Ownership: `air_round2`, IDs `S-AIR2-*` / `C-AIR2-*`.

## Findings

GA-ASI's public material is useful for the system architecture and the history of DAA standardization, but it is not an authority record for a current TSO authorization. The page describes a layered system: TCAS and ADS-B for cooperative aircraft, Due Regard Radar/ATAR for non-cooperative aircraft, and a processor/display path for the remote pilot. Its current product pages still use “on track to obtain” / “striving to obtain” language for TSO-C211/C212, while a feature list uses “FAA TSO authorization.” That internal marketing ambiguity should be preserved as a status question. The FAA/GA-ASI 2022 report independently documents prototype flight testing and comparison of ATAR, ADS-B and active-surveillance measurements with sensor models. It does not certify the complete system, aircraft installation or operation. [C-AIR2-001] [C-AIR2-002] [C-AIR2-003]

The key certification lesson is structural. FAA's own TSO explanation says a TSOA is a design/production approval for an article meeting a minimum performance standard and explicitly says installation and use require separate approval. FAA Order 8100.18A lists TSO-C211 and TSO-C212. The currently retrievable C212a draft shows how the boundary is expressed: the radar supports detection/tracking of non-cooperative traffic, software may invoke DO-178C, hardware may invoke DO-254, and the article's installation requires separate approval. The C211a draft has a placeholder effective date and should be treated as draft material. [C-AIR2-004] [C-AIR2-005] [C-AIR2-006]

FAA's 2024 AI roadmap is a strong primary source for the paper's assurance architecture. It distinguishes “learned AI” (static after offline training; each updated version is subject to assurance) from “learning AI” (changes in operation; the assurance strategy must address the learning process). It calls out runtime assurance, formal/numerical methods, system-level testing, explainability and black-box validation as research or method-development areas. The roadmap is a direction-setting document, not a blanket route to certify a flight-critical learned controller. [C-AIR2-007] [C-AIR2-008]

EASA is moving in a parallel direction but the source status matters. Issue 2's landing page summarizes learning assurance, explainability and Level 2 human-AI teaming; the PDF was not retrievable in this pass. Proposed Issue 3 is listed on EASA's site dated June 3, 2026, but only its title/date/download metadata were inspected. These are leads for a later capture pass, not detailed technical evidence. [C-AIR2-009] [C-AIR2-010]

The UK CAA's CAP3127 response is especially useful for DAA metrics and assurance scope. It reports a test phase for the DAA policy concept and discusses reliability, integrity, availability, performance, encounter-set representativeness, equipment reliance, human factors and NMAC/DWC metrics. The CAA notes that NMAC is a proxy for mid-air collision and that averaged risk-ratio metrics can hide deficiencies in particular encounters; this directly supports a compiler design that preserves scenario-level evidence and does not collapse it to one confidence score. [C-AIR2-011]

Zipline demonstrates the equipment/operation distinction. FAA announced a scoped 2023 authorization for Salt Lake City commercial package delivery BVLOS without visual observers, and the BEYOND page says a February 2023 change submission enabled DAA software within the mode-C veil. Neither page is a TSO article approval, unrestricted operational permission, or proof that the same architecture is approved elsewhere. The linked approval letters returned HTTP 403 during inspection and remain a required retrieval task. [C-AIR2-012] [C-AIR2-013]

Protector is a useful military/civil comparison, but current claims must be carefully bounded. The UK MOD describes intended NATO/UK certification and prospective access to UK/European civilian airspace. The announcement is not the Military Type Certificate, installation approval or civil operating permission. It cannot support “only certified DAA system” language. [C-AIR2-014]

## Proposed use in the worked case

The car-to-flight transition should carry the same graph nodes—operating domain, sensor coverage, learned perception, decision authority, fallback, evidence and change control—but replace the approval and hazard nodes explicitly. For flight, the graph should separate (1) equipment TSO/MPS, (2) aircraft installation/type or supplemental approval, (3) operator/airspace authorization and conditions, and (4) continued operational safety/change management. Learned perception or planning evidence cannot be inferred from a TSO title, and a DAA operational authorization cannot be silently promoted to unrestricted civil flight.

## Inspection limits and next retrieval tasks

- No article-specific FAA DRS TSO authorization record for GA-ASI was located; this is a failed/unfinished search, not evidence of absence.
- Regulations.gov links for Zipline's 2023 approval letters returned 403. Obtain the underlying downloads from docket FAA-2020-0499 and inspect conditions/limitations.
- EASA Issue 2 and Proposed Issue 3 PDFs were listed but direct downloads were rate-limited (HTTP 429); capture permitted copies and inspect their full context.
- The Protector MTC and UK MAA aircraft/operational scope were not inspected.
- No RTCA DO-365/366 or SAE/EUROCAE standard text was downloaded; the project must respect license restrictions.
- All region records deliberately have `snapshot_path: null`, `snapshot_sha256: null`, and `context_status: short_excerpt_only`; the compiler should therefore report context blockers.
