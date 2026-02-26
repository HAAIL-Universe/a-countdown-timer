import { describe, it, expect } from 'vitest';
import { Timer, TimerStatus } from '../types/timer';
import { getUrgencyColor, getUrgencyBgClass, shouldFlash, formatMMSS } from './urgency';

describe('formatMMSS', () => {
  it('converts 0 seconds to 00:00', () => {
    expect(formatMMSS(0)).toBe('00:00');
  });

  it('converts 59 seconds to 00:59', () => {
    expect(formatMMSS(59)).toBe('00:59');
  });

  it('converts 60 seconds to 01:00', () => {
    expect(formatMMSS(60)).toBe('01:00');
  });

  it('converts 61 seconds to 01:01', () => {
    expect(formatMMSS(61)).toBe('01:01');
  });

  it('converts 125 seconds to 02:05', () => {
    expect(formatMMSS(125)).toBe('02:05');
  });

  it('converts 599 seconds to 09:59', () => {
    expect(formatMMSS(599)).toBe('09:59');
  });

  it('converts 600 seconds to 10:00', () => {
    expect(formatMMSS(600)).toBe('10:00');
  });

  it('converts 3599 seconds to 59:59', () => {
    expect(formatMMSS(3599)).toBe('59:59');
  });

  it('converts 3600 seconds to 60:00 (one hour)', () => {
    expect(formatMMSS(3600)).toBe('60:00');
  });

  it('pads seconds with leading zero', () => {
    expect(formatMMSS(65)).toBe('01:05');
  });

  it('pads minutes with leading zero', () => {
    expect(formatMMSS(5)).toBe('00:05');
  });

  it('handles large values', () => {
    expect(formatMMSS(7325)).toBe('122:05');
  });
});

describe('getUrgencyColor', () => {
  it('returns green for urgency level 0', () => {
    expect(getUrgencyColor(0)).toBe('#22c55e');
  });

  it('returns blue for urgency level 1', () => {
    expect(getUrgencyColor(1)).toBe('#3b82f6');
  });

  it('returns yellow for urgency level 2', () => {
    expect(getUrgencyColor(2)).toBe('#eab308');
  });

  it('returns red for urgency level 3', () => {
    expect(getUrgencyColor(3)).toBe('#ef4444');
  });

  it('returns green as default for unknown urgency level', () => {
    expect(getUrgencyColor(4)).toBe('#22c55e');
  });

  it('returns green for negative urgency level', () => {
    expect(getUrgencyColor(-1)).toBe('#22c55e');
  });

  it('returns green for very high urgency level', () => {
    expect(getUrgencyColor(999)).toBe('#22c55e');
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

  it('returns bg-green-500 as default for unknown urgency level', () => {
    expect(getUrgencyBgClass(4)).toBe('bg-green-500');
  });

  it('returns bg-green-500 for negative urgency level', () => {
    expect(getUrgencyBgClass(-1)).toBe('bg-green-500');
  });
});

describe('shouldFlash', () => {
  const createMockTimer = (overrides: Partial<Timer> = {}): Timer => ({
    id: 'test-timer-1',
    duration: 300,
    elapsedTime: 0,
    status: 'idle' as TimerStatus,
    urgencyLevel: 0,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    ...overrides,
  });

  it('returns true when urgencyLevel is 3 and status is running', () => {
    const timer = createMockTimer({
      urgencyLevel: 3,
      status: 'running',
    });
    expect(shouldFlash(timer)).toBe(true);
  });

  it('returns false when urgencyLevel is 3 but status is idle', () => {
    const timer = createMockTimer({
      urgencyLevel: 3,
      status: 'idle',
    });
    expect(shouldFlash(timer)).toBe(false);
  });

  it('returns false when urgencyLevel is 3 but status is paused', () => {
    const timer = createMockTimer({
      urgencyLevel: 3,
      status: 'paused',
    });
    expect(shouldFlash(timer)).toBe(false);
  });

  it('returns false when urgencyLevel is 3 but status is complete', () => {
    const timer = createMockTimer({
      urgencyLevel: 3,
      status: 'complete',
    });
    expect(shouldFlash(timer)).toBe(false);
  });

  it('returns false when urgencyLevel is 0 and status is running', () => {
    const timer = createMockTimer({
      urgencyLevel: 0,
      status: 'running',
    });
    expect(shouldFlash(timer)).toBe(false);
  });

  it('returns false when urgencyLevel is 1 and status is running', () => {
    const timer = createMockTimer({
      urgencyLevel: 1,
      status: 'running',
    });
    expect(shouldFlash(timer)).toBe(false);
  });

  it('returns false when urgencyLevel is 2 and status is running', () => {
    const timer = createMockTimer({
      urgencyLevel: 2,
      status: 'running',
    });
    expect(shouldFlash(timer)).toBe(false);
  });

  it('returns false when urgencyLevel is lower than 3 regardless of status', () => {
    const statuses: TimerStatus[] = ['idle', 'running', 'paused', 'complete'];
    statuses.forEach((status) => {
      const timer = createMockTimer({
        urgencyLevel: 2,
        status,
      });
      expect(shouldFlash(timer)).toBe(false);
    });
  });
});
