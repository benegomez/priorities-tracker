"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { submitCheckIn } from "../services/checkin-service";

export function useResubmitCheckIn() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) => submitCheckIn(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["checkins", "current"] });
    },
  });
}
