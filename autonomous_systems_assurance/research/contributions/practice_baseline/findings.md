# Practice baseline: runtime assurance, hardware, simulation credibility, STPA

**Lane:** practice_baseline (`S-PRAC-` / `C-PRAC-`). **Inspected:** 2026-09-25. Snapshots are under ignored `verification/out/sources/direction_round3/`. No paywalled standard text was accessed.

- **Runtime assurance.** ASTM F3269-21 is active and offers run-time assurance as an alternative to design-time assurance for an unassured or complex aircraft function. [C-PRAC-001] This defeats an earlier Gemini lead that the practice had been withdrawn. It strengthens the paper's point that a monitor architecture is recognized engineering, while leaving the observability premise to each case.
- **Hardware.** FAA AC 20-152A recognizes DO-254 for airborne electronic hardware. [C-PRAC-002] AC 20-193 addresses multi-core interference, which can make safety-critical software non-deterministic, and excepts cores acting only as co-processors or graphics processors under another core's control with conventional databus links. [C-PRAC-003] Together with the draft ED-324 treatment of graphics processors as random hardware ([C-STAT-003]), this frames compute-hardware assurance as a configuration-specific argument.
- **Simulation credibility.** NASA-STD-7009B sets credibility-assessment practice for simulation-influenced decisions. [C-PRAC-004]
- **Hazard analysis beyond component failure.** STPA models accidents from unsafe interactions among non-failed components. [C-PRAC-005] It fits the Tempe composition failure and SOTIF-type hazards.
- **EU R157.** The EU Publications Office catalogs UN R157 as publication 2021/389. [C-PRAC-006] The regulation text and EU 2022/1426 remain uncaptured (EUR-Lex blocked).
