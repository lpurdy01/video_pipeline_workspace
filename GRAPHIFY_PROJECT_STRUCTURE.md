# Graphify-Compatible Project Structure

## Purpose

This repository should support two related workflows:

- **Graphify corpus workflow:** generate exploratory concept, source, and relationship graphs from curated source material.
- **Project wiki workflow:** promote useful graph findings into verified, citation-ready source notes, claims, requirements, and traceability records.

Graphify can discover candidate relationships. The project wiki is the maintained knowledge base that decides which relationships are valid enough to cite or use in the whitepaper.

## Recommended Shape

```text
graphify-corpus/
  README.md
  sources/
    web/
    papers/
    standards/
    books/
  working_notes/
    prompts/
    graphify_run_notes.md

graphify-out/
  graph.json
  graph.html
  GRAPH_REPORT.md
  cost.json
  cache/

project_wiki/
  PROJECT_WIKI_SCHEMA.md
  graphify_workflow.md
  index.md
  log.md
  sources/
    rierson_do178c.md
    llm_wiki_pattern.md
  concepts/
    safety_critical_traceability.md
    verification_as_evidence_production.md
    model_or_tool_qualification.md
  claims/
    safety_critical_verification_depends_on_traceability.md
    verification_requires_review_analysis_and_test.md
    model_units_need_task_specific_qualification.md
  requirements/
    traceability_link_requirements.md
    evidence_and_auditability_requirements.md
  traceability/
    link_registry.md
    source_to_claim_matrix.md

refrence_literature/
  sources_to_extract.md
  raw/
    web_clips/
    pdfs/
    extracted_markdown/
  source_notes/
```

## Corpus Rules

Graphify should run on a curated folder or with `.graphifyignore` active. Avoid feeding duplicate forms of the same source into a single run, such as both a PDF and its extracted Markdown.

The current first-pass corpus should include:

- `WHITEPAPER_STAGE_1_STRUCTURE.md`
- `project_wiki/`
- extracted Markdown source texts that are being actively mapped

The first-pass corpus should exclude:

- `graphify-out/`
- `.git/`, `.codex/`, virtual environments, caches
- duplicate PDFs when extracted Markdown is available
- abandoned draft variants unless the question is specifically about draft evolution

## Link Validity Convention

Graphify edges are candidate links. A candidate link becomes a project traceability link only when it has:

- a stable local link id
- source node and target node
- relation type
- evidence location
- short rationale
- status

Use `project_wiki/traceability/link_registry.md` as the promoted-link ledger.

## Suggested Run Pattern

```bash
python3 -m venv .venv-graphify
.venv-graphify/bin/pip install graphifyy
.venv-graphify/bin/graphify install --platform codex
```

Then invoke the Graphify skill on the curated corpus. Review generated graph relationships before promoting them into `project_wiki/traceability/link_registry.md`.
