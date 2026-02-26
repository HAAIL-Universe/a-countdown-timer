import { useMemo } from 'react';
import type { TimerStatus } from '../types/timer';

export interface CharacterFaceProps {
  urgencyLevel: number;
  status: TimerStatus;
}

export default function CharacterFace({ urgencyLevel, status }: CharacterFaceProps): JSX.Element {
  const getExpression = useMemo(() => {
    if (status === 'idle' || status === 'paused' && urgencyLevel === 0) {
      return 'happy';
    }
    if (urgencyLevel >= 3) {
      return 'upset';
    }
    if (urgencyLevel === 2) {
      return 'anxious';
    }
    return 'happy';
  }, [urgencyLevel, status]);

  const getBackgroundColor = useMemo(() => {
    if (urgencyLevel >= 3) return 'bg-red-500';
    if (urgencyLevel === 2) return 'bg-yellow-400';
    if (status === 'running') return 'bg-blue-500';
    return 'bg-green-500';
  }, [urgencyLevel, status]);

  const isFlashing = urgencyLevel >= 3 && status === 'running';

  return (
    <div
      className={`flex items-center justify-center transition-colors duration-300 ${getBackgroundColor} ${
        isFlashing ? 'animate-pulse' : ''
      }`}
      style={{
        width: '320px',
        height: '320px',
        borderRadius: '50%',
        animation: isFlashing ? 'flash 0.5s infinite' : undefined,
      }}
    >
      <style>{`
        @keyframes flash {
          0%, 100% { background-color: rgb(239, 68, 68); }
          50% { background-color: rgb(220, 38, 38); }
        }
      `}</style>

      <svg
        width="280"
        height="280"
        viewBox="0 0 280 280"
        xmlns="http://www.w3.org/2000/svg"
        className="drop-shadow-lg"
      >
        {/* Face circle */}
        <circle cx="140" cy="140" r="130" fill="#FFF8DC" stroke="#333" strokeWidth="3" />

        {/* Left eye */}
        <g>
          <circle cx="100" cy="110" r="18" fill="#333" />
          {getExpression === 'upset' && (
            <>
              <line x1="85" y1="95" x2="115" y2="95" stroke="#333" strokeWidth="3" />
              <line x1="85" y1="100" x2="115" y2="100" stroke="#333" strokeWidth="3" />
            </>
          )}
          {getExpression === 'anxious' && (
            <>
              <line x1="85" y1="90" x2="115" y2="100" stroke="#333" strokeWidth="3" />
              <line x1="115" y1="90" x2="85" y2="100" stroke="#333" strokeWidth="3" />
            </>
          )}
        </g>

        {/* Right eye */}
        <g>
          <circle cx="180" cy="110" r="18" fill="#333" />
          {getExpression === 'upset' && (
            <>
              <line x1="165" y1="95" x2="195" y2="95" stroke="#333" strokeWidth="3" />
              <line x1="165" y1="100" x2="195" y2="100" stroke="#333" strokeWidth="3" />
            </>
          )}
          {getExpression === 'anxious' && (
            <>
              <line x1="165" y1="90" x2="195" y2="100" stroke="#333" strokeWidth="3" />
              <line x1="195" y1="90" x2="165" y2="100" stroke="#333" strokeWidth="3" />
            </>
          )}
        </g>

        {/* Mouth */}
        {getExpression === 'happy' && (
          <path
            d="M 100 180 Q 140 220 180 180"
            stroke="#333"
            strokeWidth="4"
            fill="none"
            strokeLinecap="round"
          />
        )}
        {getExpression === 'anxious' && (
          <path
            d="M 100 190 Q 140 175 180 190"
            stroke="#333"
            strokeWidth="4"
            fill="none"
            strokeLinecap="round"
          />
        )}
        {getExpression === 'upset' && (
          <path
            d="M 100 170 Q 140 150 180 170"
            stroke="#333"
            strokeWidth="4"
            fill="none"
            strokeLinecap="round"
          />
        )}
      </svg>
    </div>
  );
}
