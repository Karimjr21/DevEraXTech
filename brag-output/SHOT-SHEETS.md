# Shot sheets & continuity spec — DevEraXTech flagship (20.000 s · 600 f · 1080×1920 · 30 fps)

## Shared continuity spec
- **Coordinate system**: canvas 1080×1920, origin top-left. Platform-safe text/product band 168–1330 px (no copy below 1330).
- **Brand row**: logo 96×67 + "DevEraXTech" 38 px, centred, top 186 px, f000–f509 (fades 16.55–16.85 s).
- **Campaign copy slot**: top 300 px, centred, Inter 800 uppercase.
- **Hero window**: left 60, top 610, 960×600 (40 px chrome + 960×560 viewport). Nilora page is 1440×840 at scale 0.6667.
- **Seam**: 4 px gold trace (`#d4af37 → #fff1bf → #f2d17b`) + 24 px ring terminal, 4 px `#f2d17b` stroke. S1 seam at window y 300 (canvas 910–930). S4 vertical at x 120, y 400–1180. S5 horizontal centred at (540, 975), 702 → 421 px.
- **Light**: one warm key (radial gold glow centred 50%/46%), secondary soft glow top-left. No lens flares, no full-frame linear gradients.
- **Motion signature**: reveal 0.45–0.47 s `expo.out` → align 0.35–0.40 s `power3.out/inOut` → still ≥ 0.4 s. Exits 0.18–0.3 s `power3.in` with 8–10 px blur.
- **Materials**: matte dark UI surfaces (`#0b1216`), gold hairlines, glass-free. No material changes mid-shot.

| Shot | Frames | Objective | Primary subject | Start → end frame | Camera | Motion / timing | Copy | Brand cues | Sound | Comp. method | Failure conditions | Fallback | Acceptance evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 Impossible first impression | 000–059 | Stop the scroll; read "website" | Nilora hero in desktop window | Full hero, copy settled → page parted ±30 px on the seam, grid visible | 1.000→1.035 push, no orbit | seam 0.33–0.80 s; part 0.80–1.25 s; hold | LOOKS EFFORTLESS. (from f000) | Brand row f000 | sig-note 0.32 s; soft impact 0.80 s | Deterministic HTML/CSS + real photo | Text slices through headline; seam lands late; black frame 0 | Static seam glow only | Snapshots 0 / 0.6 / 1.5 s; check pass |
| S2 Engineering reveal | 060–179 | Surprise → understanding | Same page as 4 layers | Parted → iso stack → flat window | Tilt 56° / spin −34° / scale 0.63, back to flat | seal 2.0–2.4; tilt 2.05–3.05; layers z 2.55–3.7; trace 4.1–4.52; lock-back 5.1–5.85 | EVERY DETAIL IS ENGINEERED. (2.40–5.90 s) | Gold system, brand row | drops 2.62 / 2.90; rollover 4.12; chip 4.52; impact 5.82 | CSS 3D (preserve-3d), SVG | Layer z-fighting; trace hidden behind photo; jump at 6.0 s | 2D offset stack | Snapshots 3.6 / 4.75 / 5.95 s |
| S3 Proof of value | 180–389 | Show why engineering matters | Villa Amara request flow | Hero → residence page → phone → agent dashboard Confirmed | Push 1.14 on booking panel; push 1.22 on request row | swap 0.15–0.46; click 1.60; carry 2.02–2.64; carry 3.70–4.30; confirm 5.42 | Caption "Nilora Estates / A REAL DEVERAXTECH BUILD"; labels WEBSITE / MOBILE APP VIEW / AGENT DASHBOARD | Brand row | click 7.62; card-slide 8.02 / 9.72; click+chip 11.42–11.47 | HTML recreations of real Nilora UI | Cursor misses button; three heroes compete; unreadable status | Cut the dashboard punch-in | Snapshots 6.6–11.6 s |
| S4 Engineered payoff | 375–509 (host 12.5–17.0) | Satisfying system coherence | Same residence on 3 surfaces | 3 components off-line → locked on seam → folded into seam → seam horizontal | Locked-off | seam lands 13.11; locks 13.65 / 14.20 / 14.73; sheen 15.0–15.7; still to 16.2; fold 16.2–16.55; rotate 16.57–16.97 | none (functional tags only) | Seam = logo trace | sig-two 13.11; drops 14.20 / 14.73 | HTML | Lock misses seam; fold leaves residue | Skip the rotation and cut to S5 | Snapshots 13.2–16.8 s |
| S5 Unmistakable brand | 510–599 | Recognition | Official logo | Horizontal seam → logo + wordmark + tagline + URL | Locked-off | logo wipe 17.00–17.47; word 17.45; tag 17.62; URL 17.80; hold to 20.0 | DevEraXTech / ENGINEERED EXCELLENCE / deveraxtech.com | Official PNG logo, unaltered | sig-full 17.45; music fade 18.8–20.0 | PNG + live type | Logo distorted; identity readable < 2 s | — | Snapshots 17.25–19.95 s; ffprobe |

**Loop**: no seamless loop claimed. Last frame (end card) → first frame (website) is a deliberate restart.
