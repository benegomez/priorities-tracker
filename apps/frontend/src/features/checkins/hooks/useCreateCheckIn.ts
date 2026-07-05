"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createCheckIn } from "../services/checkin-service";

export function useCreateCheckIn() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (weekStart: string) => createCheckIn(weekStart),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["checkins", "current"] });
    },
  });
}
