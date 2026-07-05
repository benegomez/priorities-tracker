import { apiGet, apiPost, apiPatch, apiDelete } from "@/lib/api-client";

export interface OwnerInfo {
  id: string;
  full_name: string;
}

export interface PhaseResponse {
  id: string;
  name: string;
  status: string;
}

export interface MemberResponse {
  user_id: string;
  full_name: string;
  role: string;
}

export interface ProjectListItem {
  id: string;
  name: string;
  description: string | null;
  status: string;
  owner: OwnerInfo | null;
  phases_count: number;
  members_count: number;
  created_at: string;
}

export interface ProjectListResponse {
  items: ProjectListItem[];
  total: number;
  page: number;
  page_size: number;
}

export interface ProjectDetailResponse {
  id: string;
  name: string;
  description: string | null;
  status: string;
  owner: OwnerInfo | null;
  phases: PhaseResponse[];
  members: MemberResponse[];
  created_at: string;
  updated_at: string;
}

export interface AvailablePhaseItem {
  id: string;
  name: string;
  project_name: string;
}

export function getProjects(page = 1, status?: string): Promise<ProjectListResponse> {
  const params = new URLSearchParams({ page: String(page) });
  if (status) params.set("status", status);
  return apiGet<ProjectListResponse>(`/api/v1/projects?${params}`);
}

export function getProjectDetail(id: string): Promise<ProjectDetailResponse> {
  return apiGet<ProjectDetailResponse>(`/api/v1/projects/${id}`);
}

export function createProject(data: { name: string; description?: string; owner_id: string }): Promise<ProjectDetailResponse> {
  return apiPost<ProjectDetailResponse>("/api/v1/projects", data);
}

export function updateProject(id: string, data: { name?: string; description?: string; owner_id?: string; status?: string }): Promise<ProjectDetailResponse> {
  return apiPatch<ProjectDetailResponse>(`/api/v1/projects/${id}`, data);
}

export function createPhase(projectId: string, name: string): Promise<PhaseResponse> {
  return apiPost<PhaseResponse>(`/api/v1/projects/${projectId}/phases`, { name });
}

export function updatePhase(projectId: string, phaseId: string, data: { name?: string; status?: string }): Promise<PhaseResponse> {
  return apiPatch<PhaseResponse>(`/api/v1/projects/${projectId}/phases/${phaseId}`, data);
}

export function addMember(projectId: string, userId: string): Promise<MemberResponse> {
  return apiPost<MemberResponse>(`/api/v1/projects/${projectId}/members`, { user_id: userId });
}

export function removeMember(projectId: string, userId: string): Promise<void> {
  return apiDelete(`/api/v1/projects/${projectId}/members/${userId}`);
}

export function getAvailablePhases(): Promise<AvailablePhaseItem[]> {
  return apiGet<AvailablePhaseItem[]>("/api/v1/projects/phases/available");
}
