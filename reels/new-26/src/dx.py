"""Core drawing kit for the DeveraXTech reels: canvas, palette, type, easing, shapes, mockups, end card."""
import math
import os
from functools import lru_cache

import aggdraw
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
W, H, FPS = 1080, 1920, 30
# Text safe box: top 220, bottom 380, right 140 are covered by the TikTok / Reels UI.
SX0, SY0, SX1, SY1 = 80, 220, 940, 1540
SCX = (SX0 + SX1) // 2  # horizontal centre of the safe box (510)
SCY = (SY0 + SY1) // 2

C = {
    "obs": (10, 10, 10),
    "obs2": (19, 17, 14),
    "obs3": (30, 27, 22),
    "gold": (212, 175, 55),
    "gold_l": (245, 213, 115),
    "gold_d": (150, 118, 34),
    "champ": (232, 217, 181),
    "ivory": (244, 239, 230),
    "paper": (238, 230, 214),
    "emer": (17, 94, 75),
    "emer_l": (52, 150, 118),
    "muted": (150, 141, 124),
    "line": (58, 52, 42),
    "white": (250, 248, 244),
    "ink": (22, 20, 17),
}


def mix(a, b, k):
    return tuple(int(round(a[i] + (b[i] - a[i]) * k)) for i in range(3))


# ---------------------------------------------------------------- timing
def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def prog(t, a, b):
    return clamp((t - a) / (b - a)) if b > a else float(t >= a)


def eo(x):  # ease out cubic
    x = clamp(x)
    return 1 - (1 - x) ** 3


def eio(x):
    x = clamp(x)
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def eexp(x):
    x = clamp(x)
    return 1 if x >= 1 else 1 - 2 ** (-10 * x)


def eback(x, s=1.4):
    x = clamp(x) - 1
    return 1 + (s + 1) * x ** 3 + s * x ** 2


def win(t, a, b, fi=0.18, fo=0.18):
    """Opacity window: in over fi seconds from a, out over fo seconds before b."""
    if t < a or t > b:
        return 0.0
    i = 1.0 if fi <= 0 else eo((t - a) / fi)
    o = 1.0 if fo <= 0 else eo((b - t) / fo)
    return min(i, o)


# ---------------------------------------------------------------- fonts
FONT_FILES = {
    "serif": ("playfair-display-latin-wght-normal.ttf", True),
    "serif_i": ("playfair-display-latin-wght-italic.ttf", True),
    "garamond": ("cormorant-garamond-latin-wght-normal.ttf", True),
    "garamond_i": ("cormorant-garamond-latin-wght-italic.ttf", True),
    "hand": ("caveat-latin-wght-normal.ttf", True),
    "arabic": ("cairo-arabic-wght-normal.ttf", True),
    "cairo": ("cairo-latin-wght-normal.ttf", True),
}
INTER = {300: "Inter-Light.otf", 400: "Inter-Regular.otf", 500: "Inter-Medium.otf",
         600: "Inter-SemiBold.otf", 700: "Inter-Bold.otf"}


@lru_cache(maxsize=512)
def font(family, size, weight=400):
    size = int(round(size))
    if family == "sans":
        w = min(INTER, key=lambda k: abs(k - weight))
        return ImageFont.truetype(os.path.join(FONTS, INTER[w]), size)
    fn, var = FONT_FILES[family]
    f = ImageFont.truetype(os.path.join(FONTS, fn), size, layout_engine=ImageFont.Layout.RAQM)
    if var:
        axes = f.get_variation_axes()
        lo, hi = axes[0]["minimum"], axes[0]["maximum"]
        f.set_variation_by_axes([clamp(weight, lo, hi)])
    return f


# Arabic: shaped and laid out right-to-left by HarfBuzz + FriBiDi through libraqm (direction="rtl").
# arabic-reshaper + python-bidi was tested first, but it maps letters to Unicode presentation forms,
# which the web-subset Cairo font does not contain (every letter rendered as a box).


# ---------------------------------------------------------------- text sprites
@lru_cache(maxsize=4096)
def sprite(text, family="serif", size=96, weight=600, color=C["ivory"], tracking=0, opacity=255):
    """Tight RGBA image of a single line of text. tracking in px between glyphs."""
    f = font(family, size, weight)
    kw = {"direction": "rtl", "language": "ar"} if family == "arabic" else {}
    asc, desc = f.getmetrics()
    pad = int(size * 0.25)
    if tracking:
        widths = [f.getlength(ch) for ch in text]
        tw = int(sum(widths) + tracking * (len(text) - 1)) + 2 * pad
    else:
        tw = int(f.getlength(text, **kw)) + 2 * pad
    th = asc + desc + 2 * pad
    im = Image.new("RGBA", (max(tw, 1), th), color + (0,))
    d = ImageDraw.Draw(im)
    if tracking:
        x = pad
        for ch, w in zip(text, widths):
            d.text((x, pad), ch, font=f, fill=color + (opacity,))
            x += w + tracking
    else:
        d.text((pad, pad), text, font=f, fill=color + (opacity,), **kw)
    bb = im.getbbox()
    if not bb:
        return im
    # keep full line height (consistent baselines), trim horizontal slack only
    return im.crop((bb[0], pad + int(asc * 0.0), bb[2], pad + asc + desc))


def text_w(text, family="serif", size=96, weight=600, tracking=0):
    return sprite(text, family, size, weight, (255, 255, 255), tracking).width


def fit_size(text, family, weight, max_w, start, tracking=0, min_size=24):
    s = start
    while s > min_size and text_w(text, family, s, weight, tracking) > max_w:
        s -= 2
    return s


@lru_cache(maxsize=1024)
def block(lines, family="serif", size=96, weight=600, color=C["ivory"], lead=1.12,
          align="center", tracking=0):
    """Multi-line text sprite. lines is a tuple of strings."""
    sps = [sprite(l, family, size, weight, color, tracking) for l in lines]
    lh = int(size * lead)
    w = max(s.width for s in sps)
    h = lh * (len(sps) - 1) + sps[-1].height
    im = Image.new("RGBA", (w, h), color + (0,))
    for i, s in enumerate(sps):
        x = (w - s.width) // 2 if align == "center" else (w - s.width if align == "right" else 0)
        im.alpha_composite(s, (x, i * lh))
    return im


def wrap(text, family, size, weight, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(trial, family, size, weight) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return tuple(lines)


_alpha_lut = {}


def with_alpha(sp, a):
    if a >= 0.999:
        return sp
    a = max(0.0, a)
    key = int(a * 100)
    lut = _alpha_lut.get(key)
    if lut is None:
        lut = [int(v * key / 100) for v in range(256)]
        _alpha_lut[key] = lut
    out = sp.copy()
    out.putalpha(sp.getchannel("A").point(lut))
    return out


def put(im, sp, x, y, anchor="mm", alpha=1.0, scale=1.0, rot=0.0):
    """Paste sprite sp on RGB image im. anchor: l/m/r + t/m/b."""
    if alpha <= 0.004:
        return
    if scale != 1.0:
        nw, nh = max(1, int(sp.width * scale)), max(1, int(sp.height * scale))
        sp = sp.resize((nw, nh), Image.BICUBIC)
    if rot:
        sp = sp.rotate(rot, resample=Image.BICUBIC, expand=True)
    sp = with_alpha(sp, alpha)
    ax, ay = anchor[0], anchor[1]
    px = x - (0 if ax == "l" else sp.width // 2 if ax == "m" else sp.width)
    py = y - (0 if ay == "t" else sp.height // 2 if ay == "m" else sp.height)
    im.paste(sp, (int(round(px)), int(round(py))), sp)


def txt(im, s, x, y, family="serif", size=96, weight=600, color=C["ivory"], anchor="mm",
        alpha=1.0, scale=1.0, tracking=0):
    sp = sprite(s, family, int(size), weight, color, tracking)
    put(im, sp, x, y, anchor, alpha, scale)
    return sp.width, sp.height


def para(im, lines, x, y, family="serif", size=96, weight=600, color=C["ivory"], anchor="mm",
         alpha=1.0, lead=1.12, align="center", scale=1.0, tracking=0):
    sp = block(tuple(lines), family, int(size), weight, color, lead, align, tracking)
    put(im, sp, x, y, anchor, alpha, scale)
    return sp.width, sp.height


@lru_cache(maxsize=256)
def glow(sp_key, radius=18, strength=1.0):
    sp = sprite(*sp_key)
    pad = radius * 3
    big = Image.new("RGBA", (sp.width + pad * 2, sp.height + pad * 2), sp_key[4] + (0,))
    big.alpha_composite(sp, (pad, pad))
    g = big.filter(ImageFilter.GaussianBlur(radius))
    if strength != 1.0:
        g.putalpha(g.getchannel("A").point(lambda v: min(255, int(v * strength))))
    return g


def glow_txt(im, s, x, y, family="serif", size=96, weight=600, color=C["gold"], alpha=1.0,
             radius=22, strength=0.9):
    g = glow((s, family, int(size), weight, color, 0, 255), radius, strength)
    put(im, g, x, y, "mm", alpha * 0.8)
    txt(im, s, x, y, family, size, weight, color, "mm", alpha)


# ---------------------------------------------------------------- backgrounds and finish
@lru_cache(maxsize=32)
def _bg(c0, c1, cx, cy, r):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xx - cx) / r) ** 2 + ((yy - cy) / (r * 1.25)) ** 2)
    k = np.clip(d, 0, 1)[..., None]
    k = k * k * (3 - 2 * k)
    a = np.array(c1, np.float32) * (1 - k) + np.array(c0, np.float32) * k
    return Image.fromarray(a.astype(np.uint8), "RGB")


def bg(c0=C["obs"], c1=C["obs2"], cx=W // 2, cy=H * 0.42, r=1100):
    """Radial background: c1 at the centre, c0 at the edges."""
    return _bg(tuple(c0), tuple(c1), int(cx), int(cy), int(r)).copy()


_GRAIN = None


def finish(im, fi, grain=6):
    """Film grain, then return RGB bytes."""
    global _GRAIN
    a = np.asarray(im, dtype=np.int16)
    if grain:
        if _GRAIN is None:
            rng = np.random.default_rng(7)
            _GRAIN = [rng.integers(-1, 2, (H // 2, W // 2), dtype=np.int16) for _ in range(6)]
        g = _GRAIN[fi % 6]
        g = np.repeat(np.repeat(g, 2, 0), 2, 1)[..., None] * (grain // 2)
        a = a + g
    return np.clip(a, 0, 255).astype(np.uint8).tobytes()


# ---------------------------------------------------------------- vector helpers (antialiased)
def pen(color, width=2, alpha=1.0):
    return aggdraw.Pen(tuple(color), width, int(255 * clamp(alpha)))


def brush(color, alpha=1.0):
    return aggdraw.Brush(tuple(color), int(255 * clamp(alpha)))


class Vec:
    """Context manager around aggdraw so shapes are antialiased."""

    def __init__(self, im):
        self.d = aggdraw.Draw(im)

    def __enter__(self):
        return self.d

    def __exit__(self, *a):
        self.d.flush()


def rrect_path(x0, y0, x1, y1, r):
    p = aggdraw.Path()
    r = min(r, (x1 - x0) / 2, (y1 - y0) / 2)
    p.moveto(x0 + r, y0)
    p.lineto(x1 - r, y0)
    p.curveto(x1 - r * 0.45, y0, x1, y0 + r * 0.45, x1, y0 + r)
    p.lineto(x1, y1 - r)
    p.curveto(x1, y1 - r * 0.45, x1 - r * 0.45, y1, x1 - r, y1)
    p.lineto(x0 + r, y1)
    p.curveto(x0 + r * 0.45, y1, x0, y1 - r * 0.45, x0, y1 - r)
    p.lineto(x0, y0 + r)
    p.curveto(x0, y0 + r * 0.45, x0 + r * 0.45, y0, x0 + r, y0)
    p.close()
    return p


def rrect(im, box, r, fill=None, outline=None, width=2, alpha=1.0, oalpha=None):
    with Vec(im) as d:
        d.path(rrect_path(*box, r), pen(outline, width, alpha if oalpha is None else oalpha) if outline else None,
               brush(fill, alpha) if fill else None)


def rect(im, box, fill, alpha=1.0):
    if alpha >= 0.999:
        ImageDraw.Draw(im).rectangle([int(v) for v in box], fill=tuple(fill))
    else:
        with Vec(im) as d:
            d.rectangle(box, None, brush(fill, alpha))


def line(im, pts, color, width=2, alpha=1.0):
    with Vec(im) as d:
        d.line(list(np.ravel(pts)), pen(color, width, alpha))


def poly_partial(pts, k):
    """First fraction k (0..1) of a polyline by length. Returns points and the head point."""
    pts = [tuple(p) for p in pts]
    if k <= 0 or len(pts) < 2:
        return [pts[0]], pts[0]
    seg = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    total = sum(seg)
    target = total * clamp(k)
    out, acc = [pts[0]], 0.0
    for i, s in enumerate(seg):
        if acc + s >= target:
            f = (target - acc) / s if s else 0
            hp = (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f)
            out.append(hp)
            return out, hp
        out.append(pts[i + 1])
        acc += s
    return out, pts[-1]


def circle(im, cx, cy, r, fill=None, outline=None, width=2, alpha=1.0):
    with Vec(im) as d:
        d.ellipse((cx - r, cy - r, cx + r, cy + r), pen(outline, width, alpha) if outline else None,
                  brush(fill, alpha) if fill else None)


def arc(im, cx, cy, r, a0, a1, color, width=4, alpha=1.0):
    """Arc from angle a0 to a1 in degrees (0 = 3 o'clock, clockwise)."""
    n = max(2, int(abs(a1 - a0) / 2))
    pts = [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
            cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
    line(im, pts, color, width, alpha)


def hline(im, x0, x1, y, color=C["gold"], width=2, alpha=1.0):
    line(im, [(x0, y), (x1, y)], color, width, alpha)


# ---------------------------------------------------------------- logo and end card
@lru_cache(maxsize=16)
def logo(h):
    im = Image.open(os.path.join(HERE, "deveraxtech-logo.png")).convert("RGBA")
    im = im.crop(im.getbbox())
    w = int(im.width * h / im.height)
    return im.resize((w, h), Image.LANCZOS)


def endcard(im, t, t0, cta, sub=None, accent=C["gold"], ink=C["ivory"], dur=2.0, cta_family="serif",
            cta_size=84, y_cta=820):
    """Final ~2 s: CTA (tied to the hook payoff), monogram, wordmark and handle.

    Returns early before t0. Everything is crisp from the first frame of the card (no slow logo intro).
    """
    if t < t0:
        return
    k = eo(prog(t, t0, t0 + 0.35))
    lines = cta if isinstance(cta, tuple) else (cta,)
    if lines == ("",):
        lines = ()
    size = cta_size
    while lines and size > 40 and max(text_w(l, cta_family, size, 600) for l in lines) > SX1 - SX0 - 20:
        size -= 2
    if lines:
        para(im, lines, SCX, y_cta + (1 - k) * 30, cta_family, size, 600, ink, alpha=k, lead=1.15)
    by = y_cta + int(size * 1.15 * len(lines) / 2) + 40
    if sub:
        txt(im, sub, SCX, by + 30, "sans", 34, 400, C["muted"] if ink != C["ink"] else (90, 84, 74), alpha=k)
        by += 70
    k2 = eo(prog(t, t0 + 0.12, t0 + 0.5))
    hline(im, SCX - 160 * k2, SCX + 160 * k2, by + 40, accent, 2, k2)
    lg = logo(150)
    put(im, lg, SCX, by + 150, alpha=k2, scale=0.92 + 0.08 * k2)
    txt(im, "DeveraXTech", SCX, by + 285, "serif", 64, 600, accent, alpha=k2, tracking=2)
    txt(im, "@deveraxtech", SCX, by + 345, "sans", 36, 500, ink, alpha=k2 * 0.9)


def eyebrow(im, s, x, y, color=C["gold"], alpha=1.0, anchor="mm", size=30):
    """Small tracked uppercase label."""
    return txt(im, s.upper(), x, y, "sans", size, 600, color, anchor, alpha, tracking=6)


# ---------------------------------------------------------------- website mockups (abstract, invented)
def browser(im, box, theme="dark", alpha=1.0, radius=22, chrome=True):
    """Generic browser window frame (no real browser UI). Returns inner content box."""
    x0, y0, x1, y1 = box
    base = C["obs2"] if theme == "dark" else C["ivory"]
    edge = C["line"] if theme == "dark" else (210, 200, 182)
    rrect(im, box, radius, base, edge, 2, alpha)
    if not chrome:
        return (x0, y0, x1, y1)
    for i in range(3):
        circle(im, x0 + 30 + i * 22, y0 + 28, 6, fill=edge, alpha=alpha)
    rrect(im, (x0 + 110, y0 + 14, x1 - 40, y0 + 42), 14, C["obs3"] if theme == "dark" else (228, 220, 204), alpha=alpha)
    return (x0, y0 + 56, x1, y1)


def bars(im, x, y, w, n=3, gap=22, h=10, color=C["muted"], alpha=0.5, last=0.6):
    """Placeholder text lines."""
    for i in range(n):
        ww = w * (last if i == n - 1 else 1.0)
        rrect(im, (x, y + i * gap, x + ww, y + i * gap + h), h / 2, color, alpha=alpha)


def photo(im, box, c0, c1, alpha=1.0, radius=14, horizon=None):
    """Abstract 'photo' block: vertical gradient with an optional skyline/horizon."""
    x0, y0, x1, y1 = [int(v) for v in box]
    w, h = x1 - x0, y1 - y0
    if w <= 2 or h <= 2:
        return
    g = np.linspace(0, 1, h, dtype=np.float32)[:, None, None]
    a = np.array(c0, np.float32) * (1 - g) + np.array(c1, np.float32) * g
    a = np.repeat(a, w, 1)
    tile = Image.fromarray(a.astype(np.uint8), "RGB")
    m = Image.new("L", (w, h), 0)
    with Vec(m) as d:
        d.path(rrect_path(0, 0, w, h, radius), None, aggdraw.Brush(255, int(255 * alpha)))
    im.paste(tile, (x0, y0), m)
    if horizon:
        hx = horizon
        line(im, [(x0 + w * px, y0 + h * py) for px, py in hx], C["gold_l"], 2, alpha * 0.8)


# ---------------------------------------------------------------- beats and devices
def say(im, t, t0, t1, lines, y=None, size=84, color=None, family="serif", weight=600, x=None,
        anchor="mm", align="center", lead=1.12, fi=0.14, fo=0.12, rise=26, max_w=None, tracking=0):
    """A text beat: snaps in (short rise), holds, snaps out. fi=0 means fully visible at t0."""
    a = win(t, t0, t1, fi, fo)
    if a <= 0:
        return
    color = C["ivory"] if color is None else color
    x = SCX if x is None else x
    y = SCY if y is None else y
    if isinstance(lines, str):
        lines = wrap(lines, family, size, weight, max_w or (SX1 - SX0))
    k = 1.0 if fi <= 0 else eo(prog(t, t0, t0 + 0.32))
    para(im, lines, x, y + (1 - k) * rise, family, size, weight, color, anchor, a, lead, align, tracking=tracking)


def phone(im, cx, cy, w=500, h=1000, screen=None, alpha=1.0, edge=None):
    """Generic handset outline (no OS UI). Returns the screen box."""
    screen = C["obs2"] if screen is None else screen
    edge = C["line"] if edge is None else edge
    box = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    rrect(im, box, 70, C["obs3"], edge, 3, alpha)
    sb = (box[0] + 16, box[1] + 16, box[2] - 16, box[3] - 16)
    rrect(im, sb, 56, screen, alpha=alpha)
    return sb


def button(im, box, label, fill=C["gold"], ink=C["obs"], size=30, alpha=1.0, outline=None, r=None):
    x0, y0, x1, y1 = box
    rrect(im, box, (y1 - y0) / 2 if r is None else r, fill, outline, 2, alpha)
    txt(im, label, (x0 + x1) / 2, (y0 + y1) / 2, "sans", size, 600, ink, alpha=alpha)


def check(im, x, y, s=26, color=C["gold"], k=1.0, width=4, alpha=1.0):
    pts = [(x - s * 0.5, y), (x - s * 0.12, y + s * 0.38), (x + s * 0.6, y - s * 0.45)]
    p, _ = poly_partial(pts, k)
    if len(p) > 1:
        line(im, p, color, width, alpha)


def strike(im, x0, x1, y, k, color=C["gold"], width=6, alpha=1.0):
    if k > 0:
        line(im, [(x0, y), (x0 + (x1 - x0) * clamp(k), y)], color, width, alpha)


def cursor(im, x, y, scale=1.0, color=C["ivory"], alpha=1.0):
    """Abstract pointer arrow (deliberately not an OS cursor)."""
    s = 46 * scale
    pts = [(x, y), (x, y + s), (x + s * 0.28, y + s * 0.74), (x + s * 0.5, y + s * 1.1),
           (x + s * 0.64, y + s * 1.03), (x + s * 0.44, y + s * 0.68), (x + s * 0.8, y + s * 0.68)]
    with Vec(im) as d:
        d.polygon(list(np.ravel(pts)), pen(C["obs"], 3, alpha), brush(color, alpha))
