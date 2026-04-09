import { Suspense, useEffect, useRef, useState } from 'react';
import { motion, useReducedMotion } from 'framer-motion';
import SectionWrapper from '../components/ui/SectionWrapper';
import AnimatedButton from '../components/ui/AnimatedButton';
import Logo3D from '../components/3d/Logo3D';
import ErrorBoundary from '../components/ui/ErrorBoundary';

export default function Home() {
  const shouldReduceMotion = useReducedMotion();
  const heroRef = useRef(null);
  const frameRef = useRef(null);
  const targetRef = useRef({ x: 0, y: 0 });
  const [parallax, setParallax] = useState({ x: 0, y: 0 });

  useEffect(() => {
    if (shouldReduceMotion || !heroRef.current) return undefined;

    const el = heroRef.current;
    const onMove = (event) => {
      const rect = el.getBoundingClientRect();
      const relX = (event.clientX - rect.left) / rect.width - 0.5;
      const relY = (event.clientY - rect.top) / rect.height - 0.5;
      targetRef.current = {
        x: relX * 16,
        y: relY * 12
      };
    };

    const onLeave = () => {
      targetRef.current = { x: 0, y: 0 };
    };

    const tick = () => {
      setParallax((prev) => {
        const nx = prev.x + (targetRef.current.x - prev.x) * 0.07;
        const ny = prev.y + (targetRef.current.y - prev.y) * 0.07;
        return { x: nx, y: ny };
      });
      frameRef.current = window.requestAnimationFrame(tick);
    };

    frameRef.current = window.requestAnimationFrame(tick);
    el.addEventListener('pointermove', onMove, { passive: true });
    el.addEventListener('pointerleave', onLeave, { passive: true });

    return () => {
      el.removeEventListener('pointermove', onMove);
      el.removeEventListener('pointerleave', onLeave);
      if (frameRef.current) window.cancelAnimationFrame(frameRef.current);
    };
  }, [shouldReduceMotion]);

  const heroContainerVariants = {
    hidden: { opacity: 0 },
    show: { opacity: 1, transition: { duration: 0.8, ease: [0.22, 1, 0.36, 1] } }
  };

  const heroItemVariants = {
    hidden: { opacity: 0, y: shouldReduceMotion ? 0 : 26, scale: shouldReduceMotion ? 1 : 0.985 },
    show: {
      opacity: 1,
      y: 0,
      scale: 1,
      transition: { duration: 0.9, ease: [0.22, 1, 0.36, 1] }
    }
  };

  return (
    <div ref={heroRef} className="home-hero-shell relative w-full overflow-hidden">
      <div className="absolute inset-0 pointer-events-none" aria-hidden>
        <div className="hero-stars" aria-hidden />
        <div className="hero-ambient-glow" aria-hidden />

        <motion.div
          className="absolute inset-0 z-0"
          style={shouldReduceMotion ? undefined : { transform: `translate3d(${parallax.x}px, ${parallax.y}px, 0)` }}
          transition={{ type: 'spring', stiffness: 30, damping: 18, mass: 1.1 }}
        >
        <ErrorBoundary fallback={<div className='text-gold text-center'>3D disabled — showing static hero.<br/>Check browser console for errors.</div>}>
          <Suspense fallback={<div className='text-gold'>Loading 3D...</div>}>
            <Logo3D />
          </Suspense>
        </ErrorBoundary>
        </motion.div>
      </div>

      <div className="min-h-screen w-full relative flex items-center justify-center">
        <motion.div
          variants={heroContainerVariants}
          initial="hidden"
          animate="show"
          className="absolute left-0 right-0 mx-auto max-w-5xl px-8 z-10 bottom-20 md:bottom-24 lg:bottom-28 xl:bottom-32"
        >
          <motion.h1 variants={heroItemVariants} className="text-5xl md:text-7xl font-bold mb-6 gold-gradient-text leading-tight">
            We build premium web & app experiences
          </motion.h1>
          <motion.p variants={heroItemVariants} className="text-lg text-gray-300 max-w-2xl mb-8">
            Modern, secure and scalable solutions — from prototypes to production.
          </motion.p>
          <motion.div variants={heroItemVariants} className="flex flex-wrap gap-4 sm:gap-6">
            <AnimatedButton to="/contact">Request a Meeting</AnimatedButton>
            <AnimatedButton variant="outline" to="/services">View Our Services</AnimatedButton>
          </motion.div>
        </motion.div>
      </div>
      <SectionWrapper id="trust" className="relative z-10 max-w-6xl mx-auto px-8 pt-6 pb-10 md:pt-8 md:pb-12">
        <p className="text-gray-400 chip-lux inline-flex items-center rounded-full px-4 py-2">
          Trusted by startups & enterprises • 50+ projects shipped
        </p>
      </SectionWrapper>
      <div className="hero-bottom-fade" aria-hidden />
    </div>
  );
}
