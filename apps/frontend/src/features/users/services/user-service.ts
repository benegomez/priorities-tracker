import { apiGet, apiPatch, apiPost } from "@/lib/api-client";

export interface UserResponse {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: "administrator" | "manager" | "employee";
  status: "active" | "inactive";
  manager_id: string | null;
  manager_name: string | null;
  created_at: string | null;
  updated_at: string | null;
}

export interface UserCreatedResponse extends UserResponse {
  temporary_password: string;
}

export interface UserListResponse {
  items: UserResponse[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}

export interface UserCreate {
  email: string;
  first_name: string;
  last_name: string;
  role: string;
  manager_id?: string;
}

export interface UserUpdate {
  first_name?: string;
  last_name?: string;
  role?: string;
  manager_id?: string;
  new_password?: string;
}

export const userService = {
  list: (params?: { page?: number; role?: string; status?: string }) => {
    const qs = new URLSearchParams();
    if (params?.page) qs.set("page", String(params.page));
    if (params?.role) qs.set("role", params.role);
    if (params?.status) qs.set("status", params.status);
    const query = qs.toString();
    return apiGet<UserListResponse>(`/api/v1/users${query ? `?${query}` : ""}`);
  },
  create: (data: UserCreate) => apiPost<UserCreatedResponse>("/api/v1/users", data),
  getById: (id: string) => apiGet<UserResponse>(`/api/v1/users/${id}`),
  update: (id: string, data: UserUpdate) => apiPatch<UserResponse>(`/api/v1/users/${id}`, data),
  updateStatus: (id: string, status: "active" | "inactive") =>
    apiPatch<{ id: string; status: string }>(`/api/v1/users/${id}/status`, { status }),
};
