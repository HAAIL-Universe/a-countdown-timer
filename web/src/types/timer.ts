export type TimerStatus = 'idle' | 'running' | 'paused' | 'complete';

export interface Timer {
  id: string;
  duration: number;
  elapsed_time: number;
  status: TimerStatus;
  urgency_level: number;
  created_at: string;
  updated_at: string;
}

export interface CreateTimerRequest {
  duration: number;
}

export interface TimerListResponse {
  items: Timer[];
  count: number;
}
