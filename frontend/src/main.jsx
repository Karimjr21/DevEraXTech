import React from 'react';
import { createRoot, hydrateRoot } from 'react-dom/client';
import '@fontsource-variable/inter';
import '@fontsource-variable/playfair-display';
import App from './App.jsx';
import { readEmbeddedPrerenderData } from '../lib/prerenderData';
import { preloadAllPages, preloadPage } from '../routes/pages';

const container = document.getElementById('root');
const app = <App prerenderData={readEmbeddedPrerenderData()} />;

// Production pages arrive prerendered (scripts/prerender.mjs): hydrate that markup in place
// instead of rebuilding it, once the landing page's code is loaded so nothing suspends.
// The dev server serves an empty shell, so render from scratch there.
if (container.firstElementChild) {
  preloadPage(window.location.pathname)
    .catch(() => {})
    .then(() => hydrateRoot(container, app));
} else {
  createRoot(container).render(app);
}

// Fetch the other pages' code in the background so navigation stays instant.
const idle = window.requestIdleCallback || (cb => setTimeout(cb, 1500));
window.addEventListener('load', () => idle(preloadAllPages), { once: true });
