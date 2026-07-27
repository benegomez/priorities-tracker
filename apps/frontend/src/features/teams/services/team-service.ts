import { apiDelete, apiGet, apiPatch, apiPost } from "@/lib/api-client";

export interface TeamMemberCRS {
  score: number;
  trend: "improving" | "stable" | "declining";
  risk_level: "low" | "moderate" | "high";
}

export interface TeamMemberWeekStatus {
  week_start: string;
  checkin_status: "draft" | "submitted" | null;
  checkout_status: "draft" | "submitted" | null;
}

export interface TeamMember {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  crs: TeamMemberCRS | null;
  week_status: TeamMemberWeekStatus;
}

export interface TeamOverviewResponse {
  members: TeamMember[];
}

export interface TeamMemberCRSCurrent {
  score: number;
  trend: "improving" | "stable" | "declining";
  risk_level: "low" | "moderate" | "high";
  week_start: string;
}

export interface TeamMemberCRSHistoryItem {
  week_start: string;
  score: number;
  trend: "improving" | "stable" | "declining";
  risk_level: "low" | "moderate" | "high";
}

export interface TeamMemberCRSResponse {
  employee: { id: string; first_name: string; last_name: string };
  current: TeamMemberCRSCurrent | null;
  history: TeamMemberCRSHistoryItem[];
}

export interface CheckInPriority {
  id: string;
  title: string;
  description: string | null;
  priority_level: string;
  status: string;
  phase_name: string | null;
  project_name: string | null;
  tasks: Array<{ id: string; title: string; status: string }>;
}

export interface TeamMemberCheckInResponse {
  id: string;
  employee_id: string;
  week_start: string;
  status: string;
  submitted_at: string | null;
  priorities_count: number;
  priorities: CheckInPriority[];
}

// ── Admin types ──────────────────────────────────────────────────────────────

export interface AdminTeamMemberItem {
  id: string;
  first_name: string;
  last_name: string;
  role: string;
  status: string;
}

export interface AdminTeamResponse {
  id: string;
  name: string;
  manager_id: string | null;
  manager_name: string | null;
  member_count: number;
  created_at: string;
  updated_at: string;
}

export interface AdminTeamDetailResponse extends AdminTeamResponse {
  members: AdminTeamMemberItem[];
}

export interface AdminTeamListResponse {
  items: AdminTeamResponse[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}

export interface TeamCreate {
  name: string;
  manager_id?: string;
}

export interface TeamUpdate {
  name?: string;
  manager_id?: string | null;
}

// ── Admin service functions ───────────────────────────────────────────────────

export const teamAdminService = {
  list: (params?: { page?: number }) => {
    const qs = new URLSearchParams();
    if (params?.page) qs.set("page", String(params.page));
    const query = qs.toString();
    return apiGet<AdminTeamListResponse>(`/api/v1/teams${query ? `?${query}` : ""}`);
  },
  create: (data: TeamCreate) => apiPost<AdminTeamResponse>("/api/v1/teams", data),
  getDetail: (id: string) => apiGet<AdminTeamDetailResponse>(`/api/v1/teams/${id}`),
  update: (id: string, data: TeamUpdate) => apiPatch<AdminTeamResponse>(`/api/v1/teams/${id}`, data),
  addMember: (teamId: string, userId: string) =>
    apiPost(`/api/v1/teams/${teamId}/members`, { user_id: userId }),
  removeMember: (teamId: string, userId: string) =>
    apiDelete(`/api/v1/teams/${teamId}/members/${userId}`),
};

// ── Manager service functions ─────────────────────────────────────────────────

export function getMyTeam(): Promise<TeamOverviewResponse> {
  return apiGet<TeamOverviewResponse>("/api/v1/teams/my-team");
}

export function getTeamMemberCRS(employeeId: string, weeks = 8): Promise<TeamMemberCRSResponse> {
  return apiGet<TeamMemberCRSResponse>(`/api/v1/teams/my-team/${employeeId}/crs?weeks=${weeks}`);
}

export function getTeamMemberCheckIn(employeeId: string): Promise<TeamMemberCheckInResponse> {
  return apiGet<TeamMemberCheckInResponse>(`/api/v1/teams/my-team/${employeeId}/checkin`);
}
