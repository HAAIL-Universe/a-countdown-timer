import { describe, it, expect } from 'vitest';
import { formatMMSS, getUrgencyColor, getUrgencyBgClass, shouldFlash } from './urgency';
import { Timer, UrgencyLevel } from '../types/timer';

describe('formatMMSS', () => {
  it('formats 0 seconds as 00:00', () => {
    expect(formatMMSS(0)).toBe('00:00');
  });

  it('formats seconds only (less than 60)', () => {
    expect(formatMMSS(45)).toBe('00:45');
  });

  it('formats minutes and seconds', () => {
    expect(formatMMSS(125)).toBe('02:05');
  });

  it('formats single-digit seconds with leading zero', () => {
    expect(formatMMSS(61)).toBe('01:01');
  });

  it('formats single-digit minutes with leading zero', () => {
    expect(formatMMSS(9)).toBe('00:09');
  });

  it('formats large duration', () => {
    expect(formatMMSS(599)).toBe('09:59');
  });

  it('formats one minute exactly', () => {
    expect(formatMMSS(60)).toBe('01:00');
  });

  it('formats ten minutes', () => {
    expect(formatMMSS(600)).toBe('10:00');
  });
});

describe('getUrgencyColor', () => {
  it('returns idle color for urgency level 0', () => {
    const color = getUrgencyColor(0);
    expect(color).toBeTruthy();
  });

  it('returns running color for urgency level 1', () => {
    const color = getUrgencyColor(1);
    expect(color).toBeTruthy();
  });

  it('returns urgent color for urgency level 2', () => {
    const color = getUrgencyColor(2);
    expect(color).toBeTruthy();
  });

  it('returns critical color for urgency level 3', () => {
    const color = getUrgencyColor(3);
    expect(color).toBeTruthy();
  });

  it('returns running color for undefined urgency level', () => {
    const color = getUrgencyColor(1 as UrgencyLevel);
    expect(color).toBeTruthy();
  });

  it('returns different colors for different urgency levels', () => {
    const color0 = getUrgencyColor(0);
    const color1 = getUrgencyColor(1);
    const color2 = getUrgencyColor(2);
    const color3 = getUrgencyColor(3);
    expect(color0).not.toBe(color1);
    expect(color1).not.toBe(color2);
    expect(color2).not.toBe(color3);
  });
});

describe('getUrgencyBgClass', () => {
  it('returns green background for urgency level 0', () => {
    expect(getUrgencyBgClass(0)).toBe('bg-green-500');
  });

  it('returns blue background for urgency level 1', () => {
    expect(getUrgencyBgClass(1)).toBe('bg-blue-500');
  });

  it('returns yellow background for urgency level 2', () => {
    expect(getUrgencyBgClass(2)).toBe('bg-yellow-400');
  });

  it('returns red background for urgency level 3', () => {
    expect(getUrgencyBgClass(3)).toBe('bg-red-500');
  });

  it('returns blue background as default for undefined level', () => {
    expect(getUrgencyBgClass(1 as UrgencyLevel)).toBe('bg-blue-500');
  });
});

describe('shouldFlash', () => {
  it('returns true when urgencyLevel is 3', () => {
    const timer: Timer = {
      id: 'test-1',
      duration: 100,
      elapsedTime: 95,
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
      duration: 100,
      elapsedTime: 10,
      status: 'running',
      urgencyLevel: 0,
      createdAt: '2024-01-01T00:00:00Z',
      updatedAt: '2024-01-01T00:00:00Z',
    };
    expect(shouldFlash(timer)).toBe(false);
  });

  it('returns false when urgencyLevel is 1', () => {
    const timer: Timer = {
      id: 'test-3',
      duration: 100,
      elapsedTime: 50,
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
      duration: 100,
      elapsedTime: 80,
      status: 'running',
      urgencyLevel: 2,
      createdAt: '2024-01-01T00:00:00Z',
      updatedAt: '2024-01-01T00:00:00Z',
    };
    expect(shouldFlash(timer)).toBe(false);
  });

  it('returns true only at critical urgency level regardless of elapsed time', () => {
    const timerCritical: Timer = {
      id: 'test-5',
      duration: 100,
      elapsedTime: 5,
      status: 'running',
      urgencyLevel: 3,
      createdAt: '2024-01-01T00:00:00Z',
      updatedAt: '2024-01-01T00:00:00Z',
    };
    expect(shouldFlash(timerCritical)).toBe(true);
  });

  it('returns true for paused timer at critical urgency', () => {
    const timerPaused: Timer = {
      id: 'test-6',
      duration: 100,
      elapsedTime: 99,
      status: 'paused',
      urgencyLevel: 3,
      createdAt: '2024-01-01T00:00:00Z',
      updatedAt: '2024-01-01T00:00:00Z',
    };
    expect(shouldFlash(timerPaused)).toBe(true);
  });
});
