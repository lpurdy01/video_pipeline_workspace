"""Render the candidate selection page from the review data."""
from __future__ import annotations

import html
import json
from pathlib import Path

DATA = json.loads(Path("out/selection_data.json").read_text())

TITLES = {
    "01_generation_got_cheap": "Cold Open: Generation Got Cheap",
    "02_chat_log_fallacy": "The Hidden Cost Of “Looks Good”",
    "03_traceability_shape": "Safety-Critical Software Already Has The Shape",
    "04_artifact_graph": "Artifacts Become A Graph",
    "05_compilation_traversal": "Compilation Means Traversal",
    "06_vqp": "The Verification Query Package",
    "07_dual_mode_review": "Same Package, Two Review Modes",
    "08_evidence_cards": "Evidence Cards, Not Conversations",
    "09_readiness_map": "Verification Readiness Is A Map, Not Magic",
    "10_evidence_surface": "Closing: The Future Is Evidence Generation",
}

SET_NAME = {"A": "Diagrammatic", "B": "Mechanistic", "C": "Concrete"}
SET_BLURB = {
    "A": "State the idea as a clean labelled diagram.",
    "B": "Show the process happening.",
    "C": "Put the real artifact on screen.",
}

CSS = """
:root {
  --ground: #EFF2F6;
  --surface: #FFFFFF;
  --surface-2: #F6F8FB;
  --line: #D8DEE8;
  --line-soft: #E7ECF3;
  --ink: #12151C;
  --muted: #5C6577;
  --gold: #96690F;
  --gold-soft: #F6EBD3;
  --teal: #0A7365;
  --defect: #A62B44;
  --screen: #05070E;
  --shadow: 0 1px 2px rgba(18,21,28,.06), 0 8px 24px rgba(18,21,28,.05);
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --ground: #080B12;
    --surface: #10141E;
    --surface-2: #151A26;
    --line: #232B3C;
    --line-soft: #1B2231;
    --ink: #E9EDF6;
    --muted: #8791A8;
    --gold: #FFCB4D;
    --gold-soft: #2A2105;
    --teal: #20F7D2;
    --defect: #FF6B85;
    --screen: #05070E;
    --shadow: 0 1px 2px rgba(0,0,0,.4), 0 10px 30px rgba(0,0,0,.35);
  }
}
:root[data-theme="dark"] {
  --ground: #080B12;
  --surface: #10141E;
  --surface-2: #151A26;
  --line: #232B3C;
  --line-soft: #1B2231;
  --ink: #E9EDF6;
  --muted: #8791A8;
  --gold: #FFCB4D;
  --gold-soft: #2A2105;
  --teal: #20F7D2;
  --defect: #FF6B85;
  --screen: #05070E;
  --shadow: 0 1px 2px rgba(0,0,0,.4), 0 10px 30px rgba(0,0,0,.35);
}

* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--ground);
  color: var(--ink);
  font-family: "IBM Plex Sans", ui-sans-serif, system-ui, sans-serif;
  font-size: 16px;
  line-height: 1.55;
  -webkit-font-smoothing: antialiased;
}
h1, h2, h3 { font-family: "Archivo", ui-sans-serif, system-ui, sans-serif; text-wrap: balance; margin: 0; }
.mono { font-family: "IBM Plex Mono", ui-monospace, monospace; font-variant-numeric: tabular-nums; }

.wrap { max-width: 1180px; margin: 0 auto; padding: 0 28px; }

/* ---------- masthead ---------- */
header.top { border-bottom: 1px solid var(--line); background: var(--surface); }
.masthead { padding: 44px 0 34px; display: grid; gap: 22px; }
.eyebrow {
  font-family: "IBM Plex Mono", monospace; font-size: 12px; letter-spacing: .14em;
  text-transform: uppercase; color: var(--muted);
}
h1 { font-size: clamp(30px, 4.2vw, 46px); font-weight: 700; letter-spacing: -.02em; line-height: 1.08; }
.standfirst { max-width: 62ch; color: var(--muted); font-size: 17px; }
.facts { display: flex; flex-wrap: wrap; gap: 10px 28px; padding-top: 4px; }
.fact { display: grid; gap: 2px; }
.fact dt { font-family: "IBM Plex Mono", monospace; font-size: 11px; letter-spacing: .12em;
  text-transform: uppercase; color: var(--muted); }
.fact dd { margin: 0; font-size: 15px; font-weight: 500; }

/* ---------- legend ---------- */
.legend { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; padding: 22px 0 30px; }
.legend-item { border: 1px solid var(--line); border-radius: 3px; background: var(--surface);
  padding: 14px 16px; display: grid; gap: 4px; }
.legend-item .k { font-family: "Archivo", sans-serif; font-weight: 700; font-size: 15px; }
.legend-item .v { color: var(--muted); font-size: 14px; }

/* ---------- sticky progress ---------- */
.bar {
  position: sticky; top: 0; z-index: 20; background: var(--surface);
  border-bottom: 1px solid var(--line);
  display: flex; align-items: center; gap: 18px; flex-wrap: wrap;
  padding: 11px 0;
}
.bar .wrap { display: flex; align-items: center; gap: 18px; flex-wrap: wrap; width: 100%; }
.count { font-family: "IBM Plex Mono", monospace; font-size: 13px; color: var(--muted); }
.count b { color: var(--ink); font-size: 15px; }
.track { flex: 1; min-width: 120px; height: 4px; background: var(--line-soft); border-radius: 99px; overflow: hidden; }
.track span { display: block; height: 100%; width: 0%; background: var(--gold); transition: width .25s ease; }
button.act {
  font-family: "IBM Plex Sans", sans-serif; font-size: 13px; font-weight: 600;
  border: 1px solid var(--line); background: var(--surface-2); color: var(--ink);
  padding: 7px 14px; border-radius: 3px; cursor: pointer;
}
button.act:hover { border-color: var(--gold); }
button.act:focus-visible { outline: 2px solid var(--gold); outline-offset: 2px; }

/* ---------- sections ---------- */
section.sec { padding: 46px 0; border-bottom: 1px solid var(--line-soft); }
.sec-head { display: grid; grid-template-columns: auto 1fr; gap: 18px; align-items: baseline; margin-bottom: 6px; }
.sec-num { font-family: "IBM Plex Mono", monospace; font-size: 13px; color: var(--gold);
  letter-spacing: .1em; padding-top: 6px; }
.sec-title { font-size: clamp(20px, 2.4vw, 27px); font-weight: 700; letter-spacing: -.015em; }
.sec-meta { color: var(--muted); font-size: 14px; margin: 6px 0 24px 0; padding-left: 46px; }

.grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }

.card {
  border: 1px solid var(--line); border-radius: 3px; background: var(--surface);
  display: grid; grid-template-rows: auto auto 1fr auto; overflow: hidden;
  box-shadow: var(--shadow);
  border-left: 3px solid transparent;
}
.card.picked { border-left-color: var(--gold); background: var(--surface-2); }
.card-head { padding: 13px 15px 11px; display: grid; gap: 3px; border-bottom: 1px solid var(--line-soft); }
.card-head .row { display: flex; align-items: center; gap: 9px; flex-wrap: wrap; }
.letter { font-family: "Archivo", sans-serif; font-weight: 700; font-size: 15px; }
.setname { font-size: 13px; color: var(--muted); }
.chip {
  font-family: "IBM Plex Mono", monospace; font-size: 10px; letter-spacing: .1em; text-transform: uppercase;
  padding: 3px 7px; border-radius: 2px; border: 1px solid var(--gold); color: var(--gold);
  background: var(--gold-soft);
}
.scene { font-family: "IBM Plex Mono", monospace; font-size: 12px; color: var(--muted); }

/* the film strip always sits on the project's own near-black, in either theme */
.strip { background: var(--screen); padding: 8px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 4px; }
.strip img { width: 100%; display: block; border-radius: 1px; }

.defects { padding: 13px 15px; display: grid; gap: 7px; align-content: start; }
.defects h4 {
  font-family: "IBM Plex Mono", monospace; font-size: 10px; letter-spacing: .12em;
  text-transform: uppercase; color: var(--muted); margin: 0; font-weight: 500;
}
.defects ul { margin: 0; padding: 0; list-style: none; display: grid; gap: 6px; }
.defects li { font-size: 13.5px; line-height: 1.45; color: var(--ink); padding-left: 14px; position: relative; }
.defects li::before {
  content: ""; position: absolute; left: 0; top: 8px; width: 5px; height: 5px;
  border-radius: 50%; background: var(--defect);
}
.defects .none { font-size: 13.5px; color: var(--teal); }

.pick { border: 0; border-top: 1px solid var(--line-soft); background: transparent; color: var(--muted);
  font-family: "IBM Plex Sans", sans-serif; font-size: 13px; font-weight: 600; padding: 11px;
  cursor: pointer; text-align: center; }
.pick:hover { color: var(--ink); background: var(--surface-2); }
.pick:focus-visible { outline: 2px solid var(--gold); outline-offset: -3px; }
.card.picked .pick { color: var(--gold); }

/* ---------- verdict panels ---------- */
.panels { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 18px; }
.panel { border: 1px solid var(--line); border-radius: 3px; background: var(--surface); padding: 15px 17px; }
.panel h4 {
  font-family: "IBM Plex Mono", monospace; font-size: 10px; letter-spacing: .12em; text-transform: uppercase;
  color: var(--muted); margin: 0 0 7px 0; font-weight: 500;
}
.panel p { margin: 0; font-size: 14px; line-height: 1.5; }
.panel.gap { border-left: 3px solid var(--defect); }

footer { padding: 40px 0 70px; color: var(--muted); font-size: 14px; }
footer p { max-width: 68ch; }

@media (max-width: 900px) {
  .grid, .legend, .panels { grid-template-columns: 1fr; }
  .sec-meta { padding-left: 0; }
}
@media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
"""


def esc(text: str) -> str:
    return html.escape(text, quote=False)


def card_html(section_id: str, letter: str, cand: dict, recommended: bool) -> str:
    frames = "".join(
        f'<img src="data:image/jpeg;base64,{b64}" alt="{letter} keyframe {i+1}" loading="lazy">'
        for i, b64 in enumerate(cand["frames"])
    )
    if cand["defects"]:
        items = "".join(f"<li>{esc(d)}</li>" for d in cand["defects"])
        defects = f"<h4>Defects found</h4><ul>{items}</ul>"
    else:
        defects = '<h4>Defects found</h4><p class="none">None flagged.</p>'
    chip = '<span class="chip">Gemini pick</span>' if recommended else ""
    return f"""
      <article class="card" data-section="{section_id}" data-set="{letter}">
        <div class="card-head">
          <div class="row"><span class="letter">{letter}</span>
            <span class="setname">{SET_NAME[letter]}</span>{chip}</div>
          <div class="scene">{esc(cand['scene'])} · {cand['duration']}s</div>
        </div>
        <div class="strip">{frames}</div>
        <div class="defects">{defects}</div>
        <button class="pick" type="button">Select {letter}</button>
      </article>"""


def section_html(item: dict) -> str:
    num = item["id"][:2]
    title = TITLES[item["id"]]
    cards = "".join(
        card_html(item["id"], s, item["candidates"][s], item["recommended"] == s)
        for s in "ABC"
    )
    return f"""
    <section class="sec" id="s{num}">
      <div class="wrap">
        <div class="sec-head">
          <div class="sec-num">{num}</div>
          <h2 class="sec-title">{esc(title)}</h2>
        </div>
        <p class="sec-meta">{esc(item['recommendation'])}</p>
        <div class="grid">{cards}</div>
        <div class="panels">
          <div class="panel">
            <h4>Suggested hybrid</h4>
            <p>{esc(item['hybrid'])}</p>
          </div>
          <div class="panel gap">
            <h4>Narration with no visual</h4>
            <p>{esc(item['mismatch'])}</p>
          </div>
        </div>
      </div>
    </section>"""


legend = "".join(
    f'<div class="legend-item"><div class="k">{s} · {SET_NAME[s]}</div>'
    f'<div class="v">{SET_BLURB[s]}</div></div>'
    for s in "ABC"
)
sections = "".join(section_html(item) for item in DATA)
tally = {s: sum(1 for d in DATA if d["recommended"] == s) for s in "ABC"}

page = f"""<title>Compiler For Trust Candidates</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>{CSS}</style>

<header class="top">
  <div class="wrap masthead">
    <div class="eyebrow">Verification Compiler · video two · candidate selection</div>
    <h1>Three ways to draw the same argument</h1>
    <p class="standfirst">Every section of <em>The Compiler For Trust</em> now has three competing
      visual treatments, all rendered in Manim. Pick one per section. Keyframes are sampled at 25%,
      55% and 90% of each clip; the defect lists are Gemini's, and are developmental input only —
      the choice is yours.</p>
    <div class="facts">
      <div class="fact"><dt>Sections</dt><dd>10</dd></div>
      <div class="fact"><dt>Candidates</dt><dd>30</dd></div>
      <div class="fact"><dt>Reviewer</dt><dd class="mono">gemini-3.1-pro-preview</dd></div>
      <div class="fact"><dt>Gemini tally</dt><dd class="mono">A {tally['A']} · B {tally['B']} · C {tally['C']}</dd></div>
    </div>
    <div class="legend">{legend}</div>
  </div>
</header>

<div class="bar">
  <div class="wrap">
    <span class="count"><b id="n">0</b> of 10 chosen</span>
    <span class="track"><span id="fill"></span></span>
    <button class="act" type="button" id="take-gemini">Start from Gemini's picks</button>
    <button class="act" type="button" id="copy">Copy decisions</button>
    <button class="act" type="button" id="clear">Clear</button>
  </div>
</div>

{sections}

<footer>
  <div class="wrap">
    <p>Renders live in <span class="mono">verification_compiler_video/manim_prototypes/</span>.
    Side-by-side clips are in <span class="mono">out/candidates/*_ABC.mp4</span>, full review text in
    <span class="mono">out/reviews/</span>. Selections are stored in this browser only.</p>
  </div>
</footer>

<script>
(function () {{
  var KEY = "vc-video2-picks";
  var GEMINI = {json.dumps({d["id"]: d["recommended"] for d in DATA})};
  var TITLES = {json.dumps(TITLES)};
  var picks = {{}};

  try {{ picks = JSON.parse(localStorage.getItem(KEY) || "{{}}"); }} catch (e) {{ picks = {{}}; }}

  function paint() {{
    document.querySelectorAll(".card").forEach(function (card) {{
      var on = picks[card.dataset.section] === card.dataset.set;
      card.classList.toggle("picked", on);
      card.querySelector(".pick").textContent = on ? "Selected " + card.dataset.set
                                                   : "Select " + card.dataset.set;
    }});
    var n = Object.keys(picks).length;
    document.getElementById("n").textContent = n;
    document.getElementById("fill").style.width = (n / 10 * 100) + "%";
  }}

  function save() {{
    try {{ localStorage.setItem(KEY, JSON.stringify(picks)); }} catch (e) {{ /* private mode */ }}
    paint();
  }}

  document.querySelectorAll(".card .pick").forEach(function (btn) {{
    btn.addEventListener("click", function () {{
      var card = btn.closest(".card");
      if (picks[card.dataset.section] === card.dataset.set) {{
        delete picks[card.dataset.section];
      }} else {{
        picks[card.dataset.section] = card.dataset.set;
      }}
      save();
    }});
  }});

  document.getElementById("take-gemini").addEventListener("click", function () {{
    picks = Object.assign({{}}, GEMINI);
    save();
  }});

  document.getElementById("clear").addEventListener("click", function () {{
    picks = {{}};
    save();
  }});

  document.getElementById("copy").addEventListener("click", function () {{
    var lines = ["# Video 2 — chosen visual treatments", ""];
    Object.keys(TITLES).sort().forEach(function (id) {{
      var p = picks[id];
      lines.push("- " + id + " — " + (p ? "set " + p : "undecided") + "  (" + TITLES[id] + ")");
    }});
    var text = lines.join("\\n");
    var btn = document.getElementById("copy");
    navigator.clipboard.writeText(text).then(function () {{
      btn.textContent = "Copied";
      setTimeout(function () {{ btn.textContent = "Copy decisions"; }}, 1600);
    }}, function () {{
      btn.textContent = "Copy failed";
      setTimeout(function () {{ btn.textContent = "Copy decisions"; }}, 1600);
    }});
  }});

  paint();
}})();
</script>
"""

out = Path("out/candidate_selection.html")
out.write_text(page, encoding="utf-8")
print(f"wrote {out}  ({out.stat().st_size/1_048_576:.2f} MB)")
