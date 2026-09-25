# Architecture vocabulary

Working explanatory distinctions; clause-level definitions must be tied to the relevant standard before publication.

| Distinction | Why it matters in this project |
|---|---|
| Safety requirement / evidence / authorization | Desired behavior, reasons to believe it, and an authority's permission are separate objects |
| Perception / prediction / planning / control | An accurate actuator controller cannot repair an unseen aircraft by itself |
| Learned / learning during operation | Training before deployment and changing behavior during a mission need different change arguments [C-007] |
| Random training / deterministic inference / uncertain environment | Uncertainty in behavior is not synonymous with random execution |
| Model confidence / empirical error / system risk | A confident prediction is not a calibrated estimate of collision probability |
| ODD / scenario coverage / monitoring | Defining an allowed domain does not prove the system recognizes when it leaves it |
| Requirement-to-code / learning assurance | The evidence path may need training data, labels, learning objectives and learned model artifacts, alongside implementation evidence |
| TSO / installation / aircraft / operational approval | Keep the object and scope of each decision visible [C-002] |
| World-model visualization / mechanistic interpretation | Seeing predicted objects is different from identifying the computations that caused them [C-010] [C-012] |
| Pruning / distillation / symbolic identification | A smaller network, imitation model and discovered equation are different artifacts [C-011] |
| Runtime monitor / recovery guarantee | Detecting a violation only helps when action is still possible under the stated assumptions [C-009] |

Related: [open tensions](open_tensions.md), [source register](../../research/sources.json), [claims](../../verification/claims.json).
