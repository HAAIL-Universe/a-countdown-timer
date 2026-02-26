import { useCallback } from "react";
import { TimerStatus } from "../types/timer";

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
  const isPaused = status === "paused";
  const isIdle = status === "idle" || status === null;

  const startButtonDisabled = isLoading || isRunning;
  const stopButtonDisabled = isLoading || (!isRunning && !isPaused);
  const resetButtonDisabled = isLoading || isIdle;

  return (
    <div className="flex flex-col items-center gap-4">
      <div className="flex gap-3 justify-center flex-wrap">
        {!isRunning && (
          <button
            onClick={handleStart}
            disabled={startButtonDisabled}
            aria-label={isPaused ? "Resume timer" : "Start timer"}
            className="px-6 py-3 font-semibold text-white bg-green-600 rounded hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 focus:ring-offset-gray-900 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isPaused ? "Resume" : "Start"}
          </button>
        )}

        {isRunning && (
          <button
            onClick={handleStop}
            disabled={stopButtonDisabled}
            aria-label="Pause timer"
            className="px-6 py-3 font-semibold text-white bg-yellow-600 rounded hover:bg-yellow-700 focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:ring-offset-2 focus:ring-offset-gray-900 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Stop
          </button>
        )}

        <button
          onClick={handleReset}
          disabled={resetButtonDisabled}
          aria-label="Reset timer"
          className="px-6 py-3 font-semibold text-white bg-red-600 rounded hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 focus:ring-offset-gray-900 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          Reset
        </button>
      </div>
    </div>
  );
}
