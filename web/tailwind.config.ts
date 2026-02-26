import type { Config } from 'tailwindcss';

export default {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        retro: {
          dark: '#0f0f1e',
          darkGray: '#1a1a2e',
          purple: '#6b46c1',
          pink: '#ec4899',
          yellow: '#fbbf24',
          orange: '#f97316',
          red: '#ef4444',
          green: '#22c55e',
          cyan: '#06b6d4',
          white: '#f5f5f5',
        },
      },
      backgroundColor: {
        urgency: {
          calm: '#0f0f1e',
          warning: '#92400e',
          critical: '#7f1d1d',
        },
      },
      borderColor: {
        urgency: {
          calm: '#6b46c1',
          warning: '#fbbf24',
          critical: '#ef4444',
        },
      },
      textColor: {
        urgency: {
          calm: '#f5f5f5',
          warning: '#fbbf24',
          critical: '#ef4444',
        },
      },
      animation: {
        flash: 'flash 0.6s ease-in-out',
        pulse: 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        flash: {
          '0%': { opacity: '1' },
          '50%': { opacity: '0.4' },
          '100%': { opacity: '1' },
        },
        pulse: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '.5' },
        },
      },
      fontFamily: {
        mono: ['Courier New', 'monospace'],
        display: ['Arial', 'sans-serif'],
      },
      fontSize: {
        timer: ['4rem', { lineHeight: '1' }],
        urgency: ['1.25rem', { lineHeight: '1.5' }],
      },
    },
  },
  plugins: [],
} satisfies Config;
