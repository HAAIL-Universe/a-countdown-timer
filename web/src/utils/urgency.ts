import { Timer } from '../types/timer';

export function getUrgencyColor(urgencyLevel: number): string {
  if (urgencyLevel === 3) return '#ff4444';
  if (urgencyLevel === 2) return '#ffdd33';
  return '#4488ff';
}

export function getUrgencyBgClass(urgencyLevel: number): string {
  if (urgencyLevel === 3) return 'bg-red-600';
  if (urgencyLevel === 2) return 'bg-yellow-500';
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
