# Handoff: 2026-09-25-direction-round2 / v1

- **Author/session and role:** Claude (Opus 5.5), Claude Code session `9764b3e0`, acting as integrator at Levi's request ("address your concerns"), after the Codex remediation round and Levi's commit `3ecbe54`.
- **Date:** 2026-09-25 (America/Los_Angeles)
- **Inputs:** the direction review (`../2026-09-25-direction-review/handoff.md`), the re-check of Codex's round, and Levi's decisions: a three-part series whose episodes each stand alone, plus the paywall rule.
- **Base commit:** `3ecbe54`. All changes below are uncommitted; Levi commits.
- **Completion:** content remediation done. The per-claim model-review refresh has not run: all prior digest-pinned reviews are stale after the rewrite. Human disposition is 0%.

## Status against the direction review

| DR | Status | Where |
|---|---|---|
| DR-01 conventional baseline | addressed | Paper §1 names DO-178C, DO-330, ARP4754A, DAL, ISO 26262/ASIL, SOTIF through public sources. The DO-178B (1992) to DO-178C (2011) timeline and the pillar table carry conventional anchors. [C-STAT-006] [C-STAT-007] |
| DR-02 aviation ML pipeline | addressed | Paper §4: ED-324/ARP6983 committee history, the issue 1 scope (non-adaptive supervised ML up to DAL C, as presented Aug 2025), the target slip June to 31 Dec 2026, CoDANN W-shape, EASA NPA plus the AI Act and its dates, FAA roadmap status. [C-STAT-001..005] |
| DR-03 SOTIF / road stack | addressed | Paper §2, "Why this is also a SOTIF problem" |
| DR-04 real failures | addressed | Paper §2: full NTSB HAR-19/03 trace, with the probable cause stated in the same beat. Paper §7: ACAS Xu verified yet unsafe in closed loop. Cybercab is out of the paper and the new scripts. [C-CASE-001..007] |
| DR-05 end-to-end tension | addressed | Paper §5, "The architecture tension" (Wayve primary statement [C-CASE-008]); episode 2 §5 |
| DR-06 yet-to-do register | addressed | Paper §5: an 11-row dated table. UN R157 is included as a comparison (proposed D-025). EU 2022/1426 is **not** claimed because retrieval was blocked. |
| DR-07 lifecycle | addressed | Paper §3: lifecycle table with a conventional-analogue column, plus the training-traps table |
| DR-08 toy demo | **blocked on Levi** | Gemini round 2 again rates purpose element 5 "partial" because the worked example is abstract. The demo is the fix. |
| DR-09 reorder | addressed | Paper follows `whitepaper_outline.md`, mapped to the purpose elements and episodes |
| DR-10 cuts | addressed | NCEES and EV material removed from both layers; the compiler section is Appendix D of the reference; one lifecycle representation in the paper; stale counts removed |
| DR-11 video format | addressed | D-023 three-part series: `video/series_structure/treatment.md` plus `ep1_script.md`, `ep2_script.md`, `ep3_script.md`; `video/script.md` marked superseded |
| DR-12 tone | addressed (paper, scripts) | Paper: 28 negations / 5,237 words (about 1 per 187; baseline 1 per 88). Scripts: 1–2 each. Reference: 72 / 7,893. Deliberately kept, since technical distinctions belong there. |
| DR-13 commit | resolved by Levi | `459c733`, `3ecbe54` |
| DR-14 tooling freeze | held | No new tools. `build_coverage_map.py` only gained data rows; one-off scripts live in the session scratchpad. |
| DR-15 brief/decisions | addressed | D-021..D-024 recorded; D-025 proposed; the brief has a "Current purpose" block; D-003 marked "refined by D-021" |
| DR-16 release timing | **open for Levi** | Options recorded in `planning/roadmap.md` |
| DR-17 figure defects | addressed | F-001, F-002 and F-008 fixed and re-rendered with headless Chromium; paper figures numbered 1–4 sequentially; MCRI expanded |
| DR-18 coverage map | addressed (PNG) | Eight-row panel 3. The editable SVG still lags and must be updated before video use. |
| DR-19 regime in take-off | addressed | Paper §7 table rows "Who gives permission?" and "How is rigor set?", plus the DAL C boundary paragraph |

The Codex round's defects are also fixed: the technical reference is rebuilt from committed Markdown (no HTML anchors), and the lost v1 content is restored.

## New evidence

- **`research/contributions/cases/`** (S-CASE-001..004, C-CASE-001..008): full snapshots and context files for NTSB HAR-19/03 (78 pp.), Katz et al. (Reluplex), Bak & Tran (ACAS Xu closed loop) and Wayve's technology page.
- **`research/contributions/standards_status/`** (S-STAT-001..006, C-STAT-001..008):
  - the SAE G-34 / EUROCAE WG-114 presentation at the FAA AI/ML Technical Exchange (Aug 2025), which is SAE-copyrighted, so only short quotes are used and it is not redistributed;
  - the EUROCAE consultation notice;
  - the EASA NPA 2025-07 page;
  - NASA Jacklin (a separate record from S-BASE-002, same independence group);
  - UK DfT and VCA pages on UN R157.
- All new regions are `full_context`: snapshots under ignored `verification/out/sources/direction_round2/`, and context files under each lane's ignored `out/context/`. **Those ignored files exist only on this machine.** Another checkout will show "snapshot missing" blockers until they are transferred.
- **Retrieval failures:** unece.org (Cloudflare 403), EUR-Lex (202 with an empty body), tesla.com/AI (403).

## Verification performed

- `python3 verification/compile.py`: structural pass; 117 sources, 135 claims, 42 artifacts.
- `python3 -m unittest discover -s verification/tests`: 19 tests OK.
- `resource_composition/review_prototype/render.sh`: HTML and PDF built (46 pp.). All 198 claim links resolve to source cards; 38 cards were generated from the registries for tags the new paper uses.
- Figures rendered and inspected at native size.
- Gemini `gemini-3.8-flash` (thinking high) audience review, one call:
  - round 1: `verification/out/nextgen_gemini_audit/20260925T185344Z_audience_structure_gemini-3.8-flash.md`
  - round 2: `20260925T203458Z_audience_structure_round2_gemini-3.8-flash.md`
  - Purpose fit moved from 1 strong / 3 partial / 1 missing to 4 strong / 1 partial.

## Round-2 Gemini dispositions

| Suggestion | Disposition |
|---|---|
| Tempe earlier in episode 1 | Partly adopted: a two-sentence Tempe teaser in the cold open; payoff stays in §4 after the four levers |
| Episode 1 close tease a controversy | Adopted, with a supported contrast [C-STD-004] [C-INTAKE-003]; its "baggage-door sensor" example was unsupported |
| Episode 2 "still missing" list duplicates | Adopted: recap plus three new items on the DAL-ladder visual |
| Episode 3 link to the paper | Adopted |
| Shorten the standards box and proposal disclaimer | Adopted, one sentence each |
| "As of late 2026, no authority provides…" | **Rejected**: a universal absence claim (D-014); the dated negative-search wording stays |
| Move the landscape to near the end of the paper | Not adopted: purpose elements 2 and 3 are core; order follows D-021 |
| Omissions: ASTM F3269, hardware (DO-254 / AMC 20-152A), NASA-STD-7009A simulation credibility, STPA | **Research leads for next round**; none captured yet |

## Open items

1. **Levi decisions:**
   - DR-08 toy demo: the remaining gap on purpose element 5.
   - D-025 UN R157 comparison scope.
   - DR-16 release timing versus ED-324.
   - Episode titles and thumbnails.
   - Whether *The Software AI Isn't Allowed To Write* fits episode 1's end screen.
2. **Review refresh:** a paced per-claim review of the new claim uses; all older packages are stale by design.
3. **Research leads:**
   - ASTM F3269 status;
   - public hardware-assurance sources (FAA AC 20-152A, EASA AMC 20-152A/20-193);
   - simulation credibility (NASA-STD-7009A);
   - STPA (Leveson, local book);
   - browser capture of UN R157 and EU 2022/1426;
   - recheck ED-324 at publication.
4. **Coverage map SVG** to match the PNG before video production.
