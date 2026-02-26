import { useState, useEffect, useRef, useCallback } from 'react';
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
  const pollIntervalRef = useRef<number | null>(null);

  const clearPollInterval = useCallback(() => {
    if (pollIntervalRef.current !== null) {
      clearInterval(pollIntervalRef.current);
      pollIntervalRef.current = null;
    }
  }, []);

  const startPolling = useCallback((timerId: string) => {
    clearPollInterval();
    pollIntervalRef.current = window.setInterval(async () => {
      try {
        const response = await timerApi.listTimers();
        const updatedTimer = response.items.find((t) => t.id === timerId);
        if (updatedTimer) {
          setTimer(updatedTimer);
          if (updatedTimer.status === 'complete' || updatedTimer.status === 'paused') {
            clearPollInterval();
          }
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch timer');
        clearPollInterval();
      }
    }, 1000);
  }, [clearPollInterval]);

  const createAndStart = useCallback(
    async (duration: number) => {
      setIsLoading(true);
      setError(null);
      try {
        const newTimer = await timerApi.createTimer(duration);
        setTimer(newTimer);
        if (newTimer.status === 'running') {
          startPolling(newTimer.id);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to create timer');
        setTimer(null);
      } finally {
        setIsLoading(false);
      }
    },
    [startPolling]
  );

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
      startPolling(started.id);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start timer');
    } finally {
      setIsLoading(false);
    }
  }, [timer, startPolling]);

  const stop = useCallback(async () => {
    if (!timer) {
      setError('No timer to stop');
      return;
    }
    clearPollInterval();
    setIsLoading(true);
    setError(null);
    try {
      const paused = await timerApi.stopTimer(timer.id);
      setTimer(paused);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to stop timer');
    } finally {
      setIsLoading(false);
    }
  }, [timer, clearPollInterval]);

  const reset = useCallback(async () => {
    if (!timer) {
      setError('No timer to reset');
      return;
    }
    clearPollInterval();
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
  }, [timer, clearPollInterval]);

  useEffect(() => {
    return () => {
      clearPollInterval();
    };
  }, [clearPollInterval]);

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
