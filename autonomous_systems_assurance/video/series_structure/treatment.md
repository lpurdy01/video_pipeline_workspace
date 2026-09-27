# Three-part series treatment

**Status:** Levi chose a three-part series on 2026-09-25, provided each episode stands on its own and the set drives viewers between the channel's videos. This treatment and the three episode scripts supersede the 31–34 minute single-film plan (`video/script.md` and `video/nextgen_structure/`). Those files are kept as history, not deleted. Titles, thumbnails and the end-screen choice of earlier video are proposals for Levi.

## Why three episodes

The previous channel video, about 11.5 minutes long, averaged about 3 minutes watched and lost roughly half its viewers in the first 35 seconds (`planning/analytics_baseline.md`). A 30-minute film would be seen, for most viewers, as its first few minutes. Three episodes of roughly 8–10 minutes give three separate chances to be discovered. Each one pays off on its own, and each one points at the next.

## Standalone rules (every episode)

1. **Its own scene in the first 20 seconds.** No "last time we saw…". Each episode opens on a concrete image that states its question.
2. **One question, answered within the episode.** A viewer who watches only this episode leaves with a complete idea.
3. **One payoff visual** the viewer could sketch afterwards.
4. **Re-establish any term used.** DAL, SOTIF and ED-324 are defined in the episode that uses them, in one line.
5. **Cross-links are invitations, not dependencies.** One mid-episode pointer at most, then the closing tease and the end screen.
6. **Claims stay tagged.** Every factual narration line carries its claim tag; the paper carries the detail.

## Shared visual language (series recognizability)

- The **van-and-cyclist intersection** and the **glider against broken terrain** recur as the series' two scenes.
- The **green cue card** ("candidate + time + uncertainty/unknown") appears in every episode.
- The **four levers** graphic (observation · envelope · authority · recovery) closes episodes 1 and 3.
- Consistent color semantics: blue = conventional / designed; amber = learned; green = evidence or proposal; red = boundary or failure; grey dotted = not yet demonstrated.
- Production defaults unchanged: rendered visuals, human final voice, no music (D-007).

## Episodes

| # | Working title (options) | Runtime | Hook (first 20 s) | Question | Payoff visual | Key claims |
|---|---|---:|---|---|---|---|
| 1 | *How Do You Certify Code Nobody Wrote?* / *Two Worlds, One Input* | ~10 min | Split screen: empty lane vs hidden cyclist; planner and monitor both get "LANE CLEAR." | Why does the software-safety playbook crack when part of the system is learned? | The six playbook pillars, four cracking; then the Tempe timeline with labels flickering and track history wiping. | C-STAT-006/007, C-BASE-001/004, C-AUTH-010, C-RISK-002, C-EVID-005, C-CASE-001–005 |
| 2 | *Who Decides When AI Is Safe Enough to Drive — or Fly?* / *The Rules for AI Aren't Finished* | ~8 min | "No federal pre-approval" card for a car beside four separate approval stamps for one aircraft box. | Who writes the rules, what exists, and what has not been decided? | The coverage map building row by row, then the "Not done yet (Sept 2026)" board; ED-324's DAL ladder with A and B behind a line. | C-STD-003/004, C-STAT-001–005/008, C-RISK-006/007, C-CHAL-001/004/006, C-AUTH-001/003/009, C-CASE-008 |
| 3 | *Building an AI Vision System to a Safety Standard — Then Letting It Fly* | ~9.5 min | A detector with a high score spots the cyclist after the last safe braking point. | What would a team actually build, and what changes when the vehicle takes off? | The road tilting into airspace with the cue card pinned; ACAS Xu's table shrinking into a network that still collides in closed loop. | C-TRAIN-001–004, C-STAT-002/003, C-PRAC-001, C-RISK-004, C-EVID-005, C-INTAKE-003, C-CASE-006/007; illustrative timing budget |

Scripts: [episode 1](ep1_script.md), [episode 2](ep2_script.md), [episode 3](ep3_script.md).

## Release and cross-link plan

**Release (D-027):** the three episodes are released together when all three are done, even if they are finished one after another. Status statements are rechecked against their sources in the week before release.

**Cross-links (D-028):** each episode links the other two and at least one earlier channel video.

| Episode | Closing tease | End screen (two slots) | Description links |
|---|---|---|---|
| 1 | "Who's writing the rules, and what they've left open." | Episode 2; *The Software AI Isn't Allowed To Write* (`80Wz-BAIkrM`) | Episodes 2 and 3; paper; earlier channel videos |
| 2 | "What a team would actually build, and letting the car take off." | Episode 3; Episode 1 | Episodes 1 and 3; paper; earlier channel videos |
| 3 | "The playbook all of this builds on is in episode 1." | Episode 1; best-fit earlier channel video (Levi to choose) | Episodes 1 and 2; paper; earlier channel videos |

*The Software AI Isn't Allowed To Write* is the natural bridge. It covers why safety-critical software is hard to produce with AI, and episode 1 covers why the same playbook cracks when AI is inside the product. It is the only earlier video recorded in this repository (`planning/analytics_baseline.md`). Levi adds the other channel videos to the description block and picks episode 3's second end-screen slot. A pinned comment on each episode asks one open question from that episode and links the series playlist.

## Thumbnail concepts (proposals)

1. The van, a faint cyclist silhouette behind it, and a green "LANE CLEAR" label. Text: "CODE NOBODY WROTE".
2. A car labelled "self-certified" beside an aircraft box covered in approval stamps. Text: "WHO SAYS IT'S SAFE?"
3. A small dark glider against terrain inside a detection box marked "?". Text: "NOW MAKE IT FLY".

Per `feedback_model_review_authority`, model critique of thumbnails is a legibility check only; Levi's judgment decides the concept.

## Production notes

- Current drafts: episode 1 about 1,140 spoken words, episode 2 about 940, episode 3 about 1,090. At 130 words per minute plus about 15% visual holds, that is roughly 10, 8.3 and 9.6 minutes. Section timecodes in the scripts are computed from those counts.
- `FEEDBACK PAUSE` markers remain for the local voice-feedback workflow; human audio stays local (AGENTS.md).
- The Tempe material uses a rendered timeline only: no crash footage, no imagery of the victim, and NTSB's probable cause stated in the same beat as the system findings.
