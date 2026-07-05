"use client";

import { useQuery } from "@tanstack/react-query";
import { getCurrentCRS } from "../services/crs-service";
import type { ApiError } from "@/lib/api-client";

export function useCurrentCRS() {
  return useQuery({
    queryKey: ["crs", "current"],
    queryFn: getCurrentCRS,
    retry: (failureCount, error: unknown) => {
      if ((error as ApiError).status === 404) return false;
      return failureCount < 2;
    },
  });
}
