"use client";

import { useMutation } from "@tanstack/react-query";
import { generateTeamSummary } from "../services/ai-service";

export function useTeamSummary() {
  return useMutation({
    mutationFn: (regenerate: boolean = false) => generateTeamSummary(regenerate),
  });
}
