import type { Timer, CreateTimerRequest, TimerListResponse } from '../types/timer';

const API_BASE = '/api/v1';

const apiCall = async <T>(
  method: string,
  path: string,
  body?: unknown
): Promise<T> => {
  const options: RequestInit = {
    method,
    headers: { 'Content-Type': 'application/json' },
  };

  if (body) {
    options.body = JSON.stringify(body);
  }

  const response = await fetch(`${API_BASE}${path}`, options);

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.message || `API error: ${response.status}`);
  }

  return response.json() as Promise<T>;
};

export async function createTimer(duration: number): Promise<Timer> {
  const payload: CreateTimerRequest = { duration };
  return apiCall('POST', '/timers', payload);
}

export async function listTimers(): Promise<TimerListResponse> {
  return apiCall('GET', '/timers');
}

export async function startTimer(id: string): Promise<Timer> {
  return apiCall('POST', `/timers/${id}/start`, {});
}

export async function stopTimer(id: string): Promise<Timer> {
  return apiCall('POST', `/timers/${id}/stop`, {});
}

export async function resetTimer(id: string): Promise<Timer> {
  return apiCall('POST', `/timers/${id}/reset`, {});
}
