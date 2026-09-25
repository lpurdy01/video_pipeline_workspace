# Independent assurance-gap challenge — search log

Search date: 2026-09-16 (America/Phoenix).  The question was deliberately adversarial: **does public, authoritative or standards-backed material already provide one inspectable end-to-end assurance/certification lifecycle for high-criticality, frozen learned components?**

This is a dated search record, not a proof that material outside the inspected set does not exist.

| Query / path | Result | Disposition |
| --- | --- | --- |
| `site:easa.europa.eu artificial intelligence certification machine learning approval published assurance paper pdf` | Located EASA NPA 2025-07(B), a detailed proposed DS.AI framework. | Retained as `S-CHAL-002`. It materially weakens any claim that there are no defined lifecycle proposals, but it is proposed and has explicit high-criticality exclusions. |
| `site:faa.gov AI machine learning certification special conditions learned assurance 2025 2026` | No final FAA source establishing a public end-to-end approval lifecycle for a high-criticality learned component was located in returned results. The existing FAA roadmap remains relevant background but was not duplicated in this lane. | Negative result only; does not establish that no FAA project-specific agreement or non-public material exists. |
| `EUROCAE SAE artificial intelligence aviation certification assurance standard published 2025` | Located EUROCAE WG-114. Its current work-program table lists ED-324 as Draft, targeted for 31 December 2026. | Retained as `S-CHAL-003`; defeated the tentative assumption that ED-324 is already a published baseline. |
| `site:gov.uk military aviation authority artificial intelligence machine learning assurance safety certification` | Located MAA/RN/2025/04. It is current authority guidance for UK military aviation and requires case-specific MCRI agreement for certified systems. | Retained as `S-CHAL-001`; it is the strongest located current authority assurance path, but it is military and non-prescriptive. |
| `Assuring the safety of machine learning for autonomous systems AMLAS methodology full pdf University of York` | Located the full public AMLAS v1.1 guide and its six-stage methodology. | Retained as `S-CHAL-004`; it directly defeats any novelty claim for a generic trained-ML lifecycle but is research guidance limited to the ML component. |
| EASA NPA explanatory-note search: `site:easa.europa.eu "NPA 2025-07" "Decision" AI trustworthiness 2026` | Located the explanatory note saying EASA *may* issue a decision following consultation. No final decision was located in the returned material. | Do not infer that a final decision does not exist. Refresh EASA's NPA and Decision libraries immediately before publication. |

## Explicitly unresolved / inaccessible evidence

- No public, completed MCRI/airworthiness package was located for a high-criticality frozen learned component. The absence is only from this search scope; military and commercial certification evidence may be restricted.
- No public final EASA decision adopting NPA 2025-07(B) was located. A browser result is not a complete Decision-library audit.
- ED-324/SAE ARP6983 full text was neither accessible nor inspected. The publisher's current status page says draft; it is not appropriate to infer obligations from the proposed EASA reference.
- No public FAA/EASA type certificate, STC, operational approval or DAA approval record was found here that makes an inspectable learned-model safety case available. This lane did not repeat the separate FAA/DAA retrieval work.
