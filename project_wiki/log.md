# Project Wiki Log

## [2026-06-25] production | Verification Compiler script and Manim storyboard prototypes

Created `verification_compiler_video/` as the standalone production workspace for the short Verification Compiler explainer. Added a full first-pass script, storyboard, production manifest, human narration/commentary review workflow, shared Manim visual style helpers, and ten rough Manim prototype scenes matching the outline. Rendered all ten low-resolution scene prototypes successfully under the ignored local Manim media directory. Updated the wiki index with the new video workspace.

## [2026-06-23] planning | Verification Compiler first-pass video outline

Used the approved Gemini API path (`models/gemini-3.1-pro-preview`, HIGH thinking) to brainstorm hooks and visuals from `video_production_plan.md`; saved the raw brainstorm under the ignored `representation_transform_visuals/agent_tools/out/` directory. Added `video_outline_first_pass.md` with a recommended 10-minute outline, hook menu, recurring Manim visual motifs, three short-form concepts under 60 seconds, claim-safety rules, and first visuals to prototype. Updated the wiki index.

## [2026-06-23] planning | Verification Compiler video production plan

Added `video_production_plan.md`, a staged production plan for adapting the representation-transform video workflow to the Verification Compiler project. The plan summarizes the first video's development stages from the repo artifacts, then maps them into a second-video workflow: thesis, claim discipline, source pass, visual language, script/article drafting, manifest spine, scratch narration, Manim scenes, review loop, human narration, and final render. Updated the wiki index with the new workflow page.

## [2026-05-20] prototype | Second prototype run — citation resolution fixed, VRM 0.393 → 0.426+ in progress

**Builder fixes** (`verification_prototype/graph/builder.py`):
- Matrix parser updated to handle 6-column format (source_key column extracted)
- `_resolve_source()` replaced with exact `source_key` lookup (slug-normalized); fuzzy match only when source_key absent
- Source extraction now includes `## Useful Claims` section (holds verbatim quotes) alongside Key Ideas / Why It Matters
- Retired matrix rows (status = "retired") now skipped — no CLAIM node or supported-by edge created
- `SOURCE_TO_MARKERS` corrected: VeriGuard slug was `llm-wiki-pattern`, now `llm-veriguard`; Parasuraman/Cummings removed; Mosier/Skitka, overcorrection, Cobleigh added

**Root cause of first run's 0.581 VRM**: All 27 supported-by edges were silently failing (slug mismatch: underscores in source_key vs hyphens in SRC node IDs). First run had 0 citation VQPs evaluated. Second run: 27 citation VQPs + 27 coverage + 1 orphan = 55 total. 8 stale result files from old run also cleared.

**Citation fixes** (source_to_claim_matrix.md):
- LLM overcorrection claim wording corrected: "at higher rates than flagging genuinely incorrect code" → "at higher rates than they miss genuinely non-compliant code"
- Context window claim status set to `retired` (suppresses VQP generation)
- VeriGuard claim reframed: now "Formal verification can be applied as a post-processing layer on LLM-generated code outputs" — matches what VeriGuard actually shows
- "Certification standards define evidence objectives not reviewer identity" cross-standard rows (ISO 26262, IEC 62443, Beningo) reworded to match what those sources actually assert (positive evidence about rigor levels, not the negative assertion about reviewer identity)
- Agent decomposition row replaced: Wei et al. (CoT within one agent — wrong mechanism for VC) → Khot et al. (Decomposed Prompting, arXiv:2210.02406, ICLR 2023) + Reinpold et al. (arXiv:2411.11582, requirements verification accuracy degrades with task count)

**New sources added**:
- `sources/reinpold_requirements_verification.md` — closest empirical precedent to VQP design; F1 0.92→0.81 as requirements per prompt grows 5→20
- `sources/agent_decomposition_literature.md` rewritten — now leads with Khot (correct mechanism: separate calls) not Wei et al.

**PDF improvements** (`whitepaper/build_pdf.py`):
- DIAGRAMS dict updated to use `_rendered.png` variants
- VRM status block added after title (amber, shows last run score + primary issues)
- Section numbers added via `_add_section_numbers()` preprocessing — TOC and body both numbered; "List of Acronyms" unnumbered
- Reporter model string corrected to "Gemini 3.1 Pro Preview (thinking mode)"

**VRM trajectory**: Run 1: 0.581 (inflated — no citation VQPs) → Run 2 post-fix: 0.393 (27 citation VQPs now evaluated, 8 stale results removed = real 0.426) → Run 3 in progress

## [2026-05-19] prototype | Verification Compiler self-referential prototype — Stage 1 complete

Built and ran a full verification compiler prototype applying the VC concept to the whitepaper itself. Gemini 3.1 Pro (HIGH thinking) served as verification agent.

**Prototype components built** (`verification_prototype/`):
- `graph/schema.py` — Node/Edge/Graph dataclasses, JSON serialize/load
- `graph/builder.py` — parses wiki + whitepaper into artifact graph (25 claims, 27 reqs, 34 sections, 18 sources)
- `graph/traverser.py` — deterministic VQP assembly (zero LLM calls): 21 citation + 20 coverage + 1 orphan = 42 VQPs
- `agents/gemini.py` — only file that calls LLM; uses `generate_thinking()` with gemini-3.1-pro-preview HIGH
- `evidence/reporter.py` — computes VRM, generates markdown report
- `run.py` — orchestrator

**Prototype results**: VRM = 0.581 (citation score 0.76, coverage score 0.35). 7/20 requirements missing or partial in whitepaper. 3/5 citation fails are builder artifacts (natural-language source resolution produced wrong source node mappings).

**Architecture discoveries** (see `data/learnings.md`, `data/gemini_architecture_consultation.md`):
- Source resolution requires stable machine-readable IDs (URI_Locator), not prose labels → SourceRegionNode requirement
- VRM formula requires separate PPV/NPV calibration per (Model_ID, Prompt_Version, Task_Type) → ModelAccuracyProfile requirement
- Document-as-AST: technical standards (DO-178C, ICDs) have hierarchical section IDs equivalent to AST boundaries; three tiers of URI_Locator addressing identified
- Three architectural challenges deferred: graph invalidation cascade, multi-unit emergent requirements, retroactive VRM updates

**Wiki updates** (this session):
- `requirements/verification_compiler_requirements.md` — added SourceRegionNode and ModelAccuracyProfile node types; `supports-claim` edge with version hashes; formal VRM formula (REQ-4.2); Section 7 (source region addressing scheme); Section 8 (three deferred architectural challenges); updated Open Questions
- `concepts/verification_compiler.md` — formal VRM formula with PPV/NPV; document-as-AST section with URI_Locator scheme



## [2026-05-18] citation | Rierson Section 9.3 — DO-178C independence definition and tool equivalence pathway

Found the authoritative primary source for the independence argument. Rierson Section 9.3 (p. 188) quotes DO-178C verbatim:

> "independence is achieved when the verification activity is performed by a **person(s)** other than the developer of the item being verified, and **a tool(s) may be used to achieve equivalence to the human verification activity.**"

This resolves the reviewer identity question. DO-178C provides two independence pathways: (1) qualified person, and (2) qualified tool achieving equivalence. Tool equivalence requires DO-330 qualification. The Verification Compiler targets TQL-5 for exactly this reason.

Additional finding: human reviewer qualification in DO-178C is informal — résumés and training history, not a formal process [Rierson lines 3655–3656]. DO-330 tool qualification is comparatively more rigorous.

Independence requirements scale with DAL: DAL A = 25 objectives require independence; DAL B = 13; DAL C/D = none.

**Files updated:**
- `project_wiki/sources/rierson_do178c.md` — added full Key Ideas citations with line numbers and block quotes
- `project_wiki/traceability/source_to_claim_matrix.md` — added two new Rierson rows; annotated Beningo row; marked LLM context window limits citation as retired from whitepaper
- `Introductory_composition.md` — `### Reviewer Qualification and Independence` section rewritten with the DO-178C verbatim quote, DAL scaling table, informal human qualification note, and two-pathway architecture (Stage 1 = person-based; longer term = tool-equivalence pathway for DAL C/D)
- PDFs rebuilt

## [2026-05-18] edit | Comprehensive consistency + cut pass on Introductory_composition.md

480 → 298 lines. All substantive content preserved; draft scaffolding removed.

**Consistency fixes:**
- Code block in "Compound Architecture" section: removed "Specialized tool (static analyzer, model checker)" as reviewer endpoint. Now shows two endpoints only: Human engineer (certification) and LLM model (nightly CI). Added note that tool evidence enters as DAG nodes (see Figure 2).
- "Development-Cycle Confidence Score" → "Verification Readiness Metric (VRM)" throughout. Terminology updated in: section heading, intro thesis, task-accuracy mitigation bullet, worked example summary. VRM framed as development management signal ("is this build ready for human certifiers?"), not a safety claim.
- Context-length degradation bullet: removed "7K tokens" / Liu et al. / Amazon citations (wrong premise — modern frontier models handle large contexts). Replaced with "irrelevant context pollution" framing: bounded queries work because the graph traversal scopes exactly what is logically related, not because of a token limit.
- Reviewer identity: "independence" section completely rewritten as "Reviewer Qualification and Independence." LLMs explicitly do NOT satisfy DO-178C reviewer requirements. LLMs operate as development-cycle pre-screeners (nightly CI). Qualified independent human engineers perform all certification review. Evidence-first presentation and canary queries added as automation bias mitigations.
- Automation bias section: added evidence-first (LLM verdict hidden until human submits) and canary queries (intentionally flawed VQPs injected to validate reviewer attentiveness). Both framed as process assurance requirements.

**Cuts:**
- "## Project Goal" → condensed into "## Motivation" (2 paragraphs)
- "## Agentic Structuring Hypothesis" → removed; content lives in project_wiki/concepts/agentic_structuring.md
- "## Safety-Critical Engineering as a Collaboration System" + "## Measurement and Qualification" → merged into new "## Safety-Critical Verification as a Coordination System" (3 paragraphs)
- Amodei pre-training/evolution paragraph → cut; replaced with 2-sentence adaptability note
- "## Possible Verification-Validation Pipeline" → cut
- "## Research Questions" → cut
- "## Expansion Areas" → cut
- "## Citation Targets" → cut
- "## Draft Thesis" → cut
- Added "## Conclusion and Stage 2 Direction" (replaces scaffolding with actual content)

**PDFs rebuilt:** report 23pp, confpaper 15pp (both in whitepaper/out/)

**Pending (not yet applied from Gemini review):**
- Derived requirements paragraph in Scope section
- Reviewer identity citation in Rierson/DO-178C
- Automation bias literature citation (Parasuraman & Manzey 2010)
- Diagram 4 "Reviewer: NOT SPECIFIED" claim — may overclaim; needs review given user clarification that standards do require qualified human reviewers

## [2026-05-18] review + pdf | Gemini 3.1 Pro round 2 review + wiki audit + PDF layout experiments

**Wiki audit:** All 18 source notes schema-compliant; index matches filesystem; all items in sources_to_extract.md acted upon; 5 recent arXiv URLs still flagged [verify URL] (pre-submission action). Log current.

**Gemini 3.1 Pro review (out/review_3p1pro_round2_2026-05-18.md)** — top 5 priorities identified:
1. Rename "Confidence Score" → "Verification Readiness Metric" (score terminology triggers probabilistic-safety alarm for certifiers)
2. Elevate and mechanize automation bias defense — UI must physically block LLM verdict until human submits independent review; this should be in main body not just Req 6.1
3. Address Derived Requirements — DO-178C certifiers will immediately ask about LLRs that trace up to safety rather than down from HLRs
4. Cut org theory/evolutionary analogies (Mintzberg, Nvidia, Amodei evolution framing) — out of place for DO-178C audience
5. Find and cite the reviewer-identity text from Rierson/DO-178C directly — load-bearing argument needs primary source quote

**Additional Gemini findings:**
- Core TQL-5 framing called "brilliant" and "most defensible regulatory argument currently possible for AI in safety-critical spaces"
- `read_sensor()` worked example called "highly effective"
- AI monoculture (developer uses Copilot, compiler uses same underlying model) needs stronger treatment than current rotating-vendors note
- "Uncertain" result state in dual-mode needs clearer definition (does it trigger immediate human escalation?)
- Automation bias citation needed (Parasuraman & Manzey 2010, or Cummings on human supervisory control)

**Diagram 5 final fix:** Removed specialized tools entirely from reviewer endpoint section. Specialized tools are evidence inputs (shown in Diagram 2), not reviewers. Bottom section now shows DAG node → Query Package → two endpoints only (Human / LLM). Re-rendered.

**PDF layouts built:** `whitepaper/build_pdf.py` — Python/weasyprint pipeline with two CSS layouts:
- `whitepaper/out/whitepaper_report.pdf` — 25 pages, single-column technical report (RTCA/NASA style, Source Serif 4, 11.5pt, 1in margins, navy headers)
- `whitepaper/out/whitepaper_confpaper.pdf` — 17 pages, two-column conference paper (SAE/AIAA/IEEE style, 10pt, 0.875in margins, uppercase section headers)
Both include: title block, abstract, all markdown content, and all 5 figures with captions.
Run: `python3 whitepaper/build_pdf.py --layout both` (or `--layout report` / `--layout confpaper`)

**Pending (next session):** Apply the 5 Gemini review priorities; find Rierson reviewer-identity quote; add Derived Requirements paragraph; automation bias citation.

## [2026-05-18] architecture | Tool qualification analysis + diagram5 correction + DAG invariant

Queried Gemini 2.5 Pro on DO-330 tool qualification requirements; applied findings.

**Key clarifications from analysis:**
- TQL-1 through TQL-5 differentiate by DAL of software AND by whether tool output is human-reviewed. TQL-5 = verification tool whose output is always human-reviewed.
- "Criteria 1" (tool needs no qualification because output is independently verified anyway) probably doesn't apply — if the project plan formally relies on the tool to generate verification evidence, the tool's reliability matters.
- **What gets qualified is the deterministic query generator and evidence packager, not the LLM.** The LLM is a non-qualified feature outside the certification workflow. This is the core argument for TQL-5.
- TQL-5 requires: TQP, TOR, functional validation tests on deterministic components, configuration management records, TAS.
- **Automation bias** is the strongest regulatory counterargument: human reviewers primed by LLM "pass" verdicts may review less rigorously. Architecture already has components to address it (accuracy profiles, conflict tracking); needs explicit process-level response.

**Files changed:**
- `Introductory_composition.md` — Regulatory Pathway section rewritten with four subsections: what qualifies vs. what does not; TQL-5 actual requirements; automation bias concern; regulatory environment
- `requirements/verification_compiler_requirements.md` — Added Req 1.3 DAG Structure Invariant (cycles forbidden, detected at construction time; required for deterministic traversal); added Section 6 Process Assurance Requirements (Req 6.1 Automation Bias Mitigation — full evidence before LLM verdict, disagreement rate reporting, no opaque aggregate score)
- `whitepaper/render_diagrams.py` — diagram5 rewritten: removed Specialized Tool as reviewer endpoint (it is an evidence node input, not a reviewer); 2 columns only (Human, LLM); specialized tools shown via dashed arrow into DAG node; DAG note added; independence/model-diversity annotations corrected
- `whitepaper/diagram5_rendered.png` — re-rendered with corrected design (500K)
- `whitepaper/diagram_specs/diagram5_spec.txt` — updated to match corrected design

**Independence framing corrected in `Introductory_composition.md`:** rotating vendors is NOT independence, it is an engineering quality benefit (multiple training sets must concur before human review time is spent). Independence is satisfied by the human final pass only.

## [2026-05-18] architecture | Review feedback cycle 2 — independence, UoI framing, requirements

Applied six pending items from prior Gemini review + user direction:

1. **Development-cycle confidence score** — rewrote section to separate developmental metric (LLM mode, cannot reach 100%) from certification evidence (human mode, binary). Both exist as structurally separate outputs of the same system.

2. **Independence subsection** — added `### Independence` to `Introductory_composition.md` under LLM Reliability section. Argues: (a) certification independence = human final pass satisfies DO-178C; (b) development independence = model has no shared cognitive history with developer; (c) model diversity during nightly CI (different vendors = different training data, architecture) provides additional reviewer independence analogous to multiple review teams.

3. **Units of Intelligence framing strengthened** — added `### LLMs as a New Category — Not DO-330 Tools` and `### The Compound Architecture and Endpoint Replaceability` subsections to `Introductory_composition.md`. Key point: LLMs were not designed to meet DO-330 constraints; they are a new category of unit of intelligence. The compound architecture addresses this by making each reviewer position an endpoint that accepts human, LLM, or tool — with human as the certification endpoint by design.

4. **Prompt configuration control (Req 3.5)** — added to `verification_compiler_requirements.md`. Prompts are versioned configuration data; every review result must record prompt version alongside model identifier; in-place prompt editing not permitted; historical queries must be reproducible from artifact graph state + code version + prompt version.

5. **Stage 1 scope** — renamed `### Scope: Non-Functional Requirements` to `### Scope: Stage 1 Trace Boundaries`. Explicitly scoped Stage 1 to LLR-to-Code and Code-to-Test traces. HLR-to-LLR consistency is Stage 2. Added rationale for why LLR is the right boundary.

6. **Diagram 5 — Units of Intelligence** — new matplotlib wireframe (`diagram5_units_of_intelligence.png`, 311K) and Nano Banana Pro render (`diagram5_rendered.png`, 500K). Shows property comparison table (Human / LLM / Specialized Tool × Capacity / Accuracy / Adaptability / Qualification / Certification Role) plus compound architecture endpoint replaceability diagram. Spec: `diagram_specs/diagram5_spec.txt`. `render_all_diagrams.sh` updated to include diagram5.

## [2026-05-18] update | Source schema compliance + regulatory source correction

Rewrote four source notes to conform to project wiki schema (Source, Why It Matters, Key Ideas, Useful Claims, Requirements Impact, Follow-Up Questions):
- sources/requirements_engineering_nl_ambiguity.md
- sources/mintzberg_org_structure.md
- sources/nvidia_management_structure.md
- sources/regulatory_ai_aviation_automotive.md

Key correction: regulatory AI sources (EASA, FAA, ISO/PAS 8800) were initially framed as supporting the "reviewer identity" claim but are actually about certifying AI/ML systems themselves (learning assurance for neural network weights), not about using AI as a verification tool for conventional C code. Source note updated to reflect correct limited relevance: background context only, not direct support. Source_to_claim_matrix row updated accordingly.

Corrected non-determinism treatment in requirements and whitepaper: removed temperature=0 as the primary mitigation; replaced with the correct architectural argument — the graph decomposition is deterministic, LLM results are classified as developmental (not certification evidence), and the final certification pass is always human. DO-330 concern is addressed by the architecture, not by trying to make LLMs deterministic.

Regulatory Pathway section in Introductory_composition.md updated: removed overclaimed EASA/FAA citations; DO-330 TQL-5 is the correct and sole regulatory pathway.

## [2026-04-26] ingest | LLM wiki pattern

Created the project wiki schema, index, log, and first source note based on the saved `llm-wiki.md` source.

## [2026-04-29] ingest | Rierson traceability prototype

Created Graphify-compatible repository structure notes, a Graphify workflow, Rierson source note, initial concept pages, claim pages, requirement pages, and traceability registries. Promoted five Rierson-derived candidate links for traceability, verification-as-evidence, and model/tool qualification claims.

## [2026-05-17] diagrams | Whitepaper visualizations

Created four Excalidraw diagrams and saved to whitepaper/diagrams.md with checkpoint IDs:
1. Artifact Graph (checkpoint 24df162c861a4a948d) — hierarchical C codebase linked to all verification artifacts
2. Verification Query Assembly (c48b56825f8e4537a2) — traversal collects one code unit's full context into a bounded query
3. Dual-Mode Operation (7abcccf0c8aa4ec9bc) — LLM and human review are interchangeable on the same decomposition
4. Cross-Standard Evidence Structure (b02a1cdf1520465682) — DO-178C/ISO 26262/IEC 62443 all define evidence objectives but not reviewer identity
Created whitepaper/ folder. Remaining diagrams to add: units of intelligence comparison, confidence score formula, pipeline overview.

## [2026-05-17] ingest | Agent-side literature sources

Processed background search results. Created four source notes: llm_context_window_limits.md (Lost in the Middle, Context Length Alone Hurts), llm_task_specific_accuracy.md (MMLU-Pro, SWE-bench/HumanEval gap, bug detection), agent_decomposition_literature.md (Chain-of-Thought, VeriGuard, formal verification papers), amodei_adaptability.md (Dwarkesh interview — pre-training as evolution, in-context adaptability). Updated source_to_claim_matrix with 4 new claim rows. All 2025 arXiv URLs flagged [verify URL] — confirm before final citation. High-confidence sources: arXiv:2307.03172, arXiv:2406.01574, arXiv:2201.11903, dwarkesh.com/p/dario-amodei-2.

## [2026-05-17] architecture | Verification compiler concrete design

Captured concrete architecture description from user discussion. Updated Introductory_composition.md verification compiler section with graph-based design. Created three missing concept pages: units_of_intelligence.md, verification_compiler.md, agentic_structuring.md. Key clarifications added:
- Context window is a design primitive (unit of work), not merely a limitation
- Dual-mode operation: LLM and human use identical graph decomposition, interchangeable per node
- Confidence score is composite: per-query result × model accuracy profile × coverage × evidence staleness
- Provable decomposition: graph structure itself proves evaluation scope completeness
- Agentic structuring / hierarchy analogy is conceptual background, not the compiler's internal design
- Model accuracy profiles are a system component (input to confidence score), not just a research question

## [2026-05-17] ingest | Counterargument and new standards sources

Added Beningo LinkedIn post (embedded software moats counterargument) and public proxy sources for ISO 26262 (NHTSA/Volpe assessments) and IEC 62443 (CISA CPG, NIST SP 800-82). Key insight: all three major safety standards (DO-178C, ISO 26262, IEC 62443) define evidence objectives and tiered levels but do not specify reviewer identity — this is the structural basis for the certification-moat counterargument.

## [2026-05-17] refactor | Rename validation→verification compiler

Renamed "Validation Compiler" → "Verification Compiler" across all working files (~40 files).
Reason: DO-178C terminology — verification = "built it right"; validation = "built the right thing". The system does verification; the old name would alienate certifiers.
Old files deleted; new: project_wiki/concepts/verification_compiler.md, requirements/verification_compiler_requirements.md.

## [2026-05-17] whitepaper | Concrete example + non-determinism requirement

Added "Worked Example" section — complete walkthrough of read_sensor() through the compiler: artifact graph fragment, full verification query text (~1.2K tokens), structured JSON result.
Added Requirement 3.3b Non-Determinism Handling — temperature=0, immutable logs, flag probabilistic results in evidence packages. Addresses DO-330 scrutiny.
Condensed "Agentic Structuring Hypothesis" — removed Nvidia/Mintzberg deep-dive, kept 3-sentence motivating point.

## [2026-05-17] diagrams | Nano Banana rendered diagram set

Rendered all 4 whitepaper diagrams via Nano Banana Pro (models/nano-banana-pro-preview):
- diagram1_rendered.png (492K) — Artifact Graph
- diagram2_rendered.png (474K) — Verification Query Assembly
- diagram3_rendered.png (313K) — Dual-Mode Operation
- diagram4_rendered.png (651K) — Cross-Standard Evidence Structure

Captured regeneration workflow:
- Spec files: whitepaper/diagram_specs/diagram{1-4}_spec.txt — edit these to change diagram content
- Render script: whitepaper/render_all_diagrams.sh — reruns all 4 via Gemini API
- Per-diagram render: whitepaper/gemini_tools/diagram_render.py --wireframe ... --spec-file ... --out ...

## [2026-05-17] ingest | Requirements engineering and org theory sources

Found and created source notes for all 3 previously-uncited claims:
1. NL spec ambiguity: Zave & Jackson (1997) TOSEM DOI:10.1145/237432.237434 + Davis (1993) — HIGH confidence peer-reviewed
2. Org theory span of control: Mintzberg (1979) The Structuring of Organizations — canonical organizational theory, HIGH confidence
3. Nvidia management span: Fortune Nov 12, 2024 (Jensen Huang ~60 direct reports) — HIGH confidence journalistic

Updated source_to_claim_matrix.md — all **uncited** rows now have sources.
Updated Introductory_composition.md — citation placeholders replaced with real citations.
Citation Targets section updated to reflect resolved vs. still-needed citations.

## [2026-05-17] tooling | Gemini API tools + whitepaper refinement

Built `whitepaper/gemini_tools/` with three scripts:
- `gemini_client.py` — shared REST helpers for text and image generation
- `whitepaper_review.py` — bundles whitepaper + wiki pages and submits to Gemini for structured critique
- `diagram_render.py` — sends matplotlib wireframe PNG + text spec to Nano Banana Pro image model for polished renders

Available models confirmed live: gemini-2.5-pro, gemini-2.5-flash, nano-banana-pro-preview, gemini-3.1-flash-image-preview, deep-research-max-preview-04-2026, imagen-4.0-generate-001. API key in the user credential store (~/.config/video-pipeline/credentials.env).

Generated first structured Gemini review (gemini_tools/out/review_2026-05-17.md). Top 5 gaps identified and addressed:
1. Added Introduction section to Introductory_composition.md with thesis roadmap, section map, and upfront LLM-trust acknowledgment
2. Added Terminology Note section defining model unit / unit of intelligence / agent consistently
3. Added "LLM Reliability and the Mitigation Architecture" subsection — maps each LLM failure mode (hallucination, context degradation, accuracy variance, opacity, no memory) to a specific architectural response
4. Added "Regulatory Pathway" subsection — DO-330 tool qualification pathway, pre-review use case, cross-standard evidence argument
5. Added Requirement 3.4 (Conflict Resolution) to verification_compiler_requirements.md — human result takes precedence, disagreement flagged for model accuracy profile recalibration
6. Added Amodei citation (Dwarkesh 2025) to Units of Intelligence section replacing the earlier placeholder
7. Added citation placeholders in source_to_claim_matrix.md for three **uncited** claims: NL spec problems, org theory span-of-control, Nvidia management structure

## [2026-04-29] ingest | Public assurance source expansion

Captured public FAA and NASA PDFs, converted them with `pdftotext`, added source notes for FAA AC 20-115D, NASA Jacklin DO-178C/DO-278A, NASA-STD-8739.8B, NPR 7150.2D, and public AS9100 references. Updated concept, claim, requirement, and traceability pages with candidate links for DO-178C public summaries, NASA software assurance directives, and AS9100 quality-management references.
