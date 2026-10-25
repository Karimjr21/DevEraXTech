# Brag Plan: DevEraXTech — "Source" (film 3)

/brag full workflow + Hyperframes 0.8.190. Provisional; not approved for publication.

## The angle
Every pixel starts as code. DevEraXTech's own homepage source (`frontend/pages/Home.jsx`, hero section, trimmed and re-wrapped) types itself in an editor. On the strong beat the code lets go and each line turns into the element it renders on deveraxtech.com. The film then walks through the studio's real process and promises, and the brand itself compiles from `<DevEraXTech />`.

## Different from film 1 and film 2
| | Film 1 "Engineered Excellence" | Film 2 "One Line" | Film 3 "Source" |
|---|---|---|---|
| Subject | A client build (Nilora) | The service range | DevEraXTech's own code, process and promises |
| Look | Photo-real UI, 3D layers | Gold line-art oner | Editorial type + code editor, rolling Playfair numerals |
| Music | Vol. 12, ~110 BPM | Vol. 1, 120 BPM | Vol. 11, 114.8 BPM |
| Payoff | Screens align on a seam | Ring terminal flies into the logo | `<DevEraXTech />` compiles into the logo |

## Grounding (all from the DevEraXTech repo)
- Code: `Home.jsx` hero — eyebrow "ENGINEERED EXCELLENCE", h1 "We build premium web &amp; app experiences" (the literal `&amp;` is in the source), "Modern, secure and scalable solutions, from prototypes to production.", `AnimatedButton` "Request a Meeting" / "View Our Services", "Secure • Scalable • Pixel-perfect". Class names are trimmed from the real ones (`gold-gradient-text`, `text-gray-300`).
- Rendered hero: the same copy, the site's gold gradient (`--gold-gradient-text`), the gold button gradient, a star field like the site's hero.
- Process: Home "How It Works · From first call to launch": Discovery call. / Plan and design. / Build, secure and launch. Descriptions shortened from the site's own sentences.
- Promises: Home "Why clients choose DevEraXTech": the four titles verbatim.
- Invented framing (no claims): "Every pixel starts as code." · "This is our homepage." (it is) · the `// design` comments · `<DevEraXTech />`.

## Storyboard — 20.0 s · 600 f · 1080×1920 · 30 fps
| Time | Beat |
|---|---|
| 0–3.6 | EVERY PIXEL / STARTS AS CODE. Editor "Home.jsx", 17 lines type out with a caret (3 lines already typed at frame 0) |
| 3.70 | Strong cue: the code dissolves; each line flies out and lands as its rendered element |
| 3.9–7.8 | THIS IS OUR / HOMEPAGE. The live hero holds; the site's gold sheen crosses the headline once |
| 7.87–14.14 | FROM FIRST CALL / TO LAUNCH. One step per bar: an italic Playfair numeral rolls 01→02→03, a progress trace with a ring terminal fills a third per step |
| 14.14–17.0 | WHY / DEVERAXTECH. Four promises land on the beat grid |
| 16.8–20.0 | `<DevEraXTech />` types, the brackets fly off, the name becomes the gold wordmark, and the logo irises open on the beat (17.275 s) with the three-note signature. ENGINEERED EXCELLENCE · deveraxtech.com held ≥ 2.3 s |

## Audio
Music: "Happy Beats / Business Moves Vol. 11", Sascha Ende, ende.app, **CC BY 4.0 (credit required)**. SFX (CC0 Kenney): a keypress at each typed line, a card slide + soft impact on the compile, a chip on each step, drops on each promise, keys on `<DevEraXTech />`. Sonic signature (shared with films 1 and 2): one note at the start, all three on the logo.

## Verified
`hyperframes check` passed (0 errors, 64 text elements contrast-checked). Encoded file: H.264 High@4.0, 1080×1920, 30 fps, 600 frames, 20.000 s, BT.709, AAC 48 kHz, −14.0 LUFS, −2.2 dBFS peak; poster (t = 4.8 s, the rendered homepage) baked into frame 0. Sound measured, not heard.
Kept warnings: editor code is 26 px (texture, but legible at full screen); the 4th promise reads for 1.2 s.
