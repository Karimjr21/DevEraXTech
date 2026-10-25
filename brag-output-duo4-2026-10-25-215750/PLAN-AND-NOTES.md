# DevEraXTech — "iPhone Duo owners are reporting cracks at the hinge" (realistic news-style TikTok)

**Status: provisional draft. Brand owner approval needed before publishing.**

- Format: 1080×1920, 30 fps, 30.0 s.
- Audio: master -14.8 LUFS, peak -3.0 dBFS. Share copy (44.1 kHz) -14.7 LUFS, peak -3.0 dBFS.
- Files:
  - `duo4.mp4`: master.
  - `duo4-share.mp4`: copy for TikTok.
  - `qa-sheet.jpg`: QA frame sheet.

## The trend
The iPhone Duo went on sale on 23 Oct 2026, and owners in several countries are posting about **inner screens cracking along the hinge**. Reviewers also flag a second, quieter problem: **"messy apps"**, meaning software not yet adapted to the fold. The film rides the first story and turns to the second, which is DevEraXTech's territory.

## Structure: 2 hooks, 2 questions
| Time (s) | Beat | Screen text | Footage |
|---|---|---|---|
| 0 | Hook 1 | "iPhone Duo owners are already reporting cracks at the hinge." Three headline cards land on the beat (Tom's Guide, Digital Trends, Gulf News), with "early reports · cause not confirmed". | Hands on a phone at night |
| 3.85 | Hook 2 | "But reviewers flagged a second problem…" The MacStories card reads "Great Hinge, *Messy Apps*…", then "…and this one is about your website." | Young man, worried, on a sofa |
| 7.6 | Question 1, answered at the end | "When your customer unfolds their phone…" then "…does your website fit the screen?" with "answer at the end ↓" | A real phone screen being browsed (two shots) |
| 12.63 | Question 2, answered on the spot | "Would you buy from a website that looks broken?", then "Most of us just close the tab.", then "Your customers do the same." | Frustrated woman at a laptop |
| 19.62 | Answer to question 1 | "The fix isn't a new phone." / "It's a responsive website, built to fit every screen, folded or not." / "That's what we build." | Woman smiling at her phone; top-down shot of someone working at a desk |
| 25.31 | End card | Logo, ENGINEERED EXCELLENCE, "Is your website ready for the fold?", deveraxtech.com | Dimmed close-up of a phone keyboard |

## Everything is real footage
Every shot is real stock video from Mixkit. Only clips marked with Mixkit's **free** licence were used; clips marked "Restricted" were left out.

| Clip | Mixkit ID |
|---|---|
| hands typing on a cell phone | 4915 |
| young man upset receiving a message | 8744 |
| woman exploring an online sales page | 42136 |
| man's hand scrolling a sales page | 42133 |
| very frustrated woman at her computer | 25575 |
| woman walking watching her phone | 4891 |
| young man scrolling at his desk (top view) | 4801 |
| hands of a young woman typing on a smartphone | 39774 |

None of the footage shows an iPhone Duo, and the film never claims it does. The phones are generic b-roll; the Duo is only talked about.

## Fact check (headline cards are quoted word for word)
- Tom's Guide: "The iPhone Duo just came out, and owners are already seeing screens crack at the hinge"
- Digital Trends: "Some iPhone Duo owners are reporting cracks around the hinge"
- Gulf News: "iPhone Duo Faces Early Durability Concerns as Screens Crack Along Hinge Hours After Launch"
- MacStories: "iPhone Duo Review Roundup: Great Hinge, Messy Apps, and Everybody Misses Face ID"

The reports are early, and coverage notes that the cause and how widespread it is are not established. The film says so on screen ("early reports · cause not confirmed"). No statistics are claimed.

## Credits
- **Post caption must include:** Music: "Investigations" by Kevin MacLeod (incompetech.com), CC BY 4.0. The track is trimmed to 40 s.
- Footage: Mixkit, Stock Video Free License (https://mixkit.co/license/).
- SFX come from the bundled /brag skill library.

## QA
- `hyperframes check`: 0 errors, 0 warnings.
- Loudness was measured, not listened to.

## Rebuild
1. Cut the clips with the ffmpeg crop/scale commands in the session log. The cut files are already saved in `composition/assets/footage/`.
2. Run `cd composition && python3 tools/gen.py && npx hyperframes render --quality delivery --fps 30 -o ../duo4.raw.mp4`.
3. Normalise loudness in two passes (I=-14, TP=-2.5), apply a 0.62 limiter, and trim to 30 s.
