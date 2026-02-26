import { useCallback } from 'react';
import { useTimer } from '../hooks/useTimer';
import { DurationInput } from './DurationInput';
import { TimerDisplay } from './TimerDisplay';
import { CharacterFace } from './CharacterFace';
import { ControlButtons } from './ControlButtons';

export default function TimerContainer() {
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
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black flex items-center justify-center p-4">
      <div className="flex flex-col items-center justify-center gap-8 w-full max-w-2xl">
        {/* Header */}
        <h1 className="text-4xl font-bold text-white mb-4">Countdown Timer</h1>

        {/* Error display */}
        {error && (
          <div className="w-full bg-red-600 text-white px-4 py-2 rounded text-sm">
            {error}
          </div>
        )}

        {/* Character Face */}
        <div className="flex justify-center">
          <CharacterFace
            urgencyLevel={timer?.urgencyLevel ?? 0}
            status={timer?.status ?? 'idle'}
          />
        </div>

        {/* Timer Display */}
        <div className="flex justify-center">
          <TimerDisplay timer={timer} />
        </div>

        {/* Duration Input or Control Buttons */}
        {!timer || timer.status === 'idle' ? (
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

        {/* Status indicator */}
        {timer && (
          <div className="text-gray-400 text-sm mt-4">
            Status: <span className="font-mono text-gray-300">{timer.status}</span>
          </div>
        )}
      </div>
    </div>
  );
}
