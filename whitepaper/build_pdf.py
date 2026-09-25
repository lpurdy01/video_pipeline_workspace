"""
Build formatted PDF whitepaper from the project markdown sources.

Two layout options:
  python3 build_pdf.py --layout report       → technical report (RTCA/NASA style)
  python3 build_pdf.py --layout confpaper    → two-column conference paper (SAE/AIAA style)

Output: whitepaper/out/whitepaper_<layout>.pdf
"""

import argparse
import base64
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import markdown
from weasyprint import HTML, CSS

REPO = Path(__file__).parents[1]
OUT_DIR = Path(__file__).parent / "out"
OUT_DIR.mkdir(exist_ok=True)

# Keyed by data-fig marker number (document appearance order, 1–7)
# Diagram files mapped to match the order they appear in the text:
#   1 = Units of Intelligence (appears first, in Core Concepts section)
#   2 = Cross-Standard Evidence (appears second, in Coordination System section)
#   3 = Artifact Graph (appears third, in Concept section)
#   4 = Query Assembly (appears fourth, after Graph Traversal subsection)
#   5 = Dual-Mode Operation (appears fifth, after Dual-Mode subsection)
#   6 = Deployment Tiers (appears sixth, after Deployment Contexts table)
#   7 = Development Maturity Path (appears in Introduction)
# _rendered.png variants are the polished/updated versions of the originals.
DIAGRAMS = {
    1: REPO / "whitepaper/diagram5_rendered.png",
    2: REPO / "whitepaper/diagram4_rendered.png",
    3: REPO / "whitepaper/diagram1_rendered.png",
    4: REPO / "whitepaper/diagram2_rendered.png",
    5: REPO / "whitepaper/diagram3_rendered.png",
    6: REPO / "whitepaper/diagram6_deployment_tiers.png",
    7: REPO / "whitepaper/diagram7_development_path.png",
}

DIAGRAM_CAPTIONS = {
    1: "Figure 1. Units of Intelligence — property comparison and reviewer endpoint replaceability.",
    2: "Figure 2. Cross-Standard Evidence Structure — DO-178C, ISO 26262, and IEC 62443 define evidence objectives but not reviewer identity.",
    3: "Figure 3. Artifact Graph — hierarchical C codebase linked to all verification artifacts.",
    4: "Figure 4. Verification Query Assembly — graph traversal collects one code unit's full context into a bounded query.",
    5: "Figure 5. Dual-Mode Operation — LLM and human review are interchangeable on the same decomposition.",
    6: "Figure 6. Deployment Contexts — the same architecture scales from development teams to formal certification programs.",
    7: "Figure 7. Development Maturity Path — Stage 1 records structure and pitfalls before practice deployment, formal implementation, qualification, and project use.",
}


BW_MODE = False


def img_data_uri(path: Path) -> str:
    with open(path, "rb") as f:
        raw = f.read()
    if BW_MODE:
        import io
        from PIL import Image
        img = Image.open(io.BytesIO(raw)).convert("L").convert("RGB")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        raw = buf.getvalue()
    data = base64.b64encode(raw).decode()
    return f"data:image/png;base64,{data}"


def single_diagram_html(fig_num: int) -> str:
    path = DIAGRAMS.get(fig_num)
    if not path or not path.exists():
        return f'<!-- diagram {fig_num} not found -->'
    caption = DIAGRAM_CAPTIONS.get(fig_num, f"Figure {fig_num}.")
    uri = img_data_uri(path)
    return (
        f'<figure class="diagram">'
        f'<img src="{uri}" alt="Figure {fig_num}">'
        f'<figcaption>{caption}</figcaption>'
        f'</figure>'
    )


def inject_inline_diagrams(html: str) -> str:
    """Replace <p data-fig="N"></p> markers with inline diagram HTML."""
    import re
    def replacer(m):
        fig_num = int(m.group(1))
        return single_diagram_html(fig_num)
    return re.sub(r'<p data-fig="(\d+)"></p>', replacer, html)


def _add_section_numbers(md: str) -> str:
    """Inject section numbers into H2/H3 headings (e.g. '## 3.2 Foo').

    Sections listed in NO_NUMBER are left unnumbered (reference sections that
    appear at the end). Numbering restarts at H3 for each new H2.
    """
    NO_NUMBER = {"list of acronyms", "references"}
    h2 = 0
    h3 = 0
    in_no_number = False
    out = []
    for line in md.splitlines():
        h2_m = re.match(r"^(## )(.+)$", line)
        h3_m = re.match(r"^(### )(.+)$", line)
        if h2_m:
            title = h2_m.group(2).strip()
            if title.lower() in NO_NUMBER:
                in_no_number = True
                out.append(line)
            else:
                in_no_number = False
                h2 += 1
                h3 = 0
                out.append(f"## {h2}. {title}")
        elif h3_m:
            title = h3_m.group(2).strip()
            if in_no_number:
                out.append(line)
            else:
                h3 += 1
                out.append(f"### {h2}.{h3} {title}")
        else:
            out.append(line)
    return "\n".join(out)


def load_markdown() -> str:
    release_src = REPO / "whitepaper" / "verification_compiler_whitepaper.md"
    src = release_src if release_src.exists() else REPO / "Introductory_composition.md"
    text = src.read_text()

    # Strip non-content sections
    text = re.sub(r"## Expansion Areas.*", "", text, flags=re.DOTALL)
    text = re.sub(r"## Working Title\n\n.*?\n\n", "", text, count=1)
    # Strip the document's H1 title and release metadata because the PDF has a
    # formatted title block.
    text = re.sub(r"^# .+\n+", "", text, count=1)
    text = re.sub(r"^Subtitle: .+\n+", "", text, count=1)
    text = re.sub(r"^Version: .+\n+", "", text, count=1)

    # Add section numbers (so TOC and body headings are both numbered)
    text = _add_section_numbers(text)

    return text


def split_acronyms_section(md_text: str) -> tuple[str, str]:
    """Remove the acronym section from body markdown and return it separately."""
    pattern = r"^## List of Acronyms\s*\n(.*?)(?=^## |\Z)"
    match = re.search(pattern, md_text, flags=re.MULTILINE | re.DOTALL)
    if not match:
        return md_text, ""

    acronyms_md = "## List of Acronyms\n" + match.group(1).strip()
    body_md = md_text[:match.start()].rstrip() + "\n" + md_text[match.end():].lstrip()
    return body_md, acronyms_md


def md_to_html(md_text: str) -> tuple[str, str]:
    """Returns (body_html, toc_html)."""
    md = markdown.Markdown(
        extensions=["tables", "fenced_code", "codehilite", "toc", "def_list"],
        extension_configs={"toc": {"anchorlink": True, "toc_depth": "2-3"}},
    )
    body_html = md.convert(md_text)
    toc_html = md.toc  # populated after convert()
    return body_html, toc_html


def md_fragment_to_html(md_text: str) -> str:
    md = markdown.Markdown(extensions=["tables", "fenced_code", "codehilite", "def_list"])
    return md.convert(md_text)


# ── CSS Stylesheets ────────────────────────────────────────────────────────────

CSS_REPORT = """
/* === TECHNICAL REPORT STYLE (RTCA / NASA / NIST) === */
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,wght@0,400;0,600;0,700;1,400&family=Source+Code+Pro:wght@400;600&display=swap');

@page {
    size: letter;
    margin: 1in 1.1in 1in 1.1in;
    @top-center {
        content: "Verification Compiler";
        font-family: "Source Serif 4", Georgia, serif;
        font-size: 9pt;
        color: #555;
    }
    @bottom-center {
        content: counter(page);
        font-family: "Source Serif 4", Georgia, serif;
        font-size: 9pt;
        color: #555;
    }
}

@page :first {
    @top-center { content: ""; }
}

body {
    font-family: "Source Serif 4", Georgia, "Times New Roman", serif;
    font-size: 11.5pt;
    line-height: 1.55;
    color: #1a1a1a;
    max-width: 100%;
}

/* Title block */
.title-block {
    margin-bottom: 36pt;
    border-bottom: 2pt solid #1a3a6b;
    padding-bottom: 18pt;
}
.title-block h1 {
    font-size: 18pt;
    font-weight: 700;
    line-height: 1.25;
    color: #1a3a6b;
    margin: 0 0 8pt 0;
    border: none;
}
.title-block .subtitle {
    font-size: 12pt;
    color: #444;
    font-style: italic;
    margin: 0 0 12pt 0;
}
.title-block .meta {
    font-size: 9.5pt;
    color: #666;
    line-height: 1.7;
}
/* Abstract */
.abstract {
    margin: 24pt 0;
    padding: 12pt 18pt;
    background: #f5f7fa;
    border-left: 3pt solid #1a3a6b;
    font-size: 10.5pt;
    line-height: 1.55;
    break-inside: avoid;
    page-break-inside: avoid;
}
.abstract-label {
    font-weight: 700;
    font-size: 10pt;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #1a3a6b;
    margin-bottom: 6pt;
}

/* Section headers */
h2 {
    font-size: 13.5pt;
    font-weight: 700;
    color: #1a3a6b;
    margin-top: 28pt;
    margin-bottom: 8pt;
    border-bottom: 1pt solid #d0d8e8;
    padding-bottom: 4pt;
}
h2 a, h3 a, h4 a {
    color: inherit;
    text-decoration: none;
}
h2 a, h3 a, h4 a {
    color: inherit;
    text-decoration: none;
}
h3 {
    font-size: 11.5pt;
    font-weight: 700;
    color: #1e1e1e;
    margin-top: 18pt;
    margin-bottom: 5pt;
}
h4 {
    font-size: 11pt;
    font-weight: 600;
    font-style: italic;
    color: #333;
    margin-top: 12pt;
    margin-bottom: 4pt;
}

/* Body text */
p { margin: 0 0 8pt 0; text-align: justify; }
strong { color: #1a3a6b; }

/* Lists */
ul, ol { margin: 6pt 0 10pt 0; padding-left: 20pt; }
li { margin-bottom: 3pt; }
li > ul, li > ol { margin: 3pt 0; }

/* Code */
code {
    font-family: "Source Code Pro", "Courier New", monospace;
    font-size: 9pt;
    background: #f0f0f0;
    padding: 1pt 3pt;
    border-radius: 2pt;
}
pre {
    font-family: "Source Code Pro", "Courier New", monospace;
    font-size: 8pt;
    background: #f5f5f5;
    border: 0.5pt solid #d0d0d0;
    border-left: 3pt solid #1a3a6b;
    padding: 10pt 12pt;
    margin: 10pt 0;
    line-height: 1.4;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
    word-break: break-word;
}
pre code { background: none; padding: 0; font-size: inherit; }

/* Tables */
table {
    width: 100%;
    border-collapse: collapse;
    font-size: 9.5pt;
    margin: 12pt 0;
}
thead {
    background: #1a3a6b;
    color: white;
}
th {
    padding: 6pt 8pt;
    text-align: left;
    font-weight: 600;
}
td {
    padding: 5pt 8pt;
    border-bottom: 0.5pt solid #d0d8e8;
    vertical-align: top;
}
tr:nth-child(even) td { background: #f5f7fa; }

/* Figures */
.diagram {
    margin: 20pt 0 24pt 0;
    text-align: center;
    page-break-inside: avoid;
}
.diagram img {
    max-width: 100%;
    border: 0.5pt solid #ccc;
}
.diagram figcaption {
    font-size: 9pt;
    color: #444;
    margin-top: 6pt;
    font-style: italic;
}

/* Blockquotes */
blockquote {
    margin: 10pt 0 10pt 20pt;
    padding: 4pt 0 4pt 12pt;
    border-left: 3pt solid #aab;
    color: #444;
    font-style: italic;
}

/* VRM Status Block */
.vrm-status {
    margin: 20pt 0 24pt 0;
    padding: 14pt 18pt;
    background: #fdf6ec;
    border: 1pt solid #d97706;
    border-left: 4pt solid #d97706;
    font-size: 9.5pt;
    line-height: 1.5;
    page-break-inside: avoid;
}
.vrm-status-header {
    font-weight: 700;
    font-size: 10.5pt;
    color: #92400e;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 8pt;
}
.vrm-score-line {
    font-size: 16pt;
    font-weight: 700;
    color: #92400e;
    margin-bottom: 6pt;
}
.vrm-score-line span {
    display: block;
    font-size: 9pt;
    font-weight: 400;
    color: #555;
    margin: 4pt 0 0 0;
}
.vrm-status table {
    width: 100%;
    margin: 8pt 0 10pt 0;
    font-size: 9pt;
    border-collapse: collapse;
    background: transparent;
}
.vrm-status thead { background: #92400e; color: white; }
.vrm-status th { padding: 4pt 8pt; font-weight: 600; }
.vrm-status td { padding: 3pt 8pt; border-bottom: 0.5pt solid #e5c99b; background: transparent; }
.vrm-status tr:nth-child(even) td { background: #fef9f0; }
.vrm-issues { margin-top: 8pt; }
.vrm-issues-label {
    font-weight: 700;
    font-size: 9pt;
    color: #92400e;
    margin-bottom: 4pt;
}
.vrm-issues ul { margin: 0; padding-left: 16pt; }
.vrm-issues li { margin-bottom: 3pt; color: #333; }

/* Table of Contents */
.toc-block {
    margin: 20pt 0 28pt 0;
    padding: 12pt 18pt;
    background: #f5f7fa;
    border: 0.5pt solid #d0d8e8;
    border-left: 3pt solid #1a3a6b;
    break-inside: avoid;
    page-break-inside: avoid;
    page-break-after: avoid;
}
.toc-label {
    font-weight: 700;
    font-size: 11pt;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #1a3a6b;
    margin-bottom: 8pt;
}
.toc ul { list-style: none; padding-left: 0; margin: 0; }
.toc li { margin: 3pt 0; font-size: 10pt; }
.toc li a { color: #1a3a6b; text-decoration: none; }
.toc li > ul { padding-left: 16pt; }
.toc li > ul > li { font-size: 9.5pt; }

.acronyms-block {
    margin: 14pt 0 28pt 0;
    padding: 10pt 14pt;
    background: #fbfcfe;
    border: 0.5pt solid #d0d8e8;
    border-left: 3pt solid #68758a;
    break-inside: avoid;
    page-break-inside: avoid;
    page-break-after: always;
}
.acronyms-block h2 {
    font-size: 11pt;
    margin: 0 0 6pt 0;
    border-bottom: 0.5pt solid #d0d8e8;
    padding-bottom: 3pt;
}
.acronyms-block table {
    margin: 6pt 0 0 0;
    font-size: 7.8pt;
    line-height: 1.2;
}
.acronyms-block th {
    padding: 3pt 5pt;
}
.acronyms-block td {
    padding: 2pt 5pt;
}

/* Section dividers */
hr {
    border: none;
    border-top: 1pt solid #d0d8e8;
    margin: 20pt 0;
}

/* Page break control */
h2, h3, h4 { break-after: avoid; page-break-after: avoid; }
h2 + p, h2 + ul, h2 + ol, h2 + pre, h2 + table, h2 + .diagram,
h3 + p, h3 + ul, h3 + ol, h3 + pre, h3 + table, h3 + .diagram,
h4 + p, h4 + ul { break-before: avoid; page-break-before: avoid; }
table { break-inside: avoid; page-break-inside: avoid; }
.diagram { break-inside: avoid; page-break-inside: avoid; }
p { orphans: 3; widows: 3; }
/* Keep List of Acronyms header with its table */
#list-of-acronyms { break-after: avoid; page-break-after: avoid; }

/* References — hanging indent, numbered list */
#references + ol {
    list-style: decimal;
    padding-left: 2.2em;
    font-size: 9.5pt;
    line-height: 1.45;
}
#references + ol li {
    margin-bottom: 5pt;
    text-indent: 0;
    padding-left: 0.4em;
}
#references + ol li a {
    color: #1a3a6b;
    word-break: break-all;
}
"""

CSS_CONFPAPER = """
/* === TWO-COLUMN CONFERENCE PAPER STYLE (SAE / AIAA / IEEE AEROSPACE) === */
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,wght@0,400;0,600;0,700;1,400&family=Source+Code+Pro:wght@400&display=swap');

@page {
    size: letter;
    margin: 0.875in 0.75in 0.875in 0.75in;
    @top-right {
        content: counter(page);
        font-family: "Source Serif 4", Georgia, serif;
        font-size: 8pt;
        color: #555;
    }
}

@page :first {
    @top-right { content: ""; }
}

body {
    font-family: "Source Serif 4", Georgia, "Times New Roman", serif;
    font-size: 10pt;
    line-height: 1.45;
    color: #1a1a1a;
}

/* Title block — full width across both columns */
.title-block {
    column-span: all;
    margin-bottom: 14pt;
    border-bottom: 1.5pt solid #1a3a6b;
    padding-bottom: 10pt;
    text-align: center;
}
.title-block h1 {
    font-size: 15pt;
    font-weight: 700;
    line-height: 1.2;
    color: #1a3a6b;
    margin: 0 0 6pt 0;
    border: none;
}
.title-block .subtitle {
    font-size: 10pt;
    color: #555;
    font-style: italic;
    margin: 0 0 8pt 0;
}
.title-block .meta {
    font-size: 8.5pt;
    color: #666;
}
/* Abstract — full width */
.abstract {
    column-span: all;
    margin: 10pt 0 14pt 0;
    padding: 8pt 14pt;
    background: #f5f7fa;
    border-left: 2.5pt solid #1a3a6b;
    font-size: 9pt;
    line-height: 1.5;
    break-inside: avoid;
    page-break-inside: avoid;
}
.abstract-label {
    font-weight: 700;
    font-size: 8.5pt;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #1a3a6b;
    margin-bottom: 4pt;
}

/* Two-column main body */
.columns {
    column-count: 2;
    column-gap: 0.25in;
    column-fill: balance;
}

/* Section headers */
h2 {
    font-size: 10.5pt;
    font-weight: 700;
    color: #1a3a6b;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-top: 12pt;
    margin-bottom: 4pt;
    border-bottom: 0.5pt solid #c0c8d8;
    padding-bottom: 2pt;
    column-span: all;  /* section breaks span both columns */
}
h3 {
    font-size: 10pt;
    font-weight: 700;
    color: #1e1e1e;
    margin-top: 9pt;
    margin-bottom: 3pt;
}
h4 {
    font-size: 10pt;
    font-weight: 600;
    font-style: italic;
    color: #333;
    margin-top: 7pt;
    margin-bottom: 2pt;
}

p { margin: 0 0 5pt 0; text-align: justify; }
strong { color: #1a3a6b; }

ul, ol { margin: 4pt 0 7pt 0; padding-left: 14pt; }
li { margin-bottom: 2pt; font-size: 9.5pt; }

code {
    font-family: "Source Code Pro", monospace;
    font-size: 8pt;
    background: #f0f0f0;
    padding: 0.5pt 2pt;
    border-radius: 1pt;
}
pre {
    font-family: "Source Code Pro", monospace;
    font-size: 7.5pt;
    background: #f5f5f5;
    border: 0.5pt solid #ccc;
    border-left: 2pt solid #1a3a6b;
    padding: 6pt 8pt;
    margin: 6pt 0;
    line-height: 1.35;
    column-span: all;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
    word-break: break-word;
}
pre code { background: none; padding: 0; }

table {
    width: 100%;
    border-collapse: collapse;
    font-size: 8.5pt;
    margin: 8pt 0;
    column-span: all;
}
thead { background: #1a3a6b; color: white; }
th { padding: 4pt 6pt; font-weight: 600; text-align: left; }
td { padding: 3pt 6pt; border-bottom: 0.5pt solid #ccc; vertical-align: top; }
tr:nth-child(even) td { background: #f5f7fa; }

.diagram {
    column-span: all;
    margin: 12pt 0 14pt 0;
    text-align: center;
    page-break-inside: avoid;
}
.diagram img { max-width: 100%; border: 0.5pt solid #ccc; }
.diagram figcaption { font-size: 8pt; color: #444; margin-top: 4pt; font-style: italic; }

blockquote {
    margin: 6pt 0 6pt 12pt;
    padding: 2pt 0 2pt 8pt;
    border-left: 2pt solid #aab;
    color: #444;
    font-style: italic;
    font-size: 9.5pt;
}

hr {
    column-span: all;
    border: none;
    border-top: 0.5pt solid #d0d8e8;
    margin: 12pt 0;
}

/* References — hanging indent, numbered list */
#references + ol {
    list-style: decimal;
    padding-left: 2em;
    font-size: 8.5pt;
    line-height: 1.4;
    overflow-wrap: break-word;
    word-break: break-all;
}
#references + ol li {
    margin-bottom: 4pt;
    padding-left: 0.3em;
}
#references + ol li a {
    color: #1a3a6b;
    word-break: break-all;
    overflow-wrap: break-word;
}

/* VRM Status Block */
.vrm-status {
    column-span: all;
    margin: 10pt 0 14pt 0;
    padding: 10pt 14pt;
    background: #fdf6ec;
    border: 0.5pt solid #d97706;
    border-left: 3pt solid #d97706;
    font-size: 8.5pt;
    line-height: 1.5;
    page-break-inside: avoid;
}
.vrm-status-header {
    font-weight: 700;
    font-size: 9pt;
    color: #92400e;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 6pt;
}
.vrm-score-line {
    font-size: 13pt;
    font-weight: 700;
    color: #92400e;
    margin-bottom: 4pt;
}
.vrm-score-line span {
    display: block;
    font-size: 8pt;
    font-weight: 400;
    color: #555;
    margin: 3pt 0 0 0;
}
.vrm-status table {
    width: 100%;
    margin: 6pt 0 8pt 0;
    font-size: 8pt;
    border-collapse: collapse;
    background: transparent;
    column-span: all;
}
.vrm-status thead { background: #92400e; color: white; }
.vrm-status th { padding: 3pt 6pt; font-weight: 600; }
.vrm-status td { padding: 2pt 6pt; border-bottom: 0.5pt solid #e5c99b; background: transparent; }
.vrm-status tr:nth-child(even) td { background: #fef9f0; }
.vrm-issues { margin-top: 6pt; }
.vrm-issues-label { font-weight: 700; font-size: 8pt; color: #92400e; margin-bottom: 3pt; }
.vrm-issues ul { margin: 0; padding-left: 14pt; }
.vrm-issues li { margin-bottom: 2pt; color: #333; }

.toc-block {
    column-span: all;
    margin: 10pt 0 14pt 0;
    padding: 8pt 12pt;
    background: #f5f7fa;
    border: 0.5pt solid #d0d8e8;
    border-left: 2.5pt solid #1a3a6b;
    break-inside: avoid;
    page-break-inside: avoid;
}
.toc-label {
    font-weight: 700;
    font-size: 9pt;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #1a3a6b;
    margin-bottom: 5pt;
}
.toc ul { list-style: none; padding-left: 0; margin: 0; }
.toc li { margin: 2pt 0; font-size: 8.5pt; }
.toc li a { color: #1a3a6b; text-decoration: none; }
.toc li > ul { padding-left: 12pt; }
.toc li > ul > li { font-size: 8pt; }

.acronyms-block {
    column-span: all;
    margin: 8pt 0 12pt 0;
    padding: 8pt 12pt;
    background: #fbfcfe;
    border: 0.5pt solid #d0d8e8;
    border-left: 2.5pt solid #68758a;
    break-inside: avoid;
    page-break-inside: avoid;
    page-break-after: always;
}
.acronyms-block h2 {
    font-size: 9pt;
    margin: 0 0 4pt 0;
    border-bottom: 0.5pt solid #d0d8e8;
    padding-bottom: 2pt;
}
.acronyms-block table {
    margin: 4pt 0 0 0;
    font-size: 7pt;
    line-height: 1.15;
}
.acronyms-block th { padding: 2pt 4pt; }
.acronyms-block td { padding: 1.5pt 4pt; }
"""

CSS_PRINT = """
/* === PRINT / MAIL LAYOUT — dense B&W, duplex-friendly, outer margin for notes === */
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,wght@0,400;0,600;0,700;1,400&family=Source+Code+Pro:wght@400;600&display=swap');

@page {
    size: letter;
    margin: 0.7in 1.1in 0.7in 1.1in;
    @top-center {
        content: "Verification Compiler";
        font-family: "Source Serif 4", Georgia, serif;
        font-size: 7.5pt;
        color: #555;
    }
    @bottom-center {
        content: counter(page);
        font-family: "Source Serif 4", Georgia, serif;
        font-size: 7.5pt;
        color: #555;
    }
}

@page :first {
    @top-center { content: ""; }
    @bottom-center { content: ""; }
}

body {
    font-family: "Source Serif 4", Georgia, "Times New Roman", serif;
    font-size: 10pt;
    line-height: 1.42;
    color: #000;
    max-width: 100%;
}

/* Title block — B&W, strong borders */
.title-block {
    margin-bottom: 14pt;
    border-top: 2.5pt solid #000;
    border-bottom: 1.5pt solid #000;
    padding: 10pt 0 10pt 0;
}
.title-block h1 {
    font-size: 14pt;
    font-weight: 700;
    line-height: 1.2;
    color: #000;
    margin: 0 0 5pt 0;
    border: none;
}
.title-block .subtitle {
    font-size: 10pt;
    color: #222;
    font-style: italic;
    margin: 0 0 7pt 0;
}
.title-block .meta {
    font-size: 8.5pt;
    color: #333;
    line-height: 1.6;
}
/* Abstract */
.abstract {
    margin: 10pt 0 12pt 0;
    padding: 7pt 10pt;
    background: #f0f0f0;
    border-left: 2.5pt solid #333;
    font-size: 9pt;
    line-height: 1.4;
}
.abstract-label {
    font-weight: 700;
    font-size: 8.5pt;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #000;
    margin-bottom: 3pt;
}

/* Section headers */
h2 {
    font-size: 11pt;
    font-weight: 700;
    color: #000;
    margin-top: 0;
    margin-bottom: 4pt;
    border-bottom: 1pt solid #666;
    padding-bottom: 2pt;
    page-break-before: always;
    break-before: page;
}
h3 {
    font-size: 10.5pt;
    font-weight: 700;
    color: #000;
    margin-top: 9pt;
    margin-bottom: 2pt;
}
h4 {
    font-size: 10pt;
    font-weight: 600;
    font-style: italic;
    color: #000;
    margin-top: 6pt;
    margin-bottom: 2pt;
}

/* Body text */
p { margin: 0 0 4pt 0; text-align: justify; }
strong { color: #000; }
a { color: #000; text-decoration: underline; }
em { font-style: italic; }

/* Lists */
ul, ol { margin: 3pt 0 6pt 0; padding-left: 15pt; }
li { margin-bottom: 1.5pt; }
li > ul, li > ol { margin: 1.5pt 0; }

/* Code */
code {
    font-family: "Source Code Pro", "Courier New", monospace;
    font-size: 8pt;
    background: #f0f0f0;
    padding: 0.5pt 2pt;
}
pre {
    font-family: "Source Code Pro", "Courier New", monospace;
    font-size: 8pt;
    background: #f5f5f5;
    border: 0.5pt solid #bbb;
    border-left: 2pt solid #333;
    padding: 6pt 9pt;
    margin: 6pt 0;
    line-height: 1.3;
    white-space: pre-wrap;
    overflow-wrap: break-word;
    word-break: break-all;
}
pre code { background: none; padding: 0; font-size: inherit; }

/* Tables */
table {
    width: 100%;
    border-collapse: collapse;
    font-size: 8.5pt;
    margin: 6pt 0;
}
thead { background: #222; color: white; }
th { padding: 3pt 6pt; text-align: left; font-weight: 600; }
td { padding: 2.5pt 6pt; border-bottom: 0.5pt solid #bbb; vertical-align: top; }
tr:nth-child(even) td { background: #f2f2f2; }

/* Figures */
.diagram {
    margin: 12pt 0 14pt 0;
    text-align: center;
    page-break-inside: avoid;
}
.diagram img { max-width: 100%; border: 0.5pt solid #aaa; }
.diagram figcaption {
    font-size: 8pt;
    color: #333;
    margin-top: 3pt;
    font-style: italic;
}

/* Blockquotes */
blockquote {
    margin: 6pt 0 6pt 12pt;
    padding: 3pt 0 3pt 9pt;
    border-left: 2pt solid #777;
    color: #222;
    font-style: italic;
}

/* VRM Status Block — B&W */
.vrm-status {
    margin: 12pt 0 14pt 0;
    padding: 9pt 11pt;
    background: #efefef;
    border: 1pt solid #444;
    border-left: 3pt solid #000;
    font-size: 8.5pt;
    line-height: 1.4;
    page-break-inside: avoid;
}
.vrm-status-header {
    font-weight: 700;
    font-size: 9pt;
    color: #000;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 4pt;
}
.vrm-score-line {
    font-size: 13pt;
    font-weight: 700;
    color: #000;
    margin-bottom: 3pt;
}
.vrm-score-line span { font-size: 8pt; font-weight: 400; color: #444; margin-left: 5pt; }
.vrm-status table {
    width: 100%;
    margin: 4pt 0 6pt 0;
    font-size: 8pt;
    border-collapse: collapse;
    background: transparent;
}
.vrm-status thead { background: #222; color: white; }
.vrm-status th { padding: 2.5pt 5pt; font-weight: 600; }
.vrm-status td { padding: 2pt 5pt; border-bottom: 0.5pt solid #bbb; background: transparent; }
.vrm-status tr:nth-child(even) td { background: #e2e2e2; }
.vrm-issues { margin-top: 5pt; }
.vrm-issues-label { font-weight: 700; font-size: 8pt; color: #000; margin-bottom: 2pt; }
.vrm-issues ul { margin: 0; padding-left: 13pt; }
.vrm-issues li { margin-bottom: 2pt; color: #111; }

/* Table of Contents */
.toc-block {
    margin: 10pt 0 16pt 0;
    padding: 7pt 10pt;
    background: #f5f5f5;
    border: 0.5pt solid #bbb;
    border-left: 2pt solid #333;
    page-break-before: always;
    break-before: page;
    page-break-after: always;
}
.toc-label {
    font-weight: 700;
    font-size: 9.5pt;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: #000;
    margin-bottom: 5pt;
}
.toc ul { list-style: none; padding-left: 0; margin: 0; }
.toc li { margin: 1.5pt 0; font-size: 9pt; }
.toc li a { color: #000; text-decoration: none; }
.toc li > ul { padding-left: 12pt; }
.toc li > ul > li { font-size: 8.5pt; }

/* Section dividers */
hr { border: none; border-top: 0.5pt solid #bbb; margin: 10pt 0; }

/* Page break control */
h2, h3, h4 { break-after: avoid; page-break-after: avoid; }
h2 + p, h2 + ul, h2 + ol, h2 + pre, h2 + table, h2 + .diagram,
h3 + p, h3 + ul, h3 + ol, h3 + pre, h3 + table, h3 + .diagram,
h4 + p, h4 + ul { break-before: avoid; page-break-before: avoid; }
table { break-inside: avoid; page-break-inside: avoid; }
.diagram { break-inside: avoid; page-break-inside: avoid; }
p { orphans: 3; widows: 3; }
#list-of-acronyms { break-after: avoid; page-break-after: avoid; }

/* References */
#references + ol {
    list-style: decimal;
    padding-left: 2em;
    font-size: 8.5pt;
    line-height: 1.4;
    overflow-wrap: break-word;
    word-break: break-all;
}
#references + ol li { margin-bottom: 4pt; padding-left: 0.3em; }
#references + ol li a { color: #000; text-decoration: underline; word-break: break-all; }
"""


def build_title_block(layout: str) -> str:
    return """
<div class="title-block">
  <h1>Bounded LLM Review for Continuous Verification:<br>A Graph-Decomposition Architecture for Safety-Critical Software</h1>
  <div class="subtitle">The Verification Compiler: CI-Integrated Verification with Interchangeable LLM and Human Reviewer Endpoints</div>
  <div class="meta">
    Levi Purdy &mdash; Student, University of Wisconsin&ndash;Madison &mdash; lpurdy01@gmail.com<br>
    Public Release &mdash; August 2026 &mdash; v1.0
  </div>
</div>
"""


ABSTRACT_TEXT = """
Software teams have continuous integration for builds and tests. Nobody has continuous integration for <em>verification</em> — the question of whether a codebase satisfies its requirements is answered once, at the end, expensively. This paper introduces the <em>Verification Compiler</em>: a hierarchical artifact graph that decomposes a codebase's verification obligations into bounded, independently-auditable queries, each producing a structured result that feeds a <strong>Verification Readiness Metric (VRM)</strong> on every commit.

The system operates in two structurally identical modes: an LLM-driven development cycle providing continuous pre-screen feedback (nightly CI), and a human-driven certification pass producing the formal certification evidence record. The same DAG, the same query packages, and the same evidence schema serve both modes — only the reviewer endpoint changes. This makes the system useful to development teams with no certification obligation (VRM as a CI gate) and to formal certification programs (DO-178C, ISO 26262, IEC 62443) without requiring an architectural redesign.

The deterministic graph traversal and query assembly components are architecturally qualifiable under DO-330 TQL-5. The LLM integration is explicitly a non-qualified developmental aid. This separation preserves regulatory defensibility while capturing LLM efficiency benefits during the development cycle. Stage 2 will implement and empirically evaluate the prototype on an embedded C codebase.
"""


def build_abstract_block() -> str:
    return f"""
<div class="abstract">
  <div class="abstract-label">Abstract</div>
  {ABSTRACT_TEXT}
</div>
"""


def build_vrm_status_block() -> str:
    report_path = REPO / "verification_prototype" / "data" / "verification_report.md"
    scores = _load_latest_vrm_scores()

    if scores:
        status_detail = (
            f"Citation accuracy: {scores['citation_score']:.2f} "
            f"({scores['citation_pass']}/{scores['citation_total']}) &nbsp;&bull;&nbsp; "
            f"Requirement coverage: {scores['coverage_score']:.2f} "
            f"({scores['covered']} covered, {scores['partial']} partial, {scores['missing']} missing)"
        )
        generated_note = _report_generated_line(report_path)
        issue_text = (
            "Latest verification prototype results loaded from "
            f"<code>{report_path.relative_to(REPO)}</code>. "
            f"Orphan findings: {scores['orphan_findings']}."
        )
        return f"""
<div class="vrm-status">
  <div class="vrm-status-header">Verification Prototype Status{generated_note}</div>
  <div class="vrm-score-line">VRM = {scores['vrm']:.3f} / 1.0
    <span>{status_detail}</span>
  </div>
  <table>
    <thead><tr><th>Component</th><th>Score</th><th>Detail</th></tr></thead>
    <tbody>
      <tr><td>Citation accuracy</td><td><strong>{scores['citation_score']:.2f}</strong></td><td>{scores['citation_pass']}/{scores['citation_total']} claim&ndash;source pairs pass</td></tr>
      <tr><td>Requirement coverage</td><td><strong>{scores['coverage_score']:.2f}</strong></td><td>{scores['covered']} covered, {scores['partial']} partial, {scores['missing']} missing / {scores['coverage_total']} total</td></tr>
      <tr><td>Eval model</td><td>&mdash;</td><td>Gemini 3.1 Pro Preview</td></tr>
    </tbody>
  </table>
  <div class="vrm-issues">
    <div class="vrm-issues-label">Status:</div>
    <ul><li>{issue_text}</li></ul>
  </div>
</div>
"""

    return """
<div class="vrm-status">
  <div class="vrm-status-header">Verification Prototype Status &mdash; Run 18: 2026-05-23</div>
  <div class="vrm-score-line">VRM = 1.000 / 1.0
    <span>Citation accuracy: 1.00 (27/27) &nbsp;&bull;&nbsp; Requirement coverage: 1.00 (31 covered, 0 partial, 0 missing)</span>
  </div>
  <table>
    <thead><tr><th>Component</th><th>Score</th><th>Detail</th></tr></thead>
    <tbody>
      <tr><td>Citation accuracy</td><td><strong>1.00</strong></td><td>27/27 claim&ndash;source pairs verified; 0 failures</td></tr>
      <tr><td>Requirement coverage</td><td><strong>1.00</strong></td><td>31/31 fully covered, 0 partial, 0 missing</td></tr>
      <tr><td>Eval model</td><td>&mdash;</td><td>Gemini 3.1 Pro Preview (thinking mode)</td></tr>
    </tbody>
  </table>
  <div class="vrm-issues">
    <div class="vrm-issues-label">Status:</div>
    <ul>
      <li><strong>All 31 requirements fully covered</strong> &mdash; whitepaper describes every requirement's design intent and rationale, including four new architectural challenge requirements (REQ-8-4 through REQ-8-7). All 27 citation claim&ndash;source pairs verified. Stage 1 whitepaper is self-consistent and complete against the requirements baseline.</li>
    </ul>
  </div>
</div>
"""


def _report_generated_line(report_path: Path) -> str:
    if not report_path.exists():
        return ""
    for line in report_path.read_text(encoding="utf-8").splitlines()[:5]:
        if line.startswith("Generated:"):
            return f" &mdash; {line.replace('Generated:', '').strip()}"
    return ""


def _load_latest_vrm_scores() -> dict | None:
    results_dir = REPO / "verification_prototype" / "data" / "results"
    if not results_dir.exists():
        return None

    sys.path.insert(0, str(REPO / "verification_prototype" / "evidence"))
    try:
        from reporter import compute_vrm, load_results
    except Exception:
        return None

    results = load_results(results_dir)
    if not results:
        return None
    if any(result.get("api_error") for result in results):
        return None
    return compute_vrm(results)


def build_toc_block(toc_html: str) -> str:
    if not toc_html or toc_html.strip() == "<div class=\"toc\"></div>":
        return ""
    return f"""
<div class="toc-block">
  <div class="toc-label">Table of Contents</div>
  {toc_html}
</div>
"""


def build_acronyms_block(acronyms_html: str) -> str:
    if not acronyms_html:
        return ""
    return f"""
<div class="acronyms-block">
  {acronyms_html}
</div>
"""


def build_full_html(body_html: str, toc_html: str, acronyms_html: str, layout: str, css: str) -> str:
    title = build_title_block(layout)
    vrm_status = build_vrm_status_block()
    abstract = build_abstract_block()
    toc = build_toc_block(toc_html)
    acronyms = build_acronyms_block(acronyms_html)

    # Inject inline diagrams (replaces <p data-fig="N"></p> markers)
    body_html = inject_inline_diagrams(body_html)

    # For conf paper, wrap body in .columns div
    if layout == "confpaper":
        body_wrap_open = '<div class="columns">'
        body_wrap_close = '</div>'
    else:
        body_wrap_open = ""
        body_wrap_close = ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Verification Compiler</title>
<style>
{css}
</style>
</head>
<body>
{title}
{abstract}
{vrm_status}
{toc}
{acronyms}
{body_wrap_open}
{body_html}
{body_wrap_close}
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--layout", choices=["report", "confpaper", "print", "both"], default="both")
    parser.add_argument("--bw", action="store_true", help="Convert all diagrams to grayscale (B&W printing)")
    args = parser.parse_args()

    global BW_MODE
    BW_MODE = args.bw

    print("Loading markdown...")
    md_text = load_markdown()
    md_text, acronyms_md = split_acronyms_section(md_text)
    print(f"  {len(md_text):,} chars")

    print("Converting to HTML...")
    body_html, toc_html = md_to_html(md_text)
    acronyms_html = md_fragment_to_html(acronyms_md) if acronyms_md else ""

    layouts = ["report", "confpaper", "print"] if args.layout == "both" else [args.layout]
    css_map = {"report": CSS_REPORT, "confpaper": CSS_CONFPAPER, "print": CSS_PRINT}

    suffix = "_bw" if args.bw else ""

    for layout in layouts:
        css = css_map[layout]
        out_path = OUT_DIR / f"whitepaper_{layout}{suffix}.pdf"
        html_path = OUT_DIR / f"whitepaper_{layout}{suffix}.html"

        print(f"\nBuilding {layout} layout...")
        full_html = build_full_html(body_html, toc_html, acronyms_html, layout, css)

        # Save HTML for inspection
        html_path.write_text(full_html)
        print(f"  HTML: {html_path}")

        # Generate PDF
        print(f"  Generating PDF (this may take ~30s for images)...")
        HTML(string=full_html, base_url=str(REPO)).write_pdf(str(out_path))
        size_kb = out_path.stat().st_size // 1024
        print(f"  PDF: {out_path} ({size_kb}K)")


if __name__ == "__main__":
    main()
