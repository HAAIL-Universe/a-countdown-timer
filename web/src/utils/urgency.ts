import { Timer } from '../types/timer';

export function getUrgencyColor(urgencyLevel: number): string {
  switch (urgencyLevel) {
    case 0:
      return '#22c55e';
    case 1:
      return '#3b82f6';
    case 2:
      return '#eab308';
    case 3:
      return '#ef4444';
    default:
      return '#22c55e';
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
      return 'bg-green-500';
  }
}

export function shouldFlash(timer: Timer): boolean {
  return timer.urgencyLevel === 3 && timer.status === 'running';
}

export function formatMMSS(totalSeconds: number): string {
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}
