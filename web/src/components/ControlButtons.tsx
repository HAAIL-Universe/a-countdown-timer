import type { TimerStatus } from '../types/timer';

interface ControlButtonsProps {
  status: TimerStatus | null;
  onStart: () => void;
  onStop: () => void;
  onReset: () => void;
  isLoading: boolean;
}

/**
 * Start, Stop, and Reset buttons.
 * Shows Stop when running, Start when idle/paused.
 */
export default function ControlButtons({
  status,
  onStart,
  onStop,
  onReset,
  isLoading,
}: ControlButtonsProps) {
  if (!status) return null;

  const isRunning = status === 'running';
  const isComplete = status === 'complete';

  return (
    <div className="flex gap-4 justify-center">
      {isRunning ? (
        <button
          onClick={onStop}
          disabled={isLoading}
          className="px-6 py-3 text-lg font-bold bg-retro-yellow text-gray-900 rounded-lg hover:bg-yellow-300 transition-colors disabled:opacity-50"
        >
          STOP
        </button>
      ) : (
        <button
          onClick={onStart}
          disabled={isLoading || isComplete}
          className="px-6 py-3 text-lg font-bold bg-retro-green text-gray-900 rounded-lg hover:bg-green-400 transition-colors disabled:opacity-50"
        >
          {status === 'paused' ? 'RESUME' : 'START'}
        </button>
      )}

      <button
        onClick={onReset}
        disabled={isLoading}
        className="px-6 py-3 text-lg font-bold bg-gray-600 text-white rounded-lg hover:bg-gray-500 transition-colors disabled:opacity-50"
      >
        RESET
      </button>
    </div>
  );
}
