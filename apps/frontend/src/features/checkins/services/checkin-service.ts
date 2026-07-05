import { apiGet, apiPost } from "@/lib/api-client";

export interface CheckInResponse {
  id: string;
  employee_id: string;
  organization_id: string;
  week_start: string;
  status: "draft" | "submitted" | "closed";
  submitted_at: string | null;
  priorities_count: number;
  created_at: string;
  updated_at: string;
}

export interface CheckInSubmitResponse {
  id: string;
  status: "submitted";
  submitted_at: string;
}

export function getCurrentCheckIn(): Promise<CheckInResponse> {
  return apiGet<CheckInResponse>("/api/v1/checkins/current");
}

export function createCheckIn(weekStart: string): Promise<CheckInResponse> {
  return apiPost<CheckInResponse>("/api/v1/checkins", { week_start: weekStart });
}

export function submitCheckIn(id: string): Promise<CheckInSubmitResponse> {
  return apiPost<CheckInSubmitResponse>(`/api/v1/checkins/${id}/submit`);
}
