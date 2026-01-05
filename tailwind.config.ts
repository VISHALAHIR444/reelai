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
          black: '#000000',
          void: '#0a0a0a',
          coal: '#1a1a1a',
          slate: '#2a2a2a',
          iron: '#3a3a3a',
          steel: '#4a4a4a',
          fog: '#888888',
          mist: '#aaaaaa',
          cloud: '#cccccc',
          chalk: '#eeeeee',
          paper: '#ffffff',
          neon: {
            cyan: '#00ffff',
            magenta: '#ff00ff',
            green: '#00ff00',
            blue: '#0080ff',
            pink: '#ff0080',
            yellow: '#ffff00',
          },
          accent: '#00ffff',
          accentDim: '#00cccc',
          gold: '#ffff00',
          ember: '#ff0040',
          velvet: '#1a0033',
          midnight: '#000011',
        },
        background: '#0a0a0e',
        foreground: '#f1f1f8',
        border: 'rgba(255,255,255,0.08)',
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
        'studio-sm': '0 1px 3px rgba(0,0,0,0.5), 0 1px 2px rgba(0,0,0,0.4)',
        'studio-md': '0 4px 16px rgba(0,0,0,0.6), 0 2px 8px rgba(0,0,0,0.4)',
        'studio-lg': '0 10px 40px rgba(0,0,0,0.7), 0 4px 20px rgba(0,0,0,0.5)',
        'studio-xl': '0 20px 80px rgba(0,0,0,0.8), 0 8px 32px rgba(0,0,0,0.6)',
        'studio-glow': '0 0 20px rgba(0,255,255,0.3), inset 0 1px 0 rgba(255,255,255,0.1)',
        'studio-glow-cyan': '0 0 20px rgba(0,255,255,0.4), 0 0 40px rgba(0,255,255,0.2)',
        'studio-glow-magenta': '0 0 20px rgba(255,0,255,0.4), 0 0 40px rgba(255,0,255,0.2)',
        'studio-glow-green': '0 0 20px rgba(0,255,0,0.4), 0 0 40px rgba(0,255,0,0.2)',
        'studio-glow-gold': '0 0 16px rgba(255,255,0,0.3)',
        'studio-depth': 'inset 0 1px 0 rgba(255,255,255,0.1), 0 1px 3px rgba(0,0,0,0.6)',
        'studio-float': '0 8px 32px rgba(0,0,0,0.5), 0 4px 16px rgba(0,0,0,0.3)',
        'neon-border': '0 0 10px rgba(0,255,255,0.5)',
      },
      animation: {
        'drift': 'drift 30s ease-in-out infinite',
        'drift-slow': 'drift 60s ease-in-out infinite',
        'fade-in': 'fadeIn 0.8s cubic-bezier(0.22, 1, 0.36, 1)',
        'slide-up': 'slideUp 0.7s cubic-bezier(0.22, 1, 0.36, 1)',
        'scale-in': 'scaleIn 0.6s cubic-bezier(0.34, 1.56, 0.64, 1)',
        'glow-pulse': 'glowPulse 3s ease-in-out infinite',
        'float': 'float 6s ease-in-out infinite',
      },
      keyframes: {
        drift: {
          '0%, 100%': { transform: 'translateY(0px) translateX(0px) rotate(0deg)' },
          '25%': { transform: 'translateY(-8px) translateX(4px) rotate(0.5deg)' },
          '50%': { transform: 'translateY(-16px) translateX(-2px) rotate(-0.3deg)' },
          '75%': { transform: 'translateY(-4px) translateX(-4px) rotate(0.2deg)' },
        },
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(8px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideUp: {
          '0%': { transform: 'translateY(24px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        scaleIn: {
          '0%': { transform: 'scale(0.95)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
        glowPulse: {
          '0%, 100%': { boxShadow: '0 0 20px rgba(99,102,241,0.15)' },
          '50%': { boxShadow: '0 0 32px rgba(99,102,241,0.25)' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-6px)' },
        },
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};
export default config;
