# DevEraXTech — "Your customer just paid $1,999 for this phone" (realistic Duo film)

**Status: provisional draft. Brand owner approval needed before publishing.**

- Format: 1080×1920, 30 fps, 31.0 s.
- Audio: the master is -14.1 LUFS with a -2.0 dBFS peak. The share copy (44.1 kHz) is -14.2 LUFS with a -3.0 dBFS peak.
- Files: `duo3.mp4` (master), `duo3-share.mp4` (copy for TikTok), `qa-sheet.jpg`.

## What makes it realistic
- **A real photographed scene.** A café table with coffee, shot from above (CC0 photo). It's softly out of focus like shallow depth of field, with warm window light, a lens vignette and a slow handheld-style push-in.
- **A photo-real foldable.** It has a brushed titanium edge, glass glare sweeps and a contact shadow on the table. It **opens like a book in real 3D**: the outer screen swings over the hinge and becomes the left half of the inner screen.
- **Real browser rendering.** The fictional café site ("Corner Café") is real HTML laid out by the browser. The broken version uses a desktop layout that really overflows: a stretched photo, a headline crossing the hinge, a button split by the fold, unreadable 11 px menu text, and a "Call us" button off the edge.
- **Native-looking UI.** It uses screen-recording touch dots (taps, a two-finger pinch, a horizontal drag), TikTok-style caption boxes and a status bar.

## Hooks and questions (the count is never shown)
| Time | Hook or question | What happens |
|---|---|---|
| 0 s | "Your customer just paid $1,999 for this phone." | The phone lifts off the table and unfolds. Then: "…and this is your website on it. Book a table?" A thumb taps the button on the hinge and nothing happens. "wait for the fix at the end ↓" |
| 7.45 s | "Can they read your menu without zooming?" | A two-finger pinch over tiny text. Answer: "Nobody wants to pinch and zoom." / "So we size text for every screen." The legible two-column menu follows. |
| 14.56 s | "Where's your 'Call us' button?" | A thumb hunts, and dragging sideways shows a sliver of red ("→ cut off"). Answer: "Off the edge." / "We keep what matters in thumb's reach." Both buttons sit on the left half and get tapped. |
| 21.83 s | "Same café. Same phone. Built right:" | It folds and unfolds into the clean two-pane layout, with 5.4″ ✓ 7.6″ ✓ hinge ✓. "Built for every screen. Even the $1,999 one." |
| 27.46 s | Ending | The table dims and the logo lands. "Is your website Duo-ready?" and deveraxtech.com |

## Fact check
- The iPhone Duo starts at $1,999 and has a 5.4″ outer and 7.6″ inner screen (Apple Newsroom, Sep 2026; SAYS price and specs).
- The phone is a generic drawing with no Apple logo or trade dress.
- "Corner Café", its menu and its prices are fictional. They are not a client or a real business.
- No statistics are claimed.

## Credits
- **Post caption must include:** Music: "Wallpaper" by Kevin MacLeod (incompetech.com), CC BY 4.0. The track is trimmed to 40 s and otherwise unaltered.
- Photos are all CC0 (public domain) and found via Openverse. No credit is required, but they are recorded here:
  - Table background: "Still items" by Freestocks.org, https://stocksnap.io/photo/still-items-DTZNYHZ46B
  - Latte in the café site: "Hot latte" by Pawan Kawan, https://stocksnap.io/photo/hot-latte-IN53G9PAJO
  - Espresso and notebook in the café site: rawpixel public-domain image 5926576, https://www.rawpixel.com/image/5926576
- SFX come from the bundled /brag skill library.

## QA
`hyperframes check`: 0 errors. One readability note: "Nobody wants to pinch and zoom." holds for 1.6 s, just under the 1.72 s floor. Loudness was measured, not listened to.

## Rebuild
`cd composition && python3 tools/gen.py && npx hyperframes render --quality delivery --fps 30 -o ../duo3.raw.mp4`

Then normalise loudness in two passes (I=-14, TP=-2.5). Use limiter 0.75 for the 48k master and 0.65 for the 44.1k share copy, and trim to 31 s.
