"use client";

import { useQuery } from "@tanstack/react-query";
import { getCurrentCheckIn } from "../services/checkin-service";
import type { ApiError } from "@/lib/api-client";

export function useCurrentCheckIn() {
  return useQuery({
    queryKey: ["checkins", "current"],
    queryFn: getCurrentCheckIn,
    retry: (failureCount, error: unknown) => {
      if ((error as ApiError).status === 404) return false;
      return failureCount < 2;
    },
  });
}
