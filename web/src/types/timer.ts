export type TimerStatus = 'idle' | 'running' | 'paused' | 'complete';

export interface Timer {
  id: string;
  duration: number;
  elapsedTime: number;
  status: TimerStatus;
  urgencyLevel: number;
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

export interface TimerResponse extends Timer {}

export interface CreateTimerResponse extends Timer {}

export interface UpdateTimerRequest {
  duration?: number;
  elapsedTime?: number;
  status?: TimerStatus;
}

export interface UpdateTimerResponse extends Timer {}

export interface StartTimerResponse extends Timer {}

export interface PauseTimerResponse extends Timer {}

export interface ResetTimerResponse extends Timer {}
