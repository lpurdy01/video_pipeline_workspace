# Figure plan and assertion review

The first two figures are rendered SVG assets for the reader-review prototype. They are explanatory project graphics, not copied authority diagrams or measurements from a real autonomy stack.

| ID | Figure | Status | Claim links | Visual limit |
|---|---|---|---|---|
| F-001 | [Designed traceability to learned evidence bridge](figures/learned_traceability_gap.svg) | rendered | [C-AUTH-010] | The FAA describes the lower-level learned-algorithm traceability problem; the green evidence bridge is the project’s proposed response. Do not read it as an FAA workflow or a claim that all conventional traceability fails. |
| F-002 | [Six-question evidence bridge](figures/evidence_bridge_ladder.svg) | rendered | project proposal | This is a skimmable grouping of project contracts, not a safety score or a sufficient acceptance checklist. |
| F-003 | Two worlds, same missed-object representation | planned | project case | Do not imply every monitor shares the same input; the graphic must show this as a falsification test. |
| F-004 | Controller, monitor, fallback, and shrinking recovery margin | planned | [C-EVID-005] | Do not treat a threshold without monitor, timing, dynamics, and recovery assumptions as a guarantee. |
| F-005 | Evidence obligations around the road-to-air architecture | planned | [C-CHAL-006] [C-EVID-001] | Green boxes must mean required evidence, not completed evidence. |
| F-006 | Road vehicle takes off: changed assumptions | planned | [C-CHAL-001] [C-CHAL-003] [C-CHAL-004] | Do not imply aviation is categorically impossible, uniformly harder, or approved by a road result. |
| F-007 | Inspection, intervention, compression, and equation discovery | planned | [C-EVID-006] [C-EVID-007] | Do not imply an interpretable feature or small model establishes safety. |
| F-008 | [Assurance shells around a learned component](figures/assurance_shells.svg) | rendered | project proposal; [C-EVID-005] | The shells assign evidence boundaries, not certification status. A deterministic action wrapper is conditional on observation, timing and control authority; it may share a perception blind spot. |
| F-009 | [Conditional risk evidence graph](figures/conditional_risk_graph.svg) | rendered | project proposal; [C-RISK-001] [C-RISK-004] [C-RISK-005] | Performance, uncertainty, exposure, recovery and a residual-risk judgment remain distinct. The graphic is not a formula, an acceptable-risk threshold, or a safety score. |
| F-010 | [Public-assurance coverage map](figures/assurance_coverage_map.png) ([editable SVG](figures/assurance_coverage_map.svg)) | rendered | [C-RISK-006] [C-RISK-007] [C-CHAL-001] [C-CHAL-006] [C-AUTH-010] [C-RISK-002] [C-DIR-003] | A source-scoped map of what the documents address and leave open. EASA's material is proposed, Level 3B is reserved, and its risk cells are not a universal approval rule, a road-automation taxonomy, or a product assessment. |

| F-011 | [Shared vision cue and training evidence](figures/vision_training_contract.svg) | rendered | [C-TRAIN-001] [C-TRAIN-002] [C-TRAIN-003] [C-TRAIN-004]; project interface | Road and air share a cue shape, not model weights, data adequacy or approval. Training boxes are obligations; a physically unobservable object cannot be inferred by a stronger model alone. |

Every rendered asset should eventually record its content hash, caption revision, source/proposal label, and scene ID in the compiler graph. A figure review must ask whether the visual preserves the same scope and limitations as its linked prose.
