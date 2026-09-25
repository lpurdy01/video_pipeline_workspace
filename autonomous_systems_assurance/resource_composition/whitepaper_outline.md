# Long-form whitepaper outline

Working title: **What Would It Take to Trust an Autonomous System?**

This is a 50–65 page target structure. It starts with an accessible physical
failure, introduces the institutional and statistical context needed to read
the proposal correctly, then becomes progressively more technical. It does not
claim that no learned-system methods exist or that any existing document has
certified the hypothetical road or airborne release.

| Section | Reader's question | Evidence / case | Planned visual |
|---|---|---|---|
| 1. The missing object | What happens when a vehicle acts on an incomplete world model? | Paired observable/unobservable worlds and monitor premise [C-EVID-005] | Same planner input, two physical worlds |
| 2. The missing link | Why does learned implementation strain ordinary traceability? | FAA learned-implementation framing [C-AUTH-010] | Designed chain → learned release → evidence bridge |
| 3. What “safe enough” means | Are accuracy, reliability, residual risk and safety the same thing? | Conventional severity/likelihood context; learned performance limits [C-RISK-001] [C-RISK-004] [C-RISK-005] | Separate branches meet at a hazard claim; no composite score |
| 4. Approval is not one thing | What differs between product compliance, operational permission and assurance evidence? | US FMVSS certification boundary; aviation approval-object distinctions [C-STD-003] [C-STD-004] [C-INTAKE-003] | Three parallel permission/evidence tracks |
| 5. The public methods landscape | What exists today, and what remains proposed, voluntary, military or scoped? | AMLAS, FAA roadmap, MAA, EASA DS.AI, ISO/PAS, UL and SAE public scope [C-CHAL-001] [C-CHAL-003] [C-CHAL-006] [C-STD-001] [C-STD-002] [C-STD-005] | Status ladder and objective crosswalk |
| 6. Risk evidence is conditional | What can test data, simulation, coverage and calibration establish? | Scenario/rare-event/calibration limits; DAA metric limits [C-EVID-002]–[C-EVID-004] [C-RISK-004] | Threshold curve → confusion matrix → encounter ledger |
| 7. The system around the model | Which conventional and deterministic layers bound a learned component, and where can they fail? | Runtime-assurance premises and shared-blind-spot test [C-EVID-005] | Nested assurance shells and broken-monitor variant |
| 8. The evidence bridge | What objects must be linked to grant a release bounded authority? | Eight project contracts, AMLAS crosswalk and release graph [C-CHAL-006] [C-EVID-001] | Hazard → release → scenario evidence → recovery/change graph |
| 9. Road worked case | What evidence would the occluded-road release actually need? | `REL-ROAD-001`, `H-ROAD-001`, obligations and risk context | Contract-by-contract open evidence ledger |
| 10. Let the car take off | Which assumptions survive, and which change, for airborne DAA? | `REL-AIR-001`, approval distinctions and DAA metric context [C-RISK-004] | Same graph, changed sensing/margin/authority nodes |
| 11. Inspection and simplification | Can verification, interpretability or a smaller model close part of the argument? | Bounded method evidence [C-EVID-006] [C-EVID-007] | Claim-limited tool cards, not an explainability switch |
| 12. Release discipline | What must reopen evidence after a data, model, sensor, monitor or ODD change? | Frozen-release distinction and method lifecycle records [C-AUTH-002] [C-CHAL-003] | Change-impact graph and re-review path |
| 13. Proposed practical architecture | What does this project add after the existing methods are respected? | Project evidence contracts and executable compiler | Inspectable case file, explicit blockers and reviewers |
| 14. What remains unresolved | What would have to happen before this becomes a publishable/operational claim? | Authority status, source limitations and open case blockers [C-STD-002] | Open-obligation board |
| Appendices | Can the reader inspect every important statement? | Claim register, source regions, method crosswalk, risk-context schema, review ledger | Hyperlinked evidence and release manifest |

## Coverage and language gates

- A document's **status** is always shown: statute, binding rule, authority
  guidance, proposed guidance, consensus standard, information report,
  research method, product statement or operating permission.
- “Self-certification” is used only for the applicable FMVSS compliance
  mechanism; it is never shorthand for a universal learned-model safety claim.
  [C-STD-003] [C-STD-004]
- The paper will not assign unfinished standards work to a shortage of skilled
  people or mathematical rigor without direct evidence. That causal explanation
  is currently unsupported.
- ROC curves, confusion matrices and aggregate DAA risk ratios are teaching
  patterns. They keep their population, threshold, scenario, error-cost and
  recovery limits visible. [C-RISK-004] [C-RISK-005]
- The paper's frozen-release architecture is a project proposal. It is not a
  standard, means of compliance, approval basis, or safety score.

The initial reader-review draft covers a shorter version of these sections. New
prose will be added only after the source and cross-artifact review baseline is
refreshed for this structure.
