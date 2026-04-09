import { useEffect, useRef } from 'react';

export default function SectionWrapper({ id, className = '', delay = 0, children, ...rest }) {
  const ref = useRef(null);

  useEffect(() => {
    const el = ref.current;
    const reduce = typeof window !== 'undefined' && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (!el) return undefined;
    if (delay) el.style.setProperty('--reveal-delay', `${delay}ms`);

    if (reduce) {
      el.classList.add('in-view');
      return undefined;
    }

    const obs = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('in-view');
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.16, rootMargin: '0px 0px -6% 0px' });

    obs.observe(el);
    return () => obs.disconnect();
  }, [delay]);

  return (
    <section id={id} ref={ref} className={`scroll-fade ${className}`} {...rest}>{children}</section>
  );
}
