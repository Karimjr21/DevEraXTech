import SectionWrapper from '../components/ui/SectionWrapper';

const timeline = [
  { year: '2024', text: 'Founded with mission to craft premium digital experiences.' },
  { year: '2025', text: 'Scaled delivery process & shipped 10+ projects.' }
];

const team = [
  { name: 'Karim', role: 'Founder & Full Stack Developer' },
  { name: 'Loay', role: 'Co-Founder & Full Stack Developer' },
  { name: 'Amr', role: 'Founder & Full Stack Developer' }
];

export default function About() {
  return (
    <div className="max-w-7xl mx-auto px-8 py-24 space-y-24">
      <SectionWrapper id="mission">
        <h2 className="text-4xl font-bold mb-6 gold-gradient-text">About Us</h2>
        <p className="text-gray-300 max-w-3xl">We deliver future-grade software emphasizing performance, design fidelity and security.</p>
      </SectionWrapper>
      <SectionWrapper id="timeline" className="space-y-8">
        <h3 className="text-2xl font-semibold text-gold">Timeline</h3>
        <div className="grid md:grid-cols-2 gap-8">
          {timeline.map(t => (
            <div key={t.year} className="glass rounded-lg p-5">
              <div className="text-gold font-semibold mb-2">{t.year}</div>
              <p className="text-xs text-gray-400">{t.text}</p>
            </div>
          ))}
        </div>
      </SectionWrapper>
      <SectionWrapper id="team" className="space-y-8">
        <h3 className="text-2xl font-semibold text-gold">Team</h3>
        <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-8">
          {team.map(m => (
            <div key={m.name} className="glass rounded-xl p-6 transition-transform hover:-translate-y-2">
              <div className="text-lg font-semibold text-gold">{m.name}</div>
              <div className="text-xs text-gray-400">{m.role}</div>
            </div>
          ))}
        </div>
      </SectionWrapper>
    </div>
  );
}
