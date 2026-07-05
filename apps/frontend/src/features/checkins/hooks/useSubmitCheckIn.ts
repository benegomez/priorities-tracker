"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { submitCheckIn } from "../services/checkin-service";

export function useSubmitCheckIn() {
  const queryClient = useQueryClient();
  const router = useRouter();

  return useMutation({
    mutationFn: (id: string) => submitCheckIn(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["checkins", "current"] });
      router.push("/employee/dashboard");
    },
  });
}
