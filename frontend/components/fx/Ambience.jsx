import { useEffect } from 'react';
import { motion, useScroll, useSpring } from 'framer-motion';

// Thin gold reading-progress line at the very top of the page.
export function ScrollProgress() {
  const { scrollYProgress } = useScroll();
  const scaleX = useSpring(scrollYProgress, { stiffness: 140, damping: 30, mass: 0.3 });
  return <motion.div className="fx-scroll-progress" style={{ scaleX }} aria-hidden />;
}

// Slowly drifting gold light and a fine film grain behind every page.
export function AmbientBackground() {
  return (
    <div className="fx-ambient" aria-hidden>
      <span className="fx-orb fx-orb--a" />
      <span className="fx-orb fx-orb--b" />
      <span className="fx-orb fx-orb--c" />
      <span className="fx-grain" />
    </div>
  );
}

// A soft gold glow that follows the pointer across cards (one delegated listener).
const SPOTLIGHT = '.about-card, .portfolio-card, .service-editorial-row, .contact-card, .contact-side-card, .portfolio-hero-card, .portfolio-bottom-cta';

export function CardSpotlight() {
  useEffect(() => {
    if (typeof window === 'undefined' || !window.matchMedia('(hover: hover)').matches) return undefined;
    let frame = 0;
    let last = null;
    const onMove = (event) => {
      last = event;
      if (frame) return;
      frame = requestAnimationFrame(() => {
        frame = 0;
        const card = last.target instanceof Element ? last.target.closest(SPOTLIGHT) : null;
        if (!card) return;
        const rect = card.getBoundingClientRect();
        card.style.setProperty('--mx', `${last.clientX - rect.left}px`);
        card.style.setProperty('--my', `${last.clientY - rect.top}px`);
      });
    };
    window.addEventListener('pointermove', onMove, { passive: true });
    return () => {
      window.removeEventListener('pointermove', onMove);
      if (frame) cancelAnimationFrame(frame);
    };
  }, []);
  return null;
}

// Decorative animated gold line art for page headers.
export function GoldOrnament({ className = '' }) {
  return (
    <svg className={`fx-ornament ${className}`} viewBox="0 0 200 200" aria-hidden focusable="false">
      <defs>
        <linearGradient id="fx-gold" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor="#b8912a" />
          <stop offset="0.5" stopColor="#f5d573" />
          <stop offset="1" stopColor="#b8912a" />
        </linearGradient>
      </defs>
      <g className="fx-ornament-spin">
        <circle className="fx-draw" cx="100" cy="100" r="88" pathLength="1" />
        <circle className="fx-dash" cx="100" cy="100" r="74" />
      </g>
      <g className="fx-ornament-spin-rev">
        <circle className="fx-draw fx-draw--late" cx="100" cy="100" r="58" pathLength="1" />
        <path className="fx-draw fx-draw--late" d="M100 30 L170 100 L100 170 L30 100 Z" pathLength="1" />
      </g>
      <circle className="fx-core" cx="100" cy="100" r="4" />
      <circle className="fx-orbit-dot" cx="100" cy="12" r="3" />
    </svg>
  );
}
