import { NavLink } from 'react-router-dom';
import AnimatedButton from './AnimatedButton';

const navItems = [
  { to: '/', label: 'Home' },
  { to: '/services', label: 'Services' },
  { to: '/portfolio', label: 'Work' },
  { to: '/about', label: 'About' },
  { to: '/contact', label: 'Contact' }
];

export default function Navbar() {
  return (
    <header className="sticky top-0 z-50 glass">
      <nav className="max-w-7xl mx-auto flex items-center justify-between px-8 py-4">
        <div className="flex items-center gap-4">
          <div className="text-2xl font-bold gold-gradient-text tracking-wide">DevEraX</div>
        </div>
        <ul className="flex gap-4 md:gap-8 text-sm font-medium overflow-x-auto no-scrollbar max-w-full">
          {navItems.map(item => (
            <li key={item.to} className="shrink-0">
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
        <AnimatedButton to="/contact">Get a Quote</AnimatedButton>
      </nav>
    </header>
  );
}
