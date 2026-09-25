# Handoff: assurance-evidence methods

Status: complete on 2026-09-16.

## Ownership and baseline

- Owner: `assurance_evidence`
- Exclusive output paths used: `research/contributions/assurance_evidence/` and this handoff directory.
- Base commit: `ab5bf71abcab3d873c541679199d89c3b300223b`
- Initial canonical source-register SHA-256: `1dbe7b18059dfe43dfbaace1bec1d65f7ab510c7ad4ff153d5561760324434e2`
- Initial canonical claim-register SHA-256: `df12a3a0aa71bb32805ee2be847594ab1d337ce4254ffa18c35ef8c4d0ea46c7`
- Initial learned-systems plan SHA-256: `a85529baa7ad9db9b177083411012e9b734cf8b7f40c2e78da7eae2a0dfe333e`
- Initial compiler diagnostic: structural compile passed; 71 sources, 71 claims, 389 blockers, 284 planned reviews and no review records.

## Delivered files

- `research/contributions/assurance_evidence/sources.json`: 7 full-context source records, 15 regions, IDs `S-EVID-001` through `S-EVID-007`.
- `research/contributions/assurance_evidence/claims.json`: 7 provisional evidence-method claims, IDs `C-EVID-001` through `C-EVID-007`.
- `research/contributions/assurance_evidence/findings.md`: contract mapping, assumptions, counterexamples and a proposed minimum evidence set for the road case.
- Ignored source cache: 7 PDFs and UTF-8 extracted contexts under `research/contributions/assurance_evidence/out/`.

## Search and retrieval record

Searches on 2026-09-16 covered NIST AI RMF/TEVV, NIST combinatorial assurance and neuron coverage, NASA UAS runtime assurance, calibration, saliency-method validation, and rare-event autonomous-vehicle simulation. Sources were selected for original publisher or primary-paper status and for direct relevance to frozen trained components.

All selected PDFs were successfully retrieved from official NIST/NASA endpoints or arXiv and transformed locally with `pdftotext`. Source and context hashes are checked by the compiler through each region record. No licensed standard was downloaded or redistributed.

## Key findings

1. The evidence architecture should combine scope/lineage, input-scenario coverage, closed-loop testing, explicit uncertainty behavior, independent monitor/recovery evidence and controlled change. It should never reduce them to one model-safety number.
2. A rare-event probability estimate is conditional on the scenario distribution, simulator and threshold. Test miles alone do not expose that conditionality.
3. Calibration needs per-release and per-ODD evaluation. It is not a proof that a high-confidence output is safe under shift.
4. Runtime assurance has a useful formal shape for a black-box learned controller, but safety depends on its external premises. An unobservable or too-late perception miss is a direct counterexample to a monitor-rescues-everything argument.
5. Interpretability artifacts must survive task-specific intervention/randomization checks. A visual layer or saliency image cannot be treated as causal evidence merely because it looks plausible.

## Integration warning / conflict handling needed

`S-EVID-005` is likely a semantic duplicate or later NTRS record of canonical `S-010` and contribution `S-METHOD2-003`, all titled *A Verification Framework for Runtime Assurance of Autonomous UAS*. This contribution supplies full local context for NTRS `20240010429`; existing records reference other IDs/versions. Do not count them as independent corroboration. Compare hashes/text and either retain this full-context record while mapping the older IDs, or retain the prior record and preserve this handoff as retrieval provenance.

No duplicate source or claim IDs were created, and no shared files were edited.

## Verification

Run after integration freeze:

```bash
python3 autonomous_systems_assurance/verification/compile.py
python3 -m unittest discover -s autonomous_systems_assurance/verification/tests -v
```

This worker did not run the compiler after writing because other lanes were concurrently adding contribution registries in the shared workspace. JSON structural validation and source/context file checks remain for the integrator's frozen build.
