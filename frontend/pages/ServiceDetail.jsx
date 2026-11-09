import { Link, useParams } from 'react-router-dom';
import { workSrcSet, HALF_SIZES } from '../lib/images';
import SectionWrapper from '../components/ui/SectionWrapper';
import { GoldOrnament } from '../components/fx/Ambience';
import AnimatedButton from '../components/ui/AnimatedButton';
import services from '../src/data/services.json';
import details from '../src/data/service-details.json';
import portfolio from '../src/data/portfolio.json';
import { serviceHref } from '../lib/serviceGroups';
import NotFound from './NotFound';

const STEPS = [
  { title: 'Discovery call.', text: 'We learn your goals, audience and must-haves, and agree on scope, timeline and budget.' },
  { title: 'Design.', text: 'You see the structure and look first, and we refine it with you before any code is written.' },
  { title: 'Build & test.', text: 'We develop on a private staging link, then test speed, security, SEO and every screen size.' },
  { title: 'Launch & care.', text: 'We go live, hand over with training and stay on hand with an optional care plan.' }
];

// One page per service at /services/:serviceId. Content comes from services.json (summary and
// features) and service-details.json (intro, audience, stack, FAQs, related links); <head> tags
// and JSON-LD come from src/seo.js.
export default function ServiceDetail() {
  const { serviceId } = useParams();
  const service = services.find(s => s.id === serviceId && !s.link);
  const detail = service && details[service.id];
  if (!detail) return <NotFound />;

  const contactHref = `/contact?service=${encodeURIComponent(service.title)}`;
  const related = (detail.related || []).map(id => services.find(s => s.id === id)).filter(Boolean);
  const work = portfolio.filter(p => (detail.work || []).includes(p.id));
  const groupId = (service.group || '').toLowerCase().replace(/&/g, 'and').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

  return (
    <div className="max-w-[1400px] mx-auto px-6 sm:px-8 py-24">
      <div className="relative isolate mb-12 md:mb-16">
        <GoldOrnament className="page-ornament" />
        <nav aria-label="Breadcrumb">
          <ol className="flex flex-wrap items-baseline gap-y-1 gap-x-2 text-[0.72rem] uppercase tracking-[0.16em] text-gray-400/85 mb-3" role="list">
            <li><Link to="/services" className="hover:text-gold focus-visible:text-gold">Services</Link></li>
            <li aria-hidden className="text-gold/40">/</li>
            {service.group && (
              <>
                <li><Link to={`/services#${groupId}`} className="hover:text-gold focus-visible:text-gold">{service.group}</Link></li>
                <li aria-hidden className="text-gold/40">/</li>
              </>
            )}
            <li aria-current="page" className="text-gray-300">{service.title}</li>
          </ol>
        </nav>
        <div className="flex items-end gap-4">
          <h1 className="text-4xl md:text-[2.6rem] font-bold gold-gradient-text leading-[1.1] max-w-4xl">{detail.h1}</h1>
          <span className="hidden sm:block h-px w-24 md:w-32 bg-gradient-to-r from-gold/55 to-transparent mb-2 shrink-0" aria-hidden />
        </div>
        <p className="mt-5 max-w-3xl text-base md:text-lg text-gray-200/90 leading-relaxed">{service.summary}</p>
        {detail.intro.map(p => (
          <p key={p.slice(0, 32)} className="mt-4 max-w-3xl text-sm md:text-base text-gray-300/90 leading-relaxed">{p}</p>
        ))}
        <div className="mt-7 flex flex-col sm:flex-row gap-4 sm:gap-5">
          <AnimatedButton to={contactHref}>Start This Project</AnimatedButton>
          <AnimatedButton variant="outline" to="/portfolio">See Our Work</AnimatedButton>
        </div>
      </div>

      <SectionWrapper id="whats-included" aria-labelledby="included-heading" className="service-editorial-row rounded-2xl p-5 md:p-6 lg:p-7">
        <div className="service-editorial-grid grid grid-cols-1 lg:grid-cols-2 gap-5 md:gap-6 lg:gap-8 items-start">
          <div className="service-editorial-pitch">
            <div className="service-editorial-kicker-row mb-3.5 md:mb-4">
              <p className="service-editorial-kicker text-[0.67rem] uppercase tracking-[0.18em] text-gray-400/82">What&apos;s Included</p>
              <span className="service-editorial-kicker-line" aria-hidden />
            </div>
            <h2 id="included-heading" className="service-editorial-title text-[1.55rem] md:text-[1.78rem] font-semibold tracking-tight leading-[1.16]">
              Everything that comes with this service
            </h2>
            <p className="service-editorial-copy mt-4 leading-relaxed text-[0.96rem] md:text-[1rem] max-w-[58ch]">{service.description}</p>
            <p className="service-editorial-support mt-4 text-[0.8rem] md:text-[0.82rem] text-gray-400/78 uppercase tracking-[0.11em]">
              {(service.features || []).length} key capabilities
            </p>
          </div>
          <div className="service-editorial-details lg:justify-self-end w-full lg:max-w-[34rem]">
            <ul className="service-editorial-list w-full" role="list">
              {(service.features || []).map(f => (
                <li key={f} className="service-editorial-item">
                  <span className="service-editorial-marker" aria-hidden />
                  <span className="service-editorial-item-text">{f}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </SectionWrapper>

      <div className="mt-16 md:mt-20 grid grid-cols-1 lg:grid-cols-2 gap-4 md:gap-5">
        <SectionWrapper id="who-its-for" aria-labelledby="audience-heading" className="about-card about-card--functional h-full p-5 md:p-6">
          <p className="text-[11px] uppercase tracking-[0.18em] text-gold/70 mb-2">Who It&apos;s For</p>
          <h2 id="audience-heading" className="text-xl font-semibold text-gold leading-snug">Built for</h2>
          <ul className="service-editorial-list mt-4" role="list">
            {detail.audience.map(a => (
              <li key={a} className="service-editorial-item">
                <span className="service-editorial-marker" aria-hidden />
                <span className="service-editorial-item-text">{a}</span>
              </li>
            ))}
          </ul>
        </SectionWrapper>
        <SectionWrapper id="technology" aria-labelledby="stack-heading" delay={60} className="about-card about-card--functional h-full p-5 md:p-6">
          <p className="text-[11px] uppercase tracking-[0.18em] text-gold/70 mb-2">Technology</p>
          <h2 id="stack-heading" className="text-xl font-semibold text-gold leading-snug">Tools and platforms we use</h2>
          <ul className="mt-4 flex flex-wrap gap-2" role="list">
            {detail.stack.map(t => <li key={t} className="portfolio-tag">{t}</li>)}
          </ul>
        </SectionWrapper>
      </div>

      <SectionWrapper id="how-it-works" className="about-card p-6 md:p-8 mt-16 md:mt-20" aria-labelledby="how-heading">
        <p className="text-[11px] tracking-[0.2em] uppercase text-gold/70">How It Works</p>
        <h2 id="how-heading" className="mt-2 text-xl md:text-2xl font-semibold text-gold leading-tight">
          How we deliver it, step by step
        </h2>
        <ol className="mt-5 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 md:gap-6 text-sm text-gray-300/90 leading-relaxed" role="list">
          {STEPS.map((step, i) => (
            <li key={step.title} className="border-t border-gold/20 pt-4">
              <span className="block font-display text-2xl text-gold/80 leading-none mb-2">{`0${i + 1}`}</span>
              <b className="text-gray-100">{step.title}</b> {step.text}
            </li>
          ))}
        </ol>
      </SectionWrapper>

      {work.length > 0 && (
        <SectionWrapper id="related-work" aria-labelledby="work-heading" className="mt-16 md:mt-20">
          <p className="text-[0.72rem] uppercase tracking-[0.16em] text-gray-400/85 mb-3">Recent Work</p>
          <h2 id="work-heading" className="text-2xl md:text-3xl font-semibold text-gold leading-tight mb-6 md:mb-8">
            Projects we have delivered
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5 md:gap-6">
            {work.map(p => (
              <article key={p.id} className="portfolio-card group">
                <div className="portfolio-media-shell">
                  <img src={p.image} srcSet={workSrcSet(p.image)} sizes={HALF_SIZES} alt={p.imageAlt || p.title} width={p.imageWidth} height={p.imageHeight} className="portfolio-media-img" loading="lazy" />
                  <div className="portfolio-media-overlay" aria-hidden />
                </div>
                <div className="p-5 sm:p-6 space-y-3">
                  <p className="text-[11px] tracking-[0.16em] uppercase text-gold/70">{p.category}</p>
                  <h3 className="text-[1.15rem] font-semibold text-gold leading-tight">{p.title}</h3>
                  <p className="text-sm text-gray-300/90 leading-relaxed portfolio-description-clamp">{p.description}</p>
                  <div className="flex flex-wrap gap-x-5 gap-y-2">
                    <a href={p.url} target="_blank" rel="noopener noreferrer" className="portfolio-cta-link">
                      Visit {new URL(p.url).hostname.replace(/^www\./, '')} <span aria-hidden>→</span>
                    </a>
                    <Link to={`/portfolio#${p.id}`} className="portfolio-cta-link">Case study <span aria-hidden>→</span></Link>
                  </div>
                </div>
              </article>
            ))}
          </div>
        </SectionWrapper>
      )}

      <SectionWrapper id="faq" className="mt-16 md:mt-20" aria-labelledby="faq-heading">
        <p className="text-[0.72rem] uppercase tracking-[0.16em] text-gray-400/85 mb-3">Good to Know</p>
        <h2 id="faq-heading" className="text-2xl md:text-3xl font-semibold text-gold leading-tight mb-6 md:mb-8">
          Frequently asked questions
        </h2>
        <div className="space-y-3 md:space-y-4">
          {detail.faq.map(item => (
            <details key={item.question} className="faq-item service-editorial-row rounded-2xl">
              <summary className="faq-question">
                <span>{item.question}</span>
                <span className="faq-marker" aria-hidden>+</span>
              </summary>
              <p className="faq-answer">{item.answer}</p>
            </details>
          ))}
        </div>
      </SectionWrapper>

      {detail.sources?.length > 0 && (
        <SectionWrapper id="further-reading" aria-labelledby="sources-heading" className="mt-10 md:mt-12">
          <h2 id="sources-heading" className="text-[0.72rem] uppercase tracking-[0.16em] text-gray-400/85 mb-3">Further reading</h2>
          <ul className="flex flex-wrap gap-x-6 gap-y-2 text-sm" role="list">
            {detail.sources.map(src => (
              <li key={src.url}>
                <a href={src.url} target="_blank" rel="noopener noreferrer" className="text-gray-300 hover:text-gold focus-visible:text-gold underline underline-offset-4 decoration-gold/30">{src.label}</a>
              </li>
            ))}
          </ul>
        </SectionWrapper>
      )}

      {related.length > 0 && (
        <SectionWrapper id="related-services" aria-labelledby="related-heading" className="mt-16 md:mt-20">
          <p className="text-[0.72rem] uppercase tracking-[0.16em] text-gray-400/85 mb-3">Often Paired With</p>
          <h2 id="related-heading" className="text-2xl md:text-3xl font-semibold text-gold leading-tight mb-6 md:mb-8">Related services</h2>
          <ul className="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-5" role="list">
            {related.map(r => (
              <li key={r.id} className="about-card home-service-card relative h-full p-5 md:p-6">
                <h3 className="text-lg font-semibold text-gold leading-snug">
                  <Link to={serviceHref(r)} className="card-stretched-link">{r.title}</Link>
                </h3>
                <p className="mt-2 text-sm text-gray-400 leading-relaxed">{r.summary}</p>
                <span className="mt-4 inline-flex items-center gap-1 text-xs uppercase tracking-[0.12em] text-gold/80" aria-hidden>
                  {r.linkLabel || 'View details'} →
                </span>
              </li>
            ))}
          </ul>
        </SectionWrapper>
      )}

      <SectionWrapper id="service-cta" aria-labelledby="service-cta-heading" className="about-card about-card--cta relative overflow-hidden p-7 sm:p-9 md:p-10 mt-16 md:mt-20">
        <div className="absolute inset-0 pointer-events-none" aria-hidden>
          <div className="absolute -top-10 right-[15%] w-32 h-32 rounded-full bg-gold/10 blur-3xl" />
        </div>
        <div className="relative z-[1] flex flex-col md:flex-row md:items-end md:justify-between gap-6 md:gap-8">
          <div className="max-w-2xl space-y-3">
            <p className="text-xs tracking-[0.2em] uppercase text-gold/70">Start a Project</p>
            <h2 id="service-cta-heading" className="text-2xl md:text-3xl font-semibold text-gold leading-tight">Ready to start your project?</h2>
            <p className="text-sm md:text-base text-gray-300/90 leading-relaxed">
              Tell us what you want to build. DevEraXTech is based in Cairo, works with clients in Egypt, the Gulf, the United States and
              Canada, and usually replies within one business day.
            </p>
          </div>
          <div className="md:pb-1 flex flex-col sm:flex-row gap-3">
            <AnimatedButton to={contactHref}>Book a Meeting</AnimatedButton>
            <AnimatedButton variant="outline" to="/services">All Services</AnimatedButton>
          </div>
        </div>
      </SectionWrapper>
    </div>
  );
}
