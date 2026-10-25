"""Realistic news-style TikTok: real stock footage (Mixkit, free licence), the iPhone Duo hinge-crack reports,
then the second problem reviewers flagged: apps and sites not built for the fold. 2 hooks, 2 questions."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "compositions")
TOTAL = 30.0

# (file, start, duration): hard cuts on the beat
CLIPS = [("h1-hands", 0.0, 3.85), ("h2-upset", 3.85, 3.75), ("q1-woman", 7.6, 2.5), ("q1-hand", 10.1, 2.53),
         ("q2-frustrated", 12.63, 6.99), ("a1-walk", 19.62, 3.18), ("a1-typing", 22.8, 2.51), ("end-desk", 25.31, 4.69)]

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
    # hook 1: the trend
    cap("c1", "iPhone Duo owners are already reporting <em>cracks at the hinge.</em>"),
    news("n1", "TOM’S GUIDE", "The iPhone Duo just came out, and owners are already seeing screens crack at the hinge", 760),
    news("n2", "DIGITAL TRENDS", "Some iPhone Duo owners are reporting cracks around the hinge", 1010),
    news("n3", "GULF NEWS", "iPhone Duo Faces Early Durability Concerns as Screens Crack Along Hinge Hours After Launch", 1200),
    '      <div class="small" id="s1" style="top:1500px">early reports · cause not confirmed</div>',
    # hook 2: the turn
    cap("c2", "But reviewers flagged a <em>second</em> problem…"),
    news("n4", "MACSTORIES", "iPhone Duo Review Roundup: Great Hinge, <u>Messy Apps</u>, and Everybody Misses Face ID", 860),
    cap("c3", "…and this one is about <em>your website.</em>"),
    # question 1 (answered at the end)
    cap("c4", "When your customer <em>unfolds</em> their phone…"),
    cap("c5", "…does your website <em>fit the screen?</em>"),
    '      <div class="small" id="s2" style="top:1500px">answer at the end ↓</div>',
    # question 2 (answered on the spot)
    cap("c6", "Would you buy from a website that <em>looks broken?</em>"),
    cap("c7", "Most of us just <em>close the tab.</em>"),
    cap("c8", "Your customers do <em>the same.</em>"),
    # answer 1
    cap("c9", "The fix isn’t a new phone."),
    cap("c10", "It’s a <em>responsive website,</em> built to fit every screen, folded or not."),
    cap("c11", "That’s what we build."),
])

def show(i, a, b=None):
    s = f'    tl.fromTo("#{i}", {{ opacity: 0, scale: 0.88 }}, {{ opacity: 1, scale: 1, duration: 0.2, ease: "back.out(2.2)", immediateRender: false }}, {a});\n'
    if b is not None:
        s += f'    tl.to("#{i}", {{ opacity: 0, duration: 0.12 }}, {b});\n'
    return s

def card(i, a, b, rot):
    return (f'    tl.fromTo("#{i}", {{ opacity: 0, y: 80, rotation: {rot * 2} }}, {{ opacity: 1, y: 0, rotation: {rot}, duration: 0.3, ease: "back.out(1.8)", immediateRender: false }}, {a});\n'
            f'    tl.to("#{i}", {{ opacity: 0, y: -40, duration: 0.18, ease: "power2.in" }}, {b});\n')

ids = ["c1", "n1", "n2", "n3", "s1", "c2", "n4", "c3", "c4", "c5", "s2", "c6", "c7", "c8", "c9", "c10", "c11"]
js = "    gsap.set([" + ", ".join(f'"#{i}"' for i in ids if i != "c1") + "], { opacity: 0 });\n"
js += '    // frame 0: hook 1 is already on screen and the first card is on its way\n'
js += '    tl.fromTo("#c1", { scale: 1.06 }, { scale: 1, duration: 0.35, ease: "power2.out" }, 0);\n'
js += '    tl.to("#c1", { opacity: 0, duration: 0.12 }, 3.75);\n'
js += card("n1", 0.36, 3.75, -2) + card("n2", 1.30, 3.75, 1.5) + card("n3", 2.55, 3.75, -1)
js += show("s1", 2.84, 3.75)
js += show("c2", 3.85, 5.6) + card("n4", 4.52, 7.45, 1) + show("c3", 5.71, 7.45)
js += show("c4", 7.6, 8.75) + show("c5", 8.86, 12.5) + show("s2", 10.1, 12.5)
js += show("c6", 12.63, 15.66) + show("c7", 15.78, 17.55) + show("c8", 17.66, 19.5)
js += show("c9", 19.62, 21.45) + show("c10", 21.55, 23.34) + show("c11", 23.44, 25.2)

caps = f'''<template>
  <style>
{CSS}  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
    <div id="cap-wrap" class="clip" data-start="0" data-duration="25.31" data-layout-allow-overflow data-layout-allow-overlap>
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
    <div id="lg-wrap" class="clip" data-start="0" data-duration="4.69">
      <div id="lg-dim"></div>
      <div id="lg-logo" role="img" aria-label="DevEraXTech logo"></div>
      <div id="lg-word">DevEraXTech</div>
      <div id="lg-tag">ENGINEERED EXCELLENCE</div>
      <div id="lg-ask">Is your website ready <em>for the fold?</em></div>
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
SFX = [("w1", 0.36, 0.6, 0.35, "card-slide-2.ogg"), ("n1", 0.4, 0.3, 0.5, "card-place-1.ogg"), ("n2", 1.32, 0.3, 0.5, "card-place-2.ogg"), ("n3", 2.57, 0.3, 0.5, "card-place-3.ogg"),
       ("cut1", 3.85, 0.3, 0.6, "impactSoft_heavy_001.ogg"), ("n4", 4.54, 0.3, 0.5, "card-place-4.ogg"), ("c3", 5.71, 0.05, 0.5, "select_008.ogg"),
       ("cut2", 7.6, 0.3, 0.55, "impactWood_medium_002.ogg"), ("c5", 8.86, 0.05, 0.5, "select_008.ogg"), ("s2", 10.1, 0.05, 0.4, "select_008.ogg"),
       ("cut3", 12.63, 0.3, 0.6, "impactSoft_heavy_001.ogg"), ("c7", 15.78, 0.2, 0.5, "impactWood_medium_001.ogg"), ("c8", 17.66, 0.05, 0.5, "select_008.ogg"),
       ("cut4", 19.62, 0.3, 0.55, "impactWood_medium_002.ogg"), ("c10", 21.55, 0.05, 0.5, "select_008.ogg"), ("c11", 23.44, 0.2, 0.5, "impactWood_medium_001.ogg"),
       ("stamp", 25.36, 0.3, 0.7, "impactSoft_heavy_001.ogg"), ("sig", 25.4, 2.8, 0.6, "sig-full.wav")]
aud = [f'      <audio id="music" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="10" data-volume="0.5" data-fade-out="1.2" src="assets/music/investigations-kevin-macleod.mp3"></audio>']
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
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="25.31" data-track-index="4" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 5"></div>
      <div id="logo" data-composition-id="logo" data-composition-src="compositions/logo.html" data-start="25.31" data-duration="4.69" data-track-index="5" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 6"></div>

      <!-- Footage: Mixkit (mixkit.co), Mixkit Stock Video Free License -->
      <!-- Music: "Investigations" by Kevin MacLeod (incompetech.com), CC BY 4.0 -->
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
