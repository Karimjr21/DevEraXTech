"""Reels 10-18."""
import math
from functools import lru_cache

import sfx
from dx import *  # noqa: F401,F403
from dx import C, SCX, SX0, SX1, W, H
from . import reel
from .a import end_sting, tick_beats

SIN = math.sin


def big_text(im, s, x, y, family, size, weight, color, anchor="mm"):
    """Uncached text for continuously scaled type (keeps the sprite cache small)."""
    if size < 4:
        return
    f = font(family, int(size), weight)
    ImageDraw.Draw(im).text((x, y), s, font=f, fill=tuple(color), anchor=anchor)


def plate(im, y0, y1, alpha=0.85, color=C["obs"]):
    rect(im, (0, y0, W, y1), color, alpha)


# =====================================================================  10  architecture & interiors
SITE = (SX0, 560, SX1, 1400)
HERO_Y = 560 + 56 + 170
HERO_SIZE = 104


def hero_layout():
    parts = [("Form ", "serif", 600, C["ivory"]), ("&", "serif_i", 400, C["champ"]), (" Light", "serif", 600, C["ivory"])]
    widths = [text_w(p[0], p[1], HERO_SIZE, p[2]) for p in parts]
    total = sum(widths)
    x = SCX - total / 2
    out = []
    for p, w in zip(parts, widths):
        out.append((p, x + w / 2))
        x += w
    return out


AMP = None


def a10(m):
    m.add(sfx.bass_hit(2.2, 70, 30), 0, 1.0)
    m.add(sfx.click(0.03, 2500), 0, 0.6)
    m.bed(sfx.pad(14, "bbmaj", 500, 0.08), 0.13)
    m.bed(sfx.air(14), 0.05)
    tick_beats(m, [2.0, 3.5, 5.0, 6.5, 8.5], sfx.click, 0.16)
    m.add(sfx.crystal(2.5, 784), 10.5, 0.25)
    end_sting(m, 12.0)


M10 = dict(
    type="Zoom-out reveal", industry="Architecture & interior design", palette="Near-monochrome: ivory and champagne, one continuous move",
    hook="Clients judge this before your work.",
    beats=[
        ("0.0–2.0", "Frame 0: an extreme macro of a single italic ampersand, its curve and soft shadow filling the frame. The camera is already pulling back. Hook on a dark band at the top."),
        ("2.0–3.5", "Still pulling back: 'The curve.'"),
        ("3.5–5.0", "'The shadow.' The ampersand now sits between two words."),
        ("5.0–6.5", "'The white space.' The words become the headline 'Form & Light'."),
        ("6.5–8.5", "'Every detail is a promise.' The browser frame, nav and project grid come into view."),
        ("8.5–12.0", "The full website settles: 'Your website is the first room they walk into.'"),
        ("12.0–14.0", "End card: 'Design the first room.' + DM 'STUDIO'."),
    ],
    sound="0.00 deep sub drop with a dry click (the size of the macro); B-flat pad filtered low; air texture; tiny clicks on each word; a single crystal note when the site completes.",
    cta="Design the first room. DM 'STUDIO' to start.",
    why="A macro shot is unreadable as an object, so the eye has to keep watching to resolve it, and the pull-back is one continuous move with no cut to leave on. Architects and designers judge type and spacing for a living, so the hook speaks their language.",
)


def draw_site10(im, z, fx, fy, tx, ty, a=1.0):
    def M(x, y):
        return tx + (x - fx) * z, ty + (y - fy) * z

    x0, y0 = M(SITE[0], SITE[1])
    x1, y1 = M(SITE[2], SITE[3])
    if x1 - x0 < 6000:
        rrect(im, (x0, y0, x1, y1), 22 * z, C["obs2"], C["line"], max(1, int(2 * min(z, 3))), a)
        cy = y0 + 28 * z
        for i in range(3):
            circle(im, x0 + (30 + i * 22) * z, cy, 6 * z, fill=C["line"], alpha=a)
        nx, ny = M(SITE[0] + 50, SITE[1] + 100)
        if z < 4:
            big_text(im, "YOUR STUDIO", nx, ny, "sans", 22 * z, 600, C["champ"], "lm")
            for i in range(3):
                bx, by = M(SITE[2] - 260 + i * 75, SITE[1] + 96)
                rect(im, (bx, by, bx + 50 * z, by + 8 * z), C["muted"], a)
        # project grid
        for i in range(4):
            gx = SITE[0] + 40 + (i % 2) * ((SITE[2] - SITE[0] - 100) / 2 + 20)
            gy = SITE[1] + 330 + (i // 2) * 240
            gw = (SITE[2] - SITE[0] - 100) / 2
            px0, py0 = M(gx, gy)
            px1, py1 = M(gx + gw, gy + 200)
            if px1 > 0 and px0 < W and py1 > 0 and py0 < H and z < 6:
                photo(im, (max(px0, -10), max(py0, -10), min(px1, W + 10), min(py1, H + 10)),
                      [(60, 56, 50), (44, 40, 36), (70, 64, 54), (38, 36, 33)][i], (18, 17, 15), a, 14 * min(z, 2))
                lx0, ly0 = M(gx + 20, gy + 150)
                lx1, _ = M(gx + gw - 20, gy + 150)
                line(im, [(lx0, ly0), (lx1, ly0)], C["champ"], 1, a * 0.5)
        if z < 3:
            for j in range(2):
                bx, by = M(SITE[0] + 50, SITE[1] + 820 + j * 26 - 60)
                rect(im, (bx, by, bx + (500 - j * 180) * z, by + 10 * z), C["muted"], a * 0.5)
    for (s, fam, wgt, col), cx in hero_layout():
        hx, hy = M(cx, HERO_Y)
        size = HERO_SIZE * z
        if s == "&":
            big_text(im, s, hx + size * 0.035, hy + size * 0.045, fam, size, wgt, (4, 4, 4))
        if -size * 2 < hx < W + size * 2:
            big_text(im, s.strip(), hx, hy, fam, size, wgt, col)


@reel(10, "first-room-zoom-out", 14.0, a10, M10, qc=[0.5, 2.5, 5.0, 8.0, 11.0, 13.0])
def r10(t):
    im = bg(C["obs"], (24, 23, 21))
    lay = hero_layout()
    ax = lay[1][1]
    p = 1 - (1 - prog(t, 0, 10.5)) ** 1.8
    z = math.exp(math.log(16) * (1 - p))
    q = p ** 3
    fx = ax + (SCX - ax) * q
    fy = HERO_Y + (980 - HERO_Y) * q
    tx, ty = SCX, 960 + 20 * q
    if t < 12.0:
        draw_site10(im, z, fx, fy, tx, ty, win(t, -1, 12.0, 0, 0.25))
        if t >= 11.75:
            rect(im, (0, 0, W, H), C["obs"], prog(t, 11.75, 12.0))
    if t < 9.0:
        plate(im, 220, 500, 0.82 * (1 - prog(t, 8.0, 9.0)))
    if t < 2.0:
        txt(im, "Clients judge this", SCX, 320, "serif", 84, 600, C["ivory"])
        txt(im, "before your work.", SCX, 415, "serif_i", 84, 500, C["champ"])
    say(im, t, 2.0, 3.5, "The curve.", 360, 84, C["champ"], "serif_i", 500)
    say(im, t, 3.5, 5.0, "The shadow.", 360, 84, C["champ"], "serif_i", 500)
    say(im, t, 5.0, 6.5, "The white space.", 360, 84, C["champ"], "serif_i", 500)
    say(im, t, 6.5, 8.5, ("Every detail", "is a promise."), 350, 76)
    say(im, t, 8.5, 12.0, ("It's the first room", "they walk into."), 350, 72)
    endcard(im, t, 12.0, "Design the first room.", "DM 'STUDIO' to start", C["champ"])
    return im


# =====================================================================  11  startups & SaaS
def a11(m):
    m.add(sfx.click(0.03, 6000), 0, 1.0)
    m.add(sfx.ping(0.9, 1567.98), 0, 0.7)
    m.add(sfx.bass_hit(0.6, 140, 55), 0, 0.5)
    m.add(sfx.snap(), 1.0, 0.6)
    m.bed(sfx.pad(12, "em", 1000), 0.08, start=1.0)
    tick_beats(m, [2.4, 3.8, 4.4, 5.0, 5.6])
    m.add(sfx.click(0.03, 6000), 7.2, 0.6)
    m.add(sfx.ping(0.9, 1567.98), 7.2, 0.4)
    m.add(sfx.chime_stab(), 8.2, 0.3)
    end_sting(m, 10.0)


M11 = dict(
    type="Guess in one second", industry="Startups & SaaS", palette="Champagne accent on obsidian",
    hook="What does this company do? 1 second.",
    beats=[
        ("0.0–1.0", "Frame 0: hook on top, a timer bar already draining; below it an invented buzzword homepage ('Empowering the future of synergy.') with gradient blobs."),
        ("1.0–2.4", "Hard cut to black: 'No idea?'"),
        ("2.4–3.8", "'Neither do your visitors.'"),
        ("3.8–7.0", "'Your headline should answer:' What it is. / Who it's for. / What happens next."),
        ("7.0–8.2", "'Try again. 1 second.' The timer drains over a clear homepage: Klozcrew, 'The closing CRM for real estate agencies.'"),
        ("8.2–10.0", "'Got it?' then OUR BUILD: Klozcrew. 'One second was enough.'"),
        ("10.0–12.0", "End card: 'Make one second enough.' + DM 'CLARITY'."),
    ],
    sound="0.00 bright click and high ping (a camera-flash feel without a real flash) over a short sub; a snap on the hard cut at 1.0; E-minor pad; ticks on the list; the same click + ping on the second test so the structure rhymes; chime on 'Got it?'.",
    cta="Make one second enough. DM 'CLARITY' with your homepage.",
    why="It is a test with a one-second clock, so the viewer plays along instinctively and fails, which is the point. Founders recognise their own vague hero copy instantly, and the second test (which they pass) proves the fix.",
)


def buzz_site(im, box, a=1.0):
    x0, y0, x1, y1 = browser(im, box, "dark", a)
    circle(im, x0 + 160, y0 + 230, 170, fill=(70, 40, 120), alpha=0.5 * a)
    circle(im, x1 - 140, y0 + 330, 200, fill=(30, 90, 140), alpha=0.45 * a)
    circle(im, SCX, y0 + 520, 160, fill=(140, 60, 110), alpha=0.35 * a)
    txt(im, "NEXUSFLOW", x0 + 40, y0 + 40, "sans", 22, 700, C["ivory"], "lm", a, tracking=4)
    para(im, ("Empowering the", "future of synergy."), SCX, y0 + 300, "sans", 62, 700, C["white"], alpha=a)
    para(im, ("Next-gen solutions for", "tomorrow's possibilities."), SCX, y0 + 470, "sans", 30, 400, C["muted"], alpha=a)
    button(im, (SCX - 270, y0 + 570, SCX - 20, y0 + 640), "Get started", (110, 70, 220), C["white"], 26, a)
    button(im, (SCX + 20, y0 + 570, SCX + 270, y0 + 640), "Learn more", C["obs3"], C["ivory"], 26, a, C["line"])


def kloz_site(im, box, a=1.0):
    x0, y0, x1, y1 = browser(im, box, "light", a)
    txt(im, "Klozcrew", x0 + 40, y0 + 46, "serif", 34, 700, C["ink"], "lm", a)
    button(im, (x1 - 230, y0 + 20, x1 - 40, y0 + 72), "Book a demo", C["ink"], C["ivory"], 22, a)
    para(im, ("The closing CRM", "for real estate", "agencies."), x0 + 40, y0 + 290, "serif", 72, 600, C["ink"], "lm", a, 1.1, "left")
    bars(im, x0 + 40, y0 + 480, x1 - x0 - 160, 2, 30, 12, (160, 150, 130), 0.6 * a)
    rrect(im, (x0 + 40, y0 + 580, x1 - 40, y1 - 40), 20, C["white"], (215, 205, 188), 2, a)
    for i in range(4):
        rrect(im, (x0 + 70 + i * 185, y0 + 620, x0 + 230 + i * 185, y1 - 70), 14, (240, 234, 222), alpha=a)


def timer_bar(im, t, t0, y=470):
    f = 1 - prog(t, t0, t0 + 1.0)
    rrect(im, (SX0 + 40, y, SX1 - 40, y + 10), 5, C["line"])
    if f > 0:
        rrect(im, (SX0 + 40, y, SX0 + 40 + (SX1 - SX0 - 80) * f, y + 10), 5, C["champ"])


@reel(11, "guess-in-one-second", 12.0, a11, M11, qc=[0.5, 1.5, 5.8, 7.6, 9.4, 11.0])
def r11(t):
    im = bg(C["obs"], (24, 24, 26))
    if t < 1.0:
        txt(im, "What does this company do?", SCX, 320, "serif", fit_size("What does this company do?", "serif", 600, 860, 72), 600, C["ivory"])
        txt(im, "1 second.", SCX, 405, "serif_i", 72, 500, C["champ"])
        timer_bar(im, t, 0.0)
        buzz_site(im, (SX0, 540, SX1, 1440))
    say(im, t, 1.0, 2.4, "No idea?", 820, 130, C["champ"], fi=0.04)
    say(im, t, 2.4, 3.8, ("Neither do", "your visitors."), 820, 104)
    if 3.8 <= t < 7.0:
        a = win(t, 3.8, 7.0, 0.12, 0.15)
        txt(im, "Your headline should answer:", SCX, 520, "sans", 44, 500, C["champ"], alpha=a)
        for i, s in enumerate(["What it is.", "Who it's for.", "What happens next."]):
            ts = 4.4 + i * 0.6
            if t >= ts:
                k = eo(prog(t, ts, ts + 0.25))
                txt(im, s, SCX, 700 + i * 160 + (1 - k) * 20, "serif", 92, 600, C["ivory"], alpha=a * k)
    if 7.0 <= t < 8.2:
        txt(im, "Try again. 1 second.", SCX, 360, "serif", 72, 600, C["ivory"])
        if t >= 7.2:
            timer_bar(im, t, 7.2)
            kloz_site(im, (SX0, 540, SX1, 1440))
    if 8.2 <= t < 10.0:
        a = win(t, 8.2, 10.0, 0.1, 0.15)
        kloz_site(im, (SX0, 540, SX1, 1440), a * 0.14)
        if t < 9.0:
            say(im, t, 8.2, 9.0, "Got it?", 900, 140, C["champ"], fo=0.1)
        else:
            eyebrow(im, "Our build · Klozcrew", SCX, 760, alpha=a)
            say(im, t, 9.0, 10.0, ("One second", "was enough."), 900, 104)
    endcard(im, t, 10.0, ("Make one second", "enough."), "DM 'CLARITY' with your homepage", C["champ"])
    return im


# =====================================================================  12  car dealerships
def counter_value(t):
    return 1 + int((min(t, 10.0) + 0.35) / 0.7)


def flap_digits(im, v, cx, cy, t, scale=1.0, alpha=1.0):
    s = f"{v:04d}"
    bw, bh, gap = 170 * scale, 240 * scale, 18 * scale
    total = 4 * bw + 3 * gap
    phase = ((min(t, 10.0) + 0.35) % 0.7) / 0.7 if t < 10.0 else 1.0
    for i, ch in enumerate(s):
        x0 = cx - total / 2 + i * (bw + gap)
        rrect(im, (x0, cy - bh / 2, x0 + bw, cy + bh / 2), 16 * scale, C["obs2"], C["line"], 2, alpha)
        changed = i == 3 or (i == 2 and s[3] == "0")
        sq = 1.0
        if changed and phase < 0.18:
            sq = 0.35 + 0.65 * eo(phase / 0.18)
        sp = sprite(ch, "serif", int(190 * scale), 700, C["gold"])
        sp2 = sp.resize((sp.width, max(1, int(sp.height * sq))), Image.BICUBIC)
        put(im, sp2, x0 + bw / 2, cy, alpha=alpha)
        line(im, [(x0 + 4, cy), (x0 + bw - 4, cy)], C["obs"], max(2, int(4 * scale)), alpha)


def car_outline(im, cx, cy, s, color, a):
    body = [(-1.0, 0.1), (-0.95, -0.12), (-0.6, -0.18), (-0.35, -0.42), (0.25, -0.44), (0.55, -0.2),
            (0.95, -0.14), (1.0, 0.1), (-1.0, 0.1)]
    line(im, [(cx + x * s, cy + y * s) for x, y in body], color, 3, a)
    line(im, [(cx - 0.3 * s, cy - 0.38 * s), (cx - 0.05 * s, cy - 0.2 * s), (cx + 0.45 * s, cy - 0.2 * s)], color, 2, a)
    for wx in (-0.58, 0.6):
        circle(im, cx + wx * s, cy + 0.1 * s, 0.17 * s, fill=C["obs"], outline=color, width=3, alpha=a)
        circle(im, cx + wx * s, cy + 0.1 * s, 0.07 * s, outline=color, width=2, alpha=a)


def a12(m):
    m.add(sfx.flap_burst(), 0, 1.0)
    m.add(sfx.bass_hit(0.9, 120, 42), 0, 0.5)
    k = 0.7
    while k < 10.0:
        m.add(sfx.flap(), k, 0.35)
        m.add(sfx.flap(), k + 0.03, 0.2)
        k += 0.7
    m.bed(sfx.pulse_bed(13, 86, 48), 0.12, end=10.0)
    tick_beats(m, [1.8, 3.4, 5.0, 6.5])
    m.add(sfx.whoosh(0.5), 7.9, 0.2)
    m.add(sfx.low_thud(), 10.0, 0.6)
    m.add(sfx.tape_stop(0.4), 10.0, 0.25)
    end_sting(m, 11.0)


M12 = dict(
    type="Cost-of-waiting meter", industry="Car dealerships", palette="Gold on obsidian, mechanical",
    hook="Buyers lost while you watch this.",
    beats=[
        ("0.0–1.8", "Frame 0: a four-digit split-flap counter is already flipping (0001, 0002…), with a gauge needle sweeping above it. Under it, in small caps: ILLUSTRATIVE COUNTER, NOT REAL DATA."),
        ("1.8–3.4", "Counter keeps flipping: 'They didn't stop wanting a car.'"),
        ("3.4–5.0", "'They found one faster.'"),
        ("5.0–6.5", "'Stock. Price range. Finance options.'"),
        ("6.5–8.0", "'Answered on the page, not on hold.'"),
        ("8.0–10.0", "The counter shrinks to the bottom while a car listing card draws in (line-art car, chips: In stock / Book a test drive / Finance calculator)."),
        ("10.0–11.0", "The counter stops dead with a thud: 'Stop the counter.'"),
        ("11.0–13.0", "End card: 'Stop the counter.' + DM 'SHOWROOM'."),
    ],
    sound="0.00 split-flap burst over a sub hit; a flap clack on every increment; an 86 bpm pulse like an idling engine; whoosh into the listing card; a thud and short tape-stop when the counter stops.",
    cta="Stop the counter. DM 'SHOWROOM' to put your stock online.",
    why="A rising number tied to the viewer's lost sales creates urgency in the first frame, and the open question is 'how high does it go?'. It is labelled illustrative on screen, so nothing is claimed as data.",
    placeholders=["The counter is illustrative and labelled so; Karim can replace it with a client's real enquiry figure only if he has one"],
)


@reel(12, "stop-the-counter", 13.0, a12, M12, push=1.8, qc=[0.5, 2.5, 6.0, 9.0, 10.5, 12.0])
def r12(t):
    im = bg(C["obs"], (30, 26, 16), cy=820)
    if t < 11.0:
        a = win(t, -1, 11.0, 0, 0.2)
        mv = eio(prog(t, 7.9, 8.4))
        cy = 860 + (1400 - 860) * mv
        sc = 1.0 - 0.6 * mv
        if mv < 0.5:
            ga = a * (1 - mv * 2)
            arc(im, SCX, 660, 230, 200, 340, C["line"], 6, ga)
            ang = 210 + 110 * prog(t, 0, 10) + 6 * SIN(t * 9) * (t < 10)
            arc(im, SCX, 660, 230, 200, min(ang, 340), C["gold"], 6, ga)
            rad = math.radians(ang)
            line(im, [(SCX, 660), (SCX + 200 * math.cos(rad), 660 + 200 * math.sin(rad))], C["gold_l"], 4, ga)
            circle(im, SCX, 660, 12, fill=C["gold"], alpha=ga)
        flap_digits(im, counter_value(t), SCX, cy, t, sc, a)
        txt(im, "ILLUSTRATIVE COUNTER · NOT REAL DATA", SCX, cy + 150 * sc + 30, "sans", 24 if sc > 0.7 else 18, 600,
            C["muted"], alpha=a, tracking=3)
        if t >= 7.9:
            k = eo(prog(t, 7.9, 8.4))
            box = (SX0, 520, SX1, 1180)
            rrect(im, box, 30, C["obs2"], C["gold_d"], 2, a * k)
            car_outline(im, SCX, 760, 300 * k, C["gold"], a * k)
            txt(im, "Sedan, 2026", box[0] + 40, 960, "serif", 52, 600, C["ivory"], "lm", a * k)
            for i, s in enumerate(["In stock", "Book a test drive", "Finance calculator"]):
                cx0 = box[0] + 40 + [0, 190, 520][i]
                w = [170, 310, 320][i]
                rrect(im, (cx0, 1030, cx0 + w, 1090), 30, C["obs3"], C["gold_d"], 2, a * k)
                txt(im, s, cx0 + w / 2, 1060, "sans", 24, 600, C["champ"], alpha=a * k)
    if t < 1.8:
        txt(im, "Buyers lost while", SCX, 330, "serif", 86, 600, C["ivory"])
        txt(im, "you watch this.", SCX, 430, "serif_i", 86, 500, C["gold_l"])
    say(im, t, 1.8, 3.4, ("They didn't stop", "wanting a car."), 380, 76)
    say(im, t, 3.4, 5.0, "They found one faster.", 380, 76, C["gold_l"])
    say(im, t, 5.0, 6.5, ("Stock. Price range.", "Finance options."), 380, 72)
    say(im, t, 6.5, 7.9, ("Answered on the page,", "not on hold."), 380, 72)
    say(im, t, 10.0, 11.0, "Stop the counter.", 380, 90, C["gold"], fi=0.05)
    endcard(im, t, 11.0, "Stop the counter.", "DM 'SHOWROOM' to put your stock online")
    return im


# =====================================================================  13  fashion & streetwear
def a13(m):
    m.add(sfx.hit808(), 0, 1.0)
    m.add(sfx.click(0.02, 3000), 0, 0.5)
    m.add(sfx.low_thud(), 1.6, 0.35)
    tick_beats(m, [3.0, 4.6], sfx.low_thud, 0.3)
    for i in range(4):
        m.add(sfx.shutter(), 6.0 + i * 0.5, 0.35)
        m.add(sfx.heartbeat_pulse(), 6.0 + i * 0.5, 0.4)
    m.add(sfx.whoosh(0.4), 7.8, 0.2)
    m.add(sfx.hit808(1.2), 9.6, 0.32)
    end_sting(m, 10.0)


M13 = dict(
    type="Single sound word", industry="Fashion & streetwear", palette="Near-monochrome: white type on black, gold only in the wordmark",
    hook="Expensive.",
    beats=[
        ("0.0–1.6", "Frame 0: 'Expensive.' fills the safe width in italic serif, shaking from the 808 hit and settling, while a hairline draws under it."),
        ("1.6–3.0", "The word lifts; under it: 'is a feeling.'"),
        ("3.0–4.6", "'It starts before the fitting room.'"),
        ("4.6–6.0", "'It starts on the homepage.'"),
        ("6.0–8.0", "Four lookbook layouts cut on the beat every half second: full-bleed editorial, two-column product, single hero product, 'New season' type spread."),
        ("8.0–9.6", "OUR BUILD: TurbanClass, a turban boutique store: 'Gold Embroidered Turban', 'Personalized turbans made just for you.'"),
        ("9.6–10.0", "'Expensive.' returns, one more 808, for the loop."),
        ("10.0–12.0", "End card: 'Look expensive before they touch it.' + DM 'DROP'."),
    ],
    sound="0.00 long, saturated 808 with a click on top; silence otherwise, so each low thud lands; shutter + pulse on each lookbook cut; a second 808 on the returning word.",
    cta="Look expensive before they touch it. DM 'DROP' before your next collection.",
    why="One huge word with a heavy hit is the fastest possible read, and 'Expensive.' is the exact status every fashion founder wants. It opens a question (what is?) that the next line answers.",
)


def lookbook(im, i, a=1.0):
    if i == 0:
        photo(im, (SX0, 520, SX1, 1440), (90, 90, 88), (20, 20, 20), a, 6)
        txt(im, "Collection 01", SX0 + 40, 1380, "serif_i", 50, 500, C["white"], "lm", a)
    elif i == 1:
        photo(im, (SX0, 560, SCX - 10, 1300), (70, 70, 68), (30, 30, 30), a, 6)
        txt(im, "The Coat", SCX + 40, 700, "serif", 56, 600, C["white"], "lm", a)
        bars(im, SCX + 40, 760, 300, 3, 26, 10, C["muted"], 0.5 * a)
    elif i == 2:
        photo(im, (SCX - 220, 560, SCX + 220, 1180), (110, 108, 104), (40, 40, 40), a, 220)
        txt(im, "Essential", SCX, 1290, "serif", 64, 600, C["white"], alpha=a)
    else:
        txt(im, "NEW", SCX, 760, "serif", 230, 700, C["white"], alpha=a)
        txt(im, "SEASON", SCX, 1000, "serif_i", 150, 400, C["white"], alpha=a)


@reel(13, "expensive", 12.0, a13, M13, qc=[0.1, 2.0, 5.0, 6.7, 8.8, 11.0])
def r13(t):
    im = bg(C["obs"], (18, 18, 18))
    size = fit_size("Expensive.", "serif_i", 600, 800, 240)
    if t < 3.0:
        shake = 16 * math.exp(-t * 5) * SIN(t * 70)
        s = 1 + 0.06 * math.exp(-t * 6)
        y = 860 - 220 * eio(prog(t, 1.6, 2.0))
        sc = 1 - 0.3 * eio(prog(t, 1.6, 2.0))
        put(im, sprite("Expensive.", "serif_i", size, 600, C["white"]), SCX + shake, y, alpha=win(t, -1, 3.0, 0, 0.12),
            scale=s * sc)
        k = 0.2 + 0.8 * eo(t / 1.2)
        hline(im, SCX - 300 * k, SCX + 300 * k, y + 150 * sc, C["white"], 2, 0.6 * win(t, -1, 3.0, 0, 0.12))
    say(im, t, 1.8, 3.0, "is a feeling.", 900, 84, C["muted"], "serif", 500)
    say(im, t, 3.0, 4.6, ("It starts before", "the fitting room."), 860, 96)
    say(im, t, 4.6, 6.0, ("It starts on", "the homepage."), 860, 104)
    if 6.0 <= t < 8.0:
        lookbook(im, int((t - 6.0) / 0.5))
    if 8.0 <= t < 9.6:
        a = win(t, 8.0, 9.6, 0.12, 0.12)
        eyebrow(im, "Our build · TurbanClass", SCX, 420, C["muted"], a)
        for j, (name, c0) in enumerate([("Gold Embroidered Turban", (120, 96, 50)), ("Custom Designer Turban", (70, 70, 70))]):
            x0 = SX0 + j * 440
            rrect(im, (x0, 500, x0 + 420, 1180), 20, C["obs2"], C["line"], 2, a)
            photo(im, (x0 + 20, 520, x0 + 400, 980), c0, (24, 22, 20), a)
            para(im, tuple(name.rsplit(" ", 1)), x0 + 30, 1060, "serif", 38, 600, C["white"], "lm", a, 1.15, "left")
        txt(im, "Personalized turbans made just for you.", SCX, 1290, "serif_i", 44, 500, C["white"], alpha=a)
    if 9.6 <= t < 10.0:
        put(im, sprite("Expensive.", "serif_i", size, 600, C["white"]), SCX, 860, alpha=win(t, 9.6, 10.0, 0, 0.1),
            scale=0.7 + 0.3 * eo(prog(t, 9.6, 9.75)))
    endcard(im, t, 10.0, ("Look expensive", "before they touch it."), "DM 'DROP' before your next collection", C["gold"], C["white"])
    return im


# =====================================================================  14  schools & academies
def a14(m):
    m.add(sfx.tape_stop(0.6), 0, 1.0)
    m.add(sfx.bass_hit(0.8, 110, 40), 0, 0.7)
    m.bed(sfx.pad(13, "cmaj", 700), 0.08, start=1.6)
    m.add(sfx.whoosh(0.6), 1.8, 0.3)
    tick_beats(m, [3.8, 4.6, 5.4], sfx.marker_strike, 0.35)
    tick_beats(m, [6.4])
    m.add(sfx.whoosh(0.5), 7.6, 0.2)
    m.add(sfx.chime_stab(), 10.0, 0.3)
    end_sting(m, 11.0)


M14 = dict(
    type="Freeze frame", industry="Schools & academies", palette="Ivory and gold on obsidian",
    hook="This is the second you lose them.",
    beats=[
        ("0.0–1.8", "Frame 0: frozen. A phone in a parent's hand shows a school site; a playhead bar at the bottom is paused on a marker that pulses with expanding gold rings. Hook at the top."),
        ("1.8–3.6", "The playhead rewinds: 'A parent. Comparing schools.'"),
        ("3.6–6.4", "Play: 'One hand. One thumb.' Three lines on the school site get struck through in gold: Fees? Call the office / Admissions: download PDF / Curriculum: contact us."),
        ("6.4–7.8", "'They decide with one thumb.'"),
        ("7.8–10.0", "OUR BUILD: an IGCSE Maths platform: courses, live sessions, assignments and parent accounts behind one login."),
        ("10.0–11.0", "The playhead passes the marker: 'Now they stay.'"),
        ("11.0–13.0", "End card: 'Win the second they decide.' + DM 'ENROL'."),
    ],
    sound="0.00 tape-stop freeze over a sub hit (the frozen moment); whoosh on the rewind; marker strikes on each crossed-out line; C-major pad; chime when the playhead passes the marker.",
    cta="Win the second they decide. DM 'ENROL' to begin.",
    why="A paused frame with a playhead tells the viewer something is about to happen, and the hook names the exact moment a school loses a family. Parents use phones one-handed, and school owners know it.",
)


def school_screen(im, sb, t, strikes):
    x0, y0, x1, y1 = sb
    rect(im, (x0 + 30, y0 + 70, x0 + 230, y0 + 90), C["ink"])
    photo(im, (x0 + 24, y0 + 120, x1 - 24, y0 + 340), (200, 190, 168), (150, 138, 110), radius=20)
    txt(im, "Our School", x0 + 50, y0 + 400, "serif", 44, 600, C["ink"], "lm")
    rows = ["Fees? Call the office", "Admissions: download PDF", "Curriculum: contact us"]
    for i, r in enumerate(rows):
        y = y0 + 480 + i * 110
        rrect(im, (x0 + 24, y - 40, x1 - 24, y + 40), 16, C["white"], (215, 205, 188), 2)
        w, _ = txt(im, r, x0 + 50, y, "sans", 26, 500, (90, 82, 70), "lm")
        if strikes[i] > 0:
            strike(im, x0 + 44, x0 + 56 + w, y, strikes[i], C["gold"], 5)


def playhead(im, f, t, pulse=True, a=1.0):
    y = 1480
    hline(im, SX0 + 20, SX1 - 20, y, C["line"], 6, a)
    x = SX0 + 20 + (SX1 - SX0 - 40) * f
    hline(im, SX0 + 20, x, y, C["gold"], 6, a)
    if pulse:
        ph = (t % 0.9) / 0.9
        circle(im, x, y, 16 + 50 * ph, outline=C["gold"], width=3, alpha=a * (1 - ph))
    circle(im, x, y, 16, fill=C["gold_l"], alpha=a)


@reel(14, "second-you-lose-them", 13.0, a14, M14, push=1.8, qc=[0.4, 2.5, 5.5, 8.5, 10.4, 12.0])
def r14(t):
    im = bg(C["obs"], (28, 26, 22))
    if t < 7.8:
        a = win(t, -1, 7.8, 0, 0.2)
        frozen = t < 1.8
        sb = phone(im, SCX - 30, 960, 470, 840, screen=C["ivory"], alpha=a)
        strikes = [prog(t, 3.8 + i * 0.8, 4.1 + i * 0.8) for i in range(3)]
        school_screen(im, sb, t, strikes)
        # thumb resting on the screen edge
        with Vec(im) as d:
            d.ellipse((SCX + 130, 1200, SCX + 290, 1440), pen(C["gold_d"], 3, a), brush(C["obs3"], a * 0.85))
        if frozen:
            rect(im, (0, 0, W, H), (120, 110, 90), 0.08)
            for bxx in (0, 26):
                rrect(im, (SX0 + 20 + bxx, 520, SX0 + 34 + bxx, 570), 4, C["gold"], alpha=0.6 + 0.4 * SIN(t * 6) ** 2)
        if t < 1.8:
            f = 0.62
        elif t < 3.6:
            f = 0.62 - 0.42 * eio(prog(t, 1.8, 2.6))
        else:
            f = 0.2 + 0.4 * prog(t, 3.6, 7.8)
        playhead(im, f, t, frozen, a)
        if t < 1.8:
            txt(im, "0:04", SX0 + 20 + (SX1 - SX0 - 40) * 0.62, 1425, "sans", 26, 600, C["gold_l"], alpha=a)
    if 7.8 <= t < 11.0:
        f = 0.6 + 0.35 * prog(t, 7.8, 11.0)
        playhead(im, f, t, False, win(t, 7.8, 11.0, 0.2, 0.2))
    if t < 1.8:
        txt(im, "This is the second", SCX, 330, "serif", 86, 600, C["ivory"])
        txt(im, "you lose them.", SCX, 430, "serif_i", 86, 500, C["gold_l"])
    say(im, t, 1.8, 3.6, ("A parent.", "Comparing schools."), 380, 72)
    say(im, t, 3.6, 6.4, "One hand. One thumb.", 380, 72)
    say(im, t, 6.4, 7.8, ("They decide", "with one thumb."), 380, 76, C["gold_l"])
    if 7.8 <= t < 10.0:
        a = win(t, 7.8, 10.0, 0.2, 0.2)
        eyebrow(im, "Our build", SCX, 330, alpha=a)
        txt(im, "IGCSE Maths platform", SCX, 400, "serif", 62, 600, C["ivory"], alpha=a)
        x0, y0, x1, y1 = browser(im, (SX0, 480, SX1, 1330), "dark", a)
        rect(im, (x0 + 2, y0, x0 + 230, y1 - 2), C["obs3"], a)
        for i, s in enumerate(["Courses", "Live sessions", "Assignments", "Parents"]):
            txt(im, s, x0 + 30, y0 + 60 + i * 70, "sans", 26, 600 if i == 0 else 500, C["gold_l"] if i == 0 else C["ivory"], "lm", a)
        cards = ["Master Copy Courses", "Office hours", "Assignment Desk", "Finished Courses"]
        for i, s in enumerate(cards):
            cx0 = x0 + 260 + (i % 2) * 300
            cy0 = y0 + 40 + (i // 2) * 330
            rrect(im, (cx0, cy0, cx0 + 280, cy0 + 300), 18, C["obs2"], C["line"], 2, a)
            para(im, tuple(wrap(s, "sans", 28, 600, 240)), cx0 + 20, cy0 + 40, "sans", 28, 600, C["ivory"], "lt", a, 1.2, "left")
            bars(im, cx0 + 20, cy0 + 200, 230, 2, 26, 10, C["muted"], 0.5 * a)
        say(im, t, 8.0, 10.0, ("Courses. Sessions. Assignments.", "One login."), 1420, 44, C["champ"], "sans", 500)
    say(im, t, 10.0, 11.0, "Now they stay.", 820, 104, C["gold_l"])
    endcard(im, t, 11.0, ("Win the second", "they decide."), "DM 'ENROL' to begin")
    return im


# =====================================================================  15  family businesses
PAPER = (238, 230, 214)
INK = (40, 34, 28)


def a15(m):
    m.add(sfx.paper_snap(), 0, 1.0)
    m.add(sfx.low_thud(0.5), 0, 0.45)
    m.add(sfx.pen_scratch(0.6), 0.02, 0.35)
    m.bed(sfx.pad(15, "fmaj", 650, 0.1), 0.12)
    for tt in (1.8, 3.8, 5.8, 7.8, 9.8, 11.6):
        m.add(sfx.pen_scratch(0.45), tt, 0.3)
    end_sting(m, 13.0, 0.3)


M15 = dict(
    type="Letter to the viewer", industry="Family businesses", palette="Ivory paper with ink and gold (the light variant of the palette)",
    hook="To the owner still saying 'next month'…",
    beats=[
        ("0.0–1.8", "Frame 0: a handwritten note on warm ivory paper; a pen line is already drawing under the salutation and the paper floats slightly."),
        ("1.8–3.8", "The salutation shrinks to the top like a real letter: 'You built this name over years.'"),
        ("3.8–5.8", "'Your customers now meet it on a phone.'"),
        ("5.8–7.8", "'Tonight, someone searched for exactly what you sell.'"),
        ("7.8–9.8", "'What did they find?'"),
        ("9.8–11.6", "'Let them find you, the way you deserve.'"),
        ("11.6–13.0", "Signed in hand: '— the DeveraXTech team'."),
        ("13.0–15.0", "End card on the paper: 'Make it this month.' + Reply 'THIS MONTH' in our DMs."),
    ],
    sound="0.00 a crisp paper snap and pen scratch over a soft thud; a warm, quiet F-major pad; a pen scratch as each line is written. Calm on purpose: the contrast with louder reels is the stop.",
    cta="Make it this month. Reply 'THIS MONTH' in our DMs.",
    why="Being addressed personally, in handwriting, is rare in a feed of shouting reels. 'Next month' is a phrase every owner has said about their website, so the line feels like it was written to them.",
)


@reel(15, "letter-next-month", 15.0, a15, M15, grain=4, qc=[0.3, 2.5, 6.5, 10.5, 12.0, 14.0])
def r15(t):
    im = bg((214, 204, 184), PAPER, cy=900, r=1300)
    fl = 4 * SIN(t * 1.3)
    if t < 13.0:
        sh = eio(prog(t, 1.8, 2.3))
        size = 104 - 42 * sh
        y = 600 - 280 * sh + fl
        a = win(t, -1, 13.0, 0, 0.25)
        txt(im, "To the owner still", SX0 + 20, y, "hand", size, 600, INK, "lm", a)
        txt(im, "saying 'next month'…", SX0 + 20, y + size * 1.05, "hand", size, 600, INK, "lm", a)
        k = 0.25 + 0.75 * eo(prog(t, 0, 1.4))
        w = text_w("saying 'next month'…", "hand", int(size), 600)
        line(im, [(SX0 + 20, y + size * 1.62), (SX0 + 20 + w * k, y + size * 1.58)], C["gold_d"], 4, a)
        lines = [(1.8, 3.8, "You built this name over years."), (3.8, 5.8, "Your customers now meet it on a phone."),
                 (5.8, 7.8, "Tonight, someone searched for exactly what you sell."), (7.8, 9.8, "What did they find?"),
                 (9.8, 11.6, "Let them find you, the way you deserve.")]
        for t0, t1, s in lines:
            if t0 <= t < t1:
                ln = wrap(s, "hand", 88, 600, 820)
                al = win(t, t0, t1, 0.0, 0.18)
                sp = block(ln, "hand", 88, 600, INK, 1.1, "left")
                rv = eo(prog(t, t0, t0 + 0.45))
                crop = sp.crop((0, 0, max(1, int(sp.width * rv)), sp.height))
                put(im, crop, SX0 + 20, 820 + fl, "lm", al)
        if 11.6 <= t < 13.0:
            al = win(t, 11.6, 13.0, 0.2, 0.2)
            txt(im, "— the DeveraXTech team", SX1 - 20, 1000 + fl, "hand", 70, 600, C["gold_d"], "rm", al)
    endcard(im, t, 13.0, ("Make it", "this month."), "Reply 'THIS MONTH' in our DMs", C["gold_d"], INK, cta_family="hand",
            cta_size=110)
    return im


# =====================================================================  16  marketing agencies (white-label)
def a16(m):
    m.add(sfx.tom(), 0, 1.0)
    m.add(sfx.bass_hit(0.9, 100, 40), 0, 0.5)
    m.bed(sfx.pulse_bed(13, 92, 52), 0.12, end=11.0)
    tick_beats(m, [1.8, 3.2, 4.6, 6.4], sfx.tom, 0.25)
    m.add(sfx.whoosh(0.5), 7.6, 0.25)
    m.add(sfx.metal_click(), 8.3, 0.35)
    tick_beats(m, [9.8])
    end_sting(m, 11.0)


M16 = dict(
    type="Unpopular opinion", industry="Marketing agencies (white-label partners)", palette="Obsidian with a deep-emerald accent",
    hook="Agencies: stop building your own websites.",
    beats=[
        ("0.0–1.8", "Frame 0: small emerald label UNPOPULAR OPINION over the hook; the frame is shaking off a drum hit and a gold underline is drawing under 'stop'."),
        ("1.8–3.2", "'Your edge is strategy.'"),
        ("3.2–4.6", "'Not debugging at 2am.'"),
        ("4.6–6.4", "'Every hour in code is an hour not selling.'"),
        ("6.4–7.6", "'Partner with a build team.'"),
        ("7.6–9.8", "Two stacked cards slide apart: front, emerald 'Your agency: strategy, brand, the client'; behind, gold-outlined 'Build partner: design, code, launch'. Caption: 'White-label. Your name on the front.'"),
        ("9.8–11.0", "'Agree? Disagree? Comments are open.'"),
        ("11.0–13.0", "End card: 'Your name on it. Our build behind it.' + DM 'PARTNER'."),
    ],
    sound="0.00 low tom hit with a sub; a 92 bpm pulse; softer toms under each statement; whoosh and a metallic click as the cards separate.",
    cta="Your name on it. Our build behind it. DM 'PARTNER' for white-label builds.",
    why="'Unpopular opinion' is a fight invitation, and telling agencies to stop doing something they sell is defensible but provocative, which drives comments. The payoff turns the argument into a partnership offer.",
)


@reel(16, "agencies-stop-building", 13.0, a16, M16, push=1.8, qc=[0.2, 2.5, 5.5, 8.6, 10.4, 12.0])
def r16(t):
    im = bg(C["obs"], (12, 30, 25))
    if t < 1.8:
        shake = 12 * math.exp(-t * 6) * SIN(t * 60)
        eyebrow(im, "Unpopular opinion", SCX, 470, C["emer_l"])
        txt(im, "Agencies:", SCX + shake, 600, "serif", 104, 600, C["ivory"])
        txt(im, "stop building", SCX + shake, 720, "serif", 104, 600, C["ivory"])
        txt(im, "your own websites.", SCX + shake, 840, "serif_i", 92, 500, C["emer_l"])
        ws = text_w("stop building", "serif", 104, 600)
        wst = text_w("stop", "serif", 104, 600)
        x0 = SCX - ws / 2 + shake
        k = 0.3 + 0.7 * eo(t / 0.6)
        hline(im, x0, x0 + wst * k, 785, C["gold"], 6)
    say(im, t, 1.8, 3.2, ("Your edge", "is strategy."), 820, 108)
    say(im, t, 3.2, 4.6, ("Not debugging", "at 2am."), 820, 108, C["emer_l"])
    say(im, t, 4.6, 6.4, ("Every hour in code is", "an hour not selling."), 820, 80)
    say(im, t, 6.4, 7.6, ("Partner with", "a build team."), 820, 104, C["gold_l"])
    if 7.6 <= t < 9.8:
        a = win(t, 7.6, 9.8, 0.15, 0.15)
        k = eio(prog(t, 7.8, 8.4))
        back = (SX0 + 60, 560 + 300 * k, SX1 - 20, 1000 + 300 * k)
        front = (SX0 + 20, 520, SX1 - 60, 960)
        rrect(im, back, 30, C["obs2"], C["gold"], 3, a)
        txt(im, "Build partner", back[0] + 40, back[3] - 150, "serif", 52, 600, C["gold_l"], "lm", a * k)
        txt(im, "Design · Code · Launch", back[0] + 40, back[3] - 80, "sans", 32, 500, C["ivory"], "lm", a * k)
        rrect(im, front, 30, C["emer"], C["emer_l"], 2, a)
        txt(im, "Your agency", front[0] + 40, front[1] + 90, "serif", 64, 600, C["ivory"], "lm", a)
        txt(im, "Strategy · Brand · The client", front[0] + 40, front[1] + 170, "sans", 32, 500, C["ivory"], "lm", a)
        say(im, t, 8.2, 9.8, ("White-label.", "Your name on the front."), 1430, 48, C["champ"], "sans", 500)
    say(im, t, 9.8, 11.0, ("Agree? Disagree?", "Comments are open."), 820, 96)
    endcard(im, t, 11.0, ("Your name on it.", "Our build behind it."), "DM 'PARTNER' for white-label builds", C["emer_l"])
    return im


# =====================================================================  17  any business (viewer challenge)
def a17(m):
    m.add(sfx.glass(), 0, 1.0)
    m.add(sfx.bass_hit(0.6, 150, 55), 0, 0.45)
    m.bed(sfx.pad(12, "fmaj", 900), 0.09)
    tick_beats(m, [1.6, 3.2])
    for tt in (4.4, 5.4, 6.4, 7.4):
        m.add(sfx.glass(0.6), tt, 0.25)
    tick_beats(m, [8.6])
    end_sting(m, 10.0)


M17 = dict(
    type="Viewer challenge", industry="Any business", palette="Gold-dominant",
    hook="Drop your website. One honest note.",
    beats=[
        ("0.0–1.6", "Frame 0: hook in gold and ivory; under it an empty URL field ('yourwebsite.com') with a blinking caret, and a gold arrow already bouncing down towards the comments."),
        ("1.6–3.2", "'We'll tell you the first thing a client notices.'"),
        ("3.2–4.4", "'Usually, one of these:'"),
        ("4.4–8.6", "One per second, big, with a glass tap each: The headline. / The first photo. / How it looks on a phone. / How fast it opens."),
        ("8.6–10.0", "'One note. Straight answer.'"),
        ("10.0–12.0", "End card: 'Your link. Our honest note.' + comment it, or DM 'NOTE' to keep it private."),
    ],
    sound="0.00 a single glass tap with a light sub; F-major pad; a softer glass tap on each item; thud + crystal on the end card.",
    cta="Your link. Our honest note. Comment it, or DM 'NOTE' to keep it private.",
    why="A direct invitation with a concrete reward (a free, specific note on your own site) is hard to scroll past, and it is built for comments and DMs. It is about the viewer's site from the first word.",
    placeholders=["Karim must be ready to reply to every link posted; the reel promises one honest note"],
)


@reel(17, "drop-your-website", 12.0, a17, M17, push=1.6, qc=[0.3, 2.0, 5.0, 7.8, 9.0, 11.0])
def r17(t):
    im = bg(C["obs"], (34, 28, 14))
    if t < 1.6:
        txt(im, "Drop your website.", SCX, 560, "serif", fit_size("Drop your website.", "serif", 600, 860, 100), 600, C["gold_l"])
        txt(im, "One honest note.", SCX, 680, "serif_i", 92, 500, C["ivory"])
        bx = (SX0 + 20, 860, SX1 - 20, 960)
        rrect(im, bx, 50, C["obs2"], C["gold"], 2)
        tw, _ = txt(im, "yourwebsite.com", bx[0] + 50, 910, "sans", 40, 500, C["muted"], "lm")
        if int(t * 3) % 2 == 0:
            rect(im, (bx[0] + 56 + tw, 885, bx[0] + 60 + tw, 935), C["gold"])
        by = 1150 + 34 * abs(SIN(t * 5))
        line(im, [(SCX, by - 120), (SCX, by)], C["gold"], 5)
        line(im, [(SCX - 40, by - 40), (SCX, by), (SCX + 40, by - 40)], C["gold"], 5)
    say(im, t, 1.6, 3.2, ("We'll tell you the first", "thing a client notices."), 820, 80)
    say(im, t, 3.2, 4.4, "Usually, one of these:", 820, 84, C["champ"])
    items = ["The headline.", "The first photo.", "How it looks on a phone.", "How fast it opens."]
    for i, s in enumerate(items):
        t0 = 4.4 + i
        if t0 <= t < t0 + 1.0:
            a = win(t, t0, t0 + 1.0, 0.06, 0.08)
            txt(im, f"{i + 1}", SCX, 640, "serif", 200, 700, C["gold"], alpha=a)
            txt(im, s, SCX, 900, "serif", fit_size(s, "serif", 600, 860, 96), 600, C["ivory"], alpha=a)
    say(im, t, 8.4, 10.0, ("One note.", "Straight answer."), 820, 108, C["gold_l"])
    endcard(im, t, 10.0, ("Your link.", "Our honest note."), "Comment it, or DM 'NOTE' to keep it private")
    return im


# =====================================================================  18  dental practices
@lru_cache(maxsize=1)
def dental_site():
    im = Image.new("RGB", (W, H), C["obs"])
    x0, y0, x1, y1 = browser(im, (SX0, 540, SX1, 1460), "light")
    txt(im, "Your Clinic", x0 + 40, y0 + 46, "serif", 38, 700, C["ink"], "lm")
    for i in range(3):
        rect(im, (x1 - 300 + i * 90, y0 + 40, x1 - 240 + i * 90, y0 + 50), (150, 140, 122))
    photo(im, (x0 + 30, y0 + 100, x1 - 30, y0 + 420), (210, 214, 216), (150, 160, 168), radius=18)
    with Vec(im) as d:
        d.chord((SCX - 150, y0 + 180, SCX + 150, y0 + 380), 200, 340, None, brush(C["white"]))
    txt(im, "stock photo", x1 - 50, y0 + 400, "sans", 18, 500, (110, 110, 110), "rm")
    txt(im, "Hours: Sat–Thu · call to confirm", x0 + 40, y0 + 480, "sans", 30, 500, (80, 74, 64), "lm")
    txt(im, "Book: call [phone] (9am–5pm)", x0 + 40, y0 + 540, "sans", 30, 500, (80, 74, 64), "lm")
    rrect(im, (x0 + 30, y0 + 600, x1 - 30, y1 - 30), 18, (226, 222, 210), (205, 196, 180), 2)
    for i in range(6):
        line(im, [(x0 + 30, y0 + 640 + i * 40), (x1 - 30, y0 + 610 + i * 46)], (205, 196, 180), 2)
    cx, cy = x1 - 200, y0 + 690
    circle(im, cx, cy, 22, fill=(190, 60, 50))
    with Vec(im) as d:
        d.polygon([cx - 18, cy + 10, cx, cy + 46, cx + 18, cy + 10], None, brush((190, 60, 50)))
    txt(im, "Main entrance →", x0 + 70, y1 - 70, "sans", 22, 600, (110, 100, 90), "lm")
    return im


@lru_cache(maxsize=1)
def dental_blur():
    return dental_site().filter(ImageFilter.GaussianBlur(9))


LENS = [(0.0, (330, 860)), (1.8, (SCX, 840)), (3.2, (420, 1076)), (4.6, (430, 1136)), (6.0, (740, 1290)),
        (7.4, (SCX, 1000)), (9.0, (SCX, 1000))]


def lens_pos(t):
    if t < 1.8:
        return 330 + 180 * eio(prog(t, 0, 1.8)), 860
    prev = LENS[0][1]
    cur = LENS[0][1]
    for t0, p in LENS:
        if t >= t0:
            prev, cur, ts = cur, p, t0
    k = eio(prog(t, ts, ts + 0.5))
    if ts == 1.8:
        prev = (510, 860)
    return prev[0] + (cur[0] - prev[0]) * k, prev[1] + (cur[1] - prev[1]) * k


def a18(m):
    m.add(sfx.porcelain(), 0, 1.0)
    m.add(sfx.bass_hit(0.6, 150, 60), 0, 0.4)
    m.bed(sfx.air(13), 0.04)
    m.bed(sfx.pad(13, "cmaj", 1100), 0.08)
    for tt in (1.8, 3.2, 4.6, 6.0, 7.4):
        m.add(sfx.porcelain(0.4), tt, 0.35)
    tick_beats(m, [9.0], sfx.low_thud, 0.3)
    end_sting(m, 11.0)


M18 = dict(
    type="Insider truth", industry="Dental practices", palette="Near-monochrome, porcelain white and ivory",
    hook="What your patients notice that you don't.",
    beats=[
        ("0.0–1.8", "Frame 0: a blurred dental clinic homepage; a magnifying lens is already gliding across it, everything inside the lens sharp. Hook at the top."),
        ("1.8–3.2", "The lens lands on the hero image: 'A stock-photo smile.'"),
        ("3.2–4.6", "On the hours line: 'Hours that say call to confirm.'"),
        ("4.6–6.0", "On the booking line: 'No way to book after 5pm.'"),
        ("6.0–7.4", "On the map: 'A pin at the wrong entrance.'"),
        ("7.4–9.0", "Lens widens: 'Whether the site feels as clean as your clinic.'"),
        ("9.0–11.0", "'They notice. Before the chair.'"),
        ("11.0–13.0", "End card: 'See your clinic through their eyes.' + DM 'SMILE'."),
    ],
    sound="0.00 a porcelain clink (clean, clinical, not a drill) over a light sub; air texture and a bright C-major pad; a smaller clink at every observation.",
    cta="See your clinic through their eyes. DM 'SMILE' for a patient's-eye look.",
    why="'That you don't' is a gentle insult to the owner's attention to detail, which is exactly what dentists pride themselves on. Every observation is specific and checkable on their own site tonight, with no invented data.",
    placeholders=["[phone] on the mockup's booking line (generic placeholder, not a real number)"],
)


@reel(18, "patients-notice", 13.0, a18, M18, qc=[0.5, 2.4, 5.0, 6.6, 8.0, 12.0])
def r18(t):
    im = bg(C["obs"], (26, 26, 26))
    if t < 11.0:
        a = win(t, -1, 11.0, 0, 0.25)
        site = dental_site()
        if a < 1:
            im = Image.blend(im, dental_blur(), a)
        else:
            im = dental_blur().copy()
        lx, ly = lens_pos(t)
        r = 150 + 120 * eio(prog(t, 7.4, 8.0)) - 100 * eio(prog(t, 9.0, 10.0))
        mag = 1.25
        src = int(r / mag)
        crop = site.crop((int(lx - src), int(ly - src), int(lx + src), int(ly + src))).resize((int(2 * r), int(2 * r)), Image.BICUBIC)
        mask = Image.new("L", crop.size, 0)
        ImageDraw.Draw(mask).ellipse((0, 0, crop.size[0] - 1, crop.size[1] - 1), fill=int(255 * a))
        im.paste(crop, (int(lx - r), int(ly - r)), mask)
        circle(im, lx, ly, r, outline=C["ivory"], width=4, alpha=a)
        plate(im, 220, 500, 0.85 * a)
    if t < 1.8:
        txt(im, "What your patients", SCX, 320, "serif", 82, 600, C["ivory"])
        txt(im, "notice that you don't.", SCX, 415, "serif_i", 82, 500, C["white"])
    obs = [(1.8, 3.2, "A stock-photo smile."), (3.2, 4.6, ("Hours that say", "'call to confirm'.")),
           (4.6, 6.0, ("No way to book", "after 5pm.")), (6.0, 7.4, ("A pin at the", "wrong entrance.")),
           (7.4, 9.0, ("Whether it feels as clean", "as your clinic."))]
    for t0, t1, s in obs:
        say(im, t, t0, t1, s, 360, 70)
    say(im, t, 9.0, 11.0, ("They notice.", "Before the chair."), 360, 78, C["white"])
    endcard(im, t, 11.0, ("See your clinic", "through their eyes."), "DM 'SMILE' for a patient's-eye look", C["champ"])
    return im
