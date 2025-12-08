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
      fontFamily: {
        display: ['Clash Display', 'sans-serif'],
        body: ['General Sans', 'sans-serif'],
        sans: ['General Sans', 'sans-serif'],
      },
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
        "organic": "14px",
        "organic-sm": "11px",
        "organic-lg": "18px",
      },
      spacing: {
        "xs": "var(--spacing-xs, 0.3rem)",
        "sm": "var(--spacing-sm, 0.65rem)",
        "md": "var(--spacing-md, 1.15rem)",
        "lg": "var(--spacing-lg, 1.8rem)",
        "xl": "var(--spacing-xl, 2.8rem)",
        "2xl": "var(--spacing-2xl, 4.2rem)",
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
        "fade-in": {
          from: { opacity: "0" },
          to: { opacity: "1" },
        },
        "slide-down": {
          from: { transform: "translateY(-10px)", opacity: "0" },
          to: { transform: "translateY(0)", opacity: "1" },
        },
        "hover-tilt": {
          "0%": { transform: "perspective(1000px) rotateX(0deg) rotateY(0deg)" },
          "100%": { transform: "perspective(1000px) rotateX(-2deg) rotateY(-2deg)" },
        },
        "press-shrink": {
          "0%, 100%": { transform: "scale(1)" },
          "50%": { transform: "scale(0.98)" },
        },
        "soft-bounce": {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-3px)" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
        "fade-in": "fade-in 0.3s ease-out",
        "slide-down": "slide-down 0.3s ease-out",
        "hover-tilt": "hover-tilt 0.6s cubic-bezier(0.22, 1, 0.36, 1)",
        "press-shrink": "press-shrink 0.4s cubic-bezier(0.22, 1, 0.36, 1)",
        "soft-bounce": "soft-bounce 0.6s ease-out",
      },
      backgroundImage: {
        "gradient-premium": "linear-gradient(135deg, #f6f6f6 0%, #e6e6e6 100%)",
        "gradient-dark": "linear-gradient(135deg, #111111 0%, #0a0a0a 100%)",
        "gradient-accent": "linear-gradient(135deg, #1a1a1a, #0d0d0d)",
      },
      boxShadow: {
        "soft": "0 2px 8px rgba(0, 0, 0, 0.08)",
        "soft-hover": "0 6px 16px rgba(0, 0, 0, 0.12)",
        "organic": "0 1px 3px rgba(0, 0, 0, 0.06), 0 4px 12px rgba(0, 0, 0, 0.08)",
        "organic-hover": "0 4px 8px rgba(0, 0, 0, 0.08), 0 12px 24px rgba(0, 0, 0, 0.12)",
      },
      backdropBlur: {
        "subtle": "2px",
        "sm": "4px",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};

export default config;
