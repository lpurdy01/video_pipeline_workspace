# Round 4 integration: standards status and risk evidence

**Integrated:** 2026-09-22  
**Inputs:** risk_evidence and standards_authority lane handoffs.  
**Question:** How should a long-form assurance paper describe the public
methods landscape, regulatory roles, probability and evidence tradeoffs without
claiming that a trained model has a generic safety score?

## Integrated finding

The project should not begin from a claim that no formal methods exist. AMLAS
is a public ML-component methodology; FAA material describes active method
development; EASA has detailed but proposed DS.AI material; and road practice
has standards/guidance with varied legal force. The strongest scoped statement
is that the inspected public record is **unfinished and fragmented** for the
hardest hypothetical civil learned-component role. It does not show one final,
publicly inspectable lifecycle that both closes the road-to-air worked-case
obligations and carries a final approval status. [C-CHAL-006] [C-STD-001]
[C-STD-002]

This does not establish that no applicant has confidential evidence, that an
authority cannot decide a project-specific case, or that every jurisdiction
uses the same approval mechanism. It is a dated research finding whose source
status remains reviewable.

## Authority and standards distinctions

| Topic | Integrated conclusion | Evidence boundary |
|---|---|---|
| FAA activity | FAA's technical-discipline page describes collaboration with industry, government, standards-development organisations and academia in the certification context. [C-STD-001] | Activity is not a completed standard, approved means of compliance or approval outcome. |
| EASA DS.AI | The captured RMT.0742 status page labels DS.AI NPA 2025-07(B) proposed and awaiting responses. [C-STD-002] | Recheck before publication; a status page can be superseded by a later decision, CRD or AMC/GM. |
| U.S. vehicle self-certification | The statutory object is compliance with applicable FMVSS, subject to reasonable care. [C-STD-003] | It is not blanket certification that a trained model is safe in all scenarios. |
| NHTSA oversight boundary | NHTSA states it does not pre-approve ADS technologies and describes FMVSS self-certification and defect authority. [C-STD-004] | Nonbinding interpretation with short captured context; do not use release-grade until a full retained snapshot is obtained. |
| SAE J3321 | The public page describes a 2026 AI/ML V&V information report with no mandatory requirements. [C-STD-005] | Public scope only, not licensed clause text, regulator recognition or a complete safety case. |

No source found in these lanes supports the claim that methods remain unfinished
because the field lacks enough qualified people, consensus participants or
mathematical rigor. Those are plausible narratives, not accepted project facts.

## Risk and probability distinctions

Conventional transport-airplane guidance supplies a useful shape for the
question: increasing failure severity calls for decreasing acceptable
likelihood, assessed with analysis, testing and—where justified—quantitative
reasoning. It is historical guidance, not a learned-model acceptance method.
[C-RISK-001]

The FAA roadmap presents DAL assignment via system safety assessment as a
starting point for scaling rigor, but says existing software/complex-hardware
guidance is inadequate for learned implementations. [C-RISK-002] EASA's
proposed DS.AI material has its own authority and severity/likelihood structure
and stated high-consequence/online-learning boundaries. [C-RISK-003] Neither
source licenses a video claim that a particular DAL maps to an allowed trained
flight-critical role.

The project graph must preserve five separate things:

1. the hazardous outcome and its severity;
2. operational exposure and scenario distribution;
3. observed error, latency, calibration and threshold tradeoffs;
4. monitor/controller/recovery response; and
5. the bounded residual-risk and authority judgment.

The UK CAA warns that aggregate DAA risk ratios can hide deficiencies in
individual encounter cases. [C-RISK-004] AMLAS's clinical ROC and confusion
matrix example shows why a threshold has contextual, potentially unequal error
costs. [C-RISK-005] These are direct reasons to reject a composite certainty,
reliability or safety score in both the paper and the compiler.

## Source-quality and conflict ledger

| Item | Integration action |
|---|---|
| FAA roadmap / EASA NPA / AMLAS duplicates | Retained as duplicate provenance in the new lanes, but recorded as the same independence family as prior project sources. They do not count as independent corroboration. |
| FAA AC 25.1309-1A | Added only as historical conventional system-safety context. It must not be converted into a learned-perception numerical requirement. |
| CAP3127 | Added as UK consultation/test-phase DAA metric material; not a DAA approval or universal AI criterion. |
| NHTSA interpretation | Browser-inspected and linkable but source context remains short until full lawful capture succeeds. |
| SAE J3321 scope page | Browser-inspected and linkable but source context remains short until full lawful capture succeeds. |
| EV versus ICE crash rates | No exposure-normalized primary comparison was accepted. Do not use this as a paper/video fact; powertrain is not a proxy for autonomy. |

## Composition consequences

1. Add a plain-language standards/status ladder before comparing methods.
2. Explain FMVSS self-certification as one legal track, separate from operating
   permission and learned-component assurance evidence.
3. Use the supplied AMLAS medical figure only to teach threshold and
   confusion-matrix tradeoffs, with its clinical scope visible.
4. Add risk-context nodes to the worked-case graph and attach scenario,
   recovery and metric-limit statements to them.
5. Keep all statements about particular products, private models, EV accident
   rates and reasons for standards maturity outside factual narration unless
   later source work supports them.
