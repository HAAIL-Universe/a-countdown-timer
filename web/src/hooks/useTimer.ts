import { useState, useEffect, useRef, useCallback } from 'react';
import type { Timer } from '../types/timer';
import * as api from '../api/timerApi';

interface UseTimerReturn {
  timer: Timer | null;
  isLoading: boolean;
  error: string | null;
  createAndStart: (duration: number) => Promise<void>;
  start: () => Promise<void>;
  stop: () => Promise<void>;
  reset: () => Promise<void>;
}

export function useTimer(): UseTimerReturn {
  const [timer, setTimer] = useState<Timer | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // Tick the timer every second when it's running (advances elapsed_time on server)
  useEffect(() => {
    if (timer?.status === 'running' && timer.id) {
      pollRef.current = setInterval(async () => {
        try {
          const updated = await api.tickTimer(timer.id);
          setTimer(updated);
          if (updated.status === 'complete') {
            if (pollRef.current) clearInterval(pollRef.current);
          }
        } catch (err) {
          // Silently retry on next interval
        }
      }, 1000);
    }

    return () => {
      if (pollRef.current) {
        clearInterval(pollRef.current);
        pollRef.current = null;
      }
    };
  }, [timer?.status, timer?.id]);

  const createAndStart = useCallback(async (duration: number) => {
    setIsLoading(true);
    setError(null);
    try {
      const created = await api.createTimer(duration);
      const started = await api.startTimer(created.id);
      setTimer(started);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create timer');
    } finally {
      setIsLoading(false);
    }
  }, []);

  const start = useCallback(async () => {
    if (!timer) return;
    setIsLoading(true);
    setError(null);
    try {
      const updated = await api.startTimer(timer.id);
      setTimer(updated);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start timer');
    } finally {
      setIsLoading(false);
    }
  }, [timer]);

  const stop = useCallback(async () => {
    if (!timer) return;
    setIsLoading(true);
    setError(null);
    try {
      const updated = await api.stopTimer(timer.id);
      setTimer(updated);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to stop timer');
    } finally {
      setIsLoading(false);
    }
  }, [timer]);

  const reset = useCallback(async () => {
    if (!timer) return;
    setIsLoading(true);
    setError(null);
    try {
      const updated = await api.resetTimer(timer.id);
      setTimer(updated);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to reset timer');
    } finally {
      setIsLoading(false);
    }
  }, [timer]);

  return { timer, isLoading, error, createAndStart, start, stop, reset };
}
