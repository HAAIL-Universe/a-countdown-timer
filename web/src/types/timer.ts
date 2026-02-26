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

export interface TimerUpdateRequest {
  duration?: number;
  elapsedTime?: number;
  status?: TimerStatus;
  urgencyLevel?: number;
}

export interface TimerResponse {
  id: string;
  duration: number;
  elapsedTime: number;
  status: TimerStatus;
  urgencyLevel: number;
  createdAt: string;
  updatedAt: string;
}

export interface TimerListResponse {
  items: Timer[];
  count: number;
}

export type UrgencyLevel = 0 | 1 | 2 | 3;

export interface TimerState {
  timer: Timer | null;
  isLoading: boolean;
  error: string | null;
}
