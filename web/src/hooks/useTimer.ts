import { useState, useEffect, useCallback, useRef } from 'react';
import { Timer } from '../types/timer';
import * as timerApi from '../api/timerApi';

export interface UseTimerReturn {
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
  const pollIntervalRef = useRef<NodeJS.Timeout | null>(null);

  const pollTimer = useCallback(async (timerId: string) => {
    try {
      const response = await timerApi.listTimers();
      const updated = response.items.find((t) => t.id === timerId);
      if (updated) {
        setTimer(updated);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch timer');
    }
  }, []);

  useEffect(() => {
    if (!timer || timer.status !== 'running') {
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
        pollIntervalRef.current = null;
      }
      return;
    }

    pollIntervalRef.current = setInterval(() => {
      pollTimer(timer.id);
    }, 1000);

    return () => {
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
        pollIntervalRef.current = null;
      }
    };
  }, [timer, pollTimer]);

  const createAndStart = useCallback(async (duration: number) => {
    setIsLoading(true);
    setError(null);
    try {
      const newTimer = await timerApi.createTimer(duration);
      setTimer(newTimer);
      const started = await timerApi.startTimer(newTimer.id);
      setTimer(started);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create timer');
      setIsLoading(false);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const start = useCallback(async () => {
    if (!timer) {
      setError('No timer to start');
      return;
    }
    setIsLoading(true);
    setError(null);
    try {
      const started = await timerApi.startTimer(timer.id);
      setTimer(started);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start timer');
    } finally {
      setIsLoading(false);
    }
  }, [timer]);

  const stop = useCallback(async () => {
    if (!timer) {
      setError('No timer to stop');
      return;
    }
    setIsLoading(true);
    setError(null);
    try {
      const stopped = await timerApi.stopTimer(timer.id);
      setTimer(stopped);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to stop timer');
    } finally {
      setIsLoading(false);
    }
  }, [timer]);

  const reset = useCallback(async () => {
    if (!timer) {
      setError('No timer to reset');
      return;
    }
    setIsLoading(true);
    setError(null);
    try {
      const resetTimer = await timerApi.resetTimer(timer.id);
      setTimer(resetTimer);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to reset timer');
    } finally {
      setIsLoading(false);
    }
  }, [timer]);

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
