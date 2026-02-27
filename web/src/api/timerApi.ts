import type { Timer, TimerListResponse } from '../types/timer';

const BASE_URL = '/api/v1/timers';

export async function createTimer(duration: number): Promise<Timer> {
  const res = await fetch(BASE_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ duration }),
  });
  if (!res.ok) throw new Error(`Create failed: ${res.status}`);
  return res.json();
}

export async function listTimers(): Promise<TimerListResponse> {
  const res = await fetch(BASE_URL);
  if (!res.ok) throw new Error(`List failed: ${res.status}`);
  return res.json();
}

export async function getTimer(id: string): Promise<Timer> {
  const res = await fetch(`${BASE_URL}/${id}`);
  if (!res.ok) throw new Error(`Get failed: ${res.status}`);
  return res.json();
}

export async function startTimer(id: string): Promise<Timer> {
  const res = await fetch(`${BASE_URL}/${id}/start`, { method: 'POST' });
  if (!res.ok) throw new Error(`Start failed: ${res.status}`);
  return res.json();
}

export async function stopTimer(id: string): Promise<Timer> {
  const res = await fetch(`${BASE_URL}/${id}/stop`, { method: 'POST' });
  if (!res.ok) throw new Error(`Stop failed: ${res.status}`);
  return res.json();
}

export async function resetTimer(id: string): Promise<Timer> {
  const res = await fetch(`${BASE_URL}/${id}/reset`, { method: 'POST' });
  if (!res.ok) throw new Error(`Reset failed: ${res.status}`);
  return res.json();
}

export async function tickTimer(id: string): Promise<Timer> {
  const res = await fetch(`${BASE_URL}/${id}/tick`, { method: 'POST' });
  if (!res.ok) throw new Error(`Tick failed: ${res.status}`);
  return res.json();
}
