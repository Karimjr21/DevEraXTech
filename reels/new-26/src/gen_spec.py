"""Writes ../reels-spec.md from the metadata that sits next to each scene's code (single source of truth)."""
import json
import os

import dx
from scenes import REELS

OUT = os.path.normpath(os.path.join(dx.HERE, ".."))
qc_path = os.path.join(OUT, "qc", "qc-report.json")
qc = {r["n"]: r for r in json.load(open(qc_path))} if os.path.exists(qc_path) else {}

L = ["# DeveraXTech: 26 new reels, spec", "",
     "Every reel is 1080x1920, 30 fps, H.264 + AAC, rendered from code in `src/` (`python3 render.py`).",
     "Frame 0 is the cover PNG in `covers/`. Text stays inside x 80–940, y 220–1540 (clear of the top 220 px,",
     "bottom 380 px and right 140 px). The DeveraXTech name and logo appear only on the end cards (10.0 s or",
     "later) and in reel 15's signed line (11.6 s). 'Our build' cameos start at 7.8 s at the earliest.", "",
     "All sound is synthesised in `src/sfx.py` (no licensed music). There is no voice-over: the on-screen",
     "text carries every reel, so they work muted.", "",
     "Portfolio cameos are real DeveraXTech builds, renamed where a person's name was in the project:",
     "the Barhouma site appears as 'IGCSE Maths platform', the Sarah site as 'CalmCare Therapy Center',",
     "and the developer portfolio is shown as it is.", "",
     "## At a glance", "",
     "| # | File | Length | Hook type | Industry | Opening sound | CTA keyword |",
     "|---|------|--------|-----------|----------|---------------|-------------|"]
for n, r in sorted(REELS.items()):
    m = r.meta
    snd = m["sound"].split(";")[0].replace("0.00 ", "")
    kw = m["cta"].split("DM ")[-1].split(" ")[0] if "DM" in m["cta"] else m["cta"]
    if n == 15:
        kw = "'THIS MONTH' (reply)"
    if n == 26:
        kw = "'ابدأ' / START"
    L.append(f"| {n} | `dxt-new-{n:02d}-{r.slug}.mp4` | {r.dur:.0f} s | {m['type']} | {m['industry']} | {snd} | {kw} |")
L.append("")

for n, r in sorted(REELS.items()):
    m = r.meta
    L += [f"## {n:02d}. {m['type']}: {m['industry']}", "",
          f"- **File:** `dxt-new-{n:02d}-{r.slug}.mp4`, cover `covers/dxt-new-{n:02d}-{r.slug}.png`, {r.dur:.0f} s",
          f"- **Palette:** {m['palette']}",
          f"- **Hook (frame 0):** {m['hook']}",
          f"- **CTA (final 2 s):** {m['cta']}", "",
          "| Time (s) | What happens |", "|---|---|"]
    for t, b in m["beats"]:
        L.append(f"| {t} | {b} |")
    L += ["", f"**Sound design:** {m['sound']}", "", f"**Why it should stop the scroll:** {m['why']}", ""]
    if m.get("placeholders"):
        L.append("**For Karim to fill or confirm:** " + "; ".join(m["placeholders"]))
        L.append("")
    if n in qc:
        q = qc[n]
        L.append(f"**QC:** {q['w']}x{q['h']}, {q['fps']} fps, {q['vcodec']}/{q['acodec']}, {q['dur']} s; loudest peak in the "
                 f"first 100 ms ({q['peak_first_100ms_db']} dBFS); {q['pixels_changed_0_to_1s_pct']}% of pixels change "
                 f"between 0.0 s and 1.0 s; hook {q['hook_words']} words. {'Pass' if q['pass'] else 'FAIL'}.")
        L.append("")

L += ["## Placeholders and claims to confirm", ""]
for n, r in sorted(REELS.items()):
    for p in r.meta.get("placeholders", []):
        L.append(f"- Reel {n:02d}: {p}")
L += ["", "Every other statement is a general observation or opinion (labelled as such in reels 16 and 25).",
      "No statistics, client names, results, testimonials or prices are invented. The only figures used are",
      "Apple's published 44 pt minimum tap target (reel 24) and Nielsen Norman Group's 10–20 seconds (reel 22),",
      "both cited on screen. Reel 12's counter is labelled 'illustrative, not real data' on screen.", "",
      "## Arabic (reel 26)", "",
      "Arabic is set in Cairo and shaped by HarfBuzz with FriBiDi (Pillow's libraqm layout, direction rtl),",
      "so letters join and run right to left. arabic-reshaper + python-bidi was tried first, but it maps letters",
      "to Unicode presentation forms that the web-subset Cairo font does not contain (every letter came out as a",
      "box), so the full shaping engine is used instead. Checked visually on frames 0, 3, 8 and 13 s.", ""]
open(os.path.join(OUT, "reels-spec.md"), "w").write("\n".join(L))
print("wrote reels-spec.md")
