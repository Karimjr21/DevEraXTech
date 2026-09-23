import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

// On navigation: scroll to the #hash target if there is one, otherwise to the top.
export default function ScrollManager() {
  const { pathname, hash } = useLocation();

  useEffect(() => {
    if (hash) {
      let tries = 0;
      const find = () => {
        const el = document.getElementById(decodeURIComponent(hash.slice(1)));
        if (el) el.scrollIntoView({ block: 'start' });
        else if (tries++ < 20) setTimeout(find, 50); // content may still be loading
      };
      find();
      return;
    }
    window.scrollTo(0, 0);
  }, [pathname, hash]);

  return null;
}
