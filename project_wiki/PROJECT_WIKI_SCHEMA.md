# Project Wiki Schema

## Purpose

This wiki is the maintained knowledge layer for the verification compiler whitepaper. Raw sources stay in `refrence_literature/`; this wiki contains synthesized, cross-linked, selectively sourced project knowledge.

The wiki should compound over time. New sources should update existing concept pages, claim pages, requirement pages, and source notes rather than creating disconnected summaries.

## Layers

- **Raw sources:** source PDFs, extracted Markdown, web clips, and source URLs. These are immutable or minimally edited.
- **Project wiki:** maintained synthesis pages written and updated by the LLM with human direction.
- **Whitepaper artifacts:** polished outline, requirements, glossary, and draft prose derived from the wiki.

## Page Types

### Source Notes

Location: `project_wiki/sources/`

Purpose: summarize one source selectively, with emphasis on claims relevant to the whitepaper.

Required sections:

- Source
- Why It Matters
- Key Ideas
- Useful Claims
- Requirements Impact
- Follow-Up Questions

### Concept Pages

Location: `project_wiki/concepts/`

Purpose: maintain evolving explanations of core project concepts.

Required sections:

- Definition
- Why It Matters
- Related Claims
- Source Support
- Open Questions

### Claim Pages

Location: `project_wiki/claims/`

Purpose: track whitepaper claims and what evidence supports or challenges them.

Required sections:

- Claim
- Status
- Supporting Sources
- Challenges or Uncertainty
- Whitepaper Use

### Requirement Pages

Location: `project_wiki/requirements/`

Purpose: translate research into requirements for the verification compiler or stage-2 prototype.

Required sections:

- Requirement
- Rationale
- Source Support
- Verification Method
- Open Questions

## Index Rules

`project_wiki/index.md` is the content-oriented map of the wiki. It should list every maintained wiki page with a one-line description and category.

Update it whenever a wiki page is added, renamed, or substantially changed.

## Log Rules

`project_wiki/log.md` is chronological and append-only. Each entry should begin with:

```text
## [YYYY-MM-DD] action | title
```

Use actions such as:

- `ingest`
- `update`
- `query`
- `lint`
- `decision`

## Ingest Workflow

When ingesting a source:

1. Read only the relevant source sections needed for the task.
2. Create or update a source note.
3. Update affected concept pages.
4. Update affected claim pages.
5. Add requirements impact when the source implies design constraints.
6. Update `index.md`.
7. Append an entry to `log.md`.

## Maintenance Workflow

Periodically lint the wiki for:

- stale claims
- unsupported claims
- contradictions between pages
- missing links between concepts and claims
- concepts mentioned repeatedly but lacking a page
- requirements without source support
- orphan source notes

## Citation Expectations

Source notes should point to the source path or URL. When possible, include page, section, or heading references. Avoid copying large passages into the wiki; summarize and cite instead.
