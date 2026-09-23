import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { SITE, buildJsonLd, canonicalUrl, getRouteMeta } from '../src/seo';

function setMeta(attr, key, content) {
  let el = document.head.querySelector(`meta[${attr}="${key}"]`);
  if (!el) {
    el = document.createElement('meta');
    el.setAttribute(attr, key);
    document.head.appendChild(el);
  }
  el.setAttribute('content', content);
}

// Keeps <head> tags in sync with the current route during client-side navigation.
// The initial values are written into each prerendered HTML file at build time.
export default function SeoManager() {
  const { pathname } = useLocation();

  useEffect(() => {
    const route = getRouteMeta(pathname);
    const url = route.noindex ? `${SITE.url}${pathname}` : canonicalUrl(route.path);

    document.title = route.title;
    setMeta('name', 'description', route.description);
    setMeta('name', 'robots', route.noindex ? 'noindex, follow' : 'index, follow, max-image-preview:large');
    setMeta('property', 'og:title', route.title);
    setMeta('property', 'og:description', route.description);
    setMeta('property', 'og:url', url);
    setMeta('name', 'twitter:title', route.title);
    setMeta('name', 'twitter:description', route.description);

    let canonical = document.head.querySelector('link[rel="canonical"]');
    if (!canonical) {
      canonical = document.createElement('link');
      canonical.rel = 'canonical';
      document.head.appendChild(canonical);
    }
    canonical.href = url;

    const ld = document.getElementById('ld-json');
    if (ld) ld.textContent = JSON.stringify(buildJsonLd(route));
  }, [pathname]);

  return null;
}
