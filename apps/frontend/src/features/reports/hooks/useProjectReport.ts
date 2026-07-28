"use client";

import { useQuery } from "@tanstack/react-query";
import { getProjectReport } from "../services/report-service";

export function useProjectReport(projectId: string, weeks = 8) {
  return useQuery({
    queryKey: ["reports", "project", projectId, weeks],
    queryFn: () => getProjectReport(projectId, weeks),
    enabled: !!projectId,
  });
}
