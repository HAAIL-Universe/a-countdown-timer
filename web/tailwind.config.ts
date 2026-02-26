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
        bg: '#1F2937',
      },
      fontFamily: {
        mono: ['JetBrains Mono', 'Courier New', 'monospace'],
      },
      fontSize: {
        timer: '4rem',
      },
      animation: {
        flash: 'flash 0.5s infinite',
      },
      keyframes: {
        flash: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.3' },
        },
      },
      spacing: {
        128: '32rem',
      },
    },
  },
  plugins: [],
};

export default config;
