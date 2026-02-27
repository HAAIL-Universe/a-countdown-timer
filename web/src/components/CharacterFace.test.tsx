import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import CharacterFace from './CharacterFace';

describe('CharacterFace', () => {
  it('renders happy face for urgencyLevel 0', () => {
    render(<CharacterFace urgencyLevel={0} status="idle" />);
    const face = screen.getByTestId('character-face');
    expect(face).toBeTruthy();
    // Happy face should have the green fill (#22C55E)
    const svg = face.querySelector('circle');
    expect(svg?.getAttribute('fill')).toBe('#22C55E');
  });

  it('renders anxious face for urgencyLevel 2', () => {
    render(<CharacterFace urgencyLevel={2} status="running" />);
    const face = screen.getByTestId('character-face');
    // Anxious face should have yellow fill (#FBBF24)
    const svg = face.querySelector('circle');
    expect(svg?.getAttribute('fill')).toBe('#FBBF24');
  });

  it('renders upset face for urgencyLevel 3', () => {
    render(<CharacterFace urgencyLevel={3} status="running" />);
    const face = screen.getByTestId('character-face');
    // Upset face should have red fill (#EF4444)
    const svg = face.querySelector('circle');
    expect(svg?.getAttribute('fill')).toBe('#EF4444');
  });
});
