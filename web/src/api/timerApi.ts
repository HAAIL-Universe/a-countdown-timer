import type { Timer, CreateTimerRequest, TimerListResponse } from '../types/timer';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

async function request<T>(method: string, path: string, body?: unknown): Promise<T> {
  const url = `${API_BASE_URL}${path}`;
  const options: RequestInit = {
    method,
    headers: { 'Content-Type': 'application/json' },
  };
  if (body) {
    options.body = JSON.stringify(body);
  }
  const response = await fetch(url, options);
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(`API error: ${response.status} ${error.message || response.statusText}`);
  }
  return response.json();
}

export async function createTimer(duration: number): Promise<Timer> {
  const payload: CreateTimerRequest = { duration };
  return request<Timer>('POST', '/api/v1/timers', payload);
}

export async function listTimers(): Promise<TimerListResponse> {
  return request<TimerListResponse>('GET', '/api/v1/timers');
}

export async function startTimer(id: string): Promise<Timer> {
  return request<Timer>('POST', `/api/v1/timers/${id}/start`);
}

export async function stopTimer(id: string): Promise<Timer> {
  return request<Timer>('POST', `/api/v1/timers/${id}/stop`);
}

export async function resetTimer(id: string): Promise<Timer> {
  return request<Timer>('POST', `/api/v1/timers/${id}/reset`);
}
