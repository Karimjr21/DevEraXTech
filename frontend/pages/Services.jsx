import SectionWrapper from '../components/ui/SectionWrapper';
import { useNavigate } from 'react-router-dom';
import { SERVICE_OPTIONS } from '../src/data/services';

export default function Services() {
  const navigate = useNavigate();
  const goToContact = (service) => navigate(`/contact?service=${encodeURIComponent(service)}`);

  const serviceCards = [
    {
      service: SERVICE_OPTIONS[0],
      title: 'Business / Corporate Websites',
      description: 'For companies, startups, agencies, shops, clinics, factories, schools, etc.',
      label: 'Includes',
      features: ['Home', 'About', 'Services', 'Contact', 'Team', 'Portfolio']
    },
    {
      service: SERVICE_OPTIONS[1],
      title: 'E-Commerce Websites',
      description: 'Online stores with:',
      label: 'Includes',
      features: ['Product pages', 'Shopping cart', 'Checkout', 'Payment integrations', 'Admin dashboard']
    },
    {
      service: SERVICE_OPTIONS[4],
      title: 'Shopify Stores',
      description: 'Bespoke Shopify experiences crafted for premium brands, featuring:',
      label: 'Includes',
      features: [
        'Elegantly designed product pages',
        'Seamless shopping cart experience',
        'Secure, trusted payment integrations',
        'Powerful Shopify admin & store control'
      ]
    },
    {
      service: SERVICE_OPTIONS[5],
      title: 'WordPress Websites',
      description: 'Bespoke WordPress experiences crafted for premium brands, featuring:',
      label: 'Includes',
      features: [
        'Custom-designed pages & layouts',
        'Fully responsive, high-performance builds',
        'Secure plugins & advanced functionality',
        'Powerful content management & admin control'
      ]
    },
    {
      service: SERVICE_OPTIONS[2],
      title: 'Portfolio Websites',
      description: 'For creatives:',
      label: 'Includes',
      features: ['Designers', 'Photographers', 'Developers', 'Agencies', 'High-visual showcase sites']
    },
    {
      service: SERVICE_OPTIONS[3],
      title: 'Landing Pages',
      description: 'High-conversion single pages for:',
      label: 'Includes',
      features: ['Marketing campaigns', 'App launches', 'Product launches', 'Service promotions']
    }
  ];

  const handleCardKeyDown = (event, service) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      goToContact(service);
    }
  };

  return (
    <div className="max-w-[1400px] mx-auto px-8 py-24">
      <div className="mb-10 md:mb-12">
        <p className="text-[0.72rem] uppercase tracking-[0.16em] text-gray-400/85 mb-3">What We Build</p>
        <div className="flex items-end gap-4">
          <h2 className="text-4xl font-bold gold-gradient-text">Services</h2>
          <span className="hidden sm:block h-px w-24 md:w-32 bg-gradient-to-r from-gold/55 to-transparent mb-2" aria-hidden />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 2xl:grid-cols-3 gap-8 items-stretch">
        {serviceCards.map((card, index) => (
          <SectionWrapper
            key={card.title}
            delay={index * 60}
            onClick={() => goToContact(card.service)}
            onKeyDown={(event) => handleCardKeyDown(event, card.service)}
            role="button"
            tabIndex={0}
            aria-label={`Select ${card.title} service`}
            className="service-card rounded-2xl p-7 md:p-8 h-full min-h-[19.25rem] md:min-h-[20rem] transform-gpu flex flex-col cursor-pointer"
          >
            <h3
              className={`service-card-title text-[1.6rem] md:text-[1.72rem] font-semibold tracking-tight leading-[1.16] ${card.title === 'Business / Corporate Websites' ? 'service-card-title--long max-w-[15ch]' : ''}`}
            >
              {card.title}
            </h3>

            <p className="service-card-copy mt-3 leading-relaxed text-[0.96rem] md:text-[0.99rem]">
              {card.description}
            </p>

            <div className="service-card-label mt-5 text-[0.69rem] uppercase tracking-[0.16em] text-gray-400/88">
              {card.label}
            </div>

            <ul className="service-feature-list mt-2 w-full" role="list">
              {card.features.map((feature) => (
                <li key={feature} className="service-feature-item">
                  <span className="service-feature-marker" aria-hidden />
                  <span className="service-feature-text">{feature}</span>
                </li>
              ))}
            </ul>
          </SectionWrapper>
        ))}
      </div>
    </div>
  );
}
