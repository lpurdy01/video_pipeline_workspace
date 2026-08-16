"""
Send rendered PDF pages to Gemini for visual formatting review.

Usage:
    python3 whitepaper/gemini_tools/visual_review.py \
        [--pages-dir whitepaper/out/pages] \
        [--out whitepaper/gemini_tools/out/visual_review_YYYYMMDD.md] \
        [--model models/gemini-2.5-pro] \
        [--batch-size 6]
"""
from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from gemini_client import generate_content, image_part

REPO = Path(__file__).resolve().parents[2]
DEFAULT_OUT = Path(__file__).parent / "out" / f"visual_review_{date.today().isoformat()}.md"
DEFAULT_PAGES = REPO / "whitepaper/out/pages"
DEFAULT_MODEL = "models/gemini-2.5-pro"

SYSTEM_PROMPT = """\
You are reviewing rendered pages of a technical whitepaper PDF for visual and layout quality.
The pages are from a single-column technical report format (US Letter, ~1 inch margins).

For each batch of pages you receive, report:
1. Page numbers with BAD PAGE BREAKS — where a section header is isolated at the bottom of a page, a figure is split across pages, a table is split awkwardly, or a paragraph is orphaned/widowed.
2. Figures/diagrams that OVERFLOW their container, clip text, or are too small to read.
3. FORMATTING ERRORS — inconsistent spacing, garbled text, overlapping elements, missing content.
4. ANYTHING THAT LOOKS WRONG or would embarrass a professional reader.

Be specific: "Page 7 — Figure 3 caption is clipped at the right margin" is useful.
"Pages look OK" is not useful. If a page range has no issues, say "Pages X-Y: no issues found."

Format your response as a structured list organized by page number.
"""


def review_batch(pages: list[Path], model: str, batch_label: str) -> str:
    parts: list[dict] = [{"text": f"{SYSTEM_PROMPT}\n\nBatch: {batch_label}\n\nReview these pages:"}]
    for p in pages:
        parts.append(image_part(p))
    parts.append({"text": "Report all layout issues found in this batch:"})
    return generate_content(model, parts, timeout=180)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pages-dir", type=Path, default=DEFAULT_PAGES)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--batch-size", type=int, default=6)
    args = parser.parse_args()

    pages = sorted(args.pages_dir.glob("page-*.png"))
    if not pages:
        raise SystemExit(f"No pages found in {args.pages_dir}")

    print(f"Found {len(pages)} pages, reviewing in batches of {args.batch_size}...")
    print(f"Model: {args.model}")

    results: list[str] = [f"# Visual Layout Review\n\nGenerated: {date.today()}\nModel: {args.model}\nPages: {len(pages)}\n"]

    for i in range(0, len(pages), args.batch_size):
        batch = pages[i : i + args.batch_size]
        page_nums = f"pages {i+1}–{min(i+args.batch_size, len(pages))}"
        print(f"  Reviewing {page_nums}...")
        try:
            response = review_batch(batch, args.model, page_nums)
            results.append(f"## {page_nums.title()}\n\n{response}\n")
        except Exception as e:
            results.append(f"## {page_nums.title()}\n\nERROR: {e}\n")

    output = "\n".join(results)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(output)
    print(f"\nReview saved: {args.out}")
    print("\n--- REVIEW PREVIEW (first 40 lines) ---")
    for line in output.splitlines()[:40]:
        print(line)


if __name__ == "__main__":
    main()
