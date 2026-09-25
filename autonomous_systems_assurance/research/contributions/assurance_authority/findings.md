# Authority and standards map: frozen trained systems

Research date: 2026-09-16. Owner: `assurance_authority`; identifiers `S-AUTH-*` and `C-AUTH-*`. These records are provisional research inputs, not accepted publication claims.

## Matrix

| Family | Current public status inspected | What it provides for a frozen trained model | What it does not establish |
|---|---|---|---|
| FAA AI roadmap | FAA Version I roadmap, 2024; explicitly living direction-setting material | A direct distinction between static learned AI and systems that learn in operation; an update should receive renewed safety assurance | A binding means of compliance, an approved evidence threshold, or a public end-to-end approval for a flight-critical learned model |
| EASA Issue 02 | Published concept paper for Level 1/2 ML, 2024 | Usable candidate objectives spanning AI assurance, explainability and risk mitigation | Definitive detailed guidance, AMC/GM, or a warranty of final approval |
| EASA Proposed Issue 03 | Proposed concept paper, dated 2026-06-03 | Candidate objectives and anticipated MOC across broader safety-related AI and advanced automation | A complete or binding MOC set, final rulemaking, or an approval decision |
| ISO/PAS 8800 | Published Publicly Available Specification, Edition 1, 2024 | A road-vehicle safety-assurance vocabulary that explicitly includes a trained AI model | Aviation applicability, a public conformity result, or clause-level evidence without licensed-text inspection |
| ANSI/UL 4600 | Active Edition 3, ANSI approved 2023; public August 2026 proposal also listed | Goal-based safety-argument structure for autonomous products and an explicit whole-item scope | A government operating authorization, sufficient evidence for every ODD, or a particular product's evaluation result |
| NHTSA ADS 2.0 / 2026 activity | Public page calls ADS 2.0 current voluntary operating guidance; July 2026 announcement says new guidance and first AV performance standards are being developed | Road evidence categories such as ODD, OEDR, fallback and validation; a live view of a federal transition | Federal model approval via VSSA, a final new performance standard, or access to proprietary evidence behind an exemption |

## Direct findings

The requested distinction between **trained systems** and systems that learn while operating has direct regulatory support. FAA calls the former static in the operating environment and says each released update is subjected to safety assurance. That validates the project's first object of study: a frozen, versioned model tied to a controlled data/model/configuration release. It does not yet give the project a complete FAA acceptance checklist. [C-AUTH-002]

There is enough public material to reject the claim that there are no processes at all. ISO/PAS 8800 and UL 4600 describe road-vehicle safety-assurance and safety-case structures, and EASA gives candidates for learning assurance and associated risk mitigation. Their statuses, jurisdictions and evidence limits materially differ. The project should call this a **portfolio of partial or scoped assurance methods**, not a single universal process. [C-AUTH-004] [C-AUTH-005] [C-AUTH-006] [C-AUTH-007]

The most direct aviation gap statement is dated. FAA's 2024 roadmap says the industry lacks a method for safety assurance of AI, but also says the roadmap is living and points to evolving standards and project-specific issue papers. The defensible publication claim is therefore: *within the stated public search scope, we did not find a universally applicable, publicly inspectable end-to-end acceptance recipe for a high-criticality frozen learned component.* The project must not say that no method exists. [C-AUTH-001] [C-AUTH-003]

Road operation is not evidence that an undisclosed trained model passed a public safety certification. NHTSA's older public ADS guidance makes its VSSA process voluntary and not subject to federal approval. A July 2026 NHTSA announcement says federal AV performance standards and new guidance are being developed, and describes a temporary exemption mechanism. This provides a deliberately contrary interpretation of the “cars are already approved” premise: operating, exemption, state-permit, FMVSS and learned-model evidence belong on distinct graph edges. [C-AUTH-008] [C-AUTH-009]

## Contrary evidence and unresolved questions

1. **Against a pure-gap narrative:** ISO/PAS 8800 is published and specifically names trained models; UL 4600 is active and defines a safety-argument framework. Any script claiming conventional process has no learned-system counterpart would be misleading.
2. **Against “standards solve it”:** UL's public scope calls its requirements possibly not sufficient, EASA explicitly describes its documents as incomplete/non-binding, and FAA identifies method development as ongoing. These materials do not yield a universal numerical pass score or a reusable safety certificate.
3. **Against “road deployment proves the model is approved”:** NHTSA's public VSSA material says the process is not federal approval. The July 2026 limited-exemption announcement does not disclose the underlying model evidence or become general authorization.
4. **Current-status tension:** NHTSA's page still calls ADS 2.0 current operating guidance, while its July 2026 announcement says updated guidance is being developed. Verify whether a new guidance document or performance standard has actually been released before publication.
5. **Search limitation:** No public FAA certification basis, issue paper, or article/installation approval was found here that defines a complete high-criticality learned-model acceptance package. That is a failed-to-find result, not evidence of nonexistence.

## Compiler implication

The evidence graph should distinguish `authority_status` (binding rule, approved authorization, issued consensus standard, voluntary guidance, proposed guidance, research) from `evidence_role` (hazard evidence, model-release evidence, scenario evidence, recovery evidence, operational permission). A standard or permit can support one node without closing the others. The compiler should reject a claim that an operating permission alone establishes model safety.
