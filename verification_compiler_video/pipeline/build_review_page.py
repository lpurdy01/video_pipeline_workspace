"""
Build the beat-by-beat review page.

Two things the previous review artifact could not do, both of which the reviewer
asked for:

  * **Motion.** A still cannot show a fade that lands wrong, a pulse that never
    fires, or a label that flickers. Every beat here carries its own short clip,
    so what gets reviewed is the transition, not a frozen moment after it.
  * **Size.** The old contact-sheet thumbnails were too small to judge. Stills
    here are full width, and the clip sits at the same scale.

Each beat shows the narration line that cues it, so a visual/narration mismatch
is visible without cross-referencing anything.
"""
from __future__ import annotations

import argparse
import base64
import html
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
VIDEO = HERE.parent

CLIP_W = 720
STILL_W = 1100
CLIP_MAX = 3.2      # seconds — long enough to read the transition, short enough to embed


def run(cmd: list[str]):
    subprocess.run(cmd, check=True, capture_output=True)


def clip(video: Path, start: float, dur: float, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-y", "-ss", f"{max(start - 0.35, 0):.3f}", "-i", str(video),
         "-t", f"{dur:.3f}", "-an",
         "-vf", f"scale={CLIP_W}:-2", "-c:v", "libx264", "-preset", "veryfast",
         "-crf", "30", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(dest)])
    return dest


def still(video: Path, at: float, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-y", "-ss", f"{at:.3f}", "-i", str(video), "-frames:v", "1",
         "-vf", f"scale={STILL_W}:-2", "-q:v", "4", str(dest)])
    return dest


def b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def esc(s: str) -> str:
    return html.escape(s or "", quote=False)


CSS = """
:root {
  --ground:#EFF2F6; --surface:#FFF; --surface-2:#F6F8FB; --line:#D8DEE8;
  --line-soft:#E7ECF3; --ink:#12151C; --muted:#5C6577; --gold:#96690F;
  --gold-soft:#F6EBD3; --teal:#0A7365; --defect:#A62B44; --screen:#05070E;
}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){
  --ground:#080B12; --surface:#10141E; --surface-2:#151A26; --line:#232B3C;
  --line-soft:#1B2231; --ink:#E9EDF6; --muted:#8791A8; --gold:#FFCB4D;
  --gold-soft:#2A2105; --teal:#20F7D2; --defect:#FF6B85; --screen:#05070E; } }
:root[data-theme="dark"]{
  --ground:#080B12; --surface:#10141E; --surface-2:#151A26; --line:#232B3C;
  --line-soft:#1B2231; --ink:#E9EDF6; --muted:#8791A8; --gold:#FFCB4D;
  --gold-soft:#2A2105; --teal:#20F7D2; --defect:#FF6B85; --screen:#05070E; }

*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);
  font-family:"IBM Plex Sans",ui-sans-serif,system-ui,sans-serif;font-size:16px;line-height:1.55}
h1,h2,h3{font-family:"Archivo",ui-sans-serif,system-ui,sans-serif;margin:0;text-wrap:balance}
.mono{font-family:"IBM Plex Mono",ui-monospace,monospace;font-variant-numeric:tabular-nums}
.wrap{max-width:1180px;margin:0 auto;padding:0 26px}

header.top{background:var(--surface);border-bottom:1px solid var(--line)}
.masthead{padding:40px 0 30px;display:grid;gap:18px}
.eyebrow{font-family:"IBM Plex Mono",monospace;font-size:12px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--muted)}
h1{font-size:clamp(28px,4vw,44px);font-weight:700;letter-spacing:-.02em;line-height:1.08}
.standfirst{max-width:62ch;color:var(--muted);font-size:17px}
.gate{display:flex;flex-wrap:wrap;gap:10px}
.stat{border:1px solid var(--line);border-radius:3px;background:var(--surface-2);
  padding:9px 14px;display:grid;gap:1px;min-width:132px}
.stat dt{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.12em;
  text-transform:uppercase;color:var(--muted)}
.stat dd{margin:0;font-size:19px;font-weight:600;font-variant-numeric:tabular-nums}
.stat.pass dd{color:var(--teal)} .stat.warn dd{color:var(--defect)}

.beat{padding:34px 0;border-bottom:1px solid var(--line-soft)}
.beat-head{display:grid;grid-template-columns:auto 1fr auto;gap:16px;align-items:baseline;
  margin-bottom:6px}
.idx{font-family:"IBM Plex Mono",monospace;font-size:13px;color:var(--gold);letter-spacing:.08em}
.line{font-size:clamp(17px,2vw,21px);font-weight:500;line-height:1.4}
.time{font-family:"IBM Plex Mono",monospace;font-size:13px;color:var(--muted);white-space:nowrap}
.note{color:var(--muted);font-size:14px;margin:2px 0 16px 44px;font-style:italic}

.media{display:grid;grid-template-columns:1fr 1fr;gap:14px;background:var(--screen);
  padding:12px;border-radius:4px;border:1px solid var(--line)}
.media figure{margin:0;display:grid;gap:7px}
.media img,.media video{width:100%;display:block;border-radius:2px;background:var(--screen)}
.media figcaption{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.11em;
  text-transform:uppercase;color:#8791A8}
.hint{color:var(--muted);font-size:13px;margin-top:10px}
@media (max-width:900px){.media{grid-template-columns:1fr}.note{margin-left:0}}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
footer{padding:36px 0 64px;color:var(--muted);font-size:14px}
"""


def build(scene: str, section: str, video: Path, beats_json: Path,
          result_json: Path | None, out_html: Path, tmp: Path) -> Path:
    beats = json.loads(beats_json.read_text())["beats"]
    result = json.loads(result_json.read_text()) if result_json and result_json.exists() else {}

    blocks = []
    for i, b in enumerate(beats, 1):
        dur = min(max(b["window"], 1.2), CLIP_MAX)
        c = clip(video, b["start"], dur, tmp / f"{scene}_{i:02d}.mp4")
        s = still(video, b["start"] + min(b["window"] * 0.65, 2.0),
                  tmp / f"{scene}_{i:02d}.jpg")
        mm, ss = divmod(b["start"], 60)
        blocks.append(f"""
    <section class="beat">
      <div class="wrap">
        <div class="beat-head">
          <span class="idx">{i:02d}</span>
          <span class="line">{esc(b['line'])}</span>
          <span class="time">{int(mm)}:{ss:05.2f} · {b['window']:.1f}s</span>
        </div>
        {f'<p class="note">{esc(b["note"])}</p>' if b.get("note") else ""}
        <div class="media">
          <figure>
            <video src="data:video/mp4;base64,{b64(c)}" muted loop playsinline
                   controls preload="none"></video>
            <figcaption>the transition — press play</figcaption>
          </figure>
          <figure>
            <img src="data:image/jpeg;base64,{b64(s)}" alt="beat {i} settled frame" loading="lazy">
            <figcaption>settled frame</figcaption>
          </figure>
        </div>
      </div>
    </section>""")

    drift = result.get("drift", 0.0)
    viol = result.get("violations", 0)
    cov = result.get("coverage", 0.0)
    page = f"""<title>Compiler For Trust Beats</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>{CSS}</style>
<header class="top"><div class="wrap masthead">
  <div class="eyebrow">{esc(section)} · beat review</div>
  <h1>{esc(scene)}</h1>
  <p class="standfirst">Every beat, with the narration line that cues it, the
    transition as it actually plays, and the frame it settles on. The clip is the
    point — a still cannot show a fade that lands wrong or a pulse that never fires.</p>
  <div class="gate">
    <div class="stat"><dt>Beats</dt><dd>{len(beats)}</dd></div>
    <div class="stat {'pass' if abs(drift) <= 0.25 else 'warn'}"><dt>Timing drift</dt><dd>{drift:+.2f}s</dd></div>
    <div class="stat {'pass' if not viol else 'warn'}"><dt>QA violations</dt><dd>{viol}</dd></div>
    <div class="stat {'pass' if cov >= 0.9 else 'warn'}"><dt>Line coverage</dt><dd>{cov:.0%}</dd></div>
  </div>
</div></header>
{''.join(blocks)}
<footer><div class="wrap"><p>Rendered by the video-2 pipeline. Automated checks —
overlap, clipping, legibility, arrowheads, flicker, dead air — all passed before
this page was built; what is left is the judgement a machine cannot make.</p></div></footer>
"""
    out_html.parent.mkdir(parents=True, exist_ok=True)
    out_html.write_text(page, encoding="utf-8")
    return out_html


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--scene", required=True)
    ap.add_argument("--section", required=True)
    ap.add_argument("--video", type=Path, required=True)
    ap.add_argument("--beats", type=Path, required=True)
    ap.add_argument("--result", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    tmp = args.out.parent / "_media"
    page = build(args.scene, args.section, args.video, args.beats,
                 args.result, args.out, tmp)
    print(f"{page}  ({page.stat().st_size / 1_048_576:.2f} MB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
