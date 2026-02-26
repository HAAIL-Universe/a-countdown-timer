import { describe, it, expect } from 'vitest';
import {
  formatMMSS,
  getUrgencyColor,
  getUrgencyBgClass,
  computeUrgencyLevel,
  shouldFlash,
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

  it('converts 120 seconds to 02:00', () => {
    expect(formatMMSS(120)).toBe('02:00');
  });

  it('converts 599 seconds to 09:59', () => {
    expect(formatMMSS(599)).toBe('09:59');
  });

  it('converts 600 seconds to 10:00', () => {
    expect(formatMMSS(600)).toBe('10:00');
  });

  it('converts 3661 seconds to 61:01', () => {
    expect(formatMMSS(3661)).toBe('61:01');
  });

  it('pads minutes with leading zero', () => {
    expect(formatMMSS(125)).toBe('02:05');
  });

  it('pads seconds with leading zero', () => {
    expect(formatMMSS(63)).toBe('01:03');
  });
});

describe('getUrgencyColor', () => {
  it('returns green for urgency level 0', () => {
    expect(getUrgencyColor(0)).toBe('text-green-400');
  });

  it('returns green for urgency level 1', () => {
    expect(getUrgencyColor(1)).toBe('text-green-400');
  });

  it('returns yellow for urgency level 2', () => {
    expect(getUrgencyColor(2)).toBe('text-yellow-400');
  });

  it('returns red for urgency level 3', () => {
    expect(getUrgencyColor(3)).toBe('text-red-500');
  });

  it('returns green for negative urgency level', () => {
    expect(getUrgencyColor(-1)).toBe('text-green-400');
  });

  it('returns green for high urgency level > 3', () => {
    expect(getUrgencyColor(5)).toBe('text-green-400');
  });
});

describe('getUrgencyBgClass', () => {
  it('returns green background for urgency level 0', () => {
    expect(getUrgencyBgClass(0)).toBe('bg-green-900');
  });

  it('returns green background for urgency level 1', () => {
    expect(getUrgencyBgClass(1)).toBe('bg-green-900');
  });

  it('returns yellow background for urgency level 2', () => {
    expect(getUrgencyBgClass(2)).toBe('bg-yellow-900');
  });

  it('returns red background for urgency level 3', () => {
    expect(getUrgencyBgClass(3)).toBe('bg-red-900');
  });

  it('returns green background for negative urgency level', () => {
    expect(getUrgencyBgClass(-1)).toBe('bg-green-900');
  });

  it('returns green background for high urgency level > 3', () => {
    expect(getUrgencyBgClass(5)).toBe('bg-green-900');
  });
});

describe('computeUrgencyLevel', () => {
  it('returns 0 (idle) when remaining time > 30 seconds', () => {
    expect(computeUrgencyLevel(0, 60)).toBe(0);
  });

  it('returns 2 (urgent) when remaining time = 30 seconds', () => {
    expect(computeUrgencyLevel(0, 30)).toBe(2);
  });

  it('returns 2 (urgent) when remaining time = 20 seconds', () => {
    expect(computeUrgencyLevel(40, 60)).toBe(2);
  });

  it('returns 3 (critical) when remaining time = 10 seconds', () => {
    expect(computeUrgencyLevel(50, 60)).toBe(3);
  });

  it('returns 3 (critical) when remaining time = 5 seconds', () => {
    expect(computeUrgencyLevel(55, 60)).toBe(3);
  });

  it('returns 3 (critical) when remaining time = 0 seconds', () => {
    expect(computeUrgencyLevel(60, 60)).toBe(3);
  });

  it('returns 3 (critical) when elapsed > duration', () => {
    expect(computeUrgencyLevel(70, 60)).toBe(3);
  });

  it('returns 2 (urgent) when remaining time = 15 seconds', () => {
    expect(computeUrgencyLevel(45, 60)).toBe(2);
  });

  it('returns 0 (idle) when remaining time = 31 seconds', () => {
    expect(computeUrgencyLevel(29, 60)).toBe(0);
  });

  it('returns 3 (critical) when remaining time = 11 seconds', () => {
    expect(computeUrgencyLevel(49, 60)).toBe(3);
  });
});

describe('shouldFlash', () => {
  const createTimer = (overrides: Partial<Timer>): Timer => ({
    id: 'test-id',
    duration: 60,
    elapsedTime: 0,
    status: 'running',
    urgencyLevel: 0,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    ...overrides,
  });

  it('returns true when urgency level is 3 and status is running', () => {
    const timer = createTimer({ urgencyLevel: 3, status: 'running' });
    expect(shouldFlash(timer)).toBe(true);
  });

  it('returns false when urgency level is 3 but status is paused', () => {
    const timer = createTimer({ urgencyLevel: 3, status: 'paused' });
    expect(shouldFlash(timer)).toBe(false);
  });

  it('returns false when urgency level is 3 but status is idle', () => {
    const timer = createTimer({ urgencyLevel: 3, status: 'idle' });
    expect(shouldFlash(timer)).toBe(false);
  });

  it('returns false when urgency level is 3 but status is complete', () => {
    const timer = createTimer({ urgencyLevel: 3, status: 'complete' });
    expect(shouldFlash(timer)).toBe(false);
  });

  it('returns false when urgency level is 2 and status is running', () => {
    const timer = createTimer({ urgencyLevel: 2, status: 'running' });
    expect(shouldFlash(timer)).toBe(false);
  });

  it('returns false when urgency level is 0 and status is running', () => {
    const timer = createTimer({ urgencyLevel: 0, status: 'running' });
    expect(shouldFlash(timer)).toBe(false);
  });

  it('returns false when both conditions are not met', () => {
    const timer = createTimer({ urgencyLevel: 2, status: 'paused' });
    expect(shouldFlash(timer)).toBe(false);
  });
});
