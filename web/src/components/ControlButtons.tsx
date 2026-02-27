import { useCallback } from "react";
import type { TimerStatus } from "../types/timer";

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

  const isRunning = status === "running";
  const canStart = !isRunning && !isLoading;
  const canStop = isRunning && !isLoading;
  const canReset = !isLoading;

  return (
    <div className="flex flex-col gap-4 w-full max-w-sm">
      <div className="flex gap-2">
        {!isRunning ? (
          <button
            onClick={handleStart}
            disabled={!canStart}
            className="flex-1 px-6 py-3 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-semibold rounded-lg transition-colors"
            aria-label="Start timer"
          >
            {isLoading ? "..." : "Start"}
          </button>
        ) : (
          <button
            onClick={handleStop}
            disabled={!canStop}
            className="flex-1 px-6 py-3 bg-yellow-600 hover:bg-yellow-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-semibold rounded-lg transition-colors"
            aria-label="Stop timer"
          >
            Stop
          </button>
        )}
      </div>

      <button
        onClick={handleReset}
        disabled={!canReset}
        className="px-6 py-3 bg-red-600 hover:bg-red-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-semibold rounded-lg transition-colors"
        aria-label="Reset timer"
      >
        Reset
      </button>
    </div>
  );
}
