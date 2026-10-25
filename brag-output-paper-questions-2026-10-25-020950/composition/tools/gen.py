"""Paper questions film: reuses the napkin film's pencil toolkit (geometry, CSS, draw/boil helpers)."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, "napkin_gen.py")).read()
exec(_src.split("# ======================================================================")[0])  # helpers only
# undrawn strokes: push the dash fully into the gap so round caps leave no dot behind
DRAW_JS = DRAW_JS.replace('p.style.strokeDasharray = L + " " + (L + 4);\n      p.dataset.len = L;', 'p.style.strokeDasharray = L + " " + (L + 16);\n      p.dataset.len = L + 8;')
assert "L + 16" in DRAW_JS

OUT = os.path.join(HERE, "..", "compositions")

CARD_CSS = '''    .card {
      position: absolute;
      left: 110px;
      top: 700px;
      width: 860px;
      height: 440px;
      background:
        linear-gradient(90deg, rgba(0, 0, 0, 0) 92px, rgba(184, 145, 42, 0.55) 92px, rgba(184, 145, 42, 0.55) 95px, rgba(0, 0, 0, 0) 95px),
        repeating-linear-gradient(180deg, rgba(0, 0, 0, 0) 0, rgba(0, 0, 0, 0) 55px, rgba(90, 110, 130, 0.16) 55px, rgba(90, 110, 130, 0.16) 57px),
        #fffdf6;
      box-shadow: 0 26px 48px rgba(90, 70, 30, 0.24);
      transform-origin: 50% 50%;
    }
    .card .q {
      position: absolute;
      left: 128px;
      top: 74px;
      width: 690px;
      font-family: "Playfair Display", serif;
      font-style: italic;
      font-size: 74px;
      line-height: 1.13;
      color: #2f2d29;
    }
'''

def card(cid, text, extra=""):
    return f'      <div class="card" id="{cid}"><div class="q">{text}</div>{extra}</div>'

SLAM_JS = '''    // a question card is slapped onto the page: no count, no warning
    function slam(sel, t, rot) {
      tl.fromTo(sel, { opacity: 0, scale: 1.18, rotation: rot - 7, y: -70 }, { opacity: 1, scale: 1, rotation: rot, y: 0, duration: 0.24, ease: "power4.out" }, t);
    }
    function toss(sel, t, dir) {
      tl.to(sel, { x: 900 * dir, y: -260, rotation: 24 * dir, opacity: 0, duration: 0.42, ease: "power3.in" }, t);
    }
'''

def ttl(tid, *lines, n=None):
    nn = f'<span class="n">{n}</span>' if n else ""
    return f'      <div class="ttl" id="{tid}">{nn}' + "".join(f'<span class="t">{l}</span>' for l in lines) + "</div>"

def svgwrap(inner, wid="", style=""):
    return f'<svg {wid} width="1080" height="1920" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0;overflow:visible;{style}">{inner}</svg>'

# ======================================================================
# Q1 — question card + crossed-out guesses (0 – 8.0)
# ======================================================================
code_doodle = [
    ([(720, 330), (690, 360), (720, 390)], dict(j=0.8, step=6)),
    ([(770, 320), (748, 400)], dict(j=0.8, step=6)),
    ([(798, 330), (828, 360), (798, 390)], dict(j=0.8, step=6)),
]
CD_A, _ = boil_paths("pencil", code_doodle, seeds=(21, 22))
strike1 = hand([(170, 1262), (420, 1250)], 31, j=1.4, step=8)
strike2 = hand([(560, 1262), (920, 1248)], 32, j=1.4, step=8)
arrow = hand(curve((780, 1188), (840, 1200), (812, 1240)) + [(800, 1228)], 33, j=0.7, step=6)
q1_body = card("q1c", "What do we do before writing any code?", f'<svg width="860" height="440" viewBox="0 0 860 440" style="position:absolute;left:0;top:0;overflow:visible"><g id="q1-cd">{CD_A}</g></svg>') + f'''
      <div class="hw" id="q1-ans" style="left:300px;top:1168px;font-size:62px;color:#7a5c0e">answer at the end ↓</div>
      <div class="hw" id="q1-g1" style="left:180px;top:1196px;font-size:104px">code?</div>
      <div class="hw" id="q1-g2" style="left:570px;top:1196px;font-size:104px">designs?</div>
      {svgwrap(f'<path class="pencil" id="q1-s1" d="{strike1}" /><path class="pencil" id="q1-s2" d="{strike2}" />')}'''
q1_js = SLAM_JS + '''    // frame 0: the card is already on the page; motion inside the first second
    gsap.set("#q1c", { rotation: -2 });
    D("#q1-cd path", false);
    D("#q1-s1,#q1-s2", false);
    gsap.set(["#q1-g1", "#q1-g2"], { clipPath: "inset(0% 100% 0% 0%)" });
    gsap.set("#q1-ans", { clipPath: "inset(0% 30% 0% 0%)", rotation: -2 });
    tl.to("#q1-ans", { clipPath: "inset(0% 0% 0% 0%)", duration: 0.5, ease: "steps(6)" }, 0.1);
    draw("#q1-cd path", 0.35, 0.25, 0.18);
    tl.fromTo("#q1c", { y: 0 }, { y: -8, duration: 3.6, ease: "sine.inOut" }, 0.2);
    // wrong guesses, written then crossed out
    tl.to("#q1-ans", { opacity: 0, duration: 0.2 }, 3.7);
    tl.to("#q1-g1", { clipPath: "inset(0% 0% 0% 0%)", duration: 0.5, ease: "steps(6)" }, 3.95);
    draw("#q1-s1", 4.7, 0.25);
    tl.to("#q1-g2", { clipPath: "inset(0% 0% 0% 0%)", duration: 0.6, ease: "steps(9)" }, 5.4);
    draw("#q1-s2", 6.2, 0.25);
    tl.to(["#q1c", "#q1-g1", "#q1-g2", "#q1-s1", "#q1-s2"], { opacity: 0, y: 40, duration: 0.3, ease: "power2.in" }, 7.55);'''
write("q1", comp("q1", 8.0, CARD_CSS, q1_body, q1_js))

# ======================================================================
# surprise cards
# ======================================================================
for cid, text, rot, dur in [("q2", "Will it work on every screen?", 3, 2.49), ("q3", "Can we fix a website we didn't build?", -3, 3.43)]:
    body = card(f"{cid}c", text)
    js = SLAM_JS + f'''    gsap.set("#{cid}c", {{ opacity: 0 }});
    slam("#{cid}c", 0.0, {rot});
    toss("#{cid}c", {dur - 0.45:.2f}, {1 if rot > 0 else -1});'''
    write(cid, comp(cid, dur, CARD_CSS, body, js))

# ======================================================================
# Answer 2 — one layout, every screen (9.05 – 16.55)
# ======================================================================
def desk():
    x1, y1, x2, y2 = 110, 700, 970, 1220
    return [
        (rrect(x1, y1, x2, y2, 18), dict(close=True, j=1.5, step=14)),
        ([(x1, y1 + 50), (x2, y1 + 50)], dict(j=0.7)),
        (ellipse(x1 + 34, y1 + 25, 8, 8, turns=1.0, n=14), dict(j=0.3, step=4)),
        (ellipse(x1 + 60, y1 + 25, 8, 8, turns=1.0, n=14), dict(j=0.3, step=4)),
        ([(x2 - 260, y1 + 25), (x2 - 40, y1 + 25)], dict(j=0.6)),
        ([(x1 + 50, y1 + 130), (x1 + 400, y1 + 130)], dict(j=0.9)),
        ([(x1 + 50, y1 + 185), (x1 + 330, y1 + 185)], dict(j=0.9)),
        (rrect(x1 + 50, y1 + 230, x1 + 230, y1 + 280, 25), dict(close=True, j=0.9)),
        (rrect(x1 + 470, y1 + 100, x2 - 50, y1 + 300, 12), dict(close=True, j=1.0)),
        (rrect(x1 + 50, y1 + 340, x1 + 290, y2 - 40, 12), dict(close=True, j=1.0)),
        (rrect(x1 + 310, y1 + 340, x1 + 550, y2 - 40, 12), dict(close=True, j=1.0)),
        (rrect(x1 + 570, y1 + 340, x2 - 50, y2 - 40, 12), dict(close=True, j=1.0)),
    ]

def tab():
    x1, y1, x2, y2 = 280, 640, 800, 1340
    return [
        (rrect(x1, y1, x2, y2, 30), dict(close=True, j=1.5, step=14)),
        ([(x1 + 40, y1 + 70), (x1 + 300, y1 + 70)], dict(j=0.8)),
        ([(x1 + 40, y1 + 115), (x1 + 230, y1 + 115)], dict(j=0.8)),
        (rrect(x1 + 40, y1 + 160, x2 - 40, y1 + 380, 14), dict(close=True, j=1.0)),
        (rrect(x1 + 40, y1 + 410, x1 + 245, y2 - 50, 14), dict(close=True, j=1.0)),
        (rrect(x1 + 275, y1 + 410, x2 - 40, y2 - 50, 14), dict(close=True, j=1.0)),
    ]

def phone():
    x1, y1, x2, y2 = 380, 660, 700, 1320
    return [
        (rrect(x1, y1, x2, y2, 44), dict(close=True, j=1.5, step=14)),
        ([(x1 + 115, y1 + 28), (x2 - 115, y1 + 28)], dict(j=0.5)),
        ([(x1 + 34, y1 + 100), (x1 + 220, y1 + 100)], dict(j=0.8)),
        (rrect(x1 + 30, y1 + 140, x2 - 30, y1 + 330, 14), dict(close=True, j=1.0)),
        (rrect(x1 + 30, y1 + 360, x2 - 30, y1 + 500, 14), dict(close=True, j=1.0)),
        (rrect(x1 + 30, y2 - 120, x2 - 30, y2 - 50, 35), dict(close=True, j=1.0)),
    ]

DK_A, DK_B = boil_paths("pencil", desk(), seeds=(41, 42))
TB_A, TB_B = boil_paths("pencil", tab(), seeds=(43, 44))
PH_A, PH_B = boil_paths("pencil", phone(), seeds=(45, 46))
a2_css = '''    .dev {
      position: absolute;
      left: 0;
      top: 0;
      width: 1080px;
      height: 1920px;
    }
    .lab {
      position: absolute;
      font-family: "Caveat", cursive;
      font-weight: 600;
      font-size: 54px;
      color: #7a5c0e;
    }
'''
a2_body = "\n".join([
    ttl("a2-t1", "Desktop."), ttl("a2-t2", "Tablet."), ttl("a2-t3", "Phone."), ttl("a2-t4", "Fast, responsive", "and scalable."),
    f'      <div class="dev" id="a2-dk">{svgwrap(f"<g class=\"gA\">{DK_A}</g><g class=\"gB\">{DK_B}</g>")}</div>',
    f'      <div class="dev" id="a2-tb">{svgwrap(f"<g class=\"gA\">{TB_A}</g><g class=\"gB\">{TB_B}</g>")}</div>',
    f'      <div class="dev" id="a2-ph">{svgwrap(f"<g class=\"gA\">{PH_A}</g><g class=\"gB\">{PH_B}</g>")}</div>',
])
a2_js = '''    // host starts 9.05 s: the same layout, redrawn for each screen
    gsap.set(["#a2-t1", "#a2-t2", "#a2-t3", "#a2-t4"], { opacity: 0, filter: "blur(8px)" });
    gsap.set(".gB", { opacity: 0 });
    D(".gA path", false);
    gsap.set("#a2-dk", { transformOrigin: "540px 960px" });
    gsap.set("#a2-tb", { transformOrigin: "540px 990px" });
    gsap.set("#a2-ph", { transformOrigin: "540px 990px" });
    const T = (id, a, b) => {
      tl.to(id, { opacity: 1, filter: "blur(0px)", duration: 0.3, ease: "power2.out" }, a);
      if (b) tl.to(id, { opacity: 0, filter: "blur(8px)", duration: 0.22, ease: "power2.in" }, b);
    };
    T("#a2-t1", 0.25, 1.85); T("#a2-t2", 2.1, 3.65); T("#a2-t3", 3.9, 5.45); T("#a2-t4", 5.7, 7.2);
    draw("#a2-dk .gA path", 0.25, 0.42, 0.07);
    tl.to("#a2-dk", { scaleX: 0.62, opacity: 0, duration: 0.3, ease: "power3.in" }, 1.75);
    draw("#a2-tb .gA path", 2.05, 0.42, 0.08);
    tl.to("#a2-tb", { scaleX: 0.62, opacity: 0, duration: 0.3, ease: "power3.in" }, 3.55);
    draw("#a2-ph .gA path", 3.85, 0.42, 0.08);
    // all three, side by side, on one baseline (5.5 s)
    tl.to("#a2-ph", { x: 320, y: 125, scale: 0.42, duration: 0.55, ease: "power3.inOut" }, 5.45);
    tl.fromTo("#a2-dk", { scaleX: 0.42, scaleY: 0.48, opacity: 0, x: -280, y: 165 }, { scaleX: 0.48, scaleY: 0.48, opacity: 1, duration: 0.5, ease: "expo.out", immediateRender: false }, 5.6);
    tl.fromTo("#a2-tb", { scale: 0.36, opacity: 0, x: 80, y: 120 }, { scale: 0.4, opacity: 1, duration: 0.5, ease: "expo.out", immediateRender: false }, 5.7);
    boil(".gA", ".gB", 6.2, 1.0);
    tl.to(["#a2-dk", "#a2-tb", "#a2-ph"], { opacity: 0, y: "+=40", duration: 0.25, ease: "power2.in" }, 7.25);'''
write("a2", comp("a2", 7.5, a2_css, a2_body, a2_js))

# ======================================================================
# Answer 3 — a site we didn't build: review, then fix (17.95 – 25.85)
# ======================================================================
X1, Y1, X2, Y2 = 110, 660, 970, 1250
messy = [
    (rrect(X1, Y1, X2, Y2, 16), dict(close=True, j=1.6, step=14)),
    ([(X1, Y1 + 50), (X2, Y1 + 50)], dict(j=0.7)),
    ([(X1 + 60, Y1 + 140), (X1 + 330, Y1 + 160), (X1 + 420, Y1 + 120)], dict(j=2.6)),
    ([(X1 + 60, Y1 + 200), (X1 + 380, Y1 + 230)], dict(j=2.4)),
    ([(X1 + 500, Y1 + 110), (X2 - 60, Y1 + 150), (X2 - 90, Y1 + 330), (X1 + 470, Y1 + 300), (X1 + 500, Y1 + 110)], dict(j=2.0)),
    ([(X1 + 500, Y1 + 110), (X2 - 90, Y1 + 330)], dict(j=1.4)),
    ([(X1 + 60, Y1 + 400), (X1 + 360, Y1 + 380), (X1 + 300, Y1 + 520), (X1 + 70, Y1 + 500), (X1 + 60, Y1 + 400)], dict(j=2.2)),
    ([(X1 + 420, Y1 + 410), (X2 - 60, Y1 + 440)], dict(j=2.4)),
    ([(X1 + 430, Y1 + 470), (X2 - 140, Y1 + 500)], dict(j=2.4)),
]
clean = [
    (rrect(X1, Y1, X2, Y2, 16), dict(close=True, j=1.2, step=14)),
    ([(X1, Y1 + 50), (X2, Y1 + 50)], dict(j=0.5)),
    ([(X1 + 60, Y1 + 140), (X1 + 420, Y1 + 140)], dict(j=0.6)),
    ([(X1 + 60, Y1 + 200), (X1 + 360, Y1 + 200)], dict(j=0.6)),
    (rrect(X1 + 490, Y1 + 110, X2 - 60, Y1 + 320, 12), dict(close=True, j=0.8)),
    (rrect(X1 + 60, Y1 + 390, X1 + 360, Y1 + 520, 12), dict(close=True, j=0.8)),
    ([(X1 + 420, Y1 + 420), (X2 - 60, Y1 + 420)], dict(j=0.6)),
    ([(X1 + 420, Y1 + 480), (X2 - 140, Y1 + 480)], dict(j=0.6)),
]
MS_A, _ = boil_paths("pencil", messy, seeds=(51, 52))
CL_A, _ = boil_paths("pencil", clean, seeds=(53, 54))
ISSUES = [  # circle centre, rx, ry, label, label pos, tick pos
    ((X1 + 240, Y1 + 175), 220, 70, "outdated plugins", (X1 + 60, Y1 + 255), (X1 + 470, Y1 + 160)),
    ((X1 + 680, Y1 + 220), 210, 140, "slow pages", (X1 + 560, Y1 + 365), (X2 - 50, Y1 + 120)),
    ((X1 + 210, Y1 + 455), 190, 100, "no backups", (X1 + 60, Y1 + 605), (X1 + 400, Y1 + 615)),
]
iss_svg = "".join(f'<path class="ink" id="a3-c{i}" d="{hand(ellipse(c[0], c[1], rx, ry, tilt=0.05 * (i - 1)), 600 + i, j=1.6)}" />' for i, (c, rx, ry, _, _, _) in enumerate(ISSUES))
tick_svg = "".join(f'<path class="ink" id="a3-k{i}" d="{hand(check(tp[0], tp[1], 1.2), 700 + i, j=0.8, step=6)}" />' for i, (_, _, _, _, _, tp) in enumerate(ISSUES))
lab_html = "\n".join(f'      <div class="hw a3l" id="a3-l{i}" style="left:{lp[0]}px;top:{lp[1]}px;font-size:56px;color:#7a5c0e">{lab}</div>' for i, (_, _, _, lab, lp, _) in enumerate(ISSUES))
strike_svg = "".join(f'<path class="pencil" id="a3-x{i}" d="{hand([(lp[0] - 6, lp[1] + 34), (lp[0] + 14 * len(lab) + 70, lp[1] + 28)], 800 + i, j=1.2, step=8)}" />' for i, (_, _, _, lab, lp, _) in enumerate(ISSUES))
mag = hand(ellipse(0, 0, 70, 70, turns=1.02, n=40), 901, j=0.8, step=6)
mag_h = hand([(50, 50), (120, 120)], 902, j=0.6, step=6)
a3_css = '''    #a3-mag {
      position: absolute;
      left: 0;
      top: 0;
      width: 260px;
      height: 260px;
      overflow: visible;
    }
'''
a3_body = "\n".join([
    ttl("a3-t1", "Yes, in most cases."), ttl("a3-t2", "We start with a", "short review."),
    f'      <div class="dev" id="a3-ms" style="position:absolute;inset:0">{svgwrap(MS_A)}</div>',
    f'      <div class="dev" id="a3-cl" style="position:absolute;inset:0">{svgwrap(CL_A)}</div>',
    f'      {svgwrap(iss_svg + tick_svg + strike_svg)}',
    lab_html,
    f'      <svg id="a3-mag" viewBox="-130 -130 260 260"><circle cx="0" cy="0" r="68" fill="rgba(255,253,246,0.35)" /><path class="pencil" d="{mag}" /><path class="pencil" d="{mag_h}" style="stroke-width:9" /></svg>',
])
a3_js = '''    // host starts 17.95 s
    gsap.set(["#a3-t1", "#a3-t2"], { opacity: 0, filter: "blur(8px)" });
    D("#a3-ms path", false);
    gsap.set("#a3-cl", { opacity: 0 });
    D("#a3-c0,#a3-c1,#a3-c2,#a3-k0,#a3-k1,#a3-k2,#a3-x0,#a3-x1,#a3-x2", false);
    gsap.set(".a3l", { clipPath: "inset(0% 100% 0% 0%)" });
    gsap.set("#a3-mag", { x: -200, y: 930, opacity: 0 });
    tl.to("#a3-t1", { opacity: 1, filter: "blur(0px)", duration: 0.3, ease: "power2.out" }, 0.2);
    draw("#a3-ms path", 0.15, 0.4, 0.06);
    // what we find (on the beat)
    [0, 1, 2].forEach((i) => {
      const t = [1.25, 1.72, 2.19][i];
      draw("#a3-c" + i, t, 0.3);
      tl.to("#a3-l" + i, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.4, ease: "steps(10)" }, t + 0.12);
    });
    // the review: a magnifier passes, and each problem is fixed behind it
    tl.to("#a3-t1", { opacity: 0, filter: "blur(8px)", duration: 0.22, ease: "power2.in" }, 3.4);
    tl.to("#a3-t2", { opacity: 1, filter: "blur(0px)", duration: 0.3, ease: "power2.out" }, 3.6);
    tl.to("#a3-mag", { opacity: 1, duration: 0.15 }, 3.6);
    tl.to("#a3-mag", { x: 1100, y: 780, duration: 1.8, ease: "power1.inOut" }, 3.6);
    tl.to("#a3-ms", { opacity: 0, duration: 0.6, ease: "power1.inOut" }, 4.0);
    tl.to("#a3-cl", { opacity: 1, duration: 0.6, ease: "power1.inOut" }, 4.0);
    [0, 1, 2].forEach((i) => {
      const t = [4.0, 4.47, 4.94][i];
      draw("#a3-x" + i, t, 0.22);
      draw("#a3-k" + i, t + 0.1, 0.25);
      tl.to("#a3-c" + i, { opacity: 0.25, duration: 0.3 }, t);
    });
    tl.to("#a3-wrap", { opacity: 0, y: 40, duration: 0.25, ease: "power2.in" }, 7.6);'''
write("a3", comp("a3", 7.9, a3_css + a2_css, a3_body, a3_js))

# ======================================================================
# Close — back to question 1, then the answer (26.4 – 33.9)
# ======================================================================
handset = hand(curve((0, 0), (-30, 70), (40, 150)) + curve((40, 150), (90, 170), (110, 130)), 950, j=1.0, step=6)
waves = hand(curve((70, 20), (100, 40), (90, 70)), 951, j=0.7, step=5) + " " + hand(curve((90, -5), (140, 30), (120, 90)), 952, j=0.7, step=5)
LIST = ["your goals", "your audience", "your timeline"]
cl_ticks = "".join(f'<path class="ink" id="cl-k{i}" d="{hand(check(200, 790 + i * 120, 1.25), 960 + i, j=0.9, step=6)}" />' for i in range(3))
cl_body = "\n".join([
    f'      <div class="hw" id="cl-so" style="left:130px;top:600px;font-size:80px;color:#7a5c0e">So…</div>',
    card("clc", "What do we do before writing any code?"),
    ttl("cl-t1", "We listen first."), ttl("cl-t2", "A clarity-first", "discovery conversation."),
    "\n".join(f'      <div class="hw cll" id="cl-l{i}" style="left:290px;top:{748 + i * 120}px;font-size:92px">{w}</div>' for i, w in enumerate(LIST)),
    f'      {svgwrap(cl_ticks + f"<g transform=\"translate(470 1130)\"><path class=\"pencil\" id=\"cl-h\" d=\"{handset}\" style=\"stroke-width:9\" /><path class=\"pencil thin\" id=\"cl-w\" d=\"{waves}\" /></g>")}',
])
cl_js = SLAM_JS + '''    // host starts 29.22 s (on the beat): the first question comes back
    gsap.set(["#cl-t1", "#cl-t2"], { opacity: 0, filter: "blur(8px)" });
    gsap.set("#clc", { opacity: 0 });
    gsap.set("#cl-so", { clipPath: "inset(0% 100% 0% 0%)", rotation: -4 });
    gsap.set(".cll", { clipPath: "inset(0% 100% 0% 0%)" });
    D("#cl-k0,#cl-k1,#cl-k2,#cl-h,#cl-w", false);
    slam("#clc", 0.0, -2);
    tl.to("#cl-so", { clipPath: "inset(0% 0% 0% 0%)", duration: 0.35, ease: "steps(4)" }, 0.3);
    // the answer (32.03 s)
    toss("#clc", 2.75, -1);
    tl.to("#cl-so", { opacity: 0, duration: 0.2 }, 2.75);
    tl.to("#cl-t1", { opacity: 1, filter: "blur(0px)", duration: 0.3, ease: "power2.out" }, 2.85);
    draw("#cl-h", 2.95, 0.4);
    draw("#cl-w", 3.3, 0.3);
    // beat-grid: 32.50, 32.97, 33.44
    [0, 1, 2].forEach((i) => {
      const t = [3.28, 3.75, 4.22][i];
      tl.to("#cl-l" + i, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.42, ease: "steps(12)" }, t);
      draw("#cl-k" + i, t + 0.3, 0.22);
    });
    tl.to("#cl-t1", { opacity: 0, filter: "blur(8px)", duration: 0.22, ease: "power2.in" }, 4.95);
    tl.to("#cl-t2", { opacity: 1, filter: "blur(0px)", duration: 0.3, ease: "power2.out" }, 5.15);
    tl.to("#cl-wrap", { opacity: 0, y: 30, duration: 0.25, ease: "power2.in" }, 7.25);'''
write("close", comp("close", 7.5, CARD_CSS, cl_body, cl_js))

# ======================================================================
# logo stamp (33.74 – 37.5) and brand row (0 – 33.7): same pieces as the napkin film
# ======================================================================
_parts = _src.split("# ======================================================================")
_s5 = [x for x in _parts if x.lstrip().startswith("s5_css")][0]
_s5 = _s5.replace('comp("s5", 4.85', 'comp("logo", 3.76').replace('write("s5"', 'write("logo"').replace("}, 4.8);", "}, 3.7);")
exec(_s5)
_bc = [x for x in _parts if x.lstrip().startswith("bc = ")][0]
_bc = _bc.replace('data-duration="27.7"', 'data-duration="36.52"').replace("27.3);", "36.12);").replace('print("ok")', "")
exec(_bc)
print("ok")
