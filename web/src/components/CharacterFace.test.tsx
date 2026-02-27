import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { CharacterFace } from './CharacterFace';
import type { TimerStatus } from '../types/timer';

describe('CharacterFace', () => {
  const renderCharacter = (urgencyLevel: number, status: TimerStatus = 'idle') => {
    return render(<CharacterFace urgencyLevel={urgencyLevel} status={status} />);
  };

  describe('happy expression (urgencyLevel 0)', () => {
    it('renders happy face for urgencyLevel 0', () => {
      renderCharacter(0);
      const svg = screen.getByRole('img', { hidden: true }) || document.querySelector('svg');
      expect(svg).toBeInTheDocument();
      const happyPaths = document.querySelectorAll('svg path[d*="Q"]');
      expect(happyPaths.length).toBeGreaterThan(0);
    });

    it('renders closed happy eyes for urgencyLevel 0', () => {
      renderCharacter(0);
      const svg = document.querySelector('svg');
      expect(svg).toBeInTheDocument();
      const eyePaths = svg?.querySelectorAll('path[d*="M 65 78"]');
      expect(eyePaths?.length).toBeGreaterThan(0);
    });

    it('renders big smile for urgencyLevel 0', () => {
      renderCharacter(0);
      const svg = document.querySelector('svg');
      const smilePath = svg?.querySelector('path[d*="M 70 125"]');
      expect(smilePath).toBeInTheDocument();
    });

    it('does not have animate-pulse class for urgencyLevel 0', () => {
      const { container } = renderCharacter(0);
      const wrapper = container.querySelector('div');
      expect(wrapper?.className).not.toContain('animate-pulse');
    });
  });

  describe('anxious expression (urgencyLevel 2)', () => {
    it('renders anxious face for urgencyLevel 2', () => {
      renderCharacter(2);
      const svg = document.querySelector('svg');
      expect(svg).toBeInTheDocument();
    });

    it('renders open anxious eyes for urgencyLevel 2', () => {
      renderCharacter(2);
      const svg = document.querySelector('svg');
      const anxiousEyes = svg?.querySelectorAll('circle[r="12"]');
      expect(anxiousEyes?.length).toBeGreaterThanOrEqual(2);
    });

    it('renders O-shaped mouth for anxious expression', () => {
      renderCharacter(2);
      const svg = document.querySelector('svg');
      const mouthCircle = svg?.querySelector('circle[cx="100"][cy="135"]');
      expect(mouthCircle).toBeInTheDocument();
      expect(mouthCircle).toHaveAttribute('r', '12');
      expect(mouthCircle).toHaveAttribute('fill', 'none');
    });

    it('does not have animate-pulse class for urgencyLevel 2', () => {
      const { container } = renderCharacter(2);
      const wrapper = container.querySelector('div');
      expect(wrapper?.className).not.toContain('animate-pulse');
    });
  });

  describe('upset expression (urgencyLevel 3)', () => {
    it('renders upset face for urgencyLevel 3', () => {
      renderCharacter(3);
      const svg = document.querySelector('svg');
      expect(svg).toBeInTheDocument();
    });

    it('renders X eyes for upset expression', () => {
      renderCharacter(3);
      const svg = document.querySelector('svg');
      const xPaths = svg?.querySelectorAll('path[d*="M 65 75"]');
      expect(xPaths?.length).toBeGreaterThan(0);
    });

    it('renders downward mouth for upset expression', () => {
      renderCharacter(3);
      const svg = document.querySelector('svg');
      const sadMouth = svg?.querySelector('path[d*="M 70 140"]');
      expect(sadMouth).toBeInTheDocument();
    });

    it('has animate-pulse class for urgencyLevel 3', () => {
      const { container } = renderCharacter(3);
      const wrapper = container.querySelector('div');
      expect(wrapper?.className).toContain('animate-pulse');
    });

    it('has animate-pulse applied when urgencyLevel is 3 with different statuses', () => {
      const statuses: TimerStatus[] = ['idle', 'running', 'paused', 'complete'];
      statuses.forEach((status) => {
        const { container, unmount } = renderCharacter(3, status);
        const wrapper = container.querySelector('div');
        expect(wrapper?.className).toContain('animate-pulse');
        unmount();
      });
    });
  });

  describe('expression transitions', () => {
    it('transitions from happy to anxious when urgencyLevel changes', () => {
      const { rerender, container: container1 } = renderCharacter(0);
      let happyMouth = container1.querySelector('path[d*="M 70 125"]');
      expect(happyMouth).toBeInTheDocument();

      rerender(<CharacterFace urgencyLevel={2} status="running" />);
      const { container: container2 } = render(
        <CharacterFace urgencyLevel={2} status="running" />,
      );
      const anxiousMouth = container2.querySelector('circle[cx="100"][cy="135"]');
      expect(anxiousMouth).toBeInTheDocument();
    });

    it('transitions from anxious to upset when urgencyLevel increases to 3', () => {
      const { rerender } = renderCharacter(2);
      rerender(<CharacterFace urgencyLevel={3} status="running" />);

      const svg = document.querySelector('svg');
      const upsetEyes = svg?.querySelector('path[d*="M 65 75"]');
      expect(upsetEyes).toBeInTheDocument();
    });
  });

  describe('SVG structure', () => {
    it('renders head circle with correct attributes', () => {
      renderCharacter(0);
      const svg = document.querySelector('svg');
      const headCircle = svg?.querySelector('circle[cx="100"][cy="100"]');
      expect(headCircle).toBeInTheDocument();
      expect(headCircle).toHaveAttribute('r', '90');
      expect(headCircle).toHaveAttribute('fill', '#FFD700');
    });

    it('renders both eye whites', () => {
      renderCharacter(0);
      const svg = document.querySelector('svg');
      const leftEye = svg?.querySelector('circle[cx="75"][cy="85"][r="18"]');
      const rightEye = svg?.querySelector('circle[cx="125"][cy="85"][r="18"]');
      expect(leftEye).toBeInTheDocument();
      expect(rightEye).toBeInTheDocument();
    });

    it('renders iris circles', () => {
      renderCharacter(0);
      const svg = document.querySelector('svg');
      const irises = svg?.querySelectorAll('circle[r="10"]');
      expect(irises?.length).toBeGreaterThanOrEqual(2);
    });

    it('has proper SVG dimensions', () => {
      renderCharacter(1);
      const svg = document.querySelector('svg');
      expect(svg).toHaveAttribute('width', '200');
      expect(svg).toHaveAttribute('height', '200');
      expect(svg).toHaveAttribute('viewBox', '0 0 200 200');
    });
  });

  describe('props handling', () => {
    it('accepts urgencyLevel as prop', () => {
      renderCharacter(0);
      expect(document.querySelector('svg')).toBeInTheDocument();
    });

    it('accepts status as prop and renders without error', () => {
      const statuses: TimerStatus[] = ['idle', 'running', 'paused', 'complete'];
      statuses.forEach((status) => {
        const { unmount } = renderCharacter(1, status);
        expect(document.querySelector('svg')).toBeInTheDocument();
        unmount();
      });
    });

    it('handles urgencyLevel 1 as happy (same as 0)', () => {
      const { container } = renderCharacter(1);
      const svg = container.querySelector('svg');
      const happyMouth = svg?.querySelector('path[d*="M 70 125"]');
      expect(happyMouth).toBeInTheDocument();
    });
  });

  describe('accessibility', () => {
    it('renders SVG with drop-shadow styling', () => {
      renderCharacter(2);
      const svg = document.querySelector('svg');
      expect(svg).toHaveAttribute('class', 'drop-shadow-lg');
    });

    it('maintains semantic div wrapper', () => {
      const { container } = renderCharacter(0);
      const wrapper = container.querySelector('div');
      expect(wrapper).toHaveClass('flex');
      expect(wrapper).toHaveClass('justify-center');
      expect(wrapper).toHaveClass('items-center');
    });
  });
});
