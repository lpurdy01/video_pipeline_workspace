# Source-context recovery

This directory stages official-source snapshots before promotion into a lane-owned `sources.json` record. A download is not treated as inspected, scoped evidence.

Run `capture.py <label> <url>` to write a raw response and SHA-256 capture manifest under ignored `out/<label>/`. Promotion requires inspection of the original, a UTF-8 context for the cited passage, an exact locator and verified snapshot hash, then a `context_status: full_context` update followed by a new digest-pinned model review.

On 2026-09-23 the recovery process captured the FAA AI roadmap, NASA's *Verification of Autonomous Systems* presentation, and UL 4600's public scope page. It corrected the FAA roadmap's physical-versus-printed page offsets and promoted FAA roadmap regions `S-008-R1`, `S-AUTH-001-R1` through `R3`, NASA Simplex region `S-METHOD2-001-R1`, and UL 4600 public-scope regions `S-AUTH-005-R1` through `R3`.

ISO and NHTSA returned HTTP 403 to direct retrieval. Their source records remain context-limited; a browser capture or another permitted official access path is still required.
