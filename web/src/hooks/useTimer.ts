import { useState, useCallback } from 'react';
import { Timer } from '../types/timer';
import { createTimer, startTimer, stopTimer } from '../api/timerApi';

export function useTimer() {
  const [timer, setTimer] = useState<Timer | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const createAndStart = useCallback(async (duration: number) => {
    setLoading(true);
    setError(null);
    try {
      const newTimer = await createTimer(duration);
      const runningTimer = await startTimer(newTimer.id);
      setTimer(runningTimer);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to create and start timer';
      setError(message);
    } finally {
      setLoading(false);
    }
  }, []);

  const start = useCallback(async () => {
    if (!timer) return;
    setLoading(true);
    setError(null);
    try {
      const updatedTimer = await startTimer(timer.id);
      setTimer(updatedTimer);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to start timer';
      setError(message);
    } finally {
      setLoading(false);
    }
  }, [timer]);

  const stop = useCallback(async () => {
    if (!timer) return;
    setLoading(true);
    setError(null);
    try {
      const updatedTimer = await stopTimer(timer.id);
      setTimer(updatedTimer);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to stop timer';
      setError(message);
    } finally {
      setLoading(false);
    }
  }, [timer]);

  const reset = useCallback(() => {
    if (!timer) return;
    setTimer({
      ...timer,
      elapsedTime: 0,
      status: 'idle',
      urgencyLevel: 0,
    });
  }, [timer]);

  return {
    timer,
    setTimer,
    createAndStart,
    start,
    stop,
    reset,
    loading,
    error,
  };
}
