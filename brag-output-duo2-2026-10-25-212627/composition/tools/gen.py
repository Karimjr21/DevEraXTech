"""'POV: your customer just unfolded their iPhone Duo' — night-sky film where the frame itself is the unfolded screen."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "compositions")

BASE = '''    #root {
      position: absolute;
      inset: 0;
      font-family: "Inter", sans-serif;
      color: #ffffff;
    }
    .hd {
      position: absolute;
      left: 60px;
      right: 60px;
      top: 250px;
      text-align: center;
      font-weight: 800;
      font-size: 86px;
      line-height: 1.04;
      letter-spacing: -0.035em;
      color: #ffffff;
    }
    .hd em {
      font-style: normal;
      color: #f6c42b;
    }
    .mono {
      font-family: "DejaVu Sans Mono", monospace;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }
    .pov {
      position: absolute;
      left: 0;
      right: 0;
      top: 180px;
      text-align: center;
      font-size: 40px;
      color: #f6c42b;
    }
    .tag {
      position: absolute;
      padding: 10px 18px 12px;
      background: #f6c42b;
      color: #0b0b0c;
      border-radius: 10px;
      font-size: 28px;
      white-space: nowrap;
      box-shadow: 0 10px 24px rgba(0, 0, 0, 0.35);
    }
    .chip {
      position: absolute;
      padding: 12px 26px 14px;
      border: 3px solid #f6c42b;
      color: #f6c42b;
      border-radius: 999px;
      font-size: 32px;
      white-space: nowrap;
    }
    /* the unfolded inner screen, full width: hinge down the middle */
    .band {
      position: absolute;
      left: 40px;
      top: 640px;
      width: 1000px;
      height: 760px;
      padding: 14px;
      background: #1a2140;
      border-radius: 48px;
      box-shadow: 0 0 0 2px rgba(120, 150, 255, 0.25), 0 40px 90px rgba(0, 0, 0, 0.6);
    }
    .scr {
      position: relative;
      width: 972px;
      height: 732px;
      background: #ffffff;
      border-radius: 36px;
      overflow: hidden;
      color: #0b0b0c;
    }
    .hinge {
      position: absolute;
      left: 494px;
      top: 0;
      width: 12px;
      height: 760px;
      background: linear-gradient(90deg, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.3) 45%, rgba(255, 255, 255, 0.35) 55%, rgba(0, 0, 0, 0));
    }
    /* closed: the outer screen */
    .closed {
      position: absolute;
      left: 340px;
      top: 720px;
      width: 400px;
      height: 600px;
      padding: 14px;
      background: #1a2140;
      border-radius: 50px;
      box-shadow: 0 0 0 2px rgba(120, 150, 255, 0.25), 0 40px 90px rgba(0, 0, 0, 0.6);
    }
    .closed .in {
      position: relative;
      width: 372px;
      height: 572px;
      background: #fff;
      border-radius: 38px;
      overflow: hidden;
      color: #0b0b0c;
    }
    .bar {
      position: absolute;
      height: 18px;
      border-radius: 9px;
      background: #dedbe6;
    }
    .btn {
      position: absolute;
      height: 76px;
      border-radius: 38px;
      background: #0b0b0c;
      color: #f6c42b;
      font-weight: 800;
      font-size: 32px;
      line-height: 76px;
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
    // times are written in film time; the host starts this scene at {start} s
    const G = (t) => +(t - {start}).toFixed(3);
    function rise(sel, t) {{
      tl.fromTo(sel, {{ opacity: 0, y: 50, filter: "blur(10px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.32, ease: "power3.out", immediateRender: false }}, t);
    }}
    function sink(sel, t) {{
      tl.to(sel, {{ opacity: 0, y: -40, filter: "blur(10px)", duration: 0.2, ease: "power2.in" }}, t);
    }}
    function pop(sel, t) {{
      tl.fromTo(sel, {{ opacity: 0, scale: 0.3 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2.6)", immediateRender: false }}, t);
    }}
    // closed outer screen -> the whole band unfolds out of it
    function unfold(closed, band, t) {{
      tl.to(closed, {{ opacity: 0, duration: 0.05 }}, t);
      tl.fromTo(band, {{ opacity: 0, clipPath: "inset(10.5% 30% 10.5% 30% round 48px)" }}, {{ opacity: 1, clipPath: "inset(0% 0% 0% 0% round 48px)", duration: 0.4, ease: "expo.out", immediateRender: false }}, t);
    }}
    function fold(closed, band, t) {{
      tl.to(band, {{ clipPath: "inset(10.5% 30% 10.5% 30% round 48px)", duration: 0.3, ease: "power3.in" }}, t);
      tl.to(band, {{ opacity: 0, duration: 0.05 }}, t + 0.3);
      tl.fromTo(closed, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.05, immediateRender: false }}, t + 0.28);
    }}
{js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
'''

def write(cid, s):
    open(os.path.join(OUT, cid + ".html"), "w").write(s)

def band(bid, inner):
    return f'      <div class="band" id="{bid}"><div class="scr" data-layout-ignore>{inner}</div><div class="hinge"></div></div>'

def closed(cid, inner):
    return f'      <div class="closed" id="{cid}"><div class="in" data-layout-ignore>{inner}</div></div>'

MOBILE = '''
          <div style="position:absolute;left:0;top:0;right:0;height:70px;border-bottom:2px solid #eee"></div>
          <div style="position:absolute;left:26px;top:20px;font-weight:900;font-size:28px">YourBrand</div>
          <div style="position:absolute;right:26px;top:24px;width:36px;height:4px;background:#0b0b0c;box-shadow:0 10px 0 #0b0b0c,0 20px 0 #0b0b0c"></div>
          <div style="position:absolute;left:22px;right:22px;top:92px;height:190px;border-radius:24px;background:linear-gradient(135deg,#1a2140,#4a63c9)"></div>
          <div style="position:absolute;left:26px;right:22px;top:302px;font-weight:900;font-size:42px;line-height:1.02;letter-spacing:-0.03em">Open daily.<br>Book online.</div>
          <div class="bar" style="left:26px;top:412px;width:300px"></div>
          <div class="bar" style="left:26px;top:442px;width:230px"></div>
          <div class="btn" style="left:26px;right:26px;top:478px">Book now</div>'''

BROKEN = '''
          <div style="position:absolute;left:0;top:0;width:972px;height:70px;background:#1a2140"></div>
          <div id="bk-nav" style="position:absolute;left:30px;top:20px;width:1200px;white-space:nowrap;color:#fff;font-weight:700;font-size:30px">LOGO &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Home &nbsp; About &nbsp; Services &nbsp; Gallery &nbsp; Blog &nbsp; Contact &nbsp; Shop</div>
          <div id="bk-img" style="position:absolute;left:0;top:70px;width:972px;height:300px;background:linear-gradient(180deg,#7fb0f0,#f0d9a8);overflow:hidden">
            <div style="position:absolute;left:120px;top:40px;width:730px;height:200px;border-radius:50%;background:#e9963c"></div>
            <div style="position:absolute;left:0;top:220px;width:972px;height:90px;background:#5f8a52"></div>
          </div>
          <div id="bk-h" style="position:absolute;left:60px;top:400px;width:1300px;white-space:nowrap;font-weight:900;font-size:96px;letter-spacing:-0.035em;color:#1a2140">Welcome to our website</div>
          <div class="btn" style="left:376px;width:220px;top:540px;border-radius:12px;background:#e0483e;color:#fff">Book now</div>
          <div class="bar" style="left:40px;top:650px;width:1100px"></div>
          <div class="bar" style="left:40px;top:684px;width:820px"></div>'''

# ======================================================================
# HOOK (0 – 7.4): POV — the outer screen unfolds into the whole frame, and the site breaks
# ======================================================================
hk_body = "\n".join([
    '      <div class="pov mono" id="hk-pov">POV:</div>',
    '      <div class="hd" id="hk-t1">your customer just unfolded their new <em>iPhone Duo</em>…</div>',
    '      <div class="hd" id="hk-t2">…and opened <em>your website.</em></div>',
    closed("hk-c", MOBILE),
    band("hk-b", BROKEN),
    '      <div class="tag mono" id="hk-g1" style="left:90px;top:760px">image stretched</div>',
    '      <div class="tag mono" id="hk-g2" style="left:560px;top:1010px">text in the fold</div>',
    '      <div class="tag mono" id="hk-g3" style="left:300px;top:1250px">button split in half</div>',
    '      <div class="chip mono" id="hk-stay" style="left:0;right:0;margin:0 auto;width:600px;text-align:center;top:1480px">we fix it at the end ↓</div>',
])
hk_js = '''    gsap.set(["#hk-t2", "#hk-g1", "#hk-g2", "#hk-g3", "#hk-stay", "#hk-b"], { opacity: 0 });
    // frame 0: the closed phone is already drifting toward us
    tl.fromTo("#hk-c", { scale: 1, rotation: -3 }, { scale: 1.06, rotation: 0, duration: 0.5, ease: "power2.in" }, 0);
    tl.fromTo("#hk-pov", { scale: 1 }, { scale: 1.25, duration: 0.12, ease: "power2.out", yoyo: true, repeat: 1 }, 0.05);
    unfold("#hk-c", "#hk-b", 0.53);
    // the layout falls apart on the bigger screen
    tl.fromTo("#bk-h", { x: 0 }, { x: -90, duration: 0.5, ease: "steps(4)", immediateRender: false }, 1.02);
    tl.fromTo("#bk-nav", { x: 0 }, { x: -8, duration: 0.06, ease: "steps(1)", repeat: 29, yoyo: true, immediateRender: false }, 1.02);
    tl.fromTo("#hk-b", { x: 0 }, { x: 10, duration: 0.05, ease: "steps(1)", repeat: 5, yoyo: true, immediateRender: false }, 2.01);
    sink("#hk-t1", 2.36);
    rise("#hk-t2", 2.5);
    pop("#hk-g1", 2.94); pop("#hk-g2", 3.38); pop("#hk-g3", 3.85);
    tl.fromTo("#hk-stay", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)", immediateRender: false }, 4.84);
    tl.fromTo("#hk-stay", { y: 0 }, { y: 12, duration: 0.25, ease: "sine.inOut", repeat: 5, yoyo: true, immediateRender: false }, 5.2);
    sink(["#hk-pov", "#hk-t2", "#hk-g1", "#hk-g2", "#hk-g3", "#hk-stay"], 7.0);
    tl.to("#hk-b", { opacity: 0, scale: 0.92, duration: 0.25, ease: "power2.in" }, 7.0);'''
write("hook", comp("hook", 0, 7.4, "", hk_body, hk_js))

# ======================================================================
# BUTTON (7.38 – 13.3): where did your "Book now" button go?
# ======================================================================
bt_css = '''    .half {
      position: absolute;
      top: 300px;
      width: 160px;
      height: 96px;
      background: #e0483e;
      color: #fff;
      font-weight: 800;
      font-size: 40px;
      line-height: 96px;
      overflow: hidden;
      white-space: nowrap;
    }
    #bt-tap {
      position: absolute;
      left: 446px;
      top: 300px;
      width: 96px;
      height: 96px;
      border-radius: 50%;
      border: 6px solid #4a63c9;
      background: rgba(74, 99, 201, 0.18);
    }
    #bt-good {
      left: 80px;
      width: 330px;
      top: 470px;
      height: 96px;
      line-height: 96px;
      border-radius: 48px;
      font-size: 40px;
      box-shadow: 0 0 0 0 rgba(246, 196, 43, 0.0);
    }
'''
bt_inner = '''
          <div style="position:absolute;left:0;top:0;right:0;height:70px;border-bottom:2px solid #eee"></div>
          <div style="position:absolute;left:30px;top:20px;font-weight:900;font-size:28px">YourBrand</div>
          <div style="position:absolute;left:80px;top:130px;width:360px;font-weight:900;font-size:56px;line-height:1.0;letter-spacing:-0.035em">Open daily.</div>
          <div class="half" id="bt-l" style="left:326px;border-radius:14px 0 0 14px;text-align:right;padding-right:4px">Book&nbsp;</div>
          <div class="half" id="bt-r" style="left:486px;border-radius:0 14px 14px 0;text-align:left;padding-left:4px">now</div>
          <div id="bt-tap"></div>
          <div class="btn" id="bt-good">Book now</div>
          <div class="bar" style="left:540px;top:150px;width:360px"></div>
          <div class="bar" style="left:540px;top:186px;width:300px"></div>'''
bt_body = "\n".join([
    '      <div class="hd" id="bt-q">Where did your <em>“Book now”</em> button go?</div>',
    band("bt-b", bt_inner),
    '      <div class="hd" id="bt-a1">Lost in <em>the fold.</em></div>',
    '      <div class="hd" id="bt-a2">We design <em>around the hinge.</em></div>',
    '      <div class="tag mono" id="bt-safe" style="left:150px;top:1250px">safe zone ✓</div>',
])
bt_js = '''    gsap.set(["#bt-a1", "#bt-a2", "#bt-safe", "#bt-good", "#bt-tap", "#bt-q"], { opacity: 0 });
    tl.fromTo("#bt-q", { opacity: 0, scale: 1.3 }, { opacity: 1, scale: 1, duration: 0.25, ease: "power4.out", immediateRender: false }, G(7.42));
    tl.fromTo("#bt-b", { opacity: 0, y: 200 }, { opacity: 1, y: 0, duration: 0.4, ease: "expo.out" }, G(7.5));
    // the button tears along the hinge
    tl.to("#bt-l", { x: -46, rotation: -6, duration: 0.5, ease: "back.out(2)" }, G(7.91));
    tl.to("#bt-r", { x: 46, rotation: 7, y: 20, duration: 0.5, ease: "back.out(2)" }, G(7.91));
    // a thumb taps the gap, and nothing happens
    tl.fromTo("#bt-tap", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.18, ease: "power2.out", immediateRender: false }, G(8.89));
    tl.to("#bt-tap", { opacity: 0, scale: 1.6, duration: 0.3, ease: "power2.out" }, G(9.07));
    sink("#bt-q", G(9.25));
    rise("#bt-a1", G(9.38));
    // the fix: one whole button, clear of the hinge
    tl.to(["#bt-l", "#bt-r"], { opacity: 0, y: 60, duration: 0.25, ease: "power2.in" }, G(10.7));
    tl.fromTo("#bt-good", { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.4)", immediateRender: false }, G(10.87));
    tl.fromTo("#bt-good", { boxShadow: "0 0 0 0 rgba(246,196,43,0.9)" }, { boxShadow: "0 0 0 26px rgba(246,196,43,0)", duration: 0.49, ease: "power2.out", repeat: 3, immediateRender: false }, G(10.9));
    sink("#bt-a1", G(10.72));
    rise("#bt-a2", G(10.87));
    pop("#bt-safe", G(11.35));
    tl.to(["#bt-b", "#bt-safe"], { opacity: 0, x: -160, duration: 0.25, ease: "power2.in" }, G(13.05));
    sink("#bt-a2", G(13.05));'''
write("button", comp("button", 7.38, 5.92, bt_css, bt_body, bt_js))

# ======================================================================
# BOTH SIDES (13.28 – 21.6): two screens, is your site using both?
# ======================================================================
bs_css = '''    #bs-empty {
      position: absolute;
      left: 530px;
      top: 100px;
      width: 400px;
      height: 590px;
      border: 5px dashed #c9c5d3;
      border-radius: 28px;
    }
    #bs-et {
      position: absolute;
      left: 530px;
      width: 400px;
      top: 370px;
      text-align: center;
      font-size: 30px;
      color: #9a96a6;
    }
    #bs-card {
      position: absolute;
      left: 530px;
      top: 100px;
      width: 400px;
      height: 590px;
      border-radius: 28px;
      background: #f4f3f8;
    }
    .dchip {
      position: absolute;
      width: 104px;
      height: 104px;
      border-radius: 20px;
      background: #fff;
      border: 3px solid #e2e0ea;
      text-align: center;
      font-weight: 800;
      font-size: 26px;
      padding-top: 22px;
      line-height: 1.2;
    }
    .dchip.on {
      background: #0b0b0c;
      color: #f6c42b;
      border-color: #0b0b0c;
    }
    .tile {
      position: absolute;
      width: 200px;
      height: 200px;
      border-radius: 22px;
    }
'''
tiles = "".join(f'<div class="tile bs-t" style="left:{36 + (i % 2) * 220}px;top:{260 + (i // 2) * 220}px;background:{c}"></div>' for i, c in enumerate(["linear-gradient(135deg,#1a2140,#4a63c9)", "#f6c42b", "#e9e4d8", "linear-gradient(135deg,#4a63c9,#9fc3ff)"]))
days = "".join(f'<div class="dchip{" on" if d == "Wed" else ""}" id="bs-d{i}" style="left:{30 + i * 122}px;top:150px">{d}<br><span style="font-weight:600;font-size:22px">{n}</span></div>' for i, (d, n) in enumerate([("Mon", "27"), ("Tue", "28"), ("Wed", "29")]))
bs_inner = f'''
          <div style="position:absolute;left:0;top:0;right:0;height:70px;border-bottom:2px solid #eee"></div>
          <div style="position:absolute;left:36px;top:20px;font-weight:900;font-size:28px">YourBrand</div>
          <div style="position:absolute;left:36px;top:110px;width:420px;font-weight:900;font-size:54px;line-height:1.0;letter-spacing:-0.035em">Our work</div>
          {tiles}
          <div id="bs-empty"></div><div id="bs-et" class="mono">empty space</div>
          <div id="bs-card">
            <div style="position:absolute;left:30px;top:40px;font-weight:900;font-size:44px;letter-spacing:-0.03em">Book a visit</div>
            {days}
            <div class="bar" style="left:30px;top:310px;width:300px;background:#dcd9e5"></div>
            <div class="bar" style="left:30px;top:346px;width:240px;background:#dcd9e5"></div>
            <div class="btn" id="bs-btn" style="left:30px;right:30px;top:470px">Book now</div>
          </div>'''
bs_body = "\n".join([
    '      <div class="hd" id="bs-q">Two screens.<br>Is your website <em>using both?</em></div>',
    band("bs-b", bs_inner),
    '      <div class="hd" id="bs-a1">We make <em>both sides</em> work.</div>',
    '      <div class="chip mono" id="bs-l1" style="left:150px;top:1460px">browse</div>',
    '      <div class="chip mono" id="bs-l2" style="left:640px;top:1460px">book</div>',
])
bs_js = '''    gsap.set(["#bs-a1", "#bs-l1", "#bs-l2", "#bs-q", "#bs-card"], { opacity: 0 });
    gsap.set(".bs-t", { opacity: 0, scale: 0.6 });
    tl.fromTo("#bs-q", { opacity: 0, scale: 1.3 }, { opacity: 1, scale: 1, duration: 0.25, ease: "power4.out", immediateRender: false }, G(13.32));
    tl.fromTo("#bs-b", { opacity: 0, y: 200 }, { opacity: 1, y: 0, duration: 0.4, ease: "expo.out" }, G(13.4));
    tl.to(".bs-t", { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)", stagger: 0.12 }, G(13.82));
    // the right half just sits there
    tl.fromTo("#bs-empty", { opacity: 1 }, { opacity: 0.35, duration: 0.25, ease: "steps(1)", repeat: 7, yoyo: true, immediateRender: false }, G(14.8));
    // the fix: browse on the left, book on the right
    sink("#bs-q", G(16.6));
    rise("#bs-a1", G(16.76));
    tl.to(["#bs-empty", "#bs-et"], { opacity: 0, duration: 0.15 }, G(16.76));
    tl.fromTo("#bs-card", { opacity: 0, x: 140 }, { opacity: 1, x: 0, duration: 0.4, ease: "expo.out", immediateRender: false }, G(16.76));
    [17.74, 18.24, 18.73].forEach((t, i) => tl.fromTo("#bs-d" + i, { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.25, ease: "back.out(2.4)", immediateRender: false }, G(t)));
    pop("#bs-l1", G(19.23)); pop("#bs-l2", G(19.71));
    tl.fromTo("#bs-btn", { scale: 1 }, { scale: 0.92, duration: 0.1, ease: "power2.in", yoyo: true, repeat: 1, immediateRender: false }, G(20.21));
    tl.to(["#bs-b", "#bs-l1", "#bs-l2"], { opacity: 0, scale: 0.92, duration: 0.25, ease: "power2.in" }, G(21.3));
    sink("#bs-a1", G(21.3));'''
write("both", comp("both", 13.28, 8.32, bs_css, bs_body, bs_js))

# ======================================================================
# RETURN (21.6 – 26.6): the same unfold — now it works
# ======================================================================
WIDE = '''
          <div style="position:absolute;left:0;top:0;right:0;height:70px;border-bottom:2px solid #eee"></div>
          <div style="position:absolute;left:36px;top:20px;font-weight:900;font-size:28px">YourBrand</div>
          <div style="position:absolute;left:530px;top:24px;font-weight:600;font-size:24px;color:#555;white-space:nowrap">Home &nbsp; Work &nbsp; Contact</div>
          <div style="position:absolute;left:36px;top:110px;width:420px;font-weight:900;font-size:64px;line-height:0.98;letter-spacing:-0.035em">Open daily.<br>Book online.</div>
          <div class="bar" style="left:36px;top:280px;width:380px"></div>
          <div class="bar" style="left:36px;top:316px;width:320px"></div>
          <div class="btn" style="left:36px;width:300px;top:380px">Book now</div>
          <div style="position:absolute;left:530px;top:100px;width:400px;height:280px;border-radius:26px;background:linear-gradient(135deg,#1a2140,#4a63c9)"></div>
          <div style="position:absolute;left:530px;top:400px;width:190px;height:290px;border-radius:26px;background:#f6c42b"></div>
          <div style="position:absolute;left:740px;top:400px;width:190px;height:290px;border-radius:26px;background:#e9e4d8"></div>
          <div style="position:absolute;left:36px;top:500px;width:420px;height:190px;border-radius:26px;background:#f4f3f8"></div>'''
rt_body = "\n".join([
    '      <div class="pov mono" id="rt-pov">same POV. our build.</div>',
    '      <div class="hd" id="rt-t1">Your customer unfolds <em>again</em>…</div>',
    '      <div class="hd" id="rt-t2">A website that unfolds as nicely as <em>the phone.</em></div>',
    closed("rt-c", MOBILE),
    band("rt-b", WIDE),
    '      <div class="tag mono" id="rt-g1" style="left:180px;top:1450px">5.4″ ✓</div>',
    '      <div class="tag mono" id="rt-g2" style="left:420px;top:1450px">7.6″ ✓</div>',
    '      <div class="tag mono" id="rt-g3" style="left:660px;top:1450px">hinge ✓</div>',
])
rt_js = '''    gsap.set(["#rt-pov", "#rt-t1", "#rt-t2", "#rt-g1", "#rt-g2", "#rt-g3", "#rt-b"], { opacity: 0 });
    rise("#rt-pov", G(21.68));
    rise("#rt-t1", G(21.68));
    tl.fromTo("#rt-c", { opacity: 0, y: 200 }, { opacity: 1, y: 0, duration: 0.35, ease: "expo.out", immediateRender: false }, G(21.68));
    pop("#rt-g1", G(22.18));
    unfold("#rt-c", "#rt-b", G(22.66));
    pop("#rt-g2", G(23.15));
    pop("#rt-g3", G(23.39));
    sink("#rt-t1", G(23.25));
    rise("#rt-t2", G(23.39));
    tl.fromTo("#rt-b", { y: 0 }, { y: -12, duration: 0.49, ease: "sine.inOut", repeat: 5, yoyo: true, immediateRender: false }, G(23.7));
    sink(["#rt-pov", "#rt-t2", "#rt-g1", "#rt-g2", "#rt-g3", "#rt-b"], G(26.35));'''
write("ret", comp("ret", 21.6, 5.0, "", rt_body, rt_js))

# ======================================================================
# LOGO (26.58 – 31.0)
# ======================================================================
lg_css = '''    #lg-glow {
      position: absolute;
      left: 240px;
      top: 380px;
      width: 600px;
      height: 600px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(246, 196, 43, 0.35) 0%, rgba(246, 196, 43, 0) 65%);
    }
    #lg-logo {
      position: absolute;
      left: 290px;
      top: 500px;
      width: 500px;
      height: 352px;
      background: url("assets/brand/deveraxtech-logo.png") center / contain no-repeat;
    }
    #lg-word {
      position: absolute;
      left: 0;
      right: 0;
      top: 890px;
      text-align: center;
      font-weight: 900;
      font-size: 104px;
      letter-spacing: -0.03em;
      color: #f6c42b;
    }
    #lg-tag {
      position: absolute;
      left: 0;
      right: 0;
      top: 1022px;
      text-align: center;
      font-weight: 700;
      font-size: 30px;
      letter-spacing: 0.3em;
      text-indent: 0.3em;
      color: #c9d2f5;
    }
    #lg-ask {
      top: 1120px;
      font-size: 72px;
    }
    #lg-url {
      left: 0;
      right: 0;
      margin: 0 auto;
      width: 440px;
      text-align: center;
      top: 1250px;
      background: #f6c42b;
      color: #0b0b0c;
      border-color: #f6c42b;
    }
'''
lg_body = '''      <div id="lg-glow"></div>
      <div id="lg-logo" role="img" aria-label="DevEraXTech logo"></div>
      <div id="lg-word">DevEraXTech</div>
      <div id="lg-tag">ENGINEERED EXCELLENCE</div>
      <div class="hd" id="lg-ask">Is your website <em>Duo-ready?</em></div>
      <div class="chip mono" id="lg-url">deveraxtech.com</div>'''
lg_js = '''    gsap.set(["#lg-word", "#lg-tag", "#lg-ask", "#lg-url"], { opacity: 0, y: 20 });
    gsap.set("#lg-glow", { opacity: 0, scale: 0.4, transformOrigin: "50% 50%" });
    tl.fromTo("#lg-logo", { opacity: 0, scaleX: 0.05, scaleY: 1, transformOrigin: "50% 50%" }, { opacity: 1, scaleX: 1, duration: 0.4, ease: "expo.out" }, 0.0);
    tl.to("#lg-glow", { opacity: 1, scale: 1, duration: 0.6, ease: "power2.out" }, 0.05);
    tl.to("#lg-word", { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0.45);
    tl.to("#lg-tag", { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0.6);
    tl.to("#lg-ask", { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }, 0.98);
    tl.to("#lg-url", { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }, 1.47);
    tl.to("#lg-glow", { scale: 1.12, duration: 0.49, ease: "sine.inOut", repeat: 4, yoyo: true }, 1.0);'''
write("logo", comp("logo", 26.58, 4.42, lg_css, lg_body, lg_js))

# ======================================================================
# brand mark (0 – 26.5)
# ======================================================================
bc = '''<template>
  <style>
    #root {
      position: absolute;
      inset: 0;
    }
    #bc {
      position: absolute;
      left: 60px;
      top: 96px;
      display: flex;
      align-items: center;
      gap: 12px;
    }
    #bc i {
      width: 56px;
      height: 40px;
      background: url("assets/brand/deveraxtech-logo.png") center / contain no-repeat;
    }
    #bc span {
      font-family: "DejaVu Sans Mono", monospace;
      font-weight: 700;
      font-size: 28px;
      letter-spacing: 0.08em;
      color: #c9d2f5;
    }
  </style>
  <div id="root" data-composition-id="brandcue" data-width="1080" data-height="1920">
    <div id="bc-wrap" class="clip" data-start="0" data-duration="26.5">
      <div id="bc"><i role="img" aria-label="DevEraXTech logo"></i><span>DEVERAXTECH // DUO CHECK</span></div>
    </div>
  </div>
  <script>
    const tl = gsap.timeline({ paused: true });
    tl.to("#bc", { opacity: 0, duration: 0.2 }, 26.3);
    window.__timelines["brandcue"] = tl;
  </script>
</template>
'''
write("brandcue", bc)

# ======================================================================
# root
# ======================================================================
SC = [("hook", 0, 7.4, 1), ("button", 7.38, 5.92, 2), ("both", 13.28, 8.32, 1), ("ret", 21.6, 5.0, 2), ("logo", 26.58, 4.42, 3)]
SFX = [("pov", 0.05, 0.05, 0.6, "select_008.ogg"), ("open", 0.53, 0.3, 0.8, "impactSoft_heavy_001.ogg"),
       ("gl1", 1.02, 0.03, 0.6, "glitch_002.ogg"), ("gl2", 1.2, 0.03, 0.6, "glitch_004.ogg"), ("gl3", 2.5, 0.03, 0.6, "glitch_002.ogg"),
       ("g1", 2.94, 0.12, 0.6, "bong_001.ogg"), ("g2", 3.38, 0.12, 0.6, "bong_001.ogg"), ("g3", 3.85, 0.12, 0.6, "bong_001.ogg"),
       ("stay", 4.84, 0.05, 0.6, "select_008.ogg"), ("out1", 7.0, 0.6, 0.35, "card-shove-1.ogg"),
       ("q2", 7.42, 0.3, 0.75, "impactWood_medium_002.ogg"), ("tear", 7.91, 0.5, 0.45, "error_005.ogg"), ("tap", 8.89, 0.09, 0.6, "click3.ogg"),
       ("a1", 9.38, 0.2, 0.5, "impactWood_medium_001.ogg"), ("fix", 10.87, 0.19, 0.6, "drop_002.ogg"), ("safe", 11.35, 0.05, 0.6, "select_008.ogg"), ("out2", 13.05, 0.6, 0.35, "card-shove-1.ogg"),
       ("q3", 13.32, 0.3, 0.75, "impactWood_medium_002.ogg"), ("t1", 13.82, 0.2, 0.35, "card-place-1.ogg"), ("t2", 13.94, 0.2, 0.35, "card-place-2.ogg"), ("t3", 14.06, 0.2, 0.35, "card-place-3.ogg"), ("t4", 14.18, 0.2, 0.35, "card-place-4.ogg"),
       ("card", 16.76, 0.6, 0.45, "card-slide-2.ogg"), ("d1", 17.74, 0.2, 0.4, "impactWood_light_001.ogg"), ("d2", 18.24, 0.2, 0.4, "impactWood_light_001.ogg"), ("d3", 18.73, 0.2, 0.4, "impactWood_light_001.ogg"),
       ("l1", 19.23, 0.05, 0.6, "select_008.ogg"), ("l2", 19.71, 0.05, 0.6, "select_008.ogg"), ("press", 20.21, 0.09, 0.6, "click3.ogg"), ("out3", 21.3, 0.6, 0.35, "card-shove-1.ogg"),
       ("q4", 21.68, 0.3, 0.7, "impactWood_medium_002.ogg"), ("r1", 22.18, 0.05, 0.6, "select_008.ogg"), ("open2", 22.66, 0.3, 0.8, "impactSoft_heavy_001.ogg"),
       ("r2", 23.15, 0.05, 0.6, "select_008.ogg"), ("r3", 23.39, 0.05, 0.6, "select_008.ogg"),
       ("stamp", 26.58, 0.3, 0.8, "impactWood_medium_002.ogg"), ("sig", 26.62, 2.8, 0.6, "sig-full.wav")]
rows = [f'      <div id="{c}" data-composition-id="{c}" data-composition-src="compositions/{c}.html" data-start="{s}" data-duration="{d}" data-track-index="{z}" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: {z}"></div>' for c, s, d, z in SC]
rows.append('      <div id="brandcue" data-composition-id="brandcue" data-composition-src="compositions/brandcue.html" data-start="0" data-duration="26.5" data-track-index="4" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 5"></div>')
aud = ['      <audio id="music" class="clip" data-start="0" data-duration="31" data-track-index="10" data-volume="0.5" data-fade-out="1.0" src="assets/music/voxel-revolution-kevin-macleod.mp3"></audio>']
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
        background: #050814;
      }
      #root {
        position: relative;
        width: 100%;
        height: 100%;
      }
      /* night sky: deep navy, a faint star field, a cool glow behind the screen */
      #sky {
        position: absolute;
        inset: 0;
        background:
          radial-gradient(ellipse 75% 45% at 50% 54%, rgba(74, 99, 201, 0.45) 0%, rgba(74, 99, 201, 0) 70%),
          radial-gradient(circle, rgba(255, 255, 255, 0.55) 1.2px, rgba(255, 255, 255, 0) 1.8px) 0 0 / 97px 89px,
          radial-gradient(circle, rgba(255, 255, 255, 0.3) 1px, rgba(255, 255, 255, 0) 1.6px) 41px 23px / 61px 67px,
          linear-gradient(180deg, #0b1433 0%, #050814 100%);
      }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="31" data-width="1080" data-height="1920">
      <div id="sky"></div>
''' + "\n".join(rows) + '''

      <!-- Music: "Voxel Revolution" by Kevin MacLeod (incompetech.com), CC BY 4.0 -->
''' + "\n".join(aud) + '''
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({ paused: true });
    </script>
  </body>
</html>
'''
open(os.path.join(HERE, "..", "index.html"), "w").write(root)
print("ok")
