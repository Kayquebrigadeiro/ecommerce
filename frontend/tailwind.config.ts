import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        background: '#05070D',
        surface: '#0D111C',
        primary: '#FF2E2E',
        secondary: '#00D4FF',
        'text-main': '#E6EDF3',
        'text-secondary': '#8B949E',
        'surface-light': '#161B26',
        'surface-lighter': '#1F2937',
      },
      spacing: {
        '4': '0.25rem',
        '8': '0.5rem',
        '12': '0.75rem',
        '16': '1rem',
        '24': '1.5rem',
        '32': '2rem',
        '48': '3rem',
        '64': '4rem',
      },
      borderRadius: {
        'sm': '0.25rem',
        'md': '0.5rem',
        'lg': '0.75rem',
        'xl': '1rem',
        '2xl': '1.5rem',
      },
      boxShadow: {
        'glow-soft': '0 0 20px rgba(255, 46, 46, 0.15)',
        'glow-neon': '0 0 30px rgba(0, 212, 255, 0.3)',
        'glow-primary': '0 0 40px rgba(255, 46, 46, 0.4)',
        'glow-secondary': '0 0 40px rgba(0, 212, 255, 0.4)',
      },
      transitionDuration: {
        'fast': '120ms',
        'normal': '240ms',
        'cinematic': '500ms',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        glow: {
          '0%': { boxShadow: '0 0 20px rgba(255, 46, 46, 0.2)' },
          '100%': { boxShadow: '0 0 40px rgba(255, 46, 46, 0.6)' },
        },
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-energy': 'linear-gradient(135deg, #FF2E2E 0%, #00D4FF 100%)',
        'gradient-dark': 'linear-gradient(180deg, #05070D 0%, #0D111C 100%)',
      },
    },
  },
  plugins: [],
}
export default config
