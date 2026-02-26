import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import CharacterFace from './CharacterFace';
import type { TimerStatus } from '../types/timer';

describe('CharacterFace', () => {
  const renderCharacterFace = (urgencyLevel: number, status: TimerStatus = 'idle') => {
    return render(<CharacterFace urgencyLevel={urgencyLevel} status={status} />);
  };

  describe('happy expression', () => {
    it('renders happy face when urgencyLevel is 0', () => {
      renderCharacterFace(0, 'idle');
      const svg = screen.getByRole('img', { hidden: true });
      expect(svg).toBeInTheDocument();

      const paths = svg.querySelectorAll('path[d^="M 100 180"]');
      expect(paths.length).toBeGreaterThan(0);
    });

    it('renders happy face when paused with urgencyLevel 0', () => {
      renderCharacterFace(0, 'paused');
      const svg = screen.getByRole('img', { hidden: true });
      expect(svg).toBeInTheDocument();

      const paths = svg.querySelectorAll('path[d^="M 100 180"]');
      expect(paths.length).toBeGreaterThan(0);
    });

    it('renders happy face when running with urgencyLevel 1', () => {
      renderCharacterFace(1, 'running');
      const svg = screen.getByRole('img', { hidden: true });
      const paths = svg.querySelectorAll('path[d^="M 100 180"]');
      expect(paths.length).toBeGreaterThan(0);
    });
  });

  describe('anxious expression', () => {
    it('renders anxious face when urgencyLevel is 2', () => {
      renderCharacterFace(2, 'running');
      const svg = screen.getByRole('img', { hidden: true });
      expect(svg).toBeInTheDocument();

      const anxiousLines = svg.querySelectorAll('line[x1="85"][y1="90"]');
      expect(anxiousLines.length).toBeGreaterThan(0);

      const anxiousMouth = svg.querySelector('path[d^="M 100 190"]');
      expect(anxiousMouth).toBeInTheDocument();
    });

    it('renders anxious face when paused with urgencyLevel 2', () => {
      renderCharacterFace(2, 'paused');
      const svg = screen.getByRole('img', { hidden: true });
      const anxiousLines = svg.querySelectorAll('line[x1="85"][y1="90"]');
      expect(anxiousLines.length).toBeGreaterThan(0);
    });
  });

  describe('upset expression', () => {
    it('renders upset face when urgencyLevel is 3', () => {
      renderCharacterFace(3, 'running');
      const svg = screen.getByRole('img', { hidden: true });
      expect(svg).toBeInTheDocument();

      const upsetLines = svg.querySelectorAll('line[x1="85"][y1="95"]');
      expect(upsetLines.length).toBeGreaterThan(0);

      const upsetMouth = svg.querySelector('path[d^="M 100 170"]');
      expect(upsetMouth).toBeInTheDocument();
    });

    it('renders upset face when urgencyLevel exceeds 3', () => {
      renderCharacterFace(4, 'running');
      const svg = screen.getByRole('img', { hidden: true });
      const upsetLines = svg.querySelectorAll('line[x1="85"][y1="95"]');
      expect(upsetLines.length).toBeGreaterThan(0);
    });

    it('renders upset face when paused with urgencyLevel 3', () => {
      renderCharacterFace(3, 'paused');
      const svg = screen.getByRole('img', { hidden: true });
      const upsetLines = svg.querySelectorAll('line[x1="85"][y1="95"]');
      expect(upsetLines.length).toBeGreaterThan(0);
    });
  });

  describe('background colors', () => {
    it('applies green background when urgencyLevel is 0 and idle', () => {
      const { container } = renderCharacterFace(0, 'idle');
      const div = container.querySelector('div.bg-green-500');
      expect(div).toBeInTheDocument();
    });

    it('applies blue background when running with urgencyLevel 1', () => {
      const { container } = renderCharacterFace(1, 'running');
      const div = container.querySelector('div.bg-blue-500');
      expect(div).toBeInTheDocument();
    });

    it('applies yellow background when urgencyLevel is 2', () => {
      const { container } = renderCharacterFace(2, 'running');
      const div = container.querySelector('div.bg-yellow-400');
      expect(div).toBeInTheDocument();
    });

    it('applies red background when urgencyLevel is 3', () => {
      const { container } = renderCharacterFace(3, 'running');
      const div = container.querySelector('div.bg-red-500');
      expect(div).toBeInTheDocument();
    });
  });

  describe('animations', () => {
    it('applies flash animation when urgencyLevel is 3 and running', () => {
      const { container } = renderCharacterFace(3, 'running');
      const div = container.querySelector('div');
      expect(div).toHaveClass('animate-pulse');
      expect(div?.style.animation).toBe('flash 0.5s infinite');
    });

    it('does not apply flash animation when urgencyLevel is 2', () => {
      const { container } = renderCharacterFace(2, 'running');
      const div = container.querySelector('div');
      expect(div).not.toHaveClass('animate-pulse');
      expect(div?.style.animation).toBeFalsy();
    });

    it('does not apply flash animation when urgencyLevel is 3 but paused', () => {
      const { container } = renderCharacterFace(3, 'paused');
      const div = container.querySelector('div');
      expect(div?.style.animation).toBeFalsy();
    });
  });

  describe('svg structure', () => {
    it('renders svg with correct dimensions', () => {
      renderCharacterFace(0, 'idle');
      const svg = screen.getByRole('img', { hidden: true });
      expect(svg).toHaveAttribute('width', '280');
      expect(svg).toHaveAttribute('height', '280');
      expect(svg).toHaveAttribute('viewBox', '0 0 280 280');
    });

    it('renders face circle', () => {
      renderCharacterFace(0, 'idle');
      const svg = screen.getByRole('img', { hidden: true });
      const circle = svg.querySelector('circle[cx="140"][cy="140"][r="130"]');
      expect(circle).toBeInTheDocument();
    });

    it('renders both eyes', () => {
      renderCharacterFace(0, 'idle');
      const svg = screen.getByRole('img', { hidden: true });
      const eyes = svg.querySelectorAll('circle[r="18"]');
      expect(eyes.length).toBe(2);
    });
  });
});
