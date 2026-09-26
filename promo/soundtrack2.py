"""Ten more genre soundtracks for the second batch of vertical reels.

Reuses the mixer and instruments from soundtrack.py and adds new voices. Cue sheets are written in BEATS of each
reel's own tempo (the HTML pages use the same beat grid), so every cut lands on the music.

  dm-chat        UK garage 2-step (132)        spy-dossier   60s spy surf (120)
  nature-doc     documentary orchestra (84)    player-card   stadium stomp anthem (80)
  recipe         bossa nova (126)              terminal      drum & bass (174)
  tarot          ethereal harp + choir (70)    western       spaghetti western (96)
  quest          celtic jig in 6/8 (8th = 0.25 s)             dating        nu-disco (118)

Usage: python3 soundtrack2.py <reel> [out.wav]
"""
import sys
import wave

import numpy as np

from soundtrack import (SR, T, Mix, adsr, bandpass, bell, clap, crash, expenv, glide_phase, hat, highpass, karplus,
                        kick_edm, kick_soft, kick_tight, lowpass, marimba, note, pad, pluck, rhodes, riser, rng, saw,
                        shaker, sine, snare_big, snare_lofi, sparkle, square, strings, subdrop, taiko, tom, vox, whoosh,
                        tick, pop, page_flip, thud, coin, register, typing, boom, glitch, tri, snare_trap, eight08, brass,
                        piano, organ)


# ---------------------------------------------------------------- new voices
def whistle(f, dur):
    t = T(dur)
    vib = 1 + 0.012 * np.sin(2 * np.pi * 5.5 * t) * np.clip((t - 0.15) / 0.2, 0, 1)
    ph = 2 * np.pi * np.cumsum(f * vib) / SR
    breath = bandpass(rng.standard_normal(len(t)), f * 0.8, f * 1.3) * 0.08
    return (np.sin(ph) + breath) * adsr(len(t), 0.05, 0.3, 0.85, 0.1) * 0.7


def flute(f, dur):
    t = T(dur)
    vib = 1 + 0.006 * np.sin(2 * np.pi * 5 * t) * np.clip((t - 0.2) / 0.2, 0, 1)
    ph = 2 * np.pi * np.cumsum(f * vib) / SR
    s = np.sin(ph) + 0.15 * np.sin(2 * ph) + bandpass(rng.standard_normal(len(t)), f, f * 3) * 0.05
    return s * adsr(len(t), 0.04, 0.2, 0.8, 0.08) * 0.6


def twang(f, dur, trem=True):
    t = T(dur)
    s = karplus(f, dur, bright=0.85, decay=0.9975)
    s = np.tanh(s * 1.6)
    if trem:
        s *= 1 - 0.35 * (0.5 + 0.5 * np.sin(2 * np.pi * 7 * t))
    return s * np.minimum(1, (dur - t) / 0.03 + 0.001) * 0.8


def nylon(f, dur):
    return lowpass(karplus(f, dur, bright=0.35, decay=0.996), 2600) * 0.8


def harp(f, dur=1.6):
    return karplus(f, dur, bright=0.55, decay=0.9985) * 0.7


def fiddle(f, dur):
    t = T(dur)
    vib = 1 + 0.01 * np.sin(2 * np.pi * 6 * t) * np.clip((t - 0.1) / 0.15, 0, 1)
    ph = np.cumsum(f * vib) / SR
    s = 2 * (ph % 1) - 1
    s = bandpass(s, 400, 4500) + bandpass(rng.standard_normal(len(t)), 2000, 6000) * 0.03
    return s * adsr(len(t), 0.03, 0.2, 0.8, 0.05) * 0.6


def upright(f, dur):
    t = T(dur)
    return (lowpass(karplus(f, dur, bright=0.3, decay=0.995), 900) + sine(f, t) * np.exp(-t * 5) * 0.6) * 0.9


def reese(f, dur):
    t = T(dur)
    s = sum(saw(f * d, t, rng.random()) for d in (0.99, 1.0, 1.013))
    wob = 500 + 350 * (0.5 + 0.5 * np.sin(2 * np.pi * 1.3 * t))
    y = lowpass(s, 700) * 0.6 + lowpass(s, float(np.mean(wob))) * 0.4
    return np.tanh(y * 1.3) * adsr(len(t), 0.01, 0.2, 0.9, 0.05) * 0.5


def choir(freqs, dur, vowel='oo'):
    t = T(dur)
    s = sum(saw(f * d, t, rng.random()) for f in freqs for d in (0.995, 1.005)) / (len(freqs) * 2)
    if vowel == 'oo':
        y = bandpass(s, 250, 450) + 0.5 * bandpass(s, 700, 900)
    else:
        y = bandpass(s, 650, 900) + 0.6 * bandpass(s, 1050, 1300)
    return y * adsr(len(t), 0.6, 1, 1, 0.6) * 2.2


def octbass(f, dur):
    t = T(dur)
    return lowpass(saw(f, t), 900) * adsr(len(t), 0.005, 0.12, 0.6, 0.03) * 0.8


def stabs(freqs, dur=0.2):
    t = T(dur)
    s = sum(saw(f * d, t, rng.random()) for f in freqs for d in (0.995, 1.005)) / (len(freqs) * 2)
    return lowpass(s, 3500) * expenv(len(t), 0.004, 0.09)


def stomp():
    t = T(0.6)
    return np.sin(glide_phase(95, 48, t, 18)) * np.exp(-t * 7) + lowpass(rng.standard_normal(len(t)), 400) * np.exp(-t * 20) * 0.7


def woodblock(f=900):
    t = T(0.1)
    return (sine(f, t) + 0.4 * sine(f * 2.7, t)) * np.exp(-t * 45) * 0.6


def bongo(f=320):
    t = T(0.25)
    return np.sin(glide_phase(f * 1.3, f, t, 40)) * np.exp(-t * 16) * 0.7


def rim():
    t = T(0.06)
    return (bandpass(rng.standard_normal(len(t)), 1500, 5000) * np.exp(-t * 120) + sine(1700, t) * np.exp(-t * 90) * 0.5) * 0.6


def ride():
    t = T(0.6)
    return (highpass(rng.standard_normal(len(t)), 5000) * np.exp(-t * 6) * 0.3 + sine(3200, t) * np.exp(-t * 8) * 0.05)


def brush():
    t = T(0.25)
    return bandpass(rng.standard_normal(len(t)), 1500, 7000) * np.sin(np.pi * t / 0.25) * 0.25


def timpani(f=65, big=False):
    t = T(2.0 if big else 1.2)
    return np.sin(glide_phase(f * 1.2, f, t, 12)) * np.exp(-t * (1.5 if big else 3)) + lowpass(rng.standard_normal(len(t)), 300) * np.exp(-t * 20) * 0.3


def bodhran(accent=False):
    t = T(0.3)
    return np.sin(glide_phase(110, 70, t, 20)) * np.exp(-t * 12) * (1 if accent else 0.55) + lowpass(rng.standard_normal(len(t)), 900) * np.exp(-t * 40) * 0.25


# ---------------------------------------------------------------- new effects
def ref_whistle():
    t = T(0.7)
    f = 2900 + 250 * np.sign(np.sin(2 * np.pi * 28 * t))
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) + bandpass(rng.standard_normal(len(t)), 2500, 4000) * 0.2) * adsr(len(t), 0.02, 0.2, 0.9, 0.08) * 0.4


def crowd(dur=2.5):
    t = T(dur)
    n = bandpass(rng.standard_normal(len(t)), 300, 3000)
    claps = np.zeros(len(t))
    for s in rng.integers(0, len(t), int(dur * 60)):
        c = clap()[: len(t) - s] * rng.uniform(0.05, 0.2)
        claps[s:s + len(c)] += c
    return (n * 0.5 + claps) * np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 0.7


def whip():
    t = T(0.18)
    return highpass(rng.standard_normal(len(t)), 2500) * np.exp(-t * 60) * (t > 0.03) + np.sin(glide_phase(3000, 800, t, 30)) * np.exp(-t * 50) * 0.3


def crack():
    """The 'DRAW!' crack: a sharp snap + canyon echo."""
    t = T(1.4)
    y = highpass(rng.standard_normal(len(t)), 800) * np.exp(-t * 50)
    for d, g in ((0.22, 0.35), (0.45, 0.18), (0.7, 0.08)):
        i = int(d * SR)
        y[i:] += y[: len(y) - i] * g
    return np.tanh(y * 2) * 0.8


def church_bell(f=196):
    t = T(3.0)
    s = sum(sine(f * r, t) * np.exp(-t * (0.8 + k * 0.5)) * a for k, (r, a) in enumerate(((1, 1), (2.0, .5), (2.4, .4), (3.0, .3), (4.2, .2))))
    return s * np.minimum(1, t / 0.003) * 0.6


def hooves(dur=2.0, rate=3.2):
    y = np.zeros(int(dur * SR))
    for i in range(int(dur * rate * 2)):
        s = int((i / (rate * 2) + (0.06 if i % 2 else 0)) * SR)
        w = woodblock(700 if i % 2 else 560) * (0.7 if i % 2 else 1)
        y[s:s + len(w)] += w[: max(0, len(y) - s)]
    return y


def sizzle(dur=1.2):
    t = T(dur)
    n = highpass(rng.standard_normal(len(t)), 4000) * (0.4 + 0.6 * (rng.random(len(t)) > 0.97))
    return n * np.sin(np.pi * t / dur) * 0.25


def typewriter(dur=1.0, rate=14, ding_end=True):
    y = typing(dur, rate) * 1.4
    if ding_end:
        b = bell(2093, 0.6) * 0.3
        s = len(y) - int(0.1 * SR)
        y = np.concatenate([y, np.zeros(len(b))])
        y[s:s + len(b)] += b
    return y


def msg_sent():
    t = T(0.25)
    return np.sin(glide_phase(500, 1500, t, 12)) * np.exp(-t * 18) * 0.4 + whoosh(0.25)[: len(t)] * 0.3


def msg_recv():
    y = np.zeros(int(0.5 * SR))
    for s0, f in ((0, 1318.5), (0.09, 1760)):
        b = bell(f, 0.4) * 0.35
        s = int(s0 * SR)
        y[s:s + len(b)] += b[: len(y) - s]
    return y


def levelup():
    seq = [note(m) for m in (72, 76, 79, 84, 88, 91)]
    y = np.zeros(int(1.4 * SR))
    for i, f in enumerate(seq):
        b = bell(f, 0.8) * 0.35
        s = int(i * 0.07 * SR)
        y[s:s + len(b)] += b[: len(y) - s]
    return y


def card_flip():
    t = T(0.2)
    return bandpass(rng.standard_normal(len(t)), 1500, 6000) * np.exp(-t * 30) * 0.5 + np.sin(glide_phase(300, 900, t, 20)) * np.exp(-t * 25) * 0.2


def stamp():
    t = T(0.35)
    return np.sin(glide_phase(140, 60, t, 25)) * np.exp(-t * 14) + bandpass(rng.standard_normal(len(t)), 300, 2500) * np.exp(-t * 40) * 0.5


def swipe(up=False):
    return whoosh(0.3, up)


def heart_pop(f=1200):
    b = bell(f * 2, 0.3) * 0.15
    p = pop(f)
    b[: len(p)] += p
    return b


def oven_ding():
    return bell(1568, 1.5) * 0.7


def keyclick_burst(dur=1.0, rate=22):
    return typing(dur, rate)


SFX2 = {
    'boom': boom, 'crash': crash, 'riser': riser, 'subdrop': subdrop, 'sparkle': sparkle, 'whoosh': whoosh,
    'whoosh_up': lambda d=0.4: whoosh(d, True), 'pop': pop, 'page': page_flip, 'thud': thud, 'coin': coin, 'register': register,
    'glitch': glitch, 'tick': tick, 'bell': bell, 'ref_whistle': ref_whistle, 'crowd': crowd, 'whip': whip, 'crack': crack,
    'church_bell': church_bell, 'hooves': hooves, 'sizzle': sizzle, 'typewriter': typewriter, 'msg_sent': msg_sent,
    'msg_recv': msg_recv, 'levelup': levelup, 'card_flip': card_flip, 'stamp': stamp, 'swipe': swipe, 'heart_pop': heart_pop,
    'oven_ding': oven_ding, 'keys': keyclick_burst, 'taiko': taiko, 'timpani': timpani, 'snare_big': snare_big,
    'kick': kick_edm, 'stomp': stomp,
}


# ---------------------------------------------------------------- helpers
def bar_iter(c, per_bar=4):
    """Yield (bar index, start seconds) from the drop to the end, in this reel's tempo."""
    B = 60 / c['bpm']
    t0, t1 = c['drop'] * B, c['end'] * B
    k = 0
    tb = t0
    while tb < t1 - 1e-6:
        yield k, tb
        k += 1
        tb += per_bar * B


def chord_at(prog, k):
    return prog[k % len(prog)]


# ================================================================ styles
def st_garage(mix, c):
    """UK garage 2-step: skippy kicks, shuffled hats, organ stabs, vocal chops, sub bass. Cm7 Abmaj7 Fm7 G7."""
    B = 60 / c['bpm']
    s16 = B / 4
    sw = s16 * 0.16                                     # shuffle: late 16th offbeats
    prog = [[48, 51, 55, 58], [44, 48, 51, 55], [41, 44, 48, 51], [43, 47, 50, 53]]
    chops = [(0, 12), (3, 10), (6, 7), (10, 12), (13, 15)]
    for i in range(int(c['drop'] * 2)):                  # intro: filtered chops
        mix.add(lowpass(vox(note(prog[0][0] + 24 + (0, 3, 7, 10)[i % 4]), B / 2 * 0.8), 1500), i * B / 2, 0.3, verb=0.4)
    for k, tb in bar_iter(c):
        ch = chord_at(prog, k)
        for st in (0, 7, 10):
            mix.add(highpass(kick_tight(), 55), tb + st * s16, 0.5 if st == 0 else 0.35, bus='drums')
        for st in (4, 12):
            mix.add(clap(), tb + st * s16, 0.75, bus='drums', verb=0.2)
            mix.add(rim(), tb + st * s16 + s16 * 3, 0.25, bus='drums')
        for st in range(16):
            off = sw if st % 2 else 0
            mix.add(hat(tone=8000), tb + st * s16 + off, 0.32 if st % 4 == 2 else 0.14, pan=0.25, bus='drums')
        mix.duck(tb, 0.5, 0.12)
        mix.add(np.sin(glide_phase(note(ch[0] - 12) * 1.5, note(ch[0] - 12), T(B * 3), 25)) * adsr(int(B * 3 * SR), 0.01, 1, 1, 0.1), tb, 0.22)
        mix.add(np.sin(2 * np.pi * note(ch[0] - 5) * T(B)) * adsr(int(B * SR), 0.01, 0.3, 0.6, 0.05), tb + 3 * B + sw, 0.16)
        for st in (3, 11):
            mix.add(sum(organ(note(m + 12), s16 * 1.6) for m in ch) / 4, tb + st * s16 + sw, 0.5, pan=-0.2)
        if k % 2 == 1:
            for st, deg in chops:
                mix.add(vox(note(ch[0] + 12 + deg), s16 * 1.8), tb + st * s16 + (sw if st % 2 else 0), 0.55, pan=0.15, verb=0.3)
    return dict(rt=1.3, damp=6000, drive=1.6)


def st_spy(mix, c):
    """60s spy surf in E minor: twang riff with spring reverb, walking upright bass, swung ride, bongos, brass stabs."""
    B = 60 / c['bpm']
    riff = [(0, 40), (1, 43), (1.5, 45), (2, 46), (2.5, 45), (3, 43), (3.5, 40)]     # E G A Bb A G E (bar)
    walk = [40, 43, 45, 47, 48, 47, 45, 43]
    for i in range(int(c['drop'])):                                                  # intro: lone twang + bongos
        mix.add(twang(note(52 if i % 2 == 0 else 55), B * 0.9), i * B, 0.35, verb=0.6)
        mix.add(bongo(300 if i % 2 else 380), i * B + B / 2, 0.4, bus='drums')
    for k, tb in bar_iter(c):
        for off, m in riff:
            mix.add(twang(note(m + 12 + (0 if k % 4 < 2 else 5)), B * 0.55), tb + off * B, 0.45, pan=-0.25, verb=0.5)
        for j in range(4):
            mix.add(upright(note(walk[(k * 4 + j) % 8] - 12 + (0 if k % 4 < 2 else 5)), B * 0.9), tb + j * B, 0.7)
            mix.add(ride(), tb + j * B, 0.35, pan=0.3, bus='drums')
            mix.add(ride(), tb + j * B + B * 0.66, 0.2, pan=0.3, bus='drums')
            mix.add(bongo(320 if j % 2 else 400), tb + j * B + B * 0.5, 0.3, pan=-0.3, bus='drums')
            if j in (1, 3):
                mix.add(brush(), tb + j * B, 0.6, bus='drums')
        mix.add(kick_soft(), tb, 0.6, bus='drums')
        if k % 2 == 1:
            mix.add(brass([note(m) for m in (52, 55, 59, 62, 66)], 0.35), tb + 3.5 * B, 0.4, verb=0.3)
    return dict(rt=2.4, damp=4500, drive=1.4)


def st_doc(mix, c):
    """Nature-documentary orchestra in D major: harp arpeggios, strings, flute, pizzicato 'curious' section, swells."""
    B = 60 / c['bpm']
    prog = [[50, 57, 62, 66], [47, 54, 59, 62], [43, 55, 59, 62], [45, 52, 57, 61]]   # D Bm G A
    for k, tb in bar_iter(dict(c, drop=0)):
        ch = chord_at(prog, k)
        mix.add(strings([note(m) for m in ch], 4 * B + 0.2, attack=0.8), tb, 0.26, verb=0.6)
        for j in range(8):
            mix.add(harp(note(ch[j % 4] + 12 + (12 if j >= 4 else 0)), 1.6), tb + j * B / 2, 0.22, pan=0.25, verb=0.5)
        t_sec = tb
        if 9.0 <= t_sec < 15.0:                                                   # curious pizzicato
            for j in range(8):
                mix.add(karplus(note(ch[(j * 3) % 4] + 12), 0.3, bright=0.4, decay=0.99) * 0.5, tb + j * B / 2 + B / 4, 0.35, pan=-0.2)
        if t_sec >= 15.0 or t_sec < 3.0:
            mel = [ch[3] + 12, ch[2] + 12, ch[1] + 24, ch[3] + 12]
            for j, m in enumerate(mel):
                mix.add(flute(note(m), B * 0.95), tb + j * B, 0.3, pan=-0.15, verb=0.5)
    for s in (2.86, 12.0, 15.0, 19.7):
        mix.add(timpani(55, True), s, 0.6, bus='drums', verb=0.3)
    return dict(rt=2.8, damp=5500, drive=1.2)


def st_stadium(mix, c):
    """Stadium anthem: stomp-stomp-clap, crowd, brass anthem chords, big toms. C G Am F."""
    B = 60 / c['bpm']
    prog = [[48, 55, 60, 64], [43, 55, 59, 62], [45, 52, 57, 60], [41, 53, 57, 60]]
    for k, tb in bar_iter(c):
        ch = chord_at(prog, k)
        for j in (0, 2):                                     # stomp stomp CLAP per half bar
            mix.add(highpass(stomp(), 70), tb + j * B, 0.6, bus='drums', verb=0.35)
            mix.add(highpass(stomp(), 70), tb + j * B + B / 2, 0.55, bus='drums', verb=0.35)
            mix.add(clap(2.0) * 1.3, tb + (j + 1) * B, 0.8, bus='drums', verb=0.5)
        mix.add(brass([note(m) for m in ch], 4 * B * 0.95), tb, 0.6, verb=0.4)
        mix.add(sine(note(ch[0] - 12), T(4 * B)) * adsr(int(4 * B * SR), 0.02, 1, 1, 0.1), tb, 0.12)
        if k >= 4:
            for j, m in enumerate((ch[3] + 12, ch[2] + 12, ch[3] + 12, ch[1] + 12)):
                mix.add(brass([note(m)], B * 0.9), tb + j * B, 0.3, pan=0.2, verb=0.4)
    return dict(rt=2.6, damp=5000, drive=1.5)


def st_bossa(mix, c):
    """Bossa nova: nylon guitar comping, bass on 1 and 3, rim clave, shaker, soft flute. Cmaj7 Am7 Dm7 G7."""
    B = 60 / c['bpm']
    prog = [[48, 52, 55, 59], [45, 52, 55, 60], [50, 53, 57, 60], [43, 53, 57, 59]]
    comp = [0, 1.5, 2.5, 3.5]                      # syncopated comping hits (beats)
    clave = [0, 1.5, 3, 4.5, 6]                    # 2-bar rim pattern (beats)
    mel = [(0, 76), (1, 74), (1.5, 72), (2.5, 71), (3, 69)]
    for k, tb in bar_iter(c):
        ch = chord_at(prog, k)
        for off in comp:
            for m in ch[1:]:
                mix.add(nylon(note(m), B * 0.9), tb + off * B + ch.index(m) * 0.012, 0.22, pan=-0.2, verb=0.25)
        mix.add(upright(note(ch[0] - 12), B * 1.4), tb, 0.6)
        mix.add(upright(note(ch[0] - 5), B * 0.9), tb + 1.5 * B, 0.45)
        mix.add(upright(note(ch[0] - 12), B * 1.4), tb + 2 * B, 0.55)
        for off in clave:
            if off < 4 or k % 2:
                mix.add(rim(), tb + (off % 4) * B, 0.3, bus='drums')
        for j in range(16):
            mix.add(shaker(), tb + j * B / 4, 0.3 if j % 2 else 0.18, pan=0.3, bus='drums')
        mix.add(kick_soft(), tb, 0.5, bus='drums')
        mix.add(kick_soft(), tb + 2 * B, 0.4, bus='drums')
        if k % 2 == 1:
            for off, m in mel:
                mix.add(flute(note(m - (0 if k % 4 == 1 else 2)), B * 0.9), tb + off * B, 0.25, pan=0.2, verb=0.4)
    return dict(rt=1.6, damp=6000, drive=1.3)


def st_dnb(mix, c):
    """Drum & bass (174): two-step break, ghost snares, rolling hats, reese bass, dark pad. Fm Db Ab Eb."""
    B = 60 / c['bpm']
    s16 = B / 4
    prog = [[41, 44, 48], [37, 41, 44], [44, 48, 51], [39, 43, 46]]
    for i in range(int(c['drop'] * 4)):                        # intro: typing-like ticks rising
        mix.add(tick(2000 + i * 40), i * s16, 0.25)
    for k, tb in bar_iter(c):
        ch = chord_at(prog, k)
        for st in (0, 10):
            mix.add(kick_tight(), tb + st * s16, 0.9, bus='drums')
        for st in (4, 12):
            mix.add(snare_big(), tb + st * s16, 0.7, bus='drums', verb=0.15)
        for st in (7, 14):
            mix.add(snare_lofi(), tb + st * s16, 0.18, bus='drums')
        for st in range(16):
            mix.add(hat(tone=9000), tb + st * s16, 0.25 if st % 2 else 0.12, pan=0.2, bus='drums')
        mix.duck(tb, 0.6, 0.1)
        mix.add(reese(note(ch[0]), 4 * B * 0.98), tb, 0.55)
        mix.add(pad([note(m + 12) for m in ch], 4 * B, 1600), tb, 0.12, verb=0.5)
        if k % 2:
            mix.add(stabs([note(m + 24) for m in ch]), tb + 3.5 * B, 0.3, verb=0.3)
    return dict(rt=1.5, damp=6000, drive=1.8)


def st_ethereal(mix, c):
    """Ethereal: choir 'oo' pads, harp, bells, low drone, wind. D dorian: Dm C G Dm."""
    B = 60 / c['bpm']
    prog = [[50, 57, 62, 65], [48, 55, 60, 64], [43, 55, 59, 62], [50, 57, 62, 65]]
    wind = lowpass(rng.standard_normal(int(c['duration'] * SR)), 600) * 0.03
    mix.add(wind * (0.6 + 0.4 * np.sin(2 * np.pi * 0.2 * T(c['duration']))), 0, 1.0, bus='fx')
    for k, tb in bar_iter(dict(c, drop=0)):
        ch = chord_at(prog, k)
        mix.add(choir([note(m) for m in ch[1:]], 4 * B + 0.5), tb, 0.35, verb=0.7)
        mix.add(strings([note(ch[0] - 12)], 4 * B + 0.3, attack=1.0), tb, 0.2, verb=0.5)
        for j in range(8):
            mix.add(harp(note(ch[(j * 2) % 4] + 12 + (12 if j % 3 == 2 else 0)), 2.2), tb + j * B / 2, 0.2, pan=(-0.3 if j % 2 else 0.3), verb=0.6)
        mix.add(bell(note(ch[3] + 24), 2.0), tb + 3 * B, 0.12, verb=0.7)
    return dict(rt=4.0, damp=5000, drive=1.2)


def st_western(mix, c):
    """Spaghetti western in A minor: whistle theme, tremolo twang, clip-clop, choir 'ah', timpani."""
    B = 60 / c['bpm']
    prog = [[45, 52, 57, 60], [43, 50, 55, 59], [41, 48, 53, 57], [40, 47, 52, 56]]   # Am G F E
    theme = [(0, 76, 1.5), (1.5, 81, .5), (2, 79, 1), (3, 76, 1), (4, 74, 1.5), (5.5, 72, .5), (6, 71, 2)]   # 2 bars
    for i, (off, m, ln) in enumerate(theme):                                         # intro whistle
        mix.add(whistle(note(m), ln * B * 0.95), off * B, 0.35, verb=0.6)
    mix.add(hooves(c['drop'] * B, 1 / B), 0, 0.35, bus='drums')
    for k, tb in bar_iter(c):
        ch = chord_at(prog, k)
        for j in range(8):                                                           # strummed tremolo guitar
            mix.add(twang(note(ch[j % 4] + (0 if j % 4 else 12)), B * 0.5), tb + j * B / 2, 0.22, pan=-0.3, verb=0.45)
        mix.add(upright(note(ch[0] - 12), B * 1.8), tb, 0.55)
        mix.add(upright(note(ch[0] - 5), B * 1.8), tb + 2 * B, 0.45)
        mix.add(hooves(4 * B, 1 / B) * 0.5, tb, 0.3, bus='drums')
        if k % 2 == 0:
            for off, m, ln in theme:
                if off < 8:
                    mix.add(whistle(note(m), ln * B * 0.95), tb + off * B, 0.38, pan=0.15, verb=0.55)
        else:
            mix.add(choir([note(m) for m in ch[1:]], 4 * B, 'ah'), tb, 0.25, verb=0.6)
    return dict(rt=3.0, damp=4500, drive=1.3)


def st_jig(mix, c):
    """Celtic jig in 6/8 (8th = B): tin whistle + fiddle melody, bouzouki drone, bodhran. D mixolydian: D C G D."""
    E = 60 / c['bpm']                           # an eighth note
    bar = 6 * E
    prog = [[50, 57, 62], [48, 55, 60], [43, 55, 59], [50, 57, 62]]
    jig = [74, 76, 78, 79, 78, 76, 74, 71, 69, 71, 74, 76]            # 2 bars of 8ths
    k = 0
    tb = c['drop'] * E
    for i in range(int(c['drop'])):                                     # intro: whistle pickup
        mix.add(flute(note(jig[i % 12] + 12), E * 0.9), i * E, 0.25, verb=0.3)
    while tb < c['end'] * E - 1e-6:
        ch = prog[k % 4]
        for j in range(6):
            m = jig[(k % 2) * 6 + j]
            mix.add(flute(note(m + 12), E * 0.95), tb + j * E, 0.32, pan=0.2, verb=0.3)
            if k >= 2:
                mix.add(fiddle(note(m), E * 0.95), tb + j * E, 0.25, pan=-0.2, verb=0.3)
            mix.add(highpass(bodhran(j in (0, 3)), 60), tb + j * E, 0.42 if j in (0, 3) else 0.22, bus='drums')
        for j in (0, 3):
            for m in ch:
                mix.add(karplus(note(m), 3 * E, bright=0.7, decay=0.996) * 0.4, tb + j * E + ch.index(m) * 0.01, 0.35, pan=-0.3, verb=0.2)
        mix.add(sine(note(ch[0] - 12), T(bar)) * adsr(int(bar * SR), 0.02, 1, 1, 0.05), tb, 0.1)
        k += 1
        tb += bar
    return dict(rt=1.4, damp=6000, drive=1.3)


def st_disco(mix, c):
    """Nu-disco (118): four-on-the-floor, octave bass, string swells and stabs, claps, open hats. Am7 Dm7 G Cmaj7."""
    B = 60 / c['bpm']
    prog = [[45, 52, 55, 60], [50, 53, 57, 60], [43, 50, 55, 59], [48, 52, 55, 59]]
    for k, tb in bar_iter(c):
        ch = chord_at(prog, k)
        for j in range(4):
            mix.add(highpass(kick_edm(), 45), tb + j * B, 0.6, bus='drums')
            mix.duck(tb + j * B, 0.35, 0.12)
            mix.add(hat(True), tb + j * B + B / 2, 0.28, pan=0.2, bus='drums')
            if j in (1, 3):
                mix.add(clap(), tb + j * B, 0.55, bus='drums', verb=0.25)
        for j in range(8):
            mix.add(octbass(note(ch[0] + (12 if j % 2 else 0)), B / 2 * 0.9), tb + j * B / 2, 0.4)
        mix.add(strings([note(m + 12) for m in ch], 4 * B, attack=0.3), tb, 0.35, verb=0.4)
        for off in (1.5, 3.5):
            mix.add(stabs([note(m + 12) for m in ch]), tb + off * B, 0.35, pan=-0.2, verb=0.3)
        if k % 2:
            for j, m in enumerate((ch[3] + 12, ch[2] + 12, ch[3] + 12, ch[1] + 24)):
                mix.add(rhodes(note(m), B * 0.9), tb + j * B, 0.2, pan=0.25, verb=0.3)
    return dict(rt=1.5, damp=7000, drive=1.5)


STYLES2 = {'garage': st_garage, 'spy': st_spy, 'doc': st_doc, 'stadium': st_stadium, 'bossa': st_bossa, 'dnb': st_dnb,
           'ethereal': st_ethereal, 'western': st_western, 'jig': st_jig, 'disco': st_disco}


# ================================================================ cue sheets (beats; they mirror each page's timeline)
def ev(beats, name, gain=0.6, args=(), verb=0.15):
    return (beats, name, gain, args, verb)


CUES2 = {
    'dm-chat': dict(style='garage', bpm=132, duration=22, drop=6, end=47.5, events=[
        ev(0, 'pop', .5, (900,)), ev(1, 'pop', .5, (1000,)), ev(2, 'pop', .6, (1150,)), ev(5, 'riser', .5, (1.0,)),
        ev(6, 'boom', .7), ev(6.5, 'msg_sent', .6), ev(8, 'tick', .4), ev(10, 'glitch', .25),
        ev(12, 'swipe', .5), ev(12.5, 'msg_sent', .6), ev(14, 'msg_recv', .5), ev(15, 'msg_recv', .5), ev(16.5, 'msg_sent', .5),
        ev(18, 'swipe', .5), ev(18.5, 'msg_sent', .6), *[ev(b, 'msg_recv', .55) for b in (21, 23, 25, 27, 29, 33)],
        ev(31, 'msg_sent', .55), ev(36, 'boom', .6), ev(36, 'sparkle', .5), ev(38, 'coin', .4)]),
    'spy-dossier': dict(style='spy', bpm=120, duration=22, drop=6, end=43, events=[
        ev(0, 'typewriter', .7, (0.9, 14)), ev(2, 'typewriter', .7, (0.9, 14)), ev(4, 'stamp', .9), ev(6, 'page', .7), ev(6, 'boom', .5),
        *[ev(7 + 1.6 * i, 'typewriter', .45, (0.6, 16, False)) for i in range(6)], ev(16.6, 'whoosh', .4, (0.3,)),
        ev(19, 'thud', .5), *[ev(b, 'tick', .4) for b in (21, 23, 25)], ev(21, 'whoosh', .3, (0.5,)),
        ev(28, 'riser', .5, (2.5,)), ev(32, 'boom', .8), ev(32, 'crash', .4), ev(35, 'typewriter', .6, (0.9, 14)), ev(38, 'stamp', .7)]),
    'nature-doc': dict(style='doc', bpm=84, duration=24, drop=4, end=33.5, events=[
        ev(0, 'whoosh', .25, (1.2,)), ev(4, 'sparkle', .35), ev(12.6, 'page', .3), ev(17.1, 'sparkle', .35),
        ev(21, 'crash', .2), ev(27.6, 'sparkle', .4), ev(28.9, 'bell', .3, (1318.5,))]),
    'player-card': dict(style='stadium', bpm=80, duration=24, drop=4, end=31, events=[
        ev(0, 'ref_whistle', .6), ev(0, 'crowd', .5, (2.5,)), ev(3, 'riser', .5, (0.75,)), ev(4, 'boom', .9), ev(4, 'sparkle', .5),
        ev(6, 'whoosh', .5, (0.4,)), ev(7, 'whoosh', .5, (0.4,)), ev(8, 'whoosh', .5, (0.4,)), ev(10, 'boom', 1.0), ev(10, 'crowd', .7, (3.0,)),
        ev(10, 'crash', .5), *[ev(12 + i, 'coin', .35) for i in range(6)], ev(20, 'whoosh', .4, (0.4,)),
        ev(24, 'ref_whistle', .5), ev(24, 'crowd', .5, (3.0,)), ev(26, 'stamp', .6)]),
    'recipe': dict(style='bossa', bpm=126, duration=23, drop=4, end=44, events=[
        ev(0, 'page', .4), ev(3.2, 'pop', .4), *[ev(5 + 2.1 * i, 'pop', .5, (700 + 90 * i,)) for i in range(5)],
        ev(16.8, 'sizzle', .5, (1.2,)), ev(18.9, 'thud', .3), ev(21, 'whoosh', .3, (0.4,)), ev(24, 'oven_ding', .7),
        ev(26.2, 'whoosh_up', .5, (0.5,)), ev(26.2, 'sparkle', .6), ev(32.5, 'pop', .4), ev(36.7, 'sparkle', .4), ev(39.1, 'pop', .4)]),
    'terminal': dict(style='dnb', bpm=174, duration=21, drop=9, end=60, events=[
        ev(0, 'keys', .5, (1.2, 22)), ev(4, 'glitch', .6), ev(5.5, 'keys', .5, (1.0, 22)), ev(9, 'boom', .8), ev(9, 'crash', .4),
        *[ev(9.6 + 1.6 * i, 'tick', .45, (2600,)) for i in range(9)], ev(23.2, 'riser', .5, (1.4,)), ev(28.4, 'coin', .5),
        ev(31.9, 'boom', .8), ev(31.9, 'glitch', .5), ev(40.6, 'tick', .5), ev(46.4, 'keys', .5, (0.8, 22)), ev(49.3, 'coin', .5)]),
    'tarot': dict(style='ethereal', bpm=70, duration=24, drop=0, end=28, events=[
        ev(0, 'sparkle', .5), ev(2.6, 'whoosh', .4, (0.8,)), *[ev(b, 'card_flip', .7) for b in (5, 10, 15)],
        *[ev(b, 'timpani', .5, (55,)) for b in (5, 10)], ev(15, 'boom', .8), ev(15, 'sparkle', .8), ev(15, 'crash', .3),
        ev(20, 'church_bell', .3, (392,)), ev(22, 'sparkle', .5)]),
    'western': dict(style='western', bpm=96, duration=24, drop=4, end=37, events=[
        ev(0, 'whoosh', .3, (1.0,)), ev(4, 'stamp', .9), ev(4, 'whip', .6), *[ev(b, 'tick', .3) for b in (5, 6, 7)],
        ev(10, 'whoosh', .5, (0.6,)), *[ev(14 + i, 'church_bell', .5) for i in range(3)], ev(17.5, 'tick', .5), ev(18, 'crack', 1.0),
        ev(19.2, 'whoosh', .4, (0.4,)), ev(22, 'coin', .5), ev(22, 'sparkle', .5), ev(30, 'whip', .5), ev(30, 'hooves', .4, (2.0, 3.2))]),
    'quest': dict(style='jig', bpm=240, duration=21, drop=6, end=81, events=[
        ev(0, 'page', .5), ev(1.6, 'sparkle', .4), ev(12, 'whoosh', .4, (0.4,)), ev(12, 'levelup', .4),
        *[ev(26 + 3 * i, 'coin', .45) for i in range(5)], ev(42, 'thud', .7), ev(44.8, 'levelup', .6), ev(48, 'sparkle', .6),
        ev(54, 'levelup', .7), ev(66, 'stamp', .6), ev(70, 'coin', .5)]),
    'dating': dict(style='disco', bpm=118, duration=22, drop=4, end=43, events=[
        ev(0, 'heart_pop', .5), ev(1, 'heart_pop', .5, (1400,)), ev(4, 'whoosh', .3, (0.3,)), ev(8, 'swipe', .6), ev(8, 'stamp', .5),
        ev(8.5, 'whoosh', .3, (0.3,)), ev(12, 'swipe', .6), ev(12, 'stamp', .5), ev(12.5, 'whoosh', .3, (0.3,)),
        *[ev(14 + i, 'pop', .35, (900 + 60 * i,)) for i in range(6)], ev(24, 'swipe', .6, (True,)), ev(24, 'stamp', .5),
        ev(24.5, 'boom', .7), ev(24.5, 'sparkle', .7), *[ev(24.5 + .25 * i, 'heart_pop', .3, (1000 + 100 * i,)) for i in range(6)],
        ev(28, 'keys', .3, (1.4, 14)), ev(31, 'msg_sent', .6), ev(32, 'sparkle', .4)]),
}


def build(name):
    c = dict(CUES2[name])
    mix = Mix(c['duration'])
    opts = STYLES2[c['style']](mix, c)
    B = 60 / c['bpm']
    for beats, nm, gain, args, verb in c['events']:
        if not isinstance(args, tuple):
            args = (args,)
        mix.add(SFX2[nm](*args), beats * B, gain, pan=float(rng.uniform(-0.25, 0.25)), bus='fx', verb=verb)
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
