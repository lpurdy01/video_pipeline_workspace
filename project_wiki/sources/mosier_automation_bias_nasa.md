# Mosier & Skitka — Automation Bias and Countermeasures (NASA, 1996–1997)

## Provenance

raw_file: refrence_literature/raw/extracted_markdown/mosier_automation_bias_nasa.txt
raw_url: https://ntrs.nasa.gov/citations/20020043049
summary_method: llm-from-url
summary_verified: true

## Source

Two companion papers from the same NASA Ames research group:

1. Mosier, K. L., Skitka, L. J., Dunbar, M., McDonnell, L., & Rosekind, M. (1997). "Automation Bias and Countermeasures in Flight Crews." NASA NTRS 20020043049.

2. Mosier, K. L., Skitka, L. J., Burdick, M. R., Heers, S. T., & Rosekind, M. R. (1996). "Decision Making In A High-Tech World: Automation Bias and Countermeasures." Society for Judgment and Decision Making Conference. NASA NTRS 20020041010.

Both are publicly available on NASA NTRS (Public Use Permitted).

## Why It Matters

Provides peer-reviewed, aerospace-domain empirical support for the automation bias mitigation requirements in the Verification Compiler (REQ-6.1). Human reviewers operating in supervisory control settings — checking evidence packages that include LLM verdicts — are exactly the high-stakes decision-making context studied here.

The two specific countermeasures studied map directly to the VC's design requirements:
- **Accountability effect** → canary queries (reviewer knows they must independently verify, not ratify)
- **Display prompts for verification behavior** → evidence-first presentation (LLM verdict withheld until human assessment submitted)

## Key Ideas

- **Automation bias**: "errors made when decision makers rely on automated cues as a heuristic" replacing vigilant information seeking. Two failure modes: commission (over-trust) and omission (failing to notice when automation doesn't alert)

- **Countermeasure 1 — Accountability**: crews perceiving themselves as accountable showed significantly greater verification behaviors and significantly fewer automation-related errors. Consistent across student and professional pilot samples.

- **Countermeasure 2 — Display prompts**: visual prompts encouraging verification of automated system status improved verification behaviors. Architecture of the display (whether and when the automated recommendation is shown) directly affects human judgment quality.

- **Countermeasure 3 — Training**: explicit training on automation bias combined with verification instruction reduces reliance on faulty automation cues. Improvement persists at follow-up (6-9 weeks).

- **Scope**: aviation/flight simulator domain — directly applicable to safety-critical software verification where human reviewers serve as supervisory controllers monitoring automated (LLM) assessments.

## Replaces

This source replaces Parasuraman & Manzey (2010) and Cummings (2004) as the primary evidence for automation bias mitigation requirements. Mosier & Skitka is preferable for a publicly shareable concept because both papers are publicly available on NASA NTRS, and the aviation context is more directly analogous to safety-critical software verification than general HF research.
