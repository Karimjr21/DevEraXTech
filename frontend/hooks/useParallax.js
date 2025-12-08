import { useEffect } from 'react';

export function useParallax(selector = '[data-parallax]') {
  useEffect(() => {
    function handler() {
      const scrolled = window.scrollY;
      document.querySelectorAll(selector).forEach(el => {
        const speed = parseFloat(el.dataset.parallax || '0.4');
        el.style.transform = `translate3d(0, ${scrolled * speed * -0.2}px,0)`;
      });
    }
    handler();
    window.addEventListener('scroll', handler);
    return () => window.removeEventListener('scroll', handler);
  }, [selector]);
}
