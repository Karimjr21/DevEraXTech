import json, sys
OUT = sys.argv[1]
BX = 1010
CY = {k: 1000 + 1150 * k for k in range(1, 7)}

def rr(x1, y1, x2, y2, r, tail=None):
    """rounded rect, CCW from the top edge near the top-right corner, closed back there"""
    d = f"M {x2-r} {y1} L {x1+r} {y1} Q {x1} {y1} {x1} {y1+r} L {x1} {y2-r} Q {x1} {y2} {x1+r} {y2} "
    if tail:
        d += tail + " "
    d += f"L {x2-r} {y2} Q {x2} {y2} {x2} {y2-r} L {x2} {y1+r} Q {x2} {y1} {x2-r} {y1}"
    return d

def rrect_closed(x1, y1, x2, y2, r):
    return (f"M {x1+r} {y1} L {x2-r} {y1} Q {x2} {y1} {x2} {y1+r} L {x2} {y2-r} Q {x2} {y2} {x2-r} {y2} "
            f"L {x1+r} {y2} Q {x1} {y2} {x1} {y2-r} L {x1} {y1+r} Q {x1} {y1} {x1+r} {y1} Z")

def circ(cx, cy, r):
    return f"M {cx-r} {cy} a {r} {r} 0 1 0 {2*r} 0 a {r} {r} 0 1 0 {-2*r} 0"

objs = {}
# 1 website
c = CY[1]; x1, y1, x2, y2, r = 130, c-260, 950, c+260, 18
objs[1] = dict(start=(x2-r, y1), out=rr(x1, y1, x2, y2, r), thin=[
    f"M {x1} {y1+64} L {x2} {y1+64}", circ(x1+40, y1+32, 9),
    f"M {x2-330} {y1+32} l 56 0 M {x2-250} {y1+32} l 56 0", rrect_closed(x2-150, y1+16, x2-34, y1+48, 16),
    rrect_closed(x1+60, y1+330, x1+250, y1+388, 29), rrect_closed(x1+480, y1+110, x2-50, y2-50, 10),
    circ(x2-170, y1+190, 34),
    f"M {x1+480} {y2-50} L {x1+580} {y2-170} L {x1+650} {y2-110} L {x1+730} {y2-210} L {x2-50} {y2-90}",
    f"M {x1+60} {y1+250} L {x1+390} {y1+250} M {x1+60} {y1+282} L {x1+330} {y1+282}"],
    bars=[f"M {x1+60} {y1+150} L {x1+430} {y1+150} M {x1+60} {y1+198} L {x1+360} {y1+198}"])
# 2 phone
c = CY[2]; x1, y1, x2, y2, r = 370, c-320, 710, c+320, 52
objs[2] = dict(start=(x2-r, y1), out=rr(x1, y1, x2, y2, r), thin=[
    rrect_closed(490, y1+20, 590, y1+46, 13),
    rrect_closed(x1+24, y1+140, x2-24, y1+330, 18), rrect_closed(x1+24, y1+352, x2-24, y1+462, 18),
    rrect_closed(x1+24, y1+484, x2-24, y1+540, 18), f"M {x1} {y2-92} L {x2} {y2-92}",
    circ(x1+60, y2-48, 7), circ(x1+133, y2-48, 7), circ(x1+206, y2-48, 7), circ(x1+280, y2-48, 7)],
    bars=[f"M {x1+34} {y1+100} L {x1+180} {y1+100}", f"M {x1+48} {y1+292} L {x1+200} {y1+292}"])
# 3 desktop
c = CY[3]; x1, y1, x2, y2, r = 110, c-270, 950, c+270, 10
objs[3] = dict(start=(x2-r, y1), out=rr(x1, y1, x2, y2, r), thin=[
    f"M {x1} {y1+56} L {x2} {y1+56}", f"M {x2-152} {y1+28} l 22 0",
    rrect_closed(x2-102, y1+17, x2-80, y1+39, 2), f"M {x2-50} {y1+17} l 22 22 M {x2-28} {y1+17} l -22 22",
    f"M {x1+220} {y1+56} L {x1+220} {y2}",
    rrect_closed(x1+260, y1+90, x1+530, y1+260, 10), rrect_closed(x1+560, y1+90, x2-40, y1+260, 10),
    rrect_closed(x1+260, y1+290, x2-40, y2-40, 10),
    f"M {x1+290} {y2-80} L {x1+400} {y2-150} L {x1+500} {y2-120} L {x1+620} {y2-200} L {x1+740} {y2-170} L {x2-70} {y2-220}"],
    bars=[f"M {x1+30} {y1+28} l 120 0", f"M {x1+40} {y1+110} l 130 0 M {x1+40} {y1+160} l 100 0 M {x1+40} {y1+210} l 120 0 M {x1+40} {y1+260} l 90 0"])
# 4 AI chat bubble
c = CY[4]; x1, y1, x2, y2, r = 150, c-200, 930, c+170, 44
tail = f"L {x1+70} {y2} L {x1+40} {y2+80} L {x1+160} {y2}"
objs[4] = dict(start=(x2-r, y1), out=rr(x1, y1, x2, y2, r, tail), thin=[],
    bars=[], dots=[(x1+90, c-100), (x1+140, c-100), (x1+190, c-100)])
# 5 payment card
c = CY[5]; x1, y1, x2, y2, r = 200, c-215, 880, c+215, 30
objs[5] = dict(start=(x2-r, y1), out=rr(x1, y1, x2, y2, r), thin=[
    rrect_closed(x1+60, y1+90, x1+150, y1+160, 12), f"M {x1+60} {y1+125} l 90 0 M {x1+105} {y1+90} l 0 70",
    f"M {x1+196} {y1+108} q 12 17 0 34 M {x1+214} {y1+98} q 20 27 0 54 M {x1+232} {y1+88} q 28 37 0 74"],
    bars=[f"M {x1+60} {y1+260} l 100 0 M {x1+190} {y1+260} l 100 0 M {x1+320} {y1+260} l 100 0 M {x1+450} {y1+260} l 100 0",
          f"M {x1+60} {y2-70} l 220 0", f"M {x2-180} {y2-70} l 110 0"])
# 6 care plan shield
c = CY[6]; x1, y1, x2, y2 = 270, c-300, 810, c+330
out6 = (f"M {x2} {y1} L {x1} {y1} L {x1} {y1+290} C {x1} {y2-130} 450 {y2-40} 540 {y2} "
        f"C 630 {y2-40} {x2} {y2-130} {x2} {y1+290} L {x2} {y1}")
objs[6] = dict(start=(x2, y1), out=out6, thin=[
    f"M 320 {c+10} L 430 {c+10} L 470 {c-80} L 520 {c+110} L 566 {c-30} L 600 {c+10} L 760 {c+10}"], bars=[])

def bus(frm, to=None, end_y=None):
    fx, fy = frm
    d = f"M {fx} {fy} L {BX-40} {fy} Q {BX} {fy} {BX} {fy+40} "
    if to:
        tx, ty = to
        d += f"L {BX} {ty-40} Q {BX} {ty} {BX-40} {ty} L {tx} {ty}"
    else:
        d += f"L {BX} {end_y}"
    return d

hook = (f"M -20 1000 L 380 1000 L 460 920 L 760 920 L 840 1000 L 970 1000 Q 1010 1000 1010 1040 "
        f"L 1010 {objs[1]['start'][1]-40} Q 1010 {objs[1]['start'][1]} 970 {objs[1]['start'][1]} L {objs[1]['start'][0]} {objs[1]['start'][1]}")
segs = [("hook", hook)]
for k in range(1, 7):
    segs.append((f"o{k}", objs[k]["out"]))
    segs.append((f"b{k}", bus(objs[k]["start"], objs[k+1]["start"] if k < 6 else None, end_y=CY[6]+470)))

svg_main = "\n".join(f'<path id="ol-{n}" class="main" d="{d}" />' for n, d in segs)
svg_thin = []
for k in range(1, 7):
    o = objs[k]
    g = "".join(f'<path class="thin" d="{d}" />' for d in o["thin"]) + "".join(f'<path class="bar" d="{d}" />' for d in o["bars"])
    g += "".join(f'<circle class="dot" cx="{x}" cy="{y}" r="15" />' for x, y in o.get("dots", []))
    svg_thin.append(f'<g id="ol-d{k}">{g}</g>')
svg_thin = "\n".join(svg_thin)

labels = [
    ("l0", None, None),
    ("l1", "WEBSITES", "E-COMMERCE · SHOPIFY · WORDPRESS"),
    ("l2", "MOBILE APPS", "iOS &amp; ANDROID FROM ONE CODEBASE"),
    ("l3", "DESKTOP SOFTWARE", "WINDOWS DESKTOP APPLICATIONS"),
    ("l4", "AI INTEGRATIONS", "WEBSITE CHATBOTS · WHATSAPP ASSISTANTS"),
    ("l5", "PAYMENTS", "PAYMOB · FAWRY · STRIPE"),
    ("l6", "CARE PLANS", "UPDATES · BACKUPS · UPTIME MONITORING"),
]
lab_html = '<div class="lab hook" id="ol-l0"><span class="a">It starts with</span><span class="b">one line.</span></div>\n'
for i, t, e in labels[1:]:
    lab_html += f'<div class="lab" id="ol-{i}"><span class="t">{t}</span><span class="e">{e}</span></div>\n'
lab_html += '<div class="lab" id="ol-l7"><span class="t g">One line.</span><span class="t">Everything we build.</span><span class="e">PLANNED, DESIGNED AND BUILT END TO END</span></div>'

# timeline numbers
S_END, Y_END = 0.42, 330.0
TX, TY = 801.0, 655.0            # logo's 4th ring terminal on screen (end card)
WX, WY = (TX - 540) / S_END + 540, (TY - Y_END) / S_END
cam = {k: 1000 - CY[k] for k in range(1, 7)}
cfg = dict(cam=cam, wx=WX, wy=WY, s_end=S_END, y_end=Y_END, cy6=CY[6], bubble=(150 + 60, CY[4] - 40))

html = open(sys.argv[2]).read()
html = (html.replace("__MAIN__", svg_main).replace("__THIN__", svg_thin).replace("__LABELS__", lab_html)
        .replace("__CFG__", json.dumps(cfg)))
open(OUT, "w").write(html)
print("ok", WX, WY)
