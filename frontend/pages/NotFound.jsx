import { useLocation } from 'react-router-dom';
import SectionWrapper from '../components/ui/SectionWrapper';
import EmptyState from '../components/ui/EmptyState';

export default function NotFound() {
  const { pathname } = useLocation();

  return (
    <div className="max-w-3xl mx-auto px-6 sm:px-8 pt-20 md:pt-28 pb-24 md:pb-28">
      <SectionWrapper>
        <EmptyState
          icon="lost"
          headingLevel={1}
          kicker="404"
          title="This page doesn't exist"
          text={`We couldn't find “${pathname}”. It may have moved, or the link may be mistyped.`}
          actionLabel="Back to Home"
          actionTo="/"
          secondaryLabel="Contact Us"
          secondaryTo="/contact"
        />
      </SectionWrapper>
    </div>
  );
}
