import { apiGet } from "@/lib/api-client";

export interface WeeklyBreakdownItem {
  week_start: string;
  committed: number;
  completed: number;
  carried_over: number;
  crs: number | null;
}

export interface IndividualReportResponse {
  employee: { id: string; first_name: string; last_name: string };
  period_weeks: number;
  total_priorities: number;
  completed_priorities: number;
  completion_rate: number;
  carried_over_count: number;
  crs_current: number | null;
  crs_trend: string | null;
  weekly_breakdown: WeeklyBreakdownItem[];
}

export interface TeamMemberSummary {
  id: string;
  first_name: string;
  last_name: string;
  completion_rate: number;
  crs: number | null;
  trend: string | null;
}

export interface TeamWeeklyBreakdownItem {
  week_start: string;
  checkins_submitted: number;
  checkouts_submitted: number;
  avg_completion: number;
}

export interface TeamReportResponse {
  team_size: number;
  period_weeks: number;
  avg_completion_rate: number;
  avg_crs: number | null;
  members: TeamMemberSummary[];
  weekly_breakdown: TeamWeeklyBreakdownItem[];
}

export interface PhaseSummary {
  id: string;
  name: string;
  total_priorities: number;
  completed_priorities: number;
  completion_rate: number;
}

export interface ProjectReportResponse {
  project: { id: string; name: string; status: string };
  period_weeks: number;
  total_priorities: number;
  completed_priorities: number;
  completion_rate: number;
  phases: PhaseSummary[];
}

export function getIndividualReport(weeks = 8): Promise<IndividualReportResponse> {
  return apiGet<IndividualReportResponse>(`/api/v1/reports/individual?weeks=${weeks}`);
}

export function getTeamReport(weeks = 8): Promise<TeamReportResponse> {
  return apiGet<TeamReportResponse>(`/api/v1/reports/team?weeks=${weeks}`);
}

export function getProjectReport(projectId: string, weeks = 8): Promise<ProjectReportResponse> {
  return apiGet<ProjectReportResponse>(`/api/v1/reports/project/${projectId}?weeks=${weeks}`);
}
