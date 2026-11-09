// Project screenshots in /public/work ship at 1904px wide plus 640/960/1440px copies
// (`<name>-<width>.webp`) so phones and small frames download a fitting size.
const WORK_WIDTHS = [640, 960, 1440];

export function workSrcSet(src, fullWidth = 1904) {
  if (!src || !/^\/work\/[^/]+\.webp$/.test(src)) return undefined;
  const base = src.replace(/\.webp$/, '');
  return [...WORK_WIDTHS.map(w => `${base}-${w}.webp ${w}w`), `${src} ${fullWidth}w`].join(', ');
}

// Showcase frame: ~680px wide inside the 6xl featured card on desktop, near full width on phones.
export const SHOWCASE_SIZES = '(min-width: 1024px) 680px, calc(100vw - 48px)';
// Card grids: 3 columns at xl, 2 at md, 1 on phones.
export const CARD_SIZES = '(min-width: 1280px) 400px, (min-width: 768px) 50vw, 100vw';
// Two-column cards on service pages (max container 1400px).
export const HALF_SIZES = '(min-width: 1400px) 660px, (min-width: 768px) 50vw, 100vw';
