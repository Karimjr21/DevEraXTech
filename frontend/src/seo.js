// Single source of truth for page titles, descriptions and structured data.
// Used by the build-time prerender (scripts/prerender.mjs) and by SeoManager at runtime.
import services from './data/services.json';
import faq from './data/faq.json';
import business from './data/business.json';
import portfolio from './data/portfolio.json';
import maintenance from './data/maintenance.json';
import serviceDetails from './data/service-details.json';
import pageFaqs from './data/page-faqs.json';

const AREAS_SHORT = 'Canada, the United States, the UAE, Saudi Arabia, Kuwait, Qatar and Egypt';

export const SITE = {
  name: 'DevEraXTech',
  url: 'https://deveraxtech.com',
  locale: 'en_US',
  logo: 'https://deveraxtech.com/icon-512.png',
  image: 'https://deveraxtech.com/og-image.jpg',
  imageAlt: 'DevEraXTech: premium web and app experiences',
  description:
    `DevEraXTech is a web design and development studio based in Cairo, Egypt, building secure, scalable, pixel-perfect websites, online stores, web and mobile apps, desktop software and AI integrations, with ongoing care plans, for clients in ${AREAS_SHORT}.`,
  foundingDate: '2024',
  founders: [
    { name: 'Karim Ahmed', jobTitle: 'Founder', url: 'https://karim.deveraxtech.com/' },
    { name: 'Loay Mohamed', jobTitle: 'Co-founder' }
  ],
  sameAs: ['https://www.instagram.com/deveraxtech']
};

export const ROUTES = [
  {
    path: '/',
    source: ['pages/Home.jsx', 'src/data/page-faqs.json', 'src/data/services.json'],
    file: 'index.html',
    name: 'Home',
    title: 'DevEraXTech | Web Design & Development Studio in Cairo',
    description:
      'Cairo studio building secure, pixel-perfect websites, online stores, web and mobile apps, AI integrations and care plans for Egypt, the Gulf, US and Canada.',
    priority: '1.0'
  },
  {
    path: '/services',
    source: ['pages/Services.jsx', 'src/data/services.json', 'src/data/faq.json'],
    file: 'services.html',
    name: 'Services',
    title: 'Web, App & Software Development Services | DevEraXTech',
    description:
      'Websites, online stores, web and mobile apps, desktop software, AI and payment integrations, SEO, redesigns, UI/UX design and care plans from a Cairo studio.',
    priority: '0.9'
  },
  {
    path: '/maintenance',
    source: ['pages/Maintenance.jsx', 'src/data/maintenance.json'],
    file: 'maintenance.html',
    name: 'Maintenance & Care Plans',
    parent: '/services',
    title: 'Website Maintenance & Care Plans | DevEraXTech',
    description:
      'Website and app care plans from DevEraXTech in Cairo: updates, security patches, backups, uptime monitoring, performance checks and priority support.',
    priority: '0.8'
  },
  {
    path: '/portfolio',
    source: ['pages/Portfolio.jsx', 'src/data/portfolio.json', 'src/data/page-faqs.json', 'components/ui/ShowcaseMedia.jsx'],
    file: 'portfolio.html',
    name: 'Work',
    title: 'Web Design Portfolio | DevEraXTech, Cairo',
    description:
      'DevEraXTech web design portfolio: the Nilora Estates MERN real estate platform, the karim.deveraxtech.com developer portfolio website and more from Cairo.',
    priority: '0.7'
  },
  {
    path: '/about',
    source: ['pages/About.jsx', 'src/data/page-faqs.json'],
    file: 'about.html',
    name: 'About',
    title: 'About DevEraXTech | Secure, Premium Digital Products',
    description:
      'Founded in 2024 in Cairo, Egypt by Karim Ahmed and Loay Mohamed, DevEraXTech builds premium digital products with security at the core.',
    priority: '0.8'
  },
  {
    path: '/contact',
    source: ['pages/Contact.jsx', 'src/data/page-faqs.json', 'src/data/business.json'],
    file: 'contact.html',
    name: 'Contact',
    title: 'Contact DevEraXTech | Book a Project Meeting',
    description:
      'Book a meeting with DevEraXTech in Cairo. Call +20 100 001 6216 or email deveraxtech@gmail.com. Open daily 9 AM to 5 PM Cairo time. Arabic, English, German.',
    priority: '0.9'
  }
];

// Every service has its own page at /services/<id>, except services that already
// point to a dedicated page through `link` (e.g. Maintenance & Care Plans -> /maintenance).
export const servicePath = s => s.link || `/services/${s.id}`;

export const SERVICE_ROUTES = services
  .filter(s => !s.link && serviceDetails[s.id])
  .map(s => ({
    path: servicePath(s),
    file: `services/${s.id}.html`,
    name: s.title,
    parent: '/services',
    serviceId: s.id,
    source: ['pages/ServiceDetail.jsx', 'src/data/service-details.json', 'src/data/services.json'],
    title: serviceDetails[s.id].seoTitle,
    description: serviceDetails[s.id].seoDescription,
    priority: '0.8'
  }));

ROUTES.push(...SERVICE_ROUTES);

export const NOT_FOUND = {
  path: '/404',
  file: '404.html',
  name: 'Page not found',
  title: 'Page Not Found | DevEraXTech',
  description: 'The page you are looking for does not exist. Explore DevEraXTech services or get in touch.',
  noindex: true
};

export function getRouteMeta(pathname) {
  const clean = pathname !== '/' ? pathname.replace(/\/+$/, '') : '/';
  return ROUTES.find(r => r.path === clean) || NOT_FOUND;
}

export function canonicalUrl(path) {
  return path === '/' ? `${SITE.url}/` : `${SITE.url}${path}`;
}

const ORG_ID = `${SITE.url}/#organization`;
const WEBSITE_ID = `${SITE.url}/#website`;

function openingHours() {
  return {
    '@type': 'OpeningHoursSpecification',
    dayOfWeek: business.hours.days.map(d => `https://schema.org/${d}`),
    opens: business.hours.opens,
    closes: business.hours.closes
  };
}

function organization() {
  return {
    '@type': ['Organization', 'ProfessionalService'],
    '@id': ORG_ID,
    name: SITE.name,
    url: `${SITE.url}/`,
    logo: { '@type': 'ImageObject', url: SITE.logo, width: 512, height: 512 },
    image: SITE.image,
    description: SITE.description,
    foundingDate: SITE.foundingDate,
    founder: SITE.founders.map(f => ({
      '@type': 'Person',
      name: f.name,
      jobTitle: f.jobTitle,
      ...(f.url ? { url: f.url, sameAs: [f.url] } : {})
    })),
    sameAs: SITE.sameAs,
    email: business.email,
    telephone: business.phoneE164,
    address: {
      '@type': 'PostalAddress',
      addressLocality: business.city,
      addressCountry: business.countryCode
    },
    areaServed: business.areasServed.map(a => ({ '@type': 'Country', name: a.name, identifier: a.code })),
    knowsLanguage: business.languages.map(l => l.code),
    openingHoursSpecification: [openingHours()],
    slogan: 'Secure. Scalable. Pixel-perfect.',
    knowsAbout: [
      'Web design',
      'Web development',
      'E-commerce development',
      'Shopify development',
      'WordPress development',
      'Landing page design',
      'Website security',
      'Web application development',
      'Mobile app development',
      'React Native',
      'Desktop software development',
      'AI integration',
      'Chatbot development',
      'Payment gateway integration',
      'Website maintenance',
      'Search engine optimization',
      'Website performance optimization',
      'Website redesign',
      'Website migration',
      'UI/UX design'
    ],
    contactPoint: {
      '@type': 'ContactPoint',
      contactType: 'sales',
      telephone: business.phoneE164,
      email: business.email,
      url: `${SITE.url}/contact`,
      areaServed: business.areasServed.map(a => a.code),
      availableLanguage: business.languages.map(l => l.name),
      hoursAvailable: openingHours()
    },
    hasOfferCatalog: {
      '@type': 'OfferCatalog',
      name: 'Web, app and software development services',
      itemListElement: services.map(s => ({
        '@type': 'Offer',
        itemOffered: { '@type': 'Service', '@id': serviceId(s), name: s.title, url: `${SITE.url}${servicePath(s)}` }
      }))
    }
  };
}

function website() {
  return {
    '@type': 'WebSite',
    '@id': WEBSITE_ID,
    url: `${SITE.url}/`,
    name: SITE.name,
    description: SITE.description,
    publisher: { '@id': ORG_ID },
    inLanguage: 'en'
  };
}

function serviceId(s) {
  return `${SITE.url}${servicePath(s)}#service`;
}

function serviceNode(s, full = false) {
  const detail = serviceDetails[s.id];
  return {
    '@type': 'Service',
    '@id': serviceId(s),
    name: s.title,
    serviceType: s.title,
    ...(s.group ? { category: s.group } : {}),
    description: s.summary,
    provider: { '@id': ORG_ID },
    url: `${SITE.url}${servicePath(s)}`,
    ...(full
      ? {
          areaServed: business.areasServed.map(a => ({ '@type': 'Country', name: a.name })),
          availableLanguage: business.languages.map(l => l.name),
          ...(detail?.audience ? { audience: { '@type': 'Audience', audienceType: detail.audience.join(', ') } } : {}),
          hasOfferCatalog: {
            '@type': 'OfferCatalog',
            name: `${s.title}: what is included`,
            itemListElement: (s.features || []).map(f => ({ '@type': 'Offer', itemOffered: { '@type': 'Service', name: f } }))
          },
          potentialAction: {
            '@type': 'CommunicateAction',
            name: `Start a ${s.title} project`,
            target: `${SITE.url}/contact?service=${encodeURIComponent(s.title)}`
          }
        }
      : {})
  };
}

function servicesList() {
  return {
    '@type': 'ItemList',
    '@id': `${SITE.url}/services#list`,
    name: 'DevEraXTech services',
    itemListElement: services.map((s, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      item: serviceNode(s)
    }))
  };
}

const absolute = path => (/^https?:\/\//.test(path) ? path : `${SITE.url}${path}`);

function portfolioList() {
  return {
    '@type': 'ItemList',
    '@id': `${SITE.url}/portfolio#list`,
    name: 'DevEraXTech web design and development projects',
    itemListElement: portfolio.map((p, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      item: {
        '@type': 'CreativeWork',
        '@id': `${SITE.url}/portfolio#${p.id}`,
        name: p.title,
        description: p.description,
        url: p.url,
        genre: p.category,
        keywords: [...(p.tags || []), ...(p.stack || [])].join(', '),
        dateCreated: p.year,
        creator: { '@id': ORG_ID },
        ...(p.services ? { about: p.services.map(id => services.find(s => s.id === id)).filter(Boolean).map(s => ({ '@id': serviceId(s) })) } : {}),
        ...(p.client ? { sourceOrganization: { '@type': 'Organization', name: p.client, url: p.url } } : {}),
        ...(p.location ? { locationCreated: { '@type': 'Place', name: p.location } } : {}),
        ...(p.image
          ? {
              image: {
                '@type': 'ImageObject',
                url: absolute(p.image),
                caption: p.imageAlt || p.title,
                ...(p.imageWidth ? { width: p.imageWidth, height: p.imageHeight } : {})
              }
            }
          : {})
      }
    }))
  };
}

function faqPage(url, items = faq) {
  return {
    '@type': 'FAQPage',
    '@id': `${url}#faq`,
    mainEntity: items.map(f => ({
      '@type': 'Question',
      name: f.question,
      acceptedAnswer: { '@type': 'Answer', text: f.answer }
    }))
  };
}

// `dateModified` (YYYY-MM-DD) comes from git history at build time; see scripts/prerender.mjs.
export function buildJsonLd(route, { dateModified } = {}) {
  const url = canonicalUrl(route.path);
  const pageType = route.path === '/about' ? 'AboutPage' : route.path === '/contact' ? 'ContactPage' : route.path === '/portfolio' ? 'CollectionPage' : 'WebPage';
  const graph = [organization(), website()];
  if (route.noindex) return { '@context': 'https://schema.org', '@graph': graph };

  const page = {
    '@type': pageType,
    '@id': `${url}#webpage`,
    url,
    name: route.title,
    description: route.description,
    isPartOf: { '@id': WEBSITE_ID },
    about: { '@id': ORG_ID },
    primaryImageOfPage: { '@type': 'ImageObject', url: SITE.image },
    inLanguage: 'en',
    author: { '@id': ORG_ID },
    publisher: { '@id': ORG_ID },
    ...(dateModified ? { dateModified } : {})
  };
  if (route.path !== '/') {
    const parent = route.parent && ROUTES.find(r => r.path === route.parent);
    const crumbs = [
      { name: 'Home', item: `${SITE.url}/` },
      ...(parent ? [{ name: parent.name, item: canonicalUrl(parent.path) }] : []),
      { name: route.name, item: url }
    ];
    page.breadcrumb = {
      '@type': 'BreadcrumbList',
      itemListElement: crumbs.map((c, i) => ({ '@type': 'ListItem', position: i + 1, ...c }))
    };
  }
  graph.push(page);
  if (route.path === '/services') {
    graph.push(servicesList(), faqPage(url));
    page.mainEntity = { '@id': `${SITE.url}/services#list` };
  }
  if (route.path === '/maintenance') {
    const svc = services.find(s => s.id === 'maintenance-care-plans');
    if (svc) {
      graph.push(serviceNode(svc));
      page.mainEntity = { '@id': serviceId(svc) };
    }
    graph.push(faqPage(url, maintenance.faq));
  }
  const PAGE_FAQ_KEYS = { '/': 'home', '/about': 'about', '/contact': 'contact', '/portfolio': 'portfolio' };
  const faqKey = PAGE_FAQ_KEYS[route.path];
  if (faqKey && pageFaqs[faqKey]?.length) graph.push(faqPage(url, pageFaqs[faqKey]));
  if (route.serviceId) {
    const svc = services.find(s => s.id === route.serviceId);
    const detail = serviceDetails[route.serviceId];
    graph.push(serviceNode(svc, true));
    page.mainEntity = { '@id': serviceId(svc) };
    page.about = { '@id': serviceId(svc) };
    if (detail?.faq?.length) graph.push(faqPage(url, detail.faq));
    const work = portfolio.filter(p => (detail?.work || []).includes(p.id));
    if (work.length) page.mentions = work.map(p => ({ '@type': 'CreativeWork', '@id': `${SITE.url}/portfolio#${p.id}`, name: p.title, url: p.url }));
  }
  if (route.path === '/portfolio' && portfolio.length) {
    graph.push(portfolioList());
    page.mainEntity = { '@id': `${SITE.url}/portfolio#list` };
  }
  return { '@context': 'https://schema.org', '@graph': graph };
}

export { services, faq, business, portfolio, serviceDetails, pageFaqs };
