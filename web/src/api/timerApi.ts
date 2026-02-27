import { Timer, CreateTimerRequest, TimerListResponse, ApiResponse } from '../types/timer';

const API_BASE = 'http://localhost:8000/api/v1';

const handleResponse = async <T>(response: Response): Promise<T> => {
  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Unknown error' }));
    throw new Error(error.error || error.message || `HTTP ${response.status}`);
  }
  const data = await response.json();
  return data.data || data;
};

export async function createTimer(duration: number): Promise<Timer> {
  const response = await fetch(`${API_BASE}/timers`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ duration } as CreateTimerRequest),
  });
  return handleResponse<Timer>(response);
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
  return handleResponse<Timer>(response);
}

export async function stopTimer(id: string): Promise<Timer> {
  const response = await fetch(`${API_BASE}/timers/${id}/stop`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });
  return handleResponse<Timer>(response);
}

export async function resetTimer(id: string): Promise<Timer> {
  const response = await fetch(`${API_BASE}/timers/${id}/reset`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });
  return handleResponse<Timer>(response);
}
