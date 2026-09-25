# Handoff: 2026-09-25-direction-remediation / v1

- **Integrator:** Codex, acting under the bounded job card `coordination/tasks/2026-09-25-direction-remediation.md`.
- **Baseline:** `459c733fc0c00a771e878b6c05a8155679fb8a0b`; dirty workspace preserved.
- **Result:** public-source/content remediation implemented as far as it does not require a Levi decision, additional external retrieval, a dedicated figure-render path, or human disposition.
- **Verification:** `python3 verification/compile.py` passes structurally after the change: 107 sources, 119 claims, 476 planned reviews; `composition_release_ready: false`. The large prose change correctly stales prior digest-pinned reviews, so current automated/human coverage is 0%; this is a review queue, not a content or safety regression.

## Direction-review disposition

| Finding | Status | Change or reason |
|---|---|---|
| DR-01 | addressed | `research/contributions/direction_remediation/`; paper standards box, conventional baseline and six-row comparison. No licensed text used. |
| DR-02 | partial | Paper records ED-324 draft/capture date, EASA NPA/second-NPA context and CoDANN W-shape. Public first-edition technical scope and current FAA recognition still need primary-source capture. |
| DR-03 | addressed | Paper’s road-stack section uses SOTIF vocabulary and keeps ISO 26262, ISO/PAS 8800 and UL 4600 scopes separate. |
| DR-04 | partial | Added bounded NTSB Tempe trace; Cybercab is one sentence in the script. ACAS Xu primary-source review remains outstanding. |
| DR-05 | partial | The paper explains the architectural consequence of losing inspectable interfaces, but no primary developer-source contribution for the end-to-end trend was added. |
| DR-06 | partial | Added a dated nine-row open-items register. EU/UNECE comparison is held for Levi’s D-008 scope decision. |
| DR-07 | addressed | Added an eight-phase manager lifecycle including exact deployment artifact and tool-influence obligations. |
| DR-08 | blocked on user | Runnable demo is the explicit user decision; no `demo/` lane was opened. |
| DR-09 | partial | New baseline, lifecycle and status material are integrated, but the existing full manuscript was not wholesale reordered; a dedicated editorial restructure remains. |
| DR-10 | partial | Removed EV/ICE and professional-qualification detours; compiler moved to Appendix D; figure labels fixed. The multiple presentations of contracts need a final editorial consolidation. |
| DR-11 | partial | Added proposed four-episode, 8–12-minute treatment in `video/series_structure/`; final format/supersession remains Levi’s decision. |
| DR-12 | partial | Added a consolidated standards-access scope box and removed two detours. Editorial density remains above the reviewer’s aspirational target and requires a human line edit. |
| DR-13 | blocked on user | No commit was made; all existing untracked work remains preserved. |
| DR-14 | addressed | No new compiler/dashboard/CrossPoint feature was added; only compilation and content integration were performed. |
| DR-15 | partial | Roadmap records decision-reserved items and current direction. The decision register/brief need a Levi-confirmed framing update. |
| DR-16 | blocked on user | Roadmap records the release-timing choice without selecting it. |
| DR-17 | partial | Fixed figure order in paper and expanded MCRI. SVG render/readability repair remains because no local SVG rasterizer is available in this environment. |
| DR-18 | deferred | `figures.md` records the required coverage-map extension, but modifying a dense public figure without a render/visual inspection would be unsafe. |
| DR-19 | partial | Existing take-off material keeps road and aviation approval layers separate; EU/UNECE comparison awaits scope decision and public source intake. |

## New evidence contribution

`S-BASE-001`–`005` / `C-BASE-001`–`005` add public, scoped records for FAA AC 20-115D, NASA’s public conventional-software explanation, FAA AC 20-174, ISO’s public ISO 26262 scope, and NTSB’s completed Tempe investigation. Regions are explicitly short-excerpt-only where a full project snapshot was not captured; the compiler therefore does not misrepresent them as release-grade context.

## Changed paths

- `research/contributions/direction_remediation/`
- `resource_composition/whitepaper.md`, `figures.md`
- `video/script.md`, `video/series_structure/treatment.md`
- `planning/roadmap.md`, `wiki/log.md`
- Four Gemini review/diagnostic defaults now use `gemini-3.8-flash` and high thinking.

## Recommended Opus review focus

1. Spot-check the five new public-source records against their exact prose uses and their short-context limitation.
2. Check the conventional-to-learned table, open-items register, SOTIF explanation, NTSB trace and lifecycle against DR-01–07.
3. Confirm the deferred/user-decision boundaries and assess whether to authorize the full manuscript reorder, figure render pass, ACAS Xu/source lane, and series decision.
4. Re-run the compiler and then decide whether a paced, rate-limited model review refresh is worth performing before human review.


## v2 — reader-first editorial pass (2026-09-25)

The earlier remediation was additive. This pass corrects that: `whitepaper.md` was reconstructed from 9,675 to 2,808 words around the reader contract in `resource_composition/reader_contract.md`. It removes the evidence-registry sequence, retains one lifecycle representation, begins with the indistinguishable-world problem, gives the airborne case a glider-against-terrain scene, and ends with the four controllable levers: observation path, operating envelope, delegated authority and recovery. The road/air comparison, standards scope and method limits remain, but are introduced only after the reader has a concrete problem.

Added `planning/editorial_audience_gate.md` and `gemini_nextgen_audit.py --task audience`. The audit is artifact-level and advisory; it does not add per-claim review packages or affect assurance/release coverage. A Gemini 3.8 Flash run is retained under ignored `verification/out/nextgen_gemini_audit/`; it was used only as editorial lead generation. Its source-retrieval suggestions are not factual integrations.

Final local checks: compiler structural pass, Python syntax pass for changed audit/link scripts, and `git diff --check` pass. The major remaining review question for Opus is whether this shortened reader path retains the right depth for the intended paper, before a matching script rewrite or another research expansion.


## v3 — two-layer paper structure (2026-09-25)

User correction: the reader-first pass cut useful material too aggressively. Recovered the locally preserved pre-rewrite review edition (`review_prototype/index.html`, rendered 2026-09-25 11:35) into `resource_composition/technical_reference.md` and added it to `verification/artifacts.json` as `A-TECHNICAL-REFERENCE`. The concise `whitepaper.md` remains a 2,808-word main path and now directs readers to the companion for the detailed evidence graph, method/risk analysis, full road case, compiler/review discussion and source cards. Compiler structural pass confirms 36 manifested artifacts. The detailed companion is explicitly a preserved baseline whose historical status/count prose must be reconciled before public release.
