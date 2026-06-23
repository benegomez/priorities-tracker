import { describe, it, expect } from "vitest";
import { loginSchema } from "@/features/auth/schemas/login-schema";

describe("loginSchema", () => {
  it("rejects invalid email", () => {
    const result = loginSchema.safeParse({ email: "not-an-email", password: "123" });
    expect(result.success).toBe(false);
    if (!result.success) {
      expect(result.error.issues[0].message).toBe("Email inválido");
    }
  });

  it("rejects empty password", () => {
    const result = loginSchema.safeParse({ email: "valid@email.com", password: "" });
    expect(result.success).toBe(false);
    if (!result.success) {
      expect(result.error.issues[0].message).toBe("La contraseña es requerida");
    }
  });

  it("accepts valid input", () => {
    const result = loginSchema.safeParse({ email: "user@company.com", password: "Secret123!" });
    expect(result.success).toBe(true);
  });

  it("rejects missing email", () => {
    const result = loginSchema.safeParse({ password: "Secret123!" });
    expect(result.success).toBe(false);
  });

  it("rejects missing password", () => {
    const result = loginSchema.safeParse({ email: "user@company.com" });
    expect(result.success).toBe(false);
  });
});
