#!/usr/bin/env python3
"""Convert a text-bearing PDF into a provenance-preserving CrossPoint EPUB."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import shutil
import subprocess
import sys
import textwrap
import zipfile
from dataclasses import dataclass
from html import escape
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET

TOOL_VERSION = "1.0.0"
DEFAULT_PROMPTS = (
    "What claim, decision, assumption, or uncertainty on this source page needs attention?",
    "Does the wording preserve the source's scope, date, and stated limits?",
    "If you bookmark this point, record the PDF page number shown at the top of the chapter.",
)


@dataclass(frozen=True)
class ExtractedPage:
    number: int
    paragraphs: tuple[str, ...]
    text_sha256: str
    extraction_method: str = "pdftotext"
    warnings: tuple[str, ...] = ()

    @property
    def character_count(self) -> int:
        return sum(map(len, self.paragraphs))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def command(args: list[str]) -> str:
    completed = subprocess.run(args, text=True, capture_output=True, check=False)
    if completed.returncode:
        raise RuntimeError(f"{args[0]} failed: {completed.stderr.strip() or 'no diagnostic output'}")
    return completed.stdout


def pdf_info(pdf_path: Path) -> dict[str, str]:
    missing = [tool for tool in ("pdfinfo", "pdftotext") if shutil.which(tool) is None]
    if missing:
        raise RuntimeError("Missing required command(s): " + ", ".join(missing))
    result = {}
    for line in command(["pdfinfo", str(pdf_path)]).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()
    try:
        if int(result["Pages"]) < 1:
            raise ValueError
    except (KeyError, ValueError) as error:
        raise RuntimeError("pdfinfo did not report a valid page count") from error
    return result


def reflow_paragraphs(text: str) -> tuple[str, ...]:
    """Retain every non-whitespace character while making PDF line wraps readable."""
    paragraphs, current = [], []
    for source_line in text.replace("\r\n", "\n").replace("\r", "\n").splitlines():
        line = re.sub(r"\s+", " ", source_line).strip()
        if line:
            current.append(line)
        elif current:
            paragraphs.append(" ".join(current))
            current = []
    if current:
        paragraphs.append(" ".join(current))
    return tuple(paragraphs)


def extract_pages(pdf_path: Path, count: int) -> list[ExtractedPage]:
    """Extract in PDF block order, with OCR only for text-empty pages.

    PDF text order is not guaranteed.  A detected multi-column page is read
    column-by-column and marked for review in the manifest rather than treated
    as an unqualified transcription.
    """
    try:
        import fitz  # PyMuPDF: available in the project authoring environment.
    except ImportError:
        return extract_pages_pdftotext(pdf_path, count)

    pages = []
    document = fitz.open(pdf_path)
    try:
        for number, page in enumerate(document, start=1):
            blocks = [block for block in page.get_text("blocks", sort=False) if len(block) >= 5 and block[4].strip()]
            ordered, warnings = ordered_text_blocks(blocks, page.rect.width)
            raw = "\n\n".join(block[4] for block in ordered)
            paragraphs = reflow_paragraphs(raw)
            method = "pymupdf_blocks"
            if len("".join(paragraphs)) < 40 and shutil.which("tesseract"):
                pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2), colorspace=fitz.csGRAY, alpha=False)
                ocr = subprocess.run(
                    ["tesseract", "stdin", "stdout", "--psm", "3"], input=pixmap.tobytes("png"), capture_output=True, check=False
                )
                if ocr.returncode == 0:
                    paragraphs = reflow_paragraphs(ocr.stdout.decode("utf-8", errors="replace"))
                    method = "tesseract_ocr"
                    warnings.append("ocr_used_verify_against_source_image")
            if not paragraphs:
                warnings.append("no_extractable_text")
            pages.append(ExtractedPage(number, paragraphs, hashlib.sha256("\n\n".join(paragraphs).encode()).hexdigest(), method, tuple(warnings)))
    finally:
        document.close()
    return pages


def extract_pages_pdftotext(pdf_path: Path, count: int) -> list[ExtractedPage]:
    pages = []
    for number in range(1, count + 1):
        raw = command(["pdftotext", "-enc", "UTF-8", "-nopgbrk", "-f", str(number), "-l", str(number), str(pdf_path), "-"])
        paragraphs = reflow_paragraphs(raw)
        pages.append(ExtractedPage(number, paragraphs, hashlib.sha256("\n\n".join(paragraphs).encode()).hexdigest(), "pdftotext_fallback"))
    return pages


def ordered_text_blocks(blocks: list[tuple], page_width: float) -> tuple[list[tuple], list[str]]:
    """Apply a conservative two-column reading-order repair when clearly safe."""
    normal = sorted(blocks, key=lambda block: (block[1], block[0]))
    narrow = [block for block in blocks if block[2] - block[0] < page_width * 0.58]
    left = [block for block in narrow if block[0] < page_width * 0.42]
    right = [block for block in narrow if block[0] > page_width * 0.42]
    if len(left) < 3 or len(right) < 3:
        return normal, []
    top = min(min(block[1] for block in left), min(block[1] for block in right))
    bottom = max(max(block[3] for block in left), max(block[3] for block in right))
    headers = [block for block in blocks if block not in narrow and block[3] <= top]
    footers = [block for block in blocks if block not in narrow and block[1] >= bottom]
    middle = [block for block in blocks if block not in narrow and block not in headers and block not in footers]
    # A full-width middle block could be a table/figure caption. Preserve it in
    # vertical order but flag the page; the reviewer must check visual context.
    return (
        sorted(headers, key=lambda block: (block[1], block[0]))
        + sorted(left, key=lambda block: (block[1], block[0]))
        + sorted(middle, key=lambda block: (block[1], block[0]))
        + sorted(right, key=lambda block: (block[1], block[0]))
        + sorted(footers, key=lambda block: (block[1], block[0])),
        ["two_column_reading_order_repaired_verify_against_source_layout"],
    )


def xhtml(title: str, body: str) -> str:
    return """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml"><head><title>{}</title>
<link rel="stylesheet" type="text/css" href="../styles/review.css" /></head><body>{}</body></html>
""".format(escape(title), body)


def intro_xhtml(title: str, source_name: str, source_hash: str, prompts: Iterable[str]) -> str:
    prompt_items = "".join(
        f'<p class="review-step"><b>{number}.</b> {escape(prompt)}</p>' for number, prompt in enumerate(prompts, start=1)
    )
    body = f"""
<h1>{escape(title)}</h1>
<p class="locator">Review copy generated from <b>{escape(source_name)}</b>.</p>
<p class="locator">Original PDF SHA-256: {source_hash}</p>
<p>This EPUB is a reader-friendly transcription organized by original PDF page. The chapter heading and bookmark location are the authoritative source locator. Formatting, figures, columns, and footnotes can change during extraction, so use the original PDF whenever visual layout matters.</p>
<h2>On-device review workflow</h2><p class="review-step"><b>1.</b> Use the table of contents to jump to a source PDF page.</p><p class="review-step"><b>2.</b> Bookmark any page that needs a decision, correction, or follow-up.</p><p class="review-step"><b>3.</b> Use a screenshot for a visual handoff when useful.</p><p class="review-step"><b>4.</b> Report the PDF page number with the bookmark or screenshot; the machine-readable manifest beside this EPUB records the matching text hash.</p>
<h2>Review prompts</h2>{prompt_items}
<p class="warning">CrossPoint supports bookmarks and screenshots, not in-book highlights or typed annotations. This package makes review locations stable; it does not capture a decision automatically.</p>
"""
    return xhtml(title, textwrap.dedent(body))


def page_xhtml(page: ExtractedPage, source_hash: str) -> str:
    content = "".join(f"<p>{escape(paragraph)}</p>" for paragraph in page.paragraphs)
    if not content:
        content = '<p class="warning">No extractable text was returned for this source page. Consult the original PDF.</p>'
    return xhtml(
        f"Source PDF page {page.number}",
        f"<h1>Source PDF page {page.number}</h1>"
        f'<p class="locator">Locator: PDF p. {page.number}</p>'
        '<p class="notice">Reflowed text extracted from this one PDF page. It is not a visual facsimile; verify layout-dependent material against the original PDF.</p>'
        f"{content}<p class='review'>Review cue: bookmark this chapter to retain the stable source locator PDF p. {page.number}.</p>",
    )


CSS = """body { margin-left: 0; margin-right: 0; }
h1 { text-align: left; font-weight: bold; margin-bottom: 0.8em; }
h2 { text-align: left; font-weight: bold; margin-top: 1.2em; }
p { text-align: left; margin-top: 0; margin-bottom: 0.8em; }
.locator, .notice, .review { font-style: italic; }
.warning { font-weight: bold; margin-top: 1.0em; }
li { text-align: left; margin-bottom: 0.5em; }
.review-step { text-align: left; margin-top: 0; margin-bottom: 0.8em; }
"""


def content_opf(title: str, author: str, language: str, source_hash: str, count: int) -> str:
    manifest = [
        '<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>',
        '<item id="css" href="styles/review.css" media-type="text/css"/>',
        '<item id="intro" href="text/intro.xhtml" media-type="application/xhtml+xml"/>',
    ]
    spine = ['<itemref idref="intro"/>']
    for number in range(1, count + 1):
        identifier = f"p{number:04d}"
        manifest.append(f'<item id="{identifier}" href="text/page-{number:04d}.xhtml" media-type="application/xhtml+xml"/>')
        spine.append(f'<itemref idref="{identifier}"/>')
    return f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="book-id" version="2.0"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:title>{escape(title)}</dc:title><dc:creator>{escape(author)}</dc:creator><dc:language>{escape(language)}</dc:language><dc:identifier id="book-id">urn:sha256:{source_hash}</dc:identifier>
</metadata><manifest>{''.join(manifest)}</manifest><spine toc="ncx">{''.join(spine)}</spine></package>
"""


def toc_ncx(title: str, author: str, source_hash: str, count: int) -> str:
    points = ['<navPoint id="intro" playOrder="1"><navLabel><text>Review guide</text></navLabel><content src="text/intro.xhtml"/></navPoint>']
    for number in range(1, count + 1):
        points.append(f'<navPoint id="p{number:04d}" playOrder="{number + 1}"><navLabel><text>Source PDF page {number}</text></navLabel><content src="text/page-{number:04d}.xhtml"/></navPoint>')
    return f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1"><head><meta name="dtb:uid" content="urn:sha256:{source_hash}"/><meta name="dtb:depth" content="1"/></head><docTitle><text>{escape(title)}</text></docTitle><docAuthor><text>{escape(author)}</text></docAuthor><navMap>{''.join(points)}</navMap></ncx>
"""


def write_epub(epub_path: Path, title: str, author: str, language: str, source_name: str, source_hash: str, pages: list[ExtractedPage], prompts: Iterable[str]) -> None:
    entries = {
        "META-INF/container.xml": """<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>""",
        "OEBPS/content.opf": content_opf(title, author, language, source_hash, len(pages)),
        "OEBPS/toc.ncx": toc_ncx(title, author, source_hash, len(pages)),
        "OEBPS/styles/review.css": CSS,
        "OEBPS/text/intro.xhtml": intro_xhtml(title, source_name, source_hash, prompts),
    }
    entries.update({f"OEBPS/text/page-{page.number:04d}.xhtml": page_xhtml(page, source_hash) for page in pages})
    with zipfile.ZipFile(epub_path, "w") as archive:
        archive.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        for path, data in entries.items():
            archive.writestr(path, data, compress_type=zipfile.ZIP_DEFLATED)


def validate_epub(epub_path: Path) -> None:
    """Structural checks that can run without a device or epubcheck."""
    with zipfile.ZipFile(epub_path) as archive:
        names = archive.namelist()
        if not names or names[0] != "mimetype" or archive.getinfo("mimetype").compress_type != zipfile.ZIP_STORED:
            raise RuntimeError("EPUB has no valid first, uncompressed mimetype entry")
        if archive.read("mimetype") != b"application/epub+zip":
            raise RuntimeError("EPUB mimetype entry is invalid")
        root = ET.fromstring(archive.read("META-INF/container.xml"))
        rootfile = root.find(".//{urn:oasis:names:tc:opendocument:xmlns:container}rootfile")
        if rootfile is None or rootfile.attrib.get("full-path") != "OEBPS/content.opf":
            raise RuntimeError("EPUB container has no OEBPS/content.opf rootfile")
        opf = ET.fromstring(archive.read("OEBPS/content.opf"))
        namespace = "{http://www.idpf.org/2007/opf}"
        manifest = opf.find(namespace + "manifest")
        spine = opf.find(namespace + "spine")
        if manifest is None or spine is None:
            raise RuntimeError("EPUB OPF lacks manifest or spine")
        hrefs = {item.attrib["id"]: item.attrib["href"] for item in manifest.findall(namespace + "item")}
        for itemref in spine.findall(namespace + "itemref"):
            if itemref.attrib["idref"] not in hrefs or "OEBPS/" + hrefs[itemref.attrib["idref"]] not in names:
                raise RuntimeError(f"EPUB spine entry {itemref.attrib['idref']!r} has no package file")


def preview_html(title: str, pages: list[ExtractedPage], source_hash: str) -> str:
    screens = []
    for page in pages:
        paragraphs = "".join(f"<p>{escape(paragraph)}</p>" for paragraph in page.paragraphs) or "<p>[No extractable text]</p>"
        screens.append(f'<section class="screen"><h1>Source PDF page {page.number}</h1><p class="locator">PDF p. {page.number} · {source_hash[:12]}…</p>{paragraphs}</section>')
    return f"""<!doctype html><html><head><meta charset="utf-8"/><title>{escape(title)} preview</title><style>body{{background:#ddd;font-family:serif;margin:0;padding:24px}}header{{max-width:800px;margin:auto auto 24px}}.screen{{box-sizing:border-box;background:#f8f8f0;border:12px solid #222;min-height:480px;width:800px;padding:30px 50px;margin:24px auto;box-shadow:0 2px 8px #777}}h1{{font-size:27px}}p{{font-size:20px;line-height:1.35}}.locator{{font-size:15px;font-style:italic}}</style></head><body><header><h1>{escape(title)} — review preview</h1><p>This previews generated reflow at an 800×480 viewport. It is not a CrossPoint firmware or e-ink display emulator.</p></header>{''.join(screens)}</body></html>"""


def safe_stem(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower() or "review"


def build_package(args: argparse.Namespace) -> tuple[Path, Path, Path]:
    pdf_path = args.pdf.resolve()
    if not pdf_path.is_file():
        raise RuntimeError(f"PDF does not exist: {pdf_path}")
    info = pdf_info(pdf_path)
    title = args.title or info.get("Title") or pdf_path.stem.replace("_", " ").replace("-", " ")
    author = args.author or info.get("Author") or "Unknown author"
    source_hash = sha256_file(pdf_path)
    pages = extract_pages(pdf_path, int(info["Pages"]))
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = safe_stem(args.stem or pdf_path.stem)
    epub_path, manifest_path, preview_path = (output_dir / f"{stem}-review.epub", output_dir / f"{stem}-review.manifest.json", output_dir / f"{stem}-review-preview.html")
    if not args.overwrite:
        present = [str(path) for path in (epub_path, manifest_path, preview_path) if path.exists()]
        if present:
            raise RuntimeError("Refusing to overwrite " + ", ".join(present) + "; pass --overwrite.")
    prompts = tuple(args.review_prompt) if args.review_prompt else DEFAULT_PROMPTS
    write_epub(epub_path, title, author, args.language, pdf_path.name, source_hash, pages, prompts)
    validate_epub(epub_path)
    manifest = {
        "schema_version": 1, "tool": "pdf_to_crosspoint_epub", "tool_version": TOOL_VERSION,
        "generated_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "source": {"filename": pdf_path.name, "sha256": source_hash, "page_count": len(pages)},
        "epub": {"filename": epub_path.name, "sha256": sha256_file(epub_path), "profile": "CrossPoint static EPUB 2"},
        "extraction": {"engine": "pdftotext -enc UTF-8 -nopgbrk, one invocation per source page", "reflow": "whitespace-normalized lines joined within blank-line-delimited paragraphs"},
        "pages": [
            {
                "pdf_page": page.number,
                "character_count": page.character_count,
                "text_sha256": page.text_sha256,
                "extraction_method": page.extraction_method,
                "warnings": list(page.warnings),
            }
            for page in pages
        ],
        "limitations": ["The EPUB reflows extracted text and is not a PDF facsimile.", "Columns, figures, equations, and visual footnote placement require checking the original PDF.", "CrossPoint bookmarks and screenshots are manual review evidence; no annotation or decision is synchronized from the device."],
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    preview_path.write_text(preview_html(title, pages, source_hash), encoding="utf-8")
    return epub_path, manifest_path, preview_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path, help="input PDF; it must contain extractable text")
    parser.add_argument("--output-dir", type=Path, default=Path("out/crosspoint_review"))
    parser.add_argument("--title")
    parser.add_argument("--author")
    parser.add_argument("--language", default="en")
    parser.add_argument("--stem")
    parser.add_argument("--review-prompt", action="append")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    try:
        paths = build_package(args)
    except RuntimeError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    for label, path in zip(("EPUB", "Manifest", "Preview"), paths):
        print(f"{label}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
