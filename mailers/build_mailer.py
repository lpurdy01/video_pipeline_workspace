"""
Assemble per-recipient mailer packets and a LetterStream batch PDF + CSV.

Packet structure:
  Page 1  — cover page: return address (top-left), recipient address (window zone),
             abstract, VRM status. Per-recipient: recipient address differs.
  Pages 2+ — whitepaper_print.pdf appended as-is.

LetterStream workflow (web UI, until API is activated):
  --batch  Merge all packets into one PDF (N × page_count pages).
           Upload to LetterStream, set "pages per recipient" to page_count,
           draw the address boxes once — LetterStream applies them to every packet.
           Set: Coversheet=Flats, Ink Color=Color (diagrams are color), Duplex=Yes.

LetterStream workflow (API, once API key is issued):
  letterstream_client.py --all
  Submits each PDF individually via POST with address fields.
  The cover page addresses are still present for human readability;
  LetterStream reads addresses from the POST fields to build the coversheet.

Color printing note:
  The whitepaper_print.pdf embeds color PNG diagrams even though most text is
  black. LetterStream supports per-page color detection. Set ink color to "Color"
  in the LetterStream UI so diagrams print in color; text-only pages are B&W cost.

Usage:
  python build_mailer.py                          # build all individual packets
  python build_mailer.py --slug aws_albarghouthi  # build one
  python build_mailer.py --batch                  # merge all into batch.pdf
  python build_mailer.py --list                   # list slugs
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from pypdf import PdfWriter, PdfReader
from weasyprint import HTML, CSS

HERE = Path(__file__).parent
DATA = HERE / "data"
OUT = HERE / "out"
WHITEPAPER_PDF_COLOR = HERE.parent / "whitepaper" / "out" / "whitepaper_print.pdf"
WHITEPAPER_PDF_BW    = HERE.parent / "whitepaper" / "out" / "whitepaper_print_bw.pdf"
WHITEPAPER_PDF = WHITEPAPER_PDF_COLOR  # overridden by --bw at runtime


# ---------------------------------------------------------------------------
# Data loaders
# ---------------------------------------------------------------------------

def load_json(path: Path) -> dict | list:
    return json.loads(path.read_text(encoding="utf-8"))

def load_config() -> dict:
    return load_json(DATA / "config.json")

def load_recipients() -> list[dict]:
    return load_json(DATA / "recipients.json")

# ---------------------------------------------------------------------------
# CSS — USPS-standard business letter address positioning
#
# Return address zone: top-left, ~0.5in from top, within 2.5in wide × 1in tall
# Recipient address zone: ~2.0in from top, left-aligned, 4 lines max
# These match LetterStream's template window positions for flat 9x12 envelopes.
# ---------------------------------------------------------------------------

CSS_COVER = """
@page {
    size: letter;
    margin: 0.5in 1.1in 0.7in 1.1in;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: Arial, Helvetica, sans-serif;
    font-size: 10.5pt;
    line-height: 1.5;
    color: #000;
}

/* ── Return address — top-left, compact ──────────────────────── */
.return-address {
    font-size: 9pt;
    line-height: 1.4;
    margin-bottom: 0.15in;
}

.return-address .ra-name {
    font-weight: bold;
    font-size: 9.5pt;
}

.return-address .ra-email {
    color: #333;
    font-size: 8.5pt;
}

.date-line {
    font-size: 9pt;
    color: #555;
    margin-bottom: 0.25in;
}

/* ── Recipient address — window zone (~2.0in from top) ────────
   Positioned so the 4-line block falls in LetterStream's flat
   envelope window after coversheet generation.
──────────────────────────────────────────────────────────────── */
.recipient-address {
    font-size: 10.5pt;
    font-weight: normal;
    line-height: 1.55;
    margin-bottom: 0.3in;
}

.recipient-address .recip-name {
    font-weight: bold;
}

/* ── Divider ─────────────────────────────────────────────────── */
hr.divider {
    border: none;
    border-top: 0.75pt solid #000;
    margin: 0.15in 0 0.22in 0;
}

/* ── Letter body ─────────────────────────────────────────────── */
.letter-body p {
    margin-bottom: 0.55em;
}

.letter-body p.gap {
    height: 0.25em;
}

.closing {
    margin-top: 0.1in;
}
"""

# ---------------------------------------------------------------------------
# HTML builder — cover page only
# ---------------------------------------------------------------------------

def letter_to_html(letter: str) -> str:
    out = []
    for line in letter.strip().split("\n"):
        s = line.strip()
        out.append(f"<p>{s}</p>" if s else '<p class="gap"></p>')
    return "\n".join(out)


def build_cover_html(r: dict, cfg: dict) -> str:
    ra = cfg["return_address"]
    paper = cfg["paper"]

    addr_lines = [f'<span class="recip-name">{r["name"]}</span>']
    for key in ["addr1", "addr2", "addr3"]:
        v = r.get(key, "").strip()
        if v:
            addr_lines.append(v)
    recipient_html = "<br>\n".join(addr_lines)

    letter_html = letter_to_html(r.get("letter", ""))

    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Cover — {r["name"]}</title></head>
<body>

<div class="return-address">
  <span class="ra-name">{ra["name"]}</span><br>
  {ra["line1"]}<br>
  {ra["line2"]}<br>
  <span class="ra-email">{ra["line3"]}</span>
</div>

<div class="date-line">{paper["date"]}</div>

<div class="recipient-address">
{recipient_html}
</div>

<div class="letter-body">
{letter_html}
</div>

</body>
</html>"""

# ---------------------------------------------------------------------------
# PDF assembly
# ---------------------------------------------------------------------------

def build_cover_pdf(r: dict, cfg: dict, out_dir: Path) -> Path:
    html_str = build_cover_html(r, cfg)
    cover_path = out_dir / "_cover.pdf"
    HTML(string=html_str, base_url=str(HERE)).write_pdf(
        str(cover_path),
        stylesheets=[CSS(string=CSS_COVER)],
    )
    return cover_path


def merge_pdfs(parts: list[Path], out_path: Path) -> int:
    writer = PdfWriter()
    for src in parts:
        reader = PdfReader(str(src))
        for page in reader.pages:
            writer.add_page(page)
    with open(out_path, "wb") as f:
        writer.write(f)
    return len(writer.pages)


def build_packet(r: dict, cfg: dict, out_dir: Path) -> tuple[Path, int]:
    out_dir.mkdir(parents=True, exist_ok=True)
    cover_pdf = build_cover_pdf(r, cfg, out_dir)
    packet_pdf = out_dir / "packet.pdf"
    total = merge_pdfs([cover_pdf, WHITEPAPER_PDF], packet_pdf)
    cover_pdf.unlink()
    return packet_pdf, total

# ---------------------------------------------------------------------------
# Batch PDF: all packets merged into one file for LetterStream batch upload
# ---------------------------------------------------------------------------

def build_batch(recipients: list[dict], cfg: dict) -> Path:
    """
    Merge all recipient packets into one PDF for LetterStream batch upload.

    In the LetterStream web UI:
      1. Upload this batch.pdf
      2. Set "# of pages per recipient" to the page count shown
      3. Draw the recipient address box (on page 1 of the first packet)
      4. Draw the return address box
      5. LetterStream applies the same box position to every packet's first page

    This is more efficient than 6 separate uploads.
    """
    pages_per = None
    batch_parts: list[Path] = []
    batch_dir = OUT / "_batch_build"
    batch_dir.mkdir(parents=True, exist_ok=True)

    for r in recipients:
        out_dir = OUT / r["slug"]
        packet_pdf = out_dir / "packet.pdf"
        if not packet_pdf.exists():
            print(f"  Building {r['slug']} first...")
            packet_pdf, total = build_packet(r, cfg, out_dir)
            if pages_per is None:
                pages_per = total
        else:
            reader = PdfReader(str(packet_pdf))
            if pages_per is None:
                pages_per = len(reader.pages)
        batch_parts.append(packet_pdf)

    suffix = "_bw" if WHITEPAPER_PDF == WHITEPAPER_PDF_BW else ""
    batch_pdf = OUT / f"batch{suffix}.pdf"
    total_pages = merge_pdfs(batch_parts, batch_pdf)

    # Clean up temp dir
    batch_dir.rmdir()

    print(f"\nBatch PDF: {batch_pdf.relative_to(HERE.parent)}")
    print(f"  {len(recipients)} recipients × {pages_per} pages = {total_pages} total pages")
    print(f"\nLetterStream web UI steps:")
    print(f"  1. Upload batch.pdf")
    print(f"  2. Set '# of Pages' = {pages_per} pages per recipient")
    print(f"  3. Draw recipient address box (top-center of address block)")
    print(f"  4. Draw return address box (top-left of return block)")
    print(f"  5. Coversheet: Flats  |  Ink Color: Color  |  Duplex: Yes")
    print(f"  6. Submit — LetterStream applies box positions to all {len(recipients)} packets")

    return batch_pdf

# ---------------------------------------------------------------------------
# Batch CSV for API submission
# ---------------------------------------------------------------------------

def export_batch_csv(recipients: list[dict], cfg: dict, out_dir: Path) -> Path:
    csv_path = out_dir / "batch_addresses.csv"
    ra = cfg["return_address"]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "slug", "recipient_name",
            "address1", "address2", "address3",
            "return_name", "return_address1", "return_address2", "return_address3",
            "pdf_file", "notes",
        ])
        writer.writeheader()
        for r in recipients:
            writer.writerow({
                "slug": r["slug"],
                "recipient_name": r["name"],
                "address1": r.get("addr1", ""),
                "address2": r.get("addr2", ""),
                "address3": r.get("addr3", ""),
                "return_name": ra["name"],
                "return_address1": ra["line1"],
                "return_address2": ra["line2"],
                "return_address3": ra.get("line3", ""),
                "pdf_file": f"out/{r['slug']}/packet.pdf",
                "notes": r.get("notes", ""),
            })
    return csv_path

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Build mailer packets")
    parser.add_argument("--slug", help="Build only this recipient slug")
    parser.add_argument("--batch", action="store_true", help="Merge all packets into out/batch.pdf")
    parser.add_argument("--list", action="store_true", help="List recipient slugs")
    parser.add_argument("--bw", action="store_true", help="Use B&W whitepaper (whitepaper_print_bw.pdf)")
    args = parser.parse_args()

    global WHITEPAPER_PDF
    if args.bw:
        WHITEPAPER_PDF = WHITEPAPER_PDF_BW

    cfg = load_config()
    recipients = load_recipients()

    if args.list:
        for r in recipients:
            notes = f"  ** {r['notes']}" if r.get("notes") else ""
            print(f"  {r['slug']:30s}  {r['name']}{notes}")
        return

    if not WHITEPAPER_PDF.exists():
        raise SystemExit(f"Whitepaper PDF not found: {WHITEPAPER_PDF}\nRun: python whitepaper/build_pdf.py --layout print")

    OUT.mkdir(parents=True, exist_ok=True)

    if args.batch:
        build_batch(recipients, cfg)
        return

    targets = [r for r in recipients if r["slug"] == args.slug] if args.slug else recipients
    if args.slug and not targets:
        raise SystemExit(f"No recipient '{args.slug}'. Use --list.")

    for r in targets:
        out_dir = OUT / r["slug"]
        print(f"Building: {r['slug']} ...", end=" ", flush=True)
        pdf, pages = build_packet(r, cfg, out_dir)
        print(f"-> {pdf.relative_to(HERE.parent)}  ({pages} pages)")

    if not args.slug:
        csv_path = export_batch_csv(recipients, cfg, OUT)
        print(f"Batch CSV: {csv_path.relative_to(HERE.parent)}")


if __name__ == "__main__":
    main()
