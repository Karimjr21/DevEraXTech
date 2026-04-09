import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

export default function AnimatedButton({
  children,
  to,
  onClick,
  variant = 'gold',
  disabled = false,
  loading = false,
  className = ''
}) {
  // Responsive sizing: clamp font/padding/height for small screens; preserve desktop via md overrides.
  const base = 'btn-premium relative inline-flex items-center justify-center rounded-md font-semibold tracking-wide overflow-hidden whitespace-nowrap text-[clamp(0.85rem,2.8vw,1rem)] md:text-base px-[clamp(0.9rem,3.5vw,1.25rem)] md:px-6 py-[clamp(0.5rem,2.5vw,0.75rem)] md:py-3 h-[clamp(2.25rem,6.5vw,2.75rem)] md:h-auto transition-all duration-300';
  const styles = variant === 'gold'
    ? 'btn-premium--primary text-dark bg-gold shadow-glow'
    : 'btn-premium--outline text-gold border border-gold/70';
  const content = (
    <span className="relative z-[2] flex items-center gap-2">
      {loading && <span className="h-4 w-4 border-2 border-dark border-t-transparent rounded-full animate-spin" />}
      <span>{children}</span>
    </span>
  );
  const cls = `${base} ${styles} ${disabled ? 'opacity-60 cursor-not-allowed' : ''} ${className}`.trim();

  const shimmer = variant === 'gold' ? <span className="btn-shimmer" aria-hidden /> : null;

  return (
    <motion.div whileHover={!disabled && { y: -2, scale: 1.01 }} whileTap={!disabled && { y: 0, scale: 0.99 }}>
      {to ? (
        <Link to={to} className={cls} onClick={onClick} aria-disabled={disabled}>
          {shimmer}
          {content}
        </Link>
      ) : (
        <button className={cls} onClick={onClick} disabled={disabled}>
          {shimmer}
          {content}
        </button>
      )}
    </motion.div>
  );
}
