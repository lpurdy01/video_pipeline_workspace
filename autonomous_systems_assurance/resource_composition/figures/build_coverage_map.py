#!/usr/bin/env python3
"""Build the publication raster for the public-assurance coverage map.

The adjacent SVG remains the editable/vector video source. This PIL render is
used by the current PDF pipeline because its SVG renderer mishandles dense SVG
text. It contains no external assets or measured product data.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).with_name("assurance_coverage_map.png")
W, H = 1800, 1260
BG, PANEL, GRID = "#071322", "#0d2034", "#42617e"
TEXT, MUTED, GREEN, BLUE, PURPLE, RED, GREY, GOLD = "#eef7ff", "#b6cbdd", "#39c79a", "#4987cc", "#9c7ae5", "#f07678", "#3d5368", "#f5cb72"


def font(size, bold=False):
    name = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(name, size)


def txt(draw, xy, text, size=22, fill=TEXT, bold=False, anchor=None):
    draw.text(xy, text, font=font(size, bold), fill=fill, anchor=anchor)


def rounded(draw, box, fill, outline=None, radius=12, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def main():
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    txt(d, (60, 40), "Public assurance material has different coverage boundaries", 38, bold=True)
    txt(d, (60, 88), "Source-scoped map, not a safety ranking. Filled regions mean a document addresses a topic; they do not mean product approval.", 21, MUTED)

    rounded(d, (50, 130, 1750, 430), PANEL, GRID, 18)
    txt(d, (82, 158), "1. Delegated authority / end-user role in EASA’s proposed DS.AI", 23, MUTED, True)
    txt(d, (82, 190), "Proposed aviation taxonomy — not SAE road levels and not a general permission matrix. [C-RISK-006]", 18, MUTED)
    y, xs = 280, [160, 430, 700, 970, 1240, 1510]
    labels = [("1A", "information", "support", BLUE), ("1B", "decision support", "full user authority", BLUE), ("2A", "directed action", "full user authority", BLUE), ("2B", "supervised action", "partial user authority", BLUE), ("3A", "safeguarded action", "limited authority on alert", PURPLE), ("3B", "RESERVED", "no assignment in proposal", RED)]
    d.line((xs[0], y, xs[-1], y), fill="#d5e6f6", width=4)
    for x, (level, a, b, color) in zip(xs, labels):
        d.ellipse((x-24, y-24, x+24, y+24), fill=color)
        txt(d, (x, y), level, 16, BG, True, "mm")
        txt(d, (x, y+50), a, 18, GOLD if level == "3B" else TEXT, True if level == "3B" else False, "mt")
        txt(d, (x, y+78), b, 15, MUTED, False, "mt")
    txt(d, (82, 385), "Key boundary: Level 3B is reserved. This proposal does not define an approved no-human-involvement category.", 18, GOLD, True)

    rounded(d, (50, 455, 1750, 865), PANEL, GRID, 18)
    txt(d, (82, 483), "2. EASA’s proposed scenario risk matrix", 23, MUTED, True)
    txt(d, (82, 515), "Per operational hour. H1 potential fatalities is unacceptable in every proposed likelihood band. [C-RISK-007]", 18, MUTED)
    cols = [("Frequent", ">1E−3/hr"), ("Probable", "1E−3…1E−5/hr"), ("Remote", "1E−5…1E−7/hr"), ("Extremely remote", "1E−7…1E−9/hr"), ("Extremely improbable", "≤1E−9/hr")]
    left, cw, top, rh = 420, 250, 590, 56
    for i,(name,band) in enumerate(cols):
        x = left + i*cw + cw//2
        txt(d,(x,553),name,17,TEXT,True,"mt"); txt(d,(x,578),band,14,MUTED,False,"mt")
    rows = [("H1 fatalities", ["UNACCEPTABLE"]*5), ("H2 serious injury", ["UNACCEPTABLE","UNACCEPTABLE","UNACCEPTABLE","ACCEPTABLE","MODERATE"]), ("H3 significant degradation", ["UNACCEPTABLE","UNACCEPTABLE","ACCEPTABLE","MODERATE","MODERATE"]), ("H4 slight degradation", ["UNACCEPTABLE","ACCEPTABLE","MODERATE","MODERATE","MODERATE"])]
    for r,(name,cells) in enumerate(rows):
        yy=top+r*rh
        txt(d,(105,yy+rh//2),name,19,TEXT,True,"lm")
        for c,cell in enumerate(cells):
            color = RED if cell == "UNACCEPTABLE" else GREEN if cell == "ACCEPTABLE" else PURPLE
            d.rounded_rectangle((left+c*cw,yy,left+(c+1)*cw-4,yy+rh-4),radius=5,fill=color)
            txt(d,(left+c*cw+cw//2,yy+rh//2-2),cell,14,BG,True,"mm")
    txt(d,(82,835),"Green/purple are proposed classifications, not product evidence or safety outcomes. Quantitative tools supplement qualitative judgment.",17,GOLD)

    rounded(d, (50, 890, 1750, 1200), PANEL, GRID, 18)
    txt(d, (82, 918), "3. Document roles and open space", 23, MUTED, True)
    bands = [("AMLAS", "ML-component lifecycle: data, model, verification, deployment", 600, BLUE, "not whole system / approval [C-CHAL-006]"), ("UK MAA", "applicant-specific military path; fixed supervised model / defined domain", 760, BLUE, "not civil approval [C-CHAL-001]"), ("FAA roadmap", "learned-implementation problem framing and research direction", 510, GREY, "not a complete means of compliance [C-AUTH-010]"), ("NHTSA SGO", "incident reporting and oversight data", 400, GREY, "not normalized safety-rate evidence [C-DIR-003]")]
    yy=970
    for name, text, length, color, limit in bands:
        txt(d,(92,yy+17),name,19,TEXT,True,"lm")
        rounded(d,(270,yy,270+length,yy+34),color,None,5,0)
        txt(d,(286,yy+17),text,15,TEXT,False,"lm")
        txt(d,(1048,yy+17),limit,14,MUTED,False,"lm")
        yy+=53
    rounded(d,(1430,950,1715,1140),PURPLE,None,12,0)
    txt(d,(1452,978),"PROJECT PROPOSAL",18,TEXT,True)
    for i,line in enumerate(("connect domain, sensing,", "release, scenario evidence,", "recovery, and change.", "Names missing evidence;", "does not grant approval.")):
        txt(d,(1452,1014+i*24),line,15,TEXT)
    txt(d,(60,1230),"Red = unacceptable only in EASA’s proposed matrix. Blue/grey = source role. Nothing in this figure is a composite safety score.",16,MUTED)
    im.save(OUT, optimize=True)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
