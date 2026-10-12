"""Synthesised sound design: every hit, click and bed is generated here, so there is nothing to license."""
import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

SR = 48000
_rng = np.random.default_rng(11)


def _t(d):
    return np.arange(int(d * SR)) / SR


def _env(d, attack=0.002, decay=0.3):
    t = _t(d)
    a = np.clip(t / attack, 0, 1) if attack > 0 else np.ones_like(t)
    return a * np.exp(-t / decay)


def _filt(x, kind, f, order=2):
    if isinstance(f, (list, tuple)):
        sos = butter(order, [f[0] / (SR / 2), f[1] / (SR / 2)], btype=kind, output="sos")
    else:
        sos = butter(order, f / (SR / 2), btype=kind, output="sos")
    return sosfilt(sos, x)


def noise(d):
    return _rng.standard_normal(int(d * SR))


def sine_sweep(f0, f1, d, curve=8.0):
    t = _t(d)
    f = f1 + (f0 - f1) * np.exp(-t * curve)
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


def norm(x, peak=1.0):
    m = np.max(np.abs(x)) or 1.0
    return x * (peak / m)


# ---------------------------------------------------------------- hits (each is normalised to 1.0 peak)
def bass_hit(d=1.2, f0=140, f1=42):
    body = sine_sweep(f0, f1, d, 14) * _env(d, 0.001, 0.45)
    click = _filt(noise(0.012), "highpass", 2500) * _env(0.012, 0.0005, 0.004)
    x = body.copy()
    x[: len(click)] += click * 0.6
    return norm(np.tanh(x * 1.6))


def hit808(d=1.8):
    body = sine_sweep(110, 46, d, 10) * _env(d, 0.001, 0.9)
    return norm(np.tanh(body * 2.4))


def click(d=0.03, f=3500):
    x = _filt(noise(d), "bandpass", (f * 0.6, min(f * 1.8, 20000))) * _env(d, 0.0003, 0.006)
    x += np.sin(2 * np.pi * f * _t(d)) * _env(d, 0.0003, 0.004) * 0.5
    return norm(x)


def metal_click(d=0.12):
    t = _t(d)
    x = sum(np.sin(2 * np.pi * f * t) * a for f, a in [(3150, 1), (4730, 0.6), (6900, 0.35)]) * _env(d, 0.0002, 0.018)
    x += _filt(noise(d), "highpass", 4000) * _env(d, 0.0002, 0.003)
    return norm(x)


def tick(d=0.08):
    t = _t(d)
    x = np.sin(2 * np.pi * 2300 * t) * _env(d, 0.0002, 0.012) + _filt(noise(d), "highpass", 3000) * _env(d, 0.0002, 0.003)
    return norm(x)


def knock(d=0.35):
    t = _t(d)
    x = (np.sin(2 * np.pi * 185 * t) + 0.6 * np.sin(2 * np.pi * 410 * t)) * _env(d, 0.0005, 0.06)
    x += _filt(noise(d), "lowpass", 1800) * _env(d, 0.0003, 0.012) * 1.5
    return norm(np.tanh(x * 1.5))


def snap(d=0.08):
    x = _filt(noise(d), "bandpass", (1800, 5200)) * _env(d, 0.0003, 0.012)
    return norm(x)


def whoosh_hit(d=0.55):
    """Whoosh that already peaks at the start (for frame 0) and trails off."""
    n = noise(d)
    t = _t(d)
    out = np.zeros_like(n)
    for i, (lo, hi) in enumerate([(300, 900), (700, 2000), (1500, 4000)]):
        out += _filt(n, "bandpass", (lo, hi)) * np.exp(-t / (0.12 + i * 0.05))
    out *= np.clip(t / 0.004, 0, 1)
    sub = sine_sweep(90, 50, d, 6) * _env(d, 0.002, 0.2) * 0.6
    return norm(out + sub)


def whoosh(d=0.6):
    """Rising-then-falling whoosh for transitions."""
    n = noise(d)
    t = _t(d)
    e = np.sin(np.pi * t / d) ** 2
    return norm(_filt(n, "bandpass", (500, 3000)) * e)


def glass(d=1.6):
    t = _t(d)
    x = sum(np.sin(2 * np.pi * f * t) * a * np.exp(-t / dec) for f, a, dec in
            [(2093, 1, 0.9), (3322, 0.5, 0.6), (5274, 0.3, 0.35), (7040, 0.15, 0.2)])
    x *= np.clip(t / 0.0004, 0, 1)
    x += _filt(noise(d), "highpass", 5000) * _env(d, 0.0002, 0.002) * 0.5
    return norm(x)


def porcelain(d=0.6):
    t = _t(d)
    x = sum(np.sin(2 * np.pi * f * t) * a * np.exp(-t / dec) for f, a, dec in
            [(2870, 1, 0.16), (4120, 0.7, 0.1), (6230, 0.4, 0.06)])
    x *= np.clip(t / 0.0003, 0, 1)
    return norm(x)


def crystal(d=3.0, f=1046.5):
    t = _t(d)
    x = sum(np.sin(2 * np.pi * f * m * t) * a * np.exp(-t / dec) for m, a, dec in
            [(1, 1, 1.6), (2.76, 0.4, 0.9), (5.4, 0.2, 0.5), (8.9, 0.08, 0.25)])
    x *= np.clip(t / 0.0006, 0, 1)
    return norm(x)


def pen_scratch(d=0.5):
    n = _filt(noise(d), "bandpass", (2500, 7000))
    t = _t(d)
    am = 0.55 + 0.45 * np.sin(2 * np.pi * 38 * t) ** 2
    return norm(n * am * _env(d, 0.001, 0.22))


def nib_boom(d=1.4):
    boom = sine_sweep(95, 38, d, 7) * _env(d, 0.001, 0.5)
    sc = np.zeros_like(boom)
    p = pen_scratch(0.45)
    sc[: len(p)] = p * 0.45
    return norm(np.tanh(boom * 1.8) + sc)


def shutter(d=0.18):
    x = np.zeros(int(d * SR))
    for at, g in [(0, 1.0), (0.055, 0.7)]:
        c = _filt(noise(0.025), "bandpass", (1200, 6000)) * _env(0.025, 0.0002, 0.005)
        i = int(at * SR)
        x[i:i + len(c)] += c * g
    return norm(x)


def keytap(d=0.06):
    t = _t(d)
    x = _filt(noise(d), "bandpass", (900, 3500)) * _env(d, 0.0002, 0.008)
    x += np.sin(2 * np.pi * 620 * t) * _env(d, 0.0002, 0.01) * 0.6
    return norm(x)


def mouse_click(d=0.1):
    x = np.zeros(int(d * SR))
    for at, g in [(0, 1.0), (0.045, 0.55)]:
        c = keytap(0.03) * g
        i = int(at * SR)
        x[i:i + len(c)] += c
    return norm(x)


def flap(d=0.04):
    x = _filt(noise(d), "bandpass", (600, 2400)) * _env(d, 0.0002, 0.006)
    x += np.sin(2 * np.pi * 380 * _t(d)) * _env(d, 0.0002, 0.008)
    return norm(x)


def flap_burst(d=0.45, n=9):
    x = np.zeros(int(d * SR))
    for i in range(n):
        c = flap() * (1 - i / (n + 2))
        j = int(i * d / n * 0.9 * SR)
        x[j:j + len(c)] += c
    sub = sine_sweep(120, 55, d, 10) * _env(d, 0.001, 0.15) * 0.7
    return norm(x + sub)


def tape_stop(d=0.5):
    t = _t(d)
    f = 220 * (1 - t / d) ** 2 + 30
    x = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.4 + np.sin(2 * np.pi * np.cumsum(f) / SR)
    x = _filt(x, "lowpass", 1500) * np.clip(1 - t / d, 0, 1)
    thud = sine_sweep(120, 50, d, 12) * _env(d, 0.001, 0.12)
    return norm(x * 0.6 + thud)


def paper_snap(d=0.2):
    x = _filt(noise(d), "highpass", 1500) * _env(d, 0.0003, 0.02)
    x += _filt(noise(d), "bandpass", (300, 1200)) * _env(d, 0.0005, 0.05) * 0.5
    return norm(x)


def tom(d=0.9):
    x = sine_sweep(170, 85, d, 9) * _env(d, 0.001, 0.28)
    head = _filt(noise(d), "bandpass", (400, 2500)) * _env(d, 0.0005, 0.02) * 0.5
    return norm(np.tanh((x + head) * 1.4))


def boom_shimmer(d=3.0):
    boom = sine_sweep(80, 35, d, 5) * _env(d, 0.001, 0.8)
    sh = crystal(d, 1568) * 0.25
    return norm(np.tanh(boom * 1.6) + sh)


def swish(d=0.22):
    t = _t(d)
    e = np.clip(t / 0.01, 0, 1) * np.exp(-t / 0.06)
    return norm(_filt(noise(d), "bandpass", (1500, 6000)) * e)


def marker_strike(d=0.3):
    x = swish(d) * 0.8
    x += knock(d) * 0.35
    return norm(x)


def ping(d=1.0, f=1318.5):
    t = _t(d)
    x = (np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * f * 2 * t)) * _env(d, 0.0005, 0.35)
    x += click(d, 5000) * 0.3
    return norm(x)


def thock(d=0.3):
    t = _t(d)
    x = sine_sweep(320, 160, d, 30) * _env(d, 0.0005, 0.05)
    x += _filt(noise(d), "bandpass", (600, 2500)) * _env(d, 0.0002, 0.01) * 0.7
    return norm(x)


def low_thud(d=0.5):
    return norm(np.tanh(sine_sweep(90, 45, d, 15) * _env(d, 0.001, 0.12) * 2))


def chime_stab(d=1.8):
    t = _t(d)
    x = 0
    for f in (523.25, 659.25, 783.99, 1046.5):
        x = x + np.sin(2 * np.pi * f * t) * np.exp(-t / 0.7) + 0.3 * np.sin(2 * np.pi * f * 3 * t) * np.exp(-t / 0.2)
    x *= np.clip(t / 0.0008, 0, 1)
    return norm(x + click(d, 6000) * 0.4)


def doum(d=0.8):
    t = _t(d)
    x = sine_sweep(140, 72, d, 18) * _env(d, 0.0008, 0.22)
    slap = _filt(noise(d), "bandpass", (200, 1200)) * _env(d, 0.0003, 0.015)
    return norm(np.tanh((x + slap * 0.7) * 1.8))


def tek(d=0.15):
    x = _filt(noise(d), "bandpass", (2000, 7000)) * _env(d, 0.0002, 0.012)
    x += np.sin(2 * np.pi * 1700 * _t(d)) * _env(d, 0.0002, 0.01) * 0.5
    return norm(x)


def piano_stab(d=2.2, notes=(220.0, 261.63, 329.63, 440.0)):
    t = _t(d)
    x = 0
    for f in notes:
        for h, a in [(1, 1), (2, 0.45), (3, 0.2), (4, 0.1)]:
            x = x + a * np.sin(2 * np.pi * f * h * t) * np.exp(-t * (1.2 + h * 0.8))
    x *= np.clip(t / 0.0015, 0, 1)
    return norm(x + low_thud(d) * 0.4)


def riser(d=1.2):
    t = _t(d)
    n = _filt(noise(d), "bandpass", (800, 5000)) * (t / d) ** 2
    return norm(n)


def heartbeat_pulse(d=0.4):
    return norm(sine_sweep(70, 45, d, 12) * _env(d, 0.002, 0.08))


# ---------------------------------------------------------------- beds
CHORDS = {
    "am": (110.0, 164.81, 220.0, 261.63),
    "dm": (73.42, 110.0, 146.83, 174.61),
    "fmaj": (87.31, 130.81, 174.61, 220.0),
    "em": (82.41, 123.47, 164.81, 196.0),
    "cmaj": (65.41, 98.0, 130.81, 164.81),
    "gm": (98.0, 146.83, 196.0, 233.08),
    "bbmaj": (58.27, 87.31, 116.54, 146.83),
}


def pad(d, chord="am", bright=900, lfo=0.15):
    t = _t(d)
    x = 0
    for i, f in enumerate(CHORDS[chord]):
        det = 1 + 0.0025 * ((i % 2) * 2 - 1)
        x = x + np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 2 * det * t) + 0.25 * np.sin(
            2 * np.pi * f * 3 * t)
    x = _filt(x, "lowpass", bright)
    x *= 0.75 + 0.25 * np.sin(2 * np.pi * lfo * t)
    return norm(x)


def pulse_bed(d, bpm=96, f=55.0):
    x = np.zeros(int(d * SR))
    step = 60 / bpm
    p = heartbeat_pulse(0.35)
    k = 0.0
    while k < d:
        i = int(k * SR)
        seg = p[: len(x) - i]
        x[i:i + len(seg)] += seg
        k += step
    return norm(x)


def air(d):
    return norm(_filt(noise(d), "bandpass", (3000, 9000)) * 0.3)


# ---------------------------------------------------------------- mixing
class Mix:
    def __init__(self, dur):
        self.n = int(dur * SR)
        self.L = np.zeros(self.n)
        self.R = np.zeros(self.n)

    def add(self, x, t, gain=1.0, pan=0.0):
        i = int(t * SR)
        if i >= self.n:
            return
        x = np.asarray(x)[: self.n - i] * gain
        self.L[i:i + len(x)] += x * (1 - max(0, pan))
        self.R[i:i + len(x)] += x * (1 + min(0, pan))

    def bed(self, x, gain=0.12, fade=0.4, start=0.0, end=None):
        end = self.n / SR if end is None else end
        n = int((end - start) * SR)
        x = np.resize(x, n)
        e = np.ones(n)
        f = int(fade * SR)
        if f:
            e[:f] = np.linspace(0, 1, f)
            e[-f:] = np.minimum(e[-f:], np.linspace(1, 0, f))
        self.add(x * e, start, gain)

    def render(self, room=0.18, peak=0.6):
        ir_n = int(1.6 * SR)
        tt = np.arange(ir_n) / SR
        irL = _rng.standard_normal(ir_n) * np.exp(-tt / 0.45)
        irR = _rng.standard_normal(ir_n) * np.exp(-tt / 0.45)
        irL = _filt(irL, "lowpass", 6000)
        irR = _filt(irR, "lowpass", 6000)
        irL /= np.sqrt(np.sum(irL ** 2))
        irR /= np.sqrt(np.sum(irR ** 2))
        wL = fftconvolve(self.L, irL)[: self.n]
        wR = fftconvolve(self.R, irR)[: self.n]
        L = self.L + wL * room
        R = self.R + wR * room
        st = np.stack([L, R], 1)
        # tail fade so the loop point is clean
        f = int(0.06 * SR)
        st[-f:] *= np.linspace(1, 0, f)[:, None]
        m = np.max(np.abs(st)) or 1.0
        st = st * (peak / m)
        # gentle high-pass to remove sub rumble below 30 Hz (saves headroom for the AAC encoder)
        st = np.stack([_filt(st[:, 0], "highpass", 30), _filt(st[:, 1], "highpass", 30)], 1)
        m = np.max(np.abs(st)) or 1.0
        return (st * (peak / m)).astype(np.float32)
