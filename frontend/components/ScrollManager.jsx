import { useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import { markNavigated } from '../lib/firstView';

// On navigation: scroll to the #hash target if there is one, otherwise to the top.
export default function ScrollManager() {
  const { pathname, hash } = useLocation();
  const landing = useRef(true);

  useEffect(() => {
    if (landing.current) landing.current = false;
    else markNavigated();

    if (hash) {
      let tries = 0;
      const find = () => {
        const el = document.getElementById(decodeURIComponent(hash.slice(1)));
        if (el) {
          el.scrollIntoView({ block: 'start' });
          // Re-align once the page transition has finished moving the content.
          setTimeout(() => el.scrollIntoView({ block: 'start' }), 650);
        }
        else if (tries++ < 20) setTimeout(find, 50); // content may still be loading
      };
      find();
      return;
    }
    window.scrollTo(0, 0);
  }, [pathname, hash]);

  return null;
}
