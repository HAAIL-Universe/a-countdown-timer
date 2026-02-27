import React from "react";
import type { Timer } from "../types/timer";
import { formatMMSS, getUrgencyBgClass, shouldFlash } from "../utils/urgency";

export interface TimerDisplayProps {
  timer: Timer | null;
}

export default function TimerDisplay({ timer }: TimerDisplayProps): React.ReactElement {
  if (!timer) {
    return (
      <div className="flex items-center justify-center p-8">
        <p className="text-gray-400 text-lg">No timer active</p>
      </div>
    );
  }

  const displayTime = formatMMSS(timer.elapsedTime);
  const bgClass = getUrgencyBgClass(timer.urgencyLevel);
  const flashClass = shouldFlash(timer) ? "animate-pulse" : "";

  return (
    <div className={`flex items-center justify-center p-8 transition-all duration-300 ${flashClass}`}>
      <div
        className={`${bgClass} rounded-lg px-8 py-6 shadow-2xl transition-colors duration-300`}
      >
        <div className="font-mono text-6xl font-bold text-white tracking-wider text-center">
          {displayTime}
        </div>
        <div className="text-center text-sm text-gray-200 mt-2 opacity-75">
          {timer.status === "running" ? "Running..." : timer.status === "paused" ? "Paused" : "Idle"}
        </div>
      </div>
    </div>
  );
}
