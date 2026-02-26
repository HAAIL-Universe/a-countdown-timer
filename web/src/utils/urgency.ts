import { Timer } from '../types/timer';

/**
 * Compute urgency level based on remaining time.
 */
export function computeUrgencyLevel(elapsed: number, duration: number): number {
  const remaining = duration - elapsed;

  if (remaining <= 0) {
    return 3; // Complete/critical
  }
  if (remaining <= 10) {
    return 3; // Critical: ≤10s
  }
  if (remaining <= 30) {
    return 2; // Urgent: ≤30s
  }
  return 0; // Idle/normal
}

/**
 * Get Tailwind color class for timer display based on urgency level.
 */
export function getUrgencyColor(urgencyLevel: number): string {
  switch (urgencyLevel) {
    case 3:
      return 'text-red-500';
    case 2:
      return 'text-yellow-400';
    default:
      return 'text-green-400';
  }
}

/**
 * Get Tailwind background class for timer container based on urgency level.
 */
export function getUrgencyBgClass(urgencyLevel: number): string {
  switch (urgencyLevel) {
    case 3:
      return 'bg-red-900';
    case 2:
      return 'bg-yellow-900';
    default:
      return 'bg-green-900';
  }
}

/**
 * Determine if timer should flash (red critical state).
 */
export function shouldFlash(timer: Timer): boolean {
  return timer.urgencyLevel === 3 && timer.status === 'running';
}

/**
 * Format seconds as MM:SS string.
 */
export function formatMMSS(totalSeconds: number): string {
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}
