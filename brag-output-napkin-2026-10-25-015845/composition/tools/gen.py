"""Generates the "From napkin to launch" compositions (hand-drawn pencil paths are jittered here, deterministically)."""
import math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "compositions")

# ---------- hand-drawn geometry ----------
def densify(pts, step=12):
    out = []
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        n = max(1, int(math.hypot(x2 - x1, y2 - y1) / step))
        for i in range(n):
            t = i / n
            out.append((x1 + (x2 - x1) * t, y1 + (y2 - y1) * t))
    out.append(pts[-1])
    return out

def hand(pts, seed, j=1.6, step=12, close=False):
    rnd = random.Random(seed)
    if close:
        pts = pts + [pts[0]]
    d = densify(pts, step)
    # low-frequency wobble so it reads as a hand, not noise
    ph, ph2 = rnd.random() * 6.28, rnd.random() * 6.28
    s = []
    for k, (x, y) in enumerate(d):
        w = math.sin(k * 0.21 + ph) * j + math.sin(k * 0.07 + ph2) * j * 0.8
        s.append((x + w + rnd.uniform(-0.4, 0.4), y - w * 0.6 + rnd.uniform(-0.4, 0.4)))
    return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in s)

def rrect(x1, y1, x2, y2, r, n=6):
    pts = []
    for cx, cy, a0 in [(x2 - r, y1 + r, -90), (x2 - r, y2 - r, 0), (x1 + r, y2 - r, 90), (x1 + r, y1 + r, 180)]:
        for i in range(n + 1):
            a = math.radians(a0 + 90 * i / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts

def ellipse(cx, cy, rx, ry, turns=1.08, n=48, tilt=0.0):
    pts = []
    for i in range(int(n * turns) + 1):
        a = 2 * math.pi * i / n - 1.9
        x, y = rx * math.cos(a), ry * math.sin(a)
        pts.append((cx + x * math.cos(tilt) - y * math.sin(tilt), cy + x * math.sin(tilt) + y * math.cos(tilt)))
    return pts

def curve(p0, p1, p2, n=24):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in [i / n for i in range(n + 1)]]

def check(x, y, s=1.0):
    return [(x, y), (x + 16 * s, y + 18 * s), (x + 48 * s, y - 26 * s)]

def boil_paths(cls, items, seeds=(1, 2)):
    """two takes of every stroke: .vA draws, .vB is the second take used only for the boil"""
    a = "".join(f'<path class="{cls} vA" d="{hand(p, seeds[0] * 100 + i, **kw)}" />' for i, (p, kw) in enumerate(items))
    b = "".join(f'<path class="{cls} vB" d="{hand(p, seeds[1] * 100 + i, **kw)}" />' for i, (p, kw) in enumerate(items))
    return a, b

# ---------- shared CSS ----------
FONTS = '''    @font-face {
      font-family: "Caveat";
      font-style: normal;
      font-weight: 400 700;
      src: url("assets/fonts/Caveat-var.woff2") format("woff2");
    }
'''
BASE = '''    #root {
      position: absolute;
      inset: 0;
      font-family: "Inter", sans-serif;
      color: #2f2d29;
    }
    .ttl {
      position: absolute;
      left: 0;
      right: 0;
      top: 286px;
      text-align: center;
    }
    .ttl .n {
      display: block;
      font-family: "Playfair Display", serif;
      font-style: italic;
      font-size: 64px;
      line-height: 1;
      color: #7a5c0e;
    }
    .ttl .t {
      display: block;
      font-family: "Playfair Display", serif;
      font-style: italic;
      font-weight: 400;
      font-size: 100px;
      line-height: 1.06;
      letter-spacing: -0.01em;
      color: #2f2d29;
    }
    .pencil {
      fill: none;
      stroke: #3a3833;
      stroke-width: 4;
      stroke-linecap: round;
      stroke-linejoin: round;
    }
    .pencil.thin {
      stroke-width: 3;
      stroke: #55524b;
    }
    .ink {
      fill: none;
      stroke: #b8912a;
      stroke-width: 7;
      stroke-linecap: round;
      stroke-linejoin: round;
    }
    .hw {
      position: absolute;
      font-family: "Caveat", cursive;
      font-weight: 600;
      color: #2f2d29;
      white-space: nowrap;
      line-height: 1;
    }
    .note {
      position: absolute;
      width: 240px;
      height: 200px;
      background: #f2d67f;
      box-shadow: 0 14px 24px rgba(90, 70, 20, 0.22), inset 0 -8px 14px rgba(160, 120, 30, 0.12);
      transform-origin: 50% 0%;
    }
    .note .hw {
      left: 22px;
      top: 30px;
      font-size: 50px;
      line-height: 1.02;
      white-space: normal;
      width: 200px;
    }
    .note svg {
      position: absolute;
      right: 10px;
      bottom: 6px;
      overflow: visible;
    }
'''
DRAW_JS = '''    // every stroke gets its own length so it can be drawn on like a pencil line
    document.querySelectorAll("#root svg path").forEach((p) => {
      const L = p.getTotalLength();
      p.style.strokeDasharray = L + " " + (L + 4);
      p.dataset.len = L;
    });
    const D = (sel, on) => document.querySelectorAll(sel).forEach((p) => (p.style.strokeDashoffset = on ? 0 : +p.dataset.len));
    function draw(sel, t, dur, stagger) {
      document.querySelectorAll(sel).forEach((p, i) => {
        tl.fromTo(p, { strokeDashoffset: +p.dataset.len }, { strokeDashoffset: 0, duration: dur, ease: "power1.inOut" }, t + i * (stagger || 0));
      });
    }
    document.querySelectorAll(".note").forEach((n) => gsap.set(n, { rotation: +n.dataset.rot }));
    // stop-motion boil: swap between two takes of the same drawing at 8 fps (finite repeats)
    function boil(groupA, groupB, t, secs) {
      const n = Math.floor(secs / 0.125);
      tl.fromTo(groupB, { opacity: 0 }, { opacity: 1, duration: 0.125, ease: "steps(1)", repeat: n, yoyo: true }, t);
      tl.fromTo(groupA, { opacity: 1 }, { opacity: 0, duration: 0.125, ease: "steps(1)", repeat: n, yoyo: true }, t);
    }
'''

def comp(cid, dur, css, body, js):
    return f'''<template>
  <style>
{FONTS}{BASE}{css}  </style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920">
    <div id="{cid}-wrap" class="clip" data-start="0" data-duration="{dur}" data-layout-allow-overflow data-layout-allow-overlap>
{body}
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{DRAW_JS}{js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
'''

def write(cid, s):
    open(os.path.join(OUT, cid + ".html"), "w").write(s)

# ======================================================================
# Shared pieces: napkin, wireframe phone, sticky notes, app UI
# ======================================================================
NAP_CSS = '''    .napkin {
      position: absolute;
      width: 620px;
      height: 620px;
      background: #fffdf6;
      box-shadow: 0 30px 50px rgba(90, 70, 30, 0.22);
      transform-origin: 50% 50%;
    }
    .napkin .fold {
      position: absolute;
      background: rgba(120, 100, 60, 0.12);
    }
    .napkin svg {
      position: absolute;
      left: 0;
      top: 0;
      overflow: visible;
    }
'''
nap_doodle = [
    (rrect(390, 250, 540, 540, 22), dict(close=True, j=1.8)),
    (curve((300, 205), (370, 200), (392, 300)), dict(j=1.2)),
    (curve((376, 282), (388, 296), (392, 300)) + [(406, 280)], dict(j=0.8, step=6)),
    (ellipse(165, 432, 135, 62, tilt=-0.06), dict(j=1.4)),
    ([(420, 300), (510, 300)], dict(j=0.8)),
    ([(420, 340), (490, 340)], dict(j=0.8)),
    (rrect(420, 470, 510, 505, 14), dict(close=True, j=1.0)),
]
NAP_A, NAP_B = boil_paths("pencil", nap_doodle)

def napkin_html(nid, left, top, rot):
    return f'''      <div class="napkin" id="{nid}" style="left:{left}px;top:{top}px">
        <div class="fold" style="left:309px;top:0;width:2px;height:620px"></div>
        <div class="fold" style="left:0;top:309px;width:620px;height:2px"></div>
        <div class="hw" id="{nid}-l1" style="left:56px;top:60px;font-size:74px">booking app</div>
        <div class="hw" id="{nid}-l2" style="left:56px;top:150px;font-size:74px">for my clinic?</div>
        <div class="hw" id="{nid}-l3" style="left:70px;top:398px;font-size:62px;color:#7a5c0e">2 taps!</div>
        <svg width="620" height="620" viewBox="0 0 620 620"><g class="nA">{NAP_A}</g><g class="nB">{NAP_B}</g></svg>
      </div>'''

PX1, PY1, PX2, PY2 = 330, 640, 750, 1330
wire = [
    (rrect(PX1, PY1, PX2, PY2, 48, n=8), dict(close=True, j=1.6, step=14)),
    ([(PX1 + 150, PY1 + 30), (PX2 - 150, PY1 + 30)], dict(j=0.6)),
    ([(PX1 + 36, PY1 + 110), (PX1 + 260, PY1 + 110)], dict(j=0.8)),
    (rrect(PX1 + 30, PY1 + 160, PX1 + 140, PY1 + 240, 16), dict(close=True, j=1.0)),
    (rrect(PX1 + 155, PY1 + 160, PX1 + 265, PY1 + 240, 16), dict(close=True, j=1.0)),
    (rrect(PX1 + 280, PY1 + 160, PX2 - 30, PY1 + 240, 16), dict(close=True, j=1.0)),
    (rrect(PX1 + 30, PY1 + 280, PX1 + 140, PY1 + 340, 16), dict(close=True, j=1.0)),
    (rrect(PX1 + 155, PY1 + 280, PX1 + 265, PY1 + 340, 16), dict(close=True, j=1.0)),
    (rrect(PX1 + 280, PY1 + 280, PX2 - 30, PY1 + 340, 16), dict(close=True, j=1.0)),
    ([(PX1 + 36, PY1 + 400), (PX1 + 220, PY1 + 400)], dict(j=0.8)),
    ([(PX1 + 36, PY1 + 440), (PX1 + 300, PY1 + 440)], dict(j=0.8)),
    (rrect(PX1 + 30, PY2 - 150, PX2 - 30, PY2 - 60, 40), dict(close=True, j=1.2)),
]
WIRE_A, WIRE_B = boil_paths("pencil", wire, seeds=(3, 4))
# the phone outline alone (kept on top once the ink floods in)
OUTLINE_A = f'<path class="pencil" d="{hand(wire[0][0], 300, close=True, j=1.6, step=14)}" />'

NOTES = [  # id, left, top, rot, text
    ("n1", 60, 760, -6, "Book in<br />2 taps"),
    ("n2", 790, 830, 5, "Arabic +<br />English"),
    ("n3", 70, 1080, 3, "Remind<br />me"),
]
TICK = hand(check(0, 0, 1.0), 77, j=0.8, step=6)

def notes_html(prefix, ticks=False):
    out = ""
    for nid, l, t, r, txt in NOTES:
        tk = f'<svg width="60" height="50" viewBox="-4 -30 60 50"><path class="ink" id="{prefix}-{nid}-tk" d="{TICK}" /></svg>' if ticks else ""
        out += f'      <div class="note" id="{prefix}-{nid}" data-rot="{r}" style="left:{l}px;top:{t}px"><div class="hw">{txt}</div>{tk}</div>\n'
    return out

APP_CSS = '''    #app {
      position: absolute;
      left: 330px;
      top: 640px;
      width: 420px;
      height: 690px;
      border-radius: 48px;
      background: #0b0b0c;
      overflow: hidden;
      color: #f2efe6;
    }
    #app .top {
      position: absolute;
      left: 30px;
      right: 30px;
      top: 26px;
      display: flex;
      justify-content: space-between;
      font-size: 18px;
      font-weight: 600;
      color: #b9b4a6;
    }
    #app .lang {
      height: 34px;
      padding: 0 12px;
      border-radius: 17px;
      border: 1px solid rgba(212, 175, 55, 0.6);
      color: #f2d17b;
      font-size: 16px;
      line-height: 32px;
    }
    #app h3 {
      position: absolute;
      left: 30px;
      top: 86px;
      margin: 0;
      font-size: 38px;
      font-weight: 800;
      color: #f5f1e6;
    }
    #app .row {
      position: absolute;
      left: 30px;
      right: 30px;
      display: flex;
      gap: 15px;
    }
    #app .row span {
      flex: 1;
      height: 80px;
      border-radius: 16px;
      background: #19181c;
      border: 1px solid rgba(212, 175, 55, 0.2);
      text-align: center;
      font-size: 20px;
      font-weight: 600;
      padding-top: 14px;
      line-height: 1.25;
      color: #cfcabd;
    }
    #app .row.t span {
      height: 60px;
      padding-top: 0;
      line-height: 58px;
      font-size: 22px;
    }
    #app .row .on {
      background: #d4af37;
      color: #14110a;
      border-color: #d4af37;
    }
    #app .rem {
      position: absolute;
      left: 30px;
      right: 30px;
      top: 400px;
      height: 70px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 22px;
      font-weight: 600;
      border-top: 1px solid rgba(242, 239, 230, 0.08);
      border-bottom: 1px solid rgba(242, 239, 230, 0.08);
    }
    #app .sw {
      width: 64px;
      height: 36px;
      border-radius: 18px;
      background: #d4af37;
      position: relative;
    }
    #app .sw i {
      position: absolute;
      right: 4px;
      top: 4px;
      width: 28px;
      height: 28px;
      border-radius: 50%;
      background: #0b0b0c;
    }
    #app .btn {
      position: absolute;
      left: 30px;
      right: 30px;
      bottom: 60px;
      height: 90px;
      border-radius: 45px;
      background: linear-gradient(135deg, #d4af37 0%, #f5d573 50%, #d4af37 100%);
      color: #0a0a0a;
      font-size: 26px;
      font-weight: 800;
      text-align: center;
      line-height: 90px;
    }
    #app .done {
      position: absolute;
      left: 30px;
      right: 30px;
      bottom: 60px;
      height: 90px;
      border-radius: 45px;
      background: #13261f;
      border: 2px solid #8fbab7;
      color: #cfe7e4;
      font-size: 26px;
      font-weight: 800;
      text-align: center;
      line-height: 86px;
    }
'''
def app_html(done=False):
    return f'''      <div id="app">
        <div class="top"><span>9:41</span><span class="lang">AR · EN</span></div>
        <h3 class="ap">Book a visit</h3>
        <div class="row ap" style="top:160px"><span>Mon<br />12</span><span class="on">Tue<br />13</span><span>Wed<br />14</span></div>
        <div class="row t ap" style="top:280px"><span>09:00</span><span class="on">10:00</span><span>11:00</span></div>
        <div class="rem ap"><span>Remind me</span><div class="sw"><i></i></div></div>
        <div class="btn ap" id="app-btn">Book appointment</div>
        <div class="done" id="app-done" style="opacity:{1 if done else 0}">✓ Booked · Tue 13, 10:00</div>
      </div>'''

# ======================================================================
# S1 — the napkin (0 – 7.3)
# ======================================================================
und = hand([(150, 520), (420, 512), (700, 518), (940, 508)], 11, j=2.2, step=10)
s1_body = f'''      <div class="ttl" id="s1-t"><span class="t">Every product</span><span class="t">starts as a scribble.</span></div>
      <svg width="1080" height="600" viewBox="0 0 1080 600" style="position:absolute;left:0;top:0;overflow:visible"><path class="ink" id="s1-und" d="{und}" /></svg>
{napkin_html("nap", 230, 660, -4)}'''
s1_js = '''    // frame 0: the first line is already written, the doodle has begun
    D("#s1-und", false);
    D("#nap .nA path", false);
    gsap.set("#nap .nB", { opacity: 0 });
    gsap.set("#nap", { rotation: -4 });
    gsap.set(["#nap-l2", "#nap-l3"], { clipPath: "inset(0% 100% 0% 0%)" });
    gsap.set("#nap-l1", { clipPath: "inset(0% 18% 0% 0%)" });
    // inside the first second: the hand keeps writing and the ink underline sweeps
    tl.to("#nap-l1", { clipPath: "inset(0% 0% 0% 0%)", duration: 0.3, ease: "steps(3)" }, 0.0);
    tl.to("#nap-l2", { clipPath: "inset(0% 0% 0% 0%)", duration: 0.9, ease: "steps(14)" }, 0.3);
    draw("#s1-und", 0.45, 0.6);
    draw("#nap .nA path", 1.25, 0.42, 0.24);
    tl.to("#nap-l3", { clipPath: "inset(0% 0% 0% 0%)", duration: 0.5, ease: "steps(7)" }, 2.1);
    boil("#nap .nA", "#nap .nB", 3.2, 3.2);
    // the napkin gets pinned up on the board (matches the next scene's first frame)
    tl.to("#nap", { x: -321, y: -191, scale: 0.48, rotation: -7, duration: 0.7, ease: "power3.inOut" }, 6.55);
    tl.to("#s1-t", { opacity: 0, filter: "blur(8px)", duration: 0.3, ease: "power2.in" }, 6.6);
    tl.to("#s1-und", { opacity: 0, duration: 0.25 }, 6.6);'''
write("s1", comp("s1", 7.35, NAP_CSS, s1_body, s1_js))

# ======================================================================
# S2 — 01 Discovery call · 02 Plan (7.3 – 14.18)
# ======================================================================
CHK = [hand(check(0, 0, 1.15), 500 + i, j=0.9, step=6) for i in range(3)]
s2_css = NAP_CSS + '''    .pin {
      position: absolute;
      width: 30px;
      height: 30px;
      border-radius: 50%;
      background: radial-gradient(circle at 35% 35%, #f5d573, #a07a18);
      box-shadow: 0 6px 10px rgba(80, 60, 20, 0.35);
    }
    .li {
      position: absolute;
      left: 560px;
      font-size: 76px;
    }
'''
chk_svg = "".join(f'<path class="ink" id="s2-ck{i}" d="{CHK[i]}" transform="translate(470 {700 + i * 110})" />' for i in range(3))
s2_body = f'''      <div class="ttl" id="s2-tA"><span class="n">01</span><span class="t">Discovery call.</span></div>
      <div class="ttl" id="s2-tB"><span class="n">02</span><span class="t">Plan…</span></div>
{napkin_html("nap2", 230, 660, -7)}
      <div class="pin" id="s2-pin" style="left:204px;top:616px"></div>
      <svg width="1080" height="1920" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0;overflow:visible">{chk_svg}
        <g id="s2-wA">{WIRE_A}</g><g id="s2-wB">{WIRE_B}</g></svg>
      <div class="hw li" id="s2-i0" style="top:655px">goals</div>
      <div class="hw li" id="s2-i1" style="top:765px">audience</div>
      <div class="hw li" id="s2-i2" style="top:875px">timeline</div>
{notes_html("s2")}'''
s2_js = '''    // host starts 7.3 s; the napkin arrives pinned exactly where the last scene left it
    gsap.set("#nap2", { x: -321, y: -191, scale: 0.48, rotation: -7 });
    D("#nap2 .nA path", true);
    gsap.set("#nap2 .nB", { opacity: 0 });
    gsap.set(["#s2-tA", "#s2-tB"], { opacity: 0, filter: "blur(8px)" });
    gsap.set("#s2-pin", { opacity: 0, scale: 1.8, transformOrigin: "50% 50%" });
    D("#s2-ck0,#s2-ck1,#s2-ck2", false);
    D("#s2-wA path", false);
    gsap.set("#s2-wB", { opacity: 0 });
    gsap.set([".li"], { clipPath: "inset(0% 100% 0% 0%)" });
    gsap.set([".note"], { opacity: 0, y: -40, scale: 1.12 });
    tl.to("#s2-pin", { opacity: 1, scale: 1, duration: 0.25, ease: "power4.out" }, 0.05);
    tl.to("#s2-tA", { opacity: 1, filter: "blur(0px)", duration: 0.35, ease: "power2.out" }, 0.1);
    // beat-grid (0.43 s): goals ✓ audience ✓ timeline ✓ on 8.19, 9.03, 9.90
    [0, 1, 2].forEach((i) => {
      const t = [0.89, 1.73, 2.6][i];
      draw("#s2-ck" + i, t, 0.28);
      tl.to("#s2-i" + i, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.45, ease: "steps(9)" }, t + 0.15);
    });
    // 02 · plan (10.76 s): the brief turns into a ruled wireframe
    tl.to(["#s2-tA"], { opacity: 0, filter: "blur(8px)", duration: 0.25, ease: "power2.in" }, 3.3);
    tl.to(["#nap2", "#s2-pin"], { x: "-=420", rotation: -16, opacity: 0, duration: 0.5, ease: "power3.in" }, 3.3);
    tl.to([".li", "#s2-ck0", "#s2-ck1", "#s2-ck2"], { opacity: 0, x: 60, duration: 0.4, ease: "power3.in" }, 3.3);
    tl.to("#s2-tB", { opacity: 1, filter: "blur(0px)", duration: 0.35, ease: "power2.out" }, 3.5);
    draw("#s2-wA path", 3.5, 0.5, 0.11);
    // sticky notes slap on, one per beat (12.48, 12.89, 13.32)
    ["#s2-n1", "#s2-n2", "#s2-n3"].forEach((s, i) => {
      tl.to(s, { opacity: 1, y: 0, scale: 1, duration: 0.28, ease: "back.out(1.3)" }, [5.18, 5.59, 6.02][i]);
    });
    boil("#s2-wA", "#s2-wB", 5.1, 1.75);'''
write("s2", comp("s2", 6.95, s2_css, s2_body, s2_js))

# ======================================================================
# S3 — …and design (14.18 – 21.05)
# ======================================================================
s3_css = APP_CSS + '''    #s3-edge {
      position: absolute;
      left: 322px;
      top: 640px;
      width: 436px;
      height: 8px;
      border-radius: 4px;
      background: linear-gradient(90deg, rgba(184, 145, 42, 0), #b8912a 15%, #f2d17b 50%, #b8912a 85%, rgba(184, 145, 42, 0));
      box-shadow: 0 0 18px rgba(212, 175, 55, 0.7);
    }
'''
s3_body = f'''      <div class="ttl" id="s3-t"><span class="n">02</span><span class="t">…and design.</span></div>
      <svg width="1080" height="1920" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0;overflow:visible"><g id="s3-wA">{WIRE_A}</g></svg>
{app_html()}
      <div id="s3-edge"></div>
      <svg width="1080" height="1920" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0;overflow:visible">{OUTLINE_A}</svg>
{notes_html("s3", ticks=True)}      <div class="hw" id="s3-rdy" style="left:770px;top:1100px;font-size:60px;color:#7a5c0e;line-height:1.05">ready to<br />build →</div>
      <svg width="1080" height="1920" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0;overflow:visible"><path class="ink" id="s3-rdyu" d="{hand([(770, 1238), (900, 1232), (990, 1240)], 61, j=1.6, step=10)}" /></svg>'''
s3_js = '''    // host starts 14.18 s with the wireframe and notes exactly as the last scene ended
    gsap.set("#s3-t", { opacity: 0, filter: "blur(8px)" });
    gsap.set("#app", { clipPath: "inset(0% 0% 100% 0%)" });
    gsap.set("#s3-edge", { opacity: 0, y: 0 });
    gsap.set(".ap", { opacity: 0, y: 14 });
    D("#s3-n1-tk,#s3-n2-tk,#s3-n3-tk", false);
    tl.to("#s3-t", { opacity: 1, filter: "blur(0px)", duration: 0.35, ease: "power2.out" }, 0.1);
    // gold ink floods the pencil wireframe from the top down
    tl.to("#s3-edge", { opacity: 1, duration: 0.1 }, 0.4);
    tl.to("#app", { clipPath: "inset(0% 0% 0% 0%)", duration: 1.0, ease: "power2.inOut" }, 0.4);
    tl.to("#s3-edge", { y: 690, duration: 1.0, ease: "power2.inOut" }, 0.4);
    tl.to("#s3-edge", { opacity: 0, duration: 0.2 }, 1.4);
    // the design settles in, on the beat
    tl.to(".ap", { opacity: 1, y: 0, duration: 0.35, ease: "power3.out", stagger: 0.43 }, 1.15);
    // each note is answered by the design (16.34, 17.18, 18.03)
    [["#s3-n1-tk", 2.16], ["#s3-n2-tk", 3.0], ["#s3-n3-tk", 3.85]].forEach(([s, t]) => draw(s, t, 0.3));
    // a note to self in gold ink, written while the design holds (19.2 s)
    D("#s3-rdyu", false);
    gsap.set("#s3-rdy", { clipPath: "inset(0% 100% 0% 0%)" });
    tl.to("#s3-rdy", { clipPath: "inset(0% 0% 0% 0%)", duration: 1.0, ease: "steps(16)" }, 4.9);
    draw("#s3-rdyu", 5.95, 0.4);
    tl.to(["#s3-rdy", "#s3-rdyu"], { opacity: 0, duration: 0.25 }, 6.6);'''
write("s3", comp("s3", 6.95, s3_css, s3_body, s3_js))

# ======================================================================
# S4 — 03 Build, secure and launch (21.05 – 27.9)
# ======================================================================
plane_pts = [(0, 0), (190, 70), (0, 130), (40, 70)]
PLANE = hand(plane_pts, 901, close=True, j=1.0, step=8)
PLANE_FOLD = hand([(40, 70), (190, 70)], 902, j=0.8, step=8)
TRAIL = "M 540 1000 C 640 960 760 820 860 640 S 1040 330 1200 230"
s4_css = APP_CSS + '''    #seal {
      position: absolute;
      left: 640px;
      top: 590px;
      width: 190px;
      height: 190px;
      border-radius: 50%;
      background: radial-gradient(circle at 38% 34%, #f0cf6e 0%, #c9a133 45%, #8a6a14 100%);
      box-shadow: 0 10px 22px rgba(90, 60, 10, 0.35), inset 0 0 0 10px rgba(255, 241, 191, 0.25);
      text-align: center;
      color: #3b2b05;
      font-family: "Playfair Display", serif;
      font-style: italic;
      font-size: 34px;
      line-height: 1;
      padding-top: 74px;
    }
    #seal small {
      display: block;
      margin-top: 8px;
      font-family: "Inter", sans-serif;
      font-style: normal;
      font-weight: 800;
      font-size: 15px;
      letter-spacing: 0.24em;
    }
    #s4-stack {
      position: absolute;
      inset: 0;
    }
    #plane {
      position: absolute;
      left: 0;
      top: 0;
      width: 200px;
      height: 140px;
      overflow: visible;
    }
    #s4-cur {
      position: absolute;
      left: 0;
      top: 0;
      width: 70px;
      height: 70px;
      overflow: visible;
    }
'''
CUR = hand([(0, 0), (0, 52), (14, 38), (26, 62), (36, 57), (25, 34), (44, 34), (0, 0)], 950, j=0.6, step=6)
s4_body = f'''      <div class="ttl" id="s4-t"><span class="n">03</span><span class="t">Build, secure</span><span class="t">and launch.</span></div>
      <div id="s4-stack">
        <svg width="1080" height="1920" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0;overflow:visible"><g id="s4-wA">{WIRE_A}</g></svg>
{app_html()}
        <svg width="1080" height="1920" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0;overflow:visible">{OUTLINE_A}</svg>
{notes_html("s4", ticks=True)}        <div id="seal" data-layout-allow-occlusion>DX<small>SECURE</small></div>
      </div>
      <svg width="1080" height="1920" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0;overflow:visible">
        <path id="s4-trail" d="{TRAIL}" fill="none" stroke="#b8912a" stroke-width="5" stroke-linecap="round" stroke-dasharray="2 16" />
        <path id="s4-trailm" d="{TRAIL}" fill="none" stroke="none" />
      </svg>
      <svg id="plane" viewBox="0 0 200 140"><path d="{PLANE}" fill="#fffdf6" stroke="#3a3833" stroke-width="4" stroke-linejoin="round" /><path d="{PLANE_FOLD}" fill="none" stroke="#b8912a" stroke-width="4" stroke-linecap="round" /></svg>
      <svg id="s4-cur" viewBox="0 0 70 70"><path d="{CUR}" fill="#fffdf6" stroke="#2f2d29" stroke-width="3.5" stroke-linejoin="round" /></svg>'''
s4_js = '''    // host starts 21.05 s
    document.getElementById("s4-trail").style.strokeDasharray = "2 16";
    gsap.set("#s4-t", { opacity: 0, filter: "blur(8px)" });
    D("#s4-n1-tk,#s4-n2-tk,#s4-n3-tk", true);
    document.querySelectorAll("#s4-wA path, #s4-stack svg path").forEach((p) => (p.style.strokeDashoffset = 0));
    gsap.set("#seal", { opacity: 0, scale: 1.7, rotation: -24, transformOrigin: "50% 50%" });
    gsap.set("#plane", { opacity: 0, x: 440, y: 930, scale: 0.2, transformOrigin: "50% 50%" });
    gsap.set("#s4-cur", { x: 920, y: 1500, opacity: 0 });
    const TL = document.getElementById("s4-trail").getTotalLength();
    gsap.set("#s4-trail", { opacity: 0 });
    tl.to("#s4-t", { opacity: 1, filter: "blur(0px)", duration: 0.35, ease: "power2.out" }, 0.1);
    // build: one tap books it (21.9 s)
    tl.to("#s4-cur", { opacity: 1, duration: 0.15 }, 0.2);
    tl.to("#s4-cur", { x: 560, y: 1225, duration: 0.6, ease: "power3.out" }, 0.2);
    tl.to("#s4-cur", { scale: 0.86, duration: 0.07 }, 0.85);
    tl.to("#s4-cur", { scale: 1, duration: 0.12 }, 0.92);
    tl.to("#app-btn", { opacity: 0, duration: 0.15 }, 0.9);
    tl.to("#app-done", { opacity: 1, duration: 0.25, ease: "power2.out" }, 0.95);
    tl.to("#s4-cur", { opacity: 0, duration: 0.2 }, 1.3);
    // secure: the wax seal is stamped on (strong cue 23.19 s)
    tl.to("#seal", { opacity: 1, scale: 1, rotation: -10, duration: 0.2, ease: "power4.in" }, 1.95); // beat-locked: 23.19s
    tl.to("#seal", { scale: 1.04, duration: 0.08, ease: "power2.out" }, 2.15);
    tl.to("#seal", { scale: 1, duration: 0.15, ease: "power2.inOut" }, 2.23);
    // launch: the whole sheet folds into a paper plane (24.46 s) and flies
    tl.to("#s4-stack", { scale: 0.08, opacity: 0, rotation: 12, transformOrigin: "50% 52%", duration: 0.5, ease: "power3.in" }, 3.4);
    tl.to("#plane", { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.6)" }, 3.75);
    tl.to("#s4-trail", { opacity: 1, duration: 0.05 }, 4.2);
    tl.fromTo("#s4-trail", { strokeDashoffset: 0, clipPath: "inset(0% 100% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 1.3, ease: "power2.in" }, 4.2);
    tl.to("#plane", { motionPath: { path: "#s4-trailm", align: "#s4-trailm", alignOrigin: [0.5, 0.5], autoRotate: true }, duration: 1.3, ease: "power2.in" }, 4.2);
    tl.to(["#s4-t", "#s4-trail"], { opacity: 0, filter: "blur(8px)", duration: 0.3, ease: "power2.in" }, 6.5);'''
write("s4", comp("s4", 6.9, s4_css, s4_body, s4_js))

# ======================================================================
# S5 — the stamp (27.75 – 32.6)
# ======================================================================
s5_css = '''    #st-logo {
      position: absolute;
      left: 280px;
      top: 560px;
      width: 520px;
      height: 365px;
    }
    #st-logo img {
      width: 520px;
      height: 365px;
      object-fit: contain;
      display: block;
    }
    #st-ring {
      position: absolute;
      left: 290px;
      top: 490px;
      width: 500px;
      height: 500px;
      border-radius: 50%;
      border: 6px solid rgba(184, 145, 42, 0.5);
    }
    #st-word {
      position: absolute;
      left: 0;
      right: 0;
      top: 980px;
      text-align: center;
      font-weight: 800;
      font-size: 110px;
      letter-spacing: -0.02em;
      color: #7a5c0e;
    }
    #st-tag {
      position: absolute;
      left: 0;
      right: 0;
      top: 1122px;
      text-align: center;
      font-weight: 700;
      font-size: 34px;
      letter-spacing: 0.3em;
      text-indent: 0.3em;
      color: #7a5c0e;
    }
    #st-hw {
      position: absolute;
      left: 0;
      right: 0;
      top: 1188px;
      text-align: center;
      font-family: "Caveat", cursive;
      font-weight: 600;
      font-size: 70px;
      color: #2f2d29;
    }
    #st-url {
      position: absolute;
      left: 0;
      right: 0;
      top: 1282px;
      text-align: center;
      font-weight: 500;
      font-size: 30px;
      color: #5f5a50;
    }
'''
s5_body = '''      <div id="st-ring"></div>
      <div id="st-logo"><img src="assets/brand/deveraxtech-logo.png" alt="DevEraXTech logo" /></div>
      <div id="st-word">DevEraXTech</div>
      <div id="st-tag">ENGINEERED EXCELLENCE</div>
      <div id="st-hw"><span id="st-hwi" style="display:inline-block">from first call to launch.</span></div>
      <div id="st-url">deveraxtech.com</div>'''
s5_js = '''    // host starts 27.75 s; the logo is stamped down on the strong cue (27.9 s)
    gsap.set("#st-logo", { opacity: 0, scale: 1.6, rotation: -12, transformOrigin: "50% 50%", filter: "blur(6px)" });
    gsap.set("#st-ring", { opacity: 0, scale: 0.6, transformOrigin: "50% 50%" });
    gsap.set(["#st-word", "#st-tag", "#st-url"], { opacity: 0, y: 12 });
    gsap.set("#st-hwi", { clipPath: "inset(0% 100% 0% 0%)" });
    tl.to("#st-logo", { opacity: 1, scale: 1, rotation: -4, filter: "blur(0px)", duration: 0.16, ease: "power4.in" }, 0.0); // beat-locked: 27.9s
    tl.to("#st-logo", { scale: 1.03, duration: 0.07, ease: "power2.out" }, 0.16);
    tl.to("#st-logo", { scale: 1, duration: 0.14, ease: "power2.inOut" }, 0.23);
    tl.to("#st-ring", { opacity: 1, scale: 1, duration: 0.12, ease: "power3.out" }, 0.15);
    tl.to("#st-ring", { opacity: 0, scale: 1.25, duration: 0.6, ease: "power2.out" }, 0.27);
    tl.to("#st-word", { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, 0.45);
    tl.to("#st-tag", { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, 0.62);
    tl.to("#st-hwi", { clipPath: "inset(0% 0% 0% 0%)", duration: 0.9, ease: "steps(24)" }, 0.85);
    tl.to("#st-url", { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, 1.0);
    tl.to("#st-url", { opacity: 1, duration: 0.01 }, 4.8);'''
write("s5", comp("s5", 4.85, s5_css, s5_body, s5_js))

# ======================================================================
# brand row (0 – 27.7)
# ======================================================================
bc = '''<template>
  <style>
    #root {
      position: absolute;
      inset: 0;
    }
    #bc-row {
      position: absolute;
      left: 0;
      right: 0;
      top: 168px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 16px;
    }
    #bc-row img {
      width: 86px;
      height: 60px;
      object-fit: contain;
    }
    #bc-row span {
      font-family: "Inter", sans-serif;
      font-weight: 800;
      font-size: 36px;
      color: #7a5c0e;
    }
  </style>
  <div id="root" data-composition-id="brandcue" data-width="1080" data-height="1920">
    <div id="bc-wrap" class="clip" data-start="0" data-duration="27.7">
      <div id="bc-row"><img src="assets/brand/deveraxtech-logo.png" alt="DevEraXTech logo" /><span>DevEraXTech</span></div>
    </div>
  </div>
  <script>
    const tl = gsap.timeline({ paused: true });
    tl.to("#bc-row", { opacity: 0, duration: 0.3, ease: "power2.in" }, 27.3);
    window.__timelines["brandcue"] = tl;
  </script>
</template>
'''
write("brandcue", bc)
print("ok")
