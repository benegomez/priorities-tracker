"use client";

import { useQuery } from "@tanstack/react-query";
import { getCRSHistory } from "../services/crs-service";

export function useCRSHistory(weeks = 8) {
  return useQuery({
    queryKey: ["crs", "history", weeks],
    queryFn: () => getCRSHistory(weeks),
  });
}
