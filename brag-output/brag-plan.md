# Brag Plan: DevEraXTech — "Beautiful isn't enough. It must be engineered."

Workflow: `/brag` full workflow (explicitly requested; brag-slim not used) → Hyperframes 0.8.190.
Status of every creative decision below: **provisional** (no human audience test was run; no brand-owner sign-off yet).

---

## A. Brand Truth Sheet (verified 2026-10-24)

| Field | Value | Source / status |
|---|---|---|
| Brand name | **DevEraXTech** | deveraxtech.com `<title>`, repo `DevEraXTech/frontend/index.html`, og-image. Verified. |
| Tagline | **ENGINEERED EXCELLENCE** | Live site hero supertitle (`pages/Home.jsx:135`); string present in live HTML. Verified. |
| Positioning line | "We build premium web & app experiences" / "Modern, secure and scalable solutions, from prototypes to production." | Home hero. Verified. |
| Services | Business websites, e-commerce, Shopify, WordPress, web apps (CRMs, booking, portals, dashboards), iOS/Android (React Native), Windows desktop, AI & payment integrations, maintenance & care plans | `src/data/services.json`, `faq.json`. Verified. |
| Logo | Gold "DX" monogram with circuit traces ending in ring terminals | `frontend/public/assets/deveraxtech-logo.png` (1536×1024 RGBA). Owner's own repo. Used unaltered (crop of transparent margin only, proportions preserved). |
| Colors | Ground `#0a0a0a`; gold `#d4af37`; gold soft `#f2d17b`; gold gradient `#b8912a → #d4af37 → #fff1bf → #f5d573 → #d4af37` | `styles/global.css`, `tailwind.config.js`. Verified. **The brief's provisional palette is overridden by these real values** (per brief §06). |
| Typography | Inter (sans/body, bold headings) + Playfair Display (display) | `tailwind.config.js`. Both are bundled in Hyperframes. Verified. |
| Distinctive assets | Logo circuit traces + ring terminals; gold-gradient wordmark; tracked uppercase gold supertitle; "Secure • Scalable • Pixel-perfect" triad | Site + og-image. |
| Portfolio (real) | **Nilora Estates** — luxury real-estate platform, Cairo, MERN; public site + user / agent / admin dashboards; "Role-based authentication and secure REST API" | `src/data/portfolio.json`; source repo `Nilora-Estates` (owner's). |
| Nilora UI tokens | base `#0b1216`, surface `#111b21`, ink `#ede6da`, muted `#9aa7ae`, accent `#c8a46b`, accent-2-soft `#8fbab7`; Cormorant Garamond + Inter Tight | `Nilora-Estates/frontend/src/index.css`. |
| Nilora real copy used | "Where the river meets the light." · "Private viewing" · "Villa Amara" · "New Cairo · Villa" · "EGP 86,500,000" · 5 bd / 6 ba / 620 m² · "Request viewing" · "Viewing requests" · statuses Pending → Confirmed · Account tab "Viewings" | `CinematicHero.jsx`, seed `properties.json`, `ViewingForm.jsx`, `AdminViewings.jsx`, `format.js`, `Account.jsx`. |
| Missing assets | Vector (SVG) logo; official brand guidelines PDF; official sonic identity; brand-approved photography | Not found. PNG logo is 1536 px — adequate for 1080-wide delivery. |
| Excluded (unverified) claims | "Trusted by startups & enterprises • 10+ projects shipped"; any client count, metric, award, testimonial | Present on site but not independently verifiable → **not used in the film**. |
| Fictional stand-ins | Visitor name in the agent table ("Private client"), viewing slot "Sat · 11:00" | Demo data, not a real customer. |

### Asset rights
- Logo, site copy, Nilora UI/copy: owner's own repositories (Karim / DevEraXTech).
- Photos: Unsplash IDs used by Nilora's own site (`1634154955216-0a8455e2fb15`, `1613490493576-7fde63acd811`, `1600607687939-ce8a6c25118c`) — Unsplash License (commercial use allowed, no attribution required).
- Fonts: Inter, Playfair Display (bundled, OFL); Cormorant Garamond, Inter Tight (Google Fonts, OFL) downloaded to `assets/fonts/`.
- Music: "Happy Beats / Business Moves Vol. 12" — Sascha Ende, ende.app, **CC BY 4.0 → credit required in the post caption** ("Music: Sascha Ende, ende.app (CC BY 4.0)").
- SFX: Kenney CC0 (bundled with /brag). Sonic signature built from CC0 glass-tap source, re-pitched (original arrangement; no exclusivity claimed).

---

## What is this?
DevEraXTech is a Cairo design-and-engineering studio. The film shows one of its real builds — Nilora Estates — and proves that the beautiful surface is a working, connected system underneath.

## The angle
Beautiful isn't enough. It must be engineered. We open on a gorgeous real website, slice it open along a seam drawn from the DevEraXTech logo's own circuit traces, and show the structure under it. Then we prove the structure matters: one tap on the real "Request viewing" button travels — as the same gold trace — from website to the buyer's phone to the agent's dashboard, where it is confirmed. Everything resolves into the logo whose traces drew the seam.

## Hook (0–2 s) — Hook A, Visual Contradiction
Frame 0: the Nilora Estates hero in a desktop window — Cairo Tower at dusk, "Where the river meets the light." — under the line **LOOKS EFFORTLESS.** and a small DevEraXTech brand row. At 0.33 s a gold seam with a ring terminal (logo geometry) draws across the page; at 0.8 s the page parts along it and the gold grid underneath shows through.

## Key moments
1. Exploded view: photo / type & components / layout grid / system layer separate in 3D. **EVERY DETAIL IS ENGINEERED.**
2. Re-hook (≈4.1 s): a trace drops from the real "Private viewing" button through every layer to the "Viewings" endpoint node.
3. Proof: cursor presses **Request viewing** on Villa Amara → the card carries to the phone ("Viewings · Pending") → the same row lands in the agent's **Viewing requests** → Confirm → **Confirmed**, and the phone flips to Confirmed too.
4. Payoff: website, phone and dashboard align on one gold seam; a reflection passes; stillness.

## Outro
The seam contracts into the logo. **DevEraXTech / ENGINEERED EXCELLENCE / deveraxtech.com**. No CTA.

## User flow worth showing
Residence page → Request viewing → appears in buyer's Viewings (Pending) → agent's Viewing requests → Confirm → Confirmed everywhere. (Real Nilora flow: `ViewingForm.jsx`, `Account.jsx`, `AdminViewings.jsx`.)

## Tone
- Preset: `cinematic` (mapped from the brief's "luxury cinematic"), restrained toward `polished`.
- Creative direction: precision digital luxury — international product-film restraint.
- Interpretation: few, deliberate moves; arrivals on long expo tails; dead-still titles; one hero per frame; stillness before the payoff.

## Format: vertical — 1080×1920, 30 fps, exactly 20.000 s (600 frames)

## Visual identity
- Ground `#0a0a0a` with local radial glows (no full-frame linear gradients — H.264 banding).
- Accent gold `#d4af37` / soft `#f2d17b`; ink `#f5f5f5`, muted `#a3a3a3`.
- Campaign display: Inter 800 uppercase (site headings are bold Inter); wordmark: Inter 700 gold gradient (matches og-image).
- Product UI: Nilora's own Cormorant Garamond + Inter Tight and Nilora tokens.

## Distinctive brand system
- **Visual signature — the Precision Seam**: a 2 px gold trace with a ring terminal, taken from the logo's circuit traces. Reveals (S1), connects (S2/S3), aligns (S4), becomes the logo (S5).
- **Motion signature**: reveal 0.45 s `expo.out` → align 0.35 s `power3.out` → still ≥ 0.4 s.
- **Type signature**: uppercase Inter 800, −0.02 em, two lines max, one gold word that carries meaning (ENGINEERED).
- **Sonic signature**: three rising glass taps (root–fifth–octave) — one note at the S1 seam, two at the S4 alignment, all three on the logo at 17.47 s.
- **Composition signature**: one product on a dark stage, warm top-left key, floor reflection below 1330 px, gold hairlines only where they mean structure.
- **Logo-swap test**: the seam *is* the logo's trace geometry and the product is DevEraXTech's own client build → swapping the logo breaks the film. Pass (self-assessed).

## Share copy (draft)
DevEraXTech. Engineered excellence. One tap on a Nilora Estates page, followed through the website, the phone and the agent's dashboard.

## Audio direction
- Role: cinematic support, restrained.
- Music: `happy-beats-business-moves-vol-12` ("steady and clean", ≈110 BPM) at ~0.30, fade out under the logo's last second.
- Music cue guidance: preset `assets/music/cues/…vol-12….music-cues.json`; strong cues used: **13.11 s** (alignment lock), **17.47 s** (logo landing). Beat grid ≈0.545 s; S4 alignment ticks on 13.11 / 13.64 / 14.20.
- Audio-reactive: subtle — music RMS lifts the stage back-glow only.
- SFX posture: sparse, motion-matched (seam, layer locks, click, card carry, confirm, three-note sonic).
- Restraint: no booms, no whoosh on every cut, nothing under 150 Hz carrying meaning.

## Storyboard

### Scene 1 — The impossible first impression — 0.000–2.000 s (f000–059)
Nilora hero in desktop window; brand row; LOOKS EFFORTLESS. Seam draws 0.33–0.80 s; page parts 0.80–1.25 s revealing gold layout grid; holds parted.
Sequential/interaction: seam draw → part. Audio: one glass tap at 0.33 s + soft impact at 0.8 s. Transition → S2: continuous (same object).

### Scene 2 — The engineering reveal — 2.000–6.000 s (f060–179)
Window tilts into isometric; 4 layers separate (photo · type & components · grid · system). EVERY DETAIL IS ENGINEERED. (2.4–5.7 s). 4.1 s: trace from "Private viewing" to "Viewings" node. 5.1–5.9 s: layers lock back flat into the window.
Audio: drop/lock ticks on layer separation and on lock-back. Transition → S3: blur swap inside the same window.

### Scene 3 — The proof of value — 6.000–13.000 s (f180–389)
Villa Amara residence page; cursor clicks Request viewing (7.2 s); card carries into phone (7.8–8.6 s) "Viewings · Pending"; row carries into agent "Viewing requests" (9.9–10.7 s); Confirm click (11.4 s) → Confirmed; phone returns beside it showing Confirmed (12.0 s).
Labels: WEBSITE / MOBILE / AGENT DASHBOARD (small, functional). Audio: click, card slide, chip/confirm accent.

### Scene 4 — The engineered payoff — 13.000–17.000 s (f390–509)
Website, phone, dashboard arrive; a gold seam crosses; all three Villa Amara rows lock to it (13.11 / 13.64 / 14.20); reflection 14.7–15.5; stillness to 16.2; everything folds into the seam by 17.0.
Audio: two-note sonic + ticks.

### Scene 5 — The unmistakable brand — 17.000–20.000 s (f510–599)
Seam lifts into the logo (lands 17.47 s on strong cue); DevEraXTech wordmark, ENGINEERED EXCELLENCE, deveraxtech.com. Identity fully readable 17.9–20.0 s (2.1 s).
Audio: full three-note sonic on 17.47 s; music fades 19.0–20.0.

**Music mood:** cinematic-steady. **Audio summary:** a single tactile note opens, the bed builds through the demo, ticks lock the payoff, and the three-note signature lands the logo.

---

## Hook competition (Phase C)
Three ~2.5 s prototypes are built from the same assets in `hooks/` (A Visual Contradiction, B Intellectual Curiosity "WHAT MAKES IT WORK?", C Satisfying Precision "EVERY DETAIL MATTERS."). Evaluation is an **expert self-assessment only** — see `hooks/HOOK-EVALUATION.md`. No viewer data exists.

## Creative risk register
| Risk | Mitigation |
|---|---|
| Tiny in-window UI text unreadable on phone | Hero lines ≥ 40 px on screen; UI text treated as texture; key states (Pending/Confirmed) set ≥ 30 px with punch-in |
| 3D CSS exploded view flickers or sorts wrong | Explicit z-index per layer, no backface; fallback = 2D offset stack |
| Over-busy middle (3 devices) | One hero at a time in S3; all three only in S4 after viewer learned them |
| Music too "happy" for luxury | Low bed (0.28–0.32), sonic signature and SFX carry the character; swap track if owner prefers |
| Viewer reads Nilora as DevEraXTech's product | Small caption "NILORA ESTATES · BUILT BY DEVERAXTECH" in S3 |
| Claims | Only verified copy; no metrics |
