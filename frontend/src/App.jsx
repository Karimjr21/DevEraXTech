import { BrowserRouter } from 'react-router-dom';
import { LazyMotion } from 'framer-motion';
import RoutesIndex from '../routes';
import Navbar from '../components/ui/Navbar';
import Footer from '../components/ui/Footer';
import SeoManager from '../components/SeoManager';
import ScrollManager from '../components/ScrollManager';
import RevealManager from '../components/fx/RevealManager';
import { AmbientBackground, CardSpotlight, ScrollProgress } from '../components/fx/Ambience';
import { PrerenderDataContext } from '../lib/prerenderData';
import '../styles/global.css';

// Framer Motion's animation code loads in its own chunk after first paint; components use `m`.
const loadMotionFeatures = () => import('./motionFeatures.js').then(mod => mod.default);

// Layout shared by the browser app and the build-time prerender (entry-server.jsx).
export function AppShell() {
  return (
    <LazyMotion features={loadMotionFeatures}>
      <div className="min-h-screen flex flex-col bg-dark">
        <SeoManager />
        <ScrollManager />
        <RevealManager />
        <CardSpotlight />
        <AmbientBackground />
        <ScrollProgress />
        <Navbar />
        <main className="flex-1 relative">
          <RoutesIndex />
        </main>
        <Footer />
      </div>
    </LazyMotion>
  );
}

export default function App({ prerenderData = null }) {
  return (
    <PrerenderDataContext.Provider value={prerenderData}>
      <BrowserRouter>
        <AppShell />
      </BrowserRouter>
    </PrerenderDataContext.Provider>
  );
}
