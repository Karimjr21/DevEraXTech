import AnimatedButton from '../components/ui/AnimatedButton';
import SectionWrapper from '../components/ui/SectionWrapper';

const timeline = [
  { year: '2024', text: 'Founded with mission to craft premium digital experiences.' },
  { year: '2025', text: 'Scaled delivery process & shipped 10+ projects.' }
];

const team = [
  { name: 'Karim Ahmed ', role: 'CEO (Chief Executive Officer)' },
  { name: 'Loay Mohamed', role: 'CFO (Chief Financial Officer)' },
  { name: 'Amr Hazem', role: 'CTO (Chief Technology Officer)' },
  { name: 'Mohamed Ayman', role: 'Operation Manager' }
];

const trustSignals = [
  {
    title: 'Secure by Design',
    detail: 'Security-focused planning from architecture to launch.'
  },
  {
    title: 'Scalable Delivery',
    detail: 'Reliable project structure designed for growth.'
  },
  {
    title: 'Premium Execution',
    detail: 'High-fidelity product quality and controlled detail.'
  },
  {
    title: 'Clear Communication',
    detail: 'Transparent updates, aligned milestones, and accountability.'
  }
];

const pillars = [
  {
    key: 'shield',
    title: 'Secure by Design',
    text: 'Security is embedded from architecture decisions to final QA, reducing risk before launch.'
  },
  {
    key: 'scale',
    title: 'Scalable Delivery',
    text: 'Structured execution keeps projects reliable as scope grows, from pilot releases to production.'
  },
  {
    key: 'design',
    title: 'Design-Led Execution',
    text: 'Every interface is shaped for clarity, conversion, and premium brand consistency.'
  },
  {
    key: 'client',
    title: 'Premium Client Experience',
    text: 'High-touch communication, clear milestones, and thoughtful delivery at every stage.'
  }
];

function getInitials(name) {
  return name
    .trim()
    .split(/\s+/)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase() || '')
    .join('');
}

function ApproachIcon({ icon }) {
  const common = 'w-5 h-5 text-gold/90';

  if (icon === 'shield') {
    return (
      <svg className={common} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" aria-hidden>
        <path d="M12 3l7 3v5c0 4.7-2.7 8.1-7 10-4.3-1.9-7-5.3-7-10V6l7-3z" />
        <path d="M9.5 12.3l1.7 1.8 3.3-3.4" />
      </svg>
    );
  }

  if (icon === 'scale') {
    return (
      <svg className={common} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" aria-hidden>
        <path d="M12 4v16" />
        <path d="M6 8h12" />
        <path d="M6.5 8l-2.8 5.2a2.5 2.5 0 0 0 2.2 3.8h1.2a2.5 2.5 0 0 0 2.2-3.8L6.5 8z" />
        <path d="M17.5 8l-2.8 5.2a2.5 2.5 0 0 0 2.2 3.8h1.2a2.5 2.5 0 0 0 2.2-3.8L17.5 8z" />
      </svg>
    );
  }

  if (icon === 'design') {
    return (
      <svg className={common} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" aria-hidden>
        <path d="M4 7h16" />
        <path d="M7 4v6" />
        <rect x="5" y="11" width="14" height="9" rx="2" />
      </svg>
    );
  }

  return (
    <svg className={common} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" aria-hidden>
      <path d="M8.5 10.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7z" />
      <path d="M15.5 12.5a4.5 4.5 0 1 0 0-9 4.5 4.5 0 0 0 0 9z" />
      <path d="M3 20c0-3.2 2.6-5.8 5.8-5.8S14.6 16.8 14.6 20" />
      <path d="M11 20c.4-2.3 2.4-4 4.8-4 2.7 0 4.8 1.9 5.2 4" />
    </svg>
  );
}

export default function About() {
  return (
    <div className="max-w-7xl mx-auto px-6 sm:px-8 pt-12 md:pt-16 pb-24 md:pb-28 space-y-16 md:space-y-20 lg:space-y-24">
      <SectionWrapper id="about-intro" className="relative overflow-hidden rounded-2xl border border-gold/15 about-hero-surface p-7 sm:p-10 lg:p-12">
        <div className="about-grid-texture" aria-hidden />
        <div className="absolute inset-0 pointer-events-none" aria-hidden>
          <div className="absolute -top-16 right-[8%] w-44 h-44 rounded-full bg-gold/10 blur-3xl" />
          <div className="absolute bottom-10 left-[10%] w-36 h-36 rounded-full bg-gold/8 blur-3xl" />
        </div>

        <div className="relative z-[1] grid lg:grid-cols-[1.1fr_0.9fr] gap-10 lg:gap-12 items-end">
          <div className="space-y-6">
            <span className="chip-lux inline-flex items-center rounded-full px-4 py-2 text-[11px] tracking-[0.2em] uppercase">
              About DevEraXTech
            </span>

            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold gold-gradient-text leading-[1.09] tracking-tight max-w-3xl">
              We build premium digital products with security at the core.
            </h1>

            <p className="text-base md:text-lg text-gray-300/90 max-w-2xl leading-relaxed">
              DevEraXTech delivers future-grade software with disciplined engineering, strong design direction, and dependable execution.
            </p>

            <div className="pt-1 flex flex-wrap items-center gap-3 text-[11px] tracking-[0.16em] uppercase text-gray-400/80">
              <span>Secure</span>
              <span className="text-gold/45" aria-hidden>•</span>
              <span>Scalable</span>
              <span className="text-gold/45" aria-hidden>•</span>
              <span>Premium Delivery</span>
            </div>
          </div>

          <div className="about-card about-card--functional p-5 sm:p-6 lg:p-7">
            <p className="text-[11px] uppercase tracking-[0.2em] text-gold/75 mb-3">Operating Principle</p>
            <p className="text-sm md:text-base text-gray-300/90 leading-relaxed">
              Each project is treated as a long-term digital asset, engineered for resilience, elegant usability, and growth.
            </p>
          </div>
        </div>
      </SectionWrapper>

      <SectionWrapper id="trust-signals" className="space-y-7 md:space-y-8">
        <div className="max-w-3xl space-y-2">
          <p className="text-xs tracking-[0.2em] uppercase text-gold/70">Trust Signals</p>
          <h2 className="text-2xl md:text-3xl font-semibold text-gold leading-tight">Built for clarity, scale, and confidence</h2>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-5">
          {trustSignals.map((signal) => (
            <article
              key={signal.title}
              className="group about-card about-card--functional p-4 md:p-5"
            >
              <div className="about-functional-icon mb-3" aria-hidden />
              <p className="text-[11px] uppercase tracking-[0.16em] text-gold/75 mb-2">Value</p>
              <h3 className="text-sm md:text-base text-gold font-semibold leading-snug mb-2">{signal.title}</h3>
              <p className="text-xs md:text-sm text-gray-400 leading-relaxed">{signal.detail}</p>
            </article>
          ))}
        </div>
      </SectionWrapper>

      <SectionWrapper id="who-we-are" className="space-y-8 md:space-y-9">
        <div className="max-w-3xl space-y-3">
          <p className="text-xs tracking-[0.2em] uppercase text-gold/70">Who We Are</p>
          <h2 className="text-2xl md:text-3xl font-semibold text-gold leading-tight">What We Build</h2>
        </div>

        <div className="about-card about-card--editorial p-6 md:p-8 lg:p-10 grid lg:grid-cols-[1.14fr_0.86fr] gap-8 lg:gap-10">
          <div className="space-y-4">
            <p className="text-gray-200/90 leading-relaxed">
              DevEraXTech is a focused product and engineering studio delivering premium digital platforms with disciplined execution.
            </p>
            <p className="text-gray-400 leading-relaxed">
              Our work balances modern product design with robust implementation to help ambitious brands launch and scale with confidence.
            </p>
          </div>

          <div className="space-y-4 lg:border-l lg:border-gold/15 lg:pl-7">
            <p className="text-sm uppercase tracking-[0.18em] text-gold/75">Core Focus</p>
            <ul className="space-y-3 text-sm text-gray-300/90">
              <li className="flex items-start gap-3">
                <span className="mt-2 w-1.5 h-1.5 rounded-full bg-gold/80" aria-hidden />
                <span>Secure, production-ready web and app solutions</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="mt-2 w-1.5 h-1.5 rounded-full bg-gold/80" aria-hidden />
                <span>High-fidelity user experience and interface systems</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="mt-2 w-1.5 h-1.5 rounded-full bg-gold/80" aria-hidden />
                <span>Scalable technical foundations for long-term growth</span>
              </li>
            </ul>
          </div>
        </div>
      </SectionWrapper>

      <SectionWrapper id="timeline" className="space-y-8 md:space-y-10">
        <div className="max-w-3xl space-y-3">
          <p className="text-xs tracking-[0.2em] uppercase text-gold/70">Journey</p>
          <h2 className="text-2xl md:text-3xl font-semibold text-gold leading-tight">Timeline</h2>
          <p className="text-sm md:text-base text-gray-400 leading-relaxed">
            A concise view of how DevEraXTech has evolved with consistent quality and delivery discipline.
          </p>
        </div>

        <div className="relative mt-2">
          <div
            className="hidden md:block absolute left-[3.4rem] top-2 bottom-2 w-px bg-gradient-to-b from-gold/40 via-gold/18 to-gold/10"
            aria-hidden
          />

          <div className="space-y-6 md:space-y-8">
            {timeline.map((item) => (
              <article key={item.year} className="md:grid md:grid-cols-[6.8rem_1fr] md:gap-8 items-start">
                <div className="mb-3 md:mb-0 md:pt-1">
                  <span className="inline-flex items-center justify-center min-w-[4.2rem] rounded-full border border-gold/35 bg-gold/10 px-4 py-1.5 text-sm font-semibold tracking-[0.08em] text-gold">
                    {item.year}
                  </span>
                </div>

                <div className="about-card about-card--functional p-5 md:p-6">
                  <p className="text-sm md:text-base text-gray-300/90 leading-relaxed">{item.text}</p>
                </div>
              </article>
            ))}
          </div>
        </div>
      </SectionWrapper>

      <SectionWrapper id="team" className="space-y-8 md:space-y-10">
        <div className="max-w-3xl space-y-3">
          <p className="text-xs tracking-[0.2em] uppercase text-gold/70">People</p>
          <h2 className="text-2xl md:text-3xl font-semibold text-gold leading-tight">Team</h2>
          <p className="text-sm md:text-base text-gray-400 leading-relaxed">
            A multidisciplinary team aligned around precision, trust, and premium execution standards.
          </p>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 md:gap-6">
          {team.map((member) => (
            <article
              key={member.name}
              className="about-card about-card--team group p-5 md:p-6 min-h-[220px] h-full flex flex-col justify-between"
            >
              <div className="about-avatar-chip w-14 h-14 rounded-full flex items-center justify-center text-sm font-semibold text-gold tracking-[0.08em]">
                {getInitials(member.name)}
              </div>

              <div className="space-y-2 pt-7">
                <h3 className="text-base md:text-lg font-semibold text-gold leading-snug">{member.name.trim()}</h3>
                <p className="text-xs md:text-sm text-gray-400 leading-relaxed">{member.role}</p>
              </div>
            </article>
          ))}
        </div>
      </SectionWrapper>

      <SectionWrapper id="why-deveraxtech" className="space-y-8 md:space-y-10">
        <div className="max-w-3xl space-y-3">
          <p className="text-xs tracking-[0.2em] uppercase text-gold/70">Why DevEraXTech</p>
          <h2 className="text-2xl md:text-3xl font-semibold text-gold leading-tight">Our Approach</h2>
          <p className="text-sm md:text-base text-gray-400 leading-relaxed">
            We combine security, execution quality, and design intent to build digital products that remain dependable long after launch.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-5 md:gap-6">
          {pillars.map((pillar) => (
            <article
              key={pillar.title}
              className="about-card about-card--feature group relative overflow-hidden p-5 md:p-6"
            >
              <div className="about-feature-glow pointer-events-none absolute -top-16 -right-16 w-44 h-44 rounded-full opacity-0 group-hover:opacity-100" aria-hidden />

              <div className="relative z-[1]">
                <div className="about-feature-icon mb-4 inline-flex h-10 w-10 items-center justify-center rounded-lg border border-gold/25 bg-gold/10">
                  <ApproachIcon icon={pillar.key} />
                </div>
                <h3 className="text-lg font-semibold text-gold mb-2">{pillar.title}</h3>
                <p className="text-sm text-gray-300/90 leading-relaxed">{pillar.text}</p>
              </div>
            </article>
          ))}
        </div>
      </SectionWrapper>

      <SectionWrapper id="about-cta" className="about-card about-card--cta relative overflow-hidden p-7 sm:p-9 md:p-10">
        <div className="absolute inset-0 pointer-events-none" aria-hidden>
          <div className="absolute -top-10 right-[15%] w-32 h-32 rounded-full bg-gold/10 blur-3xl" />
        </div>

        <div className="relative z-[1] flex flex-col md:flex-row md:items-end md:justify-between gap-6 md:gap-8">
          <div className="max-w-2xl space-y-3">
            <p className="text-xs tracking-[0.2em] uppercase text-gold/70">Start Your Project</p>
            <h2 className="text-2xl md:text-3xl font-semibold text-gold leading-tight">Ready to build a secure premium digital product?</h2>
            <p className="text-sm md:text-base text-gray-300/90 leading-relaxed">
              Partner with DevEraXTech for thoughtful strategy, strong engineering, and polished delivery.
            </p>
          </div>

          <div className="md:pb-1">
            <AnimatedButton to="/contact">Book a Meeting</AnimatedButton>
          </div>
        </div>
      </SectionWrapper>
    </div>
  );
}