import React from 'react';
import { Timer } from '../types/timer';

interface ControlButtonsProps {
  timer: Timer | null;
  onStart: () => Promise<void>;
  onStop: () => Promise<void>;
  onReset: () => Promise<void>;
  isLoading?: boolean;
}

export const ControlButtons: React.FC<ControlButtonsProps> = ({
  timer,
  onStart,
  onStop,
  onReset,
  isLoading = false,
}) => {
  const isRunning = timer?.status === 'running';

  const handleStart = async () => {
    if (!isLoading) {
      await onStart();
    }
  };

  const handleStop = async () => {
    if (!isLoading) {
      await onStop();
    }
  };

  const handleReset = async () => {
    if (!isLoading) {
      await onReset();
    }
  };

  return (
    <div className="flex gap-4 mt-8">
      {!isRunning ? (
        <button
          onClick={handleStart}
          disabled={isLoading || !timer}
          className="px-6 py-3 bg-green-500 hover:bg-green-600 disabled:bg-gray-400 disabled:cursor-not-allowed text-white font-bold rounded transition-colors"
        >
          {isLoading ? 'Loading...' : 'Start'}
        </button>
      ) : (
        <button
          onClick={handleStop}
          disabled={isLoading}
          className="px-6 py-3 bg-yellow-500 hover:bg-yellow-600 disabled:bg-gray-400 disabled:cursor-not-allowed text-white font-bold rounded transition-colors"
        >
          {isLoading ? 'Loading...' : 'Stop'}
        </button>
      )}
      <button
        onClick={handleReset}
        disabled={isLoading || !timer}
        className="px-6 py-3 bg-red-500 hover:bg-red-600 disabled:bg-gray-400 disabled:cursor-not-allowed text-white font-bold rounded transition-colors"
      >
        {isLoading ? 'Loading...' : 'Reset'}
      </button>
    </div>
  );
};
