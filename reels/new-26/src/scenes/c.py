"""Reels 19-26."""
import math

import sfx
from dx import *  # noqa: F401,F403
from dx import C, SCX, SX0, SX1, W, H
from . import reel
from .a import end_sting, tick_beats
from .b import plate

SIN = math.sin


# =====================================================================  19  interior & furniture showrooms
def room(im, s, cx, cy, a=1.0, hot=0.0, t=0.0):
    """Abstract showroom scene in a 900x900 unit box centred on (cx, cy), scaled by s."""
    def P(x, y):
        return cx + x * s, cy + y * s

    x0, y0 = P(-450, -450)
    x1, y1 = P(450, 450)
    photo(im, (x0, y0, x1, P(0, 120)[1]), (92, 80, 64), (60, 50, 40), a, 0)
    photo(im, (x0, P(0, 120)[1], x1, y1), (48, 38, 30), (26, 20, 16), a, 0)
    # window light
    with Vec(im) as d:
        d.polygon(list(sum([P(-380, -400), P(-120, -400), P(20, 120), P(-300, 120)], ())), None,
                  brush(C["champ"], 0.12 * a))
    # artwork
    rrect(im, (*P(60, -320), *P(300, -120)), 4, (40, 34, 28), C["champ"], 3, a)
    line(im, [P(90, -170), P(160, -240), P(210, -200), P(270, -260)], C["gold_l"], 2, a)
    # rug
    with Vec(im) as d:
        d.ellipse((*P(-330, 170), *P(330, 330)), None, brush((120, 104, 84), a))
    # sofa
    rrect(im, (*P(-300, 20), *P(260, 200)), 40 * s, (196, 182, 160), alpha=a)
    rrect(im, (*P(-330, 90), *P(-250, 230)), 30 * s, (182, 168, 146), alpha=a)
    rrect(im, (*P(210, 90), *P(290, 230)), 30 * s, (182, 168, 146), alpha=a)
    rrect(im, (*P(-240, 110), *P(200, 200)), 26 * s, (206, 194, 172), alpha=a)
    # lamp
    line(im, [P(360, 240), P(360, -60)], C["gold"], max(2, int(4 * s)), a)
    with Vec(im) as d:
        d.polygon(list(sum([P(310, -60), P(410, -60), P(385, -140), P(335, -140)], ())), None, brush(C["champ"], a))
    circle(im, *P(360, -40), 90 * s, fill=C["gold_l"], alpha=0.12 * a)
    if hot > 0:
        for (hx, hy), lab in [((-20, 80), "Sofa"), ((360, -100), "Floor lamp"), ((0, 260), "Wool rug")]:
            px, py = P(hx, hy)
            ph = (t * 1.2) % 1
            circle(im, px, py, 14 + 26 * ph, outline=C["ivory"], width=3, alpha=hot * a * (1 - ph))
            circle(im, px, py, 12, fill=C["ivory"], alpha=hot * a)
            w, _ = txt(im, lab, px + 30, py, "sans", 28, 600, C["obs"], "lm", 0)
            rrect(im, (px + 22, py - 24, px + 50 + w, py + 24), 24, C["ivory"], alpha=hot * a)
            txt(im, lab, px + 36, py, "sans", 28, 600, C["obs"], "lm", hot * a)


def a19(m):
    m.add(sfx.boom_shimmer(), 0, 1.0)
    m.bed(sfx.pad(14, "cmaj", 800, 0.06), 0.12)
    tick_beats(m, [1.8, 3.2, 4.6])
    m.add(sfx.chime_stab(), 5.6, 0.3)
    for tt in (7.4, 7.7, 8.0):
        m.add(sfx.porcelain(0.4), tt, 0.25)
    tick_beats(m, [9.4])
    end_sting(m, 12.0)


M19 = dict(
    type="End-first", industry="Interior & furniture showrooms", palette="Champagne accent; one continuous push-in",
    hook="This took one decision.",
    beats=[
        ("0.0–1.8", "Frame 0: the finished, beautiful showroom homepage (a single styled room, warm light) is already slowly pushing in. Hook on a dark band above it."),
        ("1.8–3.2", "'Not more products.'"),
        ("3.2–4.6", "'Not more pages.'"),
        ("4.6–5.6", "'The decision:'"),
        ("5.6–7.2", "Champagne: 'Show one room. Perfectly.'"),
        ("7.2–9.4", "The push-in reaches the room; shoppable hotspots pulse on the sofa, lamp and rug with labels and a 'Shop this room' button."),
        ("9.4–12.0", "'Let them walk in before they visit.'"),
        ("12.0–14.0", "End card: 'Make the one decision.' + DM 'ONE ROOM'."),
    ],
    sound="0.00 a deep boom with a high shimmer tail (the size of a finished space); a soft C-major pad; ticks on the 'not' lines; a chime on the decision; three porcelain taps as hotspots appear.",
    cta="Make the one decision. DM 'ONE ROOM' to start.",
    why="Opening on the finished result is the reward first, which earns the next three seconds, and 'one decision' is a riddle the viewer wants solved. No before/after: the reel is about the decision, not a comparison.",
)


@reel(19, "one-decision-room", 14.0, a19, M19, qc=[0.5, 3.0, 6.0, 8.0, 10.5, 13.0])
def r19(t):
    im = bg(C["obs"], (28, 25, 20))
    if t < 12.0:
        a = win(t, -1, 12.0, 0, 0.25)
        p = prog(t, 0, 12.0)
        s = 0.86 + 0.34 * eio(p)
        x0, y0, x1, y1 = browser(im, (SX0, 540, SX1, 1460), "dark", a)
        mask_box = (x0 + 16, y0 + 70, x1 - 16, y1 - 120)
        layer = Image.new("RGB", (int(mask_box[2] - mask_box[0]), int(mask_box[3] - mask_box[1])), C["obs"])
        room(layer, s * 0.95, layer.width / 2, layer.height / 2 + 40 * eio(p), 1.0, win(t, 7.2, 12.0, 0.3, 0.3), t)
        im.paste(layer, (int(mask_box[0]), int(mask_box[1])))
        txt(im, "YOUR SHOWROOM", x0 + 30, y0 + 36, "sans", 22, 600, C["champ"], "lm", a, tracking=4)
        txt(im, "The Living Room", x0 + 30, y1 - 70, "serif", 46, 600, C["ivory"], "lm", a)
        if t >= 7.6:
            k = eo(prog(t, 7.6, 8.0))
            button(im, (x1 - 300, y1 - 100, x1 - 30, y1 - 40), "Shop this room", C["champ"], C["obs"], 24, a * k)
        plate(im, 220, 520, 0.85 * a)
    if t < 1.8:
        txt(im, "This took", SCX, 320, "serif", 96, 600, C["ivory"])
        txt(im, "one decision.", SCX, 425, "serif_i", 96, 500, C["champ"])
    say(im, t, 1.8, 3.2, "Not more products.", 380, 80)
    say(im, t, 3.2, 4.6, "Not more pages.", 380, 80)
    say(im, t, 4.6, 5.6, "The decision:", 380, 80, C["muted"])
    say(im, t, 5.6, 7.2, ("Show one room.", "Perfectly."), 380, 80, C["champ"])
    say(im, t, 7.2, 9.4, "Every piece, one tap away.", 380, 62)
    say(im, t, 9.4, 12.0, ("Let them walk in", "before they visit."), 380, 78)
    endcard(im, t, 12.0, ("Make the", "one decision."), "DM 'ONE ROOM' to start", C["champ"])
    return im


# =====================================================================  20  coaches & consultants
EXCUSES = ["“I'm too busy.”", "“Clients find me on Instagram.”", "“It's fine for now.”",
           "“After my next launch.”", "“My nephew is on it.”"]


def a20(m):
    m.add(sfx.marker_strike(), 0, 1.0)
    m.add(sfx.bass_hit(0.7, 140, 50), 0, 0.55)
    for i in range(1, 5):
        m.add(sfx.marker_strike(), i * 1.25 + 0.35, 0.55)
    m.bed(sfx.pulse_bed(14, 96, 55), 0.1, end=6.4)
    m.add(sfx.bass_hit(1.0, 110, 40), 6.4, 0.6)
    m.add(sfx.crystal(2.0, 1318.5), 6.45, 0.2)
    m.bed(sfx.pad(8, "fmaj", 800), 0.1, start=6.4, end=14.0)
    tick_beats(m, [8.2])
    m.add(sfx.whoosh(0.5), 9.2, 0.2)
    end_sting(m, 12.0)


M20 = dict(
    type="Wrong answers only", industry="Coaches & consultants", palette="Gold strikes on obsidian",
    hook="Wrong answers only: why isn't it fixed?",
    beats=[
        ("0.0–1.25", "Frame 0: hook at the top; the first excuse, “I'm too busy.”, is already on screen with a gold strike racing through it."),
        ("1.25–6.4", "Excuses stack and get struck through every 1.25 s: Clients find me on Instagram / It's fine for now / After my next launch / My nephew is on it."),
        ("6.4–8.2", "The list falls away. 'The honest answer:' then, in gold and not struck: 'You don't know who to trust with it.'"),
        ("8.2–9.4", "'Fair. Look at the work first.'"),
        ("9.4–12.0", "OUR BUILD: Karim Ahmed's full-stack developer portfolio (shown as it is), the kind of personal-brand site a consultant needs."),
        ("12.0–14.0", "End card: 'Ask us anything. Then decide.' + DM 'HONEST'."),
    ],
    sound="0.00 marker strike (swish + knock) over a sub hit; a strike on every excuse; a 96 bpm pulse that drops out when the honest answer lands on a bigger hit and a crystal note; a pad under the rest.",
    cta="Ask us anything. Then decide. DM 'HONEST' to start.",
    why="'Wrong answers only' is a comment format people already play, and every excuse is one the viewer has said. The honest last answer (trust) is the real objection, and the CTA answers it directly.",
)


@reel(20, "wrong-answers-only", 14.0, a20, M20, qc=[0.2, 3.0, 6.0, 7.2, 10.5, 13.0])
def r20(t):
    im = bg(C["obs"], (30, 26, 18))
    if t < 6.4:
        txt(im, "Wrong answers only:", SCX, 330, "serif", 80, 600, C["ivory"])
        txt(im, "why isn't it fixed?", SCX, 425, "serif_i", 80, 500, C["gold_l"])
        a = win(t, -1, 6.4, 0, 0.2)
        for i, e in enumerate(EXCUSES):
            ti = i * 1.25
            if t < ti and i > 0:
                continue
            k = 1.0 if i == 0 else eo(prog(t, ti, ti + 0.25))
            y = 580 + i * 160
            size = fit_size(e, "serif_i", 500, 840, 64)
            w, _ = txt(im, e, SCX, y + (1 - k) * 20, "serif_i", size, 500, C["ivory"], alpha=a * k * (0.55 if t > ti + 1.0 else 1))
            sk = 0.3 + 0.7 * eo(prog(t, -0.05, 0.45)) if i == 0 else eo(prog(t, ti + 0.35, ti + 0.7))
            strike(im, SCX - w / 2 - 10, SCX + w / 2 + 10, y + 4, sk, C["gold"], 5, a)
    if 6.4 <= t < 8.2:
        a = win(t, 6.4, 8.2, 0.1, 0.15)
        txt(im, "The honest answer:", SCX, 640, "sans", 40, 500, C["muted"], alpha=a)
        para(im, ("You don't know", "who to trust", "with it."), SCX, 860, "serif", 104, 600, C["gold_l"], alpha=a)
    say(im, t, 8.2, 9.4, ("Fair.", "Look at the work first."), 820, 88)
    if 9.4 <= t < 12.0:
        a = win(t, 9.4, 12.0, 0.2, 0.2)
        eyebrow(im, "Our build", SCX, 400, alpha=a)
        txt(im, "A developer's portfolio", SCX, 470, "serif", 58, 600, C["ivory"], alpha=a)
        x0, y0, x1, y1 = browser(im, (SX0, 560, SX1, 1400), "dark", a)
        rect(im, (x0 + 2, y0, x1 - 2, y1 - 2), (24, 24, 26), a)
        txt(im, "KA", x0 + 40, y0 + 46, "sans", 30, 700, C["white"], "lm", a)
        for i in range(4):
            rect(im, (x1 - 380 + i * 90, y0 + 42, x1 - 320 + i * 90, y0 + 50), C["muted"], a)
        txt(im, "Karim Ahmed", x0 + 40, y0 + 230, "serif", 84, 600, C["white"], "lm", a)
        txt(im, "Full-Stack (MERN) Developer", x0 + 40, y0 + 320, "sans", 36, 500, (160, 200, 255), "lm", a)
        bars(im, x0 + 40, y0 + 390, x1 - x0 - 160, 3, 28, 12, C["muted"], 0.5 * a)
        button(im, (x0 + 40, y0 + 520, x0 + 300, y0 + 590), "View projects", (160, 200, 255), C["obs"], 26, a)
        for i in range(3):
            rrect(im, (x0 + 40 + i * 245, y0 + 640, x0 + 265 + i * 245, y1 - 40), 14, (36, 36, 40), (60, 60, 66), 2, a)
    endcard(im, t, 12.0, ("Ask us anything.", "Then decide."), "DM 'HONEST' to start")
    return im


# =====================================================================  21  events & weddings
N_RECT = 14
TARGETS = [(SX0 + 20, 560, SX1 - 20, 900), (SX0 + 20, 930, SCX - 10, 1130), (SCX + 10, 930, SX1 - 20, 1130),
           (SX0 + 20, 1160, SCX - 10, 1360), (SCX + 10, 1160, SX1 - 20, 1360), (SCX - 180, 1390, SCX + 180, 1460)]
LABELS = ["Save the date", "Venue", "Schedule", "Gallery", "Stay", "RSVP"]


def tunnel_rects(t):
    speed = 1.6 * (1 - eo(prog(t, 0, 3.2))) + 0.05
    # integrate speed for a smooth deceleration
    tt = min(t, 3.2)
    pos = 0.0
    steps = 40
    for i in range(steps):
        u = tt * (i + 0.5) / steps
        pos += (1.6 * (1 - eo(u / 3.2)) + 0.05) * tt / steps
    pos += 0.05 * max(0, t - 3.2)
    f = pos % 1.0
    out = []
    for i in range(N_RECT):
        d = i + f
        sc = 0.07 * (1.32 ** d)
        out.append((d, sc))
    return out, speed


def a21(m):
    m.add(sfx.whoosh_hit(), 0, 1.0)
    m.add(sfx.bass_hit(1.2, 90, 35), 0, 0.6)
    m.bed(sfx.whoosh(3.2), 0.25, start=0.1, end=3.3, fade=0.6)
    tick_beats(m, [2.0])
    m.add(sfx.riser(1.2), 2.6, 0.2)
    m.add(sfx.crystal(2.5, 1046.5), 3.4, 0.3)
    m.bed(sfx.pad(11, "bbmaj", 900), 0.11, start=3.2)
    tick_beats(m, [6.0, 7.2])
    for i in range(6):
        m.add(sfx.porcelain(0.3), 8.6 + i * 0.18, 0.18)
    end_sting(m, 12.0)


M21 = dict(
    type="Optical illusion", industry="Events & weddings", palette="Gold-dominant",
    hook="Look again. Your eyes lied.",
    beats=[
        ("0.0–2.0", "Frame 0: an infinite tunnel of gold frames is already rushing towards the viewer; the brain reads depth. Hook on a dark band."),
        ("2.0–3.2", "The tunnel slows: 'It's flat.' (it is only nested rectangles)."),
        ("3.2–6.0", "The frames slide apart and resolve, one by one, into a flat website layout: hero, four tiles and a button."),
        ("6.0–7.2", "'Your guests do this too.'"),
        ("7.2–8.6", "'They feel the event before they arrive.'"),
        ("8.6–10.0", "The layout fills in as an event site: Save the date / Venue / Schedule / Gallery / Stay / RSVP."),
        ("10.0–12.0", "OUR BUILD: Agora, an event management platform built for a university."),
        ("12.0–14.0", "End card: 'Make them feel it before they arrive.' + DM 'EVENT'."),
    ],
    sound="0.00 a whoosh that already peaks on the first frame, on a sub; a sustained rush while the tunnel moves; a riser into a crystal note as it flattens; B-flat pad; little porcelain ticks as each tile fills.",
    cta="Make them feel it before they arrive. DM 'EVENT' to start.",
    why="Depth illusions force a double take, so the viewer re-reads the frame instead of swiping, and 'your eyes lied' is a challenge. The resolve into a layout is the 'aha', and it maps straight onto how guests judge an event from its page.",
)


@reel(21, "your-eyes-lied", 14.0, a21, M21, qc=[0.0, 1.0, 2.5, 4.5, 9.2, 11.0, 13.0])
def r21(t):
    im = bg(C["obs"], (34, 28, 14), cy=920)
    cx, cy = SCX, 960
    if t < 12.0:
        a = win(t, -1, 12.0, 0, 0.25)
        rects, _ = tunnel_rects(t)
        morph = eio(prog(t, 3.2, 5.6))
        for i, (d, sc) in enumerate(rects):
            hw, hh = 600 * sc, 1000 * sc
            box = (cx - hw, cy - hh, cx + hw, cy + hh)
            depth_a = clamp(d / 3.0) * clamp((N_RECT - d) / 2.0)
            ti = i % len(TARGETS) if i >= 4 and i < 4 + len(TARGETS) else None
            if ti is not None and morph > 0:
                k = eio(prog(t, 3.2 + (i - 4) * 0.25, 4.4 + (i - 4) * 0.25))
                tb = TARGETS[ti]
                box = tuple(box[j] + (tb[j] - box[j]) * k for j in range(4))
                al = depth_a + (1 - depth_a) * k
            else:
                al = depth_a * (1 - morph)
            if al > 0.01:
                rrect(im, box, 6 + 14 * morph, None, C["gold"], 3 if sc < 1 else 4, a * al)
        if t >= 8.6:
            for i, lab in enumerate(LABELS):
                k = eo(prog(t, 8.6 + i * 0.18, 8.9 + i * 0.18))
                b = TARGETS[i]
                if i == 0:
                    photo(im, (b[0] + 6, b[1] + 6, b[2] - 6, b[3] - 6), (80, 64, 34), (20, 16, 10), a * k)
                    txt(im, "Save the date", (b[0] + b[2]) / 2, b[1] + 130, "serif_i", 72, 500, C["gold_l"], alpha=a * k)
                    txt(im, "[Names] · [Date]", (b[0] + b[2]) / 2, b[1] + 220, "sans", 32, 500, C["ivory"], alpha=a * k)
                elif i == 5:
                    rrect(im, b, 35, C["gold"], alpha=a * k)
                    txt(im, "RSVP", (b[0] + b[2]) / 2, (b[1] + b[3]) / 2, "sans", 30, 700, C["obs"], alpha=a * k)
                else:
                    txt(im, lab, (b[0] + b[2]) / 2, (b[1] + b[3]) / 2, "serif", 44, 600, C["ivory"], alpha=a * k)
        plate(im, 220, 500, 0.86 * a)
    if t < 2.0:
        txt(im, "Look again.", SCX, 320, "serif", 96, 600, C["ivory"])
        txt(im, "Your eyes lied.", SCX, 425, "serif_i", 96, 500, C["gold_l"])
    say(im, t, 2.0, 3.2, "It's flat.", 370, 104, C["gold_l"])
    say(im, t, 3.2, 6.0, ("Just frames,", "becoming a page."), 370, 70, C["champ"], "serif_i", 500)
    say(im, t, 6.0, 7.2, ("Your guests", "do this too."), 370, 80)
    say(im, t, 7.2, 8.6, ("They feel the event", "before they arrive."), 370, 72)
    if 10.0 <= t < 12.0:
        say(im, t, 10.0, 12.0, ("Our build: Agora, an event", "platform for a university."), 370, 52, C["champ"], "sans", 500)
    endcard(im, t, 12.0, ("Make them feel it", "before they arrive."), "DM 'EVENT' to start")
    return im


# =====================================================================  22  logistics & B2B
def a22(m):
    m.add(sfx.ping(), 0, 1.0)
    m.add(sfx.bass_hit(0.6, 160, 60), 0, 0.45)
    for k in range(1, 9):
        m.add(sfx.tick(0.05), k * 1.0, 0.18)
    tick_beats(m, [1.8, 3.0, 4.4, 5.8, 6.8, 7.6, 8.4])
    m.bed(sfx.pulse_bed(13, 60, 50), 0.14, end=9.4)
    m.add(sfx.low_thud(), 9.4, 0.6)
    m.add(sfx.ping(1.2, 1046.5), 9.42, 0.45)
    end_sting(m, 11.0)


M22 = dict(
    type="Direct question with a number", industry="Logistics & B2B", palette="Near-monochrome with one gold numeral",
    hook="How many seconds does your homepage get?",
    beats=[
        ("0.0–1.8", "Frame 0: the question on top; below it a stopwatch whose hand is already sweeping and whose readout is already counting up."),
        ("1.8–3.0", "'Guess before the answer.' (the loop is explicit)"),
        ("3.0–4.4", "'A buyer is comparing suppliers.'"),
        ("4.4–5.8", "'Five tabs. One shortlist.'"),
        ("5.8–9.4", "'In those seconds they look for:' What you move. / Where you cover. / How to get a quote."),
        ("9.4–11.0", "The stopwatch stops on the answer in gold: '10–20 s', sourced on screen: Nielsen Norman Group, users often leave web pages within 10–20 seconds."),
        ("11.0–13.0", "End card: 'Make the first ten seconds sell.' + DM 'QUOTE'."),
    ],
    sound="0.00 a clean sonar-style ping on a sub; a soft tick every second like a stopwatch; a 60 bpm heartbeat pulse; clicks on text; a thud and a lower ping on the answer.",
    cta="Make the first ten seconds sell. DM 'QUOTE' to start.",
    why="A direct, answerable question with a number makes the viewer guess, and a guess is an investment they want to check. The answer is a published, citable figure, not an invented one.",
    placeholders=["Source on screen: Jakob Nielsen, 'How Long Do Users Stay on Web Pages?' (Nielsen Norman Group, 2011). Keep the wording 'often'"],
)


def stopwatch(im, t, cx, cy, r, stopped_at=None):
    tt = t if stopped_at is None else stopped_at
    circle(im, cx, cy, r, fill=C["obs2"], outline=C["line"], width=4)
    for i in range(60):
        ang = math.radians(i * 6 - 90)
        r0 = r - (34 if i % 5 == 0 else 18)
        line(im, [(cx + r0 * math.cos(ang), cy + r0 * math.sin(ang)), (cx + (r - 8) * math.cos(ang), cy + (r - 8) * math.sin(ang))],
             C["ivory"] if i % 5 == 0 else C["muted"], 3 if i % 5 == 0 else 1)
    ang = math.radians((tt % 1.0) * 360 - 90)
    line(im, [(cx, cy), (cx + (r - 50) * math.cos(ang), cy + (r - 50) * math.sin(ang))], C["gold"], 5)
    circle(im, cx, cy, 14, fill=C["gold"])
    rect(im, (cx - 20, cy - r - 40, cx + 20, cy - r - 4), C["line"])
    if stopped_at is None:
        txt(im, f"{tt:05.2f}", cx, cy + r * 0.45, "sans", 52, 600, C["ivory"])


@reel(22, "seconds-your-homepage-gets", 13.0, a22, M22, qc=[0.4, 2.2, 7.0, 9.8, 12.0])
def r22(t):
    im = bg(C["obs"], (24, 23, 21))
    if t < 11.0:
        a = win(t, -1, 11.0, 0, 0.2)
        if t < 5.8:
            stopwatch(im, t, SCX, 930, 300)
        elif t < 9.4:
            stopwatch(im, t, SCX, 1250, 170)
            for i, s in enumerate(["What you move.", "Where you cover.", "How to get a quote."]):
                ts = 6.8 + i * 0.8
                if t >= ts:
                    k = eo(prog(t, ts, ts + 0.25))
                    txt(im, s, SCX, 640 + i * 130, "serif", 76, 600, C["ivory"], alpha=k * win(t, 5.8, 9.4, 0, 0.15))
        else:
            k = eback(prog(t, 9.4, 9.75))
            glow_txt(im, "10–20 sec", SCX, 820, "serif", int(200 * max(k, 0.01)), 700, C["gold"], a, 26, 0.6)
            para(im, ("Users often leave web pages", "within 10–20 seconds."), SCX, 1060, "serif", 56, 500, C["ivory"], alpha=a)
            txt(im, "Source: Nielsen Norman Group (J. Nielsen, 2011)", SCX, 1210, "sans", 28, 500, C["muted"], alpha=a)
    if t < 1.8:
        txt(im, "How many seconds", SCX, 340, "serif", 86, 600, C["ivory"])
        txt(im, "does your homepage get?", SCX, 440, "serif_i", fit_size("does your homepage get?", "serif_i", 500, 860, 80), 500, C["gold_l"])
    say(im, t, 1.8, 3.0, ("Guess before", "the answer."), 390, 84, C["gold_l"])
    say(im, t, 3.0, 4.4, ("A buyer is comparing", "suppliers."), 390, 76)
    say(im, t, 4.4, 5.8, ("Five tabs.", "One shortlist."), 390, 84)
    say(im, t, 5.8, 9.4, "In those seconds they look for:", 420, 52, C["champ"], "sans", 500)
    say(im, t, 9.4, 11.0, "The answer:", 420, 52, C["muted"], "sans", 500, fi=0.05)
    endcard(im, t, 11.0, ("Make the first", "ten seconds sell."), "DM 'QUOTE' to start")
    return im


# =====================================================================  23  premium / luxury brands
def a23(m):
    m.add(sfx.crystal(), 0, 1.0)
    m.add(sfx.low_thud(0.5), 0, 0.45)
    m.add(sfx.whoosh(0.4), 0.02, 0.25)
    for tt in (1.2, 2.6, 4.0, 5.4):
        m.add(sfx.whoosh(0.35), tt, 0.25)
        m.add(sfx.click(0.03, 2500), tt + 0.3, 0.25)
    m.bed(sfx.air(13), 0.04)
    m.add(sfx.crystal(3.0, 1568), 6.8, 0.35)
    end_sting(m, 11.0)


M23 = dict(
    type="Luxury code", industry="Premium & luxury brands", palette="Near-monochrome, maximum negative space",
    hook="What luxury homepages never show.",
    beats=[
        ("0.0–1.2", "Frame 0: a cluttered homepage (discount banner, five buttons, shouting headline); a pop-up is already sliding off the page."),
        ("1.2–2.6", "'Discount banners.' The banner lifts away."),
        ("2.6–4.0", "'Five buttons fighting.' Four of them drop out."),
        ("4.0–5.4", "'Pop-ups in the first second.' (the one we just saw leave)"),
        ("5.4–6.8", "'Exclamation marks!' The marks fall off the headline."),
        ("6.8–8.2", "What is left: a serif name, one image, one quiet link. Lots of space."),
        ("8.2–9.6", "'They leave space.'"),
        ("9.6–11.0", "'Space reads as confidence.'"),
        ("11.0–13.0", "End card: 'Say less. Mean more.' + DM 'QUIET LUXURY'."),
    ],
    sound="0.00 a single crystal-bowl strike over a soft thud, with a short whoosh for the pop-up leaving; a whoosh and click for each removal; air only otherwise; a higher crystal note when the page goes quiet.",
    cta="Say less. Mean more. DM 'QUIET LUXURY' to start.",
    why="'Never' plus 'luxury' promises insider knowledge, and the viewer is shown a page that looks like many real ones, so they check their own. The reel itself practises the point: it gets quieter as it goes.",
)


@reel(23, "luxury-never-shows", 13.0, a23, M23, qc=[0.3, 1.6, 3.2, 5.8, 7.5, 12.0])
def r23(t):
    im = bg(C["obs"], (22, 22, 22))
    if t < 11.0:
        a = win(t, -1, 11.0, 0, 0.2)
        x0, y0, x1, y1 = browser(im, (SX0, 560, SX1, 1460), "dark", a)
        # banner
        kb = eio(prog(t, 1.2, 1.6))
        if kb < 1:
            rect(im, (x0 + 2, y0 - 60 * kb, x1 - 2, y0 + 70 - 60 * kb), (190, 40, 40), a * (1 - kb))
            txt(im, "FLASH SALE · 50% OFF · TODAY ONLY", SCX, y0 + 35 - 60 * kb, "sans", 30, 700, (255, 230, 80), alpha=a * (1 - kb))
        # headline with exclamation marks
        ke = eio(prog(t, 5.4, 5.9))
        quiet = eio(prog(t, 6.6, 7.2))
        if quiet < 1:
            w, _ = txt(im, "BEST QUALITY", SCX - 60, y0 + 190, "sans", 64, 700, C["white"], alpha=a * (1 - quiet))
            for j in range(3):
                txt(im, "!", SCX - 60 + w / 2 + 20 + j * 26, y0 + 190 + ke * (400 + j * 80), "sans", 64, 700, C["white"],
                    alpha=a * (1 - ke) * (1 - quiet))
            # five buttons
            for j in range(5):
                kk = eio(prog(t, 2.6 + j * 0.08, 3.0 + j * 0.08)) if j > 0 else 0
                bx0 = x0 + 30 + j * ((x1 - x0 - 60) / 5)
                cols = [(220, 60, 60), (60, 140, 230), (250, 190, 40), (60, 180, 90), (180, 80, 200)]
                button(im, (bx0 + 4, y0 + 280 + kk * 500, bx0 + (x1 - x0 - 60) / 5 - 4, y0 + 340 + kk * 500),
                       ["BUY", "SHOP", "DEALS", "NEW", "JOIN"][j], cols[j], C["white"], 22, a * (1 - kk) * (1 - quiet))
            photo(im, (x0 + 30, y0 + 380, x1 - 30, y1 - 30), (80, 80, 84), (40, 40, 44), a * (1 - quiet))
        if quiet > 0:
            photo(im, (x0 + 120, y0 + 330, x1 - 120, y1 - 140), (70, 66, 60), (24, 22, 20), a * quiet, 4)
            txt(im, "Your Name", SCX, y0 + 170, "serif", 76, 500, C["ivory"], alpha=a * quiet, tracking=4)
            txt(im, "Discover", SCX, y1 - 80, "sans", 24, 500, C["champ"], alpha=a * quiet, tracking=6)
            hline(im, SCX - 50, SCX + 50, y1 - 60, C["champ"], 1, a * quiet)
        # pop-up leaving (frame 0) and again as the beat at 4.0
        for (t0, dirn) in ((0.0, 1), (4.0, -1)):
            kp = eio(prog(t, t0 - 0.15, t0 + 0.55)) if t0 == 0.0 else eio(prog(t, t0, t0 + 0.6))
            if t0 == 4.0 and t < 4.0:
                continue
            if kp < 1:
                px = SCX + dirn * kp * 900
                rrect(im, (px - 300, 900, px + 300, 1220), 18, C["white"], (200, 200, 200), 2, a)
                txt(im, "WAIT! Don't go!", px, 990, "sans", 44, 700, (200, 40, 40), alpha=a)
                txt(im, "Take 10% off your first order", px, 1060, "sans", 28, 500, (60, 60, 60), alpha=a)
                button(im, (px - 160, 1110, px + 160, 1180), "CLAIM NOW", (200, 40, 40), C["white"], 26, a)
        plate(im, 220, 520, 0.88 * a)
    if t < 1.2:
        txt(im, "What luxury homepages", SCX, 330, "serif", fit_size("What luxury homepages", "serif", 600, 860, 84), 600, C["ivory"])
        txt(im, "never show.", SCX, 430, "serif_i", 84, 500, C["champ"])
    beats = [(1.2, 2.6, "Discount banners."), (2.6, 4.0, "Five buttons fighting."), (4.0, 5.4, ("Pop-ups in the", "first second.")),
             (5.4, 6.8, "Exclamation marks!"), (6.8, 8.2, "What's left:"), (8.2, 9.6, "They leave space."),
             (9.6, 11.0, ("Space reads", "as confidence."))]
    for t0, t1, s in beats:
        say(im, t, t0, t1, s, 380, 74, C["ivory"] if t0 < 6.8 else C["champ"])
    endcard(im, t, 11.0, ("Say less.", "Mean more."), "DM 'QUIET LUXURY' to start", C["champ"])
    return im


# =====================================================================  24  food delivery & cloud kitchens
def thumb(im, x, y, s=1.0, a=1.0):
    """Stylised thumb: a rounded pad with a nail line, coming in from the lower right."""
    pts = [(x - 70 * s, y - 40 * s), (x + 60 * s, y - 60 * s), (x + 260 * s, y + 380 * s), (x + 60 * s, y + 470 * s)]
    with Vec(im) as d:
        d.polygon(list(sum(pts, ())), pen(C["gold_d"], 3, a), brush((92, 78, 64), a))
        d.ellipse((x - 85 * s, y - 85 * s, x + 85 * s, y + 85 * s), pen(C["gold_d"], 3, a), brush((112, 96, 80), a))
    arc(im, x + 5 * s, y - 20 * s, 48 * s, 200, 340, C["champ"], 3, a * 0.8)


def a24(m):
    m.add(sfx.thock(), 0, 1.0)
    m.add(sfx.bass_hit(0.6, 140, 55), 0, 0.5)
    m.add(sfx.low_thud(0.4), 0.45, 0.45)
    m.add(sfx.swish(), 1.0, 0.25)
    m.bed(sfx.pulse_bed(12, 104, 55), 0.11, start=1.8, end=10.0)
    tick_beats(m, [1.8, 3.2, 5.0])
    m.add(sfx.whoosh(0.5), 6.2, 0.2)
    m.add(sfx.thock(), 7.4, 0.7)
    m.add(sfx.chime_stab(), 7.45, 0.3)
    tick_beats(m, [8.4])
    end_sting(m, 10.0)


M24 = dict(
    type="Mobile thumb test", industry="Food delivery & cloud kitchens", palette="Gold on obsidian with warm food tones",
    hook="That tap just cost you an order.",
    beats=[
        ("0.0–1.0", "Frame 0: a thumb is mid-tap on a tiny '+' button on a delivery menu; it lands a few pixels off and opens the wrong item."),
        ("1.0–1.8", "The wrong item sheet slides up: the order did not happen."),
        ("1.8–3.2", "'The button is smaller than a thumb.'"),
        ("3.2–5.0", "The button is outlined and measured: 'Apple's guideline: tap targets of at least 44 pt.'"),
        ("5.0–6.2", "'Hungry people don't try twice.'"),
        ("6.2–8.4", "Rebuilt menu: full-width 'Add to order' buttons; the thumb taps once, a check and 'Added' appear inside the app."),
        ("8.4–10.0", "'Design for thumbs, not cursors.'"),
        ("10.0–12.0", "End card: 'Make every tap an order.' + DM 'ORDER'."),
    ],
    sound="0.00 a dull thock of a fingertip on glass over a sub; a low thud on the miss; a swish as the wrong sheet slides up; a 104 bpm pulse; a clean thock + chime on the successful tap.",
    cta="Make every tap an order. DM 'ORDER' to start.",
    why="Everyone has mis-tapped a tiny button, so the frame is instantly felt, and 'cost you an order' turns a design detail into lost revenue. The 44 pt minimum is Apple's published guideline, not an invented figure.",
)


def menu_screen(im, sb, big=False, wrong=0.0, added=0.0):
    x0, y0, x1, y1 = sb
    txt(im, "Tonight's menu", x0 + 40, y0 + 80, "serif", 44, 600, C["ivory"], "lm")
    rows = [("Grilled chicken bowl", (190, 120, 60)), ("Koshari, large", (170, 110, 50)), ("Extra sauce", (150, 60, 40))]
    for i, (name, col) in enumerate(rows):
        ry = y0 + 150 + i * (230 if big else 170)
        rrect(im, (x0 + 24, ry, x1 - 24, ry + (210 if big else 150)), 20, C["obs3"], C["line"], 2)
        circle(im, x0 + 90, ry + 70, 48, fill=col)
        txt(im, name, x0 + 160, ry + 50, "sans", 28, 600, C["ivory"], "lm")
        bars(im, x0 + 160, ry + 82, 200, 1, 0, 10, C["muted"], 0.5)
        if big:
            button(im, (x0 + 50, ry + 120, x1 - 50, ry + 192), "Add to order" if not (i == 0 and added > 0.5) else "Added",
                   C["gold"], C["obs"], 28)
        else:
            rrect(im, (x1 - 74, ry + 56, x1 - 44, ry + 86), 15, C["gold"])
            txt(im, "+", x1 - 59, ry + 70, "sans", 26, 700, C["obs"])
    if wrong > 0:
        hy = y1 - 420 * eo(wrong)
        rrect(im, (x0 + 4, hy, x1 - 4, y1 + 40), 40, C["obs2"], C["line"], 2)
        txt(im, "Extra sauce", x0 + 40, hy + 70, "serif", 42, 600, C["ivory"], "lm")
        txt(im, "Not what they wanted.", x0 + 40, hy + 130, "sans", 26, 500, C["muted"], "lm")
    if added > 0:
        check(im, x1 - 90, y0 + 80, 44, C["gold"], added, 6)


@reel(24, "tap-cost-an-order", 12.0, a24, M24, qc=[0.0, 0.5, 1.4, 4.0, 7.8, 11.0])
def r24(t):
    im = bg(C["obs"], (32, 24, 14))
    if t < 10.0:
        a = win(t, -1, 10.0, 0, 0.2)
        big = t >= 6.2
        sb = phone(im, SCX, 1000, 520, 920)
        menu_screen(im, sb, big, prog(t, 1.0, 1.4) if (1.0 <= t < 6.2) else 0, prog(t, 7.45, 7.8) if big else 0)
        x0, y0, x1, y1 = sb
        if not big:
            bx, by = x1 - 59, y0 + 150 + 70 + 170  # second row's tiny button
            if t < 1.0:
                dn = eo(prog(t, 0, 0.4))
                thumb(im, bx - 40 + 30 * (1 - dn), by + 20 + 60 * (1 - dn), 1.0, a)
                if t > 0.35:
                    r = 20 + 60 * prog(t, 0.35, 0.9)
                    circle(im, bx - 40, by + 20, r, outline=C["ivory"], width=3, alpha=1 - prog(t, 0.35, 0.9))
            if 3.2 <= t < 5.0:
                ka = win(t, 3.2, 5.0, 0.2, 0.2)
                rrect(im, (bx - 22, by - 22, bx + 22, by + 22), 6, None, C["gold_l"], 3, ka)
                rrect(im, (bx - 100, by - 100, bx + 60, by + 60), 20, None, C["ivory"], 2, ka * 0.7)
                txt(im, "thumb", bx - 20, by + 90, "sans", 24, 600, C["ivory"], alpha=ka)
        else:
            by = y0 + 150 + 120 + 36
            tx, ty = SCX, by
            dn = eo(prog(t, 7.0, 7.4))
            if t < 9.0:
                thumb(im, tx + 60 * (1 - dn), ty + 120 * (1 - dn), 1.0, a * win(t, 6.6, 9.0, 0.3, 0.3))
    if t < 1.8:
        txt(im, "That tap just cost", SCX, 330, "serif", 84, 600, C["ivory"])
        txt(im, "you an order.", SCX, 430, "serif_i", 84, 500, C["gold_l"])
    say(im, t, 1.8, 3.2, ("The button is smaller", "than a thumb."), 380, 72)
    say(im, t, 3.2, 5.0, ("Apple's guideline: tap targets", "of at least 44 pt."), 380, 54, C["champ"], "sans", 500)
    say(im, t, 5.0, 6.2, ("Hungry people", "don't try twice."), 380, 80, C["gold_l"])
    say(im, t, 6.2, 8.4, "One thumb. One tap. Done.", 380, 66)
    say(im, t, 8.4, 10.0, ("Design for thumbs,", "not cursors."), 380, 78, C["gold_l"])
    endcard(im, t, 10.0, ("Make every tap", "an order."), "DM 'ORDER' to start")
    return im


# =====================================================================  25  retail chains
PINS = [(300, 820), (720, 700), (650, 1180)]
USER = (470, 1000)


def a25(m):
    m.add(sfx.chime_stab(), 0, 1.0)
    m.add(sfx.bass_hit(0.6, 150, 55), 0, 0.5)
    m.bed(sfx.pad(13, "dm", 900), 0.09)
    for k in range(6):
        m.add(sfx.ping(0.6, 1760), 0.9 + k * 1.4, 0.08)
    tick_beats(m, [1.8, 3.2, 4.8, 6.4, 8.0, 9.6])
    m.add(sfx.metal_click(), 5.0, 0.3)
    end_sting(m, 11.0)


M25 = dict(
    type="Prediction", industry="Retail chains", palette="Obsidian with a deep-emerald accent",
    hook="By next year, customers will expect this.",
    beats=[
        ("0.0–1.8", "Frame 0: labelled OUR PREDICTION, the hook over an abstract city map; three branch pins glow and a radius ring is already expanding from the shopper's location."),
        ("1.8–3.2", "'Not call the branch.'"),
        ("3.2–4.8", "'Live stock. Nearest branch. Reserve.'"),
        ("4.8–6.4", "A product card slides up over the map: 'In stock at [branch]', with Reserve and Directions."),
        ("6.4–8.0", "'Reserve now. Pick up today.'"),
        ("8.0–9.6", "'An opinion, not a fact. Watch this space.'"),
        ("9.6–11.0", "'The chains that build it first set the standard.'"),
        ("11.0–13.0", "End card: 'Be the chain that's ready.' + DM 'BRANCHES'."),
    ],
    sound="0.00 a bright chime chord on a sub (a 'reveal' sound); D-minor pad; a faint radar ping each time the ring expands; clicks on each line; a metallic click as the card lands.",
    cta="Be the chain that's ready. DM 'BRANCHES' to start.",
    why="Predictions trigger a 'will it?' reaction and invite disagreement in the comments; owners of chains fear being the one that looks behind. It is labelled as opinion on screen twice.",
    placeholders=["[branch] on the product-card mockup"],
)


@reel(25, "customers-will-expect", 13.0, a25, M25, qc=[0.5, 2.5, 5.5, 8.5, 12.0])
def r25(t):
    im = bg(C["obs"], (10, 28, 23))
    if t < 11.0:
        a = win(t, -1, 11.0, 0, 0.2)
        for i in range(9):
            line(im, [(SX0, 560 + i * 110 + 20 * SIN(i)), (SX1, 600 + i * 100)], C["emer"], 2, a * 0.8)
            line(im, [(SX0 + i * 105, 540), (SX0 + 40 + i * 100, 1460)], C["emer"], 2, a * 0.8)
        ph = (t % 1.4) / 1.4
        circle(im, *USER, 40 + 330 * ph, outline=C["emer_l"], width=3, alpha=a * (1 - ph))
        circle(im, *USER, 16, fill=C["ivory"], alpha=a)
        for i, (px, py) in enumerate(PINS):
            glow = 0.6 + 0.4 * SIN(t * 4 + i) ** 2
            circle(im, px, py, 34, fill=C["emer_l"], alpha=a * 0.25 * glow)
            circle(im, px, py, 16, fill=C["gold"], alpha=a)
        if t >= 4.8:
            k = eo(prog(t, 4.8, 5.2))
            cy0 = 1500 - 520 * k
            rrect(im, (SX0, cy0, SX1, cy0 + 480), 30, C["obs2"], C["emer_l"], 2, a)
            photo(im, (SX0 + 30, cy0 + 30, SX0 + 230, cy0 + 230), (90, 80, 70), (40, 36, 30), a)
            txt(im, "Linen shirt", SX0 + 260, cy0 + 70, "serif", 52, 600, C["ivory"], "lm", a)
            txt(im, "In stock at [branch]", SX0 + 260, cy0 + 135, "sans", 30, 600, C["emer_l"], "lm", a)
            txt(im, "Pick up today", SX0 + 260, cy0 + 185, "sans", 28, 500, C["muted"], "lm", a)
            button(im, (SX0 + 30, cy0 + 290, SCX - 10, cy0 + 370), "Reserve", C["emer"], C["ivory"], 30, a)
            button(im, (SCX + 10, cy0 + 290, SX1 - 30, cy0 + 370), "Directions", C["obs3"], C["ivory"], 30, a, C["line"])
        plate(im, 220, 520, 0.85 * a)
    if t < 1.8:
        eyebrow(im, "Our prediction", SCX, 270, C["emer_l"])
        txt(im, "By next year, customers", SCX, 360, "serif", fit_size("By next year, customers", "serif", 600, 860, 78), 600, C["ivory"])
        txt(im, "will expect this.", SCX, 455, "serif_i", 80, 500, C["emer_l"])
    say(im, t, 1.8, 3.2, "Not 'call the branch'.", 380, 76)
    say(im, t, 3.2, 4.8, ("Live stock. Nearest branch.", "Reserve."), 380, 66)
    say(im, t, 4.8, 6.4, "Right on the product page.", 380, 64, C["champ"])
    say(im, t, 6.4, 8.0, ("Reserve now.", "Pick up today."), 380, 76)
    say(im, t, 8.0, 9.6, ("An opinion, not a fact.", "Watch this space."), 380, 64, C["muted"])
    say(im, t, 9.6, 11.0, ("The chains that build it", "first set the standard."), 380, 64, C["emer_l"])
    endcard(im, t, 11.0, ("Be the chain", "that's ready."), "DM 'BRANCHES' to start", C["emer_l"])
    return im


# =====================================================================  26  Egyptian SMEs (Arabic)
AR = [
    (0.0, 1.8, ("محلك حلو،", "بس مش باين"), "Your shop is great, but nobody can see it."),
    (1.8, 3.6, ("الناس بتدوّر", "على الموبايل الأول"), "People search on their phone first."),
    (3.6, 5.4, ("وإنت عارف", "قيمتك كويس"), "You know exactly what you're worth."),
    (5.4, 7.2, ("بس الزبون", "لسه ما يعرفهاش"), "But the customer doesn't know it yet."),
    (7.2, 9.4, ("خلّيها تبان", "من أول نظرة"), "Make it show at first glance."),
    (9.4, 12.0, ("موقع معمول", "على مقاسك"), "A website made to measure."),
]


def shopfront(im, cx, cy, s, lit, a=1.0):
    def P(x, y):
        return cx + x * s, cy + y * s

    col = mix(C["gold_d"], C["gold_l"], lit)
    rrect(im, (*P(-380, -300), *P(380, 300)), 10, mix(C["obs"], (60, 46, 20), lit * 0.6), col, 3, a)
    with Vec(im) as d:  # awning
        d.polygon(list(sum([P(-420, -300), P(420, -300), P(380, -380), P(-380, -380)], ())), pen(col, 3, a),
                  brush(col, a * (0.2 + 0.6 * lit)))
    for i in range(7):
        line(im, [P(-380 + i * 126, -380), P(-420 + i * 140, -300)], C["obs"], 2, a * lit)
    rrect(im, (*P(-330, -230), *P(-30, 120)), 6, mix(C["obs2"], C["gold_l"], lit * 0.35), col, 3, a)
    rrect(im, (*P(30, -230), *P(330, 300)), 6, mix(C["obs2"], (90, 70, 30), lit * 0.5), col, 3, a)
    circle(im, *P(290, 40), 10 * s, fill=col, alpha=a)


def a26(m):
    m.add(sfx.doum(), 0, 1.0)
    m.add(sfx.bass_hit(0.8, 120, 45), 0, 0.45)
    # maqsum: D T _ T D _ T _  at ~104 bpm (eighths)
    step = 60 / 104 / 2
    pattern = "DT.TD.T."
    k = 0
    tt = step * 8
    while tt < 12.0:
        c = pattern[k % 8]
        if c == "D":
            m.add(sfx.doum(0.5), tt, 0.22)
        elif c == "T":
            m.add(sfx.tek(), tt, 0.12)
        tt += step
        k += 1
    m.bed(sfx.pad(14, "dm", 800), 0.08)
    m.add(sfx.boom_shimmer(), 7.2, 0.45)
    end_sting(m, 12.0)


M26 = dict(
    type="Arabic hook (Egyptian dialect)", industry="Egyptian SMEs", palette="Gold-dominant",
    hook="محلك حلو، بس مش باين  (EN subtitle: Your shop is great, but nobody can see it.)",
    beats=[
        ("0.0–1.8", "Frame 0: the Egyptian Arabic hook in large Cairo type, correctly joined and right-to-left, with the English subtitle under it; a spotlight is already sweeping across a dark gold-line shopfront."),
        ("1.8–3.6", "الناس بتدوّر على الموبايل الأول / People search on their phone first."),
        ("3.6–5.4", "وإنت عارف قيمتك كويس / You know exactly what you're worth."),
        ("5.4–7.2", "بس الزبون لسه ما يعرفهاش / But the customer doesn't know it yet."),
        ("7.2–9.4", "The shopfront lights up gold and a website frame forms around it: خلّيها تبان من أول نظرة / Make it show at first glance."),
        ("9.4–12.0", "موقع معمول على مقاسك / A website made to measure."),
        ("12.0–14.0", "End card in Arabic: ابعتلنا كلمة «ابدأ» / DM us the word START, in Arabic or English."),
    ],
    sound="0.00 a deep darbuka doum over a sub; a quiet maqsum rhythm (doum-tek) underneath at about 104 bpm; D-minor pad; a boom with shimmer when the shop lights up.",
    cta="ابعتلنا كلمة «ابدأ» : DM us 'START' (ابدأ) to begin.",
    why="Egyptian dialect in the first frame tells local owners this is for them, not a translated foreign ad. 'Your shop is great' flatters before it stings, and 'nobody can see it' is the open loop.",
)


def ar_line(im, lines, en, y, size, color, alpha=1.0):
    for i, l in enumerate(lines):
        sz = fit_size(l, "arabic", 700, 860, size)
        txt(im, l, SCX, y + i * size * 1.25, "arabic", sz, 700, color, alpha=alpha)
    txt(im, en, SCX, y + len(lines) * size * 1.25 + 14, "sans", fit_size(en, "sans", 500, 860, 46), 500, C["ivory"], alpha=alpha * 0.9)


@reel(26, "arabic-mesh-bayen", 14.0, a26, M26, qc=[0.0, 1.0, 3.0, 8.0, 10.5, 13.0])
def r26(t):
    im = bg(C["obs"], (34, 27, 12), cy=1100)
    if t < 12.0:
        a = win(t, -1, 12.0, 0, 0.25)
        lit = eio(prog(t, 7.2, 7.8))
        frame = eio(prog(t, 7.6, 8.4))
        s = 0.85 - 0.25 * frame
        cy = 1150 - 60 * frame
        if frame > 0:
            x0, y0, x1, y1 = browser(im, (SX0, 760, SX1, 1480), "dark", a * frame)
            txt(im, "اسم محلك", x0 + 40, y0 + 40, "arabic", 34, 700, C["gold_l"], "lm", a * frame)
            button(im, (x0 + 40, y1 - 90, x0 + 300, y1 - 30), "", C["gold"], C["obs"], 26, a * frame)
            txt(im, "اطلب دلوقتي", x0 + 170, y1 - 62, "arabic", 30, 700, C["obs"], alpha=a * frame)
        shopfront(im, SCX, cy, s, lit, a)
        if lit < 1:
            sx = SCX + 380 * SIN(t * 1.6 + 0.6)
            with Vec(im) as d:
                d.polygon([SCX - 40, 520, SCX + 40, 520, sx + 220, 1480, sx - 220, 1480], None, brush(C["gold_l"], 0.10 * a * (1 - lit)))
            circle(im, sx, 1300, 200, fill=C["gold_l"], alpha=0.06 * a * (1 - lit))
    for t0, t1, lines, en in AR:
        if t0 <= t < t1:
            al = win(t, t0, t1, 0 if t0 == 0 else 0.14, 0.12)
            k = 1.0 if t0 == 0 else eo(prog(t, t0, t0 + 0.3))
            ar_line(im, lines, en, 330 + (1 - k) * 20, 100 if t0 == 0 else 90, C["gold_l"] if t0 in (0.0, 7.2) else C["ivory"], al)
    if t >= 12.0:
        k = eo(prog(t, 12.0, 12.35))
        ar_line(im, ("ابعتلنا كلمة ابدأ",), "DM us START (in Arabic or English)", 760, 96, C["gold_l"], k)
        endcard(im, t, 12.0, "", None, C["gold"], y_cta=880)
    return im
