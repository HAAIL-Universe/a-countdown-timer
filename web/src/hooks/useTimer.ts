import { useState, useEffect, useRef } from 'react';
import { Timer } from '../types/timer';
import * as timerApi from '../api/timerApi';

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
  const pollIntervalRef = useRef<NodeJS.Timeout | null>(null);

  const clearError = () => setError(null);

  const createAndStart = async (duration: number) => {
    try {
      clearError();
      setIsLoading(true);
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
  };

  const start = async () => {
    if (!timer) return;
    try {
      clearError();
      setIsLoading(true);
      const updated = await timerApi.startTimer(timer.id);
      setTimer(updated);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to start timer';
      setError(message);
    } finally {
      setIsLoading(false);
    }
  };

  const stop = async () => {
    if (!timer) return;
    try {
      clearError();
      setIsLoading(true);
      const updated = await timerApi.stopTimer(timer.id);
      setTimer(updated);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to stop timer';
      setError(message);
    } finally {
      setIsLoading(false);
    }
  };

  const reset = async () => {
    if (!timer) return;
    try {
      clearError();
      setIsLoading(true);
      const updated = await timerApi.resetTimer(timer.id);
      setTimer(updated);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to reset timer';
      setError(message);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (!timer || timer.status !== 'running') {
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
        pollIntervalRef.current = null;
      }
      return;
    }

    pollIntervalRef.current = setInterval(async () => {
      try {
        const updated = await timerApi.listTimers();
        const found = updated.items.find((t) => t.id === timer.id);
        if (found) {
          setTimer(found);
        }
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Poll failed';
        setError(message);
      }
    }, 1000);

    return () => {
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
        pollIntervalRef.current = null;
      }
    };
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
