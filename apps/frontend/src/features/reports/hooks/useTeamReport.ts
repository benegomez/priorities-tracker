"use client";

import { useQuery } from "@tanstack/react-query";
import { getTeamReport } from "../services/report-service";

export function useTeamReport(weeks = 8) {
  return useQuery({
    queryKey: ["reports", "team", weeks],
    queryFn: () => getTeamReport(weeks),
  });
}
