# Run the compiler

From the repository root:

```bash
python3 autonomous_systems_assurance/verification/compile.py
python3 autonomous_systems_assurance/verification/compile.py --release
python3 -m unittest discover -s autonomous_systems_assurance/verification/tests -v
```

Normal compilation writes ignored `verification/out/graph.json`, `snapshot.json`, `review_packages.json`, `review_queue.json`, and `report.md`. The initial release check is expected to fail: source context and independent/human reviews are incomplete.

Render the local reader-facing status surface after compiling:

```bash
python3 autonomous_systems_assurance/verification/render_dashboard.py
```

Open `autonomous_systems_assurance/verification/out/dashboard/index.html` in a browser. It links claims to their recorded source URLs and regions and separates current source-support, challenge, cross-artifact, and human-disposition outcomes. See [dashboard notes](dashboard.md).

To compare revisions, preserve the prior snapshot before rebuilding:

```bash
cp autonomous_systems_assurance/verification/out/snapshot.json /tmp/assurance-baseline.json
python3 autonomous_systems_assurance/verification/compile.py --baseline /tmp/assurance-baseline.json
```

Import an actual review record, then recompile:

```bash
python3 autonomous_systems_assurance/verification/compile.py --import-review /path/to/review.json
```

Records are append-only through this CLI; never invent a human review or label the author's own source gathering independent review. See [architecture and record contract](ARCHITECTURE.md). Normal compilation and tests need no network, API key or additional package.

The optional Gemini first pass writes candidates under ignored `out/` and does not create a human disposition. After a candidate batch completes, import only digest-current records with:

```bash
python3 autonomous_systems_assurance/verification/import_current_model_reviews.py
```
