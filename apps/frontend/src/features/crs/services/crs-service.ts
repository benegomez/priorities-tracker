import { apiGet } from "@/lib/api-client";

export interface CRSCurrentResponse {
  score: number;
  trend: "improving" | "stable" | "declining";
  risk_level: "low" | "moderate" | "high";
  week_start: string;
  formula_version: string;
  priorities_total: number;
  priorities_completed: number;
  tasks_total: number;
  tasks_completed: number;
}

export interface CRSHistoryItem {
  week_start: string;
  score: number;
  trend: "improving" | "stable" | "declining";
  risk_level: "low" | "moderate" | "high";
}

export interface CRSHistoryResponse {
  items: CRSHistoryItem[];
}

export function getCurrentCRS(): Promise<CRSCurrentResponse> {
  return apiGet<CRSCurrentResponse>("/api/v1/crs/current");
}

export function getCRSHistory(weeks = 8): Promise<CRSHistoryResponse> {
  return apiGet<CRSHistoryResponse>(`/api/v1/crs/history?weeks=${weeks}`);
}
