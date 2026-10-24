# Contact sheet of review stills: python3 tools/sheet.py out.png img1 img2 ...
import sys
from PIL import Image, ImageDraw
out, files = sys.argv[1], sys.argv[2:]
ims = [Image.open(f).convert('RGB') for f in files]
w, h = ims[0].size
s = 360 / w
tw, th = int(w * s), int(h * s)
cols = min(len(ims), 5)
rows = (len(ims) + cols - 1) // cols
sheet = Image.new('RGB', (cols * (tw + 6), rows * (th + 22)), (40, 40, 40))
d = ImageDraw.Draw(sheet)
for i, (im, f) in enumerate(zip(ims, files)):
    x, y = (i % cols) * (tw + 6), (i // cols) * (th + 22)
    sheet.paste(im.resize((tw, th), Image.LANCZOS), (x, y + 20))
    d.text((x + 4, y + 4), f.split('/')[-1], fill=(255, 255, 255))
sheet.save(out)
