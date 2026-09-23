import { createContext, useContext } from 'react';

// Data embedded into prerendered pages at build time (see scripts/prerender.mjs),
// so crawlers and first paint get real content before the API responds.
export const PrerenderDataContext = createContext(null);

export function usePrerenderData(key) {
  const data = useContext(PrerenderDataContext);
  return data && Object.prototype.hasOwnProperty.call(data, key) ? data[key] : undefined;
}

export function readEmbeddedPrerenderData() {
  if (typeof document === 'undefined') return null;
  const el = document.getElementById('__PRERENDER_DATA__');
  if (!el) return null;
  try {
    return JSON.parse(el.textContent);
  } catch {
    return null;
  }
}
