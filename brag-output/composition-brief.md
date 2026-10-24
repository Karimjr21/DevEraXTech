# Hyperframes Composition Brief: DevEraXTech — "Beautiful isn't enough. It must be engineered."

## Objective
Make a 20-second luxury cinematic brand-awareness film for DevEraXTech, built on its real Nilora Estates project.

## Output
- Composition directory: `brag-output/composition/`
- Rendered video: `brag-output/brag.mp4`
- Format: vertical, 1080×1920, 30 fps, exactly 20.000 s (600 frames)

## Source material
- DevEraXTech site: `DevEraXTech/frontend` (index.html, tailwind.config.js, styles/global.css, pages/Home.jsx, src/data/*.json, public/assets/deveraxtech-logo.png)
- Nilora Estates: `Nilora-Estates/frontend/src` (index.css tokens, CinematicHero.jsx, ViewingForm.jsx, Account.jsx, pages/admin/AdminViewings.jsx, lib/format.js, lib/schemas.js) and `backend/src/seed/data/properties.json`
- Copy that must appear verbatim: "DevEraXTech" · "ENGINEERED EXCELLENCE" · "deveraxtech.com" · "Where the river meets the light." · "Villa Amara" · "EGP 86,500,000" · "Request viewing" · "Your viewing is requested" · "Viewing requests" · "Pending" / "Confirmed"
- Campaign copy (brief): "LOOKS EFFORTLESS." · "EVERY DETAIL IS ENGINEERED."

## Creative direction
- Tone: `cinematic`, restrained toward `polished`. Precision digital luxury.
- Angle, hook, outro, storyboard: see `brag-plan.md`.
- Avoid: generic SaaS language, abstract filler, metrics, testimonials, fake errors, cracks, shards, particles, sparks, lens flares, orbits.

## Visual identity
- Ground `#0a0a0a`; accent `#d4af37` / `#e6c45a` (text, AA-safe) / `#f2d17b`; ink `#f5f5f5`
- Display: Inter 800 uppercase (bundled); wordmark Inter 700 with the site's gold gradient
- Product UI: Nilora tokens, Cormorant Garamond + Inter Tight (`assets/fonts/`, OFL)
- Signature: Precision Seam = logo circuit trace + ring terminal

## Audio
- Bed: `assets/music/happy-beats-business-moves-vol-12-by-ende-dot-app.mp3` at 0.30, fade-out 1.2 s (credit: Sascha Ende, ende.app, CC BY 4.0)
- Cue source: bundled preset (`brag/assets/music/cues/…vol-12….music-cues.json`), ≈110 BPM
- Beat locks: payoff seam lands **13.11 s** (strong cue); logo lands **17.47 s** (strong cue); alignment ticks on beat grid 13.65 / 14.20 / 14.73
- Sonic signature: `assets/sfx/sig-note.wav` (1 note, 0.32 s), `sig-two.wav` (13.11 s), `sig-full.wav` (17.45 s) — re-pitched CC0 Kenney glass tap (A4–E5–A5) + low bell
- SFX: CC0 Kenney (`impactSoft_medium`, `drop_00x`, `mouseclick1`, `click_003`, `card-slide-1`, `chip-lay-1`, `rollover2`), each at its visible action
- Audio-reactive: **not implemented**. The stage glow follows the edit's arc on the timeline instead. Reason: kept the render deterministic and simple; flagged as a next improvement.

## Hyperframes structure
- `index.html`: stage + glow, 5 scene hosts, all audio
- `compositions/reveal.html` (0–6 s): S1 + S2, one continuous object (CSS 3D exploded stack)
- `compositions/proof.html` (6–13 s): S3 website → phone → agent dashboard
- `compositions/payoff.html` (12.5–17 s): S4, overlaps S3 by 0.5 s for a seamless hand-off
- `compositions/brand.html` (17–20 s): S5 end card
- `compositions/brandcue.html` (0–17 s): persistent authentic brand row
- Gate: `npx hyperframes check` → passed (0 errors)
