"""Genre soundtrack synth for the vertical reels (numpy only).

Every reel has its own genre, so no two share a sound:

  them-vs-us      8-bit chiptune (150 BPM): square leads, triangle bass, crushed noise drums
  rate-this       cinematic trailer (60 BPM): braams, taiko, strings, piano
  money-signs     dark trap (150 BPM half-time): 808 glides, hat rolls, bell melody, sirens
  glow-up         retro MIDI website tune (90 BPM) -> future bass drop (150 BPM half-time)
  process         lo-fi chillhop (90 BPM, swung): Rhodes, soft drums, vinyl crackle, tape wobble
  worldwide       Arabic (120 BPM): darbuka maqsum, riq, oud and qanun in maqam Hijaz
  whats-included  funk-pop (120 BPM): slap bass, clav stabs, brass, marimba, shakers

Scene cuts are cued as one-shot effects in each reel's cue list (CUES at the bottom).
Usage: python3 soundtrack.py <reel> [out.wav]
"""
import sys
import wave

import numpy as np

SR = 44100
rng = np.random.default_rng(7)


# ---------------------------------------------------------------- basics
def T(sec):
    return np.arange(max(1, int(sec * SR))) / SR


def lowpass(x, cutoff, order=4):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / np.sqrt(1 + (f / cutoff) ** order)
    return np.fft.irfft(X, len(x))


def highpass(x, cutoff):
    return x - lowpass(x, cutoff)


def bandpass(x, lo, hi):
    return highpass(lowpass(x, hi), lo)


def expenv(n, a=0.002, d=0.2):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)


def adsr(n, a=0.01, d=0.1, s=0.7, r=0.1):
    t = np.arange(n) / SR
    dur = n / SR
    e = np.where(t < a, t / max(a, 1e-4), s + (1 - s) * np.exp(-(t - a) / max(d, 1e-4)))
    rel = np.clip((dur - t) / max(r, 1e-4), 0, 1)
    return e * rel


def note(m):
    return 440 * 2 ** ((m - 69) / 12)


def sine(f, t):
    return np.sin(2 * np.pi * f * t)


def saw(f, t, ph=0.0):
    return 2 * ((t * f + ph) % 1) - 1


def square(f, t, duty=0.5):
    return np.where((t * f) % 1 < duty, 1.0, -1.0)


def tri(f, t):
    return 2 * np.abs(2 * ((t * f) % 1) - 1) - 1


def glide_phase(f0, f1, t, k=30):
    """Phase for a pitch gliding from f0 to f1 (exponential approach)."""
    f = f1 + (f0 - f1) * np.exp(-t * k)
    return 2 * np.pi * np.cumsum(f) / SR


def bitcrush(x, bits=4, down=4):
    q = 2 ** (bits - 1)
    y = np.round(x * q) / q
    return np.repeat(y[::down], down)[: len(x)]


def karplus(freq, dur, bright=0.5, decay=0.996):
    """Plucked string (Karplus-Strong), vectorised one period at a time."""
    n = int(dur * SR)
    N = max(2, int(round(SR / freq)))
    out = np.zeros(n + N + 2)
    exc = rng.uniform(-1, 1, N + 1)
    smooth = np.convolve(exc, np.ones(5) / 5, 'same')
    out[: N + 1] = bright * exc + (1 - bright) * smooth
    s = N + 1
    while s < len(out):
        e = min(s + N, len(out))
        out[s:e] = decay * 0.5 * (out[s - N:e - N] + out[s - N - 1:e - N - 1])
        s = e
    y = out[:n]
    return y / (np.max(np.abs(y)) + 1e-9)


def reverb_ir(rt=1.8, damp=6000, stereo_seed=0):
    t = T(rt * 1.2)
    r = np.random.default_rng(stereo_seed)
    ir = r.standard_normal(len(t)) * np.exp(-6.9 * t / rt)
    ir = lowpass(ir, damp, 2)
    ir[: int(0.012 * SR)] *= np.linspace(0, 1, int(0.012 * SR))   # pre-delay softening
    return ir / np.sqrt(np.sum(ir ** 2))


def convolve(x, ir):
    n = len(x) + len(ir) - 1
    size = 1 << (n - 1).bit_length()
    y = np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(ir, size), size)
    return y[: len(x)]


# ---------------------------------------------------------------- mixer
class Mix:
    def __init__(self, dur):
        self.n = int(dur * SR)
        self.dur = dur
        self.bus = {k: [np.zeros(self.n), np.zeros(self.n)] for k in ('drums', 'music', 'fx', 'verb')}
        self.sc = np.ones(self.n)

    def add(self, sig, at, gain=1.0, pan=0.0, bus='music', verb=0.0):
        i = int(at * SR)
        if i >= self.n or i < 0 or gain == 0:
            return
        sig = sig[: self.n - i] * gain
        gl, gr = np.sqrt(1 - pan), np.sqrt(1 + pan)
        L, R = self.bus[bus]
        L[i:i + len(sig)] += sig * gl
        R[i:i + len(sig)] += sig * gr
        if verb:
            VL, VR = self.bus['verb']
            VL[i:i + len(sig)] += sig * gl * verb
            VR[i:i + len(sig)] += sig * gr * verb

    def duck(self, at, depth=0.7, release=0.12, length=0.5):
        i = int(at * SR)
        k = min(int(length * SR), self.n - i)
        if k > 0:
            self.sc[i:i + k] = np.minimum(self.sc[i:i + k], 1 - depth * np.exp(-np.arange(k) / SR / release))

    def render(self, rt=1.8, damp=6000, drive=1.6, wobble=0.0, master_lp=None, crackle=0.0):
        L = self.bus['drums'][0] + self.bus['music'][0] * self.sc + self.bus['fx'][0]
        R = self.bus['drums'][1] + self.bus['music'][1] * self.sc + self.bus['fx'][1]
        L = L + convolve(self.bus['verb'][0], reverb_ir(rt, damp, 1)) * 0.9
        R = R + convolve(self.bus['verb'][1], reverb_ir(rt, damp, 2)) * 0.9
        if wobble:                                    # tape wow: slowly warp time
            t = np.arange(self.n) / SR
            warp = t + wobble * np.sin(2 * np.pi * 0.55 * t) + wobble * 0.4 * np.sin(2 * np.pi * 1.7 * t)
            L = np.interp(warp, t, L)
            R = np.interp(warp, t, R)
        if crackle:                                   # vinyl crackle + hiss
            hiss = highpass(rng.standard_normal(self.n), 3000) * 0.02
            pops = np.zeros(self.n)
            idx = rng.integers(0, self.n, int(self.dur * 9))
            pops[idx] = rng.uniform(0.3, 1, len(idx)) * rng.choice([-1, 1], len(idx))
            pops = lowpass(pops, 5000)
            L += (hiss + pops) * crackle
            R += (hiss * 0.9 + np.roll(pops, 37)) * crackle
        if master_lp:
            L, R = lowpass(L, master_lp, 2), lowpass(R, master_lp, 2)
        mix = np.stack([L, R], axis=1)
        mix /= np.percentile(np.abs(mix), 99.7) + 1e-9    # loudness from the body, not one stray spike
        mix = np.tanh(mix * drive * 0.8) / np.tanh(drive * 0.8) * 0.9
        fade = np.ones(self.n)
        fs = int((self.dur - 0.5) * SR)
        fade[fs:] = np.linspace(1, 0, self.n - fs)
        return mix * fade[:, None]


# ---------------------------------------------------------------- drums
def kick_edm(big=False):
    t = T(0.9 if big else 0.45)
    ph = glide_phase(155, 45, t, 28)
    s = np.sin(ph) * np.exp(-t * (3.5 if big else 7))
    return np.tanh((s + rng.standard_normal(len(t)) * np.exp(-t * 400) * 0.3) * 1.6)


def kick_soft():
    t = T(0.4)
    return lowpass(np.sin(glide_phase(95, 52, t, 35)) * np.exp(-t * 9), 900)


def kick_tight():
    t = T(0.3)
    s = np.sin(glide_phase(180, 58, t, 45)) * np.exp(-t * 11)
    return np.tanh((s + highpass(rng.standard_normal(len(t)), 3000) * np.exp(-t * 500) * 0.4) * 1.8)


def clap(size=1.0):
    t = T(0.35)
    n = bandpass(rng.standard_normal(len(t)), 900, 2600)
    e = sum(np.exp(-np.maximum(0, t - d) * 60) * (t >= d) for d in (0, 0.011, 0.022)) + np.exp(-np.maximum(0, t - 0.03) * 16 / size) * (t > 0.03)
    return n * e * 0.6


def hat(open_=False, tone=7000):
    t = T(0.3 if open_ else 0.06)
    return highpass(rng.standard_normal(len(t)), tone) * np.exp(-t * (12 if open_ else 70)) * 0.6


def snare_trap():
    t = T(0.3)
    n = bandpass(rng.standard_normal(len(t)), 1500, 9000) * np.exp(-t * 16)
    return (n + np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30) * 0.7) * 0.8


def snare_lofi():
    t = T(0.25)
    n = lowpass(bandpass(rng.standard_normal(len(t)), 600, 5000), 3800) * np.exp(-t * 20)
    return (n + np.sin(2 * np.pi * 210 * t) * np.exp(-t * 35) * 0.5) * 0.7


def snare_big():
    t = T(0.6)
    n = bandpass(rng.standard_normal(len(t)), 700, 8000) * np.exp(-t * 9)
    return np.tanh((n + np.sin(glide_phase(260, 170, t, 20)) * np.exp(-t * 18)) * 1.3) * 0.8


def eight08(f0, dur, glide_to=None):
    t = T(dur)
    f1 = glide_to or f0
    ph = glide_phase(f0 * 1.9, f0, t, 60)
    if glide_to:                                  # slide into the next note in the last 30%
        g = np.clip((t - dur * 0.7) / (dur * 0.3), 0, 1)
        f = f0 + (f1 - f0) * g * g
        ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * np.minimum(1, t / 0.004) * np.exp(-t / max(dur * 0.9, 0.2))
    return np.tanh(s * 2.2) * 0.9


def taiko(big=False):
    t = T(2.2 if big else 1.2)
    s = np.sin(glide_phase(78, 44, t, 9)) * np.exp(-t * (1.6 if big else 3))
    n = lowpass(rng.standard_normal(len(t)), 500) * np.exp(-t * 18)
    return np.tanh((s + n * 0.8) * 1.5)


def tom(freq):
    t = T(0.5)
    return np.sin(glide_phase(freq * 1.4, freq, t, 25)) * np.exp(-t * 7) + lowpass(rng.standard_normal(len(t)), 800) * np.exp(-t * 30) * 0.3


def chip_kick():
    t = T(0.18)
    return bitcrush(np.sign(np.sin(glide_phase(160, 38, t, 30))) * np.exp(-t * 18), 3, 3) * 0.8


def chip_snare():
    t = T(0.16)
    return bitcrush(rng.uniform(-1, 1, len(t)) * np.exp(-t * 22) + square(180, t) * np.exp(-t * 60) * 0.4, 3, 6) * 0.6


def chip_hat():
    t = T(0.05)
    return bitcrush(highpass(rng.uniform(-1, 1, len(t)), 6000) * np.exp(-t * 90), 3, 2) * 0.4


def doum():
    t = T(0.45)
    return np.sin(glide_phase(130, 88, t, 25)) * np.exp(-t * 6) + lowpass(rng.standard_normal(len(t)), 500) * np.exp(-t * 25) * 0.4


def tek(soft=False):
    t = T(0.12)
    n = bandpass(rng.standard_normal(len(t)), 2500, 7500) * np.exp(-t * (70 if not soft else 90))
    return (n + np.sin(2 * np.pi * 880 * t) * np.exp(-t * 60) * 0.5) * (0.45 if soft else 0.8)


def riq():
    t = T(0.14)
    e = sum(np.exp(-np.maximum(0, t - d) * 80) * (t >= d) for d in (0, 0.018, 0.034))
    return highpass(rng.standard_normal(len(t)), 6500) * e * 0.35


def shaker():
    t = T(0.09)
    return highpass(rng.standard_normal(len(t)), 5000) * np.minimum(1, t / 0.02) * np.exp(-t * 40) * 0.35


def cowbell():
    t = T(0.3)
    return bandpass(square(545, t) + square(815, t), 400, 3000) * np.exp(-t * 14) * 0.35


def crash():
    t = T(2.5)
    return highpass(rng.standard_normal(len(t)), 4000) * np.exp(-t * 1.6) * 0.5


# ---------------------------------------------------------------- instruments
def pluck(f, dur=0.22):
    t = T(dur)
    return lowpass(saw(f, t) * 0.5 + sine(f * 2, t) * 0.3, 3500) * expenv(len(t), 0.002, 0.09)


def pad(freqs, dur, cutoff=1400, attack=0.05):
    t = T(dur)
    s = sum(saw(f * d, t, rng.random()) for f in freqs for d in (0.996, 1.004)) / (len(freqs) * 2)
    return lowpass(s, cutoff) * adsr(len(t), attack, 1, 1, 0.08)


def supersaw(freqs, dur, cutoff=5500):
    t = T(dur)
    det = (-0.011, -0.006, -0.0025, 0, 0.0025, 0.006, 0.011)
    s = sum(saw(f * (1 + d), t, rng.random()) for f in freqs for d in det) / (len(freqs) * 3)
    return lowpass(s, cutoff) * adsr(len(t), 0.01, 0.3, 0.85, 0.06)


def rhodes(f, dur):
    t = T(dur)
    s = sine(f, t) + 0.25 * sine(2 * f, t) * np.exp(-t * 3) + 0.12 * sine(f * 7.1, t) * np.exp(-t * 12)
    return s * adsr(len(t), 0.004, dur * 0.5, 0.35, 0.15) * (1 + 0.18 * sine(4.5, t))


def piano(f, dur):
    t = T(dur)
    s = sum(sine(k * f * (1 + 0.0004 * k * k), t) * np.exp(-t * (0.9 + k * 0.7)) / k for k in range(1, 6))
    return s * np.minimum(1, t / 0.003) * np.minimum(1, (dur - t) / 0.05 + 0.001)


def marimba(f, dur=0.5):
    t = T(dur)
    return (sine(f, t) * np.exp(-t * 7) + 0.35 * sine(f * 4, t) * np.exp(-t * 20)) * np.minimum(1, t / 0.002)


def bell(f, dur=1.2):
    t = T(dur)
    s = sine(f, t) + 0.5 * sine(f * 2.01, t) * np.exp(-t * 2) + 0.25 * sine(f * 3.02, t) * np.exp(-t * 4)
    return s * expenv(len(t), 0.002, dur * 0.35)


def organ(f, dur):
    t = T(dur)
    s = sum(w * sine(f * h, t) for h, w in ((1, 1), (2, 0.6), (3, 0.4), (4, 0.3), (6, 0.15), (8, 0.1)))
    return s / 2.5 * adsr(len(t), 0.01, 0.1, 0.9, 0.04)


def chip(f, dur, duty=0.25, vib=True):
    t = T(dur)
    f = f * (1 + (0.012 * np.sin(2 * np.pi * 6 * t) * np.clip((t - 0.12) / 0.1, 0, 1) if vib else 0))
    ph = np.cumsum(f) / SR
    s = np.where(ph % 1 < duty, 1.0, -1.0)
    return bitcrush(s * adsr(len(t), 0.002, 0.08, 0.7, 0.03), 4, 2) * 0.5


def chip_tri(f, dur):
    t = T(dur)
    return bitcrush(tri(f, t) * adsr(len(t), 0.002, 0.05, 0.9, 0.02), 4, 2) * 0.8


def braam(root, dur=2.5):
    t = T(dur)
    freqs = [note(root - 24), note(root - 12), note(root - 5)]
    s = sum(saw(f * d, t, rng.random()) for f in freqs for d in (0.995, 1.0, 1.006)) / 6
    dark, bright = lowpass(s, 260), lowpass(s, 2400)
    k = np.clip(t / 0.25, 0, 1) * np.exp(-t * 1.2)
    y = dark * (1 - k) + bright * k
    return np.tanh(y * 2.5) * adsr(len(t), 0.03, 1.2, 0.5, 0.6)


def strings(freqs, dur, attack=0.5):
    t = T(dur)
    vib = 1 + 0.004 * np.sin(2 * np.pi * 5.2 * t)
    s = sum(saw(f * d, t * vib, rng.random()) for f in freqs for d in (0.997, 1.003)) / (len(freqs) * 2)
    return lowpass(s, 2200) * adsr(len(t), attack, 1, 1, 0.4)


def oud(f, dur):
    s = karplus(f, dur, bright=0.75, decay=0.995)
    return lowpass(s, 3200) * np.minimum(1, (dur - T(dur)) / 0.05 + 0.001)


def qanun(f, dur):
    return karplus(f, dur, bright=0.95, decay=0.997) * 0.8


def slap(f, dur):
    t = T(dur)
    s = karplus(f, dur, bright=0.9, decay=0.992) + sine(f, t) * np.exp(-t * 6) * 0.8
    return np.tanh(s * 1.8) * adsr(len(t), 0.001, 0.2, 0.6, 0.03) * 0.8


def clav(freqs, dur=0.18):
    t = T(dur)
    s = sum(square(f, t, 0.3) for f in freqs) / len(freqs)
    return bandpass(s, 300, 3500) * expenv(len(t), 0.001, 0.07) * 0.6


def brass(freqs, dur=0.3):
    t = T(dur)
    s = sum(saw(f * d, t, rng.random()) for f in freqs for d in (0.996, 1.004)) / (len(freqs) * 2)
    return lowpass(s, 3200) * adsr(len(t), 0.02, 0.1, 0.8, 0.08) * 0.9


def vox(f, dur=0.2):
    """Chopped 'ah' vocal: a saw through three vowel formants."""
    t = T(dur)
    s = saw(f, t) + 0.5 * saw(f * 1.003, t)
    y = bandpass(s, 700, 900) + 0.7 * bandpass(s, 1080, 1260) + 0.35 * bandpass(s, 2700, 3000)
    return y * adsr(len(t), 0.01, 0.08, 0.7, 0.04) * 1.6


# ---------------------------------------------------------------- one-shot effects
def boom():
    t = T(1.8)
    s = np.sin(glide_phase(98, 38, t, 6)) * np.exp(-t * 2.2)
    return np.tanh((s + lowpass(rng.standard_normal(len(t)), 900) * np.exp(-t * 5) * 0.6) * 1.4)


def whoosh(dur=0.5, up=True):
    t = T(dur)
    n = rng.standard_normal(len(t))
    out = np.zeros_like(n)
    for k in range(24):
        a, b = k * len(t) // 24, (k + 1) * len(t) // 24
        out[a:b] = lowpass(n, 400 * (20 ** (k / 24 if up else 1 - k / 24)))[a:b]
    return out * np.sin(np.pi * t / dur) ** 2 * 0.9


def riser(dur):
    t = T(dur)
    f = 180 * (8 ** (t / dur))
    return (saw(1, np.cumsum(f) / SR) * 0.25 + highpass(rng.standard_normal(len(t)), 2000) * 0.5) * (t / dur) ** 2.2


def subdrop(dur=1.5):
    t = T(dur)
    return np.sin(glide_phase(90, 28, t, 2.2)) * np.exp(-t * 1.6)


def beep(f=880, dur=0.16):
    t = T(dur)
    return sine(f, t) * expenv(len(t), 0.003, dur / 2.5)


def tick(f=3200):
    t = T(0.03)
    return sine(f, t) * np.exp(-t * 250) * 0.5 + highpass(rng.standard_normal(len(t)), 5000) * np.exp(-t * 300) * 0.3


def glitch():
    t = T(0.18)
    sq = np.sign(np.sin(2 * np.pi * (180 + 900 * rng.random()) * t))
    bits = np.round(rng.standard_normal(len(t)) * 3) / 3
    return (sq * 0.4 + bits * 0.3) * (np.floor(t * 90) % 2 == 0) * np.exp(-t * 12)


def siren(dur=0.9):
    t = T(dur)
    f = np.where((t * 4) % 1 < 0.5, 960, 740)
    return lowpass(square(1, np.cumsum(f) / SR, 0.5), 2500) * adsr(len(t), 0.01, 0.2, 0.8, 0.1) * 0.35


def register():
    """Ka-ching: drawer rattle + bright bell."""
    t = T(0.25)
    rattle = bandpass(rng.standard_normal(len(t)), 1500, 6000) * np.exp(-t * 25) * 0.5
    y = np.zeros(int(0.9 * SR))
    y[: len(rattle)] += rattle
    b = bell(2637, 0.8) * 0.6 + bell(3520, 0.8) * 0.4
    y[int(0.07 * SR):int(0.07 * SR) + len(b)] += b[: len(y) - int(0.07 * SR)]
    return y


def coin():
    t1, t2 = T(0.07), T(0.35)
    return bitcrush(np.concatenate([square(988, t1, 0.5) * 0.5, square(1319, t2, 0.5) * 0.5 * np.exp(-t2 * 8)]), 4, 2)


def chip_wrong():
    t = T(0.45)
    return bitcrush(np.sign(np.sin(glide_phase(420, 70, t, 5))) * adsr(len(t), 0.005, 0.2, 0.7, 0.05) * 0.5, 4, 3)


def chip_boom():
    t = T(0.6)
    return bitcrush(rng.uniform(-1, 1, len(t)) * np.exp(-t * 7) + np.sign(np.sin(glide_phase(200, 30, t, 8))) * np.exp(-t * 6) * 0.6, 3, 8) * 0.8


def chip_sweep(dur=0.35):
    t = T(dur)
    return bitcrush(np.sign(np.sin(glide_phase(200, 1600, t, 4))) * np.exp(-t * 4) * 0.35, 4, 2)


def powerup():
    seq = [note(m) for m in (62, 66, 69, 74, 78, 81, 86)]
    return np.concatenate([chip(f, 0.06, 0.5, False) for f in seq] + [chip(note(86), 0.4, 0.5, True)])


def error_ding():
    t = T(0.6)
    return sum(sine(f, t) for f in (523.3, 659.3, 784)) / 3 * expenv(len(t), 0.003, 0.18) * 0.8


def scratch(dur=0.35):
    t = T(dur)
    f = 900 * np.exp(-t * 6) + 80
    return lowpass(saw(1, np.cumsum(f) / SR), 2500) * np.sin(np.pi * t / dur) * 0.6


def crt_off():
    t = T(0.5)
    return (sine(15000, t) * 0.06 * np.exp(-t * 6) + np.sin(glide_phase(300, 30, t, 10)) * np.exp(-t * 8) * 0.8
            + highpass(rng.standard_normal(len(t)), 2000) * np.exp(-t * 30) * 0.3)


def sparkle():
    y = np.zeros(int(1.0 * SR))
    for i, m in enumerate((88, 91, 95, 100, 103)):
        b = bell(note(m), 0.6) * 0.3
        s = int(i * 0.05 * SR)
        y[s:s + len(b)] += b[: len(y) - s]
    return y


def ring():
    """Phone ringback: two short trills."""
    y = np.zeros(int(1.2 * SR))
    for s0 in (0, 0.45):
        t = T(0.3)
        tone = (sine(440, t) + sine(480, t)) * 0.3 * (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 20 * t)))
        s = int(s0 * SR)
        y[s:s + len(t)] += tone * adsr(len(t), 0.01, 0.1, 1, 0.02)
    return y


def typing(dur=1.2, rate=11):
    y = np.zeros(int(dur * SR))
    k = int(dur * rate)
    for i in range(k):
        t = T(0.02)
        c = bandpass(rng.standard_normal(len(t)), 1500, 6000) * np.exp(-t * 300) * rng.uniform(0.4, 0.9)
        s = int((i / rate + rng.uniform(0, 0.03)) * SR)
        y[s:s + len(c)] += c[: max(0, len(y) - s)]
    return y


def page_flip():
    t = T(0.35)
    return bandpass(rng.standard_normal(len(t)), 800, 5000) * np.sin(np.pi * t / 0.35) ** 3 * 0.5


def chime(notes=(76, 72, 67)):
    """Airport ding-dong."""
    y = np.zeros(int((0.45 * len(notes) + 1.4) * SR))
    for i, m in enumerate(notes):
        b = bell(note(m), 1.6) * 0.55 + sine(note(m) / 2, T(1.6)) * expenv(int(1.6 * SR), 0.005, 0.5) * 0.2
        s = int(i * 0.45 * SR)
        y[s:s + len(b)] += b[: len(y) - s]
    return y


def flaps(dur=0.5, rate=40):
    y = np.zeros(int(dur * SR))
    for i in range(int(dur * rate)):
        t = T(0.012)
        c = bandpass(rng.standard_normal(len(t)), 2000, 7000) * np.exp(-t * 500) * (1 - i / (dur * rate)) * 0.8
        s = int(i / rate * SR)
        y[s:s + len(c)] += c[: max(0, len(y) - s)]
    return y


def pop(f=900):
    t = T(0.08)
    return np.sin(glide_phase(f, f * 2.4, t, 40)) * np.exp(-t * 45) * 0.8


def party_popper():
    t = T(0.6)
    bang = highpass(rng.standard_normal(len(t)), 800) * np.exp(-t * 30)
    return bang + sparkle()[: len(t)] * 0.8


def snare_roll(dur=0.9):
    y = np.zeros(int(dur * SR))
    tt = 0.0
    while tt < dur:
        rate = 10 + 30 * tt / dur
        s = snare_lofi() * (0.3 + 0.7 * tt / dur)
        i = int(tt * SR)
        y[i:i + len(s)] += s[: max(0, len(y) - i)]
        tt += 1 / rate
    return y


def thud():
    t = T(0.5)
    return np.sin(glide_phase(120, 50, t, 20)) * np.exp(-t * 10) + lowpass(rng.standard_normal(len(t)), 700) * np.exp(-t * 30) * 0.5


def kazoo_down():
    t = T(0.5)
    f = 420 * np.exp(-t * 1.6)
    return bandpass(saw(1, np.cumsum(f) / SR), 300, 2500) * adsr(len(t), 0.02, 0.2, 0.8, 0.08) * 0.5


def dice():
    y = np.zeros(int(0.6 * SR))
    for i, s0 in enumerate((0, 0.09, 0.17, 0.23, 0.28, 0.32)):
        t = T(0.03)
        c = bandpass(rng.standard_normal(len(t)), 1200, 5000) * np.exp(-t * 200) * (1 - i * 0.12)
        s = int(s0 * SR)
        y[s:s + len(c)] += c
    return y


SFX = {
    'boom': boom, 'kick': kick_edm, 'kick_big': lambda: kick_edm(True), 'whoosh': whoosh, 'whoosh_down': lambda d=0.5: whoosh(d, False),
    'riser': riser, 'subdrop': subdrop, 'crash': crash, 'beep': beep, 'tick': tick, 'glitch': glitch, 'siren': siren,
    'register': register, 'coin': coin, 'chip_wrong': chip_wrong, 'chip_boom': chip_boom, 'chip_sweep': chip_sweep,
    'powerup': powerup, 'error_ding': error_ding, 'scratch': scratch, 'crt_off': crt_off, 'sparkle': sparkle,
    'ring': ring, 'typing': typing, 'page_flip': page_flip, 'chime': chime, 'flaps': flaps, 'pop': pop,
    'party_popper': party_popper, 'snare_roll': snare_roll, 'thud': thud, 'kazoo_down': kazoo_down, 'dice': dice,
    'taiko': taiko, 'taiko_big': lambda: taiko(True), 'braam': braam, 'bell': bell, 'piano': piano, 'clap': clap,
    'snare_big': snare_big, 'doum': doum,
}


def sfx(mix, events):
    for ev in events:
        at, name = ev[0], ev[1]
        gain = ev[2] if len(ev) > 2 else 0.6
        args = ev[3] if len(ev) > 3 else ()
        verb = ev[4] if len(ev) > 4 else 0.15
        if not isinstance(args, tuple):
            args = (args,)
        mix.add(SFX[name](*args), at, gain, pan=float(rng.uniform(-0.25, 0.25)), bus='fx', verb=verb)


def steps(start, end, step):
    return np.arange(start, end - 1e-6, step)


# ================================================================ styles
def style_chiptune(mix, c):
    """8-bit arcade. D minor: Dm Bb C A, 150 BPM, lead melody + 32nd arps + triangle bass."""
    beat = 60 / 150
    drop, end = c['drop'], c['end']
    # pre-drop: pulsing triangle bass + ominous low square
    for tb in steps(0, 2.4, beat / 2):
        mix.add(chip_tri(note(38), beat * 0.4), tb, 0.35)
    for tb in steps(2.45, drop - 0.12, beat / 4):             # VS: rising arp
        k = (tb - 2.45) / (drop - 2.45)
        mix.add(chip(note(62 + int(k * 24)), beat / 4 * 0.9, 0.125, False), tb, 0.3)
    prog = [(50, [62, 65, 69]), (46, [58, 62, 65]), (48, [60, 64, 67]), (45, [61, 64, 69])]
    melody = [  # (beat offset in bar, length in beats, scale-degree semitones above chord root) per bar
        [(0, 1, 12), (1, .5, 15), (1.5, .5, 17), (2, 1, 19), (3, .5, 17), (3.5, .5, 15)],
        [(0, 1.5, 17), (1.5, .5, 15), (2, 1, 12), (3, 1, 10)],
        [(0, .5, 12), (.5, .5, 14), (1, 1, 16), (2, .5, 19), (2.5, .5, 16), (3, 1, 14)],
        [(0, 2, 16), (2, 1, 19), (3, 1, 21)],
    ]
    bar = 4 * beat
    for k, bt in enumerate(steps(drop, end, bar)):
        root, chord = prog[k % 4]
        for j in range(8):                                       # bass: root / octave 8ths
            mix.add(chip_tri(note(root - 12 + (12 if j % 2 else 0)), beat / 2 * 0.8), bt + j * beat / 2, 0.5)
        for j in range(16 * 2):                                  # 32nd-note arps
            mix.add(chip(note(chord[j % 3] + 12), beat / 8 * 0.9, 0.125, False), bt + j * beat / 8, 0.07, pan=0.3)
        if bt < 19.0 or bt >= 21.0:                              # melody rests during the scoreboard
            for off, ln, deg in melody[k % 4]:
                mix.add(chip(note(root + deg), ln * beat * 0.92, 0.25), bt + off * beat, 0.3, pan=-0.2)
        for j in range(4):
            tb = bt + j * beat
            mix.add(chip_kick(), tb, 0.9 if j in (0, 2) else 0.0, bus='drums')
            if j in (1, 3):
                mix.add(chip_snare(), tb, 0.7, bus='drums')
            mix.add(chip_hat(), tb + beat / 2, 0.5, bus='drums')
        mix.add(chip_kick(), bt + 2.5 * beat, 0.6, bus='drums')
    return dict(rt=0.6, damp=5000, drive=1.3)


def style_cinematic(mix, c):
    """Trailer score in A minor, 60 BPM: taiko ostinato, strings, piano motif, braams on cuts."""
    drop, end = c['drop'], c['end']
    for i, tb in enumerate(steps(0.9, 1.95, 0.1)):              # hook: rising piano run under the 1-10 bar
        mix.add(piano(note(69 + (0, 2, 3, 5, 7, 8, 11, 12, 14, 15)[i % 10]), 0.9), tb, 0.35, verb=0.5)
    mix.add(strings([note(57), note(64)], drop, attack=1.2), 0, 0.35, verb=0.5)
    chords = [[57, 60, 64], [53, 57, 60], [48, 55, 64], [55, 59, 62]]   # Am F C G
    motif = [76, 72, 71, 72, 74, 72, 69, 67]
    for k, bt in enumerate(steps(drop, end, 2.0)):
        ch = chords[k % 4]
        mix.add(strings([note(m) for m in ch] + [note(ch[0] - 12)], 2.1, attack=0.25), bt, 0.3, verb=0.6)
        mix.add(piano(note(motif[k % 8]), 1.9), bt, 0.28, pan=0.2, verb=0.6)
    for bt in steps(drop, 19.0, 1.0):                             # taiko: heavy on 1, light on the "and"
        mix.add(taiko(), bt, 0.55, bus='drums', verb=0.35)
        mix.add(tom(110), bt + 0.5, 0.35, bus='drums', verb=0.3)
        mix.add(tom(90), bt + 0.75, 0.25, bus='drums', verb=0.3)
    for bt in steps(12, 16, 0.25):                                # spiccato pulse over the devices
        mix.add(pluck(note(57 if int((bt - 12) * 4) % 2 == 0 else 64), 0.2), bt, 0.18, verb=0.3)
    for bt in steps(16, 18.9, 0.125):                             # taiko roll into "Built by"
        mix.add(tom(140), bt, 0.12 + 0.3 * (bt - 16) / 3, bus='drums', verb=0.3)
    for bt in steps(19.0, end, 2.0):
        mix.add(taiko(True), bt, 0.5, bus='drums', verb=0.4)
    return dict(rt=3.2, damp=5000, drive=1.4)


def style_trap(mix, c):
    """Dark trap, 150 BPM half-time. Am F Dm E, then C G Am F after the fix."""
    beat = 60 / 150
    drop, end, fix = c['drop'], c['end'], c['fix']
    s16 = beat / 4
    bar = 4 * beat
    for i, tb in enumerate(steps(0, drop - 0.1, beat / 2)):       # hook: dark bell arp
        mix.add(bell(note((69, 72, 76, 72)[i % 4]), 0.9), tb, 0.18, verb=0.5)
    dark = [(45, [57, 60, 64]), (41, [53, 57, 60]), (38, [50, 53, 57]), (40, [52, 56, 59])]
    bright = [(48, [60, 64, 67]), (43, [55, 59, 62]), (45, [57, 60, 64]), (41, [53, 57, 60])]
    bells = [0, 12, 7, 3, 0, 7, 12, 10]
    for k, bt in enumerate(steps(drop, end, bar)):
        after = bt >= fix
        if 15.0 <= bt < fix:
            continue                                              # the breakdown before "we fix all 3"
        root, ch = (bright if after else dark)[k % 4]
        nxt = (bright if after else dark)[(k + 1) % 4][0]
        mix.add(eight08(note(root - 12), bar * 0.95, glide_to=note(nxt - 12) if k % 2 else None), bt, 0.45, bus='drums')
        for st in (0, 6, 10):
            mix.add(kick_tight(), bt + st * s16, 0.6, bus='drums')
        mix.duck(bt, 0.5, 0.15)
        mix.add(snare_trap(), bt + 8 * s16, 0.75, bus='drums', verb=0.15)
        for j in range(8):                                        # hats with a triplet roll at the end
            mix.add(hat(), bt + j * 2 * s16, 0.35, pan=0.2, bus='drums')
        for j in range(6):
            mix.add(hat(), bt + 13 * s16 + j * s16 / 2, 0.22, pan=0.2, bus='drums')
        mix.add(pad([note(m) for m in ch], bar, 900), bt, 0.16, verb=0.4)
        for j, deg in enumerate(bells):
            mix.add(bell(note(ch[0] + 12 + deg), 0.6), bt + j * beat / 2, 0.2, pan=-0.2, verb=0.4)
    for tb in steps(15.0, fix - 0.12, s16 / 2):                   # hat roll build
        mix.add(hat(), tb, 0.1 + 0.3 * (tb - 15), bus='drums')
    return dict(rt=1.6, damp=5000, drive=1.7)


def style_glowup(mix, c):
    """0-8s: cheesy 90s website MIDI in C (90 BPM, organ + square lead + tinny drums).
    8s+: future bass in F# (150 BPM half-time): supersaw chords, vocal chops, big snare."""
    drop, end = c['drop'], c['end']
    b90 = 60 / 90
    mel = [72, 76, 79, 76, 77, 74, 71, 74, 72, 76, 79, 84, 83, 79, 77, 74]
    chords90 = [[60, 64, 67], [53, 57, 60], [55, 59, 62], [60, 64, 67]]
    for k, bt in enumerate(steps(2.0, 7.0, 4 * b90)):
        mix.add(sum(organ(note(m), 4 * b90) for m in chords90[k % 4]) / 3, bt, 0.4)
    for i, tb in enumerate(steps(2.0, 7.0, b90 / 2)):
        mix.add(chip(note(mel[i % 16]), b90 / 2 * 0.85, 0.5, False) * 0.6, tb, 0.45, pan=0.1)
        if i % 4 == 0:
            mix.add(bitcrush(kick_soft(), 6, 2), tb, 0.6, bus='drums')
        if i % 4 == 2:
            mix.add(bitcrush(snare_lofi(), 5, 3), tb, 0.5, bus='drums')
        mix.add(bitcrush(hat(), 5, 2), tb, 0.2, bus='drums')
    b = 60 / 150
    bar = 4 * b
    prog = [[63, 66, 70], [59, 63, 66], [66, 70, 73], [61, 65, 68]]   # D#m B F# C#
    chops = [3, 5, 7, 10, 7, 5, 3, 0]
    for k, bt in enumerate(steps(drop, end, bar)):
        ch = prog[k % 4]
        for j in range(4):
            mix.add(supersaw([note(m) for m in ch], b * 0.95), bt + j * b, 0.5, verb=0.35)
        mix.add(eight08(note(ch[0] - 24), bar * 0.9), bt, 0.32, bus='drums')
        mix.add(kick_edm(), bt, 0.9, bus='drums')
        mix.add(kick_edm(), bt + 2.5 * b, 0.6, bus='drums')
        mix.duck(bt, 0.8, 0.18, bar / 2)
        mix.duck(bt + 2.5 * b, 0.6, 0.15)
        mix.add(snare_big(), bt + 2 * b, 0.7, bus='drums', verb=0.45)
        for j in range(16):
            mix.add(hat(tone=9000), bt + j * b / 4, 0.12 + (0.1 if j % 2 else 0), pan=0.25, bus='drums')
        if k >= 1:
            for j, deg in enumerate(chops):
                mix.add(vox(note(ch[0] + 12 + deg), b / 2 * 0.8), bt + j * b / 2, 0.28, pan=-0.15, verb=0.4)
    return dict(rt=2.2, damp=7000, drive=1.6)


def style_lofi(mix, c):
    """Lo-fi chillhop, 90 BPM swung. Fmaj9 Em7 Dm9 Cmaj9, Rhodes, soft drums, crackle and tape wow."""
    drop, end = c['drop'], c['end']
    b = 60 / 90
    bar = 4 * b
    sw = 0.62                                                     # swing ratio
    mix.add(sum(rhodes(note(m), 2.3) for m in (53, 57, 64, 67)) / 3, 0.0, 0.35, verb=0.3)
    chords = [[53, 57, 64, 67], [52, 55, 59, 62], [50, 53, 57, 64], [48, 52, 59, 62]]
    melody = [(0, 76), (1.5, 74), (2, 72), (3, 69)]
    for k, bt in enumerate(steps(drop, end, bar)):
        ch = chords[k % 4]
        for m in ch:
            mix.add(rhodes(note(m), bar * 0.95), bt + 0.02 * ch.index(m), 0.16, verb=0.3)
        mix.add(sine(note(ch[0] - 12), T(b * 1.6)) * adsr(int(b * 1.6 * SR), 0.01, 0.4, 0.6, 0.1), bt, 0.4)
        mix.add(sine(note(ch[0] - 5), T(b * 0.9)) * adsr(int(b * 0.9 * SR), 0.01, 0.3, 0.5, 0.1), bt + 2.5 * b, 0.3)
        if k % 2 == 1:
            for off, m in melody:
                mix.add(rhodes(note(m + (0 if k % 4 == 1 else -2)), b * 0.9), bt + off * b, 0.12, pan=0.2, verb=0.4)
        for j in range(4):
            tb = bt + j * b
            if j in (0, 2):
                mix.add(kick_soft(), tb, 0.8, bus='drums')
            if j == 2:
                mix.add(kick_soft(), tb + b * sw, 0.45, bus='drums')
            if j in (1, 3):
                mix.add(snare_lofi(), tb, 0.55, bus='drums', verb=0.15)
            mix.add(lowpass(hat(), 9000), tb, 0.18, pan=0.2, bus='drums')
            mix.add(lowpass(hat(), 9000), tb + b * sw, 0.12, pan=0.2, bus='drums')
            mix.duck(tb, 0.3, 0.15)
    return dict(rt=1.4, damp=4500, drive=1.3, wobble=0.0022, master_lp=7500, crackle=0.5)


def style_arabic(mix, c):
    """Maqam Hijaz on D (D Eb F# G A Bb C), 120 BPM. Darbuka maqsum, riq, oud ostinato, qanun melody."""
    drop, end = c['drop'], c['end']
    b = 0.5
    bar = 4 * b
    H = [62, 63, 66, 67, 69, 70, 72, 74, 75, 78, 79, 81]
    for i, (tb, deg) in enumerate([(0.0, 7), (0.25, 6), (0.45, 5), (0.6, 4), (0.95, 2), (1.1, 1), (1.3, 0)]):   # hook: oud flourish
        mix.add(oud(note(H[deg] - 12), 0.7), tb, 0.45, verb=0.3)
    mix.add(strings([note(50), note(57)], drop, 0.4), 0, 0.2, verb=0.4)
    oud_line = [0, 0, 4, 5, 4, 3, 2, 1]                            # bass ostinato (8ths)
    qanun_phrases = [
        [(0, 7), (.5, 6), (1, 5), (1.5, 4), (2, 5), (2.5, 4), (3, 2), (3.5, 1)],
        [(0, 0), (.5, 1), (1, 2), (1.5, 4), (2, 5), (3, 4)],
        [(0, 7), (.25, 8), (.5, 7), (1, 6), (1.5, 5), (2, 4), (2.5, 5), (3, 4), (3.5, 2)],
        [(0, 2), (.5, 1), (1, 2), (1.5, 1), (2, 0)],
    ]
    for k, bt in enumerate(steps(drop, end, bar)):
        mix.add(strings([note(50), note(57), note(62)], bar, 0.2), bt, 0.12, verb=0.4)
        for j, deg in enumerate(oud_line):
            mix.add(oud(note(H[deg] - 12), b * 0.6), bt + j * b / 2, 0.4, pan=-0.2, verb=0.2)
        if 12.0 <= bt < 16.0:
            pass
        else:
            for off, deg in qanun_phrases[k % 4]:
                mix.add(qanun(note(H[deg] + 12), 0.5), bt + off * b, 0.28, pan=0.25, verb=0.35)
        # maqsum: D T . T D . T .   (8ths)
        pat = ['D', 'T', '', 'T', 'D', '', 'T', '']
        for j, hit in enumerate(pat):
            tb = bt + j * b / 2
            if hit == 'D':
                mix.add(doum(), tb, 0.9, bus='drums')
                mix.duck(tb, 0.3, 0.1)
            elif hit == 'T':
                mix.add(tek(), tb, 0.6, bus='drums', verb=0.1)
            else:
                mix.add(tek(True), tb, 0.35, bus='drums')
        for j in range(16):
            mix.add(riq(), bt + j * b / 4, 0.25 if j % 4 else 0.45, pan=0.35, bus='drums')
    return dict(rt=1.5, damp=6000, drive=1.5)


def style_funk(mix, c):
    """Funk-pop, 120 BPM: Fmaj7 Am7 Bbmaj7 C7. Slap bass, clav, brass stabs, shakers, claps."""
    drop, end = c['drop'], c['end']
    b = 0.5
    bar = 4 * b
    for i, (tb, m) in enumerate([(0, 72), (0.5, 76), (1.0, 79), (1.25, 84)]):
        mix.add(marimba(note(m), 0.6), tb, 0.5, verb=0.2)
    prog = [(41, [65, 69, 72, 76]), (45, [64, 67, 69, 72]), (46, [65, 69, 70, 74]), (48, [64, 67, 70, 72])]
    bass = [(0, 0), (0.75, 12), (1.5, 0), (2, 7), (2.5, 10), (3, 12), (3.5, 7)]   # (beat, semitones)
    for k, bt in enumerate(steps(drop, end, bar)):
        root, ch = prog[k % 4]
        for off, st in bass:
            mix.add(slap(note(root + st), b * 0.45), bt + off * b, 0.55, bus='music')
        for off in (0.5, 1.75, 2.5, 3.75):
            mix.add(clav([note(m) for m in ch]), bt + off * b, 0.35, pan=-0.3)
        if k % 2 == 0:
            for off, m in ((0, 0), (0.5, 2), (1, 4), (1.5, 7)):
                mix.add(marimba(note(ch[0] + 12 + m), 0.5), bt + 2 * b + off * b, 0.25, pan=0.3, verb=0.2)
        for j in range(4):
            tb = bt + j * b
            if j in (0, 2):
                mix.add(kick_tight(), tb, 0.85, bus='drums')
            if j == 1:
                mix.add(kick_tight(), tb + b / 2, 0.55, bus='drums')
            if j in (1, 3):
                mix.add(clap(), tb, 0.6, bus='drums', verb=0.2)
            mix.add(hat(True), tb + b / 2, 0.22, pan=0.2, bus='drums')
            for q in range(4):
                mix.add(shaker(), tb + q * b / 4, 0.25 if q % 2 else 0.4, pan=-0.3, bus='drums')
            mix.duck(tb, 0.25, 0.1)
    for tb, ch in ((9.5, [65, 69, 72]), (10.0, [67, 71, 74]), (14.5, [65, 69, 72]), (15.0, [70, 74, 77]), (17.7, [72, 76, 79])):
        mix.add(brass([note(m) for m in ch], 0.35), tb, 0.45, verb=0.25)
    return dict(rt=1.2, damp=7000, drive=1.5)


STYLES = {'chiptune': style_chiptune, 'cinematic': style_cinematic, 'trap': style_trap, 'glowup': style_glowup,
          'lofi': style_lofi, 'arabic': style_arabic, 'funk': style_funk}


# ================================================================ cue sheets (times match each reel's HTML)
CUES = {
    'them-vs-us': {
        'style': 'chiptune', 'duration': 24, 'drop': 4.0, 'end': 23.4,
        'events': [
            (0.0, 'chip_boom', 0.8), (0.5, 'chip_boom', 0.6), (1.0, 'chip_boom', 0.6), (1.5, 'chip_boom', 0.9), (1.5, 'thud', 0.6),
            (2.45, 'chip_sweep', 0.6), (3.0, 'chip_boom', 0.9), (4.0, 'chip_boom', 0.9), (4.0, 'powerup', 0.5),
            *[(4 + 3 * i, 'chip_wrong', 0.55) for i in range(5)], *[(5 + 3 * i, 'coin', 0.6) for i in range(5)],
            *[(5 + 3 * i, 'chip_boom', 0.45) for i in range(5)], *[(6.75 + 3 * i, 'chip_sweep', 0.35) for i in range(5)],
            *[(19.25 + 0.25 * i, 'coin', 0.45) for i in range(5)], (20.5, 'powerup', 0.6), (20.5, 'chip_boom', 0.7),
            (21.0, 'chip_sweep', 0.5), (22.0, 'coin', 0.55), (23.4, 'chip_boom', 0.8),
        ],
    },
    'rate-this': {
        'style': 'cinematic', 'duration': 24, 'drop': 2.0, 'end': 23.5,
        'events': [
            (0.0, 'taiko', 0.7), (0.5, 'taiko', 0.6), (1.0, 'riser', 0.6, 0.95),
            (2.0, 'braam', 1.0, 57, 0.4), (2.0, 'taiko_big', 0.9), (2.0, 'subdrop', 0.7),
            (6.0, 'braam', 0.7, 53, 0.4), (6.0, 'whoosh', 0.35, 0.6), (9.0, 'braam', 0.7, 55, 0.4), (9.0, 'whoosh', 0.35, 0.6),
            (12.0, 'braam', 0.8, 57, 0.4), (16.0, 'taiko_big', 0.7), (16.0, 'riser', 0.6, 2.9),
            (19.0, 'braam', 1.0, 57, 0.5), (19.0, 'taiko_big', 1.0), (19.0, 'subdrop', 0.8), (19.0, 'crash', 0.4),
            *[(21.0 + 0.05 * i, 'piano', 0.25, (440 * 2 ** ((0, 2, 3, 5, 7, 8, 11, 12, 14, 15)[i] / 12), 1.2)) for i in range(10)],
            (22.25, 'taiko', 0.6), (23.5, 'braam', 0.8, 57, 0.5), (23.5, 'taiko_big', 0.8),
        ],
    },
    'money-signs': {
        'style': 'trap', 'duration': 24, 'drop': 2.5, 'end': 23.4, 'fix': 16.0,
        'events': [
            (0.0, 'siren', 0.5, 1.2), (0.0, 'boom', 0.7), (0.5, 'boom', 0.5), (1.0, 'boom', 0.5), (1.4, 'register', 0.8),
            (1.5, 'riser', 0.5, 0.95),
            *[(s, 'siren', 0.35, 0.6) for s in (2.5, 7.0, 11.5)], *[(s, 'boom', 0.5) for s in (7.0, 11.5)],
            *[(s + 2.5, 'glitch', 0.5) for s in (2.5, 7.0, 11.5)], *[(s + 4.25, 'whoosh', 0.4, 0.3) for s in (2.5, 7.0)],
            (15.0, 'riser', 0.7, 0.88), (16.0, 'boom', 1.0), (16.0, 'register', 0.9), (16.0, 'crash', 0.6), (16.5, 'kick_big', 0.8),
            *[(17.0 + 0.5 * i, 'bell', 0.35, 1318.5 * 2 ** (i * 4 / 12)) for i in range(3)], (19.5, 'whoosh', 0.45), (20.5, 'register', 0.5),
        ],
    },
    'glow-up': {
        'style': 'glowup', 'duration': 24, 'drop': 8.0, 'end': 23.4,
        'events': [
            (0.0, 'whoosh', 0.5, 0.4), (0.5, 'thud', 0.5), (1.0, 'sparkle', 0.7), (2.0, 'crt_off', 0.3),
            *[(3.5 + i, 'error_ding', 0.55) for i in range(3)], (7.0, 'scratch', 0.7), (7.3, 'crt_off', 0.6),
            (8.0, 'boom', 0.9), (8.0, 'sparkle', 0.8), (8.0, 'crash', 0.6), (8.0, 'whoosh', 0.5, 0.7),
            *[(9.0 + 1.5 * i, 'sparkle', 0.35) for i in range(3)], (14.0, 'whoosh', 0.4, 0.6), (15.3, 'whoosh_down', 0.35, 0.6),
            (17.5, 'boom', 0.8), (17.5, 'crash', 0.5), (18.0, 'snare_big', 0.6), (19.5, 'sparkle', 0.5),
        ],
    },
    'process': {
        'style': 'lofi', 'duration': 24, 'drop': 2.5, 'end': 23.4,
        'events': [
            (0.0, 'thud', 0.5), (0.5, 'thud', 0.4), (1.0, 'dice', 0.9), (2.5, 'page_flip', 0.5),
            *[(4.0 + 4 * i, 'page_flip', 0.55) for i in range(3)], (4.9, 'ring', 0.45), (6.2, 'bell', 0.35, 1046.5),
            (8.9, 'typing', 0.25, (1.4, 7)), (10.2, 'bell', 0.3, 1318.5), (12.8, 'typing', 0.45, (1.3, 12)),
            (14.2, 'bell', 0.35, 1568), (14.6, 'whoosh', 0.45, 1.0), (15.2, 'sparkle', 0.35),
            (16.0, 'bell', 0.4, 1046.5), *[(16.75 + 0.5 * i, 'bell', 0.3, 1318.5 * 2 ** (i * 2 / 12)) for i in range(3)],
            (19.5, 'page_flip', 0.4),
        ],
    },
    'worldwide': {
        'style': 'arabic', 'duration': 24, 'drop': 2.0, 'end': 23.4,
        'events': [
            (0.0, 'doum', 0.8), (0.5, 'doum', 0.6), (1.0, 'boom', 0.6), (2.0, 'chime', 0.6), (2.0, 'boom', 0.6),
            *[(t, 'flaps', 0.4) for t in (2.5, 4.35, 5.6, 6.85, 8.1, 9.35, 10.6)], *[(t - 0.6, 'whoosh', 0.3, 0.6) for t in (4.35, 5.6, 6.85, 8.1, 9.35, 10.6)],
            (12.0, 'boom', 0.6), (12.75, 'doum', 0.7), (13.5, 'doum', 0.7), (14.5, 'crash', 0.35),
            *[(16.3 + 0.125 * i, 'tick', 0.3) for i in range(16)], (18.3, 'bell', 0.4, 1760),
            (19.5, 'chime', 0.7, ((72, 76, 79, 84),)), (23.4, 'boom', 0.6),
        ],
    },
    'whats-included': {
        'style': 'funk', 'duration': 24, 'drop': 4.0, 'end': 23.4,
        'events': [
            (0.0, 'pop', 0.6), (0.5, 'pop', 0.6, 1100), (1.0, 'pop', 0.7, 1300), (2.0, 'thud', 0.8),
            (3.0, 'snare_roll', 0.6, 0.85), (4.0, 'party_popper', 0.9), (4.0, 'crash', 0.5),
            *[(4.75 + 0.5 * i, 'pop', 0.45, 700 + 60 * i) for i in range(10)],
            (13.3, 'kazoo_down', 0.6), (14.05, 'kazoo_down', 0.6), (16.5, 'snare_roll', 0.4, 1.1), (17.7, 'register', 0.6),
            (19.5, 'party_popper', 0.6),
        ],
    },
}


def build(name):
    c = CUES[name]
    mix = Mix(c['duration'])
    opts = STYLES[c['style']](mix, c)
    sfx(mix, c['events'])
    return (mix.render(**opts) * 32767).astype(np.int16)


if __name__ == '__main__':
    name = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else f'{name}-audio.wav'
    pcm = build(name)
    with wave.open(out, 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print('wrote', out)
