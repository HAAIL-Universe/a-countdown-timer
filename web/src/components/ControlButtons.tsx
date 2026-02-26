import { useCallback } from 'react';
import { TimerStatus } from '../types/timer';

export interface ControlButtonsProps {
  status: TimerStatus | null;
  onStart: () => void;
  onStop: () => void;
  onReset: () => void;
  isLoading: boolean;
}

export function ControlButtons({
  status,
  onStart,
  onStop,
  onReset,
  isLoading,
}: ControlButtonsProps) {
  const handleStart = useCallback(() => {
    onStart();
  }, [onStart]);

  const handleStop = useCallback(() => {
    onStop();
  }, [onStop]);

  const handleReset = useCallback(() => {
    onReset();
  }, [onReset]);

  const isRunning = status === 'running';
  const isPaused = status === 'paused' || status === 'idle';
  const isActive = status !== null && status !== 'idle';

  return (
    <div className="control-buttons-container">
      {!isRunning && (
        <button
          onClick={handleStart}
          disabled={isLoading || status === null}
          className="control-btn control-btn--start"
          aria-label="Start timer"
        >
          {isPaused && status !== 'idle' ? 'Resume' : 'Start'}
        </button>
      )}

      {isRunning && (
        <button
          onClick={handleStop}
          disabled={isLoading}
          className="control-btn control-btn--stop"
          aria-label="Pause timer"
        >
          Stop
        </button>
      )}

      {isActive && (
        <button
          onClick={handleReset}
          disabled={isLoading}
          className="control-btn control-btn--reset"
          aria-label="Reset timer"
        >
          Reset
        </button>
      )}
    </div>
  );
}
