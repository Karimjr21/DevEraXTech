# DeveraXTech: 26 new reels, spec

Every reel is 1080x1920, 30 fps, H.264 + AAC, rendered from code in `src/` (`python3 render.py`).
Frame 0 is the cover PNG in `covers/`. Text stays inside x 80–940, y 220–1540 (clear of the top 220 px,
bottom 380 px and right 140 px). The DeveraXTech name and logo appear only on the end cards (10.0 s or
later) and in reel 15's signed line (11.6 s). 'Our build' cameos start at 7.8 s at the earliest.

All sound is synthesised in `src/sfx.py` (no licensed music). There is no voice-over: the on-screen
text carries every reel, so they work muted.

Portfolio cameos are real DeveraXTech builds, renamed where a person's name was in the project:
the Barhouma site appears as 'IGCSE Maths platform', the Sarah site as 'CalmCare Therapy Center',
and the developer portfolio is shown as it is.

## At a glance

| # | File | Length | Hook type | Industry | Opening sound | CTA keyword |
|---|------|--------|-----------|----------|---------------|-------------|
| 1 | `dxt-new-01-clinic-next-door.mp4` | 13 s | Mid-sentence start | Clinics & doctors | piano chord stab cut in mid-phrase over a sub hit (sounds like we dropped into the middle of something) | 'CLINIC' |
| 2 | `dxt-new-02-menu-three-seconds.mp4` | 12 s | Hard countdown | Restaurants & cafés | woodblock-style clock tick on top of a short sub hit | 'MENU' |
| 3 | `dxt-new-03-lawyers-before-the-call.mp4` | 13 s | Industry callout | Law firms | dry wooden knock layered with a sub hit (formal, not a cartoon gavel) | 'COUNSEL' |
| 4 | `dxt-new-04-not-your-price.mp4` | 13 s | Myth bust | E-commerce brands | finger-snap crack with a sub hit and a short swish (the strike) | 'STORE' |
| 5 | `dxt-new-05-tower-unfinished.mp4` | 15 s | Unfinished object | Real estate developers | low boom with a pen-nib scratch on top | 'TOWER' |
| 6 | `dxt-new-06-one-tile-is-off.mp4` | 13 s | Precision ASMR | Jewelry & watches | metallic click (like a clasp) on a short low thud | 'PRECISION' |
| 7 | `dxt-new-07-gym-near-me.mp4` | 13 s | Search bar | Gyms & fitness studios | keyboard tap with a short sub hit | 'NEAR ME' |
| 8 | `dxt-new-08-booking-dies-here.mp4` | 14 s | Cursor tracking | Hotels & resorts | double mouse click over a soft sub hit | 'BOOKING' |
| 9 | `dxt-new-09-salon-look-cheap.mp4` | 12 s | Quick-fire listicle | Salons & beauty | camera-shutter double click with a sub hit | 'SALON' |
| 10 | `dxt-new-10-first-room-zoom-out.mp4` | 14 s | Zoom-out reveal | Architecture & interior design | deep sub drop with a dry click (the size of the macro) | 'STUDIO' |
| 11 | `dxt-new-11-guess-in-one-second.mp4` | 12 s | Guess in one second | Startups & SaaS | bright click and high ping (a camera-flash feel without a real flash) over a short sub | 'CLARITY' |
| 12 | `dxt-new-12-stop-the-counter.mp4` | 13 s | Cost-of-waiting meter | Car dealerships | split-flap burst over a sub hit | 'SHOWROOM' |
| 13 | `dxt-new-13-expensive.mp4` | 12 s | Single sound word | Fashion & streetwear | long, saturated 808 with a click on top | 'DROP' |
| 14 | `dxt-new-14-second-you-lose-them.mp4` | 13 s | Freeze frame | Schools & academies | tape-stop freeze over a sub hit (the frozen moment) | 'ENROL' |
| 15 | `dxt-new-15-letter-next-month.mp4` | 15 s | Letter to the viewer | Family businesses | a crisp paper snap and pen scratch over a soft thud | 'THIS MONTH' (reply) |
| 16 | `dxt-new-16-agencies-stop-building.mp4` | 13 s | Unpopular opinion | Marketing agencies (white-label partners) | low tom hit with a sub | 'PARTNER' |
| 17 | `dxt-new-17-drop-your-website.mp4` | 12 s | Viewer challenge | Any business | a single glass tap with a light sub | 'NOTE' |
| 18 | `dxt-new-18-patients-notice.mp4` | 13 s | Insider truth | Dental practices | a porcelain clink (clean, clinical, not a drill) over a light sub | 'SMILE' |
| 19 | `dxt-new-19-one-decision-room.mp4` | 14 s | End-first | Interior & furniture showrooms | a deep boom with a high shimmer tail (the size of a finished space) | 'ONE ROOM' |
| 20 | `dxt-new-20-wrong-answers-only.mp4` | 14 s | Wrong answers only | Coaches & consultants | marker strike (swish + knock) over a sub hit | 'HONEST' |
| 21 | `dxt-new-21-your-eyes-lied.mp4` | 14 s | Optical illusion | Events & weddings | a whoosh that already peaks on the first frame, on a sub | 'EVENT' |
| 22 | `dxt-new-22-seconds-your-homepage-gets.mp4` | 13 s | Direct question with a number | Logistics & B2B | a clean sonar-style ping on a sub | 'QUOTE' |
| 23 | `dxt-new-23-luxury-never-shows.mp4` | 13 s | Luxury code | Premium & luxury brands | a single crystal-bowl strike over a soft thud, with a short whoosh for the pop-up leaving | 'QUIET LUXURY' |
| 24 | `dxt-new-24-tap-cost-an-order.mp4` | 12 s | Mobile thumb test | Food delivery & cloud kitchens | a dull thock of a fingertip on glass over a sub | 'ORDER' |
| 25 | `dxt-new-25-customers-will-expect.mp4` | 13 s | Prediction | Retail chains | a bright chime chord on a sub (a 'reveal' sound) | 'BRANCHES' |
| 26 | `dxt-new-26-arabic-mesh-bayen.mp4` | 14 s | Arabic hook (Egyptian dialect) | Egyptian SMEs | a deep darbuka doum over a sub | 'ابدأ' / START |

## 01. Mid-sentence start: Clinics & doctors

- **File:** `dxt-new-01-clinic-next-door.mp4`, cover `covers/dxt-new-01-clinic-next-door.png`, 13 s
- **Palette:** Near-monochrome: ivory on obsidian, gold only on the turn
- **Hook (frame 0):** …so they booked the clinic next door.
- **CTA (final 2 s):** Be the clinic next door. DM 'CLINIC' to start.

| Time (s) | What happens |
|---|---|
| 0.0–1.6 | Frame 0: hook already on screen, left-aligned as if it is the end of a sentence; a speech waveform is mid-flow and the line drifts left (we joined late). |
| 1.6–3.0 | Cut: 'Same skill. Similar prices.' |
| 3.0–4.4 | Gold: 'So why them?' (the open loop). |
| 4.4–8.0 | Phone mockup of a clinic site. 'Their website answered first:' then three patient questions tick off, one per second: Who will treat me? / When can I come? / How do I book? Each highlights that part of the page. |
| 8.0–10.8 | OUR BUILD: CalmCare Therapy Center, with its real headline 'Personalised support for every care journey.' in a browser frame. |
| 10.8–13.0 | End card: 'Be the clinic next door.' + DM 'CLINIC' + DeveraXTech wordmark + @deveraxtech. Last words echo the hook, so the loop lands. |

**Sound design:** 0.00 piano chord stab cut in mid-phrase over a sub hit (sounds like we dropped into the middle of something); quiet A-minor pad; soft clicks on every text change; whoosh into the build; low thud + crystal on the end card.

**Why it should stop the scroll:** The ellipsis and lower-case start make the brain look for the missing first half, and 'the clinic next door' is a competitor every clinic owner already resents. The viewer stays to learn why patients chose the other clinic.

**QC:** 1080x1920, 30/1 fps, h264/aac, 13.0 s; loudest peak in the first 100 ms (-1.7 dBFS); 4.09% of pixels change between 0.0 s and 1.0 s; hook 7 words. Pass.

## 02. Hard countdown: Restaurants & cafés

- **File:** `dxt-new-02-menu-three-seconds.mp4`, cover `covers/dxt-new-02-menu-three-seconds.png`, 12 s
- **Palette:** Gold-dominant
- **Hook (frame 0):** Your menu has 3 seconds.
- **CTA (final 2 s):** Let the dish speak first. DM 'MENU' to start.

| Time (s) | What happens |
|---|---|
| 0.0–3.0 | Frame 0: a huge gold 3 inside a ring that is already draining; 3…2…1 snap on each second with a hard tick. Hook sits above it the whole time. |
| 3.0–4.6 | Zero: '0' hits with a thud and tape-stop; 'At zero, they order elsewhere.' (what happens at zero). |
| 4.6–5.8 | 'In 3 seconds they need:' |
| 5.8–9.4 | A menu card builds in three hits: 1 the dish (photo), 2 the price, visible ([price] placeholder), 3 one order button. |
| 9.4–10.0 | 'Everything else can wait.' |
| 10.0–12.0 | End card: 'Let the dish speak first.' + DM 'MENU'. Cuts back to the running 3 on loop. |

**Sound design:** 0.00 woodblock-style clock tick on top of a short sub hit; ticks at 1.0 and 2.0; at 3.0 a low thud with a short tape-stop; a quiet 120 bpm sub pulse under the menu build; clicks per hit; thud + crystal on the end card.

**Why it should stop the scroll:** A countdown that is already running is the strongest frame-0 motion there is, and the number in the hook is literally ticking. The viewer waits to see what happens at zero.

**For Karim to fill or confirm:** [price] on the menu-card mockup (leave as a dash or a real menu price if Karim prefers)

**QC:** 1080x1920, 30/1 fps, h264/aac, 12.0 s; loudest peak in the first 100 ms (-1.6 dBFS); 1.85% of pixels change between 0.0 s and 1.0 s; hook 5 words. Pass.

## 03. Industry callout: Law firms

- **File:** `dxt-new-03-lawyers-before-the-call.mp4`, cover `covers/dxt-new-03-lawyers-before-the-call.png`, 13 s
- **Palette:** Near-monochrome: ivory serif on obsidian, gold hairlines
- **Hook (frame 0):** LAWYERS: clients decide before the first call.
- **CTA (final 2 s):** Be chosen before the first call. DM 'COUNSEL' to begin.

| Time (s) | What happens |
|---|---|
| 0.0–1.7 | Frame 0: 'LAWYERS:' in large tracked capitals, the rest of the hook under it; a gold rule is sweeping under the word and the frame is slowly pushing in; faint gold pillars drift behind. |
| 1.7–3.2 | 'Not in your office.' |
| 3.2–4.8 | 'On a phone screen. In seconds.' |
| 4.8–6.4 | Uncomfortable truth in gold: 'They can't judge your legal skill.' |
| 6.4–8.0 | 'So they judge what they can see.' |
| 8.0–10.8 | Roman-numbered list snaps in: I Clarity / II Credentials / III Who they'll speak to / IV How fast they can reach you. |
| 10.8–13.0 | End card: 'Be chosen before the first call.' + DM 'COUNSEL'. |

**Sound design:** 0.00 dry wooden knock layered with a sub hit (formal, not a cartoon gavel); D-minor pad; softer knocks on each statement; clicks on the list; thud + crystal on the end card.

**Why it should stop the scroll:** The first word is the viewer's job title, so lawyers self-select in a quarter of a second, and the rest of the line threatens their pipeline. 'They can't judge your legal skill' is true and uncomfortable, which keeps them through the middle.

**QC:** 1080x1920, 30/1 fps, h264/aac, 13.0 s; loudest peak in the first 100 ms (-1.8 dBFS); 1.43% of pixels change between 0.0 s and 1.0 s; hook 7 words. Pass.

## 04. Myth bust: E-commerce brands

- **File:** `dxt-new-04-not-your-price.mp4`, cover `covers/dxt-new-04-not-your-price.png`, 13 s
- **Palette:** Obsidian with a deep-emerald accent
- **Hook (frame 0):** It's not your price. It never was.
- **CTA (final 2 s):** Keep the price. Fix the path. DM 'STORE' to rebuild your checkout.

| Time (s) | What happens |
|---|---|
| 0.0–1.8 | Frame 0: the hook in three lines; a gold strike is already racing through the word 'price'. |
| 1.8–3.0 | 'They wanted it.' |
| 3.0–4.0 | 'Then checkout asked for:' |
| 4.0–6.4 | Emerald form fields stack up fast with key taps: Create an account / Phone number / Address (again) / Promo code? |
| 6.4–7.8 | 'Every extra step is a reason to leave.' |
| 7.8–9.6 | The stack collapses into one emerald button: 'Buy in two taps' with a check. |
| 9.6–11.0 | Gold: 'Fix the path, not the price.' |
| 11.0–13.0 | End card: 'Keep the price. Fix the path.' + DM 'STORE'. |

**Sound design:** 0.00 finger-snap crack with a sub hit and a short swish (the strike); emerald E-minor pad; mechanical key taps as fields pile up; a low thud when the point lands; metal click as the button forms.

**Why it should stop the scroll:** Every store owner's private fear is that they are too expensive. Opening by striking that belief out is a relief and a provocation at once, and the obvious next question is 'then what is it?'.

**QC:** 1080x1920, 30/1 fps, h264/aac, 13.0 s; loudest peak in the first 100 ms (-1.9 dBFS); 2.52% of pixels change between 0.0 s and 1.0 s; hook 7 words. Pass.

## 05. Unfinished object: Real estate developers

- **File:** `dxt-new-05-tower-unfinished.mp4`, cover `covers/dxt-new-05-tower-unfinished.png`, 15 s
- **Palette:** Gold-dominant line art on obsidian; one continuous move
- **Hook (frame 0):** Your tower is finished. Your website isn't.
- **CTA (final 2 s):** Your tower deserves a finished site. DM 'TOWER' to start your property site.

| Time (s) | What happens |
|---|---|
| 0.0–2.0 | Frame 0: a gold line drawing of a two-tower development is about a third drawn, the pen head glowing and moving. Hook above it. |
| 2.0–4.0 | The drawing keeps going: 'Buyers tour it online first.' |
| 4.0–6.0 | 'Renders. Floor plans. Payment plans.' |
| 6.0–8.0 | 'One place. One feeling.' |
| 8.0–10.5 | 'Finish the story.' The last strokes land. |
| 10.5–13.0 | Payoff: the finished drawing settles into the hero of a luxury property site. OUR BUILD: Nilora Estates, 'Where the river meets the light.' |
| 13.0–15.0 | End card: 'Your tower deserves a finished site.' + DM 'TOWER'. |

**Sound design:** 0.00 low boom with a pen-nib scratch on top; a quiet scratch texture follows the pen; F-major pad; small clicks on text changes; boom + shimmer when the drawing completes; thud + crystal on the end card.

**Why it should stop the scroll:** An unfinished drawing makes the brain wait for completion (the Zeigarnik effect), and the hook tells developers the one part of their project that is still unfinished. The completion is the payoff.

**QC:** 1080x1920, 30/1 fps, h264/aac, 15.0 s; loudest peak in the first 100 ms (-1.7 dBFS); 3.59% of pixels change between 0.0 s and 1.0 s; hook 7 words. Pass.

## 06. Precision ASMR: Jewelry & watches

- **File:** `dxt-new-06-one-tile-is-off.mp4`, cover `covers/dxt-new-06-one-tile-is-off.png`, 13 s
- **Palette:** Champagne accent on obsidian
- **Hook (frame 0):** One of these tiles is off.
- **CTA (final 2 s):** Set every pixel like a stone. DM 'PRECISION' to begin.

| Time (s) | What happens |
|---|---|
| 0.0–2.3 | Frame 0: six product tiles (ring, watch, necklace, earrings, bracelet, pendant) are mid-snap into a grid, each landing with a crisp metallic click. One lands a hair out of line. |
| 2.3–3.0 | Hold on the grid: the viewer hunts for the odd tile. |
| 3.0–4.4 | 'Found it?' |
| 4.4–6.2 | Push in on the culprit with champagne guide lines: 'Off by a hair.' |
| 6.2–7.8 | 'Your clients can't name it.' |
| 7.8–9.4 | 'But they feel it.' |
| 9.4–11.0 | The tile clicks into perfect alignment: 'In jewellery, that is a flaw.' |
| 11.0–13.0 | End card: 'Set every pixel like a stone.' + DM 'PRECISION'. |

**Sound design:** 0.00 metallic click (like a clasp) on a short low thud; one panned click per tile; air texture; a high ping when the culprit is found; the loudest click when it snaps into place; thud + crystal on the end card.

**Why it should stop the scroll:** It is a spot-the-difference challenge the viewer cannot refuse, paired with satisfying click ASMR. Jewellers live by precision, so the payoff flatters their standards and questions their website's in the same move.

**QC:** 1080x1920, 30/1 fps, h264/aac, 13.0 s; loudest peak in the first 100 ms (-2.4 dBFS); 1.33% of pixels change between 0.0 s and 1.0 s; hook 6 words. Pass.

## 07. Search bar: Gyms & fitness studios

- **File:** `dxt-new-07-gym-near-me.mp4`, cover `covers/dxt-new-07-gym-near-me.png`, 13 s
- **Palette:** Champagne accent on obsidian
- **Hook (frame 0):** Whose gym shows up first?
- **CTA (final 2 s):** Be the first name they tap. DM 'NEAR ME' to start.

| Time (s) | What happens |
|---|---|
| 0.0–1.0 | Frame 0: an abstract search field already typing 'gym ne…'; the query finishes with key taps. Hook sits above. |
| 1.0–2.5 | Three anonymous result cards drop in. The top card's name is a gold question mark. |
| 2.5–4.0 | 'Not always the best gym.' |
| 4.0–5.5 | 'The one easiest to choose.' |
| 5.5–8.5 | The top card opens into a checklist, one per half second: Hours, up to date / Exact location / Class times / Fast on a phone / Book a free trial. |
| 8.5–10.0 | The question mark flips to 'Your gym' in gold (the payoff). |
| 10.0–11.0 | 'Make it yours.' |
| 11.0–13.0 | End card: 'Be the first name they tap.' + DM 'NEAR ME'. |

**Sound design:** 0.00 keyboard tap with a short sub hit; key taps finish the query; a 128 bpm sub pulse (gym energy without loud music); light metallic ticks for each checklist item; chime when 'Your gym' appears.

**Why it should stop the scroll:** Every gym owner has searched 'gym near me' to check on rivals. The live query is instantly recognisable and the unanswered 'whose?' is the loop. The search UI is abstract and does not copy Google.

**For Karim to fill or confirm:** 'Book a free trial' is a generic checklist item; change it if the client offers no trial

**QC:** 1080x1920, 30/1 fps, h264/aac, 13.0 s; loudest peak in the first 100 ms (-1.9 dBFS); 2.95% of pixels change between 0.0 s and 1.0 s; hook 5 words. Pass.

## 08. Cursor tracking: Hotels & resorts

- **File:** `dxt-new-08-booking-dies-here.mp4`, cover `covers/dxt-new-08-booking-dies-here.png`, 14 s
- **Palette:** Obsidian with a deep-emerald accent
- **Hook (frame 0):** Watch the exact second a booking dies.
- **CTA (final 2 s):** Keep the cursor on 'Book'. DM 'BOOKING' to begin.

| Time (s) | What happens |
|---|---|
| 0.0–3.0 | Frame 0: a resort website in an abstract browser frame; a visitor cursor is already moving, hovering Rooms, then Gallery, then clicking Rates. A session timer ticks in the corner (labelled illustrative). |
| 3.0–6.0 | Rates opens onto 'Rates on request. Fill in the form.' The cursor hesitates, jitters, then drifts towards '← Back'. |
| 6.0–7.4 | Freeze with a tape-stop: a gold ring pulses on the cursor at Back. 'This second.' |
| 7.4–9.4 | Three reasons tick in: Rates hidden behind a form / No photo of the actual room / Three clicks to a date. |
| 9.4–12.0 | Rebuilt page: room photo, 'From [rate] / night', date chips and an emerald Book button. The cursor goes straight to Book and clicks. |
| 12.0–14.0 | End card: 'Keep the cursor on Book.' + DM 'BOOKING'. |

**Sound design:** 0.00 double mouse click over a soft sub hit; G-minor pad; a click on Rates; at 6.0 a tape-stop freeze; ticks for each reason; whoosh to the rebuilt page; click plus chime on Book.

**Why it should stop the scroll:** Watching someone else's cursor is voyeuristic and impossible not to follow, and 'the exact second' promises a precise answer. Hoteliers know that hesitation and want to see it named.

**For Karim to fill or confirm:** [rate] on the rebuilt-page mockup; The session timer is labelled 'illustrative session' on screen

**QC:** 1080x1920, 30/1 fps, h264/aac, 14.0 s; loudest peak in the first 100 ms (-2.4 dBFS); 5.88% of pixels change between 0.0 s and 1.0 s; hook 7 words. Pass.

## 09. Quick-fire listicle: Salons & beauty

- **File:** `dxt-new-09-salon-look-cheap.mp4`, cover `covers/dxt-new-09-salon-look-cheap.png`, 12 s
- **Palette:** Champagne and ivory on obsidian; fast cuts
- **Hook (frame 0):** 5 things that make salons look cheap.
- **CTA (final 2 s):** Look like the price you charge. DM 'SALON' to start.

| Time (s) | What happens |
|---|---|
| 0.0–1.5 | Frame 0: hook on screen; a five-segment bar is already filling, so the viewer knows a fast list is coming. |
| 1.5–2.8 | 01 'Blurry phone photos.' (a soft-focus photo block behind). |
| 2.8–4.1 | 02 'Prices only by DM.' |
| 4.1–5.4 | 03 'Five different fonts.' (each word set in a different typeface). |
| 5.4–6.7 | 04 'Booking by voice note.' |
| 6.7–8.6 | 05, the twist, in gold: 'Calling yourself luxury.' |
| 8.6–10.0 | 'Show it. Don't say it.' |
| 10.0–12.0 | End card: 'Look like the price you charge.' + DM 'SALON'. |

**Sound design:** 0.00 camera-shutter double click with a sub hit; a shutter + thud on every cut; a bigger hit with a crystal shimmer on the twist; light 100 bpm pulse.

**Why it should stop the scroll:** 'Cheap' is the word salon owners fear most, and a numbered list tells the viewer exactly how long to stay. The fifth item turns the list back on them, which drives comments.

**QC:** 1080x1920, 30/1 fps, h264/aac, 12.0 s; loudest peak in the first 100 ms (-2.0 dBFS); 3.07% of pixels change between 0.0 s and 1.0 s; hook 7 words. Pass.

## 10. Zoom-out reveal: Architecture & interior design

- **File:** `dxt-new-10-first-room-zoom-out.mp4`, cover `covers/dxt-new-10-first-room-zoom-out.png`, 14 s
- **Palette:** Near-monochrome: ivory and champagne, one continuous move
- **Hook (frame 0):** Clients judge this before your work.
- **CTA (final 2 s):** Design the first room. DM 'STUDIO' to start.

| Time (s) | What happens |
|---|---|
| 0.0–2.0 | Frame 0: an extreme macro of a single italic ampersand, its curve and soft shadow filling the frame. The camera is already pulling back. Hook on a dark band at the top. |
| 2.0–3.5 | Still pulling back: 'The curve.' |
| 3.5–5.0 | 'The shadow.' The ampersand now sits between two words. |
| 5.0–6.5 | 'The white space.' The words become the headline 'Form & Light'. |
| 6.5–8.5 | 'Every detail is a promise.' The browser frame, nav and project grid come into view. |
| 8.5–12.0 | The full website settles: 'Your website is the first room they walk into.' |
| 12.0–14.0 | End card: 'Design the first room.' + DM 'STUDIO'. |

**Sound design:** 0.00 deep sub drop with a dry click (the size of the macro); B-flat pad filtered low; air texture; tiny clicks on each word; a single crystal note when the site completes.

**Why it should stop the scroll:** A macro shot is unreadable as an object, so the eye has to keep watching to resolve it, and the pull-back is one continuous move with no cut to leave on. Architects and designers judge type and spacing for a living, so the hook speaks their language.

**QC:** 1080x1920, 30/1 fps, h264/aac, 14.0 s; loudest peak in the first 100 ms (-1.8 dBFS); 28.34% of pixels change between 0.0 s and 1.0 s; hook 6 words. Pass.

## 11. Guess in one second: Startups & SaaS

- **File:** `dxt-new-11-guess-in-one-second.mp4`, cover `covers/dxt-new-11-guess-in-one-second.png`, 12 s
- **Palette:** Champagne accent on obsidian
- **Hook (frame 0):** What does this company do? 1 second.
- **CTA (final 2 s):** Make one second enough. DM 'CLARITY' with your homepage.

| Time (s) | What happens |
|---|---|
| 0.0–1.0 | Frame 0: hook on top, a timer bar already draining; below it an invented buzzword homepage ('Empowering the future of synergy.') with gradient blobs. |
| 1.0–2.4 | Hard cut to black: 'No idea?' |
| 2.4–3.8 | 'Neither do your visitors.' |
| 3.8–7.0 | 'Your headline should answer:' What it is. / Who it's for. / What happens next. |
| 7.0–8.2 | 'Try again. 1 second.' The timer drains over a clear homepage: Klozcrew, 'The closing CRM for real estate agencies.' |
| 8.2–10.0 | 'Got it?' then OUR BUILD: Klozcrew. 'One second was enough.' |
| 10.0–12.0 | End card: 'Make one second enough.' + DM 'CLARITY'. |

**Sound design:** 0.00 bright click and high ping (a camera-flash feel without a real flash) over a short sub; a snap on the hard cut at 1.0; E-minor pad; ticks on the list; the same click + ping on the second test so the structure rhymes; chime on 'Got it?'.

**Why it should stop the scroll:** It is a test with a one-second clock, so the viewer plays along instinctively and fails, which is the point. Founders recognise their own vague hero copy instantly, and the second test (which they pass) proves the fix.

**QC:** 1080x1920, 30/1 fps, h264/aac, 12.0 s; loudest peak in the first 100 ms (-1.9 dBFS); 13.93% of pixels change between 0.0 s and 1.0 s; hook 7 words. Pass.

## 12. Cost-of-waiting meter: Car dealerships

- **File:** `dxt-new-12-stop-the-counter.mp4`, cover `covers/dxt-new-12-stop-the-counter.png`, 13 s
- **Palette:** Gold on obsidian, mechanical
- **Hook (frame 0):** Buyers lost while you watch this.
- **CTA (final 2 s):** Stop the counter. DM 'SHOWROOM' to put your stock online.

| Time (s) | What happens |
|---|---|
| 0.0–1.8 | Frame 0: a four-digit split-flap counter is already flipping (0001, 0002…), with a gauge needle sweeping above it. Under it, in small caps: ILLUSTRATIVE COUNTER, NOT REAL DATA. |
| 1.8–3.4 | Counter keeps flipping: 'They didn't stop wanting a car.' |
| 3.4–5.0 | 'They found one faster.' |
| 5.0–6.5 | 'Stock. Price range. Finance options.' |
| 6.5–8.0 | 'Answered on the page, not on hold.' |
| 8.0–10.0 | The counter shrinks to the bottom while a car listing card draws in (line-art car, chips: In stock / Book a test drive / Finance calculator). |
| 10.0–11.0 | The counter stops dead with a thud: 'Stop the counter.' |
| 11.0–13.0 | End card: 'Stop the counter.' + DM 'SHOWROOM'. |

**Sound design:** 0.00 split-flap burst over a sub hit; a flap clack on every increment; an 86 bpm pulse like an idling engine; whoosh into the listing card; a thud and short tape-stop when the counter stops.

**Why it should stop the scroll:** A rising number tied to the viewer's lost sales creates urgency in the first frame, and the open question is 'how high does it go?'. It is labelled illustrative on screen, so nothing is claimed as data.

**For Karim to fill or confirm:** The counter is illustrative and labelled so; Karim can replace it with a client's real enquiry figure only if he has one

**QC:** 1080x1920, 30/1 fps, h264/aac, 13.0 s; loudest peak in the first 100 ms (-1.6 dBFS); 4.88% of pixels change between 0.0 s and 1.0 s; hook 6 words. Pass.

## 13. Single sound word: Fashion & streetwear

- **File:** `dxt-new-13-expensive.mp4`, cover `covers/dxt-new-13-expensive.png`, 12 s
- **Palette:** Near-monochrome: white type on black, gold only in the wordmark
- **Hook (frame 0):** Expensive.
- **CTA (final 2 s):** Look expensive before they touch it. DM 'DROP' before your next collection.

| Time (s) | What happens |
|---|---|
| 0.0–1.6 | Frame 0: 'Expensive.' fills the safe width in italic serif, shaking from the 808 hit and settling, while a hairline draws under it. |
| 1.6–3.0 | The word lifts; under it: 'is a feeling.' |
| 3.0–4.6 | 'It starts before the fitting room.' |
| 4.6–6.0 | 'It starts on the homepage.' |
| 6.0–8.0 | Four lookbook layouts cut on the beat every half second: full-bleed editorial, two-column product, single hero product, 'New season' type spread. |
| 8.0–9.6 | OUR BUILD: TurbanClass, a turban boutique store: 'Gold Embroidered Turban', 'Personalized turbans made just for you.' |
| 9.6–10.0 | 'Expensive.' returns, one more 808, for the loop. |
| 10.0–12.0 | End card: 'Look expensive before they touch it.' + DM 'DROP'. |

**Sound design:** 0.00 long, saturated 808 with a click on top; silence otherwise, so each low thud lands; shutter + pulse on each lookbook cut; a second 808 on the returning word.

**Why it should stop the scroll:** One huge word with a heavy hit is the fastest possible read, and 'Expensive.' is the exact status every fashion founder wants. It opens a question (what is?) that the next line answers.

**QC:** 1080x1920, 30/1 fps, h264/aac, 12.0 s; loudest peak in the first 100 ms (-2.0 dBFS); 1.96% of pixels change between 0.0 s and 1.0 s; hook 1 words. Pass.

## 14. Freeze frame: Schools & academies

- **File:** `dxt-new-14-second-you-lose-them.mp4`, cover `covers/dxt-new-14-second-you-lose-them.png`, 13 s
- **Palette:** Ivory and gold on obsidian
- **Hook (frame 0):** This is the second you lose them.
- **CTA (final 2 s):** Win the second they decide. DM 'ENROL' to begin.

| Time (s) | What happens |
|---|---|
| 0.0–1.8 | Frame 0: frozen. A phone in a parent's hand shows a school site; a playhead bar at the bottom is paused on a marker that pulses with expanding gold rings. Hook at the top. |
| 1.8–3.6 | The playhead rewinds: 'A parent. Comparing schools.' |
| 3.6–6.4 | Play: 'One hand. One thumb.' Three lines on the school site get struck through in gold: Fees? Call the office / Admissions: download PDF / Curriculum: contact us. |
| 6.4–7.8 | 'They decide with one thumb.' |
| 7.8–10.0 | OUR BUILD: an IGCSE Maths platform: courses, live sessions, assignments and parent accounts behind one login. |
| 10.0–11.0 | The playhead passes the marker: 'Now they stay.' |
| 11.0–13.0 | End card: 'Win the second they decide.' + DM 'ENROL'. |

**Sound design:** 0.00 tape-stop freeze over a sub hit (the frozen moment); whoosh on the rewind; marker strikes on each crossed-out line; C-major pad; chime when the playhead passes the marker.

**Why it should stop the scroll:** A paused frame with a playhead tells the viewer something is about to happen, and the hook names the exact moment a school loses a family. Parents use phones one-handed, and school owners know it.

**QC:** 1080x1920, 30/1 fps, h264/aac, 13.0 s; loudest peak in the first 100 ms (-1.6 dBFS); 8.13% of pixels change between 0.0 s and 1.0 s; hook 7 words. Pass.

## 15. Letter to the viewer: Family businesses

- **File:** `dxt-new-15-letter-next-month.mp4`, cover `covers/dxt-new-15-letter-next-month.png`, 15 s
- **Palette:** Ivory paper with ink and gold (the light variant of the palette)
- **Hook (frame 0):** To the owner still saying 'next month'…
- **CTA (final 2 s):** Make it this month. Reply 'THIS MONTH' in our DMs.

| Time (s) | What happens |
|---|---|
| 0.0–1.8 | Frame 0: a handwritten note on warm ivory paper; a pen line is already drawing under the salutation and the paper floats slightly. |
| 1.8–3.8 | The salutation shrinks to the top like a real letter: 'You built this name over years.' |
| 3.8–5.8 | 'Your customers now meet it on a phone.' |
| 5.8–7.8 | 'Tonight, someone searched for exactly what you sell.' |
| 7.8–9.8 | 'What did they find?' |
| 9.8–11.6 | 'Let them find you, the way you deserve.' |
| 11.6–13.0 | Signed in hand: '— the DeveraXTech team'. |
| 13.0–15.0 | End card on the paper: 'Make it this month.' + Reply 'THIS MONTH' in our DMs. |

**Sound design:** 0.00 a crisp paper snap and pen scratch over a soft thud; a warm, quiet F-major pad; a pen scratch as each line is written. Calm on purpose: the contrast with louder reels is the stop.

**Why it should stop the scroll:** Being addressed personally, in handwriting, is rare in a feed of shouting reels. 'Next month' is a phrase every owner has said about their website, so the line feels like it was written to them.

**QC:** 1080x1920, 30/1 fps, h264/aac, 15.0 s; loudest peak in the first 100 ms (-2.4 dBFS); 1.11% of pixels change between 0.0 s and 1.0 s; hook 7 words. Pass.

## 16. Unpopular opinion: Marketing agencies (white-label partners)

- **File:** `dxt-new-16-agencies-stop-building.mp4`, cover `covers/dxt-new-16-agencies-stop-building.png`, 13 s
- **Palette:** Obsidian with a deep-emerald accent
- **Hook (frame 0):** Agencies: stop building your own websites.
- **CTA (final 2 s):** Your name on it. Our build behind it. DM 'PARTNER' for white-label builds.

| Time (s) | What happens |
|---|---|
| 0.0–1.8 | Frame 0: small emerald label UNPOPULAR OPINION over the hook; the frame is shaking off a drum hit and a gold underline is drawing under 'stop'. |
| 1.8–3.2 | 'Your edge is strategy.' |
| 3.2–4.6 | 'Not debugging at 2am.' |
| 4.6–6.4 | 'Every hour in code is an hour not selling.' |
| 6.4–7.6 | 'Partner with a build team.' |
| 7.6–9.8 | Two stacked cards slide apart: front, emerald 'Your agency: strategy, brand, the client'; behind, gold-outlined 'Build partner: design, code, launch'. Caption: 'White-label. Your name on the front.' |
| 9.8–11.0 | 'Agree? Disagree? Comments are open.' |
| 11.0–13.0 | End card: 'Your name on it. Our build behind it.' + DM 'PARTNER'. |

**Sound design:** 0.00 low tom hit with a sub; a 92 bpm pulse; softer toms under each statement; whoosh and a metallic click as the cards separate.

**Why it should stop the scroll:** 'Unpopular opinion' is a fight invitation, and telling agencies to stop doing something they sell is defensible but provocative, which drives comments. The payoff turns the argument into a partnership offer.

**QC:** 1080x1920, 30/1 fps, h264/aac, 13.0 s; loudest peak in the first 100 ms (-1.6 dBFS); 3.88% of pixels change between 0.0 s and 1.0 s; hook 6 words. Pass.

## 17. Viewer challenge: Any business

- **File:** `dxt-new-17-drop-your-website.mp4`, cover `covers/dxt-new-17-drop-your-website.png`, 12 s
- **Palette:** Gold-dominant
- **Hook (frame 0):** Drop your website. One honest note.
- **CTA (final 2 s):** Your link. Our honest note. Comment it, or DM 'NOTE' to keep it private.

| Time (s) | What happens |
|---|---|
| 0.0–1.6 | Frame 0: hook in gold and ivory; under it an empty URL field ('yourwebsite.com') with a blinking caret, and a gold arrow already bouncing down towards the comments. |
| 1.6–3.2 | 'We'll tell you the first thing a client notices.' |
| 3.2–4.4 | 'Usually, one of these:' |
| 4.4–8.6 | One per second, big, with a glass tap each: The headline. / The first photo. / How it looks on a phone. / How fast it opens. |
| 8.6–10.0 | 'One note. Straight answer.' |
| 10.0–12.0 | End card: 'Your link. Our honest note.' + comment it, or DM 'NOTE' to keep it private. |

**Sound design:** 0.00 a single glass tap with a light sub; F-major pad; a softer glass tap on each item; thud + crystal on the end card.

**Why it should stop the scroll:** A direct invitation with a concrete reward (a free, specific note on your own site) is hard to scroll past, and it is built for comments and DMs. It is about the viewer's site from the first word.

**For Karim to fill or confirm:** Karim must be ready to reply to every link posted; the reel promises one honest note

**QC:** 1080x1920, 30/1 fps, h264/aac, 12.0 s; loudest peak in the first 100 ms (-1.5 dBFS); 3.57% of pixels change between 0.0 s and 1.0 s; hook 6 words. Pass.

## 18. Insider truth: Dental practices

- **File:** `dxt-new-18-patients-notice.mp4`, cover `covers/dxt-new-18-patients-notice.png`, 13 s
- **Palette:** Near-monochrome, porcelain white and ivory
- **Hook (frame 0):** What your patients notice that you don't.
- **CTA (final 2 s):** See your clinic through their eyes. DM 'SMILE' for a patient's-eye look.

| Time (s) | What happens |
|---|---|
| 0.0–1.8 | Frame 0: a blurred dental clinic homepage; a magnifying lens is already gliding across it, everything inside the lens sharp. Hook at the top. |
| 1.8–3.2 | The lens lands on the hero image: 'A stock-photo smile.' |
| 3.2–4.6 | On the hours line: 'Hours that say call to confirm.' |
| 4.6–6.0 | On the booking line: 'No way to book after 5pm.' |
| 6.0–7.4 | On the map: 'A pin at the wrong entrance.' |
| 7.4–9.0 | Lens widens: 'Whether the site feels as clean as your clinic.' |
| 9.0–11.0 | 'They notice. Before the chair.' |
| 11.0–13.0 | End card: 'See your clinic through their eyes.' + DM 'SMILE'. |

**Sound design:** 0.00 a porcelain clink (clean, clinical, not a drill) over a light sub; air texture and a bright C-major pad; a smaller clink at every observation.

**Why it should stop the scroll:** 'That you don't' is a gentle insult to the owner's attention to detail, which is exactly what dentists pride themselves on. Every observation is specific and checkable on their own site tonight, with no invented data.

**For Karim to fill or confirm:** [phone] on the mockup's booking line (generic placeholder, not a real number)

**QC:** 1080x1920, 30/1 fps, h264/aac, 13.0 s; loudest peak in the first 100 ms (-1.6 dBFS); 0.74% of pixels change between 0.0 s and 1.0 s; hook 7 words. Pass.

## 19. End-first: Interior & furniture showrooms

- **File:** `dxt-new-19-one-decision-room.mp4`, cover `covers/dxt-new-19-one-decision-room.png`, 14 s
- **Palette:** Champagne accent; one continuous push-in
- **Hook (frame 0):** This took one decision.
- **CTA (final 2 s):** Make the one decision. DM 'ONE ROOM' to start.

| Time (s) | What happens |
|---|---|
| 0.0–1.8 | Frame 0: the finished, beautiful showroom homepage (a single styled room, warm light) is already slowly pushing in. Hook on a dark band above it. |
| 1.8–3.2 | 'Not more products.' |
| 3.2–4.6 | 'Not more pages.' |
| 4.6–5.6 | 'The decision:' |
| 5.6–7.2 | Champagne: 'Show one room. Perfectly.' |
| 7.2–9.4 | The push-in reaches the room; shoppable hotspots pulse on the sofa, lamp and rug with labels and a 'Shop this room' button. |
| 9.4–12.0 | 'Let them walk in before they visit.' |
| 12.0–14.0 | End card: 'Make the one decision.' + DM 'ONE ROOM'. |

**Sound design:** 0.00 a deep boom with a high shimmer tail (the size of a finished space); a soft C-major pad; ticks on the 'not' lines; a chime on the decision; three porcelain taps as hotspots appear.

**Why it should stop the scroll:** Opening on the finished result is the reward first, which earns the next three seconds, and 'one decision' is a riddle the viewer wants solved. No before/after: the reel is about the decision, not a comparison.

**QC:** 1080x1920, 30/1 fps, h264/aac, 14.0 s; loudest peak in the first 100 ms (-2.6 dBFS); 3.98% of pixels change between 0.0 s and 1.0 s; hook 4 words. Pass.

## 20. Wrong answers only: Coaches & consultants

- **File:** `dxt-new-20-wrong-answers-only.mp4`, cover `covers/dxt-new-20-wrong-answers-only.png`, 14 s
- **Palette:** Gold strikes on obsidian
- **Hook (frame 0):** Wrong answers only: why isn't it fixed?
- **CTA (final 2 s):** Ask us anything. Then decide. DM 'HONEST' to start.

| Time (s) | What happens |
|---|---|
| 0.0–1.25 | Frame 0: hook at the top; the first excuse, “I'm too busy.”, is already on screen with a gold strike racing through it. |
| 1.25–6.4 | Excuses stack and get struck through every 1.25 s: Clients find me on Instagram / It's fine for now / After my next launch / My nephew is on it. |
| 6.4–8.2 | The list falls away. 'The honest answer:' then, in gold and not struck: 'You don't know who to trust with it.' |
| 8.2–9.4 | 'Fair. Look at the work first.' |
| 9.4–12.0 | OUR BUILD: Karim Ahmed's full-stack developer portfolio (shown as it is), the kind of personal-brand site a consultant needs. |
| 12.0–14.0 | End card: 'Ask us anything. Then decide.' + DM 'HONEST'. |

**Sound design:** 0.00 marker strike (swish + knock) over a sub hit; a strike on every excuse; a 96 bpm pulse that drops out when the honest answer lands on a bigger hit and a crystal note; a pad under the rest.

**Why it should stop the scroll:** 'Wrong answers only' is a comment format people already play, and every excuse is one the viewer has said. The honest last answer (trust) is the real objection, and the CTA answers it directly.

**QC:** 1080x1920, 30/1 fps, h264/aac, 14.0 s; loudest peak in the first 100 ms (-2.0 dBFS); 2.67% of pixels change between 0.0 s and 1.0 s; hook 7 words. Pass.

## 21. Optical illusion: Events & weddings

- **File:** `dxt-new-21-your-eyes-lied.mp4`, cover `covers/dxt-new-21-your-eyes-lied.png`, 14 s
- **Palette:** Gold-dominant
- **Hook (frame 0):** Look again. Your eyes lied.
- **CTA (final 2 s):** Make them feel it before they arrive. DM 'EVENT' to start.

| Time (s) | What happens |
|---|---|
| 0.0–2.0 | Frame 0: an infinite tunnel of gold frames is already rushing towards the viewer; the brain reads depth. Hook on a dark band. |
| 2.0–3.2 | The tunnel slows: 'It's flat.' (it is only nested rectangles). |
| 3.2–6.0 | The frames slide apart and resolve, one by one, into a flat website layout: hero, four tiles and a button. |
| 6.0–7.2 | 'Your guests do this too.' |
| 7.2–8.6 | 'They feel the event before they arrive.' |
| 8.6–10.0 | The layout fills in as an event site: Save the date / Venue / Schedule / Gallery / Stay / RSVP. |
| 10.0–12.0 | OUR BUILD: Agora, an event management platform built for a university. |
| 12.0–14.0 | End card: 'Make them feel it before they arrive.' + DM 'EVENT'. |

**Sound design:** 0.00 a whoosh that already peaks on the first frame, on a sub; a sustained rush while the tunnel moves; a riser into a crystal note as it flattens; B-flat pad; little porcelain ticks as each tile fills.

**Why it should stop the scroll:** Depth illusions force a double take, so the viewer re-reads the frame instead of swiping, and 'your eyes lied' is a challenge. The resolve into a layout is the 'aha', and it maps straight onto how guests judge an event from its page.

**QC:** 1080x1920, 30/1 fps, h264/aac, 14.0 s; loudest peak in the first 100 ms (-1.9 dBFS); 6.23% of pixels change between 0.0 s and 1.0 s; hook 5 words. Pass.

## 22. Direct question with a number: Logistics & B2B

- **File:** `dxt-new-22-seconds-your-homepage-gets.mp4`, cover `covers/dxt-new-22-seconds-your-homepage-gets.png`, 13 s
- **Palette:** Near-monochrome with one gold numeral
- **Hook (frame 0):** How many seconds does your homepage get?
- **CTA (final 2 s):** Make the first ten seconds sell. DM 'QUOTE' to start.

| Time (s) | What happens |
|---|---|
| 0.0–1.8 | Frame 0: the question on top; below it a stopwatch whose hand is already sweeping and whose readout is already counting up. |
| 1.8–3.0 | 'Guess before the answer.' (the loop is explicit) |
| 3.0–4.4 | 'A buyer is comparing suppliers.' |
| 4.4–5.8 | 'Five tabs. One shortlist.' |
| 5.8–9.4 | 'In those seconds they look for:' What you move. / Where you cover. / How to get a quote. |
| 9.4–11.0 | The stopwatch stops on the answer in gold: '10–20 s', sourced on screen: Nielsen Norman Group, users often leave web pages within 10–20 seconds. |
| 11.0–13.0 | End card: 'Make the first ten seconds sell.' + DM 'QUOTE'. |

**Sound design:** 0.00 a clean sonar-style ping on a sub; a soft tick every second like a stopwatch; a 60 bpm heartbeat pulse; clicks on text; a thud and a lower ping on the answer.

**Why it should stop the scroll:** A direct, answerable question with a number makes the viewer guess, and a guess is an investment they want to check. The answer is a published, citable figure, not an invented one.

**For Karim to fill or confirm:** Source on screen: Jakob Nielsen, 'How Long Do Users Stay on Web Pages?' (Nielsen Norman Group, 2011). Keep the wording 'often'

**QC:** 1080x1920, 30/1 fps, h264/aac, 13.0 s; loudest peak in the first 100 ms (-1.5 dBFS); 4.2% of pixels change between 0.0 s and 1.0 s; hook 7 words. Pass.

## 23. Luxury code: Premium & luxury brands

- **File:** `dxt-new-23-luxury-never-shows.mp4`, cover `covers/dxt-new-23-luxury-never-shows.png`, 13 s
- **Palette:** Near-monochrome, maximum negative space
- **Hook (frame 0):** What luxury homepages never show.
- **CTA (final 2 s):** Say less. Mean more. DM 'QUIET LUXURY' to start.

| Time (s) | What happens |
|---|---|
| 0.0–1.2 | Frame 0: a cluttered homepage (discount banner, five buttons, shouting headline); a pop-up is already sliding off the page. |
| 1.2–2.6 | 'Discount banners.' The banner lifts away. |
| 2.6–4.0 | 'Five buttons fighting.' Four of them drop out. |
| 4.0–5.4 | 'Pop-ups in the first second.' (the one we just saw leave) |
| 5.4–6.8 | 'Exclamation marks!' The marks fall off the headline. |
| 6.8–8.2 | What is left: a serif name, one image, one quiet link. Lots of space. |
| 8.2–9.6 | 'They leave space.' |
| 9.6–11.0 | 'Space reads as confidence.' |
| 11.0–13.0 | End card: 'Say less. Mean more.' + DM 'QUIET LUXURY'. |

**Sound design:** 0.00 a single crystal-bowl strike over a soft thud, with a short whoosh for the pop-up leaving; a whoosh and click for each removal; air only otherwise; a higher crystal note when the page goes quiet.

**Why it should stop the scroll:** 'Never' plus 'luxury' promises insider knowledge, and the viewer is shown a page that looks like many real ones, so they check their own. The reel itself practises the point: it gets quieter as it goes.

**QC:** 1080x1920, 30/1 fps, h264/aac, 13.0 s; loudest peak in the first 100 ms (-1.3 dBFS); 9.16% of pixels change between 0.0 s and 1.0 s; hook 5 words. Pass.

## 24. Mobile thumb test: Food delivery & cloud kitchens

- **File:** `dxt-new-24-tap-cost-an-order.mp4`, cover `covers/dxt-new-24-tap-cost-an-order.png`, 12 s
- **Palette:** Gold on obsidian with warm food tones
- **Hook (frame 0):** That tap just cost you an order.
- **CTA (final 2 s):** Make every tap an order. DM 'ORDER' to start.

| Time (s) | What happens |
|---|---|
| 0.0–1.0 | Frame 0: a thumb is mid-tap on a tiny '+' button on a delivery menu; it lands a few pixels off and opens the wrong item. |
| 1.0–1.8 | The wrong item sheet slides up: the order did not happen. |
| 1.8–3.2 | 'The button is smaller than a thumb.' |
| 3.2–5.0 | The button is outlined and measured: 'Apple's guideline: tap targets of at least 44 pt.' |
| 5.0–6.2 | 'Hungry people don't try twice.' |
| 6.2–8.4 | Rebuilt menu: full-width 'Add to order' buttons; the thumb taps once, a check and 'Added' appear inside the app. |
| 8.4–10.0 | 'Design for thumbs, not cursors.' |
| 10.0–12.0 | End card: 'Make every tap an order.' + DM 'ORDER'. |

**Sound design:** 0.00 a dull thock of a fingertip on glass over a sub; a low thud on the miss; a swish as the wrong sheet slides up; a 104 bpm pulse; a clean thock + chime on the successful tap.

**Why it should stop the scroll:** Everyone has mis-tapped a tiny button, so the frame is instantly felt, and 'cost you an order' turns a design detail into lost revenue. The 44 pt minimum is Apple's published guideline, not an invented figure.

**QC:** 1080x1920, 30/1 fps, h264/aac, 12.0 s; loudest peak in the first 100 ms (-1.6 dBFS); 4.64% of pixels change between 0.0 s and 1.0 s; hook 7 words. Pass.

## 25. Prediction: Retail chains

- **File:** `dxt-new-25-customers-will-expect.mp4`, cover `covers/dxt-new-25-customers-will-expect.png`, 13 s
- **Palette:** Obsidian with a deep-emerald accent
- **Hook (frame 0):** By next year, customers will expect this.
- **CTA (final 2 s):** Be the chain that's ready. DM 'BRANCHES' to start.

| Time (s) | What happens |
|---|---|
| 0.0–1.8 | Frame 0: labelled OUR PREDICTION, the hook over an abstract city map; three branch pins glow and a radius ring is already expanding from the shopper's location. |
| 1.8–3.2 | 'Not call the branch.' |
| 3.2–4.8 | 'Live stock. Nearest branch. Reserve.' |
| 4.8–6.4 | A product card slides up over the map: 'In stock at [branch]', with Reserve and Directions. |
| 6.4–8.0 | 'Reserve now. Pick up today.' |
| 8.0–9.6 | 'An opinion, not a fact. Watch this space.' |
| 9.6–11.0 | 'The chains that build it first set the standard.' |
| 11.0–13.0 | End card: 'Be the chain that's ready.' + DM 'BRANCHES'. |

**Sound design:** 0.00 a bright chime chord on a sub (a 'reveal' sound); D-minor pad; a faint radar ping each time the ring expands; clicks on each line; a metallic click as the card lands.

**Why it should stop the scroll:** Predictions trigger a 'will it?' reaction and invite disagreement in the comments; owners of chains fear being the one that looks behind. It is labelled as opinion on screen twice.

**For Karim to fill or confirm:** [branch] on the product-card mockup

**QC:** 1080x1920, 30/1 fps, h264/aac, 13.0 s; loudest peak in the first 100 ms (-1.7 dBFS); 6.34% of pixels change between 0.0 s and 1.0 s; hook 7 words. Pass.

## 26. Arabic hook (Egyptian dialect): Egyptian SMEs

- **File:** `dxt-new-26-arabic-mesh-bayen.mp4`, cover `covers/dxt-new-26-arabic-mesh-bayen.png`, 14 s
- **Palette:** Gold-dominant
- **Hook (frame 0):** محلك حلو، بس مش باين  (EN subtitle: Your shop is great, but nobody can see it.)
- **CTA (final 2 s):** ابعتلنا كلمة «ابدأ» : DM us 'START' (ابدأ) to begin.

| Time (s) | What happens |
|---|---|
| 0.0–1.8 | Frame 0: the Egyptian Arabic hook in large Cairo type, correctly joined and right-to-left, with the English subtitle under it; a spotlight is already sweeping across a dark gold-line shopfront. |
| 1.8–3.6 | الناس بتدوّر على الموبايل الأول / People search on their phone first. |
| 3.6–5.4 | وإنت عارف قيمتك كويس / You know exactly what you're worth. |
| 5.4–7.2 | بس الزبون لسه ما يعرفهاش / But the customer doesn't know it yet. |
| 7.2–9.4 | The shopfront lights up gold and a website frame forms around it: خلّيها تبان من أول نظرة / Make it show at first glance. |
| 9.4–12.0 | موقع معمول على مقاسك / A website made to measure. |
| 12.0–14.0 | End card in Arabic: ابعتلنا كلمة «ابدأ» / DM us the word START, in Arabic or English. |

**Sound design:** 0.00 a deep darbuka doum over a sub; a quiet maqsum rhythm (doum-tek) underneath at about 104 bpm; D-minor pad; a boom with shimmer when the shop lights up.

**Why it should stop the scroll:** Egyptian dialect in the first frame tells local owners this is for them, not a translated foreign ad. 'Your shop is great' flatters before it stings, and 'nobody can see it' is the open loop.

**QC:** 1080x1920, 30/1 fps, h264/aac, 14.0 s; loudest peak in the first 100 ms (-1.4 dBFS); 3.57% of pixels change between 0.0 s and 1.0 s; hook 5 words. Pass.

## Placeholders and claims to confirm

- Reel 02: [price] on the menu-card mockup (leave as a dash or a real menu price if Karim prefers)
- Reel 07: 'Book a free trial' is a generic checklist item; change it if the client offers no trial
- Reel 08: [rate] on the rebuilt-page mockup
- Reel 08: The session timer is labelled 'illustrative session' on screen
- Reel 12: The counter is illustrative and labelled so; Karim can replace it with a client's real enquiry figure only if he has one
- Reel 17: Karim must be ready to reply to every link posted; the reel promises one honest note
- Reel 18: [phone] on the mockup's booking line (generic placeholder, not a real number)
- Reel 22: Source on screen: Jakob Nielsen, 'How Long Do Users Stay on Web Pages?' (Nielsen Norman Group, 2011). Keep the wording 'often'
- Reel 25: [branch] on the product-card mockup

Every other statement is a general observation or opinion (labelled as such in reels 16 and 25).
No statistics, client names, results, testimonials or prices are invented. The only figures used are
Apple's published 44 pt minimum tap target (reel 24) and Nielsen Norman Group's 10–20 seconds (reel 22),
both cited on screen. Reel 12's counter is labelled 'illustrative, not real data' on screen.

## Arabic (reel 26)

Arabic is set in Cairo and shaped by HarfBuzz with FriBiDi (Pillow's libraqm layout, direction rtl),
so letters join and run right to left. arabic-reshaper + python-bidi was tried first, but it maps letters
to Unicode presentation forms that the web-subset Cairo font does not contain (every letter came out as a
box), so the full shaping engine is used instead. Checked visually on frames 0, 3, 8 and 13 s.
