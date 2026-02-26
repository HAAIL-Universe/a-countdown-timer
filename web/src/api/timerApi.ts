import {
  Timer,
  CreateTimerRequest,
  TimerListResponse,
  CreateTimerResponse,
  UpdateTimerResponse,
  StartTimerResponse,
  PauseTimerResponse,
  ResetTimerResponse,
} from '../types/timer';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const API_VERSION = '/api/v1';

async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE}${API_VERSION}${endpoint}`;
  const response = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.message || `API Error: ${response.status}`);
  }

  return response.json();
}

export async function createTimer(duration: number): Promise<Timer> {
  return request<CreateTimerResponse>('/timers', {
    method: 'POST',
    body: JSON.stringify({ duration } as CreateTimerRequest),
  });
}

export async function listTimers(): Promise<TimerListResponse> {
  return request<TimerListResponse>('/timers', {
    method: 'GET',
  });
}

export async function startTimer(id: string): Promise<Timer> {
  return request<StartTimerResponse>(`/timers/${id}/start`, {
    method: 'POST',
  });
}

export async function stopTimer(id: string): Promise<Timer> {
  return request<PauseTimerResponse>(`/timers/${id}/pause`, {
    method: 'POST',
  });
}

export async function resetTimer(id: string): Promise<Timer> {
  return request<ResetTimerResponse>(`/timers/${id}/reset`, {
    method: 'POST',
  });
}
