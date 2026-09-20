# CrossPoint PDF review toolkit

This is an end-to-end conversion-and-review workbench for an Xteink X4 Pro running the pinned [CrossPoint Reader firmware](../../tools/crosspoint-reader). It builds a device-compatible EPUB, measures extraction risk, renders source-page review images, optionally asks a bounded model reviewer to inspect those images, then uses the actual [CrossPoint SDL simulator](../../tools/crosspoint-simulator) to capture firmware-rendered layouts before deployment.

It does **not** pretend that arbitrary PDF conversion is lossless. The EPUB chapters map one-to-one to original PDF pages, and every package carries source, extracted-page, and output hashes. Layout-heavy pages, OCR, columns, tables, equations, and figures are explicitly routed into a review queue instead of silently being treated as correct prose.

Generated packages belong under an ignored `out/` directory. The tool makes no network request until its separate upload command is run without `--dry-run`.

## What it produces

For `paper.pdf`, the converter produces:

- `paper-review.epub` — reflowed reading copy with a chapter for every original PDF page, stable `PDF p. N` locators, an NCX table of contents, and review cues.
- `paper-review.manifest.json` — source and output SHA-256 digests, an extracted-text digest per source page, extraction method, and limitations.
- `paper-review-preview.html` — a local 800×480 viewport preview. It checks the review content ergonomics; it is not an emulator of CrossPoint's C++ layout engine or e-ink waveform.

The generated EPUB uses only static XHTML, an NCX TOC, and simple element/class CSS. That profile deliberately stays within CrossPoint's documented EPUB/CSS capability rather than relying on browser-only features.

## End-to-end local pipeline

For normal use, run one command. It uses PyMuPDF block extraction first, repairs only clearly detected two-column reading order, falls back to Tesseract for text-empty pages, creates the EPUB and manifest, renders 144-DPI source images, and writes a deterministic extraction-review queue.

```bash
python3 autonomous_systems_assurance/resource_composition/crosspoint_review/run_pipeline.py \
  arbitrary-document.pdf \
  --output-dir autonomous_systems_assurance/resource_composition/crosspoint_review/out/arbitrary-document
```

The pipeline does not make a cloud call by default. Its deterministic reviewer assigns a concrete next action for every risk it finds. That gives the system a safe baseline for arbitrary PDFs—even when a model credential or network is unavailable.

For an advisory model pass, explicitly authorize that particular PDF's rendered pages and extraction summaries for upload. This does not approve a human disposition or rewrite the content, and is deliberately separate because arbitrary input may be rights-sensitive:

```bash
python3 autonomous_systems_assurance/resource_composition/crosspoint_review/run_pipeline.py \
  arbitrary-document.pdf --output-dir autonomous_systems_assurance/resource_composition/crosspoint_review/out/arbitrary-document \
  --model-review --allow-cloud-content --max-model-pages 8
```

The current project Gemini key was previously blocked by quota, so a model pass may still fail until API billing is repaired. The local review packet remains usable in that case.

## Simulator-backed layout QA

The official CrossPoint simulator is now pinned locally. It compiles the actual firmware as a Linux desktop binary, renders to SDL2, accepts scripted key/touch input, and saves deterministic BMP screenshots. It is the correct refinement loop for CrossPoint layout—not merely a browser mockup.

```bash
TOOL=autonomous_systems_assurance/resource_composition/crosspoint_review/crosspoint_simulator.py
python3 "$TOOL" doctor
python3 "$TOOL" prepare \
  autonomous_systems_assurance/resource_composition/crosspoint_review/out/arbitrary-document/arbitrary-document-review.epub \
  --write-config
python3 "$TOOL" build
SIM_OUT="$PWD/autonomous_systems_assurance/resource_composition/crosspoint_review/out/arbitrary-document/simulator"
mkdir -p "$SIM_OUT"
python3 "$TOOL" capture \
  --screenshots "1300:$SIM_OUT/reader-page-a.bmp;2200:$SIM_OUT/reader-page-b.bmp" \
  --input-script '2000:DOWN;4000:QUIT'

# Attach firmware-rendered evidence to the existing review record.
python3 autonomous_systems_assurance/resource_composition/crosspoint_review/agentic_review.py \
  arbitrary-document.pdf "$SIM_OUT/../arbitrary-document-review.manifest.json" \
  --output-dir "$SIM_OUT/../arbitrary-document-agentic-review" \
  --simulator-screenshot "$SIM_OUT/reader-page-a.bmp" \
  --simulator-screenshot "$SIM_OUT/reader-page-b.bmp"
```

`prepare` creates only ignored simulator SD-card state under `crosspoint-reader/fs_/`; it starts the simulator directly in the review EPUB. `configure` writes an ignored `platformio.local.ini` to the firmware submodule, using the X4 Pro simulator profile and a local symlink to the pinned simulator.

For headless Linux CI, prefix the capture command with `SDL_VIDEODRIVER=offscreen`. The capture schedule is process-relative: retain the simulator log and confirm it enters `EpubReader` before accepting the associated images. The reviewer records each BMP's SHA-256, expected 480×800 geometry, and blank-frame metrics; it never silently treats a device image as proof of source fidelity.

On Debian/Ubuntu the simulator needs `libsdl2-dev`, `libssl-dev`, and pioarduino/PlatformIO. The `doctor` command reports missing pieces before any build. The simulator is faithful to CrossPoint's layout, navigation, cache, and host file-transfer paths, but it does **not** simulate a physical panel's waveform, ghosting, timing, or actual RAM pressure unless a test sets its heap overrides.

## Build a review package only

The only host dependencies are Python 3.8+ and Poppler's `pdfinfo` and `pdftotext` commands.

```bash
python3 autonomous_systems_assurance/resource_composition/crosspoint_review/pdf_to_crosspoint_epub.py \
  autonomous_systems_assurance/resource_composition/review_prototype/out/autonomous_assurance_whitepaper_review.pdf \
  --title "Assurance for Learned Autonomous Systems — review copy" \
  --author "Levi Purdy" \
  --output-dir autonomous_systems_assurance/resource_composition/crosspoint_review/out/whitepaper \
  --overwrite
```

Open the generated preview locally if helpful, then inspect the EPUB structure without touching a device:

```bash
python3 autonomous_systems_assurance/resource_composition/crosspoint_review/upload_crosspoint.py \
  autonomous_systems_assurance/resource_composition/crosspoint_review/out/whitepaper/autonomous-assurance-whitepaper-review-review.epub \
  --dry-run
```

Run the toolkit's self-tests with:

```bash
cd autonomous_systems_assurance/resource_composition/crosspoint_review
python3 -m unittest test_pdf_to_crosspoint_epub.py
```

## Move it to the X4 Pro

The straightforward route is USB Drive mode: on the reader choose **File Transfer → USB Drive**, wait for the host to mount the SD card, then copy the EPUB into (for example) `/Books/Review/`. Safely eject the drive before leaving USB Drive mode. This is X4 Pro-specific firmware functionality.

For Wi-Fi, on the reader choose **File Transfer → Join a Network** (or create a hotspot). The firmware's documented HTTP endpoint is `POST /upload?path=/Books/Review`. The helper sends exactly that multipart form only when you omit `--dry-run`:

```bash
python3 autonomous_systems_assurance/resource_composition/crosspoint_review/upload_crosspoint.py \
  autonomous_systems_assurance/resource_composition/crosspoint_review/out/whitepaper/autonomous-assurance-whitepaper-review-review.epub \
  --host http://crosspoint.local --path /Books/Review
```

The folder must already exist. Uploading an identically named EPUB intentionally replaces it; CrossPoint clears its cache for the uploaded path. Use **Settings → System → Rebuild library index** if the new title does not appear in Library.

## Review protocol on the device

1. In Reader settings, use a large font and left alignment for analytical material; turn off embedded style if you prefer your global reader settings.
2. Use the EPUB's table of contents to jump to `Source PDF page N`.
3. Long-press the configured bookmark action on a page needing attention. Take a screenshot for a handoff needing visible context.
4. Report the PDF page number with each concern. The adjacent manifest supplies the source and extracted-text digest needed to associate it with the exact package.

This is intentionally a **locator-and-disposition** workflow, not an annotation system. The examined CrossPoint version supports bookmarks and screenshots but does not offer text highlighting, typed marginal notes, or synchronization of a review disposition back to this repository. Keep decisions in the project's normal review records; the reader package is a portable reading surface.

## Simulation and firmware verification boundary

CrossPoint's build system targets real ESP32 hardware, but its companion simulator does provide a full native desktop firmware path for display/input/storage workflows. It remains a simulator, not a physical-panel certification test. The final check remains: open the generated EPUB on the physical X4 Pro, navigate the table of contents, bookmark a source page, take a screenshot, and inspect the serial log if parsing fails.

For firmware work, use the X4 Pro PlatformIO environment, not the default X3/X4 C3 environment:

```bash
cd autonomous_systems_assurance/tools/crosspoint-reader
pio run -e x4pro
pio run -t unit-tests
# Connect an actual device only when intentionally flashing:
# pio run -e x4pro -t upload
```

See [firmware capabilities](firmware_capabilities.md) for the source-inspected feature map and constraints.
