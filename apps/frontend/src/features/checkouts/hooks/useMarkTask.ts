"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { markTaskCompleted } from "../services/checkout-service";

export function useMarkTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ checkoutId, taskId, completed }: { checkoutId: string; taskId: string; completed: boolean }) =>
      markTaskCompleted(checkoutId, taskId, completed),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["checkouts", "current"] });
    },
  });
}
