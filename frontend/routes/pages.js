import { createElement, lazy, useState } from 'react';

// Each page is its own chunk, so a visitor downloads only the page they open.
// The prerendered HTML modulepreloads the landing page's chunk (scripts/prerender.mjs), and
// main.jsx waits for it before hydrating, so hydration never suspends. The other pages are
// fetched in the background once the browser is idle (preloadAllPages).
const loaders = {
  '/': () => import('../pages/Home.jsx'),
  '/services': () => import('../pages/Services.jsx'),
  '/portfolio': () => import('../pages/Portfolio.jsx'),
  '/about': () => import('../pages/About.jsx'),
  '/contact': () => import('../pages/Contact.jsx'),
  '*': () => import('../pages/NotFound.jsx')
};

function lazyPage(load) {
  let loaded = null;
  const loadAndKeep = () => load().then(mod => { loaded = mod.default; return mod; });
  const Lazy = lazy(loadAndKeep);
  function Page(props) {
    // Chosen once per mount: switching from Lazy to the loaded component later would remount the page.
    const [Component] = useState(() => loaded || Lazy);
    return createElement(Component, props);
  }
  Page.preload = loadAndKeep;
  return Page;
}

export const pages = Object.fromEntries(Object.entries(loaders).map(([path, load]) => [path, lazyPage(load)]));

export function preloadPage(pathname) {
  const clean = pathname !== '/' ? pathname.replace(/\/+$/, '') : '/';
  return (pages[clean] || pages['*']).preload();
}

export function preloadAllPages() {
  Object.values(pages).forEach(page => page.preload().catch(() => {}));
}
