import React, { useState, useEffect } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import AnimatedButton from './AnimatedButton';

const navItems = [
  { to: '/', label: 'Home' },
  { to: '/services', label: 'Services' },
  { to: '/portfolio', label: 'Work' },
  { to: '/about', label: 'About' },
  { to: '/contact', label: 'Contact' }
];

export default function Navbar() {
  const location = useLocation();
  const [isScrolled, setIsScrolled] = useState(false);
  const isContact = location.pathname === '/contact';
  const isHome = location.pathname === '/';
  const hideCTA = isContact;

  useEffect(() => {
    const onScroll = () => setIsScrolled(window.scrollY > 10);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  return (
    <header className={`sticky top-0 z-50 navbar-shell ${isHome ? 'navbar-shell--home' : ''} ${isScrolled ? 'navbar-shell--scrolled' : 'navbar-shell--top'}`}>
      <nav className={`relative z-[2] max-w-6xl mx-auto px-3 sm:px-4 ${isScrolled ? 'py-2' : 'py-2.5 sm:py-3'} grid grid-cols-[auto,1fr,auto] items-center gap-2.5 sm:gap-5 transition-[padding] duration-300`}>
        <div className="flex items-center gap-3 min-w-0">
          <NavLink
            to="/"
            onClick={() => { if (typeof window !== 'undefined' && window.__setNavOpen) window.__setNavOpen(false); }}
            className="flex items-center gap-2 min-w-0 navbar-brand"
            aria-label="DevEraXTech Home"
          >
            <img
              src="/assests/DevEraXTech%20Logo.png"
              alt="DevEraXTech Logo"
              className="h-6 sm:h-7 w-auto object-contain select-none"
              draggable={false}
            />
            <span className="min-w-0 max-w-[40vw] max-[380px]:max-w-[30vw] sm:max-w-none truncate text-lg max-[380px]:text-base sm:text-xl md:text-2xl leading-none font-bold gold-gradient-text tracking-wide">
              DevEraXTech
            </span>
          </NavLink>
        </div>
        {/* Desktop nav */}
        <ul className="hidden md:flex justify-self-center gap-7 lg:gap-8 text-[0.95rem] font-medium">
          {navItems.map(item => (
            <li key={item.to}>
              <NavLink
                to={item.to}
                className={({ isActive }) => `nav-link pb-1 transition-colors relative ${isActive ? 'is-active text-gold' : 'text-gray-300'} hover:text-gold focus-visible:text-gold`}
              >
                {item.label}
                <span className="nav-link-line" />
              </NavLink>
            </li>
          ))}
        </ul>
        {/* Mobile controls */}
        <div className="md:hidden flex items-center gap-2 justify-self-end flex-shrink-0">
          {!hideCTA ? (
            <AnimatedButton className="navbar-mobile-cta h-10 px-4 text-[0.92rem] max-[380px]:h-9 max-[380px]:px-3 max-[380px]:text-[0.82rem]" to="/contact">
              Book a Meeting
            </AnimatedButton>
          ) : (
            <div className="w-0 h-9" aria-hidden />
          )}
          <MobileMenu />
        </div>
        {/* Desktop CTA */}
        <div className="hidden md:block justify-self-end">
          {!hideCTA ? (
            <AnimatedButton className="navbar-cta h-10 px-5 text-sm md:text-[0.92rem]" to="/contact">Book a Meeting </AnimatedButton>
          ) : (
            <div className="w-[128px] h-10 inline-block" aria-hidden />
          )}
        </div>
      </nav>
      {/* Mobile menu panel renders below header */}
      <MobileMenuPanel />
    </header>
  );
}

function MobileMenu() {
  const [open, setOpen] = useState(false);
  useEffect(() => {
    if (typeof window !== 'undefined') {
      if (!window.__setNavOpen) {
        window.__navOpen = false;
        window.__listeners = [];
        window.__setNavOpen = (val) => {
          window.__navOpen = val;
          window.__listeners.forEach(fn => fn(val));
        };
      }
      setOpen(window.__navOpen);
    }
  }, []);
  return (
    <button
      aria-label={open ? 'Close menu' : 'Open menu'}
      aria-expanded={open}
      onClick={() => {
        const next = !open;
        setOpen(next);
        if (typeof window !== 'undefined' && window.__setNavOpen) {
          window.__setNavOpen(next);
        }
      }}
      className="p-2 rounded-md border border-white/12 bg-black/24 text-gray-200 hover:text-gold hover:border-gold/30 transition-colors focus:outline-none focus:ring-2 focus:ring-gold/60"
    >
      <span className="sr-only">Menu</span>
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-6 h-6">
        <path d="M3.75 6.75h16.5M3.75 12h16.5M3.75 17.25h16.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      </svg>
    </button>
  );
}

function MobileMenuPanel() {
  const [open, setOpen] = useState(false);
  // Use a shared state via window for simplicity without context
  // Toggle will set window.__navOpen; panel reads and syncs on mount
  if (typeof window !== 'undefined') {
    // monkey-patch set function once
    if (!window.__setNavOpen) {
      window.__navOpen = false;
      window.__listeners = [];
      window.__setNavOpen = (val) => {
        window.__navOpen = val;
        window.__listeners.forEach(fn => fn(val));
      };
    }
    // subscribe
    useEffect(() => {
      const fn = (val) => setOpen(val);
      window.__listeners.push(fn);
      setOpen(window.__navOpen);
      return () => {
        window.__listeners = window.__listeners.filter(f => f !== fn);
      };
    }, []);
  }

  const close = () => typeof window !== 'undefined' && window.__setNavOpen(false);

  return (
      <div className={`${open ? 'block' : 'hidden'} relative z-[3] md:hidden border-t border-white/10 bg-black/68 backdrop-blur-xl`}> 
      <div className="max-w-6xl mx-auto px-4 py-3">
        <ul className="flex flex-col gap-3 text-base">
          {navItems.map(item => (
            <li key={item.to}>
              <NavLink
                to={item.to}
                onClick={close}
                className={({ isActive }) => `block py-2 px-1 rounded transition-colors ${isActive ? 'text-gold' : 'text-gray-300'} hover:text-gold`}
              >
                {item.label}
              </NavLink>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
