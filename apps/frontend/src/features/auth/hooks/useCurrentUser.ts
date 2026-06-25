"use client";

import { useQuery } from "@tanstack/react-query";
import { getMe } from "../services/auth-service";
import { useAuthStore } from "@/store/auth-store";

export function useCurrentUser() {
  const { accessToken, setUser, clearUser } = useAuthStore();

  return useQuery({
    queryKey: ["auth", "me"],
    queryFn: async () => {
      if (!accessToken) throw new Error("No token");
      const user = await getMe(accessToken);
      setUser(user);
      return user;
    },
    enabled: !!accessToken,
    retry: false,
  });
}
