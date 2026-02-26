import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        idle: '#22C55E',
        running: '#3B82F6',
        urgent: '#FBBF24',
        critical: '#EF4444',
        background: '#1F2937',
        accent: '#60A5FA',
      },
      backgroundColor: {
        dark: '#1F2937',
        'dark-lighter': '#374151',
      },
      textColor: {
        idle: '#22C55E',
        running: '#3B82F6',
        urgent: '#FBBF24',
        critical: '#EF4444',
      },
      fontSize: {
        timer: '4rem',
        'timer-sm': '2.5rem',
        label: '1rem',
      },
      fontFamily: {
        mono: ['Courier New', 'JetBrains Mono', 'monospace'],
      },
      animation: {
        flash: 'flash 0.5s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        pulse: 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        flash: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.3' },
        },
        pulse: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.7' },
        },
      },
      spacing: {
        face: '20rem',
        'face-sm': '12rem',
      },
      borderRadius: {
        pixel: '0.25rem',
      },
    },
  },
  plugins: [],
};

export default config;
