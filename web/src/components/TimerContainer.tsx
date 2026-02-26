import { useCallback } from 'react';
import { useTimer } from '../hooks/useTimer';
import { TimerDisplay } from './TimerDisplay';
import { CharacterFace } from './CharacterFace';
import { ControlButtons } from './ControlButtons';
import { DurationInput } from './DurationInput';

export function TimerContainer() {
  const {
    timer,
    isLoading,
    error,
    createAndStart,
    start,
    stop,
    reset,
  } = useTimer();

  const handleDurationSubmit = useCallback(
    async (seconds: number) => {
      await createAndStart(seconds);
    },
    [createAndStart]
  );

  const handleStart = useCallback(
    async () => {
      await start();
    },
    [start]
  );

  const handleStop = useCallback(
    async () => {
      await stop();
    },
    [stop]
  );

  const handleReset = useCallback(
    async () => {
      await reset();
    },
    [reset]
  );

  const hasActiveTimer = timer !== null;
  const urgencyLevel = timer?.urgencyLevel ?? 0;

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900">
      <div className="flex flex-col items-center gap-8 p-8 max-w-2xl">
        {/* Title */}
        <h1 className="text-4xl font-bold text-white">Countdown Timer</h1>

        {/* Error Display */}
        {error && (
          <div className="w-full p-4 bg-red-900 border border-red-700 rounded text-red-100 text-sm">
            {error}
          </div>
        )}

        {/* Character Face */}
        <div className="mt-4">
          <CharacterFace
            urgencyLevel={urgencyLevel}
            status={timer?.status ?? 'idle'}
          />
        </div>

        {/* Input or Timer Display */}
        <div className="w-full">
          {!hasActiveTimer ? (
            <DurationInput
              onSubmit={handleDurationSubmit}
              disabled={isLoading}
            />
          ) : (
            <>
              <div className="mb-6">
                <TimerDisplay timer={timer} />
              </div>

              <ControlButtons
                status={timer.status}
                onStart={handleStart}
                onStop={handleStop}
                onReset={handleReset}
                isLoading={isLoading}
              />
            </>
          )}
        </div>

        {/* Status Text */}
        {hasActiveTimer && (
          <p className="text-gray-400 text-sm mt-4">
            Status: <span className="text-white font-semibold">{timer.status}</span>
          </p>
        )}
      </div>
    </div>
  );
}

export default TimerContainer;
