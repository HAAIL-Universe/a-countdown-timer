import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { CharacterFace } from './CharacterFace';
import type { TimerStatus, UrgencyLevel } from '../types/timer';

describe('CharacterFace', () => {
  it('renders happy face for urgencyLevel 0', () => {
    render(<CharacterFace urgencyLevel={0} status="idle" />);

    const svg = screen.getByRole('img', { hidden: true });
    expect(svg).toBeInTheDocument();

    const faceCircle = svg.querySelector('circle[cx="100"][cy="100"]');
    expect(faceCircle).toHaveAttribute('fill', '#22C55E');
  });

  it('renders anxious face for urgencyLevel 2', () => {
    render(<CharacterFace urgencyLevel={2} status="running" />);

    const svg = screen.getByRole('img', { hidden: true });
    expect(svg).toBeInTheDocument();

    const faceCircle = svg.querySelector('circle[cx="100"][cy="100"]');
    expect(faceCircle).toHaveAttribute('fill', '#FBBF24');
  });

  it('renders upset face for urgencyLevel 3', () => {
    render(<CharacterFace urgencyLevel={3} status="running" />);

    const svg = screen.getByRole('img', { hidden: true });
    expect(svg).toBeInTheDocument();

    const faceCircle = svg.querySelector('circle[cx="100"][cy="100"]');
    expect(faceCircle).toHaveAttribute('fill', '#EF4444');
  });

  it('renders happy face when status is idle regardless of urgency level', () => {
    render(<CharacterFace urgencyLevel={3} status="idle" />);

    const svg = screen.getByRole('img', { hidden: true });
    const faceCircle = svg.querySelector('circle[cx="100"][cy="100"]');
    expect(faceCircle).toHaveAttribute('fill', '#22C55E');
  });

  it('renders upset face when status is complete regardless of urgency level', () => {
    render(<CharacterFace urgencyLevel={0} status="complete" />);

    const svg = screen.getByRole('img', { hidden: true });
    const faceCircle = svg.querySelector('circle[cx="100"][cy="100"]');
    expect(faceCircle).toHaveAttribute('fill', '#EF4444');
  });

  it('applies animate-pulse class for urgencyLevel 3', () => {
    const { container } = render(<CharacterFace urgencyLevel={3} status="running" />);

    const div = container.querySelector('div.flex');
    expect(div).toHaveClass('animate-pulse');
  });

  it('does not apply animate-pulse class for urgencyLevel 0', () => {
    const { container } = render(<CharacterFace urgencyLevel={0} status="idle" />);

    const div = container.querySelector('div.flex');
    expect(div).not.toHaveClass('animate-pulse');
  });

  it('applies correct scale transform for urgencyLevel 2', () => {
    const { container } = render(<CharacterFace urgencyLevel={2} status="running" />);

    const div = container.querySelector('div.flex');
    expect(div).toHaveStyle('transform: scale(1.05)');
  });

  it('applies correct scale transform for urgencyLevel 3', () => {
    const { container } = render(<CharacterFace urgencyLevel={3} status="running" />);

    const div = container.querySelector('div.flex');
    expect(div).toHaveStyle('transform: scale(1.1)');
  });

  it('renders SVG with correct dimensions', () => {
    render(<CharacterFace urgencyLevel={0} status="idle" />);

    const svg = screen.getByRole('img', { hidden: true });
    expect(svg).toHaveAttribute('width', '200');
    expect(svg).toHaveAttribute('height', '200');
    expect(svg).toHaveAttribute('viewBox', '0 0 200 200');
  });

  it('renders with transition class for smooth color changes', () => {
    const { container } = render(<CharacterFace urgencyLevel={0} status="idle" />);

    const div = container.querySelector('div.flex');
    expect(div).toHaveClass('transition-all', 'duration-300');
  });
});
