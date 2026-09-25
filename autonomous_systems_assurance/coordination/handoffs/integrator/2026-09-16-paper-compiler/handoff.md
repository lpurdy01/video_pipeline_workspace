# Handoff: paper-compiler / 2026-09-16

- Author/session and role: `paper_compiler_review` agent; independent compiler-integration audit.
- Date/time with timezone: 2026-09-16, America/Phoenix.
- Job card: parent request to audit the reader-facing whitepaper/prototype integration. The auditor did not edit `artifacts.json`, manuscript, prototype, source registry, reviews, or compiler code.
- Input baseline and hashes: Git `ab5bf71abcab3d873c541679199d89c3b300223b`; see the output hashes below. The workspace is dirty/untracked, so the Git revision alone is not a sufficient publication baseline.
- Output file paths and SHA-256 values: this handoff only.
- Completion state and any blocked deliverables: audit complete. No candidate review records were produced: a candidate would immediately become stale if the manuscript, generated HTML, or status text changes before integration.
- Writes paused for integration: yes; no integrator-owned files were changed by this audit.

## Findings and proposed changes

### P0 — the manuscript reports a superseded verification result

The manifest now includes `A-PAPER` (`resource_composition/whitepaper.md`). That content is claim-tagged and therefore correctly participates in package digests. Its addition/change invalidated 39 of the 42 existing model-review records. The report after a clean compile is:

| Item | Current result |
|---|---:|
| Structural compilation | pass |
| Manifested claims/packages | 94 / 376 |
| Stored review records | 42 |
| Current review records | 3 (two `pass`, one `uncertain`) |
| Stale review records | 39 |
| Worked-case packages | 56 |
| Current passing worked-case packages | 2 |
| Worked-case gate completion | **3.6%** |
| Automated worked-case coverage | **4.8%** |
| Human disposition coverage | 0% |

`whitepaper.md` section 8 and Appendix A instead say “39 passes”, “three source-support uncertainties”, and “69.6% gate completion.” Those are valid historical measurements of the pre-manuscript review baseline, but are not the current manifest result. The same historical result appears in `wiki/log.md`.

**Required remediation:** choose one of these truthful presentations before the PDF is described as current/validated:

1. Re-run source-support, challenge and cross-artifact reviews against the frozen manuscript baseline, then state the newly compiled value; or
2. Preserve the 69.6% number only as a dated historical baseline and put the current 3.6% value immediately beside it, explaining that `A-PAPER` changed review-package inputs; or
3. Remove numerical review coverage from the reader draft until its static status panel is generated from the compilation output.

Option 2 is the lowest-risk direction for a reader-review draft. It demonstrates the intended invalidation mechanism without implying that stale reviews validate current prose.

### P0 — the current score does not cover all paper-cited claims

The manuscript has 16 distinct claim tags:

`C-AUTH-002`, `C-AUTH-006`, `C-AUTH-007`, `C-AUTH-008`, `C-CHAL-001`, `C-CHAL-002`, `C-CHAL-003`, `C-CHAL-004`, `C-CHAL-006`, `C-EVID-001` through `C-EVID-007` (except no gaps in that EVID set).

The 56-package worked-case metric is defined for 14 different claims. It includes `C-002`, which is not cited in this manuscript, and does **not** include three claims the manuscript does cite: `C-AUTH-006`, `C-AUTH-007`, and `C-EVID-006`. Therefore even a restored 69.6% worked-case metric would not be a coverage result for all source-backed claims visible to this reader.

**Required remediation:** label that statistic exactly as “worked-case gate completion,” and add a separate paper-citation status (16 tagged claims; current model review status pending after manuscript integration), or narrow the paper’s citations to the declared worked-case set. Do not call the worked-case value “the paper’s verification score.”

### P1 — the interactive edition is outside the manifest

`resource_composition/review_prototype/index.html` and `sources.html` contain the same 16 claim IDs and make source-scope statements. They are not manifest artifacts. Thus their output is neither a claim-use input nor part of the current compiler invalidation graph. The README says that claim tags are linked to “the compiler’s source records and review state,” but the page uses static source-card text; it does not import a compilation-result snapshot or render current queue status.

**Required remediation:** once the reader layout is frozen, add separately named artifact records for the rendered/interactive edition and source-card fragment (or a deterministic generated status JSON embedded in the page). Regenerate and review them as their own cross-artifact uses. Until then, revise the README and section 1 wording to say the cards link to sources and display static scope notes, not live/current compiler review state.

### P1 — source-context language needs correction

The `C-CHAL-002` source card says “short-excerpt source record.” Its canonical source (`S-CHAL-001`, MAA/RN/2025/04) has a snapshot and `full_context` records for all three cited regions. The card should instead state that source support is pending **current** review after package invalidation, if that is the intended status.

Conversely, the public-page/standard scope claims need stronger limits in the static cards:

- `C-AUTH-002` (FAA roadmap) has a snapshot but only short-excerpt local context. Its prior uncertain source-support review is current only because the paper does not cite `C-002`; it is not a current positive review for the FAA claim.
- `C-AUTH-006`, `C-AUTH-007`, and `C-AUTH-008` have no full local source context; their current source-support packages have no passing review. `C-AUTH-006` and `C-AUTH-007` are used in the manuscript, so their source cards should make this visible.
- MAA, EASA NPA, AMLAS and the seven evidence-method sources have captured full context, but their previous pass records are stale after manuscript integration. “Full context captured” and “current source-support review passed” must remain distinct labels.

### P2 — compiler behavior is working as designed, but the reader draft should expose it accurately

The only current passing worked-case packages are `P-C-002-challenge` and `P-C-002-cross_artifact`; `P-C-002-source_support` is current but `uncertain`. All other worked-case task packages need review on the current digest. This is why `current_passing_packages` is 2 despite 42 stored records. The compiler’s conservative file-level dependency hash makes a whitepaper edit invalidate reviews for the claims that use it. This is a useful result, not a compiler defect.

The case itself remains appropriately blocked: two releases are defined rather than released; ten assumptions are open; ten evidence artifacts are planned; and sixteen obligations are open. This part of the manuscript is consistent with the current assurance-case graph.

## Search and inspection record

No web retrieval was performed. The audit inspected the following local inputs on 2026-09-16:

- `verification/artifacts.json`, `verification/compile.py`, `verification/out/review_queue.json`, `verification/out/review_packages.json`, and `verification/out/report.md`;
- all 42 JSON review records under `verification/reviews/`;
- `resource_composition/whitepaper.md`, `review_prototype/index.html`, `sources.html`, and its README;
- assurance authority/challenge/evidence source records sufficient to check context status.

The static prototype has source-card IDs for all 16 manuscript claim IDs; there is no missing card in that set. External links were not re-fetched or treated as source-context capture.

## Review provenance

This was an implementation/status audit by `paper_compiler_review`, not a source-support, challenge, cross-artifact, or human-disposition review. It creates no compiler-schema review record and resolves nothing. The current record inventory contains 42 model reviews (`gpt-5.6-luna`); 39 are stale for the current package digests. A stored model verdict is not a human disposition or independent evidence.

## Verification

Commands run against the stated frozen-at-read baseline:

```bash
python3 autonomous_systems_assurance/verification/compile.py
python3 -m unittest discover -s autonomous_systems_assurance/verification/tests -v
```

Results: structural compilation passed; composition release remains blocked; 18 compiler tests passed. The generated report is `verification/out/report.md` and the exact package state is `verification/out/review_queue.json`.

Relevant input hashes at audit:

```text
c53396367ba37cf5b9dc9b64645a67d6b0d2b59b16291d7bf7e9a7951ea978fc  resource_composition/whitepaper.md
f57c998a25de52a8e3209a1294c7c3ee5c21d741e7321d693fc95aa732ed6d8b  resource_composition/review_prototype/index.html
0ca69a31811b99923f15480c56cbe0a5f4c6d9694a4831e68ef7350720e3f461  resource_composition/review_prototype/sources.html
4bc1b6bb611410a695c748d257fe894a86088c4061506954d926749db607d6af  verification/artifacts.json
7a13a0d59139efafefefd6a4f68f930b8fc448b4c9de6b026ec39024badf8a5c  verification/out/review_queue.json
2ae4ad15c55842c65e88d32d0807dd60975d9b908c398fe2c01ac91283647707  verification/out/report.md
```

## Impact and next action

The immediate affected materials are whitepaper section 8, Appendix A, prototype source cards/README, the PDF generated from them, and `wiki/log.md` if its figure is presented as current rather than historical. The existing video/narration is not implicated until it uses the new paper facts or review figures.

Recommended integration sequence:

1. Freeze the reader manuscript and generated web inputs; revise status text to distinguish the historical 69.6% baseline from the current 3.6% result.
2. Add the interactive source-card output to the manifest, or explicitly call it an unverified derivative until it is added.
3. Generate model-review candidates against the new exact packages, beginning with source support for `C-AUTH-006`, `C-AUTH-007`, and `C-AUTH-008`, then source support/challenge/cross-artifact for the 13 worked-case claims actually cited by the paper.
4. Import only records whose package ID and digest match the freeze; recompile after each bounded batch. Human disposition remains intentionally pending.
5. Render the PDF only after the manuscript’s status panel and web prototype agree with the same compiled snapshot.

No source or claim ID remapping is proposed. The factual research framing is generally careful: it preserves proposed-versus-final authority status, does not infer proprietary Tesla/DAA evidence, separates frozen trained inference from online learning, and labels all real-release evidence as absent.

---

## Addendum — fresh cross-artifact candidate pass (2026-09-16)

The revised manuscript introduced a proposed assurance rule, conventional-software bridge, evidence-metrics matrix, fuller air-transfer limits, and removed the hard-coded gate percentage. The compiler was run after those edits, then the 14 current worked-case `cross_artifact` packages were audited against their exact digests.

**Candidate output:** `coordination/handoffs/integrator/2026-09-16-paper-compiler/cross_artifact_candidates/`

- 14 candidate JSON records, one for every current worked-case cross-artifact package.
- Each candidate is schema-valid under `compile.py`'s `validate_reviews` function.
- Each candidate matched a current package ID/digest after the final compile check.
- Verdicts: 14 `pass`, zero `uncertain` and zero `fail`.
- None was imported into `verification/reviews/`; no production manuscript, manifest, compiler, source or review record was modified.

### Frozen candidate baseline

```text
Git revision: ab5bf71abcab3d873c541679199d89c3b300223b
whitepaper: 70572198d2341607f258c81c24930664f0715e7445efc2775384021f002800b8
compiler:   ee34f81c224c29b69aeedd87e2b6f6ba6f92a21057c9cb75268de518e8043c12
manifest:   4bc1b6bb611410a695c748d257fe894a86088c4061506954d926749db607d6af
queue:      b722f77585e1e271df0d8466c7303c92b867aa2780551f82ac694e47326a8eb2
```

The pass verdicts mean the tagged uses preserve their claim scopes across the manifested artifacts. They do not replace source-support, challenge, current-policy/freshness work, rights-aware retrieval, case evidence, or human disposition. In particular, the FAA/NHTSA and TSO context limitations remain source-support blockers even though their cross-artifact language is appropriately bounded.

**Verification:**

```bash
python3 autonomous_systems_assurance/verification/compile.py
python3 - <<'PY'
# loaded every candidate and ran compile.validate_reviews; compared each
# (package_id, input_digest) with verification/out/review_queue.json
PY
```

Both checks succeeded at the frozen candidate baseline. Import candidates only if the manifest inputs still produce the same package digests; otherwise regenerate the affected record rather than modifying its digest after review.

---

## Addendum — paper-only claim candidates (2026-09-16)

Nine unimported model-review candidates now live in `paper_only_candidates/`, covering `source_support`, `challenge`, and `cross_artifact` for the three claims cited by the reader-facing paper but outside the worked-case score:

| Claim | Source support | Challenge | Cross artifact | Reason |
|---|---|---|---|---|
| `C-AUTH-006` ISO/PAS 8800 public scope | uncertain | pass | pass | Public-page excerpts match the narrow claim, but no full captured context or licensed text exists. |
| `C-AUTH-007` ANSI/UL 4600 public scope | uncertain | pass | pass | Public-page excerpts match the narrow claim, but no full captured context or licensed text exists. |
| `C-EVID-006` saliency sanity checks | pass | pass | pass | Complete captured source supports a method-specific explanation limit; all uses preserve it. |

All nine candidate records are schema-valid and matched current package ID/digest pairs after the final compile check. No source, claim, manifest, paper, or `verification/reviews/` record was modified. The source-support uncertainty is intentional and must not be converted to a pass merely because the public scope wording is plausible.
