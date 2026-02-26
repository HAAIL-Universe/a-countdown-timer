import React from 'react';
import { Timer } from '../types/timer';
import {
  formatMMSS,
  getUrgencyColor,
  getUrgencyBgClass,
  shouldFlash,
} from '../utils/urgency';

interface TimerDisplayProps {
  timer: Timer | null;
}

export const TimerDisplay: React.FC<TimerDisplayProps> = ({ timer }) => {
  if (!timer) {
    return (
      <div className="flex items-center justify-center h-64 bg-gray-800 rounded-lg border border-gray-700">
        <p className="text-gray-400">No timer running</p>
      </div>
    );
  }

  const remaining = Math.max(0, timer.duration - timer.elapsedTime);
  const displayTime = formatMMSS(remaining);
  const colorClass = getUrgencyColor(timer.urgencyLevel);
  const bgClass = getUrgencyBgClass(timer.urgencyLevel);
  const flashClass = shouldFlash(timer) ? 'animate-flash' : '';

  return (
    <div
      className={`flex items-center justify-center p-8 rounded-lg border-2 border-gray-600 transition-colors duration-200 ${bgClass} ${flashClass}`}
    >
      <div className={`font-mono text-8xl font-bold ${colorClass} text-center`}>
        {displayTime}
      </div>
    </div>
  );
};

export default TimerDisplay;
