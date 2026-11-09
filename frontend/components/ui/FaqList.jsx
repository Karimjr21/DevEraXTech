// Visible FAQ block. The same items feed the page's FAQPage JSON-LD (src/seo.js), so
// what crawlers read in structured data always matches what visitors see.
export default function FaqList({ items, className = '' }) {
  return (
    <div className={`space-y-3 md:space-y-4 ${className}`}>
      {items.map(item => (
        <details key={item.question} className="faq-item service-editorial-row rounded-2xl">
          <summary className="faq-question">
            <span>{item.question}</span>
            <span className="faq-marker" aria-hidden>+</span>
          </summary>
          <p className="faq-answer">{item.answer}</p>
        </details>
      ))}
    </div>
  );
}
