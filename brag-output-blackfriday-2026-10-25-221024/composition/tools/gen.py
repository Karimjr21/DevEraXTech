"""Realistic Black Friday TikTok: real stock footage (Mixkit, free licence). Black Friday is Fri 27 Nov 2026,
33 days out. 2 hooks, 2 questions: one answered at the end, one on the spot."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "compositions")
TOTAL = 29.0

# (file, start, duration): hard cuts on the beat
CLIPS = [("h1-clock", 0.0, 3.88), ("h2-deals", 3.88, 3.84), ("q1-crowd", 7.72, 4.32), ("q2-hourglass", 12.04, 2.88),
         ("q2-frustrated", 14.92, 3.37), ("a1-shopping", 18.29, 2.87), ("a1-delivery", 21.16, 2.88), ("end-box", 24.04, 4.96)]

# ---------------------------------------------------------------- captions + headline cards
CSS = '''    #root {
      position: absolute;
      inset: 0;
      font-family: "Inter", sans-serif;
    }
    /* TikTok-style caption: white bold type with a black outline and soft shadow */
    .cap {
      position: absolute;
      left: 60px;
      right: 60px;
      top: 300px;
      text-align: center;
      font-weight: 800;
      font-size: 70px;
      line-height: 1.12;
      letter-spacing: -0.02em;
      color: #ffffff;
      -webkit-text-stroke: 10px #000000;
      paint-order: stroke fill;
      text-shadow: 0 6px 18px rgba(0, 0, 0, 0.45);
    }
    .cap em {
      font-style: normal;
      color: #ffd23f;
    }
    .small {
      position: absolute;
      left: 0;
      right: 0;
      text-align: center;
      font-weight: 700;
      font-size: 34px;
      color: #ffffff;
      -webkit-text-stroke: 6px #000;
      paint-order: stroke fill;
    }
    /* headline card, like a screenshot of a news story */
    .news {
      position: absolute;
      left: 90px;
      width: 900px;
      padding: 26px 32px 30px;
      background: #ffffff;
      border-radius: 22px;
      box-shadow: 0 24px 50px rgba(0, 0, 0, 0.45);
      color: #111;
      transform-origin: 50% 50%;
    }
    .news .src {
      font-weight: 800;
      font-size: 28px;
      letter-spacing: 0.02em;
      color: #c8102e;
      margin-bottom: 10px;
    }
    .news .hl {
      font-family: Georgia, "DejaVu Serif", serif;
      font-weight: 700;
      font-size: 38px;
      line-height: 1.2;
    }
'''

def cap(cid, html, top=300):
    return f'      <div class="cap" id="{cid}" style="top:{top}px">{html}</div>'

def news(nid, src, hl, top):
    return f'      <div class="news" id="{nid}" style="top:{top}px"><div class="src">{src}</div><div class="hl">{hl}</div></div>'

body = "\n".join([
    # hook 1: the countdown
    cap("c1", "Black Friday is <em>33 days</em> away."),
    '      <div class="small" id="s0" style="top:1500px">Friday, November 27</div>',
    # hook 2: the open loop
    cap("c2", "Early deals are <em>already live</em>…"),
    cap("c3", "…here’s the check <em>everyone forgets.</em>"),
    # question 1 (answered at the end)
    cap("c4", "What happens when <em>everyone</em> clicks at once?"),
    '      <div class="small" id="s2" style="top:1500px">answer at the end ↓</div>',
    # question 2 (answered on the spot)
    cap("c5", "How long would you wait for a <em>checkout</em> to load?"),
    cap("c6", "A few seconds… <em>then you’re gone.</em>"),
    cap("c7", "So are <em>your customers.</em>"),
    # answer 1
    cap("c8", "Build it to <em>handle the rush.</em>"),
    cap("c9", "Fast pages. <em>Smooth checkout.</em>"),
    cap("c10", "That’s what we build."),
])

def show(i, a, b=None):
    s = f'    tl.fromTo("#{i}", {{ opacity: 0, scale: 0.88 }}, {{ opacity: 1, scale: 1, duration: 0.2, ease: "back.out(2.2)", immediateRender: false }}, {a});\n'
    if b is not None:
        s += f'    tl.to("#{i}", {{ opacity: 0, duration: 0.12 }}, {b});\n'
    return s

def card(i, a, b, rot):
    return (f'    tl.fromTo("#{i}", {{ opacity: 0, y: 80, rotation: {rot * 2} }}, {{ opacity: 1, y: 0, rotation: {rot}, duration: 0.3, ease: "back.out(1.8)", immediateRender: false }}, {a});\n'
            f'    tl.to("#{i}", {{ opacity: 0, y: -40, duration: 0.18, ease: "power2.in" }}, {b});\n')

ids = ["c1", "s0", "c2", "c3", "c4", "s2", "c5", "c6", "c7", "c8", "c9", "c10"]
js = "    gsap.set([" + ", ".join(f'"#{i}"' for i in ids if i != "c1") + "], { opacity: 0 });\n"
js += '    // frame 0: hook 1 is already on screen and punching in\n'
js += '    tl.fromTo("#c1", { scale: 1.12 }, { scale: 1, duration: 0.3, ease: "power3.out" }, 0);\n'
js += '    tl.fromTo("#c1", { scale: 1 }, { scale: 1.08, duration: 0.12, ease: "power2.out", yoyo: true, repeat: 1, immediateRender: false }, 2.93);\n'
js += '    tl.to("#c1", { opacity: 0, duration: 0.12 }, 3.76);\n'
js += show("s0", 1.0, 3.76)
js += show("c2", 3.88, 5.68) + show("c3", 5.8, 7.6)
js += show("c4", 7.72, 11.92) + show("s2", 9.65, 11.92)
js += show("c5", 12.04, 14.8) + show("c6", 14.92, 16.73) + show("c7", 16.85, 18.17)
js += show("c8", 18.29, 20.08) + show("c9", 20.2, 22.01) + show("c10", 22.13, 23.92)

caps = f'''<template>
  <style>
{CSS}  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
    <div id="cap-wrap" class="clip" data-start="0" data-duration="24.04" data-layout-allow-overflow data-layout-allow-overlap>
{body}
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}    window.__timelines["captions"] = tl;
  </script>
</template>
'''
open(os.path.join(OUT, "captions.html"), "w").write(caps)

# ---------------------------------------------------------------- end card over the footage
logo = '''<template>
  <style>
    #root {
      position: absolute;
      inset: 0;
      font-family: "Inter", sans-serif;
    }
    #lg-dim {
      position: absolute;
      inset: 0;
      background: radial-gradient(ellipse 80% 60% at 50% 45%, rgba(8, 8, 10, 0.7), rgba(8, 8, 10, 0.9));
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
      color: #e6e6e6;
    }
    #lg-ask {
      position: absolute;
      left: 60px;
      right: 60px;
      top: 1110px;
      text-align: center;
      font-weight: 800;
      font-size: 64px;
      line-height: 1.1;
      color: #fff;
    }
    #lg-ask em {
      font-style: normal;
      color: #ffd23f;
    }
    #lg-url {
      position: absolute;
      left: 0;
      right: 0;
      margin: 0 auto;
      width: 400px;
      top: 1300px;
      padding: 12px 0 14px;
      border-radius: 999px;
      text-align: center;
      background: #f6c42b;
      color: #111;
      font-weight: 800;
      font-size: 38px;
    }
  </style>
  <div id="root" data-composition-id="logo" data-width="1080" data-height="1920">
    <div id="lg-wrap" class="clip" data-start="0" data-duration="4.96">
      <div id="lg-dim"></div>
      <div id="lg-logo" role="img" aria-label="DevEraXTech logo"></div>
      <div id="lg-word">DevEraXTech</div>
      <div id="lg-tag">ENGINEERED EXCELLENCE</div>
      <div id="lg-ask">Is your website ready for <em>Black Friday?</em></div>
      <div id="lg-url">deveraxtech.com</div>
    </div>
  </div>
  <script>
    const tl = gsap.timeline({ paused: true });
    gsap.set(["#lg-word", "#lg-tag", "#lg-ask", "#lg-url"], { opacity: 0, y: 20 });
    tl.fromTo("#lg-dim", { opacity: 0 }, { opacity: 1, duration: 0.35, ease: "power2.out" }, 0.0);
    tl.fromTo("#lg-logo", { opacity: 0, scale: 1.25, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.45, ease: "power3.out" }, 0.05);
    tl.to("#lg-word", { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0.55);
    tl.to("#lg-tag", { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0.7);
    tl.to("#lg-ask", { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }, 1.0);
    tl.to("#lg-url", { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }, 1.3);
    tl.to("#lg-url", { scale: 1.05, duration: 0.32, ease: "sine.inOut", repeat: 5, yoyo: true }, 1.9);
    window.__timelines["logo"] = tl;
  </script>
</template>
'''
open(os.path.join(OUT, "logo.html"), "w").write(logo)

# ---------------------------------------------------------------- root
vids = []
for i, (f, s, d) in enumerate(CLIPS):
    vids.append(f'      <video id="v-{f}" class="clip" data-start="{s}" data-duration="{d}" data-track-index="{1 + i % 2}" muted playsinline src="assets/footage/{f}.mp4" style="position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover"></video>')
SFX = [("tick1", 0.03, 0.12, 0.6, "bong_001.ogg"), ("date", 1.0, 0.05, 0.5, "select_008.ogg"), ("hit1", 2.93, 0.3, 0.7, "impactSoft_heavy_001.ogg"),
       ("cut1", 3.88, 0.6, 0.35, "card-slide-2.ogg"), ("c3", 5.8, 0.05, 0.5, "select_008.ogg"),
       ("cut2", 7.72, 0.3, 0.6, "impactWood_medium_002.ogg"), ("s2", 9.65, 0.05, 0.4, "select_008.ogg"),
       ("cut3", 12.04, 0.3, 0.6, "impactSoft_heavy_001.ogg"), ("c6", 14.92, 0.2, 0.5, "impactWood_medium_001.ogg"), ("c7", 16.85, 0.05, 0.5, "select_008.ogg"),
       ("cut4", 18.29, 0.3, 0.6, "impactWood_medium_002.ogg"), ("c9", 20.2, 0.05, 0.5, "select_008.ogg"), ("c10", 22.13, 0.2, 0.5, "impactWood_medium_001.ogg"),
       ("stamp", 24.09, 0.3, 0.7, "impactSoft_heavy_001.ogg"), ("sig", 24.13, 2.8, 0.6, "sig-full.wav")]
aud = [f'      <audio id="music" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="10" data-volume="0.42" data-fade-out="1.2" src="assets/music/werq-kevin-macleod.mp3"></audio>']
aud += [f'      <audio id="s-{n}" class="clip" data-start="{s}" data-duration="{d}" data-track-index="{11 + i}" data-volume="{v}" src="assets/sfx/{f}"></audio>' for i, (n, s, d, v, f) in enumerate(SFX)]
root = f'''<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }}
      html,
      body {{
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: #000;
      }}
      #root {{
        position: relative;
        width: 100%;
        height: 100%;
        overflow: hidden;
      }}
      /* soft top and bottom shade so captions read over any shot */
      #shade {{
        position: absolute;
        inset: 0;
        z-index: 3;
        background: linear-gradient(180deg, rgba(0, 0, 0, 0.45) 0%, rgba(0, 0, 0, 0) 32%, rgba(0, 0, 0, 0) 70%, rgba(0, 0, 0, 0.35) 100%);
      }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{chr(10).join(vids)}
      <div id="shade"></div>
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="24.04" data-track-index="4" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 5"></div>
      <div id="logo" data-composition-id="logo" data-composition-src="compositions/logo.html" data-start="24.04" data-duration="4.96" data-track-index="5" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 6"></div>

      <!-- Footage: Mixkit (mixkit.co), Mixkit Stock Video Free License -->
      <!-- Music: "Werq" by Kevin MacLeod (incompetech.com), CC BY 4.0 -->
{chr(10).join(aud)}
    </div>
    <script>
      const main = gsap.timeline({{ paused: true }});
      // slow handheld-style push on every shot
''' + "".join(f'      main.fromTo("#v-{f}", {{ scale: 1.0 }}, {{ scale: 1.06, duration: {d}, ease: "none" }}, {s});\n' for f, s, d in CLIPS) + '''      window.__timelines["main"] = main;
    </script>
  </body>
</html>
'''
open(os.path.join(HERE, "..", "index.html"), "w").write(root)
print("ok")
