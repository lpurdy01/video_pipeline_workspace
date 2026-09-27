# Handoff: 2026-09-25-direction-round3 / v1

- **Author/session and role:** Claude (Opus 5.5), Claude Code session `9764b3e0`, integrator.
- **Trigger:** Levi, 2026-09-25: "do all the things not done yet", plus four answers:
  1. hesitant on the toy demo (laptop-only compute; unclear benefit);
  2. "decide for me" on the UN R157 scope;
  3. release the episodes together when done, possibly finishing them sequentially;
  4. interlink other channel videos.
- **Base:** round 2 (`../2026-09-25-direction-round2/handoff.md`), uncommitted on top of `3ecbe54`. Levi commits.

## Decisions recorded (planning/decisions.md)

| ID | Decision |
|---|---|
| D-025 | UN R157 enters as a road-regime comparison; worked case stays US-scoped (decided on Levi's delegation). |
| D-026 | No runnable simulation. Purpose element 5 is closed with worked artifacts instead: a timing budget and release manifest in the paper §3; a label policy, evaluation template and change-impact record in the technical reference, Appendix F. All are labelled illustrative. |
| D-027 | Release all three episodes together when done; recheck dated status statements the week before release. |
| D-028 | Interlink with other channel videos. The plan is in `video/series_structure/treatment.md`: end screens, descriptions, pinned comments. |

## Work completed

**Research: new lane `practice_baseline`** (S-PRAC-001..006, C-PRAC-001..006; full-context snapshots under ignored `verification/out/sources/direction_round3/`):
- **ASTM F3269-21** run-time assurance practice: active, last updated 19 Nov 2021. This **defeats** the earlier Gemini lead that it had been withdrawn.
- **FAA AC 20-152A** (DO-254) and **AC 20-193** (multi-core interference, with an exception for co-processors and graphics processors in some configurations).
- **NASA-STD-7009B**: simulation credibility.
- **STPA Handbook** (Leveson and Thomas, 2018).
- **EU catalog record** of UN R157 (2021/389).

Still uncaptured: EU 2022/1426 and the R157 text (EUR-Lex and UNECE block automated retrieval).

**Paper:**
- §2: ASTM F3269 alongside the monitor premise; STPA in the SOTIF section.
- §3: STPA added to the phase 1 analogue; new "What two of the artifacts look like" subsection (a 30 mph timing budget showing the envelope lever as a rule, and a release manifest).
- §4: EU R157 publication.
- §5: hardware register row rewritten (AC 20-152A, AC 20-193 plus the draft ED-324 graphics-processor treatment).
- §6: simulation-credibility and ASTM rows.
- New reading links.

**Technical reference:** Appendix F, worked artifact examples.

**Episode 3:** timing-budget beat and the ASTM F3269 line; runtime now about 9.6 minutes.

**Figures:** coverage-map SVG now matches the PNG (eight rows) and has panel-1 and panel-2 label alignment fixes; PNG and caption carry C-PRAC-006.

**Series treatment:** release and cross-link plan. *The Software AI Isn't Allowed To Write* (`80Wz-BAIkrM`) is the only earlier video recorded in the repo, so Levi fills in the others.

## Verification

- Compiler: structural pass; 123 sources, 141 claims, 43 artifacts. Tests: 19 OK. Review edition renders.
- **Paced model review of all shipped claim uses:**
  - Command: `first_pass_model_review.py --all-claims --used-by` for the paper, the technical reference and the three episode scripts; `gemini-3.8-flash` at high thinking, 1 worker, 15 s minimum interval.
  - Scope: 77 claims × 3 tasks = 231 packages.
  - Results: see "Review results" below, filled in at completion.

## Review results

**Run.** First with 1 worker (it stalled on a hung request), then 3 workers with a 15 s minimum between request starts. `first_pass_model_review.py` now sets a 5-minute HTTP timeout per request; a timeout is logged in `errors.json`, never recorded as a verdict. The run **stopped at 113 of 231** when the Gemini project returned `402 RESOURCE_EXHAUSTED: prepayment credits are depleted`. The runner's quota guard halted further calls; 117 packages were never sent.

**Outcome of the 113 completed reviews:**

| Task | Pass | Uncertain | Fail |
|---|---:|---:|---:|
| Source support | 25 | 13 | 0 |
| Challenge | 38 | 0 | 0 |
| Cross-artifact | 36 | 0 | 1 |

**Acted on:**
- **Fail, P-C-CASE-001 cross-artifact.** The episode 1 cold-open teaser placed the Tempe crash right after "every line of code can be correct" without the probable cause. Rewritten to name the chain "from its perception software all the way to the human who was supposed to be watching", with C-CASE-004 now tagged.
- **Uncertain, C-CASE-005 source support.** The reviewer saw a context window that stopped before NTSB §1.9.1. Root cause: a bug in my round-2/3 context builder. Python `splitlines()` also splits on the PDF form-feed characters, so every PDF-derived context window was offset by about one line per page. All 27 round-2/3 regions were rebuilt with `\n` splitting, and every region now contains its quoted excerpt. (The NTSB timeline region is a layout table with the phrase split across columns; its rows were verified present.)
- **Uncertain, C-BASE-001/002/003 source support** (short excerpts only). Upgraded to `full_context` with retained public PDFs: AC 20-115D, the NASA Jacklin paper and AC 20-174. C-BASE-005 gained the full-context NTSB report region S-CASE-001-R1 as additional support.

**Not fixable here:**
- **C-BASE-004** (ISO 26262 page returns 403) stays short-excerpt.
- Older-lane short-excerpt limitations remain on C-002, C-AIR2-004, C-AIR2-007, C-AUTH-008, C-AUTH-009, C-CHAL-006 and C-EVID-001.
- **C-016** is an inference claim; "uncertain" is the expected source-support outcome for it.

**Consequence.** The compiler hashes every artifact's full dependency closure into each package digest, so these fixes (correct source contexts, the episode 1 rewrite) invalidated all 113 candidates. None were imported. That is correct: they reviewed faulty context windows. **All 231 packages for the shipped artifacts await review.**

**Process recommendation (D-027).** Run the per-claim review once, after content freeze and just before release. Any later edit to the paper's dependency closure re-stales every package.

**To resume**, after topping up AI Studio prepaid credits:

```bash
cd autonomous_systems_assurance
python3 verification/first_pass_model_review.py --all-claims \
  --used-by resource_composition/whitepaper.md --used-by resource_composition/technical_reference.md \
  --used-by video/series_structure/ep1_script.md --used-by video/series_structure/ep2_script.md \
  --used-by video/series_structure/ep3_script.md --workers 3 --min-request-interval 15
python3 verification/import_current_model_reviews.py
python3 verification/compile.py
```

At the observed pace (about 3.7 reviews per minute) the full set takes about an hour.

## Open items

- Human disposition remains 0%. Only Levi can record it, when he chooses to review.
- EU 2022/1426 and the R157 text need a browser capture if the paper ever makes content claims about them.
- ED-324/ARP6983: re-read the published issue if it appears before release (D-027).
- Episode titles, thumbnails and episode 3's second end-screen video: Levi's choice.
