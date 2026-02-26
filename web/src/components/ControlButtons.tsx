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
  const canControl = !isLoading && status !== 'complete';

  return (
    <div className="flex gap-3">
      {isRunning ? (
        <button
          onClick={handleStop}
          disabled={isLoading}
          className="px-6 py-2 bg-yellow-600 text-white font-semibold rounded hover:bg-yellow-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          aria-label="Stop timer"
        >
          Stop
        </button>
      ) : (
        <button
          onClick={handleStart}
          disabled={isLoading || status === 'complete'}
          className="px-6 py-2 bg-green-600 text-white font-semibold rounded hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          aria-label="Start timer"
        >
          Start
        </button>
      )}

      <button
        onClick={handleReset}
        disabled={isLoading}
        className="px-6 py-2 bg-red-600 text-white font-semibold rounded hover:bg-red-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        aria-label="Reset timer"
      >
        Reset
      </button>
    </div>
  );
}

export default ControlButtons;
