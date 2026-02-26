import { useMemo } from 'react';
import type { Timer } from '../types/timer';
import { formatMMSS, shouldFlash, getUrgencyColor } from '../utils/urgency';

export interface TimerDisplayProps {
  timer: Timer | null;
}

export default function TimerDisplay({ timer }: TimerDisplayProps) {
  const displayTime = useMemo(() => {
    if (!timer) return '00:00';
    const remaining = Math.max(0, timer.duration - timer.elapsedTime);
    return formatMMSS(remaining);
  }, [timer]);

  const color = useMemo(() => {
    if (!timer) return '#22C55E';
    return getUrgencyColor(timer.urgencyLevel);
  }, [timer]);

  const isFlashing = useMemo(() => {
    if (!timer) return false;
    return shouldFlash(timer);
  }, [timer]);

  return (
    <div className="timer-display-container">
      <div
        className={`timer-display ${isFlashing ? 'timer-display--flash' : ''}`}
        style={{ color }}
      >
        {displayTime}
      </div>

      <style>{`
        .timer-display-container {
          display: flex;
          justify-content: center;
          align-items: center;
          width: 100%;
          min-height: 200px;
        }

        .timer-display {
          font-family: 'Courier New', 'JetBrains Mono', monospace;
          font-size: 120px;
          font-weight: bold;
          line-height: 1;
          letter-spacing: 0.05em;
          text-align: center;
          transition: color 0.3s ease-in-out;
        }

        .timer-display--flash {
          animation: flash-animation 0.5s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }

        @keyframes flash-animation {
          0%,
          100% {
            opacity: 1;
          }
          50% {
            opacity: 0.3;
          }
        }
      `}</style>
    </div>
  );
}
