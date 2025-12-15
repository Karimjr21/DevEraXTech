export default function Footer() {
  return (
    <footer className="border-t border-gray-800 mt-12">
      <div className="max-w-7xl mx-auto px-8 py-10 text-sm flex flex-col md:flex-row md:items-center md:justify-between gap-6">
        <div className="flex items-center gap-4">
          <div className="font-semibold tracking-wide gold-gradient-text text-lg">DevEraXTech</div>
          <a
            href="https://www.instagram.com/deveraxtech?igsh=MWR5aTY2N3g1eWVjNQ=="
            target="_blank"
            rel="noreferrer"
            aria-label="DevEraXTech on Instagram"
            className="inline-flex items-center justify-center w-7 h-7 rounded-full border border-gold/40 text-gold hover:bg-gold hover:text-dark transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4">
              <path d="M7 2h10a5 5 0 015 5v10a5 5 0 01-5 5H7a5 5 0 01-5-5V7a5 5 0 015-5zm0 2a3 3 0 00-3 3v10a3 3 0 003 3h10a3 3 0 003-3V7a3 3 0 00-3-3H7zm5 3a5 5 0 110 10 5 5 0 010-10zm0 2a3 3 0 100 6 3 3 0 000-6zm5.5-2a1.5 1.5 0 110 3 1.5 1.5 0 010-3z" />
            </svg>
          </a>
        </div>
        <div className="flex-1 text-gray-400 leading-relaxed">
          Premium web & app experiences • Secure • Scalable • Pixel-perfect
        </div>
        <div className="text-gray-500">© {new Date().getFullYear()} DevEraXTech. All rights reserved.</div>
      </div>
    </footer>
  );
}
