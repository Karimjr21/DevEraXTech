import { useRef } from 'react';

// Featured project preview: the screenshot sits in a gold-framed browser window on a lit
// stage. The frame tilts toward the pointer, the image drifts slowly and a light sweep
// crosses it on hover. Entrance and motion are pure CSS (see .showcase-* in global.css)
// and switch off under prefers-reduced-motion.
export default function ShowcaseMedia({ item, onImageError }) {
  const stageRef = useRef(null);
  const frame = useRef(0);

  const host = (() => {
    try { return new URL(item.url).hostname.replace(/^www\./, ''); } catch { return item.client || item.title; }
  })();

  const onPointerMove = (event) => {
    const el = stageRef.current;
    if (!el || event.pointerType === 'touch') return;
    const rect = el.getBoundingClientRect();
    const x = (event.clientX - rect.left) / rect.width - 0.5;
    const y = (event.clientY - rect.top) / rect.height - 0.5;
    cancelAnimationFrame(frame.current);
    frame.current = requestAnimationFrame(() => {
      el.style.setProperty('--tilt-x', `${(-y * 7).toFixed(2)}deg`);
      el.style.setProperty('--tilt-y', `${(x * 9).toFixed(2)}deg`);
      el.style.setProperty('--glow-x', `${((x + 0.5) * 100).toFixed(1)}%`);
      el.style.setProperty('--glow-y', `${((y + 0.5) * 100).toFixed(1)}%`);
    });
  };

  const onPointerLeave = () => {
    const el = stageRef.current;
    if (!el) return;
    cancelAnimationFrame(frame.current);
    el.style.setProperty('--tilt-x', '0deg');
    el.style.setProperty('--tilt-y', '0deg');
    el.style.setProperty('--glow-x', '50%');
    el.style.setProperty('--glow-y', '40%');
  };

  return (
    <div
      ref={stageRef}
      className="showcase-stage"
      onPointerMove={onPointerMove}
      onPointerLeave={onPointerLeave}
    >
      <div className="showcase-aura" aria-hidden />
      <div className="showcase-grid" aria-hidden />
      <span className="showcase-corner showcase-corner--tl" aria-hidden />
      <span className="showcase-corner showcase-corner--br" aria-hidden />
      <span className="showcase-kicker" aria-hidden>Case study · {item.year || 'Live'}</span>
      <span className="showcase-watermark" aria-hidden>{item.client || item.title}</span>

      <div className="showcase-frame">
        <div className="showcase-chrome" aria-hidden>
          <span className="showcase-dots"><i /><i /><i /></span>
          <span className="showcase-url">
            <svg viewBox="0 0 16 16" width="10" height="10"><path fill="currentColor" d="M8 1a3.5 3.5 0 0 0-3.5 3.5V7H4a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V8a1 1 0 0 0-1-1h-.5V4.5A3.5 3.5 0 0 0 8 1Zm-2 6V4.5a2 2 0 1 1 4 0V7H6Z" /></svg>
            {host}
          </span>
        </div>
        <div className="showcase-screen">
          <img
            src={item.image}
            alt={item.imageAlt || item.title}
            width={item.imageWidth}
            height={item.imageHeight}
            className="showcase-img"
            onError={onImageError}
            loading="lazy"
            decoding="async"
          />
          <span className="showcase-sweep" aria-hidden />
          <span className="showcase-vignette" aria-hidden />
        </div>
        <div className="showcase-reflection" aria-hidden>
          <img src={item.image} alt="" loading="lazy" decoding="async" />
        </div>
      </div>

      <span className="showcase-badge" aria-hidden>
        <span className="showcase-badge-dot" />
        Live{item.location ? ` · ${item.location.split(',')[0]}` : ''}
      </span>

      <span className="showcase-visit" aria-hidden>
        Visit
        <br />
        site
      </span>
    </div>
  );
}
