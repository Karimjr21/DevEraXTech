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

## 3–9. Seven more vertical reels (9:16, 24 s), each with its own look and sound

No two reels share a visual world, transition style, closing card or music genre. The only shared code is the
timing helpers in `kit/`; each reel switches off the kit's default chrome (`look: {...}` in its `kit.setup`) and
draws its own.

| File | Hook | Visual world | Transitions | Music (`soundtrack.py` style) |
|---|---|---|---|---|
| `deveraxtech-them-vs-us.mp4` | "Your competitors don't want you to see this" | neon arcade fighting game: synthwave sun, neon grid floor, CRT scanlines, health bars, "FIGHT! / K.O. / CONTINUE?" | pixel-block dissolves | 8-bit chiptune, 150 BPM (`chiptune`) |
| `deveraxtech-rate-this.mp4` | "Rate this website." ★ 1–10 | cinema: letterbox, timecode, teal/amber grade, serif italics, film-credit roll, "A production by" card | slow dissolves + light leaks | trailer score: braams, taiko, strings, piano, 60 BPM (`cinematic`) |
| `deveraxtech-money-signs.mp4` | "3 signs your website is costing you money" | breaking news: LIVE bug, hazard stripes, scrolling ticker, pulsing alarm edge, headline-card CTA | RGB-split glitch cuts | dark trap: 808 glides, hat rolls, bells, sirens, 150 BPM half-time (`trap`) |
| `deveraxtech-glow-up.mp4` | "Watch this website glow up ✨" | a 90s desktop (teal wallpaper, grey windows, error dialogs, taskbar) → a luxury serif world framed in gold | CRT switch-off, gold wipe, before/after slider | cheesy retro MIDI → future-bass drop (`glowup`) |
| `deveraxtech-process.mp4` | "Hiring a web studio shouldn't feel like a gamble" | navy blueprint grid, outlined numerals, drafting title block, spec sheet, APPROVED stamp | calm slide-ups, drawn dimension lines, no shake | lo-fi chillhop: swung drums, Rhodes, vinyl crackle, tape wobble, 90 BPM (`lofi`) |
| `deveraxtech-worldwide.mp4` | "A studio in Cairo. Serving 7 countries." | airport departures: split-flap board, night-sky globe with arcs from Cairo, boarding-pass CTA | flap flips | Arabic: darbuka maqsum, riq, oud and qanun in maqam Hijaz, 120 BPM (`arabic`) |
| `deveraxtech-whats-included.mp4` | "What you actually get when you hire us 👇" | the one light reel: cream paper, white cards, brand confetti, unboxed counter, gift-tag CTA | springy bounces | funk-pop: slap bass, clav, brass stabs, marimba, shakers, 120 BPM (`funk`) |

`soundtrack.py` is a small numpy synth (mixer with buses, sidechain and convolution reverb; Karplus-Strong strings for
oud, qanun and slap bass; bit-crushed 8-bit voices; 808s with glide; tape wobble and vinyl crackle). Each reel's cue
list places sound effects on that reel's cuts.

```bash
for r in them-vs-us rate-this money-signs glow-up process worldwide whats-included; do
  python3 soundtrack.py $r $r-audio.wav
  node render.mjs deveraxtech-$r.mp4 --page $r.html --audio $r-audio.wav
done
```

## 10–19. Ten more vertical reels, second batch (9:16, 21–24 s)

Each has its own hook format, visual world, display typeface and music genre (none repeat the first batch). Scene
cuts are timed in beats of each reel's own tempo, and `soundtrack2.py` places its cues on the same beats.

| File | Hook | Visual world | Music (`soundtrack2.py`) |
|---|---|---|---|
| `deveraxtech-dm-chat.mp4` | "POV: you asked 3 agencies for a website 😬" | dark chat app: left on seen, "we'll use a template 👍", then DevEraXTech replies | UK garage 2-step, 132 |
| `deveraxtech-spy-dossier.mp4` | "CLASSIFIED FILE Nº 0127" | desk + typewriter file, manila folder, redaction bar, evidence board with red string, threat gauge | 60s spy surf, 120 |
| `deveraxtech-nature-doc.mp4` | "Here, in Cairo… we observe something rare." | wildlife documentary: binoculars, field notebook, herd of templates, subtitles | documentary orchestra, 84 |
| `deveraxtech-player-card.mp4` | "Rating our web studio like a football player ⚽" | stadium floodlights, pack-opening walkout, gold 99 card (self-rated), broadcast stat bars | stadium stomp anthem, 80 |
| `deveraxtech-recipe.mp4` | "The recipe for a website that sells 🍳" | marble counter, handwritten recipe card, mixing bowl, oven timer, cloche reveal | bossa nova, 126 |
| `deveraxtech-terminal.mp4` | `❯ why is my website so slow?` | a full-screen shell session: errors, `npx deveraxtech --premium`, build log, BUILD SUCCEEDED | drum & bass, 174 |
| `deveraxtech-tarot.mp4` | "Let's read your website's fortune" | velvet, candles, crystal ball; The Past / The Present / The Future cards | ethereal harp + choir, 70 |
| `deveraxtech-western.mp4` | "This town ain't big enough for two websites 🤠" | sepia desert, WANTED poster, high-noon showdown, sheriff badge | spaghetti western, 96 |
| `deveraxtech-quest.mp4` | "⚔️ New quest unlocked" | parchment map, hero card, skill tree, legendary loot, level-up | celtic jig in 6/8 |
| `deveraxtech-dating.mp4` | "Swipe right on your next web studio 💘" | a fictional swipe app ("Studio Match"): nope, nope, like, it's a match | nu-disco, 118 |

Display faces live in `assets/fonts/` (`kit/fonts2.css`): Bebas Neue, Cinzel Decorative, MedievalSharp, Patrick Hand,
Rye, Caveat, Fredoka (SIL OFL) and Special Elite (Apache 2.0).

```bash
for r in dm-chat spy-dossier nature-doc player-card recipe terminal tarot western quest dating; do
  python3 soundtrack2.py $r $r-audio.wav
  node render.mjs deveraxtech-$r.mp4 --page $r.html --audio $r-audio.wav
done
```
