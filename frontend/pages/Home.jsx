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
          className="absolute inset-0 z-0 hero-3d-stage"
          style={shouldReduceMotion ? undefined : { transform: `translate3d(${parallax.x + 14}px, ${parallax.y + 10}px, 0)` }}
          transition={{ type: 'spring', stiffness: 30, damping: 18, mass: 1.1 }}
        >
        <ErrorBoundary fallback={<div className='text-gold text-center'>3D disabled — showing static hero.<br/>Check browser console for errors.</div>}>
          <Suspense fallback={<div className='text-gold'>Loading 3D...</div>}>
            <Logo3D />
          </Suspense>
        </ErrorBoundary>
        </motion.div>
      </div>

      <div className="min-h-screen w-full relative flex flex-col items-center justify-center pt-20 md:pt-24">
        {/* Subtle overlay to reduce 3D object visual competition with text */}
        <div
          className="absolute inset-x-0 top-0 -bottom-28 z-[5] pointer-events-none hero-text-focus-vignette"
          aria-hidden
        />

        <motion.div
          variants={heroContainerVariants}
          initial="hidden"
          animate="show"
          className="relative z-10 left-0 right-0 mx-auto max-w-5xl px-8 w-full text-center"
        >
          {/* Premium supertitle */}
          <motion.div variants={heroItemVariants} className="mb-6 md:mb-8">
            <p className="text-xs md:text-sm font-semibold tracking-widest text-gold/70 uppercase">
              ENGINEERED EXCELLENCE
            </p>
          </motion.div>

          {/* Main headline with refined typography */}
          <motion.h1
            variants={heroItemVariants}
            className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold mb-6 md:mb-8 gold-gradient-text leading-[1.14] md:leading-[1.09] max-w-3xl md:max-w-4xl mx-auto"
          >
            We build premium web &amp; app experiences
          </motion.h1>

          {/* Supporting paragraph */}
          <motion.p
            variants={heroItemVariants}
            className="text-base md:text-lg text-gray-300/90 max-w-2xl mx-auto mb-10 md:mb-12 leading-relaxed"
          >
            Modern, secure and scalable solutions — from prototypes to production.
          </motion.p>

          {/* CTA button group with refined spacing and hierarchy */}
          <motion.div variants={heroItemVariants} className="flex flex-col sm:flex-row gap-4 sm:gap-5 items-center justify-center">
            <AnimatedButton to="/contact">Request a Meeting</AnimatedButton>
            <AnimatedButton variant="outline" to="/services">View Our Services</AnimatedButton>
          </motion.div>

          <motion.div
            variants={heroItemVariants}
            className="mt-8 md:mt-9 flex flex-wrap items-center justify-center gap-x-3 gap-y-2 text-[0.72rem] sm:text-xs tracking-[0.08em] uppercase text-gray-400/70"
            aria-label="Service quality details"
          >
            <span>Secure</span>
            <span className="text-gold/40" aria-hidden>•</span>
            <span>Scalable</span>
            <span className="text-gold/40" aria-hidden>•</span>
            <span>Pixel-perfect</span>
          </motion.div>
        </motion.div>
      </div>
      <SectionWrapper id="trust" className="relative z-10 max-w-6xl mx-auto px-8 pt-10 md:pt-14 lg:pt-16 pb-16 md:pb-20">
        <div className="flex justify-center">
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
            viewport={{ once: true, margin: '-10% 0px' }}
          >
            <p className="text-sm md:text-base text-gray-400/80 chip-lux inline-flex items-center rounded-full px-4 md:px-6 py-2.5 md:py-3 gap-3 backdrop-blur-sm">
              <span className="inline-block w-1.5 h-1.5 rounded-full bg-gold/60"></span>
              Trusted by startups &amp; enterprises • 50+ projects shipped
            </p>
          </motion.div>
        </div>
      </SectionWrapper>
      <div className="hero-bottom-fade" aria-hidden />
    </div>
  );
}
