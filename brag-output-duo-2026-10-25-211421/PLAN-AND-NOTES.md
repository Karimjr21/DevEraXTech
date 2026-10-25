# DevEraXTech — "Is your website ready for the iPhone Duo?"

**Status: provisional draft. Brand owner approval needed before publishing.**

- Format: 1080×1920, 30 fps, 31.2 s.
- Audio: master is -14.8 LUFS with a -1.2 dBFS peak. The 44.1 kHz share copy is -15.1 LUFS with a -1.4 dBFS peak.
- Files:
  - `duo.mp4`: master.
  - `duo-share.mp4`: copy for TikTok and phones.
  - `qa-sheet.jpg`: a frame every 2 s.

## Why this one is built differently
The "Before any code" post lost most viewers at 0:01 (TikTok retention: 6% average watched). Its opening frame was a quiet, low-contrast card on cream paper, which reads as a still image. This film changes that:
- **Frame 0 is already loud and moving:** a saturated gold-yellow ground, heavy black type, and a closed foldable phone shaking under the question.
- **0.22 s:** the phone snaps open (5.4″ → 7.6″) and the website inside breaks. Warning badges pop on the beat.
- **The questions are personal and topical.** They start with "your" and point at a phone that launched two days ago.
- **The music starts on the beat drop**, so there is no quiet intro.

## Questions (no count is ever shown)
| Time (s) | Question | Answer |
|---|---|---|
| 0 | "Is your website ready for the iPhone Duo?" (then "Does your site survive the unfold?", with "the fix is at the end ↓") | Answered at the end. |
| 7.35 | "Would you wait 5 seconds for a website to load?" The phone counts 1…5 on the beat, then gets swiped away. | "Neither would your customers." / "So we build websites that load fast." |
| 15.7 | "Does your website still look like it's 2010?" A retro site (marquee, under-construction tape, visitor counter) is scanned into a modern one. | "A redesign that looks like today." |
| 22.8 | "So… is your website ready for the iPhone Duo?" The phone opens again and the layout reflows: 5.4″ ✓ 7.6″ ✓ | "Ours are. Responsive on every screen, even the newest." |
| 27.5 | Black takeover with the gold logo: DevEraXTech / ENGINEERED EXCELLENCE / "Is yours ready?" / deveraxtech.com | |

## Fact check
- iPhone Duo is Apple's first foldable. It was unveiled on 9 Sep 2026 and went on sale on 23 Oct 2026, with a 5.4″ outer screen and a 7.6″ inner screen. Sources: Apple Newsroom "Apple unveils iPhone Duo" and TidBITS, 11 Sep 2026.
- The phone in the film is a generic drawing. It has no Apple logo or trade dress; the name appears only as a question.
- "5 seconds" is a hypothetical in a question, not a statistic.
- The websites shown are generic mock-ups ("YourBrand"), not client work.

## Credits
- **Post caption must include:** Music: "Funkorama" by Kevin MacLeod (incompetech.com), CC BY 4.0. The track is trimmed to start at 6.95 s; it is otherwise unaltered.
- SFX come from the bundled /brag skill library.

## QA
`hyperframes check`: 0 errors. One readability note: the returning Duo question holds for 2.33 s, against a 2.4 s floor. Loudness was measured, not listened to.

## Rebuild
```
cd composition && python3 tools/gen.py && npx hyperframes check && npx hyperframes render --quality delivery --fps 30 -o ../duo.raw.mp4
```
Then run loudnorm with two passes (I=-14, TP=-2.5, linear) and trim to 31.19 s. Use a limiter of 0.8 for the 48k master and 0.65 for the 44.1k share copy.
