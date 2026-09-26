# DevEraXTech brand reel

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

The video has no audio track; add music in any editor.
