"""'The Atelier': a luxury brand film. Real footage of master crafts (watchmaking, calligraphy, gold casting)
dissolving into a developer at work. No questions, no hard sell: brand awareness for DevEraXTech."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "compositions")
TOTAL = 32.0
X = 0.6  # dissolve length

# (file, start, end): each shot after the first dissolves in over X seconds before its cut point
SHOTS = [("l1-watch", 0.0, 4.73), ("l2-pen", 4.73, 9.39), ("l3-gold", 9.39, 14.07), ("l4-code", 14.07, 18.74),
         ("l5-keys", 18.74, 21.08), ("l5-face", 21.08, 23.43), ("l6-movement", 23.43, 25.77)]

# chapter lines: (id, label, line, in, out)
LINES = [("t1", "I · Microns", "A watchmaker works in microns.", 0.0, 4.25),
         ("t2", "II · Strokes", "A calligrapher, in single strokes.", 4.95, 8.95),
         ("t3", "III · Degrees", "Gold is poured to the degree.", 9.6, 13.65),
         ("t4", "IV · Milliseconds", "We work in milliseconds.", 14.3, 18.3),
         ("t5", "", "Because a website<br>is a craft, too.", 18.95, 23.0),
         ("t6", "", "Measured. Refined.<br>Built to last.", 23.6, 25.35)]

FONTS = '''    @font-face {
      font-family: "Cormorant Garamond";
      font-style: italic;
      font-weight: 500;
      src: url("assets/fonts/CormorantGaramond-italic.woff2") format("woff2");
    }
    @font-face {
      font-family: "Cormorant Garamond";
      font-style: normal;
      font-weight: 500;
      src: url("assets/fonts/CormorantGaramond-normal.woff2") format("woff2");
    }
    @font-face {
      font-family: "Cinzel";
      font-style: normal;
      font-weight: 500;
      src: url("assets/fonts/Cinzel-normal.woff2") format("woff2");
    }
'''

# ---------------------------------------------------------------- chapter titles
css = FONTS + '''    #root {
      position: absolute;
      inset: 0;
    }
    .ch {
      position: absolute;
      left: 80px;
      right: 80px;
      top: 1150px;
      text-align: center;
    }
    .ch .lab {
      display: block;
      font-family: "Cinzel", serif;
      font-weight: 500;
      font-size: 30px;
      letter-spacing: 0.42em;
      text-indent: 0.42em;
      text-transform: uppercase;
      color: #edd28c;
      text-shadow: 0 2px 14px rgba(0, 0, 0, 0.9);
    }
    .ch .rule {
      display: block;
      width: 120px;
      height: 2px;
      margin: 26px auto 30px;
      background: linear-gradient(90deg, rgba(217, 185, 104, 0), #d9b968, rgba(217, 185, 104, 0));
    }
    .ch .ln {
      display: block;
      font-family: "Cormorant Garamond", serif;
      font-style: italic;
      font-weight: 500;
      font-size: 82px;
      line-height: 1.08;
      color: #f7f2e8;
      text-shadow: 0 4px 30px rgba(0, 0, 0, 0.65);
    }
'''
body = []
for i, lab, ln, a, b in LINES:
    labhtml = f'<span class="lab">{lab}</span><span class="rule"></span>' if lab else '<span class="rule"></span>'
    body.append(f'      <div class="ch" id="{i}">{labhtml}<span class="ln">{ln}</span></div>')
js = "    gsap.set([" + ", ".join(f'"#{l[0]}"' for l in LINES[1:]) + "], { opacity: 0 });\n"
js += '    // frame 0: the first chapter is already set; its gold rule draws out\n'
js += '    tl.fromTo("#t1 .rule", { scaleX: 0.2 }, { scaleX: 1, duration: 1.2, ease: "power2.out" }, 0);\n'
js += '    tl.fromTo("#t1 .ln", { scale: 1.04 }, { scale: 1, duration: 3.0, ease: "power1.out" }, 0);\n'
js += f'    tl.to("#t1", {{ opacity: 0, y: -14, filter: "blur(6px)", duration: 0.5, ease: "power2.in" }}, {LINES[0][4]});\n'
for i, lab, ln, a, b in LINES[1:]:
    js += f'    tl.fromTo("#{i}", {{ opacity: 0, y: 18, filter: "blur(8px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.9, ease: "power2.out", immediateRender: false }}, {a});\n'
    js += f'    tl.fromTo("#{i} .rule", {{ scaleX: 0.2 }}, {{ scaleX: 1, duration: 1.2, ease: "power2.out", immediateRender: false }}, {a});\n'
    js += f'    tl.to("#{i}", {{ opacity: 0, y: -14, filter: "blur(6px)", duration: 0.5, ease: "power2.in" }}, {b});\n'
open(os.path.join(OUT, "chapters.html"), "w").write(f'''<template>
  <style>
{css}  </style>
  <div id="root" data-composition-id="chapters" data-width="1080" data-height="1920">
    <div id="ch-wrap" class="clip" data-start="0" data-duration="25.77" data-layout-allow-overflow data-layout-allow-overlap>
{chr(10).join(body)}
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}    window.__timelines["chapters"] = tl;
  </script>
</template>
''')

# ---------------------------------------------------------------- the signature
sig = '''<template>
  <style>
''' + FONTS + '''    #root {
      position: absolute;
      inset: 0;
    }
    #sg-bg {
      position: absolute;
      inset: 0;
      background: radial-gradient(ellipse 70% 45% at 50% 44%, #1b1710 0%, #0a0907 55%, #050504 100%);
    }
    #sg-logo {
      position: absolute;
      left: 320px;
      top: 560px;
      width: 440px;
      height: 310px;
      background: url("assets/brand/deveraxtech-logo.png") center / contain no-repeat;
    }
    /* a slow band of light passes across the logo, like light on polished metal */
    #sg-sheen {
      position: absolute;
      left: 320px;
      top: 560px;
      width: 440px;
      height: 310px;
      background: linear-gradient(105deg, rgba(255, 255, 255, 0) 35%, rgba(255, 246, 220, 0.55) 50%, rgba(255, 255, 255, 0) 65%) 0 0 / 300% 100% no-repeat;
      -webkit-mask: url("assets/brand/deveraxtech-logo.png") center / contain no-repeat;
      mask: url("assets/brand/deveraxtech-logo.png") center / contain no-repeat;
    }
    #sg-word {
      position: absolute;
      left: 0;
      right: 0;
      top: 930px;
      text-align: center;
      font-family: "Cinzel", serif;
      font-weight: 500;
      font-size: 84px;
      letter-spacing: 0.08em;
      text-indent: 0.08em;
      color: #e3c77e;
    }
    #sg-rule {
      position: absolute;
      left: 440px;
      top: 1052px;
      width: 200px;
      height: 2px;
      background: linear-gradient(90deg, rgba(217, 185, 104, 0), #d9b968, rgba(217, 185, 104, 0));
    }
    #sg-tag {
      position: absolute;
      left: 0;
      right: 0;
      top: 1082px;
      text-align: center;
      font-family: "Cinzel", serif;
      font-size: 30px;
      letter-spacing: 0.5em;
      text-indent: 0.5em;
      color: #cfc4ad;
    }
    #sg-line {
      position: absolute;
      left: 0;
      right: 0;
      top: 1180px;
      text-align: center;
      font-family: "Cormorant Garamond", serif;
      font-style: italic;
      font-size: 64px;
      color: #f7f2e8;
    }
    #sg-url {
      position: absolute;
      left: 0;
      right: 0;
      top: 1300px;
      text-align: center;
      font-family: "Cormorant Garamond", serif;
      font-size: 40px;
      letter-spacing: 0.18em;
      text-indent: 0.18em;
      color: #d9b968;
    }
  </style>
  <div id="root" data-composition-id="signature" data-width="1080" data-height="1920">
    <div id="sg-wrap" class="clip" data-start="0" data-duration="6.23">
      <div id="sg-bg"></div>
      <div id="sg-logo" role="img" aria-label="DevEraXTech logo"></div>
      <div id="sg-sheen"></div>
      <div id="sg-word">DevEraXTech</div>
      <div id="sg-rule"></div>
      <div id="sg-tag">ENGINEERED EXCELLENCE</div>
      <div id="sg-line">Websites, crafted.</div>
      <div id="sg-url">deveraxtech.com</div>
    </div>
  </div>
  <script>
    const tl = gsap.timeline({ paused: true });
    // host starts 25.77 s (strong cue); everything arrives slowly, nothing bounces
    gsap.set(["#sg-word", "#sg-tag", "#sg-line", "#sg-url"], { opacity: 0, y: 14 });
    gsap.set("#sg-rule", { scaleX: 0 });
    tl.fromTo("#sg-bg", { opacity: 0 }, { opacity: 1, duration: 0.6, ease: "power1.out" }, 0.0);
    tl.fromTo("#sg-logo", { opacity: 0, scale: 0.94, filter: "blur(12px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 1.6, ease: "power2.out" }, 0.2);
    tl.fromTo("#sg-sheen", { backgroundPosition: "100% 0" }, { backgroundPosition: "-50% 0", duration: 1.8, ease: "power1.inOut" }, 1.2);
    tl.to("#sg-word", { opacity: 1, y: 0, duration: 1.0, ease: "power2.out" }, 1.2);
    tl.to("#sg-rule", { scaleX: 1, duration: 1.0, ease: "power2.out" }, 1.7);
    tl.to("#sg-tag", { opacity: 1, y: 0, duration: 1.0, ease: "power2.out" }, 1.9);
    tl.to("#sg-line", { opacity: 1, y: 0, duration: 1.0, ease: "power2.out" }, 2.7);
    tl.to("#sg-url", { opacity: 1, y: 0, duration: 1.0, ease: "power2.out" }, 3.3);
    tl.fromTo("#sg-sheen", { backgroundPosition: "100% 0" }, { backgroundPosition: "-50% 0", duration: 1.8, ease: "power1.inOut", immediateRender: false }, 4.2);
    window.__timelines["signature"] = tl;
  </script>
</template>
'''
open(os.path.join(OUT, "signature.html"), "w").write(sig)

# ---------------------------------------------------------------- root
vids, mjs = [], []
for i, (f, s, e) in enumerate(SHOTS):
    a = s if i == 0 else round(s - X, 2)
    d = round(e - a, 2)
    vids.append(f'      <video id="v{i}" class="clip" data-start="{a}" data-duration="{d}" data-track-index="{1 + i % 2}" muted playsinline src="assets/footage/{f}.mp4" style="position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover;z-index:{1 + i}"></video>')
    mjs.append(f'      main.fromTo("#v{i}", {{ scale: 1.0 }}, {{ scale: 1.05, duration: {d}, ease: "none" }}, {a});')
    if i > 0:
        mjs.append(f'      main.fromTo("#v{i}", {{ opacity: 0 }}, {{ opacity: 1, duration: {X}, ease: "power1.inOut", immediateRender: false }}, {a});')
mjs.append('      main.to("#v6", { opacity: 0, duration: 0.55, ease: "power1.in" }, 25.2);')
aud = [f'      <audio id="music" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="10" data-volume="0.9" data-fade-out="2.2" src="assets/music/gymnopedie-no1-kevin-macleod.mp3"></audio>',
       '      <audio id="s-sig" class="clip" data-start="26.0" data-duration="2.8" data-track-index="11" data-volume="0.35" src="assets/sfx/sig-full.wav"></audio>']
root = f'''<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      @font-face {{
        font-family: "Cinzel";
        font-style: normal;
        font-weight: 500;
        src: url("assets/fonts/Cinzel-normal.woff2") format("woff2");
      }}
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
      /* lens vignette and a warm lift */
      #grade {{
        position: absolute;
        inset: 0;
        z-index: 20;
        background:
          radial-gradient(ellipse 85% 70% at 50% 48%, rgba(0, 0, 0, 0) 50%, rgba(0, 0, 0, 0.62) 100%),
          linear-gradient(180deg, rgba(0, 0, 0, 0.0) 0%, rgba(0, 0, 0, 0.0) 46%, rgba(0, 0, 0, 0.62) 62%, rgba(0, 0, 0, 0.72) 80%, rgba(0, 0, 0, 0.6) 100%);
      }}
      /* cinema bars, with a quiet maker's mark in the top one */
      .bar {{
        position: absolute;
        left: 0;
        right: 0;
        height: 150px;
        background: #000;
        z-index: 30;
      }}
      #mark {{
        position: absolute;
        left: 0;
        right: 0;
        top: 66px;
        z-index: 31;
        text-align: center;
        font-family: "Cinzel", serif;
        font-size: 28px;
        letter-spacing: 0.6em;
        text-indent: 0.6em;
        color: #b99a52;
      }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{chr(10).join(vids)}
      <div id="grade"></div>
      <div id="chapters" data-composition-id="chapters" data-composition-src="compositions/chapters.html" data-start="0" data-duration="25.77" data-track-index="4" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 25"></div>
      <div id="signature" data-composition-id="signature" data-composition-src="compositions/signature.html" data-start="25.77" data-duration="6.23" data-track-index="5" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 26"></div>
      <div class="bar" style="top:0"></div>
      <div class="bar" style="bottom:0"></div>
      <div id="mark">DEVERAXTECH</div>

      <!-- Footage: Mixkit (mixkit.co), Mixkit Stock Video Free License -->
      <!-- Music: "Gymnopedie No. 1" (Erik Satie) performed by Kevin MacLeod (incompetech.com), CC BY 4.0 -->
{chr(10).join(aud)}
    </div>
    <script>
      const main = gsap.timeline({{ paused: true }});
      // each shot drifts in slowly; shots dissolve into one another
{chr(10).join(mjs)}
      main.fromTo("#mark", {{ opacity: 0.0 }}, {{ opacity: 1, duration: 1.5, ease: "power1.out" }}, 0.0);
      main.to("#mark", {{ opacity: 0, duration: 0.8 }}, 25.4);
      window.__timelines["main"] = main;
    </script>
  </body>
</html>
'''
open(os.path.join(HERE, "..", "index.html"), "w").write(root)
print("ok")
