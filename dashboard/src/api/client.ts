import type { ApiError } from "@/types/api";

const BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? "/api").replace(/\/$/, "");

export class ApiRequestError extends Error implements ApiError {
  status: number;
  detail?: unknown;
  constructor(status: number, message: string, detail?: unknown) {
    super(message);
    this.name = "ApiRequestError";
    this.status = status;
    this.detail = detail;
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const url = `${BASE_URL}${path}`;
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json", ...(init?.headers ?? {}) },
    ...init,
  });
  if (!res.ok) {
    let detail: unknown;
    try {
      detail = await res.json();
    } catch {
      detail = await res.text();
    }
    throw new ApiRequestError(res.status, `HTTP ${res.status} on ${path}`, detail);
  }
  return (await res.json()) as T;
}

export const apiGet = <T>(path: string) => request<T>(path, { method: "GET" });
export const apiPost = <T>(path: string, body?: unknown) =>
  request<T>(path, {
    method: "POST",
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });
export const apiPut = <T>(path: string, body?: unknown) =>
  request<T>(path, {
    method: "PUT",
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });
export const apiDelete = <T>(path: string) => request<T>(path, { method: "DELETE" });
