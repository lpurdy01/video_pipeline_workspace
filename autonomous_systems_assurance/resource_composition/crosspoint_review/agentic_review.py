#!/usr/bin/env python3
"""Produce local and opt-in model review records for a CrossPoint EPUB conversion.

The reviewer never edits extracted content. It reports layout/extraction risks and
routes them to a deterministic rebuild or a human source-layout check. Cloud
review is deliberately opt-in because arbitrary PDFs may carry rights-sensitive
content.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

TOOL_VERSION = "1.1.0"


def issue(page: int | None, severity: str, category: str, evidence: str, action: str) -> dict[str, Any]:
    return {"page": page, "severity": severity, "category": category, "evidence": evidence, "suggested_action": action}


def local_review(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for page in manifest["pages"]:
        number, chars = page["pdf_page"], page["character_count"]
        for warning in page.get("warnings", []):
            severity = "high" if warning == "no_extractable_text" else "medium"
            action = "Run OCR or retain a source-image companion, then compare to the source page." if warning == "no_extractable_text" else "Inspect this source page against its PDF image before accepting reading order."
            issues.append(issue(number, severity, "extraction", warning, action))
        if page.get("extraction_method") == "tesseract_ocr":
            issues.append(issue(number, "medium", "ocr", "OCR text can misrecognize symbols, equations, or tables.", "Human-check quoted, numeric, mathematical, and tabular material against the source image."))
        if chars < 80:
            issues.append(issue(number, "high", "coverage", f"Only {chars} extracted characters.", "Treat as image/layout-first content; do not rely on the reflowed chapter alone."))
        if chars > 5500:
            issues.append(issue(number, "medium", "density", f"{chars} extracted characters on one source page.", "Split dense source material by semantic section only after a source-preserving review."))
    return issues


def source_renders(pdf_path: Path, output_dir: Path, dpi: int = 144) -> list[Path]:
    try:
        import fitz
    except ImportError as error:
        raise RuntimeError("PyMuPDF is required to render source-review images.") from error
    output_dir.mkdir(parents=True, exist_ok=True)
    document = fitz.open(pdf_path)
    try:
        scale = dpi / 72
        rendered = []
        for number, page in enumerate(document, start=1):
            path = output_dir / f"source-page-{number:04d}.png"
            page.get_pixmap(matrix=fitz.Matrix(scale, scale), colorspace=fitz.csGRAY, alpha=False).save(path)
            rendered.append(path)
        return rendered
    finally:
        document.close()


def review_simulator_bmp(path: Path, expected_width: int, expected_height: int) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Check a firmware-rendered BMP without interpreting or changing its text.

    This is deliberately conservative: it establishes that the simulator emitted
    a nonblank frame at the expected X4 Pro logical size. Source-fidelity and
    semantic questions remain in the page review queue (or its opt-in model pass).
    """
    data = path.read_bytes()
    record: dict[str, Any] = {
        "path": str(path),
        "sha256": hashlib.sha256(data).hexdigest(),
        "bytes": len(data),
    }
    issues: list[dict[str, Any]] = []
    if len(data) < 54 or data[:2] != b"BM":
        issues.append(issue(None, "high", "simulator_capture", "Not a readable BMP capture.", "Re-run the scripted simulator capture before accepting device-layout QA."))
        return record, issues
    pixel_offset = struct.unpack_from("<I", data, 10)[0]
    width, height = struct.unpack_from("<ii", data, 18)
    bits_per_pixel = struct.unpack_from("<H", data, 28)[0]
    record.update({"width": width, "height": abs(height), "bits_per_pixel": bits_per_pixel})
    if (width, abs(height)) != (expected_width, expected_height):
        issues.append(issue(None, "high", "simulator_geometry", f"Capture is {width}x{abs(height)}, expected {expected_width}x{expected_height}.", "Check the X4 Pro simulator profile and capture backend before using this image as layout evidence."))
    if bits_per_pixel != 32 or pixel_offset >= len(data):
        issues.append(issue(None, "medium", "simulator_capture", f"Unexpected BMP encoding ({bits_per_pixel} bpp).", "Inspect the capture manually; blank-frame detection was not applied."))
        return record, issues
    pixels = data[pixel_offset:]
    # Sample evenly rather than allocating a decoded full image; simulator BMPs
    # are 32-bit BGRA, and this only guards against a blank/failed renderer.
    sample_count = min(4096, len(pixels) // 4)
    step = max(4, (len(pixels) // max(1, sample_count)) // 4 * 4)
    luminance: list[int] = []
    for offset in range(0, min(len(pixels) - 3, step * sample_count), step):
        blue, green, red = pixels[offset], pixels[offset + 1], pixels[offset + 2]
        luminance.append((77 * red + 150 * green + 29 * blue) // 256)
    if luminance:
        white = sum(value >= 250 for value in luminance) / len(luminance)
        dark = sum(value <= 5 for value in luminance) / len(luminance)
        record.update({"sample_count": len(luminance), "white_fraction": round(white, 4), "dark_fraction": round(dark, 4)})
        if white > 0.995 or dark > 0.995:
            issues.append(issue(None, "high", "simulator_blank_frame", f"Capture is nearly uniform (white={white:.3f}, dark={dark:.3f}).", "Re-run capture after the reader has rendered the target page; retain the log with the review packet."))
    return record, issues


def parse_model_response(text: str) -> dict[str, Any]:
    cleaned = re.sub(r"^\x60\x60\x60(?:json)?\s*|\s*\x60\x60\x60$", "", text.strip(), flags=re.I)
    start, end = cleaned.find("{"), cleaned.rfind("}")
    value = json.loads(cleaned if start < 0 else cleaned[start:end + 1])
    if not isinstance(value.get("issues"), list):
        raise ValueError("model response has no issues list")
    valid = []
    for item in value["issues"]:
        if not isinstance(item, dict) or item.get("severity") not in ("low", "medium", "high"):
            raise ValueError("model returned an invalid issue")
        if not all(isinstance(item.get(key), str) and item[key].strip() for key in ("category", "evidence", "suggested_action")):
            raise ValueError("model issue lacks required explanatory fields")
        valid.append({key: item[key] for key in ("severity", "category", "evidence", "suggested_action")})
    return {"issues": valid}


def cloud_review(pdf_path: Path, manifest: dict[str, Any], renders: list[Path], max_pages: int) -> list[dict[str, Any]]:
    workspace = Path(__file__).resolve().parents[3]
    sys.path.insert(0, str(workspace))
    from workspace_credentials import require
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=require("GEMINI_API_KEY"))
    results = []
    for page, image_path in zip(manifest["pages"][:max_pages], renders[:max_pages]):
        text = f"PDF page {page['pdf_page']}; extraction method={page.get('extraction_method')}; warnings={page.get('warnings', [])}; characters={page['character_count']}."
        prompt = f"""You are a strict quality reviewer for a small 800x480 CrossPoint e-reader EPUB conversion.
Review the supplied original PDF page image against this extraction summary:
{text}
Find only concrete conversion risks: missing/garbled text, wrong reading order, tables/equations/figures that need a source-image companion, or density that will not reflow readably. Do not rewrite content and do not assert facts outside this page.
Return only JSON: {{"issues":[{{"severity":"low|medium|high","category":"...","evidence":"...","suggested_action":"..."}}]}}."""
        response = client.models.generate_content(
            model="gemini-3.1-pro-preview",
            contents=[prompt, types.Part.from_bytes(data=image_path.read_bytes(), mime_type="image/png")],
            config=types.GenerateContentConfig(temperature=0.0),
        )
        try:
            assessment = parse_model_response(response.text or "")
            results.append({"pdf_page": page["pdf_page"], "review": assessment})
        except Exception as error:
            results.append({"pdf_page": page["pdf_page"], "review": {"issues": []}, "error": str(error)[:600]})
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--model-review", action="store_true", help="ask Gemini to review rendered source pages")
    parser.add_argument("--allow-cloud-content", action="store_true", help="explicitly authorize upload of these rendered PDF pages and extraction summaries")
    parser.add_argument("--max-model-pages", type=int, default=8, help="bound cloud-review volume (default: 8)")
    parser.add_argument("--simulator-screenshot", action="append", type=Path, default=[], help="firmware-rendered BMP to record and sanity-check; may be repeated")
    parser.add_argument("--expected-device-width", type=int, default=480)
    parser.add_argument("--expected-device-height", type=int, default=800)
    args = parser.parse_args()
    if args.model_review and not args.allow_cloud_content:
        parser.error("--model-review requires --allow-cloud-content")
    if not args.pdf.is_file() or not args.manifest.is_file():
        parser.error("PDF and manifest must both exist")
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    renders = source_renders(args.pdf, output_dir / "source_pages")
    result: dict[str, Any] = {
        "schema_version": 1,
        "tool": "crosspoint_agentic_review",
        "tool_version": TOOL_VERSION,
        "created_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "source_sha256": manifest["source"]["sha256"],
        "epub_sha256": manifest["epub"]["sha256"],
        "local_issues": local_review(manifest),
        "status": "needs_human_or_simulator_review",
        "limitations": [
            "Local checks identify extraction risk; they do not prove semantic fidelity.",
            "A model review, when enabled, is advisory and never a human disposition.",
            "Simulator screenshots verify firmware layout behavior but not physical e-ink waveform or panel ghosting.",
        ],
    }
    simulator_records = []
    simulator_issues = []
    for screenshot in args.simulator_screenshot:
        screenshot = screenshot.resolve()
        if not screenshot.is_file():
            parser.error(f"simulator screenshot does not exist: {screenshot}")
        record, issues = review_simulator_bmp(screenshot, args.expected_device_width, args.expected_device_height)
        simulator_records.append(record)
        simulator_issues.extend(issues)
    if simulator_records:
        result["simulator_review"] = {"captures": simulator_records, "issues": simulator_issues}
    if args.model_review:
        result["model_review"] = cloud_review(args.pdf, manifest, renders, args.max_model_pages)
        result["model_review_scope"] = {"model": "gemini-3.1-pro-preview", "pages": min(args.max_model_pages, len(renders))}
    (output_dir / "conversion_review.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"review": str(output_dir / "conversion_review.json"), "source_page_images": len(renders), "local_issues": len(result["local_issues"]), "simulator_issues": len(simulator_issues), "model_review": args.model_review}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
