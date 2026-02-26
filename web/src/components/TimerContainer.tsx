import React from 'react';
import { useTimer } from '../hooks/useTimer';
import { DurationInput } from './DurationInput';
import { TimerDisplay } from './TimerDisplay';
import { CharacterFace } from './CharacterFace';
import { ControlButtons } from './ControlButtons';
import { computeUrgencyLevel } from '../utils/urgency';

interface TimerContainerProps {}

export function TimerContainer({}: TimerContainerProps) {
  const { timer, isLoading, error, createAndStart, start, stop, reset } =
    useTimer();

  const handleDurationSubmit = async (seconds: number) => {
    await createAndStart(seconds);
  };

  const urgencyLevel = timer
    ? computeUrgencyLevel(timer.elapsedTime, timer.duration)
    : 0;

  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center p-4">
      <div className="w-full max-w-2xl">
        <div className="flex flex-col gap-12">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-white mb-2">
              Countdown Timer
            </h1>
            <p className="text-gray-400">
              Set a duration and watch the character react to urgency
            </p>
          </div>

          {error && (
            <div className="bg-red-900 border border-red-700 rounded-lg p-4 text-red-200">
              {error}
            </div>
          )}

          {!timer ? (
            <div className="bg-gray-800 rounded-lg p-8 border border-gray-700">
              <DurationInput
                onSubmit={handleDurationSubmit}
                disabled={isLoading}
              />
            </div>
          ) : (
            <>
              <CharacterFace urgencyLevel={urgencyLevel} status={timer.status} />

              <TimerDisplay timer={timer} />

              <ControlButtons
                status={timer.status}
                onStart={start}
                onStop={stop}
                onReset={reset}
                isLoading={isLoading}
              />
            </>
          )}

          {timer && (
            <div className="text-center text-sm text-gray-500">
              <p>
                {timer.status === 'running'
                  ? 'Timer is counting down...'
                  : timer.status === 'paused'
                    ? 'Timer is paused'
                    : 'Timer ready to start'}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default TimerContainer;
