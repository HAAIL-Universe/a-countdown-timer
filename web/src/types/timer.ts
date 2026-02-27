export type TimerStatus = 'idle' | 'running' | 'paused' | 'complete';

export type UrgencyLevel = 0 | 1 | 2 | 3;

export interface Timer {
  id: string;
  duration: number;
  elapsedTime: number;
  status: TimerStatus;
  urgencyLevel: UrgencyLevel;
  createdAt: string;
  updatedAt: string;
}

export interface CreateTimerRequest {
  duration: number;
}

export interface TimerListResponse {
  items: Timer[];
  count: number;
}

export interface CreateTimerResponse {
  id: string;
  duration: number;
  elapsedTime: number;
  status: TimerStatus;
  urgencyLevel: UrgencyLevel;
  createdAt: string;
  updatedAt: string;
}

export interface TimerUpdateRequest {
  duration?: number;
}

export interface TimerActionResponse {
  id: string;
  duration: number;
  elapsedTime: number;
  status: TimerStatus;
  urgencyLevel: UrgencyLevel;
  createdAt: string;
  updatedAt: string;
}

export interface ApiError {
  detail: string;
  status: number;
}

export interface CharacterExpression {
  level: UrgencyLevel;
  expression: 'happy' | 'neutral' | 'anxious' | 'upset';
  description: string;
}

export interface ColorTheme {
  idle: string;
  running: string;
  urgent: string;
  critical: string;
  background: string;
}

export const URGENCY_THRESHOLDS = {
  CRITICAL: 10,
  URGENT: 30,
} as const;

export const CHARACTER_EXPRESSIONS: Record<UrgencyLevel, CharacterExpression> = {
  0: { level: 0, expression: 'happy', description: 'Idle or just started' },
  1: { level: 1, expression: 'neutral', description: 'Running normally' },
  2: { level: 2, expression: 'anxious', description: 'Urgent (≤30s)' },
  3: { level: 3, expression: 'upset', description: 'Critical (≤10s)' },
} as const;

export const COLOR_PALETTE: ColorTheme = {
  idle: '#22C55E',
  running: '#3B82F6',
  urgent: '#FBBF24',
  critical: '#EF4444',
  background: '#1F2937',
} as const;
