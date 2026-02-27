import {
  Timer,
  TimerListResponse,
  CreateTimerRequest,
  CreateTimerResponse,
  TimerActionResponse,
  ApiError,
} from '../types/timer';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api/v1';

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error: ApiError = await response.json().catch(() => ({
      detail: `HTTP ${response.status}`,
      status: response.status,
    }));
    throw error;
  }
  return response.json();
}

export async function createTimer(duration: number): Promise<Timer> {
  const payload: CreateTimerRequest = { duration };
  const response = await fetch(`${API_BASE}/timers`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  return handleResponse<CreateTimerResponse>(response) as Promise<Timer>;
}

export async function listTimers(): Promise<TimerListResponse> {
  const response = await fetch(`${API_BASE}/timers`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  });
  return handleResponse<TimerListResponse>(response);
}

export async function startTimer(id: string): Promise<Timer> {
  const response = await fetch(`${API_BASE}/timers/${id}/start`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });
  return handleResponse<TimerActionResponse>(response) as Promise<Timer>;
}

export async function stopTimer(id: string): Promise<Timer> {
  const response = await fetch(`${API_BASE}/timers/${id}/stop`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });
  return handleResponse<TimerActionResponse>(response) as Promise<Timer>;
}

export async function resetTimer(id: string): Promise<Timer> {
  const response = await fetch(`${API_BASE}/timers/${id}/reset`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });
  return handleResponse<TimerActionResponse>(response) as Promise<Timer>;
}
