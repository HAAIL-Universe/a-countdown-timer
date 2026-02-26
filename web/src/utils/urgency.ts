import type { Timer } from '../types/timer';

export function computeUrgencyLevel(duration: number, elapsedTime: number): number {
  if (duration <= 0) return 0;
  const timeRemaining = duration - elapsedTime;
  if (timeRemaining > 30) return 0;
  if (timeRemaining > 10) return 2;
  if (timeRemaining > 0) return 3;
  return 3;
}

export function getUrgencyColor(urgencyLevel: number): string {
  if (urgencyLevel === 0) return '#22C55E';
  if (urgencyLevel === 2) return '#FBBF24';
  if (urgencyLevel === 3) return '#EF4444';
  return '#3B82F6';
}

export function getUrgencyBgClass(urgencyLevel: number): string {
  if (urgencyLevel === 0) return 'bg-green-500';
  if (urgencyLevel === 2) return 'bg-yellow-400';
  if (urgencyLevel === 3) return 'bg-red-500';
  return 'bg-blue-500';
}

export function shouldFlash(timer: Timer): boolean {
  return timer.urgencyLevel === 3 && timer.status === 'running';
}

export function formatMMSS(totalSeconds: number): string {
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}
