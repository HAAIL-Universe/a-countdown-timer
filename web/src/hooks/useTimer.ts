import { useState, useEffect, useCallback } from 'react';
import { Timer } from '../types/timer';
import { resetTimer } from '../api/timerApi';

interface UseTimerReturn {
  timer: Timer | null;
  isLoading: boolean;
  error: string | null;
  createAndStart: (duration: number) => Promise<void>;
  start: () => Promise<void>;
  stop: () => Promise<void>;
  reset: () => Promise<void>;
}

export function useTimer(initialDurationSeconds?: number): UseTimerReturn {
  const [timer, setTimer] = useState<Timer | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchLatest = useCallback(async (timerId: string) => {
    try {
      const response = await fetch(`/api/timers/${timerId}`);
      if (!response.ok) throw new Error('Failed to fetch timer');
      const found = await response.json();
      setTimer(found);
      setError(null);
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Failed to fetch timer';
      setError(msg);
    }
  }, []);

  const createAndStart = useCallback(async (duration: number) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch('/api/timers', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ duration }),
      });
      if (!response.ok) throw new Error('Failed to create timer');
      const newTimer = await response.json();
      setTimer(newTimer);
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Failed to create timer';
      setError(msg);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const start = useCallback(async () => {
    if (!timer) return;
    setIsLoading(true);
    setError(null);
    try {
      setTimer(timer);
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Failed to start timer';
      setError(msg);
    } finally {
      setIsLoading(false);
    }
  }, [timer]);

  const stop = useCallback(async () => {
    if (!timer) return;
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch(`/api/timers/${timer.id}`);
      if (!response.ok) throw new Error('Failed to fetch timer');
      const updated = await response.json();
      if (updated) {
        setTimer(updated);
      }
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Failed to stop timer';
      setError(msg);
    } finally {
      setIsLoading(false);
    }
  }, [timer]);

  const reset = useCallback(async () => {
    if (!timer) return;
    setIsLoading(true);
    setError(null);
    try {
      await resetTimer(timer.id);
      const response = await fetch(`/api/timers/${timer.id}`);
      if (!response.ok) throw new Error('Failed to fetch timer');
      const updated = await response.json();
      if (updated) {
        setTimer(updated);
      }
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Failed to reset timer';
      setError(msg);
    } finally {
      setIsLoading(false);
    }
  }, [timer]);

  useEffect(() => {
    if (!timer || timer.status !== 'running') return;

    const interval = setInterval(() => {
      fetchLatest(timer.id);
    }, 1000);

    return () => clearInterval(interval);
  }, [timer, fetchLatest]);

  return {
    timer,
    isLoading,
    error,
    createAndStart,
    start,
    stop,
    reset,
  };
}
