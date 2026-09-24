import { Writable } from 'node:stream';
import { renderToPipeableStream } from 'react-dom/server';
import { StaticRouter } from 'react-router';
import { AppShell } from './App.jsx';
import { PrerenderDataContext } from '../lib/prerenderData';

// Used only at build time by scripts/prerender.mjs to produce static HTML per route.
// Waits for every lazy-loaded page (onAllReady), so the HTML always holds the full content.
export function render(url, prerenderData) {
  return new Promise((resolve, reject) => {
    let html = '';
    const sink = new Writable({
      write(chunk, _encoding, callback) { html += chunk; callback(); },
      final(callback) { resolve(html); callback(); }
    });
    const { pipe } = renderToPipeableStream(
      <PrerenderDataContext.Provider value={prerenderData}>
        <StaticRouter location={url}>
          <AppShell />
        </StaticRouter>
      </PrerenderDataContext.Provider>,
      { onAllReady() { pipe(sink); }, onShellError: reject, onError: reject }
    );
  });
}

export { ROUTES, NOT_FOUND, SITE, buildJsonLd, canonicalUrl, services, faq, homeFaq, business } from './seo.js';
