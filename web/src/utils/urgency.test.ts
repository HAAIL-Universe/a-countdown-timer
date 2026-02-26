import { describe, it, expect } from 'vitest';
import {
  formatMMSS,
  getUrgencyColor,
  getUrgencyBgClass,
  shouldFlash,
  computeUrgencyLevel,
} from './urgency';
import { Timer } from '../types/timer';

describe('formatMMSS', () => {
  it('converts 0 seconds to 00:00', () => {
    expect(formatMMSS(0)).toBe('00:00');
  });

  it('converts 5 seconds to 00:05', () => {
    expect(formatMMSS(5)).toBe('00:05');
  });

  it('converts 59 seconds to 00:59', () => {
    expect(formatMMSS(59)).toBe('00:59');
  });

  it('converts 60 seconds to 01:00', () => {
    expect(formatMMSS(60)).toBe('01:00');
  });

  it('converts 65 seconds to 01:05', () => {
    expect(formatMMSS(65)).toBe('01:05');
  });

  it('converts 600 seconds to 10:00', () => {
    expect(formatMMSS(600)).toBe('10:00');
  });

  it('converts 3661 seconds to 61:01', () => {
    expect(formatMMSS(3661)).toBe('61:01');
  });

  it('pads single digit minutes with zero', () => {
    expect(formatMMSS(30)).toBe('00:30');
  });

  it('pads single digit seconds with zero', () => {
    expect(formatMMSS(125)).toBe('02:05');
  });
});

describe('getUrgencyColor', () => {
  it('returns green for urgency level 0', () => {
    expect(getUrgencyColor(0)).toBe('#22C55E');
  });

  it('returns blue for urgency level 1', () => {
    expect(getUrgencyColor(1)).toBe('#3B82F6');
  });

  it('returns yellow for urgency level 2', () => {
    expect(getUrgencyColor(2)).toBe('#FBBF24');
  });

  it('returns red for urgency level 3', () => {
    expect(getUrgencyColor(3)).toBe('#EF4444');
  });

  it('returns default gray for unknown urgency level', () => {
    expect(getUrgencyColor(99)).toBe('#1F2937');
  });

  it('returns default gray for negative urgency level', () => {
    expect(getUrgencyColor(-1)).toBe('#1F2937');
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

  it('returns default bg-gray-800 for unknown urgency level', () => {
    expect(getUrgencyBgClass(99)).toBe('bg-gray-800');
  });
});

describe('shouldFlash', () => {
  it('returns true when urgencyLevel is 3', () => {
    const timer: Timer = {
      id: 'test-1',
      duration: 60,
      elapsedTime: 55,
      status: 'running',
      urgencyLevel: 3,
      createdAt: '2024-01-01T00:00:00Z',
      updatedAt: '2024-01-01T00:00:00Z',
    };
    expect(shouldFlash(timer)).toBe(true);
  });

  it('returns false when urgencyLevel is 0', () => {
    const timer: Timer = {
      id: 'test-2',
      duration: 60,
      elapsedTime: 0,
      status: 'idle',
      urgencyLevel: 0,
      createdAt: '2024-01-01T00:00:00Z',
      updatedAt: '2024-01-01T00:00:00Z',
    };
    expect(shouldFlash(timer)).toBe(false);
  });

  it('returns false when urgencyLevel is 1', () => {
    const timer: Timer = {
      id: 'test-3',
      duration: 120,
      elapsedTime: 30,
      status: 'running',
      urgencyLevel: 1,
      createdAt: '2024-01-01T00:00:00Z',
      updatedAt: '2024-01-01T00:00:00Z',
    };
    expect(shouldFlash(timer)).toBe(false);
  });

  it('returns false when urgencyLevel is 2', () => {
    const timer: Timer = {
      id: 'test-4',
      duration: 120,
      elapsedTime: 95,
      status: 'running',
      urgencyLevel: 2,
      createdAt: '2024-01-01T00:00:00Z',
      updatedAt: '2024-01-01T00:00:00Z',
    };
    expect(shouldFlash(timer)).toBe(false);
  });
});

describe('computeUrgencyLevel', () => {
  it('returns 0 when timer has not started (elapsedTime === 0)', () => {
    expect(computeUrgencyLevel(0, 100)).toBe(0);
  });

  it('returns 1 when timer is running but >30s remaining', () => {
    expect(computeUrgencyLevel(10, 100)).toBe(1);
  });

  it('returns 2 when remaining time is between 11 and 30 seconds', () => {
    expect(computeUrgencyLevel(70, 100)).toBe(2);
  });

  it('returns 2 when exactly 30 seconds remaining', () => {
    expect(computeUrgencyLevel(70, 100)).toBe(2);
  });

  it('returns 3 when remaining time is 10 seconds or less', () => {
    expect(computeUrgencyLevel(90, 100)).toBe(3);
  });

  it('returns 3 when exactly 10 seconds remaining', () => {
    expect(computeUrgencyLevel(90, 100)).toBe(3);
  });

  it('returns 3 when timer has expired (elapsedTime >= duration)', () => {
    expect(computeUrgencyLevel(100, 100)).toBe(3);
  });

  it('returns 3 when timer has exceeded duration', () => {
    expect(computeUrgencyLevel(105, 100)).toBe(3);
  });

  it('returns 1 when 31 seconds remain (just outside level 2)', () => {
    expect(computeUrgencyLevel(69, 100)).toBe(1);
  });

  it('returns 3 when 11 seconds remain (boundary between levels 2 and 3)', () => {
    expect(computeUrgencyLevel(89, 100)).toBe(3);
  });
});
