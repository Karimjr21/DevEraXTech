import { useEffect, useRef } from 'react';

// Gold circuit-board hero art: traces run in from the screen edges to a faint "processor"
// outline behind the headline, with light pulses travelling inward along them.
// Pure SVG + CSS (no WebGL). The layout is generated from a fixed seed so the server-rendered
// markup and the browser render are identical.

function rng(seed) {
  let s = seed >>> 0;
  return () => {
    s = (s + 0x6d2b79f5) >>> 0;
    let t = s;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const r1 = (n) => Math.round(n * 10) / 10;

// Builds traces fanning out from one side of the chip. `axis` is 'x' for left/right sides
// (traces leave horizontally) and 'y' for top/bottom sides (traces leave vertically).
function fan({ rand, W, H, chip, side, count }) {
  const { x0, y0, x1, y1, cx, cy } = chip;
  const horizontal = side === 'left' || side === 'right';
  const dir = side === 'left' || side === 'top' ? -1 : 1;
  const edgeStart = horizontal ? (side === 'left' ? x0 : x1) : (side === 'top' ? y0 : y1);
  const span = horizontal ? [y0 + 40, y1 - 40] : [x0 + 60, x1 - 60];
  const center = horizontal ? cy : cx;
  const half = (span[1] - span[0]) / 2;
  const room = horizontal ? (side === 'left' ? x0 : W - x1) : (side === 'top' ? y0 : H - y1);
  const traces = [];

  for (let i = 0; i < count; i += 1) {
    const along = span[0] + ((span[1] - span[0]) * (i + 0.5)) / count;
    const offset = along - center;
    const outer = Math.min(1, Math.abs(offset) / half);
    // Outer pins bend earlier and spread further so the fan never crosses itself.
    const run1 = 26 + (1 - outer) * room * 0.22 + rand() * 14;
    const spread = offset * (0.55 + rand() * 0.35);
    const runEnd = room * (0.45 + rand() * 0.6);
    const offEdge = runEnd > room * 0.95;

    const p = (a, b) => (horizontal ? [edgeStart + dir * a, b] : [b, edgeStart + dir * a]);
    const pin = p(0, along);
    const bendA = p(run1, along);
    const bendB = p(run1 + Math.abs(spread), along + spread);
    const end = p(offEdge ? room + 40 : Math.max(run1 + Math.abs(spread) + 30, runEnd), along + spread);

    // Path runs from the outer end to the chip so pulses travel inward.
    const d = `M${r1(end[0])} ${r1(end[1])} L${r1(bendB[0])} ${r1(bendB[1])} L${r1(bendA[0])} ${r1(bendA[1])} L${r1(pin[0])} ${r1(pin[1])}`;
    traces.push({
      d,
      pin,
      pad: offEdge ? null : end,
      delay: r1(0.15 + rand() * 1.1),
      pulse: rand() < 0.7,
      pulseDur: r1(3.2 + rand() * 3.6),
      pulseDelay: r1(1.6 + rand() * 5),
      horizontal
    });
  }
  return traces;
}

function layout({ W, H, chipW, chipH, counts, seed }) {
  const rand = rng(seed);
  const cx = W / 2;
  const cy = H * 0.53;
  const chip = { x0: cx - chipW / 2, y0: cy - chipH / 2, x1: cx + chipW / 2, y1: cy + chipH / 2, cx, cy };
  const traces = [
    ...fan({ rand, W, H, chip, side: 'left', count: counts.x }),
    ...fan({ rand, W, H, chip, side: 'right', count: counts.x }),
    ...fan({ rand, W, H, chip, side: 'top', count: counts.y }),
    ...fan({ rand, W, H, chip, side: 'bottom', count: counts.y })
  ];
  return { W, H, chip, traces };
}

const LANDSCAPE = layout({ W: 1600, H: 900, chipW: 1060, chipH: 470, counts: { x: 5, y: 6 }, seed: 20240 });
const PORTRAIT = layout({ W: 900, H: 1600, chipW: 700, chipH: 900, counts: { x: 5, y: 5 }, seed: 777 });

function Board({ data, className }) {
  const { W, H, chip, traces } = data;
  const corner = 46;
  return (
    <svg className={`circuit-board ${className}`} viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="xMidYMid slice" aria-hidden focusable="false">
      <defs>
        <linearGradient id={`ct-gold-${className}`} x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor="#8a6a1c" />
          <stop offset="0.45" stopColor="#e9c565" />
          <stop offset="1" stopColor="#8a6a1c" />
        </linearGradient>
        <radialGradient id={`ct-fade-${className}`} cx="50%" cy="50%" r="62%">
          <stop offset="0.35" stopColor="#fff" stopOpacity="1" />
          <stop offset="1" stopColor="#fff" stopOpacity="0.25" />
        </radialGradient>
        <mask id={`ct-mask-${className}`}>
          <rect width={W} height={H} fill={`url(#ct-fade-${className})`} />
        </mask>
        <pattern id={`ct-grid-${className}`} width="28" height="28" patternUnits="userSpaceOnUse">
          <circle cx="1" cy="1" r="1" className="ct-grid-dot" />
        </pattern>
      </defs>

      <rect width={W} height={H} fill={`url(#ct-grid-${className})`} className="ct-grid" />

      <g mask={`url(#ct-mask-${className})`} style={{ '--ct-stroke': `url(#ct-gold-${className})` }}>
        {/* Corner brackets frame the headline like the edge of a processor die */}
        {[[chip.x0, chip.y0, 1, 1], [chip.x1, chip.y0, -1, 1], [chip.x0, chip.y1, 1, -1], [chip.x1, chip.y1, -1, -1]].map(([x, y, sx, sy]) => (
          <path key={`${x}-${y}`} className="ct-corner" pathLength="1" d={`M${x} ${y + sy * corner} L${x} ${y + sy * 8} Q${x} ${y} ${x + sx * 8} ${y} L${x + sx * corner} ${y}`} />
        ))}

        {traces.map((t, i) => (
          <g key={i}>
            <path className="ct-trace" d={t.d} pathLength="1" style={{ '--d': `${t.delay}s` }} />
            {t.pulse && (
              <>
                <path className="ct-pulse-glow" d={t.d} pathLength="1" style={{ '--t': `${t.pulseDur}s`, '--pd': `${t.pulseDelay}s` }} />
                <path className="ct-pulse" d={t.d} pathLength="1" style={{ '--t': `${t.pulseDur}s`, '--pd': `${t.pulseDelay}s` }} />
              </>
            )}
            <circle className="ct-pin" cx={t.pin[0]} cy={t.pin[1]} r="2.6" style={{ '--d': `${t.delay}s` }} />
            {t.pad && (
              <g className="ct-pad" style={{ '--d': `${t.delay + 1.2}s` }}>
                <circle cx={t.pad[0]} cy={t.pad[1]} r="5.5" />
                <circle className="ct-pad-core" cx={t.pad[0]} cy={t.pad[1]} r="1.8" />
              </g>
            )}
          </g>
        ))}
      </g>
    </svg>
  );
}

export default function CircuitHero() {
  const ref = useRef(null);

  // Pause all animation while the hero is off-screen.
  useEffect(() => {
    const el = ref.current;
    if (!el || typeof IntersectionObserver === 'undefined') return undefined;
    const io = new IntersectionObserver(([entry]) => {
      el.classList.toggle('is-paused', !entry.isIntersecting);
    });
    io.observe(el);
    return () => io.disconnect();
  }, []);

  return (
    <div ref={ref} className="circuit-hero" aria-hidden>
      <Board data={LANDSCAPE} className="ct-landscape" />
      <Board data={PORTRAIT} className="ct-portrait" />
    </div>
  );
}
