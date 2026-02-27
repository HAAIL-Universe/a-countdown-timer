import { useState, useEffect, useRef, useCallback } from 'react';
import { Timer } from '../types/timer';
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

export function useTimer(initialDurationSeconds?: number): UseTimerReturn {
  const [timer, setTimer] = useState<Timer | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const pollingIntervalRef = useRef<NodeJS.Timeout | null>(null);

  const stopPolling = useCallback(() => {
    if (pollingIntervalRef.current) {
      clearInterval(pollingIntervalRef.current);
      pollingIntervalRef.current = null;
    }
  }, []);

  const startPolling = useCallback((timerId: string) => {
    stopPolling();
    pollingIntervalRef.current = setInterval(async () => {
      try {
        const response = await api.listTimers();
        const updated = response.items.find((t) => t.id === timerId);
        if (updated) {
          setTimer(updated);
          if (updated.status !== 'running') {
            stopPolling();
          }
        }
      } catch (err) {
        const msg = err instanceof Error ? err.message : 'Poll failed';
        setError(msg);
        stopPolling();
      }
    }, 1000);
  }, [stopPolling]);

  const createAndStart = useCallback(
    async (duration: number) => {
      setIsLoading(true);
      setError(null);
      try {
        const newTimer = await api.createTimer(duration);
        setTimer(newTimer);
        const started = await api.startTimer(newTimer.id);
        setTimer(started);
        startPolling(started.id);
      } catch (err) {
        const msg = err instanceof Error ? err.message : 'Failed to create and start timer';
        setError(msg);
        setIsLoading(false);
      }
    },
    [startPolling]
  );

  const start = useCallback(async () => {
    if (!timer) return;
    setIsLoading(true);
    setError(null);
    try {
      const updated = await api.startTimer(timer.id);
      setTimer(updated);
      startPolling(updated.id);
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Failed to start timer';
      setError(msg);
    } finally {
      setIsLoading(false);
    }
  }, [timer, startPolling]);

  const stop = useCallback(async () => {
    if (!timer) return;
    setIsLoading(true);
    setError(null);
    try {
      stopPolling();
      const updated = await api.stopTimer(timer.id);
      setTimer(updated);
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Failed to stop timer';
      setError(msg);
    } finally {
      setIsLoading(false);
    }
  }, [timer, stopPolling]);

  const reset = useCallback(async () => {
    if (!timer) return;
    setIsLoading(true);
    setError(null);
    try {
      stopPolling();
      const updated = await api.resetTimer(timer.id);
      setTimer(updated);
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Failed to reset timer';
      setError(msg);
    } finally {
      setIsLoading(false);
    }
  }, [timer, stopPolling]);

  useEffect(() => {
    return () => {
      stopPolling();
    };
  }, [stopPolling]);

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
