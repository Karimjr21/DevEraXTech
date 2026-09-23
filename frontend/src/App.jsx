import { BrowserRouter } from 'react-router-dom';
import RoutesIndex from '../routes';
import Navbar from '../components/ui/Navbar';
import Footer from '../components/ui/Footer';
import SeoManager from '../components/SeoManager';
import ScrollManager from '../components/ScrollManager';
import { PrerenderDataContext } from '../lib/prerenderData';
import '../styles/global.css';

// Layout shared by the browser app and the build-time prerender (entry-server.jsx).
export function AppShell() {
  return (
    <div className="min-h-screen flex flex-col bg-dark">
      <SeoManager />
      <ScrollManager />
      <Navbar />
      <main className="flex-1">
        <RoutesIndex />
      </main>
      <Footer />
    </div>
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
