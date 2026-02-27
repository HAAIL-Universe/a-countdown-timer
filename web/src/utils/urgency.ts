import type { Timer } from '../types/timer';

/**
 * Map urgency level (0-3) to a Tailwind text color class.
 * 0: green, 1: blue, 2: yellow, 3: red
 */
export function getUrgencyColor(urgencyLevel: number): string {
  switch (urgencyLevel) {
    case 0:
      return 'text-retro-green';
    case 1:
      return 'text-retro-blue';
    case 2:
      return 'text-retro-yellow';
    case 3:
      return 'text-retro-red';
    default:
      return 'text-retro-green';
  }
}

/**
 * Map urgency level to a Tailwind background color class.
 */
export function getUrgencyBgClass(urgencyLevel: number): string {
  switch (urgencyLevel) {
    case 0:
      return 'bg-retro-green';
    case 1:
      return 'bg-retro-blue';
    case 2:
      return 'bg-retro-yellow';
    case 3:
      return 'bg-retro-red';
    default:
      return 'bg-retro-green';
  }
}

/**
 * Should the timer display flash? True when elapsed >= 90% of duration.
 */
export function shouldFlash(timer: Timer): boolean {
  if (timer.duration <= 0) return false;
  return (timer.elapsed_time / timer.duration) * 100 >= 90;
}

/**
 * Format total seconds into MM:SS display.
 */
export function formatMMSS(totalSeconds: number): string {
  const clamped = Math.max(0, Math.floor(totalSeconds));
  const minutes = Math.floor(clamped / 60);
  const seconds = clamped % 60;
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}
