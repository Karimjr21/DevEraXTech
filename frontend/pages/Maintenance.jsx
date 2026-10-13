import { Link } from 'react-router-dom';
import SectionWrapper from '../components/ui/SectionWrapper';
import { GoldOrnament } from '../components/fx/Ambience';
import AnimatedButton from '../components/ui/AnimatedButton';
import services from '../src/data/services.json';
import care from '../src/data/maintenance.json';

const SERVICE_ID = 'maintenance-care-plans';
const serviceTitle = services.find(s => s.id === SERVICE_ID)?.title || 'Maintenance & Care Plans';
const contactHref = `/contact?service=${encodeURIComponent(serviceTitle)}`;
const ctaClass = 'service-editorial-cta h-9 md:h-10 px-[1.125rem] md:px-5 text-[0.8rem] md:text-[0.84rem] uppercase tracking-[0.08em]';

export default function Maintenance() {
  return (
    <div className="max-w-[1400px] mx-auto px-8 py-24">
      <div className="relative isolate mb-12 md:mb-16">
        <GoldOrnament className="page-ornament" />
        <nav aria-label="Breadcrumb">
          <ol className="flex flex-wrap items-baseline gap-y-1 gap-x-2 text-[0.72rem] uppercase tracking-[0.16em] text-gray-400/85 mb-3" role="list">
            <li><Link to="/services" className="hover:text-gold focus-visible:text-gold">Services</Link></li>
            <li aria-hidden className="text-gold/40">/</li>
            <li aria-current="page" className="text-gray-300">Maintenance &amp; Care Plans</li>
          </ol>
        </nav>
        <div className="flex items-end gap-4">
          <h1 className="text-4xl font-bold gold-gradient-text">Website Maintenance &amp; Care Plans</h1>
          <span className="hidden sm:block h-px w-24 md:w-32 bg-gradient-to-r from-gold/55 to-transparent mb-2" aria-hidden />
        </div>
        <p className="mt-4 max-w-3xl text-sm md:text-base text-gray-300/90 leading-relaxed">
          Launch is the start, not the finish. DevEraXTech care plans keep your website or app secure, fast and up to date after
          it goes live, with updates, security patches, backups, uptime monitoring and one team to call when something needs to
          change. We look after sites we built and, after a short review, sites built elsewhere.
        </p>
        <div className="mt-7 flex flex-col sm:flex-row gap-4 sm:gap-5">
          <AnimatedButton to={contactHref}>Discuss a Care Plan</AnimatedButton>
          <AnimatedButton variant="outline" to="/services#growth-and-support">View All Services</AnimatedButton>
        </div>
      </div>

      <SectionWrapper id="whats-covered" aria-labelledby="covered-heading" className="service-editorial-row rounded-2xl p-5 md:p-6 lg:p-7">
        <div className="service-editorial-grid grid grid-cols-1 lg:grid-cols-2 gap-5 md:gap-6 lg:gap-8 items-start">
          <div className="service-editorial-pitch">
            <div className="service-editorial-kicker-row mb-3.5 md:mb-4">
              <p className="service-editorial-kicker text-[0.67rem] uppercase tracking-[0.18em] text-gray-400/82">What&apos;s Covered</p>
              <span className="service-editorial-kicker-line" aria-hidden />
            </div>
            <h2 id="covered-heading" className="service-editorial-title text-[1.55rem] md:text-[1.78rem] font-semibold tracking-tight leading-[1.16]">
              Care that keeps your site secure, fast and current
            </h2>
            <p className="service-editorial-copy mt-4 leading-relaxed text-[0.96rem] md:text-[1rem] max-w-[58ch]">
              Every plan is built from the same core of careful, routine work. The plan you choose decides how much of it we handle
              and how quickly we respond.
            </p>
            <p className="service-editorial-support mt-4 text-[0.8rem] md:text-[0.82rem] text-gray-400/78 uppercase tracking-[0.11em]">
              {care.covered.length} areas of care
            </p>
          </div>

          <div className="service-editorial-details lg:justify-self-end w-full lg:max-w-[34rem]">
            <ul className="service-editorial-list w-full" role="list">
              {care.covered.map(item => (
                <li key={item.title} className="service-editorial-item">
                  <span className="service-editorial-marker" aria-hidden />
                  <span className="service-editorial-item-text">
                    <strong className="font-semibold text-gray-100">{item.title}.</strong> {item.text}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </SectionWrapper>

      <SectionWrapper id="plans" aria-labelledby="plans-heading" className="mt-16 md:mt-20">
        <p className="text-[0.72rem] uppercase tracking-[0.16em] text-gray-400/85 mb-3">Care Plans</p>
        <h2 id="plans-heading" className="text-2xl md:text-3xl font-semibold text-gold leading-tight">
          Three plans, scoped to your site
        </h2>
        <p className="mt-3 max-w-3xl text-sm md:text-base text-gray-400 leading-relaxed">
          Every plan is tailored after a short review of your website or app, so you only pay for the care you need. We share
          pricing once we understand your setup.
        </p>
        <div className="mt-8 grid grid-cols-1 lg:grid-cols-3 gap-4 md:gap-5">
          {care.plans.map((plan, i) => (
            <article key={plan.id} className="about-card about-card--functional h-full p-5 md:p-6 flex flex-col">
              <p className="text-[11px] uppercase tracking-[0.18em] text-gold/70 mb-2">Plan {String(i + 1).padStart(2, '0')}</p>
              <h3 className="text-xl font-semibold text-gold leading-snug">{plan.name}</h3>
              <p className="mt-2 text-sm text-gray-400 leading-relaxed">{plan.bestFor}</p>
              <ul className="service-editorial-list mt-4" role="list">
                {plan.items.map(item => (
                  <li key={item} className="service-editorial-item">
                    <span className="service-editorial-marker" aria-hidden />
                    <span className="service-editorial-item-text">{item}</span>
                  </li>
                ))}
              </ul>
              <div className="mt-auto pt-6">
                <AnimatedButton variant="outline" to={contactHref} className={ctaClass}>
                  Ask About {plan.name} <span aria-hidden className="ml-1">→</span>
                </AnimatedButton>
              </div>
            </article>
          ))}
        </div>
      </SectionWrapper>

      <SectionWrapper id="how-it-works" className="about-card p-6 md:p-8 mt-16 md:mt-20" aria-labelledby="how-heading">
        <p className="text-[11px] tracking-[0.2em] uppercase text-gold/70">How It Works</p>
        <h2 id="how-heading" className="mt-2 text-xl md:text-2xl font-semibold text-gold leading-tight">
          From first review to ongoing care
        </h2>
        <ol className="mt-5 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 md:gap-6 text-sm text-gray-300/90 leading-relaxed" role="list">
          {care.steps.map((step, i) => (
            <li key={step.title} className="border-t border-gold/20 pt-4">
              <span className="block font-display text-2xl text-gold/80 leading-none mb-2">{`0${i + 1}`}</span>
              <b className="text-gray-100">{step.title}</b> {step.text}
            </li>
          ))}
        </ol>
      </SectionWrapper>

      <SectionWrapper id="faq" className="mt-16 md:mt-20" aria-labelledby="faq-heading">
        <p className="text-[0.72rem] uppercase tracking-[0.16em] text-gray-400/85 mb-3">Good to Know</p>
        <h2 id="faq-heading" className="text-2xl md:text-3xl font-semibold text-gold leading-tight mb-6 md:mb-8">
          Care plan questions
        </h2>
        <div className="space-y-3 md:space-y-4">
          {care.faq.map(item => (
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

      <SectionWrapper id="care-cta" aria-labelledby="care-cta-heading" className="about-card about-card--cta relative overflow-hidden p-7 sm:p-9 md:p-10 mt-16 md:mt-20">
        <div className="absolute inset-0 pointer-events-none" aria-hidden>
          <div className="absolute -top-10 right-[15%] w-32 h-32 rounded-full bg-gold/10 blur-3xl" />
        </div>
        <div className="relative z-[1] flex flex-col md:flex-row md:items-end md:justify-between gap-6 md:gap-8">
          <div className="max-w-2xl space-y-3">
            <p className="text-xs tracking-[0.2em] uppercase text-gold/70">Start a Care Plan</p>
            <h2 id="care-cta-heading" className="text-2xl md:text-3xl font-semibold text-gold leading-tight">Ready to hand over the upkeep?</h2>
            <p className="text-sm md:text-base text-gray-300/90 leading-relaxed">
              Tell us about your website or app and we will recommend the plan that fits, usually within one business day.
            </p>
          </div>
          <div className="md:pb-1">
            <AnimatedButton to={contactHref}>Discuss a Care Plan</AnimatedButton>
          </div>
        </div>
      </SectionWrapper>
    </div>
  );
}
