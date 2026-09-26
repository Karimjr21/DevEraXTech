"""Synthesises the soundtrack for hook.html: a 120 BPM track whose hits line up with the video's cuts.

0-8s   tension: clock ticks, drone, countdown beeps, glitch hits, a riser, then silence
8s     the drop: impact + full beat (kick, clap, hats, sidechained bass, chords and a pluck hook)
29s    final hit and tail

Usage: python3 make-hook-audio.py [out.wav]   (needs numpy)
"""
import sys
import wave

import numpy as np

SR = 44100
DUR = 30.0
BEAT = 0.5
DROP = 8.0
N = int(SR * DUR)
rng = np.random.default_rng(7)

L = np.zeros(N)
R = np.zeros(N)


def t_axis(sec):
    return np.arange(int(sec * SR)) / SR


def add(sig, at, gain=1.0, pan=0.0):
    """Mix a mono signal in at time `at` (seconds), pan -1..1."""
    i = int(at * SR)
    if i >= N:
        return
    sig = sig[: N - i] * gain
    L[i:i + len(sig)] += sig * np.sqrt((1 - pan) / 2) * np.sqrt(2)
    R[i:i + len(sig)] += sig * np.sqrt((1 + pan) / 2) * np.sqrt(2)


def lowpass(x, cutoff):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / np.sqrt(1 + (f / cutoff) ** 4)       # 2nd-order-ish rolloff
    return np.fft.irfft(X, len(x))


def highpass(x, cutoff):
    return x - lowpass(x, cutoff)


def env(n, a=0.002, d=0.2):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-t / d)


def note(midi):
    return 440 * 2 ** ((midi - 69) / 12)


def saw(freq, t):
    return 2 * ((t * freq) % 1) - 1


# ---------- instruments ----------
def kick(big=False):
    t = t_axis(0.9 if big else 0.45)
    f = 45 + 110 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * np.exp(-t * (3.5 if big else 7))
    click = rng.standard_normal(len(t)) * np.exp(-t * 400) * 0.3
    return np.tanh((s + click) * 1.6)


def clap():
    t = t_axis(0.3)
    n = highpass(lowpass(rng.standard_normal(len(t)), 2500), 800)
    e = np.exp(-t * 22) + 0.6 * np.exp(-np.maximum(0, t - 0.012) * 30) * (t > 0.012)
    return n * e * 0.8


def hat(open_=False):
    t = t_axis(0.25 if open_ else 0.06)
    return highpass(rng.standard_normal(len(t)), 7000) * np.exp(-t * (14 if open_ else 70)) * 0.6


def tick():
    t = t_axis(0.03)
    return np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 250) * 0.5 + highpass(rng.standard_normal(len(t)), 5000) * np.exp(-t * 300) * 0.3


def beep(freq, dur=0.16):
    t = t_axis(dur)
    return np.sin(2 * np.pi * freq * t) * env(len(t), 0.003, dur / 2.5)


def boom():
    t = t_axis(1.8)
    f = 38 + 60 * np.exp(-t * 6)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.2)
    noise = lowpass(rng.standard_normal(len(t)), 900) * np.exp(-t * 5) * 0.6
    return np.tanh((s + noise) * 1.4)


def glitch():
    t = t_axis(0.16)
    sq = np.sign(np.sin(2 * np.pi * (180 + 900 * rng.random()) * t))
    bits = np.round(rng.standard_normal(len(t)) * 3) / 3
    gate = (np.floor(t * 90) % 2 == 0)
    return (sq * 0.4 + bits * 0.3) * gate * np.exp(-t * 14)


def whoosh(dur=0.5, up=True):
    t = t_axis(dur)
    n = rng.standard_normal(len(t))
    out = np.zeros_like(n)
    # sweep a band through the noise in chunks
    chunks = 24
    for k in range(chunks):
        a, b = k * len(t) // chunks, (k + 1) * len(t) // chunks
        c = 400 * (20 ** (k / chunks if up else 1 - k / chunks))
        out[a:b] = lowpass(n, c)[a:b]
    shape = np.sin(np.pi * t / dur) ** 2
    return out * shape * 0.9


def riser(dur):
    t = t_axis(dur)
    f = 180 * (8 ** (t / dur))
    tone = saw(1, np.cumsum(f) / SR) * 0.25
    n = highpass(rng.standard_normal(len(t)), 2000) * 0.5
    return (tone + n) * (t / dur) ** 2.2


def crash():
    t = t_axis(2.5)
    return highpass(rng.standard_normal(len(t)), 4000) * np.exp(-t * 1.6) * 0.5


def pluck(freq, dur=0.22):
    t = t_axis(dur)
    s = saw(freq, t) * 0.5 + np.sin(2 * np.pi * freq * 2 * t) * 0.3
    return lowpass(s, 3500) * env(len(t), 0.002, 0.09)


def pad_chord(freqs, dur):
    t = t_axis(dur)
    s = sum(saw(f * d, t) for f in freqs for d in (0.996, 1.004)) / (len(freqs) * 2)
    return lowpass(s, 1400) * np.minimum(1, t / 0.05) * np.minimum(1, (dur - t) / 0.05)


# ---------- section A: tension (0 - 8s) ----------
t_a = t_axis(DROP)
drone = (np.sin(2 * np.pi * 55 * t_a) + 0.5 * lowpass(saw(55.3, t_a), 300)) * np.minimum(1, t_a / 0.3)
drone *= 0.18 * (0.6 + 0.4 * np.clip((t_a - 4) / 3.5, 0, 1))
drone[int(7.75 * SR):] = 0                          # the gap before the drop
add(drone, 0)

for i in range(int(7.5 / BEAT) + 1):              # clock tick on every beat
    add(tick(), i * BEAT, 0.6 if i % 2 == 0 else 0.35)
add(boom(), 0.0, 0.9)                             # STOP
add(boom(), 0.5, 0.7)                             # SCROLLING
add(whoosh(0.45), 1.1, 0.5)
for at, f in [(2.0, 880), (2.5, 880), (3.0, 880), (3.5, 1760)]:
    add(beep(f, 0.18 if at < 3.5 else 0.4), at, 0.5)
add(kick(big=True), 3.5, 0.8)
for at in (4.5, 5.0, 5.5, 6.0):
    add(glitch(), at, 0.55, pan=rng.uniform(-0.5, 0.5))
    add(kick(), at, 0.55)
add(boom(), 6.5, 1.0)                             # "you're losing customers"
add(riser(1.25), 6.5, 0.7)
add(whoosh(1.2, up=True), 6.55, 0.6)

# ---------- section B: the drop (8 - 29.5s) ----------
END = 29.0
# Am - F - C - G, one chord per bar (4 beats)
prog = [(57, [57, 60, 64]), (53, [53, 57, 60]), (48, [55, 60, 64]), (55, [55, 59, 62])]
hook = [0, 2, 1, 2, 0, 2, 1, 3]                   # index into the chord for the 8th-note pluck
add(boom(), DROP, 1.0)
add(kick(big=True), DROP, 1.0)
add(crash(), DROP, 0.8)

beats = np.arange(DROP, END, BEAT)
for bi, bt in enumerate(beats):
    add(kick(), bt, 0.95)
    if bi % 2 == 1:
        add(clap(), bt, 0.55)
    add(hat(open_=(bi % 4 == 3)), bt + BEAT / 2, 0.35, pan=0.3)
    add(hat(), bt + BEAT / 4, 0.12, pan=-0.3)

# sidechain gain: duck everything melodic right after each kick
sc = np.ones(N)
for bt in beats:
    i = int(bt * SR)
    n = min(int(BEAT * SR), N - i)
    sc[i:i + n] = 1 - 0.75 * np.exp(-np.arange(n) / SR / 0.09)

mel_L = np.zeros(N)
mel_R = np.zeros(N)
bar = 4 * BEAT
for k, bt in enumerate(np.arange(DROP, END, bar)):
    root, chord = prog[k % 4]
    dur = min(bar, END - bt)
    # sub bass on 8ths
    for j in range(int(dur / (BEAT / 2))):
        tt = t_axis(BEAT / 2 * 0.9)
        b = np.sin(2 * np.pi * note(root - 24) * tt) + 0.3 * lowpass(saw(note(root - 12), tt), 600)
        i = int((bt + j * BEAT / 2) * SR)
        seg_ = (b * env(len(tt), 0.004, 0.2) * 0.42)[: N - i]
        mel_L[i:i + len(seg_)] += seg_
        mel_R[i:i + len(seg_)] += seg_
    # pad
    p = pad_chord([note(m) for m in chord], dur) * 0.22
    i = int(bt * SR)
    p = p[: N - i]
    mel_L[i:i + len(p)] += p
    mel_R[i:i + len(p)] += np.roll(p, 300)
    # the hook: 8th-note pluck arpeggio, an octave up (from bar 2 so the drop breathes)
    if k >= 1:
        for j in range(int(dur / (BEAT / 2))):
            m = chord[hook[j % 8] % 3] + 12 + (12 if hook[j % 8] == 3 else 0)
            pl = pluck(note(m)) * 0.28
            i = int((bt + j * BEAT / 2) * SR)
            pl = pl[: N - i]
            mel_L[i:i + len(pl)] += pl * 0.8
            mel_R[i:i + len(pl)] += pl
L += mel_L * sc
R += mel_R * sc

# transitions: whooshes into each scene, impacts on the big moments
for at in (9.75, 11.8, 17.6, 21.8, 25.2):
    add(whoosh(0.45), at, 0.45, pan=rng.uniform(-0.4, 0.4))
for at in (12.0, 18.0, 22.0, 25.5):
    add(crash(), at, 0.35)
add(boom(), 25.5, 0.6)
add(kick(big=True), END, 1.0)
add(boom(), END, 0.9)
add(crash(), END, 0.7)

# ---------- master ----------
mix = np.stack([L, R], axis=1)
fade = np.ones(N)
fade[int(29.3 * SR):] = np.linspace(1, 0, N - int(29.3 * SR))
mix *= fade[:, None]
mix = np.tanh(mix / np.max(np.abs(mix)) * 2.4) * 0.9   # glue + soft-clip limiter
pcm = (mix * 32767).astype(np.int16)

out = sys.argv[1] if len(sys.argv) > 1 else 'hook-audio.wav'
with wave.open(out, 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print('wrote', out)
