import { describe, it, expect } from 'vitest';
import { formatMMSS, getUrgencyColor, getUrgencyBgClass, shouldFlash } from './urgency';
import { Timer } from '../types/timer';

describe('urgency utilities', () => {
  describe('formatMMSS', () => {
    it('formats 0 seconds as 00:00', () => {
      expect(formatMMSS(0)).toBe('00:00');
    });

    it('formats single digit seconds with leading zero', () => {
      expect(formatMMSS(5)).toBe('00:05');
    });

    it('formats exactly 60 seconds as 01:00', () => {
      expect(formatMMSS(60)).toBe('01:00');
    });

    it('formats 90 seconds as 01:30', () => {
      expect(formatMMSS(90)).toBe('01:30');
    });

    it('formats 5 minutes as 05:00', () => {
      expect(formatMMSS(300)).toBe('05:00');
    });

    it('formats 5 minutes 30 seconds as 05:30', () => {
      expect(formatMMSS(330)).toBe('05:30');
    });

    it('formats 59 seconds as 00:59', () => {
      expect(formatMMSS(59)).toBe('00:59');
    });

    it('formats 1 hour (3600 seconds) as 60:00', () => {
      expect(formatMMSS(3600)).toBe('60:00');
    });

    it('handles large durations', () => {
      expect(formatMMSS(7265)).toBe('121:05');
    });
  });

  describe('getUrgencyColor', () => {
    it('returns blue (#4488ff) for urgency level 0', () => {
      expect(getUrgencyColor(0)).toBe('#4488ff');
    });

    it('returns blue (#4488ff) for urgency level 1', () => {
      expect(getUrgencyColor(1)).toBe('#4488ff');
    });

    it('returns yellow (#ffdd33) for urgency level 2', () => {
      expect(getUrgencyColor(2)).toBe('#ffdd33');
    });

    it('returns red (#ff4444) for urgency level 3', () => {
      expect(getUrgencyColor(3)).toBe('#ff4444');
    });

    it('returns red (#ff4444) for urgency level > 3', () => {
      expect(getUrgencyColor(4)).toBe('#ff4444');
    });

    it('returns red (#ff4444) for negative urgency level', () => {
      expect(getUrgencyColor(-1)).toBe('#ff4444');
    });
  });

  describe('getUrgencyBgClass', () => {
    it('returns bg-blue-500 for urgency level 0', () => {
      expect(getUrgencyBgClass(0)).toBe('bg-blue-500');
    });

    it('returns bg-blue-500 for urgency level 1', () => {
      expect(getUrgencyBgClass(1)).toBe('bg-blue-500');
    });

    it('returns bg-yellow-500 for urgency level 2', () => {
      expect(getUrgencyBgClass(2)).toBe('bg-yellow-500');
    });

    it('returns bg-red-600 for urgency level 3', () => {
      expect(getUrgencyBgClass(3)).toBe('bg-red-600');
    });

    it('returns bg-red-600 for urgency level > 3', () => {
      expect(getUrgencyBgClass(4)).toBe('bg-red-600');
    });
  });

  describe('shouldFlash', () => {
    const createTimer = (overrides: Partial<Timer> = {}): Timer => ({
      id: 'test-id',
      duration: 60,
      elapsedTime: 0,
      status: 'idle',
      urgencyLevel: 0,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      ...overrides,
    });

    it('returns false when urgency level is 0 and status is running', () => {
      const timer = createTimer({
        urgencyLevel: 0,
        status: 'running',
      });
      expect(shouldFlash(timer)).toBe(false);
    });

    it('returns false when urgency level is 2 and status is running', () => {
      const timer = createTimer({
        urgencyLevel: 2,
        status: 'running',
      });
      expect(shouldFlash(timer)).toBe(false);
    });

    it('returns true when urgency level is 3 and status is running', () => {
      const timer = createTimer({
        urgencyLevel: 3,
        status: 'running',
      });
      expect(shouldFlash(timer)).toBe(true);
    });

    it('returns false when urgency level is 3 but status is paused', () => {
      const timer = createTimer({
        urgencyLevel: 3,
        status: 'paused',
      });
      expect(shouldFlash(timer)).toBe(false);
    });

    it('returns false when urgency level is 3 but status is idle', () => {
      const timer = createTimer({
        urgencyLevel: 3,
        status: 'idle',
      });
      expect(shouldFlash(timer)).toBe(false);
    });

    it('returns false when urgency level is 3 but status is complete', () => {
      const timer = createTimer({
        urgencyLevel: 3,
        status: 'complete',
      });
      expect(shouldFlash(timer)).toBe(false);
    });

    it('returns false when urgency level is 4 and status is running', () => {
      const timer = createTimer({
        urgencyLevel: 4,
        status: 'running',
      });
      expect(shouldFlash(timer)).toBe(false);
    });
  });
});
