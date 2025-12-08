import { Suspense } from 'react';
import SectionWrapper from '../components/ui/SectionWrapper';
import AnimatedButton from '../components/ui/AnimatedButton';
import Logo3D from '../components/3d/Logo3D';
import ErrorBoundary from '../components/ui/ErrorBoundary';

export default function Home() {
  return (
    <div className="space-y-24">
      <div className="min-h-screen w-full relative flex items-center justify-center">
        <ErrorBoundary fallback={<div className='text-gold text-center'>3D disabled — showing static hero.<br/>Check browser console for errors.</div>}>
          <Suspense fallback={<div className='text-gold'>Loading 3D...</div>}>
            <Logo3D />
          </Suspense>
        </ErrorBoundary>
        <div className="absolute bottom-12 left-0 right-0 mx-auto max-w-5xl px-8 z-10">
          <h1 className="text-5xl md:text-7xl font-bold mb-6 gold-gradient-text leading-tight">We build premium web & app experiences</h1>
          <p className="text-lg text-gray-300 max-w-2xl mb-8">Modern, secure and scalable solutions — from prototypes to production.</p>
          <div className="flex gap-6">
            <AnimatedButton to="/contact">Get a Quote</AnimatedButton>
            <AnimatedButton variant="outline" to="/services">View Our Services</AnimatedButton>
          </div>
        </div>
      </div>
      <SectionWrapper id="trust" className="max-w-6xl mx-auto px-8 py-24">
        <p className="text-gray-400">Trusted by startups & enterprises • 50+ projects shipped</p>
      </SectionWrapper>
    </div>
  );
}
