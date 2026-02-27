import { useMemo } from 'react';
import type { TimerStatus } from '../types/timer';

interface CharacterFaceProps {
  urgencyLevel: number;
  status: TimerStatus;
}

export function CharacterFace({ urgencyLevel, status }: CharacterFaceProps) {
  const expression = useMemo(() => {
    if (urgencyLevel === 0) return 'happy';
    if (urgencyLevel <= 1) return 'happy';
    if (urgencyLevel === 2) return 'anxious';
    return 'upset';
  }, [urgencyLevel]);

  const isCritical = urgencyLevel === 3;
  const containerClass = isCritical ? 'animate-pulse' : '';

  return (
    <div className={`flex justify-center items-center ${containerClass}`}>
      <svg
        width="200"
        height="200"
        viewBox="0 0 200 200"
        className="drop-shadow-lg"
      >
        {/* Head circle */}
        <circle cx="100" cy="100" r="90" fill="#FFD700" stroke="#333" strokeWidth="3" />

        {/* Left eye white */}
        <circle cx="75" cy="85" r="18" fill="#fff" stroke="#333" strokeWidth="2" />
        {/* Left iris */}
        <circle cx="75" cy="85" r="10" fill="#333" />

        {/* Right eye white */}
        <circle cx="125" cy="85" r="18" fill="#fff" stroke="#333" strokeWidth="2" />
        {/* Right iris */}
        <circle cx="125" cy="85" r="10" fill="#333" />

        {/* Expression-based mouth */}
        {expression === 'happy' && (
          <>
            {/* Closed happy eyes */}
            <path d="M 65 78 Q 75 88 85 78" stroke="#333" strokeWidth="3" fill="none" strokeLinecap="round" />
            <path d="M 115 78 Q 125 88 135 78" stroke="#333" strokeWidth="3" fill="none" strokeLinecap="round" />
            {/* Big smile */}
            <path d="M 70 125 Q 100 145 130 125" stroke="#333" strokeWidth="4" fill="none" strokeLinecap="round" />
          </>
        )}

        {expression === 'anxious' && (
          <>
            {/* Open anxious eyes */}
            <circle cx="75" cy="85" r="12" fill="#333" />
            <circle cx="125" cy="85" r="12" fill="#333" />
            {/* O-shaped mouth (surprised/worried) */}
            <circle cx="100" cy="135" r="12" fill="none" stroke="#333" strokeWidth="3" />
          </>
        )}

        {expression === 'upset' && (
          <>
            {/* X eyes (very upset) */}
            <path d="M 65 75 L 85 95" stroke="#333" strokeWidth="4" strokeLinecap="round" />
            <path d="M 85 75 L 65 95" stroke="#333" strokeWidth="4" strokeLinecap="round" />
            <path d="M 115 75 L 135 95" stroke="#333" strokeWidth="4" strokeLinecap="round" />
            <path d="M 135 75 L 115 95" stroke="#333" strokeWidth="4" strokeLinecap="round" />
            {/* Downward mouth (sad) */}
            <path d="M 70 140 Q 100 125 130 140" stroke="#333" strokeWidth="4" fill="none" strokeLinecap="round" />
          </>
        )}
      </svg>
    </div>
  );
}
