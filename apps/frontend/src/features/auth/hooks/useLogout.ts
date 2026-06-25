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
      router.push("/auth/login");
    },
  });
}
