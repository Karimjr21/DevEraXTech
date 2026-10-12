"""Reels 01-09."""
import math

import sfx
from dx import *  # noqa: F401,F403
from dx import C, SCX, SX0, SX1, SY0, W, H
from . import reel

SIN = math.sin


def tick_beats(m, times, kind=None, gain=0.22):
    for tt in times:
        m.add((kind or sfx.click)(), tt, gain)


def end_sting(m, t, gain=0.35):
    m.add(sfx.low_thud(), t, gain)
    m.add(sfx.crystal(2.0, 1318.5), t + 0.05, gain * 0.35)


# =====================================================================  01  clinics
def a01(m):
    m.add(sfx.piano_stab(2.4), 0, 1.0)
    m.add(sfx.bass_hit(), 0, 0.55)
    m.bed(sfx.pad(13, "am", 700), 0.09)
    tick_beats(m, [1.6, 3.0, 4.4, 5.0, 6.0, 7.0])
    m.add(sfx.whoosh(0.5), 7.7, 0.22)
    end_sting(m, 11.0)


M01 = dict(
    type="Mid-sentence start", industry="Clinics & doctors", palette="Near-monochrome: ivory on obsidian, gold only on the turn",
    hook="…so they booked the clinic next door.",
    beats=[
        ("0.0–1.6", "Frame 0: hook already on screen, left-aligned as if it is the end of a sentence; a speech waveform is mid-flow and the line drifts left (we joined late)."),
        ("1.6–3.0", "Cut: 'Same skill. Similar prices.'"),
        ("3.0–4.4", "Gold: 'So why them?' (the open loop)."),
        ("4.4–8.0", "Phone mockup of a clinic site. 'Their website answered first:' then three patient questions tick off, one per second: Who will treat me? / When can I come? / How do I book? Each highlights that part of the page."),
        ("8.0–10.8", "OUR BUILD: CalmCare Therapy Center, with its real headline 'Personalised support for every care journey.' in a browser frame."),
        ("10.8–13.0", "End card: 'Be the clinic next door.' + DM 'CLINIC' + DeveraXTech wordmark + @deveraxtech. Last words echo the hook, so the loop lands."),
    ],
    sound="0.00 piano chord stab cut in mid-phrase over a sub hit (sounds like we dropped into the middle of something); quiet A-minor pad; soft clicks on every text change; whoosh into the build; low thud + crystal on the end card.",
    cta="Be the clinic next door. DM 'CLINIC' to start.",
    why="The ellipsis and lower-case start make the brain look for the missing first half, and 'the clinic next door' is a competitor every clinic owner already resents. The viewer stays to learn why patients chose the other clinic.",
)


def clinic_phone_screen(im, sb, t, focus):
    x0, y0, x1, y1 = sb
    w = x1 - x0
    scroll = -14 * SIN(t * 0.8)
    top = y0 + 70 + scroll
    rect(im, (x0 + 40, top, x0 + 180, top + 16), C["ink"])
    rect(im, (x1 - 120, top, x1 - 40, top + 16), (190, 180, 160))
    # hero
    photo(im, (x0 + 30, top + 60, x1 - 30, top + 300), (226, 218, 202), (198, 186, 160), radius=22)
    txt(im, "Care that", x0 + 60, top + 150, "serif", 46, 600, C["ink"], "lm")
    txt(im, "listens.", x0 + 60, top + 205, "serif_i", 46, 500, C["ink"], "lm")
    # doctor card
    dy = top + 340
    rrect(im, (x0 + 30, dy, x1 - 30, dy + 150), 22, C["white"], (215, 205, 188), 2)
    circle(im, x0 + 100, dy + 75, 42, fill=(205, 192, 168))
    bars(im, x0 + 165, dy + 50, w - 230, 3, 26, 12, (150, 140, 122), 0.7)
    # slots
    sy = dy + 190
    for i in range(6):
        cx0 = x0 + 30 + (i % 3) * ((w - 60) / 3)
        cy0 = sy + (i // 3) * 74
        hot = focus == 1 and i == 4
        rrect(im, (cx0 + 6, cy0, cx0 + (w - 60) / 3 - 6, cy0 + 60), 16, C["gold"] if hot else C["white"],
              (215, 205, 188), 2)
        txt(im, ["9:00", "10:30", "12:00", "15:00", "16:30", "18:00"][i], cx0 + (w - 60) / 6, cy0 + 30, "sans", 24, 600,
            C["obs"] if hot else (110, 102, 88))
    # book
    by = sy + 180
    button(im, (x0 + 30, by, x1 - 30, by + 84), "Book a visit", C["ink"] if focus != 2 else C["gold"],
           C["ivory"] if focus != 2 else C["obs"], 30)
    boxes = [(x0 + 22, dy - 8, x1 - 22, dy + 158), (x0 + 22, sy - 10, x1 - 22, sy + 144), (x0 + 22, by - 8, x1 - 22, by + 92)]
    if focus is not None and 0 <= focus < 3:
        rrect(im, boxes[focus], 28, None, C["gold"], 4)


@reel(1, "clinic-next-door", 13.0, a01, M01, qc=[2.0, 3.5, 5.5, 9.0, 12.0])
def r01(t):
    im = bg(C["obs"], (27, 25, 22))
    if t < 4.4:
        a = win(t, -1, 4.4, 0, 0.25)
        for i in range(30):
            h = 10 + 52 * abs(SIN(t * 7.3 + i * 0.9) * SIN(t * 3.1 + i * 0.37))
            x = SX0 + 22 + i * 17
            rrect(im, (x, 470 - h / 2, x + 7, 470 + h / 2), 3, C["muted"], alpha=0.7 * a)
    if t < 1.6:
        dxo = -16 * t
        size = fit_size("…so they booked", "serif", 600, 820, 116)
        for i, (s, col) in enumerate([("…so they booked", C["ivory"]), ("the clinic", C["ivory"]), ("next door.", C["champ"])]):
            txt(im, s, SX0 + 44 + dxo, 640 + i * size * 1.12, "serif", size, 600, col, "lm")
    say(im, t, 1.6, 3.0, ("Same skill.", "Similar prices."), 820, 100)
    if 3.0 <= t < 4.4:
        glow_txt(im, "So why them?", SCX, 820, "serif", 120, 600, C["gold"], win(t, 3.0, 4.4, 0.12, 0.12))
    if 4.4 <= t < 8.0:
        a = win(t, 4.4, 8.0, 0.2, 0.2)
        say(im, t, 4.4, 8.0, "Their website answered first:", 300, 52, C["champ"], fi=0.2)
        qs = ["Who will treat me?", "When can I come?", "How do I book?"]
        focus = None
        for i, q in enumerate(qs):
            if 5.0 + i <= t < 6.0 + i:
                focus = i
            say(im, t, 5.0 + i, 6.0 + i if i < 2 else 8.0, q, 400, 56, C["gold"], "serif_i", 500)
        k = eo(prog(t, 4.4, 4.9))
        sb = phone(im, SCX, 960 + (1 - k) * 80, 470, 900, screen=C["ivory"], alpha=a)
        clinic_phone_screen(im, sb, t, focus)
        if a < 1:
            rect(im, (0, 500, W, 1430), C["obs"], 1 - a)
    if 7.8 <= t < 10.9:
        a = win(t, 7.8, 10.9, 0.25, 0.2)
        eyebrow(im, "Our build", SCX, 400, alpha=a)
        txt(im, "CalmCare Therapy Center", SCX, 470, "serif", 60, 600, C["ivory"], alpha=a)
        s = 0.96 + 0.04 * eo(prog(t, 7.8, 10.9))
        bx = (SX0 + 10, 560, SX1 - 10, 1330)
        inner = browser(im, bx, "light", a)
        x0, y0, x1, y1 = inner
        rrect(im, (x0 + 40, y0 + 40, x0 + 420, y0 + 84), 22, (252, 244, 248), (230, 210, 222), 2, a)
        txt(im, "For more considered pain care", x0 + 60, y0 + 62, "sans", 22, 600, (132, 58, 98), "lm", a)
        txt(im, "Personalised support", x0 + 40, y0 + 160, "serif", 58 * s, 600, (49, 42, 53), "lm", a)
        txt(im, "for every", x0 + 40, y0 + 228, "serif_i", 58 * s, 500, (180, 40, 110), "lm", a)
        txt(im, "care journey.", x0 + 40, y0 + 296, "serif", 58 * s, 600, (49, 42, 53), "lm", a)
        bars(im, x0 + 40, y0 + 360, x1 - x0 - 120, 3, 28, 12, (150, 140, 150), 0.5 * a)
        button(im, (x0 + 40, y0 + 470, x0 + 330, y0 + 540), "Request a demo", (49, 42, 53), C["white"], 24, a)
        button(im, (x0 + 350, y0 + 470, x0 + 620, y0 + 540), "Secure log in", C["white"], (49, 42, 53), 24, a,
               outline=(200, 190, 200))
        rrect(im, (x0 + 40, y0 + 580, x1 - 40, y1 - 30), 22, (247, 245, 248), (232, 225, 234), 2, a)
        say(im, t, 8.2, 10.9, "Calm. Clear. Bookable.", 1420, 46, C["champ"], "serif_i", 500)
    endcard(im, t, 11.0, ("Be the clinic", "next door."), "DM 'CLINIC' to start")
    return im


# =====================================================================  02  restaurants
def a02(m):
    m.add(sfx.bass_hit(1.0, 160, 45), 0, 0.85)
    m.add(sfx.tick(), 0, 1.0)
    m.add(sfx.tick(), 1.0, 0.7)
    m.add(sfx.tick(), 2.0, 0.7)
    m.add(sfx.low_thud(0.8), 3.0, 0.75)
    m.add(sfx.tape_stop(0.4), 3.0, 0.25)
    m.bed(sfx.pulse_bed(12, 120, 55), 0.15, start=4.6, end=10.0)
    tick_beats(m, [4.6, 5.8, 6.9, 8.0, 9.4])
    end_sting(m, 10.0)


M02 = dict(
    type="Hard countdown", industry="Restaurants & cafés", palette="Gold-dominant",
    hook="Your menu has 3 seconds.",
    beats=[
        ("0.0–3.0", "Frame 0: a huge gold 3 inside a ring that is already draining; 3…2…1 snap on each second with a hard tick. Hook sits above it the whole time."),
        ("3.0–4.6", "Zero: '0' hits with a thud and tape-stop; 'At zero, they order elsewhere.' (what happens at zero)."),
        ("4.6–5.8", "'In 3 seconds they need:'"),
        ("5.8–9.4", "A menu card builds in three hits: 1 the dish (photo), 2 the price, visible ([price] placeholder), 3 one order button."),
        ("9.4–10.0", "'Everything else can wait.'"),
        ("10.0–12.0", "End card: 'Let the dish speak first.' + DM 'MENU'. Cuts back to the running 3 on loop."),
    ],
    sound="0.00 woodblock-style clock tick on top of a short sub hit; ticks at 1.0 and 2.0; at 3.0 a low thud with a short tape-stop; a quiet 120 bpm sub pulse under the menu build; clicks per hit; thud + crystal on the end card.",
    cta="Let the dish speak first. DM 'MENU' to start.",
    why="A countdown that is already running is the strongest frame-0 motion there is, and the number in the hook is literally ticking. The viewer waits to see what happens at zero.",
    placeholders=["[price] on the menu-card mockup (leave as a dash or a real menu price if Karim prefers)"],
)


def ring(im, cx, cy, r, frac, color, width=10, alpha=1.0):
    arc(im, cx, cy, r, 0, 360, C["line"], width, alpha)
    if frac > 0:
        arc(im, cx, cy, r, -90, -90 + 360 * frac, color, width, alpha)


@reel(2, "menu-three-seconds", 12.0, a02, M02, qc=[1.5, 3.2, 6.0, 8.5, 11.0])
def r02(t):
    im = bg(C["obs"], (34, 28, 14), cy=900)
    if t < 3.0:
        sec = int(t)
        frac = 1 - (t - sec)
        n = 3 - sec
        s = 1 + 0.07 * (1 - eo(prog(t - sec, 0, 0.22)))
        ring(im, SCX, 950, 330, frac, C["gold"], 12)
        glow_txt(im, str(n), SCX, 930, "serif", int(520 * s), 700, C["gold"], 1.0, 30, 0.7)
        txt(im, "Your menu has", SCX, 380, "serif", 84, 600, C["ivory"])
        txt(im, "3 seconds.", SCX, 480, "serif", 84, 600, C["gold_l"])
    elif t < 4.6:
        a = win(t, 3.0, 4.6, 0, 0.15)
        txt(im, "0", SCX, 600, "serif", 260, 700, C["gold_d"], alpha=a * (1 - prog(t, 3.0, 3.5) * 0.6))
        say(im, t, 3.15, 4.6, ("At zero, they", "order elsewhere."), 1000, 96)
    say(im, t, 4.6, 5.8, ("In 3 seconds", "they need:"), 860, 96, C["champ"])
    if 5.8 <= t < 9.4:
        a = win(t, 5.8, 9.4, 0.15, 0.15)
        labels = ["1  The dish", "2  The price, visible", "3  One button"]
        step = 0 if t < 6.9 else 1 if t < 8.0 else 2
        say(im, t, [5.8, 6.9, 8.0][step], [6.9, 8.0, 9.4][step], labels[step], 380, 60, C["gold"], "sans", 600, fi=0.1)
        box = (SX0 + 40, 500, SX1 - 40, 1420)
        rrect(im, box, 36, C["obs2"], C["gold_d"], 2, a)
        # dish photo (abstract plate)
        k1 = eo(prog(t, 5.8, 6.2))
        photo(im, (box[0] + 30, 530, box[2] - 30, 530 + 470 * k1), (60, 42, 20), (24, 18, 10), a)
        if k1 > 0.5:
            circle(im, SCX, 765, 170, fill=(235, 226, 206), alpha=a)
            circle(im, SCX, 765, 120, fill=(196, 120, 52), alpha=a)
            circle(im, SCX - 30, 740, 40, fill=(122, 150, 70), alpha=a)
            circle(im, SCX + 40, 790, 30, fill=(214, 168, 70), alpha=a)
        if t >= 6.9:
            k = eo(prog(t, 6.9, 7.2))
            txt(im, "Signature dish", box[0] + 50, 1070, "serif", 58, 600, C["ivory"], "lm", a * k)
            txt(im, "[price]", box[2] - 50, 1070, "serif", 58, 600, C["gold_l"], "rm", a * k)
            bars(im, box[0] + 50, 1130, box[2] - box[0] - 100, 2, 26, 12, C["muted"], 0.5 * a * k)
        if t >= 8.0:
            k = eback(prog(t, 8.0, 8.35))
            cy = 1300
            hw = (box[2] - box[0] - 100) / 2 * k
            button(im, (SCX - hw, cy - 50, SCX + hw, cy + 50), "Order now" if k > 0.6 else "", C["gold"], C["obs"], 36, a)
    say(im, t, 9.4, 10.0, ("Everything else", "can wait."), 860, 96, fo=0.1)
    endcard(im, t, 10.0, ("Let the dish", "speak first."), "DM 'MENU' to start")
    return im


# =====================================================================  03  law firms
def a03(m):
    m.add(sfx.knock(), 0, 1.0)
    m.add(sfx.bass_hit(0.9, 120, 40), 0, 0.5)
    m.bed(sfx.pad(13, "dm", 600), 0.1)
    tick_beats(m, [1.7, 3.2, 4.8, 6.4], sfx.knock, 0.25)
    tick_beats(m, [8.0, 8.7, 9.4, 10.1])
    end_sting(m, 11.0)


M03 = dict(
    type="Industry callout", industry="Law firms", palette="Near-monochrome: ivory serif on obsidian, gold hairlines",
    hook="LAWYERS: clients decide before the first call.",
    beats=[
        ("0.0–1.7", "Frame 0: 'LAWYERS:' in large tracked capitals, the rest of the hook under it; a gold rule is sweeping under the word and the frame is slowly pushing in; faint gold pillars drift behind."),
        ("1.7–3.2", "'Not in your office.'"),
        ("3.2–4.8", "'On a phone screen. In seconds.'"),
        ("4.8–6.4", "Uncomfortable truth in gold: 'They can't judge your legal skill.'"),
        ("6.4–8.0", "'So they judge what they can see.'"),
        ("8.0–10.8", "Roman-numbered list snaps in: I Clarity / II Credentials / III Who they'll speak to / IV How fast they can reach you."),
        ("10.8–13.0", "End card: 'Be chosen before the first call.' + DM 'COUNSEL'."),
    ],
    sound="0.00 dry wooden knock layered with a sub hit (formal, not a cartoon gavel); D-minor pad; softer knocks on each statement; clicks on the list; thud + crystal on the end card.",
    cta="Be chosen before the first call. DM 'COUNSEL' to begin.",
    why="The first word is the viewer's job title, so lawyers self-select in a quarter of a second, and the rest of the line threatens their pipeline. 'They can't judge your legal skill' is true and uncomfortable, which keeps them through the middle.",
)


@reel(3, "lawyers-before-the-call", 13.0, a03, M03, qc=[0.9, 4.0, 5.5, 9.5, 12.0])
def r03(t):
    im = bg(C["obs"], (22, 21, 19))
    for i in range(7):
        x = (i * 170 + t * 9) % (W + 170) - 85
        line(im, [(x, 0), (x, H)], C["gold_d"], 1, 0.12)
    if t < 1.7:
        s = 1 + 0.025 * eio(t / 1.7)
        txt(im, "LAWYERS:", SCX, 560, "serif", int(150 * s), 700, C["ivory"], tracking=8)
        k = 0.35 + 0.65 * eo(t / 0.7)
        hw = 380 * k * s
        hline(im, SCX - hw, SCX + hw, 680, C["gold"], 3)
        txt(im, "clients decide", SCX, 790, "serif", int(84 * s), 500, C["champ"])
        txt(im, "before the first call.", SCX, 890, "serif", int(84 * s), 500, C["champ"])
    say(im, t, 1.7, 3.2, "Not in your office.", 820, 100)
    say(im, t, 3.2, 4.8, ("On a phone screen.", "In seconds."), 820, 96)
    say(im, t, 4.8, 6.4, ("They can't judge", "your legal skill."), 820, 100, C["gold"])
    say(im, t, 6.4, 8.0, ("So they judge", "what they can see."), 820, 100)
    if 8.0 <= t < 10.9:
        a = win(t, 8.0, 10.9, 0.1, 0.2)
        items = [("I", "Clarity."), ("II", "Credentials."), ("III", "Who they'll speak to."), ("IV", "How fast they can reach you.")]
        for i, (r, s) in enumerate(items):
            ti = 8.0 + i * 0.7
            if t >= ti:
                k = eo(prog(t, ti, ti + 0.25))
                y = 560 + i * 170
                txt(im, r, SX0 + 40, y, "serif", 54, 600, C["gold"], "lm", a * k)
                txt(im, s, SX0 + 160 - (1 - k) * 30, y, "serif", fit_size(s, "serif", 600, 680, 62), 600, C["ivory"], "lm", a * k)
                hline(im, SX0 + 40, SX1 - 20, y + 70, C["line"], 1, a * k)
    endcard(im, t, 11.0, ("Be chosen before", "the first call."), "DM 'COUNSEL' to begin")
    return im


# =====================================================================  04  e-commerce
def a04(m):
    m.add(sfx.snap(), 0, 1.0)
    m.add(sfx.bass_hit(0.8, 150, 48), 0, 0.6)
    m.add(sfx.swish(), 0.05, 0.3)
    m.bed(sfx.pad(13, "em", 800), 0.08)
    tick_beats(m, [1.8, 3.0])
    tick_beats(m, [4.0, 4.55, 5.1, 5.65], sfx.keytap, 0.4)
    m.add(sfx.low_thud(), 6.4, 0.3)
    m.add(sfx.whoosh(0.5), 7.6, 0.25)
    m.add(sfx.metal_click(), 8.3, 0.4)
    tick_beats(m, [9.6])
    end_sting(m, 11.0)


M04 = dict(
    type="Myth bust", industry="E-commerce brands", palette="Obsidian with a deep-emerald accent",
    hook="It's not your price. It never was.",
    beats=[
        ("0.0–1.8", "Frame 0: the hook in three lines; a gold strike is already racing through the word 'price'."),
        ("1.8–3.0", "'They wanted it.'"),
        ("3.0–4.0", "'Then checkout asked for:'"),
        ("4.0–6.4", "Emerald form fields stack up fast with key taps: Create an account / Phone number / Address (again) / Promo code?"),
        ("6.4–7.8", "'Every extra step is a reason to leave.'"),
        ("7.8–9.6", "The stack collapses into one emerald button: 'Buy in two taps' with a check."),
        ("9.6–11.0", "Gold: 'Fix the path, not the price.'"),
        ("11.0–13.0", "End card: 'Keep the price. Fix the path.' + DM 'STORE'."),
    ],
    sound="0.00 finger-snap crack with a sub hit and a short swish (the strike); emerald E-minor pad; mechanical key taps as fields pile up; a low thud when the point lands; metal click as the button forms.",
    cta="Keep the price. Fix the path. DM 'STORE' to rebuild your checkout.",
    why="Every store owner's private fear is that they are too expensive. Opening by striking that belief out is a relief and a provocation at once, and the obvious next question is 'then what is it?'.",
)


@reel(4, "not-your-price", 13.0, a04, M04, push=1.8, qc=[0.2, 2.2, 5.5, 8.8, 10.0, 12.0])
def r04(t):
    im = bg(C["obs"], (12, 30, 25))
    if t < 1.8:
        size = 104
        txt(im, "It's not", SCX, 620, "serif", size, 600, C["ivory"])
        w1 = text_w("your ", "serif", size, 600)
        wl = text_w("your price.", "serif", size, 600)
        wp = text_w("price", "serif", size, 600)
        x0 = SCX - wl / 2
        txt(im, "your price.", SCX, 745, "serif", size, 600, C["ivory"])
        k = 0.3 + 0.7 * eo(t / 0.45)
        strike(im, x0 + w1 - 6, x0 + w1 + wp + 10, 752, k, C["gold"], 8)
        txt(im, "It never was.", SCX, 900, "serif_i", 92, 500, C["emer_l"])
    say(im, t, 1.8, 3.0, "They wanted it.", 820, 110)
    say(im, t, 3.0, 4.0, ("Then checkout", "asked for:"), 820, 100, C["champ"])
    if 4.0 <= t < 9.6:
        a = win(t, 4.0, 9.6, 0.1, 0.2)
        fields = ["Create an account", "Phone number", "Address (again)", "Promo code?"]
        collapse = eio(prog(t, 7.8, 8.3))
        for i, f in enumerate(fields):
            ti = 4.0 + i * 0.55
            if t < ti:
                continue
            k = eback(prog(t, ti, ti + 0.25))
            y = 560 + i * 170
            y = y + (980 - y) * collapse
            hh = 60 * (1 - collapse)
            if hh > 2:
                rrect(im, (SX0 + 40, y - hh, SX1 - 40, y + hh), 22, C["obs2"], C["emer_l"], 3, a * min(1, k))
                txt(im, f, SX0 + 80, y, "sans", 40 * (0.6 + 0.4 * (1 - collapse)), 500, C["ivory"], "lm", a * (1 - collapse))
        say(im, t, 6.4, 7.8, ("Every extra step is", "a reason to leave."), 1350, 56, C["gold_l"])
        if t >= 8.1:
            k = eback(prog(t, 8.1, 8.5))
            hw = (SX1 - SX0 - 80) / 2 * k
            button(im, (SCX - hw, 920, SCX + hw, 1040), "Buy in two taps" if k > 0.7 else "", C["emer"], C["ivory"], 44, a)
            check(im, SCX, 1170, 70, C["gold"], prog(t, 8.5, 8.9), 8, a)
    say(im, t, 9.6, 11.0, ("Fix the path,", "not the price."), 820, 104, C["gold"])
    endcard(im, t, 11.0, ("Keep the price.", "Fix the path."), "DM 'STORE' to rebuild your checkout", C["gold"])
    return im


# =====================================================================  05  real estate developers
def tower_strokes():
    """Gold line drawing of a two-tower development, in a 1000-unit box (x -500..500, y 0..-1000)."""
    S = []
    S.append([(-480, 0), (480, 0)])  # ground
    # main tower
    S.append([(-150, 0), (-150, -900), (-40, -980), (150, -900), (150, 0)])
    for y in range(-80, -900, -70):
        S.append([(-150, y), (150, y)])
    S.append([(-40, -980), (-40, -1040)])
    for x in (-75, 0, 75):
        S.append([(x, -10), (x, -880)])
    # second tower
    S.append([(190, 0), (190, -560), (380, -620), (380, 0)])
    for y in range(-70, -560, -70):
        S.append([(190, y), (380, y - 25 * (y / -560))])
    # podium and canopy
    S.append([(-420, 0), (-420, -160), (-150, -160)])
    S.append([(-420, -160), (-460, -180)])
    S.append([(-360, 0), (-360, -110), (-220, -110), (-220, 0)])
    # trees
    for x in (-470, 430):
        S.append([(x, 0), (x, -60)])
    return S


_STROKES = None


def draw_tower(im, k, ox, oy, sc, color=C["gold"], width=3, alpha=1.0, head=True):
    global _STROKES
    if _STROKES is None:
        _STROKES = tower_strokes()
    lens = [sum(math.dist(s[i], s[i + 1]) for i in range(len(s) - 1)) for s in _STROKES]
    total = sum(lens)
    target = total * clamp(k)
    acc = 0
    hp = None
    for s, L in zip(_STROKES, lens):
        if acc >= target:
            break
        f = 1.0 if acc + L <= target else (target - acc) / L
        pts, hp = poly_partial(s, f)
        line(im, [(ox + x * sc, oy + y * sc) for x, y in pts], color, width, alpha)
        acc += L
    if head and hp is not None and k < 1:
        hx, hy = ox + hp[0] * sc, oy + hp[1] * sc
        circle(im, hx, hy, 16, fill=C["gold_l"], alpha=0.25 * alpha)
        circle(im, hx, hy, 6, fill=C["white"], alpha=alpha)


def a05(m):
    m.add(sfx.nib_boom(), 0, 1.0)
    m.bed(sfx.pen_scratch(0.5) * 0.5, 0.05, start=0.2, end=10.5, fade=0.3)
    m.bed(sfx.pad(15, "fmaj", 900), 0.11)
    tick_beats(m, [2.0, 4.0, 6.0, 8.0], sfx.click, 0.18)
    m.add(sfx.boom_shimmer(), 10.5, 0.55)
    end_sting(m, 13.0)


M05 = dict(
    type="Unfinished object", industry="Real estate developers", palette="Gold-dominant line art on obsidian; one continuous move",
    hook="Your tower is finished. Your website isn't.",
    beats=[
        ("0.0–2.0", "Frame 0: a gold line drawing of a two-tower development is about a third drawn, the pen head glowing and moving. Hook above it."),
        ("2.0–4.0", "The drawing keeps going: 'Buyers tour it online first.'"),
        ("4.0–6.0", "'Renders. Floor plans. Payment plans.'"),
        ("6.0–8.0", "'One place. One feeling.'"),
        ("8.0–10.5", "'Finish the story.' The last strokes land."),
        ("10.5–13.0", "Payoff: the finished drawing settles into the hero of a luxury property site. OUR BUILD: Nilora Estates, 'Where the river meets the light.'"),
        ("13.0–15.0", "End card: 'Your tower deserves a finished site.' + DM 'TOWER'."),
    ],
    sound="0.00 low boom with a pen-nib scratch on top; a quiet scratch texture follows the pen; F-major pad; small clicks on text changes; boom + shimmer when the drawing completes; thud + crystal on the end card.",
    cta="Your tower deserves a finished site. DM 'TOWER' to start your property site.",
    why="An unfinished drawing makes the brain wait for completion (the Zeigarnik effect), and the hook tells developers the one part of their project that is still unfinished. The completion is the payoff.",
)


@reel(5, "tower-unfinished", 15.0, a05, M05, push=2.0, qc=[1.0, 5.0, 9.0, 11.5, 14.0])
def r05(t):
    im = bg(C["obs"], (30, 25, 14), cy=1000)
    k = 0.33 + 0.67 * eio(prog(t, 0, 10.5)) if t < 10.5 else 1.0
    mv = eio(prog(t, 10.5, 11.4))
    sc = 0.78 - 0.36 * mv
    ox = SCX
    oy = 1440 - (1440 - 1090) * mv
    if t < 13.0:
        a_draw = win(t, -1, 13.0, 0, 0.2)
        if t >= 10.5:
            a = win(t, 10.6, 13.0, 0.3, 0.2)
            eyebrow(im, "Our build", SCX, 330, alpha=a)
            txt(im, "Nilora Estates", SCX, 400, "serif", 64, 600, C["ivory"], alpha=a)
            bx = (SX0 + 10, 480, SX1 - 10, 1460)
            inner = browser(im, bx, "dark", a)
            x0, y0, x1, y1 = inner
            photo(im, (x0 + 20, y0 + 20, x1 - 20, y0 + 520), (70, 52, 30), (14, 12, 10), a)
            txt(im, "NILORA ESTATES", x0 + 50, y0 + 60, "sans", 22, 600, C["champ"], "lm", a, tracking=5)
            txt(im, "Where the river", x0 + 50, y0 + 610, "serif", 60, 600, C["ivory"], "lm", a)
            txt(im, "meets the light.", x0 + 50, y0 + 680, "serif_i", 60, 500, C["gold_l"], "lm", a)
            button(im, (x0 + 50, y0 + 750, x0 + 330, y0 + 815), "View residences", C["gold"], C["obs"], 24, a)
            button(im, (x0 + 350, y0 + 750, x0 + 620, y0 + 815), "Book a viewing", C["obs2"], C["ivory"], 24, a, C["gold_d"])
        draw_tower(im, k, ox, oy, sc, C["gold"], 3 if mv < 0.5 else 2, a_draw)
    if t < 2.0:
        txt(im, "Your tower is finished.", SCX, 330, "serif", fit_size("Your tower is finished.", "serif", 600, 840, 76), 600, C["ivory"])
        txt(im, "Your website isn't.", SCX, 425, "serif_i", 76, 500, C["gold_l"])
    say(im, t, 2.0, 4.0, ("Buyers tour it", "online first."), 380, 70)
    say(im, t, 4.0, 6.0, ("Renders. Floor plans.", "Payment plans."), 380, 66)
    say(im, t, 6.0, 8.0, "One place. One feeling.", 380, 70)
    say(im, t, 8.0, 10.5, "Finish the story.", 380, 76, C["gold_l"], "serif_i", 500)
    endcard(im, t, 13.0, ("Your tower deserves", "a finished site."), "DM 'TOWER' to start your property site")
    return im


# =====================================================================  06  jewelry & watches
TILES = [(SCX - 215, 640), (SCX + 215, 640), (SCX - 215, 980), (SCX + 215, 980), (SCX - 215, 1320), (SCX + 215, 1320)]
OFF = 3  # the tile that lands out of alignment
OFFSETS = [(-70, -40), (60, -55), (-55, 50), (75, 35), (-40, 70), (50, 60)]


def jewel_icon(im, i, cx, cy, a):
    g = C["champ"]
    if i == 0:  # ring
        circle(im, cx, cy + 10, 46, outline=g, width=5, alpha=a)
        with Vec(im) as d:
            d.polygon([cx - 18, cy - 40, cx, cy - 62, cx + 18, cy - 40, cx, cy - 26], pen(g, 3, a), brush(C["white"], a * 0.8))
    elif i == 1:  # watch
        rrect(im, (cx - 20, cy - 90, cx + 20, cy + 90), 10, None, g, 4, a)
        circle(im, cx, cy, 48, fill=C["obs"], outline=g, width=5, alpha=a)
        line(im, [(cx, cy), (cx, cy - 30)], g, 3, a)
        line(im, [(cx, cy), (cx + 22, cy + 8)], g, 3, a)
    elif i == 2:  # necklace
        arc(im, cx, cy - 50, 80, 20, 160, g, 4, a)
        circle(im, cx, cy + 36, 14, fill=C["gold_l"], alpha=a)
    elif i == 3:  # earrings
        for s in (-1, 1):
            circle(im, cx + s * 34, cy - 30, 10, outline=g, width=4, alpha=a)
            with Vec(im) as d:
                d.polygon([cx + s * 34, cy - 14, cx + s * 34 - 18, cy + 30, cx + s * 34, cy + 56, cx + s * 34 + 18, cy + 30],
                          pen(g, 3, a), None)
    elif i == 4:  # bracelet
        with Vec(im) as d:
            d.ellipse((cx - 70, cy - 34, cx + 70, cy + 34), pen(g, 6, a), None)
    else:  # pendant
        line(im, [(cx - 60, cy - 70), (cx, cy - 10), (cx + 60, cy - 70)], g, 3, a)
        with Vec(im) as d:
            d.polygon([cx, cy - 14, cx - 26, cy + 20, cx, cy + 60, cx + 26, cy + 20], pen(g, 3, a), brush(C["gold"], a * 0.5))


def tile_pos(i, t, fixed):
    cx, cy = TILES[i]
    ts = -0.25 + i * 0.45
    k = eback(prog(t, ts, ts + 0.3), 1.2)
    ox, oy = OFFSETS[i]
    x = cx + ox * (1 - k)
    y = cy + oy * (1 - k)
    rot = 0
    if i == OFF and not fixed:
        x += 11 * k
        y -= 6 * k
        rot = 1.4 * k
    return x, y, rot, k


def zmap(x, y, z):
    """Zoom z about the off tile, sliding it towards the frame centre."""
    fx, fy = TILES[OFF]
    kk = (z - 1) / 0.8
    tx, ty = SCX, 980
    return fx + (x - fx) * z + (tx - fx) * kk, fy + (y - fy) * z + (ty - fy) * kk


def draw_tiles(im, t, zoom=1.0, fixed=False, alpha=1.0):
    for i in range(6):
        x, y, rot, k = tile_pos(i, t, fixed)
        a = (0.35 + 0.65 * k) * alpha
        x, y = zmap(x, y, zoom)
        hw, hh = 190 * zoom, 150 * zoom
        if rot:
            tile = Image.new("RGBA", (int(hw * 2) + 40, int(hh * 2) + 40), (0, 0, 0, 0))
            rrect(tile, (20, 20, 20 + hw * 2, 20 + hh * 2), 18 * zoom, C["obs2"], C["line"], 2, a)
            jewel_icon(tile, i, 20 + hw, 20 + hh - 20 * zoom, a)
            bars(tile, 20 + hw - 70 * zoom, 20 + hh + 80 * zoom, 140 * zoom, 1, 0, 9 * zoom, C["muted"], 0.6 * a)
            put(im, tile.rotate(-rot, Image.BICUBIC, expand=True), x, y)
        else:
            rrect(im, (x - hw, y - hh, x + hw, y + hh), 18 * zoom, C["obs2"], C["line"], 2, a)
            jewel_icon(im, i, x, y - 20 * zoom, a)
            bars(im, x - 70 * zoom, y + 80 * zoom, 140 * zoom, 1, 0, 9 * zoom, C["muted"], 0.6 * a)


def a06(m):
    m.add(sfx.metal_click(), 0, 1.0)
    m.add(sfx.low_thud(0.4), 0, 0.5)
    for i in range(1, 6):
        m.add(sfx.metal_click(), -0.25 + i * 0.45 + 0.3, 0.55, pan=0.3 * (1 if i % 2 else -1))
    m.bed(sfx.air(13), 0.05)
    m.bed(sfx.pad(13, "cmaj", 1200), 0.07, start=3.0)
    tick_beats(m, [3.0, 6.2, 7.8])
    m.add(sfx.ping(0.8, 1760), 4.6, 0.3)
    m.add(sfx.metal_click(), 9.5, 0.8)
    end_sting(m, 11.0)


M06 = dict(
    type="Precision ASMR", industry="Jewelry & watches", palette="Champagne accent on obsidian",
    hook="One of these tiles is off.",
    beats=[
        ("0.0–2.3", "Frame 0: six product tiles (ring, watch, necklace, earrings, bracelet, pendant) are mid-snap into a grid, each landing with a crisp metallic click. One lands a hair out of line."),
        ("2.3–3.0", "Hold on the grid: the viewer hunts for the odd tile."),
        ("3.0–4.4", "'Found it?'"),
        ("4.4–6.2", "Push in on the culprit with champagne guide lines: 'Off by a hair.'"),
        ("6.2–7.8", "'Your clients can't name it.'"),
        ("7.8–9.4", "'But they feel it.'"),
        ("9.4–11.0", "The tile clicks into perfect alignment: 'In jewellery, that is a flaw.'"),
        ("11.0–13.0", "End card: 'Set every pixel like a stone.' + DM 'PRECISION'."),
    ],
    sound="0.00 metallic click (like a clasp) on a short low thud; one panned click per tile; air texture; a high ping when the culprit is found; the loudest click when it snaps into place; thud + crystal on the end card.",
    cta="Set every pixel like a stone. DM 'PRECISION' to begin.",
    why="It is a spot-the-difference challenge the viewer cannot refuse, paired with satisfying click ASMR. Jewellers live by precision, so the payoff flatters their standards and questions their website's in the same move.",
)


@reel(6, "one-tile-is-off", 13.0, a06, M06, qc=[0.5, 2.5, 5.2, 10.0, 12.0])
def r06(t):
    im = bg(C["obs"], (26, 24, 20))
    zoom = 1 + 0.8 * eio(prog(t, 4.4, 5.0)) * (1 - eio(prog(t, 9.0, 9.5)))
    fixed = t >= 9.5
    if t < 11.0:
        a = win(t, -1, 11.0, 0, 0.2)
        draw_tiles(im, t, zoom, fixed, a)
        for i in range(6):
            ts = -0.25 + i * 0.45 + 0.3
            ga = win(t, ts, ts + 0.35, 0.02, 0.3) * 0.6
            if ga > 0:
                cx, cy = TILES[i]
                line(im, [(cx - 190, cy - 230), (cx - 190, cy + 230)], C["champ"], 1, ga)
                line(im, [(SX0, cy - 150), (SX1, cy - 150)], C["champ"], 1, ga)
        if 4.6 <= t < 9.6:
            ga = win(t, 4.6, 9.6, 0.25, 0.2)
            # the true column edge (from the tile above) versus the off tile's edge
            ex, _ = zmap(TILES[1][0] - 190, 0, zoom)
            ox_, _, _, _ = tile_pos(OFF, t, fixed)
            ex2, _ = zmap(ox_ - 190, 0, zoom)
            line(im, [(ex, 520), (ex, 1480)], C["champ"], 2, ga * 0.7)
            line(im, [(ex2, 520), (ex2, 1480)], C["gold_l"], 3, ga)
        zk = (zoom - 1) / 0.8
        if zk > 0:
            rect(im, (0, 0, W, 500), C["obs"], 0.92 * zk)
    if t < 3.0:
        txt(im, "One of these", SCX, 330, "serif", 82, 600, C["ivory"])
        txt(im, "tiles is off.", SCX, 420, "serif_i", 82, 500, C["champ"])
    say(im, t, 3.0, 4.4, "Found it?", 380, 96, C["champ"])
    say(im, t, 4.6, 6.2, "Off by a hair.", 380, 80, C["gold_l"])
    say(im, t, 6.2, 7.8, ("Your clients", "can't name it."), 380, 80)
    say(im, t, 7.8, 9.4, "But they feel it.", 380, 84)
    say(im, t, 9.5, 11.0, ("In jewellery,", "that is a flaw."), 380, 80, C["champ"])
    endcard(im, t, 11.0, ("Set every pixel", "like a stone."), "DM 'PRECISION' to begin", C["champ"])
    return im


# =====================================================================  07  gyms
QUERY = "gym near me"


def a07(m):
    m.add(sfx.keytap(), 0, 1.0)
    m.add(sfx.bass_hit(0.7, 130, 50), 0, 0.55)
    for i in range(6, len(QUERY)):
        m.add(sfx.keytap(), (i - 6) * 0.09 + 0.09, 0.45)
    m.bed(sfx.pulse_bed(13, 128, 50), 0.14, start=1.0, end=11.0)
    tick_beats(m, [1.0, 1.3, 1.6, 2.5, 4.0])
    tick_beats(m, [5.6 + i * 0.5 for i in range(5)], sfx.metal_click, 0.25)
    m.add(sfx.chime_stab(), 8.5, 0.35)
    end_sting(m, 11.0)


M07 = dict(
    type="Search bar", industry="Gyms & fitness studios", palette="Champagne accent on obsidian",
    hook="Whose gym shows up first?",
    beats=[
        ("0.0–1.0", "Frame 0: an abstract search field already typing 'gym ne…'; the query finishes with key taps. Hook sits above."),
        ("1.0–2.5", "Three anonymous result cards drop in. The top card's name is a gold question mark."),
        ("2.5–4.0", "'Not always the best gym.'"),
        ("4.0–5.5", "'The one easiest to choose.'"),
        ("5.5–8.5", "The top card opens into a checklist, one per half second: Hours, up to date / Exact location / Class times / Fast on a phone / Book a free trial."),
        ("8.5–10.0", "The question mark flips to 'Your gym' in gold (the payoff)."),
        ("10.0–11.0", "'Make it yours.'"),
        ("11.0–13.0", "End card: 'Be the first name they tap.' + DM 'NEAR ME'."),
    ],
    sound="0.00 keyboard tap with a short sub hit; key taps finish the query; a 128 bpm sub pulse (gym energy without loud music); light metallic ticks for each checklist item; chime when 'Your gym' appears.",
    cta="Be the first name they tap. DM 'NEAR ME' to start.",
    why="Every gym owner has searched 'gym near me' to check on rivals. The live query is instantly recognisable and the unanswered 'whose?' is the loop. The search UI is abstract and does not copy Google.",
    placeholders=["'Book a free trial' is a generic checklist item; change it if the client offers no trial"],
)


@reel(7, "gym-near-me", 13.0, a07, M07, push=2.5, qc=[0.5, 2.0, 7.0, 9.2, 12.0])
def r07(t):
    im = bg(C["obs"], (25, 23, 20))
    if t < 11.0:
        a = win(t, -1, 11.0, 0, 0.2)
        n = min(len(QUERY), 6 + int(t / 0.09))
        bx = (SX0 + 10, 560, SX1 - 10, 680)
        rrect(im, bx, 60, C["obs2"], C["champ"], 2, a)
        circle(im, bx[0] + 64, 614, 20, outline=C["champ"], width=4, alpha=a)
        line(im, [(bx[0] + 78, 628), (bx[0] + 96, 646)], C["champ"], 5, a)
        tw, _ = txt(im, QUERY[:n], bx[0] + 120, 620, "sans", 48, 500, C["ivory"], "lm", a)
        if int(t * 2.5) % 2 == 0:
            rect(im, (bx[0] + 126 + tw, 592, bx[0] + 130 + tw, 648), C["champ"], a)
        expand = eio(prog(t, 5.4, 5.9))
        for i in range(3):
            ts = 1.0 + i * 0.3
            if t < ts:
                continue
            k = eo(prog(t, ts, ts + 0.3))
            y0 = 740 + i * 170 + (1 - k) * 40 + (420 * expand if i > 0 else 0)
            h = 140 + (420 * expand if i == 0 else 0)
            hot = i == 0
            rrect(im, (SX0 + 10, y0, SX1 - 10, y0 + h), 26, C["obs2"], C["gold"] if hot and t > 2.5 else C["line"], 2, a * k)
            rrect(im, (SX0 + 34, y0 + 22, SX0 + 130, y0 + 118), 18, C["obs3"], alpha=a * k)
            if hot:
                if t < 8.5:
                    txt(im, "?", SX0 + 170, y0 + 50, "serif", 64, 700, C["gold"], "lm", a * k)
                else:
                    kk = eo(prog(t, 8.5, 8.8))
                    glow_txt(im, "Your gym", SX0 + 170 + 120 * kk, y0 + 52, "serif", 56, 600, C["gold_l"], a * kk, 14, 0.6)
                bars(im, SX0 + 170, y0 + 94, 420, 1, 0, 12, C["muted"], 0.5 * a * k)
            else:
                bars(im, SX0 + 170, y0 + 40, 380, 2, 40, 14, C["muted"], 0.45 * a * k)
        if expand > 0:
            items = ["Hours, up to date", "Exact location", "Class times", "Fast on a phone", "Book a free trial"]
            for i, s in enumerate(items):
                ts = 5.6 + i * 0.5
                if t < ts:
                    continue
                k = eo(prog(t, ts, ts + 0.25))
                y = 905 + i * 78
                check(im, SX0 + 70, y, 30, C["gold"], prog(t, ts, ts + 0.25), 5, a)
                txt(im, s, SX0 + 120, y, "sans", 38, 500, C["ivory"], "lm", a * k)
    if t < 2.5:
        txt(im, "Whose gym", SCX, 340, "serif", 92, 600, C["ivory"])
        txt(im, "shows up first?", SCX, 445, "serif_i", 88, 500, C["champ"])
    say(im, t, 2.5, 4.0, ("Not always", "the best gym."), 380, 78)
    say(im, t, 4.0, 5.5, ("The one easiest", "to choose."), 380, 78, C["champ"])
    say(im, t, 5.5, 8.5, "What the top result shows:", 400, 52, C["champ"], "sans", 500)
    say(im, t, 8.5, 10.0, "First in line.", 400, 76, C["gold_l"])
    say(im, t, 10.0, 11.0, "Make it yours.", 400, 84)
    endcard(im, t, 11.0, ("Be the first name", "they tap."), "DM 'NEAR ME' to start", C["champ"])
    return im


# =====================================================================  08  hotels & resorts
def cur_path(t):
    keys = [(0.0, (640, 1180)), (0.8, (330, 660)), (1.6, (480, 660)), (2.6, (720, 660)), (3.0, (720, 660)),
            (4.2, (560, 1050)), (4.8, (600, 1080)), (5.2, (540, 1020)), (6.0, (190, 620)), (9.6, (190, 620)),
            (10.6, (600, 1290)), (12.0, (600, 1290))]
    for (t0, p0), (t1, p1) in zip(keys, keys[1:]):
        if t0 <= t <= t1:
            k = eio(prog(t, t0, t1))
            return p0[0] + (p1[0] - p0[0]) * k, p0[1] + (p1[1] - p0[1]) * k
    return keys[-1][1]


def a08(m):
    m.add(sfx.mouse_click(), 0, 1.0)
    m.add(sfx.bass_hit(0.8, 120, 45), 0, 0.5)
    m.bed(sfx.pad(14, "gm", 700), 0.1)
    m.add(sfx.mouse_click(), 3.0, 0.5)
    m.add(sfx.tape_stop(0.6), 6.0, 0.55)
    tick_beats(m, [7.4, 8.1, 8.8])
    m.add(sfx.whoosh(0.5), 9.4, 0.25)
    m.add(sfx.mouse_click(), 11.2, 0.7)
    m.add(sfx.chime_stab(), 11.25, 0.3)
    end_sting(m, 12.0)


M08 = dict(
    type="Cursor tracking", industry="Hotels & resorts", palette="Obsidian with a deep-emerald accent",
    hook="Watch the exact second a booking dies.",
    beats=[
        ("0.0–3.0", "Frame 0: a resort website in an abstract browser frame; a visitor cursor is already moving, hovering Rooms, then Gallery, then clicking Rates. A session timer ticks in the corner (labelled illustrative)."),
        ("3.0–6.0", "Rates opens onto 'Rates on request. Fill in the form.' The cursor hesitates, jitters, then drifts towards '← Back'."),
        ("6.0–7.4", "Freeze with a tape-stop: a gold ring pulses on the cursor at Back. 'This second.'"),
        ("7.4–9.4", "Three reasons tick in: Rates hidden behind a form / No photo of the actual room / Three clicks to a date."),
        ("9.4–12.0", "Rebuilt page: room photo, 'From [rate] / night', date chips and an emerald Book button. The cursor goes straight to Book and clicks."),
        ("12.0–14.0", "End card: 'Keep the cursor on Book.' + DM 'BOOKING'."),
    ],
    sound="0.00 double mouse click over a soft sub hit; G-minor pad; a click on Rates; at 6.0 a tape-stop freeze; ticks for each reason; whoosh to the rebuilt page; click plus chime on Book.",
    cta="Keep the cursor on 'Book'. DM 'BOOKING' to begin.",
    why="Watching someone else's cursor is voyeuristic and impossible not to follow, and 'the exact second' promises a precise answer. Hoteliers know that hesitation and want to see it named.",
    placeholders=["[rate] on the rebuilt-page mockup", "The session timer is labelled 'illustrative session' on screen"],
)


@reel(8, "booking-dies-here", 14.0, a08, M08, push=6.0, qc=[1.0, 4.5, 6.5, 8.5, 11.3, 13.0])
def r08(t):
    im = bg(C["obs"], (12, 28, 24))
    if t < 12.0:
        a = win(t, -1, 12.0, 0, 0.2)
        bx = (SX0, 520, SX1, 1440)
        x0, y0, x1, y1 = browser(im, bx, "dark", a)
        sess = min(t, 6.0) if t < 9.4 else t - 9.4
        txt(im, f"illustrative session  00:{sess:04.1f}", x1 - 30, y0 + 30, "sans", 22, 500, C["muted"], "rm", a)
        rebuilt = t >= 9.4
        if not rebuilt:
            rrect(im, (x0 + 20, y0 + 50, x0 + 150, y0 + 100), 25, C["obs3"], C["line"], 2, a)
            txt(im, "← Back", x0 + 85, y0 + 75, "sans", 24, 600, C["ivory"], alpha=a)
            for i, s in enumerate(["Rooms", "Gallery", "Rates"]):
                txt(im, s, x0 + 230 + i * 200, y0 + 75, "sans", 30, 500, C["champ"], "mm", a)
            if t < 3.0:
                photo(im, (x0 + 20, y0 + 130, x1 - 20, y0 + 560), (20, 60, 52), (150, 120, 60), a)
                line(im, [(x0 + 20, y0 + 470), (x1 - 20, y0 + 470)], C["gold_l"], 2, a * 0.6)
                txt(im, "Your Resort", x0 + 60, y0 + 640, "serif", 64, 600, C["ivory"], "lm", a)
                bars(im, x0 + 60, y0 + 700, x1 - x0 - 140, 3, 26, 12, C["muted"], 0.4 * a)
            else:
                txt(im, "Rates on request.", x0 + 60, y0 + 200, "serif", 58, 600, C["ivory"], "lm", a)
                txt(im, "Fill in the form and we'll get back to you.", x0 + 60, y0 + 260, "sans", 26, 400, C["muted"], "lm", a)
                for i in range(4):
                    rrect(im, (x0 + 60, y0 + 330 + i * 100, x1 - 60, y0 + 400 + i * 100), 16, C["obs3"], C["line"], 2, a)
                button(im, (x0 + 60, y0 + 750, x0 + 320, y0 + 815), "Send request", C["obs3"], C["muted"], 24, a, C["line"])
        else:
            k = eo(prog(t, 9.4, 9.8))
            photo(im, (x0 + 20, y0 + 30, x1 - 20, y0 + 470), (40, 34, 26), (120, 96, 60), a * k)
            rrect(im, (x0 + 200, y0 + 250, x1 - 200, y0 + 420), 12, (200, 190, 170), alpha=a * k * 0.6)
            txt(im, "Sea-view suite", x0 + 50, y0 + 540, "serif", 56, 600, C["ivory"], "lm", a * k)
            txt(im, "From [rate] / night", x0 + 50, y0 + 605, "sans", 30, 500, C["gold_l"], "lm", a * k)
            for i, s in enumerate(["Fri 12", "Sat 13", "Sun 14"]):
                rrect(im, (x0 + 50 + i * 170, y0 + 650, x0 + 200 + i * 170, y0 + 710), 18, C["obs3"], C["line"], 2, a * k)
                txt(im, s, x0 + 125 + i * 170, y0 + 680, "sans", 24, 500, C["ivory"], alpha=a * k)
            pulse = 1 + 0.04 * SIN(t * 8) if t < 11.2 else 1
            hw = 230 * pulse
            button(im, (SCX - hw, 1260, SCX + hw, 1350), "Book", C["emer"], C["ivory"], 40, a * k)
        cx, cy = cur_path(t)
        if 3.6 < t < 5.6:
            cx += 6 * SIN(t * 31)
            cy += 4 * SIN(t * 23)
        if 6.0 <= t < 9.4:
            r = 40 + 50 * ((t - 6.0) % 0.8) / 0.8
            circle(im, cx + 6, cy + 10, r, outline=C["gold"], width=4, alpha=a * (1 - ((t - 6.0) % 0.8) / 0.8))
            circle(im, cx + 6, cy + 10, 36, outline=C["gold"], width=3, alpha=a)
        if 11.2 <= t < 11.8:
            r = 30 + 120 * prog(t, 11.2, 11.8)
            circle(im, cx, cy, r, outline=C["emer_l"], width=4, alpha=a * (1 - prog(t, 11.2, 11.8)))
        cursor(im, cx, cy, 1.0, C["ivory"], a)
    if t < 6.0:
        txt(im, "Watch the exact second", SCX, 330, "serif", 74, 600, C["ivory"])
        txt(im, "a booking dies.", SCX, 420, "serif_i", 74, 500, C["emer_l"])
    say(im, t, 6.0, 7.4, "This second.", 380, 96, C["gold"], fi=0.05)
    reasons = ["Rates hidden behind a form", "No photo of the actual room", "Three clicks to a date"]
    if 7.4 <= t < 9.4:
        for i, s in enumerate(reasons):
            ts = 7.4 + i * 0.7
            if t >= ts:
                k = eo(prog(t, ts, ts + 0.2))
                y = 1500 - (2 - i) * 0 if False else 300 + i * 70
                txt(im, s, SCX, y, "sans", 46, 600, C["ivory"], alpha=k * win(t, 7.4, 9.4, 0, 0.15))
    say(im, t, 9.4, 12.0, ("Show the room. Show the rate.", "One tap to book."), 370, 58)
    endcard(im, t, 12.0, ("Keep the cursor", "on 'Book'."), "DM 'BOOKING' to begin", C["emer_l"])
    return im


# =====================================================================  09  salons & beauty
def a09(m):
    m.add(sfx.shutter(), 0, 1.0)
    m.add(sfx.bass_hit(0.7, 140, 50), 0, 0.6)
    for tt in (1.5, 2.8, 4.1, 5.4):
        m.add(sfx.shutter(), tt, 0.6)
        m.add(sfx.low_thud(0.3), tt, 0.25)
    m.add(sfx.bass_hit(1.0, 120, 40), 6.7, 0.6)
    m.add(sfx.crystal(2.0, 1568), 6.75, 0.25)
    m.bed(sfx.pulse_bed(12, 100, 60), 0.12, end=10.0)
    tick_beats(m, [8.6])
    end_sting(m, 10.0)


M09 = dict(
    type="Quick-fire listicle", industry="Salons & beauty", palette="Champagne and ivory on obsidian; fast cuts",
    hook="5 things that make salons look cheap.",
    beats=[
        ("0.0–1.5", "Frame 0: hook on screen; a five-segment bar is already filling, so the viewer knows a fast list is coming."),
        ("1.5–2.8", "01 'Blurry phone photos.' (a soft-focus photo block behind)."),
        ("2.8–4.1", "02 'Prices only by DM.'"),
        ("4.1–5.4", "03 'Five different fonts.' (each word set in a different typeface)."),
        ("5.4–6.7", "04 'Booking by voice note.'"),
        ("6.7–8.6", "05, the twist, in gold: 'Calling yourself luxury.'"),
        ("8.6–10.0", "'Show it. Don't say it.'"),
        ("10.0–12.0", "End card: 'Look like the price you charge.' + DM 'SALON'."),
    ],
    sound="0.00 camera-shutter double click with a sub hit; a shutter + thud on every cut; a bigger hit with a crystal shimmer on the twist; light 100 bpm pulse.",
    cta="Look like the price you charge. DM 'SALON' to start.",
    why="'Cheap' is the word salon owners fear most, and a numbered list tells the viewer exactly how long to stay. The fifth item turns the list back on them, which drives comments.",
)


@reel(9, "salon-look-cheap", 12.0, a09, M09, push=1.5, qc=[0.6, 2.0, 4.5, 7.5, 9.0, 11.0])
def r09(t):
    im = bg(C["obs"], (30, 27, 22))
    starts = [1.5, 2.8, 4.1, 5.4, 6.7]
    if t < 10.0:
        a = win(t, -1, 10.0, 0, 0.2)
        seg_w = (SX1 - SX0 - 40 - 4 * 16) / 5
        for i in range(5):
            x = SX0 + 20 + i * (seg_w + 16)
            rrect(im, (x, 1400, x + seg_w, 1410), 5, C["line"], alpha=a)
            s0 = 0.0 if i == 0 else starts[i - 1]
            s1 = starts[i]
            f = prog(t, s0, s1)
            if f > 0:
                rrect(im, (x, 1400, x + max(10, seg_w * f), 1410), 5, C["gold"] if i == 4 else C["champ"], alpha=a)
    if t < 1.5:
        txt(im, "5 things that make", SCX, 690, "serif", 84, 600, C["ivory"])
        txt(im, "salons look cheap.", SCX, 795, "serif_i", 88, 500, C["champ"])
    items = ["Blurry phone photos.", "Prices only 'by DM'.", None, "Booking by voice note.", "Calling yourself 'luxury'."]
    for i, s in enumerate(items):
        t0 = starts[i]
        t1 = starts[i + 1] if i < 4 else 8.6
        if not (t0 <= t < t1):
            continue
        a = win(t, t0, t1, 0.06, 0.08)
        txt(im, f"{i + 1:02d}", SCX, 560, "serif", 230, 700, C["gold"] if i == 4 else C["line"], alpha=a)
        if i == 0:
            ph = Image.new("RGB", (560, 340))
            photo(ph, (0, 0, 560, 340), (120, 100, 90), (50, 40, 36))
            circle(ph, 280, 150, 80, fill=(200, 170, 150))
            ph = ph.filter(ImageFilter.GaussianBlur(14))
            put(im, ph.convert("RGBA"), SCX, 1150, alpha=a * 0.7)
        if s is None:
            fams = [("sans", 700), ("serif_i", 500), ("hand", 600), ("garamond", 700)]
            ws = ["Five", "different", "fonts", "."]
            xs = SCX - 380
            for (f, wgt), w in zip(fams, ws):
                sz = 84 if f != "hand" else 100
                ww, _ = txt(im, w, xs, 880, f, sz, wgt, C["ivory"], "lm", a)
                xs += ww + (18 if w != "fonts" else 0)
        else:
            size = fit_size(s, "serif", 600, 820, 92)
            txt(im, s, SCX, 880, "serif", size, 600, C["gold_l"] if i == 4 else C["ivory"], alpha=a)
        if i == 4:
            txt(im, "(the twist)", SCX, 990, "sans", 32, 500, C["muted"], alpha=a)
    say(im, t, 8.6, 10.0, ("Show it.", "Don't say it."), 820, 112, C["champ"])
    endcard(im, t, 10.0, ("Look like the price", "you charge."), "DM 'SALON' to start", C["champ"])
    return im
