# Scope and authority review — reader-facing whitepaper

Reviewed: 2026-09-16. Scope: factual status, authority boundaries, and inferences in `resource_composition/whitepaper.md`. This is a review handoff; it does not alter the draft.

## Release-blocking corrections

1. **Replace the first-pass verification numbers before rendering.** Lines 225 and 265 say that 39 of 56 core gates pass (69.6%). The current compiler output, [`verification/out/report.md`](../../../verification/out/report.md), generated at 13:25 after this paper was in the artifact manifest, instead reports **2 current passing packages of 56 (3.6%)**, 42 review records, and 376 planned reviews. The difference is materially important: a review record can remain in the ledger while becoming stale when a package input digest changes. The draft must either regenerate its figures from the final compiler snapshot, or state a dated historical snapshot and explain that it is not current. Do not publish the 69.6% figure as current.

2. **Remove the unsupported `not identified a final lifecycle` conclusion or turn it into a documented search result.** Lines 13 and 237 say that there is no final, public, universal recipe / that the public research reviewed has not identified a final, publicly inspectable civil lifecycle closing the hardest flight-critical case. `C-CHAL-003`, `C-CHAL-004`, and `C-CHAL-006` establish the status and scope of three documents; they do not establish completeness of the wider public record. The paragraph does call this a scoped failed-to-find result, which is the right direction, but it needs a visible search boundary: databases/sites searched, date, document classes, and what would count as a positive. Suggested wording: “Within this project’s retrieved and inspected public sources as of [date], we have not yet located …; this is a search result, not a claim about private programs or all jurisdictions.” Link the retrieval log.

3. **Do not classify the worked DAA case as catastrophic by implication.** Line 237 says the failure “contributes directly to a potentially catastrophic autonomous flight decision.” The challenge record for `C-CHAL-004` specifically says to map the DAA function and aircraft-level failure-condition allocation before applying EASA’s fatality/multiple-life-threatening-injury exclusion. The current case has no such allocation. Say “the project’s highest-consequence hypothetical case” or “a case that may fall outside the proposal’s boundary depending on the allocated failure condition,” until an aircraft/system safety assessment exists.

## Important fixes before a public review version

4. **Keep calibration-shift language as a requirement, not a claimed finding.** Line 155 says calibration “may fail under shift,” then gives glare/fog/fault examples under `C-EVID-004`. That claim only supports empirical calibration findings on the paper’s evaluated classification settings; its scope explicitly says it is not a system-level safety bound. Rewrite: “Calibration demonstrated on one evaluation distribution does not establish calibration under shifted conditions. The proposed case therefore requires partitioned and shifted-condition evaluation …” This preserves the intended argument without assigning an unshown OOD result to Guo et al.

5. **Tighten the approval taxonomy.** Line 212 correctly warns that approval objects differ, but it states a broad list without a claim tag or defined jurisdiction. `C-002` only directly supports the narrower U.S. fact that a TSO authorization is distinct from installation/use approval, and that source currently has short captured context / an unresolved source-support record. Make the sentence an explicitly project-defined taxonomy: “For this paper, we distinguish …”; attach `[C-002]` only to the TSO-versus-installation sentence; say that the applicability and meaning of each approval depends on jurisdiction and product. Do not let the reader infer that the taxonomy itself proves a product’s approval chain.

6. **Mark current authority statements that rest on limited source context.** Line 31 (`C-AUTH-002`) and line 131 (`C-AUTH-008`) use claims whose source-support records were previously uncertain because the captured source region is short. They may remain in a reader-review prototype, but the interactive source card should visibly show “provisional / limited captured context,” and the prose should avoid a stronger construction than the claim registry. In particular, call the NHTSA material “ADS 2.0 guidance” and retain its stated historic/voluntary scope; do not present it as a statement of current NHTSA approval policy.

## Argument and precision improvements

7. **Qualify the indistinguishable-world thought experiment.** Line 48 holds only for the same effective input/state and a deterministic planner/controller policy; a planner may otherwise use time/history/randomness. Suggested: “If the relevant internal state presented to a deterministic planner is the same in both worlds, that planner has no information with which to choose differently.” This strengthens the core idea without overclaiming an information-theory result.

8. **Do not suggest sensor diversity is sufficient.** Line 63 says the argument needs “a different sensing path” when monitor and planner share a failure. The case correctly calls for an “independent-enough” path, but a different sensor can still have common-mode failures. Change to “an evidence-backed sufficiently independent observation path,” then retain operational restriction / authority allocation alternatives. This aligns with `AS-ROAD-004`, `AS-AIR-004`, and the `C-EVID-005` challenge.

9. **Make method-to-contract mapping labels visible.** Line 113 calls AMLAS “an excellent baseline for O-002 through O-004 and part of O-003.” The crosswalk actually labels O-002 and O-004 as **partial**, O-003 as **direct**, and O-005–O-007 outside scope. Use the exact labels or link the table: “The project crosswalk uses AMLAS directly for lineage, and partially for observability and hazard-relevant performance.” This keeps a reader from treating the methodology as a general system method.

10. **Keep the non-disclosure point as project discipline.** Line 41 says that deployment, a demonstration, or an investigation “does not disclose the evidence” behind a particular model. This is generally sensible, but it is a broad absence statement. Safer: “This paper does not treat public deployment, product demonstrations, or an investigation as disclosure of a model’s assurance evidence.”

11. **Separate recommendation from authority process.** Line 239 ends “Then let an authority decide ….” Read as a prescription only if tagged as project recommendation. Suggested: “An applicant could then present an inspectable, jurisdiction-specific case to the relevant authority.” No claim here should imply that this architecture is an accepted means of compliance.

## Observations that are already well-controlled

- Lines 5, 13–15, 97, 103, 173, 191, 210, 216, and 284–286 repeatedly distinguish a project proposal / blocked case / traceability tool from certification, authorization, or product evidence. Preserve these guardrails.
- AMLAS (lines 109–113), MAA (115–119), and EASA (121–125) retain document status and jurisdiction rather than calling any of them a universal certification standard. This matches the source claims.
- Lines 141–169 correctly avoid a composite accuracy / mileage / neuron-coverage / interpretability safety score. The runtime-assurance section names timing, dynamics, monitoring and recovery premises.
- The road-to-air table (199–206) treats airborne transfer as a changed evidence problem, not as direct transfer of road results. Good architectural framing.
- The stated 10 open assumptions, 10 planned evidence artifacts, 16 open obligations, and two defined-not-released releases agree with `assurance_case.json` at review time. These values should nevertheless be refreshed from the final compiler run with the other dynamic figures.

## Minimum validation after edits

1. Re-run compilation after the final markdown/HTML source changes and take every number in the paper from that output.
2. Have a model reviewer check only the revised source-backed paragraphs against their source-region scope, especially `C-AUTH-002`, `C-AUTH-008`, `C-CHAL-003`, `C-CHAL-004`, and `C-EVID-004`.
3. Ensure the interactive source cards surface provisional status and short-context limitations next to the relevant claim tags.
