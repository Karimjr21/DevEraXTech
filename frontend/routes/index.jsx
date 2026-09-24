import { Suspense } from 'react';
import { Routes, Route, useLocation } from 'react-router-dom';
import { AnimatePresence, m, useReducedMotion } from 'framer-motion';
import { pages } from './pages';

const EASE = [0.22, 1, 0.36, 1];

export default function RoutesIndex() {
  const location = useLocation();
  const reduce = useReducedMotion();
  const { '/': Home, '/services': Services, '/portfolio': Portfolio, '/about': About, '/contact': Contact, '*': NotFound } = pages;

  return (
    <AnimatePresence mode="wait" initial={false}>
      <m.div
        key={location.pathname}
        initial={reduce ? { opacity: 0 } : { opacity: 0, y: 18 }}
        animate={{ opacity: 1, y: 0, transition: { duration: 0.55, ease: EASE }, transitionEnd: { transform: 'none' } }}
        exit={reduce ? { opacity: 0 } : { opacity: 0, y: -10, transition: { duration: 0.25, ease: EASE } }}
      >
        {/* Always rendered so server and browser markup match; hidden by CSS for reduced motion. */}
        <span key={`bar-${location.pathname}`} className="fx-route-bar" aria-hidden />
        <Suspense fallback={null}>
          <Routes location={location}>
            <Route path="/" element={<Home />} />
            <Route path="/services" element={<Services />} />
            <Route path="/portfolio" element={<Portfolio />} />
            <Route path="/about" element={<About />} />
            <Route path="/contact" element={<Contact />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </Suspense>
      </m.div>
    </AnimatePresence>
  );
}
