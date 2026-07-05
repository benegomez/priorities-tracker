"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createTask } from "../services/priority-service";
import type { CreateTaskValues } from "../schemas/task-schema";

export function useCreateTask(checkinId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ priorityId, data }: { priorityId: string; data: CreateTaskValues }) =>
      createTask(priorityId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["checkins", "current"] });
      queryClient.invalidateQueries({ queryKey: ["checkins", checkinId, "priorities"] });
    },
  });
}
