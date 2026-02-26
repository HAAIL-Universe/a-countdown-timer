import { Timer } from '../types/timer';
import { formatMMSS, getUrgencyColor, shouldFlash } from '../utils/urgency';

interface TimerDisplayProps {
  timer: Timer | null;
}

export default function TimerDisplay({ timer }: TimerDisplayProps) {
  if (!timer) {
    return (
      <div className="text-6xl font-mono font-bold text-gray-400">
        {formatMMSS(0)}
      </div>
    );
  }

  const remaining = timer.duration - timer.elapsedTime;
  const timeString = formatMMSS(Math.max(0, remaining));
  const isFlashing = shouldFlash(timer);
  const color = getUrgencyColor(timer.urgencyLevel);

  return (
    <div
      className={`text-8xl font-mono font-bold transition-colors duration-300 ${
        isFlashing ? 'animate-pulse' : ''
      }`}
      style={{ color }}
    >
      {timeString}
    </div>
  );
}
