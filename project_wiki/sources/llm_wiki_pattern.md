# LLM Wiki Pattern

## Provenance

raw_file: refrence_literature/Dev_Safety-Critical_Software/karpathy_llm_wiki/llm-wiki.md
raw_url: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
summary_method: llm-extract-from-raw
summary_verified: false

## Source

Local path: `refrence_literature/Dev_Safety-Critical_Software/karpathy_llm_wiki/llm-wiki.md`

Original source listed in file: `https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f`

## Why It Matters

This source gives Stage 1 a working research-management pattern. Instead of treating source gathering as a pile of documents plus ad hoc chats, it recommends a persistent wiki maintained by an LLM. That fits this project because the whitepaper will require accumulating evidence, linking claims to sources, identifying contradictions, and gradually turning research into requirements.

## Key Ideas

- Raw documents should remain separate from synthesized working knowledge.
- The LLM should incrementally maintain a Markdown wiki as new sources arrive.
- The wiki should include cross-references, summaries, entity or concept pages, contradictions, and evolving synthesis.
- A schema document should define conventions so the LLM behaves like a disciplined maintainer.
- The knowledge base should have an `index.md` for content navigation and a `log.md` for chronological maintenance history.
- Useful answers, comparisons, and analyses should be filed back into the wiki instead of disappearing into chat history.
- Periodic linting should identify stale claims, contradictions, orphan pages, missing cross-references, and source gaps.

## Useful Claims

- A persistent wiki lets project knowledge compound across sources.
- Raw retrieval alone can force the model to rediscover synthesis on every query.
- LLMs are well suited to the bookkeeping work of maintaining summaries, links, and consistency.
- Humans should curate sources, direct analysis, ask questions, and review outputs.
- The schema is the key control surface for making an LLM-maintained wiki reliable.

## Requirements Impact

- The project should separate raw sources from maintained synthesis.
- The repository should include a project wiki schema.
- Every ingest should update source notes, concept pages, claim pages, requirements, index, and log as appropriate.
- The whitepaper workflow should include periodic wiki linting.
- Source notes should be selective and claim-oriented, not full-document dumps.

## Follow-Up Questions

- What metadata should each source note include for citation and auditability?
- Should claims be represented as individual pages, a matrix, or both?
- How formal should requirement pages become before Stage 2?
- At what scale will simple `rg`/index navigation stop being enough?
