"""Automated frame QC: temporal continuity, flicker, black frames, clipping.

usage: python3 -I tools/qc.py <frames_dir> <report_prefix> [fps]
Writes <prefix>.csv (per-frame metrics), <prefix>.png (timeline plot) and prints
flagged frames. Intentional cuts are listed so they are not reported as pops.
"""
import sys, os, glob
import numpy as np
from PIL import Image, ImageDraw

INTENDED_CUTS = [3.0, 6.0, 9.0, 12.0, 16.0, 20.0, 21.333, 22.667, 24.0, 28.0, 33.0]


def main():
    d, prefix = sys.argv[1], sys.argv[2]
    fps = float(sys.argv[3]) if len(sys.argv) > 3 else 60
    files = sorted(glob.glob(os.path.join(d, '*.png')))
    lum, diff, clip, black = [], [], [], []
    prev = None
    for f in files:
        im = Image.open(f).convert('L').resize((180, 320), Image.BILINEAR)
        a = np.asarray(im, dtype=np.float32) / 255
        lum.append(a.mean())
        clip.append((a > 0.985).mean())
        black.append(a.max() < 0.03)
        diff.append(0.0 if prev is None else np.abs(a - prev).mean())
        prev = a
    lum, diff, clip = map(np.array, (lum, diff, clip))
    n = len(files)
    t = np.array([int(os.path.basename(f)[:5]) for f in files]) / fps
    # spike = frame difference far above its local neighbourhood (a pop or a flicker)
    flags = []
    for i in range(2, n - 2):
        local = np.median(np.r_[diff[max(1, i - 6):i - 1], diff[i + 2:i + 7]])
        near_cut = any(abs(t[i] - c) < 0.08 for c in INTENDED_CUTS)
        if diff[i] > max(0.02, 4.0 * local) and not near_cut:
            flags.append((i, t[i], 'pop', diff[i], local))
        if clip[i] > 0.04:
            flags.append((i, t[i], 'clipping', clip[i], 0))
    blk = [i for i in range(n) if black[i]]
    with open(prefix + '.csv', 'w') as fh:
        fh.write('frame,t,mean_luma,frame_diff,clipped_fraction,black\n')
        for i in range(n):
            fh.write(f'{i},{t[i]:.3f},{lum[i]:.4f},{diff[i]:.4f},{clip[i]:.4f},{int(black[i])}\n')
    # timeline plot
    W, H = 1800, 420
    img = Image.new('RGB', (W, H), (14, 15, 18))
    g = ImageDraw.Draw(img)
    T = t[-1] if n else 1
    for c in INTENDED_CUTS:
        x = int(c / T * (W - 1))
        g.line([(x, 0), (x, H)], fill=(45, 48, 54))
    def plot(v, scale, col):
        pts = [(int(t[i] / T * (W - 1)), int(H - 10 - min(1, v[i] * scale) * (H - 30))) for i in range(n)]
        g.line(pts, fill=col, width=1)
    plot(lum, 2.5, (185, 190, 197))
    plot(diff, 8.0, (142, 166, 191))
    plot(clip, 10.0, (220, 120, 90))
    for f in flags:
        x = int(f[1] / T * (W - 1))
        g.ellipse([x - 3, 4, x + 3, 10], fill=(255, 80, 80))
    g.text((8, 8), 'luma (silver)  frame-diff (blue)  clipping (orange)  grey lines = intended cuts', fill=(200, 200, 200))
    img.save(prefix + '.png')
    print(f'{n} frames · flagged {len(flags)} · black frames {len(blk)}')
    for f in flags[:60]:
        print(f'  frame {f[0]:5d}  t={f[1]:6.2f}s  {f[2]:8s}  value={f[3]:.4f}  local={f[4]:.4f}')
    if blk:
        print('  black:', blk[:20], '...' if len(blk) > 20 else '')


if __name__ == '__main__':
    main()
