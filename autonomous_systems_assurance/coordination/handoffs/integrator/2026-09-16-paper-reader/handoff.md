# Reader review: current whitepaper prototype

**Reviewer:** technical-generalist reader/editor  
**Reviewed:** `resource_composition/whitepaper.md`, `resource_composition/review_prototype/index.html`, generated PDF  
**Review scope:** narrative clarity, usefulness as a direction-setting read, road-to-air transfer, and reader-facing rendering. This is editorial feedback, not a source-support disposition.

## Verdict

The paper has a sound and unusually clear core: assurance for a frozen trained release is an argument about a hazardous decision, not a contest to find one impressive model metric. The early occlusion example, explicit distinction between a finding/proposal/open condition, and refusal to equate the compiler gate with a safety score make it safe and useful for a technical generalist.

It is a strong **30--45 minute position paper plus source exploration**, rather than the requested one-to-two-hour project review. The Markdown is about 4,761 words. The current PDF is 27 pages mainly because every level-two heading starts a page; it feels longer than it reads and has several sparse pages. Expand the worked argument and improve the PDF before presenting it as the primary reader artifact.

## What is already working

1. **Opening premise.** “The problem is not that training is random” correctly separates frozen trained models from online learning and leads to a more productive question.
2. **Road encounter.** The two-indistinguishable-worlds explanation gives the reader a concrete failure before standards and terminology appear. It is the best material for the first video act as well.
3. **Honest positioning.** AMLAS, MAA, EASA, road standards, and the FAA roadmap are described with scope boundaries. This supports the important conclusion: public methods exist, but the paper does not identify a final public civil path for the hard flight-critical case.
4. **The eight contracts.** The table gives the proposed architecture a memorable shape. The later R1--R8 list supplies a usable first assurance argument.
5. **Source UX concept.** Claim tags, source cards, and direct original-document links make this substantially more reviewable than a conventional bibliography.

## Highest-value narrative revisions

### 1. State the proposed answer before the method survey

The abstract says what the graph is, but the reader does not see the project’s actual rule of operation until the contract table in section 3. Add a short boxed proposition after the road failure trace:

> A frozen trained component may influence a hazardous maneuver only when a versioned release, bounded operating domain, observable hazard distinction, hazard-partitioned performance evidence, closed-loop margin, useful intervention/recovery, system composition, and change control are all argued together. A failure in any one proposition restricts authority or blocks the release.

Then show an eight-node diagram or one-screen chain from **release → assumptions → hazard → obligations → evidence → authority decision → change impact**. This lets the rest of the paper read as evidence for an answer, not as a tour of relevant fields.

### 2. Add a compact conventional-to-trained bridge

The intended reader knows the earlier DO-178C/conventional-safety discussion. They need one explicit bridge explaining what remains familiar and what changes:

| Conventional artifact | Corresponding trained-system artifact | Additional assurance question |
|---|---|---|
| configured source/build | data/labels/training/configuration/weights/deployment transform | does this release represent the claimed operating domain? |
| requirement-based test | scenario-partitioned, held-out and shifted-condition evaluation | does a metric expose the hazardous error and latency? |
| integration test | closed-loop encounter and recovery evidence | is there still maneuver margin after an error? |
| change impact | release graph that includes data, model, sensor and ODD | which evidence must be rerun? |

The point is not to recapitulate DO-178C. It is to make the new evidence contracts feel like an extension of traceability discipline rather than a wholly separate philosophy.

### 3. Turn “Let the car take off” into a real transfer argument

The comparison table is accurate but too quick. It says what changes without showing how the assurance argument changes. Add an airborne R1--R8 parallel table or a two-column mapping that makes the transfer explicit:

* **Preserved:** release lineage, bounded domain, scenario-conditioned evaluation, change impact, monitor premises.
* **Changed:** encounter geometry, detection horizon, cooperative/noncooperative traffic, airspace rules, alerting/maneuver coordination, separation criteria, and the allowed recovery state.
* **Harder rather than merely higher consequence:** a road vehicle may often reduce exposure by slowing; an aircraft in an encounter needs separation in time, and landing is usually not an immediate DAA fallback.

A simple non-normative timeline would make the intuition concrete: detection/track establishment → decision/alert → control response → last recoverable separation. Label it a *case-specific margin accounting aid*, not a formula that proves safety. Then make the reader ask which evidence fills each interval.

### 4. Clarify the monitor/recovery distinction

The present text usefully warns about a shared missed-perception path. Keep it, but distinguish three questions that currently blur together:

1. What signal reveals the dangerous condition?
2. Who has authority to intervene, and how fast?
3. What maneuver/state remains safe once intervention occurs?

For air, avoid presenting “landing” as the natural collision-avoidance recovery. A near-term DAA recovery is normally a separation-preserving action, alert, maneuver, or an operational restriction; a landing may belong to a later contingency path. This will make the road-to-air difference technically sharper.

### 5. Give the project direction choices a more consequential form

The existing review agenda is good, but it reads as a list of questions after a conclusion. Frame 3--4 direction choices with their consequence for the next artifact. For example:

* first worked demonstration: observability/common-cause monitor failure vs. scenario taxonomy vs. confidence-to-authority policy;
* system boundary: learned perception feeding a constrained conventional planner vs. learned planning itself;
* evidence depth: a toy parameterized encounter versus a data/release manifest mockup;
* aviation focus: sensor/track assurance versus the approval-object map.

That will help the user guide the project at the high level they asked for.

## Important scope and reader-expectation gaps

* The paper appropriately avoids making a claim about a particular DAA product. Still, the reader who arrived through the DAA question needs a short callout: **why public terms such as “certified DAA” do not resolve the trained-perception assurance question.** Name the layers that must not be conflated: equipment authorization, installation, aircraft airworthiness basis, operational approval, and learned-model evidence. Link it to the planned product-specific source review rather than naming a product prematurely.
* Explain once that the “eight evidence contracts” are project-defined, while AMLAS/MAA/EASA are source methodologies or authority material. It appears in section 3, but repeat it at the crosswalk so it cannot be read as a claimed standard.
* The paper says no single metric is a safety score, but a short summary table could make the treatment of metrics memorable: scenario coverage / rare-event estimate / calibration / interpretability / neuron coverage, each with “what it can show” and “what it cannot close.” Section 5 explains these well in prose; the table would let a reader return to it.
* Section 8 is necessary but slightly early for a general reader. It could begin with a one-sentence reader benefit: “This is how the project prevents a source caveat from disappearing when a claim becomes a video caption.” Then the counts become evidence of process rather than project bookkeeping.

## Interactive and PDF defects to fix before sharing

1. **Claim links do not run in the HTML.** `header.html` calls `document.querySelector('main')`, but Pandoc’s generated `index.html` contains no `<main>` element. `createTreeWalker(null, ...)` throws, so claim tags are not transformed into source-card links and the compact-view listener is never registered. Use `document.body` or wrap the Pandoc body content in a real `<main>`, and guard missing elements.
2. **Invalid document structure.** `header.html` is injected into `<head>` through `--include-in-header`, yet it contains `<div id="reader-controls">`. Put the control in `--include-before-body`, or create it from a script after `DOMContentLoaded`. Keep only CSS/script metadata in the head.
3. **PDF title duplication.** The PDF’s first page contains the title twice: Pandoc emits its title block and the manuscript also begins with an H1. Suppress Pandoc’s title block (`--metadata title=` alone is not enough) or remove/convert the duplicate manuscript H1. The first-page extracted text begins with the title repeated twice.
4. **PDF pacing.** The `@media print` rule `h2 { break-before: page; }` forces every section to a new page and produces a 27-page, sparse document for 4,761 words. Remove the unconditional break, preserve only major parts/appendices, and allow sections 6--9 to flow. This will make the PDF feel intentionally composed rather than mechanically paginated.
5. **PDF claim links.** Claim-tag linking is currently JavaScript-based, so WeasyPrint does not make those tags into PDF hyperlinks. Generate Markdown/HTML anchors before print (or use explicit Markdown links for tags) so the PDF contains clickable source-card references as promised. Direct bibliography/source URLs are present; the tag-to-card interaction is not.
6. **Source-card print behavior.** Closed HTML `<details>` are good interaction controls but weak printed references. Provide an expanded, numbered reference list or force source-card detail text visible for the PDF. Reader-facing PDF citations should not rely on a click-to-expand element.
7. **Readability of source cards.** The cards should include each source’s status at a glance: authority/research/standard, jurisdiction, document status, source-support review state, and exact role in the argument. The current scope-limit prose is good; a compact metadata row would make scans faster.

## Suggested next reader version structure

1. Executive question and one-paragraph answer.
2. The occluded-road encounter and indistinguishable-world failure.
3. The proposed assurance rule and evidence-graph diagram.
4. Conventional traceability extended for a frozen trained release.
5. Eight contracts, grouped into release/domain, performance/dynamics, and system/change.
6. Existing methods crosswalk and its limits.
7. Road R1--R8 worked case with its open blockers.
8. Airborne transfer: preserved propositions, changed assumptions, DAA approval-object map, airborne R1--R8.
9. Evidence-method matrix: what each metric can and cannot establish.
10. Compiler/review state, source cards, project direction choices, and appendices.

This would make the paper a credible one-to-two-hour review once expanded with a full crosswalk, a visual/timeline, and source reading. The present version is already a good concise briefing from which to build it.
