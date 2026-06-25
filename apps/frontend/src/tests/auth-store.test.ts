import { describe, it, expect, beforeEach } from "vitest";
import { useAuthStore } from "@/store/auth-store";

describe("auth-store", () => {
  beforeEach(() => {
    useAuthStore.getState().clearUser();
  });

  it("starts with null user", () => {
    expect(useAuthStore.getState().user).toBeNull();
    expect(useAuthStore.getState().accessToken).toBeNull();
  });

  it("setUser updates user state", () => {
    const user = {
      id: "123",
      email: "test@test.com",
      role: "employee" as const,
      organization_id: "org-1",
      full_name: "Test User",
    };
    useAuthStore.getState().setUser(user);
    expect(useAuthStore.getState().user).toEqual(user);
  });

  it("setTokens updates token state", () => {
    useAuthStore.getState().setTokens("access-123", "refresh-456");
    expect(useAuthStore.getState().accessToken).toBe("access-123");
    expect(useAuthStore.getState().refreshToken).toBe("refresh-456");
  });

  it("clearUser resets all state", () => {
    useAuthStore.getState().setUser({
      id: "123",
      email: "test@test.com",
      role: "employee",
      organization_id: "org-1",
      full_name: "Test User",
    });
    useAuthStore.getState().setTokens("at", "rt");

    useAuthStore.getState().clearUser();

    expect(useAuthStore.getState().user).toBeNull();
    expect(useAuthStore.getState().accessToken).toBeNull();
    expect(useAuthStore.getState().refreshToken).toBeNull();
  });
});
