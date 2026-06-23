import { create } from "zustand";

export type UserRole = "administrator" | "manager" | "employee";

export interface AuthUser {
  id: string;
  email: string;
  role: UserRole;
  organization_id: string;
  full_name: string;
}

interface AuthStore {
  user: AuthUser | null;
  accessToken: string | null;
  refreshToken: string | null;
  setUser: (user: AuthUser) => void;
  setTokens: (accessToken: string, refreshToken: string) => void;
  clearUser: () => void;
}

export const useAuthStore = create<AuthStore>((set) => ({
  user: null,
  accessToken: null,
  refreshToken: null,
  setUser: (user) => set({ user }),
  setTokens: (accessToken, refreshToken) => set({ accessToken, refreshToken }),
  clearUser: () => set({ user: null, accessToken: null, refreshToken: null }),
}));
