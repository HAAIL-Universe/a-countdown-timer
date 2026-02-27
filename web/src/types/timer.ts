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

export interface TimerUpdateRequest {
  duration?: number;
  elapsedTime?: number;
  status?: TimerStatus;
  urgencyLevel?: number;
}

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}

export interface ApiErrorResponse {
  error: string;
  message: string;
}

export interface HealthResponse {
  status: 'ok' | 'error';
}
