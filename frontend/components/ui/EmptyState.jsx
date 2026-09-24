import AnimatedButton from './AnimatedButton';

const ICONS = {
  empty: (
    <path d="M4 7.5 12 3l8 4.5v9L12 21l-8-4.5v-9Zm0 0 8 4.5m0 0 8-4.5M12 12v9" />
  ),
  error: (
    <path d="M12 8v5m0 3.5h.01M10.3 3.9 2.6 17.2A2 2 0 0 0 4.3 20h15.4a2 2 0 0 0 1.7-2.8L13.7 3.9a2 2 0 0 0-3.4 0Z" />
  ),
  search: (
    <path d="m20 20-4.3-4.3M17 10.5a6.5 6.5 0 1 1-13 0 6.5 6.5 0 0 1 13 0Z" />
  ),
  lost: (
    <path d="M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Zm3.5-12.5-2 5-5 2 2-5 5-2Z" />
  )
};

// Card shown when a section has nothing to display: no data yet, a failed request,
// a filter with no matches, or an unknown page.
export default function EmptyState({
  icon = 'empty',
  kicker,
  title,
  text,
  actionLabel,
  actionTo,
  onAction,
  secondaryLabel,
  secondaryTo,
  role,
  headingLevel = 3,
  className = ''
}) {
  const Heading = `h${headingLevel}`;
  return (
    <div className={`portfolio-empty-card empty-state p-8 sm:p-10 text-center ${className}`} role={role}>
      <div className="empty-state-icon" aria-hidden>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
          {ICONS[icon] || ICONS.empty}
        </svg>
      </div>
      {kicker && <p className="text-[11px] tracking-[0.2em] uppercase text-gold/70 mb-2">{kicker}</p>}
      <Heading className="text-xl text-gold font-semibold mb-2">{title}</Heading>
      {text && <p className="text-sm text-gray-400 max-w-md mx-auto leading-relaxed">{text}</p>}
      {(actionLabel || secondaryLabel) && (
        <div className="mt-6 flex flex-wrap items-center justify-center gap-3">
          {actionLabel && (
            <AnimatedButton to={actionTo} onClick={onAction} className="min-w-[10rem]">
              {actionLabel}
            </AnimatedButton>
          )}
          {secondaryLabel && (
            <AnimatedButton to={secondaryTo} variant="outline" className="min-w-[10rem]">
              {secondaryLabel}
            </AnimatedButton>
          )}
        </div>
      )}
    </div>
  );
}

// Placeholder blocks shown while data is loading.
export function LoadingCards({ count = 3, label = 'Loading', className = '' }) {
  return (
    <div className={className} role="status" aria-live="polite">
      <span className="sr-only">{label}…</span>
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="portfolio-empty-card skeleton-card" aria-hidden>
          <div className="skeleton-line skeleton-line--short" />
          <div className="skeleton-line skeleton-line--title" />
          <div className="skeleton-line" />
          <div className="skeleton-line skeleton-line--mid" />
        </div>
      ))}
    </div>
  );
}
