import { useState, useEffect, useCallback } from 'react';
import type { Timer } from '../types/timer';
import * as timerApi from '../api/timerApi';

export function useTimer(initialDurationSeconds?: number) {
  const [timer, setTimer] = useState<Timer | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const createAndStart = useCallback(async (duration: number) => {
    setIsLoading(true);
    setError(null);
    try {
      const newTimer = await timerApi.createTimer(duration);
      setTimer(newTimer);
      const started = await timerApi.startTimer(newTimer.id);
      setTimer(started);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to create timer';
      setError(message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const start = useCallback(async () => {
    if (!timer) return;
    setIsLoading(true);
    setError(null);
    try {
      const updated = await timerApi.startTimer(timer.id);
      setTimer(updated);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to start timer';
      setError(message);
    } finally {
      setIsLoading(false);
    }
  }, [timer]);

  const stop = useCallback(async () => {
    if (!timer) return;
    setIsLoading(true);
    setError(null);
    try {
      const updated = await timerApi.stopTimer(timer.id);
      setTimer(updated);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to stop timer';
      setError(message);
    } finally {
      setIsLoading(false);
    }
  }, [timer]);

  const reset = useCallback(async () => {
    if (!timer) return;
    setIsLoading(true);
    setError(null);
    try {
      const updated = await timerApi.resetTimer(timer.id);
      setTimer(updated);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to reset timer';
      setError(message);
    } finally {
      setIsLoading(false);
    }
  }, [timer]);

  useEffect(() => {
    if (!timer || timer.status !== 'running') return;

    const intervalId = setInterval(async () => {
      try {
        const response = await timerApi.listTimers();
        const updated = response.items.find((t) => t.id === timer.id);
        if (updated) {
          setTimer(updated);
        }
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Poll failed';
        setError(message);
      }
    }, 1000);

    return () => clearInterval(intervalId);
  }, [timer?.id, timer?.status]);

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
