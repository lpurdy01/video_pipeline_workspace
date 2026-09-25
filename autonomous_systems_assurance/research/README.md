# Research workflow

[`sources.json`](sources.json) is the structured source register. [`initial_findings.md`](initial_findings.md) is the first synthesis; [`questions.md`](questions.md) is the research agenda. Claims and open challenges live in [`../verification/claims.json`](../verification/claims.json).

For each source, record stable ID, publisher, URL, publication date (null when unknown), access date, jurisdiction, authority/type, actual inspection scope, source regions and limits. A public abstract supports only its scope; a failed PDF fetch is not a review of that PDF.

Current regions contain short inspected excerpts and locators. They are retrieval anchors, not context-complete evidence packets. Full source snapshots and their hashes are deliberately unset until actually captured. The compiler treats that as unfinished work.

Ingest:

1. Retrieve the primary source, identify edition/date and preserve permitted full material under `out/sources/`.
2. Extract relevant passages with surrounding qualifications, locators and source-file SHA-256. Preserve source text; write interpretation separately.
3. Update the register, claim evidence edges and wiki synthesis, including conflicting evidence.
4. Compile review packages; inspect the original context during review.
5. Record reviewer identity, task, exact input digest, result, limits and human disposition.
6. Recompile and examine downstream changes to the paper, narration, figures and release.

Do not count syndicated reporting or multiple pages repeating a vendor announcement as independent corroboration. An authority is primary for its decision; the vendor may be primary for what it says it built. Neither alone establishes the other's claim.

Use public publisher scopes for licensed standards until authorized texts are available. Reference downloads remain local and are not automatically included in the public resource export.
