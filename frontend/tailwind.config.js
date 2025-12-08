/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    './index.html',
    './src/**/*.{js,jsx,ts,tsx}',
    './components/**/*.{js,jsx,ts,tsx}',
    './pages/**/*.{js,jsx,ts,tsx}'
  ],
  theme: {
    extend: {
      colors: {
        dark: '#0a0a0a',
        gold: '#d4af37'
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif']
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
