import { z } from "zod";

export const createTaskSchema = z.object({
  title: z.string().min(1, "El título es requerido").max(255),
  description: z.string().max(500).nullable().optional(),
});

export type CreateTaskValues = z.infer<typeof createTaskSchema>;
