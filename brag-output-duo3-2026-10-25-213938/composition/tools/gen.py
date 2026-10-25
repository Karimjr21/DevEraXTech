"""Realistic Duo film: a photographed café table, a titanium foldable that opens like a book in 3D,
and a fictional café website rendered live in the browser (broken first, then built right)."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "compositions")

# inner screen 836 x 616, split by the hinge at x = 418
SW, SH, HX = 836, 616, 418

BASE = '''    #root {
      position: absolute;
      inset: 0;
      font-family: "Inter", sans-serif;
    }
    /* TikTok-native caption: black type on white line boxes */
    .cap {
      position: absolute;
      left: 70px;
      right: 70px;
      top: 230px;
      text-align: center;
      font-weight: 800;
      font-size: 62px;
      line-height: 1.42;
      letter-spacing: -0.02em;
    }
    .cap span {
      background: #ffffff;
      color: #111111;
      padding: 4px 18px 8px;
      border-radius: 14px;
      -webkit-box-decoration-break: clone;
      box-decoration-break: clone;
    }
    .cap.dark span {
      background: #111111;
      color: #ffffff;
    }
    .cap b {
      color: #c8102e;
      font-weight: 800;
    }
    .cap.dark b {
      color: #f6c42b;
    }
    .lab {
      position: absolute;
      padding: 10px 22px 12px;
      border-radius: 999px;
      background: rgba(17, 17, 17, 0.82);
      color: #fff;
      font-weight: 700;
      font-size: 34px;
      white-space: nowrap;
    }
    /* ---------- the phone ---------- */
    .ph {
      position: absolute;
      left: 110px;
      top: 720px;
      width: 860px;
      height: 640px;
      perspective: 2400px;
    }
    .shadow {
      position: absolute;
      left: 40px;
      top: 590px;
      width: 780px;
      height: 90px;
      border-radius: 50%;
      background: radial-gradient(ellipse at 50% 50%, rgba(0, 0, 0, 0.55) 0%, rgba(0, 0, 0, 0) 70%);
      transform-origin: 75% 50%;
    }
    .body {
      position: absolute;
      inset: 0;
      transform-style: preserve-3d;
    }
    .half {
      position: absolute;
      top: 0;
      width: 430px;
      height: 640px;
      padding: 5px;
      /* brushed titanium edge */
      background: linear-gradient(135deg, #e9eaee 0%, #8e9198 22%, #d7d9de 48%, #6c7077 72%, #c9cbd0 100%);
      box-shadow: 0 30px 60px rgba(0, 0, 0, 0.45);
    }
    .half .glass {
      position: absolute;
      inset: 5px;
      background: #050505;
      overflow: hidden;
    }
    .half .win {
      position: absolute;
      top: 7px;
      width: 418px;
      height: 616px;
      overflow: hidden;
      background: #fff;
    }
    .inR {
      left: 430px;
      border-radius: 0 52px 52px 0;
    }
    .inR .glass {
      border-radius: 0 47px 47px 0;
    }
    .inR .win {
      left: 0;
      border-radius: 0 40px 40px 0;
    }
    .cover {
      position: absolute;
      left: 430px;
      top: 0;
      width: 430px;
      height: 640px;
      transform-style: preserve-3d;
      transform-origin: 0% 50%;
    }
    .face {
      position: absolute;
      inset: 0;
      -webkit-backface-visibility: hidden;
      backface-visibility: hidden;
    }
    .face.front {
      border-radius: 52px;
    }
    .face.front .glass {
      border-radius: 47px;
    }
    .face.front .win {
      left: 6px;
      border-radius: 40px;
    }
    .face.back {
      transform: rotateY(180deg);
      border-radius: 52px 0 0 52px;
    }
    .face.back .glass {
      border-radius: 47px 0 0 47px;
    }
    .face.back .win {
      left: 7px;
      border-radius: 40px 0 0 40px;
    }
    .crease {
      position: absolute;
      left: 424px;
      top: 0;
      width: 12px;
      height: 640px;
      background: linear-gradient(90deg, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.22) 45%, rgba(255, 255, 255, 0.28) 55%, rgba(0, 0, 0, 0));
    }
    .glare {
      position: absolute;
      left: -300px;
      top: -100px;
      width: 220px;
      height: 900px;
      background: linear-gradient(90deg, rgba(255, 255, 255, 0), rgba(255, 255, 255, 0.16), rgba(255, 255, 255, 0));
    }
    .site {
      position: absolute;
      top: 0;
      width: 836px;
      height: 616px;
      background: #fffdf8;
      color: #2a211c;
      overflow: hidden;
    }
    .mob {
      position: absolute;
      left: 0;
      top: 0;
      width: 418px;
      height: 616px;
      background: #fffdf8;
      color: #2a211c;
      overflow: hidden;
    }
    .sb {
      position: absolute;
      left: 0;
      right: 0;
      top: 0;
      height: 40px;
      font-weight: 700;
      font-size: 17px;
      color: #111;
      z-index: 3;
    }
    .sb i {
      position: absolute;
      top: 15px;
      height: 11px;
      border-radius: 3px;
      background: #111;
    }
    .touch {
      position: absolute;
      width: 70px;
      height: 70px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.55);
      border: 3px solid rgba(80, 80, 80, 0.55);
      box-shadow: 0 0 18px rgba(0, 0, 0, 0.25);
      z-index: 9;
    }
'''

def sbar(w, time_left, right):
    """status bar: time on the left, signal + battery on the right"""
    return (f'<div class="sb"><span style="position:absolute;left:{time_left}px;top:11px">10:24</span>'
            f'<i style="left:{right - 64}px;width:22px;height:9px;top:16px"></i>'
            f'<i style="left:{right - 36}px;width:30px;background:none;border:2px solid #111;top:14px;height:13px"></i>'
            f'<i style="left:{right - 33}px;width:20px;top:17px;height:7px"></i></div>')

def phone(pid, outer, inner, extra=""):
    """inner is the 836-wide site; it is shown through two 418-wide windows either side of the hinge"""
    return f'''      <div class="ph" id="{pid}">
        <div class="shadow" id="{pid}-sh"></div>
        <div class="body" id="{pid}-body">
          <div class="half inR"><div class="glass"><div class="win" data-layout-ignore><div class="site" style="left:-{HX}px">{inner}</div></div><div class="glare {pid}-gl"></div></div></div>
          <div class="crease" id="{pid}-crease"></div>
          <div class="cover" id="{pid}-cover">
            <div class="half face front"><div class="glass"><div class="win" data-layout-ignore><div class="mob">{outer}</div></div><div class="glare {pid}-gl"></div></div></div>
            <div class="half face back"><div class="glass"><div class="win" data-layout-ignore><div class="site" style="left:0">{inner}</div></div><div class="glare {pid}-gl"></div></div></div>
          </div>
        </div>{extra}
      </div>'''

PHONE_JS = '''    // closed: only the cover (outer screen) shows, centred on the table
    function closedState(p) {
      gsap.set(p + "-cover", { rotationY: 0 });
      gsap.set(p + "-body", { x: -215 });
      gsap.set(p + "-crease", { opacity: 0 });
      gsap.set(p + "-sh", { scaleX: 0.5, x: -215 });
    }
    function openState(p) {
      gsap.set(p + "-cover", { rotationY: -180 });
      gsap.set(p + "-body", { x: 0 });
      gsap.set(p + "-sh", { scaleX: 1, x: 0 });
    }
    // opens like a book: the cover swings over the hinge and becomes the left half of the inner screen
    function unfold(p, t) {
      tl.to(p + "-cover", { rotationY: -180, duration: 0.7, ease: "power2.inOut" }, t);
      tl.to(p + "-body", { x: 0, duration: 0.7, ease: "power2.inOut" }, t);
      tl.to(p + "-sh", { scaleX: 1, x: 0, duration: 0.7, ease: "power2.inOut" }, t);
      tl.to(p + "-crease", { opacity: 1, duration: 0.2 }, t + 0.5);
    }
    function fold(p, t) {
      tl.to(p + "-crease", { opacity: 0, duration: 0.1 }, t);
      tl.to(p + "-cover", { rotationY: 0, duration: 0.6, ease: "power2.inOut" }, t);
      tl.to(p + "-body", { x: -215, duration: 0.6, ease: "power2.inOut" }, t);
      tl.to(p + "-sh", { scaleX: 0.5, x: -215, duration: 0.6, ease: "power2.inOut" }, t);
    }
    function glare(p, t) {
      tl.fromTo("." + p.slice(1) + "-gl", { x: 0 }, { x: 1100, duration: 1.2, ease: "power1.inOut", immediateRender: false }, t);
    }
    function cap(sel, t) {
      tl.fromTo(sel, { opacity: 0, scale: 0.9, y: 20 }, { opacity: 1, scale: 1, y: 0, duration: 0.22, ease: "back.out(2)", immediateRender: false }, t);
    }
    function uncap(sel, t) {
      tl.to(sel, { opacity: 0, duration: 0.14, ease: "power1.in" }, t);
    }
    function touch(sel, t, x, y) {
      tl.fromTo(sel, { opacity: 0, scale: 1.4, x: x, y: y }, { opacity: 1, scale: 1, x: x, y: y, duration: 0.15, ease: "power2.out", immediateRender: false }, t);
    }
'''

def comp(cid, start, dur, css, body, js):
    return f'''<template>
  <style>
{BASE}{css}  </style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920">
    <div id="{cid}-wrap" class="clip" data-start="0" data-duration="{dur}" data-layout-allow-overflow data-layout-allow-overlap>
{body}
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    // times are written in film time; the host starts this scene at {start} s
    const G = (t) => +(t - {start}).toFixed(3);
{PHONE_JS}{js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
'''

def write(cid, s):
    open(os.path.join(OUT, cid + ".html"), "w").write(s)

# ---------------- the fictional café, three ways ----------------
SERIF = "font-family:Georgia,'DejaVu Serif',serif"

MOBILE = sbar(418, 34, 392) + f'''
          <div style="position:absolute;left:0;right:0;top:40px;height:62px;border-bottom:1px solid #eee3d6"></div>
          <div style="position:absolute;left:26px;top:56px;{SERIF};font-weight:700;font-size:28px">Corner Café</div>
          <div style="position:absolute;right:26px;top:66px;width:32px;height:3px;background:#2a211c;box-shadow:0 9px 0 #2a211c,0 18px 0 #2a211c"></div>
          <div style="position:absolute;left:18px;right:18px;top:118px;height:200px;border-radius:20px;background:url('assets/photos/latte.jpg') center / cover"></div>
          <div style="position:absolute;left:26px;right:18px;top:336px;{SERIF};font-weight:700;font-size:38px;line-height:1.05">Fresh coffee.<br>Brunch all day.</div>
          <div style="position:absolute;left:26px;top:434px;width:330px;font-size:18px;line-height:1.4;color:#6b5d52">Open 8–4 every day. Walk in or book a table.</div>
          <div style="position:absolute;left:26px;right:26px;top:504px;height:62px;border-radius:31px;background:#2a211c;color:#fff;font-weight:700;font-size:22px;line-height:62px;text-align:center">Book a table</div>'''

BROKEN = sbar(836, 34, 810) + f'''
          <div style="position:absolute;left:0;top:40px;width:836px;height:60px;background:#2a211c"></div>
          <div class="bk-nav" style="position:absolute;left:24px;top:56px;width:1300px;white-space:nowrap;color:#f4e9dc;font-size:22px;font-weight:600"><span style="{SERIF};font-size:26px;font-weight:700">Corner Café</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Home &nbsp; Menu &nbsp; About us &nbsp; Events &nbsp; Gallery &nbsp; Gift cards &nbsp; Contact</div>
          <div style="position:absolute;left:0;top:100px;width:836px;height:250px;background:url('assets/photos/latte.jpg') 0 0 / 100% 100% no-repeat"></div>
          <div class="bk-h" style="position:absolute;left:40px;top:366px;width:1400px;white-space:nowrap;{SERIF};font-weight:700;font-size:84px;letter-spacing:-0.01em">Fresh coffee. Brunch all day.</div>
          <div style="position:absolute;left:338px;top:478px;width:160px;height:56px;border-radius:6px;background:#2a211c;color:#fff;font-weight:700;font-size:20px;line-height:56px;text-align:center">Book a table</div>
          <div style="position:absolute;left:40px;top:556px;width:1100px;font-size:11px;line-height:1.5;color:#6b5d52;white-space:nowrap">Espresso 2.80 · Flat white 3.60 · Latte 3.90 · Cappuccino 3.70 · Iced coffee 4.10 · Pancakes 7.50 · Avocado toast 8.20 · Granola 6.40</div>
          <div style="position:absolute;left:784px;top:478px;width:180px;height:56px;border-radius:6px;background:#c8102e;color:#fff;font-weight:700;font-size:20px;line-height:56px;text-align:center">Call us</div>'''

MENU_TINY = sbar(836, 34, 810) + f'''
          <div style="position:absolute;left:0;top:40px;width:836px;height:60px;background:#2a211c"></div>
          <div style="position:absolute;left:24px;top:56px;{SERIF};font-size:26px;font-weight:700;color:#f4e9dc">Corner Café</div>
          <div style="position:absolute;left:40px;top:124px;{SERIF};font-weight:700;font-size:30px">Our menu</div>
          <div class="mt-txt" style="position:absolute;left:40px;top:174px;width:756px;font-size:11px;line-height:1.55;color:#4a3d34">
            <b>COFFEE</b> — Espresso 2.80 · Double espresso 3.20 · Americano 3.00 · Flat white 3.60 · Latte 3.90 · Cappuccino 3.70 · Mocha 4.20 · Iced coffee 4.10 · Cold brew 4.30<br>
            <b>TEA</b> — Breakfast tea 2.60 · Green tea 2.60 · Mint tea 2.60 · Chai latte 3.80<br>
            <b>BRUNCH</b> — Pancakes with berries 7.50 · Avocado toast 8.20 · Eggs on sourdough 7.90 · Granola bowl 6.40 · Halloumi wrap 8.60 · Shakshuka 9.20<br>
            <b>CAKES</b> — Banana bread 3.20 · Carrot cake 3.80 · Brownie 3.10 · Cinnamon roll 3.40<br>
            All prices include tax. Ask our team about allergens. Oat, soy and almond milk available on request at no extra charge.
          </div>
          <div style="position:absolute;left:40px;top:330px;width:360px;height:250px;border-radius:14px;background:url('assets/photos/espresso.jpg') center / cover"></div>
          <div style="position:absolute;left:436px;top:330px;width:360px;height:250px;border-radius:14px;background:url('assets/photos/latte.jpg') center / cover"></div>'''

MENU_BIG = sbar(836, 34, 810) + f'''
          <div style="position:absolute;left:0;top:40px;right:0;height:62px;border-bottom:1px solid #eee3d6"></div>
          <div style="position:absolute;left:30px;top:56px;{SERIF};font-size:26px;font-weight:700">Corner Café</div>
          <div style="position:absolute;left:30px;top:122px;{SERIF};font-weight:700;font-size:40px">Coffee</div>
          <div style="position:absolute;left:30px;top:186px;width:350px;font-size:25px;line-height:1.75;color:#2a211c">Espresso <span style="float:right">2.80</span><br>Flat white <span style="float:right">3.60</span><br>Latte <span style="float:right">3.90</span><br>Cappuccino <span style="float:right">3.70</span><br>Iced coffee <span style="float:right">4.10</span></div>
          <div style="position:absolute;left:448px;top:122px;{SERIF};font-weight:700;font-size:40px">Brunch</div>
          <div style="position:absolute;left:448px;top:186px;width:350px;font-size:25px;line-height:1.75;color:#2a211c">Pancakes <span style="float:right">7.50</span><br>Avocado toast <span style="float:right">8.20</span><br>Eggs on sourdough <span style="float:right">7.90</span><br>Granola bowl <span style="float:right">6.40</span><br>Shakshuka <span style="float:right">9.20</span></div>
          <div style="position:absolute;left:30px;width:350px;top:500px;height:68px;border-radius:34px;background:#2a211c;color:#fff;font-weight:700;font-size:24px;line-height:68px;text-align:center">Book a table</div>
          <div style="position:absolute;left:448px;width:350px;top:500px;height:68px;border-radius:34px;border:3px solid #2a211c;color:#2a211c;font-weight:700;font-size:24px;line-height:62px;text-align:center">Order ahead</div>'''

GOOD = sbar(836, 34, 810) + f'''
          <div style="position:absolute;left:0;top:40px;right:0;height:62px;border-bottom:1px solid #eee3d6"></div>
          <div style="position:absolute;left:30px;top:56px;{SERIF};font-size:28px;font-weight:700">Corner Café</div>
          <div style="position:absolute;left:448px;top:62px;font-size:20px;font-weight:600;color:#6b5d52;white-space:nowrap">Menu &nbsp;&nbsp; Visit &nbsp;&nbsp; Gift cards</div>
          <div style="position:absolute;left:30px;top:130px;width:360px;{SERIF};font-weight:700;font-size:52px;line-height:1.04">Fresh coffee.<br>Brunch all day.</div>
          <div style="position:absolute;left:30px;top:262px;width:350px;font-size:21px;line-height:1.45;color:#6b5d52">Open 8–4 every day. Walk in, or book a table in two taps.</div>
          <div class="good-btn" style="position:absolute;left:30px;width:360px;top:420px;height:66px;border-radius:33px;background:#2a211c;color:#fff;font-weight:700;font-size:24px;line-height:66px;text-align:center">Book a table</div>
          <div class="good-call" style="position:absolute;left:30px;width:360px;top:502px;height:66px;border-radius:33px;border:3px solid #2a211c;color:#2a211c;font-weight:700;font-size:24px;line-height:60px;text-align:center">Call us</div>
          <div style="position:absolute;left:448px;top:118px;width:360px;height:280px;border-radius:22px;background:url('assets/photos/latte.jpg') center / cover"></div>
          <div style="position:absolute;left:448px;top:414px;width:172px;height:154px;border-radius:18px;background:url('assets/photos/espresso.jpg') center / cover"></div>
          <div style="position:absolute;left:636px;top:414px;width:172px;height:154px;border-radius:18px;background:#efe4d6;{SERIF};font-weight:700;font-size:26px;line-height:1.15;padding:22px 18px">See the<br>menu →</div>'''

# ======================================================================
# HOOK (0 – 7.45)
# ======================================================================
hk_body = "\n".join([
    '      <div class="cap" id="hk-c1"><span>Your customer just paid</span><br><span><b>$1,999</b> for this phone.</span></div>',
    '      <div class="cap" id="hk-c2"><span>…and this is your website</span><br><span>on it. <b>Book a table?</b></span></div>',
    phone("#hk".lstrip("#"), MOBILE, BROKEN, extra='\n        <div class="touch" id="hk-t" style="left:0;top:0"></div>'),
    '      <div class="lab" id="hk-l" style="left:0;right:0;margin:0 auto;width:470px;text-align:center;top:1480px">wait for the fix at the end ↓</div>',
])
hk_js = '''    closedState("#hk");
    gsap.set(["#hk-c2", "#hk-t", "#hk-l"], { opacity: 0 });
    // frame 0: the phone is already lifting off the table
    tl.fromTo("#hk", { y: 30, rotation: -4 }, { y: 0, rotation: 0, duration: 0.6, ease: "power2.out" }, 0);
    glare("#hk", 0.03);
    unfold("#hk", 0.36);
    tl.fromTo(".bk-nav", { x: 0 }, { x: -5, duration: 0.05, ease: "steps(1)", repeat: 19, yoyo: true, immediateRender: false }, 1.34);
    tl.fromTo(".bk-h", { x: 0 }, { x: -70, duration: 0.6, ease: "steps(5)", immediateRender: false }, 1.34);
    uncap("#hk-c1", 2.5);
    cap("#hk-c2", 2.62);
    // a thumb tries the button: it sits on the hinge and does nothing
    touch("#hk-t", 3.59, 393, 495);
    tl.to("#hk-t", { scale: 0.8, duration: 0.08, yoyo: true, repeat: 3 }, 3.8);
    tl.to("#hk-t", { opacity: 0, duration: 0.2 }, 4.4);
    tl.fromTo("#hk-body", { x: 0 }, { x: 8, duration: 0.05, ease: "steps(1)", repeat: 5, yoyo: true, immediateRender: false }, 4.24);
    tl.fromTo("#hk-l", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.25, ease: "back.out(2)", immediateRender: false }, 5.2);
    tl.to(["#hk", "#hk-c2", "#hk-l"], { opacity: 0, duration: 0.22, ease: "power1.in" }, 7.2);'''
write("hook", comp("hook", 0, 7.45, "", hk_body, hk_js))

# ======================================================================
# ZOOM (7.42 – 14.5): can they read your menu without zooming?
# ======================================================================
zm_body = "\n".join([
    '      <div class="cap dark" id="zm-q"><span>Can they read your menu</span><br><span><b>without zooming?</b></span></div>',
    '      <div class="cap" id="zm-a1"><span>Nobody wants to</span><br><span>pinch and zoom.</span></div>',
    '      <div class="cap" id="zm-a2"><span>So we size text for</span><br><span><b>every screen.</b></span></div>',
    phone("zm", MOBILE, MENU_TINY, extra='\n        <div class="touch" id="zm-t1" style="left:0;top:0"></div><div class="touch" id="zm-t2" style="left:0;top:0"></div>'),
    phone("zb", MOBILE, MENU_BIG),
])
zm_js = '''    openState("#zm"); openState("#zb");
    gsap.set(["#zm-a1", "#zm-a2", "#zm-q", "#zm-t1", "#zm-t2", "#zb"], { opacity: 0 });
    
    cap("#zm-q", G(7.45));
    tl.fromTo("#zm", { opacity: 0, y: 120 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out", immediateRender: false }, G(7.5));
    glare("#zm", G(7.7));
    // two fingers pinch outward over the tiny text
    touch("#zm-t1", G(8.74), 300, 180); touch("#zm-t2", G(8.74), 360, 230);
    tl.to("#zm-t1", { x: 170, y: 90, duration: 0.9, ease: "power2.inOut" }, G(8.9));
    tl.to("#zm-t2", { x: 520, y: 330, duration: 0.9, ease: "power2.inOut" }, G(8.9));
    tl.fromTo(".zm-z", { scale: 1 }, { scale: 2.6, duration: 0.9, ease: "power2.inOut", immediateRender: false }, G(8.9));
    tl.to(["#zm-t1", "#zm-t2"], { opacity: 0, duration: 0.2 }, G(10.0));
    uncap("#zm-q", G(10.25));
    cap("#zm-a1", G(10.37));
    // the fix: the same menu, readable at a glance
    tl.to("#zm", { opacity: 0, duration: 0.2 }, G(11.9));
    tl.to("#zb", { opacity: 1, duration: 0.2 }, G(11.9));
    uncap("#zm-a1", G(11.9));
    cap("#zm-a2", G(11.97));
    glare("#zb", G(12.1));
    tl.to(["#zb", "#zm-a2"], { opacity: 0, duration: 0.2, ease: "power1.in" }, G(14.3));'''
# the pinch zooms the site inside both windows of the zoom phone
write("zoom", comp("zoom", 7.42, 7.1, "", zm_body.replace('<div class="site" style="left:-418px">' + MENU_TINY, '<div class="site zm-z" style="left:-418px;transform-origin:418px 220px">' + MENU_TINY).replace('<div class="site" style="left:0">' + MENU_TINY, '<div class="site zm-z" style="left:0;transform-origin:418px 220px">' + MENU_TINY), zm_js))

# ======================================================================
# CALL (14.5 – 21.8): where's your "Call us" button?
# ======================================================================
cl_body = "\n".join([
    '      <div class="cap dark" id="cl-q"><span>Where’s your</span><br><span><b>“Call us”</b> button?</span></div>',
    '      <div class="cap" id="cl-a1"><span>Off the edge.</span></div>',
    '      <div class="cap" id="cl-a2"><span>We keep what matters</span><br><span><b>in thumb’s reach.</b></span></div>',
    phone("cl", MOBILE, BROKEN, extra='\n        <div class="touch" id="cl-t" style="left:0;top:0"></div>'),
    phone("cg", MOBILE, GOOD, extra='\n        <div class="touch" id="cg-t" style="left:0;top:0"></div>'),
    '      <div class="lab" id="cl-arrow" style="left:700px;top:1380px">→ cut off</div>',
])
cl_js = '''    openState("#cl"); openState("#cg");
    gsap.set(["#cl-q", "#cl-a1", "#cl-a2", "#cl-t", "#cg", "#cg-t", "#cl-arrow"], { opacity: 0 });
    cap("#cl-q", G(14.56));
    tl.fromTo("#cl", { opacity: 0, y: 120 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out", immediateRender: false }, G(14.6));
    // a thumb hunts around the page
    touch("#cl-t", G(15.52), 200, 300);
    tl.to("#cl-t", { x: 560, y: 220, duration: 0.5, ease: "power2.inOut" }, G(15.7));
    tl.to("#cl-t", { x: 720, y: 520, duration: 0.5, ease: "power2.inOut" }, G(16.3));
    // drag: the page slides sideways (it is wider than the screen) and shows a sliver of red
    tl.to("#cl .site", { x: -70, duration: 0.5, ease: "power2.out" }, G(17.14));
    tl.to("#cl-t", { x: 640, duration: 0.5, ease: "power2.out" }, G(17.14));
    tl.to("#cl .site", { x: 0, duration: 0.4, ease: "back.out(2)" }, G(17.9));
    tl.to("#cl-t", { opacity: 0, duration: 0.2 }, G(18.3));
    pop2("#cl-arrow", G(17.45));
    uncap("#cl-q", G(18.0));
    cap("#cl-a1", G(18.12));
    // the fix: both buttons on the left half, right under the thumb
    tl.to(["#cl", "#cl-arrow"], { opacity: 0, duration: 0.2 }, G(19.4));
    tl.to("#cg", { opacity: 1, duration: 0.2 }, G(19.4));
    uncap("#cl-a1", G(19.4));
    cap("#cg-a", G(19.5));
    touch("#cg-t", G(19.9), 210, 520);
    tl.to("#cg-t", { scale: 0.8, duration: 0.1, yoyo: true, repeat: 1 }, G(20.05));
    tl.to(["#cg", "#cg-a", "#cg-t"], { opacity: 0, duration: 0.2, ease: "power1.in" }, G(21.6));'''
cl_js = cl_js.replace('cap("#cg-a"', 'cap("#cl-a2"').replace('["#cg", "#cg-a", "#cg-t"]', '["#cg", "#cl-a2", "#cg-t"]')
cl_js = '''    function pop2(sel, t) {
      tl.fromTo(sel, { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2.4)", immediateRender: false }, t);
    }
''' + cl_js
write("call", comp("call", 14.5, 7.3, "", cl_body, cl_js))

# ======================================================================
# RETURN (21.8 – 27.5): same café, built right
# ======================================================================
rt_body = "\n".join([
    '      <div class="cap dark" id="rt-c1"><span>Same café.</span><br><span>Same phone. <b>Built right:</b></span></div>',
    '      <div class="cap" id="rt-c2"><span>Built for every screen.</span><br><span>Even the <b>$1,999</b> one.</span></div>',
    phone("rt", MOBILE, GOOD),
    '      <div class="lab" id="rt-l1" style="left:190px;top:1450px">5.4″ ✓</div>',
    '      <div class="lab" id="rt-l2" style="left:430px;top:1450px">7.6″ ✓</div>',
    '      <div class="lab" id="rt-l3" style="left:670px;top:1450px">hinge ✓</div>',
])
rt_js = '''    closedState("#rt");
    gsap.set(["#rt-c1", "#rt-c2", "#rt-l1", "#rt-l2", "#rt-l3"], { opacity: 0 });
    cap("#rt-c1", G(21.83));
    tl.fromTo("#rt", { opacity: 0, y: 120 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out", immediateRender: false }, G(21.85));
    tl.fromTo("#rt-l1", { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2.4)", immediateRender: false }, G(22.3));
    unfold("#rt", G(22.95));
    glare("#rt", G(23.5));
    tl.fromTo("#rt-l2", { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2.4)", immediateRender: false }, G(23.59));
    tl.fromTo("#rt-l3", { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2.4)", immediateRender: false }, G(23.91));
    uncap("#rt-c1", G(24.75));
    cap("#rt-c2", G(24.88));
    tl.fromTo("#rt", { y: 0 }, { y: -10, duration: 0.65, ease: "sine.inOut", repeat: 3, yoyo: true, immediateRender: false }, G(25.0));
    tl.to(["#rt", "#rt-c2", "#rt-l1", "#rt-l2", "#rt-l3"], { opacity: 0, duration: 0.25, ease: "power1.in" }, G(27.2));'''
write("ret", comp("ret", 21.8, 5.7, "", rt_body, rt_js))

# ======================================================================
# LOGO (27.46 – 31.0): the table dims, the logo lands
# ======================================================================
lg_css = '''    #lg-dim {
      position: absolute;
      inset: 0;
      background: radial-gradient(ellipse 80% 60% at 50% 45%, rgba(10, 8, 6, 0.72), rgba(10, 8, 6, 0.92));
    }
    #lg-logo {
      position: absolute;
      left: 300px;
      top: 520px;
      width: 480px;
      height: 338px;
      background: url("assets/brand/deveraxtech-logo.png") center / contain no-repeat;
    }
    #lg-word {
      position: absolute;
      left: 0;
      right: 0;
      top: 890px;
      text-align: center;
      font-weight: 900;
      font-size: 100px;
      letter-spacing: -0.03em;
      color: #f6c42b;
    }
    #lg-tag {
      position: absolute;
      left: 0;
      right: 0;
      top: 1018px;
      text-align: center;
      font-weight: 700;
      font-size: 30px;
      letter-spacing: 0.3em;
      text-indent: 0.3em;
      color: #e8dcc6;
    }
    #lg-ask {
      top: 1110px;
    }
    #lg-url {
      left: 0;
      right: 0;
      margin: 0 auto;
      width: 380px;
      text-align: center;
      top: 1290px;
      background: #f6c42b;
      color: #111;
    }
'''
lg_body = '''      <div id="lg-dim"></div>
      <div id="lg-logo" role="img" aria-label="DevEraXTech logo"></div>
      <div id="lg-word">DevEraXTech</div>
      <div id="lg-tag">ENGINEERED EXCELLENCE</div>
      <div class="cap" id="lg-ask"><span>Is your website <b>Duo-ready?</b></span></div>
      <div class="lab" id="lg-url">deveraxtech.com</div>'''
lg_js = '''    gsap.set(["#lg-word", "#lg-tag", "#lg-ask", "#lg-url"], { opacity: 0, y: 20 });
    tl.fromTo("#lg-dim", { opacity: 0 }, { opacity: 1, duration: 0.35, ease: "power2.out" }, 0.0);
    tl.fromTo("#lg-logo", { opacity: 0, scale: 1.25, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.45, ease: "power3.out" }, 0.05);
    tl.to("#lg-word", { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0.5);
    tl.to("#lg-tag", { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0.65);
    tl.to("#lg-ask", { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }, 1.0);
    tl.to("#lg-url", { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }, 1.3);
    tl.to("#lg-url", { scale: 1.05, duration: 0.32, ease: "sine.inOut", repeat: 5, yoyo: true }, 1.7);'''
write("logo", comp("logo", 27.46, 3.54, lg_css, lg_body, lg_js))

# brand mark, top-left like a creator watermark
bc = '''<template>
  <style>
    #root {
      position: absolute;
      inset: 0;
    }
    #bc {
      position: absolute;
      left: 56px;
      top: 104px;
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 8px 20px 8px 12px;
      border-radius: 999px;
      background: rgba(17, 17, 17, 0.55);
    }
    #bc i {
      width: 54px;
      height: 38px;
      background: url("assets/brand/deveraxtech-logo.png") center / contain no-repeat;
    }
    #bc span {
      font-family: "Inter", sans-serif;
      font-weight: 800;
      font-size: 28px;
      color: #fff;
    }
  </style>
  <div id="root" data-composition-id="brandcue" data-width="1080" data-height="1920">
    <div id="bc-wrap" class="clip" data-start="0" data-duration="27.4">
      <div id="bc"><i role="img" aria-label="DevEraXTech logo"></i><span>DevEraXTech</span></div>
    </div>
  </div>
  <script>
    const tl = gsap.timeline({ paused: true });
    tl.to("#bc", { opacity: 0, duration: 0.2 }, 27.2);
    window.__timelines["brandcue"] = tl;
  </script>
</template>
'''
write("brandcue", bc)

# ======================================================================
# root
# ======================================================================
SC = [("hook", 0, 7.45, 1), ("zoom", 7.42, 7.1, 2), ("call", 14.5, 7.3, 1), ("ret", 21.8, 5.7, 2), ("logo", 27.46, 3.54, 3)]
SFX = [("lift", 0.0, 0.6, 0.35, "card-slide-2.ogg"), ("open", 0.36, 0.6, 0.5, "card-shove-1.ogg"), ("click", 1.0, 0.2, 0.6, "impactWood_light_001.ogg"),
       ("gl", 1.34, 0.03, 0.4, "glitch_002.ogg"), ("cap2", 2.62, 0.05, 0.5, "select_008.ogg"),
       ("tap1", 3.8, 0.09, 0.6, "click3.ogg"), ("tap2", 3.96, 0.09, 0.6, "click3.ogg"), ("err", 4.24, 0.5, 0.45, "error_005.ogg"), ("lab", 5.2, 0.05, 0.5, "select_008.ogg"),
       ("q2", 7.45, 0.3, 0.6, "impactWood_medium_002.ogg"), ("in2", 7.5, 0.6, 0.3, "card-slide-2.ogg"), ("pinch", 8.9, 0.6, 0.3, "card-slide-2.ogg"),
       ("a1", 10.37, 0.2, 0.5, "impactWood_medium_001.ogg"), ("swap", 11.97, 0.19, 0.5, "drop_002.ogg"),
       ("q3", 14.56, 0.3, 0.6, "impactWood_medium_002.ogg"), ("in3", 14.6, 0.6, 0.3, "card-slide-2.ogg"), ("drag", 17.14, 0.6, 0.3, "card-slide-2.ogg"), ("cut", 17.45, 0.12, 0.5, "bong_001.ogg"),
       ("a2", 18.12, 0.2, 0.5, "impactWood_medium_001.ogg"), ("swap2", 19.4, 0.19, 0.5, "drop_002.ogg"), ("tap3", 20.05, 0.09, 0.6, "click3.ogg"),
       ("q4", 21.83, 0.3, 0.6, "impactWood_medium_002.ogg"), ("l1", 22.3, 0.05, 0.5, "select_008.ogg"), ("open2", 22.95, 0.6, 0.5, "card-shove-1.ogg"), ("click2", 23.59, 0.2, 0.6, "impactWood_light_001.ogg"),
       ("l3", 23.91, 0.05, 0.5, "select_008.ogg"), ("c2", 24.88, 0.2, 0.5, "impactWood_medium_001.ogg"),
       ("stamp", 27.46, 0.3, 0.7, "impactSoft_heavy_001.ogg"), ("sig", 27.52, 2.8, 0.6, "sig-full.wav")]
rows = [f'      <div id="{c}" data-composition-id="{c}" data-composition-src="compositions/{c}.html" data-start="{s}" data-duration="{d}" data-track-index="{z}" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: {z}"></div>' for c, s, d, z in SC]
rows.append('      <div id="brandcue" data-composition-id="brandcue" data-composition-src="compositions/brandcue.html" data-start="0" data-duration="27.4" data-track-index="4" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 5"></div>')
aud = ['      <audio id="music" class="clip" data-start="0" data-duration="31" data-track-index="10" data-volume="0.42" data-fade-out="1.2" src="assets/music/wallpaper-kevin-macleod.mp3"></audio>']
aud += [f'      <audio id="s-{n}" class="clip" data-start="{s}" data-duration="{d}" data-track-index="{11 + i}" data-volume="{v}" src="assets/sfx/{f}"></audio>' for i, (n, s, d, v, f) in enumerate(SFX)]
root = '''<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }
      html,
      body {
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: #1b130d;
      }
      #root {
        position: relative;
        width: 100%;
        height: 100%;
        overflow: hidden;
      }
      /* a real café table, shot from above, softly out of focus */
      #table {
        position: absolute;
        left: -100px;
        top: 0;
        width: 1280px;
        height: 1920px;
        background: url("assets/photos/table.jpg") center / cover;
      }
      /* warm window light and a lens vignette */
      #light {
        position: absolute;
        inset: 0;
        background:
          radial-gradient(ellipse 70% 50% at 30% 20%, rgba(255, 214, 160, 0.22), rgba(255, 214, 160, 0) 70%),
          radial-gradient(ellipse 90% 75% at 50% 50%, rgba(0, 0, 0, 0) 55%, rgba(0, 0, 0, 0.55) 100%);
      }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="31" data-width="1080" data-height="1920">
      <div id="table"></div>
      <div id="light"></div>
''' + "\n".join(rows) + '''

      <!-- Music: "Wallpaper" by Kevin MacLeod (incompetech.com), CC BY 4.0 -->
''' + "\n".join(aud) + '''
    </div>
    <script>
      const main = gsap.timeline({ paused: true });
      // handheld camera: a slow push-in with a gentle drift
      main.fromTo("#table", { scale: 1.0, x: 0, y: 0 }, { scale: 1.12, x: 30, y: -20, duration: 31, ease: "none" }, 0);
      window.__timelines["main"] = main;
    </script>
  </body>
</html>
'''
open(os.path.join(HERE, "..", "index.html"), "w").write(root)
print("ok")
