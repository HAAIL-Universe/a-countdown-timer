import { TimerStatus } from '../types/timer';

interface CharacterFaceProps {
  urgencyLevel: number;
  status: TimerStatus;
}

export function CharacterFace({ urgencyLevel, status }: CharacterFaceProps) {
  const getExpression = () => {
    if (urgencyLevel === 0) return 'happy';
    if (urgencyLevel === 1) return 'neutral';
    if (urgencyLevel === 2) return 'anxious';
    if (urgencyLevel === 3) return 'upset';
    return 'happy';
  };

  const getBackgroundColor = () => {
    if (urgencyLevel === 3) return 'bg-red-600';
    if (urgencyLevel === 2) return 'bg-yellow-500';
    if (status === 'running') return 'bg-blue-600';
    return 'bg-green-600';
  };

  const expression = getExpression();
  const bgColor = getBackgroundColor();
  const isFlashing = urgencyLevel === 3;

  return (
    <div className={`flex justify-center items-center ${isFlashing ? 'animate-pulse' : ''}`}>
      <style>{`
        @keyframes flash {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.5; }
        }
        .character-flash {
          animation: flash 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94) infinite;
        }
        .character-face {
          width: 280px;
          height: 280px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          position: relative;
          transition: background-color 0.3s ease;
        }
        .eye {
          width: 24px;
          height: 36px;
          background: #000;
          border-radius: 50%;
          position: absolute;
          top: 90px;
        }
        .eye-left {
          left: 80px;
        }
        .eye-right {
          right: 80px;
        }
        .eyebrow {
          width: 40px;
          height: 6px;
          background: #000;
          position: absolute;
          top: 70px;
          border-radius: 3px;
        }
        .eyebrow-left {
          left: 70px;
        }
        .eyebrow-right {
          right: 70px;
        }
        .mouth {
          position: absolute;
          bottom: 50px;
        }
        .mouth-happy {
          width: 80px;
          height: 40px;
          border: 6px solid #000;
          border-top: none;
          border-radius: 0 0 80px 80px;
        }
        .mouth-neutral {
          width: 60px;
          height: 8px;
          background: #000;
          border-radius: 4px;
        }
        .mouth-anxious {
          width: 60px;
          height: 8px;
          background: #000;
          border-radius: 4px;
        }
        .mouth-upset {
          width: 80px;
          height: 40px;
          border: 6px solid #000;
          border-bottom: none;
          border-radius: 80px 80px 0 0;
        }
        .eyebrow-anxious-left {
          transform: rotate(-15deg);
        }
        .eyebrow-anxious-right {
          transform: rotate(15deg);
        }
        .eyebrow-upset-left {
          transform: rotate(25deg);
        }
        .eyebrow-upset-right {
          transform: rotate(-25deg);
        }
      `}