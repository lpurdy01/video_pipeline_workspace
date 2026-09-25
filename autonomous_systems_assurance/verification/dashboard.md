# Local verification dashboard

Run `python3 verification/render_dashboard.py` from `autonomous_systems_assurance/` after a compiler run. It writes an ignored, static [dashboard](out/dashboard/index.html) and machine-readable `data.json`.

The dashboard reports current package review status per claim, source/context links, whitepaper/script use, historical-review exclusion, and blockers. It deliberately never combines those signals into a safety or confidence score.
