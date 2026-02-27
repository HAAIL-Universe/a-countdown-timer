import React, { useCallback } from 'react';
import { useTimer } from '../hooks/useTimer';
import DurationInput from './DurationInput';
import TimerDisplay from './TimerDisplay';
import { ControlButtons } from './ControlButtons';
import { CharacterFace } from './CharacterFace';

const TimerContainer: React.FC = () => {
  const { timer, isLoading, error, createAndStart, start, stop, reset } = useTimer();

  const handleDurationSubmit = useCallback(
    async (seconds: number) => {
      await createAndStart(seconds);
    },
    [createAndStart]
  );

  const handleStart = useCallback(async () => {
    await start();
  }, [start]);

  const handleStop = useCallback(async () => {
    await stop();
  }, [stop]);

  const handleReset = useCallback(async () => {
    await reset();
  }, [reset]);

  return (
    <div className="min-h-screen w-full bg-gray-900 flex flex-col items-center justify-center p-4">
      {/* Character Face */}
      <div className="mb-8">
        <CharacterFace
          urgencyLevel={timer?.urgencyLevel ?? 0}
          status={timer?.status ?? 'idle'}
        />
      </div>

      {/* Timer Display */}
      <div className="mb-8">
        <TimerDisplay timer={timer} />
      </div>

      {/* Error Message */}
      {error && (
        <div className="mb-6 px-4 py-3 bg-red-700 text-white rounded-lg text-sm">
          {error}
        </div>
      )}

      {/* Input and Controls */}
      <div className="flex flex-col gap-8 items-center">
        {!timer ? (
          <DurationInput onSubmit={handleDurationSubmit} disabled={isLoading} />
        ) : (
          <ControlButtons
            status={timer.status}
            onStart={handleStart}
            onStop={handleStop}
            onReset={handleReset}
            isLoading={isLoading}
          />
        )}
      </div>

      {/* Footer Info */}
      <div className="mt-12 text-center text-gray-500 text-xs">
        <p>Countdown Timer v1.0</p>
      </div>
    </div>
  );
};

export default TimerContainer;
