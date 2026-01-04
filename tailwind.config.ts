import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
    "./app/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        studio: {
          black: '#09090b',
          coal: '#0f0f12',
          slate: '#151519',
          iron: '#1a1a1f',
          steel: '#24242a',
          fog: '#71717a',
          mist: '#a1a1aa',
          cloud: '#d4d4d8',
          chalk: '#e4e4e7',
          paper: '#f4f4f5',
          accent: '#8b7aff',
          accentDim: '#6b5bd4',
          gold: '#d4a574',
          ember: '#ff6b6b',
        },
        background: '#09090b',
        foreground: '#f4f4f5',
        border: 'rgba(255,255,255,0.06)',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['Inter', 'system-ui', 'sans-serif'],
      },
      fontSize: {
        'display-xl': ['5rem', { lineHeight: '1', letterSpacing: '-0.02em', fontWeight: '600' }],
        'display-lg': ['3.5rem', { lineHeight: '1.1', letterSpacing: '-0.02em', fontWeight: '600' }],
        'display-md': ['2.5rem', { lineHeight: '1.2', letterSpacing: '-0.01em', fontWeight: '600' }],
        'display-sm': ['1.875rem', { lineHeight: '1.3', letterSpacing: '-0.01em', fontWeight: '600' }],
      },
      boxShadow: {
        'studio-sm': '0 2px 8px rgba(0,0,0,0.4)',
        'studio-md': '0 8px 24px rgba(0,0,0,0.5)',
        'studio-lg': '0 16px 48px rgba(0,0,0,0.6)',
        'studio-glow': '0 0 32px rgba(139,122,255,0.2)',
        'studio-glow-gold': '0 0 24px rgba(212,165,116,0.15)',
      },
      animation: {
        'drift': 'drift 20s ease-in-out infinite',
        'fade-in': 'fadeIn 0.6s ease-out',
        'slide-up': 'slideUp 0.5s ease-out',
      },
      keyframes: {
        drift: {
          '0%, 100%': { transform: 'translateY(0px) rotate(0deg)' },
          '50%': { transform: 'translateY(-20px) rotate(2deg)' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};
export default config;
