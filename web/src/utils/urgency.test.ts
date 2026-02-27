import { describe, it, expect } from 'vitest';
import { formatMMSS, getUrgencyColor, shouldFlash } from './urgency';
import type { Timer } from '../types/timer';

function makeTimer(overrides: Partial<Timer> = {}): Timer {
  return {
    id: '00000000-0000-0000-0000-000000000001',
    duration: 100,
    elapsed_time: 0,
    status: 'running',
    urgency_level: 0,
    created_at: '2026-01-01T00:00:00Z',
    updated_at: '2026-01-01T00:00:00Z',
    ...overrides,
  };
}

describe('formatMMSS', () => {
  it('converts 0 seconds to 00:00', () => {
    expect(formatMMSS(0)).toBe('00:00');
  });

  it('converts 65 seconds to 01:05', () => {
    expect(formatMMSS(65)).toBe('01:05');
  });

  it('converts 3600 seconds to 60:00', () => {
    expect(formatMMSS(3600)).toBe('60:00');
  });

  it('handles negative values as 00:00', () => {
    expect(formatMMSS(-5)).toBe('00:00');
  });
});

describe('getUrgencyColor', () => {
  it('returns green class for level 0', () => {
    expect(getUrgencyColor(0)).toBe('text-retro-green');
  });

  it('returns blue class for level 1', () => {
    expect(getUrgencyColor(1)).toBe('text-retro-blue');
  });

  it('returns yellow class for level 2', () => {
    expect(getUrgencyColor(2)).toBe('text-retro-yellow');
  });

  it('returns red class for level 3', () => {
    expect(getUrgencyColor(3)).toBe('text-retro-red');
  });
});

describe('shouldFlash', () => {
  it('returns false when elapsed < 90% of duration', () => {
    const timer = makeTimer({ elapsed_time: 89, duration: 100 });
    expect(shouldFlash(timer)).toBe(false);
  });

  it('returns true when elapsed >= 90% of duration', () => {
    const timer = makeTimer({ elapsed_time: 90, duration: 100 });
    expect(shouldFlash(timer)).toBe(true);
  });

  it('returns true when elapsed == 100% of duration', () => {
    const timer = makeTimer({ elapsed_time: 100, duration: 100 });
    expect(shouldFlash(timer)).toBe(true);
  });

  it('returns false for zero duration', () => {
    const timer = makeTimer({ elapsed_time: 50, duration: 0 });
    expect(shouldFlash(timer)).toBe(false);
  });
});
