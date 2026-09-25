# Assurance for Learned Autonomous Systems

Started 2026-09-08. Working name; independent whitepaper, video, and resource project.

**Central question:** How could we design a practical assurance architecture for learned autonomous systems?

**Audience:** technical generalists and engineers; accessible video, rigorous whitepaper. Both choices were confirmed by Levi on 2026-09-08.

The narrative begins with a car perceiving the world, navigating and avoiding hazards. Toward the end, the same visual vehicle takes off: we examine what changes when the problem becomes aviation, including detecting and avoiding approaching aircraft. This narrative choice was confirmed by Levi on 2026-09-08. We investigate the differences instead of assuming them.

Start with [the project brief](PROJECT_BRIEF.md), [the previous-project review](planning/previous_project_review.md), and [initial research](research/initial_findings.md). The [decision register](planning/decisions.md) distinguishes settled direction from proposals.

| Folder | Purpose |
|---|---|
| `research/` | Primary-source register, research questions, findings, and access limitations |
| `wiki/` | Maintained synthesis, terminology, competing explanations, and index |
| `assurance/` | The learned-system architecture being investigated and its worked case |
| `verification/` | The project's own claim/evidence compiler, review contracts, and checks |
| `resource_composition/` | Whitepaper structure, figures, bibliography and public-package composition |
| `video/` | Narrative, storyboard, future rendering integration, local recordings |
| `publication/` | Export inventory and release evidence; later GitHub and launch preparation |
| `planning/` | Prior-project retrospective, decisions, milestones, and analytics context |
| `coordination/` | Three research lanes, paper/video ownership, job cards, handoffs and frozen authoring baselines |

Two architectures must stay distinct: `assurance/` concerns the autonomous vehicle; `verification/` checks our research and communication about it. The compiler is production infrastructure, not a repeat of the previous video's subject.

Initial status: research seed and design proposals. No final paper, rendered video, certification conclusion, or completed independent cross-verification is claimed. Source inspection is recorded with its actual scope; publication remains gated on further review.

Generated outputs belong in ignored `out/` directories. Human voice and its detailed timing stay local. See [AGENTS.md](AGENTS.md).

Parallel workers start with [the coordination protocol](coordination/README.md). Research agents write separate contribution registries; the compiler merges them without shared-file edits. Paper and video authors work in separate folders against an agreed evidence baseline.

Run the local foundation with `python3 autonomous_systems_assurance/verification/compile.py` from the repository root. See [compiler commands](verification/README.md) and [setup status](planning/setup_status.md) for implemented checks and remaining work.

For the current review package, start with the [reader whitepaper](resource_composition/whitepaper.md), [recording-feedback script](video/script.md), and generated local [verification dashboard](verification/out/dashboard/index.html). The dashboard is regenerated from the live compiler graph and is not a safety score.
