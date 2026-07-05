import { apiGet, apiPost, apiPatch } from "@/lib/api-client";

export interface CheckOutTaskItem {
  id: string;
  title: string;
  status: string;
  completed: boolean;
}

export interface CheckOutPriorityItem {
  id: string;
  title: string;
  status: string;
  priority_level: string;
  completed: boolean;
  tasks: CheckOutTaskItem[];
}

export interface CheckOutResponse {
  id: string;
  checkin_id: string;
  employee_id: string;
  organization_id: string;
  week_start: string;
  status: "draft" | "submitted";
  submitted_at: string | null;
  notes: string | null;
  lessons_learned: string | null;
  priorities: CheckOutPriorityItem[];
  created_at: string;
  updated_at: string;
}

export interface CheckOutSummary {
  priorities_total: number;
  priorities_completed: number;
  priorities_carried: number;
  tasks_total: number;
  tasks_completed: number;
}

export interface CheckOutSubmitResponse {
  id: string;
  status: "submitted";
  submitted_at: string;
  summary: CheckOutSummary;
}

export function getCurrentCheckOut(): Promise<CheckOutResponse> {
  return apiGet<CheckOutResponse>("/api/v1/checkouts/current");
}

export function createCheckOut(checkinId: string): Promise<CheckOutResponse> {
  return apiPost<CheckOutResponse>("/api/v1/checkouts/", { checkin_id: checkinId });
}

export function markPriorityCompleted(checkoutId: string, priorityId: string, completed: boolean) {
  return apiPatch<{ priority_id: string; completed: boolean }>(
    `/api/v1/checkouts/${checkoutId}/priorities/${priorityId}`,
    { completed }
  );
}

export function markTaskCompleted(checkoutId: string, taskId: string, completed: boolean) {
  return apiPatch<{ task_id: string; completed: boolean }>(
    `/api/v1/checkouts/${checkoutId}/tasks/${taskId}`,
    { completed }
  );
}

export function submitCheckOut(id: string, data: { notes?: string | null; lessons_learned?: string | null }): Promise<CheckOutSubmitResponse> {
  return apiPost<CheckOutSubmitResponse>(`/api/v1/checkouts/${id}/submit`, data);
}
