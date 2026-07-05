"use client";

import { useMutation } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { login, getMe, type AuthError } from "../services/auth-service";
import { useAuthStore } from "@/store/auth-store";
import type { LoginFormValues } from "../schemas/login-schema";

export function useLogin() {
  const router = useRouter();
  const { setUser, setTokens } = useAuthStore();

  return useMutation({
    mutationFn: async (data: LoginFormValues) => {
      const tokens = await login(data);
      const user = await getMe(tokens.access_token);
      return { tokens, user };
    },
    onSuccess: ({ tokens, user }) => {
      setTokens(tokens.access_token, tokens.refresh_token);
      setUser(user);

      // Set cookies for Next.js middleware (route protection)
      document.cookie = `access_token=${tokens.access_token}; path=/; max-age=${tokens.expires_in}`;
      document.cookie = `user_role=${user.role}; path=/; max-age=${tokens.expires_in}`;

      const redirectMap = {
        employee: "/employee/dashboard",
        manager: "/manager/dashboard",
        administrator: "/admin/dashboard",
      } as const;

      router.push(redirectMap[user.role]);
    },
  });
}
