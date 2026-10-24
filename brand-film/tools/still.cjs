// Render individual stills for review: node tools/still.cjs <out_dir> <w> <h> <variant> t1 t2 ...
// NOTEXT=1 renders clean plates (no typography on scenes 01–08) for thumbnails.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const [out, w, h, variant, ...ts] = process.argv.slice(2);
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: 400, height: 400 } });
  p.on('console', (m) => { if (m.type() === 'error' || m.type() === 'warning') console.log('[page]', m.text().slice(0, 400)); });
  p.on('pageerror', (e) => console.log('[pageerror]', e.message));
  await p.goto(`http://localhost:8765/src/index.html?w=${w}&h=${h}&variant=${variant}${process.env.NOTEXT ? "&notext=1" : ""}`);
  await p.waitForFunction('window.filmReady === true', null, { timeout: 180000 });
  for (const t of ts) {
    const t0 = Date.now();
    const url = await p.evaluate((tt) => window.grabFrame(tt), +t);
    const f = path.join(out, `${variant}_${(+t).toFixed(3)}.png`);
    fs.writeFileSync(f, Buffer.from(url.split(',')[1], 'base64'));
    console.log(f, Date.now() - t0, 'ms');
  }
  await b.close();
})();
