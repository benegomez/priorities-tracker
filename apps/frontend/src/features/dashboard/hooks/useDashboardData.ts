"use client";

import { useQueries } from "@tanstack/react-query";
import { getCurrentCheckIn } from "@/features/checkins/services/checkin-service";
import { getCurrentCRS, getCRSHistory } from "@/features/crs/services/crs-service";
import type { ApiError } from "@/lib/api-client";

const no404Retry = (failureCount: number, error: unknown) => {
  if ((error as ApiError).status === 404) return false;
  return failureCount < 2;
};

export function useDashboardData() {
  const [checkIn, crs, history] = useQueries({
    queries: [
      { queryKey: ["checkins", "current"], queryFn: getCurrentCheckIn, retry: no404Retry },
      { queryKey: ["crs", "current"], queryFn: getCurrentCRS, retry: no404Retry },
      { queryKey: ["crs", "history", 8], queryFn: () => getCRSHistory(8), retry: no404Retry },
    ],
  });
  return { checkIn, crs, history };
}
