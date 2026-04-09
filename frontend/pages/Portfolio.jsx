import { useEffect, useState } from 'react';
import AnimatedButton from '../components/ui/AnimatedButton';
import SectionWrapper from '../components/ui/SectionWrapper';
import { fetchPortfolio } from '../lib/api';
import Lightbox from '../components/ui/Lightbox';

function getDescription(item) {
  if (item?.description && String(item.description).trim()) {
    return String(item.description).trim();
  }

  const category = item?.category || 'Digital Product';
  return `Premium ${category.toLowerCase()} delivery focused on performance, design quality, and secure implementation.`;
}

function getTags(item) {
  if (Array.isArray(item?.tags) && item.tags.length) {
    return item.tags.slice(0, 3);
  }

  return [item?.category || 'Digital Product', 'Responsive UX', 'Secure Build'];
}

export default function Portfolio() {
  const [items, setItems] = useState([]);
  const [filter, setFilter] = useState('All');
  const [active, setActive] = useState(null);
  const [imageFallbacks, setImageFallbacks] = useState({});

  useEffect(() => { fetchPortfolio().then(setItems); }, []);

  const categories = ['All', ...Array.from(new Set(items.map(i => i.category)))];
  const shown = filter === 'All' ? items : items.filter(i => i.category === filter);
  const hasSingle = shown.length === 1;
  const uniqueCategories = Array.from(new Set(items.map(i => i.category))).length;

  const openItem = (item) => {
    if (item.url) {
      window.open(item.url, '_blank', 'noopener,noreferrer');
      return;
    }
    setActive(item);
  };

  return (
    <div className="max-w-7xl mx-auto px-6 sm:px-8 pt-16 md:pt-20 pb-24 md:pb-28">
      <SectionWrapper className="space-y-10 md:space-y-12">
        <div className="portfolio-hero-card p-7 sm:p-9 md:p-10 grid lg:grid-cols-[1.12fr_0.88fr] gap-7 md:gap-9 lg:gap-10 items-end">
          <div className="space-y-4 md:space-y-5">
            <p className="text-[11px] tracking-[0.2em] uppercase text-gold/72">Selected Work</p>
            <h2 className="text-4xl md:text-5xl font-bold gold-gradient-text leading-[1.08]">Portfolio</h2>
            <p className="text-sm md:text-base text-gray-300/90 max-w-2xl leading-relaxed">
              A curated selection of digital platforms and web products delivered with premium execution standards.
            </p>
          </div>

          <div className="portfolio-note-card p-5 sm:p-6 space-y-3">
            <p className="text-[11px] tracking-[0.18em] uppercase text-gold/70">How We Deliver</p>
            <ul className="space-y-2.5 text-xs sm:text-sm text-gray-300/90">
              <li className="portfolio-check-row"><span className="portfolio-check-dot" aria-hidden />Security-led implementation</li>
              <li className="portfolio-check-row"><span className="portfolio-check-dot" aria-hidden />Performance-oriented experiences</li>
              <li className="portfolio-check-row"><span className="portfolio-check-dot" aria-hidden />Scalable architecture decisions</li>
            </ul>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          {categories.map(cat => (
            <button
              key={cat}
              onClick={() => setFilter(cat)}
              className={`portfolio-filter-pill ${filter===cat ? 'portfolio-filter-pill--active' : 'portfolio-filter-pill--idle'}`}
              aria-pressed={filter === cat}
            >
              {cat}
            </button>
          ))}
        </div>

        <div className="grid sm:grid-cols-3 gap-3 md:gap-4">
          <div className="portfolio-stat-chip">
            <p className="portfolio-stat-label">Projects</p>
            <p className="portfolio-stat-value">{items.length || 0}</p>
          </div>
          <div className="portfolio-stat-chip">
            <p className="portfolio-stat-label">Categories</p>
            <p className="portfolio-stat-value">{uniqueCategories || 0}</p>
          </div>
          <div className="portfolio-stat-chip">
            <p className="portfolio-stat-label">Showcased</p>
            <p className="portfolio-stat-value">Premium Delivery</p>
          </div>
        </div>

        {shown.length === 0 && (
          <div className="portfolio-empty-card p-8 sm:p-10 text-center">
            <h3 className="text-xl text-gold font-semibold mb-2">No Matching Projects</h3>
            <p className="text-sm text-gray-400">Try another filter to explore more portfolio work.</p>
          </div>
        )}

        {hasSingle ? (
          (() => {
            const item = shown[0];
            const tags = getTags(item);
            const description = getDescription(item);
            const showPlaceholder = !item.image || imageFallbacks[item.id];

            return (
              <SectionWrapper
                className="portfolio-card portfolio-featured-card group cursor-pointer"
                onClick={() => openItem(item)}
                onKeyDown={(event) => {
                  if (event.key === 'Enter' || event.key === ' ') {
                    event.preventDefault();
                    openItem(item);
                  }
                }}
                role="button"
                tabIndex={0}
              >
                <div className="portfolio-media-shell portfolio-media-shell--single">
                  {!showPlaceholder ? (
                    <img
                      src={item.image}
                      alt={item.title}
                      className="portfolio-media-img"
                      onError={() => setImageFallbacks(prev => ({ ...prev, [item.id]: true }))}
                      loading="lazy"
                    />
                  ) : (
                    <div className="portfolio-media-placeholder" aria-label="Project preview placeholder" role="img">
                      <div className="portfolio-media-placeholder-line" />
                      <div className="portfolio-media-placeholder-dot" />
                    </div>
                  )}
                  <div className="portfolio-media-overlay" aria-hidden />
                </div>

                <div className="p-6 sm:p-7 md:p-8 space-y-5">
                  <div className="space-y-3">
                    <p className="text-[11px] tracking-[0.16em] uppercase text-gold/70">{item.category}</p>
                    <h3 className="text-2xl md:text-[1.9rem] font-semibold text-gold leading-tight">{item.title}</h3>
                    <p className="text-sm md:text-base text-gray-300/90 leading-relaxed max-w-xl">{description}</p>
                  </div>

                  <div className="flex flex-wrap gap-2.5">
                    {tags.map((tag) => (
                      <span key={`${item.id}-${tag}`} className="portfolio-tag">{tag}</span>
                    ))}
                  </div>

                  <div>
                    {item.url ? (
                      <a
                        href={item.url}
                        target="_blank"
                        rel="noreferrer"
                        onClick={(event) => event.stopPropagation()}
                        className="portfolio-cta-link"
                      >
                        View Project <span aria-hidden>→</span>
                      </a>
                    ) : (
                      <button
                        type="button"
                        onClick={(event) => {
                          event.stopPropagation();
                          setActive(item);
                        }}
                        className="portfolio-cta-link"
                      >
                        See Details <span aria-hidden>→</span>
                      </button>
                    )}
                  </div>
                </div>
              </SectionWrapper>
            );
          })()
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5 md:gap-6">
            {shown.map((item, index) => {
              const tags = getTags(item);
              const description = getDescription(item);
              const showPlaceholder = !item.image || imageFallbacks[item.id];
              const featured = shown.length > 2 && index === 0;

              return (
                <SectionWrapper
                  key={item.id}
                  className={`portfolio-card group cursor-pointer ${featured ? 'md:col-span-2' : ''}`}
                  onClick={() => openItem(item)}
                  onKeyDown={(event) => {
                    if (event.key === 'Enter' || event.key === ' ') {
                      event.preventDefault();
                      openItem(item);
                    }
                  }}
                  role="button"
                  tabIndex={0}
                >
                  <div className={`portfolio-media-shell ${featured ? 'portfolio-media-shell--featured' : ''}`}>
                    {!showPlaceholder ? (
                      <img
                        src={item.image}
                        alt={item.title}
                        className="portfolio-media-img"
                        onError={() => setImageFallbacks(prev => ({ ...prev, [item.id]: true }))}
                        loading="lazy"
                      />
                    ) : (
                      <div className="portfolio-media-placeholder" aria-label="Project preview placeholder" role="img">
                        <div className="portfolio-media-placeholder-line" />
                        <div className="portfolio-media-placeholder-dot" />
                      </div>
                    )}
                    <div className="portfolio-media-overlay" aria-hidden />
                  </div>

                  <div className="p-5 sm:p-6 space-y-4">
                    <div className="space-y-2.5">
                      <p className="text-[11px] tracking-[0.16em] uppercase text-gold/70">{item.category}</p>
                      <h3 className="text-xl sm:text-[1.35rem] font-semibold text-gold leading-tight">{item.title}</h3>
                      <p className="text-sm text-gray-300/90 leading-relaxed portfolio-description-clamp">{description}</p>
                    </div>

                    <div className="flex flex-wrap gap-2">
                      {tags.map((tag) => (
                        <span key={`${item.id}-${tag}`} className="portfolio-tag">{tag}</span>
                      ))}
                    </div>

                    <div>
                      {item.url ? (
                        <a
                          href={item.url}
                          target="_blank"
                          rel="noreferrer"
                          onClick={(event) => event.stopPropagation()}
                          className="portfolio-cta-link"
                        >
                          View Project <span aria-hidden>→</span>
                        </a>
                      ) : (
                        <button
                          type="button"
                          onClick={(event) => {
                            event.stopPropagation();
                            setActive(item);
                          }}
                          className="portfolio-cta-link"
                        >
                          See Details <span aria-hidden>→</span>
                        </button>
                      )}
                    </div>
                  </div>
                </SectionWrapper>
              );
            })}
          </div>
        )}

        <div className="portfolio-bottom-cta p-7 sm:p-9 md:p-10">
          <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-6 md:gap-8">
            <div className="space-y-3 max-w-2xl">
              <p className="text-[11px] tracking-[0.2em] uppercase text-gold/70">Next Project</p>
              <h3 className="text-2xl md:text-3xl font-semibold text-gold leading-tight">Ready to launch your next premium digital product?</h3>
              <p className="text-sm md:text-base text-gray-300/90 leading-relaxed">
                Share your goals and we will map the right approach for secure, scalable, and high-impact delivery.
              </p>
            </div>
            <AnimatedButton to="/contact" className="w-full sm:w-auto min-w-[13rem]">Book a Meeting</AnimatedButton>
          </div>
        </div>
      </SectionWrapper>
      {active && <Lightbox item={active} onClose={()=>setActive(null)} />}
    </div>
  );
}
