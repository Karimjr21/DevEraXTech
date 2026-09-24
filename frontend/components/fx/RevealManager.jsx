import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

// Site-wide scroll reveal. Runs only in the browser, so prerendered HTML (what search
// engines and AI crawlers read) always contains fully visible content.
const TARGETS = [
  'h1', 'h2', 'h3', 'p', 'li', 'dl', 'details', 'form',
  '.about-card', '.portfolio-card', '.portfolio-hero-card', '.portfolio-empty-card', '.portfolio-bottom-cta',
  '.service-editorial-row', '.contact-card', '.contact-side-card', '.empty-state', '.btn-premium'
].map(s => `main ${s}`).join(',');

// Areas that already have their own entrance choreography.
const SKIP = '.home-hero-shell, .rv-skip';
const STAGGER_MS = 80;
const MAX_STAGGER = 6;

export default function RevealManager() {
  const { pathname } = useLocation();

  useEffect(() => {
    if (typeof window === 'undefined' || !('IntersectionObserver' in window)) return undefined;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return undefined;
    const main = document.querySelector('main');
    if (!main) return undefined;

    const io = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('rv-in');
        io.unobserve(entry.target);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -4% 0px' });

    const prepare = () => {
      const counters = new Map();
      main.querySelectorAll(TARGETS).forEach(el => {
        if (el.classList.contains('rv') || el.closest(SKIP)) return;
        // Animate a card as one block instead of every line inside it.
        if (el.parentElement && el.parentElement.closest('.rv')) return;
        const parent = el.parentElement;
        const i = counters.get(parent) || 0;
        counters.set(parent, i + 1);
        el.style.setProperty('--rv-delay', `${Math.min(i, MAX_STAGGER) * STAGGER_MS}ms`);
        el.classList.add('rv', /^H[12]$/.test(el.tagName) ? 'rv-heading' : 'rv-rise');
        io.observe(el);
      });
    };

    // Wait a frame so the new route's DOM is in place.
    const raf = requestAnimationFrame(prepare);
    let queued = false;
    const mo = new MutationObserver(() => {
      if (queued) return;
      queued = true;
      requestAnimationFrame(() => { queued = false; prepare(); });
    });
    mo.observe(main, { childList: true, subtree: true });

    return () => {
      cancelAnimationFrame(raf);
      mo.disconnect();
      io.disconnect();
    };
  }, [pathname]);

  return null;
}
