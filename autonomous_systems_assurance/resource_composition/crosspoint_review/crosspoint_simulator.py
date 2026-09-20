#!/usr/bin/env python3
"""Prepare, build, and capture the official CrossPoint X4 Pro SDL simulator."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
TOOLS = PROJECT / "tools"
FIRMWARE = TOOLS / "crosspoint-reader"
SIMULATOR = TOOLS / "crosspoint-simulator"
BEGIN = "; BEGIN crosspoint-review simulator"
END = "; END crosspoint-review simulator"


def doctor(firmware: Path, simulator: Path) -> dict:
    include_paths = [Path(path) for path in os.environ.get("CPLUS_INCLUDE_PATH", "").split(os.pathsep) if path]
    openssl_header = Path("/usr/include/openssl/md5.h").is_file() or any(
        (path / "openssl" / "md5.h").is_file() for path in include_paths
    )
    sdl_header = Path("/usr/include/SDL2/SDL.h").is_file() or any(
        (path / "SDL2" / "SDL.h").is_file() for path in include_paths
    )
    return {
        "firmware": str(firmware),
        "firmware_present": (firmware / "platformio.ini").is_file(),
        "firmware_freeink_initialized": (firmware / "freeink-sdk" / "libs").is_dir(),
        "simulator": str(simulator),
        "simulator_present": (simulator / "sample-platformio-linux-wsl.ini").is_file(),
        "pio": shutil.which("pio"),
        "sdl2_config": shutil.which("sdl2-config"),
        "curl": shutil.which("curl"),
        "openssl_headers": openssl_header,
        "sdl2_headers": sdl_header,
    }


def managed_config(simulator: Path) -> str:
    sample = simulator / "sample-platformio-linux-wsl.ini"
    body = sample.read_text(encoding="utf-8").replace(
        "simulator=https://github.com/crosspoint-reader/crosspoint-simulator",
        "simulator=symlink://../crosspoint-simulator",
    )
    # AnimatedGIF uses Arduino's PROGMEM copy helper even on the host build.
    # The simulator maps flash-backed data to ordinary host memory.
    body = body.replace("  -Isrc\n", "  -Isrc\n  -Dmemcpy_P=memcpy\n")
    return f"{BEGIN}\n{body.rstrip()}\n{END}\n"


def write_config(firmware: Path, simulator: Path) -> None:
    target = firmware / "platformio.local.ini"
    block = managed_config(simulator)
    existing = target.read_text(encoding="utf-8") if target.exists() else ""
    if BEGIN in existing and END in existing:
        start = existing.index(BEGIN)
        end = existing.index(END, start) + len(END)
        updated = existing[:start].rstrip() + "\n\n" + block + existing[end:].lstrip()
    else:
        if "[env:simulator" in existing:
            raise RuntimeError(f"{target} already defines a simulator environment; inspect it rather than adding a competing one.")
        updated = existing.rstrip() + ("\n\n" if existing.strip() else "") + block
    target.write_text(updated, encoding="utf-8")


def prepare(epub: Path, firmware: Path, book_name: str) -> dict:
    if not epub.is_file():
        raise RuntimeError(f"EPUB not found: {epub}")
    destination = firmware / "fs_" / "books" / book_name
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(epub, destination)
    state_dir = firmware / "fs_" / ".crosspoint"
    state_dir.mkdir(parents=True, exist_ok=True)
    state = {
        "openEpubPath": f"/books/{book_name}",
        "readerActivityLoadCount": 0,
        "lastSleepFromReader": True,
        "showBootScreen": True,
    }
    state_path = state_dir / "state.json"
    state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    return {"book": str(destination), "state": str(state_path), "device_path": state["openEpubPath"]}


def build(firmware: Path) -> int:
    pio = shutil.which("pio")
    if not pio:
        raise RuntimeError("pio is not on PATH")
    command = [str(Path(pio).resolve()), "run", "-e", "simulator_x4_pro"]
    first = subprocess.run(command, cwd=firmware, check=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    sys.stdout.write(first.stdout)
    if first.returncode == 0:
        return 0
    # Some native PlatformIO toolchains leave the generated Epub archive without
    # an index for nested block objects. This is only a cache/build artifact, not
    # a firmware-source modification. Rebuild that archive once and retry the
    # link; any real compiler/link error still returns its original failure.
    build_root = firmware / ".pio" / "build" / "simulator_x4_pro"
    archives = list(build_root.glob("lib*/libEpub.a"))
    archive = archives[0] if len(archives) == 1 else build_root / "missing-Epub.a"
    archive_root = archive.parent
    objects = sorted((archive_root / "Epub").rglob("*.o")) if (archive_root / "Epub").is_dir() else []
    ar = shutil.which("ar")
    link_signature = "undefined reference to `TextBlock::" in first.stdout
    if not link_signature or not ar or not archive.is_file() or not objects:
        return first.returncode
    rebuilt = archive.with_name("libEpub.rebuilt.a")
    subprocess.run([ar, "rcs", str(rebuilt), *map(str, objects)], check=True)
    os.replace(rebuilt, archive)
    print("Retried native simulator link after rebuilding its generated Epub archive index.", file=sys.stderr)
    second = subprocess.run(command, cwd=firmware, check=False)
    return second.returncode


def capture(firmware: Path, screenshots: str, input_script: str, http_port: int | None) -> int:
    binary = firmware / ".pio" / "build" / "simulator_x4_pro" / "program"
    if not binary.is_file():
        raise RuntimeError(f"Simulator binary missing: {binary}; run the build command first.")
    environment = os.environ.copy()
    environment["CROSSPOINT_SIM_SCREENSHOTS"] = screenshots
    environment["CROSSPOINT_SIM_INPUT_SCRIPT"] = input_script
    if http_port:
        environment["CROSSPOINT_SIM_HTTP_PORT"] = str(http_port)
    return subprocess.run([str(binary)], cwd=firmware, env=environment, check=False).returncode


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--firmware-dir", type=Path, default=FIRMWARE)
    parser.add_argument("--simulator-dir", type=Path, default=SIMULATOR)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor")
    config = sub.add_parser("configure")
    config.add_argument("--write", action="store_true", help="write/update the ignored firmware platformio.local.ini")
    prepare_parser = sub.add_parser("prepare")
    prepare_parser.add_argument("epub", type=Path)
    prepare_parser.add_argument("--book-name", default="crosspoint-review.epub")
    prepare_parser.add_argument("--write-config", action="store_true")
    sub.add_parser("build")
    capture_parser = sub.add_parser("capture")
    capture_parser.add_argument("--screenshots", required=True, help="simulator schedule, e.g. 7000:./qa/reader.bmp")
    capture_parser.add_argument("--input-script", default="9000:QUIT")
    capture_parser.add_argument("--http-port", type=int)
    args = parser.parse_args()
    firmware, simulator = args.firmware_dir.resolve(), args.simulator_dir.resolve()
    if args.command == "doctor":
        print(json.dumps(doctor(firmware, simulator), indent=2))
        return 0
    if not (firmware / "platformio.ini").is_file() or not (simulator / "sample-platformio-linux-wsl.ini").is_file():
        print("error: firmware/simulator directories are incomplete; initialize both submodules first.", file=sys.stderr)
        return 2
    try:
        if args.command == "configure":
            if not args.write:
                print(f"Would add the X4 Pro simulator environment to {firmware / 'platformio.local.ini'}. Re-run with --write.")
                return 0
            write_config(firmware, simulator)
            print(f"Configured {firmware / 'platformio.local.ini'}; it is ignored by the firmware repository.")
        elif args.command == "prepare":
            if args.write_config:
                write_config(firmware, simulator)
            print(json.dumps(prepare(args.epub.resolve(), firmware, args.book_name), indent=2))
        elif args.command == "build":
            status = doctor(firmware, simulator)
            missing = [name for name in ("pio", "sdl2_config", "openssl_headers", "sdl2_headers") if not status[name]]
            if missing:
                raise RuntimeError("Simulator build prerequisites missing: " + ", ".join(missing) + ". Run doctor for details.")
            return build(firmware)
        elif args.command == "capture":
            return capture(firmware, args.screenshots, args.input_script, args.http_port)
    except RuntimeError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
