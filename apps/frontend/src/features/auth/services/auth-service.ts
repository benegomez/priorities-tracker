import type { LoginFormValues } from "../schemas/login-schema";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "";

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface RefreshResponse {
  access_token: string;
  expires_in: number;
}

export interface MeResponse {
  id: string;
  email: string;
  role: "administrator" | "manager" | "employee";
  organization_id: string;
  full_name: string;
}

export interface AuthError {
  status: number;
  detail: string;
  retryAfter?: number;
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    const error: AuthError = {
      status: response.status,
      detail: body.detail ?? "Error desconocido",
      retryAfter: response.headers.get("Retry-After")
        ? Number(response.headers.get("Retry-After"))
        : undefined,
    };
    throw error;
  }
  return response.json() as Promise<T>;
}

export async function login(data: LoginFormValues): Promise<LoginResponse> {
  const response = await fetch(`${API_URL}/api/v1/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return handleResponse<LoginResponse>(response);
}

export async function logout(accessToken: string, refreshToken: string): Promise<void> {
  await fetch(`${API_URL}/api/v1/auth/logout`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${accessToken}`,
    },
    body: JSON.stringify({ refresh_token: refreshToken }),
  });
}

export async function refreshToken(token: string): Promise<RefreshResponse> {
  const response = await fetch(`${API_URL}/api/v1/auth/refresh`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh_token: token }),
  });
  return handleResponse<RefreshResponse>(response);
}

export async function getMe(accessToken: string): Promise<MeResponse> {
  const response = await fetch(`${API_URL}/api/v1/auth/me`, {
    headers: { Authorization: `Bearer ${accessToken}` },
  });
  return handleResponse<MeResponse>(response);
}
