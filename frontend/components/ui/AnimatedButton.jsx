import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

export default function AnimatedButton({ children, to, onClick, variant = 'gold', disabled = false, loading = false }) {
  // Responsive sizing: clamp font/padding/height for small screens; preserve desktop via md overrides.
  const base = 'relative inline-flex items-center justify-center rounded-md font-semibold tracking-wide overflow-hidden whitespace-nowrap text-[clamp(0.85rem,2.8vw,1rem)] md:text-base px-[clamp(0.9rem,3.5vw,1.25rem)] md:px-6 py-[clamp(0.5rem,2.5vw,0.75rem)] md:py-3 h-[clamp(2.25rem,6.5vw,2.75rem)] md:h-auto';
  const styles = variant === 'gold'
    ? 'text-dark bg-gold shadow-glow'
    : 'text-gold border border-gold';
  const content = (
    <span className="flex items-center gap-2">
      {loading && <span className="h-4 w-4 border-2 border-dark border-t-transparent rounded-full animate-spin" />}
      <span>{children}</span>
    </span>
  );
  const cls = `${base} ${styles} ${disabled ? 'opacity-60 cursor-not-allowed' : ''}`;
  return (
    <motion.div whileHover={!disabled && { scale: 1.05 }} whileTap={!disabled && { scale: 0.97 }}>
      {to ? (
        <Link to={to} className={cls} onClick={onClick} aria-disabled={disabled}>
          {content}
        </Link>
      ) : (
        <button className={cls} onClick={onClick} disabled={disabled}>
          {content}
        </button>
      )}
    </motion.div>
  );
}
