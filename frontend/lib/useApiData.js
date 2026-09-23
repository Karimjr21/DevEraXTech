import { useCallback, useEffect, useState } from 'react';
import { usePrerenderData } from './prerenderData';

// Loads data from an API call and tracks loading / error / ready states.
// When the page was prerendered with data for `key`, that data is shown immediately
// and the API refreshes it in the background. `retry` re-runs the request.
export default function useApiData(fetcher, key) {
  const initial = usePrerenderData(key);
  const hasInitial = initial !== undefined;
  const [state, setState] = useState(() =>
    hasInitial ? { status: 'ready', data: initial } : { status: 'loading', data: [] }
  );
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    let cancelled = false;
    if (!hasInitial || attempt > 0) setState(prev => ({ ...prev, status: 'loading' }));
    fetcher()
      .then(data => { if (!cancelled) setState({ status: 'ready', data }); })
      .catch(() => {
        if (cancelled) return;
        // Keep showing prerendered data if a background refresh fails.
        setState(prev => (hasInitial && attempt === 0 ? prev : { status: 'error', data: [] }));
      });
    return () => { cancelled = true; };
  }, [fetcher, attempt, hasInitial]);

  const retry = useCallback(() => setAttempt(n => n + 1), []);
  return { ...state, retry };
}
