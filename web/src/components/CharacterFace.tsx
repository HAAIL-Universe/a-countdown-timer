import React, { useMemo } from "react";
import type { TimerStatus, UrgencyLevel } from "../types/timer";

export interface CharacterFaceProps {
  urgencyLevel: UrgencyLevel;
  status: TimerStatus;
}

export const CharacterFace: React.FC<CharacterFaceProps> = ({
  urgencyLevel,
  status,
}) => {
  const faceState = useMemo(() => {
    if (status === "idle") {
      return { expression: "happy", color: "#22C55E", scale: 1 };
    }
    if (status === "complete") {
      return { expression: "upset", color: "#EF4444", scale: 1 };
    }
    switch (urgencyLevel) {
      case 0:
        return { expression: "happy", color: "#22C55E", scale: 1 };
      case 1:
        return { expression: "neutral", color: "#3B82F6", scale: 1 };
      case 2:
        return { expression: "anxious", color: "#FBBF24", scale: 1.05 };
      case 3:
        return { expression: "upset", color: "#EF4444", scale: 1.1 };
      default:
        return { expression: "happy", color: "#22C55E", scale: 1 };
    }
  }, [urgencyLevel, status]);

  const eyeState = useMemo(() => {
    switch (faceState.expression) {
      case "happy":
        return { eyeType: "happy" };
      case "neutral":
        return { eyeType: "neutral" };
      case "anxious":
        return { eyeType: "worried" };
      case "upset":
        return { eyeType: "closed" };
      default:
        return { eyeType: "happy" };
    }
  }, [faceState.expression]);

  const mouthState = useMemo(() => {
    switch (faceState.expression) {
      case "happy":
        return { mouthType: "smile", points: "10,35 50,50 90,35" };
      case "neutral":
        return { mouthType: "straight", points: "15,40 85,40" };
      case "anxious":
        return { mouthType: "frown", points: "10,45 50,30 90,45" };
      case "upset":
        return { mouthType: "sad", points: "15,50 50,35 85,50" };
      default:
        return { mouthType: "smile", points: "10,35 50,50 90,35" };
    }
  }, [faceState.expression]);

  const flashAnimation = urgencyLevel === 3 ? "animate-pulse" : "";

  return (
    <div
      className={`flex items-center justify-center transition-all duration-300 ${flashAnimation}`}
      style={{ transform: `scale(${faceState.scale})` }}
    >
      <svg
        width="200"
        height="200"
        viewBox="0 0 200 200"
        className="drop-shadow-lg"
      >
        {/* Face circle */}
        <circle
          cx="100"
          cy="100"
          r="90"
          fill={faceState.color}
          stroke="#000"
          strokeWidth="3"
        />

        {/* Left eye */}
        {eyeState.eyeType === "happy" && (
          <g>
            <circle cx="70" cy="80" r="12" fill="#000" />
            <path d="M 58 92 Q 70 100 82 92" stroke="#000" strokeWidth="3" fill="none" />
          </g>
        )}
        {eyeState.eyeType === "neutral" && (
          <g>
            <circle cx="70" cy="80" r="12" fill="#000" />
            <line x1="60" y1="95" x2="80" y2="95" stroke="#000" strokeWidth="3" />
          </g>
        )}
        {eyeState.eyeType === "worried" && (
          <g>
            <circle cx="70" cy="75" r="12" fill="#000" />
            <path d="M 60 90 Q 70 100 80 90" stroke="#000" strokeWidth="3" fill="none" />
          </g>
        )}
        {eyeState.eyeType === "closed" && (
          <line x1="58" y1="82" x2="82" y2="82" stroke="#000" strokeWidth="4" />
        )}

        {/* Right eye */}
        {eyeState.eyeType === "happy" && (
          <g>
            <circle cx="130" cy="80" r="12" fill="#000" />
            <path d="M 118 92 Q 130 100 142 92" stroke="#000" strokeWidth="3" fill="none" />
          </g>
        )}
        {eyeState.eyeType === "neutral" && (
          <g>
            <circle cx="130" cy="80" r="12" fill="#000" />
            <line x1="120" y1="95" x2="140" y2="95" stroke="#000" strokeWidth="3" />
          </g>
        )}
        {eyeState.eyeType === "worried" && (
          <g>
            <circle cx="130" cy="75" r="12" fill="#000" />
            <path d="M 120 90 Q 130 100 140 90" stroke="#000" strokeWidth="3" fill="none" />
          </g>
        )}
        {eyeState.eyeType === "closed" && (
          <line x1="118" y1="82" x2="142" y2="82" stroke="#000" strokeWidth="4" />
        )}

        {/* Mouth */}
        <polyline
          points={mouthState.points}
          stroke="#000"
          strokeWidth="4"
          fill="none"
          strokeLinecap="round"
          strokeLinejoin="round"
        />

        {/* Blush for anxious state */}
        {faceState.expression === "anxious" && (
          <>
            <ellipse cx="40" cy="110" rx="10" ry="15" fill="#FF6B9D" opacity="0.4" />
            <ellipse cx="160" cy="110" rx="10" ry="15" fill="#FF6B9D" opacity="0.4" />
          </>
        )}

        {/* Tears for upset state */}
        {faceState.expression === "upset" && (
          <>
            <line x1="70" y1="95" x2="70" y2="115" stroke="#6BA3FF" strokeWidth="3" />
            <circle cx="70" cy="120" r="3" fill="#6BA3FF" />
            <line x1="130" y1="95" x2="130" y2="115" stroke="#6BA3FF" strokeWidth="3" />
            <circle cx="130" cy="120" r="3" fill="#6BA3FF" />
          </>
        )}
      </svg>
    </div>
  );
};

export default CharacterFace;
