// Procedural 2D surfaces drawn into canvases and used as textures.
// Everything here is deliberately conceptual: no real brands, clients or products.

export function canvas(w, h) {
  const c = document.createElement('canvas');
  c.width = w; c.height = h;
  return c;
}

export function roundRect(g, x, y, w, h, r) {
  g.beginPath();
  g.roundRect(x, y, w, h, r);
}

// The "generic flat website" that Scene 01 rejects: grey bars, a stock hero, a default button.
export function drawGenericSite(g, w, h) {
  const s = w / 900;
  g.fillStyle = '#e6e7e9'; g.fillRect(0, 0, w, h);
  // nav
  g.fillStyle = '#ffffff'; g.fillRect(0, 0, w, 110 * s);
  g.fillStyle = '#b8bcc2'; g.fillRect(50 * s, 38 * s, 150 * s, 36 * s);
  g.fillStyle = '#7d828a'; g.font = `600 ${20 * s}px Arial, sans-serif`; g.textAlign = 'center';
  g.fillText('LOGO', 125 * s, 63 * s);
  g.fillStyle = '#c9ccd1';
  for (let i = 0; i < 4; i++) g.fillRect((470 + i * 100) * s, 50 * s, 70 * s, 14 * s);
  // hero with the stock-photo placeholder glyph
  g.fillStyle = '#c4c8ce'; g.fillRect(0, 110 * s, w, 620 * s);
  g.strokeStyle = '#aeb3ba'; g.lineWidth = 10 * s;
  g.beginPath(); g.moveTo(250 * s, 560 * s); g.lineTo(380 * s, 400 * s); g.lineTo(470 * s, 500 * s);
  g.lineTo(540 * s, 430 * s); g.lineTo(660 * s, 560 * s); g.stroke();
  g.beginPath(); g.arc(600 * s, 300 * s, 38 * s, 0, Math.PI * 2); g.stroke();
  g.fillStyle = '#4a4f57'; g.font = `700 ${54 * s}px Arial, sans-serif`;
  g.fillText('Welcome to Our Website', w / 2, 830 * s);
  g.fillStyle = '#a3a8af';
  g.fillRect(170 * s, 870 * s, 560 * s, 16 * s); g.fillRect(240 * s, 902 * s, 420 * s, 16 * s);
  g.fillStyle = '#6b84a6'; roundRect(g, 330 * s, 950 * s, 240 * s, 66 * s, 6 * s); g.fill();
  g.fillStyle = '#ffffff'; g.font = `700 ${22 * s}px Arial, sans-serif`;
  g.fillText('LEARN MORE', w / 2, 992 * s);
  // three cards
  for (let i = 0; i < 3; i++) {
    const x = (50 + i * 275) * s;
    g.fillStyle = '#f4f5f6'; g.fillRect(x, 1080 * s, 250 * s, 300 * s);
    g.fillStyle = '#c9ccd1'; g.beginPath(); g.arc(x + 125 * s, 1160 * s, 42 * s, 0, Math.PI * 2); g.fill();
    g.fillStyle = '#b3b7bd'; g.fillRect(x + 40 * s, 1240 * s, 170 * s, 14 * s);
    g.fillStyle = '#d0d3d7';
    for (let j = 0; j < 3; j++) g.fillRect(x + 30 * s, (1278 + j * 26) * s, 190 * s, 10 * s);
  }
  // footer
  g.fillStyle = '#5e636b'; g.fillRect(0, 1440 * s, w, h - 1440 * s);
  g.fillStyle = '#7a7f87';
  for (let i = 0; i < 4; i++) g.fillRect((60 + i * 200) * s, 1490 * s, 140 * s, 12 * s);
}
