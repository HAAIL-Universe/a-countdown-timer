import { useMemo } from 'react';
import type { Timer } from '../types/timer';
import { getUrgencyBgClass, formatMMSS, shouldFlash } from '../utils/urgency';

interface TimerDisplayProps {
  timer: Timer | null;
}

export default function TimerDisplay({ timer }: TimerDisplayProps) {
  const displayTime = useMemo(() => {
    if (!timer) return '00:00';
    const remainingSeconds = Math.max(0, timer.duration - timer.elapsedTime);
    return formatMMSS(remainingSeconds);
  }, [timer]);

  const bgClass = useMemo(() => {
    if (!timer) return 'bg-blue-500';
    return getUrgencyBgClass(timer.urgencyLevel);
  }, [timer]);

  const flashClass = useMemo(() => {
    if (!timer) return '';
    return shouldFlash(timer) ? 'animate-flash' : '';
  }, [timer]);

  return (
    <div className={`flex justify-center items-center py-8 px-4 rounded-lg transition-colors duration-300 ${bgClass} ${flashClass}`}>
      <div className="font-mono text-8xl font-bold text-white drop-shadow-lg tracking-wider">
        {displayTime}
      </div>
    </div>
  );
}
