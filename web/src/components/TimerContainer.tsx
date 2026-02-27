import { useTimer } from '../hooks/useTimer';
import CharacterFace from './CharacterFace';
import TimerDisplay from './TimerDisplay';
import DurationInput from './DurationInput';
import ControlButtons from './ControlButtons';

/**
 * Top-level layout wrapper: full viewport, centered column, dark background.
 * Composes all sub-components into a cohesive timer experience.
 */
export default function TimerContainer() {
  const { timer, isLoading, error, createAndStart, start, stop, reset } = useTimer();

  const hasTimer = timer !== null;
  const timerStatus = timer?.status ?? 'idle';
  const urgencyLevel = timer?.urgency_level ?? 0;

  return (
    <div className="flex flex-col items-center justify-center p-8 max-w-lg mx-auto">
      <h1 className="text-2xl font-bold text-gray-300 mb-8 tracking-wider uppercase">
        Countdown Timer
      </h1>

      <CharacterFace
        urgencyLevel={urgencyLevel}
        status={timerStatus}
      />

      <TimerDisplay timer={timer} />

      {!hasTimer && (
        <DurationInput
          onSubmit={createAndStart}
          disabled={isLoading}
        />
      )}

      {hasTimer && (
        <ControlButtons
          status={timerStatus}
          onStart={start}
          onStop={stop}
          onReset={reset}
          isLoading={isLoading}
        />
      )}

      {error && (
        <div className="mt-4 px-4 py-2 bg-red-900/50 text-retro-red rounded text-sm">
          {error}
        </div>
      )}

      {timer?.status === 'complete' && (
        <div className="mt-6 text-retro-red text-xl font-bold animate-urgency-flash">
          TIME'S UP!
        </div>
      )}
    </div>
  );
}
