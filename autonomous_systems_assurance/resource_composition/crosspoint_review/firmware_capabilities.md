# CrossPoint Reader capability map for Xteink X4 Pro

Inspected against the submodule commit `8c84ef3268fd56147ae1625e04f773f0f50b7720` (2026-09-19). This is a source-and-documentation map, not a claim that every feature has been exercised on this particular physical device.

## The practical content contract

| Area | Supported at this revision | Review-toolkit implication |
|---|---|---|
| Native reading files | EPUB 2/3, `.xtc`/`.xtch`, `.txt`, and `.md`; `.bmp` and `.png` open in the image viewer. The browser's extension dispatch is in `src/activities/home/FileBrowserActivity.cpp`. | Use EPUB for rich, navigable review copy. PDF is not a native reader format. |
| EPUB reading | Embedded styles, images, hyphenation, kerning, adaptive tables, CJK ruby, navigation links, footnotes, bookmarks, dictionary lookup, go-to-percent, auto page turn, orientation, Focus Reading, and KOReader progress sync are listed in `README.md`. | Generate a conservative static EPUB: simple XHTML, internal TOC, paragraphs, and element/class CSS. |
| CSS profile | Element, class, element+class, and grouped selectors are supported; descendant selectors, pseudo selectors, media queries, imports, and font-face are ignored (`lib/Epub/Epub/css/CssParser.h`). | Do not treat an EPUB as a browser page. The generator avoids scripts, SVG, web fonts, and complex CSS. |
| Image path | EPUB image handling covers PNG/JPEG; image decoders reject unsupported dimensions/features, and image loading is user-configurable. | Do not use page-raster images as the primary PDF route. A portrait PDF page reduced to this display would be hard to read; reflowed text is the default. |
| Review actions | Bookmarks, screenshots, chapter navigation, go-to-percent, touch links and dictionary lookups (touch devices) are supported. | Bookmark plus `PDF p. N` is the stable review locator. Screenshot is the visual handoff. |
| Annotation | No text-highlighting, typed note, or review-disposition sync feature was found in the inspected user guide/source path. | Decisions must remain in the assurance project's review workflow; do not call reader bookmarks evidence by themselves. |
| Library | Up to 4,096 supported books, metadata title/author, recent/added/title/author views, search, folder browser, and SD cache management. | The EPUB metadata is set from PDF metadata or explicit CLI arguments. Rebuild the library index after a manual copy if necessary. |
| Transfer | HTTP multipart upload, WebSocket upload, WebDAV, Calibre wireless mode, AP/STA Wi-Fi, OPDS, and file-manager actions. The HTTP contract is documented in `docs/webserver-endpoints.md`. | The helper uses the simplest documented form: `POST /upload?path=/Books/Review`. |
| X4 Pro transfer | USB mass-storage drive mode is compiled for `FREEINK_CAP_USB_MSC`; the X4 Pro profile uses an ESP32-S3, touch, frontlight, PSRAM, native SDMMC, and USB MSC (`platformio.ini`). | USB Drive is the most reliable bulk-transfer path and needs no credentials or LAN. Safely eject before returning to the reader. |
| Reader controls | Orientation, status bar configuration, font family/size/spacing/margins, paragraph alignment, hyphenation, anti-aliasing, image rendering, Focus Reading, button remapping, and sleep-screen controls. | Reader settings are personal; package CSS should not overrule them heavily. |
| Localization | The README reports 34 UI languages, CJK fallback, and RTL support. | Set `--language` accurately where known; retain the original PDF if extraction/layout needs a language-specific check. |
| Maintenance | OTA release updates, SD `firmware.bin` updates, local caches under `/.crosspoint`, and serial logging are supported. | An uploaded replacement EPUB clears its own cache. Do not delete `/.crosspoint` casually: it clears device cache/progress state. |

## What can and cannot be simulated

The pinned [CrossPoint Simulator](../../tools/crosspoint-simulator) compiles the reader firmware as a native SDL2 application. Its X4 Pro profile implements the 800×480 device shape, touch/swipe input, capacitive Home key, frontlight state, RTC, simulated SD card, host-backed file transfer, scripted input, and deterministic BMP screenshots. This project provides a local adapter that starts a generated EPUB directly in that simulated SD card and captures it through the real firmware layout path.

The firmware also contains host-side CMake/CTest suites for parser and utility behavior, registered as `pio run -t unit-tests` by `scripts/register_unit_tests_target.py`. Those tests fetch GoogleTest through CMake and complement, rather than replace, the simulator.

The X4 Pro build profile is `[env:x4pro]` in `platformio.ini`; it is separate from the default ESP32-C3 profile. A compile (`pio run -e x4pro`) checks the actual target configuration. Flashing (`pio run -e x4pro -t upload`) changes hardware and is deliberately not part of this toolkit.

The simulator intentionally does **not** model device-specific waveform timing, ghosting, power sequencing, or actual memory pressure unless test-specific heap overrides are set. The converter's HTML preview is only a fast ergonomic preview. Opening the package on the reader is the final compatibility check.

## Feature choices made by the toolkit

- Uses EPUB, not direct PDF, because no PDF dispatch or PDF reader was found in the firmware.
- Uses an EPUB 2 OPF plus NCX because CrossPoint's codebase explicitly parses `content.opf` and its reader supports chapter navigation.
- Keeps every original PDF page as a separate EPUB spine item and writes the source hash into the chapter locator and machine-readable manifest.
- Never claims a reflowed line, table, equation, image, or page break is visually equivalent to the PDF; source-page visual checks remain necessary.
- Does not access the device until an operator explicitly runs the uploader without `--dry-run`.
