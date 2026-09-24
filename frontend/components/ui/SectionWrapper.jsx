import { useEffect, useRef } from 'react';
import { isVisibleOnLanding } from '../../lib/firstView';

export default function SectionWrapper({ id, className = '', delay = 0, children, ...rest }) {
  const ref = useRef(null);

  useEffect(() => {
    const el = ref.current;
    const reduce = typeof window !== 'undefined' && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (!el) return undefined;
    if (delay) el.style.setProperty('--reveal-delay', `${delay}ms`);

    if (reduce || isVisibleOnLanding(el)) {
      el.classList.add('in-view');
      return undefined;
    }
    el.classList.add('is-pending');

    // Reveal when 16% of the section is visible OR it fills a quarter of the screen.
    // (A ratio alone never triggers for sections taller than ~6 screens, e.g. on phones.)
    const obs = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        const enough = entry.intersectionRatio >= 0.16 || entry.intersectionRect.height >= window.innerHeight * 0.25;
        if (entry.isIntersecting && enough) {
          entry.target.classList.add('in-view');
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: [0, 0.05, 0.1, 0.16, 0.25, 0.5], rootMargin: '0px 0px -6% 0px' });

    obs.observe(el);
    return () => obs.disconnect();
  }, [delay]);

  return (
    <section id={id} ref={ref} className={`scroll-fade ${className}`} {...rest}>{children}</section>
  );
}
