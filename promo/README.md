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
