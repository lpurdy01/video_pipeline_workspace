# Decision register

Updated 2026-09-25.

| ID | Decision | Status |
|---|---|---|
| D-001 | Separate whitepaper/video/resource project; reuse previous processes | User requested |
| D-002 | Technical generalists and engineers; accessible video, rigorous paper | User confirmed |
| D-003 | Lead with a practical assurance architecture for learned autonomous systems | User confirmed; refined by D-021 |
| D-004 | Begin with car perception/navigation/avoidance; vehicle takes off near the end to test changing assumptions | User confirmed |
| D-005 | Build toward a fuller executable compiler with review queues and change-impact tracking, alongside a Markdown wiki | User preference; initial compiler implementation bounded below |
| D-006 | Gemini may process project text, scratch TTS and rendered visuals; human voice and detailed timing stay local | User explicitly approved for this project |
| D-007 | Human final voice, deterministic rendered final visuals, no music | Carried-forward working defaults; revisit before production |
| D-008 | Primary jurisdictions: US civil aviation/road vehicles; EASA and UK military explicitly compared | Proposed scope |
| D-009 | Show review coverage and blockers, not a composite safety/confidence score | Proposed architecture principle |
| D-010 | DAA experience is approximately five years old; use it to motivate questions, not current capability claims | User clarified; no names supplied |
| D-011 | Tesla/Cybercab may be a dated, click-worthy road opening, but the project centers the assurance architecture for learned autonomous systems rather than any company or developing investigation | User clarified 2026-09-15 |
| D-012 | The first adequacy argument concerns frozen, versioned trained models. In-service learning is a separate comparison and is excluded from the first worked assurance claim. | User clarified 2026-09-15 |
| D-013 | Express assurance as independently reviewable evidence contracts per hazard and operational domain, never as one composite model-safety score. | Project design decision 2026-09-15 |
| D-014 | The project may report only an audited, scoped finding that no publicly inspectable end-to-end method was found. It must never turn an incomplete search into the claim that no such method exists. | Project research decision 2026-09-15 |
| D-015 | AMLAS is the learned-component lifecycle baseline. The project will compare its artefacts with MAA case-specific guidance and EASA's proposed DS.AI, then state the remaining system/authority gaps. | Research integration 2026-09-16 |
| D-016 | The working literature finding is narrowed: inspected public material contains mature methods and authority pathways, but has not yet shown a final, publicly inspectable civil lifecycle that closes the hardest high-criticality trained-model case. | Independent challenge integration 2026-09-16 |
| D-017 | Open with the FAA's learned-versus-designed implementation framing. The paper will state the lost direct requirement-to-weight explanation plainly, then offer an evidence bridge; it will not claim that conventional requirements, software assurance, or traceability disappear. | Reader-structure decision 2026-09-22 |
| D-018 | Expand into a long-form standards, risk-evidence and proposed-architecture argument. Describe the public landscape as unfinished and fragmented rather than empty; distinguish US FMVSS self-certification from a learned-model safety claim; do not attribute standards maturity to a shortage of qualified people without evidence. | Research integration 2026-09-22 |
| D-019 | Preserve performance observations, uncertainty, exposure, recovery, residual-risk reasoning and safety/authority conclusions as separate graph objects. The compiler must never compute or present a composite certainty, reliability or safety score. | Compiler and visual architecture decision 2026-09-22 |
| D-020 | Use one shared, narrow vision-cue interface for the road and air worked cases: candidate image location/bearing, time and uncertainty/unknown. Give road and air separate data, frozen releases, tracking, action authority and evidence. Make AMLAS data/learning/verification failure modes visible in both paper and script. | User direction 2026-09-25 |
| D-021 | Controlling purpose: give industry engineers and managers perspective on (1) the scope of the learned-system assurance problem, (2) where the field is now, (3) gaps between standards and what authorities have yet to do, (4) the comparison with conventional software assurance, and (5) a proposed project structure worked through a simple vision-to-control pipeline. | User stated 2026-09-25 |
| D-022 | Paywalled standards (DO-178C, DO-330, ARP4754A/B, ISO 26262, ISO 21448, ISO/PAS 8800, UL 4600, ED-324/ARP6983 when published) may be named, but their content is characterized only through public regulator, government, standards-body or open-research documents, with the access boundary recorded in the source record. | User constraint 2026-09-25 |
| D-023 | Video is a three-part series; each episode stands alone and cross-links to the others and to earlier channel videos. Supersedes the 31–34 minute single-film plan; the D-004 take-off is the climax of episode 3. Scripts: `video/series_structure/`. | User confirmed 2026-09-25 |
| D-024 | Default model reviewer: `gemini-3.8-flash` with thinking level high (benchmarked above 3.1 Pro on 2026-09-25); one worker, at least 15 s between requests, stop on 429. Output is lead generation and review, never evidence. | User direction 2026-09-25 |
| D-025 | Road regulation adds UN R157 type approval as a comparison with US self-certification; EU Implementing Regulation 2022/1426 is not claimed until a primary source is captured. The worked case stays US-scoped. | Decided 2026-09-25 by the integrator on Levi's delegation ("decide for me") |
| D-026 | No runnable toy simulation: out of scope for laptop-only compute, and it would not strengthen the argument. Purpose element 5 is closed with worked artifacts instead: a timing budget and release manifest in the paper, and a label policy, evaluation-report template and change-impact record in the technical reference. All are labelled illustrative. | Levi hesitant 2026-09-25; integrator decision |
| D-027 | Release the three episodes together when all are done, even if they are finished sequentially; recheck dated status statements the week before release. | User decided 2026-09-25 |
| D-028 | Interlink the series with Levi's other channel videos through end screens, descriptions and pinned comments (plan in `video/series_structure/treatment.md`). | User decided 2026-09-25 |

## Decisions after the first worked case

- How to extend the executable compiler after proving its graph, review and invalidation contracts on this project's first claims.
- Which safety-case notation serves readers: plain claim/argument/evidence initially, GSN if it adds value.
- ~~Whether the practical artifact is an evidence-case walkthrough alone or also a reproducible toy simulation.~~ Resolved by D-026: worked artifacts, no simulation.
- Scope of authority delegated to the learned component and whether fallback observes an independent sensor path.
- ~~Target duration~~ resolved by D-023 (three episodes of roughly 8–10 minutes); main paper about 5,000 words plus the technical reference.
- Which independent reviewer and evidence-search workflow establish meaningful challenge, and how human decisions are recorded.
- Final public repository name, license, release format and publication destination.

No new external publication is requested at this setup stage.
