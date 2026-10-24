import { clamp, ease, inv } from './util.js';

// Deterministic typography, composited in 2D over the rendered plate.
// Sizes are authored against a 1080-wide frame and scale with the output width.
// Platform-safe area (TikTok / Reels UI): x 100–940, y 260–1480 at 1080×1920.
export const SAFE = { left: 100, right: 940, top: 260, bottom: 1480, cx: 520 };

export const FONT = {
  light: '"InterDisplay Light"',
  regular: '"InterDisplay Regular"',
  medium: '"InterDisplay Medium"',
  semibold: '"InterDisplay SemiBold"',
};

/**
 * spec: { lines, start, end, y, size, family, tracking, color, inDur, outDur, stagger, align }
 * y is the baseline of the first line in 1080-space px.
 */
export function drawTitle(ctx, W, t, spec) {
  const k = W / 1080;
  const {
    lines, start, end,
    y = 1300, size = 58, family = FONT.medium, tracking = 0.16, lineGap = 1.28,
    color = '233,236,239', inDur = 0.55, outDur = 0.32, stagger = 0.09,
    shadow = 0.55, cx = SAFE.cx,
  } = spec;
  if (t < start - 0.01 || t > end + 0.01) return;
  const maxW = (SAFE.right - SAFE.left) * k;

  ctx.save();
  ctx.textAlign = 'center';
  ctx.textBaseline = 'alphabetic';

  // Common size so every line in the block shares one scale.
  let px = size * k;
  ctx.font = `${px}px ${family}`;
  ctx.letterSpacing = `${tracking * px}px`;
  const widest = Math.max(...lines.map((l) => ctx.measureText(l).width));
  if (widest > maxW) px *= maxW / widest;

  const outT = clamp((t - (end - outDur)) / outDur);
  lines.forEach((line, i) => {
    const t0 = start + i * stagger;
    const p = ease.outQuart(inv(t0, t0 + inDur, t));
    if (p <= 0) return;
    const trackNow = tracking + 0.05 * (1 - p) + 0.035 * ease.inCubic(outT);
    ctx.font = `${px}px ${family}`;
    ctx.letterSpacing = `${trackNow * px}px`;
    const by = y * k + i * px * lineGap;
    const rise = (1 - p) * px * 0.42 + ease.inCubic(outT) * px * 0.12;
    const alpha = p * (1 - ease.inOutCubic(outT));

    // Reveal wipe: each line is unmasked from its baseline upward.
    ctx.save();
    ctx.beginPath();
    const top = by - px * 1.05;
    ctx.rect(0, top + (1 - p) * px * 1.25, W, px * 1.5);
    ctx.clip();
    // tracking adds trailing space after the final glyph; offset to stay optically centred
    const x = cx * k + (trackNow * px) / 2;
    if (shadow > 0) {
      ctx.shadowColor = `rgba(0,0,0,${shadow * alpha})`;
      ctx.shadowBlur = 28 * k;
    }
    ctx.fillStyle = `rgba(${color},${alpha})`;
    ctx.fillText(line, x, by - rise);
    ctx.restore();
  });
  ctx.restore();
}

export async function loadFonts(base) {
  const faces = [
    ['InterDisplay Light', 'InterDisplay-Light.otf'],
    ['InterDisplay Regular', 'InterDisplay-Regular.otf'],
    ['InterDisplay Medium', 'InterDisplay-Medium.otf'],
    ['InterDisplay SemiBold', 'InterDisplay-SemiBold.otf'],
  ];
  for (const [name, file] of faces) {
    const f = new FontFace(name, `url(${base}/${file})`);
    await f.load();
    document.fonts.add(f);
  }
}

// Soft cinematic darkening behind a text block so type stays readable over busy plates.
export function scrim(ctx, W, H, amount, y = 1200, height = 520) {
  if (amount <= 0) return;
  const k = W / 1080;
  const g = ctx.createLinearGradient(0, (y - height * 0.6) * k, 0, (y + height * 0.6) * k);
  g.addColorStop(0, 'rgba(0,0,0,0)');
  g.addColorStop(0.5, `rgba(0,0,0,${0.55 * amount})`);
  g.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = g;
  ctx.fillRect(0, (y - height * 0.6) * k, W, height * 1.2 * k);
}
