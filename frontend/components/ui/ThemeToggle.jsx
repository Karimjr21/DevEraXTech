import React, { useEffect, useState } from 'react';
import { THEME_KEY, applyTheme, getTheme, setTheme } from '../../lib/theme';

function Sun({ fixed = false }) {
  return (
    <svg className={fixed ? 'absolute' : 'theme-toggle__icon theme-toggle__sun absolute'} width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="12" cy="12" r="4" />
      <path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41" />
    </svg>
  );
}

function Moon() {
  return (
    <svg className="theme-toggle__icon theme-toggle__moon absolute" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z" />
    </svg>
  );
}

export default function ThemeToggle({ variant = 'icon', className = '' }) {
  const [theme, setLocal] = useState(getTheme);

  useEffect(() => {
    // Sync with the real attribute (the inline script may have set it) and keep
    // every instance and tab in step.
    setLocal(getTheme());
    const onChange = (e) => setLocal(e.detail === 'light' ? 'light' : 'dark');
    const onStorage = (e) => {
      if (e.key === THEME_KEY && (e.newValue === 'light' || e.newValue === 'dark')) applyTheme(e.newValue);
    };
    window.addEventListener('dx-themechange', onChange);
    window.addEventListener('storage', onStorage);
    return () => {
      window.removeEventListener('dx-themechange', onChange);
      window.removeEventListener('storage', onStorage);
    };
  }, []);

  const isLight = theme === 'light';
  const toggle = () => setTheme(isLight ? 'dark' : 'light');

  if (variant === 'row') {
    return (
      <button
        type="button"
        aria-pressed={isLight}
        onClick={toggle}
        className={`flex w-full items-center justify-between py-2 px-1 rounded text-base text-gray-300 hover:text-gold transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-gold/60 ${className}`}
      >
        <span className="inline-flex items-center gap-3">
          <span className="relative inline-flex h-5 w-5 items-center justify-center" aria-hidden="true">
            <Sun fixed />
          </span>
          <span>Light theme</span>
        </span>
        <span aria-hidden="true" data-on={isLight ? 'true' : 'false'} className="theme-switch border border-gold/30">
          <span className={`theme-switch__knob ${isLight ? 'bg-gold' : 'bg-gray-500'}`} />
        </span>
      </button>
    );
  }

  return (
    <button
      type="button"
      aria-label="Light theme"
      aria-pressed={isLight}
      title={isLight ? 'Switch to dark theme' : 'Switch to light theme'}
      onClick={toggle}
      className={`theme-toggle relative inline-flex h-10 w-10 items-center justify-center rounded-full border border-white/10 bg-black/25 text-gray-200 hover:text-gold hover:border-gold/30 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-gold/60 ${className}`}
    >
      <Sun />
      <Moon />
    </button>
  );
}
