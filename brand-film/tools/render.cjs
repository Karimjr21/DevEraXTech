// Batch frame renderer: lossless PNG intermediates, one file per frame.
// node tools/render.cjs <out_dir> <w> <h> <variant> <first> <last> [stride] [offset]
// stride/offset let several workers interleave over one range.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const [out, w, h, variant, first, last, stride = '1', offset = '0'] = process.argv.slice(2);
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: 400, height: 400 } });
  p.on('pageerror', (e) => console.log('[pageerror]', e.message));
  await p.goto(`http://localhost:8765/src/index.html?w=${w}&h=${h}&variant=${variant}`);
  await p.waitForFunction('window.filmReady === true', null, { timeout: 300000 });
  const t0 = Date.now();
  let n = 0;
  for (let f = +first + +offset; f <= +last; f += +stride) {
    const file = path.join(out, `${String(f).padStart(5, '0')}.png`);
    if (fs.existsSync(file)) continue;
    const url = await p.evaluate((fr) => window.grabFrame(fr / 60), f);
    fs.writeFileSync(file + '.tmp', Buffer.from(url.split(',')[1], 'base64'));
    fs.renameSync(file + '.tmp', file);
    n++;
    if (n % 60 === 0) console.log(`${variant} frame ${f} · ${((Date.now() - t0) / n / 1000).toFixed(2)} s/frame`);
  }
  console.log(`done ${variant} ${first}-${last} (+${offset}/${stride}): ${n} frames in ${((Date.now() - t0) / 1000).toFixed(0)} s`);
  await b.close();
})();
