from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
OUT = ROOT / "manifest_pipeline" / "out"


def repo_path(path: str | Path) -> Path:
    path = Path(path)
    if path.is_absolute():
        return path
    return (REPO_ROOT / path).resolve()


def run(cmd: list[str]) -> None:
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)


def resolved_audio_by_section() -> dict[str, dict]:
    path = OUT / "resolved_manifest.json"
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {section["id"]: section for section in data.get("sections", [])}


def main() -> int:
    parser = argparse.ArgumentParser(description="Build local word-level alignment JSON for manifest audio.")
    parser.add_argument("--manifest", type=Path, default=ROOT / "production_manifest.json")
    parser.add_argument("--out-dir", type=Path, default=OUT / "alignments")
    parser.add_argument("--sections", nargs="*", help="Optional section IDs to align.")
    parser.add_argument("--source", choices=["scratch", "resolved"], default="scratch",
                        help="scratch uses manifest scratch_path; resolved uses resolved_manifest audio_path.")
    parser.add_argument("--allow-human", action="store_true",
                        help="Allow local transcription of human audio from resolved_manifest. Never uploads it.")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--model", default="small")
    parser.add_argument("--device", default="auto")
    parser.add_argument("--compute-type", default="int8")
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    wanted = set(args.sections or [])
    resolved = resolved_audio_by_section()
    transcriber = ROOT / "narration_pipeline" / "transcribe_words.py"
    args.out_dir.mkdir(parents=True, exist_ok=True)

    for section in manifest.get("sections", []):
        section_id = section["id"]
        if wanted and section_id not in wanted:
            continue
        out = args.out_dir / f"{section_id}.json"
        if out.exists() and not args.force:
            print(f"skip existing {out}")
            continue

        audio_source = "scratch_tts"
        audio = repo_path(section["audio"]["scratch_path"])
        if args.source == "resolved" and section_id in resolved:
            record = resolved[section_id]
            audio_source = record.get("audio_source", "")
            audio = Path(record["audio_path"])

        if audio_source == "human" and not args.allow_human:
            print(f"skip human audio {section_id}; pass --allow-human for local-only transcription")
            continue
        if not audio.exists():
            print(f"skip missing audio {section_id}: {audio}")
            continue

        run([
            sys.executable,
            transcriber.as_posix(),
            "--audio", audio.as_posix(),
            "--out", out.as_posix(),
            "--model", args.model,
            "--device", args.device,
            "--compute-type", args.compute_type,
        ])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
