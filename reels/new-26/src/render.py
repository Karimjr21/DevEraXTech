"""Render reels: python3 render.py [numbers...]   (no numbers = all 26)

Writes ../dxt-new-NN-<slug>.mp4, ../covers/dxt-new-NN-<slug>.png (frame 0) and QC frames to ../qc/.
"""
import os
import subprocess
import sys
import wave

import numpy as np

import dx
import sfx
from scenes import REELS

OUT = os.path.normpath(os.path.join(dx.HERE, ".."))
QC = os.path.join(OUT, "qc")
COVERS = os.path.join(OUT, "covers")


def write_wav(path, st):
    pcm = (np.clip(st, -1, 1) * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sfx.SR)
        w.writeframes(pcm.tobytes())


def render(n):
    r = REELS[n]
    name = f"dxt-new-{n:02d}-{r.slug}"
    os.makedirs(QC, exist_ok=True)
    os.makedirs(COVERS, exist_ok=True)
    frames = int(round(r.dur * dx.FPS))
    tmp = os.environ.get("REEL_TMP", "/tmp")
    wav = os.path.join(tmp, name + ".wav")
    mix = sfx.Mix(r.dur)
    r.audio(mix)
    write_wav(wav, mix.render(room=r.room))
    mp4 = os.path.join(OUT, name + ".mp4")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{dx.W}x{dx.H}",
           "-r", str(dx.FPS), "-i", "-", "-i", wav, "-c:v", "libx264", "-preset", "slow", "-crf", "24", "-tune", "grain",
           "-pix_fmt", "yuv420p", "-profile:v", "high", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
           "-shortest", "-movflags", "+faststart", mp4]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for fi in range(frames):
        t = fi / dx.FPS
        im = r.draw(t)
        if r.push and t < r.push:
            im = dx.push_in(im, 1 + 0.04 * dx.eo(t / r.push))
        if fi == 0:
            im.save(os.path.join(COVERS, name + ".png"))
            im.save(os.path.join(QC, f"{n:02d}-f000.png"))
        if fi == dx.FPS:
            im.save(os.path.join(QC, f"{n:02d}-f030.png"))
        for qs in r.qc:
            if fi == int(qs * dx.FPS):
                im.save(os.path.join(QC, f"{n:02d}-t{qs:05.2f}.png"))
        p.stdin.write(dx.finish(im, fi, r.grain))
    p.stdin.close()
    p.wait()
    os.remove(wav)
    if p.returncode:
        raise SystemExit(f"ffmpeg failed for {name}")
    print("rendered", name, f"{r.dur:.1f}s")


def remux(n):
    """Rebuild only the audio track of an existing reel."""
    r = REELS[n]
    name = f"dxt-new-{n:02d}-{r.slug}"
    tmp = os.environ.get("REEL_TMP", "/tmp")
    wav = os.path.join(tmp, name + ".wav")
    mix = sfx.Mix(r.dur)
    r.audio(mix)
    write_wav(wav, mix.render(room=r.room))
    mp4 = os.path.join(OUT, name + ".mp4")
    out = os.path.join(tmp, name + ".mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp4, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", out], check=True)
    os.replace(out, mp4)
    os.remove(wav)
    print("remuxed", name)


if __name__ == "__main__":
    if sys.argv[1:2] == ["--audio"]:
        for n in [int(a) for a in sys.argv[2:]] or sorted(REELS):
            remux(n)
        raise SystemExit
    nums = [int(a) for a in sys.argv[1:]] or sorted(REELS)
    for n in nums:
        render(n)
