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
