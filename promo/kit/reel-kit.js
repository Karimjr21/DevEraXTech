// Shared timing helpers and "chrome" (grain, sparks, progress bar, profile row, flashes, beat camera)
// for the vertical DevEraXTech reels. Each reel defines its own scenes and calls kit.chrome(t) per frame.
(function () {
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const seg = (t, a, b) => clamp((t - a) / (b - a));
  const easeOut = (x) => 1 - Math.pow(1 - x, 3);
  const easeInOut = (x) => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
  const back = (x) => { const c = 2.2; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
  const decay = (t, at, k = 8) => t < at ? 0 : Math.exp(-(t - at) * k);
  const slam = (t, at, d = .22) => { const k = seg(t, at, at + d); return { o: k > 0 ? 1 : 0, s: 1 + (1 - back(k)) * 1.6 }; };
  const pop = (t, at, d = .3) => { const k = seg(t, at, at + d); return { o: clamp(k * 3), s: .6 + back(k) * .4 }; };
  const rise = (t, at, d = .3) => easeOut(seg(t, at, at + d));
  const win = (t, a, b) => t >= a && t < b ? 1 : 0;
  const show = (el, o, tf = '') => { el.style.opacity = o; el.style.transform = tf; };
  const rng = (seed) => () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  const $ = (s) => document.querySelector(s);

  /**
   * cfg: { duration, bpm, beatFrom, beatTo, hits: [{t, amp}], bursts: [t], goldFlashes: [t], whiteFlashes: [t],
   *        blackouts: [[a, b]], goldFrom }
   */
  function setup(cfg) {
    const stage = $('#stage'), world = $('#world');
    world.insertAdjacentHTML('afterbegin', `<div id="bgGold" class="layer"></div><div id="rays" class="layer"></div>
      <canvas id="sparks" class="layer" width="1080" height="1920"></canvas>`);
    stage.insertAdjacentHTML('beforeend', `<canvas id="grain" class="layer" width="540" height="960"></canvas><div id="vig" class="layer"></div>
      <div id="progress"><i></i></div><div id="handle"><img src="assets/logo.png" alt="">deveraxtech <span>· Web studio</span></div>
      <div id="goldFlash" class="layer"></div><div id="flash" class="layer"></div><div id="black" class="layer"></div>`);
    const beat = 60 / cfg.bpm;
    const gctx = $('#grain').getContext('2d');
    const tiles = Array.from({ length: 6 }, (_, k) => {
      const r = rng(99 + k), img = gctx.createImageData(540, 960);
      for (let i = 0; i < img.data.length; i += 4) { const v = r() * 255; img.data[i] = img.data[i + 1] = img.data[i + 2] = v; img.data[i + 3] = 255; }
      return img;
    });
    const sctx = $('#sparks').getContext('2d'), sr = rng(5);
    const sparks = Array.from({ length: 90 }, () => ({ a: sr() * 6.283, v: 400 + sr() * 1400, s: 2 + sr() * 5, life: .5 + sr() * .9 }));
    const dust = Array.from({ length: 70 }, () => ({ x: sr() * 1080, y: sr() * 1920, v: 20 + sr() * 60, s: 1 + sr() * 3, p: sr() * 6.28 }));

    function chrome(t, extra = {}) {
      gctx.putImageData(tiles[Math.floor(t * 30) % tiles.length], 0, 0);
      sctx.clearRect(0, 0, 1080, 1920);
      const gold = t >= (cfg.goldFrom ?? 0);
      if (gold) for (const d of dust) {
        const y = ((d.y - d.v * t) % 1920 + 1920) % 1920;
        sctx.fillStyle = `rgba(245,213,115,${.25 + .25 * Math.sin(t * 2 + d.p)})`; sctx.beginPath(); sctx.arc(d.x, y, d.s, 0, 6.283); sctx.fill();
      }
      for (const b of cfg.bursts || []) {
        const dt = t - b; if (dt < 0 || dt > 1.5) continue;
        for (const p of sparks) {
          if (dt > p.life) continue;
          const k = dt / p.life, dist = p.v * (1 - Math.pow(1 - k, 3)) * .9;
          sctx.fillStyle = `rgba(247,220,133,${1 - k})`; sctx.beginPath();
          sctx.arc(540 + Math.cos(p.a) * dist, 900 + Math.sin(p.a) * dist + 300 * dt * dt, p.s * (1 - k * .5), 0, 6.283); sctx.fill();
        }
      }
      const inBeat = t >= cfg.beatFrom && t < cfg.beatTo;
      const pump = inBeat ? Math.exp(-((t - cfg.beatFrom) % beat) * 9) : 0;
      let shake = extra.shake || 0;
      for (const h of cfg.hits || []) shake += decay(t, h.t, 14) * (h.amp ?? 14);
      world.style.transform = `translate(${Math.sin(t * 91) * shake}px, ${Math.cos(t * 77) * shake}px) scale(${(extra.zoom || 1) * (1 + pump * .022)})`;
      $('#bgGold').style.opacity = gold ? 1 : 0;
      $('#rays').style.opacity = gold && inBeat ? .6 + pump * .4 : 0;
      $('#rays').style.transform = `rotate(${t * 6}deg) scale(1.6)`;
      $('#flash').style.opacity = Math.max(0, ...(cfg.whiteFlashes || []).map(f => decay(t, f, 10) * .6));
      $('#goldFlash').style.opacity = Math.max(0, ...(cfg.goldFlashes || []).map(f => decay(t, f, 3.5) * .9));
      $('#black').style.opacity = Math.max(seg(t, cfg.duration - .6, cfg.duration), ...(cfg.blackouts || []).map(([a, b]) => win(t, a, b)));
      $('#progress i').style.width = (t / cfg.duration * 100) + '%';
      const hd = easeOut(seg(t, .6, 1.1));
      show($('#handle'), hd * (1 - seg(t, cfg.duration - .6, cfg.duration)), `translateY(${(1 - hd) * -20}px)`);
      return { pump, beat };
    }

    window.DURATION = cfg.duration;
    window.SIZE = { width: 1080, height: 1920 };
    return chrome;
  }

  // Wait for fonts/images, draw frame 0, and loop live when opened in a normal browser.
  function start() {
    window.ready = document.fonts.ready
      .then(() => Promise.all([...document.images].map(i => i.decode().catch(() => {}))))
      .then(() => window.render(0));
    if (!navigator.webdriver) {
      const t0 = performance.now();
      const loop = () => { window.render(((performance.now() - t0) / 1000) % window.DURATION); requestAnimationFrame(loop); };
      window.ready.then(() => requestAnimationFrame(loop));
    }
  }

  // Standard closing scene: logo, two lines, CTA button, url, handle.
  function ctaMarkup(l1, l2, btn = 'Request a meeting →') {
    return `<img class="abs endLogo" src="assets/logo.png" alt=""><div class="abs cx hv endL1">${l1}</div>
      <div class="abs cx hv endL2"><span class="hl">${l2}</span></div><div class="abs cta endBtn">${btn}</div>
      <div class="abs cx url gold-text endUrl">deveraxtech.com</div><div class="abs cx ig endIg">@deveraxtech</div>`;
  }
  function animateCta(root, t, at, pump) {
    const q = (c) => root.querySelector(c);
    const lg = pop(t, at, .3); show(q('.endLogo'), lg.o, `scale(${lg.s})`);
    const a = rise(t, at + .1, .25); show(q('.endL1'), a, `translateY(${(1 - a) * 40}px)`);
    const b = slam(t, at + .5, .22); show(q('.endL2'), b.o, `scale(${b.s})`);
    const c = pop(t, at + 1, .3); show(q('.endBtn'), c.o, `scale(${c.s * (1 + pump * .05)})`);
    q('.endBtn').style.boxShadow = `0 0 ${60 + pump * 70}px rgba(212,175,55,${.45 + pump * .3})`;
    const u = rise(t, at + 1.4, .25); show(q('.endUrl'), u, `translateY(${(1 - u) * 30}px)`);
    const g = rise(t, at + 1.6, .25); show(q('.endIg'), g, `translateY(${(1 - g) * 30}px)`);
  }

  window.kit = { ctaMarkup, animateCta, clamp, seg, easeOut, easeInOut, back, decay, slam, pop, rise, win, show, rng, $, setup, start };
})();
