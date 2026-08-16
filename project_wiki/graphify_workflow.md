# Graphify Workflow

## Purpose

Graphify is an exploratory graph tool for finding candidate relationships across source material, wiki notes, claims, and requirements. It is useful for discovering clusters and possible cross-references.

Graphify output is not automatically citation-ready. The project wiki promotes only reviewed relationships into traceability records.

## Workflow

1. Select a bounded corpus.
2. Run Graphify with duplicate and generated files excluded.
3. Read `graphify-out/GRAPH_REPORT.md` for clusters, high-degree nodes, and surprising connections.
4. Inspect `graphify-out/graph.json` for candidate edges.
5. Promote useful candidate edges into `project_wiki/traceability/link_registry.md`.
6. Update affected source notes, concept pages, claim pages, requirement pages, and `project_wiki/index.md`.
7. Append a log entry.

## Promotion Criteria

A Graphify edge should be promoted only if it has:

- a source location that can be checked
- a clear relation type
- a target claim, concept, requirement, or source note
- enough rationale to survive later review

Candidate links should remain marked `candidate` until a human or a later review pass verifies the evidence.

## Relationship Statuses

- `candidate`: discovered by Graphify or Codex, not yet reviewed.
- `verified`: evidence location and rationale have been checked.
- `rejected`: relationship was inspected and found misleading, unsupported, or too vague.

## Link ID Pattern

Use stable IDs:

```text
link_<source_slug>__<relation>__<target_slug>__NNN
```

Example:

```text
link_rierson_ch6_traceability__supports__claim_safety_traceability__001
```
