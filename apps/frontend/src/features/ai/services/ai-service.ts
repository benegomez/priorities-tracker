import { apiPost } from "@/lib/api-client";

export interface DataSnapshot {
  team_size: number;
  week_start: string;
  avg_crs: number;
  total_priorities: number;
  completed_priorities: number;
  completion_rate: number;
}

export interface TeamSummaryResponse {
  summary: string;
  generated_at: string;
  model: string | null;
  data_snapshot: DataSnapshot;
  fallback: boolean;
  cached: boolean;
}

export function generateTeamSummary(regenerate = false): Promise<TeamSummaryResponse> {
  return apiPost<TeamSummaryResponse>("/api/v1/ai/team-summary", { regenerate });
}
