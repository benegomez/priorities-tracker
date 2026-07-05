"use client";

import { useMutation } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { logout } from "../services/auth-service";
import { useAuthStore } from "@/store/auth-store";

export function useLogout() {
  const router = useRouter();
  const { accessToken, refreshToken, clearUser } = useAuthStore();

  return useMutation({
    mutationFn: async () => {
      if (accessToken && refreshToken) {
        await logout(accessToken, refreshToken);
      }
    },
    onSettled: () => {
      clearUser();
      // Clear cookies used by Next.js middleware
      document.cookie = "access_token=; path=/; max-age=0";
      document.cookie = "user_role=; path=/; max-age=0";
      router.push("/auth/login");
    },
  });
}
