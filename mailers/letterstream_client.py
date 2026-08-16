"""
LetterStream API client — Method 2 (HTTP POST, single file per recipient).

Auth: md5(base64_encode(last6(timestamp) + api_key + first6(timestamp)))
Endpoint: https://www.letterstream.com/apis/index.php  POST multipart/form-data

All submissions use preauth=1 — jobs land in cart/preauth state and will NOT
be mailed until manually released via the LetterStream dashboard (doauth=authcode).

Credentials: LETTERSTREAM_API_ID / LETTERSTREAM_API_KEY, read from the user
credential store at ~/.config/video-pipeline/credentials.env (see
workspace_credentials.py in the repo root).

Usage:
  python letterstream_client.py --test           # verify auth + account balance
  python letterstream_client.py --list           # list recipient slugs
  python letterstream_client.py --slug dan_negrut  # preauth one
  python letterstream_client.py --all            # preauth all 7 (2s gap between each)
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import sys
import time
from pathlib import Path

import requests
from pypdf import PdfReader

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from workspace_credentials import require  # noqa: E402

HERE = Path(__file__).parent
DATA = HERE / "data"
OUT = HERE / "out"

API_ENDPOINT = "https://www.letterstream.com/apis/index.php"


# ---------------------------------------------------------------------------
# Credentials
# ---------------------------------------------------------------------------

def load_credentials() -> tuple[str, str]:
    return require("LETTERSTREAM_API_ID"), require("LETTERSTREAM_API_KEY")


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------

def make_auth_params(api_id: str, api_key: str) -> dict:
    """
    LetterStream one-time hash auth (Section III of API docs).
    unique_id = Unix timestamp (10-18 digits, used once only).
    string_to_hash = last6(unique_id) + api_key + first6(unique_id)
    hash = md5(base64_encode(string_to_hash))
    """
    unique_id = str(int(time.time()))
    string_to_hash = unique_id[-6:] + api_key + unique_id[:6]
    h = hashlib.md5(base64.b64encode(string_to_hash.encode())).hexdigest()
    return {"a": api_id, "h": h, "t": unique_id}


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def load_recipients() -> list[dict]:
    return load_json(DATA / "recipients.json")

def load_config() -> dict:
    return load_json(DATA / "config.json")


# ---------------------------------------------------------------------------
# Address formatting  (Table 4.2.2 — delimiter is ":")
#
# Recipient: doc_id:name1:name2:addr1:addr2:city:state:zip
# Sender:    name1:name2:addr1:addr2:city:state:zip  (no doc_id)
#
# Our recipient JSON layout:
#   addr1 = dept/institution  → name2 (address name line 2)
#   addr2 = building + street → addr1 (first street line)
#   addr3 = "City, ST ZIP"   → parsed into city/state/zip
#   edge case: addr3 empty   → addr1=street, addr2="City, ST ZIP"
# ---------------------------------------------------------------------------

def parse_city_state_zip(s: str) -> tuple[str, str, str]:
    m = re.match(r'^(.+),\s+([A-Z]{2})\s+(\S+)$', s.strip())
    if m:
        return m.group(1).strip(), m.group(2), m.group(3)
    return s.strip(), "", ""


def recipient_to_str(r: dict, doc_suffix: str = "") -> str:
    base = r["slug"].replace("_", "")
    doc_id = (base + doc_suffix)[:20]
    name = r["name"]
    addr1 = r.get("addr1", "").strip()
    addr2 = r.get("addr2", "").strip()
    addr3 = r.get("addr3", "").strip()

    if addr3:
        name2 = addr1          # dept line as second name line
        street = addr2         # building+street as addr1
        city, state, zc = parse_city_state_zip(addr3)
    else:
        name2 = ""
        street = addr1
        city, state, zc = parse_city_state_zip(addr2)

    return f"{doc_id}:{name}:{name2}:{street}::{city}:{state}:{zc}"


def sender_str(cfg: dict) -> str:
    ra = cfg["return_address"]
    # name: "Levi Purdy" → split into name1:name2
    parts = ra["name"].split(" ", 1)
    name1, name2 = parts[0], (parts[1] if len(parts) > 1 else "")
    # line1: "4764 E Sunrise Dr, Unit #630"
    # line2: "Tucson, AZ 85718-4535"
    city, state, zc = parse_city_state_zip(ra["line2"])
    line1 = ra["line1"]
    if "," in line1:
        street, apt = [p.strip() for p in line1.split(",", 1)]
    else:
        street, apt = line1, ""
    return f"{name1}:{name2}:{street}:{apt}:{city}:{state}:{zc}"


# ---------------------------------------------------------------------------
# API calls
# ---------------------------------------------------------------------------

def test_connectivity(api_id: str, api_key: str) -> None:
    """Auth check + account balance (accountstatus=1)."""
    params = make_auth_params(api_id, api_key)
    params["accountstatus"] = "1"
    params["debug"] = "3"
    resp = requests.post(API_ENDPOINT, data=params, timeout=30)
    print(f"HTTP {resp.status_code}")
    print(resp.text)


def submit_one(r: dict, cfg: dict, api_id: str, api_key: str) -> str:
    """
    Submit one flat mailer via Method 2 with preauth=1.
    Job lands in preauth/cart state — not mailed until doauth is sent.
    Job name includes timestamp to guarantee uniqueness across all past jobs.
    """
    pdf_path = OUT / r["slug"] / "packet.pdf"
    if not pdf_path.exists():
        raise FileNotFoundError(
            f"Packet not found: {pdf_path}\n"
            f"Run: python build_mailer.py --bw"
        )

    pages = len(PdfReader(str(pdf_path)).pages)
    # Job name: max ~30 chars, unique, human-readable
    job_name = f"vc26_{r['slug'][:12]}_{int(time.time())}"

    params = make_auth_params(api_id, api_key)
    # Last 4 digits of timestamp used as doc_id suffix to guarantee
    # uniqueness across batches (doc_id must be unique across all active jobs).
    doc_suffix = params["t"][-4:]
    to_str = recipient_to_str(r, doc_suffix)

    params.update({
        "debug":      "3",
        "job":        job_name,
        "from":       sender_str(cfg),
        "to[]":       to_str,
        "pages":      str(pages),
        "mailtype":   "flat",
        "coversheet": "true",
        "duplex":     "Y",
        "ink":        "B",    # Black and white
        "paper":      "W",    # White 8.5x11 20#
        "preauth":    "1",    # Cart only, not released to production
    })

    print(f"  job:   {job_name}")
    print(f"  pages: {pages}")
    print(f"  to[]:  {to_str}")
    print(f"  from:  {sender_str(cfg)}")

    with open(pdf_path, "rb") as f:
        resp = requests.post(
            API_ENDPOINT,
            data=params,
            files={"single_file": (f"{r['slug']}.pdf", f, "application/pdf")},
            timeout=180,
        )

    print(f"  HTTP {resp.status_code}")
    print(f"  {resp.text.strip()}")
    return resp.text


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="LetterStream flat mailer client")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--test", action="store_true",
                       help="Verify auth and print account balance")
    group.add_argument("--slug", metavar="SLUG",
                       help="Submit one recipient (preauth mode)")
    group.add_argument("--all", action="store_true",
                       help="Submit all recipients (preauth mode)")
    group.add_argument("--list", action="store_true",
                       help="List recipient slugs")
    args = parser.parse_args()

    if args.list:
        for r in load_recipients():
            notes = f"  ** {r['notes']}" if r.get("notes") else ""
            print(f"  {r['slug']:30s}  {r['name']}{notes}")
        return

    api_id, api_key = load_credentials()

    if args.test:
        print(f"API_ID: {api_id}")
        print(f"Endpoint: {API_ENDPOINT}\n")
        test_connectivity(api_id, api_key)
        return

    cfg = load_config()
    recipients = load_recipients()

    if args.slug:
        targets = [r for r in recipients if r["slug"] == args.slug]
        if not targets:
            raise SystemExit(f"No recipient '{args.slug}'. Use --list.")
    else:
        targets = recipients

    for i, r in enumerate(targets):
        print(f"\n[{r['slug']}]")
        try:
            submit_one(r, cfg, api_id, api_key)
        except Exception as e:
            print(f"  ERROR: {e}", file=sys.stderr)
        # Ensure unique timestamps between submissions (auth uses time())
        if i < len(targets) - 1:
            time.sleep(2)

    print(f"\nDone. {len(targets)} job(s) submitted in preauth mode.")
    print("Release in LetterStream dashboard: My Jobs → select job → Authorize.")


if __name__ == "__main__":
    main()
