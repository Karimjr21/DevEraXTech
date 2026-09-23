import SectionWrapper from '../components/ui/SectionWrapper';
import { useNavigate } from 'react-router-dom';
import AnimatedButton from '../components/ui/AnimatedButton';
import EmptyState, { LoadingCards } from '../components/ui/EmptyState';
import { fetchServices } from '../lib/api';
import useApiData from '../lib/useApiData';

export default function Services() {
  const navigate = useNavigate();
  const goToContact = (service) => navigate(`/contact?service=${encodeURIComponent(service)}`);

  const { status, data: serviceCards, retry } = useApiData(fetchServices);

  return (
    <div className="max-w-[1400px] mx-auto px-8 py-24">
      <div className="mb-10 md:mb-12">
        <p className="text-[0.72rem] uppercase tracking-[0.16em] text-gray-400/85 mb-3">What We Build</p>
        <div className="flex items-end gap-4">
          <h2 className="text-4xl font-bold gold-gradient-text">Services</h2>
          <span className="hidden sm:block h-px w-24 md:w-32 bg-gradient-to-r from-gold/55 to-transparent mb-2" aria-hidden />
        </div>
      </div>

      {status === 'loading' && (
        <LoadingCards count={3} label="Loading services" className="space-y-6 md:space-y-8" />
      )}

      {status === 'error' && (
        <EmptyState
          icon="error"
          role="alert"
          title="We couldn't load our services"
          text="Something went wrong while fetching the service list. Please try again, or contact us directly and we'll walk you through what we offer."
          actionLabel="Try Again"
          onAction={retry}
          secondaryLabel="Contact Us"
          secondaryTo="/contact"
        />
      )}

      {status === 'ready' && serviceCards.length === 0 && (
        <EmptyState
          kicker="Updating"
          title="Our service list is being refreshed"
          text="We're updating our offerings. Tell us what you want to build and we'll tailor a solution for you."
          actionLabel="Book a Meeting"
          actionTo="/contact"
        />
      )}

      {status === 'ready' && serviceCards.length > 0 && (
      <div className="space-y-6 md:space-y-8 lg:space-y-10">
        {serviceCards.map((card, index) => (
          <SectionWrapper
            key={card.id || card.title}
            delay={index * 60}
            className="service-editorial-row rounded-2xl p-5 md:p-6 lg:p-7"
          >
            <div className="service-editorial-grid grid grid-cols-1 lg:grid-cols-2 gap-5 md:gap-6 lg:gap-8 items-start">
              <div className={`${index % 2 === 1 ? 'lg:order-2' : ''} service-editorial-pitch`}> 
                <div className="service-editorial-kicker-row mb-3.5 md:mb-4">
                  <p className="service-editorial-kicker text-[0.67rem] uppercase tracking-[0.18em] text-gray-400/82">
                    {`0${index + 1}`} / Premium Service
                  </p>
                  <span className="service-editorial-kicker-line" aria-hidden />
                </div>
                <h3
                  className={`service-editorial-title text-[1.55rem] md:text-[1.78rem] font-semibold tracking-tight leading-[1.16] ${card.title === 'Business / Corporate Websites' ? 'service-editorial-title--long max-w-[17ch]' : ''}`}
                >
                  {card.title}
                </h3>
                <p className="service-editorial-copy mt-4 leading-relaxed text-[0.96rem] md:text-[1rem] max-w-[58ch]">
                  {card.description}
                </p>

                <p className="service-editorial-support mt-4 text-[0.8rem] md:text-[0.82rem] text-gray-400/78 uppercase tracking-[0.11em]">
                  {(card.features || []).length} key capabilities
                </p>
              </div>

              <div className={`${index % 2 === 1 ? 'lg:order-1' : ''} service-editorial-details lg:justify-self-end w-full lg:max-w-[34rem]`}>
                <div className="service-editorial-includes text-[0.69rem] uppercase tracking-[0.16em] text-gray-400/88 mb-3">
                  {card.label || 'Includes'}
                </div>

                <ul className="service-editorial-list w-full" role="list">
                  {(card.features || []).map((feature) => (
                    <li key={feature} className="service-editorial-item">
                      <span className="service-editorial-marker" aria-hidden />
                      <span className="service-editorial-item-text">{feature}</span>
                    </li>
                  ))}
                </ul>

                <div className="mt-5 md:mt-6">
                  <AnimatedButton
                    variant="outline"
                    className="service-editorial-cta h-9 md:h-10 px-4.5 md:px-5 text-[0.8rem] md:text-[0.84rem] uppercase tracking-[0.08em]"
                    onClick={() => goToContact(card.title)}
                  >
                    Start This Project <span aria-hidden className="ml-1">→</span>
                  </AnimatedButton>
                </div>
              </div>
            </div>
          </SectionWrapper>
        ))}
      </div>
      )}
    </div>
  );
}
