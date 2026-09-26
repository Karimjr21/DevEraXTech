// Renders reel.html frame by frame (deterministic, no dropped frames) and encodes an H.264 MP4.
// Usage: node render.mjs [out.mp4] [--fps 30] [--stills t1,t2,...]
import { chromium } from 'playwright';
import { spawn, execSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const out = path.resolve(args.find(a => a.endsWith('.mp4')) || path.join(here, 'deveraxtech-brand-reel.mp4'));
const fps = +opt('--fps', 30);
const stills = opt('--stills');
const ffmpeg = process.env.FFMPEG || execSync('python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())"').toString().trim();

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
await page.goto('file://' + path.join(here, 'reel.html'));
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
  '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out],
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
