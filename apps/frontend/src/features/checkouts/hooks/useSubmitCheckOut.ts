"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { submitCheckOut } from "../services/checkout-service";

export function useSubmitCheckOut() {
  const queryClient = useQueryClient();
  const router = useRouter();

  return useMutation({
    mutationFn: ({ id, notes, lessonsLearned }: { id: string; notes?: string; lessonsLearned?: string }) =>
      submitCheckOut(id, { notes: notes || null, lessons_learned: lessonsLearned || null }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["checkouts", "current"] });
      router.push("/employee/dashboard");
    },
  });
}
