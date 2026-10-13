// Theme state lives on <html data-theme="light"> (dark = attribute absent).
// The inline script in index.html applies a stored choice before first paint;
// this module handles toggling, persistence and meta updates. SSR-safe: no
// DOM access at module level.
export const THEME_KEY = 'dx-theme';
export const THEME_META = { dark: '#0a0a0a', light: '#faf7f0' };

export function getTheme() {
  if (typeof document === 'undefined') return 'dark';
  return document.documentElement.getAttribute('data-theme') === 'light' ? 'light' : 'dark';
}

export function applyTheme(theme) {
  if (typeof document === 'undefined') return;
  const next = theme === 'light' ? 'light' : 'dark';
  const root = document.documentElement;
  // Suppress color transitions for the frames of the switch (see global.css).
  root.classList.add('theme-switching');
  if (next === 'light') root.setAttribute('data-theme', 'light');
  else root.removeAttribute('data-theme');
  root.style.colorScheme = next;
  const tc = document.querySelector('meta[name="theme-color"]');
  if (tc) tc.setAttribute('content', THEME_META[next]);
  const cs = document.querySelector('meta[name="color-scheme"]');
  if (cs) cs.setAttribute('content', next);
  requestAnimationFrame(() => requestAnimationFrame(() => root.classList.remove('theme-switching')));
  window.dispatchEvent(new CustomEvent('dx-themechange', { detail: next }));
}

export function setTheme(theme) {
  applyTheme(theme);
  try {
    localStorage.setItem(THEME_KEY, theme === 'light' ? 'light' : 'dark');
  } catch {
    /* storage unavailable: the choice still applies for this session */
  }
}
