import { apiPost } from "@/lib/api-client";
import type { CreatePriorityValues } from "../schemas/priority-schema";
import type { CreateTaskValues } from "../schemas/task-schema";

export interface PriorityResponse {
  id: string;
  checkin_id: string;
  phase_id: string;
  owner_id: string;
  organization_id: string;
  title: string;
  description: string | null;
  priority_level: "low" | "medium" | "high";
  status: "draft" | "planned" | "in_progress" | "completed" | "carried_over";
  week_start: string;
  created_at: string;
  updated_at: string;
  tasks: TaskResponse[];
}

export interface TaskResponse {
  id: string;
  priority_id: string;
  title: string;
  description: string | null;
  status: "pending" | "in_progress" | "completed" | "cancelled";
  created_at: string;
  updated_at: string;
}

export function createPriority(data: CreatePriorityValues): Promise<PriorityResponse> {
  return apiPost<PriorityResponse>("/api/v1/priorities", data);
}

export function createTask(priorityId: string, data: CreateTaskValues): Promise<TaskResponse> {
  return apiPost<TaskResponse>(`/api/v1/priorities/${priorityId}/tasks`, data);
}
