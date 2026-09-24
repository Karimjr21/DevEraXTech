import { useEffect, useState } from 'react';

// False during the prerender and the first (hydrating) browser render, true right after.
// Use it for values that depend on the visitor (current time, URL), so the first browser
// render matches the prerendered HTML exactly.
export default function useHydrated() {
  const [hydrated, setHydrated] = useState(false);
  useEffect(() => setHydrated(true), []);
  return hydrated;
}
