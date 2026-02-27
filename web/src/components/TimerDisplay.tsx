import type { Timer } from '../types/timer';
import { formatMMSS, getUrgencyColor, shouldFlash } from '../utils/urgency';

interface TimerDisplayProps {
  timer: Timer | null;
}

/**
 * Large MM:SS countdown display with monospace font.
 * Applies urgency color and flash animation at 90%+.
 */
export default function TimerDisplay({ timer }: TimerDisplayProps) {
  if (!timer) {
    return (
      <div className="text-6xl font-mono font-bold text-gray-500 mb-6">
        00:00
      </div>
    );
  }

  const remaining = Math.max(0, timer.duration - timer.elapsed_time);
  const colorClass = getUrgencyColor(timer.urgency_level);
  const flash = shouldFlash(timer) && timer.status === 'running';

  return (
    <div
      className={`text-7xl font-mono font-bold mb-6 transition-colors duration-300 ${colorClass} ${flash ? 'animate-urgency-flash' : ''}`}
      data-testid="timer-display"
    >
      {formatMMSS(remaining)}
    </div>
  );
}
