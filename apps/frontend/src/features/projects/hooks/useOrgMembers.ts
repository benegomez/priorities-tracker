"use client";

import { useQuery } from "@tanstack/react-query";
import { apiGet } from "@/lib/api-client";

export interface OrgMember {
  id: string;
  full_name: string;
  role: string;
  email: string;
}

export function useOrgMembers() {
  return useQuery({
    queryKey: ["users", "org-members"],
    queryFn: () => apiGet<OrgMember[]>("/api/v1/projects/org-members"),
  });
}
