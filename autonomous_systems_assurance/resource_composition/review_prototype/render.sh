#!/usr/bin/env bash
set -euo pipefail

project_root="$(cd "$(dirname "$0")/../.." && pwd)"
prototype_dir="$project_root/resource_composition/review_prototype"
mkdir -p "$prototype_dir/out"

pandoc "$project_root/resource_composition/whitepaper.md" \
  --standalone --toc --toc-depth=2 \
  --metadata title="Assurance for Learned Autonomous Systems — reader review draft" \
  --include-in-header="$prototype_dir/header.html" \
  --include-after-body="$prototype_dir/sources.html" \
  --css=style.css \
  --output="$prototype_dir/index.html"

python3 "$prototype_dir/write_status_panel.py"
pandoc "$prototype_dir/out/current_status_panel.html" --standalone --output="$prototype_dir/out/current_status_fragment.html"
python3 "$prototype_dir/link_claim_tags.py" "$prototype_dir/index.html"
python3 - "$prototype_dir/index.html" "$prototype_dir/out/current_status_fragment.html" <<'PYTHON'
from pathlib import Path
import sys
page = Path(sys.argv[1])
fragment = Path(sys.argv[2]).read_text(encoding="utf-8")
body = fragment.split("<body>", 1)[1].split("</body>", 1)[0]
text = page.read_text(encoding="utf-8")
page.write_text(text.replace("</body>", body + "\n</body>", 1), encoding="utf-8")
PYTHON
weasyprint "$prototype_dir/index.html" "$prototype_dir/out/autonomous_assurance_whitepaper_review.pdf"
echo "Wrote $prototype_dir/index.html and $prototype_dir/out/autonomous_assurance_whitepaper_review.pdf"
