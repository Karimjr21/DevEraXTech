import subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
tmp = os.path.join(HERE, "_site_base.html")
subprocess.run([sys.executable, os.path.join(HERE, "gen.py"), tmp, os.path.join(HERE, "site.tpl.html")], check=True, capture_output=True)
base = open(tmp).read(); os.remove(tmp)

SITE_ON = '''    // the site is already rendered; the code is hidden underneath
    gsap.set(["#sc-ed", ".ln", "#sc-cur"], { opacity: 0 });
    TYPING.forEach(([i]) => gsap.set("#sc-c" + i, { clipPath: "inset(0% 0% 0% 0%)" }));
    FLY.forEach(([sel]) => gsap.set(sel, { y: 0, x: 0, scale: 1, opacity: 1, filter: "blur(0px)" }));
    gsap.set("#sc-hero", { opacity: 1 });
'''
modes = {
 "hero": dict(dur=8.5, titles='''      <div class="ttl" id="hs-t1"><span class="s">What does a premium</span><span class="m">website look like</span><span class="s">on the inside?</span></div>
      <div class="ans-l" id="hs-ans">ANSWER AT THE END</div>
      <div id="hs-seam" style="position: absolute; left: 240px; top: 618px; width: 600px; height: 4px; border-radius: 2px; background: linear-gradient(90deg, rgba(212,175,55,0), #d4af37 8%, #fff1bf 55%, #f2d17b 100%); box-shadow: 0 0 14px rgba(242,209,123,0.85); transform-origin: 0 50%"></div>
      <div id="hs-term" style="position: absolute; left: 228px; top: 608px; width: 24px; height: 24px; border-radius: 50%; border: 4px solid #f2d17b; background: #0a0a0a; box-shadow: 0 0 16px rgba(242,209,123,0.9)"></div>
      <div class="ttl" id="hs-t2"><span class="a">You only see</span><span class="b" style="font-size: 118px">the surface.</span></div>''',
  tl=SITE_ON + '''    gsap.set("#hs-t2", { opacity: 0, filter: "blur(10px)" });
    gsap.set("#hs-seam", { scaleX: 0 });
    gsap.set("#hs-term", { x: 0, opacity: 0 });
    const tl = gsap.timeline({ paused: true });
    // motion inside the first second: the seam draws, the sheen crosses, the stars drift
    tl.to("#hs-term", { opacity: 1, duration: 0.05 }, 0.35);
    tl.to("#hs-seam", { scaleX: 1, duration: 0.7, ease: "expo.out" }, 0.35);
    tl.to("#hs-term", { x: 600, duration: 0.7, ease: "expo.out" }, 0.35);
    tl.to("#sc-r-h1", { backgroundPosition: "0% 0", duration: 2.0, ease: "power2.inOut" }, 0.8);
    tl.fromTo("#sc-stars", { y: 0 }, { y: -40, duration: 8.4, ease: "none" }, 0);
    tl.to(["#hs-seam", "#hs-term"], { opacity: 0, duration: 0.3, ease: "power2.in" }, 3.7);
    // question 1 is on screen from frame 0 over the live deveraxtech.com hero; it is answered only at the end
    tl.to(["#hs-t1", "#hs-ans"], { opacity: 0, filter: "blur(10px)", duration: 0.3, ease: "power3.in" }, 3.7);
    tl.to("#hs-t2", { opacity: 1, filter: "blur(0px)", duration: 0.35, ease: "power3.out" }, 4.1);
    // the surface, slowly: the site's own gold sheen crosses the headline
    tl.to("#sc-r-h1", { backgroundPosition: "100% 0", duration: 2.4, ease: "power2.inOut" }, 4.4);
    tl.to("#sc-r-b1", { boxShadow: "0 0 0 6px rgba(242,209,123,0.35), 0 0 40px rgba(242,209,123,0.6)", duration: 0.6, ease: "power2.out" }, 6.6);
    tl.to("#hs-t2", { opacity: 0, filter: "blur(10px)", duration: 0.25, ease: "power3.in" }, 8.1);
'''),
 "inside": dict(dur=8.9, titles='''      <div class="ttl" id="hi-t1"><span class="s" style="font-size: 60px">So… what does a premium</span><span class="m">website look like</span><span class="s">on the inside?</span></div>
      <div class="ttl" id="hi-t2"><span class="b" style="font-size: 150px">Like this.</span></div>
      <div class="ttl" id="hi-t3"><span class="a">Every pixel</span><span class="b" style="font-size: 92px">starts as code.</span></div>''',
  tl=SITE_ON + '''    gsap.set(["#hi-t1", "#hi-t2", "#hi-t3"], { opacity: 0, filter: "blur(10px)" });
    const tl = gsap.timeline({ paused: true });
    // host starts 26.32 s: back to question 1
    tl.to("#hi-t1", { opacity: 1, filter: "blur(0px)", duration: 0.35, ease: "power3.out" }, 0.05);
    tl.to("#hi-t1", { opacity: 0, filter: "blur(10px)", duration: 0.25, ease: "power3.in" }, 3.6);
    // the answer, part 1: the homepage folds back into its own source (strong cue 30.17 s)
    FLY.forEach(([sel, dy, d]) => {
      tl.to(sel, { y: dy, x: -140, scale: 0.55, opacity: 0, filter: "blur(10px)", duration: 0.5, ease: "power3.in" }, 3.85 + d * 0.6);
    });
    tl.to("#sc-hero", { opacity: 0, duration: 0.5, ease: "power2.in" }, 3.9);
    tl.fromTo("#sc-ed", { opacity: 0, scale: 0.96, filter: "blur(8px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.6, ease: "expo.out" }, 4.05);
    tl.fromTo(".ln", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.4, ease: "power3.out", stagger: 0.025 }, 4.15);
    tl.set("#sc-cur", { x: LEFT + CW * 46, y: 676 + 37 * 16 + 4 }, 4.6);
    tl.to("#sc-cur", { opacity: 1, duration: 0.1 }, 4.7);
    tl.to("#hi-t2", { opacity: 1, filter: "blur(0px)", duration: 0.35, ease: "power3.out" }, 4.15);
    tl.to("#hi-t2", { opacity: 0, filter: "blur(10px)", duration: 0.25, ease: "power3.in" }, 6.2);
    // part 2: and it compiles back into the page (strong cue 32.74 s)
    tl.to("#sc-cur", { opacity: 0, duration: 0.1 }, 6.38);
    tl.to(".ln", { opacity: 0, filter: "blur(8px)", duration: 0.35, ease: "power3.in", stagger: 0.012 }, 6.4);
    tl.to("#sc-ed", { opacity: 0, scale: 0.96, filter: "blur(8px)", duration: 0.45, ease: "power3.in" }, 6.44);
    tl.to("#sc-hero", { opacity: 1, duration: 0.6, ease: "power2.out" }, 6.55);
    FLY.forEach(([sel, , d]) => {
      tl.to(sel, { y: 0, x: 0, scale: 1, opacity: 1, filter: "blur(0px)", duration: 0.7, ease: "expo.out" }, 6.42 + d); // beat-locked: 32.74s
    });
    tl.to("#hi-t3", { opacity: 1, filter: "blur(0px)", duration: 0.35, ease: "power3.out" }, 6.7);
    tl.to(["#hi-t3", ".r", ".btn", "#sc-hero"], { opacity: 0, filter: "blur(10px)", duration: 0.25, ease: "power3.in" }, 8.6);
'''),
}
for mid, m in modes.items():
    s = base.replace("__TITLES__", m["titles"]).replace("__TIMELINE__", m["tl"]).replace("__ID", mid).replace("__DUR", str(m["dur"]))
    open(os.path.join(HERE, "..", "compositions", mid + ".html"), "w").write(s)
print("ok")
