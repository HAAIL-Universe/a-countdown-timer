import type { TimerStatus } from '../types/timer';

interface CharacterFaceProps {
  urgencyLevel: number;
  status: TimerStatus;
}

/**
 * Pac-Man-style pixel art character face.
 * Expression progresses: happy (0) -> neutral (1) -> anxious (2) -> upset (3).
 */
export default function CharacterFace({ urgencyLevel, status }: CharacterFaceProps) {
  const faceColor = getFaceColor(urgencyLevel);
  const isComplete = status === 'complete';

  return (
    <div className="flex items-center justify-center mb-8" data-testid="character-face">
      <svg
        width="200"
        height="200"
        viewBox="0 0 200 200"
        className={isComplete ? 'animate-bounce' : ''}
      >
        {/* Face circle */}
        <circle cx="100" cy="100" r="90" fill={faceColor} />

        {/* Eyes */}
        {renderEyes(urgencyLevel, isComplete)}

        {/* Mouth */}
        {renderMouth(urgencyLevel, isComplete)}
      </svg>
    </div>
  );
}

function getFaceColor(urgencyLevel: number): string {
  switch (urgencyLevel) {
    case 0: return '#22C55E'; // green - happy
    case 1: return '#3B82F6'; // blue - neutral
    case 2: return '#FBBF24'; // yellow - anxious
    case 3: return '#EF4444'; // red - upset
    default: return '#22C55E';
  }
}

function renderEyes(urgencyLevel: number, isComplete: boolean) {
  if (isComplete) {
    // X eyes for complete
    return (
      <>
        <g transform="translate(65, 70)">
          <line x1="0" y1="0" x2="20" y2="20" stroke="#1F2937" strokeWidth="5" strokeLinecap="round" />
          <line x1="20" y1="0" x2="0" y2="20" stroke="#1F2937" strokeWidth="5" strokeLinecap="round" />
        </g>
        <g transform="translate(115, 70)">
          <line x1="0" y1="0" x2="20" y2="20" stroke="#1F2937" strokeWidth="5" strokeLinecap="round" />
          <line x1="20" y1="0" x2="0" y2="20" stroke="#1F2937" strokeWidth="5" strokeLinecap="round" />
        </g>
      </>
    );
  }

  if (urgencyLevel >= 3) {
    // Squinting sad eyes
    return (
      <>
        <ellipse cx="75" cy="80" rx="12" ry="6" fill="#1F2937" />
        <ellipse cx="125" cy="80" rx="12" ry="6" fill="#1F2937" />
      </>
    );
  }

  if (urgencyLevel >= 2) {
    // Wide worried eyes with raised brows
    return (
      <>
        <circle cx="75" cy="80" r="12" fill="white" />
        <circle cx="75" cy="82" r="7" fill="#1F2937" />
        <circle cx="125" cy="80" r="12" fill="white" />
        <circle cx="125" cy="82" r="7" fill="#1F2937" />
        {/* Raised eyebrows */}
        <line x1="62" y1="60" x2="88" y2="64" stroke="#1F2937" strokeWidth="4" strokeLinecap="round" />
        <line x1="138" y1="64" x2="112" y2="60" stroke="#1F2937" strokeWidth="4" strokeLinecap="round" />
      </>
    );
  }

  // Happy/neutral eyes
  return (
    <>
      <circle cx="75" cy="80" r="10" fill="white" />
      <circle cx="75" cy="80" r="6" fill="#1F2937" />
      <circle cx="125" cy="80" r="10" fill="white" />
      <circle cx="125" cy="80" r="6" fill="#1F2937" />
    </>
  );
}

function renderMouth(urgencyLevel: number, isComplete: boolean) {
  if (isComplete) {
    // Open distressed mouth
    return <ellipse cx="100" cy="135" rx="20" ry="15" fill="#1F2937" />;
  }

  if (urgencyLevel >= 3) {
    // Frown
    return (
      <path
        d="M 70 145 Q 100 125 130 145"
        fill="none"
        stroke="#1F2937"
        strokeWidth="5"
        strokeLinecap="round"
      />
    );
  }

  if (urgencyLevel >= 2) {
    // Wavy uncertain mouth
    return (
      <path
        d="M 70 135 Q 85 145 100 135 Q 115 125 130 135"
        fill="none"
        stroke="#1F2937"
        strokeWidth="4"
        strokeLinecap="round"
      />
    );
  }

  if (urgencyLevel >= 1) {
    // Straight neutral mouth
    return (
      <line x1="75" y1="135" x2="125" y2="135" stroke="#1F2937" strokeWidth="4" strokeLinecap="round" />
    );
  }

  // Big happy smile
  return (
    <path
      d="M 70 125 Q 100 160 130 125"
      fill="none"
      stroke="#1F2937"
      strokeWidth="5"
      strokeLinecap="round"
    />
  );
}
