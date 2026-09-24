import { useEffect, useRef } from 'react';
import dots from '../../src/data/globe-dots.json';

// Gold dotted globe with arcs from Cairo to the markets DevEraXTech serves.
// Canvas 2D, no map libraries: land dots are precomputed (src/data/globe-dots.json).
const HQ = { name: 'Cairo', lon: 31.24, lat: 30.04, label: [-12, -12, 'right'] };
// label: [dx, dy, align] in CSS pixels, tuned so the Gulf cluster stays legible.
const CITIES = [
  { name: 'Toronto', lon: -79.38, lat: 43.65, label: [8, -9, 'left'] },
  { name: 'New York', lon: -74.0, lat: 40.71, label: [8, 8, 'left'] },
  { name: 'Kuwait City', lon: 47.98, lat: 29.37, label: [0, -15, 'center'] },
  { name: 'Doha', lon: 51.53, lat: 25.29, label: [10, 0, 'left'] },
  { name: 'Dubai', lon: 55.27, lat: 25.2, label: [10, 13, 'left'] },
  { name: 'Riyadh', lon: 46.68, lat: 24.71, label: [-6, 16, 'right'] }
];

const RAD = Math.PI / 180;
const GOLD = '242,209,123';

function toVec(lon, lat) {
  const l = lon * RAD;
  const p = lat * RAD;
  return [Math.cos(p) * Math.cos(l), Math.cos(p) * Math.sin(l), Math.sin(p)];
}

// Great-circle interpolation between unit vectors a and b.
function slerp(a, b, t) {
  const dot = Math.min(1, Math.max(-1, a[0] * b[0] + a[1] * b[1] + a[2] * b[2]));
  const w = Math.acos(dot);
  const s = Math.sin(w) || 1;
  const k1 = Math.sin((1 - t) * w) / s;
  const k2 = Math.sin(t * w) / s;
  return [a[0] * k1 + b[0] * k2, a[1] * k1 + b[1] * k2, a[2] * k1 + b[2] * k2];
}

const DOT_VECS = dots.map(([lon, lat]) => toVec(lon, lat));
const HQ_VEC = toVec(HQ.lon, HQ.lat);
const ARCS = CITIES.map((c, i) => {
  const to = toVec(c.lon, c.lat);
  const angle = Math.acos(HQ_VEC[0] * to[0] + HQ_VEC[1] * to[1] + HQ_VEC[2] * to[2]);
  const lift = 0.06 + angle * 0.16; // longer routes arc higher
  const pts = [];
  for (let s = 0; s <= 48; s += 1) {
    const t = s / 48;
    const v = slerp(HQ_VEC, to, t);
    const h = 1 + Math.sin(Math.PI * t) * lift;
    pts.push([v[0] * h, v[1] * h, v[2] * h]);
  }
  return { city: c, to, pts, phase: i / CITIES.length };
});

export default function GoldGlobe({ className = '' }) {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return undefined;
    const ctx = canvas.getContext('2d');
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    let size = 0;
    let dpr = 1;
    let raf = 0;
    let visible = true;
    const start = performance.now();

    const resize = () => {
      const rect = canvas.getBoundingClientRect();
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      size = Math.max(160, Math.round(rect.width));
      canvas.width = size * dpr;
      canvas.height = size * dpr;
    };

    const draw = (now) => {
      const t = reduce ? 0 : (now - start) / 1000;
      const W = size * dpr;
      const cx = W / 2;
      const cy = W / 2;
      const R = W * 0.4;
      // Gentle sway that keeps Cairo, the Gulf and North America in view.
      const lon0 = (-10 + Math.sin(t * 0.12) * 16) * RAD;
      const lat0 = 24 * RAD;
      const cl = Math.cos(lon0);
      const sl = Math.sin(lon0);
      const cp = Math.cos(lat0);
      const sp = Math.sin(lat0);
      const project = (v) => {
        const x1 = v[0] * cl + v[1] * sl;
        const y1 = -v[0] * sl + v[1] * cl;
        const depth = x1 * cp + v[2] * sp;
        const up = -x1 * sp + v[2] * cp;
        return [cx + R * y1, cy - R * up, depth, Math.hypot(y1, up)];
      };

      ctx.clearRect(0, 0, W, W);

      // Halo and sphere.
      const halo = ctx.createRadialGradient(cx, cy, R * 0.9, cx, cy, R * 1.35);
      halo.addColorStop(0, `rgba(${GOLD},0.16)`);
      halo.addColorStop(1, `rgba(${GOLD},0)`);
      ctx.fillStyle = halo;
      ctx.fillRect(0, 0, W, W);

      const body = ctx.createRadialGradient(cx - R * 0.35, cy - R * 0.4, R * 0.1, cx, cy, R);
      body.addColorStop(0, '#1d1809');
      body.addColorStop(0.6, '#0d0b06');
      body.addColorStop(1, '#050505');
      ctx.beginPath();
      ctx.arc(cx, cy, R, 0, Math.PI * 2);
      ctx.fillStyle = body;
      ctx.fill();
      ctx.lineWidth = 1.2 * dpr;
      ctx.strokeStyle = `rgba(${GOLD},0.35)`;
      ctx.stroke();

      // Graticule.
      ctx.lineWidth = 0.6 * dpr;
      ctx.strokeStyle = `rgba(${GOLD},0.07)`;
      const line = (fn) => {
        ctx.beginPath();
        let pen = false;
        for (let s = 0; s <= 90; s += 1) {
          const [x, y, depth] = project(fn(s / 90));
          if (depth > 0) {
            if (pen) ctx.lineTo(x, y); else ctx.moveTo(x, y);
            pen = true;
          } else pen = false;
        }
        ctx.stroke();
      };
      for (let lon = -180; lon < 180; lon += 30) line(u => toVec(lon, -85 + u * 170));
      for (let lat = -60; lat <= 60; lat += 30) line(u => toVec(-180 + u * 360, lat));

      // Land dots.
      for (let i = 0; i < DOT_VECS.length; i += 1) {
        const [x, y, depth] = project(DOT_VECS[i]);
        if (depth <= 0.02) continue;
        const r = (0.5 + depth * 0.7) * dpr;
        ctx.fillStyle = `rgba(${GOLD},${(0.16 + depth * 0.62).toFixed(3)})`;
        ctx.beginPath();
        ctx.arc(x, y, r, 0, Math.PI * 2);
        ctx.fill();
      }

      // Arcs with a travelling light.
      ARCS.forEach(arc => {
        const P = arc.pts.map(project);
        const hidden = p => p[2] < 0 && p[3] < 1;
        ctx.lineWidth = 1.1 * dpr;
        ctx.strokeStyle = `rgba(${GOLD},0.5)`;
        ctx.beginPath();
        let pen = false;
        P.forEach(p => {
          if (hidden(p)) { pen = false; return; }
          if (pen) ctx.lineTo(p[0], p[1]); else ctx.moveTo(p[0], p[1]);
          pen = true;
        });
        ctx.stroke();

        const cycle = reduce ? 1 : ((t * 0.28 + arc.phase) % 1.4) / 1.4 * 1.4;
        if (cycle <= 1) {
          const head = Math.floor(cycle * (P.length - 1));
          const tail = Math.max(0, head - 9);
          for (let k = tail; k < head; k += 1) {
            const a = P[k];
            const b = P[k + 1];
            if (hidden(a) || hidden(b)) continue;
            const f = (k - tail) / Math.max(1, head - tail);
            ctx.strokeStyle = `rgba(255,241,191,${(0.15 + f * 0.85).toFixed(3)})`;
            ctx.lineWidth = (1 + f * 1.6) * dpr;
            ctx.beginPath();
            ctx.moveTo(a[0], a[1]);
            ctx.lineTo(b[0], b[1]);
            ctx.stroke();
          }
        }
      });

      // City markers and labels.
      ctx.font = `500 ${10.5 * dpr}px "Inter Variable", Inter, system-ui, sans-serif`;
      ctx.textBaseline = 'middle';
      const marker = (vec, label, isHQ, [lx, ly, align]) => {
        const [x, y, depth] = project(vec);
        if (depth <= 0.05) return;
        const pulse = isHQ && !reduce ? (Math.sin(t * 2.4) + 1) / 2 : 0.5;
        if (isHQ) {
          ctx.beginPath();
          ctx.arc(x, y, (7 + pulse * 7) * dpr, 0, Math.PI * 2);
          ctx.strokeStyle = `rgba(${GOLD},${(0.5 - pulse * 0.4).toFixed(3)})`;
          ctx.lineWidth = 1 * dpr;
          ctx.stroke();
        }
        const glow = ctx.createRadialGradient(x, y, 0, x, y, (isHQ ? 9 : 6) * dpr);
        glow.addColorStop(0, 'rgba(255,241,191,0.95)');
        glow.addColorStop(1, 'rgba(255,241,191,0)');
        ctx.fillStyle = glow;
        ctx.beginPath();
        ctx.arc(x, y, (isHQ ? 9 : 6) * dpr, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = `rgba(${GOLD},${(0.45 + depth * 0.5).toFixed(3)})`;
        // Keep labels inside the canvas: flip to the other side of the marker if needed.
        const width = ctx.measureText(label).width;
        let tx = x + lx * dpr;
        let ta = align;
        if (ta === 'left' && tx + width > W - 4 * dpr) { tx = x - Math.abs(lx) * dpr; ta = 'right'; }
        if (ta === 'right' && tx - width < 4 * dpr) { tx = x + Math.abs(lx) * dpr; ta = 'left'; }
        if (ta === 'center') tx = Math.min(W - 4 * dpr - width / 2, Math.max(4 * dpr + width / 2, tx));
        ctx.textAlign = ta;
        ctx.fillText(label, tx, y + ly * dpr);
      };
      CITIES.forEach(c => marker(toVec(c.lon, c.lat), c.name, false, c.label));
      marker(HQ_VEC, 'Cairo HQ', true, HQ.label);
    };

    const loop = (now) => {
      draw(now);
      if (!reduce && visible && !document.hidden) raf = requestAnimationFrame(loop);
    };
    const restart = () => {
      cancelAnimationFrame(raf);
      if (!reduce && visible && !document.hidden) raf = requestAnimationFrame(loop);
    };

    resize();
    draw(performance.now());
    restart();

    const ro = new ResizeObserver(() => { resize(); draw(performance.now()); });
    ro.observe(canvas);
    const io = new IntersectionObserver(([entry]) => { visible = entry.isIntersecting; restart(); });
    io.observe(canvas);
    document.addEventListener('visibilitychange', restart);

    return () => {
      cancelAnimationFrame(raf);
      ro.disconnect();
      io.disconnect();
      document.removeEventListener('visibilitychange', restart);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className={`gold-globe ${className}`}
      role="img"
      aria-label="Globe showing DevEraXTech in Cairo connected to Toronto, New York, Dubai, Riyadh, Kuwait City and Doha"
    />
  );
}
