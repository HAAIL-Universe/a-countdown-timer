import { describe, it, expect } from 'vitest';
import { formatMMSS, getUrgencyColor, shouldFlash } from './urgency';
import type { Timer } from '../types/timer';

describe('formatMMSS', () => {
  it('formats 0 seconds as 00:00', () => {
    expect(formatMMSS(0)).toBe('00:00');
  });

  it('formats single digit seconds as 00:0X', () => {
    expect(formatMMSS(5)).toBe('00:05');
  });

  it('formats seconds under 60 as MM:SS', () => {
    expect(formatMMSS(45)).toBe('00:45');
  });

  it('formats exactly 60 seconds as 01:00', () => {
    expect(formatMMSS(60)).toBe('01:00');
  });

  it('formats 90 seconds as 01:30', () => {
    expect(formatMMSS(90)).toBe('01:30');
  });

  it('formats 605 seconds as 10:05', () => {
    expect(formatMMSS(605)).toBe('10:05');
  });

  it('formats 3661 seconds as 61:01', () => {
    expect(formatMMSS(3661)).toBe('61:01');
  });

  it('pads both minutes and seconds with leading zeros', () => {
    expect(formatMMSS(61)).toBe('01:01');
    expect(formatMMSS(601)).toBe('10:01');
  });
});

describe('getUrgencyColor', () => {
  it('returns green hex for urgency level 0', () => {
    expect(getUrgencyColor(0)).toBe('#22C55E');
  });

  it('returns yellow hex for urgency level 2', () => {
    expect(getUrgencyColor(2)).toBe('#FBBF24');
  });

  it('returns red hex for urgency level 3', () => {
    expect(getUrgencyColor(3)).toBe('#EF4444');
  });

  it('returns blue hex for unknown urgency level', () => {
    expect(getUrgencyColor(1)).toBe('#3B82F6');
    expect(getUrgencyColor(4)).toBe('#3B82F6');
    expect(getUrgencyColor(-1)).toBe('#3B82F6');
  });

  it('returns blue hex for any unmapped level', () => {
    expect(getUrgencyColor(5)).toBe('#3B82F6');
  });
});

describe('shouldFlash', () => {
  const baseTimer: Timer = {
    id: 'test-timer',
    duration: 100,
    elapsedTime: 0,
    status: 'idle',
    urgencyLevel: 0,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  };

  it('returns true when urgencyLevel is 3 and status is running', () => {
    const timer: Timer = {
      ...baseTimer,
      urgencyLevel: 3,
      status: 'running',
    };
    expect(shouldFlash(timer)).toBe(true);
  });

  it('returns false when urgencyLevel is 3 but status is not running', () => {
    expect(
      shouldFlash({
        ...baseTimer,
        urgencyLevel: 3,
        status: 'idle',
      })
    ).toBe(false);

    expect(
      shouldFlash({
        ...baseTimer,
        urgencyLevel: 3,
        status: 'paused',
      })
    ).toBe(false);

    expect(
      shouldFlash({
        ...baseTimer,
        urgencyLevel: 3,
        status: 'complete',
      })
    ).toBe(false);
  });

  it('returns false when status is running but urgencyLevel is not 3', () => {
    expect(
      shouldFlash({
        ...baseTimer,
        urgencyLevel: 0,
        status: 'running',
      })
    ).toBe(false);

    expect(
      shouldFlash({
        ...baseTimer,
        urgencyLevel: 2,
        status: 'running',
      })
    ).toBe(false);

    expect(
      shouldFlash({
        ...baseTimer,
        urgencyLevel: 1,
        status: 'running',
      })
    ).toBe(false);
  });

  it('returns false when both conditions are false', () => {
    expect(
      shouldFlash({
        ...baseTimer,
        urgencyLevel: 0,
        status: 'idle',
      })
    ).toBe(false);
  });
});
