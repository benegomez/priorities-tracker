"use client";

import { useQuery } from "@tanstack/react-query";
import { getAvailablePhases } from "@/features/projects/services/project-service";

export function useAvailablePhases() {
  return useQuery({
    queryKey: ["projects", "phases", "available"],
    queryFn: getAvailablePhases,
  });
}
