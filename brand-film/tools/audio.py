"""Original score, sound design and sonic logo for the DevEraXTech brand film.

Everything is synthesised here from first principles (oscillators, noise, filters,
a synthetic reverb), so there is no third-party audio and no licensing question.
Event times mirror the scene files (see src/scenes/*): change one, change both.

usage: python3 tools/audio.py <out_dir> [variant]   variant: main | shock | curiosity
writes  music.wav, sfx.wav (48 kHz / 32-bit stereo stems, unmastered)
"""
import sys, os
import numpy as np
from scipy import signal
from scipy.io import wavfile

SR = 48000
DUR = 36.0
N = int(SR * DUR)
RNG = np.random.default_rng(36036)

# ---- timeline (seconds), mirrored from the scenes -------------------------------
VARIANT = sys.argv[2] if len(sys.argv) > 2 else 'main'
SHOCK = {'main': 1.0, 'shock': 0.32, 'curiosity': 1.9}[VARIANT]
S03_LANDINGS = [6.5, 6.72, 6.96, 7.16, 7.34, 7.44, 7.54]
S07_CLICKS = [20.74, 21.98, 23.2]
S08_RISES = [24.0, 24.8, 25.6]
S08_CONVERGE = 27.0
LOCK = 30.3
SHEEN = (34.0, 35.05)
BEAT = 0.5  # 120 BPM: every attention event in the edit falls on this grid


def midi(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def tvec(dur):
    return np.arange(int(dur * SR)) / SR


class Bus:
    def __init__(self):
        self.x = np.zeros((N, 2))

    def add(self, sig, t0, pan=0.0, gain=1.0):
        """Mono or stereo signal placed at t0 with equal-power pan (-1..1)."""
        if sig.ndim == 1:
            a = (pan + 1) * np.pi / 4
            sig = np.stack([sig * np.cos(a), sig * np.sin(a)], 1) * np.sqrt(2)
        i0 = int(round(t0 * SR))
        if i0 >= N:
            return
        j0 = max(0, -i0)
        i0 = max(0, i0)
        n = min(len(sig) - j0, N - i0)
        if n > 0:
            self.x[i0:i0 + n] += sig[j0:j0 + n] * gain


def env_exp(t, decay):
    return np.exp(-t / decay)


def adsr(n, a, r, total=None):
    t = np.arange(n) / SR
    total = total if total is not None else n / SR
    e = np.minimum(1, t / max(a, 1e-4))
    e *= np.clip((total - t) / max(r, 1e-4), 0, 1)
    return e


def sos(kind, f, order=2):
    f = np.atleast_1d(f) / (SR / 2)
    f = np.clip(f, 1e-4, 0.999)
    return signal.butter(order, f if len(f) > 1 else f[0], btype=kind, output='sos')


def filt(x, kind, f, order=2):
    return signal.sosfilt(sos(kind, f, order), x, axis=0)


def sweep_filter(x, kind, f0, f1, block=0.02, curve=2.0):
    """Time-varying Butterworth: block-wise with overlap-add crossfades."""
    hop = int(block * SR)
    win = np.hanning(hop * 2 + 1)[:-1]
    out = np.zeros_like(x)
    nb = (len(x) + hop - 1) // hop
    for b in range(nb):
        s = max(0, b * hop - hop // 2)
        e = min(len(x), s + hop * 2)
        p = (b / max(1, nb - 1)) ** curve
        f = f0 * (f1 / f0) ** p
        seg = signal.sosfilt(sos(kind, f), x[max(0, s - 2048):e], axis=0)[s - max(0, s - 2048):]
        w = win[: len(seg)] if x.ndim == 1 else win[: len(seg), None]
        out[s:s + len(seg)] += seg * w
    return out


def noise(dur):
    return RNG.standard_normal(int(dur * SR))


def saw(f, dur, harmonics=16, rolloff=6.0, detune=0.0):
    t = tvec(dur)
    out = np.zeros_like(t)
    for k in range(1, harmonics + 1):
        if f * k > SR * 0.45:
            break
        out += np.sin(2 * np.pi * f * k * t * (1 + detune) + k * 0.7) / k * np.exp(-k / rolloff)
    return out


# ---- instruments -----------------------------------------------------------------
def sub_hit(f0, f1, dur, decay, glide=0.08):
    t = tvec(dur)
    f = f1 + (f0 - f1) * np.exp(-t / glide)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * env_exp(t, decay) * adsr(len(t), 0.003, 0.05)


def kick(gain=1.0):
    t = tvec(0.6)
    f = 46 + 110 * np.exp(-t / 0.03)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(t, 0.22)
    click = filt(noise(0.6), 'highpass', 3000) * env_exp(t, 0.004) * 0.25
    return (body + click) * gain


def clap():
    d = 0.35
    t = tvec(d)
    n = filt(noise(d), 'bandpass', [900, 2600])
    e = np.zeros_like(t)
    for off in (0, 0.011, 0.023):
        e += (t >= off) * np.exp(-np.clip(t - off, 0, None) / 0.006)
    e += (t >= 0.03) * np.exp(-np.clip(t - 0.03, 0, None) / 0.11) * 0.6
    return n * e * 0.5


def hat(open_=False):
    d = 0.35 if open_ else 0.08
    t = tvec(d)
    return filt(noise(d), 'highpass', 7500) * env_exp(t, 0.09 if open_ else 0.016) * 0.35


def tick(f=4200, d=0.03):
    t = tvec(d)
    ping = np.sin(2 * np.pi * f * t) * env_exp(t, 0.006)
    tr = filt(noise(d), 'highpass', 5000) * env_exp(t, 0.0015)
    return ping * 0.6 + tr * 0.5


def click_heavy(f=3200):
    """Tactile machined click with low-frequency weight."""
    t = tvec(0.5)
    tr = filt(noise(0.5), 'highpass', 2500) * env_exp(t, 0.0018)
    ping = (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 2.71 * t)) * env_exp(t, 0.025)
    thump = sub_hit(140, 62, 0.5, 0.09, 0.02)
    return tr * 0.9 + ping * 0.35 + thump * 0.9


def glass_tinkle(f):
    d = 0.5
    t = tvec(d)
    dec = 0.03 + 0.15 * RNG.random()
    s = sum(a * np.sin(2 * np.pi * f * r * t + RNG.random() * 6) for r, a in ((1, 1), (2.76, 0.5), (5.4, 0.25)))
    return s * env_exp(t, dec) * adsr(len(t), 0.0008, 0.02)


def bell(f, dur=3.0, index=2.2, ratio=3.5, decay=1.4):
    t = tvec(dur)
    idx = index * env_exp(t, 0.35)
    mod = np.sin(2 * np.pi * f * ratio * t) * idx
    car = np.sin(2 * np.pi * f * t + mod)
    body = np.sin(2 * np.pi * f * t) * 0.6 + np.sin(2 * np.pi * f * 2 * t) * 0.12
    return (car * 0.55 + body) * env_exp(t, decay) * adsr(len(t), 0.004, 0.3)


def metal_resonance(f0, dur=4.0):
    t = tvec(dur)
    out = np.zeros_like(t)
    for r, a, d in ((1, 1, 2.4), (2.32, 0.6, 1.8), (4.25, 0.4, 1.2), (6.63, 0.25, 0.9), (9.38, 0.15, 0.6)):
        out += a * np.sin(2 * np.pi * f0 * r * t + RNG.random() * 6) * env_exp(t, d)
    return out * adsr(len(t), 0.02, 0.5)


def pluck(f, dur, bright=1.0):
    t = tvec(dur)
    out = np.zeros_like(t)
    for k in range(1, 18):
        if f * k > SR * 0.45:
            break
        out += np.sin(2 * np.pi * f * k * t) / k * np.exp(-t * (4 + k * 2.2 / bright))
    return out * adsr(len(t), 0.002, 0.03)


def pad(notes, dur, attack=1.0, release=1.0, bright=5.0, gain=1.0):
    t = tvec(dur)
    L = np.zeros_like(t)
    R = np.zeros_like(t)
    for m in notes:
        f = midi(m)
        for d, side in ((-0.0035, 0), (0.0035, 1), (0.0, 2)):
            v = saw(f, dur, harmonics=14, rolloff=bright, detune=d)
            if side == 0:
                L += v
            elif side == 1:
                R += v
            else:
                L += v * 0.6
                R += v * 0.6
    e = adsr(len(t), attack, release)
    return np.stack([L, R], 1) * e[:, None] * gain / max(1, len(notes))


def taiko(gain=1.0):
    t = tvec(1.2)
    f = 52 + 40 * np.exp(-t / 0.05)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(t, 0.4)
    skin = filt(noise(1.2), 'lowpass', 500) * env_exp(t, 0.08) * 0.6
    return (body + skin) * gain


def whoosh(dur, f0, f1, curve=1.5, shape='swell'):
    n = noise(dur)
    x = sweep_filter(n, 'bandpass' if False else 'lowpass', f0, f1, curve=curve)
    t = tvec(dur)
    if shape == 'swell':
        e = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 2
    elif shape == 'rise':
        e = (t / dur) ** 2.5
    else:
        e = np.exp(-t / (dur * 0.3))
    return x * e


def riser(dur, f0=300, f1=9000):
    n = noise(dur)
    x = sweep_filter(n, 'highpass', f0, f1 * 0.3, curve=1.2) * 0.6 + sweep_filter(n, 'lowpass', f0 * 2, f1, curve=1.6) * 0.4
    t = tvec(dur)
    return x * (t / dur) ** 2.2


def reverb_ir(seconds=2.8, predelay=0.012, bright=6000, seed=5):
    r = np.random.default_rng(seed)
    n = int(seconds * SR)
    t = np.arange(n) / SR
    ir = r.standard_normal((n, 2)) * np.exp(-t * 6.9 / seconds)[:, None]
    ir = filt(ir, 'lowpass', bright)
    ir[: int(predelay * SR)] = 0
    return ir / np.sqrt((ir ** 2).sum())


def reverb(x, ir, wet):
    out = np.stack([signal.fftconvolve(x[:, c], ir[:, c])[:N] for c in range(2)], 1)
    return out * wet


# ---- compose ---------------------------------------------------------------------
def build():
    M = Bus()      # music
    Mrv = Bus()    # music reverb send
    S = Bus()      # sound design
    Srv = Bus()    # sfx reverb send

    # ===== ACT 1 · 0–3 · silence, fracture, suspense =====
    # glass under strain: sparse ticks accelerating into the shock
    crack0 = {'main': 0.0, 'shock': 0.0, 'curiosity': 0.6}[VARIANT]
    tt = crack0
    while tt < SHOCK:
        p = (tt - crack0) / max(1e-3, SHOCK - crack0)
        S.add(tick(3000 + 3000 * RNG.random(), 0.02), tt, pan=RNG.uniform(-0.5, 0.5), gain=0.05 + 0.2 * p)
        tt += 0.12 * (1 - p) ** 1.5 + 0.012
    S.add(filt(noise(SHOCK - crack0 + 0.05), 'bandpass', [2500, 6000]) * np.linspace(0, 0.03, int((SHOCK - crack0 + 0.05) * SR)), crack0)
    # the fracture: sub drop, shatter body, a rain of glass
    S.add(sub_hit(70, 31, 2.5, 0.9, 0.06), SHOCK, gain=1.0)
    sh = filt(noise(1.2), 'highpass', 1800) * env_exp(tvec(1.2), 0.18)
    S.add(sh, SHOCK, gain=0.45)
    Srv.add(sh, SHOCK, gain=0.35)
    for _ in range(320):
        dt = RNG.exponential(0.45)
        if SHOCK + dt > 2.95:
            continue
        g = 0.12 * np.exp(-dt / 0.6) * (0.4 + RNG.random())
        tk = glass_tinkle(2400 + 7000 * RNG.random())
        S.add(tk, SHOCK + dt, pan=RNG.uniform(-0.9, 0.9), gain=g)
        Srv.add(tk, SHOCK + dt, gain=g * 0.8)
    # the dive into the fragment
    S.add(riser(1.0, 400, 9000), 2.0, gain=0.22)
    Srv.add(riser(1.0, 400, 9000), 2.0, gain=0.12)

    # ===== ACT 2 · 3–9 · new standard, low rhythmic tension =====
    S.add(sub_hit(36, 49, 3.0, 1.4, 0.8) * adsr(int(3.0 * SR), 0.5, 1.0), 3.0, gain=0.6)   # sub swell
    S.add(metal_resonance(73.42, 4.0), 3.02, gain=0.18)
    Srv.add(metal_resonance(73.42, 4.0), 3.02, gain=0.14)
    lq = sweep_filter(noise(2.4), 'lowpass', 300, 1800, curve=1.0) * np.sin(np.pi * np.linspace(0, 1, int(2.4 * SR))) ** 2
    S.add(lq * (1 + 0.5 * np.sin(np.linspace(0, 30, len(lq)))), 3.1, gain=0.06)
    S.add(whoosh(0.9, 200, 4000, shape='swell'), 5.3, gain=0.22)
    for i, lt in enumerate(S03_LANDINGS):
        S.add(tick(2600 + 180 * i, 0.04), lt, pan=(-0.4, 0.4, 0, 0.5, -0.5, 0, 0.3)[i], gain=0.35)
        S.add(sub_hit(120, 70, 0.2, 0.05, 0.01), lt, gain=0.25)
    S.add(whoosh(0.6, 300, 6000, shape='rise'), 8.45, gain=0.2)

    tt = 3.0
    while tt < 9.0 - 1e-6:   # heartbeat on the half-note
        M.add(sub_hit(58, 38, 0.6, 0.18, 0.03), tt, gain=0.25 + 0.2 * (tt - 3) / 6)
        tt += 1.0
    tt = 3.5
    while tt < 9.0 - 1e-6:   # muted bass ostinato, opening slowly
        b = pluck(midi(38), 0.24, bright=0.35 + 0.8 * (tt - 3.5) / 5.5)
        M.add(b, tt, gain=0.16 + 0.1 * (tt - 3.5) / 5.5)
        tt += 0.25
    M.add(pad([50, 53, 57, 64], 6.4, attack=2.5, release=1.2, bright=2.5), 3.0, gain=0.12)
    Mrv.add(pad([50, 53, 57, 64], 6.4, attack=2.5, release=1.2, bright=2.5), 3.0, gain=0.1)
    tt = 6.0
    while tt < 9.0 - 1e-6:
        M.add(tick(6500, 0.015), tt, pan=0.3 if int(tt * 4) % 2 else -0.3, gain=0.05)
        tt += 0.125

    # ===== ACT 3 · 9–20 · engineered: modern electronic rhythm =====
    S.add(sub_hit(90, 34, 2.2, 0.7, 0.05), 9.0, gain=1.0)
    S.add(kick(1.0), 9.0, gain=0.8)
    hitn = filt(noise(1.5), 'bandpass', [200, 5000]) * env_exp(tvec(1.5), 0.12)
    S.add(hitn, 9.0, gain=0.25)
    Srv.add(hitn, 9.0, gain=0.5)
    for i in range(8):   # fine percussive details after the impact
        S.add(tick(5000 - i * 300, 0.03), 9.12 + i * 0.0625, pan=(-1) ** i * 0.6, gain=0.18 * (1 - i / 9))
    # outline trace: a fine rising line ending on a chime
    tr = tvec(0.8)
    zz = np.sin(2 * np.pi * np.cumsum(900 + 900 * (tr / 0.8) ** 2) / SR) * np.sin(np.pi * tr / 0.8) ** 2
    S.add(zz, 10.95, gain=0.05)
    S.add(bell(midi(86), 2.0, index=1.2, decay=0.6), 11.75, gain=0.08)
    Srv.add(bell(midi(86), 2.0, index=1.2, decay=0.6), 11.75, gain=0.1)
    # phone: materialise, turn, roll, push
    S.add(sub_hit(110, 55, 0.8, 0.2), 12.0, gain=0.35)
    S.add(whoosh(1.0, 200, 3000), 12.95, pan=-0.3, gain=0.2)
    S.add(whoosh(0.7, 250, 3500), 14.25, pan=0.3, gain=0.16)
    S.add(riser(1.0, 300, 10000), 15.0, gain=0.2)
    # granular intelligence: grains of light trading places across the stereo field
    for _ in range(420):
        gt = 16.0 + RNG.random() * 4.0
        dens = (gt - 16.0) / 4.0
        if RNG.random() > 0.35 + 0.65 * dens:
            continue
        f = midi(RNG.choice([62, 65, 69, 74, 77, 81, 86]))
        d = 0.04 + 0.08 * RNG.random()
        g = np.sin(2 * np.pi * f * tvec(d)) * np.hanning(int(d * SR))
        S.add(g, gt, pan=RNG.uniform(-1, 1), gain=0.035)
        Srv.add(g, gt, gain=0.04)
    S.add(riser(2.0, 200, 8000), 18.0, gain=0.18)

    chords = [(9, 50), (11, 46), (13, 53), (15, 48), (17, 50), (19, 46)]  # (start, bass midi) Dm Bb F C Dm Bb
    triads = {50: [62, 65, 69], 46: [58, 62, 65], 53: [65, 69, 72], 48: [60, 64, 67]}
    tt = 9.0
    while tt < 19.5 - 1e-6:
        M.add(kick(), tt, gain=0.55)
        tt += 0.5
    tt = 9.5
    while tt < 20.0 - 1e-6:
        M.add(clap(), tt, gain=0.45)
        Mrv.add(clap(), tt, gain=0.25)
        tt += 1.0
    tt = 9.0
    while tt < 20.0 - 1e-6:
        k = round((tt - 9.0) / 0.125)
        if tt >= 12.0 and k % 4 == 2:
            M.add(hat(True), tt, pan=0.2, gain=0.22)
        else:
            M.add(hat(), tt, pan=-0.2 if k % 2 else 0.2, gain=0.2 if k % 2 else 0.3)
        tt += 0.125 if tt < 19.5 else 0.0625
    for (c0, bass) in chords:
        c1 = min(c0 + 2, 20)
        tt = c0
        while tt < c1 - 1e-6:
            M.add(saw(midi(bass - 12), 0.22, harmonics=10, rolloff=3) * env_exp(tvec(0.22), 0.09), tt, gain=0.28)
            tt += 0.25
        M.add(pad(triads[bass], c1 - c0 + 0.3, attack=0.4, release=0.4, bright=3.5), c0, gain=0.09)
        Mrv.add(pad(triads[bass], c1 - c0 + 0.3, attack=0.4, release=0.4, bright=3.5), c0, gain=0.08)
        if c0 >= 12:   # elegant accelerating arpeggio
            step = 0.25 if c0 < 14 else 0.125
            tt = c0
            i = 0
            while tt < c1 - 1e-6:
                note = triads[bass][i % 3] + 12 * ((i // 3) % 2)
                ap = pluck(midi(note), 0.3, bright=1.4)
                M.add(ap, tt, pan=0.35 * np.sin(i * 0.9), gain=0.07)
                Mrv.add(ap, tt, gain=0.06)
                tt += step
                i += 1

    # ===== ACT 4 · 20–28 · obsessive craft, values: cinematic percussion =====
    for i, ct in enumerate(S07_CLICKS):
        S.add(click_heavy(3200 - 300 * i), ct, gain=0.75)
        Srv.add(click_heavy(3200 - 300 * i), ct, gain=0.2)
    for cut in (21.333, 22.667):
        S.add(whoosh(0.25, 800, 6000, shape='decay'), cut - 0.02, gain=0.06)
    S.add(whoosh(0.8, 200, 5000), 23.35, gain=0.18)
    for i, r0 in enumerate(S08_RISES):
        rum = filt(noise(0.9), 'lowpass', 180) * np.sin(np.pi * np.linspace(0, 1, int(0.9 * SR)))
        S.add(rum, r0, gain=0.5)
        S.add(sub_hit(80, 33, 2.0, 0.7, 0.05), r0 + 0.04, gain=0.75 + 0.1 * i)
        S.add(taiko(1.0), r0 + 0.04, gain=0.45)
        Srv.add(taiko(1.0), r0 + 0.04, gain=0.4)
    S.add(sub_hit(100, 30, 3.0, 1.1, 0.05), S08_CONVERGE, gain=1.0)
    S.add(metal_resonance(55.0, 3.0), S08_CONVERGE, gain=0.22)
    Srv.add(metal_resonance(55.0, 3.0), S08_CONVERGE, gain=0.25)
    S.add(whoosh(0.85, 200, 3000, shape='rise'), 27.15, gain=0.18)

    # taiko ostinato, densifying bar by bar
    pattern_a = [0, 1.0, 1.5]
    pattern_b = [0, 0.5, 1.0, 1.25, 1.5, 1.75]
    for bar in range(4):
        b0 = 20.0 + bar * 2.0
        pat = pattern_a if b0 < 24 else pattern_b
        for p in pat:
            tt = b0 + p
            if tt >= 27.0:
                continue
            M.add(taiko(1.0), tt, pan=RNG.uniform(-0.3, 0.3), gain=0.25 + 0.06 * bar)
            Mrv.add(taiko(1.0), tt, gain=0.15)
    prog_ = [(20, [50, 57, 62, 57]), (22, [46, 53, 58, 53]), (24, [43, 50, 55, 50]), (26, [45, 52, 57, 52])]
    pads4 = {20: [50, 53, 57, 62], 22: [46, 50, 53, 58], 24: [43, 50, 55, 58], 26: [45, 49, 52, 57]}
    for c0, cell in prog_:
        c1 = min(c0 + 2, 27.0)
        tt = c0
        i = 0
        while tt < c1 - 1e-6:   # string ostinato
            st = saw(midi(cell[i % 4]), 0.13, harmonics=12, rolloff=4) * adsr(int(0.13 * SR), 0.01, 0.05)
            M.add(st, tt, pan=0.25 * ((i % 2) * 2 - 1), gain=0.06 + 0.02 * (c0 - 20) / 2)
            tt += 0.125
            i += 1
        sw = pad(pads4[c0], c1 - c0 + 0.4, attack=1.2, release=0.4, bright=4 + (c0 - 20) / 2, gain=1.0)
        M.add(sw, c0, gain=0.08 + 0.03 * (c0 - 20) / 2)
        Mrv.add(sw, c0, gain=0.09)
    tt = 20.0
    while tt < 27.0 - 1e-6:
        M.add(kick(0.7), tt, gain=0.3)
        tt += 0.5
    M.add(pad([38, 50, 57, 62, 69], 1.0, attack=0.01, release=0.8, bright=5), S08_CONVERGE, gain=0.18)
    Mrv.add(pad([38, 50, 57, 62, 69], 1.0, attack=0.01, release=0.8, bright=5), S08_CONVERGE, gain=0.3)
    rev = filt(noise(0.9), 'highpass', 3000) * (tvec(0.9) / 0.9) ** 3   # reverse swell into the reveal
    M.add(rev, 27.05, gain=0.12)

    # ===== ACT 5 · 28–36 · brand reveal and sonic logo =====
    for _ in range(600):   # metallic fragments in the air, gathering
        gt = 28.0 + 2.3 * RNG.random() ** 0.8
        tk = glass_tinkle(5000 + 5000 * RNG.random())
        g = 0.02 + 0.05 * ((gt - 28.0) / 2.3) ** 2
        S.add(tk, gt, pan=RNG.uniform(-1, 1), gain=g)
        Srv.add(tk, gt, gain=g)
    S.add(riser(1.8, 500, 12000), 28.5, gain=0.08)
    # sonic signature: D5 · A5 · E6, a rising fifth and a ninth, on eighth notes
    sig = [(74, -0.15), (81, 0.1), (88, 0.2)]
    for i, (m, pn) in enumerate(sig):
        b = bell(midi(m), 3.2, index=2.0 - 0.4 * i, ratio=3.5, decay=1.5 + 0.3 * i)
        S.add(b, LOCK + i * 0.25, pan=pn, gain=0.32)
        Srv.add(b, LOCK + i * 0.25, gain=0.35)
    S.add(sub_hit(55, 36.71, 3.0, 1.3, 0.12), LOCK, gain=0.9)
    # soft echo of the signature when the reflection crosses the mark
    for i, (m, pn) in enumerate(sig):
        b = bell(midi(m - 12), 2.5, index=1.0, decay=1.2)
        S.add(b, SHEEN[0] + 0.2 + i * 0.25, pan=pn, gain=0.07)
        Srv.add(b, SHEEN[0] + 0.2 + i * 0.25, gain=0.09)
    sw = filt(noise(1.05), 'highpass', 5000) * np.sin(np.pi * np.linspace(0, 1, int(1.05 * SR))) ** 2
    pan_sweep = np.linspace(-1, 1, len(sw))
    S.add(np.stack([sw * np.cos((pan_sweep + 1) * np.pi / 4), sw * np.sin((pan_sweep + 1) * np.pi / 4)], 1) * 1.4, SHEEN[0], gain=0.05)

    reveal = pad([50, 54, 57, 61, 64], 7.7, attack=2.0, release=2.2, bright=3.0)
    M.add(reveal, 28.2, gain=0.13)
    Mrv.add(reveal, 28.2, gain=0.16)
    M.add(pad([26, 38], 5.6, attack=0.05, release=2.5, bright=2.0), LOCK, gain=0.22)

    # ---- reverb returns
    ir_m = reverb_ir(3.2, bright=5500, seed=1)
    ir_s = reverb_ir(2.6, bright=8000, seed=2)
    music = M.x + reverb(Mrv.x, ir_m, 1.0)
    sfx = S.x + reverb(Srv.x, ir_s, 1.0)
    # clean edges: the film starts and ends in silence so it loops
    fade = np.ones(N)
    fade[-int(0.12 * SR):] = np.linspace(1, 0, int(0.12 * SR)) ** 2
    end = np.clip((35.95 - np.arange(N) / SR) / 1.4, 0, 1) ** 1.5
    end[: int(34.0 * SR)] = 1
    music *= (fade * end)[:, None]
    sfx *= fade[:, None]
    for x in (music, sfx):
        x -= filt(x, 'lowpass', 18)   # remove DC / subsonic rumble below 18 Hz
    music = translate(music, 1.0) * 1.9
    sfx = translate(sfx, 0.8)
    return music, sfx


def translate(x, amount):
    """Phone-speaker translation: trim the deep sub and add its harmonics in the
    120–700 Hz band, so impacts still read on speakers that cannot reproduce 40 Hz."""
    low = filt(x, 'lowpass', 110, 4)
    peak = max(np.max(np.abs(low)), 1e-9)
    harm = np.tanh(low / peak * 4.0) * peak
    harm = filt(harm, 'bandpass', [130, 700], 2)
    return x - 0.35 * amount * low + 0.9 * amount * harm


def write(path, x):
    peak = np.max(np.abs(x))
    wavfile.write(path, SR, (np.clip(x, -1, 1) * (2 ** 31 - 1)).astype(np.int32))
    return peak


if __name__ == '__main__':
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    music, sfx = build()
    norm = 0.5 / max(np.max(np.abs(music + sfx)), 1e-9)   # unmastered stems share one gain
    print('music peak', write(os.path.join(out, 'music.wav'), music * norm))
    print('sfx peak', write(os.path.join(out, 'sfx.wav'), sfx * norm))
