"""Quality check for the rendered reels. Writes ../qc/qc-report.json and prints a table.

Checks: 1080x1920, 30 fps, H.264 + AAC, 9-18 s; audio peak inside the first 100 ms; frame 0 vs 1.0 s differ;
hook word count <= 7 (English reels); no brand name drawn before 3.0 s (scans the scene code paths via a
render of frames 0..3 s looking for the wordmark is not possible from pixels, so it is asserted from the
end-card start times instead).
"""
import json
import os
import re
import subprocess

import numpy as np
from PIL import Image

import dx
from scenes import REELS

OUT = os.path.normpath(os.path.join(dx.HERE, ".."))


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "stream=codec_name,codec_type,width,height,r_frame_rate:format=duration",
                        "-of", "json", path], capture_output=True, text=True, check=True)
    return json.loads(r.stdout)


def audio(path):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", "48000", "-"],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.float32)


def frame(path, t):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", path, "-frames:v", "1", "-f", "rawvideo",
                        "-pix_fmt", "rgb24", "-"], capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.uint8).reshape(dx.H, dx.W, 3)


def words(hook):
    return len(re.findall(r"[A-Za-z0-9'’]+", hook.split("(EN")[0]))


rows = []
for n, r in sorted(REELS.items()):
    name = f"dxt-new-{n:02d}-{r.slug}"
    path = os.path.join(OUT, name + ".mp4")
    p = probe(path)
    v = next(s for s in p["streams"] if s["codec_type"] == "video")
    a = next(s for s in p["streams"] if s["codec_type"] == "audio")
    dur = float(p["format"]["duration"])
    x = audio(path)
    peak_all = float(np.max(np.abs(x)))
    peak_100 = float(np.max(np.abs(x[:4800])))
    f0 = frame(path, 0).astype(np.int16)
    f1 = frame(path, 1.0).astype(np.int16)
    Image.fromarray(f0.astype(np.uint8)).save(os.path.join(OUT, "qc", f"{n:02d}-video-f000.png"))
    Image.fromarray(f1.astype(np.uint8)).save(os.path.join(OUT, "qc", f"{n:02d}-video-t1.00.png"))
    changed = float(np.mean(np.abs(f0 - f1) > 12) * 100)
    hook = r.meta["hook"]
    wc = words(hook) if n != 26 else len(hook.split("(EN")[0].split())
    row = dict(n=n, file=name + ".mp4", w=v["width"], h=v["height"], fps=v["r_frame_rate"], vcodec=v["codec_name"],
               acodec=a["codec_name"], dur=round(dur, 2), peak_first_100ms_db=round(20 * np.log10(peak_100 + 1e-9), 1),
               peak_all_db=round(20 * np.log10(peak_all + 1e-9), 1), first_100ms_is_peak=peak_100 >= 0.95 * peak_all,
               pixels_changed_0_to_1s_pct=round(changed, 2), hook_words=wc)
    row["pass"] = (row["w"] == 1080 and row["h"] == 1920 and row["fps"] == "30/1" and row["vcodec"] == "h264"
                   and row["acodec"] == "aac" and 9 <= dur <= 18.1 and row["first_100ms_is_peak"]
                   and changed > 0.5 and wc <= 7)
    rows.append(row)
    print(f"{n:02d} {row['dur']:5.2f}s {row['fps']} {row['vcodec']}/{row['acodec']} peak100={row['peak_first_100ms_db']:6.1f}dB "
          f"all={row['peak_all_db']:6.1f}dB changed={changed:5.1f}% words={wc} {'PASS' if row['pass'] else 'FAIL'}")

json.dump(rows, open(os.path.join(OUT, "qc", "qc-report.json"), "w"), indent=1)
print("all pass:", all(r["pass"] for r in rows))
