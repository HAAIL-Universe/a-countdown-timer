import { describe, it, expect } from 'vitest';
import { formatMMSS, getUrgencyColor, getUrgencyBgClass, shouldFlash } from './urgency';
import { Timer } from '../types/timer';

describe('formatMMSS', () => {
  it('converts 0 seconds to 00:00', () => {
    expect(formatMMSS(0)).toBe('00:00');
  });

  it('converts seconds to MM:SS with leading zeros', () => {
    expect(formatMMSS(5)).toBe('00:05');
    expect(formatMMSS(59)).toBe('00:59');
  });

  it('converts 60 seconds to 01:00', () => {
    expect(formatMMSS(60)).toBe('01:00');
  });

  it('converts 125 seconds to 02:05', () => {
    expect(formatMMSS(125)).toBe('02:05');
  });

  it('converts 3661 seconds to 61:01', () => {
    expect(formatMMSS(3661)).toBe('61:01');
  });

  it('handles large durations', () => {
    expect(formatMMSS(5999)).toBe('99:59');
  });

  it('pads both minutes and seconds with leading zeros', () => {
    expect(formatMMSS(1)).toBe('00:01');
    expect(formatMMSS(120)).toBe('02:00');
  });
});

describe('getUrgencyColor', () => {
  it('returns green hex for urgency level 0', () => {
    expect(getUrgencyColor(0)).toBe('#22C55E');
  });

  it('returns blue hex for urgency level 1', () => {
    expect(getUrgencyColor(1)).toBe('#3B82F6');
  });

  it('returns yellow hex for urgency level 2', () => {
    expect(getUrgencyColor(2)).toBe('#FBBF24');
  });

  it('returns red hex for urgency level 3', () => {
    expect(getUrgencyColor(3)).toBe('#EF4444');
  });

  it('returns green hex for unknown urgency level', () => {
    expect(getUrgencyColor(4)).toBe('#22C55E');
    expect(getUrgencyColor(-1)).toBe('#22C55E');
    expect(getUrgencyColor(100)).toBe('#22C55E');
  });
});

describe('getUrgencyBgClass', () => {
  it('returns bg-green-500 for urgency level 0', () => {
    expect(getUrgencyBgClass(0)).toBe('bg-green-500');
  });

  it('returns bg-blue-500 for urgency level 1', () => {
    expect(getUrgencyBgClass(1)).toBe('bg-blue-500');
  });

  it('returns bg-yellow-400 for urgency level 2', () => {
    expect(getUrgencyBgClass(2)).toBe('bg-yellow-400');
  });

  it('returns bg-red-500 for urgency level 3', () => {
    expect(getUrgencyBgClass(3)).toBe('bg-red-500');
  });

  it('returns bg-green-500 for unknown urgency level', () => {
    expect(getUrgencyBgClass(4)).toBe('bg-green-500');
    expect(getUrgencyBgClass(-1)).toBe('bg-green-500');
  });
});

describe('shouldFlash', () => {
  it('returns true when urgency level is 3', () => {
    const timer: Timer = {
      id: 'timer-1',
      duration: 60,
      elapsedTime: 54,
      status: 'running',
      urgencyLevel: 3,
      createdAt: '2024-01-01T00:00:00Z',
      updatedAt: '2024-01-01T00:00:10Z',
    };
    expect(shouldFlash(timer)).toBe(true);
  });

  it('returns false when urgency level is 0', () => {
    const timer: Timer = {
      id: 'timer-1',
      duration: 60,
      elapsedTime: 0,
      status: 'idle',
      urgencyLevel: 0,
      createdAt: '2024-01-01T00:00:00Z',
      updatedAt: '2024-01-01T00:00:00Z',
    };
    expect(shouldFlash(timer)).toBe(false);
  });

  it('returns false when urgency level is 1', () => {
    const timer: Timer = {
      id: 'timer-1',
      duration: 60,
      elapsedTime: 10,
      status: 'running',
      urgencyLevel: 1,
      createdAt: '2024-01-01T00:00:00Z',
      updatedAt: '2024-01-01T00:00:05Z',
    };
    expect(shouldFlash(timer)).toBe(false);
  });

  it('returns false when urgency level is 2', () => {
    const timer: Timer = {
      id: 'timer-1',
      duration: 60,
      elapsedTime: 48,
      status: 'running',
      urgencyLevel: 2,
      createdAt: '2024-01-01T00:00:00Z',
      updatedAt: '2024-01-01T00:00:12Z',
    };
    expect(shouldFlash(timer)).toBe(false);
  });

  it('flashes only when urgency is exactly 3, regardless of other timer state', () => {
    const timerPaused: Timer = {
      id: 'timer-1',
      duration: 100,
      elapsedTime: 95,
      status: 'paused',
      urgencyLevel: 3,
      createdAt: '2024-01-01T00:00:00Z',
      updatedAt: '2024-01-01T00:01:35Z',
    };
    expect(shouldFlash(timerPaused)).toBe(true);

    const timerComplete: Timer = {
      id: 'timer-1',
      duration: 100,
      elapsedTime: 100,
      status: 'complete',
      urgencyLevel: 3,
      createdAt: '2024-01-01T00:00:00Z',
      updatedAt: '2024-01-01T00:01:40Z',
    };
    expect(shouldFlash(timerComplete)).toBe(true);
  });
});
