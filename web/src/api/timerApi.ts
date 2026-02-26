import { Timer, CreateTimerRequest, TimerListResponse } from '../types/timer';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const API_PATH = '/api/v1/timers';

async function request<T>(method: string, path: string, body?: object): Promise<T> {
  const url = `${API_BASE}${path}`;
  const options: RequestInit = {
    method,
    headers: { 'Content-Type': 'application/json' },
  };

  if (body) {
    options.body = JSON.stringify(body);
  }

  const res = await fetch(url, options);
  if (!res.ok) {
    throw new Error(`API error: ${res.status} ${res.statusText}`);
  }

  return res.json();
}

export async function createTimer(duration: number): Promise<Timer> {
  const payload: CreateTimerRequest = { duration };
  return request<Timer>('POST', API_PATH, payload);
}

export async function listTimers(): Promise<TimerListResponse> {
  return request<TimerListResponse>('GET', API_PATH);
}

export async function startTimer(id: string): Promise<Timer> {
  return request<Timer>('POST', `${API_PATH}/${id}/start`);
}

export async function stopTimer(id: string): Promise<Timer> {
  return request<Timer>('POST', `${API_PATH}/${id}/stop`);
}

export async function resetTimer(id: string): Promise<Timer> {
  return request<Timer>('POST', `${API_PATH}/${id}/reset`);
}
