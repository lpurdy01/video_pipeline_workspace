# Handoff: 2026-09-15-intake-browser / v1

- Author/session and role: Codex / integrator
- Date/time with timezone: 2026-09-15, America/Phoenix
- Job card: `coordination/tasks/2026-09-15-intake-browser.md`
- Input baseline and hashes: user-supplied PDFs in ignored `book_dump/`; normalized PDF and context hashes are pinned in `research/contributions/intake_20260915/sources.json`
- Output file paths and SHA-256 values: source records, claims and findings in `research/contributions/intake_20260915/`; ignored snapshots under `verification/out/sources/book_intake/` and `verification/out/sources/browser_20260915/`
- Completion state and any blocked deliverables: complete for supplied material and public browser exploration; later NHTSA AQ material, GA-ASI authorization-holder evidence and Protector MTC remain unresolved
- Writes paused for integration: yes

## Findings and proposed changes

`S-INTAKE-001` and `C-INTAKE-001` record that Zipline's 2023 operating exemption explicitly did not authorize its DAA system. `S-INTAKE-002` records the later Zipline amendment's safety-case condition. `S-INTAKE-003` provides the effective TSO-C211a manufacturer/installation distinction. `S-INTAKE-004` and `C-INTAKE-005` retain Amazon's still-under-review DAA/visual-observer relief as a counterexample. `S-INTAKE-005` and `C-INTAKE-004` capture the dated TxMCCS Tesla authorization and Cybercab rows without treating them as technical safety evidence.

The source context for existing `S-ROAD2-004` was completed from the supplied NHTSA opening resume. The project decision register now says Tesla remains optional click-worthy context while the assurance architecture remains the subject.

## Search and inspection record

Chromium loaded both Regulations.gov decision pages and their attachment labels, the TxMCCS search route and the Tesla Robotaxi detail page. It obtained the current working detail URL after the old route returned 404. NHTSA's AQ page returned access denied. FAA DRS browse loaded, but did not expose an authorization-holder result through the public scripted search controls; no absence inference is made. The FAA TSO-C212a page is an accessible draft in the document reader but returned HTTP 403 to Chromium; it was retained as an unpromoted draft.

## Review provenance

No review records were created. Source inspection and browser capture do not satisfy the compiler's source-support, challenge, cross-artifact or human-disposition review contracts.

## Verification

`python3 autonomous_systems_assurance/verification/compile.py` passed after the intake contribution was added: 71 sources, 71 provisional claims, 15 artifacts, 284 planned reviews, zero review records and 390 blockers. The normal compile is structural validation only.

## Impact and next action

The paper can use `C-INTAKE-001` and `C-INTAKE-003` for the central separation between operational authorization, equipment standard and installation approval. Use `C-INTAKE-004` only for a tightly dated road opening. Extract and inspect page-specific context for the remaining FAA, EASA, CAA and NASA sources before drafting factual narration.
