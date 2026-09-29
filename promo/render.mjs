// Renders reel.html frame by frame (deterministic, no dropped frames) and encodes an H.264 MP4.
// Usage: node render.mjs [out.mp4] [--page reel.html] [--audio track.wav|reel.mp4] [--fps 30] [--scale 2] [--stills t1,t2,... --dir DIR]
// --scale S renders at S× the page's CSS size (S=2: 1080×1920 -> 2160×3840, 1920×1080 -> 3840×2160). It is Chromium's
// device scale factor, so every CSS/SVG pixel value (type, positions, strokes, radii, blurs, shadows, transforms) is
// multiplied by S and rasterised natively, not upscaled. Canvases read window.devicePixelRatio to size their backing store.
// --audio also accepts an .mp4: its AAC track is copied unchanged (used to keep a re-render's audio identical).
import { chromium } from 'playwright';
import { spawn, execSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const pageFile = opt('--page', 'reel.html');
const audio = opt('--audio');
const out = path.resolve(args.find(a => a.endsWith('.mp4')) || path.join(here, 'deveraxtech-brand-reel.mp4'));
const fps = +opt('--fps', 30);
const stills = opt('--stills');
const scale = +opt('--scale', 1);
const ffmpeg = process.env.FFMPEG || execSync('python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())"').toString().trim();

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: scale });
await page.goto('file://' + path.join(here, pageFile));
const size = await page.evaluate(() => window.SIZE);
if (size) await page.setViewportSize(size);
await page.evaluate(() => window.ready);
const duration = await page.evaluate(() => window.DURATION);

if (stills) {
  for (const t of stills.split(',').map(Number)) {
    await page.evaluate(t => window.render(t), t);
    await page.screenshot({ path: path.join(opt('--dir', here), `still-${t}.png`) });
  }
  await browser.close();
  process.exit(0);
}

const enc = spawn(ffmpeg, ['-y', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
  ...(audio ? ['-i', path.resolve(audio), '-map', '0:v:0', '-map', '1:a:0', '-shortest',
    ...(audio.endsWith('.mp4') ? ['-c:a', 'copy'] : ['-c:a', 'aac', '-b:a', '192k'])] : []),
  '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', '-profile:v', 'high',
  ...(scale > 1 ? ['-level:v', '5.1'] : []), '-movflags', '+faststart', out],
  { stdio: ['pipe', 'inherit', 'inherit'] });
const total = Math.round(duration * fps);
for (let f = 0; f < total; f++) {
  await page.evaluate(t => window.render(t), f / fps);
  const buf = await page.screenshot({ type: 'jpeg', quality: 95 });
  if (!enc.stdin.write(buf)) await new Promise(r => enc.stdin.once('drain', r));
  if (f % fps === 0) process.stdout.write(`\r${Math.round(f / fps)}s / ${duration}s`);
}
enc.stdin.end();
await new Promise(r => enc.on('close', r));
await browser.close();
console.log(`\nwrote ${out}`);
