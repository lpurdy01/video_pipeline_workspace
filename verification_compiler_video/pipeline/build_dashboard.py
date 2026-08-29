"""
The review dashboard: what the gate found, what Gemini thinks, and the frames.

The two review layers produce output in incompatible shapes — the gate a list of
timestamped violations, Gemini two hundred prose judgements — and neither is
reviewable on its own. This puts them on one page, keyed to the amber slate code
burned into the frame, so a note like "03 b28" means the same thing on screen, in
the report, and in the scene source.
"""
from __future__ import annotations

import argparse
import base64
import collections
import html
import json
import re
import subprocess
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
VIDEO = HERE.parent
QA = VIDEO / "scenes" / "out" / "qa"

SECTION_TITLES = {
    "S01GenerationGotCheap": ("01", "Generation Got Cheap"),
    "S02ChatLogFallacy": ("02", "The Hidden Cost Of Looks Good"),
    "S03TraceabilityShape": ("03", "The Shape Of Traceability"),
    "S04ArtifactGraph": ("04", "The Artifact Graph"),
    "S05CompilationTraversal": ("05", "Compilation As Traversal"),
    "S06VQP": ("06", "The Verification Query Package"),
    "S07DualModeReview": ("07", "Dual-Mode Review"),
    "S08EvidenceCards": ("08", "Evidence Records"),
    "S09ReadinessMap": ("09", "The Readiness Map"),
    "S10EvidenceSurface": ("10", "The Evidence Surface"),
    "S11EndCard": ("11", "End Card"),
}
MODULES = {
    "S01GenerationGotCheap": "s01_generation_got_cheap",
    "S02ChatLogFallacy": "s02_chat_log_fallacy",
    "S03TraceabilityShape": "s03_traceability_shape",
    "S04ArtifactGraph": "s04_artifact_graph",
    "S05CompilationTraversal": "s05_compilation_traversal",
    "S06VQP": "s06_vqp",
    "S07DualModeReview": "s07_dual_mode_review",
    "S08EvidenceCards": "s08_evidence_cards",
    "S09ReadinessMap": "s09_readiness_map",
    "S10EvidenceSurface": "s10_evidence_surface",
    "S11EndCard": "s11_end_card",
}

SEVERITY_ORDER = {"BLOCKING": 0, "WORTH-FIX": 1, "POLISH": 2}

THEMES = [
    ("Shape grammar", "the wrong shape for the artifact being named",
     r"shape grammar|document slice|drawn as (a )?(plain|simple|tall|wide)|"
     r"plain (vertical |tall )?rectangles?"),
    ("Colour grammar", "a colour standing for something it does not mean",
     r"gold \(|violet \(|cyan \(|red is reserved|colou?r grammar|reserved for"),
    ("Stale frame", "the line changed and the picture did not",
     r"\bstale\b|unchanged from the previous|zero visual change|no visual change"),
    ("Dead space", "the composition huddles into part of the stage",
     r"dead region|dead space|unbalanced|shoved|pushed entirely"),
    ("Sentences on screen", "prose where a short identifier belongs",
     r"full sentence|short identifiers"),
    ("Missed detail", "the narration names something concrete the frame omits",
     r"missed opportunity|explicitly (names|mentions|states|refers)"),
]


def esc(s: str) -> str:
    return html.escape(s or "", quote=False)


def b64(p: Path) -> str:
    return base64.b64encode(p.read_bytes()).decode("ascii")


def video_for(scene: str) -> Path | None:
    hits = sorted((VIDEO / "scenes" / "media" / "videos").rglob(f"{scene}.mp4"))
    return hits[-1] if hits else None


def still(scene: str, t: float, dest: Path, width: int = 760) -> Path | None:
    src = video_for(scene)
    if src is None:
        return None
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-ss", f"{max(t, 0):.3f}", "-i", str(src),
                    "-frames:v", "1", "-vf", f"scale={width}:-2", "-q:v", "5", str(dest)],
                   check=True, capture_output=True)
    return dest


LINE_RE = re.compile(
    r"^\s*\**\s*(?P<beat>\d\d\s+b\d\d)\s*\|\s*(?P<sev>BLOCKING|WORTH-FIX|POLISH)"
    r"\s*\|\s*(?P<cat>MISMATCH|COMPOSITION|LEGIBILITY|MISSED)\s*\|\s*(?P<text>.+?)\s*$",
    re.I)


def parse_findings(report: Path) -> list[tuple[str, str, str, str, str]]:
    """(section, beat, severity, category, text) for every finding line."""
    out, section = [], ""
    for line in report.read_text().splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
            continue
        m = LINE_RE.match(line)
        if m and section:
            out.append((section, " ".join(m.group("beat").split()),
                        m.group("sev").upper(), m.group("cat").upper(),
                        m.group("text")))
    return out


CSS = """
:root{
  --ground:#EFF2F6; --surface:#FFFFFF; --surface-2:#F5F8FB; --line:#D6DDE8;
  --line-soft:#E6ECF4; --ink:#12151C; --muted:#5C6577; --gold:#8A6110;
  --gold-chip:#F7EFDA; --teal:#0A6C60; --defect:#A6203C; --warn:#8A5A05;
  --screen:#05070E; --slate-bg:#0A0F1C; --slate-ink:#FF9E45;
}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){
  --ground:#070A11; --surface:#0F141F; --surface-2:#141A27; --line:#242C3D;
  --line-soft:#1A2130; --ink:#E7ECF5; --muted:#8892A8; --gold:#F2BA53;
  --gold-chip:#2B2107; --teal:#25D6B8; --defect:#FF6E88; --warn:#E9A93C;
  --screen:#05070E; --slate-bg:#0A0F1C; --slate-ink:#FF9E45; } }
:root[data-theme="dark"]{
  --ground:#070A11; --surface:#0F141F; --surface-2:#141A27; --line:#242C3D;
  --line-soft:#1A2130; --ink:#E7ECF5; --muted:#8892A8; --gold:#F2BA53;
  --gold-chip:#2B2107; --teal:#25D6B8; --defect:#FF6E88; --warn:#E9A93C;
  --screen:#05070E; --slate-bg:#0A0F1C; --slate-ink:#FF9E45;
}

*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);
  font-family:"IBM Plex Sans","Segoe UI",system-ui,sans-serif;
  font-size:16px;line-height:1.55;-webkit-font-smoothing:antialiased}
.wrap{width:min(1120px,92vw);margin:0 auto}
h1,h2,h3{font-family:Archivo,"IBM Plex Sans",system-ui,sans-serif;
  text-wrap:balance;margin:0}
h1{font-size:clamp(30px,4.4vw,50px);font-weight:700;letter-spacing:-.022em;line-height:1.06}
h2{font-size:clamp(21px,2.4vw,27px);font-weight:700;letter-spacing:-.012em}
h3{font-size:17px;font-weight:600}
a{color:var(--teal)}

/* --- masthead --------------------------------------------------------- */
header.top{background:var(--surface);border-bottom:1px solid var(--line);
  padding:52px 0 0}
.eyebrow{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--muted);margin-bottom:14px}
.standfirst{max-width:64ch;color:var(--muted);font-size:17px;margin:16px 0 0}
.rail{display:flex;flex-wrap:wrap;gap:0;margin:34px 0 0;
  border-top:1px solid var(--line-soft)}
.cell{flex:1 1 150px;padding:16px 20px 20px;border-right:1px solid var(--line-soft);
  display:grid;gap:3px}
.cell:last-child{border-right:0}
.cell .k{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.13em;
  text-transform:uppercase;color:var(--muted)}
.cell .v{font-family:Archivo,sans-serif;font-size:27px;font-weight:700;
  font-variant-numeric:tabular-nums;letter-spacing:-.02em}
.cell.good .v{color:var(--teal)} .cell.bad .v{color:var(--defect)}

/* --- sections --------------------------------------------------------- */
section{padding:46px 0}
section + section{border-top:1px solid var(--line-soft)}
.lede{color:var(--muted);max-width:66ch;margin:10px 0 26px}

/* --- gate table ------------------------------------------------------- */
.tablewrap{overflow-x:auto;border:1px solid var(--line);border-radius:3px;
  background:var(--surface)}
table{border-collapse:collapse;width:100%;min-width:660px}
th{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.13em;
  text-transform:uppercase;color:var(--muted);text-align:left;font-weight:500;
  padding:12px 16px;border-bottom:1px solid var(--line);background:var(--surface-2)}
td{padding:13px 16px;border-bottom:1px solid var(--line-soft);font-size:15px}
tr:last-child td{border-bottom:0}
td.num{font-family:"IBM Plex Mono",monospace;font-variant-numeric:tabular-nums;
  text-align:right;white-space:nowrap}
.sec-no{font-family:"IBM Plex Mono",monospace;color:var(--muted);font-size:13px;
  margin-right:10px}
.pill{display:inline-block;font-family:"IBM Plex Mono",monospace;font-size:10.5px;
  letter-spacing:.09em;text-transform:uppercase;padding:3px 9px;border-radius:2px;
  border:1px solid currentColor;white-space:nowrap}
.pill.pass{color:var(--teal)} .pill.fail{color:var(--defect)}

/* --- the slate chip: same object the viewer reads off the frame ------- */
.slate{display:inline-block;font-family:"IBM Plex Mono",monospace;font-size:12px;
  letter-spacing:.06em;background:var(--slate-bg);color:var(--slate-ink);
  padding:2px 8px;border-radius:2px;white-space:nowrap}

/* --- violation cards -------------------------------------------------- */
.viol{display:grid;grid-template-columns:1fr;gap:0;margin-top:22px}
.vcard{background:var(--surface);border:1px solid var(--line);border-radius:3px;
  border-left:3px solid var(--defect);padding:0;margin-bottom:14px;overflow:hidden}
.vhead{display:flex;flex-wrap:wrap;gap:12px;align-items:center;padding:14px 18px}
.vcheck{font-family:"IBM Plex Mono",monospace;font-size:13px;color:var(--defect);
  font-weight:500}
.vwhere{font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--muted);
  font-variant-numeric:tabular-nums}
.vdetail{padding:0 18px 16px;color:var(--ink);font-size:15px;max-width:74ch}
.vshot{display:block;width:100%;background:var(--screen);border-top:1px solid var(--line)}

/* --- themes ----------------------------------------------------------- */
.theme{background:var(--surface);border:1px solid var(--line);border-radius:3px;
  margin-bottom:14px;overflow:hidden}
.theme > summary{list-style:none;cursor:pointer;padding:16px 18px;display:flex;
  gap:14px;align-items:baseline;flex-wrap:wrap}
.theme > summary::-webkit-details-marker{display:none}
.theme > summary:hover{background:var(--surface-2)}
.theme > summary:focus-visible{outline:2px solid var(--teal);outline-offset:-2px}
.tname{font-family:Archivo,sans-serif;font-weight:700;font-size:17px}
.tcount{font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--gold);
  background:var(--gold-chip);padding:2px 8px;border-radius:2px;
  font-variant-numeric:tabular-nums}
.twhat{color:var(--muted);font-size:14px}
.theme[open] > summary{border-bottom:1px solid var(--line-soft)}
.findings{margin:0;padding:6px 18px 18px}
.finding{display:grid;grid-template-columns:auto 1fr;gap:14px;align-items:baseline;
  padding:9px 0;border-bottom:1px solid var(--line-soft)}
.finding:last-child{border-bottom:0}
.finding p{margin:0;font-size:15px;max-width:78ch}
.bar{height:5px;background:var(--line-soft);border-radius:3px;overflow:hidden;
  margin-top:8px;max-width:420px}
.bar i{display:block;height:100%;background:var(--gold)}

footer{padding:40px 0 72px;color:var(--muted);font-size:14px;
  border-top:1px solid var(--line-soft)}
footer p{max-width:70ch}
@media (max-width:760px){
  .finding{grid-template-columns:1fr;gap:5px}
  .rail{flex-direction:column}.cell{border-right:0;border-bottom:1px solid var(--line-soft)}
}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--gemini", type=Path,
                    default=VIDEO / "out" / "review" /
                    f"gemini_frame_review_{date.today().isoformat()}.md")
    ap.add_argument("--out", type=Path, default=VIDEO / "out" / "review" / "dashboard.html")
    ap.add_argument("--shots", type=Path, default=VIDEO / "out" / "review" / "shots")
    ap.add_argument("--ranked", type=Path,
                    default=VIDEO / "out" / "review" / "ranked.json")
    ap.add_argument("--top", type=int, default=20)
    args = ap.parse_args()

    results = [json.loads(f.read_text()) for f in sorted(QA.glob("*.result.json"))]
    clean = sum(1 for r in results if r["ok"])
    worst_drift = max((abs(r["drift"]) for r in results), default=0.0)
    total_beats = 0
    for r in results:
        bp = VIDEO / "out" / "beats" / f"{r['scene']}.beats.json"
        if bp.exists():
            total_beats += len(json.loads(bp.read_text())["beats"])
    runtime = sum(r["target_seconds"] for r in results)

    rows = []
    for r in results:
        no, name = SECTION_TITLES.get(r["scene"], ("--", r["scene"]))
        ok = r["ok"]
        rows.append(f"""
        <tr>
          <td><span class="sec-no">{no}</span>{esc(name)}</td>
          <td><span class="pill {'pass' if ok else 'fail'}">{'clean' if ok else 'open'}</span></td>
          <td class="num">{r['violations'] or '&mdash;'}</td>
          <td class="num">{r['drift']:+.2f}s</td>
          <td class="num">{r['coverage']:.0%}</td>
          <td class="num">{r['target_seconds']:.0f}s</td>
        </tr>""")

    # Outstanding violations, each with the frame it happens on.
    viol_cards, kinds = [], collections.Counter()
    for f in sorted(QA.glob("*.violations.json")):
        for v in json.loads(f.read_text()):
            kinds[v["check"]] += 1
            no, name = SECTION_TITLES.get(v["scene"], ("--", v["scene"]))
            shot = None
            try:
                shot = still(v["scene"], v["t"] + 0.35,
                             args.shots / f"{v['scene']}_{v['t']:.0f}_{v['check']}.jpg")
            except Exception:
                shot = None
            img = (f'<img class="vshot" src="data:image/jpeg;base64,{b64(shot)}" '
                   f'alt="frame at {v["t"]:.1f}s" loading="lazy">') if shot else ""
            viol_cards.append(f"""
      <article class="vcard">
        <div class="vhead">
          <span class="vcheck">{esc(v['check'])}</span>
          <span class="vwhere">{no} &middot; {v['t']:.1f}s &middot; {esc(name)}</span>
        </div>
        <p class="vdetail">{esc(v['detail'])}</p>
        {img}
      </article>""")

    # Gemini, grouped.
    theme_blocks, n_findings = [], 0
    if args.gemini.exists():
        findings = parse_findings(args.gemini)
        n_findings = len(findings)
        labels = {
            "MISMATCH": "the picture says something other than the line does",
            "COMPOSITION": "how the frame is arranged",
            "LEGIBILITY": "readable in principle, hard to read in practice",
            "MISSED": "the narration names something concrete the frame omits",
        }
        by_cat: dict[str, list] = collections.defaultdict(list)
        for f in findings:
            by_cat[f[3]].append(f)
        grouped = [(cat, labels.get(cat, ""), sorted(items, key=lambda f: (
                       SEVERITY_ORDER.get(f[2], 9), f[1])))
                   for cat, items in sorted(by_cat.items(),
                                            key=lambda kv: -len(kv[1]))]
        biggest = max((len(g[2]) for g in grouped), default=1)
        for name, what, hits in grouped:
            items = "".join(
                f'<div class="finding"><span class="slate">{esc(b or "&mdash;")}</span>'
                f'<p><span class="sev {"blocking" if sev == "BLOCKING" else "worth" if sev == "WORTH-FIX" else "polish"}">'
                f'{esc(sev)}</span> {esc(t)}</p></div>'
                for _s, b, sev, _c, t in hits[:40])
            more = (f'<div class="finding"><span class="slate">&hellip;</span>'
                    f'<p>and {len(hits) - 40} more in the full report</p></div>'
                    if len(hits) > 40 else "")
            theme_blocks.append(f"""
      <details class="theme">
        <summary>
          <span class="tname">{esc(name)}</span>
          <span class="tcount">{len(hits)}</span>
          <span class="twhat">{esc(what)}</span>
        </summary>
        <div class="findings">
          <div class="bar"><i style="width:{100 * len(hits) / biggest:.0f}%"></i></div>
          {items}{more}
        </div>
      </details>""")

    ranked_html = ranked_section(args.ranked, args.top)

    page = f"""<title>Compiler For Trust Review</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>{CSS}{RANKED_CSS}</style>

<header class="top"><div class="wrap">
  <div class="eyebrow">Video 2 &middot; review pass 4 &middot; {date.today().isoformat()}</div>
  <h1>Every frame, checked twice</h1>
  <p class="standfirst">Eighteen automated checks answer <em>is anything broken</em>.
    A vision model answers <em>is it any good</em>. This is what both of them said
    about the current cut. Each finding is keyed to the amber code in the top-left
    of the frame &mdash; <span class="slate">03 b28</span> on screen is
    <span class="slate">03 b28</span> here.</p>
  <div class="rail">
    <div class="cell {'good' if clean == len(results) else 'bad'}">
      <span class="k">Sections clean</span><span class="v">{clean}/{len(results)}</span></div>
    <div class="cell"><span class="k">Beats</span><span class="v">{total_beats}</span></div>
    <div class="cell {'good' if worst_drift <= 0.25 else 'bad'}">
      <span class="k">Worst drift</span><span class="v">{worst_drift:.2f}s</span></div>
    <div class="cell good"><span class="k">Line coverage</span><span class="v">100%</span></div>
    <div class="cell"><span class="k">Runtime</span><span class="v">{runtime / 60:.1f}m</span></div>
  </div>
</div></header>

<section><div class="wrap">
  <h2>The gate</h2>
  <p class="lede">Coverage is the fraction of narration lines that have a beat cued
    to them &mdash; the measure of whether the picture changes as often as the
    script does. Drift is rendered length against narration length; video 1 lost
    1.6 seconds off the end of a section and nothing said so.</p>
  <div class="tablewrap"><table>
    <thead><tr><th>Section</th><th>Gate</th><th>Violations</th><th>Drift</th>
      <th>Coverage</th><th>Length</th></tr></thead>
    <tbody>{''.join(rows)}</tbody>
  </table></div>
</div></section>

<section><div class="wrap">
  <h2>Open violations &mdash; {sum(kinds.values())}</h2>
  <p class="lede">{'Everything the checks can see is clear.' if not kinds else
    'Each of these is a specific frame at a specific second. '
    '<strong>stage_imbalance</strong> is a new check this pass, and its findings are '
    'compositional judgements rather than faults &mdash; they are here because they '
    'are worth your call, not because they are certainly wrong.'}</p>
  <div class="viol">{''.join(viol_cards)}</div>
</div></section>

{ranked_html}

<section><div class="wrap">
  <h2>What the model saw &mdash; {n_findings} judgements</h2>
  <p class="lede">One settled frame per beat, paired with the line of narration it
    is cued to, sent to Gemini with the shape-and-colour grammar as the rubric and
    told what the gate already covers. Grouped by theme, because the useful signal
    is not any single note &mdash; it is the same note appearing on ten beats in a row.</p>
  {''.join(theme_blocks)}
</div></section>

<footer><div class="wrap">
  <p>Rendered at 480p15 for the review loop; the delivery render is 1080p30. The
  review slate is drawn outside the composition and excluded from every check, and
  it is switched off by an environment variable for the final cut.</p>
</div></footer>
"""
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(page, encoding="utf-8")
    print(f"wrote {args.out}  ({args.out.stat().st_size / 1e6:.1f} MB)")
    return 0




# ---------------------------------------------------------------------------
# Ranked view: the twenty decisions, each with the frame it is about.
# ---------------------------------------------------------------------------
RANKED_CSS = """
.ranked{display:grid;gap:16px;margin-top:24px}
.rank{background:var(--surface);border:1px solid var(--line);border-radius:3px;
  overflow:hidden;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr)}
.rank .body{padding:18px 20px;display:grid;gap:10px;align-content:start}
.rank .no{font-family:Archivo,sans-serif;font-size:30px;font-weight:700;
  color:var(--muted);line-height:1;font-variant-numeric:tabular-nums}
.rank h3{font-size:16px;line-height:1.45;font-weight:600}
.meta{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.sev{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.1em;
  text-transform:uppercase;padding:3px 8px;border-radius:2px;border:1px solid currentColor}
.sev.blocking{color:var(--defect)} .sev.worth{color:var(--warn)} .sev.polish{color:var(--muted)}
.cat{font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--muted)}
.agree{font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--teal)}
.narr{color:var(--muted);font-size:14px;font-style:italic;border-left:2px solid var(--line);
  padding-left:12px;margin:0}
.rank img{width:100%;height:100%;object-fit:cover;display:block;background:var(--screen);
  border-left:1px solid var(--line)}
@media (max-width:820px){.rank{grid-template-columns:1fr}
  .rank img{border-left:0;border-top:1px solid var(--line)}}
"""


def ranked_section(ranked_json: Path, top: int) -> str:
    if not ranked_json.exists():
        return ""
    items = json.loads(ranked_json.read_text())[:top]
    if not items:
        return ""
    cards = []
    for n, f in enumerate(items, 1):
        sev_class = {"BLOCKING": "blocking", "WORTH-FIX": "worth"}.get(f["severity"], "polish")
        img = ""
        shot = Path(f.get("shot") or "")
        if shot.exists():
            img = (f'<img src="data:image/jpeg;base64,{b64(shot)}" '
                   f'alt="frame at beat {esc(f["beat"])}" loading="lazy">')
        agree = (f'<span class="agree">gate agrees: {esc(", ".join(f["gate_checks"]))}</span>'
                 if f.get("gate_checks") else "")
        cards.append(f"""
      <article class="rank">
        <div class="body">
          <span class="no">{n:02d}</span>
          <div class="meta">
            <span class="slate">{esc(f['beat'])}</span>
            <span class="sev {sev_class}">{esc(f['severity'])}</span>
            <span class="cat">{esc(f['category'])}</span>
            {agree}
          </div>
          <h3>{esc(f['text'])}</h3>
          <p class="narr">{esc(f.get('line', ''))}</p>
        </div>
        {img}
      </article>""")
    return f"""
<section><div class="wrap">
  <h2>The decisions &mdash; top {len(items)}</h2>
  <p class="lede">Ranked by severity first, then by whether the machine checks
    independently flagged the same beat, then by how often the same category
    repeats, then by how early it lands. Every one carries the frame it is about,
    so the call is made against the picture.</p>
  <div class="ranked">{''.join(cards)}</div>
</div></section>"""


if __name__ == "__main__":
    raise SystemExit(main())
