import React, { useCallback } from 'react';
import { TimerStatus } from '../types/timer';

interface ControlButtonsProps {
  status: TimerStatus | null;
  onStart: () => void;
  onStop: () => void;
  onReset: () => void;
  isLoading: boolean;
}

export const ControlButtons: React.FC<ControlButtonsProps> = ({
  status,
  onStart,
  onStop,
  onReset,
  isLoading,
}) => {
  const isRunning = status === 'running';
  const isPaused = status === 'paused';
  const isIdle = status === 'idle' || status === null;

  const handleStart = useCallback(() => {
    onStart();
  }, [onStart]);

  const handleStop = useCallback(() => {
    onStop();
  }, [onStop]);

  const handleReset = useCallback(() => {
    onReset();
  }, [onReset]);

  return (
    <div className="flex gap-4 justify-center items-center mt-8">
      {/* Start/Resume Button */}
      {(isIdle || isPaused) && (
        <button
          onClick={handleStart}
          disabled={isLoading}
          className="px-8 py-3 bg-green-500 hover:bg-green-600 disabled:bg-gray-500 text-white font-semibold rounded-lg transition-colors duration-200"
          aria-label="Start countdown timer"
        >
          {isLoading ? 'Loading...' : isPaused ? 'Resume' : 'Start'}
        </button>
      )}

      {/* Stop Button */}
      {isRunning && (
        <button
          onClick={handleStop}
          disabled={isLoading}
          className="px-8 py-3 bg-yellow-500 hover:bg-yellow-600 disabled:bg-gray-500 text-white font-semibold rounded-lg transition-colors duration-200"
          aria-label="Pause countdown timer"
        >
          Stop
        </button>
      )}

      {/* Reset Button */}
      <button
        onClick={handleReset}
        disabled={isLoading}
        className="px-8 py-3 bg-red-500 hover:bg-red-600 disabled:bg-gray-500 text-white font-semibold rounded-lg transition-colors duration-200"
        aria-label="Reset countdown timer"
      >
        Reset
      </button>
    </div>
  );
};

export default ControlButtons;
