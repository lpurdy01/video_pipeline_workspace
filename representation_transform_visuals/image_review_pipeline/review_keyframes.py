from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import subprocess
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = "auto"
DEFAULT_OUT_DIR = ROOT / "image_review_pipeline" / "out"


MODEL_PREFERENCE = [
    # Prefer strongest reasoning/vision models for critique. Cost is not the
    # bottleneck for this workflow; missed visual problems are.
    "gemini-3.1-pro-preview",
    "gemini-pro-latest",
    "gemini-3-pro-preview",
    "gemini-2.5-pro",
    "gemini-3.5-flash",
    "gemini-3.1-flash-lite",
    "gemini-3.1-flash-lite-preview",
    "gemini-3-flash-preview",
    "gemini-2.5-flash",
]


VISUAL_LANGUAGE = """
Project visual language:
- Nearly black background, not slide-deck gray.
- Sparse labels; narration carries most words.
- Bright popping colors: cyan, electric blue, violet, gold, green; red for loss or assumptions.
- Prefer glowing geometry, vector spaces, matrices, axes, and motion over panels and explanatory text.
- Text should not overlap, be tiny, or be awkwardly tilted unless intentionally part of 3D space.
- Important objects such as matrices, vectors, axes, and relationship arrows should be visible and readable.
- The style should feel closer to 3Blue1Brown-inspired mathematical animation than PowerPoint.
"""


BASE_PROMPT = f"""
You are reviewing keyframes for a technical YouTube animation about learned representation transforms.

{VISUAL_LANGUAGE}

Each frame has a section ID, an elapsed timestamp, and (when available) the narration line playing at that moment. Use the timestamp + narration to evaluate **whether the visual matches what the narrator is saying right then.**

A human reviewer just gave us a long list of overlap / layout issues that the previous review missed. Be much more rigorous about this. For EACH frame, run the following checklist explicitly and report each hit:

OVERLAP / LAYOUT CHECKLIST (look hard — these are the failures we miss most):
A. **Text-on-text overlap.** For every pair of visible text elements, do their bounding boxes intersect? Bottom-of-frame "narration walk" captions in particular collide with diagram text — flag every instance.
B. **Text crossed by lines or arrows.** Is any text glyph being struck through by a connector line, axis, arrow, dashed line, or circle stroke? Flag the specific element pair.
C. **Edge clipping.** Is any text, box, arrow tip, or labeled glyph being cut off by the frame edge? (Common on 854x480: anything past x≈±6.7 or y≈±3.7.)
D. **Arrow lands on a letter.** Does any arrow tip end inside a text glyph instead of just outside it (e.g. arrow tip overlapping the letter "l" in "lion")?
E. **Label sits over a glowing dot / node / box.** Is text rendered on top of a circle, sphere, matrix, or box such that the symbol shows through?
F. **Boxed-text inside a 3D scene.** Is there a rectangle with text that's tilted or partially obscured by 3D camera perspective?
G. **Caption immediately above/below another caption.** Multiple captions/subtitles stacked too close to read independently.
H. **Glyph that doesn't match neighbors.** E.g. an "ℒ" Laplace symbol shown over a Fourier transform, an icon for a different concept than the narration.
I. **Dim text on near-black.** Any element using muted grey, dark brown, dark green, or unsetfilled stroke text that disappears.

NARRATIVE CHECKLIST:
J. **Narration vs. visual mismatch.** The narration line for this timestamp is provided — does the on-screen visual emphasize what the narrator is saying RIGHT NOW? If the narrator just said "stripe API / billing table / cached entitlement", are those choices visualized? If the narrator is listing technologies, are those technologies popping in?
K. **Dead-end animation.** Is something fading out without anything taking its place? Is the scene at a static hold for ≥5s while the narrator is rapidly listing new ideas?
L. **Missed visualization opportunity.** Is the narrator describing a concrete metaphor (e.g. "DCT throws away information your eye won't notice") that the current visual doesn't show?

For each image:
1. Describe what the frame appears to show in one or two sentences.
2. Run the OVERLAP / LAYOUT CHECKLIST — go letter by letter (A through I). For each letter that has a hit, write the specific element pair and one-line fix. If none, write "A-I clear".
3. Run the NARRATIVE CHECKLIST (J, K, L). Same format.
4. One-line summary verdict: PASS / MINOR / BLOCKING.

Then close with:
- Story/Beat Suggestions
- Highest Priority Fixes (group by which `at HH:MM:SS.ss` timestamps need attention)

Be specific. "Bottom text overlaps" is not useful — say *which* two elements and at *what* timestamp.
"""


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and value and key not in os.environ:
            os.environ[key] = value


def api_key() -> str:
    load_env_file(ROOT / ".env")
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise SystemExit("Set GEMINI_API_KEY in the shell or representation_transform_visuals/.env.")
    return key


def mime_type(path: Path) -> str:
    guessed, _ = mimetypes.guess_type(path.as_posix())
    return guessed or "image/png"


def image_part(path: Path) -> dict:
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return {
        "inline_data": {
            "mime_type": mime_type(path),
            "data": data,
        }
    }


def normalize_model_name(name: str) -> str:
    return name.removeprefix("models/")


def available_gemini_models() -> set[str]:
    url = "https://generativelanguage.googleapis.com/v1beta/models"
    response = requests.get(
        url,
        headers={"X-goog-api-key": api_key()},
        timeout=60,
    )
    if response.status_code >= 400:
        raise RuntimeError(f"Gemini model list error {response.status_code}: {response.text}")

    available: set[str] = set()
    for model in response.json().get("models", []):
        methods = model.get("supportedGenerationMethods", [])
        if "generateContent" not in methods:
            continue
        available.add(normalize_model_name(model.get("name", "")))
    return available


def resolve_model(model: str) -> str:
    if model and model != "auto":
        return normalize_model_name(model)

    available = available_gemini_models()
    for candidate in MODEL_PREFERENCE:
        if candidate in available:
            return candidate
    raise RuntimeError(
        "No preferred Gemini visual review model is available. "
        f"Available generateContent models: {', '.join(sorted(available))}"
    )


def extract_keyframes(video: Path, timestamps: list[float], out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for timestamp in timestamps:
        out = out_dir / f"keyframe_{timestamp:06.2f}s.png"
        subprocess.run(
            [
                "ffmpeg",
                "-v",
                "error",
                "-y",
                "-ss",
                str(timestamp),
                "-i",
                video.as_posix(),
                "-frames:v",
                "1",
                "-update",
                "1",
                out.as_posix(),
            ],
            check=True,
        )
        paths.append(out)
    return paths


def call_gemini(images: list[Path], model: str, context: str = "") -> str:
    resolved_model = resolve_model(model)
    prompt = BASE_PROMPT
    if context:
        prompt += "\n\nScene context:\n" + context
    parts = [{"text": prompt}]
    for idx, path in enumerate(images, start=1):
        parts.append({"text": f"Frame {idx}: {path.name}"})
        parts.append(image_part(path))

    # gemini-2.5-flash consumes its entire token budget as thoughts with no output
    # text unless thinking is disabled. Pro models require thinking and reject budget=0.
    body: dict = {"contents": [{"parts": parts}]}
    if "flash" in resolved_model and any(x in resolved_model for x in ("2.5", "3.0", "3.1", "3.5")):
        body["generationConfig"] = {"thinkingConfig": {"thinkingBudget": 0}}

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{resolved_model}:generateContent"
    print(f"Using Gemini visual review model: {resolved_model}")
    response = requests.post(
        url,
        headers={
            "Content-Type": "application/json",
            "X-goog-api-key": api_key(),
        },
        data=json.dumps(body),
        timeout=600,
    )
    if response.status_code >= 400:
        raise RuntimeError(f"Gemini API error {response.status_code}: {response.text}")

    payload = response.json()
    text_chunks = []
    for candidate in payload.get("candidates", []):
        for part in candidate.get("content", {}).get("parts", []):
            if "text" in part:
                text_chunks.append(part["text"])
    if not text_chunks:
        raise RuntimeError(f"No text returned by Gemini: {json.dumps(payload)[:1000]}")
    return "\n".join(text_chunks)


def main() -> None:
    parser = argparse.ArgumentParser(description="Review generated animation keyframes with Gemini vision.")
    parser.add_argument("--images", nargs="*", type=Path, default=[])
    parser.add_argument("--video", type=Path)
    parser.add_argument("--timestamps", nargs="*", type=float, default=[3.0, 10.0, 17.0])
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help="Gemini model id, or 'auto' to use the strongest available preferred visual review model.",
    )
    parser.add_argument(
        "--print-model",
        action="store_true",
        help="Print the resolved review model and exit without reviewing images.",
    )
    parser.add_argument("--out", type=Path)
    parser.add_argument("--context-file", type=Path, help="Optional scene/manifest context to include in the visual review prompt.")
    args = parser.parse_args()

    if args.print_model:
        print(resolve_model(args.model))
        return

    if not args.out:
        raise SystemExit("Provide --out unless using --print-model.")

    images = list(args.images)
    if args.video:
        images.extend(extract_keyframes(args.video, args.timestamps, DEFAULT_OUT_DIR / "extracted_keyframes"))
    images = [path for path in images if path.exists()]
    if not images:
        raise SystemExit("No images found. Provide --images and/or --video.")

    context = args.context_file.read_text(encoding="utf-8") if args.context_file and args.context_file.exists() else ""
    review = call_gemini(images, args.model, context)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(review, encoding="utf-8")
    print(args.out)


if __name__ == "__main__":
    main()
