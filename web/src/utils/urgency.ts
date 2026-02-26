import { Timer } from '../types/timer';

export function getUrgencyColor(urgencyLevel: number): string {
  switch (urgencyLevel) {
    case 0:
      return '#22C55E';
    case 1:
      return '#3B82F6';
    case 2:
      return '#FBBF24';
    case 3:
      return '#EF4444';
    default:
      return '#1F2937';
  }
}

export function getUrgencyBgClass(urgencyLevel: number): string {
  switch (urgencyLevel) {
    case 0:
      return 'bg-green-500';
    case 1:
      return 'bg-blue-500';
    case 2:
      return 'bg-yellow-400';
    case 3:
      return 'bg-red-500';
    default:
      return 'bg-gray-800';
  }
}

export function shouldFlash(timer: Timer): boolean {
  return timer.urgencyLevel === 3;
}

export function formatMMSS(totalSeconds: number): string {
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}

export function computeUrgencyLevel(elapsedTime: number, duration: number): number {
  const remainingTime = duration - elapsedTime;

  if (remainingTime <= 0) {
    return 3;
  }
  if (remainingTime <= 10) {
    return 3;
  }
  if (remainingTime <= 30) {
    return 2;
  }
  if (remainingTime < duration) {
    return 1;
  }
  return 0;
}
