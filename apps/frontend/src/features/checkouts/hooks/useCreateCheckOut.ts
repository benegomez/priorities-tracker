"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createCheckOut } from "../services/checkout-service";

export function useCreateCheckOut() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (checkinId: string) => createCheckOut(checkinId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["checkouts", "current"] });
    },
  });
}
