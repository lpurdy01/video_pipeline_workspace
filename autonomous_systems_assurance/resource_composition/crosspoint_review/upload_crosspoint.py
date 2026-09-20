#!/usr/bin/env python3
"""Validate and upload one review EPUB through CrossPoint's documented HTTP API."""

from __future__ import annotations

import argparse
import http.client
import mimetypes
import sys
import uuid
from pathlib import Path
from urllib.parse import urlencode, urlparse

from pdf_to_crosspoint_epub import validate_epub


def normalized_device_url(host: str, destination: str) -> tuple[str, str, str]:
    parsed = urlparse(host)
    if parsed.scheme != "http" or not parsed.netloc or parsed.path not in ("", "/") or parsed.query or parsed.fragment:
        raise ValueError("--host must be an HTTP origin such as http://crosspoint.local (no path or query)")
    if not destination.startswith("/"):
        raise ValueError("--path must start with /")
    return parsed.netloc, "/upload?" + urlencode({"path": destination}), parsed.scheme


def multipart_body(epub_path: Path, boundary: str) -> bytes:
    filename = epub_path.name
    content_type = mimetypes.guess_type(filename)[0] or "application/epub+zip"
    prefix = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f"Content-Type: {content_type}\r\n\r\n"
    ).encode()
    return prefix + epub_path.read_bytes() + f"\r\n--{boundary}--\r\n".encode()


def upload(epub_path: Path, host: str, destination: str, timeout: float) -> tuple[int, str]:
    netloc, target, _ = normalized_device_url(host, destination)
    boundary = "----crosspoint-review-" + uuid.uuid4().hex
    body = multipart_body(epub_path, boundary)
    connection = http.client.HTTPConnection(netloc, timeout=timeout)
    try:
        connection.request("POST", target, body=body, headers={"Content-Type": f"multipart/form-data; boundary={boundary}", "Content-Length": str(len(body))})
        response = connection.getresponse()
        return response.status, response.read().decode(errors="replace")
    finally:
        connection.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("epub", type=Path)
    parser.add_argument("--host", default="http://crosspoint.local", help="reader web-server origin")
    parser.add_argument("--path", default="/Books/Review", help="existing directory on the reader SD card")
    parser.add_argument("--timeout", type=float, default=60)
    parser.add_argument("--dry-run", action="store_true", help="validate and show destination without sending anything")
    args = parser.parse_args()
    epub_path = args.epub.resolve()
    if not epub_path.is_file():
        print(f"error: EPUB does not exist: {epub_path}", file=sys.stderr)
        return 2
    try:
        validate_epub(epub_path)
        netloc, target, _ = normalized_device_url(args.host, args.path)
    except (RuntimeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(f"Validated {epub_path.name}; destination http://{netloc}{target}")
    if args.dry_run:
        print("Dry run: no device request was made.")
        return 0
    try:
        status, response_text = upload(epub_path, args.host, args.path, args.timeout)
    except OSError as error:
        print(f"error: device upload failed: {error}", file=sys.stderr)
        return 1
    if 200 <= status < 300 and "File uploaded successfully:" in response_text:
        print(response_text.strip())
        return 0
    print(f"error: reader returned HTTP {status}: {response_text.strip()}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

