# DevEraXTech — "Before any code" (paper questions film)

**Status: provisional draft. Brand owner approval needed before publishing.**

- Format: 1080×1920, 30 fps, 40.3 s. Audio: -14 LUFS integrated, peak about -2.3 dBFS.
- Files:
  - `paper-q.mp4`: master, 48 kHz audio.
  - `paper-q-share.mp4`: 44.1 kHz audio, for phones and TikTok uploads.
  - `qa-sheet.jpg`: a frame every 2.5 s, taken from the encoded master.
- Look: paper and pencil, the same style as the "From napkin to launch" film (cream dot-grid paper, graphite pencil lines, gold ink, Playfair italic, Caveat handwriting).

## Approach: questions with no count
The question count is never shown.

| Time (s) | What happens |
|---|---|
| 0–8 | Opening question, already on screen at frame 0: "What do we do before writing any code?" with "answer at the end ↓". Two wrong guesses ("code?", "designs?") are written and crossed out. |
| 7.65 | Surprise card: "Will it work on every screen?" It is answered on the spot: one layout is redrawn for desktop, tablet and phone. "Fast, responsive and scalable." |
| 17.5 | Surprise card: "Can we fix a website we didn't build?" Answer: "Yes, in most cases." Gold ink circles outdated plugins, slow pages and no backups. A magnifier passes over the site and each problem is ticked. "We start with a short review." |
| 29.2 | The opening question comes back with "So…". Answer: "We listen first." Checklist: your goals ✓ your audience ✓ your timeline ✓, next to an ear doodle. "A clarity-first discovery conversation." |
| 36.56 | Logo stamp: DevEraXTech, ENGINEERED EXCELLENCE, "from first call to launch.", deveraxtech.com |

The claims are the same service statements used in the earlier films. No metrics, client names or testimonials are shown.

## Credits
- Music: "Lobby Time" by Kevin MacLeod (incompetech.com), licensed under CC BY 4.0. Trimmed to start at 1.3 s.
- **Post caption must include:** Music: "Lobby Time" by Kevin MacLeod (incompetech.com), CC BY 4.0
- SFX and `sig-full.wav` come from the bundled /brag skill library, the same files used in the earlier films. Caveat is bundled as a local woff2.

## QA
`hyperframes check`: 0 errors. One leftover runtime note, "GSAP target not found", is harmless. Card hold times were lengthened to meet the readability floor. Loudness was measured, not listened to.

## Rebuild
```
cd composition && python3 tools/gen.py && npx hyperframes check && npx hyperframes render --quality delivery --fps 30 -o ../paper-q.raw.mp4
```
Then loudnorm with two passes (I=-14, TP=-2.5, linear), add a limiter at 0.8 after `aresample`, and trim to 40.32 s.
