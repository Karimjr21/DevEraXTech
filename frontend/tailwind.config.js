/** @type {import('tailwindcss').Config} */
// Theme-aware color channels (declared in styles/global.css). Dark channel
// values equal Tailwind's default literals, so dark output is unchanged.
const v = (n) => `rgb(var(--${n}) / <alpha-value>)`;
// Text and rings get an alpha lift that is 0 in dark (identical output) and
// raises faint alpha-modified text to AA contrast in light.
const t = (n) =>
  `rgb(var(--${n}) / calc(<alpha-value> + (1 - <alpha-value>) * var(--text-alpha-lift, 0)))`;
const STEPS = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950];
const grayScale = (fn) => Object.fromEntries(STEPS.map((s) => [s, fn(`gray-${s}`)]));

export default {
  darkMode: 'class',
  content: [
    './index.html',
    './src/**/*.{js,jsx,ts,tsx}',
    './components/**/*.{js,jsx,ts,tsx}',
    './pages/**/*.{js,jsx,ts,tsx}',
    './lib/**/*.{js,jsx,ts,tsx}'
  ],
  theme: {
    extend: {
      colors: {
        dark: '#0a0a0a',
        gold: '#d4af37',
        page: v('color-bg-rgb'),
        white: v('tw-white'),
        black: v('tw-black'),
        gray: grayScale(v),
        red: { 300: v('red-300'), 400: v('red-400'), 500: v('red-500') },
        green: { 300: v('green-300'), 400: v('green-400'), 500: v('green-500') }
      },
      textColor: {
        white: t('tw-white'),
        gray: grayScale(t),
        gold: t('gold-text-rgb'),
        red: { 300: t('red-300'), 400: t('red-400') },
        green: { 300: t('green-300'), 400: t('green-400') }
      },
      borderColor: {
        DEFAULT: v('border-default'),
        gold: v('gold-line-rgb')
      },
      ringColor: {
        gold: t('gold-ring-rgb')
      },
      fontFamily: {
        sans: ['"Inter Variable"', 'Inter', 'system-ui', 'sans-serif'],
        display: ['"Playfair Display Variable"', '"Playfair Display"', 'Georgia', 'serif']
      },
      boxShadow: {
        glow: '0 0 8px rgba(212,175,55,0.6), 0 0 24px rgba(212,175,55,0.4)'
      },
      backgroundImage: {
        'gold-gradient': 'linear-gradient(135deg,#d4af37 0%,#f5d573 50%,#d4af37 100%)'
      }
    }
  },
  plugins: []
};
