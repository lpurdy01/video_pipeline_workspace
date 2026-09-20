#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import unittest
import zipfile
from pathlib import Path

from pdf_to_crosspoint_epub import ExtractedPage, reflow_paragraphs, validate_epub, write_epub
from upload_crosspoint import multipart_body, normalized_device_url
from agentic_review import local_review


class CrossPointReviewEpubTests(unittest.TestCase):
    def test_reflow_preserves_non_whitespace_content(self) -> None:
        self.assertEqual(reflow_paragraphs("A line\ncontinues here.\n\nNext paragraph."), ("A line continues here.", "Next paragraph."))

    def test_epub_is_structurally_valid_and_has_one_spine_item_per_source_page(self) -> None:
        pages = [ExtractedPage(1, ("First source paragraph.",), "a" * 64), ExtractedPage(2, ("Second source paragraph.",), "b" * 64)]
        with tempfile.TemporaryDirectory() as temporary:
            epub_path = Path(temporary) / "review.epub"
            write_epub(epub_path, "Test review", "Tester", "en", "source.pdf", "c" * 64, pages, ("Check scope.",))
            validate_epub(epub_path)
            with zipfile.ZipFile(epub_path) as archive:
                self.assertEqual(archive.namelist()[0], "mimetype")
                self.assertEqual(archive.getinfo("mimetype").compress_type, zipfile.ZIP_STORED)
                self.assertIn("OEBPS/text/page-0002.xhtml", archive.namelist())
                self.assertIn(b"Source PDF page 2", archive.read("OEBPS/text/page-0002.xhtml"))

    def test_upload_contract_uses_documented_path_parameter_and_multipart_file(self) -> None:
        self.assertEqual(normalized_device_url("http://crosspoint.local", "/Books/Review"), ("crosspoint.local", "/upload?path=%2FBooks%2FReview", "http"))
        with tempfile.TemporaryDirectory() as temporary:
            epub_path = Path(temporary) / "review.epub"
            epub_path.write_bytes(b"epub-bytes")
            body = multipart_body(epub_path, "boundary")
        self.assertIn(b'filename="review.epub"', body)
        self.assertTrue(body.endswith(b"--boundary--\r\n"))

    def test_local_reviewer_routes_ocr_and_column_repair_to_human_checks(self) -> None:
        manifest = {
            "pages": [
                {"pdf_page": 1, "character_count": 9, "extraction_method": "tesseract_ocr", "warnings": ["ocr_used_verify_against_source_image"]},
                {"pdf_page": 2, "character_count": 250, "extraction_method": "pymupdf_blocks", "warnings": ["two_column_reading_order_repaired_verify_against_source_layout"]},
            ]
        }
        findings = local_review(manifest)
        self.assertTrue(any(item["page"] == 1 and item["category"] == "ocr" for item in findings))
        self.assertTrue(any(item["page"] == 2 and item["category"] == "extraction" for item in findings))


if __name__ == "__main__":
    unittest.main()
