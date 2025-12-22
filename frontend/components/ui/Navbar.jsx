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
  const isContact = location.pathname === '/contact';
  const isHome = location.pathname === '/';
  const hideCTA = isContact || isHome;
  return (
    <header className="sticky top-0 z-50 glass">
      <nav className="max-w-6xl mx-auto px-3 sm:px-4 py-2 sm:py-3 flex items-center justify-between">
        <div className="flex items-center gap-3 min-w-0">
          <NavLink
            to="/"
            onClick={() => { if (typeof window !== 'undefined' && window.__setNavOpen) window.__setNavOpen(false); }}
            className="flex items-center gap-2 min-w-0"
            aria-label="DevEraXTech Home"
          >
            <img
              src="/assests/DevEraXTech%20Logo.png"
              alt="DevEraXTech Logo"
              className="h-6 sm:h-7 w-auto object-contain select-none"
              draggable={false}
            />
            <span className="min-w-0 max-w-[42vw] sm:max-w-none truncate text-lg sm:text-xl md:text-2xl leading-none font-bold gold-gradient-text tracking-wide">
              DevEraXTech
            </span>
          </NavLink>
        </div>
        {/* Desktop nav */}
        <ul className="hidden md:flex gap-8 text-sm font-medium">
          {navItems.map(item => (
            <li key={item.to}>
              <NavLink
                to={item.to}
                className={({ isActive }) => `pb-1 transition-colors relative ${isActive ? 'text-gold' : 'text-gray-300'} hover:text-gold`}
              >
                {item.label}
                <span className="absolute left-0 -bottom-[2px] h-[2px] w-full bg-gold scale-x-0 group-hover:scale-x-100 transition-transform origin-left" />
              </NavLink>
            </li>
          ))}
        </ul>
        {/* Mobile controls */}
        <div className="md:hidden flex items-center gap-2 flex-shrink-0">
          {!hideCTA ? (
            <AnimatedButton to="/contact">
              <span className="hidden sm:inline">Request a Meeting</span>
              <span className="sm:hidden">Meeting</span>
            </AnimatedButton>
          ) : (
            <div className="w-0 h-10" aria-hidden />
          )}
          <MobileMenu />
        </div>
        {/* Desktop CTA */}
        <div className="hidden md:block">
          {!hideCTA ? (
            <AnimatedButton className="ml-4" to="/contact">Request a Meeting</AnimatedButton>
          ) : (
            <div className="ml-4 w-[160px] h-11 inline-block" aria-hidden />
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
      className="p-2 rounded-md border border-white/10 bg-black/30 text-gray-200 focus:outline-none focus:ring-2 focus:ring-gold"
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
    <div className={`${open ? 'block' : 'hidden'} md:hidden border-t border-white/10 bg-black/70 backdrop-blur`}> 
      <div className="max-w-6xl mx-auto px-4 py-3">
        <ul className="flex flex-col gap-3 text-base">
          {navItems.map(item => (
            <li key={item.to}>
              <NavLink
                to={item.to}
                onClick={close}
                className={({ isActive }) => `block py-2 px-1 rounded ${isActive ? 'text-gold' : 'text-gray-300'} hover:text-gold`}
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
