import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        retro: {
          dark: '#1a1a1a',
          bg: '#0f0f0f',
          accent: '#00ff41',
          accentDim: '#00aa2c',
          neutral: '#cccccc',
          warning: '#ffdd00',
          danger: '#ff0000',
          dangerDim: '#aa0000',
        },
      },
      animation: {
        flash: 'flash 0.5s ease-in-out infinite',
      },
      keyframes: {
        flash: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.4' },
        },
      },
      fontFamily: {
        mono: ['Courier New', 'monospace'],
      },
      fontSize: {
        'display': ['4rem', { lineHeight: '1.2' }],
        'subheading': ['1.5rem', { lineHeight: '1.4' }],
      },
    },
  },
  plugins: [],
};

export default config;
