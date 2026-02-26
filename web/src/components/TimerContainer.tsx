import { useCallback } from 'react';
import { useTimer } from '../hooks/useTimer';
import { DurationInput } from './DurationInput';
import { TimerDisplay } from './TimerDisplay';
import { CharacterFace } from './CharacterFace';
import { ControlButtons } from './ControlButtons';

export function TimerContainer() {
  const { timer, isLoading, error, createAndStart, start, stop, reset } = useTimer();

  const handleDurationSubmit = useCallback(
    (seconds: number) => {
      createAndStart(seconds);
    },
    [createAndStart]
  );

  const hasActiveTimer = timer !== null;

  return (
    <div className="min-h-screen w-screen bg-gray-900 flex flex-col items-center justify-center p-4">
      {/* Header */}
      <div className="mb-8 text-center">
        <h1 className="text-4xl font-bold text-white mb-2">
          Countdown Timer
        </h1>
        <p className="text-gray-400">Set a duration and watch the urgency rise</p>
      </div>

      {/* Error display */}
      {error && (
        <div className="mb-6 px-4 py-3 bg-red-900 border border-red-700 rounded-lg text-red-200 text-sm max-w-md">
          {error}
        </div>
      )}

      {/* Main content area */}
      <div className="flex flex-col items-center gap-8">
        {/* Timer display or duration input */}
        {!hasActiveTimer ? (
          <DurationInput
            onSubmit={handleDurationSubmit}
            disabled={isLoading}
          />
        ) : (
          <>
            {/* Character face */}
            <CharacterFace
              urgencyLevel={timer.urgencyLevel}
              status={timer.status}
            />

            {/* Timer display */}
            <TimerDisplay timer={timer} />

            {/* Control buttons */}
            <ControlButtons
              status={timer.status}
              onStart={start}
              onStop={stop}
              onReset={reset}
              isLoading={isLoading}
            />
          </>
        )}
      </div>

      {/* Footer info */}
      {hasActiveTimer && timer && (
        <div className="mt-12 text-center text-gray-500 text-sm">
          <p>Status: <span className="text-white font-semibold">{timer.status}</span></p>
          <p>Elapsed: {Math.floor(timer.elapsedTime)}s / {timer.duration}s</p>
        </div>
      )}
    </div>
  );
}

export default TimerContainer;
