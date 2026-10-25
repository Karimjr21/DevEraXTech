# DevEraXTech — "POV: your customer just unfolded their iPhone Duo"

**Status: provisional draft. Brand owner approval needed before publishing.**

- Format: 1080×1920, 30 fps, 31.0 s.
- Audio: the master is -14.1 LUFS with a -2.1 dBFS peak. The share copy (44.1 kHz) is -14.4 LUFS with a -2.1 dBFS peak.
- Files: `duo2.mp4` (master), `duo2-share.mp4` (copy for TikTok), `qa-sheet.jpg`.

## What's different from the first Duo film
| | First Duo film (yellow) | This film |
|---|---|---|
| Look | Loud yellow ground, black type, phone mock-up | Night-sky navy (one of the Duo's colours) with a star field, white and gold type, monospace "debug" tags |
| Hook format | A direct question | A **POV** setup: "POV: your customer just unfolded their new iPhone Duo…" then "…and opened your website." |
| Device | Phone mock-up | The unfolded screen fills the whole width of the frame, with the hinge down the centre |
| Music | Funk | Electronic: "Voxel Revolution", 123 BPM |

## Hooks and questions (the count is never shown)
| Time (s) | Hook or question | What happens |
|---|---|---|
| 0 | POV hook | Frame 0 shows the closed phone already moving. At 0.53 s it unfolds into the whole frame and the site breaks. Tags pop on the beat: IMAGE STRETCHED, TEXT IN THE FOLD, BUTTON SPLIT IN HALF. Then "we fix it at the end ↓". |
| 7.4 | "Where did your 'Book now' button go?" | The button tears along the hinge and a tap lands in the gap. Answer: "Lost in the fold." / "We design around the hinge." The whole button moves to the left side with SAFE ZONE ✓. |
| 13.3 | "Two screens. Is your website using both?" | The right half stays empty and blinks. Answer: "We make both sides work." Browse on the left, book on the right. |
| 21.7 | Return: "Same POV. Our build." / "Your customer unfolds again…" | Clean reflow: 5.4″ ✓ 7.6″ ✓ hinge ✓. "A website that unfolds as nicely as the phone." |
| 26.6 | Ending | Logo, ENGINEERED EXCELLENCE, "Is your website Duo-ready?", deveraxtech.com |

## Fact check
- The device facts (5.4″ outer screen, 7.6″ inner screen, book-style fold, on sale 23 Oct 2026) come from Apple Newsroom and TidBITS.
- The phone is a generic drawing with no Apple logo or trade dress.
- The POV is a dramatised scenario, not a testimonial.
- The websites are generic mock-ups, and the dates on the booking chips are only for illustration.

## Credits
- **Post caption must include:** Music: "Voxel Revolution" by Kevin MacLeod (incompetech.com), CC BY 4.0. The music is trimmed to 40 s and otherwise unaltered.
- SFX come from the bundled /brag skill library.

## QA
`hyperframes check`: 0 errors, 0 warnings. Loudness was measured, not listened to.

## Rebuild
`cd composition && python3 tools/gen.py && npx hyperframes render --quality delivery --fps 30 -o ../duo2.raw.mp4`

Then normalise loudness in two passes (I=-14, TP=-2.5). Apply the limiter at 0.75 for the 48k master and 0.65 for the 44.1k share copy, and trim to 31 s.
