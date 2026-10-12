# DeveraXTech reels: new set of 26

- `dxt-new-NN-<slug>.mp4`: the 26 reels (1080x1920, 30 fps, H.264 + AAC, 9–18 s).
- `covers/`: cover PNG for each reel. Each one is frame 0, which is also the hook frame.
- `reels-spec.md`: per reel, the hook type, industry, exact hook text, second-by-second beats, sound design, CTA and why it should stop the scroll.
- `captions.md`: caption, hashtags and a pinned comment for each reel.
- `qc/`: frame 0 and the 1.0 s frame of every rendered file, plus `qc-report.json`.
- `src/`: the generator. Everything (visuals and sound) is drawn in code, so any reel can be edited and re-rendered.

## Re-render

```bash
cd src
pip install pillow numpy scipy aggdraw     # Pillow needs libraqm for the Arabic reel
python3 preview.py 7 /tmp/sheet.png        # contact sheet of one reel, for quick checks
python3 render.py 7                        # one reel (or no number for all 26)
python3 qc.py                              # format, audio-peak, motion and hook-length checks
python3 gen_spec.py                        # rebuild reels-spec.md from the scene metadata
```

Fonts in `src/fonts/` are open-licence (OFL): Playfair Display, Cormorant Garamond, Caveat, Cairo and Inter.
