import { BrowserRouter } from 'react-router-dom';
import RoutesIndex from '../routes';
import Navbar from '../components/ui/Navbar';
import Footer from '../components/ui/Footer';
import '../styles/global.css';

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col bg-dark">
        <Navbar />
        <main className="flex-1">
          <RoutesIndex />
        </main>
        <Footer />
      </div>
    </BrowserRouter>
  );
}
