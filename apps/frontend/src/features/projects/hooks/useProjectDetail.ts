"use client";

import { useQuery } from "@tanstack/react-query";
import { getProjectDetail } from "../services/project-service";

export function useProjectDetail(id: string) {
  return useQuery({
    queryKey: ["projects", id],
    queryFn: () => getProjectDetail(id),
    enabled: !!id,
  });
}
