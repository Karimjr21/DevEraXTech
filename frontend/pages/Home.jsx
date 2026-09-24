import { Suspense, lazy, useEffect, useRef, useState } from 'react';
import { m, useReducedMotion } from 'framer-motion';
import { Link } from 'react-router-dom';
import SectionWrapper from '../components/ui/SectionWrapper';
import { LoadingCards } from '../components/ui/EmptyState';
import AnimatedButton from '../components/ui/AnimatedButton';
import CircuitHero from '../components/fx/CircuitHero';
const GoldGlobe = lazy(() => import('../components/fx/GoldGlobe'));
import ErrorBoundary from '../components/ui/ErrorBoundary';
import { fetchServices } from '../lib/api';
import useApiData from '../lib/useApiData';
import business from '../src/data/business.json';
import homeFaq from '../src/data/home-faq.json';

// Loads the globe only when its card approaches the viewport.
function GlobeSlot() {
  const ref = useRef(null);
  const [show, setShow] = useState(false);
  useEffect(() => {
    const el = ref.current;
    if (!el || typeof IntersectionObserver === 'undefined') { setShow(true); return undefined; }
    const io = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) { setShow(true); io.disconnect(); }
    }, { rootMargin: '400px 0px' });
    io.observe(el);
    return () => io.disconnect();
  }, []);
  return (
    <div ref={ref} className="globe-slot rv-skip" aria-hidden={!show}>
      {show && (
        <ErrorBoundary fallback={null}>
          <Suspense fallback={null}>
            <GoldGlobe />
          </Suspense>
        </ErrorBoundary>
      )}
    </div>
  );
}

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

  const { status: servicesStatus, data: services } = useApiData(fetchServices, 'services');

  return (
    <>
    <div ref={heroRef} className="home-hero-shell relative w-full overflow-hidden">
      <div className="absolute inset-0 pointer-events-none" aria-hidden>
        <div className="hero-stars" aria-hidden />
        <div className="hero-ambient-glow" aria-hidden />

        <m.div
          className="absolute inset-0 z-0 hero-3d-stage"
          style={shouldReduceMotion ? undefined : { transform: `translate3d(${parallax.x + 14}px, ${parallax.y + 10}px, 0)` }}
          transition={{ type: 'spring', stiffness: 30, damping: 18, mass: 1.1 }}
        >
          <CircuitHero />
        </m.div>
      </div>

      <div className="min-h-screen w-full relative flex flex-col items-center justify-center pt-20 md:pt-24">
        {/* Subtle overlay to reduce 3D object visual competition with text */}
        <div
          className="absolute inset-x-0 top-0 -bottom-28 z-[5] pointer-events-none hero-text-focus-vignette"
          aria-hidden
        />

        <m.div
          variants={heroContainerVariants}
          initial="hidden"
          animate="show"
          className="relative z-10 left-0 right-0 mx-auto max-w-5xl px-8 w-full text-center"
        >
          {/* Premium supertitle */}
          <m.div variants={heroItemVariants} className="mb-6 md:mb-8">
            <p className="text-xs md:text-sm font-semibold tracking-widest text-gold/70 uppercase">
              ENGINEERED EXCELLENCE
            </p>
          </m.div>

          {/* Main headline with refined typography */}
          <m.h1
            variants={heroItemVariants}
            className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold mb-6 md:mb-8 gold-gradient-text leading-[1.14] md:leading-[1.09] max-w-3xl md:max-w-4xl mx-auto"
          >
            We build premium web &amp; app experiences
          </m.h1>

          {/* Supporting paragraph */}
          <m.p
            variants={heroItemVariants}
            className="text-base md:text-lg text-gray-300/90 max-w-2xl mx-auto mb-10 md:mb-12 leading-relaxed"
          >
            Modern, secure and scalable solutions, from prototypes to production.
          </m.p>

          {/* CTA button group with refined spacing and hierarchy */}
          <m.div variants={heroItemVariants} className="flex flex-col sm:flex-row gap-4 sm:gap-5 items-center justify-center">
            <AnimatedButton to="/contact">Request a Meeting</AnimatedButton>
            <AnimatedButton variant="outline" to="/services">View Our Services</AnimatedButton>
          </m.div>

          <m.div
            variants={heroItemVariants}
            className="mt-8 md:mt-9 flex flex-wrap items-center justify-center gap-x-3 gap-y-2 text-[0.72rem] sm:text-xs tracking-[0.08em] uppercase text-gray-400/70"
            aria-label="Service quality details"
          >
            <span>Secure</span>
            <span className="text-gold/40" aria-hidden>•</span>
            <span>Scalable</span>
            <span className="text-gold/40" aria-hidden>•</span>
            <span>Pixel-perfect</span>
          </m.div>
        </m.div>
      </div>
      <SectionWrapper id="trust" className="relative z-10 max-w-6xl mx-auto px-8 pt-10 md:pt-14 lg:pt-16 pb-16 md:pb-20">
        <div className="flex justify-center">
          <m.div
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
            viewport={{ once: true, margin: '-10% 0px' }}
          >
            <p className="text-sm md:text-base text-gray-400/80 chip-lux inline-flex items-center rounded-full px-4 md:px-6 py-2.5 md:py-3 gap-3 backdrop-blur-sm">
              <span className="inline-block w-1.5 h-1.5 rounded-full bg-gold/60"></span>
              Trusted by startups &amp; enterprises • 10+ projects shipped
            </p>
          </m.div>
        </div>
      </SectionWrapper>
      <div className="hero-bottom-fade" aria-hidden />
    </div>

    <SectionWrapper id="what-we-build" className="max-w-6xl mx-auto px-6 sm:px-8 pt-6 pb-16 md:pb-20" aria-labelledby="home-services-heading">
      <div className="max-w-3xl mb-8 md:mb-10 space-y-3">
        <p className="text-[11px] tracking-[0.2em] uppercase text-gold/70">What We Build</p>
        <h2 id="home-services-heading" className="text-2xl md:text-3xl font-semibold text-gold leading-tight">
          Websites engineered to be secure, scalable and pixel-perfect
        </h2>
        <p className="text-sm md:text-base text-gray-300/90 leading-relaxed">
          DevEraXTech is a web design and development studio in Cairo, Egypt. We build premium web and app experiences
          for companies, startups and creatives: business websites, online stores and high-conversion pages that look
          exceptional and work flawlessly on every device. Every project is treated as a long-term digital asset,
          engineered for resilience, elegant usability and growth. Whether you need a corporate website, a new online store
          or a single campaign landing page, we plan, design and build it end to end with the same care and attention to
          detail.
        </p>
      </div>

      {servicesStatus === 'ready' && services.length > 0 && (
        <ul className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-5" role="list">
          {services.map(service => (
            <li key={service.id || service.title} className="about-card home-service-card relative h-full p-5 md:p-6">
              {/* Only the title is the link (short anchor text); its ::after overlay keeps the whole card clickable. */}
              <h3 className="text-lg font-semibold text-gold leading-snug">
                <Link to={`/services#${service.id}`} className="card-stretched-link">{service.title}</Link>
              </h3>
              <p className="mt-2 text-sm text-gray-400 leading-relaxed">
                {service.summary || service.description}
              </p>
              <span className="mt-4 inline-flex items-center gap-1 text-xs uppercase tracking-[0.12em] text-gold/80" aria-hidden>
                View details →
              </span>
            </li>
          ))}
        </ul>
      )}

      {servicesStatus === 'loading' && (
        <LoadingCards count={3} label="Loading services" className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-5" />
      )}

      <div className="mt-10 md:mt-12 grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-5">
        {[
          ['Secure by Design', 'Security is embedded from architecture decisions to final QA, reducing risk before launch.'],
          ['Scalable Delivery', 'Structured execution keeps projects reliable as scope grows, from pilot releases to production.'],
          ['Clear Communication', 'Transparent updates, aligned milestones and a response to most inquiries within one business day.']
        ].map(([title, text]) => (
          <div key={title} className="border-l border-gold/30 pl-4">
            <h3 className="text-sm font-semibold text-gray-100 uppercase tracking-[0.1em]">{title}</h3>
            <p className="mt-2 text-sm text-gray-400 leading-relaxed">{text}</p>
          </div>
        ))}
      </div>

      <div className="mt-12 md:mt-14">
        <p className="text-[11px] tracking-[0.2em] uppercase text-gold/70">Why DevEraXTech</p>
        <h2 className="mt-2 text-xl md:text-2xl font-semibold text-gold leading-tight">Why clients choose DevEraXTech</h2>
        <div className="mt-5 grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-5">
          {[
            ['Premium design, not templates', 'Every interface is designed around your brand and your customers, so your website feels distinctive and communicates quality from the first screen.'],
            ['Security built in from day one', 'Security decisions start at the architecture stage and continue through final QA, which reduces risk before your website ever goes live.'],
            ['Fast, responsive and scalable', 'Pages are built to load quickly and adapt to phones, tablets and desktops, on a structure that can grow as your business adds pages, products or markets.'],
            ['One clear line of communication', 'You get transparent updates, aligned milestones and a response to most inquiries within one business day, in Arabic, English or German.']
          ].map(([title, text]) => (
            <div key={title} className="border-l border-gold/30 pl-4">
              <h3 className="text-base font-semibold text-gray-100">{title}</h3>
              <p className="mt-1.5 text-sm text-gray-400 leading-relaxed">{text}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="mt-12 md:mt-14 space-y-5 md:space-y-6">
        <div className="about-card p-6 md:p-8">
          <p className="text-[11px] tracking-[0.2em] uppercase text-gold/70">How It Works</p>
          <h2 className="mt-2 text-xl md:text-2xl font-semibold text-gold leading-tight">From first call to launch</h2>
          <ol className="mt-5 grid grid-cols-1 md:grid-cols-3 gap-5 md:gap-6 text-sm text-gray-300/90 leading-relaxed" role="list">
            {[
              ['Discovery call.', 'Tell us about your goals, audience and timeline, and we map the right approach before proposing any scope.'],
              ['Plan and design.', 'You get a clear scope with milestones, then interfaces designed for clarity, conversion and your brand.'],
              ['Build, secure and launch.', 'We engineer a fast, secure, responsive site and launch it with transparent updates at every step.']
            ].map(([title, text], i) => (
              <li key={title} className="border-t border-gold/20 pt-4">
                <span className="block font-display text-2xl text-gold/80 leading-none mb-2">0{i + 1}</span>
                <b className="text-gray-100">{title}</b> {text}
              </li>
            ))}
          </ol>
          <Link to="/about#how-we-work" className="mt-5 inline-flex items-center gap-1 text-xs uppercase tracking-[0.12em] text-gold/80 hover:text-gold">
            Read about our full process <span aria-hidden>→</span>
          </Link>
        </div>

        <div className="about-card p-6 md:p-8 grid grid-cols-1 md:grid-cols-[1fr_1.05fr] gap-6 md:gap-10 items-center">
          <div>
            <p className="text-[11px] tracking-[0.2em] uppercase text-gold/70">Where We Work</p>
            <h2 className="mt-2 text-xl md:text-2xl font-semibold text-gold leading-tight">Cairo-based, serving clients worldwide</h2>
            <p className="mt-4 text-sm text-gray-300/90 leading-relaxed">
              DevEraXTech is based in {business.city}, {business.country}, and builds websites for clients in{' '}
              {business.areasServed.map(a => a.name).join(', ').replace(/, ([^,]*)$/, ' and $1')}.
            </p>
            <p className="mt-3 text-sm text-gray-400 leading-relaxed">
              We work in {business.languages.map(l => l.name).join(', ').replace(/, ([^,]*)$/, ' and $1')}, and we are available
              every day from 9:00 AM to 5:00 PM Cairo time. Meetings booked online show both Cairo time and your local time.
            </p>
          </div>
          <GlobeSlot />
        </div>
      </div>

      <div className="mt-12 md:mt-14 max-w-3xl">
        <p className="text-[11px] tracking-[0.2em] uppercase text-gold/70">Before You Start</p>
        <h2 className="mt-2 text-xl md:text-2xl font-semibold text-gold leading-tight">Common questions before starting a website</h2>
        <div className="mt-5 space-y-5">
          {homeFaq.map(item => (
            <div key={item.question}>
              <h3 className="text-base font-semibold text-gray-100">{item.question}</h3>
              <p className="mt-1.5 text-sm text-gray-400 leading-relaxed">{item.answer}</p>
            </div>
          ))}
        </div>
      </div>

      <p className="mt-12 md:mt-14 max-w-2xl mx-auto text-center text-sm md:text-base text-gray-300/90 leading-relaxed">
        Ready to build a website that reflects the quality of your business? Tell us what you have in mind, choose a meeting
        time that suits you, and we will reply with clear next steps, usually within one business day.
      </p>

      <div className="mt-6 md:mt-8 flex flex-col sm:flex-row gap-4 sm:gap-5 items-center justify-center">
        <AnimatedButton to="/contact">Start Your Project</AnimatedButton>
        <AnimatedButton variant="outline" to="/services">Explore All Services</AnimatedButton>
      </div>
    </SectionWrapper>
    </>
  );
}
