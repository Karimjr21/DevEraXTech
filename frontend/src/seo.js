// Single source of truth for page titles, descriptions and structured data.
// Used by the build-time prerender (scripts/prerender.mjs) and by SeoManager at runtime.
import services from './data/services.json';
import faq from './data/faq.json';

export const SITE = {
  name: 'DevEraXTech',
  url: 'https://deveraxtech.com',
  locale: 'en_US',
  logo: 'https://deveraxtech.com/icon-512.png',
  image: 'https://deveraxtech.com/og-image.jpg',
  imageAlt: 'DevEraXTech — premium web & app experiences',
  description:
    'DevEraXTech is a web design and development studio building secure, scalable, pixel-perfect websites: business and corporate sites, e-commerce, Shopify stores, WordPress websites, portfolios and landing pages.',
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
    title: 'DevEraXTech | Premium Web Design & Development Studio',
    description:
      'DevEraXTech designs and builds secure, scalable, pixel-perfect websites — business sites, e-commerce, Shopify, WordPress, portfolios and landing pages.',
    priority: '1.0'
  },
  {
    path: '/services',
    file: 'services.html',
    name: 'Services',
    title: 'Web Design & Development Services | DevEraXTech',
    description:
      'Business and corporate websites, e-commerce stores, Shopify stores, WordPress websites, portfolio sites and high-conversion landing pages by DevEraXTech.',
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
      'Founded in 2024 by Karim Ahmed and Loay Mohamed, DevEraXTech builds premium digital products with disciplined engineering and security at the core.',
    priority: '0.8'
  },
  {
    path: '/contact',
    file: 'contact.html',
    name: 'Contact',
    title: 'Contact DevEraXTech | Book a Project Meeting',
    description:
      'Tell us about your website or app project and book a meeting with DevEraXTech. Most inquiries receive a response within one business day.',
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

function organization() {
  return {
    '@type': 'Organization',
    '@id': ORG_ID,
    name: SITE.name,
    url: `${SITE.url}/`,
    logo: { '@type': 'ImageObject', url: SITE.logo, width: 512, height: 512 },
    image: SITE.image,
    description: SITE.description,
    foundingDate: SITE.foundingDate,
    founder: SITE.founders.map(f => ({ '@type': 'Person', name: f.name, jobTitle: f.jobTitle })),
    sameAs: SITE.sameAs,
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
      url: `${SITE.url}/contact`,
      availableLanguage: ['English']
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

export { services, faq };
