# DevEraXTech: *Engineered Excellence* QC report

Film: 36.000 s · 9:16 · 2160 frames · rendered natively at 1080 × 1920, 60 fps progressive · stereo, 48 kHz

## 1. What was actually used, and what was not

| Item | Status |
|---|---|
| **Full Brag skill** | **Not available in this environment.** No skill by that name exists here, and none was run. Nothing in this film or this report claims its execution. |
| **Hyper Frame skill** | **Not available in this environment.** None was run. The frame-level checks below were done with this project's own tools (`tools/qc.py`, review stills, contact sheets). |
| Generative video / image models | Not used. Every frame is rendered deterministically by Three.js (WebGL, SwiftShader software renderer) in headless Chromium. |
| Stock footage, stock music, third-party SFX | None. All audio is synthesized in `tools/audio.py` from oscillators, noise and filters. It is original, with no licensing dependency. |
| Official brand assets | `frontend/public/assets/deveraxtech-logo.png`, unmodified, composited 1:1 (only transparent padding is trimmed). Inter Display (the site typeface, SIL OFL). |

## 2. Specification vs. delivered: honest gaps

| Brief | Delivered | Why |
|---|---|---|
| 4320 × 7680 (8K) master | **1080 × 1920 native.** No 8K file, and no upscaled file labelled 8K | This environment has no GPU. Software WebGL took about 3.8 s per 1080p frame on 3 workers, which makes an 8K render of 2160 frames (16× the pixels) impractical here. The renderer is resolution-independent (`?w=4320&h=7680`), so a genuine 8K render is possible on GPU hardware. Fixed-size elements (particle point sizes, texture resolutions) would need checking at that scale. |
| 120 fps slow-motion acquisition | Not applicable | Nothing is filmed. Slow motion is designed into the simulation instead (e.g. the Scene 01 shatter uses a time remap: violent first instant, then slow motion). The renderer can output any frame rate. |
| Scene-linear workflow, HDR highlights | Linear-light rendering (half-float buffers), ACES filmic tone mapping, sRGB / BT.709 SDR delivery | No HDR (PQ/HLG) deliverable is produced. |
| Motion blur | **Not rendered** (0° shutter) | Accumulation blur would multiply render time 2–4×. Fast motion was choreographed to avoid strobing instead, and no frame-to-frame pops remain (section 4). This is the main item to add on GPU hardware. |
| Shallow depth of field | **Not optically simulated** | Depth is carried by fog, particle size and lighting. Three.js's bokeh pass produced ring artefacts in tests, so it was not used. |
| Professionally mastered stereo | Mastered to −14 LUFS integrated, −1.5 dBTP ceiling (section 5) | **The mix has not been listened to.** I can't hear audio. It was checked only by spectrogram, loudness, peak and phone-speaker-band measurements. A human listening pass on studio monitors **and** phone speakers is required before release. |
| Highest-quality master | `master/…_master.mov`: H.264 High, CRF 8, 1080p60, 24-bit PCM, about 250 MB | Not committed to git (GitHub's 100 MB file limit). It, and the lossless PNG frames, are re-creatable bit-for-bit from the source in this folder (see README). |

## 3. Scene-by-scene checks

Each scene was rendered on its own as review stills, inspected, and corrected before the final render. Fixes made during QC are listed.

| Scene | Checks | Result / fixes made |
|---|---|---|
| 01 Pattern interrupt | Fracture lines = crack lines (same geometry); one fragment survives; text legibility over debris | Pass. Fixes: reframed so the slab reads as an object in black; screen fragments go dark after impact; slowed debris (it was leaving frame in 0.15 s); **a one-frame glare at 2.42 s regenerated** (radiance clamp plus near-lens silhouetting); scrim behind type. |
| 02 New standard | Continuous blob → portal morph, no tearing; clockwise orbit; fly-through | Pass. Fixes: chrome environment so chrome reads as chrome; floor glare removed. A 0.2 s pass through darkness (5.87–6.05 s) is intentional: it is the camera inside the portal. |
| 03 Not just designed | Original concept site (labelled *Concept*); modules land on grid; parallax dolly | Pass. Fix: dolly distance so the whole site reads before the push-through. |
| 04 Engineered | Traces, pads, vias, pulses coherent; a single signal draws the phone outline | Pass. Fix: pulse brightness and bloom reduced. |
| 05 Beyond the screen | Phone from the outline (matched framing); app → store (swap hidden at the back of the turn) → dashboard | Pass. Fixes: a store → dashboard **blank-screen cut replaced with a dissolve**; the push-in no longer over-magnifies the screen texture (pixelation removed). |
| 06 Built to think bigger | Strands from the dashboard graph; portal arcade from 02; wide → macro | Pass. Fixes: strands reorganised into four calm bundles (they read as tangled); white-out at the convergence removed. |
| 07 Every pixel | Three macros with match cuts; three clicks at 20.74 / 21.98 / 23.2 s | Pass. Fixes: macro A reframed so two components read; the glint light that caused bloom flashes in B removed; grid C misalignment visible before the snap. |
| 08 Values | Monoliths rise from below the floor (clip planes, no intersection); planar reflections; converge | Pass. Fixes: black glass readable against a graphite backdrop; floor seams continue 07's grid; the move ends on the blank black face. |
| 09 Reveal | Particles sample the official logo's own pixels; exact hand-over to the artwork | Pass. The bounding box of the particle mark matches the composited PNG (verified numerically). Fixes: colour pipeline (sRGB → linear) so particles match the artwork; obsidian background. |
| 10 Memory anchor | Logo + typeset wordmark + tagline + URL; one silver reflection; loop state | Pass. Ends on obsidian with no logo, the state the loop returns from; the hard cut back to frame 0 lands on silence. |

**Typography:** all type is set in 2D from Inter Display, so spelling is exact. Copy as briefed: THE INTERNET DOESN'T NEED ANOTHER WEBSITE. · IT NEEDS A NEW STANDARD. · NOT JUST DESIGNED. · ENGINEERED. · BEYOND THE SCREEN. · BUILT TO THINK BIGGER. · EVERY PIXEL. EVERY DETAIL. · SECURE. SCALABLE. PIXEL-PERFECT. · DevEraXTech · ENGINEERED EXCELLENCE. · deveraxtech.com

**Safe zones:** every headline sits inside x 100–940, y 260–1480 (of 1080 × 1920), clear of TikTok and Reels UI. The brand lock-up is centred and ends above y ≈ 1340.

**Brand integrity:** the logo is never redrawn, recoloured, distorted or generated. Gold appears only with the brand, matching the official identity (`#d4af37` gradient). The world palette is obsidian #08090B, graphite #17191D, titanium #B9BEC5, platinum #E9ECEF and a restrained #8EA6BF.

**Claims audit:** no clients, case studies, awards, metrics, prices or CTAs. Interfaces are labelled *Concept*; the product is "Object 01 · Concept". There is no meeting, subscription or discount language.

## 4. Automated temporal QC (`tools/qc.py`, final 1080p frames)

`out/qc_main.csv` / `.png`: per-frame luma, frame difference and clipping for all 2160 frames.

- Pops / flicker outside intended cuts: **0 defects.** Two flags at 22.83 s are the intended onset of the grid snap (difference 0.023, the detector's floor).
- Black frames: 12 at 5.87–6.05 s (the portal fly-through, intentional) and 1 at 28.05 s (Scene 08's "empty black space", intentional).
- Highlight clipping above 4 % of frame: none flagged.
- Alt openings (shock, curiosity): 0 flags, 0 black frames.

## 5. Audio

| File | Integrated | True peak |
|---|---|---|
| 36 s music + SFX | −13.9 LUFS | −1.3 dBTP |
| 36 s SFX only | −14.7 LUFS | −1.2 dBTP |
| 15 s cut | −14.0 LUFS | −1.5 dBTP |
| 6 s sonic identity | −14.0 LUFS | −1.5 dBTP |

- **Structure (as briefed):** 0–3 near-silence → fracture impact → glass rain → riser; 3–9 sub swell, metal resonance, heartbeat pulse, interface micro-clicks; 9–20 impact then a 120 BPM electronic section (i–VI–III–VII in D minor), with the arpeggio accelerating 12–16 and granular grains 16–20; 20–28 three tactile clicks, taiko ostinato, string ostinato, monolith impacts, convergence hit, reverse swell; 28–33 particle shimmer into the sonic logo; 33–36 echo and fade to silence.
- **Sonic logo:** three FM "titanium bell" notes, D5 · A5 · E6 (a rising fifth, then a ninth) on eighth notes at 30.30 / 30.55 / 30.80 s, over a D1 sub impact. A soft echo an octave lower plays at 34.2 s with the silver reflection.
- **Small-speaker translation:** the sub band is partly converted into harmonics (130–700 Hz) so impacts still register on phones. With a 300 Hz high-pass, the mix measures about 6 LU below full-band.
- **Sync:** every event time in `tools/audio.py` is mirrored from the scene constants (`S03_LANDINGS`, `S07_CLICKS`, `S08_RISES`, `LOCK`, `SHEEN`).
- **Muted-safe version:** a silent stereo track with all text overlays intact.

## 6. Deliverables

| # | Brief item | File(s) |
|---|---|---|
| 1 | Main 36 s vertical film | `tiktok/…_36s_tiktok_60p_music.mp4`, `instagram/…_36s_instagram_30p_music.mp4` |
| 2 | Alt opening: shock (titanium slug fired through the slab, fracture at 0.32 s) | `openings/…_alt-opening-shock_3s_60p.mp4` + full 36 s version |
| 3 | Alt opening: curiosity (opens on an abstract crystal surface, reveal, fracture at 1.9 s) | `openings/…_alt-opening-curiosity_3s_60p.mp4` + full 36 s version |
| 4 | 15 s cut (0–6, 24.3–28, 29–31.3, 33–36) | `tiktok/…_15s_…`, `instagram/…_15s_…` |
| 5 | 6 s logo + sonic identity (30–36) | `tiktok/…_06s_…`, `instagram/…_06s_…` |
| 6 | Platform exports | TikTok 1080p60 H.264 High, ~12 Mbps cap, AAC 320k; Instagram 1080p30 H.264 High, ~8 Mbps cap, AAC 256k; all −14 LUFS, faststart |
| — | Music / SFX-only / muted-safe | `…_music.mp4`, `…_sfx-only.mp4`, `…_muted-safe.mp4` (both platforms) |
| 7 | Highest-quality master | `master/…_master.mov` (local only, see §2) and `…_review_540x960.mp4` |
| 8 | Thumbnails | `thumbnails/clean_*.jpg` (10 text-free plates), `thumbnails/titled_*.jpg` (5) |
| 9 | Scene-level source | `src/scenes/s01…s10`; each scene renders on its own (`tools/still.cjs`, `tools/render.cjs`); stems in `audio/` |
| 10 | QC report | this file |

**Views:** one million views is an aspiration, not a forecast. Nothing here guarantees reach.
