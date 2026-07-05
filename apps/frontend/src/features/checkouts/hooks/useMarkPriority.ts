"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { markPriorityCompleted } from "../services/checkout-service";

export function useMarkPriority() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ checkoutId, priorityId, completed }: { checkoutId: string; priorityId: string; completed: boolean }) =>
      markPriorityCompleted(checkoutId, priorityId, completed),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["checkouts", "current"] });
    },
  });
}
