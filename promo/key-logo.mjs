// One-off: keys the cream background out of the brand logo so it sits on the dark reel.
import { chromium } from 'playwright';
import fs from 'node:fs';
const src = fs.readFileSync(new URL('../frontend/public/assets/deveraxtech-logo.png', import.meta.url)).toString('base64');
const b = await chromium.launch();
const p = await b.newPage();
const out = await p.evaluate(async (src) => {
  const img = new Image(); img.src = 'data:image/png;base64,' + src; await img.decode();
  const c = document.createElement('canvas'); c.width = img.width; c.height = img.height;
  const x = c.getContext('2d'); x.drawImage(img, 0, 0);
  const d = x.getImageData(0, 0, c.width, c.height); const a = d.data;
  // Flood-fill from the border through low-saturation pixels: that is the cream background.
  // Specular highlights inside the metal are also pale, but they are not connected to the edge.
  const W = c.width, H = c.height, alpha = new Float32Array(W * H).fill(1), seen = new Uint8Array(W * H);
  const tOf = (p) => Math.min(1, Math.max(0, (a[p*4] - a[p*4+2] - 70) / 60));
  const stack = [];
  for (let xx = 0; xx < W; xx++) stack.push(xx, (H - 1) * W + xx);
  for (let y = 0; y < H; y++) stack.push(y * W, y * W + W - 1);
  while (stack.length) {
    const p = stack.pop(); if (seen[p]) continue; seen[p] = 1;
    const t = tOf(p); alpha[p] = t;
    if (t >= 0.5) continue;                  // reached the logo edge: stop spreading
    const px = p % W;
    if (px > 0) stack.push(p - 1); if (px < W - 1) stack.push(p + 1);
    if (p >= W) stack.push(p - W); if (p < W * (H - 1)) stack.push(p + W);
  }
  for (let p = 0; p < W * H; p++) a[p*4+3] = Math.round(255 * alpha[p]);
  x.putImageData(d, 0, 0);
  // crop to content
  let minX=c.width,minY=c.height,maxX=0,maxY=0;
  for (let y=0;y<c.height;y++) for (let xx=0;xx<c.width;xx++) if (a[(y*c.width+xx)*4+3]>40){minX=Math.min(minX,xx);maxX=Math.max(maxX,xx);minY=Math.min(minY,y);maxY=Math.max(maxY,y);}
  const pad=20, w=maxX-minX+pad*2, h=maxY-minY+pad*2;
  const c2=document.createElement('canvas'); c2.width=w; c2.height=h;
  c2.getContext('2d').drawImage(c,minX-pad,minY-pad,w,h,0,0,w,h);
  return c2.toDataURL('image/png').split(',')[1];
}, src);
fs.writeFileSync(new URL('./assets/logo.png', import.meta.url), Buffer.from(out, 'base64'));
await b.close();
