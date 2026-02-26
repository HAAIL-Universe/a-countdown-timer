import { TimerStatus } from "../types/timer";

interface CharacterFaceProps {
  urgencyLevel: number;
  status: TimerStatus;
}

export function CharacterFace({
  urgencyLevel,
  status,
}: CharacterFaceProps) {
  const getExpression = () => {
    if (urgencyLevel === 0 || status === "idle") return "happy";
    if (urgencyLevel === 3) return "upset";
    if (urgencyLevel >= 2) return "anxious";
    return "happy";
  };

  const expression = getExpression();

  return (
    <div className="flex justify-center items-center py-6">
      <svg
        width="120"
        height="120"
        viewBox="0 0 120 120"
        className="drop-shadow-lg"
      >
        {/* Face circle */}
        <circle
          cx="60"
          cy="60"
          r="50"
          fill="#FFD700"
          stroke="#000"
          strokeWidth="2"
        />

        {/* Left Eye */}
        {expression === "happy" && (
          <>
            <circle
              cx="40"
              cy="45"
              r="8"
              fill="#000"
            />
            <circle
              cx="40"
              cy="45"
              r="3"
              fill="#FFF"
            />
          </>
        )}
        {expression === "anxious" && (
          <>
            <ellipse
              cx="40"
              cy="40"
              rx="7"
              ry="10"
              fill="#000"
            />
            <circle
              cx="40"
              cy="37"
              r="2"
              fill="#FFF"
            />
          </>
        )}
        {expression === "upset" && (
          <>
            <ellipse
              cx="40"
              cy="45"
              rx="8"
              ry="4"
              fill="#000"
              transform="rotate(-15 40 45)"
            />
            <ellipse
              cx="40"
              cy="43"
              rx="2"
              ry="1"
              fill="#FFF"
              transform="rotate(-15 40 43)"
            />
          </>
        )}

        {/* Right Eye */}
        {expression === "happy" && (
          <>
            <circle
              cx="80"
              cy="45"
              r="8"
              fill="#000"
            />
            <circle
              cx="80"
              cy="45"
              r="3"
              fill="#FFF"
            />
          </>
        )}
        {expression === "anxious" && (
          <>
            <ellipse
              cx="80"
              cy="40"
              rx="7"
              ry="10"
              fill="#000"
            />
            <circle
              cx="80"
              cy="37"
              r="2"
              fill="#FFF"
            />
          </>
        )}
        {expression === "upset" && (
          <>
            <ellipse
              cx="80"
              cy="45"
              rx="8"
              ry="4"
              fill="#000"
              transform="rotate(15 80 45)"
            />
            <ellipse
              cx="80"
              cy="43"
              rx="2"
              ry="1"
              fill="#FFF"
              transform="rotate(15 80 43)"
            />
          </>
        )}

        {/* Mouth */}
        {expression === "happy" && (
          <path
            d="M 45 75 Q 60 85 75 75"
            stroke="#000"
            strokeWidth="3"
            fill="none"
            strokeLinecap="round"
          />
        )}
        {expression === "anxious" && (
          <path
            d="M 45 80 L 60 70 L 75 80"
            stroke="#000"
            strokeWidth="3"
            fill="none"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        )}
        {expression === "upset" && (
          <path
            d="M 45 70 Q 60 60 75 70"
            stroke="#000"
            strokeWidth="3"
            fill="none"
            strokeLinecap="round"
          />
        )}
      </svg>

      {/* Status indicator text */}
      <div className="ml-4 text-center">
        <p className="text-sm font-semibold text-gray-700">
          {expression === "happy" && "Ready!"}
          {expression === "anxious" && "Hurrying..."}
          {expression === "upset" && "Critical!"}
        </p>
        <p className="text-xs text-gray-500 mt-1">
          Level: {urgencyLevel}
        </p>
      </div>
    </div>
  );
}

export default CharacterFace;
