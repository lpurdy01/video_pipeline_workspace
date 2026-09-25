# Handoff: 2026-09-25-direction-review / v1

- **Author/session and role:** Claude (Opus 5.5) in Claude Code session `9764b3e0`, acting as an independent direction reviewer at Levi's request. This is not a lane worker. The only project file this review writes is this handoff. Raw model output is under ignored `verification/out/`.
- **Date/time:** 2026-09-25T12:03-07:00
- **Job card:** none yet. Whoever acts as integrator creates job cards from §7 before assigning work.
- **Input baseline:** repository `HEAD 62f05a4`, dirty shared workspace. The file hashes are in §10.
- **Output:** this file.
- **Completion state:** review complete. **No remediation was performed.** Every item below is open.
- **Follow-up:** Levi will ask the reviewer to re-check progress against the `DR-xx` "Done when" checks in §4 and the metrics in §10. Report status per `DR-xx` in your own handoff.

---

## 0. How to use this handoff

1. Read §1 (the user's inputs) and §3 (the paywall constraint) before touching anything. Both bind the work.
2. §4 lists the findings as `DR-01` to `DR-19`. Each has a **Done when** checklist. This is a review, not a specification. You may reject or modify a recommendation if you write down why. Decisions reserved for Levi are marked **USER DECISION** and collected in §8.
3. Follow `coordination/README.md`. Integrator-only paths (`planning/`, `PROJECT_BRIEF.md`, `assurance/`, `verification/`, `wiki/`, `coordination/tasks/`, `coordination/lanes.json`, `research/sources.json`) change only while someone is explicitly acting as integrator.
4. In your handoff, give each DR one status: `addressed` / `partial` / `deferred (reason)` / `rejected (reason)` / `blocked on user`. Also say where the change lives (file and section).
5. Keep the project's claim discipline. New factual statements need source/claim records in a contribution registry, with public URLs, inspection scope and status. Everything marked **[VERIFY]** in this handoff was **not** checked against a primary source in this review. It is a lead, not a claim.

---

## 1. User inputs captured in this session (2026-09-25)

**U-1. Audience and purpose.** This is Levi's statement, lightly cleaned. It is the controlling brief for the restructure:

> The target audience is industry professionals, engineers, and managers. It is supposed to give perspective to technical people on the scope of the problem, where we are currently at, gaps between different standards and what standard authorities have yet to do, compared to what has already been done for conventional software development, and a proposed project structure with the example of a simple vision → control pipeline showing what developing to an ML safety standard would look like.

The five purpose elements used throughout this handoff:
- **P1** scope of the problem
- **P2** where we are now
- **P3** gaps between standards, and what authorities have yet to do
- **P4** comparison with conventional software assurance
- **P5** a proposed project structure, worked through a simple vision → control pipeline

**U-2. Openness to challenge.** "You can argue with this video/paper's purpose; I am open to considering better things to do with my time. But I think I see a gap in public content."

**U-3. HARD CONSTRAINT: no access to paywalled standards.**

> Although we can reference them, I can't access DO-178C or other documents that are behind expensive paywalls. We have to allude to them with other documents that we can reference.

See §3 for the operating rules and the proxy list.

**U-4. Model choice for Gemini work.** Use the strongest model available, which need not be a "Pro" model. Levi expected the newer thinking/Flash generations to have overtaken 3.1 Pro. That was **checked and confirmed**:
- Artificial Analysis Intelligence Index: Gemini 3.8 Flash (high) = 41, 3.1 Pro Preview = 30.
- benchlm: 3.8 Flash leads overall, with overlapping intervals, and leads clearly on the agentic and coding lanes.
- `gemini-pro-latest` still resolved to `gemini-3.1-pro-preview` on 2026-09-25.

**Use `gemini-3.8-flash` with `generationConfig.thinkingConfig.thinkingLevel = "high"`** (verified working). Rate-limit deliberately: one worker, at least 15 s between request starts, stop on the first 429. Gemini output is lead generation and review, never evidence.

These scripts still hard-code 3.1 Pro and should be updated, recording that the reviewer model changed:
- `verification/first_pass_model_review.py:26`
- `verification/gemini_diagnostic.py:28`
- `research/gemini_independent_20260916/run_grounded_research.py:121`
- `resource_composition/crosspoint_review/agentic_review.py:142,202`

**U-5. Standing decisions not reopened by this review:**
- D-004: the car takes off near the end.
- D-007: human voice, rendered visuals, no music.
- D-010: Levi's DAA experience is dated and names no programs.
- D-011: Tesla is optional hook material only.
- D-012: frozen models first.
- D-020: one shared vision-cue interface for road and air.

Where §4 recommends changing a decision (D-003, D-008), it is marked USER DECISION.

---

## 2. Summary verdict

**Worth doing, with a narrower claim to differentiation.**

The strongest idea is original and under-served in public material. We call it "two worlds, one input": observability comes before software correctness. A deterministic planner or monitor cannot recover information that no channel captured, which is exactly why monitor-based and decomposition-based safety claims fail when channels share perception.

Against the stated purpose, however:

| Purpose | Current coverage | Main reason |
|---|---|---|
| P1 scope | Strong | FAA learned-implementation framing, plus the two-worlds argument |
| P2 where we are | Partial | ED-324/ARP6983, SOTIF, CoDANN/W-shaped process and EASA Concept Paper are in the research registries but absent from the paper |
| P3 gaps and what authorities have yet to do | Partial | The status ladder and coverage map exist, but there is no explicit register of open items |
| P4 vs conventional software | **Missing** | 0 paper mentions of DO-178C, ISO 26262, IEC 61508, ARP4754, MC/DC, DAL or ASIL. One 4-row table in §3 |
| P5 project structure | Partial | Eight abstract contracts and a 6-step training sequence. No plans, artifacts, roles or gates a manager recognises. No runnable example |

The prose is also over-qualified, at about one negation construction per 88 words. The likely cause is structural: the compiler's review lanes (source-support, challenge, cross-artifact) reward qualification, and nothing reviews reader value.

**Differentiation to aim for.** Public material exists: EASA's Concept Paper, AMLAS, academic surveys, and road-safety-case literature. What is rare is the combination of:
1. a manager-level, pillar-by-pillar comparison of the conventional assurance playbook and what ML breaks;
2. a road-vs-air comparison of regulatory regimes;
3. a runnable, system-level, closed-loop worked example with change control.

Item 3 ages slowest and plays to this project's tooling strengths. The landscape survey alone will date within months (see DR-17).

---

## 3. Operating rules for paywalled standards (U-3)

**Rules**

1. **Name, don't quote.** You may name DO-178C, DO-254, DO-330, ARP4754B, ARP4761A, ISO 26262, ISO 21448, ISO/PAS 8800, IEC 61508, UL 4600, ED-324/ARP6983 and similar documents. Never quote or paraphrase clause-level content you have not lawfully read.
2. **Attribute every characterization to a public source.** Write "FAA AC 20-115D recognizes DO-178C as an acceptable means of compliance for airborne software…", not "DO-178C requires…". A claim's `scope` field should name the public document that makes the statement. Treat the paywalled standard as the *subject*, never the *evidence*.
3. **Prefer regulator and government publications**, then open-access peer-reviewed or book sources, then publisher abstracts and scope pages. Vendor blogs and consultancy summaries are leads only.
4. **Record the access boundary.** Source records note "standard text not accessed; characterization from <public source>". The paper needs one short box, e.g. "About the standards cited", explaining that several key standards are copyrighted and paywalled, so the paper characterizes them through public regulator material. *Optional point:* the cost barrier to public scrutiny of safety standards is itself part of the landscape. Only make this point with a sourced framing.
5. Do not redistribute licensed standards (existing AGENTS.md rule).
6. **Reuse public captures from the sister project** by creating **new** source records in this project's registry. Copy no claims or conclusions (AGENTS.md: "do not copy old claims").

**Public proxies already available locally**, paths relative to the repository root. Re-inspect them before relying on them:

| Local file | What it can support | Notes |
|---|---|---|
| `refrence_literature/raw/pdfs/faa_ac_20_115d.pdf` (+ `raw/extracted_markdown/faa_ac_20_115d.txt`) | FAA recognition of DO-178C/ED-12C, DO-330 tool qualification and the supplements. The regulator's own framing of software levels | Public FAA advisory circular |
| `refrence_literature/raw/pdfs/nasa_ntrs_20120016835_jacklin_do178c.pdf` (+ extracted text) | Public NASA explanation of DO-178C/DO-278A objectives, structural coverage, DO-330, and the model-based / OO / formal-methods supplements | Jacklin, NASA NTRS 20120016835 |
| `refrence_literature/raw/pdfs/npr_7150_2d.pdf`, `nasa_std_8739_8b.pdf` (+ extracted) | A public government software standard with MC/DC requirements for safety-critical software, usable as a public analog of structural-coverage practice | NASA; state clearly that this is NASA's requirement, not DO-178C's |
| `refrence_literature/Developing_safety_critical_software/Rierson … DO-178C … (2013, CRC Press).md` | Secondary-source explanation of DO-178C, DO-254, ARP4754 (41 mentions), MC/DC, tool qualification, and history | Published book. Cite as a book; don't redistribute the text |
| `autonomous_systems_assurance/verification/out/sources/book_intake/text/maurer-autonomous-driving.txt` | Open-access description of ISO 26262 (26 mentions) and road safety concepts | *Autonomous Driving* (Springer OA, 978-3-662-48847-8). Already record S-016..S-020 in this project |
| `autonomous_systems_assurance/verification/out/sources/retrieval_check/easa_issue2.pdf`, `easa_issue3.pdf` | EASA's own framing of learning assurance relative to development assurance (ED-12C/DO-178C, ED-79/ARP4754) | Already retrieved; content relative to DO-178C was **not** inspected in this review **[VERIFY]** |
| Local book *Engineering a Safer World* (Leveson, MIT Press OA) | STPA and system-theoretic hazard analysis (relevant to composition and unsafe control actions) | Already in `research/books_inventory.md` |

**Candidate public proxies to retrieve.** All **[VERIFY]**: availability, current edition and exact content were not checked.
- **Aviation system level:**
  - FAA AC 20-174 (FAA recognition of ARP4754A; check whether a revision covers ARP4754B);
  - AC 25.1309-1B and AC 23.1309-1E (failure-condition classes, probability and DAL relationships);
  - FAA Order 8110.49A (software approval guidelines).
- **Aviation hardware and platform:**
  - FAA AC 20-152A (DO-254);
  - EASA AMC 20-152A (airborne electronic hardware);
  - EASA AMC 20-193 and CAST-32A (multicore). Relevant to GPU/accelerator inference as an open gap.
- **Structural coverage:** NASA/TM-2001-210876, *A Practical Tutorial on Modified Condition/Decision Coverage* (Hayhurst et al.).
- **ML-specific aviation:**
  - EASA/Daedalean CoDANN I and II reports (W-shaped learning assurance vs the V-model); the project already has a summary-level record;
  - the DEEL/ANITI white paper *Machine Learning in Certified Systems* (arXiv 2103.10529 [VERIFY ID]);
  - public ED-324/ARP6983 material: EUROCAE's open-consultation page, the FAA AI/ML Tech Exchange presentation (Aug 2025, "ED-324/ARP6983"), and the paper "A study of an ACAS-Xu exact implementation using ED-324/ARP6983".
- **Automotive:**
  - ISO Online Browsing Platform pages (scope, terms and definitions) for ISO 26262 / 21448 / PAS 8800;
  - NHTSA DOT HS reports that summarize ISO 26262 (e.g. DOT HS 812 285 [VERIFY]);
  - peer-reviewed or open papers explaining the SOTIF known/unknown × safe/unsafe areas;
  - SAE J3016 (free view [VERIFY]);
  - UL 4600 via UL Standards & Engagement free digital view [VERIFY], or public Koopman papers on UL 4600;
  - Waymo's public safety-case papers (the project already has `C-ROAD2-012`/`C-ROAD2-013` process claims).
- **Regulation (public):**
  - UNECE Regulation No. 157 text and the UNECE 130 km/h press release;
  - EUR-Lex Commission Implementing Regulation (EU) 2022/1426;
  - EU AI Act, Regulation (EU) 2024/1689 (EASA's NPA is the aviation response to it).

---

## 4. Findings and requested changes

### A. Argument gaps

**DR-01: Conventional-software baseline is missing (P4). Highest priority.**

The comparison lacks the thing being compared against. Engineers and managers know these pillars:
- system → item → software/hardware development assurance, with ARP4754-style allocation and DAL/ASIL/SIL levels;
- bidirectional requirements traceability;
- requirements-based testing plus structural coverage (MC/DC at the highest level), which is how "no unintended functionality" is argued;
- independence of verification;
- configuration management;
- tool qualification;
- certification liaison.

State which pillars ML breaks and what is proposed to replace each. Neuron coverage (already in §5 of the paper) will then make sense to the reader as a failed analog of structural coverage. Add a short maturation timeline: conventional software assurance took decades to reach its current editions, and ML assurance's first dedicated process standards are only now arriving. **Exact dates are [VERIFY]** against public sources (Rierson, Jacklin, FAA ACs).

**Done when:**
- [ ] A section explains the baseline in manager-level language, sourced only per §3.
- [ ] A table has columns *conventional pillar → what a learned component breaks → substitute evidence → who proposes it (AMLAS / EASA / ED-324 public description / project)*, with ≥6 rows.
- [ ] New source records exist in a contribution registry for at least: aviation software assurance, aviation system assurance, automotive functional safety, and structural coverage.
- [ ] No clause text from a paywalled standard appears. Characterizations are attributed.
- [ ] The timeline dates carry claim tags or are removed.

**DR-02: The aviation ML standards pipeline is absent from the paper (P2, P3).**

The research has it: `C-CHAL-005` records ED-324 as "Draft", target publication 31 Dec 2026, captured 2026-09-16. Also in research: the CoDANN W-shaped process (`C-METHOD2-008`), EASA Concept Paper Issue 2 and Proposed Issue 3 (`C-AUTH-004/005`), and ISO 21448 (`C-METHOD2-011`). None appear in the manuscript.

ED-324/ARP6983 is the joint EUROCAE WG-114 / SAE G-34 process standard. Web summaries say its first edition covers frozen, supervised ML only **[VERIFY with a public primary source]**. That matches D-012 and should be said.

EASA NPA 2025-07 status checked in this review via a web search summary of EASA pages:
- published 10 Nov 2025;
- comment period extended to 10 Mar 2026;
- the first step of RMT.0742, with a second NPA planned in 2026 to deploy the framework into domain regulations;
- a response to the EU AI Act (Reg. 2024/1689).

Recapture before use.

**Conflict to record:** some older web sources said ED-324 would publish in Q1 2026. The project's 2026-09-16 capture of EUROCAE's own page says draft, target 31 Dec 2026. Recheck EUROCAE directly.

**Done when:**
- [ ] The paper describes ED-324/ARP6983 with its capture date, status, the committee behind it, and first-edition scope (from a public source).
- [ ] The paper includes the W-shaped learning-assurance idea (CoDANN/EASA source) as the aviation audience's familiar visual.
- [ ] The paper states the EASA NPA timeline, including the planned second NPA and the AI Act driver.
- [ ] The FAA status is stated (roadmap, project-specific issue papers, whether ARP6983 recognition is pending).
- [ ] Each item carries a status label and an "as of" date.

**DR-03: SOTIF and the road standards stack (P2, P3).**

The occluded-cyclist case is the textbook SOTIF hazard: a functional insufficiency plus a triggering condition, not a random or systematic fault. Automotive readers will ask "isn't this just SOTIF?", and the paper should answer them. The roles to explain, per §3 sourcing:
- ISO 26262 for faults;
- ISO 21448 for insufficiencies, triggering conditions, and the known/unknown and safe/unsafe areas;
- ISO/PAS 8800 for AI elements;
- UL 4600 for the autonomy safety case.

Consider STPA (Leveson, local open-access book) as the composition-analysis method.

**Done when:**
- [ ] A road-stack explanation exists.
- [ ] The cyclist hazard is described in SOTIF vocabulary with a public source.
- [ ] The paper states what the stack leaves open for learned perception.
- [ ] No paywalled clause content appears.

**DR-04: Use real, adjudicated failures instead of open inquiries (P1, P5).**

- **Uber ATG, Tempe 2018, NTSB HAR-19/03** (public). Checked in this review via a search summary of NTSB material:
  - the system detected the pedestrian about 5.6 s before impact;
  - her classification changed between unknown, vehicle and bicycle (vehicle at about 4.6 s, bicycle at about 2.5 s);
  - at 1.3 s the system determined emergency braking was needed, but the design precluded activating it, relying on the human operator.
  - Gemini additionally claims that reclassification discarded track history, which fed the path prediction **[VERIFY in HAR-19/03]**.
  - Lesson: detection was not the failure. Tracking, prediction, action suppression and authority allocation were. That is exactly O-005, O-006 and O-007.
  - The project's rule against inferring from investigations targets *open inquiries*. A final NTSB board report is an adjudicated finding. Quote its findings, not an inference.
- **ACAS Xu.**
  - Katz et al., *Reluplex* (CAV 2017), verified properties of a neural-network compression of the ACAS Xu advisory tables.
  - Bak & Tran, *Neural Network Compression of ACAS Xu Early Prototype Is Unsafe: Closed-Loop Verification Through Quantized State Backreachability* (NFM 2022), found the early prototype network unsafe in closed-loop analysis.
  - This is the cleanest public "component proof ≠ system safety" case, and it sits in the DAA domain the video takes off into.
  - Both titles were confirmed in this review. The findings' exact scope is **[VERIFY]**.
- **Cybercab.** Demote the NHTSA inquiry (`C-ROAD2-004/005`) to at most one sentence, or remove it. As the paper itself says, it proves nothing about model evidence.

**Done when:**
- [ ] The Uber trace is in the worked walkthrough (DR-07), with claims sourced to HAR-19/03.
- [ ] The ACAS Xu closed-loop result is in the methods or take-off section, with claims.
- [ ] Cybercab is reduced to one sentence or less in both paper and script.

**DR-05: The architecture-trend tension is missing (P1, P3).**

Industry is moving toward end-to-end learned driving and foundation models. Examples: Tesla's public statements about end-to-end networks, and Wayve. **[VERIFY with primary developer statements]**; the existing `C-ROAD2-010` covers only Tesla's BEV/world-model description.

These architectures collapse the interfaces the evidence bridge depends on: cue → tracker → planner → monitor. The public frameworks (ED-324 first edition, the MAA recommendation for fixed supervised models, EASA's NPA scope) handle modular, frozen, supervised components. "The architecture that can be assured and the architecture being shipped are diverging" may be the most valuable perspective for managers. It also turns D-020's vision-cue interface from a teaching simplification into an argument: **the architecture choice determines whether a system can be assured.**

**Done when:**
- [ ] A subsection frames this as a tension, not a verdict.
- [ ] The trend is sourced to public developer statements.
- [ ] The paper states what an end-to-end design would need to replace each lost interface.

**DR-06: An explicit "what authorities have yet to do" register (P3).**

Turn the scattered status material into one dated table with columns *open item / owner / status as of <date> / consequence for a program today*. Candidate rows, all needing claim tags:
- ED-324/ARP6983 publication and FAA recognition;
- FAA ML policy or advisory circular (none found; project-specific issue papers only);
- EASA's second NPA;
- EASA Level 3B, which is reserved;
- H1 (potential fatality) hazards, unacceptable in every likelihood band;
- online and continual learning (excluded across frameworks);
- quantitative perception-performance targets linked to hazard rates;
- qualification of ML development tools;
- assurance of COTS GPU/accelerator hardware;
- a runtime-assurance standard. ASTM F3269 status is unknown; a Gemini lead claimed it was withdrawn **[VERIFY]**;
- US road: no FMVSS for ADS performance; voluntary guidance; a state-by-state patchwork.

Add the positive side of road practice as well: the public safety-case process and third-party audit disclosures (Waymo, `C-ROAD2-012`/`013`).

**Road regime contrast (USER DECISION on D-008 scope).** US self-certification versus EU/UNECE pre-approval:
- UNECE R157 ALKS is the first harmonized Level 3 regulation, extended to 130 km/h with lane change from January 2023 (confirmed via UNECE press);
- EU Implementing Regulation 2022/1426 sets ADS type-approval for fully automated vehicles in small series (confirmed via search summary).

This is the sharpest "gap between standards" contrast available. D-008 currently scopes road coverage to the US. Recommend adding EU/UNECE at least as a comparison row.

**Done when:**
- [ ] The register table exists with ≥8 claim-tagged rows and a capture date.
- [ ] The EU/UNECE contrast is included, or its exclusion is recorded as a user decision.

**DR-07: A project structure a manager would recognize (P5). This is the practical centerpiece.**

Build a lifecycle table for the vision → control pipeline:
- **Rows (phases):** system safety assessment and hazard allocation → ML requirements and ODD → data management → model learning → implementation and deployment transform (export, compile, quantize) → learning and implementation verification → integration and closed loop → operation, monitoring and change.
- **Columns:**
  - artifact produced;
  - its conventional analog, e.g. plan set, requirements, verification cases, configuration index. **Source this per §3**; the plan names come from the public FAA/NASA/Rierson descriptions;
  - which framework asks for it (AMLAS stage / EASA objective family / ED-324 public description / project);
  - owner role;
  - review gate;
  - the eight-contract ID (O-001..O-008).

Keep the eight contracts as the spine, and **keep one representation of them** (see DR-11). Include:
- the existing training-traps table (§4, lines 187-194). It is good;
- the 6-step training sequence;
- the Uber trace (DR-04).

**Tool qualification and the deployment transform (from DR-01):** the deployed network is a different function from the evaluated one unless evaluation runs on the exact exported/compiled/quantized artifact. The training framework, data tooling, simulator and compiler are tools whose influence needs an argument. Gemini called quantization "non-deterministic"; that is overstated, so don't repeat it.

**Done when:**
- [ ] The lifecycle table exists with ≥8 phases, each mapped to O-IDs, with conventional analogs sourced per §3.
- [ ] Tool qualification and the deployment transform appear as explicit rows or obligations.
- [ ] A manager can read the table as "what my program would produce".

**DR-08: Runnable toy worked example (P5). USER DECISION.**

`planning/decisions.md` lists "whether the practical artifact is an evidence-case walkthrough alone or also a reproducible toy simulation" as open. The reviewer strongly recommends **yes**:
- a small 2D or low-fidelity road simulation;
- a small detector producing the D-020 cue;
- a braking controller, a monitor, and real artifacts: data manifest, grouped splits by encounter, partitioned evaluation, a closed-loop "correct but too late" failure trace, and a camera or mounting change that invalidates evidence through the compiler graph.

This is the project's most durable differentiator.

**Done when:**
- [ ] Levi has decided.
- [ ] If yes, a job card with its own lane and write path exists (proposed `demo/`, IDs `S-DEMO-`/`C-DEMO-`) with the AGENTS.md rule "no physical deployment; state assumptions and evidence limits".

### B. Structure

**DR-09: Reorder the whitepaper to follow the purpose statement.**

Proposed order, mapping current sections to new ones:

| New § | Content | Draws from current |
|---|---|---|
| 1 | Hook: two worlds, one input (about 1 page) | §2 lines 72-94 |
| 2 | How conventional safety software is assured today, with timeline | **new** (DR-01) |
| 3 | What a learned component breaks, pillar by pillar | §1 + §3 "bridge from conventional" table |
| 4 | Where we are: status ladder, coverage map, ED-324, road stack, road-vs-air regimes | §4 (+DR-02, DR-03) |
| 5 | What authorities have yet to do, plus the architecture-trend tension | **new** (DR-05, DR-06) + parts of §9 |
| 6 | Developing a vision → control pipeline to an ML standard | §2 vision task, §4 training traps + sequence, §3 contracts, §6 R1–R8 (merged), Uber (DR-04, DR-07) |
| 7 | What each verification method can and can't close | §5 minus tangents (DR-11); may fold into §6 |
| 8 | Let it take off: physics *and* regulatory regime change; ACAS Xu | §7 (+DR-04) |
| 9 | What teams should do now: actionable, manager-facing | §9 rewritten |
| App. | Case status; the verification compiler; method crosswalk; sources; consolidated limits/scope box | §8, App. A–C, §10 review agenda (drop from the public version) |

**Done when:**
- [ ] The headings follow this order, or a documented alternative with rationale.
- [ ] Every current section is accounted for: moved, merged or cut.

**DR-10: Cut and consolidate.**
- Move §8 ("A verification compiler for the paper itself") to an appendix. It is meta for this audience.
- **Cut** "Professional qualification is not a maturity test" (NCEES) and "Road incidents and electric vehicles…" (EV vs ICE). They were Levi's earlier hypotheses, which the research correctly refuted. Publishing the refutation gives the reader nothing. Keep the research records; just remove the manuscript uses (C-DIR-001/002; keep C-DIR-003 only if the SGO point survives).
- The eight contracts appear **four times**: the rule box in §2, the table in §3, R1–R8 in §6, and Figure 2 ("six questions"), whose caption says eight. Keep one canonical representation and reconcile six vs eight.
- Remove hard-coded counts from prose. §8 says "89 source records and 94 provisional claims"; the compiler now reports 102 and 114.

**Done when:**
- [ ] All four bullets above are resolved.

**DR-11: Video format (runtime and structure).**

Analytics baseline (`planning/analytics_baseline.md`): the previous ~11.5-minute video averaged 2:57 viewed; retention fell 96.4% → 52.6% in the first 35 s and about 19% → 10% after 10:30. At the planned 31–34 minutes, most viewers will see only the first few minutes.

**Recommend a 3–4 episode series of 8–12 minutes, each standalone, each hooking within 20 s:**
1. *Why the software safety playbook breaks on ML*: two worlds, the conventional pillars, the FAA framing.
2. *Who's writing the rules, road vs air*: the landscape, ED-324, US vs UNECE, the yet-to-do list.
3. *Building a vision → control pipeline to an ML safety standard*: the lifecycle, training traps, Uber.
4. *Let it take off*: DAA physics, ACAS Xu, aviation approval layers.

The alternative is a single 12–15 minute flagship plus the paper. Keep the standards landscape; Gemini's outline dropped it, but it is P2/P3. **USER DECISION** on the format. This audience may also be better reached through a LinkedIn article series or a conference venue alongside YouTube.

**Done when:**
- [ ] The format decision is recorded.
- [ ] A new treatment under `video/` (e.g. `video/series_structure/`) has per-episode runtime ≤12 min, a hook ≤20 s, claim-tagged narration beats, and one "payoff" visual per episode.
- [ ] The old 31–34 min plan is marked superseded, not deleted.

### C. Tone

**DR-12: Reduce hedging density without losing accuracy.**

Baseline counts (reproducible command in §10):
- whitepaper: **99** negation constructions in 8,731 words, and "propos*" **49**×;
- script: **64** in 4,987 words, and "propos*" 23×.

Remedies:
1. One scope/limits box near the top, merged with Appendix C, and one "About the standards cited" box (§3 rule 4).
2. State scope inside a positive sentence. Replace "This is a project architecture, not a claim that a second sensor or a monitor automatically makes a system safe" with "A monitor helps only if it can see something the planner can't."
3. Keep all claim tags.
4. Integrator: add an **editorial/audience gate** to the review process, alongside source-support, challenge and cross-artifact, so something reviews reader value.

Guideline target: at most about 1 negation per 200 words, and "propos*" at most about 20 in the paper. This is not a hard metric; do not game it by rephrasing hedges into different words. A human read decides.

**Done when:**
- [ ] The scope boxes exist.
- [ ] The density is at or near the guideline in both paper and script.
- [ ] The editorial gate is documented, or deferred with a reason.

### D. Project and process

**DR-13: Almost nothing is committed. USER DECISION.**

`git ls-files autonomous_systems_assurance` shows 10 tracked paths, all CrossPoint tooling. The whitepaper, script, research registries, claims, assurance graph and figures are all **untracked** (`??`). Do not commit without Levi's go-ahead.

**Done when:**
- [ ] Levi has decided and the outcome is recorded.

**DR-14: Freeze tooling until the content restructure lands.**

Publishable content is about 13.7k words (paper plus script). Against that sit about 16.7k words of planning, coordination and integration docs, 669 handoff/review files, about 3k lines of Python tooling, and 340 MB of e-reader firmware under `tools/`. Human-disposition coverage is **0%**. The bottleneck is authorial decisions and Levi's review, not verification.

**Done when:**
- [ ] No new compiler, dashboard or CrossPoint features are added until DR-01..DR-12 are addressed or deferred.
- [ ] Compiler use is limited to compiling, adding new prose to `verification/artifacts.json`, and rate-limited reviews.

**DR-15: Brief and decisions have drifted from U-1. Integrator, with USER DECISION.**

`PROJECT_BRIEF.md` and D-003 ("lead with a practical assurance architecture") predate U-1. U-1 puts P2, P3 and P4 first. Proposals:
- amend D-003, or add a D-021 recording the U-1 purpose;
- add a decision recording U-3 (paywall constraint and proxy rule);
- add a decision recording the U-4 model choice;
- resolve the D-008 road-scope question (DR-06);
- update the outdated line in decisions.md: "provisional video range 9–12 minutes" conflicts with the 30–38 minute plan (`planning/longform_project_flow.md`). Settle this under DR-11.

**Done when:**
- [ ] The decision register and brief reflect U-1, U-3 and U-4.
- [ ] USER DECISION items are asked, not assumed.

**DR-16: Release timing relative to ED-324.**

The target is 31 Dec 2026, about 3 months out. A paper released before it that does not discuss it looks stale on arrival. Either publish with an explicit "as of" date and an update plan, or time the release to the standard's publication. That is a natural news hook: "the first aviation ML process standard just arrived; here's what it covers and what it still doesn't". **USER DECISION.**

**Done when:**
- [ ] A release-timing plan is recorded in `planning/roadmap.md` (integrator).

### E. Defects

**DR-17: Manuscript and figure defects.**
- Figure numbering in the paper runs 1, 2, 2a, 3, **5, 4**: Figure 5 (line 237) appears before Figure 4 (line 255).
- Figure 2 is titled "six questions", but its caption says "eight evidence contracts" (line 49).
- Text overflow and clipping were seen when rendering with headless Chromium. The PDF renderer may differ, so re-check there:
  - `learned_traceability_gap.svg`: the "No direct requirement coverage argument" label overlaps the Release-lineage box; the bottom captions overlap; the right column is clipped.
  - `evidence_bridge_ladder.svg`: the box 4 title is clipped; box 6 text overruns its border.
  - `assurance_shells.svg`: the "allowed action" label collides with the arrows; "release/change" is clipped.
- "MCRI" is never expanded (line 211).

Per `feedback_model_review_authority` (user memory): if text is unreadable, make it bigger or shorter; never delete the idea it carried.

**Done when:**
- [ ] Numbering is sequential and six vs eight is reconciled.
- [ ] The three SVGs render without overlap or clipping (attach renders to your handoff).
- [ ] MCRI is expanded.

**DR-18: Extend the coverage map.**

`assurance_coverage_map` is the strongest figure. It is EASA-centric. Add:
- reference rows for the conventional baseline (aviation software and system assurance, automotive functional safety), sourced per §3;
- the road stack (SOTIF, PAS 8800, UL 4600);
- ED-324 with its status;
- UNECE/EU road type approval, if the D-008 decision allows.

Keep its "not a ranking" semantics.

**Done when:**
- [ ] The updated figure plus a caption with claim tags exists.
- [ ] `figures.md` is updated.

**DR-19: Take-off section should show a regime change, not only physics.**

The current §7 focuses on sensing, timing and recovery physics. Add the second half of the contrast: road (US self-certification / state permits / UNECE type approval) versus aviation (TSO, installation, type certificate, operational approval, and DAL allocation via the system safety assessment, described per §3 sources). This keeps the "take off" doing double duty for P3.

**Done when:**
- [ ] The take-off section contains a sourced regime comparison, without ranking which domain is "harder".

---

## 5. Independent model review: provenance and dispositions

- **Model:** `gemini-3.8-flash`, `thinkingLevel=high`, one call. 20,451 prompt tokens, 3,711 output tokens, 3,649 thinking tokens.
- **Input:** whitepaper.md and script.md at the §10 hashes, plus the U-1 purpose statement and a senior-reviewer prompt (script at the session scratchpad, not preserved in the project).
- **Output:** `verification/out/nextgen_gemini_audit/20260925T185344Z_audience_structure_gemini-3.8-flash.md` (sha256 in §10). This is lead generation, not evidence or a disposition.
- **Author relationship:** a different model family from the reviewer, but it read the same text. That gives reviewer diversity, not independent evidence.

**Where Gemini converged with the Claude review:**
- SOTIF missing;
- WG-114/G-34 (ED-324/ARP6983) missing;
- tool qualification and DAL/ASIL allocation and decomposition missing;
- the Uber NTSB case;
- hedging density;
- runtime far too long;
- move the compiler section to an appendix;
- "two worlds, one input" is the strongest idea;
- the public gap is bridging ML engineers and system-safety assessors.

**Gemini suggestions rejected or modified:**

| Gemini suggestion | Disposition | Reason |
|---|---|---|
| Its video outline drops the standards landscape | Rejected | The landscape is P2/P3 in U-1 |
| "Taking the Same Model to 250 Knots" | Rejected | D-020 and the paper correctly say only the interface transfers, not the model |
| Quantization introduces "non-deterministic tensor truncation" | Modified | The real point: the deployed artifact is a different function unless evaluated directly (DR-07) |
| "Completely unviable" runtime; "brilliant" device | Tone discounted | Directionally right, overstated |
| "Nobody certifies an end-to-end ML model to DAL A" | Unverified | Treat as a lead only |
| ASIL decomposition example "ASIL D = ASIL B(D) + ASIL B(D)" | Lead | Describe decomposition only via a public source (§3) |

---

## 6. Cautions: do not do these

- Do not quote, closely paraphrase, or infer clause content of paywalled standards (§3).
- Do not say "no method exists" or "no one has published X". Use the project's dated "we did not find, within this search" formulation (D-014).
- Do not transfer the road model, data adequacy or approvals to air (D-020).
- Do not promote any **[VERIFY]** item in this handoff to narration or prose before it has a source record.
- Do not delete research records when removing manuscript uses (DR-10). Remove the uses only.
- Do not strip scope accuracy to hit the DR-12 density guideline. Consolidate scope; don't lose it.
- Do not commit, push, or change `lanes.json` without the integrator role and, for commits, Levi's go-ahead.

---

## 7. Suggested job split (per `coordination/README.md`)

The ID prefixes below were checked as unused on 2026-09-25. Prefixes in use: METHOD2, ROAD2, AIR2, AUTH, RISK, EVID, CHAL, STD, INTAKE, TRAIN, ROAD-AIR, DIR, ROAD, and numeric seeds.

**Wave 1: research. Can run as 3 parallel workers.**

| Job | Lane dir | Prefixes | Write paths | Covers |
|---|---|---|---|---|
| `2026-09-2x-baseline-01` | `baseline_public` | `S-BASE-` / `C-BASE-` | `research/contributions/baseline_public/`, `coordination/handoffs/baseline_public/` | DR-01, tool-qualification part of DR-07, DR-19 aviation approval layers |
| `2026-09-2x-status-01` | `standards_status` | `S-STAT-` / `C-STAT-` | `research/contributions/standards_status/`, `coordination/handoffs/standards_status/` | DR-02, DR-03, DR-06 (incl. UNECE/EU and the ASTM F3269 check) |
| `2026-09-2x-cases-01` | `cases` | `S-CASE-` / `C-CASE-` | `research/contributions/cases/`, `coordination/handoffs/cases/` | DR-04, DR-05 |

**Wave 2: composition, against frozen Wave-1 claims. Can run as 2 parallel workers.**

| Job | Lane | Write paths | Covers |
|---|---|---|---|
| `2026-09-2x-paper-01` | PAPER | `resource_composition/`, `coordination/handoffs/paper/` | DR-07, DR-09, DR-10, DR-12 (paper), DR-17, DR-18 |
| `2026-09-2x-video-01` | VIDEO | `video/`, `coordination/handoffs/video/` | DR-11, DR-12 (script) |

**Integrator: throughout.**
- Create job cards and `lanes.json` entries for the new lanes.
- Ask Levi the §8 questions.
- DR-13 to DR-16.
- Update Gemini script defaults (U-4).
- Add new prose to `verification/artifacts.json`.
- Compile, then run rate-limited reviews.
- Update `wiki/log.md`.

**Blocked on Levi:** DR-08 (toy demo lane `demo/`, `S-DEMO-`/`C-DEMO-`).

The coordination README notes a four-agent session limit. Run the waves in sequence if needed.

---

## 8. Questions requiring Levi (collect answers before or at the start of work)

1. **DR-13:** Commit the current untracked project state now, as a pre-restructure snapshot?
2. **DR-08:** Build a runnable toy vision → control demo as the P5 centerpiece?
3. **DR-11:** Video as a 3–4 episode series (recommended), or one 12–15 min flagship? Is the 31–34 min plan superseded?
4. **DR-06 / D-008:** Add EU/UNECE road regulation, at least as a comparison row?
5. **DR-16:** Release before ED-324's target date with an update plan, or time the release to its publication?
6. **DR-15:** Confirm that U-1 replaces D-003's framing as the controlling purpose.

---

## 9. Follow-up review plan (what the reviewer will check)

1. Recompute the §10 hashes and diff the whitepaper heading list against DR-09.
2. For each DR, check the "Done when" boxes against the named files and sections. Read your handoff's per-DR status table.
3. Re-run the §10 metric commands (negation density, standards mentions, "propos*" count, compiler summary).
4. Verify that every new factual sentence about a paywalled standard is claim-tagged, and that its source record points to a public document with the access boundary recorded.
5. Spot-check 5 new claims against their source context.
6. Render the changed figures and inspect them.
7. Run `python3 autonomous_systems_assurance/verification/compile.py` and compare its summary with the §10 baseline. Expect `planned_reviews` to rise and passing packages to become stale after major prose changes; that is not a regression.
8. Optionally, re-run the same Gemini 3.8 Flash (high) audience review on the new text for a before/after comparison.

---

## 10. Baseline record (2026-09-25T12:03-07:00, HEAD 62f05a4, dirty workspace)

**SHA-256, paths relative to `autonomous_systems_assurance/`:**

```text
9e66223562e2784e5c75651f40d603cfa2dae0a01172545417c94c3de9726092 resource_composition/whitepaper.md
8f1744984b8894d2ff183faeb616f6c65c4787b576e3c0a01fd3c0b1ef780038 resource_composition/whitepaper_outline.md
c4fb6d6dacaa9ab568dfd73602056fb6f37ab3d0e76c0029490dc0bffb16b90e video/script.md
2862cbb603f970d3b9a2727423addf4cbd42f83a3900559faeb14394b58be946 video/nextgen_structure/treatment.md
adeaff4b4b1a5cc618702c6d179c7b70e230a57e69ea01c0483ba9c86d7d3214 video/nextgen_structure/script_outline.md
16d46f5f19d169c88f371d6bfd2b9302ad8b343c2f37263d75391a7499ec0ec2 PROJECT_BRIEF.md
e710df16a832f9f0dcf90a67bcf944c6f8192e68fe36af61722d30a239f584d6 planning/decisions.md
7526c4493279afbcf6b8c1878167a8fe2703a3243dd92307da7bfa8404a8f341 assurance/assurance_case.json
25bc9e58ad85a921279394b76d3f1880e9cadbe76b851e25b050b000af4f6596 assurance/architecture.md
d2a5506c6e2c5a28574e1f02ec2c843123b57c256d1fcb51fde20bd4d31fae1e assurance/method_crosswalk.json
df12a3a0aa71bb32805ee2be847594ab1d337ce4254ffa18c35ef8c4d0ea46c7 verification/claims.json
2bc8b7e289d3ecbcb63f54a41a446575097a7304556960c820b0e6d4ce5dc534 research/sources.json
5b252f5e4a90c35ee3bd7431d16771ba448d809448d444a3096c1a79efc28a9d resource_composition/figures/assurance_coverage_map.svg
084463ee96d7fbb393c669704325a607250506b556a6dade95904b8cad99c5b8 resource_composition/figures/assurance_coverage_map.png
21804a013ed8f70a453217730dff720f258384a2587ae20704d2336ac6d3cb46 resource_composition/figures/assurance_shells.svg
7192daff97ef00b3e6e3c5f886cee40719074b468b3dbf657b6fab8e19f51a30 resource_composition/figures/conditional_risk_graph.svg
99c778762761b1e3b35e4d3a74e0458a4f263333fa864a4cff0d6c7fc667806a resource_composition/figures/evidence_bridge_ladder.svg
f696cfc9b8df2b0bf78933ebdc90c4f5352d0d910f127a40d50804ba54654a21 resource_composition/figures/learned_traceability_gap.svg
6ee09648983e64fe906e8043c8fe6e009549f966e4d4371fe372d1da98c1aeb2 resource_composition/figures/vision_training_contract.svg
949a0fcfa6064b9ae3ea2ab0e0d262c3a8c089e9610598faf06da890832cca2f verification/out/nextgen_gemini_audit/20260925T185344Z_audience_structure_gemini-3.8-flash.md
```

**Metrics**, reproducible from `autonomous_systems_assurance/`:

| Metric | Whitepaper | Script |
|---|---:|---:|
| Words (`wc -w`) | 8,731 | 4,987 |
| Negation constructions (command below) | 99 | 64 |
| `propos` occurrences | 49 | 23 |
| Mentions of DO-178 / ISO 26262 / IEC 61508 / ARP4754 / MC/DC / DAL / ASIL | 0 | 0 |
| Mentions of ED-324 / ARP6983 / SOTIF / 21448 | 0 | 0 |

```bash
grep -oiE '\b(is not|are not|does not|do not|not a|not an|not evidence|not proof|not itself|nor)\b' FILE | wc -l
grep -oiE 'propos' FILE | wc -l
```

**Compiler summary** (`python3 autonomous_systems_assurance/verification/compile.py`, run 2026-09-25):
- sources 102, claims 114, artifacts 35;
- planned_reviews 456, current_passing_packages 70, review_records 603, blockers 819;
- worked-case verification coverage 72.8%, automated review coverage 97.1%, human disposition coverage 0.0%;
- composition_release_ready: false.

**Repository state:** `git ls-files autonomous_systems_assurance | wc -l` = 10 (CrossPoint tooling only). Everything else in the project is untracked.

**Web checks performed in this review** (search-result summaries, not captured source records). Each needs a proper source record before use:

| Topic | Source | What was checked |
|---|---|---|
| Model choice | Artificial Analysis, Gemini 3.8 Flash release page; benchlm 3.1 Pro vs 3.8 Flash | Gemini 3.8 Flash vs 3.1 Pro benchmarks |
| ED-324 | EUROCAE "Open Consultation for ED-324"; FAA AI/ML Tech Exchange presentation (Aug 2025, ED-324/ARP6983); ResearchGate "A study of an ACAS-Xu exact implementation using ED-324/ARP6983" | Existence and status of the standard |
| EASA NPA | EASA NPA 2025-07 page and news release | Publication date, comment period, second NPA, AI Act driver |
| Uber | NTSB HAR-19/03 (`ntsb.gov/investigations/AccidentReports/Reports/HAR1903.pdf`) | Timeline and design facts |
| ACAS Xu | Bak & Tran, NFM 2022 (Springer, doi 10.1007/978-3-031-06773-0_15); Katz et al., Reluplex (arXiv 1702.01135) | Titles and the closed-loop result |
| UNECE / EU road | UNECE press release on R157 at 130 km/h; search summary for EU 2022/1426 | Regulation scope and dates |
