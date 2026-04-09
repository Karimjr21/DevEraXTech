export default function Footer() {
  return (
    <footer className="footer-shell relative z-10">
      <div className="mx-auto max-w-7xl px-6 sm:px-8 lg:px-10 pt-6 md:pt-7 pb-6 md:pb-7">
        <div className="grid gap-4 md:gap-5 lg:grid-cols-[auto,1fr,auto] lg:items-center text-center lg:text-left">
          <div className="flex items-center justify-center lg:justify-start gap-3">
            <div className="font-semibold tracking-wide gold-gradient-text text-base sm:text-lg md:text-xl">
              DevEraXTech
            </div>
            <span className="hidden sm:inline-flex h-1.5 w-1.5 rounded-full bg-gold/60" aria-hidden />
          </div>

          <div className="flex items-center justify-center gap-3 text-[0.78rem] sm:text-sm tracking-[0.16em] uppercase text-gray-400/75">
            <span>Secure</span>
            <span className="text-gold/40" aria-hidden>•</span>
            <span>Scalable</span>
            <span className="text-gold/40" aria-hidden>•</span>
            <span>Pixel-perfect</span>
          </div>

          <div className="flex items-center justify-center lg:justify-end gap-4 sm:gap-5 text-[0.8rem] sm:text-sm leading-5 text-gray-500">
            <a
              href="https://www.instagram.com/deveraxtech?igsh=MWR5aTY2N3g1eWVjNQ=="
              target="_blank"
              rel="noreferrer"
              aria-label="DevEraXTech on Instagram"
              className="group inline-flex h-10 w-10 items-center justify-center rounded-full border border-gold/20 bg-white/5 text-gold/85 transition-all duration-300 hover:border-gold/45 hover:bg-gold/10 hover:text-gold focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gold/50"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="h-4 w-4 transition-transform duration-300 group-hover:scale-105">
                <path d="M7 2h10a5 5 0 015 5v10a5 5 0 01-5 5H7a5 5 0 01-5-5V7a5 5 0 015-5zm0 2a3 3 0 00-3 3v10a3 3 0 003 3h10a3 3 0 003-3V7a3 3 0 00-3-3H7zm5 3a5 5 0 110 10 5 5 0 010-10zm0 2a3 3 0 100 6 3 3 0 000-6zm5.5-2a1.5 1.5 0 110 3 1.5 1.5 0 010-3z" />
              </svg>
            </a>

            <div className="hidden sm:block h-5 w-px bg-white/10" aria-hidden />

            <div className="text-gray-500">
              © {new Date().getFullYear()} DevEraXTech. All rights reserved.
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
