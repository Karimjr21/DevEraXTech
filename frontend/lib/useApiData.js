import { useCallback, useEffect, useState } from 'react';

// Loads data from an API call and tracks loading / error / ready states.
// `retry` re-runs the request (used by error-state buttons).
export default function useApiData(fetcher) {
  const [state, setState] = useState({ status: 'loading', data: [] });
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    let cancelled = false;
    setState(prev => ({ ...prev, status: 'loading' }));
    fetcher()
      .then(data => { if (!cancelled) setState({ status: 'ready', data }); })
      .catch(() => { if (!cancelled) setState({ status: 'error', data: [] }); });
    return () => { cancelled = true; };
  }, [fetcher, attempt]);

  const retry = useCallback(() => setAttempt(n => n + 1), []);
  return { ...state, retry };
}
