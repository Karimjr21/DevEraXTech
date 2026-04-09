export default function Footer() {
  return (
    <footer className="footer-shell relative z-10">
      <div className="mx-auto max-w-7xl px-6 sm:px-8 lg:px-10 pt-8 md:pt-10 pb-8 md:pb-10">
        <div className="mb-6 md:mb-7 flex items-center justify-center lg:justify-start gap-3 text-[0.62rem] uppercase tracking-[0.26em] text-gray-400/65">
          <span className="h-px w-10 bg-gradient-to-r from-gold/60 via-gold/20 to-transparent" aria-hidden />
          <span>Premium execution, quietly delivered</span>
        </div>

        <div className="grid gap-6 md:gap-8 lg:grid-cols-[1.05fr,1fr,auto] lg:items-end text-center lg:text-left">
          <div className="space-y-2.5">
            <div className="flex items-center justify-center lg:justify-start gap-3">
              <div className="font-semibold tracking-wide gold-gradient-text text-base sm:text-lg">DevEraXTech</div>
              <span className="hidden sm:inline-flex h-1.5 w-1.5 rounded-full bg-gold/60" aria-hidden />
            </div>
            <p className="mx-auto lg:mx-0 max-w-sm text-[0.82rem] sm:text-sm leading-5 text-gray-400/75">
              Premium web & app experiences for teams that want secure, scalable delivery with a refined finish.
            </p>
          </div>

          <div className="space-y-2.5 lg:justify-self-center">
            <div className="text-[0.64rem] uppercase tracking-[0.22em] text-gray-500">Connect</div>
            <div className="flex items-center justify-center lg:justify-start gap-3.5">
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

              <div className="text-[0.82rem] sm:text-sm leading-5 text-gray-400/75">
                Secure • Scalable • Pixel-perfect
              </div>
            </div>
          </div>

          <div className="text-[0.8rem] sm:text-sm leading-5 text-gray-500 lg:justify-self-end lg:text-right">
            © {new Date().getFullYear()} DevEraXTech. All rights reserved.
          </div>
        </div>
      </div>
    </footer>
  );
}
