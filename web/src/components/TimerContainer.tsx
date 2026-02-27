import { useState } from 'react';
import { useTimer } from '../hooks/useTimer';
import { CharacterFace } from './CharacterFace';
import TimerDisplay from './TimerDisplay';
import DurationInput from './DurationInput';

export default function TimerContainer() {
  const [durationInput, setDurationInput] = useState<number>(300);
  const { timer, isLoading, error, createAndStart, start, stop, reset } = useTimer();

  const handleDurationSubmit = async (seconds: number) => {
    setDurationInput(seconds);
    await createAndStart(seconds);
  };

  const urgencyLevel = timer?.urgencyLevel ?? 0;
  const status = timer?.status ?? 'idle';

  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="bg-gray-800 rounded-2xl shadow-2xl p-8 space-y-8">
          {/* Header */}
          <div className="text-center">
            <h1 className="text-4xl font-bold text-white mb-2">
              Countdown Timer
            </h1>
            <p className="text-gray-400 text-sm">
              Stay focused with visual urgency cues
            </p>
          </div>

          {/* Error Display */}
          {error && (
            <div className="bg-red-900 border border-red-700 rounded-lg p-4 text-red-100 text-sm">
              {error}
            </div>
          )}

          {/* Character Face */}
          <div className="flex justify-center">
            <CharacterFace urgencyLevel={urgencyLevel} status={status} />
          </div>

          {/* Timer Display */}
          <TimerDisplay timer={timer} />

          {/* Duration Input & Control Buttons */}
          <div className="space-y-4">
            {!timer || status === 'idle' ? (
              <DurationInput
                onSubmit={handleDurationSubmit}
                disabled={isLoading}
              />
            ) : (
              <div className="flex gap-2">
                {status === 'running' && (
                  <button
                    onClick={stop}
                    disabled={isLoading}
                    className="flex-1 bg-yellow-600 hover:bg-yellow-700 disabled:bg-gray-600 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
                  >
                    {isLoading ? 'Loading...' : 'Pause'}
                  </button>
                )}
                {status === 'paused' && (
                  <button
                    onClick={start}
                    disabled={isLoading}
                    className="flex-1 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
                  >
                    {isLoading ? 'Loading...' : 'Resume'}
                  </button>
                )}
                <button
                  onClick={reset}
                  disabled={isLoading}
                  className="flex-1 bg-red-600 hover:bg-red-700 disabled:bg-gray-600 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
                >
                  {isLoading ? 'Loading...' : 'Reset'}
                </button>
              </div>
            )}
          </div>

          {/* Status Indicator */}
          {timer && (
            <div className="text-center text-xs text-gray-500 uppercase tracking-wide">
              Status: {status}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
