# Hyperframes Composition Brief: DevEraXTech TikTok

## Objective
A luxurious vertical brand-awareness TikTok for DevEraXTech: 3 hooks, 3 trending tech questions, and
Q1's answer withheld until the end behind an always-climbing answer meter.

## Output
- Composition directory: `brag-output/composition/`
- Rendered video: `brag-output/brag.mp4`
- Format: vertical, 1080x1920, 30fps
- Duration: 40s (the user's brief overrides the 15–25s brag window; see brag-plan.md)

## Source Material
- Project root: repo root; files read: frontend/index.html, pages/Home.jsx, tailwind.config.js,
  src/data/services.json, src/data/portfolio.json, src/data/business.json
- Copy that must appear verbatim: "We build premium web & app experiences", "Premium design, not
  templates", "Secure · Scalable · Pixel-perfect", service items "Website chatbots", "WhatsApp
  assistants", "Automated lead capture", "Core Web Vitals", "Schema markup", Nilora's "Where the river
  meets the light."
- Assets: frontend/public/assets/deveraxtech-logo.png, frontend/public/work/nilora-estates-real-estate-website.webp

## Creative Direction
- Tone: cinematic with polished restraint: a luxury watch-commercial grammar
- Hooks, questions, payoff, outro: see brag-plan.md storyboard (the contract)
- Avoid: generic SaaS language, invented stats/numbers about the studio, bounce, breathing titles

## Visual Identity
- Background #0a0a0a; accent #d4af37; gradient #d4af37/#f5d573; text #ffffff, #d1d5db
- Display: Playfair Display (bundled); body: Inter (bundled)
- Keep key text inside x 90–940, y 260–1400 (TikTok UI safe)

## Audio
- Music: assets/music/happy-beats-business-moves-vol-12-by-ende-dot-app.mp3 at 0.32, fade-out 3s
- Cue source: brag/assets/music/cues/happy-beats-business-moves-vol-12-by-ende-dot-app.music-cues.json
- Audio-reactive: subtle, bass to the ambient gold glow
- SFX: impact/impactBell_heavy_000 (hook word, "No."), impact/impactSoft_medium_* (question arrivals),
  impact/impactGlass_light_* (answer chips/pass rows), interface/glitch_004 (meter stall),
  casino/dice-shake-1 (tension), impact/impactBell_heavy_003 (logo)

## Hyperframes Instructions
Standard brag handoff: the hyperframes contract, registry, media-use and cli. `check` is the gate. Render locally.
