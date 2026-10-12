"""Contact sheet of frames: python3 preview.py N out.png [times...]"""
import sys
from PIL import Image
from scenes import REELS

n = int(sys.argv[1])
out = sys.argv[2]
r = REELS[n]
ts = [float(x) for x in sys.argv[3:]] or [0, 1.0] + [round(x * 0.5, 2) for x in range(3, int(r.dur * 2))]
import dx
th = [(dx.push_in(r.draw(t), 1 + 0.04 * dx.eo(t / r.push)) if r.push and t < r.push else r.draw(t)).resize((270, 480)) for t in ts]
cols = 8
rows = (len(th) + cols - 1) // cols
sheet = Image.new("RGB", (cols * 274, rows * 484), (80, 0, 0))
for i, im in enumerate(th):
    sheet.paste(im, ((i % cols) * 274 + 2, (i // cols) * 484 + 2))
sheet.save(out)
print(ts)
