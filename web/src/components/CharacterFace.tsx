import { useMemo } from 'react';
import type { TimerStatus } from '../types/timer';

export interface CharacterFaceProps {
  urgencyLevel: number;
  status: TimerStatus;
}

export function CharacterFace({ urgencyLevel, status }: CharacterFaceProps) {
  const { expression, eyeStyle, mouthStyle } = useMemo(() => {
    if (urgencyLevel === 0) {
      return {
        expression: 'happy',
        eyeStyle: 'open',
        mouthStyle: 'smile',
      };
    }
    if (urgencyLevel <= 1) {
      return {
        expression: 'neutral',
        eyeStyle: 'open',
        mouthStyle: 'neutral',
      };
    }
    if (urgencyLevel === 2) {
      return {
        expression: 'anxious',
        eyeStyle: 'raised',
        mouthStyle: 'uncertain',
      };
    }
    return {
      expression: 'upset',
      eyeStyle: 'closed',
      mouthStyle: 'sad',
    };
  }, [urgencyLevel]);

  const colorClass = useMemo(() => {
    if (urgencyLevel === 0) return 'fill-green-500';
    if (urgencyLevel === 1) return 'fill-blue-500';
    if (urgencyLevel === 2) return 'fill-yellow-400';
    return 'fill-red-500';
  }, [urgencyLevel]);

  const isFlashing = urgencyLevel === 3;
  const animationClass = isFlashing ? 'animate-pulse' : '';

  return (
    <div className={`flex justify-center items-center ${animationClass}`}>
      <svg
        viewBox="0 0 200 200"
        width="240"
        height="240"
        className={`${colorClass} transition-all duration-300 drop-shadow-lg`}
      >
        <circle cx="100" cy="100" r="95" className="stroke-current stroke-2" fill="currentColor" />

        {eyeStyle === 'open' && (
          <>
            <circle cx="75" cy="80" r="12" className="fill-gray-900" />
            <circle cx="125" cy="80" r="12" className="fill-gray-900" />
          </>
        )}

        {eyeStyle === 'raised' && (
          <>
            <ellipse cx="75" cy="75" rx="12" ry="14" className="fill-gray-900" />
            <ellipse cx="125" cy="75" rx="12" ry="14" className="fill-gray-900" />
            <path d="M 60 70 Q 75 60 90 70" stroke="currentColor" strokeWidth="2" fill="none" />
            <path d="M 110 70 Q 125 60 140 70" stroke="currentColor" strokeWidth="2" fill="none" />
          </>
        )}

        {eyeStyle === 'closed' && (
          <>
            <path d="M 60 80 Q 75 75 90 80" stroke="gray-900" strokeWidth="3" fill="none" />
            <path d="M 110 80 Q 125 75 140 80" stroke="gray-900" strokeWidth="3" fill="none" />
          </>
        )}

        {mouthStyle === 'smile' && (
          <path d="M 70 120 Q 100 145 130 120" stroke="currentColor" strokeWidth="3" fill="none" strokeLinecap="round" />
        )}

        {mouthStyle === 'neutral' && (
          <line x1="70" y1="130" x2="130" y2="130" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
        )}

        {mouthStyle === 'uncertain' && (
          <path d="M 75 135 Q 100 120 125 135" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round" />
        )}

        {mouthStyle === 'sad' && (
          <path d="M 70 135 Q 100 115 130 135" stroke="currentColor" strokeWidth="3" fill="none" strokeLinecap="round" />
        )}
      </svg>
    </div>
  );
}

export default CharacterFace;
