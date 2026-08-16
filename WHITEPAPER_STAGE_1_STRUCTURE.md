# Stage 1 Whitepaper Structure

## Purpose

Stage 1 is for gathering enough source material and organizing the project's concepts well enough to produce a requirements-oriented whitepaper.

The goal is not to write the final whitepaper immediately. The goal is to build a working research scaffold:

- collect relevant source material
- extract and summarize sources into manageable notes
- define the core thesis
- identify claims that need evidence
- organize requirements for a verification compiler
- decide what must be demonstrated in later stages

## Current Source Status

The local `llm-wiki.md` file has been saved and can now be used as a source for the research workflow itself. Its main contribution is the idea that raw sources should not be treated as the working knowledge base. Instead, the project should maintain a persistent, LLM-maintained wiki of extracted concepts, source notes, claim maps, contradictions, and evolving synthesis.

The Rierson safety-critical software book has been extracted to Markdown and can support the DO-178C, verification, validation, traceability, and process-assurance side of the whitepaper.

## Adopted Knowledge-Base Pattern

The LLM wiki source suggests a useful three-layer structure:

- **Raw sources:** immutable documents, PDFs, web clippings, extracted Markdown, and source snapshots. These are the source of truth and should not be rewritten by the agent.
- **Working wiki:** LLM-maintained Markdown pages that synthesize raw sources into concepts, claims, source notes, comparisons, requirements, and open questions.
- **Schema:** a small instruction document that defines page types, metadata, ingest workflow, logging conventions, citation expectations, and maintenance rules.

For this project, the working wiki should not merely summarize sources. It should compile the research into whitepaper-ready artifacts:

- concept pages
- source notes
- claim pages
- requirement pages
- contradiction or uncertainty notes
- traceability maps from claim to source
- whitepaper outline sections

The important shift is that each new source should update persistent project knowledge. We should avoid repeatedly rediscovering the same facts from raw documents.

## Working Whitepaper Thesis

Safety-critical software engineering can be understood as a disciplined collaboration system for limited units of intelligence. Modern agent systems introduce new units of intelligence with different strengths and failure modes. If these units are structured, qualified, delegated, and reviewed according to principles drawn from safety-critical engineering, they may become useful participants in verification and validation workflows.

The long-term artifact is a verification compiler: a system that decomposes requirements into traceable units, delegates bounded verification tasks to qualified model units, validates implementation artifacts against those requirements, and packages evidence for human review.

## Proposed Working Structure

### 1. Problem and Motivation

This section explains why safety-critical software verification is expensive, why natural-language requirements are difficult to validate against implementation, and why agent systems are worth studying.

Questions to answer:

- Where does human verification time go?
- Which verification tasks are tedious but necessary?
- Why are English-language specifications difficult to use as precise software contracts?
- Why are current LLM/agent systems interesting but insufficient by themselves?

Source needs:

- DO-178C or secondary explanations of verification objectives
- safety-critical software development process descriptions
- requirements engineering literature on ambiguity and traceability
- LLM/agent literature on context limits, hallucination, reliability, and tool use

### 2. Units of Intelligence

This section defines humans, individual models, tools, agents, review boards, and organizations as units of intelligence with measurable limits and qualifications.

Concepts to develop:

- capacity
- accuracy
- adaptability
- specialization
- reviewability
- qualification
- context limits
- task-specific competence

Source needs:

- LLM overview material such as the Karpathy LLM wiki
- model evaluation and benchmark material
- agent reliability and task decomposition sources
- organizational theory or engineering management sources

### 3. Agentic Structuring

This section explains why systems of specialized units may outperform a single general unit, especially when work can be decomposed and reviewed.

Concepts to develop:

- hierarchy
- delegation
- specialization
- independent review
- manager/reviewer/worker patterns
- flatter innovation-oriented structures versus verification-heavy structures
- communication costs and failure modes

Source needs:

- multi-agent collaboration literature
- agent decomposition papers or engineering reports
- organizational structure sources
- evidence or credible reporting on Nvidia-style management span, if used

### 4. Safety-Critical Engineering as an Existing Coordination Pattern

This section treats safety-critical engineering standards as mature patterns for coordinating human units of intelligence.

Concepts to develop:

- verification and validation
- traceability
- configuration control
- issue tracking
- process assurance
- independence
- review boards and approval gates
- Design Assurance Level rigor scaling

Source needs:

- Rierson extracted Markdown
- DO-178C summaries and official or authoritative secondary sources
  - Captured: FAA AC 20-115D, public FAA recognition of DO-178C/DO-330 and related supplements.
  - Captured: NASA NTRS Jacklin paper summarizing DO-178C, DO-278A, DO-330, and related supplements.
  - Constraint: DO-178C and companion RTCA documents remain licensed; use public FAA/NASA sources unless licensed access is provided.
- NASA software assurance directives
  - Captured: NASA-STD-8739.8B, Software Assurance and Software Safety Standard.
  - Captured: NPR 7150.2D, NASA Software Engineering Requirements.
- AS9100 quality management references
  - Captured as public references only: IAQG 9100 overview, SAE AS9100D metadata, and NASA SMA article on AS9100/IA9100.
  - Constraint: AS9100D itself is licensed; do not quote or depend on full standard text without licensed access.

### 5. Qualification of Model Units

This section asks what it would mean for a model or agent system to be qualified for delegated safety-critical verification tasks.

Concepts to develop:

- task-specific qualification
- prompt and context qualification
- toolchain qualification
- reproducibility
- audit logs
- human review gates
- independent model challenge
- evidence attached to claims

Source needs:

- tool qualification concepts from DO-178C or DO-330
- LLM evaluation literature
- AI assurance and model governance sources
- software assurance sources on evidence and auditability

### 6. Verification Compiler Concept

This section defines the proposed system architecture.

Possible components:

- specification intake
- requirement atomization
- traceability tree construction
- implementation analysis
- delegated verification tasks
- independent review
- uncertainty reporting
- evidence packaging
- requirements database
- audit trail

Source needs:

- traceability and requirements management literature
- safety-critical verification process sources
- LLM tool-use and structured-output sources
- software analysis and testing sources

### 7. Requirements for the Stage 2 Prototype

This section translates the whitepaper into requirements for later implementation.

Requirement categories:

- source ingestion requirements
- requirement extraction requirements
- traceability requirements
- agent delegation requirements
- evidence requirements
- auditability requirements
- human review requirements
- evaluation requirements
- non-goals and boundaries

## Source Processing Workflow

Each source should move through these states:

1. **Identified:** the source is listed, with URL or local path.
2. **Captured:** the source has been downloaded or extracted to local text/Markdown.
3. **Indexed:** basic metadata and relevant sections are identified.
4. **Selective summary:** only relevant sections are summarized.
5. **Claim mapping:** source material is linked to project claims.
6. **Requirements impact:** source material is translated into system requirements or design constraints.

The LLM wiki pattern adds two maintenance operations:

7. **Wiki update:** concept pages, claim maps, source notes, and requirement pages are updated.
8. **Lint:** periodically check for stale claims, contradictions, orphan notes, missing source links, and concepts that deserve their own pages.

## Recommended Repository Shape

```text
refrence_literature/
  sources_to_extract.md
  raw/
    web_clips/
    pdfs/
    extracted_markdown/
  source_notes/
    llm_wiki_notes.md
    rierson_do178c_notes.md
    nasa_software_assurance_notes.md
    as9100_notes.md
    agent_decomposition_notes.md
  claim_maps/
    claims_needing_sources.md
    source_to_claim_matrix.md
project_wiki/
  PROJECT_WIKI_SCHEMA.md
  index.md
  log.md
  concepts/
    units_of_intelligence.md
    verification_compiler.md
    agentic_structuring.md
    natural_language_specifications.md
  claims/
    claim_agent_decomposition.md
    claim_safety_traceability.md
  requirements/
    verification_compiler_requirements.md
whitepaper/
  outline.md
  requirements.md
  glossary.md
  draft.md
```

The repository does not need every file immediately, but this gives the project a place to put different kinds of thought without mixing raw extraction, source notes, claims, and final prose.

## Immediate Next Tasks

- Fill `sources_to_extract.md` with source candidates.
- Create a project wiki schema based on the LLM wiki pattern.
- Create `index.md` and `log.md` for the project wiki.
- Create a selective note for the saved LLM wiki source.
- Create selective notes from the Rierson extraction instead of ingesting the whole book.
- Build a `claims_needing_sources.md` list from `Introductory_composition_full.md`.
- Start a whitepaper outline that separates claims, evidence, and requirements.
