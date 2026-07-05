"use client";

import { useQuery } from "@tanstack/react-query";
import { getProjects } from "../services/project-service";

export function useProjects(page = 1, status?: string) {
  return useQuery({
    queryKey: ["projects", { page, status }],
    queryFn: () => getProjects(page, status),
  });
}
