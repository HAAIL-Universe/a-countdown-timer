import { useState, useEffect, useCallback, useRef } from 'react';
import type { Timer, TimerState } from '../types/timer';

export function useTimer(initialDurationSeconds: number = 0) {
  const [state, setState] = useState<TimerState>({
    timer: null,
    isLoading: false,
    error: null,
  });

  const pollIntervalRef = useRef<NodeJS.Timeout | null>(null);

  const stopPolling = useCallback(() => {
    if (pollIntervalRef.current) {
      clearInterval(pollIntervalRef.current);
      pollIntervalRef.current = null;
    }
  }, []);

  const createTimer = useCallback(async (duration: number): Promise<Timer> => {
    const response = await fetch('/api/v1/timers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ duration }),
    });

    if (!response.ok) {
      throw new Error(`Failed to create timer: ${response.status}`);
    }

    return response.json() as Promise<Timer>;
  }, []);

  const startTimer = useCallback(async (timerId: string): Promise<Timer> => {
    const response = await fetch(`/api/v1/timers/${timerId}/start`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    });

    if (!response.ok) {
      throw new Error(`Failed to start timer: ${response.status}`);
    }

    return response.json() as Promise<Timer>;
  }, []);

  const stopTimer = useCallback(async (timerId: string): Promise<Timer> => {
    const response = await fetch(`/api/v1/timers/${timerId}/stop`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    });

    if (!response.ok) {
      throw new Error(`Failed to stop timer: ${response.status}`);
    }

    return response.json() as Promise<Timer>;
  }, []);

  const resetTimer = useCallback(async (timerId: string): Promise<Timer> => {
    const response = await fetch(`/api/v1/timers/${timerId}/reset`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    });

    if (!response.ok) {
      throw new Error(`Failed to reset timer: ${response.status}`);
    }

    return response.json() as Promise<Timer>;
  }, []);

  const startPolling = useCallback((timerId: string) => {
    stopPolling();

    const poll = async () => {
      try {
        const response = await fetch(`/api/v1/timers/${timerId}`, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
        });

        if (!response.ok) {
          throw new Error(`Failed to fetch timer: ${response.status}`);
        }

        const timer = await response.json() as Timer;
        setState((prev) => ({ ...prev, timer, error: null }));

        if (timer.status !== 'running') {
          stopPolling();
        }
      } catch (err) {
        const errorMsg = err instanceof Error ? err.message : 'Unknown error';
        setState((prev) => ({ ...prev, error: errorMsg }));
      }
    };

    poll();
    pollIntervalRef.current = setInterval(poll, 1000);
  }, [stopPolling]);

  useEffect(() => {
    return () => {
      stopPolling();
    };
  }, [stopPolling]);

  const createAndStart = useCallback(
    async (duration: number) => {
      setState({ timer: null, isLoading: true, error: null });
      try {
        const newTimer = await createTimer(duration);
        setState({ timer: newTimer, isLoading: false, error: null });

        if (newTimer.status === 'running') {
          startPolling(newTimer.id);
        }
      } catch (err) {
        const errorMsg = err instanceof Error ? err.message : 'Failed to create timer';
        setState({ timer: null, isLoading: false, error: errorMsg });
      }
    },
    [createTimer, startPolling]
  );

  const start = useCallback(async () => {
    if (!state.timer) return;

    setState((prev) => ({ ...prev, isLoading: true }));
    try {
      const updated = await startTimer(state.timer.id);
      setState({ timer: updated, isLoading: false, error: null });
      startPolling(updated.id);
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Failed to start timer';
      setState((prev) => ({ ...prev, isLoading: false, error: errorMsg }));
    }
  }, [state.timer, startTimer, startPolling]);

  const stop = useCallback(async () => {
    if (!state.timer) return;

    stopPolling();
    setState((prev) => ({ ...prev, isLoading: true }));
    try {
      const updated = await stopTimer(state.timer.id);
      setState({ timer: updated, isLoading: false, error: null });
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Failed to stop timer';
      setState((prev) => ({ ...prev, isLoading: false, error: errorMsg }));
    }
  }, [state.timer, stopTimer, stopPolling]);

  const reset = useCallback(async () => {
    if (!state.timer) return;

    stopPolling();
    setState((prev) => ({ ...prev, isLoading: true }));
    try {
      const updated = await resetTimer(state.timer.id);
      setState({ timer: updated, isLoading: false, error: null });
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Failed to reset timer';
      setState((prev) => ({ ...prev, isLoading: false, error: errorMsg }));
    }
  }, [state.timer, resetTimer, stopPolling]);

  return {
    timer: state.timer,
    isLoading: state.isLoading,
    error: state.error,
    createAndStart,
    start,
    stop,
    reset,
  };
}
