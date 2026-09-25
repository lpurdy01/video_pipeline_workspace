#!/usr/bin/env python3
"""Capture an official-source recovery candidate without changing source records.

Usage: capture.py <label> <url>

The capture is deliberately separated from source-registry promotion. A later
integrator must inspect the content, create a scoped UTF-8 context, hash the
snapshot, and update the matching region record before the compiler treats it
as full context.
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen


if len(sys.argv) != 3:
    raise SystemExit("usage: capture.py <label> <url>")

label, url = sys.argv[1:]
out = Path(__file__).parent / "out" / label
out.mkdir(parents=True, exist_ok=True)
request = Request(url, headers={"User-Agent": "Mozilla/5.0 (research source recovery)"})
with urlopen(request, timeout=40) as response:
    body = response.read()
    content_type = response.headers.get_content_type()
    final_url = response.url

suffix = ".pdf" if content_type == "application/pdf" or body.startswith(b"%PDF") else ".html"
snapshot = out / f"snapshot{suffix}"
snapshot.write_bytes(body)
(out / "capture.json").write_text(json.dumps({
    "url": url,
    "final_url": final_url,
    "captured_at": datetime.now(timezone.utc).isoformat(),
    "content_type": content_type,
    "bytes": len(body),
    "sha256": hashlib.sha256(body).hexdigest(),
    "snapshot": snapshot.name,
}, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"label": label, "content_type": content_type, "bytes": len(body), "snapshot": str(snapshot)}))
