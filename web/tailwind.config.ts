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
        dark: '#0F1419',
        neon: {
          green: '#00FF00',
          cyan: '#00FFFF',
          magenta: '#FF00FF',
          yellow: '#FFFF00',
        },
      },
      fontFamily: {
        mono: ['JetBrains Mono', 'Courier New', 'monospace'],
        retro: ['Press Start 2P', 'Courier New', 'monospace'],
      },
      fontSize: {
        timer: ['4rem', { lineHeight: '1' }],
        'timer-sm': ['2rem', { lineHeight: '1' }],
        label: ['0.875rem', { lineHeight: '1.25rem' }],
      },
      spacing: {
        full: '100%',
      },
      animation: {
        pulse: 'pulse 1s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'flash-red': 'flashRed 0.3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'pulse-slow': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        flashRed: {
          '0%, 100%': { backgroundColor: '#EF4444', opacity: '1' },
          '50%': { backgroundColor: '#7C2D12', opacity: '0.8' },
        },
      },
      backgroundImage: {
        'urgency-idle': 'linear-gradient(135deg, #1F2937 0%, #0F1419 100%)',
        'urgency-running': 'linear-gradient(135deg, #1E40AF 0%, #1F2937 100%)',
        'urgency-urgent': 'linear-gradient(135deg, #B45309 0%, #1F2937 100%)',
        'urgency-critical': 'linear-gradient(135deg, #7C2D12 0%, #1F2937 100%)',
      },
      minHeight: {
        screen: '100vh',
      },
      width: {
        face: '300px',
        'face-lg': '400px',
        'face-sm': '200px',
      },
      height: {
        face: '300px',
        'face-lg': '400px',
        'face-sm': '200px',
      },
    },
  },
  plugins: [],
};

export default config;
