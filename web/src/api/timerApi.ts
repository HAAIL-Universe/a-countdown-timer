import {
  Timer,
  TimerResponse,
  TimerListResponse,
  CreateTimerRequest,
  TimerUpdateRequest,
  ApiErrorResponse,
} from '../types/timer';

const API_BASE_URL = 'http://localhost:8000/api/v1';

interface FetchOptions extends RequestInit {
  headers?: Record<string, string>;
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error: ApiErrorResponse = await response.json();
    throw new Error(error.message || 'API request failed');
  }
  return response.json();
}

async function apiCall<T>(
  endpoint: string,
  options: FetchOptions = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  const response = await fetch(url, {
    ...options,
    headers,
  });

  return handleResponse<T>(response);
}

export async function createTimer(duration: number): Promise<Timer> {
  const payload: CreateTimerRequest = { duration };
  const response = await apiCall<TimerResponse>('/timers', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
  return response;
}

export async function listTimers(): Promise<TimerListResponse> {
  return apiCall<TimerListResponse>('/timers', {
    method: 'GET',
  });
}

export async function startTimer(id: string): Promise<Timer> {
  const response = await apiCall<TimerResponse>(`/timers/${id}/start`, {
    method: 'POST',
  });
  return response;
}

export async function stopTimer(id: string): Promise<Timer> {
  const response = await apiCall<TimerResponse>(`/timers/${id}/stop`, {
    method: 'POST',
  });
  return response;
}

export async function resetTimer(id: string): Promise<Timer> {
  const response = await apiCall<TimerResponse>(`/timers/${id}/reset`, {
    method: 'POST',
  });
  return response;
}
