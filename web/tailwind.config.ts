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
          dark: '#1a1a2e',
          darkBg: '#0f0f1e',
          accent: '#00d9ff',
          warning: '#ffcd00',
          danger: '#ff006e',
          success: '#00ff88',
          muted: '#666b7f',
          light: '#e8eef7',
        },
      },
      backgroundColor: {
        'retro-base': '#1a1a2e',
        'retro-dark': '#0f0f1e',
      },
      textColor: {
        'retro-accent': '#00d9ff',
        'retro-warning': '#ffcd00',
        'retro-danger': '#ff006e',
        'retro-success': '#00ff88',
        'retro-muted': '#666b7f',
        'retro-light': '#e8eef7',
      },
      borderColor: {
        'retro-accent': '#00d9ff',
        'retro-warning': '#ffcd00',
        'retro-danger': '#ff006e',
      },
      animation: {
        pulse: 'pulse 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        flash: 'flash 0.3s ease-in-out infinite',
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
        display: ['4rem', { lineHeight: '1' }],
        lg: ['1.5rem', { lineHeight: '1.5' }],
      },
    },
  },
  plugins: [],
};

export default config;
