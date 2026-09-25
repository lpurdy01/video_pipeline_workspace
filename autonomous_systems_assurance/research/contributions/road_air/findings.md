# Road-to-air research contribution

As of 2026-09-08. Provisional research, awaiting independent challenge and integration. Ownership: `road_air` research lane. This contribution does not change canonical claims or publication readiness.

## Strongest addition: Texas permission has a federal compliance dependency

Texas requires commercial driverless operators to maintain TxDMV authorization from May 28, 2026. Its application asks applicants to acknowledge state-law compliance, recording capability, applicable federal-law compliance, and a minimal-risk response to ADS failure. The state can restrict, suspend or revoke authorization. This is a useful concrete interface for our assurance graph: operator permission depends on obligations that remain separately enforceable. [C-ROAD-AIR-001] [C-ROAD-AIR-002] [TxDMV program explanation](https://www.txdmv.gov/AVprogram)

The federal side is visible in NHTSA's September 4, 2026 Cybercab Audit Query: the agency is examining Tesla's basis for FMVSS self-certification after Austin deployment, including how Tesla treated requirements associated with absent human controls. This is an investigation, not a final adverse finding. Pair it with the Texas source without implying that state authorization decides federal compliance. The existing canonical source `S-006` already covers this announcement; do not count a second copy as independent corroboration. [NHTSA announcement](https://www.nhtsa.gov/press-releases/investigation-tesla-cybercab-self-certification)

Texas DPS lists a Cybercab first-responder plan. That proves the plan is listed; it does not establish a specific operator's active TxDMV authorization or a vehicle's federal compliance. The page displays February 27, 2026, but this is not evidence of when the Cybercab link was added. [C-ROAD-AIR-003] [DPS first-responder plans](https://www.dps.texas.gov/section/cav/connected-autonomous-vehicles)

## Inspection record and unresolved scope

| Source | Actually inspected | Remaining gap |
|---|---|---|
| TxDMV AV program | Program description, effective/enforcement dates, application acknowledgments, enforcement and lookup instructions | Underlying enacted statute and final rules need clause-level review |
| NHTSA Cybercab announcement | Full article dated September 4, 2026 | Underlying AQ record, Tesla submissions, and any later disposition |
| Texas DPS | Listing page and Cybercab link label | Linked plan itself not inspected |
| TxMCCS operator lookup | Opened Truck Stop and automated-vehicles URLs; redirected/returned no readable text | Actual Tesla authorization, vehicle list, conditions and current status remain uninspected |
| Zipline Exemption 19111B | Search discovery only; direct PDF retrieval returned HTTP 403 | Letter contents and all attached conditions remain uninspected |

The operator lookup is [TxMCCS Truck Stop](https://txmccs.txdmv.gov/truckstop). No Tesla-specific active authorization claim is proposed from secondary reports of its contents. No full sources were captured, so source-region snapshots are null.

## Aviation handoff

A useful next artifact is the September 18, 2023 [Zipline Exemption 19111B letter in FAA docket FAA-2020-0499](https://downloads.regulations.gov/FAA-2020-0499-0033/attachment_1.pdf). This is a retrieval lead only: the direct PDF request failed. Another researcher should obtain the grant, predecessor and incorporated conditions before claiming acoustic sensing was accepted for a particular operational scope. Its existence in search results does not close the canonical Zipline gap.

## Suggested worked-case use — project inference

Show the car's assurance graph with separate nodes for an operating authorization, applicable vehicle requirements, operator procedures and supporting safety evidence. During takeoff, preserve the questions but replace the jurisdiction-specific approval objects and test the physical assumptions. A graph edge should name the actual dependency; the word “approved” should never stand alone. This is a proposed explanatory device, not a conclusion that road and air approval burdens are equivalent.

The minimal-risk node is particularly useful: make the demonstration ask what the fallback must accomplish and what sensor information it requires. Then revisit those assumptions in flight. Do not turn a state application acknowledgment into proof that any particular fallback succeeds.
