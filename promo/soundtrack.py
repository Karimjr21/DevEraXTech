"""Cue-sheet soundtrack synth for the vertical reels (numpy only).

A reel's soundtrack = an intro/tension section, a drop, a sidechained beat with a pluck hook, and
one-shot sound effects placed on the video's cuts. Cue sheets live in CUES at the bottom.

Usage: python3 soundtrack.py <cue-name> [out.wav]
"""
import sys
import wave

import numpy as np

SR = 44100
rng = np.random.default_rng(7)


def t_axis(sec):
    return np.arange(int(sec * SR)) / SR


def lowpass(x, cutoff):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / np.sqrt(1 + (f / cutoff) ** 4)
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


# ---------- instruments / effects ----------
def kick(big=False):
    t = t_axis(0.9 if big else 0.45)
    f = 45 + 110 * np.exp(-t * 28)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * (3.5 if big else 7))
    return np.tanh((s + rng.standard_normal(len(t)) * np.exp(-t * 400) * 0.3) * 1.6)


def clap():
    t = t_axis(0.3)
    n = highpass(lowpass(rng.standard_normal(len(t)), 2500), 800)
    return n * (np.exp(-t * 22) + 0.6 * np.exp(-np.maximum(0, t - 0.012) * 30) * (t > 0.012)) * 0.8


def hat(open_=False):
    t = t_axis(0.25 if open_ else 0.06)
    return highpass(rng.standard_normal(len(t)), 7000) * np.exp(-t * (14 if open_ else 70)) * 0.6


def tick(freq=3200):
    t = t_axis(0.03)
    return np.sin(2 * np.pi * freq * t) * np.exp(-t * 250) * 0.5 + highpass(rng.standard_normal(len(t)), 5000) * np.exp(-t * 300) * 0.3


def beep(freq=880, dur=0.16):
    t = t_axis(dur)
    return np.sin(2 * np.pi * freq * t) * env(len(t), 0.003, dur / 2.5)


def boom():
    t = t_axis(1.8)
    f = 38 + 60 * np.exp(-t * 6)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.2)
    return np.tanh((s + lowpass(rng.standard_normal(len(t)), 900) * np.exp(-t * 5) * 0.6) * 1.4)


def glitch():
    t = t_axis(0.16)
    sq = np.sign(np.sin(2 * np.pi * (180 + 900 * rng.random()) * t))
    bits = np.round(rng.standard_normal(len(t)) * 3) / 3
    return (sq * 0.4 + bits * 0.3) * (np.floor(t * 90) % 2 == 0) * np.exp(-t * 14)


def buzzer():
    """Game-show 'wrong answer'."""
    t = t_axis(0.42)
    s = sum(np.sign(np.sin(2 * np.pi * f * t)) for f in (98, 104, 147))
    return lowpass(s / 3, 1800) * np.minimum(1, t / 0.01) * np.minimum(1, (0.42 - t) / 0.05) * 0.7


def ding(freq=1318.5):
    """Bright bell 'correct answer'."""
    t = t_axis(1.0)
    s = np.sin(2 * np.pi * freq * t) + 0.5 * np.sin(2 * np.pi * freq * 2.01 * t) + 0.25 * np.sin(2 * np.pi * freq * 3.02 * t)
    return s * env(len(t), 0.002, 0.35) * 0.45


def shutter():
    t = t_axis(0.12)
    n = highpass(rng.standard_normal(len(t)), 1500)
    return n * (np.exp(-t * 90) + 0.7 * np.exp(-np.maximum(0, t - 0.05) * 90) * (t > 0.05)) * 0.8


def whoosh(dur=0.5, up=True):
    t = t_axis(dur)
    n = rng.standard_normal(len(t))
    out = np.zeros_like(n)
    chunks = 24
    for k in range(chunks):
        a, b = k * len(t) // chunks, (k + 1) * len(t) // chunks
        out[a:b] = lowpass(n, 400 * (20 ** (k / chunks if up else 1 - k / chunks)))[a:b]
    return out * np.sin(np.pi * t / dur) ** 2 * 0.9


def riser(dur):
    t = t_axis(dur)
    f = 180 * (8 ** (t / dur))
    return (saw(1, np.cumsum(f) / SR) * 0.25 + highpass(rng.standard_normal(len(t)), 2000) * 0.5) * (t / dur) ** 2.2


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
    return lowpass(s, 1400) * np.minimum(1, t / 0.05) * np.minimum(1, np.maximum(0, dur - t) / 0.05)


SFX = {
    'kick': lambda a: kick(), 'kick_big': lambda a: kick(True), 'boom': lambda a: boom(), 'glitch': lambda a: glitch(),
    'buzzer': lambda a: buzzer(), 'ding': lambda a: ding(note(a) if a else 1318.5), 'shutter': lambda a: shutter(),
    'whoosh': lambda a: whoosh(a or 0.5), 'whoosh_down': lambda a: whoosh(a or 0.5, up=False), 'riser': lambda a: riser(a),
    'crash': lambda a: crash(), 'beep': lambda a: beep(a or 880), 'tick': lambda a: tick(a or 3200), 'clap': lambda a: clap(),
}


def build(cue):
    dur, bpm = cue['duration'], cue['bpm']
    beat = 60 / bpm
    n = int(SR * dur)
    L, R = np.zeros(n), np.zeros(n)

    def add(sig, at, gain=1.0, pan=0.0, into=None):
        i = int(at * SR)
        if i >= n:
            return
        sig = sig[: n - i] * gain
        l, r = into if into else (L, R)
        l[i:i + len(sig)] += sig * np.sqrt(1 - pan)
        r[i:i + len(sig)] += sig * np.sqrt(1 + pan)

    # intro drone under the tension section
    drop, end = cue['drop'], cue['end']
    if drop > 0.5:
        ta = t_axis(drop)
        root = note(cue['progression'][0][0] - 24)
        drone = (np.sin(2 * np.pi * root * ta) + 0.5 * lowpass(saw(root * 1.005, ta), 300)) * np.minimum(1, ta / 0.3)
        drone *= 0.18 * (0.6 + 0.4 * ta / drop)
        drone[int((drop - cue.get('gap', 0.15)) * SR):] = 0
        add(drone, 0)

    # the beat
    beats = np.arange(drop, end, beat)
    for bi, bt in enumerate(beats):
        add(kick(), bt, 0.95)
        if bi % 2 == 1:
            add(clap(), bt, 0.55)
        add(hat(open_=(bi % 4 == 3)), bt + beat / 2, 0.35, pan=0.3)
        add(hat(), bt + beat / 4, 0.12, pan=-0.3)
    sc = np.ones(n)
    for bt in beats:
        i = int(bt * SR)
        k = min(int(beat * SR), n - i)
        sc[i:i + k] = 1 - 0.75 * np.exp(-np.arange(k) / SR / 0.09)

    ml, mr = np.zeros(n), np.zeros(n)
    bar = 4 * beat
    prog, hook = cue['progression'], cue['hook']
    for k, bt in enumerate(np.arange(drop, end, bar)):
        root, chord = prog[k % len(prog)]
        while root - 24 < 28:                          # keep the sub bass audible (>= ~41 Hz)
            root += 12
        d = min(bar, end - bt)
        for j in range(int(round(d / (beat / 2)))):
            tt = t_axis(beat / 2 * 0.9)
            b = np.sin(2 * np.pi * note(root - 24) * tt) + 0.3 * lowpass(saw(note(root - 12), tt), 600)
            add(b * env(len(tt), 0.004, 0.2) * 0.42, bt + j * beat / 2, into=(ml, mr))
        add(pad_chord([note(m) for m in chord], d) * 0.22, bt, into=(ml, mr))
        if k >= cue.get('hook_from_bar', 1):
            for j in range(int(round(d / (beat / 2)))):
                h = hook[j % len(hook)]
                m = chord[h % len(chord)] + 12 + (12 if h >= len(chord) else 0)
                add(pluck(note(m)) * 0.28, bt + j * beat / 2, pan=0.15, into=(ml, mr))
    L += ml * sc
    R += mr * sc

    # drop + ending hits, then the cue sheet
    add(boom(), drop, 1.0)
    add(kick(True), drop, 1.0)
    add(crash(), drop, 0.8)
    add(kick(True), end, 1.0)
    add(boom(), end, 0.9)
    add(crash(), end, 0.7)
    for ev in cue['events']:
        at, name = ev[0], ev[1]
        gain = ev[2] if len(ev) > 2 else 0.6
        arg = ev[3] if len(ev) > 3 else None
        add(SFX[name](arg), at, gain, pan=float(rng.uniform(-0.3, 0.3)))

    mix = np.stack([L, R], axis=1)
    fade = np.ones(n)
    fs = int((dur - 0.6) * SR)
    fade[fs:] = np.linspace(1, 0, n - fs)
    mix *= fade[:, None]
    mix = np.tanh(mix / np.max(np.abs(mix)) * 2.4) * 0.9
    return (mix * 32767).astype(np.int16)


def rounds(first, count, length):
    """Them-vs-us rounds: buzzer for them, ding + crash for us, whoosh out."""
    ev = []
    for i in range(count):
        r = first + i * length
        ev += [(r, 'buzzer', 0.55), (r, 'kick', 0.5), (r + 1.0, 'ding', 0.6, 76 + i * 2), (r + 1.0, 'crash', 0.35),
               (r + 1.0, 'boom', 0.45), (r + length - 0.3, 'whoosh', 0.45, 0.4)]
    return ev


CUES = {
    # "Your competitors don't want you to see this" — them vs us, 5 rounds
    'them-vs-us': {
        'duration': 24, 'bpm': 120, 'drop': 4.0, 'end': 23.5, 'gap': 0.12,
        'progression': [(50, [50, 53, 57]), (46, [46, 50, 53]), (53, [53, 57, 60]), (48, [48, 52, 55])],  # Dm Bb F C
        'hook': [0, 1, 2, 3, 2, 1, 0, 2],
        'events': [
            (0.0, 'boom', 0.9), (0.5, 'boom', 0.6), (1.0, 'boom', 0.6), (1.5, 'kick_big', 0.9), (1.5, 'crash', 0.6),
            *[(x, 'tick', 0.5) for x in np.arange(0, 2.5, 0.25)],
            (2.4, 'whoosh', 0.6, 0.35), (3.0, 'kick_big', 0.9), (3.0, 'boom', 0.8), (3.0, 'riser', 0.7, 0.88),
            *rounds(4.0, 5, 3.0),
            *[(19.25 + i * 0.25, 'ding', 0.45, 72 + i * 2) for i in range(5)], (20.5, 'boom', 0.8), (20.5, 'crash', 0.5),
            (21.0, 'whoosh', 0.5), (22.0, 'crash', 0.4), (22.0, 'boom', 0.5),
        ],
    },
    # "Rate this website 1-10" — showcase flex
    'rate-this': {
        'duration': 24, 'bpm': 120, 'drop': 2.0, 'end': 23.5, 'gap': 0.1,
        'progression': [(48, [48, 52, 55]), (55, [55, 59, 62]), (57, [57, 60, 64]), (53, [53, 57, 60])],  # C G Am F
        'hook': [0, 2, 3, 2, 1, 2, 0, 3], 'hook_from_bar': 0,
        'events': [
            (0.0, 'boom', 0.8), (0.5, 'kick_big', 0.7),
            *[(0.9 + i * 0.1, 'beep', 0.35, 440 * 2 ** (i / 12)) for i in range(10)], (1.0, 'riser', 0.7, 0.95),
            (6.0, 'shutter', 0.7), (6.0, 'whoosh', 0.4, 0.3), (9.0, 'shutter', 0.7), (9.0, 'whoosh', 0.4, 0.3),
            (12.0, 'whoosh', 0.5), (12.0, 'crash', 0.4), (16.0, 'crash', 0.4), (16.0, 'boom', 0.5),
            *[(16.0 + i * 0.5, 'ding', 0.4, 79 + i * 2) for i in range(4)], (18.0, 'kick_big', 0.6),
            (19.0, 'boom', 0.8), (19.0, 'crash', 0.5),
            *[(21.0 + i * 0.05, 'tick', 0.35, 2000 + i * 200) for i in range(10)], (22.25, 'boom', 0.5), (22.25, 'crash', 0.35),
        ],
    },
}

# ---- five more reels ----
CUES.update({
    # "3 signs your website is costing you money" — countdown listicle
    'money-signs': {
        'duration': 24, 'bpm': 120, 'drop': 2.5, 'end': 23.5, 'gap': 0.1,
        'progression': [(45, [45, 48, 52]), (41, [41, 45, 48]), (43, [43, 47, 50]), (40, [40, 44, 47])],  # Am F G E
        'hook': [0, 2, 1, 2, 3, 2, 1, 2],
        'events': [
            (0.0, 'boom', 0.9), (0.5, 'boom', 0.6), (1.0, 'boom', 0.6), (1.4, 'kick_big', 0.9), (1.4, 'crash', 0.5),
            *[(1.4 + i * 0.12, 'ding', 0.25, 84 + (i % 3) * 3) for i in range(6)], (1.6, 'riser', 0.6, 0.85),
            *[(s, 'kick_big', 0.6) for s in (2.5, 7.0, 11.5)], *[(s + 2.5, 'buzzer', 0.5) for s in (2.5, 7.0, 11.5)],
            *[(s + 4.2, 'whoosh', 0.45, 0.35) for s in (2.5, 7.0)], (7.0, 'glitch', 0.4), (11.5, 'glitch', 0.4),
            (15.0, 'riser', 0.7, 0.88), (16.0, 'boom', 1.0), (16.0, 'crash', 0.7), (16.5, 'kick_big', 0.8),
            *[(17.0 + i * 0.5, 'ding', 0.5, 76 + i * 3) for i in range(3)], (19.5, 'whoosh', 0.5), (20.5, 'crash', 0.4),
        ],
    },
    # "Watch this website glow up" — before/after
    'glow-up': {
        'duration': 24, 'bpm': 120, 'drop': 8.0, 'end': 23.5, 'gap': 0.12,
        'progression': [(52, [52, 56, 59]), (49, [49, 52, 56]), (45, [45, 49, 52]), (47, [47, 51, 54])],  # E C#m A B
        'hook': [0, 1, 2, 3, 2, 1, 2, 1],
        'events': [
            (0.0, 'boom', 0.8), (0.5, 'boom', 0.6), (1.0, 'kick_big', 0.8), (1.0, 'crash', 0.4),
            *[(2.0 + i * 0.5, 'tick', 0.35) for i in range(10)], (2.0, 'shutter', 0.5),
            *[(3.5 + i, 'buzzer', 0.45) for i in range(3)], (7.0, 'boom', 0.9), (7.0, 'riser', 0.8, 0.88),
            (8.0, 'whoosh', 0.7, 0.7), *[(9.0 + i * 1.5, 'ding', 0.5, 76 + i * 4) for i in range(3)],
            (14.0, 'whoosh', 0.45, 0.6), (15.3, 'whoosh_down', 0.4, 0.6), (17.5, 'boom', 0.8), (17.5, 'crash', 0.5),
            (18.0, 'kick_big', 0.7), (19.5, 'whoosh', 0.5), (20.5, 'crash', 0.4),
        ],
    },
    # "Here's exactly how we work" — 3 steps
    'process': {
        'duration': 24, 'bpm': 120, 'drop': 2.5, 'end': 23.5, 'gap': 0.12,
        'progression': [(50, [50, 54, 57]), (47, [47, 50, 54]), (43, [43, 47, 50]), (45, [45, 49, 52])],  # D Bm G A
        'hook': [0, 2, 1, 3, 0, 2, 1, 2],
        'events': [
            (0.0, 'boom', 0.8), (0.5, 'boom', 0.6), (1.0, 'kick_big', 0.8), (1.0, 'glitch', 0.4), (1.3, 'riser', 0.6, 1.05),
            (3.0, 'kick_big', 0.6), *[(4.0 + i * 4, 'whoosh', 0.5, 0.35) for i in range(3)], *[(4.0 + i * 4, 'ding', 0.45, 74 + i * 5) for i in range(3)],
            *[(4.9 + i * 0.35, 'beep', 0.2, 660) for i in range(4)], (6.2, 'ding', 0.5, 88),
            *[(9.0 + i * 0.15, 'tick', 0.3, 2400 + i * 150) for i in range(7)], (10.2, 'crash', 0.35),
            (14.2, 'kick_big', 0.6), (14.6, 'whoosh', 0.6, 0.9), (15.2, 'crash', 0.5),
            (16.0, 'boom', 0.8), *[(16.75 + i * 0.5, 'ding', 0.45, 79 + i * 3) for i in range(3)], (19.5, 'whoosh', 0.5), (20.5, 'crash', 0.4),
        ],
    },
    # "A studio in Cairo. Serving 7 countries."
    'worldwide': {
        'duration': 24, 'bpm': 120, 'drop': 2.0, 'end': 23.5, 'gap': 0.1,
        'progression': [(48, [48, 52, 55]), (45, [45, 48, 52]), (41, [41, 45, 48]), (43, [43, 47, 50])],  # C Am F G
        'hook': [0, 1, 2, 3, 2, 3, 1, 2], 'hook_from_bar': 0,
        'events': [
            (0.0, 'boom', 0.8), (0.5, 'boom', 0.6), (1.0, 'kick_big', 0.8), (1.1, 'riser', 0.6, 0.8),
            *[(2.5 + i * 1.25, 'whoosh', 0.35, 0.55) for i in range(1, 7)], *[(2.5 + i * 1.25 + (0.6 if i else 0), 'ding', 0.45, 76 + i * 2) for i in range(7)],
            (12.0, 'boom', 0.7), (12.75, 'kick_big', 0.6), (13.5, 'kick_big', 0.6), (14.5, 'crash', 0.5),
            (16.0, 'boom', 0.7), *[(16.3 + i * 0.25, 'tick', 0.3) for i in range(8)], (18.3, 'ding', 0.5, 84),
            (19.5, 'crash', 0.5), (19.5, 'boom', 0.6),
        ],
    },
    # "What you actually get when you hire us" — unboxing
    'whats-included': {
        'duration': 24, 'bpm': 120, 'drop': 4.0, 'end': 23.5, 'gap': 0.12,
        'progression': [(53, [53, 57, 60]), (50, [50, 53, 57]), (46, [46, 50, 53]), (48, [48, 52, 55])],  # F Dm Bb C
        'hook': [0, 2, 3, 2, 1, 2, 3, 1],
        'events': [
            (0.0, 'boom', 0.8), (0.5, 'boom', 0.6), (1.0, 'kick_big', 0.8), (2.0, 'kick_big', 0.9), (2.0, 'crash', 0.4),
            *[(3.0 + i * 0.11, 'tick', 0.3, 1800 + i * 90) for i in range(8)], (3.0, 'riser', 0.8, 0.88),
            (4.0, 'whoosh', 0.6, 0.6), *[(4.3 + i * 0.5, 'ding', 0.35, 72 + (i * 2) % 14) for i in range(10)],
            (9.5, 'boom', 0.7), (10.0, 'kick_big', 0.7), (13.3, 'buzzer', 0.35), (14.05, 'buzzer', 0.35),
            (14.5, 'boom', 0.6), (15.0, 'crash', 0.5), (16.5, 'boom', 0.7), (17.7, 'crash', 0.5), (17.7, 'ding', 0.5, 88),
            (19.5, 'whoosh', 0.5), (20.5, 'crash', 0.4),
        ],
    },
})

if __name__ == '__main__':
    name = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else f'{name}-audio.wav'
    pcm = build(CUES[name])
    with wave.open(out, 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print('wrote', out)
