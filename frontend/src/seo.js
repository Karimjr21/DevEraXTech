// Single source of truth for page titles, descriptions and structured data.
// Used by the build-time prerender (scripts/prerender.mjs) and by SeoManager at runtime.
import services from './data/services.json';
import faq from './data/faq.json';
import business from './data/business.json';

const AREAS_SHORT = 'Canada, the United States, the UAE, Saudi Arabia, Kuwait, Qatar and Egypt';

export const SITE = {
  name: 'DevEraXTech',
  url: 'https://deveraxtech.com',
  locale: 'en_US',
  logo: 'https://deveraxtech.com/icon-512.png',
  image: 'https://deveraxtech.com/og-image.jpg',
  imageAlt: 'DevEraXTech: premium web and app experiences',
  description:
    `DevEraXTech is a web design and development studio based in Cairo, Egypt, building secure, scalable, pixel-perfect websites (business and corporate sites, e-commerce, Shopify stores, WordPress websites, portfolios and landing pages) for clients in ${AREAS_SHORT}.`,
  foundingDate: '2024',
  founders: [
    { name: 'Karim Ahmed', jobTitle: 'Founder' },
    { name: 'Loay Mohamed', jobTitle: 'Co-founder' }
  ],
  sameAs: ['https://www.instagram.com/deveraxtech']
};

export const ROUTES = [
  {
    path: '/',
    file: 'index.html',
    name: 'Home',
    title: 'DevEraXTech | Web Design & Development Studio in Cairo',
    description:
      'Cairo-based studio building secure, pixel-perfect websites, e-commerce, Shopify and WordPress sites for clients in Egypt, the Gulf, the US and Canada.',
    priority: '1.0'
  },
  {
    path: '/services',
    file: 'services.html',
    name: 'Services',
    title: 'Web Design & Development Services | DevEraXTech',
    description:
      'Business websites, e-commerce, Shopify, WordPress, portfolio sites and landing pages for clients in Egypt, UAE, Saudi Arabia, Kuwait, Qatar, US and Canada.',
    priority: '0.9'
  },
  {
    path: '/portfolio',
    file: 'portfolio.html',
    name: 'Work',
    title: 'Our Work | DevEraXTech Portfolio',
    description:
      'Selected websites and digital products delivered by DevEraXTech with design precision, technical rigor and premium execution standards.',
    priority: '0.7'
  },
  {
    path: '/about',
    file: 'about.html',
    name: 'About',
    title: 'About DevEraXTech | Secure, Premium Digital Products',
    description:
      'Founded in 2024 in Cairo, Egypt by Karim Ahmed and Loay Mohamed, DevEraXTech builds premium digital products with security at the core.',
    priority: '0.8'
  },
  {
    path: '/contact',
    file: 'contact.html',
    name: 'Contact',
    title: 'Contact DevEraXTech | Book a Project Meeting',
    description:
      'Book a meeting with DevEraXTech in Cairo. Call +20 100 001 6216 or email deveraxtech@gmail.com. Open daily 9 AM to 5 PM Cairo time. Arabic, English, German.',
    priority: '0.9'
  }
];

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
    founder: SITE.founders.map(f => ({ '@type': 'Person', name: f.name, jobTitle: f.jobTitle })),
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
      'Website security'
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
      name: 'Web design and development services',
      itemListElement: services.map(s => ({
        '@type': 'Offer',
        itemOffered: { '@type': 'Service', '@id': `${SITE.url}/services#${s.id}`, name: s.title }
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

function servicesList() {
  return {
    '@type': 'ItemList',
    '@id': `${SITE.url}/services#list`,
    name: 'DevEraXTech services',
    itemListElement: services.map((s, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      item: {
        '@type': 'Service',
        '@id': `${SITE.url}/services#${s.id}`,
        name: s.title,
        serviceType: s.title,
        description: s.summary,
        provider: { '@id': ORG_ID },
        url: `${SITE.url}/contact?service=${encodeURIComponent(s.title)}`
      }
    }))
  };
}

function faqPage(url) {
  return {
    '@type': 'FAQPage',
    '@id': `${url}#faq`,
    mainEntity: faq.map(f => ({
      '@type': 'Question',
      name: f.question,
      acceptedAnswer: { '@type': 'Answer', text: f.answer }
    }))
  };
}

export function buildJsonLd(route) {
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
    inLanguage: 'en'
  };
  if (route.path !== '/') {
    page.breadcrumb = {
      '@type': 'BreadcrumbList',
      itemListElement: [
        { '@type': 'ListItem', position: 1, name: 'Home', item: `${SITE.url}/` },
        { '@type': 'ListItem', position: 2, name: route.name, item: url }
      ]
    };
  }
  graph.push(page);
  if (route.path === '/services') {
    graph.push(servicesList(), faqPage(url));
    page.mainEntity = { '@id': `${SITE.url}/services#list` };
  }
  return { '@context': 'https://schema.org', '@graph': graph };
}

export { services, faq, business };
