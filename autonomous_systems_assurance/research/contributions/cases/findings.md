# Cases: adjudicated failures, closed-loop verification and architecture direction

**Lane:** cases (`S-CASE-` / `C-CASE-`). **Inspected:** 2026-09-25. Full snapshots are under ignored `verification/out/sources/direction_round2/`; context files are under `out/context/` in this lane.

## Tempe (NTSB HAR-19/03)

The complete NTSB board report supports a detailed perception-to-control trace. The system first detected the pedestrian 5.6 seconds before impact; it classified her at different times as a vehicle, an unknown object and a bicyclist, never as a pedestrian, and did not predict her path. [C-CASE-001] Reclassification discarded tracking history, and "other" objects received no goal. [C-CASE-002] Emergency handling suppressed braking for one second without an operator alert and precluded braking for mitigation alone. [C-CASE-003] NTSB's probable cause is the operator's distraction, with Uber ATG's inadequate safety risk assessment, operator oversight and safety culture as contributing factors. [C-CASE-004] The post-crash changes NTSB describes were system-level: keep the vehicle's own collision-mitigation braking active, remove action suppression, keep track history across reclassification. [C-CASE-005]

Boundary: one 2018 developmental system. The probable cause must accompany any use of the system findings.

## ACAS Xu

Reluplex verified properties of prototype ACAS Xu networks at larger scale than earlier methods. [C-CASE-006] Bak and Tran showed that the early prototype's neural-network compression, analyzed in closed loop under favorable assumptions, still has collision counterexamples. [C-CASE-007] Together they show that open-loop component proofs are not closed-loop safety.

Boundary: an early research prototype; no statement about fielded ACAS X.

## Architecture direction

Wayve describes replacing the modular sense-plan-act architecture with a single network from raw sensors to driving outputs. [C-CASE-008] This is a vendor self-description used only to show that an end-to-end direction exists. It is contrasted, as project reasoning, with public frameworks built around modular, frozen, supervised components.
