// Conceptual interfaces for Scenes 03 and 05. They are illustrations of craft, not
// products: placeholder names, no client marks, no fabricated metrics.
import { clamp, ease, inv, smooth } from './util.js';

export const UI = {
  bg: '#0c0e11', panel: '#14171b', panel2: '#1b1f24', line: 'rgba(185,190,197,0.16)', line2: 'rgba(185,190,197,0.32)',
  text: '#e9ecef', sub: '#8d939b', dim: '#5a6068', accent: '#8ea6bf', silver: '#b9bec5',
};
const F = (w, px) => `${px}px "InterDisplay ${w}"`;

function rr(g, x, y, w, h, r) { g.beginPath(); g.roundRect(x, y, w, h, r); }
function track(g, px, em) { g.letterSpacing = `${em * px}px`; }

// A brushed-titanium object drawn as an image: the "hero photo" of the concept site.
export function titaniumArt(g, x, y, w, h, t = 0) {
  g.save();
  rr(g, x, y, w, h, Math.min(w, h) * 0.04); g.clip();
  const bg = g.createLinearGradient(x, y, x, y + h);
  bg.addColorStop(0, '#16191d'); bg.addColorStop(1, '#0a0b0d');
  g.fillStyle = bg; g.fillRect(x, y, w, h);
  const cx = x + w * 0.5, cy = y + h * 0.52, R = Math.min(w, h) * 0.34;
  // ring body
  for (let i = 0; i < 2; i++) {
    const rg = g.createLinearGradient(cx - R, cy - R, cx + R, cy + R);
    const s = (t * 0.15) % 1;
    rg.addColorStop(0, '#2a2e33'); rg.addColorStop(clamp(0.3 + s * 0.2), '#e9ecef');
    rg.addColorStop(clamp(0.45 + s * 0.2), '#5d636b'); rg.addColorStop(0.8, '#b9bec5'); rg.addColorStop(1, '#25292e');
    g.strokeStyle = rg; g.lineWidth = R * (i ? 0.05 : 0.28);
    g.beginPath(); g.ellipse(cx, cy, R * (i ? 0.78 : 1), R * (i ? 0.78 : 1) * 0.92, -0.3, 0, Math.PI * 2); g.stroke();
  }
  const glow = g.createRadialGradient(cx, cy + R * 1.4, 0, cx, cy + R * 1.4, R * 1.6);
  glow.addColorStop(0, 'rgba(142,166,191,0.16)'); glow.addColorStop(1, 'rgba(142,166,191,0)');
  g.fillStyle = glow; g.fillRect(x, y, w, h);
  g.restore();
}

// Concept website modules: each is drawn into its own canvas so it can fly in on its own axis.
export const SITE_MODULES = [
  { id: 'nav', w: 1.8, h: 0.16, x: 0, y: 1.42 },
  { id: 'headline', w: 1.8, h: 0.62, x: 0, y: 0.98 },
  { id: 'art', w: 1.8, h: 1.0, x: 0, y: 0.1 },
  { id: 'lede', w: 1.8, h: 0.3, x: 0, y: -0.58 },
  { id: 'card0', w: 0.56, h: 0.62, x: -0.62, y: -1.12 },
  { id: 'card1', w: 0.56, h: 0.62, x: 0, y: -1.12 },
  { id: 'card2', w: 0.56, h: 0.62, x: 0.62, y: -1.12 },
];

export function drawSiteModule(id, g, W, H) {
  g.clearRect(0, 0, W, H);
  const u = W / 1.8; // px per world unit for full-width modules
  g.textBaseline = 'alphabetic';
  if (id === 'nav') {
    g.fillStyle = UI.text; g.font = F('SemiBold', H * 0.3); track(g, H * 0.3, 0.32); g.textAlign = 'left';
    g.fillText('CONCEPT', H * 0.55, H * 0.6);
    g.strokeStyle = UI.silver; g.lineWidth = 2; g.strokeRect(H * 0.2, H * 0.32, H * 0.22, H * 0.22);
    g.font = F('Regular', H * 0.24); track(g, H * 0.24, 0.12); g.fillStyle = UI.sub; g.textAlign = 'right';
    g.fillText('Index      Craft      Studio', W - H * 0.3, H * 0.6);
    g.fillStyle = UI.line; g.fillRect(0, H - 2, W, 2);
  } else if (id === 'headline') {
    g.fillStyle = UI.text; g.textAlign = 'left';
    const px = H * 0.3; g.font = F('Light', px); track(g, px, -0.02);
    g.fillText('Quiet power,', u * 0.06, H * 0.42);
    g.fillText('precisely made.', u * 0.06, H * 0.82);
    g.font = F('Medium', H * 0.075); track(g, H * 0.075, 0.3); g.fillStyle = UI.accent; g.textAlign = 'right';
    g.fillText('CONCEPT INTERFACE · 01', W - u * 0.06, H * 0.16);
  } else if (id === 'art') {
    titaniumArt(g, u * 0.06, 0, W - u * 0.12, H, 0.6);
  } else if (id === 'lede') {
    g.fillStyle = UI.sub;
    for (let i = 0; i < 3; i++) g.fillRect(u * 0.06, H * (0.2 + i * 0.17), u * (i === 2 ? 0.7 : 1.05), H * 0.06);
    g.strokeStyle = UI.line2; g.lineWidth = 3; rr(g, W - u * 0.5, H * 0.22, u * 0.44, H * 0.5, H * 0.25); g.stroke();
    g.fillStyle = UI.text; g.font = F('Medium', H * 0.17); track(g, H * 0.17, 0.2); g.textAlign = 'center';
    g.fillText('EXPLORE', W - u * 0.28, H * 0.53);
  } else if (id.startsWith('card')) {
    const k = +id.slice(4);
    g.fillStyle = UI.panel; rr(g, 4, 4, W - 8, H - 8, W * 0.05); g.fill();
    g.strokeStyle = UI.line; g.lineWidth = 2; g.stroke();
    g.strokeStyle = UI.silver; g.lineWidth = W * 0.012;
    const cx = W * 0.22, cy = H * 0.28, r = W * 0.09;
    g.beginPath();
    if (k === 0) { g.rect(cx - r, cy - r, r * 2, r * 2); g.moveTo(cx - r, cy); g.lineTo(cx + r, cy); }
    else if (k === 1) { g.arc(cx, cy, r, 0, Math.PI * 2); g.moveTo(cx - r * 0.5, cy); g.lineTo(cx + r * 0.5, cy); }
    else { g.moveTo(cx - r, cy + r); g.lineTo(cx, cy - r); g.lineTo(cx + r, cy + r); g.closePath(); }
    g.stroke();
    g.fillStyle = UI.text; g.font = F('Medium', W * 0.075); track(g, W * 0.075, 0.04); g.textAlign = 'left';
    g.fillText(['Architecture', 'Interface', 'Motion'][k], W * 0.13, H * 0.62);
    g.fillStyle = UI.dim;
    g.fillRect(W * 0.13, H * 0.72, W * 0.7, H * 0.03); g.fillRect(W * 0.13, H * 0.8, W * 0.5, H * 0.03);
  }
}

// ---- Phone screens (Scene 05). Each takes progress 0..1 for its own entrance animation.
export function drawPhoneApp(g, W, H, t, enter = 1) {
  g.fillStyle = UI.bg; g.fillRect(0, 0, W, H);
  const p = (d) => ease.outQuart(clamp(enter * 1.6 - d));
  g.save(); g.globalAlpha = p(0);
  g.fillStyle = UI.sub; g.font = F('Medium', W * 0.035); track(g, W * 0.035, 0.24); g.textAlign = 'left';
  g.fillText('GOOD EVENING', W * 0.08, H * 0.1);
  g.fillStyle = UI.text; g.font = F('Light', W * 0.09); track(g, W * 0.09, -0.01);
  g.fillText('Your space', W * 0.08, H * 0.155);
  g.restore();
  // ring dial
  g.save(); g.globalAlpha = p(0.15);
  const cx = W * 0.5, cy = H * 0.36, R = W * 0.27;
  g.strokeStyle = UI.line; g.lineWidth = W * 0.035; g.beginPath(); g.arc(cx, cy, R, 0, Math.PI * 2); g.stroke();
  const a = -Math.PI / 2, sweep = Math.PI * 2 * 0.68 * ease.outCubic(clamp(enter * 1.3 - 0.2));
  const rg = g.createLinearGradient(cx - R, cy - R, cx + R, cy + R);
  rg.addColorStop(0, '#e9ecef'); rg.addColorStop(1, '#8ea6bf');
  g.strokeStyle = rg; g.lineCap = 'round'; g.beginPath(); g.arc(cx, cy, R, a, a + sweep); g.stroke();
  g.fillStyle = UI.text; g.font = F('Light', W * 0.06); g.textAlign = 'center'; track(g, W * 0.06, 0.02);
  g.fillText('Balanced', cx, cy + W * 0.02);
  g.restore();
  // cards
  ['Climate', 'Lighting', 'Access'].forEach((label, i) => {
    g.save(); g.globalAlpha = p(0.3 + i * 0.12);
    const y = H * (0.56 + i * 0.12) + (1 - p(0.3 + i * 0.12)) * H * 0.03;
    g.fillStyle = UI.panel; rr(g, W * 0.07, y, W * 0.86, H * 0.1, W * 0.04); g.fill();
    g.strokeStyle = UI.line; g.lineWidth = 2; g.stroke();
    g.fillStyle = UI.text; g.font = F('Medium', W * 0.045); track(g, W * 0.045, 0.02); g.textAlign = 'left';
    g.fillText(label, W * 0.13, y + H * 0.058);
    // toggle
    g.fillStyle = i === 1 ? '#3a4048' : '#8ea6bf';
    rr(g, W * 0.72, y + H * 0.032, W * 0.14, H * 0.036, H * 0.018); g.fill();
    g.fillStyle = UI.text; g.beginPath(); g.arc(i === 1 ? W * 0.75 : W * 0.83, y + H * 0.05, H * 0.014, 0, Math.PI * 2); g.fill();
    g.restore();
  });
  tabBar(g, W, H);
}

export function drawPhoneStore(g, W, H, t, enter = 1) {
  g.fillStyle = UI.bg; g.fillRect(0, 0, W, H);
  const p = (d) => ease.outQuart(clamp(enter * 1.6 - d));
  g.save(); g.globalAlpha = p(0);
  titaniumArt(g, W * 0.06, H * 0.07 + (1 - p(0)) * H * 0.04, W * 0.88, H * 0.42, t);
  g.restore();
  g.save(); g.globalAlpha = p(0.2);
  g.fillStyle = UI.accent; g.font = F('Medium', W * 0.032); track(g, W * 0.032, 0.3); g.textAlign = 'left';
  g.fillText('OBJECT 01 · CONCEPT', W * 0.08, H * 0.55);
  g.fillStyle = UI.text; g.font = F('Light', W * 0.085); track(g, W * 0.085, -0.01);
  g.fillText('Titanium Ring', W * 0.08, H * 0.605);
  g.fillStyle = UI.dim;
  g.fillRect(W * 0.08, H * 0.64, W * 0.78, H * 0.008); g.fillRect(W * 0.08, H * 0.66, W * 0.6, H * 0.008);
  g.restore();
  // finish swatches
  g.save(); g.globalAlpha = p(0.35);
  ['#b9bec5', '#3a3f46', '#e9ecef'].forEach((c, i) => {
    g.fillStyle = c; g.beginPath(); g.arc(W * (0.12 + i * 0.1), H * 0.71, W * 0.03, 0, Math.PI * 2); g.fill();
    if (i === 0) { g.strokeStyle = UI.text; g.lineWidth = 2; g.beginPath(); g.arc(W * 0.12, H * 0.71, W * 0.042, 0, Math.PI * 2); g.stroke(); }
  });
  g.restore();
  g.save(); g.globalAlpha = p(0.5);
  g.fillStyle = UI.text; rr(g, W * 0.07, H * 0.77, W * 0.86, H * 0.065, H * 0.0325); g.fill();
  g.fillStyle = UI.bg; g.font = F('SemiBold', W * 0.04); track(g, W * 0.04, 0.2); g.textAlign = 'center';
  g.fillText('ADD TO BAG', W * 0.5, H * 0.812);
  g.restore();
  tabBar(g, W, H);
}

function tabBar(g, W, H) {
  g.fillStyle = UI.line; g.fillRect(0, H * 0.9, W, 2);
  for (let i = 0; i < 4; i++) {
    g.strokeStyle = i === 0 ? UI.text : UI.dim; g.lineWidth = W * 0.008;
    g.beginPath(); g.arc(W * (0.17 + i * 0.22), H * 0.945, W * 0.025, 0, Math.PI * 2); g.stroke();
  }
}

// Dashboard (landscape). `lines` 0..1 lights the connection graph that becomes Scene 06's strands.
export function drawDashboard(g, W, H, t, enter = 1, lines = 0) {
  g.fillStyle = UI.bg; g.fillRect(0, 0, W, H);
  const p = (d) => ease.outQuart(clamp(enter * 1.5 - d));
  const pad = H * 0.07;
  // sidebar
  g.save(); g.globalAlpha = p(0);
  g.fillStyle = UI.panel; g.fillRect(0, 0, W * 0.12, H);
  for (let i = 0; i < 5; i++) { g.fillStyle = i === 1 ? UI.text : UI.dim; g.fillRect(W * 0.035, H * (0.18 + i * 0.11), W * 0.05, H * 0.018); }
  g.restore();
  const X0 = W * 0.12 + pad;
  g.save(); g.globalAlpha = p(0.05);
  g.fillStyle = UI.text; g.font = F('Light', H * 0.07); track(g, H * 0.07, -0.01); g.textAlign = 'left';
  g.fillText('Systems overview', X0, H * 0.14);
  g.fillStyle = UI.accent; g.font = F('Medium', H * 0.026); track(g, H * 0.026, 0.3);
  g.fillText('CONCEPT DASHBOARD', X0, H * 0.065);
  g.restore();
  // area chart (shape only; no fabricated values)
  g.save(); g.globalAlpha = p(0.15);
  const cw = W * 0.46, ch = H * 0.36, cy = H * 0.22;
  g.fillStyle = UI.panel; rr(g, X0, cy, cw, ch, H * 0.02); g.fill();
  g.beginPath();
  const n = 48, grow = ease.outCubic(clamp(enter * 1.4 - 0.2));
  for (let i = 0; i <= n; i++) {
    const x = X0 + cw * 0.05 + (cw * 0.9 * i) / n;
    const v = 0.5 + 0.22 * Math.sin(i * 0.31 + 1.2) + 0.12 * Math.sin(i * 0.77) + 0.004 * i;
    const y = cy + ch * 0.88 - ch * 0.7 * v * grow;
    if (i === 0) g.moveTo(x, y); else g.lineTo(x, y);
  }
  g.strokeStyle = UI.text; g.lineWidth = H * 0.006; g.stroke();
  g.lineTo(X0 + cw * 0.95, cy + ch * 0.88); g.lineTo(X0 + cw * 0.05, cy + ch * 0.88); g.closePath();
  const ag = g.createLinearGradient(0, cy, 0, cy + ch);
  ag.addColorStop(0, 'rgba(142,166,191,0.35)'); ag.addColorStop(1, 'rgba(142,166,191,0)');
  g.fillStyle = ag; g.fill();
  g.restore();
  // bars
  g.save(); g.globalAlpha = p(0.25);
  const bx = X0, by = cy + ch + pad * 0.6, bw = cw, bh = H - by - pad;
  g.fillStyle = UI.panel; rr(g, bx, by, bw, bh, H * 0.02); g.fill();
  for (let i = 0; i < 12; i++) {
    const v = (0.35 + 0.5 * Math.abs(Math.sin(i * 1.7 + 0.4))) * ease.outCubic(clamp(enter * 1.5 - 0.3 - i * 0.02));
    g.fillStyle = i === 7 ? UI.text : '#3a414a';
    g.fillRect(bx + bw * (0.06 + i * 0.075), by + bh * 0.88 - bh * 0.7 * v, bw * 0.04, bh * 0.7 * v);
  }
  g.restore();
  // connection graph: the integrations map
  g.save(); g.globalAlpha = p(0.3);
  const gx = X0 + cw + pad * 0.6, gw = W - gx - pad, gy = cy, gh = H - cy - pad;
  g.fillStyle = UI.panel; rr(g, gx, gy, gw, gh, H * 0.02); g.fill();
  const nodes = GRAPH.map(([u, v]) => [gx + gw * u, gy + gh * v]);
  for (const [a, b] of GRAPH_EDGES) {
    const [x0, y0] = nodes[a], [x1, y1] = nodes[b];
    g.strokeStyle = `rgba(185,190,197,${0.25 + 0.75 * lines})`; g.lineWidth = H * (0.003 + 0.004 * lines);
    if (lines > 0) { g.shadowColor = 'rgba(233,236,239,0.9)'; g.shadowBlur = H * 0.03 * lines; }
    g.beginPath(); g.moveTo(x0, y0);
    g.bezierCurveTo((x0 + x1) / 2, y0, (x0 + x1) / 2, y1, x1, y1); g.stroke();
  }
  g.shadowBlur = 0;
  nodes.forEach(([x, y], i) => {
    g.fillStyle = i === 0 ? UI.text : UI.panel2; g.strokeStyle = UI.silver; g.lineWidth = H * 0.004;
    g.beginPath(); g.arc(x, y, H * (i === 0 ? 0.028 : 0.018), 0, Math.PI * 2); g.fill(); g.stroke();
  });
  g.restore();
}

export const GRAPH = [[0.5, 0.5], [0.18, 0.2], [0.82, 0.22], [0.15, 0.78], [0.85, 0.8], [0.5, 0.12], [0.5, 0.9]];
export const GRAPH_EDGES = [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [1, 5], [2, 5], [3, 6], [4, 6]];
