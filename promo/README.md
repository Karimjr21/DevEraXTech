# DevEraXTech promo videos

## 1. Brand reel (16:9, silent)

`deveraxtech-brand-reel.mp4`: a 38-second, 1920×1080 promo video built from the site's own brand assets:
the gold logo, Playfair Display / Inter, the dark-and-gold palette, the services, the Nilora Estates case study
and the business details from `frontend/src/data`.

- `reel.html`: the animated reel. Open it in a browser for a live, looping preview.
- `render.mjs`: renders it frame by frame with Playwright and encodes an H.264 MP4 with ffmpeg.
- `key-logo.mjs`: one-off script that cut `assets/logo.png` out of the logo's cream background.

```bash
cd promo
npm i -D playwright && pip install imageio-ffmpeg   # or set FFMPEG=/path/to/ffmpeg
node render.mjs                                      # -> deveraxtech-brand-reel.mp4
node render.mjs --stills 8.5,25 --dir /tmp           # PNG stills at given seconds
```

The brand reel has no audio track; add music in any editor.

## 2. Hook reel (9:16, with soundtrack)

`deveraxtech-hook-reel.mp4`: a 30-second vertical cut for Reels / TikTok / Shorts. It opens with a
scroll-stopping hook ("Stop scrolling", then a 3-second countdown), names the viewer's pain points, drops into the
brand on the beat, shows the Nilora Estates work, flips each pain point into a fix and ends on a call to action.
All cuts sit on a 120 BPM grid.

- `hook.html`: the animated vertical reel (live preview when opened in a browser).
- `make-hook-audio.py`: synthesises the matching soundtrack (tension build, riser, drop, beat with a pluck hook). Needs numpy.

```bash
python3 make-hook-audio.py hook-audio.wav
node render.mjs deveraxtech-hook-reel.mp4 --page hook.html --audio hook-audio.wav
```

### Arabic cut

`deveraxtech-hook-reel-ar.mp4` is the same reel in Arabic, laid out right-to-left with Arabic-Indic numerals, set in
Cairo (`assets/cairo-arabic.woff2`, SIL Open Font License). All copy for both languages lives in the `COPY` object in
`hook.html`; `?lang=ar` switches it.

```bash
node render.mjs deveraxtech-hook-reel-ar.mp4 --page "hook.html?lang=ar" --audio hook-audio.wav
```

## 3. "Them vs Us" (9:16, with soundtrack)

`deveraxtech-them-vs-us.mp4`, 24 s. Hook: "Your competitors don't want you to see this" + a CLASSIFIED stamp, a VS
face-off, then five rounds of other agencies (buzzer) vs DevEraXTech (gold slam + ding), a 0–5 scoreboard
and the call to action.

## 4. "Rate this website 1–10" (9:16, with soundtrack)

`deveraxtech-rate-this.mp4`, 24 s. Engagement hook with a filling 1–10 bar over a blurred teaser, then a cinematic
camera over the Nilora Estates build (hero, typography, details), laptop + phone, the feature list, "Built by
DevEraXTech" and "Your score? Want one like this?".

Both are built on the shared `kit/` (look, effects, beat camera) and `soundtrack.py`, which holds one cue
sheet per reel:

```bash
python3 soundtrack.py them-vs-us them-vs-us-audio.wav
node render.mjs deveraxtech-them-vs-us.mp4 --page them-vs-us.html --audio them-vs-us-audio.wav
python3 soundtrack.py rate-this rate-this-audio.wav
node render.mjs deveraxtech-rate-this.mp4 --page rate-this.html --audio rate-this-audio.wav
```

## 5–9. Five more vertical reels (9:16, 24 s, with soundtracks)

| File | Hook | Format |
|---|---|---|
| `deveraxtech-money-signs.mp4` | "3 signs your website is costing you money" | countdown listicle (#3 → #1), then "We fix all 3" |
| `deveraxtech-glow-up.mp4` | "Watch this website glow up ✨" | a dated template site vs the Nilora build: gold wipe on the drop, then a before/after slider |
| `deveraxtech-process.mp4` | "Hiring a web studio shouldn't feel like a gamble" | the 3-step process (call → plan & design → build, secure & launch) |
| `deveraxtech-worldwide.mp4` | "A studio in Cairo. Serving 7 countries. 🌍" | dotted globe (site's land dots) with arcs from Cairo, languages, opening hours |
| `deveraxtech-whats-included.mp4` | "What you actually get when you hire us 👇" | unboxing: items fly out of a gold box, "Not extras. The standard." |

```bash
for r in money-signs glow-up process worldwide whats-included; do
  python3 soundtrack.py $r $r-audio.wav
  node render.mjs deveraxtech-$r.mp4 --page $r.html --audio $r-audio.wav
done
```
