// Single source of truth for page titles, descriptions and structured data.
// Used by the build-time prerender (scripts/prerender.mjs) and by SeoManager at runtime.
import services from './data/services.json';
import faq from './data/faq.json';
import business from './data/business.json';
import portfolio from './data/portfolio.json';
import maintenance from './data/maintenance.json';

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
      'Cairo studio building secure, pixel-perfect websites, online stores, web and mobile apps, AI integrations and care plans for Egypt, the Gulf, US and Canada.',
    priority: '1.0'
  },
  {
    path: '/services',
    file: 'services.html',
    name: 'Services',
    title: 'Web, App & Software Development Services | DevEraXTech',
    description:
      'Websites, online stores, web and mobile apps, desktop software, AI and payment integrations, SEO, redesigns, UI/UX design and care plans from a Cairo studio.',
    priority: '0.9'
  },
  {
    path: '/maintenance',
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
    file: 'portfolio.html',
    name: 'Work',
    title: 'Web Design Portfolio | DevEraXTech, Cairo',
    description:
      'Web design portfolio of DevEraXTech, a Cairo studio: MERN stack web apps like the Nilora Estates real estate platform, business websites, e-commerce and landing pages.',
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

function serviceNode(s) {
  return {
    '@type': 'Service',
    '@id': `${SITE.url}/services#${s.id}`,
    name: s.title,
    serviceType: s.title,
    ...(s.group ? { category: s.group } : {}),
    description: s.summary,
    provider: { '@id': ORG_ID },
    url: s.link ? `${SITE.url}${s.link}` : `${SITE.url}/contact?service=${encodeURIComponent(s.title)}`
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
      page.mainEntity = { '@id': `${SITE.url}/services#${svc.id}` };
    }
    graph.push(faqPage(url, maintenance.faq));
  }
  if (route.path === '/portfolio' && portfolio.length) {
    graph.push(portfolioList());
    page.mainEntity = { '@id': `${SITE.url}/portfolio#list` };
  }
  return { '@context': 'https://schema.org', '@graph': graph };
}

export { services, faq, business, portfolio };
