import { useEffect, useState } from 'react';
import type { Timer } from '../types/timer';
import { formatMMSS, getUrgencyBgClass, shouldFlash } from '../utils/urgency';

export interface TimerDisplayProps {
  timer: Timer | null;
}

export function TimerDisplay({ timer }: TimerDisplayProps) {
  const [displayTime, setDisplayTime] = useState<string>('00:00');

  useEffect(() => {
    if (timer) {
      const timeRemaining = Math.max(0, timer.duration - timer.elapsedTime);
      setDisplayTime(formatMMSS(timeRemaining));
    } else {
      setDisplayTime('00:00');
    }
  }, [timer]);

  if (!timer) {
    return (
      <div className="timer-display timer-display-idle">
        00:00
      </div>
    );
  }

  const urgencyClass = getUrgencyBgClass(timer.urgencyLevel);
  const isFlashing = shouldFlash(timer);
  const baseClass = 'timer-display transition-all duration-500';

  let colorClass = 'timer-display-idle';
  if (timer.status === 'running') {
    colorClass = 'timer-display-running';
  }
  if (timer.urgencyLevel === 2) {
    colorClass = 'timer-display-urgent';
  }
  if (timer.urgencyLevel === 3) {
    colorClass = 'timer-display-critical';
  }

  return (
    <div className={`relative inline-block ${isFlashing ? 'animate-pulse' : ''}`}>
      <div className={`${urgencyClass} ${baseClass} absolute inset-0 rounded-xl opacity-20 ${
        isFlashing ? 'animate-urgency-flash' : ''
      } pointer-events-none`} />
      <div className={`${baseClass} ${colorClass} relative z-10`}>
        {displayTime}
      </div>
    </div>
  );
}
