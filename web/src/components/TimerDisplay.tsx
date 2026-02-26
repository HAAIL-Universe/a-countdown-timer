import { useMemo } from 'react';
import { Timer } from '../types/timer';
import { formatMMSS, getUrgencyBgClass, shouldFlash } from '../utils/urgency';

interface TimerDisplayProps {
  timer: Timer | null;
}

export function TimerDisplay({ timer }: TimerDisplayProps) {
  const displayTime = useMemo(() => {
    if (!timer) return '00:00';
    const remaining = Math.max(0, timer.duration - timer.elapsedTime);
    return formatMMSS(remaining);
  }, [timer]);

  const bgClass = useMemo(() => {
    if (!timer) return 'bg-green-500';
    return getUrgencyBgClass(timer.urgencyLevel);
  }, [timer]);

  const animationClass = useMemo(() => {
    if (!timer || !shouldFlash(timer)) return '';
    return 'animate-flash';
  }, [timer]);

  return (
    <div
      className={`
        flex items-center justify-center
        w-72 h-72 rounded-full
        ${bgClass}
        transition-colors duration-300
        ${animationClass}
        shadow-lg
      `}
    >
      <span
        className="
          text-white
          font-mono
          text-7xl
          font-bold
          tracking-wider
          select-none
        "
      >
        {displayTime}
      </span>
    </div>
  );
}

export default TimerDisplay;
