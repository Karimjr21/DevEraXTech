// Scroll reveals must never hide what the visitor is already looking at on the page they
// landed on: the prerendered content is visible before JavaScript runs, and hiding it again
// to fade it back in causes a flash and delays Largest Contentful Paint.
// After the first in-app navigation, new pages animate in as usual.
let navigated = false;

export function markNavigated() {
  navigated = true;
}

// True for an element on the landing page that is currently inside the viewport.
export function isVisibleOnLanding(el) {
  if (navigated) return false;
  const rect = el.getBoundingClientRect();
  return rect.top < window.innerHeight && rect.bottom > 0;
}
