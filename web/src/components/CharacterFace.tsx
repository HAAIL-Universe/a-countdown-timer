import { TimerStatus } from '../types/timer';

export interface CharacterFaceProps {
  urgencyLevel: number;
  status: TimerStatus;
}

export function CharacterFace({ urgencyLevel, status }: CharacterFaceProps) {
  const getExpression = () => {
    if (urgencyLevel === 0) return 'happy';
    if (urgencyLevel === 2) return 'anxious';
    if (urgencyLevel === 3) return 'upset';
    return 'happy';
  };

  const expression = getExpression();
  const isRunning = status === 'running';

  return (
    <div className={`flex items-center justify-center transition-all duration-300 ${
      isRunning ? 'animate-pulse' : ''
    }`}>
      <svg
        width="200"
        height="200"
        viewBox="0 0 200 200"
        className={`transition-all duration-500 ${
          expression === 'upset' ? 'animate-bounce' : ''
        }`}
      >
        {/* Face circle */}
        <circle
          cx="100"
          cy="100"
          r="90"
          fill={
            expression === 'happy'
              ? '#FFD700'
              : expression === 'anxious'
              ? '#FFA500'
              : '#FF6B6B'
          }
          stroke="#000"
          strokeWidth="3"
        />

        {/* Left eye */}
        {expression === 'happy' && (
          <>
            <circle cx="70" cy="70" r="12" fill="#000" />
            <circle cx="72" cy="68" r="4" fill="#FFF" />
          </>
        )}

        {expression === 'anxious' && (
          <>
            <ellipse cx="70" cy="70" rx="14" ry="18" fill="none" stroke="#000" strokeWidth="3" />
            <line x1="70" y1="60" x2="70" y2="80" stroke="#000" strokeWidth="2" />
            <line x1="60" y1="70" x2="80" y2="70" stroke="#000" strokeWidth="2" />
          </>
        )}

        {expression === 'upset' && (
          <>
            <line x1="55" y1="55" x2="85" y2="85" stroke="#000" strokeWidth="4" />
            <line x1="85" y1="55" x2="55" y2="85" stroke="#000" strokeWidth="4" />
          </>
        )}

        {/* Right eye */}
        {expression === 'happy' && (
          <>
            <circle cx="130" cy="70" r="12" fill="#000" />
            <circle cx="132" cy="68" r="4" fill="#FFF" />
          </>
        )}

        {expression === 'anxious' && (
          <>
            <ellipse cx="130" cy="70" rx="14" ry="18" fill="none" stroke="#000" strokeWidth="3" />
            <line x1="130" y1="60" x2="130" y2="80" stroke="#000" strokeWidth="2" />
            <line x1="120" y1="70" x2="140" y2="70" stroke="#000" strokeWidth="2" />
          </>
        )}

        {expression === 'upset' && (
          <>
            <line x1="115" y1="55" x2="145" y2="85" stroke="#000" strokeWidth="4" />
            <line x1="145" y1="55" x2="115" y2="85" stroke="#000" strokeWidth="4" />
          </>
        )}

        {/* Mouth */}
        {expression === 'happy' && (
          <path d="M 60 120 Q 100 150 140 120" stroke="#000" strokeWidth="4" fill="none" strokeLinecap="round" />
        )}

        {expression === 'anxious' && (
          <path d="M 60 130 Q 100 125 140 130" stroke="#000" strokeWidth="4" fill="none" strokeLinecap="round" />
        )}

        {expression === 'upset' && (
          <path d="M 60 140 Q 100 120 140 140" stroke="#000" strokeWidth="4" fill="none" strokeLinecap="round" />
        )}
      </svg>
    </div>
  );
}
