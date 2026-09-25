# Road lane round 2: authorization, compliance, and public technical claims

Research date: 2026-09-08. Every statement below is provisional and should be checked against the cited source region before publication. This lane records what public authority records and company descriptions say; it does not infer that a permit, deployment, or investigation proves the learned system safe.

## The authorization stack is layered

Texas has introduced an explicit state authorization for commercial operation of qualifying automated vehicles. TxDMV says companies operating commercially on or after May 28, 2026 must maintain an active authorization, while individually owned personal-use vehicles are outside that authorization requirement [C-ROAD2-001] [C-ROAD2-002]. TxDMV describes its own administrative authority to issue, restrict, suspend, or revoke an authorization, while DPS and local law enforcement retain roadside and traffic-law enforcement roles. This is an operational permission and enforcement surface; it is not a published model-certification or learned-component safety case.

The public TxDMV lookup is a useful distinction between a company-level authorization and a vehicle-level record. The inspected Tesla Robotaxi, LLC record was marked Authorized and listed 2026 Tesla Model Y vehicles [C-ROAD2-003]. The inspected rows did not establish a Cybercab record. The record also exposed no technical test evidence. The project should therefore avoid turning “authorized” into “the model has been certified safe.”

NHTSA adds a federal vehicle-compliance layer through manufacturer self-certification followed by agency oversight. Its September 4 announcement says AQ26002 examines the basis and technical data for Tesla's Cybercab self-certification [C-ROAD2-004]. The opening resume records September 3, 2026, an estimated population of 1,000, and a design lacking permanently attached conventional manual controls [C-ROAD2-005]. The record is consequential precisely because it is unresolved: it is an inquiry into the certification basis, not a finding that Cybercab is unsafe or noncompliant.

California shows two additional separations. DMV publishes testing and deployment permit categories and, on the inspected page, lists Tesla Robotaxi LLC and Waymo LLC among testing-with-driver holders [C-ROAD2-006]. A Waymo-specific page states a particular platform and ODD scope, including all-times operation and all-rain/fog/other-conditions language [C-ROAD2-007]. Those ODD entries are bounded permissions or listings, not universal claims about the system.

CPUC regulates passenger service separately. Its program description ties eligibility to corresponding DMV permits, describes a communication link for driverless pilot service, and requires Passenger Safety Plans for driverless programs [C-ROAD2-008]. The current permits-issued table lists Waymo under Driverless Deployment, but the linked 2023 certificate inspected here says it expired July 2, 2025 [C-ROAD2-009]. That mismatch is a research lead: a current table and a historical PDF must be reconciled before publication. A stale linked document is not evidence of current authority, and a current table is not evidence that every linked document remains current.

## The public system descriptions expose different assurance shapes

Tesla's public AI page describes camera networks, birds-eye-view outputs, world representations, trajectory planning, and large-scale evaluation infrastructure [C-ROAD2-010]. This is useful for the worked example because it gives concrete names for intermediate artifacts: road layout, static infrastructure, 3D objects, trajectories, test clips, simulation and hardware-in-the-loop evaluation. It remains a vendor description rather than a regulator-reviewed architecture. The page does not show that a tensor is an explanation, that an intermediate representation is stable across retraining, or that the current Cybercab uses exactly this architecture.

Waymo's public perception description gives a contrasting multi-sensor account: lidar, cameras and radar are fused with machine-learning software; the system is described as reasoning about occlusion and its own perceptual limits [C-ROAD2-011]. That is a strong worked-case prompt for the assurance architecture: each sensor and fusion claim creates assumptions about range, weather, latency, disagreement, and what happens when a relevant object is hidden. The source is dated and company-authored, so it cannot supply quantitative false-negative bounds or current product configuration by itself.

Waymo also publicly describes a process-level safety case: major software updates, new geographies, and new vehicle platforms go through evidence-based analysis, acceptance criteria, governance, and post-deployment performance analysis [C-ROAD2-012]. A later Waymo announcement reports TÜV SÜD audits of its safety-case and remote-assistance programs, but the inspected page did not contain the auditor's full report [C-ROAD2-013]. For the whitepaper, this is a concrete example of a public safety-case lifecycle and an unresolved source-quality boundary, not proof that the lifecycle closes every learned-behavior obligation.

## Implications for the project's compiler and narrative

The useful cross-check is to model “permission to operate” as one evidence branch among several. Texas authorization answers who may commercially operate under a state program. California DMV answers testing/deployment and stated ODD scope. CPUC answers passenger-service program conditions. NHTSA's AQ answers whether a federal self-certification basis is under examination. None of those records, alone, answers whether a perception model detects every relevant hazard, whether a planner selects a safe maneuver under sensor disagreement, or whether a retrained model preserves the prior argument.

The project's compiler should keep these as separate claim families and source independence groups, with explicit links to jurisdiction, date, vehicle/platform, ODD, and lifecycle state. The proposed synthesis is that authorization, vehicle compliance, passenger-service permission, and learned-behavior evidence are separate obligations that must be cross-linked rather than collapsed into a single “certified” status [C-ROAD2-014]. The central unresolved question for the next research wave is whether the public permits expose enough evidence to reconstruct those links, or whether the assurance case must explicitly mark the unobserved portions as obligations and blockers.

## Research leads

- Retrieve the enacted Texas Transportation Code Subchapter J and final Chapter 220 rules, then compare their application acknowledgments with the TxDMV summary.
- Capture the current TxMCCS Tesla record and reconcile the registered Model Y rows with any Cybercab authorization record.
- Retrieve NHTSA's subsequent AQ26002 associated documents as the investigation changes; preserve the opening resume separately from later findings.
- Locate the current CPUC Waymo renewal/amendment record behind the Driverless Deployment table and explain why the public 2023 certificate link is expired.
- Retrieve the linked Waymo readiness paper and TÜV SÜD auditor material if publicly available; preserve Waymo's own claims and auditor evidence as distinct source groups.
