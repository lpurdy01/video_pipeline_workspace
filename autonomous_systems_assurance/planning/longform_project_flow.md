# Long-form project flow: evidence before proposal

Status: composition and research plan, 2026-09-22. This document does not
promote the proposed narrative claims. It records the questions that research
must answer before the whitepaper and video can make them.

## The thesis to test

The opening must not say that safety methods for learned systems do not exist.
AMLAS, military assurance guidance, aviation rulemaking material, automotive
functional-safety practice, and runtime-assurance research are all important
counterexamples to that statement. The narrower, testable question is:

> What public, accepted evidence path would let a trained component receive a
> bounded safety-critical authority, and what still remains unresolved for the
> highest-consequence civil roles?

The FAA roadmap supplies the opening tension: a trained implementation breaks
the ordinary lower-level requirement-to-implementation explanation. The paper
then makes a constructive claim only where the evidence supports it: no one
metric, model inspection method, permit, standards document, or volume of road
data substitutes for the linked evidence needed for a particular hazardous
decision.

## Claims that require correction or evidence

| Tempting wording | Status | Safer working wording | Evidence still required |
|---|---|---|---|
| “There is no formal method for ML certification.” | Too broad | Public methods exist; their status, scope, and accepted use differ by jurisdiction and consequence. | Clause-level AMLAS, MAA, EASA and authority comparison. |
| “Cars have a lower safety bar.” | Ambiguous | US road-vehicle entry, operational permission, and product enforcement use different mechanisms from aircraft certification. This does not rank the intrinsic danger of road and flight. | Statute, FMVSS/self-certification, state deployment and aviation approval sources. |
| “Manufacturers self-certify autonomous systems as safe.” | Too broad | US manufacturers certify conformance to applicable FMVSS; that process, voluntary ADS disclosures, defect authority, and a learned-component assurance case are distinct objects. | NHTSA statutory/interpretive source and a scoped ADS source. |
| “Standards are delayed because qualified people have not circulated.” | Unfounded causal story | Standards and regulator guidance develop through evidence, rulemaking, consensus and implementation experience. The project can document process status, but cannot assign social causes without evidence. | Standards-body and regulator process records. |
| “A better ROC curve proves safety.” | False | A detection tradeoff is evidence about a specified task and data distribution. A safety case must connect it to hazards, exposure, time, control authority, recovery and change. | Statistical-evaluation, system-safety and runtime-assurance sources. |

## Reader journey

The whitepaper should move from a familiar failure to progressively denser
material. The video follows the same order but uses a single running encounter
and returns to its concrete question between abstract sections.

1. **A car is about to act on an incomplete world.** Introduce the hazardous
   decision and the fact that a learned component supplies part of the world
   model.
2. **Why conventional assurance has a missing link.** Explain designed
   requirements, learned weights, and the FAA framing without treating either
   conventional engineering or trained models as unknowable.
3. **What “safe enough” actually asks.** Separate harm, risk, reliability,
   performance, confidence and evidence. A graph has to preserve those
   distinctions instead of averaging them into a score.
4. **The legal and institutional landscape.** Explain the different objects:
   aircraft/component/installation/operation approval; road product
   self-certification, enforcement and operating permission; voluntary versus
   binding material; research versus a means of compliance.
5. **The current methods.** Compare AMLAS, MAA, EASA DS.AI and relevant road
   practice by objective and gap. Let their overlap and disagreement be seen.
6. **How statistical evidence enters a safety case.** Explain confusion
   matrices, thresholds, calibration, base rates, scenario selection and
   uncertainty using an accessible diagnostic example. Then show why none
   alone determines a safe action.
7. **The layered system.** Place the learned component inside sensors,
   preprocessing, world representation, planner, controller, monitor,
   recovery, compute and operating restrictions. Ask which shell can observe
   and constrain which failure.
8. **The monitor challenge.** A deterministic wrapper can limit action only
   under stated observations, timing and control authority. It cannot recover
   an object absent from every relevant observation path.
9. **The evidence bridge.** Introduce the project’s hazard-to-release
   contracts and show their links in an executable graph.
10. **Road worked case.** Apply every contract to the occluded-conflict
    encounter; leave missing evidence visibly open.
11. **Let the car take off.** Preserve the graph, replace the assumptions, and
    distinguish DAA equipment, installation, aircraft and operational claims.
12. **What inspection can and cannot buy.** Interpretability, verification,
    simplification and symbolic discovery may narrow a claim but do not erase
    coverage, integration and operational evidence.
13. **A practical release discipline.** Define the frozen release, change
    triggers, independent challenge, operational feedback and evidence expiry.
14. **The proposal and its limits.** Present the project architecture as a
    reusable assurance scaffold, not a standard, approval recipe or safety
    score.

## Evidence graph semantics

The expanded compiler must preserve distinct node types and edges:

```text
hazard ──exposure/conditional-risk──> harmful outcome
  │                                      ▲
  ├──operating-domain constraint──> release authority
  ├──scenario/evaluation evidence──> performance observation
  ├──assumption──> monitor/recovery claim
  ├──change trigger──> release invalidation
  └──argument/standard objective──> required evidence

performance observation ≠ reliability estimate ≠ risk estimate ≠ safety claim
```

An accuracy, sensitivity or false-alarm number is an observation whose meaning
depends on the dataset, threshold and target condition. A reliability estimate
also requires time/exposure and uncertainty treatment. A risk claim must add
harm severity and operational exposure. A safety conclusion must show that the
specified residual risk is acceptable under a defined authority and recovery
strategy. The compiler should represent those links and their open assumptions;
it must not compute a single “certainty” or “safety” score.

## Long-form production targets

| Output | Target | Gate before lock |
|---|---|---|
| Whitepaper | 50–65 reader pages, approximately 14,000–18,000 words plus appendices | Claim/source context and cross-artifact review refreshed after the section structure is stable. |
| Video | 30–38 minutes, approximately 4,300–5,500 spoken words | Script uses the paper’s reviewed claims and each visual has a scope/claim review. |
| Diagrams | 12–16 original explanatory figures plus cited-source visual references only when rights and meaning are verified | Caption, proposal/source label, claim links, visual limitation and rendered-frame review. |
| Resource package | Browseable source cards, source locations, claim graph, manuscript, video script, diagram sources and review records | Native source/rights status and release inventory are explicit. |

## Immediate work sequence

1. Integrate the standards-authority and risk-evidence contribution handoffs
   without flattening their scope distinctions.
2. Extend the method crosswalk with objective-level agreements, divergence and
   status labels; do not infer agreement merely from similar names.
3. Add explicit performance-observation, risk-assumption and action-authority
   graph nodes to the compiler after validating a minimal schema and tests.
4. Write Sections 3–8 from the integrated source baseline and add the
   corresponding diagrams.
5. Build the 30-minute narration from the reviewed whitepaper, then run
   source-support, challenge and cross-artifact review on its new packages.
