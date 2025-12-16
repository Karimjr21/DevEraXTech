import React from 'react';

// Abstract data-flow ribbons using SVG; subtle motion via CSS keyframes.
// Layering: this component renders behind hero content (z-0) and is non-interactive.
export default function Logo3D() {
  return (
    <div className="fixed inset-0 pointer-events-none z-0">
      <svg
        className="w-full h-full"
        viewBox="0 0 1600 900"
        preserveAspectRatio="xMidYMid slice"
        aria-hidden="true"
      >
        {/* Background tint to ensure richness without overpowering */}
        <rect x="0" y="0" width="1600" height="900" fill="transparent" />

        {/* Ribbons: gold and derived shades; low opacity for subtlety */}
        <path
          d="M -100 200 C 200 150, 400 250, 700 220 C 950 200, 1200 260, 1700 220"
          fill="none"
          stroke="#d4af37"
          strokeWidth="2"
          opacity="0.18"
          className="animate-ribbon-1"
        />
        <path
          d="M -100 500 C 250 520, 450 460, 780 480 C 1020 500, 1280 540, 1700 520"
          fill="none"
          stroke="#c79a2f"
          strokeWidth="2"
          opacity="0.12"
          className="animate-ribbon-2"
        />
        <path
          d="M -100 350 C 220 330, 420 380, 760 360 C 1000 340, 1300 400, 1700 360"
          fill="none"
          stroke="#a8842a"
          strokeWidth="1.8"
          opacity="0.1"
          className="animate-ribbon-3"
        />
        <path
          d="M -100 650 C 260 630, 520 690, 860 660 C 1120 640, 1380 700, 1700 660"
          fill="none"
          stroke="#d4af37"
          strokeWidth="1.6"
          opacity="0.14"
          className="animate-ribbon-4"
        />
      </svg>

      {/* Inline styles for animation; respects reduced motion */}
      <style>{`
        @keyframes driftA { 0% { transform: translateX(0px); } 50% { transform: translateX(18px); } 100% { transform: translateX(0px); } }
        @keyframes driftB { 0% { transform: translateX(0px); } 50% { transform: translateX(-14px); } 100% { transform: translateX(0px); } }
        @keyframes driftC { 0% { transform: translateX(0px); } 50% { transform: translateX(10px); } 100% { transform: translateX(0px); } }
        @keyframes driftD { 0% { transform: translateX(0px); } 50% { transform: translateX(-8px); } 100% { transform: translateX(0px); } }

        .animate-ribbon-1 { animation: driftA 24s ease-in-out infinite; }
        .animate-ribbon-2 { animation: driftB 28s ease-in-out infinite; }
        .animate-ribbon-3 { animation: driftC 30s ease-in-out infinite; }
        .animate-ribbon-4 { animation: driftD 26s ease-in-out infinite; }

        @media (prefers-reduced-motion: reduce) {
          .animate-ribbon-1, .animate-ribbon-2, .animate-ribbon-3, .animate-ribbon-4 { animation: none; }
        }
      `}</style>
    </div>
  );
}
