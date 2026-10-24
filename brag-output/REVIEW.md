# REVIEW — DevEraXTech flagship (provisional, technically complete, not approved for publication)

## Deliverables
| File | What |
|---|---|
| `brag.mp4` | **Flagship master**: 1080×1920, H.264 High, yuv420p, BT.709 SDR, 30 fps, 600 frames, 20.000 s, AAC 48 kHz stereo 256 kb/s, −14.1 LUFS integrated, −1.2 dBFS peak, poster baked into frame 0, faststart |
| `brag-muted.mp4` | Same picture, no audio track (muted-safe export) |
| `brag.jpg` | Poster / custom thumbnail (t = 1.5 s: seam open, copy settled) |
| `brag.raw.mp4` | Hyperframes render before loudness normalisation and poster bake |
| `hooks/hookA.mp4`, `hookB.mp4`, `hookC.mp4` | 2.5 s hook prototypes + `HOOK-EVALUATION.md` |
| `brag-plan.md` | Brand Truth Sheet, rights, strategy, brand system, storyboard, risk register |
| `SHOT-SHEETS.md` | Shot-level contract + continuity spec |
| `composition-brief.md` | Hyperframes hand-off |
| `share-copy.txt`, `share-copy-variants.md` | Captions (include the required CC BY music credit) |
| `composition/` | Editable Hyperframes source |

## What was actually run (Hyperframes 0.8.190, /brag full workflow)
1. Brand audit from the owner's repos (`DevEraXTech`, `Nilora-Estates`) + live deveraxtech.com (title and "ENGINEERED EXCELLENCE" confirmed in live HTML).
2. `npx hyperframes init --resolution portrait`, then 5 sub-compositions written by hand (HTML/CSS/SVG/GSAP, CSS 3D).
3. `npx hyperframes lint` → 0 errors, 0 warnings. `npx hyperframes check` → **passed**: layout and contrast run, 71 text elements contrast-checked, 0 errors.
4. `npx hyperframes snapshot` at every scene beat; `render --quality delivery` (1 m 24 s, software GPU).
5. Checked on the **encoded file**: ffprobe metadata; frames decoded at 25 timestamps; frame-diff across both hard scene boundaries (f179→180 and f509→510); EBU R128 loudness; `hyperframes audio` onsets.
6. ffmpeg: two-pass `loudnorm` (−25.5 → −14.1 LUFS), poster overlaid on frame 0 only, CRF 13 re-encode.

## Quality gates
| Gate | Result | Evidence |
|---|---|---|
| 1 Brand identity | Pass | Official PNG logo, unaltered (transparent margin cropped only); "DevEraXTech" and "ENGINEERED EXCELLENCE" verbatim; no invented claims, metrics or testimonials |
| 2 Hook | Pass | Frame 0: website + "LOOKS EFFORTLESS." + logo; change at 0.33 s |
| 3 Narrative | Pass (self-assessed) | website → structure → real flow → system → logo |
| 4 Distinctiveness | Pass (self-assessed) | Seam/ring terminal from the logo's own traces, used in all 5 scenes; three-note sonic in S1/S4/S5 |
| 5 Temporal consistency | Pass | Mean abs diff at scene seams: 0.05 (f509→510) and 2.25 → fixed (floor glow carried across) |
| 6 Typography & UI | Pass with warnings | All campaign/brand text ≥ 34 px; in-window UI text is 9–20 px by design (texture, flagged by `check` as `text_below_floor` warnings) |
| 7 Sound | Pass (measured, **not heard**) | Onsets at the visual hits: 0.32, 0.83, 2.62, 4.57, 7.62, 11.42, 13.09, 17.44 s; no clipping (peak −1.2 dBFS); licences: CC0 SFX, CC BY 4.0 music (credit required) |
| 8 Export | Pass | ffprobe above |

## Weighted creative rubric (one reviewer's evidence, no viewer data)
| Category | Weight | Score /10 | Evidence |
|---|---|---|---|
| Hook & initial attention | 20% | 8 | Clear contradiction within 1 s; strong poster. Not audience-tested |
| Brand recognition & memory | 20% | 8 | Logo present 0–17 s + end card; seam = logo geometry |
| Product & customer-value clarity | 15% | 7 | Real flow (Request → Pending → Confirmed) is clear; dashboard text is small even after the 1.22 punch-in |
| Originality & distinctiveness | 15% | 7 | The seam system is ownable; the exploded-layer view is a known genre |
| Technical feasibility & reliability | 10% | 9 | Fully deterministic; renders identically |
| Cinematic craftsmanship | 10% | 6 | Clean, restrained, but flat CSS lighting. No real material/specular work or 3D renders |
| Mobile & platform presentation | 10% | 8 | All copy inside 168–1330 px |
| **Weighted** | | **7.6** | |

**Weakest category: cinematic craftsmanship.** Highest-impact next fix: replace the flat stage with a real lit plate (an approved AI-generated or shot studio backdrop with consistent top-left key) behind the deterministic UI, and add a glass/specular pass on the S4 sheen.

## Remaining known issues (none critical or major)
- P2: 12.45–12.6 s — the dashboard blurs out a beat before the payoff cards fully arrive (a brief near-empty stage).
- P2: "Your viewing is requested" reads for 0.5 s (below its 1.7 s floor). The phone card repeats the information right after.
- P2: Hook C's frame 0 can read as broken.
- Audio-reactive visuals were not implemented (planned in /brag, optional).
- Music is the bundled CC BY track. It is a little "upbeat corporate" for luxury; the owner may prefer a licensed score.
- No seamless loop (deliberate restart).

## Not done, on purpose
- **Campaign expansion** (15 s cut, 6 s identity, behind-the-engineering edit, 36 s, thumbnails, Arabic version). The brief gates these on flagship approval by the brand owner, which has not happened.
- No paid generation, no uploads, no publishing, no commits to any repo.

## Approval status
Technically final against the brief's stop conditions. **Creative choices are provisional. Not approved for publication**: that sign-off belongs to the brand owner.
