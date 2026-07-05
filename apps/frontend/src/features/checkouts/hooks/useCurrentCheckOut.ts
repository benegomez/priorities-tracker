"use client";

import { useQuery } from "@tanstack/react-query";
import { getCurrentCheckOut } from "../services/checkout-service";
import type { ApiError } from "@/lib/api-client";

export function useCurrentCheckOut() {
  return useQuery({
    queryKey: ["checkouts", "current"],
    queryFn: getCurrentCheckOut,
    retry: (failureCount, error: unknown) => {
      if ((error as ApiError).status === 404) return false;
      return failureCount < 2;
    },
  });
}
