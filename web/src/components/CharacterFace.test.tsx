import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { CharacterFace } from './CharacterFace';

describe('CharacterFace', () => {
  it('renders happy face for urgencyLevel 0', () => {
    const { container } = render(
      <CharacterFace urgencyLevel={0} status="idle" />
    );

    const circle = container.querySelector('circle[r="12"]');
    expect(circle).toBeInTheDocument();

    const svg = container.querySelector('svg');
    expect(svg).toHaveClass('fill-green-500');
  });

  it('renders anxious face for urgencyLevel 2', () => {
    const { container } = render(
      <CharacterFace urgencyLevel={2} status="running" />
    );

    const ellipse = container.querySelector('ellipse[rx="12"]');
    expect(ellipse).toBeInTheDocument();

    const svg = container.querySelector('svg');
    expect(svg).toHaveClass('fill-yellow-400');
  });

  it('renders upset face for urgencyLevel 3', () => {
    const { container } = render(
      <CharacterFace urgencyLevel={3} status="running" />
    );

    const svg = container.querySelector('svg');
    expect(svg).toHaveClass('fill-red-500');
    expect(svg?.parentElement).toHaveClass('animate-pulse');
  });

  it('renders neutral face for urgencyLevel 1', () => {
    const { container } = render(
      <CharacterFace urgencyLevel={1} status="idle" />
    );

    const svg = container.querySelector('svg');
    expect(svg).toHaveClass('fill-blue-500');
  });

  it('applies green color for urgencyLevel 0', () => {
    const { container } = render(
      <CharacterFace urgencyLevel={0} status="idle" />
    );

    const svg = container.querySelector('svg');
    expect(svg).toHaveClass('fill-green-500');
  });

  it('applies yellow color for urgencyLevel 2', () => {
    const { container } = render(
      <CharacterFace urgencyLevel={2} status="running" />
    );

    const svg = container.querySelector('svg');
    expect(svg).toHaveClass('fill-yellow-400');
  });

  it('applies red color and flash animation for urgencyLevel 3', () => {
    const { container } = render(
      <CharacterFace urgencyLevel={3} status="running" />
    );

    const svg = container.querySelector('svg');
    expect(svg).toHaveClass('fill-red-500');

    const wrapper = svg?.parentElement;
    expect(wrapper).toHaveClass('animate-pulse');
  });

  it('renders open eyes for urgencyLevel 0', () => {
    const { container } = render(
      <CharacterFace urgencyLevel={0} status="idle" />
    );

    const circles = container.querySelectorAll('circle[r="12"]');
    expect(circles.length).toBe(2);
  });

  it('renders raised eyebrows for urgencyLevel 2', () => {
    const { container } = render(
      <CharacterFace urgencyLevel={2} status="running" />
    );

    const ellipses = container.querySelectorAll('ellipse[rx="12"]');
    expect(ellipses.length).toBe(2);
  });

  it('renders sad mouth for urgencyLevel 3', () => {
    const { container } = render(
      <CharacterFace urgencyLevel={3} status="running" />
    );

    const paths = container.querySelectorAll('path');
    const sadMouthPath = Array.from(paths).find(
      (p) => p.getAttribute('d') === 'M 70 135 Q 100 115 130 135'
    );
    expect(sadMouthPath).toBeInTheDocument();
  });

  it('renders smile for urgencyLevel 0', () => {
    const { container } = render(
      <CharacterFace urgencyLevel={0} status="idle" />
    );

    const paths = container.querySelectorAll('path');
    const smilePath = Array.from(paths).find(
      (p) => p.getAttribute('d') === 'M 70 120 Q 100 145 130 120'
    );
    expect(smilePath).toBeInTheDocument();
  });

  it('has SVG with correct viewBox', () => {
    const { container } = render(
      <CharacterFace urgencyLevel={0} status="idle" />
    );

    const svg = container.querySelector('svg');
    expect(svg).toHaveAttribute('viewBox', '0 0 200 200');
  });

  it('applies transition class to SVG', () => {
    const { container } = render(
      <CharacterFace urgencyLevel={0} status="idle" />
    );

    const svg = container.querySelector('svg');
    expect(svg).toHaveClass('transition-all', 'duration-300');
  });

  it('renders centered flexbox container', () => {
    const { container } = render(
      <CharacterFace urgencyLevel={0} status="idle" />
    );

    const wrapper = container.firstChild;
    expect(wrapper).toHaveClass('flex', 'justify-center', 'items-center');
  });

  it('does not flash animation for urgencyLevel 0', () => {
    const { container } = render(
      <CharacterFace urgencyLevel={0} status="idle" />
    );

    const wrapper = container.firstChild;
    expect(wrapper).not.toHaveClass('animate-pulse');
  });

  it('does not flash animation for urgencyLevel 2', () => {
    const { container } = render(
      <CharacterFace urgencyLevel={2} status="running" />
    );

    const wrapper = container.firstChild;
    expect(wrapper).not.toHaveClass('animate-pulse');
  });
});
