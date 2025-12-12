import SectionWrapper from '../components/ui/SectionWrapper';
import { useNavigate } from 'react-router-dom';

export default function Services() {
  const navigate = useNavigate();
  const goToContact = (service) => navigate(`/contact?service=${encodeURIComponent(service)}`);
  return (
    <div className="max-w-[1400px] mx-auto px-8 py-24">
      <h2 className="text-4xl font-bold mb-12 gold-gradient-text">Services</h2>

      <div className="grid grid-cols-1 lg:grid-cols-2 2xl:grid-cols-3 gap-8 items-stretch">
        <SectionWrapper onClick={() => goToContact('Business / Corporate Websites')} className="lux-card rounded-2xl p-10 md:p-14 h-full min-h-80 transform-gpu flex flex-col items-center text-center gap-6 cursor-pointer">
          <h3 className="text-2xl md:text-3xl font-semibold heading-gold tracking-tight leading-tight">Business / Corporate Websites</h3>
          <p className="text-gray-300/90 max-w-xl leading-relaxed">
            For companies, startups, agencies, shops, clinics, factories, schools, etc.
          </p>
          <div className="text-sm text-gray-400">Includes:</div>
          <ul className="flex flex-wrap justify-center gap-4 w-full max-w-xl">
            {['Home','About','Services','Contact','Team','Portfolio'].map(item => (
              <li
                key={item}
                className="chip-lux w-36 h-10 inline-flex items-center justify-center rounded-md text-sm transition-all origin-center"
              >
                {item}
              </li>
            ))}
          </ul>
        </SectionWrapper>

        <SectionWrapper onClick={() => goToContact('E-Commerce Websites')} className="lux-card rounded-2xl p-10 md:p-14 h-full min-h-80 transform-gpu flex flex-col items-center text-center gap-6 cursor-pointer">
          <h3 className="text-2xl md:text-3xl font-semibold heading-gold tracking-tight leading-tight">E-Commerce Websites</h3>
          <p className="text-gray-300/90 max-w-xl leading-relaxed">Online stores with:</p>
          <ul className="flex flex-wrap justify-center gap-4 w-full max-w-xl">
            {['Product pages','Shopping cart','Checkout','Payment integrations','Admin dashboard'].map(item => (
              <li
                key={item}
                className="chip-lux w-40 h-10 inline-flex items-center justify-center rounded-md text-sm transition-all origin-center"
              >
                {item}
              </li>
            ))}
          </ul>
        </SectionWrapper>

        <SectionWrapper onClick={() => goToContact('Portfolio Websites')} className="lux-card rounded-2xl p-10 md:p-14 h-full min-h-80 transform-gpu flex flex-col items-center text-center gap-6 cursor-pointer">
          <h3 className="text-2xl md:text-3xl font-semibold heading-gold tracking-tight leading-tight">Portfolio Websites</h3>
          <p className="text-gray-300/90 max-w-xl leading-relaxed">For creatives:</p>
          <ul className="flex flex-wrap justify-center gap-4 w-full max-w-xl">
            {['Designers','Photographers','Developers','Agencies','High-visual showcase sites'].map(item => (
              <li
                key={item}
                className="chip-lux w-40 h-10 inline-flex items-center justify-center rounded-md text-sm transition-all origin-center"
              >
                {item}
              </li>
            ))}
          </ul>
        </SectionWrapper>

        <SectionWrapper onClick={() => goToContact('Landing Pages')} className="lux-card rounded-2xl p-10 md:p-14 h-full min-h-80 transform-gpu flex flex-col items-center text-center gap-6 cursor-pointer">
          <h3 className="text-2xl md:text-3xl font-semibold heading-gold tracking-tight leading-tight">Landing Pages</h3>
          <p className="text-gray-300/90 max-w-xl leading-relaxed">High-conversion single pages for:</p>
          <ul className="flex flex-wrap justify-center gap-4 w-full max-w-xl">
            {['Marketing campaigns','App launches','Product launches','Service promotions'].map(item => (
              <li
                key={item}
                className="chip-lux w-40 h-10 inline-flex items-center justify-center rounded-md text-sm transition-all origin-center"
              >
                {item}
              </li>
            ))}
          </ul>
        </SectionWrapper>
      </div>
    </div>
  );
}
