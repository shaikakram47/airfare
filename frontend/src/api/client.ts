import type {
  FormOptions,
  FlightInput,
  ModelMetric,
  PredictionSummary,
  TrainResponse,
} from "../types/api";

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const url = `${API_BASE}${path}`;
  const response = await fetch(url, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Request failed (${response.status})`);
  }

  return response.json() as Promise<T>;
}

export function fetchOptions(): Promise<FormOptions> {
  return request<FormOptions>("/api/options");
}

export function fetchMetrics(): Promise<ModelMetric[]> {
  return request<ModelMetric[]>("/api/metrics");
}

export function predictFare(payload: FlightInput): Promise<PredictionSummary> {
  return request<PredictionSummary>("/api/predict", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function trainModels(): Promise<TrainResponse> {
  return request<TrainResponse>("/api/train", { method: "POST" });
}

export function checkHealth(): Promise<{ status: string }> {
  return request<{ status: string }>("/api/health");
}
