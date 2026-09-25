# Review prototype

`index.html` is the reader-facing, self-contained review edition of the current whitepaper. It has a linked table of contents, expandable source cards, claim-tag links, and print styling. `out/autonomous_assurance_whitepaper_review.pdf` is the corresponding paginated snapshot.

The renderer also appends a compiler-derived **Current compiler status** panel. It is generated from the current graph and overrides static count snapshots in the manuscript when they age; it remains a gate-completion display, not a safety score.

Regenerate both after editing `../whitepaper.md`:

```bash
./render.sh
```

The HTML is a review artifact, not a release claim. Claim tags link to static source cards with the source and scope notes used by this reader draft; consult the generated compiler report for the live review queue. The PDF retains source-card and external-source hyperlinks.
