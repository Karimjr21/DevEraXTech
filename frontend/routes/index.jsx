import { Routes, Route, useLocation } from 'react-router-dom';
import { AnimatePresence, motion, useReducedMotion } from 'framer-motion';
import Home from '../pages/Home';
import Services from '../pages/Services';
import Portfolio from '../pages/Portfolio';
import About from '../pages/About';
import Contact from '../pages/Contact';
import NotFound from '../pages/NotFound';

const EASE = [0.22, 1, 0.36, 1];

export default function RoutesIndex() {
  const location = useLocation();
  const reduce = useReducedMotion();

  return (
    <AnimatePresence mode="wait" initial={false}>
      <motion.div
        key={location.pathname}
        initial={reduce ? { opacity: 0 } : { opacity: 0, y: 18 }}
        animate={{ opacity: 1, y: 0, transition: { duration: 0.55, ease: EASE }, transitionEnd: { transform: 'none' } }}
        exit={reduce ? { opacity: 0 } : { opacity: 0, y: -10, transition: { duration: 0.25, ease: EASE } }}
      >
        {!reduce && <span key={`bar-${location.pathname}`} className="fx-route-bar" aria-hidden />}
        <Routes location={location}>
          <Route path="/" element={<Home />} />
          <Route path="/services" element={<Services />} />
          <Route path="/portfolio" element={<Portfolio />} />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </motion.div>
    </AnimatePresence>
  );
}
