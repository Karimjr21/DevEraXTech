"""'Is your website ready for the iPhone Duo?' — bold yellow question film. Writes compositions/*.html."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "compositions")

Y, K, W = "#f6c42b", "#0b0b0c", "#fffaf0"

BASE = '''    #root {
      position: absolute;
      inset: 0;
      font-family: "Inter", sans-serif;
      color: #0b0b0c;
    }
    .big {
      position: absolute;
      left: 70px;
      right: 70px;
      top: 250px;
      font-weight: 900;
      font-size: 104px;
      line-height: 0.98;
      letter-spacing: -0.04em;
    }
    .big .hl {
      display: inline-block;
      margin-top: 14px;
      padding: 4px 22px 12px;
      background: #0b0b0c;
      color: #f6c42b;
      border-radius: 18px;
    }
    .q {
      position: absolute;
      left: 60px;
      width: 960px;
      top: 230px;
      padding: 44px 50px 50px;
      background: #0b0b0c;
      color: #fffaf0;
      border-radius: 34px;
      font-weight: 900;
      font-size: 80px;
      line-height: 1.02;
      letter-spacing: -0.035em;
      box-shadow: 0 22px 0 rgba(0, 0, 0, 0.18);
      transform-origin: 50% 50%;
    }
    .q b {
      color: #f6c42b;
      font-weight: 900;
    }
    .pill {
      position: absolute;
      padding: 14px 30px 16px;
      background: #0b0b0c;
      color: #f6c42b;
      border-radius: 999px;
      font-weight: 800;
      font-size: 44px;
      letter-spacing: -0.01em;
      white-space: nowrap;
    }
    /* foldable phone: a passport-shaped outer screen, a book-style inner screen */
    .dev {
      position: absolute;
      left: 130px;
      top: 720px;
      width: 820px;
      height: 600px;
    }
    .outer {
      position: absolute;
      left: 205px;
      top: 0;
      width: 410px;
      height: 600px;
      background: #111;
      border-radius: 50px;
      box-shadow: 0 30px 50px rgba(60, 40, 0, 0.35);
    }
    .outer .scr {
      position: absolute;
      inset: 16px;
      background: #fff;
      border-radius: 36px;
      overflow: hidden;
    }
    .open {
      position: absolute;
      inset: 0;
    }
    .half {
      position: absolute;
      top: 0;
      width: 410px;
      height: 600px;
      background: #111;
    }
    .half.L {
      left: 0;
      border-radius: 50px 0 0 50px;
      box-shadow: 0 30px 50px rgba(60, 40, 0, 0.35);
    }
    .half.R {
      left: 410px;
      border-radius: 0 50px 50px 0;
      transform-origin: 0% 50%;
      box-shadow: 0 30px 50px rgba(60, 40, 0, 0.35);
    }
    .site {
      position: absolute;
      left: 16px;
      top: 16px;
      width: 788px;
      height: 568px;
      background: #fff;
      border-radius: 36px;
      overflow: hidden;
    }
    .hinge {
      position: absolute;
      left: 404px;
      top: 0;
      width: 12px;
      height: 600px;
      background: linear-gradient(90deg, rgba(0, 0, 0, 0.0), rgba(0, 0, 0, 0.28) 45%, rgba(255, 255, 255, 0.25) 55%, rgba(0, 0, 0, 0.0));
    }
    .bar {
      position: absolute;
      height: 16px;
      border-radius: 8px;
      background: #d9d6cf;
    }
    .warn {
      position: absolute;
      width: 78px;
      height: 78px;
      border-radius: 50%;
      background: #f6c42b;
      border: 6px solid #0b0b0c;
      color: #0b0b0c;
      font-weight: 900;
      font-size: 50px;
      line-height: 64px;
      text-align: center;
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
    // times below are written in film time; the host starts this scene at {start} s
    const G = (t) => +(t - {start}).toFixed(3);  // scenes after 12 s also slide 1.19 s (two beats) later in the host
{js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
'''

def write(cid, s):
    open(os.path.join(OUT, cid + ".html"), "w").write(s)

def device(did, outer_html, site_html, extra=""):
    return f'''      <div class="dev" id="{did}">
        <div class="open" id="{did}-open">
          <div class="half L"></div>
          <div class="half R" id="{did}-R"></div>
          <div class="site" id="{did}-site" data-layout-ignore>{site_html}</div>
          <div class="hinge" id="{did}-hinge"></div>
        </div>
        <div class="outer" id="{did}-outer"><div class="scr" data-layout-ignore>{outer_html}</div></div>{extra}
      </div>'''

UNFOLD_JS = '''    // unfold: the outer phone gives way to the book-style inner screen
    function setClosed(d) {
      gsap.set(d + "-open", { opacity: 0 });
      gsap.set(d + "-R", { scaleX: 0 });
      gsap.set(d + "-site", { clipPath: "inset(0% 50% 0% 0%)" });
    }
    function unfold(d, t) {
      tl.to(d + "-outer", { opacity: 0, duration: 0.06 }, t);
      tl.to(d + "-open", { opacity: 1, duration: 0.06 }, t);
      tl.to(d + "-R", { scaleX: 1, duration: 0.36, ease: "back.out(1.6)" }, t);
      tl.to(d + "-site", { clipPath: "inset(0% 0% 0% 0%)", duration: 0.36, ease: "back.out(1.6)" }, t);
      tl.fromTo(d, { x: 205 }, { x: 0, duration: 0.36, ease: "back.out(1.6)", immediateRender: false }, t);
    }
    function slam(sel, t, rot) {
      tl.fromTo(sel, { opacity: 0, scale: 1.25, rotation: rot - 6 }, { opacity: 1, scale: 1, rotation: rot, duration: 0.22, ease: "power4.out", immediateRender: false }, t);
    }
    function toss(sel, t, dir) {
      tl.to(sel, { x: 1100 * dir, rotation: 18 * dir, duration: 0.4, ease: "power3.in" }, t);
    }
    function pop(sel, t) {
      tl.fromTo(sel, { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2.4)", immediateRender: false }, t);
    }
'''

# ---------------- website pieces ----------------
def broken_site():
    return '''
            <div style="position:absolute;left:0;top:0;width:788px;height:58px;background:#1d2b4a"></div>
            <div class="bk" id="bk-nav" style="position:absolute;left:24px;top:14px;width:900px;font-weight:700;font-size:26px;color:#fff;white-space:nowrap;letter-spacing:0.02em">LOGO &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Home &nbsp; About &nbsp; Services &nbsp; Portfolio &nbsp; Blog &nbsp; Contact &nbsp; Shop</div>
            <div class="bk" id="bk-img" style="position:absolute;left:0;top:58px;width:788px;height:220px;background:linear-gradient(180deg,#9fc3e8,#e8d7b4);overflow:hidden">
              <div style="position:absolute;left:150px;top:30px;width:500px;height:150px;border-radius:50%;background:#e8a54b"></div>
              <div style="position:absolute;left:0;top:150px;width:788px;height:90px;background:#6c8f5c"></div>
            </div>
            <div class="bk" id="bk-h" style="position:absolute;left:30px;top:296px;width:1100px;font-weight:900;font-size:76px;letter-spacing:-0.03em;white-space:nowrap;color:#1d2b4a">Welcome to our website</div>
            <div class="bk" id="bk-btn" style="position:absolute;left:304px;top:400px;width:200px;height:66px;border-radius:12px;background:#e0483e;color:#fff;font-weight:800;font-size:30px;line-height:66px;text-align:center">Book now</div>
            <div class="bar bk" style="left:30px;top:500px;width:900px"></div>
            <div class="bar bk" style="left:30px;top:530px;width:700px"></div>'''

def mobile_site():
    return '''
            <div style="position:absolute;left:0;top:0;right:0;height:64px;background:#fff;border-bottom:2px solid #eee"></div>
            <div style="position:absolute;left:24px;top:18px;font-weight:900;font-size:26px">YourBrand</div>
            <div style="position:absolute;right:24px;top:22px;width:34px;height:4px;background:#0b0b0c;box-shadow:0 9px 0 #0b0b0c,0 18px 0 #0b0b0c"></div>
            <div style="position:absolute;left:20px;top:82px;right:20px;height:170px;border-radius:22px;background:linear-gradient(135deg,#1d2b4a,#3d5a99)"></div>
            <div style="position:absolute;left:24px;top:272px;right:20px;font-weight:900;font-size:40px;line-height:1.02;letter-spacing:-0.03em">Your business, looking sharp.</div>
            <div class="bar" style="left:24px;top:378px;width:290px"></div>
            <div class="bar" style="left:24px;top:404px;width:220px"></div>
            <div style="position:absolute;left:24px;right:24px;top:446px;height:64px;border-radius:32px;background:#0b0b0c;color:#f6c42b;font-weight:800;font-size:26px;line-height:64px;text-align:center">Book now</div>'''

def wide_site():
    tiles = "".join(f'<div style="position:absolute;left:{426 + (i % 2) * 186}px;top:{90 + (i // 2) * 236}px;width:172px;height:222px;border-radius:20px;background:{c}"></div>' for i, c in enumerate(["linear-gradient(135deg,#1d2b4a,#3d5a99)", "#f6c42b", "#e9e4d8", "linear-gradient(135deg,#3d5a99,#9fc3e8)"]))
    return '''
            <div style="position:absolute;left:0;top:0;right:0;height:64px;background:#fff;border-bottom:2px solid #eee"></div>
            <div style="position:absolute;left:28px;top:18px;font-weight:900;font-size:26px">YourBrand</div>
            <div style="position:absolute;left:426px;top:22px;font-weight:600;font-size:22px;color:#555;white-space:nowrap">Home &nbsp; Services &nbsp; Contact</div>
            <div style="position:absolute;left:28px;top:96px;width:340px;font-weight:900;font-size:50px;line-height:1.0;letter-spacing:-0.035em">Your business, looking sharp.</div>
            <div class="bar" style="left:28px;top:280px;width:320px"></div>
            <div class="bar" style="left:28px;top:308px;width:270px"></div>
            <div class="bar" style="left:28px;top:336px;width:300px"></div>
            <div style="position:absolute;left:28px;width:250px;top:392px;height:68px;border-radius:34px;background:#0b0b0c;color:#f6c42b;font-weight:800;font-size:28px;line-height:68px;text-align:center">Book now</div>''' + tiles

# ======================================================================
# HOOK (0 – 7.35): the closed phone shakes from frame 0, snaps open, the site breaks
# ======================================================================
hook_css = '''    #hk-tag {
      left: 640px;
      top: 600px;
      font-size: 34px;
      padding: 10px 22px 12px;
    }
    #hk-stay {
      left: 0;
      right: 0;
      margin: 0 auto;
      width: 560px;
      top: 1400px;
      text-align: center;
    }
'''
hook_body = "\n".join([
    '      <div class="big" id="hk-t1">Is your website<br>ready for the<br><span class="hl">iPhone Duo?</span></div>',
    '      <div class="big" id="hk-t2">Does your site<br>survive<br><span class="hl">the unfold?</span></div>',
    '      <div class="pill" id="hk-tag">5.4″ → 7.6″</div>',
    device("hk", mobile_site(), broken_site(), extra='''
        <div class="warn" id="hk-w1" style="left:690px;top:300px">!</div>
        <div class="warn" id="hk-w2" style="left:370px;top:396px">!</div>
        <div class="warn" id="hk-w3" style="left:40px;top:40px">!</div>'''),
    '      <div class="pill" id="hk-stay">the fix is at the end ↓</div>',
])
hook_js = UNFOLD_JS + '''    setClosed("#hk");
    gsap.set("#hk-t2", { opacity: 0 });
    gsap.set(["#hk-w1", "#hk-w2", "#hk-w3", "#hk-stay"], { opacity: 0 });
    gsap.set("#hk-tag", { rotation: 6 });
    // frame 0: the phone is already buzzing (finite shake)
    tl.fromTo("#hk", { rotation: -2.5 }, { rotation: 2.5, duration: 0.05, ease: "none", repeat: 3, yoyo: true }, 0);
    tl.to("#hk", { rotation: 0, duration: 0.03 }, 0.2);
    unfold("#hk", 0.22);
    tl.fromTo("#hk-tag", { scale: 1 }, { scale: 1.18, duration: 0.12, ease: "power2.out", yoyo: true, repeat: 1 }, 0.22);
    // the layout falls apart on the bigger screen
    tl.fromTo("#bk-h", { x: 0 }, { x: -60, duration: 0.6, ease: "steps(4)" }, 0.81);
    tl.fromTo("#bk-img", { scaleY: 1 }, { scaleY: 1.12, transformOrigin: "50% 0%", duration: 0.3, ease: "steps(3)" }, 0.81);
    tl.fromTo("#bk-nav", { x: 0 }, { x: -6, duration: 0.06, ease: "steps(1)", repeat: 31, yoyo: true }, 0.81);
    pop("#hk-w1", 1.29); pop("#hk-w2", 2.0); pop("#hk-w3", 2.6);
    // the question sharpens on the strong cue
    tl.to("#hk-t1", { opacity: 0, x: -60, duration: 0.14, ease: "power2.in" }, 2.5);
    tl.fromTo("#hk-t2", { opacity: 0, x: 60 }, { opacity: 1, x: 0, duration: 0.2, ease: "power3.out", immediateRender: false }, 2.6);
    tl.fromTo("#hk-stay", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)", immediateRender: false }, 4.38);
    tl.fromTo("#hk-stay", { y: 0 }, { y: 12, duration: 0.3, ease: "sine.inOut", repeat: 5, yoyo: true, immediateRender: false }, 4.7);
    // fold shut and drop out
    tl.to("#hk", { y: 1300, rotation: 12, duration: 0.45, ease: "power3.in" }, 6.76);
    tl.to(["#hk-t2", "#hk-tag", "#hk-stay"], { opacity: 0, y: -40, duration: 0.25, ease: "power2.in" }, 6.9);'''
write("hook", comp("hook", 0, 7.35, hook_css, hook_body, hook_js))

# ======================================================================
# SPEED (7.3 – 14.45): would you wait 5 seconds?
# ======================================================================
sp_css = '''    #sp-ring {
      position: absolute;
      left: 129px;
      top: 150px;
      width: 120px;
      height: 120px;
      border-radius: 50%;
      border: 12px solid #e9e4d8;
      border-top-color: #0b0b0c;
    }
    .num {
      position: absolute;
      left: 0;
      right: 0;
      top: 300px;
      text-align: center;
      font-weight: 900;
      font-size: 150px;
      letter-spacing: -0.04em;
      color: #0b0b0c;
    }
    #sp-load {
      position: absolute;
      left: 0;
      right: 0;
      top: 470px;
      text-align: center;
      font-weight: 600;
      font-size: 26px;
      color: #8a857a;
    }
    #sp-prog {
      position: absolute;
      left: 40px;
      width: 298px;
      top: 72px;
      height: 10px;
      border-radius: 5px;
      background: #0b0b0c;
      transform-origin: 0% 50%;
    }
'''
nums = "".join(f'<div class="num" id="sp-n{i}">{i}</div>' for i in range(1, 6))
sp_outer = f'<div id="sp-prog"></div><div id="sp-ring"></div>{nums}<div id="sp-load">loading…</div>'
sp_body = "\n".join([
    '      <div class="q" id="sp-q">Would you wait <b>5 seconds</b> for a website to load?</div>',
    device("sp", sp_outer, ""),
    '      <div class="big" id="sp-a1" style="top:330px">Neither would<br><span class="hl">your customers.</span></div>',
    '      <div class="big" id="sp-a2" style="top:330px;font-size:96px">So we build<br>websites that<br><span class="hl">load fast.</span></div>',
    '      <div class="pill" id="sp-swipe" style="left:340px;top:1040px">swiped away.</div>',
    device("sp2", mobile_site(), ""),
])
sp_js = UNFOLD_JS + '''    gsap.set("#sp-open", { opacity: 0 });
    gsap.set(["#sp-n1", "#sp-n2", "#sp-n3", "#sp-n4", "#sp-n5", "#sp-a1", "#sp-a2", "#sp-swipe", "#sp-q"], { opacity: 0 });
    gsap.set("#sp-prog", { scaleX: 0.04 });
    slam("#sp-q", G(7.35), -2);
    tl.fromTo("#sp", { y: 900 }, { y: 0, duration: 0.45, ease: "expo.out", immediateRender: false }, G(7.45));
    tl.fromTo("#sp-ring", { rotation: 0 }, { rotation: 1440, duration: 3.6, ease: "none", immediateRender: false }, G(7.45));
    tl.to("#sp-prog", { scaleX: 0.22, duration: 3.2, ease: "power4.out" }, G(7.6));
    // one count per beat — painfully slow
    [7.94, 8.53, 9.13, 9.72, 10.32].forEach((t, i) => {
      if (i > 0) tl.to("#sp-n" + i, { opacity: 0, duration: 0.05 }, G(t));
      tl.fromTo("#sp-n" + (i + 1), { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.18, ease: "power3.out", immediateRender: false }, G(t));
    });
    // and the thumb gives up
    tl.to("#sp", { y: -1500, rotation: -8, duration: 0.42, ease: "power3.in" }, G(10.91));
    tl.fromTo("#sp-swipe", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)", immediateRender: false }, G(11.2));
    toss("#sp-q", G(11.2), 1);
    tl.fromTo("#sp-a1", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.25, ease: "power3.out", immediateRender: false }, G(11.51));
    tl.to(["#sp-a1", "#sp-swipe"], { opacity: 0, duration: 0.15 }, G(12.85));
    tl.fromTo("#sp-a2", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.25, ease: "power3.out", immediateRender: false }, G(12.99));
    // ...and the next one is simply there, ready
    gsap.set("#sp2-open", { opacity: 0 });
    tl.fromTo("#sp2", { opacity: 0, scale: 0.6, y: 120 }, { opacity: 1, scale: 1, y: 0, duration: 0.3, ease: "back.out(2.2)" }, G(12.99));
    tl.fromTo("#sp2", { rotation: 0 }, { rotation: 2, duration: 0.3, ease: "sine.inOut", repeat: 5, yoyo: true, immediateRender: false }, G(13.4));
    tl.to(["#sp-a2", "#sp2"], { opacity: 0, x: -80, duration: 0.2, ease: "power2.in" }, G(15.41));'''
write("speed", comp("speed", 7.3, 8.34, sp_css, sp_body, sp_js))

# ======================================================================
# RETRO (14.45 – 21.58): does your website still look like it's 2010?
# ======================================================================
re_css = '''    .old {
      position: absolute;
      inset: 0;
      background: repeating-linear-gradient(45deg, #dfe8ff 0 14px, #c9d6f7 14px 28px);
      font-family: "Times New Roman", "Liberation Serif", serif;
    }
    #re-marq {
      position: absolute;
      left: 0;
      top: 26px;
      white-space: nowrap;
      font-weight: 700;
      font-size: 40px;
      color: #8b008b;
    }
    .bev {
      position: absolute;
      left: 60px;
      width: 258px;
      height: 58px;
      background: linear-gradient(180deg, #f4f4f4, #bdbdbd);
      border: 3px outset #ddd;
      font-weight: 700;
      font-size: 26px;
      line-height: 52px;
      text-align: center;
      color: #00e;
      text-decoration: underline;
    }
    #re-ctr {
      position: absolute;
      left: 74px;
      top: 470px;
      padding: 6px 14px;
      background: #000;
      color: #39ff14;
      font-family: "DejaVu Sans Mono", monospace;
      font-size: 28px;
    }
    #re-uc {
      position: absolute;
      left: 0;
      right: 0;
      top: 96px;
      height: 44px;
      background: repeating-linear-gradient(-45deg, #f6c42b 0 22px, #0b0b0c 22px 44px);
    }
    #re-uct {
      position: absolute;
      left: 0;
      right: 0;
      top: 152px;
      text-align: center;
      font-weight: 700;
      font-size: 30px;
      white-space: nowrap;
      color: #c00000;
    }
    #re-new {
      position: absolute;
      inset: 0;
      background: #fff;
    }
    #re-scan {
      position: absolute;
      left: 0;
      right: 0;
      top: 0;
      height: 14px;
      background: #f6c42b;
      box-shadow: 0 0 30px #f6c42b;
    }
'''
old_html = '''<div class="old"><div id="re-marq">★ WELCOME TO OUR WEBSITE!!! ★ BEST PRICES!!! ★</div><div id="re-uc"></div><div id="re-uct">UNDER CONSTRUCTION</div>
              <div class="bev" style="top:220px">Click here!</div><div class="bev" style="top:296px">Sign our guestbook</div><div class="bev" style="top:372px">Best viewed in IE</div>
              <div id="re-ctr">Visitors: <span id="re-c">004213</span></div></div>'''
re_outer = old_html + '<div id="re-new">' + mobile_site() + '</div><div id="re-scan"></div>'
re_body = "\n".join([
    '      <div class="q" id="re-q">Does your website still look like it’s <b>2010?</b></div>',
    device("re", re_outer, ""),
    '      <div class="big" id="re-a1" style="top:330px">A redesign<br>that looks like<br><span class="hl">today.</span></div>',
])
re_js = UNFOLD_JS + '''    gsap.set("#re-open", { opacity: 0 });
    gsap.set(["#re-q", "#re-a1"], { opacity: 0 });
    gsap.set("#re-new", { clipPath: "inset(0% 0% 100% 0%)" });
    gsap.set("#re-scan", { opacity: 0 });
    slam("#re-q", G(14.48), 2);
    tl.fromTo("#re", { y: 900 }, { y: 0, duration: 0.45, ease: "expo.out", immediateRender: false }, G(14.6));
    tl.fromTo("#re-marq", { x: 380 }, { x: -900, duration: 5.0, ease: "none", immediateRender: false }, G(14.6));
    tl.fromTo("#re-uct", { opacity: 1 }, { opacity: 0.15, duration: 0.3, ease: "steps(1)", repeat: 7, yoyo: true, immediateRender: false }, G(14.9));
    // the makeover sweeps down the screen
    tl.to("#re-scan", { opacity: 1, duration: 0.05 }, G(16.85));
    tl.fromTo("#re-scan", { y: 0 }, { y: 560, duration: 0.6, ease: "power2.inOut", immediateRender: false }, G(16.85));
    tl.to("#re-new", { clipPath: "inset(0% 0% 0% 0%)", duration: 0.6, ease: "power2.inOut" }, G(16.85));
    tl.to("#re-scan", { opacity: 0, duration: 0.1 }, G(17.45));
    tl.fromTo("#re", { scale: 1 }, { scale: 1.05, duration: 0.15, ease: "power2.out", yoyo: true, repeat: 1, immediateRender: false }, G(17.45));
    toss("#re-q", G(18.9), -1);
    tl.fromTo("#re-a1", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.25, ease: "power3.out", immediateRender: false }, G(19.23));
    tl.to("#re", { y: 1300, duration: 0.4, ease: "power3.in" }, G(21.1));
    tl.to("#re-a1", { opacity: 0, x: -80, duration: 0.2, ease: "power2.in" }, G(21.3));'''
write("retro", comp("retro", 14.45, 7.13, re_css, re_body, re_js))

# ======================================================================
# FIX (21.58 – 26.4): back to the Duo, and this time it reflows
# ======================================================================
fx_body = "\n".join([
    '      <div class="big" id="fx-t1" style="font-size:96px">So… is <span style="white-space:nowrap">your website</span><br>ready for the<br><span class="hl">iPhone Duo?</span></div>',
    '      <div class="big" id="fx-t2">Ours are.<br><span style="font-size:64px;line-height:1.05;letter-spacing:-0.03em;display:block;margin-top:24px">Responsive on every screen, even the newest.</span></div>',
    device("fx", mobile_site(), wide_site()),
    '      <div class="pill" id="fx-p1" style="left:250px;top:1380px">5.4″ ✓</div>',
    '      <div class="pill" id="fx-p2" style="left:590px;top:1380px">7.6″ ✓</div>',
])
fx_js = UNFOLD_JS + '''    setClosed("#fx");
    gsap.set(["#fx-t2", "#fx-p1", "#fx-p2"], { opacity: 0 });
    tl.fromTo("#fx-t1", { opacity: 0, scale: 1.15 }, { opacity: 1, scale: 1, transformOrigin: "0% 50%", duration: 0.22, ease: "power4.out" }, G(21.61));
    tl.fromTo("#fx", { y: 900 }, { y: 0, duration: 0.4, ease: "expo.out" }, G(21.7));
    pop("#fx-p1", G(22.2));
    unfold("#fx", G(22.79));
    pop("#fx-p2", G(23.39));
    tl.to("#fx-t1", { opacity: 0, x: -60, duration: 0.14, ease: "power2.in" }, G(23.85));
    tl.fromTo("#fx-t2", { opacity: 0, x: 60 }, { opacity: 1, x: 0, duration: 0.22, ease: "power3.out", immediateRender: false }, G(23.99));
    tl.fromTo("#fx", { y: 0 }, { y: -14, duration: 0.6, ease: "sine.inOut", repeat: 2, yoyo: true, immediateRender: false }, G(24.4));
    tl.to(["#fx", "#fx-p1", "#fx-p2", "#fx-t2"], { opacity: 0, duration: 0.2 }, G(26.2));'''
write("fix", comp("fix", 21.58, 4.82, "", fx_body, fx_js))

# ======================================================================
# LOGO (26.35 – 30.0): black takes over, gold logo slams
# ======================================================================
lg_css = '''    #lg-bg {
      position: absolute;
      inset: 0;
      background: #0b0b0c;
    }
    #lg-logo {
      position: absolute;
      left: 290px;
      top: 470px;
      width: 500px;
      height: 352px;
      background: url("assets/brand/deveraxtech-logo.png") center / contain no-repeat;
    }
    #lg-word {
      position: absolute;
      left: 0;
      right: 0;
      top: 860px;
      text-align: center;
      font-weight: 900;
      font-size: 108px;
      letter-spacing: -0.03em;
      color: #f6c42b;
    }
    #lg-tag {
      position: absolute;
      left: 0;
      right: 0;
      top: 996px;
      text-align: center;
      font-weight: 700;
      font-size: 32px;
      letter-spacing: 0.3em;
      text-indent: 0.3em;
      color: #d8b24a;
    }
    #lg-ask {
      position: absolute;
      left: 0;
      right: 0;
      top: 1100px;
      text-align: center;
      font-weight: 900;
      font-size: 80px;
      letter-spacing: -0.035em;
      color: #fffaf0;
    }
    #lg-url {
      left: 0;
      right: 0;
      margin: 0 auto;
      width: 420px;
      top: 1230px;
      text-align: center;
      background: #f6c42b;
      color: #0b0b0c;
    }
'''
lg_body = '''      <div id="lg-bg"></div>
      <div id="lg-logo" role="img" aria-label="DevEraXTech logo"></div>
      <div id="lg-word">DevEraXTech</div>
      <div id="lg-tag">ENGINEERED EXCELLENCE</div>
      <div id="lg-ask">Is yours ready?</div>
      <div class="pill" id="lg-url">deveraxtech.com</div>'''
lg_js = '''    gsap.set("#lg-bg", { clipPath: "circle(0% at 50% 50%)" });
    gsap.set("#lg-logo", { opacity: 0, scale: 1.7, rotation: -10, transformOrigin: "50% 50%" });
    gsap.set(["#lg-word", "#lg-tag", "#lg-ask", "#lg-url"], { opacity: 0, y: 20 });
    tl.to("#lg-bg", { clipPath: "circle(80% at 50% 50%)", duration: 0.32, ease: "power3.in" }, 0.0);
    tl.to("#lg-logo", { opacity: 1, scale: 1, rotation: 0, duration: 0.18, ease: "power4.in" }, 0.22);
    tl.to("#lg-logo", { scale: 1.04, duration: 0.07, ease: "power2.out" }, 0.4);
    tl.to("#lg-logo", { scale: 1, duration: 0.14, ease: "power2.inOut" }, 0.47);
    tl.to("#lg-word", { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0.6);
    tl.to("#lg-tag", { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0.75);
    tl.to("#lg-ask", { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }, 1.2);
    tl.to("#lg-url", { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }, 1.45);
    tl.to("#lg-url", { scale: 1.06, duration: 0.3, ease: "sine.inOut", repeat: 3, yoyo: true }, 2.0);'''
write("logo", comp("logo", 26.35, 3.65, lg_css, lg_body, lg_js))

# ======================================================================
# brand pill (0 – 26.3)
# ======================================================================
bc = '''<template>
  <style>
    #root {
      position: absolute;
      inset: 0;
    }
    #bc {
      position: absolute;
      left: 0;
      right: 0;
      margin: 0 auto;
      top: 140px;
      width: 330px;
      height: 64px;
      border-radius: 999px;
      background: #0b0b0c;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 12px;
    }
    #bc i {
      width: 58px;
      height: 42px;
      background: url("assets/brand/deveraxtech-logo.png") center / contain no-repeat;
    }
    #bc span {
      font-family: "Inter", sans-serif;
      font-weight: 800;
      font-size: 30px;
      color: #f6c42b;
    }
  </style>
  <div id="root" data-composition-id="brandcue" data-width="1080" data-height="1920">
    <div id="bc-wrap" class="clip" data-start="0" data-duration="27.49">
      <div id="bc"><i role="img" aria-label="DevEraXTech logo"></i><span>DevEraXTech</span></div>
    </div>
  </div>
  <script>
    const tl = gsap.timeline({ paused: true });
    tl.to("#bc", { opacity: 0, duration: 0.2 }, 27.29);
    window.__timelines["brandcue"] = tl;
  </script>
</template>
'''
write("brandcue", bc)
print("ok")
