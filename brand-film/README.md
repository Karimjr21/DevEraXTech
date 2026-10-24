# DevEraXTech: *Engineered Excellence* brand film

A 36-second, 9:16 brand-awareness film for DevEraXTech. It has no CTA and no voice-over, and it is built to loop.

Every frame is rendered by code in this folder: Three.js scenes running in headless Chromium, composited deterministically in 2D. Every sound is synthesized from oscillators and noise in `tools/audio.py`. No generative video model, stock footage or third-party audio was used, so every shot can be re-rendered exactly, frame by frame.

## Structure

| Time | Scene | On-screen text | File |
|---|---|---|---|
| 00:00–00:03 | Pattern interrupt: a generic website frozen in a crystal slab shatters | THE INTERNET DOESN'T NEED ANOTHER WEBSITE. | `src/scenes/s01-interrupt.js` |
| 00:03–00:06 | The surviving fragment liquefies into a chrome portal | IT NEEDS A NEW STANDARD. | `s02-standard.js` |
| 00:06–00:09 | An original concept website assembles in glass architecture | NOT JUST DESIGNED. | `s03-design.js` |
| 00:09–00:12 | Metallic trace network beneath the interface; a signal draws a phone | ENGINEERED. | `s04-engineering.js` |
| 00:12–00:16 | Titanium phone: concept app → concept store → dashboard | BEYOND THE SCREEN. | `s05-ecosystem.js` |
| 00:16–00:20 | Illuminated strands through an arcade of portals, converging on a hub | BUILT TO THINK BIGGER. | `s06-intelligence.js` |
| 00:20–00:24 | Three macro details: shaft seats, glass edge catches light, grid snaps | EVERY PIXEL. EVERY DETAIL. | `s07-craft.js` |
| 00:24–00:28 | Three black-glass monoliths rise and converge | SECURE. · SCALABLE. · PIXEL-PERFECT. | `s08-values.js` |
| 00:28–00:33 | Metallic fragments aggregate onto the official mark; sonic logo | DevEraXTech | `s09-reveal.js` |
| 00:33–00:36 | Memory anchor; one silver reflection; resolves to obsidian | ENGINEERED EXCELLENCE. · deveraxtech.com | `s10-anchor.js` |

## Brand decisions

- **The logo is the official artwork** (`assets/brand/deveraxtech-logo.png`, copied unmodified from `frontend/public/assets/`). It is drawn 1:1, with only its transparent padding trimmed. The particle reveal samples the artwork's own pixels, so the hand-over to the real file is exact. Nothing generates or redraws the mark.
- **Palette:** the world is obsidian, graphite, titanium and platinum, per the brief. The official identity is gold (`#d4af37`, the site's gold gradient). Because the brief puts official assets first, gold appears only when the brand arrives: the mark, and a wordmark set in the site's own gold gradient. The whole film stays cold and metallic until that moment.
- **Typography** is Inter Display (the site's family, OFL licensed, bundled in `assets/fonts/`). All type is composited in 2D from real fonts, so spelling is exact.
- **No invented work:** every interface on screen is labelled *Concept*. There are no clients, metrics, awards or portfolio claims.

## Rendering

```bash
cd brand-film
npm install                      # three.js
pip install scipy numpy pillow   # audio + QC
python3 -m http.server 8765 &    # the renderer is served locally

# frames (lossless PNG), interleaved over N workers
node tools/render.cjs out/frames/main 1080 1920 main 0 2159 3 0 &
node tools/render.cjs out/frames/main 1080 1920 main 0 2159 3 1 &
node tools/render.cjs out/frames/main 1080 1920 main 0 2159 3 2 &
node tools/render.cjs out/frames/shock     1080 1920 shock     0 179
node tools/render.cjs out/frames/curiosity 1080 1920 curiosity 0 179

# audio stems per variant, then every edit, master and platform encode
python3 tools/audio.py out/audio/main main
python3 tools/audio.py out/audio/shock shock
python3 tools/audio.py out/audio/curiosity curiosity
python3 tools/deliver.py .

# QC and review stills
python3 tools/qc.py out/frames/main out/qc_main
node tools/still.cjs out/stills 1080 1920 main 1.4 5.3 8.2      # any timestamps
```

URL flags on `src/index.html`: `w`, `h`, `variant=main|shock|curiosity`, `notext=1` (clean plates for thumbnails).

The QC report is in `deliverables/QC_REPORT.md`.
