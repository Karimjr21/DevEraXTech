import { renderToString } from 'react-dom/server';
import { StaticRouter } from 'react-router';
import { AppShell } from './App.jsx';
import { PrerenderDataContext } from '../lib/prerenderData';

// Used only at build time by scripts/prerender.mjs to produce static HTML per route.
export function render(url, prerenderData) {
  return renderToString(
    <PrerenderDataContext.Provider value={prerenderData}>
      <StaticRouter location={url}>
        <AppShell />
      </StaticRouter>
    </PrerenderDataContext.Provider>
  );
}

export { ROUTES, NOT_FOUND, SITE, buildJsonLd, canonicalUrl, services, faq, business } from './seo.js';
