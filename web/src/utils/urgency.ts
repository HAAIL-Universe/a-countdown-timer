import { Timer, UrgencyLevel, COLOR_PALETTE } from '../types/timer';

export function getUrgencyColor(urgencyLevel: UrgencyLevel): string {
  switch (urgencyLevel) {
    case 0:
      return COLOR_PALETTE.idle;
    case 1:
      return COLOR_PALETTE.running;
    case 2:
      return COLOR_PALETTE.urgent;
    case 3:
      return COLOR_PALETTE.critical;
    default:
      return COLOR_PALETTE.running;
  }
}

export function getUrgencyBgClass(urgencyLevel: UrgencyLevel): string {
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
      return 'bg-blue-500';
  }
}

export function shouldFlash(timer: Timer): boolean {
  return timer.urgencyLevel === 3;
}

export function formatMMSS(totalSeconds: number): string {
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
}
