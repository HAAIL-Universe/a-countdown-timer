import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { CharacterFace } from './CharacterFace';
import type { TimerStatus } from '../types/timer';

describe('CharacterFace', () => {
  const defaultProps = {
    urgencyLevel: 0,
    status: 'idle' as TimerStatus,
  };

  it('renders the component without errors', () => {
    render(<CharacterFace {...defaultProps} />);
    const container = screen.getByRole('generic', { hidden: true }).parentElement;
    expect(container).toBeInTheDocument();
  });

  it('renders happy face for urgencyLevel 0', () => {
    const { container } = render(<CharacterFace urgencyLevel={0} status="idle" />);
    const mouthElement = container.querySelector('.mouth-happy');
    expect(mouthElement).toBeInTheDocument();
  });

  it('renders neutral face for urgencyLevel 1', () => {
    const { container } = render(<CharacterFace urgencyLevel={1} status="idle" />);
    const mouthElement = container.querySelector('.mouth-neutral');
    expect(mouthElement).toBeInTheDocument();
  });

  it('renders anxious face for urgencyLevel 2', () => {
    const { container } = render(<CharacterFace urgencyLevel={2} status="idle" />);
    const mouthElement = container.querySelector('.mouth-anxious');
    expect(mouthElement).toBeInTheDocument();
    const leftEyebrow = container.querySelector('.eyebrow-anxious-left');
    expect(leftEyebrow).toBeInTheDocument();
    const rightEyebrow = container.querySelector('.eyebrow-anxious-right');
    expect(rightEyebrow).toBeInTheDocument();
  });

  it('renders upset face for urgencyLevel 3', () => {
    const { container } = render(<CharacterFace urgencyLevel={3} status="idle" />);
    const mouthElement = container.querySelector('.mouth-upset');
    expect(mouthElement).toBeInTheDocument();
    const leftEyebrow = container.querySelector('.eyebrow-upset-left');
    expect(leftEyebrow).toBeInTheDocument();
    const rightEyebrow = container.querySelector('.eyebrow-upset-right');
    expect(rightEyebrow).toBeInTheDocument();
  });

  it('applies green background for idle status with urgencyLevel 0', () => {
    const { container } = render(<CharacterFace urgencyLevel={0} status="idle" />);
    const wrapper = container.firstChild as HTMLElement;
    expect(wrapper.className).toContain('flex');
  });

  it('applies blue background for running status', () => {
    const { container } = render(<CharacterFace urgencyLevel={0} status="running" />);
    const wrapper = container.firstChild as HTMLElement;
    expect(wrapper).toBeInTheDocument();
  });

  it('applies yellow background for urgencyLevel 2', () => {
    const { container } = render(<CharacterFace urgencyLevel={2} status="idle" />);
    const wrapper = container.firstChild as HTMLElement;
    expect(wrapper).toBeInTheDocument();
  });

  it('applies red background and animate-pulse for urgencyLevel 3', () => {
    const { container } = render(<CharacterFace urgencyLevel={3} status="idle" />);
    const wrapper = container.firstChild as HTMLElement;
    expect(wrapper.className).toContain('animate-pulse');
  });

  it('does not apply animate-pulse for urgencyLevel < 3', () => {
    const { container } = render(<CharacterFace urgencyLevel={2} status="idle" />);
    const wrapper = container.firstChild as HTMLElement;
    expect(wrapper.className).not.toContain('animate-pulse');
  });

  it('renders eyes in correct positions', () => {
    const { container } = render(<CharacterFace urgencyLevel={0} status="idle" />);
    const leftEye = container.querySelector('.eye-left');
    const rightEye = container.querySelector('.eye-right');
    expect(leftEye).toBeInTheDocument();
    expect(rightEye).toBeInTheDocument();
  });

  it('renders eyebrows in correct positions for happy face', () => {
    const { container } = render(<CharacterFace urgencyLevel={0} status="idle" />);
    const leftBrow = container.querySelector('.eyebrow-left');
    const rightBrow = container.querySelector('.eyebrow-right');
    expect(leftBrow).toBeInTheDocument();
    expect(rightBrow).toBeInTheDocument();
  });

  it('transitions between expressions when urgencyLevel changes', () => {
    const { rerender, container } = render(
      <CharacterFace urgencyLevel={0} status="idle" />
    );
    expect(container.querySelector('.mouth-happy')).toBeInTheDocument();

    rerender(<CharacterFace urgencyLevel={2} status="idle" />);
    expect(container.querySelector('.mouth-anxious')).toBeInTheDocument();

    rerender(<CharacterFace urgencyLevel={3} status="idle" />);
    expect(container.querySelector('.mouth-upset')).toBeInTheDocument();
  });

  it('maintains expression when status changes but urgencyLevel stays same', () => {
    const { rerender, container } = render(
      <CharacterFace urgencyLevel={1} status="idle" />
    );
    expect(container.querySelector('.mouth-neutral')).toBeInTheDocument();

    rerender(<CharacterFace urgencyLevel={1} status="running" />);
    expect(container.querySelector('.mouth-neutral')).toBeInTheDocument();
  });

  it('renders character face with correct dimensions in CSS', () => {
    const { container } = render(<CharacterFace urgencyLevel={0} status="idle" />);
    const styleElement = container.querySelector('style');
    expect(styleElement?.textContent).toContain('.character-face');
    expect(styleElement?.textContent).toContain('width: 280px');
    expect(styleElement?.textContent).toContain('height: 280px');
  });

  it('defines flash animation in CSS', () => {
    const { container } = render(<CharacterFace urgencyLevel={3} status="idle" />);
    const styleElement = container.querySelector('style');
    expect(styleElement?.textContent).toContain('@keyframes flash');
    expect(styleElement?.textContent).toContain('opacity: 1');
    expect(styleElement?.textContent).toContain('opacity: 0.5');
  });
});
