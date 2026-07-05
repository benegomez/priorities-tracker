"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createPriority } from "../services/priority-service";
import type { CreatePriorityValues } from "../schemas/priority-schema";

export function useCreatePriority(checkinId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreatePriorityValues) => createPriority(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["checkins", "current"] });
      queryClient.invalidateQueries({ queryKey: ["checkins", checkinId, "priorities"] });
    },
  });
}
