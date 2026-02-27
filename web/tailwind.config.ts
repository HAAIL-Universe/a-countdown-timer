import type { Config } from 'tailwindcss'

export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        'retro-green': '#22C55E',
        'retro-blue': '#3B82F6',
        'retro-yellow': '#FBBF24',
        'retro-red': '#EF4444',
        'retro-bg': '#1F2937',
      },
      fontFamily: {
        mono: ['JetBrains Mono', 'Courier New', 'monospace'],
      },
      animation: {
        'urgency-flash': 'urgency-flash 0.5s ease-in-out infinite alternate',
      },
      keyframes: {
        'urgency-flash': {
          '0%': { opacity: '1' },
          '100%': { opacity: '0.4' },
        },
      },
    },
  },
  plugins: [],
} satisfies Config
