import { useEffect, useState } from 'react';
import SectionWrapper from '../components/ui/SectionWrapper';
import { fetchPortfolio } from '../lib/api';
import Lightbox from '../components/ui/Lightbox';

export default function Portfolio() {
  const [items, setItems] = useState([]);
  const [filter, setFilter] = useState('All');
  const [active, setActive] = useState(null);
  useEffect(() => { fetchPortfolio().then(setItems); }, []);
  const categories = ['All', ...Array.from(new Set(items.map(i => i.category)))];
  const shown = filter === 'All' ? items : items.filter(i => i.category === filter);

  return (
    <div className="max-w-7xl mx-auto px-8 py-24">
      <h2 className="text-4xl font-bold mb-8 gold-gradient-text">Portfolio</h2>
      <div className="flex flex-wrap gap-3 mb-12">
        {categories.map(cat => (
          <button
            key={cat}
            onClick={() => setFilter(cat)}
            className={`px-4 py-2 rounded-md text-xs font-semibold tracking-wide transition-all ${filter===cat? 'bg-gold text-dark shadow-glow':'glass text-gray-300 hover:text-gold'}`}
          >{cat}</button>
        ))}
      </div>
      <div className="columns-1 sm:columns-2 md:columns-3 gap-6 space-y-6">
        {shown.map(item => (
          <SectionWrapper key={item.id} className="break-inside-avoid glass rounded-lg overflow-hidden p-0 group cursor-pointer" onClick={()=>setActive(item)}>
            <div className="overflow-hidden">
              <img src={item.image} alt={item.title} className="rounded-t w-full h-auto group-hover:scale-[1.03] transition-transform" />
            </div>
            <div className="p-4">
              <h3 className="text-lg font-semibold text-gold mb-1">{item.title}</h3>
              <p className="text-xs text-gray-400">{item.category}</p>
            </div>
          </SectionWrapper>
        ))}
      </div>
      {active && <Lightbox item={active} onClose={()=>setActive(null)} />}
    </div>
  );
}
