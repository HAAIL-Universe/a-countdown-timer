import { useCallback } from "react";
import { TimerStatus } from "../types/timer";

interface ControlButtonsProps {
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
  const isRunning = status === "running";
  const isPaused = status === "paused";
  const isIdle = status === "idle" || status === null;

  const handleStart = useCallback(() => {
    onStart();
  }, [onStart]);

  const handleStop = useCallback(() => {
    onStop();
  }, [onStop]);

  const handleReset = useCallback(() => {
    onReset();
  }, [onReset]);

  const startDisabled = isRunning || isLoading || isIdle;
  const stopDisabled = !isRunning || isLoading;
  const resetDisabled = isLoading;

  return (
    <div className="flex gap-3 justify-center w-full">
      {!isRunning && (
        <button
          onClick={handleStart}
          disabled={startDisabled}
          aria-label="Start countdown"
          className="px-6 py-2 bg-green-500 hover:bg-green-600 disabled:bg-gray-400 disabled:cursor-not-allowed text-white font-semibold rounded-lg transition"
        >
          {isPaused ? "Resume" : "Start"}
        </button>
      )}

      {isRunning && (
        <button
          onClick={handleStop}
          disabled={stopDisabled}
          aria-label="Stop countdown"
          className="px-6 py-2 bg-yellow-500 hover:bg-yellow-600 disabled:bg-gray-400 disabled:cursor-not-allowed text-white font-semibold rounded-lg transition"
        >
          Stop
        </button>
      )}

      <button
        onClick={handleReset}
        disabled={resetDisabled || isIdle}
        aria-label="Reset countdown"
        className="px-6 py-2 bg-red-500 hover:bg-red-600 disabled:bg-gray-400 disabled:cursor-not-allowed text-white font-semibold rounded-lg transition"
      >
        Reset
      </button>
    </div>
  );
}

export default ControlButtons;
